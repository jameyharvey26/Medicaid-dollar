# Obsolete artifacts — proposed for deletion at the next commit
Built 19 September 2026. Nothing has been deleted. Reachability was tested by
walking imports from the seven gates, not by eye.

## A. Recommend deleting

| file | why |
|---|---|
| `byteproof.py` | Retired 18 September and replaced by `renderproof.py` (S-104). Nobody imports it. Still in the repo. |
| `render_v4.py` | Superseded by `render_v4_1.py`. Nobody imports it. |
| `medicaid_dollar_sankey.html` | Pre-ledger national diagram. No tracker line, no ledger, superseded by the build. |
| `medicaid_dollar_sankey_DC.html` | Pre-ledger DC diagram. Same. |
| `dc_preview.png` | Preview of the pre-ledger DC diagram. |
| `NEXT_SESSION_PROMPT_3.md`, `NEXT_SESSION_PROMPT_5.md` | Superseded briefs. `_6` is current. The manifest carries the history. |
| `build_palette_test.py`, `palette_color.png`, `palette_grayscale.png` | One-off palette proof. `palette.py` is imported by nothing except this script. |
| `graffle.py` | OmniGraffle export path. Imported by nothing, referenced by nothing. |
| `read_comments.py` | Imported by nothing, referenced by nothing. |

## B. Do NOT delete — looks dead, is not

| file | why it stays |
|---|---|
| `build_sankey_dc.py` | **Imported by `ledger_dc.py` and `ledger_dc_2024.py`.** The live DC panel still reads constants out of the pre-ledger script, including the uncited $425.3M and $411.2M plan revenues. It is not dead code, it is the DC panel's data source, and it cannot go until those figures are re-homed. |
| `fmap.py`, `phasein.py`, `ramp.py` | No gate reaches them, but `tobe2030.py` imports `fmap` and `phasein`, `fmap` imports `ramp`, and the FY2030 ledger's basis prose names all three as the derivation path. |
| `financing.py` | Imported by nothing, but it is the only written record of the financing derivation. Retire it into the endnotes before deleting it, or lose the method. |
| `html2typst.py`, `render_typst.py`, `paper_national.typ`, `Medicaid_Dollars_National_TYPST.pdf` | The Typst port. Deferred, not obsolete (SESSION_START §8). |
| `build_xlsx.py`, `medicaid_dollar_data.xlsx` | Pre-ledger, but the workbook is a deliverable people have. Kill only when you have decided nothing downstream reads it. |
| `build_doc.js`, `medicaid_dollar_methodology.docx` | Same. |
| `build_headlines.py`, `headlines.json`, `headlines_DC.md` | Not part of the paper build. Unclear whether still live for you. |
| `encoding_specimens/` | Reference specimens. Small. |
| `synth.py` | Imported by `coverage.py`. Its render output is excluded at commit, the module is not. |
| `paper_national_v4.html`, `Medicaid_Dollars_National_DRAFT_v4.pdf`, `Medicaid_Dollars_National_DRAFT_v5.0.pdf` | **JW, 19 September: whole-number versions are kept.** Every `.0` release of the manuscript stays in the repo as a reference point. Point releases (`v4.1`, `v4.2` …) are superseded and may go; `v4.0`, `v5.0` and so on do not. |

## A2. Deleted in this commit (already removed from the package)

These two were renamed, not dropped, but git sees a rename as a delete plus an
add. **GitHub Desktop will not remove them on a drag-in — delete them by hand.**

| file | why |
|---|---|
| `paper_national_v4_1.html` | Renamed to `paper_national_v5_0.html`. A point release. |
| `render_v4_1.py` | Renamed to `render_v5_0.py`. |

`Medicaid_Dollars_National_DRAFT_v4.1.pdf` is left in place unchanged.

## C. Questions this raised

- `ledger_dc.py` and `ledger_dc_2024.py` both exist; `instances.py` imports the
  first, `build.py` the second. Two DC ledgers, one live.
- `ledger_2030.py` and `ledger_national_2030.py` both exist; `build.py` imports
  both. `ledger_2030.py` was also `byteproof.py`'s only other caller.
