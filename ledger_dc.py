# ledger_dc.py — District of Columbia, FY2024, in the NATIONAL view.
#
# This is the STATE-SERIES artifact: national columns, national scale, national
# tracker, so it can be read against the national pair (S-060, S-070). The
# existing named-plan DC diagram is a different product and stays where it is.
#
# REDUCED FIDELITY, declared on the artifact (S-071). Where DC data is missing it
# is ABSENT, not estimated from a national share (S-068). Three things are absent
# and each is listed on the render:
#
#   1. Beneficiary shares. DC group totals are not in hand, so the beneficiary
#      column is omitted entirely rather than filled with national percentages.
#   2. Behavioral health as a separate provider node. DC's source detail folds it
#      into wrap-around services, so DC shows five nodes rather than six. The
#      dollars are present; the split is not.
#   3. Public-company earnings and dual-plan retention. No DC figure, so those
#      peels are omitted; dual capitation runs straight through to care.
#
# Documented fraud is also absent: no DC figure.
#
# SOURCE: CMS-64 / MACStats FY2024 DC spine; MCO split and payer peel from DHCF
# CY2023; MCO to service mix is a national proxy and is MODELLED. Carried over
# from build_sankey_dc.py, which JW notes is likely stale on several axes.
# **All vintages need re-checking before DC ships to a reader (EN-39).**

SCALE = 43.72                      # $M per $1 of the DC $100

fed, state = 73.17, 26.83
admin      = 234 / SCALE
medicare   = 86 / SCALE
mc_total   = 1802 / SCALE
pace       = 15 / SCALE
dsnp       = 25 / SCALE
mco_cap    = mc_total - pace - dsnp
ffs        = 2250 / SCALE

# --- plan-level retention, aggregated up to the national view's two lanes ----
_plan = ["HSCSN", "MedStar Family Choice DC", "Wellpoint DC", "AmeriHealth Caritas DC"]
_comp = ["MedStar Family Choice DC", "Wellpoint DC", "AmeriHealth Caritas DC"]
_rev = {"AmeriHealth Caritas DC": 841.0, "Wellpoint DC": 425.3,
        "MedStar Family Choice DC": 411.2, "HSCSN": 184.0}
_clm = {"AmeriHealth Caritas DC": 755.5, "Wellpoint DC": 348.5,
        "MedStar Family Choice DC": 379.6, "HSCSN": 154.4}
_cap = {"HSCSN": 184.0 / SCALE}
_resid = mco_cap - _cap["HSCSN"]; _revT = sum(_rev[p] for p in _comp)
for _p in _comp:
    _cap[_p] = _rev[_p] / _revT * _resid
_care = {p: _cap[p] * (_clm[p] / _rev[p]) for p in _plan}

mco      = mco_cap
mco_care = sum(_care.values())
mco_ret  = mco - mco_care
mco_adm  = mco_ret            # ABSENT: no DC margin/earnings split
dual_adm = 0.0
earnings = 0.0                # ABSENT: no DC public-company earnings figure

# PACE and the D-SNP wrap are the capitated dual-focused lane here.
dual      = pace + dsnp
dual_ret  = 0.0               # ABSENT: no DC retention figure for these
dual_care = dual

fraud = 0.0                   # ABSENT: no DC documented-fraud figure

# --- provider nodes: five, not six. Behavioral health is not separable. -----
ORDER_DC = ["Long-term care", "Hospitals", "Physicians & clinics",
            "Wrap around services", "Rx drugs"]
ffs_n = {"Long-term care": 1236 / SCALE, "Physicians & clinics": 406 / SCALE,
         "Hospitals": 297 / SCALE, "Wrap around services": 222 / SCALE,
         "Rx drugs": 89 / SCALE}

# MCO care to service mix: national proxy. MODELLED, flagged on the artifact.
_natmix = {"Long-term care": 8.82, "Hospitals": 9.98,
           "Physicians & clinics": 9.76 + 6.03,
           "Wrap around services": 8.38, "Rx drugs": 2.38}
_mixT = sum(_natmix.values())
_mix = {p: _natmix[p] / _mixT for p in ORDER_DC}
mcoc_n = {p: mco_care * _mix[p] for p in ORDER_DC}

# duals: Medicare covers acute, so the Medicaid dollar is LTSS plus a wrap
dualc_n = {p: 0.0 for p in ORDER_DC}
dualc_n["Long-term care"] = dual_care * 0.75
dualc_n["Wrap around services"] = dual_care * 0.25

node = {p: ffs_n[p] + mcoc_n[p] + dualc_n[p] for p in ORDER_DC}

ABSENT = [
    "Beneficiary shares: DC group totals not in hand, column omitted",
    "Behavioral health: folded into wrap-around services in the DC source",
    "Public-company earnings and dual-plan retention: no DC figure",
    "Documented fraud: no DC figure",
]

if __name__ == "__main__":
    print(f"DC FY2024, per $100   federal {fed}  local {state}")
    print(f"  administration {admin:.2f}   Medicare premiums {medicare:.2f}")
    print(f"  managed care {mco:.2f}   PACE + D-SNP {dual:.2f}   fee-for-service {ffs:.2f}")
    print(f"  disbursed {100-admin-medicare:.2f}   claims {mco_care+dual_care+ffs:.2f}")
    print("  provider nodes:", {p: round(node[p], 2) for p in ORDER_DC})
    print("  ABSENT:"); [print("   -", a) for a in ABSENT]
