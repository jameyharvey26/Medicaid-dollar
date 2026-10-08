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
# split. DC's directed payments are provider-tax financed, so D-41 holds here
# for the same reason it holds nationally — which is why the one DC lever we
# have derived needs no gross-up at all.
GROSS_DC = {
    "Work reporting": GROSS_EXPANSION,
    "Six-month renewals": GROSS_EXPANSION,
    "Blocked senior enrollment rule": GROSS_REGULAR,
    "Blocked Medicaid enrollment rule": GROSS_REGULAR,
    "Everything else": GROSS_BLENDED,
    "Provider tax limits": 1.000,
    "Directed payment caps": 1.000,
}

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
    assert set(GROSS_DC) == set(GROSS_NATIONAL)


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
    for k in GROSS_NATIONAL:
        print(f"  {k:<34}{GROSS_DC[k]:>8.4f}{GROSS_NATIONAL[k]:>11.3f}")
