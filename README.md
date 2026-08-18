# $100 Medicaid Dollars — DRAFT V.4 (Public Comment)

A quantitative reference showing how $100 of total Medicaid spending flows from
funding sources, through the state agency and three payer lanes, to providers and
the populations that consume each service. Federal fiscal year 2024 basis.

This folder is a self-contained checkpoint of Version 4 (Public Comment). It
contains the three finished deliverables plus the source scripts that generate
them, so the whole set can be regenerated or edited later.

---

## Contents

| File | What it is |
|------|------------|
| `medicaid_dollar_sankey.html` | The infographic — a self-contained HTML/SVG Sankey (open in any browser). |
| `medicaid_dollar_data.xlsx` | Companion workbook: every figure, formula, source and assumption (6 tabs). |
| `medicaid_dollar_methodology.docx` | Methodology, data-sources and assumptions write-up. |
| `build_scripts/build_sankey.py` | Generates the HTML + an `.svg`. Run: `python3 build_sankey.py` |
| `build_scripts/build_xlsx.py` | Generates the workbook. Run: `python3 build_xlsx.py` |
| `build_scripts/build_doc.js` | Generates the docx (uses `docx` npm pkg). Run: `node build_doc.js` |

The build scripts are the source of truth. If you want to change a number or a
label, edit the script and re-run it rather than editing the output files.

---

## The conserved ledger (per $100 of total Medicaid spending)

Every cut below balances; the diagram, workbook and doc all use these figures.

```
Sources:    Federal $64.70 + State $35.30                         = $100.00
  - Administration            $5.07
  - Medicare premiums (duals) $2.90   (returns to the federal govt)
Disbursed                                                          =  $92.03
  split into 3 payer lanes:  MCO capitation        $40.06
                             Dual-MCO capitation   $10.89
                             Fee-for-service       $41.08
  - Plan administration & earnings $5.61
        = plan administration $4.85  ($3.81 non-dual MCO + $1.04 dual-MCO)
        + public-company earnings $0.76 (a subset of margin; est.)
Claims paid (reaches providers)                                    =  $86.42
  - Documented fraud          $0.15
Health services delivered                                          =  $86.27
```

### Six provider nodes ($ per $100; FFS / MCO / Dual)
| Node | Total | FFS | MCO | Dual |
|------|------:|----:|----:|-----:|
| Long-term care | 28.53 | 19.72 | 6.93 | 1.89 |
| Hospitals | 18.66 | 8.68 | 7.84 | 2.14 |
| Wrap around services\* | 13.33 | 4.95 | 6.59 | 1.79 |
| Physicians & clinics | 12.63 | 2.87 | 7.68 | 2.08 |
| Behavioral health | 9.51 | 3.48 | 4.74 | 1.29 |
| Rx drugs | 3.76 | 1.38 | 1.87 | 0.51 |

\* "Wrap around services" = the CMS-64 "Other acute" line + Dental, net of the
behavioral-health carve (labs, imaging, equipment, dental, screening,
transportation, hospice, etc.). Not a one-to-one CMS category.

### Beneficiary mix (% of each node's dollars: Children / Adults / Disabled / Aged)
LTC 1/9/46/44 · Hospitals 23/48/18/10 · Wrap 25/44/19/12 · Physicians 29/48/15/9
· Behavioral 14/48/31/7 · Rx 12/44/28/16. (IPF-balanced to group totals
Children 13.48 / Adults 29.56 / Disabled 24.98 / Aged 18.41.)

---

## Key data sources & vintages
- CMS-64 / MACStats (Feb 2026): total spend $957.4B; benefits $908.8B; federal share 64.7%.
- Capitation $496.1B; FFS-itemized $400.0B (CMS-64 Ex.17).
- Dual managed-care capitation ~$106B — triangulated from the CY2022 MedPAC–MACPAC
  Duals Data Book (the softest figure in the model).
- Managed-care service mix: HMA "New Insights" T-MSIS-based mix, CY2021.
- Plan economics: MLR ~89%, admin ~9%, margin ~2% (Big-Five filings / Georgetown CCF).
- Fraud proxy: MFCU recoveries FY2024 (~$1.4B), drawn not-to-scale.
- Behavioral-health carve ~11% of service dollars (literature 9.3–13%).

## Conventions worth remembering
- Unit is **$100 of total Medicaid outlays** (benefits + admin), split fed/state at 64.7%.
- **Any label change in the Sankey must propagate to the workbook and the doc.**
- The diagram avoids the word "retention" (plan dollars are labeled "administration").
- PBMs are deliberately not broken out.
- Pie labels are a re-expression of provider dollars, not a separately measured flow.

## Open / backlog ideas
- Three state-level political "fork" variants (needs state Medicaid $ + FMAP).
- Firmer public-company earnings carve via 10-K segment allocation.
- Optional PBM "drug-dollar anatomy" inset.
