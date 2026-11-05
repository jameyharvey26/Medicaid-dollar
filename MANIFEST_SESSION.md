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

---

# Session manifest — 2026-11-03

Research session worked without JW against `NEXT_SESSION_PROMPT_12.md`, then a
decision pass with him. Findings in `DC_RESEARCH_2026-11-03.md`, questions and
options in `DC_QUESTIONS_FOR_JW.md`, signatures needed in
`DC_SIGNOFF_LIST.md`. Nothing below is drawn yet.

**APPENDED, not replacing.** This file is the only thing `decisions_index.py`
reads, and each session has been overwriting it, which is why `DECISIONS.md`
reports 40 of 117 numbers found. Appending keeps the October register.

## Decisions

- D-118 · The District's leftovers lane draws the three named provisions as three derived figures, not a national residual's rate. CBO scored §71108 at $195M, §71109 at $6.2B and §71112 at $4.2B over ten years; the work-reporting construction puts them at 0.0030, 0.0533 and 0.0406 per $100 of the FY2030 hundred against a placeholder of 1.0587. Closes `DC_ENGINE_TODO` item 1.
- D-119 · The three section scores are drawn on CBO's 21 July 2025 vintage (publication 61570), with the reconciliation gap declared on the plate. The unlisted Chapter 1 sections sum to about $137B against the 28 October supplemental's "Other" of $60.1B, and CBO publishes no decomposition; the six named lanes agree between the two documents to the tenth.
- D-120 · The three provisions' FY2030 position is derived through `phasein.py` from the statutory step schedules, not by spreading the ten-year total evenly. A second rule for a question the repo has already answered once is how two answers get into a model.
- D-121 · `RATE_BAND`'s upper end extends to Urban Institute's low-mitigation scenario, 55%. Urban's figure is a model output and may not enter `RATE_OBSERVED`, whose note declares its members to be the only real-world observations at scale; it sits beside it as a named third end with its own status.
- D-122 · The work-reporting band carries both denominators with the mismatch declared, as `RATE_BASIS_DIFFERS` already does for Arkansas. Urban's implied District base is about 109,000 against `EXPANSION_AT_RISK` of 78,322, which DHCF's own testimony corroborates at 78,000.
- D-123 · Section 71102 is drawn as two lanes, not one, split by mechanism: renewal automation measured on ex parte headroom, and post-termination recovery measured on procedural disenrolment. The District's §71102 dollars divide between them in proportion to those two District rates, which is the one modelled step.
- D-124 · Both §71102 lanes are struck on FY2026 months only, from March 2026 forward. A FY2030 panel describes the District as it now operates, post-cut and post-MMIS; the pre-March regime has ended.
- D-125 · The seniors lane defaults at 19% of QMB-only enrollees above 100% FPL, with the band running to about 50%, and DHCF's own count named as the acquisition that closes it. 19% is the end with a mechanism behind it: what the rest of the country does above the federal floor through SLMB and QI.
- D-126 · The national panel gets its own service-mix declaration in its own words — service totals measured off Exhibit 17, payer split within each bar modelled — and `MIX_BORROWED` stays the District claim. The removal JW ordered on 30 October stands; the defect was one flag carrying two different claims. `ask.js` text changes with it.
- D-127 · `PRIOR_LAW_CAGR` stands at 5.27% and the District's Human Support Services federal series becomes a cross-check on the FY2030 to-be total. `SUPERSEDED_BY` is closed and rewritten: the FY2026 Proposed volume does not contain a Medicaid trajectory, and neither does the FY2027 Approved volume, by design.
- D-128 · The FY2030 zeros in the District's dedicated-tax tables are read as a certification boundary, not a forecast, and the FY2029 step-downs are taken as the real signal. The same volume's Revenue chapter contradicts its own Table 2-3; the contradiction is footnoted and the OCFO asked.
- D-129 · The §71109 status line carries all three facts dated rather than resolving them: the provision is in force federally, DHCF advised something in February 2026, and a Washington-only injunction exists in *Neighborhood House v. HHS*.
- D-130 · The work-requirement slider drives the medically-frail exclusion share, 10.0% to 21%, with CMS's interim final rule and Urban's broad definition as named detents; the lane's dollars follow through the exposed population. The dollar pair — CBO $317.0B against CMS's own RIA at $350.3B — becomes a cross-check, because CMS does not attribute its $33.3B departure to frailty alone.
- D-131 · `AFTER_THE_DEMO` §4 is closed: $2.90–$5.40 was never a range. $2.90 is `peel.medicare`, sourced to MACStats Exhibit 17 and signed 2026-09-18 JW; $5.40 occurs once, in a code comment warning against reading a control mid-drag.
- D-132 · The beneficiary column leaves the frozen spine table and becomes an anchored but unsized SURFACE. Its left edge stays at `PROVIDERS.x1`, its existence stays frozen because the Medicare Savings lever terminates in it, and the pie-to-number-line alignment stays frozen; its width is a renderer choice and `W` is derived from it rather than declared. Paper draws 420 and the engine 200; both are correct. JW, 2026-11-03: the pies are for printed Sankeys and become their own view in the app, not yet designed, so no inflexible rules about canvas sizes. Closes `AFTER_THE_DEMO` §3.

