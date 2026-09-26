# provider_mix.py — the provider phase, computed from its sources.
#
# These six node totals and the eighteen cells beneath them used to be pasted
# constants in three files. The method that produced them lived in
# `build_xlsx.py`, the workbook builder, and the ledger cited an exhibit that
# cannot produce them: MACStats Exhibit 17 reports managed care as a single
# line and never distributes it across services. Nobody publishes a national
# split of capitation by service category. So the provider phase is MODELLED,
# it always was, and this module is where that modelling is written down.
#
# THREE INPUTS, three different sources, three different vintages.
#
#   1. FFS_MIX    CMS-64 fee-for-service spending by service category,
#                 FY2024. Reconciles exactly to MACStats February 2026
#                 Exhibit 17: the categories below sum to $400,002M, which is
#                 Exhibit 17's gross fee-for-service total to the dollar.
#                 MEASURED.
#
#   2. HMA_KEY    The capitated half. Health Management Associates, "New
#                 Insights on Medicaid Spending", a T-MSIS service mix at
#                 CY2021, which prices managed-care encounters at
#                 fee-for-service and Medicare rates. MODELLED, and three
#                 years older than everything around it.
#
#                 KNOWN BIAS, direction stated: HMA's "Professional" category
#                 unbundles hospital-based physician work that CMS-64 bundles
#                 into Hospital. Against CMS-64 convention this OVERSTATES
#                 physicians and clinics and UNDERSTATES hospitals.
#
#   3. BH_CARVE   Behavioral health, taken across the other categories.
#                 MACPAC, March 2026 Report to Congress, Chapter 2, Table 2-8
#                 and Figure 2-1, CY2023 T-MSIS. MODELLED.
#
# ON THE CARVE, which is the part that changed.
#
# It used to be five hand-set numbers with no source anywhere in the code, and
# the original script called the cross-line split an estimate. MACPAC's
# chapter is the first national claims-based estimate of behavioral health
# spending since 2015, so for most of this project's life there was nothing to
# cite. There is now.
#
# What MACPAC publishes is a split by CARE SETTING, not by the service
# categories this diagram uses. The mapping from one to the other is ours and
# is written out in BH_SETTING below so a reader can disagree with it. Four
# further differences of basis, none of them resolvable by arithmetic:
#
#   - MACPAC counts any claim carrying a behavioral health diagnosis in any
#     position, so an admission for something else with depression recorded
#     second counts in full. Overstates.
#   - Non-dually-eligible enrollees only. Understates.
#   - CY2023 against this ledger's FY2024.
#   - Denominator is service-related spending of $642.3B, not the $957.4B
#     total computable this ledger runs on.
#
# Because of the last of those, the carve's TOTAL is held at this ledger's own
# basis and only its DISTRIBUTION is taken from MACPAC. MACPAC's own total is
# $95.3B against this ledger's $91.0B, which is agreement to about five
# percent across two different bases and is the most the source can be asked
# to say. JW's ruling, 16 September: adopt MACPAC.
#
# Long-term care takes no carve. MACPAC's care settings do not identify
# long-term care at all, so there is no basis for one — that is an absence,
# not a zero, and it is declared rather than assumed.

# 1. fee-for-service, $M, CMS-64 FY2024 (= Exhibit 17 gross FFS)
# D-83. These five used to be typed here. They are now derived from the nine
# published Exhibit 17 columns in basis_national.py, where the mapping from
# column to node is written out. The old comment on "Other" was wrong: other
# practitioner sits in physicians and clinics, not in the wrap-around node.
# The arithmetic was right and the description was not, which is exactly what
# a typed total hides. S-073.
import basis_national as _BN

FFS_MIX = {"Long-term care": _BN.LTC_FFS_M,
           "Hospitals": _BN.HOSPITAL_M,
           "Other": _BN.WRAP_FFS_M,            # other acute + dental
           "Physicians & clinics": _BN.PHYS_FFS_M,
           "Rx drugs": _BN.DRUGS_M}

# 2. capitated half, HMA T-MSIS key, CY2021
HMA_KEY = {"Long-term care": .197, "Hospitals": .238, "Other": .235,
           "Physicians & clinics": .251, "Rx drugs": .079}

# 3. behavioral health by care setting, % of BH service spending,
#    MACPAC March 2026 ch.2 Table 2-8, CY2023. The published column sums to
#    100.2 rather than 100 because each entry is rounded to a tenth, so the
#    shares below are normalised by the printed total rather than by 100.
BH_SETTING = {
    # setting                  share   mapped to
    "inpatient":              (27.6, "Hospitals"),
    "outpatient hospital":    (1.8,  "Hospitals"),
    "emergency department":   (1.0,  "Hospitals"),
    "outpatient":             (33.6, "Physicians & clinics"),
    "CMHC":                   (8.0,  "Physicians & clinics"),
    "FQHC":                   (3.2,  "Physicians & clinics"),
    "telehealth":             (4.6,  "Physicians & clinics"),
    "SUD residential":        (2.6,  "Other"),
    "other settings":         (17.8, "Other"),
}
BH_SERVICES = 79_800     # $M, Table 2-8, excluding drugs
BH_DRUGS = 15_500        # $M, Figure 2-1, mapped whole to Rx drugs
BH_TOTAL = 9.51          # per $100, this ledger's own basis. See header.

