# The NAIC route

Pre-Phase 0. Written 2026-09-15. Establishes whether Medicaid underwriting gain
can be obtained from statutory filings, on what terms, and at what price. No
figure has been pulled yet; this is the route and its cost.

---

## 1. The exhibit, named

**Health annual statement blank, Page 7, Analysis of Operations by Lines of
Business.** Title XIX Medicaid is its own column. The NAIC risk-based capital
instructions define that column as business where the entity, for a fee, agrees
to cover the full medical costs of Medicaid subscribers, and state that the
Title XIX Medicaid premium line ties to Page 7, lines 1 and 2.

That page carries premium, incurred claims, administrative expense and net
underwriting gain in the Medicaid column. It is the only routine filing that
reports Medicaid **profit** rather than Medicaid **revenue**, and every licensed
entity writing Medicaid risk files one.

Filing deadline is 1 March for the preceding calendar year, so CY2025 statements
are on file now and CY2024 has been on file since March 2025.

## 2. Access, priced rather than worked around

Two routes, and they are not alternatives — they cover different entities.

**NAIC InsData.** The purchase channel. Requires an account. Annual Key
Statement Pages are **$13.00 per company-statement**; quarterly pages are $4.25.
CSV rather than PDF is quoted separately through the Insurance Data Products
department. NAIC states it does not offer refunds or exchanges.

Page 7 is inside the Key package. So is everything else the work needs, which is
the finding that changes the shape of the job — see section 4.

**The domiciliary regulator, free.** DISB publishes Health Entity financial
statements for entities domiciled in the District, drawn from the electronic
filings, posted within about ten business days of receipt, with a caveat that
later amendments may not yet be reflected. That covers the DC comprehensive
plans and HSCSN at no cost.

Coverage is uneven across the country. Some departments post health entity
statements; some do not. The national pull therefore goes through InsData and
the DC pull does not need to.

**A boundary, stated.** Purchasing and account creation are JW's to do. The
route is established and priced; it is not executed.

**A second boundary.** disb.dc.gov refuses automated requests, so the DC
statements have to be downloaded by hand. The page is confirmed to exist and to
carry health entity annual statements; which entities and which years are
posted has not been enumerated.

## 3. Entity, not brand

Filings are by licensed legal entity. For DC:

| Plan as the reader knows it | Licensed entity | Domicile |
|---|---|---|
| AmeriHealth Caritas DC | AmeriHealth Caritas District of Columbia, Inc. | DC |
| Wellpoint DC (formerly Amerigroup) | Amerigroup District of Columbia, Inc. | DC |
| MedStar Family Choice DC | MedStar Family Choice DC | DC |
| HSCSN | Health Services for Children with Special Needs, Inc. | DC |
| UnitedHealthcare District Dual Choice | UnitedHealthcare Insurance Company | not DC |

Four of the five are DC-domiciled and land on the DISB page. The fifth does not,
and it is the worked example of the entity problem: United's District Dual
Choice Medicaid wrap sits inside a multi-state entity's Title XIX column, not in
a DC-domiciled filing. Its DC portion has to be recovered from Schedule T, or
the lane stays absent.

Domiciles above are inferred from the plans' DC-only operation and have not been
verified against the Jurat page. Verify on the pull.

## 4. What is actually inside the $13

The Key package is not just Page 7. It also carries:

- **Schedule T — Premiums and Other Considerations.** Premium by state. This is
  the published answer to the multi-state entity allocation problem in section 3.
- **Schedule Y Part 1 — Organizational Chart.** Parent to subsidiary. This is
  the ownership mapping half of EN-43.
- **Underwriting and Investment Exhibit Parts 1, 2 and 3** — premiums, claims
  incurred, and analysis of expenses.
- **Exhibit 1 — Enrollment by Product Type.** Denominator for PMPM.

Schedule Y Part 3, Ultimate Controlling Party, is in the Non-Key package at the
same $13.

**Consequence for EN-43.** The brief scoped the NAIC pull and the SEC ownership
mapping as separate work. They are not. The parent-to-entity chart ships in the
same statement as the Medicaid column it needs to be applied to, at no extra
cost. SEC filings remain the check on it, not the source of it.

## 5. What is inside the Title XIX column, and what is not

Open, and it is the item most likely to bite.

An entity may book state-only programs in the Title XIX column. DC has exactly
this: the comprehensive plans' revenue carries DC Healthcare Alliance and
Immigrant Children's Program enrollees, which are locally funded and outside
the federal Medicaid spine. Whether those land in Title XIX Medicaid or in Other
Health Risk Revenue has to be read off each statement, not assumed.

Two further scope questions, both to be answered on the pull rather than now:
whether the column is net or gross of reinsurance and risk corridors, and how
directed payments pass through it.

## 6. Basis

Statutory filings are **calendar year** on an **incurred** basis. The ledger
spine is **federal fiscal year** on CMS-64 **total computable**. Those do not
reconcile without a stated bridge. Any figure taken from here carries
`basis="statutory, calendar year, incurred"` and does not silently sit beside a
CMS-64 figure.

## 7. Status

Pre-Phase 0 is **not closed**. The route is established, the exhibit is named,
the access terms are priced and the entity list is drawn. No number has been
obtained.

Closing it requires, in order:

1. Download the four DC statements from DISB by hand. Free.
2. Read Page 7 Title XIX for each; record premium, incurred claims,
   administrative expense, underwriting gain. Check Alliance and ICP treatment.
3. Recover United's DC Medicaid wrap from Schedule T, or declare it absent.
4. For the national figure, draw the entity list from Schedule Y Part 1 of the
   parent holding companies, then price the InsData order at $13 per entity-year.
