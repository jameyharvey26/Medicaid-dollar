# Session manifest — 2026-08-29

## New modules (the refactor)
| file | what it is |
|---|---|
| `sankey.py` | the renderer. `render(cfg) -> (baseline, overlay)`. All drawing, once. |
| `instances.py` | one `Instance` per artifact: ledger, steps, HR-1 terminals, tracker, titles. |
| `outflows.py` | column boundaries and the outflow ledger. Geometry declared once. |
| `check.py` | conservation gate. Runs before drawing; failure stops the build. |
| `ledger_2030.py` | FY2030 post-HR-1 ledger computation. |
| `ledger_dc.py` | DC FY2024 ledger, reduced fidelity, absences declared. |
| `build.py` | the only entry point. `python3 build.py [2024\|2030\|dc]`. |
| `build_pair.py` | stacked comparison sheet, now four panels. |

## New analysis
| file | what it is |
|---|---|
| `phasein.py` | statutory phase-in table for P.L. 119-21 and the anchor-year cross. |
| `tobe2030.py` | FY2030 numerator, denominator and per-$100 lane split. |

## New documents
| file | what it is |
|---|---|
| `STYLE_GUIDE.md` | binding diagram rules. A violation is a defect, not a preference. |
| `ARCHITECTURE.md` | state series and vantage views. Ledger / View / Layout seam. |
| `ENDNOTES.md` | numbered endnote register, EN-1 to EN-40. |
| `PAPER_PASSAGES.md` | publication-voice prose written as findings land, P-01 to P-03. |
| `MANIFEST_SESSION.md` | this file. |

## Deleted
`build_sankey.py`, `build_tobe_2030.py`, `build_sankey_2030.py`, `_gen_*.py`.
The text-substitution fork is gone (S-064).

`build_sankey_dc.py` is KEPT. It is not superseded: it is the named-plan DC
diagram, which is a different product and the prototype for the vantage layer
(S-070). It is no longer the DC state artifact.

## Renders
`national_2024_*`, `national_2030_{holds,scales,mixed}_*`, `dc_2024_*`,
`national_pair_2024_2030.png`, `sheet_national_dc.png`.

## Decisions and notes added
D-63 split overhead · D-64 bite phases · D-65 provider tax sources federal ·
D-66 the state artifact is the national view.
S-051 through S-072.
EN-1 through EN-40. P-01 through P-03.

## Verification
Refactor proven a no-op: `national_baseline.png` and
`national_2030_mixed_combined.png` both diff to an empty bounding box against
pre-refactor renders. All three instances pass `check.py`.
