# dc_hr1_acquired.py — figures acquired for the DC FY2030 panel, 28 Oct 2026.
#
# STAGED, NOT WIRED. Nothing imports this file. It exists so that an
# acquisition run is recorded with its sources at the moment it was made,
# before any direction call is taken on how the figures are used. Wiring it in
# is a decision, and the decisions are in DC_HR1_PREFLIGHT_2026-10-28.md.
#
# Nothing here is signed. "Signed" means a person opened the source and agreed
# with the number; nobody has. Every figure below is UNVERIFIED by that test.
#
# S-105 holds: a figure read off a source is typed once, here, with the source
# on the same block. Everything else is derived.

from ledger import ABSENT, DERIVED, MEASURED, MODELLED

import basis_dc as _B


# ===========================================================================
# 1. SECTION 71116 TIMING — the FY2028/FY2029 dispute, settled on the rule
# ===========================================================================
PHASEDOWN_RULE_SOURCE = (
    "CMS-2449-P, Medicaid Managed Care State Directed Payments and Medicaid "
    "Fee-for-Service Targeted Medicaid Practitioner Payments, proposed rule, "
    "91 FR 30400, 22 May 2026, background: section 71116(b) 'requires a phase "
    "down beginning with the first rating period that starts on or after "
    "January 1, 2028'")

# Second, independent confirmation of the rating period, on a different
# document from the approval letter tobe2030_dc already cites.
RATING_PERIOD_SOURCE_2 = (
    "CMS approved preprint DC_Fee_IPH.OPH_New_20241001-20250930, rating "
    "period 1 October 2024 through 30 September 2025")

# A rating period beginning 1 Oct 2027 starts BEFORE 1 Jan 2028, so FY2028 is
# not reached and FY2029 is the first affected period. tobe2030_dc's reading
# is correct and DHCF's "starting in FY2028" is a year early on the rule.
FIRST_AFFECTED_FY_RESOLVED = 2029
DHCF_STATEMENT = ("DHCF, FY2027 budget hearing presentation, 7 May 2026, and "
                  "April 2026 Medicaid Advisory Committee session: the SDP "
                  "'must be reduced by 10% each year starting in FY 2028'")
DHCF_DISPUTE_STATUS = ("resolved on the rule, OPEN on DHCF's intent — worth "
                       "one question to DHCF before publication; a year moves "
                       "the FY2030 figure by one full step")


# ===========================================================================
# 2. THE SDP ITSELF — the preprint, which carries more than the total
# ===========================================================================
SDP_PREPRINT = ("CMS approved preprint DC_Fee_IPH.OPH_New_20241001-20250930, "
                "District of Columbia, inpatient and outpatient hospital "
                "state directed payment, rating period FY2025")

SDP_TOTAL_FY25 = 485_154_441.0        # ties to tobe2030_dc.GRANDFATHERED_M
SDP_FEDERAL_FY25 = 376_029_678.0
SDP_NONFEDERAL_FY25 = 109_124_763.0
SDP_SPLIT_STATUS = MEASURED

SDP_FEDERAL_SHARE = SDP_FEDERAL_FY25 / SDP_TOTAL_FY25      # ~0.7751

# Payment level AFTER the directed payment, as a share of the average
# commercial rate. Preprint Table 2. These are shares of COMMERCIAL, not of
# Medicare, and the ceiling in sec. 71116 is a Medicare ceiling.
SDP_PCT_OF_ACR = {
    "DC Healthy Families inpatient":  0.970,
    "DC Healthy Families outpatient": 0.658,
    "CASSIP inpatient":               0.951,
    "CASSIP outpatient":              0.790,
}

# Does the taper terminate by FY2030? No. Sourced, not inferred.
KFF_SOURCE = ("KFF, 'At Least 37 States Have Medicaid State Directed Payments "
              "for Hospital Services That Could Be Reduced by the 2025 "
              "Reconciliation Law Limits': estimated spending above the new "
              "limits is 100 percent of DC's hospital SDP spending, DC and "
              "Louisiana being the only two jurisdictions at 100 percent, "
              "because the base rate alone already exceeds the limit")
DIRECTED_REACHES_LIMIT_BY_FY30 = False      # was ABSENT in tobe2030_dc
DIRECTED_STEPS_TO_TERMINATION = 10          # 10 points a year off the original

# What is still missing to state the termination year on District evidence
# rather than on KFF's conversion.
ACR_TO_MEDICARE_RATIO = ABSENT
ACR_TO_MEDICARE_TARGET = ("RAND Hospital Price Transparency study, relative "
                          "price of commercial to Medicare for District of "
                          "Columbia hospitals")


