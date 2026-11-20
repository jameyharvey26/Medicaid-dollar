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

## 2026-11-11

- D-138 · `teachingproof._root()` is fixed. It parsed `build.py`'s OUT with a regex that matched only a quoted literal, and `build.py` declares `OUT = os.path.join(REPO, "build_out", "nat")`, so the match never fired and the fallback returned the repository's PARENT directory. Every panel read MISSING with the advice "run build.py" — precisely the failure the function's own docstring says it was written to prevent, reintroduced when OUT moved. It now reads the quoted segments off the OUT line and joins them under REPO. The gate has been reporting nothing since OUT moved, and nothing noticed.
- D-139 · With D-138 in, `teachingproof.py` FAILS, and it should. It reports 283 strings the teaching register does not account for, 14 of them claimed as ported where the engine emits no such string. The gate was green in the 27 October notes because it was measuring an empty set. EXPECT is NOT updated to absorb this: the register is behind the panels and that is a real debt, not a gate to re-pin. Nothing here attempts to close it.
- D-140 · `build.py`'s pinned beneficiary-overlay advisory is repinned from y=673 to y=672. D-133 moved the FY2030 lane values and the overlay shifted a pixel with them; it is the same advisory about the same overlap. Pinned again by coordinate rather than loosened to a substring, because a geometry advisory that stops naming coordinates stops being a pin.
- D-141 · The nine FY2030 reference renders are re-blessed, with D-133 and the seven lane values named in the blessing reason. The FY2024 and DC panels did not move, which is the check that the change was confined to what D-133 said it would touch.
- D-142 · Two gates cannot be run from the Cowork Linux VM: `anchorproof.py` and, by dependency, anything else that drives the engine in a browser. The VM's egress refuses Playwright's browser download, and nothing in the repo should be changed to accommodate that. `engine_texts.json` for this build was produced by running `engine_texts.py` in the cloud container against the same engine file and committing the result back; `anchorproof.py` was attempted there too and could not complete — the engine loads but never paints `#plate svg` in that container, with no page error. Both gates must be run on a machine with a working Playwright install before this build is published. They are NOT reported here as passing.

## 2026-11-18

