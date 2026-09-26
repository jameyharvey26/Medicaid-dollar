# basis_national.py — the national dollar basis, in one place.
#
# D-83. These constants and the lane derivation below used to live in
# ledger_national_2024.py, while provider_mix.py carried its own typed copies
# of the three lane values it needed (41.08, 35.65, 9.69, struck on the old
# hundred). Two copies of the same figures, one of which nothing checked.
#
# ledger_national_2024.py and provider_mix.py both read this module, so there
# is one derivation and it promulgates. Nothing here computes a provider mix
# or builds a ledger; it is the arithmetic of the denominator and the lanes,
# and nothing else.
#
# Sources are named in ledger_national_2024.py, which is where the Fig objects
# that carry provenance are built. The dollars are Exhibit 16 and Exhibit 17,
# FY2024, MACPAC February 2026, CMS-64 FMR as of 3 June 2025.

# ---- Exhibit 16, total row, in millions ----------------------------------
BENEFITS_M = 908839.0
ADMIN_M = 40360.0
MFCU_M, SNC_M = 497.0, 468.0        # federal oversight, 75% FFP
VFC_M = 7239.0                      # Vaccines for Children, 100% federal
FED_M, ST_M = 620355.0, 337048.0

# ---- Exhibit 17, total row, in millions -----------------------------------
MEDICARE_M = 27774.0                # Medicare premiums and coinsurance
CAP_M = 496097.0                    # managed care and premium assistance
FFS_M = 400002.0                    # fee for service, nine columns
COLL_M = -15201.0                   # third-party liability, estate, other
DUAL_CAP_M = 106000.0               # triangulated; softest figure in the model

# Exhibit 17 breaks the wrap-around node's fee-for-service half into two
# published lines. The node total was previously typed as their sum; it is
# derived here so the ordering claim in the body text rests on the source
# rather than on a figure carried by hand. S-073.
HOSPITAL_M = 91443.0
PHYSICIAN_M = 9534.0
DENTAL_M = 6186.0
OTHER_PRACTITIONER_M = 3660.0
CLINIC_M = 19295.0                  # clinic, health center, FQHC, birth center
OTHER_ACUTE_M = 55098.0
DRUGS_M = 20206.0                   # net of rebates; see the note below
INSTITUTIONAL_LTSS_M = 64628.0
HCBS_M = 129952.0

# The five diagram nodes, mapped from the nine published columns. The mapping
# is the only judgement here and it is written out so a reader can disagree
# with it; the dollars are Exhibit 17's own.
LTC_FFS_M = INSTITUTIONAL_LTSS_M + HCBS_M                      # 194,580
WRAP_FFS_M = OTHER_ACUTE_M + DENTAL_M                          #  61,284
PHYS_FFS_M = PHYSICIAN_M + CLINIC_M + OTHER_PRACTITIONER_M     #  32,489
FFS_TOTAL_M = (LTC_FFS_M + HOSPITAL_M + WRAP_FFS_M
               + PHYS_FFS_M + DRUGS_M)                         # 400,002

# DRUG REBATES are not visible anywhere on this panel and are not the same
# thing as collections. Exhibit 17 reports fee-for-service drugs net of
# rebates, and folds managed-care drug rebates into the managed care line.
# Neither is separable from the spending it nets against, so the panel cannot
# show a rebate flow without inventing one. Declared, not estimated. Open.

# ---- the hundred ----------------------------------------------------------
# D-70. Struck where the money becomes a Medicaid dollar: at the state agency,
# budgeted and cost-allocated. Not at appropriation. Vaccines for Children
# peels before it and is outside.
HUNDRED_M = BENEFITS_M + ADMIN_M + MFCU_M + SNC_M          # 950,164
PER_DOLLAR = HUNDRED_M / 100.0
OLD_HUNDRED_M = HUNDRED_M + VFC_M                          # what it used to be
RESCALE = OLD_HUNDRED_M / HUNDRED_M                        # x1.00762


def per100(m: float) -> float:
    return m / PER_DOLLAR


# ---- the payer lanes ------------------------------------------------------
# What is left after the three things that peel before the payers. Every lane
# is a share of THIS, so the three sum to it by construction and the claims
# total is the same number read down the page or across it.
REACHES_PAYERS = 100.0 - per100(ADMIN_M + MFCU_M + SNC_M + MEDICARE_M)

# COLLECTIONS. Exhibit 17 reports them as a single unallocated negative: the
# source declines to say which lane recovered the money. Gross lanes are
# $94.31 per $100 against the $92.73 that reaches the payers, and the $1.60 of
# collections is exactly that gap. Folded pro rata by share of gross — the
# convention the workbook has always used, now written down. A MODELLED
# allocation of a MEASURED total; the key is ours because the source publishes
# none. MACPAC computes its own service shares exclusive of collections rather
# than distributing them, which is the same refusal.
_GROSS_M = CAP_M + FFS_M
COLL_100 = per100(COLL_M)                       # -1.60, reported not drawn
CAP_100 = REACHES_PAYERS * CAP_M / _GROSS_M
FFS_100 = REACHES_PAYERS * FFS_M / _GROSS_M
DUAL_100 = CAP_100 * DUAL_CAP_M / CAP_M
MCO_100 = CAP_100 - DUAL_100

# Plan retention is struck against the old hundred and converts; the lanes do
# not, because they are derived on the current one. Care is what is left.
MCO_ADM, DUAL_ADM = 3.81 * RESCALE, 1.04 * RESCALE
MCO_MARGIN, DUAL_MARGIN = 0.60 * RESCALE, 0.16 * RESCALE
MCO_CARE = MCO_100 - MCO_ADM - MCO_MARGIN
DUAL_CARE = DUAL_100 - DUAL_ADM - DUAL_MARGIN
FFS_CARE = FFS_100                     # Rule A: no payer, no retention
CLAIMS_100 = MCO_CARE + DUAL_CARE + FFS_CARE

if __name__ == "__main__":
    print(f"hundred          {HUNDRED_M:>12,.0f} $M")
    print(f"reaches payers   {REACHES_PAYERS:>12.6f}")
    print(f"  mco            {MCO_100:>12.6f}")
    print(f"  dual           {DUAL_100:>12.6f}")
    print(f"  ffs            {FFS_100:>12.6f}")
    print(f"  sum            {MCO_100+DUAL_100+FFS_100:>12.6f}")
    print(f"collections      {COLL_100:>12.6f}")
    print(f"claims paid      {CLAIMS_100:>12.6f}")
