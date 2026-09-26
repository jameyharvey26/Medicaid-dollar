# signatures.py — who signed what, and at which value.
#
# THE HOLE THIS CLOSES. The signature used to be one line in the ledger
# module, stamped onto every measured and modelled figure at build time. It
# recorded the value at the instant of stamping, in the same process, so it
# could catch a figure edited after signing inside one run — which is what the
# break test exercises — and could never catch a figure whose source constant
# changed between sessions. On 16 September the provider phase moved and JW's
# 15 September signature was carried onto four node totals he had never seen.
# Nothing reported it. Every gate passed.
#
# A signature is now a fact written down here: a key, the exact value that was
# agreed, and who agreed it. `_sign` matches the ledger against this register.
# If a figure has moved, it does not get signed, `check` reports it LAPSED and
# the build fails. Correcting a figure therefore costs a deliberate line here,
# which is the point.
#
# S-093, JW 16 September: no signature without a stacked before-and-after of
# every panel the change touches, rendered full width, with the changed
# figures named above it. The register is the record that this happened.

REVIEW = "2026-09-18 JW"

# Signed 2026-09-16 on the stacked FY2024 and FY2030 comparison sheets, after
# the MACPAC behavioral health carve was adopted. The two EN-43 earnings
# margins remain deliberately unsigned; EN-43 states that the $0.76 has no
# primary source, and signing it would assert that someone opened a document
# the register says does not exist.
UNSIGNED = {
    "payer.dual.margin",
    "payer.mco.margin",
}

# LAPSED 2026-09-18 by D-70. The $100 was re-struck at the state agency
# rather than at appropriation, so the denominator moved from $957,403M to
# $950,164M and every figure below it rose about 0.76 percent. Kept as the
# record of what was agreed on 16 September, and at what value. These are
# not signatures.
LAPSED_2026_09_16 = {
    'beneficiaries.row.Adults': 29.56,
    'beneficiaries.row.Aged': 18.41,
    'beneficiaries.row.Children': 13.48,
    'beneficiaries.row.Disabled': 24.98,
    'claims.cell.dual.Behavioral health': 1.35,
    'claims.cell.dual.Hospitals': 2.03,
    'claims.cell.dual.Long-term care': 1.91,
    'claims.cell.dual.Other': 2.06,
    'claims.cell.dual.Physicians & clinics': 1.78,
    'claims.cell.dual.Rx drugs': 0.56,
    'claims.cell.ffs.Behavioral health': 3.18,
    'claims.cell.ffs.Hospitals': 8.27,
    'claims.cell.ffs.Long-term care': 19.98,
    'claims.cell.ffs.Other': 5.69,
    'claims.cell.ffs.Physicians & clinics': 2.45,
    'claims.cell.ffs.Rx drugs': 1.51,
    'claims.cell.mco.Behavioral health': 4.97,
    'claims.cell.mco.Hospitals': 7.47,
    'claims.cell.mco.Long-term care': 7.02,
    'claims.cell.mco.Other': 7.58,
    'claims.cell.mco.Physicians & clinics': 6.56,
    'claims.cell.mco.Rx drugs': 2.05,
    'payer.dual.admin': 1.04,
    'payer.dual.capitation': 10.89,
    'payer.ffs.capitation': 41.08,
    'payer.ffs.care': 41.08,
    'payer.mco.admin': 3.81,
    'payer.mco.capitation': 40.06,
    'peel.admin': 5.07,
    'peel.fraud': 0.15,
    'peel.medicare': 2.9,
    'source.federal': 64.7,
    'source.state': 35.3,
}

# AGREED 2026-09-25 JW on reference_renders/sign_2026-09-25.png, per S-093
# and S-107: the FY2024 and FY2030 panels, each as the complete artifact with
# its tracker line in register, v5.0 stacked over proposed.
#
# Three things were agreed, not one.
#
# That each figure below is right.
#
# That the collections convention is right (D-83). Exhibit 17 reports
# collections - third-party liability, estate and other recoveries, NOT drug
# rebates - as a single unallocated negative of $15,201M, $1.60 per $100. The
# source declines to say which lane recovered the money, so it is folded pro
# rata across the capitated and fee-for-service lanes by each lane's share of
# gross. The pro-rata key is ours; the dollars are measured.
#
# That when a printed line cannot close, the anchor holds and the decrement
# gives way (S-106).
#
# The 26 figures that lapsed under D-83 are re-agreed here at their new
# values, together with the 10 that never moved.
SIGNED = {
    'beneficiaries.row.Adults': 29.78057501122407,
    'beneficiaries.row.Aged': 18.5473743557725,
    'beneficiaries.row.Children': 13.58058698076118,
    'beneficiaries.row.Disabled': 25.166399315980286,
    'claims.cell.dual.Behavioral health': 1.36,
    'claims.cell.dual.Hospitals': 2.04,
    'claims.cell.dual.Long-term care': 1.92,
    'claims.cell.dual.Other': 2.07,
    'claims.cell.dual.Physicians & clinics': 1.8,
    'claims.cell.dual.Rx drugs': 0.56,
    'claims.cell.ffs.Behavioral health': 3.21,
    'claims.cell.ffs.Hospitals': 8.33,
    'claims.cell.ffs.Long-term care': 20.13,
    'claims.cell.ffs.Other': 5.74,
    'claims.cell.ffs.Physicians & clinics': 2.47,
    'claims.cell.ffs.Rx drugs': 1.52,
    'claims.cell.mco.Behavioral health': 5.01,
    'claims.cell.mco.Hospitals': 7.53,
    'claims.cell.mco.Long-term care': 7.08,
    'claims.cell.mco.Other': 7.63,
    'claims.cell.mco.Physicians & clinics': 6.61,
    'claims.cell.mco.Rx drugs': 2.06,
    'payer.dual.admin': 1.0479234321653947,
    'payer.dual.capitation': 10.968803343653088,
    'payer.ffs.capitation': 41.39191768932002,
    'payer.ffs.care': 41.39191768932002,
    'payer.mco.admin': 3.8390271889905323,
    'payer.mco.capitation': 40.36695545234942,
    'peel.admin': 4.2476877675853855,
    'peel.fraud': 0.15114280271616268,
    'peel.medicare': 2.923074332431033,
    'peel.oversight': 0.101561414661048,
    'peel.vfc': 0.7618684774417891,
    'scale': 9501.64,
    'source.federal': 65.2892553285538,
    'source.state': 35.47261314888798,
}