- D-143 · The District's two composite HR-1 lanes are written out of the ledger and five District-derived lanes are written in. Section 71102 becomes `Blocked renewal automation` and `Blocked reconsideration period` (D-123); the leftovers lane becomes `LTSS home equity cap`, `Legal immigrant eligibility` and `Retroactive eligibility` (D-118). `ABSENT_LEVERS` is now empty and `_ASSUMED` has nothing left to turn on: no lever on the FY2030 District panel is absent, assumed, or carrying a national figure under a District label. Each new lane inherits the charge and reach of the lane it came out of, unchanged — splitting a lane is not a reason to move where in the lifecycle its dollar stops. The District's drawn HR-1 total falls from 10.3406 to 9.1833 per $100, because the two lanes removed were worth 1.6953 between them and the five that replace them are worth 0.5380.
- D-144 · The three provisions are struck on CBO's published FY2030 section figures, which supersedes both D-119's ten-year-total spreading and D-120's statutory step schedules. Workbook 61570 publishes section 71108, 71109 and 71112 by fiscal year, so the FY2030 position is read (D-133). Per $100: 0.0026, 0.0561, 0.0446, against the 0.0030 / 0.0533 / 0.0406 recorded at D-118 and the 0.0047 / 0.1084 / 0.0734 the 3 November preview drew. The only modelled step left is the District share, and it is the share construction the rest of the file already uses: long-term care spending for the home equity cap, because that is the base it bites on, and the hundred for the other two.
- D-145 · The section 71102 split is implemented on the District's own renewal record rather than on the national rate. CMS's Eligibility Operations and Enrollment Snapshot, March to June 2026 (D-124), puts District ex parte renewal at 71.5% against the national 47.5%, so District headroom is 28.5% against 52.5% and its exposure ratio is 0.5429. The dollars divide between the two lanes in proportion to the District's own two rates — headroom 28.5% against procedural disenrolment 13.75% — giving 0.2932 and 0.1415 per $100 against band ends of 0.5401 and 0.2606. One exposure ratio for the lane total and one proportional split: that is the single modelled step D-123 declares, and the monthly table is now a sourced constant rather than a figure in a research document.
- D-146 · Four engine defects are fixed in `engine/explorer_engine.html`, ported from the 3 November preview. The claims fan forks from each plan's own arrival block instead of a shared lane cursor, so an MCO's claims leave its own bar and composite into the provider bars in the ledger's proportions — this was wrong on the national panel too, not only the District's. Retention re-allocation carries a released AMOUNT rather than a ratio, so moving the MCO administration slider no longer scales the room reserved for peels charged after the claim and the Sankey stops stepping. `money()` keeps four places below a cent, so a sub-cent lane reads as a figure rather than as $0.00. A slider with more than three marks grows its label row and drops alternate labels.
- D-147 · The engine's `IMPLIED` constant is corrected from 0.181112 to 0.175707. The work-reporting band's marks are placed by ratio against that rate, so a stale value put Arkansas and New Hampshire in the wrong places on a correct default. The band also gains Urban's low-mitigation end (D-121).
- D-148 · `DCBANDS` is GENERATED from the ledger and pasted into the engine, which is a declared leak of the same kind as `IMPLIED` and no better: a band can now drift from the ledger it describes, and only a person re-running the generator will notice. `engine_data_export.py` should emit the bands alongside DATA. Until it does, a ledger change means regenerating the block. The provider tax lane is deliberately absent from the table: its floor could not be reproduced from the current constants, and a band end nobody can re-derive is worse than no band.
- D-149 · Generated artifacts come out of the index and stay out. `medicaid_dollar_explorer.html` and `explorer_data.json` are rewritten by `build_explorer.py` on every run, nothing reads a committed copy, and they produce a diff of about 36,000 lines per rebuild; they were added by accident in `551ba9f` and are untracked again here under the same rule `.gitignore` already applies to every other build output. `Claude outputs/` is ignored outright: it is scratch, and a 49MB zip reached pushed history through it. Untracking does not remove that blob from the pack — only a history rewrite does, and that is the one case where rewriting is worth it, because no forward fix can reach it.
- D-150 · The District folds Exhibit 17's collections line pro rata across the capitated and fee-for-service lanes by each lane's share of gross, which is what D-83 does nationally. It had been taking the whole of the −$10M out of wrap-around services alone: four of the five diagram nodes matched the published columns to the dollar and wrap-around was drawn at $222M against the $232M Exhibit 17 prints. Wrap-around is the catch-all node, the one that already absorbs what does not fit a named column, so the reduction was invisible by construction and nothing in the repo recorded it. Exhibit 17's nine fee-for-service columns for the District are read into `basis_dc.py` for the first time — the column order verified against the exhibit's own TOTAL row, which reproduces `basis_national.py`'s nine constants exactly — and the five nodes derive from them rather than being typed, so Tier 1.3's "mapping of nine columns to five nodes" can now be read instead of trusted. An assert holds the gap between gross lanes and what reaches the payers equal to the collections line. The three Exhibit 17 lines become anchors in their own right — `ex17.ffs_gross`, `ex17.managed_care`, `ex17.collections` — because Tier 1.2 asked for a signature on a reconciliation that existed only as arithmetic and a comment. Per $100: wrap-around 17.62 → 17.80, fee-for-service lane 51.46 → 51.57, MCO capitation 40.30 → 40.20, long-term care 35.30 → 35.21, hospitals 14.26 → 14.23, physicians and clinics 15.85 → 15.81, Rx drugs 4.08 → 4.07. JW's ruling: one rule everywhere, so the next state inherits it.
- D-151 · Every District plan figure comes from one rule: the Title XIX Medicaid column of the plan's own annual statement, lines 7, 17, 19 plus 20, 21 and 24, apportioned only where that column covers more than the District. Three plans carried three different errors. Wellpoint's two expense lines were apportioned from the entity total on a comment saying they are published for the entity; they are not, the statement prints both in the Title XIX column, and the apportionment was wrong by $766,632. MedStar took revenue from Schedule T and costs from the Title XIX column, which are not the same quantity — Schedule T is direct premium and the column is net of ceded reinsurance and includes other health care revenue — a difference of $851,976 before apportionment. AmeriHealth's line 21 was invisible: the plan set $5,003,850 aside against Title XIX contracts it expected to lose on, a premium deficiency reserve in full, and its published underwriting gain is after it, so about a third of what this panel calls AmeriHealth's margin is a reserve movement rather than earnings. AmeriHealth's FIGURE IS UNCHANGED and deliberately so: the money did not buy care and is not administration, it stayed with the plan, and retention has to close, so deducting it would leave a dollar undrawn (S-108). What was wrong was the description, and the two parts are now named on the figure. `agreement()` asserts every plan's residual margin equals its filed underwriting gain plus its filed reserve movement, on filed dollars, before the scaling that is ours. STATUS: the nine plan figures and the three folded lanes were MEASURED and are not measurements — no statement contains $814.071M, and no source publishes a $40M District dual-and-PACE line or a $1,762M MCO lane — so they become MODELLED with the filed figure named in each note, which is what the national panel already does with its own folded lane. The five fee-for-service cells move the other way: they carried the generic spine source and a STALE note naming no document a signer could open, and they are Exhibit 17 readings, so they now say so. Measured figures on DC FY2024 fall from 26 to 15, which is the honest count.
- D-152 · OPEN, not implemented. A state gets its own signature process, the same as national — JW's ruling, 18 November. `_sign` lives inside `ledger_national_2024.py` and is called only there; no District ledger references `signatures`, `SIGNED`, `UNSIGNED` or `REVIEW`, so District entries added to the register today would do nothing, and `coverage.py dc` will go on reporting every DC figure as unverified whatever anyone agrees to. The register is also a flat namespace the District reuses exactly — `scale`, `peel.admin`, `peel.medicare`, `payer.ffs.capitation`, `source.federal` and five more — so a shared dict lets a District signature silently lapse a national one, which is the 16 September failure pointed in a new direction. Per-jurisdiction registers, not panel-prefixed keys in one file: `signatures.py` keeps national, `signatures_dc.py` is new, `_sign` moves into `ledger.py` or a small `signing.py` and takes the register as an argument, and adding the fifth state becomes adding a file rather than editing one four other panels read. This BLOCKS all District signing and is the first thing to do next session.
- D-153 · The District FY2030 panel enters the render register. Three things had to be true and none of them was. It carried three violet placeholders, which is why `build_dc_2030` wrote to `drafts/` and said so — D-143 derived all five District lanes and `ABSENT_LEVERS` is empty, so there are none left and the reason expired. `sheet.py` declared it a blank with `DC_2030_BLOCKED` saying DC-specific lane values do not exist and the national mix cannot be scaled; both were true when written and neither is now, so the blocking note is retired in place rather than deleted, because what a panel refused to draw and why is part of the record. And it could not be drawn at all: `views.V_DC_2030` still named `Blocked Medicaid enrollment rule` and `DC provisions not separately scored`, the two lanes D-143 retired, so `PeelSum.resolve` raised KeyError before anything rendered — and nothing noticed, because `build_dc_2030` was never wired to `build.py`'s entry point. The ledger was right for three weeks and no picture of it could be made. It is now built by `build.py dc`, measured by crossings, compared by renderproof on every run, and blessed with ten tributaries each carrying its own name, zero crossings in the margin, and the tracker line adding up as printed. `anchorproof.py` has still never run against it: that gate drives the engine in a browser and D-142 stands, so the engine's version of this panel remains unproven even though the paper one is now in the register.
- D-154 · An alias copies GEOMETRY and never the printed name. `outflows.ALIASES` was written for a RENAME — one DC lane onto one national lane — where inheriting `label` was harmless. D-143 made it a SPLIT: five District lanes onto two national geometries. Copying the label wholesale printed "Other" three times over the three named provisions D-118 exists to name, and "Medicaid enrollment rule suspended" twice over the two lanes D-123 exists to separate. The panel undid both decisions in the drawing while the ledger held them correctly, which is the whole failure mode of a picture nobody has looked at. Each District lane now declares its own printed name. Where a lane LEAVES the trunk is likewise layout and not a claim about the flow, so the five lanes take their own trunk slots: sharing two slots put two curves out of one point and they crossed in the margin at (766,745), which rule 2.9 forbids. `views._dc_of` preferred the national entry unconditionally and discarded those slots; it now prefers the District's own. Charge and reach are untouched and stay identical to the parent lane's, which is what D-143 claims and what `ledger_dc_2030.HR1_DC` holds.
- D-155 · A lane smaller than a cent prints as a figure, not as zero. `sankey.py` formatted every tributary amount at two places, so the District's FY2030 home equity cap lane — 0.0026 per $100 — drew as "−$0.00", a number claiming the lane is empty. The renderer's own placeholder branch refuses to print exactly that string, with a comment saying why; the same defect arrived from the other direction and nobody had drawn a sub-cent lane on paper before. D-146 fixed this in the engine. Below half a cent the paper renderer now shows four places and above it nothing changes, so no figure on any blessed panel moved.
- D-156 · `gates.py` EXPECT is re-pinned for the sixth panel: three frozen advisories where there were two, four tracker lines where there were three, six clean panels where there were five. All three counts moved because `build.py dc` draws the District FY2030 panel now. Re-pinned to the new counts rather than loosened to a substring or a minimum, on the same rule as D-140: a count that stops counting stops being a gate.
- D-157 · `anchorproof.py` was never blocked by the missing browser. D-142 recorded that the engine "loads but never paints `#plate svg`" in the Cowork container and filed it as an environment fault, to be cleared by running the gate on a machine with a working Playwright. It is not an environment fault: there has been no `#plate` in this engine since it was restructured. The engine's SVG lives in `#picture`, the selector returned null, and the gate would have failed in exactly the same way on any machine with any browser — including the one it was waiting for. The engine draws all four panels and drew them the whole time; the container was never the problem. Selector corrected, and `("DC", "2030")` added to `enginecrossings.PANELS`, which had never carried it: the engine's largest panel had no gate looking at it at all. Both gates now run and pass against the engine's own render — ten District FY2030 tributaries, none adrift, no crossings in the margin. Run from the cloud container, which has Chromium preinstalled; the Cowork VM still cannot download one and D-142 stands on that narrower point.
- D-158 · `geometry_export.py` exports every outflow declaration, including the District's. It excluded aliases, reasoning that a state edition renaming a lane points at geometry already exported under the national name and that exporting both would put two entries in the engine's spine for one position on the flow. That assumed an alias is a pure rename carrying nothing of its own. D-143 split two national lanes into five District ones and D-154 gave each its own printed name and trunk slot, so the engine had no entry for any of them: all five fell back to the state agency column's left edge, left from x=584, and the engine's DC FY2030 panel carried SIX margin crossings against the paper panel's none, while printing the national labels over the District's lanes. Two entries at one x was never a contradiction — they are different lanes leaving at the same place and no two of them appear on the same panel. The condition is removed rather than narrowed: it was one more thing to be wrong about and it was wrong for three weeks with no gate able to see it.
- D-159 · OPEN, not resolved. The paper and the engine print the District FY2030 source band with the same label and different quantities. The paper reads "Federal 73.2% / State 26.8%", the engine "Federal 72.6% / State 27.4%". Both are arithmetically right and neither is a defect in itself: the provider tax lane is charged at FEDERAL, so the paper band is struck BEFORE the HR-1 levers and the engine's AFTER them. Both artifacts label it the same way and a reader moving between them cannot tell which they are looking at. Which one is correct is an editorial call about what the band is for, and it is JW's, not a quiet edit. The $73.17 and $26.83 figures either side of it agree on both artifacts.
- D-160 · The engine strikes the federal/state band BEFORE the levers, as the paper does. This closes D-159. The engine read `(fed-fb-fo)/hundred` — the share after the HR-1 federal bite and over the post-lever hundred — and printed 72.6/27.4 on the District FY2030 panel against the paper's 73.2/26.8. `sankey.py` strikes it as `(fed-fo)/_ARRIVE`: the bite comes out of the band's drawn HEIGHT but not out of the percentage, because the label answers how the dollar was blended and the geometry answers how much of it is left, and those are different questions. Only a 100-percent-federal peel before the blend moves the share, which is the difference D-70 exposes. `ARRIVE` was already computed in the engine and is the same quantity. JW's ruling, 19 November: show the split before the levers. Every panel now agrees between the two artifacts — DC 73.2/26.8, national 64.5/35.5.
- D-161 · OPEN, diagnosed and not fixed. The engine's national FY2030 panel carries one margin crossing the paper's does not: documented fraud passes under directed payment caps at (1412,839), both leaving CLAIMS for PROVIDERS. The cause is in `dropFor`, the solver that decides how steeply a ribbon leaves. It collects blockers as `b.x > x0+2 && b.x < x1-2 && b.y < y1` — terminals that stop sooner and sit HIGHER — and finds the gentlest drop that gets the ribbon BELOW all of them. It has no symmetric constraint: nothing records what a ribbon must stay ABOVE. Fraud dives to clear a blocker and in diving passes under directed payment caps, whose terminal sits lower than fraud's, so the two cross twice and the detector catches the first. A tiebreak on declared terminal height was tried and is a no-op here, because the order was already right — the fault is in the curve between the endpoints, not in the row order, which is what §2b's own comment says. The fix is a second constraint in `dropFor` and it is a real change to the solver; it is not taken in the same session as the DC work. Note also that a bad patch here is invisible to the crossing gate: a comparator that throws unwinds the sort and every tributary vanishes, and a drawing with nothing in it reports zero crossings. `anchorproof` catches that, because it counts what it measured.
- D-162 · The engine is published as a claude.ai artifact and its question box is declared, so it answers there. The ask panel calls `claude.use('sample')` and was written against the current runtime contract already — null-guarded, with a fallback that says the offline copy has it switched off and everything else works — so nothing in the page changed. What was missing was the DECLARATION: a capability a page uses but does not declare is refused at run time, silently, and the panel would have shown its offline message on the published page with no indication why. Declared as `{sample:{}}`, no images, at contract 0.2.96. The artifact is private to its owner; sharing is JW's to do from its page. The engine file in the repo is unchanged by this and the published copy is a publish of it, not a fork: a rebuild republishes rather than diverging.
