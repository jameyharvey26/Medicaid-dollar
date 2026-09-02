# instances.py — one config per artifact.
#
# Replaces the text-substitution fork. `build_tobe_2030.py` used to read
# `build_sankey.py` as a string and run ~20 replacements on it before executing
# the result. Every replacement was a copy of a line from the master, so every
# change to the master silently broke or subtly altered one of them. That is the
# mechanism behind Medicare premiums, the tracker and documented fraud each
# drifting into two different treatments (S-062, S-063).
#
# Now: one renderer, many instances. A new state edition is a config, not a fork.

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from outflows import COLS, col_right

ORDER = ["Long-term care", "Hospitals", "Other", "Physicians & clinics",
         "Behavioral health", "Rx drugs"]


@dataclass
class Instance:
    name: str
    # ---- ledger, $ per $100 -------------------------------------------
    fed: float; state: float
    admin: float; medicare: float
    mco: float; dual: float; ffs: float
    mco_ret: float; dual_ret: float; earnings: float; adm_marg: float
    mco_adm: float; dual_adm: float
    mco_care: float; dual_care: float
    node: Dict[str, float]
    fraud: float
    ffs_n: Dict[str, float]
    mcoc_n: Dict[str, float]
    dualc_n: Dict[str, float]
    gt: Dict[str, float]
    # ---- trunk steps: (name, "top"|"bot", value, x) --------------------
    # Administration and Medicare premiums are pinned at 615 and 715 in every
    # instance. They are far enough apart that the Medicare return curve clears
    # the administration band; HR-1 steps interleave around them and must never
    # displace them (STYLE_GUIDE 3.5).
    steps: List[Tuple] = field(default_factory=list)
    # ---- HR-1 ---------------------------------------------------------
    fed_bite: float = 0.0           # off the federal slope; 0 on the as-is
    fed_bite_name: str = "Provider tax limits"
    hr1_term: Dict[str, Tuple] = field(default_factory=dict)   # name -> (x, row, sub)
    sa_hr1: float = 0.0             # HR-1 taken at the state agency
    claims_hr1: float = 0.0         # HR-1 taken at the claims fan
    claims_hr1_name: str = "Directed payment caps"
    tracker_hr1: List[Tuple] = field(default_factory=list)
    cp0_label: List[str] = field(default_factory=lambda: ["$100 Medicaid", "Dollars"])
    order: List[str] = field(default_factory=lambda: list(ORDER))
    disp: Dict[str, str] = field(default_factory=lambda: {"Other": "Wrap around services"})
    show_beneficiaries: bool = True
    absent: List[str] = field(default_factory=list)   # declared, never estimated
    centre: Tuple[str,str] = ("100 Dollars of","Medicaid Spending")
    kicker: str = ""
    title: str = ""
    strap: str = ""


# ============================ FY2024 AS-IS ================================
AS_IS_2024 = Instance(
    name="national_2024",
    fed=64.70, state=35.30,
    admin=5.07, medicare=2.90,
    mco=40.06, dual=10.89, ffs=41.08,
    mco_ret=4.41, dual_ret=1.20, earnings=0.76, adm_marg=4.85,
    mco_adm=3.81, dual_adm=1.04,
    mco_care=35.65, dual_care=9.69,
    node={"Long-term care": 28.53, "Hospitals": 18.66, "Other": 13.33,
          "Physicians & clinics": 12.63, "Behavioral health": 9.51, "Rx drugs": 3.76},
    fraud=0.15,
    ffs_n={"Long-term care": 19.72, "Hospitals": 8.68, "Other": 4.95,
           "Physicians & clinics": 2.87, "Behavioral health": 3.48, "Rx drugs": 1.38},
    mcoc_n={"Long-term care": 6.93, "Hospitals": 7.84, "Other": 6.59,
            "Physicians & clinics": 7.68, "Behavioral health": 4.74, "Rx drugs": 1.87},
    dualc_n={"Long-term care": 1.89, "Hospitals": 2.14, "Other": 1.79,
             "Physicians & clinics": 2.08, "Behavioral health": 1.29, "Rx drugs": 0.51},
    gt={"Children": 13.48, "Adults": 29.56, "Disabled": 24.98, "Aged": 18.41},
    steps=[("admin", "top", 5.07, 615), ("medicare", "top", 2.90, 715)],
    kicker="AS IS  \u00b7  FY2024 ACTUAL",
    title="$100 of Medicaid spending, before P.L. 119-21",
    strap="CMS-64 FY2024 national totals. Measured, except where flagged.",
)