# ===========================================================================
# 3. PROVIDER TAX — the bite is published, on the Dedicated Taxes line
# ===========================================================================
#
# DHCF's narrative ("the Directed Payment Provider Fee Funds revert to the
# FY2025 level") restated as arithmetic, and confirmed by a second table:
# FY2027 proposed lands $0.83M from the FY2025 actual.
#
# BASIS WARNING, carried from basis_dc: this is an appropriation, not CMS-64.
# The FY2024 figure here is identical to basis_dc.DC_DEDTAX_M, which is how we
# know the two tables are the same line.
DEDTAX_SOURCE = ("Government of the District of Columbia, Department of "
                 "Health Care Finance (HT0), Table HT0-2, FY2026 and FY2027 "
                 "Proposed Budget and Financial Plan chapters")

DEDTAX_M = {
    2024: 114.647,      # actual
    2025: 235.337,      # actual
    2026: 285.940,      # approved
    2027: 236.167,      # proposed
}
DEDTAX_STATUS = MEASURED

PROVIDER_TAX_STEP_FY27_M = DEDTAX_M[2026] - DEDTAX_M[2027]      # 49.773
REVERT_RESIDUAL_M = DEDTAX_M[2027] - DEDTAX_M[2025]             # 0.830

# NOT AN FY2030 FIGURE. The freeze holds the tax at a nominal FY2025 level
# while prior law would have grown it, so the FY2030 gap is WIDER than the
# FY2027 step. Carrying the step forward unchanged is a floor, not an
# estimate. Q3 in the pre-flight memo.
PROVIDER_TAX_FY30_M = ABSENT

# The rate taper does not reach DC. Expansion-state safe-harbour schedule
# against DC's own rate.
SAFE_HARBOUR_SCHEDULE = {2028: 0.055, 2029: 0.050, 2030: 0.045,
                         2031: 0.040, 2032: 0.035}
DC_HOSPITAL_TAX_RATE = 0.03
DC_TAX_RATE_SOURCE = ("DHCF FY2026 budget testimony: the hospital provider "
                      "tax is 3 percent of net patient revenue")
TAPER_BINDS_DC = DC_HOSPITAL_TAX_RATE > min(SAFE_HARBOUR_SCHEDULE.values())

# Corroboration only, not a publishable basis: it mixes the tax freeze and the
# ACR limit in one number, and the panel draws them as two levers.
NET_ACR_M = {2025: 307.0, 2026: 455.0, 2027: 299.0}
NET_ACR_SOURCE = ("DHCF, FY2027 budget hearing presentation, 7 May 2026, net "
                  "inpatient and outpatient hospital revenue, DHCF "
                  "beneficiaries")


# ===========================================================================
# 4. THE ENROLMENT-SIDE LEVERS — District denominators
# ===========================================================================
ENROL_SOURCE = ("DHCF, Monthly Medicaid and Alliance Enrollment Report, "
                "February 2026 edition, data through January 2026, "
                "preliminary; January 2025 shown for comparison")

ENROL = {                       # (Jan 2025, Jan 2026)
    "childless adult 0-133% FPL":   (76_278, 78_322),
    "childless adult 134-210% FPL": (16_417, 1),
    "parent/caretaker":             (36_270, 29_669),
    "child non-CHIP":               (75_774, 72_301),
    "child CHIP":                   (17_580, 16_276),
    "ABD SSI":                      (22_556, 21_701),
    "ABD other":                    (7_294, 7_473),
    "QMB only":                     (11_622, 12_880),
    "LTSS EPD waiver":              (5_912, 6_746),
    "LTSS DD waiver":               (1_909, 1_888),
    "LTSS non-waiver":              (3_389, 3_015),
    "pregnant":                     (863, 1_004),
    "incarcerated":                 (897, 1_405),
    "other":                        (220, 467),
}
MEDICAID_TOTAL = (276_981, 253_148)
DUALS = (35_726, 36_243)
SENIORS_65_PLUS = (28_076, 29_559)

# The 134-210% band is not an error and not HR-1. The District cut childless
# adult and parent eligibility to 138% FPL itself, effective 1 January 2026,
# and auto-enrolled about 15,000 people into the Healthy DC Plan.
DC_OWN_ELIGIBILITY_CUT = ("DHCF, February FY26 MCAC presentation: income "
                          "threshold for Parent/Caretaker Relatives and "
                          "Childless Adults reduced to 138% FPL, adults above "
                          "it disenrolled effective 31 December 2025; about "
                          "15,000 auto-enrolled in the Healthy DC Plan")
