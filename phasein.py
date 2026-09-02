# phasein.py
# Statutory phase-in table for P.L. 119-21, Title VII, Subtitle B, Chapter 1.
# Answers D-62 step 1 and step 2: per provision, effective date / step schedule /
# year of full effect; then the share of the ten-year overlay at full statutory
# effect in each candidate anchor year.
#
# BASIS (D-36): ten-year weights are DEFICIT effects, matching ramp.py and the
# CBO supplemental of 28 Oct 2025. All years are FEDERAL FISCAL years, because
# the ledger's denominator (CBO Jan-2025 Budget Projections) and the CMS-64
# baseline are both fiscal-year. This matters: several provisions key to
# CALENDAR dates, and a January calendar date lands one quarter into the
# fiscal year. See §71119 below, where it is decisive.
#
# SOURCING (S-049, S-050): every date below is from the enacted text or from
# CMS's own implementing guidance / rulemaking on the enacted text. No date is
# modelled. The RAMP weights ARE modelled and are flagged as such (S-012).

TEN_YR = {  # $B, deficit effect, CBO Supplemental 28 Oct 2025. Sums to 886.8.
    "Work reporting":                   317.0,
    "Provider tax limits":              182.7,
    "Directed payment caps":            149.4,
    "Blocked senior enrollment rule":    66.0,
    "Six-month renewals":                58.0,
    "Blocked Medicaid enrollment rule":  53.6,
    "Everything else":                   60.1,
}

# --- The statutory phase-in table -------------------------------------------
# full_fy: first FEDERAL FISCAL YEAR in which the provision is at full
#          statutory effect for every state, for the whole year.
STATUTE = {
    "Blocked senior enrollment rule": dict(
        sec="71101", effective="Enactment, 4 Jul 2025",
        steps="None. Single moratorium, in force through 1 Oct 2034.",
        full_fy=2026,
        cite="P.L. 119-21 s.71101; KFF, effective upon enactment; K&S, runs to 1 Oct 2034."),
    "Blocked Medicaid enrollment rule": dict(
        sec="71102", effective="Enactment, 4 Jul 2025",
        steps="None. Single moratorium, in force through 1 Oct 2034.",
        full_fy=2026,
        cite="P.L. 119-21 s.71102; same."),
    "Six-month renewals": dict(
        sec="71107", effective="Renewals initiated on/after 1 Jan 2027",
        steps="None. One-step change, 12-month to 6-month renewal cycle.",
        full_fy=2028,
        cite="CRS R48633; KFF (renewals scheduled on/after 31 Dec 2026); CMS CIB 8 Dec 2025."),
    "Work reporting": dict(
        sec="71119", effective="1 Jan 2027 (states may implement earlier)",
        steps=("Good-faith-effort exemptions available; a granted exemption "
               "expires NOT LATER THAN 31 DEC 2028 and may not be renewed."),
        full_fy=2030,
        cite=("P.L. 119-21 s.71119(c); SSA s.1902(xx)(11)(C)(i); CMS CIB 8 Dec 2025. "
              "31 Dec 2028 falls one quarter INTO FY2029, so FY2029 is 3/4 universal; "
              "FY2030 is the first full fiscal year with no exemption possible.")),
    "Provider tax limits": dict(
        sec="71115", effective="FYs beginning on/after 1 Oct 2026 (FY2027 freeze)",
        steps=("Expansion states only: safe harbour steps down 0.5pp/yr from 6.0% — "
               "FY2028 5.5, FY2029 5.0, FY2030 4.5, FY2031 4.0, FY2032 3.5 and after."),
        full_fy=2032,
        cite=("CMS DCL 14 Nov 2025; CMS-2452-P (91 FR 46562, 23 Jul 2026). "
              "Nursing facility and ICF/IID classes exempt from the step-down; "
              "non-expansion states are frozen at Jul-2025 levels, not reduced.")),
    "Directed payment caps": dict(
        sec="71116", effective="Rating periods on/after 4 Jul 2025 (non-grandfathered)",
        steps=("Grandfathered SDPs: reduced 10 percentage points of the ORIGINAL "
               "grandfathered dollar amount each year (non-compounding), from the "
               "first rating period on/after 1 Jan 2028, UNTIL the 100%/110% "
               "Medicare limit is reached."),
        full_fy=None,  # <- the statute fixes no year
        cite=("P.L. 119-21 s.71116(b); CMS SDP letter 2 Feb 2026; CMS SDP proposed "
              "rule 20 May 2026. Number of steps depends on how far above Medicare "
              "each SDP starts, so the year of full effect is NOT set by statute.")),
    "Everything else": dict(
        sec="residual", effective="Mixed",
        steps=("Residual basket. Cost sharing (71120) bites FYs beginning on/after "
               "1 Oct 2028; alien eligibility (71109) 1 Oct 2026; retroactive "
               "coverage (71112) 1 Jan 2027; plus CBO's interaction netting."),
        full_fy=2030,
        cite="Mixed; residual is PROVISIONAL per fmap.py."),
}

