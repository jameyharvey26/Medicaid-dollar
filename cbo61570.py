# cbo61570.py — CBO's section-by-section score for P.L. 119-21, Title VII,
# Subtitle B, Chapter 1 (Medicaid), by fiscal year.
#
# SOURCE. Congressional Budget Office, "Estimated Budgetary Effects of Public
# Law 119-21, to Provide for Reconciliation Pursuant to Title II of H. Con.
# Res. 14, Relative to CBO's January 2025 Baseline", publication 61570,
# 21 July 2025. Workbook `61570-pl119-21-2025Recon-CLB.xlsx`, sheet
# "Title VII", table 7, rows 180-288. Retrieved 2026-11-04.
#
# WHAT THIS CLOSES. D-119 recorded that the three section scores were taken on
# this vintage but that the workbook itself had never been opened — the egress
# proxy refuses cbo.gov and the allowlist request is D-Q13 on the sign-off
# list. It is open now. Every Chapter 1 section is here, by year, so the
# FY2030 position of a provision no longer has to be derived from the
# statutory step schedules: CBO publishes it directly. See D-120, which this
# supersedes for the three named provisions.
#
# UNITS. Millions of dollars, outlays, as CBO prints them: negative is a
# reduction in federal spending. `*` in the workbook means "between -$500,000
# and $500,000" and is carried here as None, not as zero. Budget authority
# differs from outlays by a few million in several sections and is not carried;
# the spending figure is outlays.
#
# NOT SIGNED. Transcribed by a script from the workbook, checked against the
# 28 October supplemental for the six lanes the two documents share. No person
# has opened the workbook and agreed with it.

SOURCE = ("CBO publication 61570, 21 July 2025, "
          "61570-pl119-21-2025Recon-CLB.xlsx, sheet 'Title VII', table 7")
VINTAGE = "2025-07-21"
BASIS = "Millions of dollars, outlays, relative to CBO's January 2025 baseline"
RETRIEVED = "2026-11-04"

YEARS = (2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034)

# section -> (title, {fiscal year: outlays in $M})
SECTIONS = {
    "71101": ("Moratorium on Implementation of Rule Relating to Eligibility "
              "and Enrollment in Medicare Savings Programs",
              (0, -1668, -5243, -7318, -7649, -8044, -8411, -8796, -9251, -9628)),
    "71102": ("Moratorium on Implementation of Rule Relating to Eligibility "
              "and Enrollment for Medicaid, CHIP, and the Basic Health Program",
              (0, -4020, -5617, -5794, -6080, -6337, -6592, -6859, -7140, -7416)),
    "71103": ("Reducing Duplicate Enrollment Under the Medicaid and CHIP Programs",
              (0, 1, 2, 3, 4, -2774, -3842, -3059, -3803, -3951)),
    "71104": ("Ensuring Deceased Individuals Do Not Remain Enrolled",
              (0, 0, None, None, None, None, None, None, None, None)),
    "71105": ("Ensuring Deceased Providers Do Not Remain Enrolled",
              (0, 0, 0, None, None, None, None, None, None, None)),
    "71106": ("Payment Reduction Related to Certain Erroneous Excess Payments "
              "Under Medicaid",
              (0, 0, 0, 0, 0, -108, -3208, -1303, -84, -2847)),
    "71107": ("Eligibility Redeterminations",
              (0, 4, -5083, -7071, -7461, -7809, -8180, -8560, -8978, -9392)),
    "71108": ("Revising Home Equity Limit for Determining Eligibility for "
              "Long-Term Care Services Under the Medicaid Program",
              (-1, -5, -5, -11, -20, -24, -28, -32, -38, -31)),
    "71109": ("Alien Medicaid Eligibility",
              (0, -372, -588, -665, -703, -726, -758, -778, -798, -823)),
    "71110": ("Expansion FMAP for Emergency Medicaid",
              (0, 0, -2459, -3112, -3285, -3466, -3658, -3856, -4070, -4294)),
    "71111": ("Moratorium on Implementation of Rule Relating to Staffing "
              "Standards for Long-Term Care Facilities Under the Medicare and "
              "Medicaid Programs",
              (0, -287, -987, -2061, -3020, -3287, -3323, -3354, -3386, -3418)),
    "71112": ("Reducing State Medicaid Costs",
              (0, 0, -151, -421, -555, -577, -601, -587, -644, -670)),
    "71113": ("Federal Payments to Prohibited Entities",
              (-44, -31, 91, 8, 7, 6, 5, 4, 4, 3)),
    "71114": ("Sunsetting Increased FMAP Incentive",
              (0, -953, -1360, -1406, -1480, -1545, -1613, -1683, -1759, -1830)),
    "71115": ("Provider Taxes",
              (0, -2786, -4737, -7600, -12294, -18585, -26724, -34099, -39317,
               -44976)),
    "71116": ("State Directed Payments",
              (0, -5457, -7475, -9271, -13335, -16552, -19599, -22846, -25861,
               -29028)),
    "71117": ("Requirements Regarding Waiver of Uniform Tax Requirement for "
              "Medicaid Provider Tax",
              (0, -3158, -3426, -3518, -3684, -3828, -3969, -4172, -4345, -4506)),
    "71118": ("Requiring Budget Neutrality for Medicaid Demonstration Projects "
              "Under Section 1115",
              (0, 2, -48, -103, -222, -349, -483, -630, -657, -682)),
    "71119": ("Requirement for States to Establish Medicaid Community "
              "Engagement Requirements for Certain Individuals",
              (0, 180, -12960, -18960, -39810, -46280, -48440, -50690, -53100,
               -55550)),
    "71120": ("Modifying Cost Sharing Requirements for Certain Expansion "
              "Individuals Under the Medicaid Program",
              (0, 1, 6, 4, -1100, -1152, -1209, -1268, -1331, -1395)),
    "71121": ("Making Certain Adjustments to Coverage of Home or "
              "Community-Based Services Under Medicaid",
              (0, 2, 27, 194, 533, 810, 1144, 1216, 1289, 1365)),
}

