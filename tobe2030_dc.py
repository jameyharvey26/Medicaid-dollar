# tobe2030_dc.py — the District of Columbia FY2030 to-be, in dollars.
#
# The national to-be takes CBO's national score and distributes it across seven
# levers. That route is closed for DC: CBO publishes no District line, for the
# numerator or the denominator. Allocating the national score by DC's share of
# anything would be filling a missing figure with a share from somewhere else,
# which is the one rule this panel exists to demonstrate.
#
# So DC's levers are RE-DERIVED on District inputs where the District publishes
# them, and ABSENT where it does not. Divergence from the national per-$100
# figure is the finding, not a fault to reconcile away.
#
# WHAT TRANSFERS FROM THE NATIONAL MODEL, UNCHANGED, AND WHY
#   The seven levers themselves      federal statute, identical in every state
#   RAMP, the statutory phase-in     read off the step schedules in the law
#   BITE, where each lane leaves     a claim about the flow, not about a state
#   charged / reach                  lifecycle phases, model structure
#   TERMINAL copy                    presentation, shared
#
# WHAT CANNOT TRANSFER
#   TEN_YR    CBO national only. No District line exists.
#   The gross-up from federal to total-computable. It runs off FMAP, and
#             fmap.py is national throughout with no state seam. DC is unusual:
#             a statutory 70 percent match rather than the formula, with
#             expansion at 90. Not yet built; see ABSENT below.
#   The FY2030 prior-law denominator, which has no District source and is
#             struck on a declared national growth rate. See THE FY2030 HUNDRED.

from ledger import ABSENT, DERIVED, MODELLED
import basis_dc as _B

# ---- the seven levers, as the national model names them --------------------
LEVERS = ["Work reporting", "Provider tax limits", "Directed payment caps",
          "Blocked senior enrollment rule", "Six-month renewals",
          "Blocked Medicaid enrollment rule", "Everything else"]


# ===========================================================================
# DIRECTED PAYMENT CAPS — derived on District inputs
# ===========================================================================
#
# Section 71116 replaces the average-commercial-rate ceiling on state directed
# payments with a Medicare-based limit: 100 percent of the total published
# Medicare rate for expansion states, 110 percent for non-expansion. DC is an
# expansion state, so 100 percent.
#
# Programs above the limit are temporarily grandfathered if their rating period
# falls inside a window around enactment. CMS guidance of 2 February 2026
# replaced the September 2025 reading and widened that window to 180 BUSINESS
# days either side of 4 July 2025, covering 11 October 2024 to 27 March 2026.
# DC's program sits inside it.
#
# From the first rating period beginning on or after 1 January 2028, the
# grandfathered total dollar amount falls by 10 percentage points a year until
# the rate reaches the limit. CMS's proposed rule applies each 10 points to the
# ORIGINAL grandfathered amount, not to the prior year's reduced figure, and
# NAMD supports that reading for budget predictability. Straight line, not
# compounding. CMS's own worked example: a $100M program loses $10M a year.
SDP_SOURCE = ("D.C. Department of Health Care Finance, FY 2026 Medicaid "
              "Advisory Committee meeting, 22 April 2026, summary of ACR "
              "changes FY2025-FY2027")
SDP_RULE = ("P.L. 119-21 sec. 71116; CMS-2449-P; CMS grandfathering guidance "
            "2 February 2026")

# JW, 2026-10-07: use DHCF's own planning assumption and footnote that it is
# one. DHCF states that from 10/1/2026 the District may only collect taxes
# imposed as of 4 July 2025, so the Directed Payment Provider Fee Funds revert
# to the FY2025 level. The FY2026 projection of $658.7M would give a larger
# base and the grandfathering window appears to permit it, but it rested on a
# CMS approval DHCF was still awaiting. The conservative base understates DC's
# exposure; if the higher base is later approved the figure moves in the
# direction that strengthens the finding rather than undermining it.
GRANDFATHERED_M = 485.2            # FY2025 SDP approved by CMS
GRANDFATHERED_ALT_M = 658.7        # FY2026 projected, NOT used; see above
GRANDFATHERED_STATUS = MODELLED    # a planning assumption, not a published figure

STEP_PER_YEAR = 0.10               # 10 percentage points of the ORIGINAL amount

# RATING PERIOD — ESTABLISHED, not assumed. CMS's approval letter to DC's
# Medicaid Director, control name DC_Fee_IPH_New_20231001-20240930, states the
# rating period as 1 October 2023 through 30 September 2024. DC's directed
# payments run on the FEDERAL FISCAL YEAR.
#
# A previous reading of this file took the rating period to be the calendar
# year, on the strength of the plan filings in the project folder being labelled
# CY2023 and CY2024. Those are NAIC annual statements, which every insurer
# files on a calendar year whatever its contracts run on. The CY was the
# statement year, not the rating period. Corrected 2026-10-07.
#
# NO CALENDAR / FISCAL SEAM FOR DC. Because the rating period and the panel's
# fiscal year coincide, each FY sits wholly at one step and no weighting is
# needed. This will NOT hold for a state whose rating period is the calendar
# year — there, an FY panel straddles two steps and the position has to be
# weighted by months. Keep that in shared code when it is written; it is a
# property of the state, not of the model.
RATING_PERIOD = "federal fiscal year, 1 October to 30 September"
RATING_PERIOD_SOURCE = ("CMS approval letter to DC Medicaid, 16 December 2024, "
                        "control name DC_Fee_IPH_New_20231001-20240930")