# BH_TOTAL was struck against a claims total of $86.42, the figure the panel
# carried before D-70 moved the denominator. That is a BASIS, not an output:
# it names the base the 9.51 was measured against, so it is typed here and
# named rather than appearing bare inside an expression. S-105.
BH_BASIS = 86.42

CATS = ["Long-term care", "Hospitals", "Other", "Physicians & clinics",
        "Rx drugs"]
NODES = CATS[:2] + ["Other", "Physicians & clinics", "Behavioral health",
                    "Rx drugs"]
ORDER = ["Long-term care", "Hospitals", "Other", "Physicians & clinics",
         "Behavioral health", "Rx drugs"]


def carve_shares():
    """Behavioral health as a share of itself, by this diagram's categories."""
    d = {c: 0.0 for c in CATS}
    for _, (share, cat) in BH_SETTING.items():
        d[cat] += BH_SERVICES * share
    tot_pct = sum(s for s, _ in BH_SETTING.values())
    d = {c: v / tot_pct for c, v in d.items()}
    d["Rx drugs"] += BH_DRUGS
    t = sum(d.values())
    return {c: v / t for c, v in d.items()}


def allocate(ffs: float, mco_care: float, dual_care: float):
    """The provider phase for one panel. Returns (ffs_n, mco_n, dual_n, node).

    Everything is carried at full precision and rounded once at the end. The
    six rounded node totals are then forced to sum to the money that actually
    arrived, by trimming the node with the largest upward rounding — which is
    where the cent on long-term care comes from, and it is a rounding residue
    rather than anything to do with published figures.
    """
    csum = sum(FFS_MIX.values())
    capcare = mco_care + dual_care
    f = {c: ffs * FFS_MIX[c] / csum for c in CATS}
    m = {c: mco_care * HMA_KEY[c] for c in CATS}
    d = {c: dual_care * HMA_KEY[c] for c in CATS}

    carve = {c: BH_TOTAL * (capcare + ffs) / BH_BASIS * s
             for c, s in carve_shares().items()}

    BHf = BHm = BHd = 0.0
    for c in CATS:
        tot = f[c] + m[c] + d[c]
        fr = carve[c] / tot if tot else 0.0
        BHf += f[c] * fr; BHm += m[c] * fr; BHd += d[c] * fr
        f[c] *= (1 - fr); m[c] *= (1 - fr); d[c] *= (1 - fr)
    f["Behavioral health"], m["Behavioral health"], d["Behavioral health"] = BHf, BHm, BHd

    exact = {c: f[c] + m[c] + d[c] for c in ORDER}
    node = {c: round(v, 2) for c, v in exact.items()}
    gap = round(sum(node.values()) - sum(exact.values()), 2)
    while abs(gap) >= 0.005:
        step = 0.01 if gap > 0 else -0.01
        c = max(ORDER, key=lambda k: (node[k] - exact[k]) * (1 if gap > 0 else -1))
        node[c] = round(node[c] - step, 2)
        gap = round(gap - step, 2)
    r2 = lambda x: {k: round(v, 2) for k, v in x.items()}
    return r2(f), r2(m), r2(d), node


# D-83. These three used to be typed here at two decimals on the old hundred,
# duplicating figures the ledger also carried. They are now read from the one
# place the lanes are derived, so a change to the denominator or to the
# collections fold promulgates into the provider phase instead of leaving two
# copies to drift. S-073.
FFS_N, MCO_N, DUAL_N, NODE = allocate(_BN.FFS_CARE, _BN.MCO_CARE,
                                      _BN.DUAL_CARE)

if __name__ == "__main__":
    print("behavioral health carve, share of itself:")
    for c, s in carve_shares().items():
        print(f"   {c:24}{s*100:6.2f}%   {BH_TOTAL*s:6.3f} per $100")
    print(f"\n{'node':24}{'ffs':>8}{'mco':>8}{'dual':>8}{'total':>9}")
    for c in ORDER:
        print(f"{c:24}{FFS_N[c]:>8.2f}{MCO_N[c]:>8.2f}{DUAL_N[c]:>8.2f}{NODE[c]:>9.2f}")
    print(f"{'SUM':24}{'':>8}{'':>8}{'':>8}{sum(NODE.values()):>9.2f}"
          f"   (money arriving: 86.42)")
