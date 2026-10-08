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

# DISCREPANCY, OPEN. DHCF's April 2026 advisory deck states the District's SDP
# "will need to be reduced by 10% each year starting in FY2028." On a fiscal
# rating period the first affected period is FY2029, not FY2028. Either DHCF is
# using the fiscal year loosely, or it anticipates a change we have not seen.
# A year either way moves the FY2030 figure by one full step, so this is worth
# settling before publication. Not resolved by assumption here.
DHCF_STATED_FIRST_YEAR = 2028
FIRST_AFFECTED_FY_DISPUTED = DHCF_STATED_FIRST_YEAR != _FIRST_AFFECTED_FY
DIRECTED_CUT_IF_DHCF_RIGHT_M = GRANDFATHERED_M * 3 * STEP_PER_YEAR

# NOT THE END STATE. The phase-down continues past FY2030 until the rate
# reaches 100 percent of Medicare. DC's programme is ACR-based and an ACR
# ceiling sits well above Medicare, so three steps do not reach the limit and
# FY2030 is a partial bite. How far above is NOT ESTABLISHED here: it needs
# DC's directed payment rate as a percentage of Medicare, which has not been
# acquired. Until it is, this lever cannot be shown as terminating.
DIRECTED_REACHES_LIMIT_BY_FY30 = None     # ABSENT, not False


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
# The coupling is DECLARED here and NOT yet modelled. Modelling it means the
# FY2027 revert has to be established as a dollar figure first, and the only
# statement we have is DHCF's narrative that the funds revert, with no amount.
PROVIDER_TAX_COUPLED_TO_DIRECTED = True
PROVIDER_TAX_CUT_M = None                 # ABSENT


# ===========================================================================
# THE REMAINING FIVE LEVERS — absent, with reasons
# ===========================================================================
#
# Each is federal statute and applies in DC. None has a published District
# figure, and none may be allocated from the national score. What each needs is
# named, so acquisition has a target rather than a wish.
ABSENT_LEVERS = {
    "Work reporting": (
        "Applies to the expansion adult population. DHCF publishes DC's "
        "expansion enrolment and the effective date (1/1/2027), so this is "
        "acquirable rather than unknowable. Needs: enrolment at risk, and a "
        "disenrolment assumption that would be MODELLED and must be declared."),
    "Six-month renewals": (
        "Same population, effective 1/1/2027. Same acquisition path."),
    "Blocked Medicaid enrollment rule": (
        "Rule-driven on DC's eligibility groups. Needs the affected groups."),
    "Blocked senior enrollment rule": (
        "Rule-driven. DHCF reports enrolment growth is highest among people "
        "aged 65+, so DC's exposure may diverge sharply from national."),
    "Everything else": (
        "A residual in the national model, defined by what CBO scored. It has "
        "no District analogue and may not have one; a residual cannot be "
        "re-derived from DC sources because it is not a thing, it is a "
        "remainder. Open question for JW."),
}

# Two further items DC's own source raises that the national lever set does not
# separate out. Recorded so they are not lost; not yet levers.
DC_ONLY_NOTED = {
    "Legal immigrant eligibility": (
        "DHCF: full-benefit Medicaid narrows for certain legal immigrants from "
        "10/1/2026, with emergency-condition coverage retained."),
    "Retroactive eligibility": (
        "DHCF: 90 days to 30 for childless adults and 60 for others, "
        "from 1/1/2027."),
}


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
    assert set(ABSENT_LEVERS) | {"Directed payment caps",
                                 "Provider tax limits"} == set(LEVERS)


_check()


if __name__ == "__main__":
    print("DC FY2030 to-be\n")
    print(f"  grandfathered base        {GRANDFATHERED_M:>10,.1f} $M  "
          f"(MODELLED: DHCF planning assumption)")
    print(f"  alternative base, unused  {GRANDFATHERED_ALT_M:>10,.1f} $M")
    print(f"  rating period             {RATING_PERIOD}")
    print(f"  first affected period     FY{_FIRST_AFFECTED_FY}"
          f"   (FY2028 begins 1 Oct 2027, too early)")
    print(f"  FY2030 position           {FY30_CUT_FRACTION*100:>10,.0f} points off base"
          f"  ({FY30_STEPS} steps)")
    print()
    print(f"  directed payment cut, FY2030   {DIRECTED_CUT_M:>10,.2f} $M")
    print(f"  if DHCF's FY2028 start is right{DIRECTED_CUT_IF_DHCF_RIGHT_M:>10,.2f} $M"
          f"   <- OPEN DISCREPANCY")
    print()
    print(f"  prior-law growth, national implied {PRIOR_LAW_CAGR*100:>9.3f}%/yr  ({CAGR_STATUS})")
    print(f"  DC FY2030 hundred              {FY30_HUNDRED_M:>10,.1f} $M  ({FY30_HUNDRED_STATUS})")
    print(f"  directed payment lever         {DIRECTED_CUT_PER100:>10.2f} per $100 of the FY2030 hundred")
    print()
    print(f"  levers absent: {len(ABSENT_LEVERS)} of {len(LEVERS)}, "
          f"plus provider tax (coupled, undetermined)")