# The statute bites on rating periods BEGINNING on or after 1 January 2028.
# FY2028 begins 1 October 2027, which is before that date, so FY2028 is NOT
# affected. FY2029 is the first affected period.
_FIRST_AFFECTED_FY = 2029
_steps_by_fy = {fy: fy - _FIRST_AFFECTED_FY + 1 for fy in (2029, 2030, 2031)}

FY30_STEPS = _steps_by_fy[2030]                      # 2
FY30_CUT_FRACTION = FY30_STEPS * STEP_PER_YEAR       # 0.20
DIRECTED_CUT_M = GRANDFATHERED_M * FY30_CUT_FRACTION

# DISCREPANCY — RESOLVED ON THE RULE, 2026-10-29, open only on DHCF's intent.
# DHCF's April 2026 advisory deck and its 7 May 2026 budget testimony both say
# the SDP "must be reduced by 10% each year starting in FY2028." On the rating
# period established above the first affected period is FY2029, and CMS's own
# proposed rule states the test in terms this leaves no room in:
PHASEDOWN_RULE_SOURCE = (
    "CMS-2449-P, 91 FR 30400, 22 May 2026, background: section 71116(b) "
    "'requires a phase down beginning with the first rating period that "
    "starts on or after January 1, 2028'")
# A rating period beginning 1 October 2027 starts BEFORE 1 January 2028, so
# FY2028 is not reached. The rating period is confirmed twice now, on two
# different documents — the approval letter cited above and the FY2025
# preprint DC_Fee_IPH.OPH_New_20241001-20250930.
RATING_PERIOD_SOURCE_2 = ("CMS approved preprint "
                          "DC_Fee_IPH.OPH_New_20241001-20250930, rating "
                          "period 1 October 2024 to 30 September 2025")
# The model does not move to meet DHCF. The question is worth putting to them
# before publication, because a year is one full step, and the alternative is
# kept here so the size of the disagreement stays visible.
DHCF_STATED_FIRST_YEAR = 2028
FIRST_AFFECTED_FY_DISPUTED = False        # resolved on the rule
DIRECTED_CUT_IF_DHCF_RIGHT_M = GRANDFATHERED_M * 3 * STEP_PER_YEAR

# NOT THE END STATE, and now sourced rather than open. KFF's analysis of the
# approved preprints puts 100 percent of DC's hospital SDP spending above the
# new limit — DC and Louisiana are the only two jurisdictions at 100 percent —
# because DC's base rate alone already exceeds the Medicare-based ceiling. On
# that reading the phase-down runs the whole programme down, ten steps, and
# FY2030 at two steps is unambiguously partial.
KFF_ABOVE_LIMIT_SOURCE = (
    "KFF, 'At Least 37 States Have Medicaid State Directed Payments for "
    "Hospital Services That Could Be Reduced by the 2025 Reconciliation Law "
    "Limits': estimated spending above the new limits is 100 percent of DC's "
    "hospital SDP spending")
DIRECTED_REACHES_LIMIT_BY_FY30 = False            # was ABSENT
DIRECTED_STEPS_TO_TERMINATION = int(round(1.0 / STEP_PER_YEAR))

# STILL ABSENT, and now located precisely. To state the termination YEAR on
# District evidence rather than on KFF's conversion we need DC hospitals'
# commercial price as a percentage of Medicare. The preprint's Table 2 gives
# the post-SDP level as a share of ACR — 97.0 percent (DC Healthy Families
# inpatient), 65.8 (HF outpatient), 95.1 and 79.0 (CASSIP) — which is a share
# of commercial, not of Medicare.
SDP_PCT_OF_ACR = {"DC Healthy Families inpatient": 0.970,
                  "DC Healthy Families outpatient": 0.658,
                  "CASSIP inpatient": 0.951,
                  "CASSIP outpatient": 0.790}
ACR_TO_MEDICARE_RATIO = None              # ABSENT
ACR_TO_MEDICARE_TARGET = (
    "RAND, Prices Paid to Hospitals by Private Health Plans, Round 5.1 "
    "(RRA1144-2-v2), Supplemental Material Annex, Table 7, relative prices by "
    "state. The annex is a ZIP at "
    "rand.org/content/dam/rand/pubs/research_reports/RRA1100/RRA1144-2-v2/"
    "RAND_RRA1144-3-v2.annex.zip. The report body names only highlight states "
    "and says it covers 'all U.S. states besides Maryland', which does not "
    "settle whether DC is included, suppressed or omitted. ACQUISITION: open "
    "the annex and read the DC row, or establish that there is not one.")

