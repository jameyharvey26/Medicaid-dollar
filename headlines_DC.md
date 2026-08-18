# District of Columbia — Medicaid headline facts

**1. Nearly $5 billion a year.** DC Medicaid runs about $4.9 billion (FY2025) — roughly $3.6B federal, $1.3B local; about $4.44B of that buys actual health services.

**2. Almost a quarter of the entire city budget.** At $4.9B of DC's $21.2 billion budget, about $1 of every $4.40 the District spends flows through its single largest agency.

**3. No state leans harder on long-term care.** LTC is about 30% of DC's Medicaid benefits on the fee-for-service lines alone — and higher counting the LTSS inside managed care and PACE — and DC spends more Medicaid LTSS per resident ($1,554) than any state in the country.

**4. Near-universal coverage — but the gap just doubled.** DC has one of the lowest uninsured rates in the country, yet it jumped from 2.7% to 4.5% in 2024 — the steepest one-year rise of any state — leaving about 95.5% of residents covered.

**5. More than one in three Washingtonians is on Medicaid.** About 257,000 residents — 38% (north of 300,000 counting the locally funded Alliance) — and Medicaid pays for 46% of all DC births.

**6. For every local dollar, the federal government sends almost three — and the program delivers nearly four.** At DC's ~73% blended match, each $1.00 of care is about $0.73 federal and $0.27 local — roughly $2.70 federal : $1.00 local : $3.70 of care (and $1 local unlocks $9 federal for the 90%-matched expansion adults).

**7. The bite deepens fast — about 1 in 25 of DC's Medicaid care dollars gone in 2027, 1 in 11 by 2028, 1 in 8 by 2029.** DC stands to lose roughly $175–235M of Medicaid-funded care in FY2027 (~4%), ~$400–540M in FY2028 (~9%), and ~$650–730M in FY2029 (~13%) — counted as total program dollars, since every lost federal dollar pulls DC's local match and provider revenue down with it. Work requirements and more frequent renewals hit first; provider-tax limits and payment caps pile on through 2028–29.

---

## Sources & basis

**1. total_spend** [external source]  
- Basis: DC executive budget: DHCF (agency HT0) gross funds, FY2025 approved. Higher than CMS-64 actuals (gross vs net; includes local-only Alliance/ICP and admin).  
- Source: DC OCFO, FY2025 Approved Budget — Dept. of Health Care Finance (HT0) tables; corroborated by DC Action.  
- Vintage: FY2025 (approved budget)  
- Link: https://cfo.dc.gov/sites/default/files/dc/sites/ocfo/publication/attachments/ht_dhcf_tables_2025j.pdf

**2. share_of_city_budget** [external source]  
- Basis: DHCF gross funds ÷ total DC gross-funds budget, FY2025 approved (gross-to-gross).  
- Source: Congressional Research Service, DC FY2025 Budget Status (R48609); DC OCFO DHCF tables.  
- Vintage: FY2025 (approved budget)  
- Link: https://www.congress.gov/crs-product/R48609