# CBO's own printed ten-year totals, kept as a check on the yearly series
# rather than re-derived from it. A section whose years sum to something else
# is a transcription fault; `check()` says so.
TEN_YEAR_PRINTED = {
    "71101": -66008, "71102": -55855, "71103": -17419, "71104": None,
    "71105": None, "71106": -7550, "71107": -62530, "71108": -195,
    "71109": -6211, "71110": -28200, "71111": -23123, "71112": -4206,
    "71113": 53, "71114": -13629, "71115": -191118, "71116": -149424,
    "71117": -34606, "71118": -3172, "71119": -325610, "71120": -7444,
    "71121": 6580,
}


def year(sec: str, fy: int):
    """Outlays in $M for one section in one fiscal year. None means CBO
    printed `*`: smaller than $500,000 either way, which is not zero."""
    return SECTIONS[sec][1][YEARS.index(fy)]


def chapter1(fy: int) -> int:
    """Chapter 1 outlays in $M for one fiscal year, treating `*` as zero.
    The three `*` sections are below CBO's own rounding floor and cannot move
    this total by more than a rounding unit."""
    return sum(v for s in SECTIONS
               for v in (SECTIONS[s][1][YEARS.index(fy)],) if v is not None)


def check():
    """Every section's years against CBO's printed ten-year total."""
    bad = []
    for s, (_t, vals) in SECTIONS.items():
        printed = TEN_YEAR_PRINTED[s]
        if printed is None:
            continue
        got = sum(v for v in vals if v is not None)
        if got != printed:
            bad.append((s, got, printed, got - printed))
    return bad


if __name__ == "__main__":
    bad = check()
    print(f"{len(SECTIONS)} sections, {SOURCE}")
    print(f"FY2029 {chapter1(2029):,} $M · FY2030 {chapter1(2030):,} $M")
    print(f"2025-2034 {sum(v for v in TEN_YEAR_PRINTED.values() if v):,} $M")
    if bad:
        print("\nYEARS DO NOT SUM TO CBO'S PRINTED TOTAL:")
        for s, got, printed, d in bad:
            print(f"  {s}: years {got:,}, printed {printed:,}, off by {d:,}")
    else:
        print("all sections sum to CBO's printed ten-year total")


# ===========================================================================
# THE REVENUE BLOCK — why the model carries two numbers for the same section
# ===========================================================================
#
# Table 7 scores Chapter 1 twice: direct spending (rows 180-288) and revenues
# (rows 814-872). Nine of the 21 sections have a revenue effect. The deficit
# effect of a section is its outlays MINUS its revenues, and that is the basis
# `ramp.py`'s TEN_YR uses while D-26's illustrative figures use outlays.
#
# `ramp.py` has carried a flag since 2026-08-27 calling this "an $8.6B
# section-level wedge, unresolved" and naming it open task 2. It is not
# unresolved. See `reconcile_ramp()`.
#
# Same source, same sheet, same units: millions of dollars, revenues.