# The SDP's own federal split, MEASURED, from the same preprint. D-41 sets the
# national directed-payment gross-up to 1.000 in the ABSENCE of a split; DC has
# the split, and JW's call (2026-10-29) is that a state fact beats a national
# decision taken without one. Flagged as a candidate to re-open D-41.
SDP_TOTAL_FY25 = 485_154_441.0
SDP_FEDERAL_FY25 = 376_029_678.0
SDP_NONFEDERAL_FY25 = 485_154_441.0 - 376_029_678.0
SDP_FEDERAL_SHARE = SDP_FEDERAL_FY25 / SDP_TOTAL_FY25
SDP_SPLIT_SOURCE = ("CMS approved preprint "
                    "DC_Fee_IPH.OPH_New_20241001-20250930: total up to "
                    "$485,154,441, federal share $376,029,678")
REOPEN_D41 = ("A measured financing split in the first state panel is "
              "evidence about the national model, not only about DC.")


# ===========================================================================
# PROVIDER TAX LIMITS — coupled to the lever above, which is a finding
# ===========================================================================
#
# DC's directed payments are financed by a hospital provider tax. HR-1 freezes
# provider taxes at their 4 July 2025 level, and DHCF states this alone returns
# the directed payment programme to the FY2025 level in FY2027 — BEFORE the
# phase-down starts. DC therefore takes two sequential bites from two levers,
# and the second lever's base is set by the first.
#
# The national model treats these as independent tributaries with separate
# ramps. In DC they are mechanically coupled. That is a finding about the
# architecture, not a DC quirk to patch: the second state will have it too
# wherever directed payments are provider-tax financed, which is most of them.
#
# THE AMOUNT, found 2026-10-29. It was in DHCF's own budget tables all along,
# on the Dedicated Taxes line — the same line basis_dc.DC_DEDTAX_M reads for
# FY2024, which is how we know the two tables are one line.
DEDTAX_SOURCE = ("Government of the District of Columbia, Department of "
                 "Health Care Finance (HT0), Table HT0-2, FY2027 Proposed "
                 "Budget and Financial Plan chapter, which carries all four "
                 "years on one table")
DEDTAX_M = {2024: 114.647,      # actual
            2025: 235.337,      # actual
            2026: 285.940,      # approved
            2027: 236.167}      # proposed

# FY2027 lands within a million of the FY2025 actual, which is DHCF's
# narrative — "the Provider Fee Funds revert to the FY2025 level" — restated
# as arithmetic and confirmed by a second, independent table.
PROVIDER_TAX_COUPLED_TO_DIRECTED = True
PROVIDER_TAX_STEP_FY27_M = DEDTAX_M[2026] - DEDTAX_M[2027]
REVERT_RESIDUAL_M = DEDTAX_M[2027] - DEDTAX_M[2025]

# THE RATE TAPER DOES NOT REACH DC, and this is a finding rather than a quirk.
# Section 71115 steps the expansion-state safe harbour down 5.5 / 5.0 / 4.5 /
# 4.0 / 3.5 percent from FY2028. DC's hospital provider tax is 3 percent of
# net patient revenue — below every step including the floor. The District's
# entire section 71115 exposure is the OTHER half of the section: from
# 1 October 2026 it may only collect taxes imposed as of 4 July 2025, which
# kills the enlarged tax DHCF filed on 30 June 2025 and was still awaiting
# approval on. A jurisdiction can be fully exposed to 71115 while sitting
# under every threshold in the published schedule, because the freeze and the
# taper are two different instruments and only one of them is a rate.
SAFE_HARBOUR_SCHEDULE = {2028: 0.055, 2029: 0.050, 2030: 0.045,
                         2031: 0.040, 2032: 0.035}
DC_HOSPITAL_TAX_RATE = 0.03
DC_TAX_RATE_SOURCE = ("DHCF FY2026 budget testimony: the hospital provider "
                      "tax is 3 percent of net patient revenue")
TAPER_BINDS_DC = DC_HOSPITAL_TAX_RATE > min(SAFE_HARBOUR_SCHEDULE.values())

# Corroboration, not a basis. DHCF's FY2027 testimony gives net ACR payments
# to hospitals of $307M (FY2025 actual), $455M (FY2026 projected) and $299M
# (FY2027 projected), attributing the fall to the federal limit. The payment
# side and the tax side tell the same story a year apart. Not published off,
# because it mixes the freeze and the ACR limit in one number and the panel
# draws them as two levers.
NET_ACR_M = {2025: 307.0, 2026: 455.0, 2027: 299.0}

# PROVIDER_TAX_CUT_M is derived below, after the FY2030 hundred, because the
# FY2030 level needs the prior-law growth rate. See THE PROVIDER TAX IN FY2030.


