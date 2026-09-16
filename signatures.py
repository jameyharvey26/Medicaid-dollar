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

REVIEW = "2026-09-16 JW"

# Signed 2026-09-16 on the stacked FY2024 and FY2030 comparison sheets, after
# the MACPAC behavioral health carve was adopted. The two EN-43 earnings
# margins remain deliberately unsigned; EN-43 states that the $0.76 has no
# primary source, and signing it would assert that someone opened a document
# the register says does not exist.
UNSIGNED = {
    "payer.dual.margin",
    "payer.mco.margin",
}

SIGNED = {
    "beneficiaries.row.Adults": 29.56,
    "beneficiaries.row.Aged": 18.41,
    "beneficiaries.row.Children": 13.48,
    "beneficiaries.row.Disabled": 24.98,
    "claims.cell.dual.Behavioral health": 1.35,
    "claims.cell.dual.Hospitals": 2.03,
    "claims.cell.dual.Long-term care": 1.91,
    "claims.cell.dual.Other": 2.06,
    "claims.cell.dual.Physicians & clinics": 1.78,
    "claims.cell.dual.Rx drugs": 0.56,
    "claims.cell.ffs.Behavioral health": 3.18,
    "claims.cell.ffs.Hospitals": 8.27,
    "claims.cell.ffs.Long-term care": 19.98,
    "claims.cell.ffs.Other": 5.69,
    "claims.cell.ffs.Physicians & clinics": 2.45,
    "claims.cell.ffs.Rx drugs": 1.51,
    "claims.cell.mco.Behavioral health": 4.97,
    "claims.cell.mco.Hospitals": 7.47,
    "claims.cell.mco.Long-term care": 7.02,
    "claims.cell.mco.Other": 7.58,
    "claims.cell.mco.Physicians & clinics": 6.56,
    "claims.cell.mco.Rx drugs": 2.05,
    "payer.dual.admin": 1.04,
    "payer.dual.capitation": 10.89,
    "payer.ffs.capitation": 41.08,
    "payer.ffs.care": 41.08,
    "payer.mco.admin": 3.81,
    "payer.mco.capitation": 40.06,
    "peel.admin": 5.07,
    "peel.fraud": 0.15,
    "peel.medicare": 2.9,
    "source.federal": 64.7,
    "source.state": 35.3,
}
