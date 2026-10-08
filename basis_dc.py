# basis_dc.py — the District of Columbia dollar basis, in one place.
#
# The same move D-83 made nationally, for the same reason. These constants and
# SCALE lived in ledger_dc_2024.py, which was fine while DC had one panel.
# DC FY2030 is now in scope and needs the identical denominator: two ledgers
# reading one basis, rather than two copies of four dollar figures with
# nothing checking that they agree.
#
# Nothing here builds a ledger or decides a lane. It is the arithmetic of the
# denominator, and the declarations about what the denominator is not.
#
# S-105: the dollars below are typed because they are read off a published
# exhibit. Every per-$100 figure is divided by SCALE at the point of use and
# is typed nowhere, so a revised exhibit moves the whole panel through one
# line.

# ---- sources --------------------------------------------------------------
EX16 = ("MACPAC, MACStats: Medicaid and CHIP Data Book, Exhibit 16, Medicaid "
        "Spending by State, Category, and Source of Funds, FY 2024, published "
        "February 2026; MACPAC analysis of CMS-64 FMR net expenditure data as "
        "of 3 June 2025")
EX17 = ("MACPAC, MACStats: Medicaid and CHIP Data Book, Exhibit 17, Total "
        "Medicaid Benefit Spending by State and Category, FY 2024, published "
        "February 2026; MACPAC analysis of CMS-64 FMR net expenditure data as "
        "of 3 June 2025")
DHCF_BUDGET = ("Government of the District of Columbia, FY2027 Proposed Budget "
               "and Financial Plan, Department of Health Care Finance (HT0), "
               "agency financial summary, FY2024 actual")

# ---- Exhibit 16, District of Columbia row, in millions ---------------------
#   Total Medicaid, DC, FY 2024   $4,372M   ->  SCALE
#     federal                     $3,199M
#     state                       $1,173M
#   State program administration    $234M   ->  peel.admin
#
# The exhibit's own note: figures may change if a state revises its
# expenditure data after certification.
DC_TOTAL_M = 4372.0
DC_FED_M = 3199.0
DC_STATE_M = 1173.0
DC_ADMIN_M = 234.0

# ---- Exhibit 17, District of Columbia row, in millions --------------------
#   Fee-for-service, nine columns        $2,260M
#   Managed care and premium assistance  $1,802M
#   Medicare premiums and coinsurance       $86M   ->  peel.medicare
#   Collections                            -$10M
#   Total spending on benefits           $4,138M
#   plus state program administration      $234M
#   = total computable, Exhibit 16       $4,372M
DC_MEDICARE_M = 86.0

# ---- the non-federal share, by instrument ---------------------------------
# Exhibit 16 reports a single non-federal share; DC's appropriation splits it,
# and one part is not a general-fund appropriation at all. Dedicated Taxes are
# provider assessments levied on the hospitals and nursing facilities at the
# right-hand end of this diagram, used as the non-federal share, matched, and
# paid back to those same provider classes.
#
# Basis warning, carried forward: the dedicated-tax figure is an
# appropriation and the state share is CMS-64, so the local-appropriation
# residual has parents in two accountings and is DERIVED, not measured.
DC_DEDTAX_M = 114.647

# ---- the hundred ----------------------------------------------------------
# D-70, struck where the money becomes a Medicaid dollar: at the state agency.
SCALE = DC_TOTAL_M / 100.0


def per100(m: float) -> float:
    return m / SCALE