# ===========================================================================
# THE REMAINING FIVE LEVERS — absent, with reasons
# ===========================================================================
#
# Each is federal statute and applies in DC. None has a published District
# figure, and none may be allocated from the national score. What each needs is
# named, so acquisition has a target rather than a wish.
# Work reporting and six-month renewals LEFT this dict on 2026-10-29: DHCF
# publishes the population and the dollars, so both are now derived below.
ABSENT_LEVERS = {
    "Blocked Medicaid enrollment rule": (
        "Section 71102 blocks the eligibility-and-enrolment rule. Its effect "
        "falls on PROCESS — ABD interviews, renewal alignment, the 90-day "
        "reconsideration period, CHIP lockouts — not on a nameable group, and "
        "the people affected are those who WOULD HAVE enrolled or stayed "
        "enrolled under easier mechanics. They are a counterfactual, not a "
        "row in DHCF's enrolment report. JW, 2026-10-29: leave ABSENT and "
        "draw it as absence; a provision-by-provision mapping of our own "
        "would be a modelled step with no source behind it."),
    "Blocked senior enrollment rule": (
        "Section 71101 blocks the Medicare Savings Programs rule. Unlike "
        "71102 this one HAS a measured District denominator — QMB-only "
        "enrolment, 12,880 in January 2026, rising while total Medicaid fell "
        "24,000. What is missing is the rate, and no direction has been taken "
        "on it. The Q1 route would work here too."),
    "DC provisions not separately scored": (
        "Renamed from 'Everything else' on JW's call, 2026-10-29. Nationally "
        "that lane is a residual defined by what CBO scored, and a residual "
        "cannot be re-derived from District sources because it is not a "
        "thing, it is a remainder. The DC lane carries named District "
        "provisions instead — see DC_NAMED_PROVISIONS — and is NOT comparable "
        "lane-to-lane with the national residual. The provisions are real and "
        "dated; none is sized, so the lane's amount stays ABSENT."),
}

# The three provisions that fill the renamed lane. Each is federal statute,
# each has a date, none has a District dollar figure.
DC_NAMED_PROVISIONS = {
    "Home equity cap for LTSS": (
        "$1,000,000 cap on home equity for long-term services and supports "
        "eligibility, from 1 January 2028. DC's aged share of benefit "
        "spending is 24.4 percent and its disabled share 35.8 percent, both "
        "above national, so an LTSS eligibility lever may matter more here "
        "than in the national panel, where it sits inside the residual."),
    "Legal immigrant eligibility": (
        "Full-benefit Medicaid narrows for certain legal immigrants from "
        "1 October 2026, with emergency-condition coverage retained. STATUS "
        "CONTESTED: a preliminary injunction has suspended the provision "
        "pending federal litigation, and CMS has not issued written guidance "
        "for several groups (DHCF, February 2026 advisory session). A panel "
        "drawn today has to say so."),
    "Retroactive eligibility": (
        "From 1 January 2027: one month for expansion adults, two months for "
        "all other groups. Same rule, in different units, as the 90-to-30 and "
        "90-to-60 day change DHCF states."),
}
DC_ONLY_NOTED = DC_NAMED_PROVISIONS      # old name, kept for callers


# ===========================================================================
# THE FY2030 HUNDRED — struck on a declared national growth assumption
# ===========================================================================
#
# D-01 as re-anchored makes the FY2030 hundred prior-law FY2030 spending.
# There is no CBO District row and no pre-enactment DC financial plan reaching
# FY2030, so DC's own prior-law FY2030 total cannot be read from a source.
#
# WHAT IS DONE INSTEAD, and why this is not the move the panel refuses.
# DC's FY2024 hundred is grown to FY2030 at the prior-law rate IMPLIED BY THE
# NATIONAL MODEL'S OWN COUNTERFACTUAL: basis_national's FY2024 hundred against
# tobe2030's FY2030 prior-law total, both already in this repo, both at CBO's
# January 2025 baseline vintage.
#
# This is a DENOMINATOR assumption, not a lever figure, and the distinction is
# the whole of it. Allocating CBO's national HR-1 score to DC by some District
# share would fill a missing figure with a share from somewhere else, which is
# the rule DC exists to demonstrate and which the five ABSENT levers above
# obey. A growth rate applied to the hundred is a stated counterfactual: it
# appears on the artifact, a reader can disagree with it, and redoing the panel
# with a different rate is one constant. The levers are claims about the
# District; the hundred is an assumption about the world.
#
# It also keeps DC and national on ONE prior-law assumption at ONE vintage,
# which is what makes the per-$100 comparison between the two panels mean
# anything.
#
# S-105: the rate is derived from the two national constants, never typed. If
# the CBO baseline is ever re-anchored, DC's hundred moves with it and the two
# panels cannot drift apart.
import basis_national as _BN
import tobe2030 as _T30

_N24_B = _BN.HUNDRED_M / 1000.0        # $B, national FY2024 hundred
_N30_B = _T30.TOTAL_30                 # $B, national FY2030 prior law
HUNDRED_YEARS = 6                      # FY2024 -> FY2030

PRIOR_LAW_CAGR = (_N30_B / _N24_B) ** (1.0 / HUNDRED_YEARS) - 1.0
CAGR_STATUS = MODELLED
CAGR_SOURCE = ("implied by basis_national.HUNDRED_M (MACStats Exhibit 16, "
               "FY2024) and tobe2030.TOTAL_30 (CBO letter to Boyle and "
               "Pallone, 5 Mar 2025, January 2025 baseline vintage)")

