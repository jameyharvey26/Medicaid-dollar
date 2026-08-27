# FY2029 allocation across CBO-scored sections.
# BASIS DISCIPLINE (D-36): section totals are DEFICIT effects, so allocate the
# FY2029 DEFICIT figure (-$90.146B), not the outlay figure. Mixing them is the error.
# BASIS FLAG 2026-08-27 (session 2): D-26's illustrative figures are computed from
# $325.6B, the federal OUTLAY reduction for 71119 (CRS R48755), while TEN_YR below
# uses $317.0B, the DEFICIT effect. An $8.6B section-level wedge, unresolved.
# See WHITEPAPER_BRIEF_APPEND_2026-08-27b.md. Input to open task 2.
FY29_DEFICIT = 90.146
TEN_YR = {  # $B, deficit effect, CBO Supplemental 28 Oct 2025
 "Work requirements §71119": 317.0,
 "Provider taxes §71115": 182.7,
 "State directed payments §71116": 149.4,
 "MSP moratorium §71101": 66.0,
 "Six-month redeterminations §71107": 58.0,
 "E&E moratorium §71102": 53.6,
 "Other + interactions": 60.1,
}
# Ramp position in FY2029, from statutory schedules in the CBO narrative.
# weight = share of that section's steady-state effect realised in FY2029.
RAMP = {
 # blocked on enactment (Jul 2025); at full effect well before 2029
 "MSP moratorium §71101": 1.00,
 "E&E moratorium §71102": 1.00,
 # 6-mo redeterminations begin Jan 2027; full effect by 2028
 "Six-month redeterminations §71107": 1.00,
 # states may impose from Jan 2027, MUST by Jan 2029 -> 2029 first universal year,
 # but partial-year and rollout drag
 "Work requirements §71119": 0.75,
 # hold-harmless steps 6.0->5.5 in 2028, 5.0 in 2029, reaching 3.5 in 2032.
 # 2029 is 2 of 5 steps = 1.0pp of the eventual 2.5pp reduction
 #
 # FLAGGED 2026-08-27 (session 2): this single weight blends TWO mechanisms
 # with different time profiles and must be decomposed before publication.
 #   (a) EXPANSION states: the scheduled phase-down described above. Nursing
 #       facility and ICF/IID taxes are EXEMPT from it entirely.
 #   (b) NON-EXPANSION states: frozen at July 2025 levels, not reduced. Loss
 #       accrues only against a rising baseline, so no year-one effect and
 #       the gap widens over time.
 # Value left unchanged pending decomposition. 0.40 is NOT settled.
 # Source: CRS R48633; CMS Dear Colleague 11/14/2025; ASPE 2026.
 "Provider taxes §71115": 0.40,
 # SDPs above Medicare cut 10pp/yr from FY2028 -> FY2029 is year 2
 "State directed payments §71116": 0.25,
 # mixed bag; assume mid-ramp
 "Other + interactions": 0.60,
}
raw = {k: TEN_YR[k]*RAMP[k] for k in TEN_YR}
tot = sum(raw.values())
print(f"{'Lane':38} {'10-yr $B':>9} {'ramp':>5} {'FY29 $B':>8} {'share':>6}")
print("-"*70)
alloc={}
for k,v in sorted(raw.items(), key=lambda x:-x[1]):
    a = v/tot*FY29_DEFICIT
    alloc[k]=a
    print(f"{k:38} {TEN_YR[k]:9.1f} {RAMP[k]:5.2f} {a:8.2f} {a/FY29_DEFICIT*100:5.1f}%")
print("-"*70)
print(f"{'TOTAL':38} {sum(TEN_YR.values()):9.1f} {'':5} {sum(alloc.values()):8.2f} {100.0:5.1f}%")
