# views.py — the framing for each artifact. No numbers.
#
# These were fields on `Instance`, sitting beside the ledger values, which made
# it impossible to tell which half of a config was a claim about the world and
# which half was a decision about the page.

from view import View
from outflows import OUTFLOWS as _OF

# The three pinned peel positions, read from the one declaration rather
# than typed again here. They were 615 / 665 / 715 in four files.
_PIN = {k: _OF[n]["src_x"] for k, n in
        (("admin", "Administration"), ("oversight", "Federal oversight"),
         ("medicare", "Medicare premiums"))}

SUBS_NAT = [("vaccines for children", "vfc", "admin", "FEDERAL", "Vaccines"),
            ("administration, oversight and Medicare premiums", "adm_med", "admin",
             "STATE_AGENCY", "State Admin"),
            ("plan administration + earnings", "plan", "admin", "PAYER",
             "MCO Admin"),
            ("documented fraud", "fraud", "fraud", "PROVIDERS", "Fraud")]

V_NAT = View(
    root="state_agency",
    cp0_label=["Actuals"],
    cp0_year="2024",
    centre=("100 Dollars of", "Medicaid Spending"),
    disp={"Other": "Wrap around services"},
    step_x=dict(_PIN),
    subs_spec=SUBS_NAT,
    show_beneficiaries=True,
    kicker="AS IS  \u00b7  FY2024 ACTUAL",
    title="$100 of Medicaid spending, before P.L. 119-21",
    strap="CMS-64 FY2024 national totals. Measured, except where flagged.",
)

V_DC = View(
    root="state_agency",
    # Not "$100 DC Medicaid Dollars" any more. D-70 strikes the hundred at the
    # state agency, and the first anchor reports what enters. On this panel the
    # two coincide, because DC has nothing that peels before the hundred — but
    # that is a fact about DC, not a definition, and the label must not assert
    # the hundred one column early.
    cp0_label=["Actuals"],
    cp0_year="2024",
    centre=("100 Dollars of", "DC Medicaid Spending"),
    disp={},
    step_x={k: _PIN[k] for k in ("admin", "medicare")},
    subs_spec=SUBS_NAT,
    show_beneficiaries=False,
    kicker="AS IS  \u00b7  DISTRICT OF COLUMBIA  \u00b7  FY2024",
    title="$100 of DC Medicaid spending, before P.L. 119-21",
    strap="REDUCED FIDELITY. CMS-64 / MACStats FY2024 DC spine; payer peel DHCF "
          "CY2023; MCO service mix is a national proxy (modelled). Vintages need "
          "re-checking.",
)


# --------------------------------------------------------------------------
# FY2030 to-be. The HR-1 tributaries split three ways: the amount and the reach
# are in `ledger_national_2030.py`, the terminal sub-label and the declaration
# order are here, and `src_x` stays in `outflows.py`. Nothing below is a number
# except a lattice coordinate.

from instances import T_SLOT
from outflows import OUTFLOWS as _OF
from view import PeelSum

# The tracker lattice has five edges and the reach vocabulary has six phases.
# Directed payment caps would have reached a provider; there is no PROVIDERS
# edge, so the terminal rides the last one before it. A lattice fact, kept
# where lattice facts belong.
REACH_SLOT = dict(T_SLOT, PROVIDERS=T_SLOT["CLAIMS"])

# Declaration order. The fan packs its rows in it (S-085).
SUB_2030 = {
    "Provider tax limits": "federal match never drawn",
    "Blocked senior enrollment rule":
        "2023 rule; dual eligibles pay these Medicare costs themselves",
    "Work reporting": "will not enroll; would have reached disbursements",
    "Six-month renewals": "will not survive renewal; would have reached the payer",
    "Blocked Medicaid enrollment rule": "2024 rule; would have reached a paid claim",
    # JW: name it, give examples, and let it take the top row where it costs
    # almost no height.
    "Everything else": "e.g. home equity, cost sharing",
    "Directed payment caps": "will not top up hospital, nursing facility, academic rates",
}

# The four levers the "Eligibility Rules" marker sums. The Medicare Savings
# moratorium was the fifth until D-89 pulled it out: its dollar would have paid
# a Medicare premium rather than bought care, and summing it with these four
# told the reader they were the same kind of loss. It gets its own marker.
SA_LEVERS = ("Work reporting", "Six-month renewals",
             "Blocked Medicaid enrollment rule", "Everything else")
SA_TRUNK = SA_LEVERS + ("Blocked senior enrollment rule",)

V_2030 = View(
    root="state_agency",
    cp0_label=["Projected under", "prior law"],
    cp0_year="2030",
    centre=("100 Dollars of", "Medicaid Spending"),
    disp={"Other": "Wrap around services"},
    # The five levers take their trunk x from outflows.OUTFLOWS, which is the
    # one declaration of where a tributary leaves the trunk. Administration and
    # Administration and Medicare premiums keep their pinned offsets in every
    # instance; the positions come from OUTFLOWS, not from a literal here.
    step_x={**{n: _OF[n]["src_x"] for n in SA_TRUNK},
            **_PIN},
    subs_spec=[
        ("provider tax limits", PeelSum(("Provider tax limits",)), "hr1",
         "STATE_GOVT", "Provider Tax"),
        ("vaccines for children", "vfc", "admin", "FEDERAL", "Vaccines"),
        ("administration, oversight and Medicare premiums", "adm_med", "admin",
         "STATE_AGENCY", "State Admin"),
        ("work reporting, renewals, enrollment rules, other",
         PeelSum(SA_LEVERS), "hr1", "STATE_AGENCY", "Eligibility Rules"),
        ("Medicare Savings moratorium",
         PeelSum(("Blocked senior enrollment rule",)), "hr1", "STATE_AGENCY",
         "Medicare Savings"),
        ("plan administration + earnings", "plan", "admin", "PAYER", "MCO Admin"),
        ("directed payment caps", PeelSum(("Directed payment caps",)), "hr1",
         "CLAIMS", "Payment Caps"),
        ("documented fraud", "fraud", "fraud", "PROVIDERS", "Fraud"),
    ],
    hr1_sub=SUB_2030,
    reach_slot=REACH_SLOT,
    show_beneficiaries=True,
    kicker="TO BE  \u00b7  FY2030 PROJECTION",
    title="$100 of Medicaid spending under prior law, with P.L. 119-21 applied",
    strap="Every figure modelled. HR-1 lanes CBO Oct 2025; denominator CBO Jan 2025 vintage.",
)