FY30_HUNDRED_M = _B.DC_TOTAL_M * (1.0 + PRIOR_LAW_CAGR) ** HUNDRED_YEARS
FY30_HUNDRED_STATUS = MODELLED
SCALE30 = FY30_HUNDRED_M / 100.0


def per100_30(m: float) -> float:
    """$ per $100 of the DC FY2030 prior-law hundred. Not the FY2024 hundred."""
    return m / SCALE30


DIRECTED_CUT_PER100 = per100_30(DIRECTED_CUT_M)

# WHAT THIS RATE IGNORES, declared rather than buried. It is a national rate on
# a District programme. DC's own trend differs in ways we can name: enrolment
# growth concentrated among people aged 65+, dual-eligible and PACE capitation
# rising far faster than the rest of the book, and eligibility reductions the
# District itself enacted for FY2026. The rate sits inside the range of DC's
# own observed growth — 5.49% on Exhibit 16 FY2022-24 against 5.27% here — but
# that is corroboration, not derivation.
#
# SUPERSESSION, declared. The District's FY2026 Proposed Budget and Financial
# Plan, transmitted 27 May 2025 and therefore pre-enactment, carries a
# four-year prior-law trajectory through FY2029. When it is acquired, DC's own
# trajectory replaces this rate and the extrapolation shrinks to a single year.
# That is a one-constant change because everything divides through SCALE30.
SUPERSEDED_BY = ("DC FY2026 Proposed Budget and Financial Plan, 27 May 2025, "
                 "four-year financial plan FY2026-FY2029 (pre-enactment "
                 "vintage). On the acquisition list.")

# DEFLATOR, open. A growth rate blends real growth and price growth. Shares are
# unaffected, but any LEVEL or per-enrollee figure published off this hundred
# needs a stated deflator. Parked early-reader item (d); it lands here.
DEFLATOR_STATED = None


# ===========================================================================
# THE PROVIDER TAX IN FY2030 — derived, with the measured step as its floor
# ===========================================================================
#
# JW, 2026-10-29 (Q3). The measured FY2027 step is $49.773M, and it is NOT the
# FY2030 figure. The freeze holds the tax at a NOMINAL FY2025 level while
# prior law would have grown it, so the gap widens every year on its own. The
# lever is therefore the divergence between a growing prior-law base and a
# flat line, not a constant.
#
# One modelled assumption, stated: the prior-law tax base would have tracked
# Medicaid spending, so it grows at PRIOR_LAW_CAGR — the same rate as the
# denominator, which keeps the lever and the hundred on one counterfactual.
#
# The flat carry-forward of the FY2027 step is kept beside it as the FLOOR.
# It is measured at both ends and understates FY2030; drawing both is what
# makes the mechanism — a frozen nominal cap biting harder every year —
# visible rather than asserted.
_TAX_BASE_FY = 2026                       # last pre-freeze approved level
_TAX_FROZEN_LEVEL_M = DEDTAX_M[2025]      # nominal, frozen at the 4 Jul 2025 level
_TAX_YEARS = 2030 - _TAX_BASE_FY

PROVIDER_TAX_PRIOR_LAW_FY30_M = (DEDTAX_M[_TAX_BASE_FY]
                                 * (1.0 + PRIOR_LAW_CAGR) ** _TAX_YEARS)
PROVIDER_TAX_CUT_M = PROVIDER_TAX_PRIOR_LAW_FY30_M - _TAX_FROZEN_LEVEL_M
PROVIDER_TAX_CUT_FLOOR_M = PROVIDER_TAX_STEP_FY27_M      # measured, understates
PROVIDER_TAX_STATUS = MODELLED
PROVIDER_TAX_PER100 = per100_30(PROVIDER_TAX_CUT_M)
PROVIDER_TAX_FLOOR_PER100 = per100_30(PROVIDER_TAX_CUT_FLOOR_M)

# THE COUPLING, MODELLED IN SEQUENCE — JW, 2026-10-29 (Q4).
#
# Order: the tax freeze bites first, in FY2027, and sets the SDP base at the
# FY2025 approved level; the section 71116 phase-down then runs 10 points a
# year on THAT base from FY2029. GRANDFATHERED_M is already the post-revert
# figure, which is what the assertion below pins.
#
# NOT THE SAME DOLLAR, and this is what keeps the two lanes from
# double-counting. The provider tax lever measures NON-FEDERAL FINANCING that
# will not be collected, and leaves the flow at STATE GOVERNMENT. The directed
# payment lever measures a PAYMENT that will not be made, and leaves at
# CLAIMS. They are two stages of one event, drawn at the two points where the
# money actually stops — exactly as the national model separates them.
#
# Most expansion states finance directed payments with a provider tax, so this
# ordering is shared code waiting to happen, not a DC patch.
COUPLING_ORDER = ("freeze (FY2027, sets the base) -> phase-down (FY2029+, "
                  "runs on that base)")
COUPLING_MODELLED = True