## New documents

| file | what it is |
|---|---|
| `DC_RESEARCH_2026-11-03.md` | the session's findings, with a numbered source register. |
| `DC_QUESTIONS_FOR_JW.md` | the questions put to JW, with options and recommendations. |
| `DC_SIGNOFF_LIST.md` | three tiers of data points needing a signature. |
| `dc_endnotes.py` | generates the District's numbered endnote register from the ledgers' `Fig` records. |
| `DC_ENDNOTES.md` | that register. 139 figures across the two District panels. |
| `DC_ENDNOTE_KEYS.txt` | append-only key order. A DC-EN number is this file's line position; never reorder it. |

## Still true at close

**No District figure is signed.** 0 of 139.

**A defect raised and not closed.** `peel.medicare` is signed at $2.9231 and
`SIGNING_2026-09-18.md` records the move from 2.90 to 2.92, but $2.90 is still
typed in `build_doc.js`, `build_xlsx.py`, `README.md`,
`encoding_specimens/bite_points.py`, the August whitepaper brief, and at EN-19
and EN-27. The lane is right; the figure printed beside it is a cent stale.

**Two repo defects found and not yet fixed.** The service-mix comment in
`ledger_dc_2024.py` compares a share of fee-for-service to a share of total
spending; `DC_NAMED_PROVISIONS` overstates the §71109 injunction. Both are
written up in `DC_SIGNOFF_LIST.md`.

**Nothing from D-118 to D-130 is drawn.** The decisions are taken; the engine,
the ledgers and the paper are untouched.

---

# Decision register backfill

Written 2026-11-03. `DECISIONS.md` is generated wholly from this file, and
this file had been REPLACED each session, so its register could only ever
hold the current session's decisions — every earlier manifest's entries were
dropped the next time `decisions_index.py` ran. That is why the file reported
"coverage is partial" and named backfilling as an open item.

The forty entries below are recovered from the generated `DECISIONS.md` and
written back in parseable form, so a clean regeneration yields them. **Only
the parsed summary survived**; the fuller wording went with the manifests
these came from. Dates and numbers are as the register recorded them.

**This file is now APPEND-ONLY.** Replacing it destroys the register.

## Backfilled from DECISIONS.md — 2026-09-19

- D-76 · FY2030 sources rebased.

## Backfilled from DECISIONS.md — 2026-09-21

- D-78 · The $425.3M "Wellpoint DC" lane is a two-plan composite.
- D-79 · The named-plan block rebases on DHCF CY2024, agreed, not executed.
- D-80 · DHCF plan revenue is not Medicaid.
- D-81 · DC MCOs pay no long-term care.
- D-82 · The non-federal share is decomposed, not replaced.

## Backfilled from DECISIONS.md — 2026-09-25

- D-83 · The payer lanes are derived from Exhibit 17 dollars.
- D-84 · Provenance is stamped, not typed.
- D-85 · The cover figure is cut.
- D-86 · The moratorium labels are renamed.

## Backfilled from DECISIONS.md — 2026-09-26