# --- Modelled ramp weights, derived from the schedules above ----------------
# MODELLED (S-012). Each weight is the share of that lane's steady-state effect
# realised in the given fiscal year, derived mechanically from the step schedule.
SDP_PP_TO_LIMIT = 60  # modelled: pp of the original amount that must come off
                      # before a typical grandfathered SDP reaches the Medicare
                      # limit. 60 => SDP starting near 2.5x Medicare => 6 steps
                      # => full effect FY2033. Sensitivity run below.

def weight(lane, fy, sdp_pp=SDP_PP_TO_LIMIT):
    if lane in ("Blocked senior enrollment rule", "Blocked Medicaid enrollment rule"):
        return 1.0 if fy >= 2026 else 0.0
    if lane == "Six-month renewals":
        return 1.0 if fy >= 2028 else (0.5 if fy == 2027 else 0.0)
    if lane == "Work reporting":
        # universal only from 1 Jan 2029 = 3 of 4 quarters of FY2029
        if fy >= 2030: return 1.0
        if fy == 2029: return 0.75
        if fy == 2028: return 0.45   # mandatory but exemptions live
        if fy == 2027: return 0.20   # mandatory from Q2, heavy rollout drag
        return 0.0
    if lane == "Provider tax limits":
        # steps of the eventual 2.5pp reduction: 0.5pp per year from FY2028
        if fy < 2028: return 0.0
        return min(1.0, 0.5 * (fy - 2027) / 2.5)
    if lane == "Directed payment caps":
        if fy < 2028: return 0.0
        return min(1.0, 10.0 * (fy - 2027) / sdp_pp)
    if lane == "Everything else":
        if fy >= 2030: return 1.0
        return {2027: 0.25, 2028: 0.40, 2029: 0.60}.get(fy, 0.0)
    return 0.0

TOTAL = sum(TEN_YR.values())

print("=" * 96)
print("STATUTORY PHASE-IN TABLE — P.L. 119-21, Title VII, Subtitle B, Ch. 1")
print("=" * 96)
for lane, d in STATUTE.items():
    fe = d["full_fy"]
    print(f"\n{lane}  (s.{d['sec']})   10-yr ${TEN_YR[lane]:.1f}B")
    print(f"  effective    : {d['effective']}")
    print(f"  step schedule: {d['steps']}")
    print(f"  full effect  : {'FY' + str(fe) if fe else 'NOT FIXED BY STATUTE'}")

print("\n" + "=" * 96)
print("CANDIDATE YEARS — share of the ten-year overlay at FULL statutory effect")
print("=" * 96)
print(f"{'FY':>5} {'at full effect':>16} {'share':>8} {'mid-ramp':>10} {'not yet started':>16}")
print("-" * 96)
for fy in range(2027, 2036):
    full = sum(TEN_YR[l] for l in TEN_YR if weight(l, fy) >= 0.999)
    none = sum(TEN_YR[l] for l in TEN_YR if weight(l, fy) <= 0.001)
    mid = TOTAL - full - none
    print(f"{fy:>5} {full:>13.1f}$B {full/TOTAL*100:>7.1f}% {mid:>8.1f}$B {none:>13.1f}$B")

print("\n" + "=" * 96)
print("LANE-BY-LANE RAMP POSITION (modelled weights, derived from the schedules)")
print("=" * 96)
years = [2028, 2029, 2030, 2031, 2032, 2033]
print(f"{'Lane':34} " + " ".join(f"{y:>7}" for y in years))
print("-" * 96)
for lane in TEN_YR:
    print(f"{lane:34} " + " ".join(f"{weight(lane, y):>7.2f}" for y in years))

print("\n" + "=" * 96)
print("HOW THE PICTURE CHANGES — lane mix at each candidate anchor")
print("=" * 96)
for fy in (2029, 2030, 2032):
    raw = {l: TEN_YR[l] * weight(l, fy) for l in TEN_YR}
    tot = sum(raw.values())
    print(f"\nFY{fy}   (relative composition of that year's overlay)")
    for l, v in sorted(raw.items(), key=lambda x: -x[1]):
        print(f"   {l:34} {v/tot*100:5.1f}%   (10-yr share {TEN_YR[l]/TOTAL*100:4.1f}%)")

print("\n" + "=" * 96)
print("SENSITIVITY — directed payment caps, pp needed to reach the Medicare limit")
print("=" * 96)
print(f"{'pp needed':>10} {'implied full-effect FY':>24} {'FY2029 weight':>15}")
for pp in (40, 60, 80):
    print(f"{pp:>10} {'FY' + str(2027 + pp // 10):>24} {10.0 * 2 / pp:>15.2f}")
print("\nramp.py currently carries 0.25, which implies 80pp / FY2035 — outside the")
print("scoring window. 0.40 for provider taxes is now confirmed: FY2029 is step 2")
print("of 5, i.e. 1.0pp of the eventual 2.5pp reduction.")
