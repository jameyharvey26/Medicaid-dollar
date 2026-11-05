# ramp.py — FY2029 allocation across CBO-scored sections.
#
# SUPERSEDED IN PART, 2026-11-05 (D-133). This file modelled the allocation by
# spreading each lane's ten-year total across its statutory step schedule,
# because D-37 recorded that CBO publishes no per-section ANNUAL detail.
# D-37's premise is false. Workbook 61570 (CBO, 21 Jul 2025) publishes every
# Chapter 1 section by fiscal year; `cbo61570.py` carries it. The allocation
# is READ now. The modelled weights are kept below, unused, as the record of
# what they cost:
#
#   FY2029, $B        modelled    CBO     error
#   Directed payments     5.99   13.34   -55.1%
#   E&E moratorium        8.60    5.84   +47.3%
#   MSP moratorium       10.59    7.65   +38.4%
#   Six-month redets      9.31    6.92   +34.4%
#   Work requirements    38.15   38.67    +1.4%
#   Provider taxes       11.73   11.65    -0.7%
#   Everything else       5.79    6.08    +4.9%
#
# The total always conserved at 90.146 because the allocation was normalised
# to it, which is why four lanes could be a third to a half wrong without any
# balance line moving.
#
# BASIS (D-36 / D-45): deficit effect, outlays minus revenues. RESOLVED
# 2026-11-05 (D-135): the "$8.6B section-level wedge, unresolved" flagged here
# on 27 August is §71119's revenue line, -8,650 against outlays of -325,610,
# giving the -316,960 that CBO prints as $317.0B. Both figures are CBO's, on
# two bases. Open task 2 is closed.
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
# RETIRED (D-133). Nothing reads these.
RAMP_RETIRED = {
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
import cbo61570 as _CBO
SECTION = {"Work requirements \u00a771119":"71119",
           "Provider taxes \u00a771115":"71115",
           "State directed payments \u00a771116":"71116",
           "MSP moratorium \u00a771101":"71101",
           "Six-month redeterminations \u00a771107":"71107",
           "E&E moratorium \u00a771102":"71102"}
alloc_read = {k: -_CBO.deficit(v, 2029)/1000.0 for k, v in SECTION.items()}
alloc_read["Other + interactions"] = FY29_DEFICIT - sum(alloc_read.values())
print(f"{'Lane':38} {'10-yr $B':>9} {'src':>5} {'FY29 $B':>8} {'share':>6}")
print("-"*70)
alloc = dict(alloc_read)
for k, a in sorted(alloc.items(), key=lambda x: -x[1]):
    print(f"{k:38} {TEN_YR[k]:9.1f} {'read':>5} {a:8.2f} {a/FY29_DEFICIT*100:5.1f}%")
print("-"*70)
print(f"{'TOTAL':38} {sum(TEN_YR.values()):9.1f} {'':5} {sum(alloc.values()):8.2f} {100.0:5.1f}%")