HEALTHY_DC_AUTO_ENROLLED = 15_000

# THE POPULATION EXPOSED TO sec. 71119 AND sec. 71107 IN FY2030. The expansion
# group only, after the District's own cut — not the FY2024 mix, which would
# overstate both levers by about a sixth.
EXPANSION_AT_RISK = ENROL["childless adult 0-133% FPL"][1]      # 78,322

# The dollars, from the same budget table that carries the dedicated taxes.
GROUP8_MCO_M = {2024: 712.779, 2025: 931.882, 2026: 1103.824}
GROUP8_SOURCE = ("DHCF (HT0) Table HT0-4, MCO - Childless Adults (Group 8): "
                 "FY2024 actual, FY2025 approved, FY2026 proposed")

# The one modelled step left in these two levers. Q1 in the pre-flight memo.
DISENROLMENT_RATE = ABSENT

# DC's own implementation rules, which narrow the exposed population further.
WORK_REQUIREMENT_RULES = {
    "effective": "1 January 2027",
    "population": "expansion adults 19-64",
    "test": "one month of compliance; 80 hours work, community service, work "
            "programme, or half-time education",
    "lookback": "one month before the application month",
    "cure period": "30 calendar days after notice",
    "exemptions": ("Medicare enrollees, former foster youth, medically frail, "
                   "pregnant and post-partum, parents and caretaker relatives "
                   "(DC: parents up to 138% FPL not subject)"),
}
RENEWALS_RULE = ("expansion adults move from 12-month to six-month "
                 "certification periods, 1 January 2027")

# sec. 71101, the blocked senior enrolment rule, has a measured denominator.
MSP_DENOMINATOR = ENROL["QMB only"][1]                          # 12,880

# sec. 71102, the blocked Medicaid enrolment rule. Rule-driven on
# administrative process rather than a named population. No District figure and
# no defensible group mapping found.
BLOCKED_MEDICAID_RULE_GROUPS = ABSENT


# ===========================================================================
# 5. THE FY2024 BENEFICIARY ROW — MACStats, same vintage as the national
# ===========================================================================
EX21_FY23 = ("MACPAC, MACStats, Exhibit 21, Medicaid Spending by State, "
             "Eligibility Group and Dually Eligible Status, FY 2023")
EX15_FY23 = ("MACPAC, MACStats, Exhibit 15, Medicaid Full Year Equivalent "
             "Enrollment by State and Eligibility Group, FY 2023")

DC_EX21_TOTAL_M = 4094.0
DC_SPEND_SHARE = {                 # shares of benefit spending, FY2023
    "Children":                     0.100,
    "New adult group":              0.181,
    "Other adult":                  0.118,
    "Individuals with disabilities": 0.358,
    "Aged":                         0.244,
}
DC_DUAL_SPEND_M = 1375.0
DC_FYE_ENROL_K = {"Child": 80, "New adult group": 93, "Other adult": 59,
                  "Disabled": 29, "Aged": 31}
DC_FYE_TOTAL_K = 291

# DECLARED, NOT SMOOTHED. Both exhibits carry a data-quality footnote on DC.
EX_FOOTNOTE_DC = ("MACPAC footnote: the District's reported new adult group "
                  "enrolment differs from the CMS-64 benchmark by more than "
                  "20 percent; average monthly enrolment 33 percent below it")

# And the two sources disagree about the size of the expansion group.
_EX21_NEW_ADULT_SHARE = DC_SPEND_SHARE["New adult group"]
_DHCF_GROUP8_SHARE = GROUP8_MCO_M[2024] / _B.DC_TOTAL_M
NEW_ADULT_SHARE_DISAGREEMENT = _EX21_NEW_ADULT_SHARE - _DHCF_GROUP8_SHARE


# ===========================================================================
# 6. PROVISIONS THE NATIONAL SEVEN DO NOT CARRY
# ===========================================================================
DC_EXTRA_PROVISIONS = {
    "Home equity cap for LTSS": (
        "$1,000,000 cap on home equity for long-term services and supports "
        "eligibility, effective 1 January 2028. DC's aged share of spending "
        "is 24.4% and its disabled share 35.8%, both above national, so this "
        "may matter more here than in the national panel, where it sits "
        "inside the residual."),
    "Non-citizen eligibility restriction": (
        "Effective 1 October 2026 — UNDER PRELIMINARY INJUNCTION, suspended "
        "pending federal litigation, per DHCF's February 2026 advisory "
        "session. CMS has not issued written guidance for several groups. A "
        "panel drawn today has to say the status is contested."),
    "Retroactive coverage": (
        "From 1 January 2027: one month for expansion adults, two months for "
        "all other groups. Same rule DC_ONLY_NOTED records as 30 and 60 days."),
}


