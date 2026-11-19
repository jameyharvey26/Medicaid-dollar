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
    # STRAP RESTORED 2026-10-29, corrected. The forked session's wording said
    # all four plans carry care, administration and margin off their own
    # CY2024 filing. Three do. HSCSN is not an MCO in the regulatory sense,
    # files no comparable statement, and sits on CY2023 with no split at all —
    # so the strap says three, and says which year the fourth is on. A strap
    # that rounds "three of four" up to "four" is the kind of small untruth
    # that a plan president finds first.
    strap="CMS-64 / MACStats FY2024 DC spine. The payer column is the four "
          "plans: AmeriHealth, Wellpoint and MedStar on their own CY2024 "
          "Title XIX reporting, each with its administration and margin; "
          "HSCSN on CY2023, with no published split. The District publishes "
          "no managed-care service mix, so that fan is absent.",
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

# DC does not rename the national lanes any more — it replaces them. D-143
# retired the two composite lanes and wrote five District-derived lanes in
# their place: section 71102 became `Blocked renewal automation` and `Blocked
# reconsideration period` (D-123), and the leftovers lane became the three
# named provisions (D-118).
#
# THIS VIEW WAS NOT UPDATED WHEN THAT HAPPENED, and that is why the panel has
# been unrendered since. `DC_SA_LEVERS` still named the two retired lanes, so
# `PeelSum.resolve` raised KeyError on the first one and the build stopped
# before it drew anything. Nobody saw it because nothing calls
# `build_dc_2030()` — it is not wired into `build.py`'s entry point. The
# ledger was right and the picture of it could not be made.
DC_SA_LEVERS = ("Work reporting", "Six-month renewals",
                "Blocked renewal automation", "Blocked reconsideration period",
                "LTSS home equity cap", "Legal immigrant eligibility",
                "Retroactive eligibility")
DC_SA_TRUNK = DC_SA_LEVERS + ("Blocked senior enrollment rule",)

# Each new lane keeps the GEOMETRY of the lane it came out of.
# `outflows.OUTFLOWS` is the national declaration of where a tributary leaves
# the trunk and how far it reaches, and splitting a lane is an editorial act,
# not a claim about the flow: D-143 holds the charge and reach of every new
# lane identical to its parent's, and `ledger_dc_2030.HR1_DC` says so in the
# data. So the DC names map back to the national keys for position, and
# outflows is left untouched. If a DC lane ever leaves somewhere else, that is
# a finding and it earns its own entry there rather than an alias here.
DC_GEOM_ALIAS = {
    # section 71102, split in two — both still leave at the state agency and
    # both still reach the claims column
    "Blocked renewal automation":     "Blocked Medicaid enrollment rule",
    "Blocked reconsideration period": "Blocked Medicaid enrollment rule",
    # the three named provisions out of the leftovers lane — all three leave
    # at the state agency and stop there
    "LTSS home equity cap":       "Everything else",
    "Legal immigrant eligibility": "Everything else",
    "Retroactive eligibility":     "Everything else",
}

# Terminal copy per lane. The national residual's entry goes, because the DC
# panel no longer has a residual: it has five named provisions, a closed and
# dated list, and one of them is enjoined, which the panel has to carry.
DC_SUB_2030 = {k: v for k, v in SUB_2030.items()
               if k not in ("Everything else",
                            "Blocked Medicaid enrollment rule")}
DC_SUB_2030.update({
    "Blocked renewal automation":
        "will not be renewed without a form the District already has",
    "Blocked reconsideration period":
        "will not come back after a paperwork lapse",
    "LTSS home equity cap":
        "will not pass the home equity test for long-term care",
    "Legal immigrant eligibility":
        "will not be eligible — but see the injunction below",
    "Retroactive eligibility":
        "will not be covered for the months before the claim",
})


def _dc_of(name):
    """A DC lane's geometry: its own entry where outflows declares one, and
    the lane it came out of otherwise.

    The fallback used to be the only path, which silently discarded the DC
    slots outflows declares for the split lanes: five tributaries resolved to
    two trunk positions and two of them crossed in the margin. Prefer the
    District's own entry.
    """
    return _OF.get(name) or _OF[DC_GEOM_ALIAS.get(name, name)]

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


# --------------------------------------------------------------------------
# DC FY2030 to-be. V_2030's structure on V_DC's framing. What is dropped is
# dropped because DC does not publish it, not because the panel is simplified:
# no Vaccines for Children line, no federal oversight peel, no DC fraud figure,
# no beneficiary overlay. Each absence is already declared on the ledger.
V_DC_2030 = View(
    root="state_agency",
    cp0_label=["Projected under", "prior law"],
    cp0_year="2030",
    centre=("100 Dollars of", "DC Medicaid Spending"),
    disp={},
    step_x={**{n: _dc_of(n)["src_x"] for n in DC_SA_TRUNK},
            **{k: _PIN[k] for k in ("admin", "medicare")}},
    subs_spec=[
        ("provider tax limits", PeelSum(("Provider tax limits",)), "hr1",
         "STATE_GOVT", "Provider Tax"),
        ("administration and Medicare premiums", "adm_med", "admin",
         "STATE_AGENCY", "State Admin"),
        ("work reporting, renewals, enrollment rules, other",
         PeelSum(DC_SA_LEVERS), "hr1", "STATE_AGENCY", "Eligibility Rules"),
        ("Medicare Savings moratorium",
         PeelSum(("Blocked senior enrollment rule",)), "hr1", "STATE_AGENCY",
         "Medicare Savings"),
        ("plan administration + earnings", "plan", "admin", "PAYER", "MCO Admin"),
        ("directed payment caps", PeelSum(("Directed payment caps",)), "hr1",
         "CLAIMS", "Payment Caps"),
    ],
    declarations_below=True,
    hr1_sub=DC_SUB_2030,
    reach_slot=REACH_SLOT,
    show_beneficiaries=False,
    kicker="TO BE  \u00b7  DISTRICT OF COLUMBIA  \u00b7  FY2030",
    title="$100 of DC Medicaid spending under prior law, with P.L. 119-21 applied",
    strap="DRAFT. Every HR-1 lane is derived on District inputs: no lane is "
          "absent, assumed, or carrying a national figure under a District "
          "label. The FY2030 hundred and the disenrolment rate are modelled "
          "and declared.",
)
