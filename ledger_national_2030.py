# ledger_national_2030.py — the national to-be, in the Ledger shape.
#
# Same numbers as instances.to_be_2030(ledger_2030.ledger(variant), per100).
# Nothing is revalued here. `ledger_2030.ledger()` still does the arithmetic;
# this module wraps its output in Fig and Peel so the FY2030 panel runs through
# the same Ledger + View + compose path as the two as-is panels, and so its
# register generates rather than being maintained.
#
# THE SPLIT, which is the whole difficulty of this artifact.
#
# An HR-1 tributary carries two different kinds of fact and they were sitting in
# one place. This module takes only the first kind.
#
#   Ledger   how much leaves (`amount`), which phase it is charged to
#            (`charged`), and how far down the lifecycle the dollar would have
#            got had it not left (`reach`). All three are claims about the
#            world. S-085.
#   View     the terminal's sub-label, and the order the tributaries are
#            declared in. Presentation.
#   Layout   `src_x`, `term_col`, `label_dy`, and the fan's row packing. Stays
#            in `outflows.py`, untouched.
#
# `reach` is currently declared twice: here, and in `outflows.OUTFLOWS`, which
# `outflows.terminal_x` reads at line 521. That is one fact with two
# declarations, which is the S-073 failure mode with a phase name instead of a
# dollar. Retiring the `outflows` copy is a Layout change and is not taken in
# the same session as the seam, so `agreement()` below asserts the two match
# and the build fails if they ever drift.
#
# Every figure on this panel is MODELLED. The two sourced anchors sit one level
# up, in `tobe2030.py`: CBO's October 2025 supplemental for the numerator and
# the March 2025 letter at January 2025 vintage for the denominator. What this
# ledger holds is those two anchors put through a ramp, a gross-up and a set of
# bite phases, and none of that is published by anybody.

from dataclasses import replace

from ledger import (DERIVED, Fig, Ledger, MODELLED, Matrix, Payer, Peel)
from ledger_national_2024 import (RESCALE, PER_DOLLAR, VFC_M, FED_M, ST_M,
                                  HUNDRED_M, ADMIN_M, MFCU_M, SNC_M)

from ledger_2030 import ledger as _arith, B, B_ffs_n, B_mcoc_n, B_dualc_n, ORDER
from tobe2030 import per100, FY30_DEFICIT, FED_OUTLAYS_30, TOTAL_30

NODES = list(ORDER)

CBO = ("CBO Supplemental Cost Estimate, P.L. 119-21 Title VII Subtitle B Ch.1, "
       "28 Oct 2025, by fiscal year; denominator CBO letter to Boyle and "
       "Pallone, 5 Mar 2025, Table 1, January 2025 baseline vintage")

# Where each tributary is charged, and how far the dollar would have got. The
# first column is D-64. The second is S-085 and is the claim the terminal
# answers; it is not the same question as the first and the two disagree on
# four of the seven lanes, which is the point of carrying both.
HR1 = {
    #  key                                  charged          reach
    "Work reporting":                   ("STATE_AGENCY", "DISBURSE"),
    "Six-month renewals":               ("STATE_AGENCY", "PAYER"),
    "Blocked Medicaid enrollment rule": ("STATE_AGENCY", "CLAIMS"),
    "Everything else":                  ("STATE_AGENCY", "STATE_AGENCY"),
    "Blocked senior enrollment rule":   ("STATE_AGENCY", "BENEFICIARY"),
    "Provider tax limits":              ("FEDERAL",      "FEDERAL"),
    # Charged at the claims fan; the dollar would have reached a provider. The
    # terminal nonetheless rides the CLAIMS edge, because the tracker lattice
    # has no PROVIDERS edge to ride. That is a lattice fact and it belongs to
    # the View, not here. Writing CLAIMS in this column to make the two agree
    # would be moving geometry to settle an arithmetic question.
    "Directed payment caps":            ("CLAIMS",       "PROVIDERS"),
}
# Declaration order of the five state-agency levers. It is the order
# `outflows.OUTFLOWS` declares them in, which is source order, and the steps on
# the trunk are emitted in it (S-085). Changing it moves ribbons.
SA_ORDER = ["Work reporting", "Six-month renewals",
            "Blocked Medicaid enrollment rule", "Everything else",
            "Blocked senior enrollment rule"]