REVENUES = {
    "71102": (0, -162, -223, -232, -240, -249, -259, -276, -287, -297),
    "71106": (0, 0, 0, 0, 0, -5, -139, -61, -3, -127),
    "71107": (0, 0, -368, -515, -539, -565, -594, -624, -654, -685),
    "71110": (0, 0, -12, -20, -21, -22, -23, -25, -26, -28),
    "71114": (0, -59, -83, -87, -91, -96, -101, -107, -111, -116),
    "71115": (0, -188, -331, -468, -648, -856, -1123, -1376, -1598, -1836),
    "71117": (0, -61, -67, -69, -70, -71, -72, -75, -76, -77),
    "71118": (0, 0, 0, -1, -2, -3, -6, -8, -8, -8),
    "71119": (0, 0, -411, -628, -1138, -1273, -1283, -1294, -1306, -1317),
}

REVENUE_TEN_YEAR_PRINTED = {
    "71102": -2225, "71106": -335, "71107": -4544, "71110": -177,
    "71114": -851, "71115": -8424, "71117": -638, "71118": -36,
    "71119": -8650,
}


def revenue(sec: str, fy: int) -> int:
    """Revenues in $M for one section in one fiscal year. Zero where the
    section has no revenue effect."""
    r = REVENUES.get(sec)
    return 0 if r is None else r[YEARS.index(fy)]


def deficit(sec: str, fy: int):
    """Deficit effect in $M: outlays minus revenues. This is `ramp.py`'s
    basis. None where CBO printed `*` for outlays."""
    o = year(sec, fy)
    return None if o is None else o - revenue(sec, fy)


def ten_year(sec: str, basis: str = "deficit"):
    """CBO's printed ten-year total on the chosen basis, in $M."""
    o = TEN_YEAR_PRINTED[sec]
    if o is None:
        return None
    return o if basis == "outlays" else o - REVENUE_TEN_YEAR_PRINTED.get(sec, 0)


# ramp.py's six named lanes, and the residual it calls "Other + interactions".
RAMP_LANES = {
    "71119": "Work requirements",
    "71115": "Provider taxes",
    "71116": "State directed payments",
    "71101": "MSP moratorium",
    "71107": "Six-month redeterminations",
    "71102": "E&E moratorium",
}
RAMP_TEN_YR_B = {          # $B, as ramp.py types them
    "71119": 317.0, "71115": 182.7, "71116": 149.4,
    "71101": 66.0, "71107": 58.0, "71102": 53.6,
}
RAMP_OTHER_B = 60.1


def reconcile_ramp():
    """Each of ramp.py's six lanes against this workbook, on both bases,
    plus the residual it does not name."""
    out = []
    for sec, name in RAMP_LANES.items():
        out.append({
            "sec": sec, "name": name,
            "ramp_B": RAMP_TEN_YR_B[sec],
            "outlays_B": TEN_YEAR_PRINTED[sec] / 1000,
            "deficit_B": ten_year(sec) / 1000,
        })
    named_def = sum(ten_year(s) for s in RAMP_LANES)
    all_out = sum(v for v in TEN_YEAR_PRINTED.values() if v is not None)
    all_rev = sum(REVENUE_TEN_YEAR_PRINTED.values())
    all_def = all_out - all_rev
    return out, {
        "chapter1_outlays_B": all_out / 1000,
        "chapter1_revenues_B": all_rev / 1000,
        "chapter1_deficit_B": all_def / 1000,
        "named_six_deficit_B": named_def / 1000,
        "residual_deficit_B": (all_def - named_def) / 1000,
        "ramp_other_B": -RAMP_OTHER_B,
    }