# ===========================================================================
# 7. WHAT IS STILL ABSENT
# ===========================================================================
STILL_ABSENT = {
    "sec. 71102 affected groups in DC": "no mapping found",
    "DC commercial-to-Medicare ratio": ACR_TO_MEDICARE_TARGET,
    "District FY2030 prior-law denominator": (
        "The DHCF chapters of the FY2026 and FY2027 volumes stop at the budget "
        "year. DC publishes its four-year financial plan at District and fund "
        "level, not as an agency Medicaid trajectory. NOT FOUND WHERE IT "
        "SHOULD BE, not proved absent — Volume 1 not exhausted."),
    "District HR-1 coverage-loss estimate": (
        "None published. DHCF's budget materials quantify the SDP and the tax "
        "and say nothing about enrolment effects of the federal law."),
    "FY2024 plan retention split, dual and PACE retention, service mix": (
        "Priority 1 from 27 October. Untouched here, and the larger hole."),
}


def _check():
    assert abs(SDP_TOTAL_FY25 - (SDP_FEDERAL_FY25 + SDP_NONFEDERAL_FY25)) < 1.0
    assert 0.70 < SDP_FEDERAL_SHARE < 0.85
    assert abs(SDP_TOTAL_FY25 / 1e6 - 485.2) < 0.1, (
        "the preprint total must tie to tobe2030_dc.GRANDFATHERED_M")
    assert abs(_B.DC_DEDTAX_M - DEDTAX_M[2024]) < 1e-9, (
        "the Dedicated Taxes line and basis_dc.DC_DEDTAX_M must be one line")
    assert abs(REVERT_RESIDUAL_M) < 1.0, (
        "FY2027 must land at the FY2025 level for the revert reading to hold")
    assert PROVIDER_TAX_STEP_FY27_M > 0
    assert not TAPER_BINDS_DC, (
        "DC's 3 percent rate sits below the 3.5 percent floor; if this ever "
        "fires, DC raised its tax and the whole sec. 71115 reading changes")
    assert FIRST_AFFECTED_FY_RESOLVED == 2029
    assert abs(sum(DC_SPEND_SHARE.values()) - 1.0) < 0.011, (
        "Exhibit 21 shares, allowing for rounding at one decimal")
    assert EXPANSION_AT_RISK < sum(ENROL["childless adult 0-133% FPL"][:1]) + \
        ENROL["childless adult 134-210% FPL"][0], (
        "the at-risk population must be the post-cut group, not the FY2024 mix")
    assert DISENROLMENT_RATE is ABSENT, "Q1 is not answered"
    assert PROVIDER_TAX_FY30_M is ABSENT, "Q3 is not answered"


_check()


if __name__ == "__main__":
    print("DC x HR-1 — acquired 28 October 2026, staged, nothing wired\n")
    print(f"  sec. 71116 first affected period   FY{FIRST_AFFECTED_FY_RESOLVED}"
          f"   (DHCF says FY2028; resolved on the rule)")
    print(f"  taper terminates by FY2030         {DIRECTED_REACHES_LIMIT_BY_FY30}"
          f"   ({DIRECTED_STEPS_TO_TERMINATION} steps to termination)")
    print(f"  SDP federal share, measured        {SDP_FEDERAL_SHARE:>8.4f}")
    print()
    print(f"  provider tax step FY2026->FY2027   {PROVIDER_TAX_STEP_FY27_M:>8.3f} $M"
          f"   (lands {REVERT_RESIDUAL_M:+.3f} $M from FY2025 actual)")
    print(f"  safe-harbour taper binds DC        {TAPER_BINDS_DC}"
          f"   (3.0% rate against a 3.5% floor)")
    print()
    print(f"  expansion adults at risk, Jan 2026 {EXPANSION_AT_RISK:>8,}")
    print(f"  QMB only, the sec. 71101 group     {MSP_DENOMINATOR:>8,}")
    print(f"  Group 8 MCO spending, FY2024       {GROUP8_MCO_M[2024]:>8,.1f} $M"
          f"   ({_DHCF_GROUP8_SHARE*100:.1f} of the hundred)")
    print(f"  Exhibit 21 new adult group share   "
          f"{_EX21_NEW_ADULT_SHARE*100:>8.1f}%"
          f"   (disagrees by {NEW_ADULT_SHARE_DISAGREEMENT*100:+.1f} points)")
    print()
    print(f"  still absent: {len(STILL_ABSENT)} items")
    for k in STILL_ABSENT:
        print(f"    - {k}")
