"""
fmap.py - Per-lane FMAP gross-up rates for the HR-1 overlay. Closes D-26 task 1.

CBO scores federal dollars. The $100 ledger is total computable (federal + state).
Each lane must be grossed up by 1/FMAP, at the rate applicable to THAT lane's
population or financing mechanism. Using the all-population blend everywhere
overstates expansion lanes by ~39% and understates non-expansion lanes by ~10%.

Companion to financing.py, which holds the non-federal-share side.

DERIVED FROM PRIMARY DATA, not from secondary citation:
  CMS-64 New Adult Group Expenditures, data.medicaid.gov dataset
  00505e90-f8ac-5921-b12f-5e23ba7ffcf3, National Totals rows, four FY2024
  quarters (QE 12/31/2023, 3/31/2024, 6/30/2024, 9/30/2024), updated Feb 2026.
  Retrieved 2026-08-27. See CMS64_FY2024 below for the raw inputs, so every
  rate here can be recomputed rather than trusted.

SCOPE: Medical Assistance Payments only. Administration is NOT in this dataset
(federal MAP $595.0B vs MACStats total federal $620.4B; ~$25B of federal admin
sits outside). Correct basis for benefit-loss lanes. WRONG basis for D-32.
"""

# ---------------------------------------------------------------------------
# Raw inputs. National Totals, $ as reported.
# ---------------------------------------------------------------------------
CMS64_FY2024 = {
    # quarter: (total_computable, federal, VIII_tc, VIII_fed, newly_tc, newly_fed)
    "QE_2023-12-31": (221_217_414_003, 145_794_786_900, 44_259_341_593,
                      39_118_379_522, 35_775_091_880, 32_219_194_488),
    "QE_2024-03-31": (228_906_909_741, 147_865_752_269, 48_093_119_514,
                      42_535_896_245, 39_452_092_416, 35_537_322_505),
    "QE_2024-06-30": (227_245_953_466, 146_429_184_056, 45_504_821_894,
                      40_127_792_187, 36_381_275_750, 32_777_269_688),
    "QE_2024-09-30": (241_975_839_213, 154_867_607_180, 48_390_506_343,
                      42_209_268_959, 37_311_646_342, 33_585_079_072),
}

_tc  = sum(v[0] for v in CMS64_FY2024.values())
_fed = sum(v[1] for v in CMS64_FY2024.values())
_vtc = sum(v[2] for v in CMS64_FY2024.values())
_vfd = sum(v[3] for v in CMS64_FY2024.values())
_ntc = sum(v[4] for v in CMS64_FY2024.values())
_nfd = sum(v[5] for v in CMS64_FY2024.values())

BLENDED_ALL          = _fed / _tc                      # 0.6472
EXPANSION_EFFECTIVE  = _vfd / _vtc                     # 0.8805
NEWLY_ELIGIBLE_ONLY  = _nfd / _ntc                     # 0.9006
NON_EXPANSION        = (_fed - _vfd) / (_tc - _vtc)    # 0.5879

# FFCRA CAVEAT, measured not assumed. The enhanced match ran through Dec 2023,
# so QE_2023-12-31 carries a residual 1.5pp enhancement. Non-expansion computes
# to 60.28% in that quarter against 58.2-58.5% in the three clean ones. Using
# the clean three quarters instead gives NON_EXPANSION = 0.5831, a 0.5pp
# difference. Full FY2024 retained for consistency with D-07's FY basis; the
# clean-quarter alternative is here so the choice is visible, not buried.
NON_EXPANSION_FFCRA_CLEAN = 0.5831

# ---------------------------------------------------------------------------
# Per-lane rates
# ---------------------------------------------------------------------------
# None means genuinely unknown -> hard stop, per S-035. Do not fill with a guess.

