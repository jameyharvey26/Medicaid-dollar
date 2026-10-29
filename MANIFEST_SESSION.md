# Session manifest — 2026-10-29, afternoon

Focus: the web explorer. Four panels live — US FY2024, US FY2030, DC FY2024,
DC FY2030 — with the District's panels showing the named plans. The paper
work in this session was what had to happen first, not the object.

## The repo could not run outside Claude's cloud sandbox

Ten hardcoded paths across eight files wrote to `/home/claude/...` or
`/mnt/user-data/outputs/...`. Those directories exist only inside the sandbox
the code was written in; on a Mac `build.py` died on line 33 before drawing
anything, and so did the explorer, deck, xlsx, docx and publish builds. This
is why nothing in the repo ran on JW's Mac on 29 October, and it would have
stayed broken after the Python install that was blamed for it.

| file | was | is |
|---|---|---|
| `build.py` | `/home/claude/nat` | `build_out/nat` under the repo |
| `build_explorer.py` | both | the repo folder |
| `build_xlsx.py`, `build_doc.js` | `/home/claude/...` | beside the module |
| `build_deck.py`, `deckfit.py` | `/mnt/user-data/outputs` | the repo folder |
| `publish.py`, `explorerproof.py` | `/mnt/user-data/outputs` | the repo folder |

`build_out/` and `reference_renders/diffs/` are gitignored.

## `INSTALL WHAT PYTHON NEEDS.command`

New. Triggers Apple's command line tools, installs resvg_py, pymupdf, pillow
and playwright, fetches the headless browser, and reports in plain language.
It says in its own header that the dialog macOS shows is Apple's, about 600MB,
and not Visual Studio — which is what the prompt was read as.

## renderproof: nine panels moved, for two unrelated reasons

Established by rebuilding at 69f61bf, the commit the register was blessed at,
where all fifteen panels reproduce BYTE FOR BYTE on a different machine — so
the renders are reproducible and the gate means what it says — and then
bisecting the five commits since.

- The three DC FY2024 panels moved on their data: eleven figures, the payer
  column re-based on CY2024 Title XIX reporting and the service fan drawn on
  the assumed national mix. **Blessed, with that reason.**
- Six national FY2030 panels moved at **c518476** — HR-1 terminals pinned to
  the fan (`term_dy`) rather than to absolute canvas y, so the geometry
  exports to the engine. No figure changed; terminals move about a pixel.
  **Left unblessed on JW's instruction**, so the flag stays planted until the
  frozen v8.0 question is settled. Written up in `RENDER_DEFECTS.md` so it is
  not re-derived every session.

`renderproof --bless` grew `--only`, because blessing all fifteen under one
reason would have filed a DC reason against six national panels. One fact,
one declaration applies to blessings too.

## The DC FY2030 panel

Three lanes had no District figure. Now:

- **Seniors lane (71101) DERIVED**, on the District's own QMB-only enrolment
  as a share of the national QMB-only count, applied to CBO's score. Both
  counts published; both checked to be the same definition before dividing.
  $2.09 per $100 against the national $1.28 — the District is
  over-represented in that group relative to its spending, because it runs
  the QMB group ONLY, to 300% FPL against a federal floor of 100%. Published
  as an UPPER BOUND for that same reason, with the band running down to zero
  and the acquisition that would close it named.
- **Paperwork lane (71102) ASSUMED** from the national share, behind the
  named `assumed_levers` switch.
- **Leftovers lane ASSUMED** from the national residual, same switch, under
  protest recorded in `DC_ENGINE_TODO.md`: the national lane is a remainder
  and the District lane carries three named provisions, and they are not the
  same quantity.

With every lane carrying a figure and the FY2024 service fan carried forward,
**the ledger now passes the full conservation gate**. The six pinned faults
are gone and `build_dc_2030` goes back to `LD.gate`; the pinned set is kept
for the `assumed_levers` off path, which still conserves nothing and should
not.

## Plate defects, all three

- Absent lanes drew as `−$0.00`. `placeholder.py` gained a declared `WIDTH`,
  `compose` reads which lanes are absent off the ledger, and `sankey` draws
  them violet, hatched, labelled "placeholder — no figure acquired", with no
  `trace()` because a placeholder is not a quantity.
- The declarations column ran eighty lines into space for thirty, struck
  through the Medicare Savings terminal and finished under the tracker. New
  `View.declarations_below` draws it as a full-width three-column band under
  the tracker and grows the draft canvas by what it used. Not a smaller font.
- Medicare Savings no longer overlaps anything; it was the declarations
  column running through it.

## The engine

- `DC|2030` added to `engine_data_export.PANELS`; `ledger_dc_2030` gained
  `build()` so it looks like every other ledger module, and re-exports
  `PLAN_PALETTE` so the plans keep their reserved colours.
- The exporter now REFUSES to write a panel with an HR-1 lane that has no
  figure, rather than letting `{"absent": ...}` reach a renderer that would
  draw it as zero.
- The dead-cell card was rewritten generic. It had described the DC FY2030
  panel's absence in prose and would have gone on doing so after the panel
  existed; it now names what is missing from the key and nothing else.
- The trunk label names the jurisdiction — every panel said "100 Dollars of
  Medicaid Spending", so a screenshot of the District's hundred was
  indistinguishable from the nation's.
- The absent-split note drew as one unbroken line across the flow. Shown
  short, with the whole of it on hover; `txt` gained a `tip` argument.
- `engine_fonts.py` is new: Jost and Nunito travel inside the file, from
  `paper_fonts/`, so a bad connection in a room cannot change the typeface
  every layout figure is measured against. Idempotent.

## New documents

| file | what it is |
|---|---|
| `DC_ENGINE_TODO.md` | every District assumption now on the plate, worst first, each with what would replace it and who would have to be asked. |

## Still true at close

**No District figure is signed.** Not one, in either year. Every demo carries
that stipulation.

The six national FY2030 panels are unblessed by choice. `renderproof` is red
and `gates.py` will report it; `RENDER_DEFECTS.md` says why and holds the
command that closes it.
