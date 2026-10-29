# fmap_dc.py — District of Columbia match rates, and the gross-up.
#
# fmap.py is national throughout and has no state seam. Every FY2030 lever that
# removes a FEDERAL dollar needs to be converted to total-computable dollars
# before it can sit on a panel struck on total computable, and the conversion
# runs off the match rate of the population the lever touches. That rate is a
# state fact, so it lives here.
#
# DC IS NOT A FORMULA STATE. Section 4725(b) of the Balanced Budget Act of 1997
# amended section 1905(b) of the Social Security Act to set the FMAP for the
# District of Columbia, for titles XIX and XXI, at 70 percent. It is a fixed
# statutory number, not the per-capita-income formula every state gets, and it
# does not move year to year. That single fact drives most of DC's divergence
# from the national figure on every enrollment-side lever.
FMAP_SOURCE = ("Social Security Act sec. 1905(b) as amended by Balanced Budget "
               "Act of 1997 sec. 4725(b); HHS annual FMAP notice")

FMAP_DC = 0.70              # regular match, statutory
EFMAP_DC = 0.79             # title XXI enhanced, statutory
FMAP_EXPANSION = 0.90       # SSA sec. 1905(y), newly eligible adults
FMAP_ADMIN_GENERAL = 0.50   # ordinary state administration
FMAP_ADMIN_SKILLED = 0.75   # skilled professional medical personnel, systems

import basis_dc as _B

# ---- what the observed blend implies -------------------------------------
# Exhibit 16 reports DC's federal and total for benefits and for administration
# separately, so the blended rates are MEASURED, not assumed.
BENEFITS_TOTAL_M = _B.DC_TOTAL_M - _B.DC_ADMIN_M          # 4,138
BENEFITS_FED_M = _B.DC_FED_M - (_B.DC_ADMIN_M - 89.0)     # admin state = 89
ADMIN_FED_M = _B.DC_ADMIN_M - 89.0                        # 145
BLEND_BENEFITS = BENEFITS_FED_M / BENEFITS_TOTAL_M
BLEND_ADMIN = ADMIN_FED_M / _B.DC_ADMIN_M
BLEND_ALL = _B.DC_FED_M / _B.DC_TOTAL_M


def _two_rate_solve(blend, low, high):
    """Share of spending at the high rate implied by an observed blend."""
    return (blend - low) / (high - low)


# DERIVED, and the assumption is the whole of it: that DC's benefit spending is
# matched at only two rates, 70 and 90. It is not. Family planning is matched
# at 90, services through Indian Health at 100, and title XXI sits outside this
# exhibit entirely. Every one of those pushes the true expansion share BELOW
# the figure here, so this is an UPPER BOUND on the expansion share and not a
# point estimate. Published as a bound or not at all.
EXPANSION_SHARE_UPPER = _two_rate_solve(BLEND_BENEFITS, FMAP_DC, FMAP_EXPANSION)

# Same construction for administration, same caveat. The two ordinary rates are
# 50 and 75; other rates exist (90 for eligibility systems development) and
# would lower the implied skilled share.
ADMIN_SKILLED_SHARE_UPPER = _two_rate_solve(
    BLEND_ADMIN, FMAP_ADMIN_GENERAL, FMAP_ADMIN_SKILLED)


# ---- the gross-up ---------------------------------------------------------
# A lever scored in federal dollars becomes total-computable dollars by
# dividing by the match rate of the population it touches. The national model
# carries these as a GROSS dict of typed factors; here they are derived from
# the statutory rates so that a rate change moves them.
def gross_up(fed_rate: float) -> float:
    return 1.0 / fed_rate


GROSS_EXPANSION = gross_up(FMAP_EXPANSION)       # 1.1111
GROSS_REGULAR = gross_up(FMAP_DC)                # 1.4286
GROSS_BLENDED = gross_up(BLEND_ALL)              # 1.3667

# WHICH LEVER TAKES WHICH, following the national model's own assignment:
#   work reporting, six-month renewals      expansion adults   -> GROSS_EXPANSION
#   blocked senior / Medicaid enrolment     regular            -> GROSS_REGULAR
#   everything else                         blended            -> GROSS_BLENDED
#   provider tax limits                     NONE (D-39)        -> 1.000
#   directed payment caps                   NONE (D-41)        -> 1.000
#
# The two 1.000 lanes are not an oversight. The provider tax lane funds the
# state's own match rather than drawing one, and directed payment financing is
# split.
GROSS_DC = {
    "Work reporting": GROSS_EXPANSION,
    "Six-month renewals": GROSS_EXPANSION,
    "Blocked senior enrollment rule": GROSS_REGULAR,
    "Blocked Medicaid enrollment rule": GROSS_REGULAR,
    "DC provisions not separately scored": GROSS_BLENDED,
    "Provider tax limits": 1.000,
    "Directed payment caps": 1.000,
}

# ---------------------------------------------------------------------------
# WHICH DC LEVERS ACTUALLY USE THIS TABLE — and it is fewer than it looks.
#
# The gross-up exists to convert a lever scored in FEDERAL dollars into total
# computable dollars. That is the national route: CBO scores federal, the
# panel is struck on total computable, so every lane is multiplied up.
#
# As of 2026-10-29 the four derived DC levers do not come that way. Each is
# derived from a District figure that is ALREADY total computable — DHCF's
# Group 8 program line, the Dedicated Taxes line, the SDP preprint total. A
# gross-up applied on top of those would inflate every one of them by the
# reciprocal of a match rate that has already been accounted for.
#
# So: this table governs any DC lever derived the NATIONAL way, and the levers
# below bypass it. The distinction is mechanical, not stylistic, and it is the
# kind of thing that silently doubles a lane if nobody writes it down.
DERIVED_IN_TOTAL_COMPUTABLE = {
    "Work reporting", "Six-month renewals",
    "Provider tax limits", "Directed payment caps",
}