# ===========================================================================
# THE TWO ENROLMENT LEVERS — District denominators, one modelled rate
# ===========================================================================
#
# Both apply to the expansion adult group from 1 January 2027, and DHCF
# publishes that group monthly and books its spending as its own budget line.
# Nothing below is allocated from CBO: the denominator is DC's, the dollars
# are DC's, and the single modelled step is the rate.
ENROL_SOURCE = ("DHCF, Monthly Medicaid and Alliance Enrollment Report, "
                "February 2026 edition, data through January 2026, "
                "preliminary")
GROUP8_SOURCE = ("DHCF (HT0) Table HT0-4, MCO - Childless Adults (Group 8), "
                 "FY2024 actual")

# The population exposed. NOT the FY2024 mix: the District cut childless adult
# and parent eligibility to 138% FPL itself, effective 1 January 2026, and
# auto-enrolled about 15,000 people into the Healthy DC Plan. The 134-210% FPL
# band reads 1 in January 2026 against 16,417 a year earlier. A DC panel built
# off the FY2024 bands would overstate both levers by about a sixth.
EXPANSION_AT_RISK = 78_322                # childless adult 0-133% FPL, Jan 2026
EXPANSION_PRE_CUT_BAND = 16_417           # 134-210% FPL, Jan 2025, now gone
DC_OWN_ELIGIBILITY_CUT = ("DHCF, February FY26 MCAC presentation: threshold "
                          "for Parent/Caretaker Relatives and Childless "
                          "Adults reduced to 138% FPL, adults above it "
                          "disenrolled effective 31 December 2025")

# The dollars, grown to FY2030 on the same counterfactual as the hundred.
GROUP8_MCO_FY24_M = 712.779
DC_EXPANSION_FY30_M = GROUP8_MCO_FY24_M * (1.0 + PRIOR_LAW_CAGR) ** HUNDRED_YEARS

# ---- the rate ------------------------------------------------------------
#
# JW, 2026-10-29 (Q1), combining the three options on the table: publish a
# RANGE, with a single declared DEFAULT inside it, and let both become the
# slider in the explorer — the default is where the slider sits, the range is
# how far it travels.
#
# THE DEFAULT is the rate implied by CBO's own score, derived here and typed
# nowhere (S-105): each national lever's FY2030 total-computable dollars over
# national expansion-group spending at FY2030. A rate is not a dollar
# allocation, and that distinction is declared on the plate rather than
# assumed to be obvious.
import ledger_national_2024 as _N24

NATIONAL_NEW_ADULT_SHARE = _N24.EX21_ADULT_PCT["New adult group"] / 100.0
_NATIONAL_EXPANSION_FY30_B = _T30.TOTAL_30 * NATIONAL_NEW_ADULT_SHARE

CBO_IMPLIED_RATE = {k: _T30.tc30[k] / _NATIONAL_EXPANSION_FY30_B
                    for k in ("Work reporting", "Six-month renewals")}
RATE_DEFAULT = sum(CBO_IMPLIED_RATE.values())
RATE_DEFAULT_STATUS = MODELLED
RATE_DEFAULT_SOURCE = ("implied by tobe2030's FY2030 lever dollars over "
                       "national new-adult-group spending (MACStats Exhibit "
                       "21 share, FY2023), both already in this repo")

# THE ENDS are the only two real-world observations of a work-reporting
# requirement at scale.
RATE_OBSERVED = {
    "Arkansas 2018": 0.25,    # about a quarter of those subject, first 7 months
    "New Hampshire 2019": 0.40,   # about 40 percent of those subject, month 1
}
RATE_OBSERVED_SOURCE = ("CBPP, States' Experiences Confirm Harmful Effects of "
                        "Medicaid Work Requirements: Arkansas 18,164 cases "
                        "terminated, about a quarter of those subject, June "
                        "2018 - January 2019; New Hampshire almost 17,000 set "
                        "to lose coverage, about 40 percent of those subject, "
                        "June 2019, before the July 2019 suspension")

# THE DENOMINATORS DIFFER, and the plate has to say so rather than let the
# band read as like-for-like. The default is a share of EXPANSION-GROUP
# SPENDING, which includes people the requirement exempts. The two observed
# rates are coverage loss among THOSE SUBJECT, a smaller group. Until DC's
# exempt share is established the upper ends are an upper bound, not a
# comparable figure — which is why the band runs from the default UP, and why
# the next acquisition is named here.
RATE_BAND = (RATE_DEFAULT, max(RATE_OBSERVED.values()))
RATE_BASIS_DIFFERS = (
    "The default is a share of expansion-group spending; the observed ends "
    "are coverage loss among those subject to the requirement, a smaller "
    "group. Not like-for-like until DC's exempt share is established.")
EXEMPT_SHARE = None                       # ABSENT — the next acquisition
EXEMPT_SHARE_TARGET = (
    "DC's exempt share of expansion adults. DHCF publishes the exemption set "
    "- Medicare enrollees, former foster youth, medically frail, pregnant and "
    "post-partum, parents and caretaker relatives - but not the count falling "
    "in it. Needed to put the band's ends on the default's denominator.")

