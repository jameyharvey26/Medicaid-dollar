# views.py — the framing for each artifact. No numbers.
#
# These were fields on `Instance`, sitting beside the ledger values, which made
# it impossible to tell which half of a config was a claim about the world and
# which half was a decision about the page.

from view import View

SUBS_NAT = [("administration + Medicare premiums", "adm_med", "admin",
             "STATE_AGENCY", "State Admin"),
            ("plan administration + earnings", "plan", "admin", "PAYER",
             "MCO Admin"),
            ("documented fraud", "fraud", "fraud", "PROVIDERS", "Fraud")]

V_NAT = View(
    root="state_agency",
    cp0_label=["Medicaid Dollars", "(2024 actuals)"],
    centre=("100 Dollars of", "Medicaid Spending"),
    disp={"Other": "Wrap around services"},
    step_x={"admin": 615, "medicare": 715},
    subs_spec=SUBS_NAT,
    show_beneficiaries=True,
    kicker="AS IS  \u00b7  FY2024 ACTUAL",
    title="$100 of Medicaid spending, before P.L. 119-21",
    strap="CMS-64 FY2024 national totals. Measured, except where flagged.",
)

V_DC = View(
    root="state_agency",
    cp0_label=["$100 DC Medicaid", "Dollars"],
    centre=("100 Dollars of", "DC Medicaid Spending"),
    disp={},
    step_x={"admin": 615, "medicare": 715},
    subs_spec=SUBS_NAT,
    show_beneficiaries=False,
    kicker="AS IS  \u00b7  DISTRICT OF COLUMBIA  \u00b7  FY2024",
    title="$100 of DC Medicaid spending, before P.L. 119-21",
    strap="REDUCED FIDELITY. CMS-64 / MACStats FY2024 DC spine; payer peel DHCF "
          "CY2023; MCO service mix is a national proxy (modelled). Vintages need "
          "re-checking.",
)