METHOD = ("Ten-year CBO score apportioned to FY2030 by the statutory ramp in "
          "phasein.py, grossed from federal to total-computable dollars in "
          "fmap.py, over a denominator of federal FY2030 outlays at the "
          "January 2025 vintage divided by the FY2024 blended federal share "
          "held constant (D-10, D-11).")


def _mod(v, note):
    return Fig(v, status=MODELLED, note=note)


def agreement():
    """`reach` is declared here and in `outflows.OUTFLOWS`. Assert they agree.

    One fact, two declarations, and the second one drives the terminal x. This
    does not fix the duplication; it makes the duplication unable to drift
    quietly, which is the part that bites. Returns a list of failures.
    """
    from outflows import OUTFLOWS
    out = []
    for name, (charged, reach) in HR1.items():
        o = OUTFLOWS.get(name)
        if o is None:
            out.append(f"{name}: in the ledger, not in OUTFLOWS")
            continue
        theirs = o.get("reach") or o["term_col"]
        if theirs != reach:
            out.append(f"{name}: ledger reach {reach}, outflows {theirs}")
    for name, o in OUTFLOWS.items():
        if o.get("cls") == "hr1" and name not in HR1:
            out.append(f"{name}: in OUTFLOWS, not in the ledger")
    return out


def build(variant: str = "mixed") -> Ledger:
    L = _arith(variant)

    # --- payers ----------------------------------------------------------
    # The two capitated lanes scale by the same ratio, because both are struck
    # as a fixed share of disbursed. So the earnings carve scales by that one
    # ratio too and the split across the lanes is unchanged.
    r = L["mco"] / B["mco"]
    scaled = (variant in ("scales", "mixed"))
    marg = ("Retention scales with capitation under the MLR floor (D-63). "
            "EN-43 carve, unchanged in proportion." if scaled
            else "Retention held at FY2024 dollars (D-63). EN-43 carve.")
    payers = [
        Payer("mco", "MCO capitation", "mco",
              capitation=_mod(L["mco"], METHOD),
              care=Fig.derived(L["mco_care"], ("payer.mco.capitation",
                                              "payer.mco.admin",
                                              "payer.mco.margin")),
              admin=_mod(L["mco_adm"], "Plan administration, " + marg),
              margin=_mod(L["earnings"] * 0.60 / 0.76, marg)),
        Payer("dual", "Dual MCO capitation", "dual",
              capitation=_mod(L["dual"], METHOD),
              care=Fig.derived(L["dual_care"], ("payer.dual.capitation",
                                               "payer.dual.admin",
                                               "payer.dual.margin")),
              admin=_mod(L["dual_adm"], "Dual plan administration, " + marg),
              margin=_mod(L["earnings"] * 0.16 / 0.76, marg)),
        Payer("ffs", "Fee-for-service", "ffs",
              capitation=_mod(L["ffs"], METHOD),
              care=_mod(L["ffs"], "Rule A: fee-for-service has no payer and no "
                                  "retention. It runs through the payer phase "
                                  "unchanged."),
              admin=Fig.absent("fee-for-service has no plan administration"),
              margin=Fig.absent("fee-for-service has no margin")),
    ]

    # --- claims ----------------------------------------------------------
    # Row margins are struck from the cells rather than from care, because the
    # directed-payment-cap bite lands inside the matrix on the capitated leg.
    # care less the claims-side peel is what they sum to, which is what the
    # gate asserts.
    cells = {}
    for row, src in (("mco", L["mcoc"]), ("dual", L["dualc"]), ("ffs", L["ffsn"])):
        for node in NODES:
            cells[(row, node)] = _mod(src[node], MIX_NOTE[row])
    row_margin = {row: Fig.derived(sum(src[n] for n in NODES),
                                   tuple(f"claims.cell.{row}.{n}" for n in NODES))
                  for row, src in (("mco", L["mcoc"]), ("dual", L["dualc"]),
                                   ("ffs", L["ffsn"]))}
    claims = Matrix(
        name="claims", rows=["mco", "dual", "ffs"], cols=NODES,
        row_margin=row_margin,
        col_margin={n: Fig.derived(
            L["node"][n],
            tuple(f"claims.cell.{r}.{n}" for r in ("mco", "dual", "ffs")))
            for n in NODES},
        cell=cells,
    )

    # --- beneficiaries ---------------------------------------------------
    # FY2024 group shares carried forward against the FY2030 provider total.
    # EN-47: the split is the FY2024 split times one multiplier, so every group
    # falls by the same proportion. That is the assumption, stated, and it is
    # why no per-beneficiary-class finding is drawn off it.
    tot = sum(L["node"].values())
    G24 = {"Children": 13.48, "Adults": 29.56, "Disabled": 24.98, "Aged": 18.41}
    ben = Matrix(
        name="beneficiaries", rows=list(G24), cols=NODES,
        row_margin={g: _mod(v * tot / 86.43,
                            "FY2024 eligibility-group share of provider spending "
                            "held constant and applied to the FY2030 total. "
                            "EN-47.")
                    for g, v in G24.items()},
        col_margin={n: Fig.derived(L["node"][n], (f"claims.col.{n}",))
                    for n in NODES},
        cell={},
        note="Interior unallocated, as on the FY2024 ledger.",
    )

    # --- peels -----------------------------------------------------------
    # Order matters: the trunk steps are emitted in peel order, and the five
    # state-agency levers have to come off in the order outflows declares them
    # or the fan packs differently.
    def hr1(name):
        charged, reach = HR1[name]
        return Peel(name, name, _mod(per100[name], METHOD), charged,
                    reach=reach, kind="hr1")

    # D-70/D-71/D-72, completed by D-83. This used to take the inherited FY2024
    # $5.07 overhead figure - administration plus federal oversight plus a
    # vaccine purchase, bundled - and split it three ways on FY2024
    # proportions. That was a patch, not the D-70 correction: the as-is panel
    # was re-derived from Exhibit 16 dollars while the to-be panel went on
    # carrying the pre-D-70 bundle and carving the vaccine back out of it. The
    # two panels were struck against different definitions of overhead, and
    # because the baseline was also typed on the old hundred the discrepancy
    # cancelled and nothing reported it.
    #
    # The vaccine purchase is now derived from Exhibit 16 dollars exactly as it
    # is on the as-is panel, so the same $0.76 leaves the federal column on both
    # and the pair is a comparison. CBO does not project VFC separately, so it
    # is held at FY2024 dollars (D-71), the convention already used for the
    # federal share (D-10, D-11). What is left splits two ways.
    _A = L["admin"]
    _OVERHEAD = ADMIN_M + MFCU_M + SNC_M
    _adm, _ovs = _A * ADMIN_M / _OVERHEAD, _A * (MFCU_M + SNC_M) / _OVERHEAD
    _vfc = VFC_M / PER_DOLLAR

    peels = [Peel("vfc", "Vaccines for Children",
                  _mod(_vfc, "Vaccines for Children, $7,239M, held at FY2024 "
                             "dollars to FY2030 (D-71, D-83). The same figure "
                             "the as-is panel peels. Before the blend, "
                             "terminates at CDC."),
                  "FEDERAL", reach="FEDERAL", kind="return", outside=True)]
    peels += [hr1(n) for n in SA_ORDER]
    peels += [
        Peel("admin", "Administration",
             _mod(_adm, "State programme administration only, held at FY2024 "
                        "dollars (D-63)." if variant in ("holds", "mixed")
                        else "State programme administration only, scaling with "
                             "the trunk (D-63)."),
             "STATE_AGENCY", reach="STATE_AGENCY", kind="admin"),
        Peel("oversight", "Federal oversight",
             _mod(_ovs, "EN-50. Fraud Control Units and survey and "
                        "certification, carried on the FY2024 proportion."),
             "STATE_AGENCY", reach="STATE_AGENCY", kind="admin"),
        Peel("medicare", "Medicare premiums",
             _mod(L["medicare"], "FY2024 Medicare premium lane less the blocked "
                                 "senior enrollment rule, which is charged "
                                 "separately above."),
             "STATE_AGENCY", reach="STATE_AGENCY", kind="return"),
        hr1("Provider tax limits"),
        hr1("Directed payment caps"),
        Peel("fraud", "Documented fraud",
             _mod(L["fraud"], "FY2024 documented fraud scaled with the "
                              "fee-for-service lane. Providers receive it; it "
                              "is not services delivered."),
             "PROVIDERS", reach="PROVIDERS", kind="fraud"),
    ]

    def _rebase(L):
        """D-70 moved the normalization point on the as-is panel. The to-be
        panel has to follow or the pair is not a comparison. Same factor, same
        reason: a change of units, not of measurement."""
        def r(f):
            return f if f.value is None else replace(f, value=f.value * RESCALE)
        for x in L.peels:
            if not x.outside:
                x.amount = r(x.amount)
        # Everything below the agency is scaled to the money that actually
        # arrives there, not by the raw factor. Scaling lanes by RESCALE would
        # scale the 100 as well and leave the vaccine amount unaccounted.
        disb, _ = L.disbursed()
        lanes = sum(pr.capitation.n for pr in L.lanes())
        g = disb / lanes
        def r2(f):
            return f if f.value is None else replace(f, value=f.value * g)
        for pr in L.payers:
            for fld in ("capitation", "care", "admin", "margin"):
                setattr(pr, fld, r2(getattr(pr, fld)))
        for m in [L.claims] + ([L.beneficiaries] if L.beneficiaries else []):
            for d in (m.row_margin, m.col_margin, m.cell):
                for k in list(d):
                    d[k] = r2(d[k])
        return L

    # ------------------------------------------------------------------
    # The federal source, derived backward from the hundred (D-76).
    #
    # D-70 strikes the hundred at the state agency. D-71 peels the Vaccines
    # for Children purchase off the federal column before the blend. So what
    # ENTERS the federal column is its share of the hundred plus that peel,
    # and the share of the hundred is whatever the state residual leaves.
    #
    # Deriving it forward instead, from FED_M — the FY2024 federal dollar
    # total — silently carries FY2024's vaccine purchase onto the FY2030
    # panel, because FED_M is sized to the FY2024 peel and the FY2030 peel is
    # smaller. The agency then holds more than the hundred. That was the state
    # of this file until 2026-09-19. `check` does not catch it: TOL is $0.02
    # and the gap is under a cent.
    #
    # _superseded and _agency_was are computed, not typed, so the basis line
    # cannot drift away from the code that produced it. They exist only to be
    # quoted in that line; nothing downstream reads them.
    # ------------------------------------------------------------------
    _state_share  = ST_M / (HUNDRED_M / 100.0)      # state share OF THE HUNDRED
    _fed_share    = 100.0 - _state_share            # federal share OF THE HUNDRED
    _fed_enters   = _fed_share + _vfc               # what enters the federal column
    _superseded   = FED_M / (HUNDRED_M / 100.0)     # the pre-D-76 derivation
    _agency_was   = _superseded + _state_share - _vfc

    _FED_BASIS = (
        "FY2024 federal appropriation share of the hundred held constant to "
        "FY2030 (D-10, D-11), plus the FY2030 Vaccines for Children purchase, "
        "which is wholly federal and peels before the blend (D-71). Derived "
        f"backward from the hundred: {_fed_share:.4f} of the hundred is "
        f"federal once the state residual of {_state_share:.4f} is taken, and "
        f"the {_vfc:.4f} vaccine peel is added on top, so {_fed_enters:.4f} "
        f"enters and {_fed_enters + _state_share - _vfc:.4f} is budgeted "
        "(D-70). Deriving it forward from the FY2024 federal dollar total "
        f"instead gives {_superseded:.4f}, which carries the FY2024 vaccine "
        f"purchase onto the FY2030 panel and leaves {_agency_was:.4f} at the "
        "agency. Corrected 2026-09-19, D-76.")

    return _rebase(Ledger(
        geography="United States", year="FY2030", scenario="to_be",
        scale=Fig(PER_DOLLAR, status=DERIVED,
                  basis="$M per $1 of the FY2030 hundred budgeted to Medicaid "
                        "under prior law"),
        sources={"federal": _mod(_fed_enters, _FED_BASIS),
                 "state": _mod(_state_share,
                               "Residual of the appropriation share.")},
        peels=peels, payers=payers, nodes=NODES, claims=claims,
        beneficiaries=ben,
        declarations=[],
        note=CBO,
    ))


MIX_NOTE = {
    "mco": "FY2024 managed-care service mix applied to the FY2030 capitated "
           "lane, less the directed-payment-cap bite on the three provider "
           "classes the statute names (EN-21).",
    "dual": "FY2024 dual-plan service mix, same basis.",
    "ffs": "FY2024 fee-for-service mix scaled with the fee-for-service lane.",
}


if __name__ == "__main__":
    import ledger as LD
    for v in ("holds", "scales", "mixed"):
        L = build(v)
        fails = LD.check(L)
        print(f"{v:8} {'CONSERVES' if not fails else 'FAILS'}   "
              f"{len(L.figures())} figures")
        for x in fails:
            print("    " + x)
    a = agreement()
    print("\nreach agreement with outflows: " + ("ok" if not a else "DRIFT"))
    for x in a:
        print("    " + x)