LANES = {
    "Work reporting": {
        "section": "71119",
        "rate": EXPANSION_EFFECTIVE,
        "basis": "ACA expansion adult group (VIII), measured effective rate",
        "rationale": (
            "D-43. Applies to nonpregnant, nondisabled adults 19-64 eligible via "
            "the expansion pathway or an 1115 MEC-equivalent waiver, i.e. the VIII "
            "group as a whole. The VIII group is NOT uniformly at 90%: newly "
            "eligible spending measures 90.06%, matching the statutory rate at "
            "SSA 1905(y)(1), but not-newly-eligible spending is 20% of the group "
            "and measures 80.03%. Blended, 88.05%. Using 90% understates the "
            "gross-up on the largest lane by roughly $8B over ten years."),
        "status": "SETTLED",
    },
    "Six-month renewals": {
        "section": "71107",
        "rate": EXPANSION_EFFECTIVE,
        "basis": "Same population as work reporting",
        "rationale": (
            "SSA 1902(e)(14)(L) as added by 71107 reaches the expansion adult "
            "group and the 1115 equivalent only; all other groups stay on 12-month "
            "renewal. Same VIII composition, same 88.05%."),
        "status": "SETTLED",
    },
    "Blocked Medicaid enrollment rule": {
        "section": "71102",
        "rate": NON_EXPANSION,
        "basis": "Non-expansion blended, derived",
        "rationale": (
            "CBO's supplemental narrates the blocked provisions as limiting annual "
            "determinations to aged/blind/disabled enrollees, barring in-person "
            "redetermination interviews, and adding steps before terminating for "
            "returned mail. Weighted to non-MAGI aged and disabled enrollees, who "
            "are non-expansion. 64.7% is a blend containing 88% expansion money and "
            "understates this lane by about 10%. CHIP/BHP contamination appears "
            "small: the scored provisions CBO describes are Medicaid."),
        "status": "SETTLED",
    },
    "Blocked senior enrollment rule": {
        "section": "71101",
        "rate": NON_EXPANSION,
        "basis": "Non-expansion blended, derived; QI carve-out OUTSTANDING",
        "rationale": (
            "Medicare Savings Programs for dual eligibles, a non-expansion "
            "population. BUT the three MSP categories do not share a rate: QMB and "
            "SLMB match at regular FMAP, while QI is 100% FEDERAL from a capped "
            "allotment (CMS SMD 10-003). The QI portion grosses up at 1.000, not "
            "1.701. Rate below is the QMB/SLMB treatment only."),
        "status": "SETTLED",
        # D-44. QI carve-out set to ZERO on a STRUCTURAL argument, not a measured
        # split. QI is a capped federal entitlement: states enrol first-come,
        # first-served and stop when the year's allotment is exhausted (unlike
        # QMB/SLMB, which have no cap). Blocking a rule that would have raised
        # enrolment therefore produces no federal QI savings, because the ceiling
        # binds the spending rather than the enrolment. The pot is the same size
        # either way; it just runs out sooner.
        #
        # Scale corroborates independently: MACRA allocated $980M for CY2016, so
        # ~$1B/yr is the ENTIRE programme, against a lane scored at $66B/10yr.
        #
        # BOUND: if QI were 15% of the lane (its ENROLMENT share, and a hard upper
        # bound since QI pays less per person than QMB) the lane would be $105.3B
        # rather than $112.3B. 6% of one lane, under 1% of the overlay.
        #
        # OPEN CAVEAT for the footnote, not modelled: MACRA established a formula
        # for future allotments. Whether that formula is responsive to enrolment is
        # unverified. If allotments rise with prior-year uptake, some QI sensitivity
        # returns over a ten-year window.
        #
        # DO NOT substitute MACPAC's 53/32/15 MSP split here. That is ENROLMENT.
        # QMB pays premiums plus all cost sharing; SLMB and QI pay the Part B
        # premium only. Using it as a spending share is S-034.
        "qi_share": 0.0,
        "qi_share_upper_bound": 0.15,
    },
    "Everything else": {
        "section": "residual",
        "rate": BLENDED_ALL,
        "basis": "All-population blend",
        "rationale": (
            "Cost sharing, immigrant eligibility, retroactive coverage, minor items "
            "and CBO's interaction netting (D-35). Genuinely mixed, so the "
            "all-population blend is the honest expression of an unknown mix. "
            "MODELLED - flag on artifact."),
        "status": "PROVISIONAL",
    },
    "Provider tax limits": {
        "section": "71115",
        "rate": None,       # No gross-up applies at all.
        "basis": "D-39 - exempt from D-25",
        "rationale": (
            "No population rate applies. Grossing up manufactures a state share "
            "that was never state money: the non-federal share of a provider-tax-"
            "financed payment is the providers' own money recycled. Providers lose "
            "the federal match; the general-fund-substituting portion moves to the "
            "second ledger (D-40). See financing.py."),
        "status": "RESOLVED - no gross-up",
    },
    "Directed payment caps": {
        "section": "71116",
        "rate": None,       # Splits three ways.
        "basis": "D-41 - splits by financing source",
        "rationale": (
            "Provider-tax financed behaves as 71115 (no gross-up). IGT financed "
            "likewise, but lands on local rather than state government. State "
            "general fund financed grosses up at full strength, at the "
            "payment-weighted FMAP of the affected managed care rate cells, which "
            "sits between the non-expansion and expansion rates. Blocked on the "
            "tax-vs-IGT split held in financing.py."),
        "status": "SETTLED - split, see sdp_split()",
    },
}

