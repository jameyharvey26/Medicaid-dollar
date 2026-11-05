# Source register

Primary documents this analysis depends on. Confirmed reachable 2026-08-27 unless
noted. S-050: confirm the specific vintage exists before relying on its contents.

## The score

**CBO supplemental cost estimate, P.L. 119-21, Title VII, Subtitle B, Chapter 1**
28 October 2025. Figures identical to CBO's July 2025 estimate.
https://www.cbo.gov/system/files/2025-10/PL-119-21-Medicaid%20_0.pdf

- Ten-year (2025–2034) deficit reduction $886.8B. Outlays $914.6B; the ~$28B gap is
  revenue and has no place in a spending diagram (D-36).
- §71116 directed payments: $149.4B over 2025–2034.
- **Measured relative to CBO's January 2025 baseline.** This fixes the counterfactual
  vintage for the to-be denominator (D-60).
- Accounts for judicial and administrative actions through 10 April 2025.
- ~~Per-section **annual** detail is not published — aggregate year-by-year only (D-37).~~
  **FALSE. Corrected 2026-11-05 (D-133).** CBO publishes per-section annual
  detail for every Chapter 1 section in the workbook below. D-37's premise was
  wrong, and `ramp.py`, `phasein.py` and `tobe2030.py` all modelled an
  allocation that did not need modelling. The chapter table here remains the
  right numerator; what changes is that the lanes are read, not inferred.

**CBO, "Estimated Budgetary Effects of Public Law 119-21 … Relative to CBO's
January 2025 Baseline", publication 61570, 21 July 2025**
https://www.cbo.gov/publication/61570 — workbook
`61570-pl119-21-2025Recon-CLB.xlsx`, sheet "Title VII", table 7. Retrieved
2026-11-05 and transcribed into `cbo61570.py`.

- All 21 Chapter 1 sections, direct spending and revenues, by fiscal year
  2025–2034. Same baseline and the same 10 April 2025 cutoff as the
  supplemental.
- Every section's yearly series sums to CBO's own printed ten-year total,
  21 of 21.
- The six lanes the two documents share agree to the dollar on the deficit
  basis. The CHAPTER TOTALS DO NOT: this workbook sums to $963.8B against the
  supplemental's $886.8B. The $77.0B is CBO's interaction netting among
  Chapter 1 policies, which the supplemental carries inside its "Other" line
  (D-134). Sum the sections and you overstate the chapter by about 8% from
  FY2029 on.
- The register's earlier claim that these two documents' "figures are
  identical" holds for the six named sections and NOT for the chapter.

## The denominator (to-be baseline)

**CBO 10-Year Budget Projections, January 2025** — publication 51118.
https://www.cbo.gov/system/files/2025-01/51118-2025-01-Budget-Projections.xlsx
Medicaid outlays by fiscal year at the vintage the score is measured against.
Available for every candidate anchor year 2025–2035. **Not yet pulled.**

Index page: https://www.cbo.gov/data/budget-economic-data

## Medicaid baseline detail — the gap (D-61)

**Publication 51301.** Index:
https://www.cbo.gov/data/baseline-projections-selected-programs

There is **no January 2025 vintage**. The series runs June 2024 → February 2026,
uniquely among programs in that series.

- June 2024: https://www.cbo.gov/system/files/2024-06/51301-2024-06-medicaid.pdf
  Pre-HR-1 and correct in basis, but superseded — CBO's January 2025 revision raised
  the ten-year Medicaid projection by ~$817B / 12%.
- February 2026: https://www.cbo.gov/system/files/2026-02/51301-2026-02-medicaid.pdf
  Current vintage but incorporates HR-1. Not the counterfactual.

Consequence: component splits (fee-for-service, managed care, Medicare premiums,
institutional LTC, HCBS) cannot be sourced at the correct vintage. D-11's
held-constant FY2024 structure stands; S-043 stands.

## Still needed

**Statutory phase-in schedule, P.L. 119-21.** Per provision: effective date, step
schedule, year of full effect. Determines the anchor year (D-62). Sourceable from the
enacted text. **Not started.**

## Baseline (as-is)

CMS-64 FY2024 national totals, MAP only. See `fmap.py` for lane-level provenance.
