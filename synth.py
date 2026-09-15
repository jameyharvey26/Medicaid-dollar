"""synth.py — synthetic jurisdiction fixtures. WORKING FILE, not for commit.

Two variants of the same made-up jurisdiction:

  python3 synth.py none    no managed care at all. Exercises absent-lane
                           collapse: the lanes must disappear entirely.
  python3 synth.py thin    a $1.00 MCO lane and a $1.00 dual lane. Exercises
                           the peels at legible width: administration and
                           margin come off lanes small enough to watch.

Numbers are invented. Nothing here is a state and nothing here is published.
"""
import sys

import sankey, build
from ledger import Fig, Ledger, MEASURED, Matrix, Payer, Peel
from compose import compose
from view import View

N = ["Long-term care", "Hospitals", "Physicians & clinics",
     "Wrap around services", "Rx drugs"]
SRC = dict(source="synthetic", vintage="n/a", basis="test fixture",
           status=MEASURED)


def m(v, note=""):
    return Fig(v, note=note, **SRC)


def build_ledger(variant="none"):
    thin = variant == "thin"

    mco_cap = 1.00 if thin else 0.0
    dual_cap = 1.00 if thin else 0.0
    ffs = 95.0 - mco_cap - dual_cap

    mco_adm, mco_marg = (0.20, 0.05) if thin else (0.0, 0.0)
    dual_adm, dual_marg = (0.10, 0.00) if thin else (0.0, 0.0)
    mco_care = mco_cap - mco_adm - mco_marg
    dual_care = dual_cap - dual_adm - dual_marg

    ffs_n = {"Long-term care": 30.0, "Hospitals": 25.0,
             "Physicians & clinics": 20.0, "Wrap around services": 13.0,
             "Rx drugs": 5.0}
    ffs_n["Wrap around services"] += ffs - sum(ffs_n.values())

    if thin:
        mco_n = {"Long-term care": 0.20, "Hospitals": 0.20,
                 "Physicians & clinics": 0.20, "Wrap around services": 0.10,
                 "Rx drugs": 0.05}
        dual_n = {"Long-term care": 0.60, "Hospitals": 0.0,
                  "Physicians & clinics": 0.0, "Wrap around services": 0.30,
                  "Rx drugs": 0.0}
    else:
        mco_n = {k: 0.0 for k in N}
        dual_n = {k: 0.0 for k in N}

    col = {k: ffs_n[k] + mco_n[k] + dual_n[k] for k in N}
    note = "small but real" if thin else "no managed care in this jurisdiction"

    return Ledger(
        geography="Testland", year="FY2024", scenario="as_is", scale=m(1.0),
        sources={"federal": m(60.0), "state": m(40.0)},
        peels=[Peel("admin", "Administration", m(4.0), "STATE_AGENCY",
                    reach="STATE_AGENCY"),
               Peel("medicare", "Medicare premiums", m(1.0), "STATE_AGENCY",
                    reach="STATE_AGENCY", kind="return")],
        payers=[
            Payer("mco", "MCO capitation", "mco",
                  capitation=m(mco_cap, note), care=m(mco_care),
                  admin=m(mco_adm), margin=m(mco_marg)),
            Payer("dual", "Dual MCO capitation", "dual",
                  capitation=m(dual_cap, note), care=m(dual_care),
                  admin=m(dual_adm), margin=m(dual_marg)),
            Payer("ffs", "Fee-for-service", "ffs",
                  capitation=m(ffs), care=m(ffs),
                  admin=Fig.absent("no plan administration"),
                  margin=Fig.absent("no margin")),
        ],
        nodes=N,
        claims=Matrix("claims", rows=["mco", "dual", "ffs"], cols=N,
                      row_margin={"mco": m(mco_care), "dual": m(dual_care),
                                  "ffs": m(ffs)},
                      col_margin={k: m(v) for k, v in col.items()},
                      cell={**{("ffs", k): m(v) for k, v in ffs_n.items()},
                            **{("mco", k): m(v) for k, v in mco_n.items()},
                            **{("dual", k): m(v) for k, v in dual_n.items()}}),
        declared=["mco", "dual", "ffs"],
        declarations=([] if thin else
                      ["Managed care: this jurisdiction has none. The lane is "
                       "absent, not empty.",
                       "Capitated dual plan: none."]),
    )


def view(variant):
    subs = [("administration + Medicare premiums", "adm_med", "admin",
             "STATE_AGENCY", "State Admin")]
    if variant == "thin":
        subs.append(("plan administration + earnings", "plan", "admin",
                     "PAYER", "MCO Admin"))
    return View(
        cp0_label=["$100 Testland", "Dollars"],
        centre=("100 Dollars of", "Testland Medicaid Spending"),
        step_x={"admin": 615, "medicare": 715},
        subs_spec=subs,
        show_beneficiaries=False,
        kicker="TEST  \u00b7  " + ("THIN CAPITATED LANES" if variant == "thin"
                                   else "FEE-FOR-SERVICE ONLY"),
        title=("Thin lanes: $1.00 of MCO capitation and $1.00 of dual capitation"
               if variant == "thin" else
               "Absent-lane collapse: a jurisdiction with no managed care"),
        strap="SYNTHETIC. Invented numbers, built to exercise the renderer.",
    )


if __name__ == "__main__":
    import ledger as LD
    v = sys.argv[1] if len(sys.argv) > 1 else "none"
    L = build_ledger(v)
    LD.gate(L, f"synthetic [{v}]")
    cfg = compose(L, view(v))
    print("collapsed lanes:", cfg.collapsed or "(none)")
    base, over = sankey.render(cfg)
    build.emit(f"synth_{v}", base, over)