# Ten-year CBO figures from ramp.py, $B.
# BASIS WARNING: these are the DEFICIT series. D-26's own illustrative figures
# reverse-engineer to the OUTLAY series ($325.6B for 71119 vs $317.0B here), an
# $8.6B section-level wedge. Open task 2. Rates above are basis-agnostic; these
# dollar results are not, and move when task 2 resolves.
TEN_YR_DEFICIT = {
    "Work reporting": 317.0,
    "Six-month renewals": 58.0,
    "Blocked senior enrollment rule": 66.0,
    "Blocked Medicaid enrollment rule": 53.6,
    "Provider tax limits": 182.7,
    "Directed payment caps": 149.4,
    "Everything else": 60.1,
}


# D-46. SDP financing mix, from ASPE 2026: $8.4B of $12.3B of the non-federal
# share of 2022 SDP spending was provider-tax or IGT financed.
SDP_PROVIDER_FINANCED = 8.4 / 12.3
SDP_GENERAL_FUND      = 1.0 - SDP_PROVIDER_FINANCED

# Rate applied to the general-fund-financed slice only. MODELLED: SDPs cover
# hospital, nursing facility and academic-medical-centre physician services used
# across every eligibility group, and no payment-weighted managed care rate is
# published. The all-population blend is the honest expression of that. Flag on
# artifact.
SDP_GENERAL_FUND_RATE = BLENDED_ALL

# The tax/IGT split is NOT separated. MACPAC recommended Congress require states
# to report non-federal share by source (general funds, health care taxes, IGTs,
# CPEs); Congress has not acted, so every published figure combines taxes and
# IGTs. For the FIRST ledger the distinction is immaterial - both recycle, both
# exempt from gross-up. It matters only for which line of the second ledger
# receives it, and D-03 node 4 already reads "state and local". Revisit for state
# editions, where single-state preprints make it tractable.
SDP_TAX_VS_IGT_SPLIT = None   # deliberately unresolved, not blocking


def sdp_split(fed=149.4):
    """D-41/D-46. Directed payment caps, split by financing source."""
    prov = fed * SDP_PROVIDER_FINANCED
    genf = fed * SDP_GENERAL_FUND
    return {
        "provider_and_local_financed_fed": prov,
        "provider_and_local_financed_total": None,   # no gross-up applies
        "general_fund_financed_fed": genf,
        "general_fund_financed_total": genf / SDP_GENERAL_FUND_RATE,
        "state_relief": genf / SDP_GENERAL_FUND_RATE - genf,
    }


def table():
    rows = []
    for name, d in LANES.items():
        fed = TEN_YR_DEFICIT[name]
        if d["rate"] is None:
            rows.append((name, d["section"], None, None, fed, None, d["status"]))
        else:
            r = d["rate"]
            rows.append((name, d["section"], r, 1 / r, fed, fed / r, d["status"]))
    return rows


if __name__ == "__main__":
    print(f"Derived from CMS-64 FY2024 (MAP only, four quarters):")
    print(f"  All-population blend      {BLENDED_ALL:7.2%}   (validates D-10's 64.7%)")
    print(f"  VIII newly eligible       {NEWLY_ELIGIBLE_ONLY:7.2%}   (validates statutory 90%)")
    print(f"  VIII group effective      {EXPANSION_EFFECTIVE:7.2%}   <- D-43")
    print(f"  Non-expansion blended     {NON_EXPANSION:7.2%}   <- unblocks 3 lanes")
    print()
    print(f"{'Lane':34}{'§':>7}{'rate':>9}{'x':>8}{'fed $B':>9}{'total $B':>10}  status")
    print("-" * 105)
    tot_f = tot_t = 0.0
    for n, s, r, f, fed, tot, st in table():
        rs = f"{r:.2%}" if r else "n/a"
        fs = f"{f:.3f}" if f else "n/a"
        ts = f"{tot:.1f}" if tot else "--"
        print(f"{n:34}{s:>7}{rs:>9}{fs:>8}{fed:>9.1f}{ts:>10}  {st}")
        tot_f += fed
        tot_t += tot or 0
    print("-" * 105)
    print(f"{'TOTAL (grossed lanes only)':34}{'':>7}{'':>9}{'':>8}{tot_f:>9.1f}{tot_t:>10.1f}")
    print()
    print("Two lanes carry no gross-up by decision (D-39, D-41); their federal")
    print("figures are NOT summed into the total-computable column.")