# D-41 AND THE MEASURED SPLIT. JW, 2026-10-29 (Q5): a state fact beats a
# national decision taken in the absence of one. D-41 sets the national
# directed-payment gross-up to 1.000 because SDP financing is split and the
# split was not known. DC's split IS known — 77.51 percent federal on the
# FY2025 preprint — so DC's 1.000 is no longer an inheritance. It is 1.000 for
# a different and better reason: the DC figure is already total computable.
# The measured split is carried for the federal / non-federal division of the
# flow, which is where it actually bears.
SDP_FEDERAL_SHARE_DC = 376_029_678.0 / 485_154_441.0
SDP_SPLIT_SOURCE = ("CMS approved preprint "
                    "DC_Fee_IPH.OPH_New_20241001-20250930: total up to "
                    "$485,154,441, federal share $376,029,678")
REOPEN_D41 = ("A measured financing split in the first state panel is "
              "evidence about the NATIONAL model, not only about DC. D-41 "
              "should be re-opened with this on the table.")

# THE PROVIDER TAX LANE IS A DC DIVERGENCE, DECLARED NOT RESOLVED.
# D-39 sets the provider tax gross-up to 1.000 nationally because the lane
# funds the state's own match rather than drawing one. In the District the
# dedicated tax IS the non-federal share and it DOES draw match, so a dollar
# of tax that is never collected costs more than a dollar of Medicaid. The
# multiplier is not established: the dedicated-tax line funds more than the
# SDP, and the SDP's own non-federal share ($109.1M) is smaller than the tax
# line ($235.3M), so the two cannot be divided into each other. Published at
# the non-federal level, which is conservative and keeps the DC lane on the
# same basis as the national one.
PROVIDER_TAX_GROSS_DC = None              # ABSENT, declared
PROVIDER_TAX_GROSS_NOTE = (
    "DC's dedicated tax draws federal match, so the total-computable effect "
    "exceeds the tax figure. The multiplier is not established and the lane "
    "is published at the non-federal level. This is a divergence from D-39, "
    "not an application of it.")

# The national figures, for the comparison that is the point of the exercise.
GROSS_NATIONAL = {
    "Work reporting": 1.136,
    "Six-month renewals": 1.136,
    "Blocked senior enrollment rule": 1.701,
    "Blocked Medicaid enrollment rule": 1.701,
    "Everything else": 1.545,
    "Provider tax limits": 1.000,
    "Directed payment caps": 1.000,
}


def _check():
    assert abs(BLEND_ALL - 0.731702) < 1e-5, BLEND_ALL
    assert 0.0 < EXPANSION_SHARE_UPPER < 1.0
    assert GROSS_REGULAR < GROSS_NATIONAL["Blocked senior enrollment rule"], (
        "DC's statutory 70% must make its regular-match gross-up SMALLER "
        "than the national blend; if this flips, something is wrong")
    assert set(GROSS_DC) - {"DC provisions not separately scored"} == \
        set(GROSS_NATIONAL) - {"Everything else"}, (
            "the DC lever set differs from the national one only by the "
            "renamed residual lane")
    assert DERIVED_IN_TOTAL_COMPUTABLE <= set(GROSS_DC)
    for _k in ("Provider tax limits", "Directed payment caps"):
        assert GROSS_DC[_k] == 1.000
    assert 0.70 < SDP_FEDERAL_SHARE_DC < 0.85
    assert PROVIDER_TAX_GROSS_DC is None, (
        "the DC provider tax multiplier is declared absent; if a figure is "
        "set here the lane's basis changes and the panel note must change too")


_check()


if __name__ == "__main__":
    print("DC match rates, statutory\n")
    print(f"  regular FMAP (sec. 1905(b), fixed)   {FMAP_DC:>8.2%}")
    print(f"  enhanced FMAP, title XXI             {EFMAP_DC:>8.2%}")
    print(f"  expansion, newly eligible            {FMAP_EXPANSION:>8.2%}")
    print()
    print("observed blends, from Exhibit 16 (measured)\n")
    print(f"  benefits                             {BLEND_BENEFITS:>8.2%}")
    print(f"  administration                       {BLEND_ADMIN:>8.2%}")
    print(f"  all Medicaid                         {BLEND_ALL:>8.2%}")
    print()
    print("implied, as UPPER BOUNDS only (two-rate assumption)\n")
    print(f"  expansion share of benefit dollars  <={EXPANSION_SHARE_UPPER:>8.2%}")
    print(f"  skilled share of admin dollars      <={ADMIN_SKILLED_SHARE_UPPER:>8.2%}")
    print()
    print("gross-up, federal dollars -> total computable\n")
    print(f"  {'lever':<34}{'DC':>8}{'national':>11}")
    _rename = {"Everything else": "DC provisions not separately scored"}
    for k in GROSS_NATIONAL:
        dc_key = _rename.get(k, k)
        mark = "  (bypassed)" if dc_key in DERIVED_IN_TOTAL_COMPUTABLE else ""
        print(f"  {dc_key:<40}{GROSS_DC[dc_key]:>8.4f}"
              f"{GROSS_NATIONAL[k]:>11.3f}{mark}")
    print()
    print("  bypassed: derived from a District figure that is already total")
    print("  computable, so the table does not apply. See "
          "DERIVED_IN_TOTAL_COMPUTABLE.")
    print(f"  SDP federal share, measured            "
          f"{SDP_FEDERAL_SHARE_DC:>8.4f}")
    print(f"  provider tax multiplier                  "
          f"{'ABSENT':>8}  (D-39 divergence, declared)")