def to_be_2030(L, per100):
    """Build the FY2030 instance from the computed ledger and lane values."""
    PT = per100["Provider tax limits"]
    sa = [("Blocked senior enrollment rule", 598),
          ("Work reporting", 648),
          ("Six-month renewals", 682),
          ("Blocked Medicaid enrollment rule", 748),
          ("Everything else", 786)]
    steps = [(n, "bot", per100[n], x) for n, x in sa]
    steps += [("admin", "top", L["admin"], 615),
              ("medicare", "top", L["medicare"], 715)]
    return Instance(
        name="national_2030",
        fed=64.70, state=35.30,
        admin=L["admin"], medicare=L["medicare"],
        mco=L["mco"], dual=L["dual"], ffs=L["ffs"],
        mco_ret=L["mco_ret"], dual_ret=L["dual_ret"], earnings=L["earnings"],
        adm_marg=L["mco_adm"] + L["dual_adm"],
        mco_adm=L["mco_adm"], dual_adm=L["dual_adm"],
        mco_care=L["mco_care"], dual_care=L["dual_care"],
        node=L["node"], fraud=L["fraud"],
        ffs_n=L["ffsn"], mcoc_n=L["mcoc"], dualc_n=L["dualc"],
        gt={k: v * sum(L["node"].values()) / 86.43
            for k, v in {"Children": 13.48, "Adults": 29.56,
                         "Disabled": 24.98, "Aged": 18.41}.items()},
        steps=steps,
        fed_bite=PT,
        hr1_term={
            "Provider tax limits": (552, -1, "federal match never drawn"),
            "Blocked senior enrollment rule": (720, 1, "duals will not enrol; cost shifts to the beneficiary"),
            "Work reporting": (900, 2, "will not enrol"),
            "Six-month renewals": (1080, 0, "will not survive renewal"),
            "Blocked Medicaid enrollment rule": (1240, 1, "will not enrol"),
            "Everything else": (1180, 2, "mixed phases \u2014 UNRESOLVED"),
            "Directed payment caps": (1560, 2, "will not top up hospital, nursing facility, academic rates"),
        },
        sa_hr1=sum(per100[n] for n, _ in sa),
        claims_hr1=per100["Directed payment caps"],
        tracker_hr1=[
            (col_right("FEDERAL"), PT, "provider tax limits"),
            (col_right("STATE_AGENCY"), sum(per100[n] for n, _ in sa),
             "work reporting, renewals, enrolment rules, other"),
            (col_right("CLAIMS"), per100["Directed payment caps"],
             "directed payment caps"),
        ],
        cp0_label=["$100 prior law", "FY2030"],
        kicker="TO BE  \u00b7  FY2030 PROJECTION",
        title="$100 of Medicaid spending under prior law, with P.L. 119-21 applied",
        strap="Every figure modelled. HR-1 lanes CBO Oct 2025; denominator CBO Jan 2025 vintage.",
    )


# ============================ DC FY2024 AS-IS =============================
def as_is_dc():
    """District of Columbia, FY2024, in the national view. Reduced fidelity;
    absences are declared on the artifact, never estimated (S-068, S-071)."""
    import ledger_dc as D
    return Instance(
        name="dc_2024",
        fed=D.fed, state=D.state,
        admin=D.admin, medicare=D.medicare,
        mco=D.mco, dual=D.dual, ffs=D.ffs,
        mco_ret=D.mco_ret, dual_ret=D.dual_ret, earnings=D.earnings,
        adm_marg=D.mco_adm + D.dual_adm,
        mco_adm=D.mco_adm, dual_adm=D.dual_adm,
        mco_care=D.mco_care, dual_care=D.dual_care,
        node=D.node, fraud=D.fraud,
        ffs_n=D.ffs_n, mcoc_n=D.mcoc_n, dualc_n=D.dualc_n,
        gt={},
        steps=[("admin", "top", D.admin, 615), ("medicare", "top", D.medicare, 715)],
        order=D.ORDER_DC,
        disp={},
        show_beneficiaries=False,
        absent=D.ABSENT,
        cp0_label=["$100 DC Medicaid", "Dollars"],
        centre=("100 Dollars of","DC Medicaid Spending"),
        kicker="AS IS  \u00b7  DISTRICT OF COLUMBIA  \u00b7  FY2024",
        title="$100 of DC Medicaid spending, before P.L. 119-21",
        strap="REDUCED FIDELITY. CMS-64 / MACStats FY2024 DC spine; payer peel DHCF CY2023; "
              "MCO service mix is a national proxy (modelled). Vintages need re-checking.",
    )