**3. long_term_care_intensity** [external source]  
- Basis: FFS share (~30%) is CMS-64/MACStats Ex.17 (Sankey-consistent floor). All-in LTSS share and per-resident rank use the comprehensive CMS/Mathematica LTSS measure incl. managed LTSS + PACE.  
- Source: MACStats Ex.17 (FFS LTSS, FY2024); CMS Medicaid LTSS Annual Expenditures Report (per-resident #1; national 33.5%), FY2020 — most recent comprehensive report.  
- Vintage: FFS: FY2024; comprehensive LTSS: FY2020  
- Link: https://www.medicaid.gov/media/164316

**4. coverage_rate** [external source]  
- Basis: Census American Community Survey 1-year uninsured rate.  
- Source: U.S. Census Bureau ACS 2024 1-year estimates; SHADAC analysis.  
- Vintage: 2024 (ACS 1-year)  
- Link: https://www.shadac.org/news/2024-american-community-survey-acs-health-insurance-coverage-data-rising-uninsured

**5. medicaid_population_share** [external source]  
- Basis: KFF state Medicaid fact sheet (Medicaid + CHIP enrollment as share of population); births share per KFF/DC Action.  
- Source: KFF, 'Medicaid in the District of Columbia' (May 2025); enrollment incl. Alliance per healthinsurance.org.  
- Vintage: 2025  
- Link: https://files.kff.org/attachment/fact-sheet-medicaid-state-DC

**6. leverage_ratio** [ledger-derived]  
- Basis: Function of DC's blended federal share (FMAP). Derives from the ledger; for a DC fork the ledger carries DC's 73.2% blended share (MACStats Ex.16: federal $3,199M / total $4,372M).  
- Source: MACStats Exhibit 16, Medicaid Spending by State, Category, and Source of Funds, FY2024 (DC line).  
- Vintage: FY2024  
- Link: https://www.macpac.gov/wp-content/uploads/2026/01/EXHIBIT-16.-Medicaid-Spending-by-State-Category-and-Source-of-Funds-FY-2024.pdf

**7. hr1_squeeze** [modeled estimate]  
- Basis: ESTIMATE, state perspective, CARE basis. Reduction measured against total DC Medicaid benefits (federal+state care dollars), ~$4.14B FY2024 grown ~5%/yr. Federal funding cut run through the national year-by-year ramp and provision timing, calibrated to the published full-phase anchor (national federal Medicaid -12.7% in 2029, Commonwealth Fund), then grossed up to care via DC's ~73.8% benefits federal share. DC's own KFF 10-year and CF 2029 rows live in chart/image appendices and should replace the scaled values when extracted. Excludes the separate, unpassed FMAP-recalculation threat (~$731M-$1.1B/yr).  
- Source: Commonwealth Fund (Ku et al.), H.R.1 funding cuts brief, Jun 2026 (2029 = -12.7% national, $90.9B; cumulative $904B by 2034); KFF state allocation of CBO estimates, Jul 2025; CBO P.L. 119-21; provision timing per Georgetown CCF, Urban Institute, Pew.  
- Vintage: 2025–2034 window; 2029 anchor from Jun 2026 brief  
- Link: https://www.commonwealthfund.org/publications/issue-briefs/2026/jun/hr-1-funding-cuts-rural-health-transformation

## Reconciliation notes (methodology, not for the infographic)

- Fact #3 (long-term care): the Sankey shows fee-for-service LTC (~30% of DC benefits, CMS-64 basis). The headline uses the comprehensive CMS/Mathematica LTSS measure that includes managed LTSS and PACE (~mid-to-high 30s%, national benchmark 33.5%). The difference is managed LTSS, which CMS-64 does not itemize. Both are correct on their own basis.
- Fact #6 (leverage ratio) is the only ledger-derived headline: it is a function of the jurisdiction's blended federal share (FMAP). For a DC fork the ledger carries DC's 73.2% blended share, not the national 64.7%.
- Fact #7 (H.R.1) is a modeled estimate, not a published DC-by-year figure. CBO/KFF publish 10-year totals; the year split is our derivation from the national ramp and is tagged 'modeled'.

## Custom analyses (state-specific — NOT portable across states)

### Economic ripple: tax base & health-workforce effects of a ~13% provider cut (2029)  [draft] [modeled estimate]
*Question:* If DC Medicaid provider spending falls ~13% by 2029, how does that hit DC's tax base and the employability of its health-union workforce?

*Basis:* Scaled from Commonwealth Fund national IMPLAN ratios (~$1.30 lost GDP and ~$0.10 lost state/local tax per $1 of federal Medicaid cut; ~half of job losses inside health care) applied to DC's ~$500M FY2029 federal cut / ~$650-730M provider-revenue cut, then adjusted for DC's tax and workforce structure. Order-of-magnitude, not a DC-specific IMPLAN run.

- **tax base:**
  - **naive local revenue loss:** ~$45-55M/yr (national ratio applied blindly)
  - **adjusted local revenue loss:** low-to-mid tens of millions/yr, with much of the true damage exported to MD/VA
  - **why lower and exported:**
    - Home Rule Act bars DC from taxing non-resident wages; >60% of the DC workforce and ~2/3 of income earned in DC are non-resident (mostly MD/VA), so the income-tax channel is muted and lands on the suburbs.
    - >50% of DC property is tax-exempt and the major hospitals are nonprofit, so there is little property-tax base to erode.
    - The metro supply chain is regional, so indirect/induced losses leak across the borders.
  - **secondary pressure:** More uninsured residents -> more uncompensated care and more demand on the locally funded Alliance; distressed providers will seek local bailout dollars.
  - **irony:** The same commuter-tax prohibition that drives DC's structural deficit also insulates its tax base from commuter health-job losses; but resident workers (Wards 5/7/8) are exactly whom DC taxes and serves.
- **health workforce:**
  - **jobs at risk:** Order of several thousand across the DC economy, ~half in health care; a substantial share are commuters whose jobs and income-tax effects sit in MD/VA.
  - **most exposed:** Long-term care (nursing homes, home care) - the most Medicaid-dependent sector and the most unionized low-wage segment, and DC is LTC-heavy. Then safety-net hospitals (Howard, Cedar Hill) and FQHCs (Unity Health Care, Mary's Center, Community of Hope).
  - **union footprint:** 1199SEIU (hospitals, nursing homes, home care, clinics, pharmacies) plus the nurses' unions.
  - **mechanism:** Layoffs, unit closures, hiring freezes, hours/wage pressure (template: NewYork-Presbyterian cut ~1,000 workers incl. 121 1199SEIU caregivers + 65 nurses, closing units). Union contracts cushion individuals (seniority/bumping/severance) but positions still contract; lower-seniority and new entrants are hit hardest.
  - **compounding:** DC's CFO already projects ~40,000 lost federal jobs and a mild recession this decade; health care was the cushioning sector, so this cut removes the shock absorber in the same window.
- **swing factor:** Whether DC backfills the provider-tax/SDP cuts with local dollars (protects jobs, deepens the budget hole) or lets them flow through as provider-revenue cuts (protects the budget, costs the jobs).

*Sources:*
- Commonwealth Fund (Ku et al.), H.R.1 funding cuts brief — IMPLAN ratios — https://www.commonwealthfund.org/publications/issue-briefs/2026/jun/hr-1-funding-cuts-rural-health-transformation
- Brookings, DC statehood fiscal implications — non-resident income, structural deficit — https://www.brookings.edu/articles/if-the-district-of-columbia-becomes-a-state-fiscal-implications/
- Tax Foundation — federal law bars DC taxing non-resident income — https://taxfoundation.org/research/all/state/state-income-taxes-nonresidents/
- 1199SEIU — DC contract footprint — https://www.1199seiu.org/news/contracts
- NYSNA/1199SEIU — NewYork-Presbyterian layoffs (mechanism template) — https://www.nysna.org/press/healthcare-workers-spoke-out-and-demanded-immediate-end-newyork-presbyterians-cuts-staffing
- 1199SEIU 'Fighting Care Cuts' — LTC Medicaid dependence — https://www.1199seiu.org/magazine/fighting-care-cuts