# COVERAGE, not rate. The national model treats both levers as coverage events
# - a person is dropped, nobody keeps a fraction of their care - so the
# spending share and the coverage share are the same number on the stated
# assumption that people dropped carry the group's average per-enrollee
# spending. Declared, because it is the step that lets one slider drive both
# the dollars and the people.
COVERAGE_NOT_RATE = True
PEOPLE_AT_DEFAULT = EXPANSION_AT_RISK * RATE_DEFAULT

WORK_REPORTING_CUT_M = CBO_IMPLIED_RATE["Work reporting"] * DC_EXPANSION_FY30_M
RENEWALS_CUT_M = CBO_IMPLIED_RATE["Six-month renewals"] * DC_EXPANSION_FY30_M
WORK_REPORTING_PER100 = per100_30(WORK_REPORTING_CUT_M)
RENEWALS_PER100 = per100_30(RENEWALS_CUT_M)

# DC's own implementation rules, which narrow the exposed population further
# and are published. Recorded so the exempt-share acquisition has a target.
WORK_REQUIREMENT_RULES = {
    "effective": "1 January 2027",
    "population": "expansion adults 19-64",
    "test": "one month of compliance; 80 hours work, community service, work "
            "programme, or half-time education",
    "lookback": "one month before the application month",
    "cure period": "30 calendar days after notice",
    "exemptions": "Medicare enrollees, former foster youth, medically frail, "
                  "pregnant and post-partum, parents and caretaker relatives "
                  "(DC: parents up to 138% FPL not subject)",
}
RENEWALS_RULE = ("expansion adults move from 12-month to six-month "
                 "certification periods, 1 January 2027")

# Section 71101's denominator is measured even though its rate is not.
MSP_DENOMINATOR = 12_880                  # QMB only, January 2026


# ===========================================================================
# THE FY2030 HUNDRED'S SUPERSESSION — hunted, not found
# ===========================================================================
#
# SUPERSEDED_BY above puts the District's own four-year trajectory on the
# acquisition list. Hunted 2026-10-29 and not found. Checked: the DHCF agency
# chapter of the FY2026 volume (FY2024 actual, FY2025 approved, FY2026
# proposed, stops); the DHCF chapter of the FY2027 volume (stops at FY2027);
# DHCF's FY2026 budget testimony (says savings "flow through the entirety of
# the four-year financial plan" and gives no Medicaid figures for it); DHCF's
# FY2026 budget slides; and the June 2025 MCAC budget presentation. The
# District publishes its four-year plan at District and fund level, not as an
# agency Medicaid trajectory.
#
# NOT PROVED ABSENT. One place is unchecked: the Executive Summary volume of
# the FY2026 PROPOSED budget, which is distributed as a Box document rather
# than a direct PDF. If an agency-level Medicaid trajectory exists anywhere it
# is there.
SUPERSESSION_HUNT = (
    "Hunted 2026-10-29 across both DHCF agency chapters, the FY2026 budget "
    "testimony, the FY2026 budget slides and the June 2025 MCAC budget "
    "presentation. All stop at the budget year. Remaining place to look: the "
    "Executive Summary volume of the FY2026 Proposed Budget and Financial "
    "Plan, Box-hosted. The national-implied rate stands until then.")

# And no District HR-1 coverage-loss estimate exists at all: DHCF's budget
# materials quantify the SDP and the tax and say nothing about enrolment
# effects of the federal law. JW, 2026-10-29: publish OUR figure, derived from
# the Q1 range on DC's own denominator, rather than citing a national model
# allocated down.
DC_COVERAGE_ESTIMATE_EXISTS = False