- D-87 · The spine moves once, and is frozen again.
- D-88 · The flow area gains 40 units.
- D-89 · The Medicare Savings loss leaves the Eligibility Rules bundle.
- D-90 · The artwork is drawn on the page, not on a card.
- D-91 · The Adults row becomes two rows.
- D-93 · The provenance line is stamped, not laid out.
- D-94 · whitespace.py is rebuilt on content, not on ink.
- D-95 · The crops become a family of tapers.
- D-96 · A section starts a page.
- D-97 · The generated figures are drawn at the size of the slot they sit in.
- D-98 · The provisions section is reordered into phase order, and the figures.
- D-99 · The tables follow the diagram, and the whitespace pass is mostly.
- D-100 · Figure 10 joins the taper family instead of being its own drawing.
- D-101 · Bite and reach are two declarations, and the audit that followed.
- D-102 · One incidence model, not two.

## Backfilled from DECISIONS.md — 2026-09-27

- D-103 · The project's public address, in one place.
- D-104 · The incidence model must declare what it leaves out.
- D-105 · The explorer is a build target, not a file.
- D-106 · The diagram goes back, with handles.
- D-107 · One version across all three artifacts, HTML and PDF of each.
- D-108 · A detector that discards its own input in silence.
- D-109 · A panel stops where the knowledge stops.
- D-110 · Everything on the drawing is a handle.
- D-111 · The punch list.
- D-112 · The plate does not move.
- D-113 · A label belongs to the thing it names.
- D-114 · The explorer is 2.3 MB, and opens on a phone.
- D-115 · Two arbitrary numbers doing real damage.
- D-116 · The HTML artifacts are for a screen.
- D-117 · The whitepaper's own address.


## 2026-11-05

- D-133 · The national lane allocation is READ from CBO's section-by-section workbook, not modelled from the statutory step schedules. D-37 recorded that CBO publishes no per-section annual detail; that is false, and workbook 61570 publishes every Chapter 1 section by fiscal year. `ramp.py`, `phasein.py` and `tobe2030.py` each inferred from a step schedule to a dollar, which was the modelled step; `cbo61570.py` now supplies the dollar. The weights are retired in place as `RAMP_RETIRED`, not deleted, because what they cost is part of the record: at FY2029 directed payments ran 55.1% low and the three lanes held at full effect ran 34–47% high; at FY2030 directed payment caps ran 34% low. The chapter total conserved throughout, because the allocation was normalised to it, which is why no balance line ever moved. The published FY2030 figure moves from $10.34 to $10.07 per $100 on the D-70 basis, EN-12 from $10.26 to $9.99, and the District's `CBO_IMPLIED_RATE` for work reporting from 0.181112 to 0.175707, carrying `RATE_DEFAULT` from 0.2142 to 0.20399.
- D-134 · The "Everything else" lane is two quantities of opposite sign and must not carry one ramp weight. It is the fifteen unnamed Chapter 1 sections PLUS CBO's interaction netting: at FY2030, −$16.823B of provisions against +$9.335B of netting, drawn as −$7.488B. `phasein.py` said as much in prose and then weighted the pair at 0.60. The split is now computable by year — `cbo61570.residual_split()` — and the lane is read whole from the chapter total rather than ramped. Separating the two components for their own treatment is NOT done here and is the open item.
- D-135 · The $8.6B section-level wedge flagged in `ramp.py` on 27 August, open task 2, is closed. It is §71119's revenue line: outlays −325,610 less revenues −8,650 gives the −316,960 CBO prints as $317.0B. Both figures are CBO's, on two bases, and `ramp.py` was already on the right one. Nothing moves; the flag and D-26's correction note come off.
- D-136 · The claim in `SOURCES.md` that the 28 October supplemental's figures are "identical to CBO's July 2025 estimate" holds for the six named sections and fails for the chapter: workbook $963.8B against supplemental $886.8B. The $77.0B is interaction netting among Chapter 1 policies, carried inside the supplemental's "Other" line, and it means a section-by-section sum overstates the chapter by about 8% from FY2029 on. Register corrected; the workbook is now a primary source in its own right.
- D-137 · `engine/explorer_engine_PREVIEW_2026-11-03.html` is STALE against D-133 and is not patched here. Its work-reporting band carries the superseded 0.181112 and its three District provision lanes were positioned by the step schedules D-133 retires. A half-updated preview is worse than a declared stale one; the rebuild is the next session's first job.
