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

# AGREED 2026-09-18 JW on the stacked sheets reference_renders/sign_2024.png
# and sign_2030.png, per S-093. 36 figures: the 33 that lapsed under
# D-70, re-agreed at their new values, plus three never signed before —
# `peel.vfc`, `peel.oversight`, and `scale`, which was carried as DERIVED
# with no parents and so could not be verified at all until today.
#
# Two things were agreed, not one: that each number is right, and that the
# denominator it is struck against — $950,164M, the money budgeted to
# Medicaid at the state agency — is the right denominator.
SIGNED = {
    'beneficiaries.row.Adults': 29.785208321931794,
    'beneficiaries.row.Aged': 18.550259986697036,
    'beneficiaries.row.Children': 13.582699870759155,
    'beneficiaries.row.Disabled': 25.17031474566496,
    'claims.cell.dual.Behavioral health': 1.3602852244454644,
    'claims.cell.dual.Hospitals': 2.0454659300920683,
    'claims.cell.dual.Long-term care': 1.9245516879191382,
    'claims.cell.dual.Other': 2.075694490635301,
    'claims.cell.dual.Physicians & clinics': 1.793561258898464,
    'claims.cell.dual.Rx drugs': 0.5642664634736742,
    'claims.cell.ffs.Behavioral health': 3.2042274175826493,
    'claims.cell.ffs.Hospitals': 8.333006523084435,
    'claims.cell.ffs.Long-term care': 20.132221321792873,
    'claims.cell.ffs.Other': 5.7333503163664385,
    'claims.cell.ffs.Physicians & clinics': 2.468665777697324,
    'claims.cell.ffs.Rx drugs': 1.521504214009371,
    'claims.cell.mco.Behavioral health': 5.007864863328857,
    'claims.cell.mco.Hospitals': 7.526911575264902,
    'claims.cell.mco.Long-term care': 7.073483167116414,
    'claims.cell.mco.Other': 7.637749630590088,
    'claims.cell.mco.Physicians & clinics': 6.609978572120181,
    'claims.cell.mco.Rx drugs': 2.0656183037875566,
    'payer.dual.admin': 1.0479234321653947,
    'payer.dual.capitation': 10.972967477193412,
    'payer.ffs.capitation': 41.39297557053309,
    'payer.ffs.care': 41.39297557053309,
    'payer.mco.admin': 3.8390271889905323,
    'payer.mco.capitation': 40.36520451206319,
    'peel.admin': 4.2476877675853855,
    'peel.fraud': 0.15114280271616268,
    'peel.medicare': 2.923074332431033,
    'peel.oversight': 0.101561414661048,
    'peel.vfc': 0.7618684774417891,
    'scale': 9501.64,
    'source.federal': 65.2892553285538,
    'source.state': 35.47261314888798,
}