# ===========================================================================
# THE SUPPLEMENTAL, AND WHAT THE $77.0B IS
# ===========================================================================
#
# SOURCE. CBO, "Supplemental Cost Estimate", 28 October 2025, publication
# 61837: P.L. 119-21, Title VII, Finance, Subtitle B, Health, Chapter 1,
# Medicaid, as enacted 4 July 2025. Same baseline as the workbook — January
# 2025 — and the same cutoff for judicial and administrative actions,
# 10 April 2025. Chapter table only; CBO publishes no section-level annual
# detail there, which is D-37.
#
# THE DISCREPANCY. The two documents share a baseline, a vintage and a
# chapter, and their six named section figures agree to the dollar. Their
# chapter totals do not:
#
#     workbook 61570, 21 sections summed   -963,787
#     supplemental, chapter table          -886,754
#                                          ---------
#                                           +77,033
#
# WHAT IT IS. Interaction netting among Chapter 1 policies. The workbook
# scores each section standing alone. The supplemental nets the overlaps —
# the same enrollee dropped by the work requirement is not dropped again by
# the six-month redetermination — and parks the netting in its seventh line,
# "Other Medicaid-Related Effects and Interactions Among Policies", which CBO
# describes as the remaining Chapter 1 policies with interactions among
# related policies included.
#
# `phasein.py` already said this: the residual is the basket "plus CBO's
# interaction netting". It was right. The netting is simply not in the
# workbook's own Interactions sheet, which scores only interactions BETWEEN
# titles and holds one entry, CAFE civil penalties against the clean vehicle
# credits, $3.0B, nothing touching Medicaid.
#
# IT RECONCILES TWO WAYS. By chapter total, +77,033. By residual —
# the supplemental's -60,100 against the workbook's fifteen unnamed sections
# at -137,085 — +76,985. The $48M between them is the rounding in a figure
# CBO prints to one decimal of a billion.
#
# WHAT IT MEANS FOR THE MODEL. `ramp.py` is on the netted basis and conserves
# against CBO's published total: its seven lanes sum to 886.8 and its
# FY29_DEFICIT of 90.146 is the supplemental's 2029 line exactly. The defect
# is narrower and real: the "Everything else" lane is not one thing. It is
# -137.1B of fifteen actual provisions and +77.0B of netting, two components
# of opposite sign that cannot share one ramp weight. `ramp.py` gives the
# basket 0.60. See `interaction()` for the year-by-year series that lets the
# two be separated.

SUPPLEMENTAL = ("CBO Supplemental Cost Estimate, 28 October 2025, "
                "publication 61837, P.L. 119-21 Title VII Subtitle B "
                "Chapter 1, chapter table")

SUP_OUTLAYS = {2025: -45, 2026: -16847, 2027: -46747, 2028: -62661,
               2029: -92944, 2030: -111441, 2031: -128616, 2032: -139659,
               2033: -150708, 2034: -164965}
SUP_REVENUES = {2025: 0, 2026: -454, 2027: -1460, 2028: -2020, 2029: -2798,
                2030: -3289, 2031: -3899, 2032: -4294, 2033: -4588,
                2034: -5078}
SUP_DEFICIT = {2025: -45, 2026: -16393, 2027: -45287, 2028: -60641,
               2029: -90146, 2030: -108152, 2031: -124717, 2032: -135365,
               2033: -146120, 2034: -159887}
SUP_TEN_YEAR = {"outlays": -914634, "revenues": -27880, "deficit": -886754}

# The supplemental's seventh line, $B, as ramp.py and phasein.py carry it.
SUP_OTHER_B = -60.1


def workbook_deficit(fy: int) -> int:
    """Chapter 1 deficit effect in $M for one year, summing the workbook's
    sections standing alone. `*` sections count as zero."""
    return chapter1(fy) - sum(revenue(s, fy) for s in SECTIONS)


def interaction(fy: int) -> int:
    """CBO's interaction netting for one fiscal year, in $M: the supplemental's
    chapter deficit less the workbook's sections summed. Positive, because
    netting gives savings back."""
    return SUP_DEFICIT[fy] - workbook_deficit(fy)


def interaction_share(fy: int) -> float:
    """Netting as a share of the summed sections. Around 8 percent from 2029
    on; this is how much a section-by-section sum overstates the chapter."""
    wd = workbook_deficit(fy)
    return 0.0 if not wd else interaction(fy) / abs(wd)


def residual_split(fy: int):
    """The 'Everything else' lane, separated. Returns the fifteen unnamed
    sections and the netting, which have opposite signs and different ramps
    and must not share a weight."""
    named = sum(d for s in RAMP_LANES
                for d in (deficit(s, fy),) if d is not None)
    return {
        "unnamed_sections": workbook_deficit(fy) - named,
        "interaction_netting": interaction(fy),
        "lane_total": workbook_deficit(fy) - named + interaction(fy),
    }


def reconcile_supplemental():
    """Both routes to the same number, and the rounding between them."""
    wd = sum(v for v in TEN_YEAR_PRINTED.values() if v) \
        - sum(REVENUE_TEN_YEAR_PRINTED.values())
    named = sum(ten_year(s) for s in RAMP_LANES)
    resid = wd - named
    by_chapter = SUP_TEN_YEAR["deficit"] - wd
    by_residual = round(SUP_OTHER_B * 1000) - resid
    return {
        "workbook_sections_summed": wd,
        "supplemental_chapter": SUP_TEN_YEAR["deficit"],
        "netting_by_chapter_total": by_chapter,
        "netting_by_residual": by_residual,
        "rounding_between_routes": by_chapter - by_residual,
        "overstatement_share": by_chapter / abs(wd),
    }
