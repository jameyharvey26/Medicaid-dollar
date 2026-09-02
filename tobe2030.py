# tobe2030.py — the FY2030 to-be ledger, per $100 of prior-law 2030 spending.
#
# D-01 (as re-anchored): $100 = FY2030 total Medicaid spending under PRIOR LAW.
# D-60: the counterfactual vintage is CBO's January 2025 baseline, because that
#       is what the score is measured against.
#
# NUMERATOR — sourced, not modelled.
#   CBO Supplemental Cost Estimate, P.L. 119-21 Title VII Subtitle B Ch.1,
#   28 Oct 2025, "By Fiscal Year, Billions of Dollars":
#     FY2030 effect on the deficit  -108.152
#     FY2030 estimated outlays      -111.441
#     FY2030 estimated revenues       -3.289
#   Deficit basis throughout, per D-45. The revenue wedge is forgone tax on
#   employer coverage; it was never a Medicaid dollar and has no node here.
#
# DENOMINATOR — sourced, not modelled.
#   CBO letter to Ranking Members Boyle and Pallone, 5 Mar 2025, Table 1,
#   "Outlays From Accounts Indicated to Be Under the Jurisdiction of the House
#   Committee on Energy and Commerce", data source The Budget and Economic
#   Outlook: 2025 to 2035 (January 2025). FEDERAL Medicaid outlays FY2030 = $837B.
#   This closes the D-61 gap for the aggregate. The component detail remains
#   unavailable at the January 2025 vintage, so D-11 and S-043 still stand.

FY30_DEFICIT   = 108.152   # $B, federal, sourced
FED_OUTLAYS_30 = 837.0     # $B, federal, sourced, Jan-2025 vintage
FED_SHARE      = 0.6472    # MODELLED (D-10 / fmap.py, FY2024 CMS-64 blend held
                           # constant to 2030 per D-11). The one modelled step
                           # between the two sourced figures above.
TOTAL_30 = FED_OUTLAYS_30 / FED_SHARE

TEN_YR = {
    "Work reporting":                   317.0,
    "Provider tax limits":              182.7,
    "Directed payment caps":            149.4,
    "Blocked senior enrollment rule":    66.0,
    "Six-month renewals":                58.0,
    "Blocked Medicaid enrollment rule":  53.6,
    "Everything else":                   60.1,
}
# Ramp position at FY2030, from phasein.py. Derived from the statutory step
# schedules; MODELLED (S-012).
RAMP = {
    "Work reporting":                   1.00,
    "Provider tax limits":              0.60,
    "Directed payment caps":            0.50,
    "Blocked senior enrollment rule":   1.00,
    "Six-month renewals":               1.00,
    "Blocked Medicaid enrollment rule": 1.00,
    "Everything else":                  1.00,
}
# Gross-up from federal dollars to total-computable dollars, from fmap.py.
# Two lanes carry none by decision (D-39, D-41): the provider tax lane funds the
# state's own match rather than drawing one, and SDP financing is split.
GROSS = {
    "Work reporting":                   1.136,
    "Six-month renewals":               1.136,
    "Blocked senior enrollment rule":   1.701,
    "Blocked Medicaid enrollment rule": 1.701,
    "Everything else":                  1.545,
    "Provider tax limits":              1.000,
    "Directed payment caps":            1.000,
}
# Where each lane leaves the flow. Established, not invented here.
BITE = {
    "Provider tax limits":              "STATE GOVERNMENT",
    "Blocked senior enrollment rule":   "STATE AGENCY",
    "Work reporting":                   "DISBURSEMENTS",
    "Six-month renewals":               "DISBURSEMENTS",
    "Blocked Medicaid enrollment rule": "DISBURSEMENTS",
    "Everything else":                  "DISBURSEMENTS",
    "Directed payment caps":            "CLAIMS",
}
# Terminal node copy. Future tense throughout (D-56, S-047). Plain language
# leads, section number sits in the footnote block (S-033).
TERMINAL = {
    "Work reporting":                   "will not become coverage",
    "Provider tax limits":              "will not be matched",
    "Directed payment caps":            "will not top up hospital rates",
    "Blocked senior enrollment rule":   "will not become premium help",
    "Six-month renewals":               "will not survive renewal",
    "Blocked Medicaid enrollment rule": "will not become enrolment",
    "Everything else":                  "will not become services",
}

raw = {k: TEN_YR[k] * RAMP[k] for k in TEN_YR}
tot = sum(raw.values())
fed30  = {k: raw[k] / tot * FY30_DEFICIT for k in raw}          # federal $B, FY2030
tc30   = {k: fed30[k] * GROSS[k] for k in fed30}                # total-computable $B
per100 = {k: tc30[k] / TOTAL_30 * 100 for k in tc30}            # $ per $100

if __name__ == "__main__":
    print(f"FY2030 denominator: federal ${FED_OUTLAYS_30:.0f}B / {FED_SHARE:.4f} "
          f"= ${TOTAL_30:,.1f}B total  (federal share MODELLED)")
    print(f"FY2030 numerator  : federal ${FY30_DEFICIT:.3f}B deficit effect (sourced)\n")
    print(f"{'Lane':34} {'fed $B':>8} {'x':>6} {'tot $B':>8} {'per $100':>9}  bite point")
    print("-" * 96)
    for k in sorted(per100, key=lambda x: -per100[x]):
        print(f"{k:34} {fed30[k]:8.2f} {GROSS[k]:6.3f} {tc30[k]:8.2f} {per100[k]:9.2f}  {BITE[k]}")
    print("-" * 96)
    print(f"{'TOTAL':34} {sum(fed30.values()):8.2f} {'':6} {sum(tc30.values()):8.2f} "
          f"{sum(per100.values()):9.2f}")
    print()
    print(f"Federal-only, no gross-up : ${FY30_DEFICIT/TOTAL_30*100:.2f} per $100")
    print(f"Total-computable          : ${sum(per100.values()):.2f} per $100")
    print()
    print("Reading: of every $100 that would have flowed through Medicaid in FY2030")
    print(f"under prior law, ${sum(per100.values()):.2f} will not flow under HR-1.")

# --- MEDICAL COST GROWTH, memo only (EN-30) --------------------------------
# NOT part of the conserved ledger. Drawn to scale, subtracted after "to
# providers", and never netted into the $100.
#
# SOURCE: CMS Office of the Actuary, National Health Expenditure Projections
# 2025-2034. Per-enrollee Medicaid spending growth averages 5.8% a year over
# 2025-2033.
#
# BASIS WARNING, and it is the reason this is a memo and not a lever: 5.8% is
# per-enrollee SPENDING growth, which blends price with utilisation and
# intensity. It is not a pure price index. Used as a deflator it therefore
# OVERSTATES pure medical price inflation. It is the right measure for the
# question "what will it cost a provider to deliver the FY2024 bundle of care
# in FY2030", which is the question the audience actually has, and the wrong
# measure for "what happened to prices". Say which one the copy is claiming.
COST_GROWTH = 0.058
YEARS_24_30 = 6
COST_FACTOR = (1 + COST_GROWTH) ** YEARS_24_30   # 1.4037