# ---- what this hundred is NOT, declared ------------------------------------
#
# 1. NO FEDERAL OVERSIGHT PEEL. The national hundred includes Medicaid Fraud
#    Control Units and survey-and-certification. Exhibit 16 publishes those as
#    national lines only; its note says state-level estimates exist but are not
#    shown. DC's hundred therefore omits an element the national hundred
#    includes. Bounded, not guessed: the two are 0.102% of the national
#    hundred, which on DC's total is on the order of $4M, so the comparability
#    effect is about a tenth of a cent per $100. Declared rather than
#    estimated; acquiring the state-level figure would close it.
#
# 2. NO VACCINES FOR CHILDREN LINE, hence no RESCALE. Nationally VFC peels
#    before the hundred and the old-hundred conversion exists to carry figures
#    struck against it. DC has no published VFC row and no legacy figures
#    struck on a different hundred, so there is no DC analogue of
#    basis_national.RESCALE. Do not import one.
#
# 3. ALLIANCE AND THE IMMIGRANT CHILDREN'S PROGRAM ARE OUTSIDE THIS HUNDRED,
#    and this is a boundary rather than an omission. Both are locally funded,
#    draw no federal match, and are not Title XIX, so neither appears on the
#    CMS-64 and neither belongs in a Medicaid dollar. DHCF's FY2024 actual
#    carries them at $147.448M and $19.114M, $166.562M together, as sibling
#    line items inside the same agency.
#
#    This is not idle. DISB required an amended CY2023 statement from one plan
#    for precisely this reason: Alliance and ICP had been booked in the Title
#    XIX column, and moving them out reduced that plan's reported Medicaid
#    premium from $313.220M to $280.742M. A tenth of the column was not
#    Medicaid. Any DC figure sourced from a plan filing has to be checked
#    against this boundary before it is used.
#
#    If Alliance is ever drawn, it belongs upstream of the ledger as context
#    showing local appropriation dividing into the state share that draws
#    match and the part that does not. Drawing it inside the flow and peeling
#    it out would break conservation at the first node.
DC_ALLIANCE_MCO_M = 147.448        # DHCF FY2024 actual, H02707
DC_ICP_MCO_M = 19.114              # DHCF FY2024 actual, H02710
DC_LOCAL_ONLY_M = DC_ALLIANCE_MCO_M + DC_ICP_MCO_M

# 4. THE HUNDRED IS WIDER THAN DHCF. About $171M of non-federal Medicaid
#    spending sits outside DHCF's appropriation: DHCF's own non-federal funds
#    are $1,168.573M, of which $166.562M is Alliance and ICP, leaving roughly
#    $1,002M against Exhibit 16's state share of $1,173M. The residual is
#    local money spent by sister agencies and certified as the non-federal
#    share. This is the arithmetic reason the hundred cannot be struck on
#    DHCF's own program figure: that figure would omit it by construction.
DC_DHCF_NONFEDERAL_M = 1168.573    # local + dedicated taxes + special purpose
DC_OUTSIDE_DHCF_M = DC_STATE_M - (DC_DHCF_NONFEDERAL_M - DC_LOCAL_ONLY_M)


def _check():
    """Internal agreement. Fails the import rather than the panel."""
    assert abs(SCALE * 100.0 - DC_TOTAL_M) < 1e-9
    assert abs((DC_FED_M + DC_STATE_M) - DC_TOTAL_M) < 1.0, (
        "Exhibit 16 federal + state must reconcile to total within rounding")
    assert DC_ADMIN_M < DC_TOTAL_M
    assert DC_LOCAL_ONLY_M > 0


_check()


if __name__ == "__main__":
    print(f"DC hundred              {DC_TOTAL_M:>12,.1f} $M")
    print(f"  federal               {DC_FED_M:>12,.1f}   "
          f"{per100(DC_FED_M):>8.4f} per $100")
    print(f"  state                 {DC_STATE_M:>12,.1f}   "
          f"{per100(DC_STATE_M):>8.4f} per $100")
    print(f"  of which dedicated    {DC_DEDTAX_M:>12,.3f}   "
          f"{per100(DC_DEDTAX_M):>8.4f} per $100")
    print(f"state admin peel        {DC_ADMIN_M:>12,.1f}   "
          f"{per100(DC_ADMIN_M):>8.4f} per $100")
    print(f"medicare peel           {DC_MEDICARE_M:>12,.1f}   "
          f"{per100(DC_MEDICARE_M):>8.4f} per $100")
    print()
    print(f"outside the hundred, local only  {DC_LOCAL_ONLY_M:>10,.3f} $M")
    print(f"non-federal outside DHCF         {DC_OUTSIDE_DHCF_M:>10,.3f} $M")