def _check():
    assert abs(FY30_CUT_FRACTION - 0.20) < 1e-12, FY30_CUT_FRACTION
    assert FY30_STEPS == 2, "FY2029 and FY2030 only; FY2028 begins too early"
    assert DIRECTED_CUT_IF_DHCF_RIGHT_M > DIRECTED_CUT_M
    assert FY30_HUNDRED_M is not None
    assert 0.03 < PRIOR_LAW_CAGR < 0.08, (
        "the prior-law rate must stay inside the range of DC's own observed "
        "growth; outside it, the national rate is no longer corroborated")
    assert abs(SCALE30 * 100.0 - FY30_HUNDRED_M) < 1e-9
    assert FY30_HUNDRED_M > _B.DC_TOTAL_M, "FY2030 must exceed FY2024"

    # the lever set still partitions, with the lane renamed
    assert set(ABSENT_LEVERS) | {"Directed payment caps", "Provider tax limits",
                                 "Work reporting", "Six-month renewals"} == \
        set(LEVERS) - {"Everything else"} | {"DC provisions not separately scored"}

    # section 71116 timing, resolved on the rule
    assert not FIRST_AFFECTED_FY_DISPUTED
    assert _FIRST_AFFECTED_FY == 2029
    assert DIRECTED_REACHES_LIMIT_BY_FY30 is False
    assert DIRECTED_STEPS_TO_TERMINATION == 10

    # the SDP split ties to the preprint and to the grandfathered base
    assert abs(SDP_TOTAL_FY25 + 0.0 - (SDP_FEDERAL_FY25 + SDP_NONFEDERAL_FY25)) < 1.0
    assert abs(SDP_TOTAL_FY25 / 1e6 - GRANDFATHERED_M) < 0.1, (
        "the preprint total must tie to the grandfathered base")
    assert 0.70 < SDP_FEDERAL_SHARE < 0.85

    # the dedicated-tax line is the same line basis_dc reads
    assert abs(_B.DC_DEDTAX_M - DEDTAX_M[2024]) < 1e-9
    assert abs(REVERT_RESIDUAL_M) < 1.0, (
        "FY2027 must land at the FY2025 level or the revert reading fails")
    assert not TAPER_BINDS_DC, (
        "DC's 3 percent rate sits below the 3.5 percent floor; if this fires, "
        "DC raised its tax and the whole section 71115 reading changes")

    # Q3: the derived FY2030 figure must exceed its own measured floor
    assert PROVIDER_TAX_CUT_M > PROVIDER_TAX_CUT_FLOOR_M > 0, (
        "a frozen nominal cap bites harder every year; if the derived figure "
        "falls below the measured FY2027 step the growth assumption is wrong")

    # Q4: the phase-down base must be the POST-revert figure, never the FY2026
    # projection, or the two coupled levers double-count
    assert GRANDFATHERED_M < GRANDFATHERED_ALT_M
    assert COUPLING_MODELLED

    # Q1: the default sits inside the band and below the observed ends
    assert 0.0 < RATE_DEFAULT < 1.0
    assert RATE_BAND[0] <= RATE_BAND[1]
    assert RATE_DEFAULT < min(RATE_OBSERVED.values()), (
        "if the CBO-implied rate ever exceeds the observed ends, the basis "
        "note below it is no longer the explanation and must be rewritten")
    assert EXEMPT_SHARE is None, "the band's ends are not yet like-for-like"
    assert WORK_REPORTING_CUT_M > RENEWALS_CUT_M > 0
    assert DC_EXPANSION_FY30_M > GROUP8_MCO_FY24_M

    # the four derived levers all land on the same hundred
    for v in (DIRECTED_CUT_PER100, PROVIDER_TAX_PER100,
              WORK_REPORTING_PER100, RENEWALS_PER100):
        assert 0.0 < v < 100.0


_check()


if __name__ == "__main__":
    print("DC FY2030 to-be\n")
    print(f"  grandfathered base        {GRANDFATHERED_M:>10,.1f} $M  "
          f"(MODELLED: DHCF planning assumption, post-revert)")
    print(f"  rating period             {RATING_PERIOD}")
    print(f"  first affected period     FY{_FIRST_AFFECTED_FY}"
          f"   (resolved on CMS-2449-P; DHCF says FY{DHCF_STATED_FIRST_YEAR})")
    print(f"  FY2030 position           {FY30_CUT_FRACTION*100:>10,.0f} points off base"
          f"  ({FY30_STEPS} of {DIRECTED_STEPS_TO_TERMINATION} steps)")
    print(f"  terminates by FY2030      {str(DIRECTED_REACHES_LIMIT_BY_FY30):>10}"
          f"   (KFF: 100% of DC's SDP above the limit)")
    print(f"  SDP federal share         {SDP_FEDERAL_SHARE:>10.4f}   (MEASURED)")
    print()
    print(f"  prior-law growth, national implied {PRIOR_LAW_CAGR*100:>9.3f}%/yr  ({CAGR_STATUS})")
    print(f"  DC FY2030 hundred              {FY30_HUNDRED_M:>10,.1f} $M  ({FY30_HUNDRED_STATUS})")
    print()
    print(f"  disenrolment rate, default     {RATE_DEFAULT*100:>10.2f}%"
          f"   (CBO-implied; band to {RATE_BAND[1]*100:.0f}%)")
    print(f"  expansion adults at risk       {EXPANSION_AT_RISK:>10,}")
    print(f"  people at the default          {PEOPLE_AT_DEFAULT:>10,.0f}")
    print()
    print(f"  {'lever':<34} {'$M':>10} {'per $100':>10}")
    print("  " + "-" * 56)
    for name, m, p in (
            ("Work reporting", WORK_REPORTING_CUT_M, WORK_REPORTING_PER100),
            ("Provider tax limits", PROVIDER_TAX_CUT_M, PROVIDER_TAX_PER100),
            ("Directed payment caps", DIRECTED_CUT_M, DIRECTED_CUT_PER100),
            ("Six-month renewals", RENEWALS_CUT_M, RENEWALS_PER100)):
        print(f"  {name:<34} {m:>10,.2f} {p:>10.2f}")
    print(f"  {'(provider tax floor, measured)':<34} "
          f"{PROVIDER_TAX_CUT_FLOOR_M:>10,.2f} {PROVIDER_TAX_FLOOR_PER100:>10.2f}")
    print()
    print(f"  levers derived: 4 of {len(LEVERS)}; absent: {len(ABSENT_LEVERS)}")
    for k in ABSENT_LEVERS:
        print(f"     ABSENT  {k}")
