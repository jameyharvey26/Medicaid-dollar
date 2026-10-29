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


---

# Session manifest — 2026-09-03

## Changed
| file | what changed |
|---|---|
| `sheet.py` | NEW. Generalised N-panel comparison sheet. Replaces `build_pair.py`. |
| `build.py` | now calls `sheet.py` instead of `build_pair.py`. One line. |
| `STYLE_GUIDE.md` | 6.3 names `sheet.py`; new 6.3a on N panels and no rescaling. |
| `graffle.py` | NEW. Exports a rendered instance SVG to an OmniGraffle document. |

## Deleted — these must be removed, not overwritten
| file | why |
|---|---|
| `build_pair.py` | superseded by `sheet.py`. |
| `reference_renders/national_pair_2024_2030.png` | stale. No builder produced it after `build_pair.py` moved to four panels. Now regenerated on demand as `sheet_national_pair.png`. |

## New renders
`reference_renders/sheet_national_pair.png`, `reference_renders/sheet_overhead.png`.
`sheet_national_dc.png` rebuilt, byte-for-byte unchanged.

## Verification
`sheet.py` proven a no-op on the default set: `sheet_national_dc.png` diffs to an
empty bounding box against the pre-change render (S-064 standard, STYLE_GUIDE 6.5).
Full `python3 build.py` clean; all four instances pass `check.py`.

## Corrected this session
Overhead-scales sensitivity was recorded as $77.91 in D-63, EN-17 and the
`sheet.py` panel caption. The build returns $77.8498 and always has. Verified by an
independent recomputation from `tobe2030.per100` and the FY2024 base reproducing all
three variants to four places, so the build is right and the record was wrong.
Corrected to $77.85, spread $0.57. Origin of $77.91 not reconstructible and not
guessed at. New standing note S-073 on hand-carried figures; the caption rule folds
into S-066.


## OmniGraffle export
`python3 graffle.py national_2030_mixed` -> `reference_renders/national_2030_mixed.graffle`.
333 objects: 100 rects, 84 beziers, 16 lines, 4 circles, 129 text. Element count
reconciles against the SVG exactly, no silent drops. SVG groups become OmniGraffle
layers `baseline` and `overlay-hr1`, so HR-1 can be switched off.

Export only. Nothing is ever read back from a .graffle into the ledger: a figure
that can be typed over in a drawing tool is not a sourced figure (S-073). Markup
comes back as instructions and lands in `sankey.py` or `instances.py`.

Verified by reading the plist back, reconstructing SVG from the stored bounds and
UnitPoints, and re-rendering: geometry matches the original. NOT verified inside
OmniGraffle itself, which is not available in this container. The specific
unverified item is whether OmniGraffle reads Bezier `UnitPoints` in the same
[start, c1, c2, end, ...] order this writes.


## Fan layout — no avoidable crossings (STYLE_GUIDE 2.9)
`outflows.fan_tiers` / `fan_rows` / `fan_crossings` added. `instances.hr1_term`
drops its hand-assigned row and is now `(terminal x, sub)`; terminal Y is solved
per render. `sankey._draw_hr1` calls the solver and ASSERTS zero crossings, so a
crossing fails the build. `build.py` now rebuilds every sheet in `sheet.SETS`,
which it had stopped doing when `all` became the default set.

Before: 8 crossing pairs among the five state-agency tributaries. After: 0, no
layout warnings. Detector self-tested against the old hand-assigned rows: it
reports the crossing they produced.

Change is confined to the FY2030 panel: sheet diff bounding box (318, 2393, 2273,
3015). FY2024 and DC panels bit-identical.


## Rule 2.9 extended to ALL outflows
The first pass applied it only to `_draw_hr1`. Ordinary outflows were on a separate
path with hardcoded terminals and never went through the solver.

- `outflows.resolve_bite_order` — Administration and Medicare premiums peel from
  the same trunk edge; whichever terminates higher now peels first. Fixes a
  crossing present on all three diagrams.
- `sankey` — each peel records its OWN origin. Medicare's origin was read off
  administration's step, which is what made the order un-swappable.
- `fan_rows` — pinned participants. Documented fraud enters the solve with a fixed
  terminal so tributaries can be capped ABOVE it, not just floored below it.
- Provider keep-out boxes narrowed from bar +/-70 to bar +/-8; the padding was
  pushing terminals down needlessly.

Verified with a geometric detector (`xdetect.py`, sampled bezier centrelines,
segment intersection). Before: ADMIN x MEDI on all three, plus FRAUD x 2 HR-1
ribbons on FY2030. After: zero on national_2024, all three FY2030 variants, and
dc_2024.

OPEN: the directed-payment-caps and documented-fraud LABEL blocks are now adjacent
and cramped, and the DPC terminal sits close under the Rx drugs bar. Uncrossed but
not yet comfortable. Not touched further without JW.


## Rule 2.9 scoped to the margin (2.9c)
`crossings.py` added: geometric gate over every render. Derives the main-flow body
envelope from the render's own lane colours and counts intersections only outside
it. Joins (ribbons handing off at a shared endpoint) are not crossings.

Reads 0 in the margin on national_2024, all three FY2030 variants, and dc_2024.
The dual-retain / MCO-care crossing is correct and retained under 2.9c.

DELETED: `reference_renders/national_2030_{combined.svg,combined.png,baseline.svg}`
— stale, from before the overhead variants; no builder produces them and
`crossings.py` was reporting against them.


## Tracker rebuilt as a ledger (STYLE_GUIDE 4, rewritten)
`tracker.py` NEW: lattice, slot assignment, invisible sub-columns, balance/bite
placement, row de-collision. `sankey.py` tracker block replaced. `instances.py`
gains `subs_spec` — the subtraction ledger (label, amount, class, charged column,
short name) — from which BOTH the tracker slots and the tributary terminals derive,
so they cannot disagree.

FY2024: 4 balances (205, 820, 1300, 1970), 3 bites (560, 1060, 1560).
FY2030: 7 balances, 6 bites, state agency subdivided.
Fraud recharged from CLAIMS to PROVIDERS — providers receive it. Its tracker
amount is now red, having been grey while red on the flow.

## Session close
Full `build.py` clean. `crossings.py` reads 0 in the margin on all five renders.
`check.py` passes on all instances.

OPEN, not fixed: on FY2030 the bite short names still overlap the phase names at
that density. FY2024 is clean. Agreed with JW to fix when FY2030 is taken up.


# Session 2026-09-04

## Opening gate: crossings.py read 1, and the render was not real
`python3 crossings.py` reported one margin crossing in `national_2030`. It was in
`reference_renders/national_2030_combined.svg`, a file no builder writes. The
previous manifest records that file as DELETED; it was still in the repo, because
a deletion noted in chat is not a deletion in the working tree.

Root cause, and it is not the stale file: `build.py` copied the mixed render's PNG
forward under the old name `national_2030_combined.png` and did NOT copy its SVG,
so a PNG and an SVG sharing a name came from different builds. `crossings.py` then
globbed the directory for `*_combined.svg`, answering "what files are here" when
the question is "what do we draw".

- `build.py` — both PNG aliases removed (`national_2030_combined.png`,
  `national_baseline.png`). One render, one name.
- `sheet.py` — the `national_2024` panel asks for `national_2024_combined.png`
  instead of the alias `national_baseline.png`.
- `crossings.py` — scan list derived from `sheet.py: PANELS`; a `*_combined.svg`
  no panel claims is an ORPHAN and fails the gate; a declared panel with no SVG
  reports MISSING rather than being silently skipped.
- STYLE_GUIDE **6.6** added. Standing note **S-079**.

DELETE FROM THE REPO (will not be removed by dragging in the zip):
    reference_renders/national_2030_combined.svg
    reference_renders/national_2030_combined.png
    reference_renders/national_2030_baseline.svg
    reference_renders/national_baseline.png
    reference_renders/national_baseline.svg

`crossings.py` now reads 0 on all five renders, orphan check clean.

## FY2030 tracker: bite short names
The defect was not an overprint. The three below-line rows are at different
heights, so nothing collided in pixels. "Eligibility Rules" spanned 634–832 around
its bite dot at 733, with balance dots at 647 and 820 either side: "Eligibility"
sat under one, "Rules" under the other, and the row read as annotation on
"Disbursed". Measured, not eyeballed.

Fix is geometric and keyed to DOTS, not to neighbouring label spans:

- `tracker.py` — `text_w`, `neighbour_room`, `wrap_short`, `short_lines`.
  A below-line label may not reach past the dot on either side of its own. A short
  name that does not fit WRAPS; it is never shrunk, because type size is frozen
  across panels the way scale is. A single word that still overruns raises and
  fails the build, since the fix is then the name in `subs_spec`, not the layout.
  `SHORT_LEAD = 26`.
- `sankey.py` — short names drawn as lines; canvas `H` 1240 → 1264 to carry the
  second line. `W` untouched: column register is frozen, panel height never was.
- STYLE_GUIDE **4.8** added. Standing note **S-078**.

Result: FY2030 wraps to "Eligibility" / "Rules", spans [669,797] and [704,762],
both inside the 647–820 gap. Every other short name in both years is unchanged and
already satisfied the rule. FY2024's below-line block is identical to last
session, same x, same y, same wording.

## Rebuilt
`build.py` (2024, 2030 mixed, DC) and `build.py sensitivity` (holds, scales,
mixed) — the sensitivities are rebuilt this once so no render is left at the old
1240 canvas. All viewBoxes 0 0 2200 1264. `check.py` passes on every instance.
`crossings.py` 0. Sheets regenerated: working, national_dc, overhead.

## Endnote audit (S-054, standard procedure — not requested)
Extracted every figure printed on the two national panels from the rendered SVGs
and checked each against `ENDNOTES.md`. 23 figures were on the artifacts with no
entry: the whole FY2024 measured spine, the three payer lanes, the six provider
nodes, and their FY2030 counterparts. EN-20 covered them by CLASS with vintages
but did not carry the figures, and 5.4 asks for the figures.

- **EN-37 AMENDED** — the rebuilt tracker prints $92.06, which the old entry ran
  through implicitly. No figure moved; a figure became visible.
- **EN-42** — FY2024 spine, lanes, nodes and beneficiary shares. MACStats Feb 2026
  Ex.16/17/21 on CMS-64 FY2024; federal share independently recomputed from the
  four FY2024 quarters in `fmap.py`. Ex.21 is FY2023 and the mixed vintage is
  restated on the figures rather than left at EN-20.
- **EN-44** — the FY2030 lanes, nodes and margin as drawn, all modelled outputs of
  the conserved ledger.

Coverage re-checked programmatically after writing: every `$NN.NN` on either panel
now resolves to an entry.

## EN-43 — NEW OPEN ITEM, and it blocks the freeze
Public-company earnings **$0.76** (FY2024) and **$0.69** (FY2030) are printed,
labelled, and drawn with the same weight as measured figures beside them. They are
an estimate with no primary source. `README.md` has carried "a subset of margin;
est." and a note that a 10-K segment carve is wanted; no endnote existed and the
artifact does not flag it.

The $5.61 payer total is sound — it is the measured margin. Only the split between
plan administration (sourced, EN-15) and earnings (not sourced) rests on the
estimate, and nothing downstream of the payer column moves if the carve changes.

Recommended: take the earnings label off for the freeze and draw the undivided
$5.61 margin with the split declared absent on the panel (S-071), then do the 10-K
carve afterwards. An absent split declared is honest at any vintage; the carve is
filings work that should not gate the presentation layer. **JW's call — asked in
chat, not actioned.**

## Directed payment caps: origination and termination not visible
JW's report. The lane was declared and drawn — the defect was terminal placement.
`_clear_obstacles` pushed the caps terminal below the provider bars; `_place` then
hit the PINNED fraud terminal 40 units under the last bar as a ceiling, found no
room, took its `y = max(top, ceiling)` escape hatch, and put the terminal back on
the Rx drugs bar with its label printed across the bar. The ribbon then ran the
whole way hidden under the fee-for-service band because both ended at the same
place. Neither gate saw it: `crossings.py` scans the margin, `fan_crossings`
compares tributaries to tributaries, and neither looks at furniture.

- `sankey.py` — fraud terminal drop 40 → 96, with the reasoning at the line. It is
  a ceiling for every tributary terminating in that column, not a local nudge.
- Standing note **S-080**.

Result: caps terminates in clear space below the Rx drugs bar with a visible
terminus, its own corridor out of the claims column, and its label no longer over
the bar. Both gates pass — `crossings.py` 0 on all five, `check.py` clean.

FY2024 changed too, as it must: same rule, same panels in register. `ImageChops`
bbox (1543, 897, 2078, 1142) — the fraud terminal and its label, nothing else.
Its label had been crowded under the Rx drugs bar there as well.

## Directed payment caps were leaving the wrong lane
JW, reading the corrected render: do these really subtract only from
fee-for-service? They do not. A state directed payment is defined at 42 CFR
438.6(c) as directing an MCO's, PIHP's or PAHP's expenditures — managed care by
construction, no fee-for-service counterpart. The bite was carved off the bottom of
the fee-for-service band, saying the opposite of what the instrument is.

- `sankey.py` — the claims-column HR-1 bite now leaves the top edge of the
  managed-care block. Not the bottom: that edge is measured at y=553.8 and the
  fee-for-service lane starts at exactly 553.8, so a bite there sits on a shared
  edge and reads as either lane.
- **EN-45** written. Standing note **S-081**.

No figure moved. $0.85 unchanged, claims subtraction unchanged, every tracker
balance unchanged, conservation unchanged. `crossings.py` 0 on all five,
`check.py` clean. FY2024 has no HR-1 bite and is untouched by this change.

Declared limitation in EN-45: SDPs apply across MCO and dual-MCO capitation and the
ledger does not decompose the $0.85 between them, so the ribbon leaves the combined
block at one edge rather than split in proportion. Not filled with a share (S-068).

## The number line rebuilt on four anchors (JW's sketch + rules)
- `outflows.py` — `DECREMENT_MEMBERS`, `decrement_span`, `decrement_x`,
  `TRACKER_ANCHORS`. Marker placement is derived from the outflow geometry
  already declared, so the line cannot drift out of register with the Sankey.
- `tracker.py` — `ledger`, `mark_tiers`, `shape_gap`, `collisions`, and the
  anchor/marker geometry. The running-ledger model above it is left in place but
  superseded.
- `sankey.py` — new drawing block: four Agilian-blue anchors, shaped markers,
  summing only at anchors. Canvas `H` 1264 → 1300 for the second tier.
- `_draw_hr1` — `STACKS` removed; every tributary placed individually.
- STYLE_GUIDE **4.9 / 4.10 / 4.11**, 4.7 superseded. Notes **S-082/083/084**.

Gates: `crossings.py` 0 on all five, `check.py` clean. Sensitivities rebuilt so
nothing is left at the old canvas.

**One printed figure changes and it is not a ledger change.** FY2030 Claims Paid
reads $78.77, not $77.93. The old line put "Claims paid" at the claims column's
RIGHT edge, after directed payment caps; the anchor sits at its LEFT edge, where
money enters. $78.77 is what arrives, $77.93 was what left. Same six decrements,
same amounts, same conservation, same $77.79 delivered. EN-37 needs amending and
`PAPER_PASSAGES.md` needs checking for $77.93.

**Open, reported by the build, for JW.** `State Admin` and `Eligibility Rules` sit
24 units apart: administration and all five eligibility tributaries terminate on
the state agency's right edge, so their midpoints nearly coincide. Labels are
tiered and legible, but the two shapes very nearly touch.

## Presentation tweaks (JW)
- **Column sub-labels** renamed to name the FUNCTION each column performs rather
  than how the drawing was assembled: federal appropriation / blended cost
  allocation / budgeted to Medicaid / payment mechanisms / MCO administration /
  claims paid to providers / sized by spend. Beneficiaries unchanged.
- **Footer** was a note to ourselves about register. Replaced with what the
  artifact is: two dollars at the same scale, FY2024 and FY2030 under P.L. 119-21,
  and what the line beneath each panel means.
- **HR-1 rule** no longer cuts through the Rx drugs fan. It is derived from the
  flow's own lowest point rather than the literal y=788 it had been sitting at, so
  it drops below everything the flow draws and cannot cross a ribbon again.
- **Documented fraud** redrawn as a ribbon in the same family as the lanes above
  it, not a stroke swooping across the canvas. It terminates at the RIGHT END OF
  THE PROVIDER BARS — providers are where fraud happens in this ledger — instead
  of on the providers/beneficiaries boundary, which read as though beneficiaries
  were party to it. It now stays ABOVE the HR-1 rule: fraud is not something HR-1
  takes out, and a line diving through that zone said it was. It is no longer a
  fan participant, only a keep-out box.
- **Label overlaps** (Provider tax limits over the state band, among others) clear
  as a consequence of the rule dropping.
- `FAN_FLOOR` 1024 → 1100, tracker `RULE_Y` 1030 → 1106, `BY` 1112 → 1188, canvas
  `H` 1300 → 1376. Moving the HR-1 zone down cost the fan 76 units of room and it
  overflowed; the tracker moves down with it rather than the fan being squeezed.

Cost, stated: FY2024 has no HR-1 tributaries, so the taller canvas leaves a band
of white below its flow. Register requires both panels share column and tracker
geometry (1.2), so that space is the price of comparability, not a defect.

Gates: `crossings.py` 0 on all five, `check.py` clean.

## PARKING LOT — tributaries terminating where they would have reached
JW: the reach sub-labels ("would have reached a paid claim", "would have reached
disbursements") suggest the tributaries should terminate THERE, showing where the
bite hurts. This is a direct conflict with **S-075**, which put terminals on the
tracker lattice and moved reach into the sub-label as text.

Worth noting before it is taken up: it would also move the Eligibility Rules
decrement marker. `decrement_span` takes the furthest forward termination, which
is currently the state agency's right edge (820) for all five. If they terminated
at their reach columns the furthest becomes the claims edge (1560) and the marker
moves from 742 to about 1112 — which would resolve the 24-unit collision with
State Admin the build is currently reporting. The −$8.17 total is unaffected
either way; it is a sum of the same five figures.

---

# SESSION 2026-09-11 — reach terminals, the beneficiary overlay, the fan fit

## Settled: the parking-lot item above
Tributaries now terminate at the reach they declare (S-085). The prediction in the
parking-lot note was half right. It did move the Eligibility Rules marker from 742
to 1112 and did dissolve the 24-unit collision — but 1112 sits DOWNSTREAM of
Funding Disbursed, the anchor that has already subtracted the $8.17, so the line
stopped adding up on its face. JW called it: the rule had been over-engineered.

The resolution is that the canvas and the line answer different questions and read
different keys (S-091). `_canvas_term_x` is the reach and sets the terminal and the
fan's peel order. `_terminus_x` is the charged column and sets the marker's span,
exactly as before S-085. **All six markers are back to their pre-session values:
238.0, 717.5, 742.0, 1180.0, 1431.0, 1533.0.** The 24-unit collision is back with
them and remains open.

## The tracker bug this exposed
`tracker.ledger` summed each anchor by comparing the anchor's x to the MARKER's x.
Correct only for as long as every marker's midpoint fell before its own anchor.
The first render after S-085 reported **Funding Disbursed $92.06, 7.94% lost** on a
panel whose trunk narrows to $83.89, with every gate passing. Anchors now sum by
each decrement's ORIGIN (S-086).

## Beneficiary overlay (EN-46)
Per provider class, dollars and cents, on any panel carrying decrements. LTC
−$2.78, hospitals −$1.95, physicians −$1.41, wrap around −$1.18, behavioural
−$0.84, Rx −$0.33; sum $8.49. One scale across all six, declared on the artifact
with a $1.00 reference bar, and NOT the flow's scale. `prior_node` comes by
reference from `AS_IS_2024.node`, never transcribed (S-073).

Per beneficiary class was rejected, not deferred: the FY2030 split is the FY2024
split times one multiplier, so all four classes fall by exactly 9.83%. Drawn, it
would have published an assumption as a finding (EN-47).

## Fan geometry
- Peel order left to right, fixed by JW: Other, Blocked senior enrollment, Work
  reporting, Six-month renewals, Blocked Medicaid enrollment rule. Declaration
  order is now the EXPLICIT tie-break where two tributaries reach the same column
  (S-090) — it had been falling out of a stable sort, and I reported that accident
  to JW as a geometric constraint.
- A tributary's amount rides its name or sits below its sub-label, SOLVED per
  tributary, deepest row first, spacing giving before legibility (S-089).
- One text metric, `outflows._text_w`, including the background box the renderer
  paints (S-088). The old estimate was narrower than the box drawn; correcting it
  cost 20 units of fan depth that were never really there.
- `FAN_LABEL_H_TIGHT` 30, `FAN_TIGHT_GAP` 40 → 8. Fan now fits the 1100 floor with
  no warnings.
- "Everything else" prints as **Other** via a declared `label`. The key stays
  distinct because "Other" is already the wrap-around-services provider key.
- `label_dy`: directed payment caps lifted 30 (was reading as a clause of the
  Blocked Medicaid enrollment rule); Blocked senior enrollment lifted 52 to sit
  above its terminal, crossing a ribbon, accepted by JW.

## Editorial
- `enrol`/`enrolment` → `enroll`/`enrollment` across nine files, three live on the
  artifact. Every rendered string checked; nothing else misspelled.
- Footer re-based: "Two $100.00 of Medicaid spending at the same scale…". The
  "dollar" framing had crept back into the last line a reader reads. "The line
  beneath each panel is what reaches care" deleted.
- "Other" sub-label: "mixed phases — UNRESOLVED" → "e.g. home equity, cost
  sharing". EN-31 updated; it is now the only place the basket's contents are
  described.
- NOT SHOWN block added, then removed by JW. EN-47 and EN-31 carry both gaps.
- The beneficiary key moved below the pies and, like the declarations, draws LAST
  (S-087): the fan composites over the base and was printing through it.

## Deleted — these need removing by hand, a zip will not do it
`build_pair.py`, `COMMIT_INSTRUCTIONS.md`,
`reference_renders/national_2030_{baseline,combined,overlay}.svg`,
`reference_renders/national_2030_combined.png`,
`reference_renders/national_baseline.{svg,png}`.
The `national_2030_*` set was the ORPHAN the crossing gate reported at session
open, and it still carried the pre-fix `enrol` spelling.

## Gates at close
`crossings.py` 0 on all five panels. `check.py` clean. `build.py` reports one NOTE,
the 24-unit marker collision. FY2024 panel pixel-identical to session open.

## Open, carried forward
- State Admin / Eligibility Rules 24 units apart. Unchanged by this session.
- **STYLE_GUIDE 4.8 has no gate on the four-anchor line.** `neighbour_room` is
  only reachable from `short_lines`, the superseded running-ledger path, so the
  rule has been binding and untested since S-082. Measured: both State Admin and
  Eligibility Rules currently violate it. JW's to schedule.
- Endnote keys vs artifact labels now diverge in one place ("Everything else" /
  "Other"). Fine while it is one, worth a convention if it becomes two.

## QUEUED FOR THE COMMENT PASS — do not apply before JW's notes arrive
JW, 2026-09-11. Held deliberately so the whole set of edits lands in one rebuild.

- **Q-01 · Gloss the bill number at first use, twice.** The law is cited throughout as
  P.L. 119-21. Medicaid practitioners say "H.R. 1". Bind the two once on the cover and
  once at first use in Section I, then let the public law number carry the rest of the
  paper alone. Same treatment the house rules already give capitation and the medical
  loss ratio: the term stays and gets one clean gloss.
  Reason for the formal citation: H.R. 1 is the majority's first bill of every Congress
  and will name something else in 2027; every statutory section cited in Section IV
  (§71101 through §71119) is a section of the enacted law, not of the bill.
  Files: `paper_national.html`, cover block and the Section I opening.

---

# SESSION 2026-09-14 — the national manuscript, the charter, and two gates

## What shipped
**`Medicaid_Dollars_National_DRAFT_v4.pdf`** is the live draft. Eighteen pages, landscape
letter, two columns, Jost and Nunito embedded. Twelve figures, every one a crop of the two
master panels at native resolution, cut by `make_figs.py` and never redrawn. Body prose is
about 4,700 words against 11,400 at first draft, which is 41% and inside the charter band.

Source is `paper_national_v4.html`, rendered by `render_v4.py`. `paper_national_v3.html`
and its PDF are kept for one cycle as the comparison; text is identical between them.

## The editorial charter (new, authoritative)
`EDITORIAL_CHARTER.md` sits **above** `EDITORIAL_STANDING_NOTES.md`. Where a standing note
conflicts, the charter wins and the note is marked superseded in place. C-00 through C-11
plus C-09A and C-10A. Origin: JW's reader-first instruction, two redlines totalling 103
comments, and seven techniques from the firm's editorial expert.

Superseded in place: S-071 as applied to prose (limits now live in footnotes, the artifact
rule is unchanged), S-002 in part (the firm still takes a position, it no longer announces
that it is taking one), S-033 in part. D-33 withdrawn: the state, plan and provider
checklists are cut from every edition.

## Two gates, both wired into `render_v4.py`
**`whitespace.py`** rasterises each page and reports dead space per column in text lines.
Cover pages, plates, section-final pages and the last page are exempt by design. It also
measures horizontal slack beside a page-spanning figure.

**`figurefit.py`** reads label coordinates out of the panel SVGs, the crop box each figure
cuts from `paper_figs/crops.json`, and the captions opening on each page, then reports any
subject the page treats as its own whose label sits outside every crop on that page.

*Four detector bugs found and fixed this session, all the same class: a gate pointed at the
wrong input agrees with itself.* Whitespace first scanned PDF objects and counted the
renderer's full-page white rectangle as content, reporting zero on every page. The
horizontal check first measured the image rather than the frame, so a portrait crop centred
in a full-width band read as a column figure. The section-end test keyed on the literal
string "SECTION" and went blind the moment the Roman numerals were removed. And figurefit
counted "Detail from Figure 5" as the whole panel being present, which contains everything,
so every check passed. Recorded at C-10A.0.

## Renderer
Ported the manuscript to Typst (`html2typst.py`, `paper_national.typ`, `render_typst.py`)
to get real float placement: 15 pages against 19 and one whitespace failure against four,
with the same content. **JW rejected it on appearance and the port is parked, not deleted.**
Both gates run against either PDF, so the comparison stays cheap. The four-page saving is
what proper float placement buys, and the stranded columns that remain in the HTML build
are that limitation.

## Endnote maintenance
EN-46's three statute-specific rates were paired with the wrong services; corrected in
place with the amendment noted. The ordering was right in `PAPER_PASSAGES.md` and wrong in
the endnote, which is S-073 in its purest form: the figures were correct and the mapping
was carried by hand.

## Open, for JW
1. **The repo is public and the draft is now substantially complete.** Per the standing
   instruction this is the flag.
2. **S-092 is live.** At the start of the next chat following this commit, ask whether
   the co-author has seen the disclosure wording on the author page.
3. **EN-43 re-scope, not yet ruled on.** 10-K segment disclosures cannot produce a measured
   Medicaid earnings figure; they give revenue, not line-of-business profit, so the carve
   stays an allocation however much work is done. NAIC statutory filings do break out a
   Medicaid line with underwriting gain. JW's proposed structure is to take the total from
   NAIC and carve the public-company share from SEC ownership mapping. That moves nonprofit
   retention out of the $4.85 administration band and changes both panels, so it is a
   rebuild rather than a wording fix.
4. **Four whitespace strandings remain**, pages 6, 9, 10 and 15 of v4. Three are a figure
   that cannot fit its column and jumps. Not fixable in this renderer.
5. **The pie cell percentages are still fit from an unsourced seed** at `sankey.py:505`.
   Ruled "deal with it when we get to that part of the document" and still open.

---

# SESSION 2026-09-15 — v4.1, the dark gate, and a scale error

## What shipped
**`Medicaid_Dollars_National_DRAFT_v4.1.pdf`** is the live draft. Eighteen pages, same
figures, same panels. Source is `paper_national_v4_1.html`, rendered by `render_v4_1.py`.
`paper_national_v4.html` and its PDF are kept for one cycle as the comparison. v3 goes on
the delete list.

## The figurefit gate was never running
`render_v4.py` line 20 read `exit(call(whitespace) or call(figurefit))`. Whitespace exits 1
on the four accepted strandings, so the `or` short-circuited and figurefit never executed.
It had been dark since the day it was wired in, and would have stayed dark for as long as
the strandings are the accepted state. Split into two captured return codes; both gates now
run and the render still fails if either fails. Applied to `render_v4.py` and `render_v4_1.py`.

Same class as the four recorded at C-10A.0, with a new variant: a gate pointed at the wrong
input agrees with itself, and a gate that never fires agrees with nothing. **Verify gate
execution, not just the exit code.**

## A scale error behind a style violation
C-07.2's live instance read "Forty-one cents of every Medicaid dollar still moves this way."
The banned phrase was the visible defect. The arithmetic underneath it was the real one: the
fee-for-service lane is $41.08 of $100, so on the base the paper actually uses this is
forty-one dollars per hundred, not forty-one cents per dollar. The ratio is the same; the
base is not, and the page it sits on shows a hundred-dollar diagram. The redline's proposed
fix, "forty-one cents of every $100," was wrong in the other direction by two orders of
magnitude. Written as **"Forty-one dollars of every hundred still moves this way."**

Standing note candidate: a quantity restated on a base other than $100 is a defect even when
the ratio is right, because every figure in the paper is read against the hundred.

C-07.2 scan: 29 instances across 17 files at session start, up from 24 across 15. The growth
is the charter, `ENDNOTES.md` and `PAPER_PASSAGES.md` quoting the phrase in order to ban it.
Zero remain in the live manuscript; 28 remain in code and retired documents.

## Twelve edits applied from JW's redline
Nine prose corrections, the bio rewrite, the arithmetic fix and the draft date. Applied and
verified one at a time with a per-edit result printed, then verified again independently by
searching for both the superseded and the replacement text. Twelve of twelve landed.

Two calls made and flagged rather than assumed: the cover stamp is dated for v4.1 rather than
carrying 11 September, and "Everything else" stayed lowercase against the redline, because
capitalizing it in one sentence would have left it inconsistent with the provision table, the
heading above it and the endnote register.

## Author page
JW's biography generalized for a national readership. Ward Four, the residency claim, the CBE
designation and the Williams Administration reference are out. The District of Columbia
survives as the place the work happened, because it carries the credential.

**S-092 remains open.** The draft has been shared with the co-author. Sharing is not review, and the
note asks specifically whether she has seen the disclosure wording on the author page.

## Open, for JW
1. **The repo is public and a link is now outside the firm.** Both trigger conditions for the
   standing privacy reminder have fired.
2. **DC is next.** JW has turned to the DC model, data and whitepaper. `STATE_PLAYBOOK.md` and
   `build_sankey_dc.py` are the starting points. Scope not yet set.
3. Carried forward unresolved: EN-43 re-scope, the pie cell seed at `sankey.py:505`, the
   renderer choice, and the four whitespace strandings.

---

# SESSION 2026-09-15b — the seam, cut and proved

## What shipped
The Ledger / View / Layout seam from `ARCHITECTURE.md`, with the national as-is
and DC as-is rendering through it byte-identically. No artifact changed. The
national presentation layer was not touched.

New: `ledger.py`, `view.py`, `compose.py`, `views.py`, `coverage.py`,
`ledger_national_2024.py`, `ledger_dc_2024.py`, `ACQUISITION.md`,
`NAIC_ROUTE.md`, `prove.py`, `byteproof.py`, `synth.py`.
Changed: `build.py` (gate wiring), `sankey.py` (absent-lane collapse),
`instances.py` (`Instance.collapsed`).

## Phase 0, against JW's four items
1. **`Fig` with provenance — done.** Value, source, vintage, basis, status,
   note, and a signature. Endnotes generate from the ledger. A figure without
   provenance fails the build.
2. **`check(ledger)` as a real gate — done and wired.** `build.py` runs it
   before emitting. Verified it refuses, not merely that it exists.
3. **Absent-lane collapse — done.** A collapsed lane disappears with its label,
   its bar, its peels and its tracker row. Proved on a synthetic
   fee-for-service-only jurisdiction.
4. **The expand flag — done.** `View(expand=["mco","dual"])` opens DC into six
   named payers off the same ledger. Not a second graph.

**Remaining before Phase 0 closes: the FY2030 to-be through the new path.**

## Byte identity
```
national_2024      IDENTICAL   40,406 bytes
dc_2024 (legacy)   IDENTICAL   24,341 bytes
```
DC is proved on `build(legacy_mix=True)`, which reproduces exactly what
`ledger_dc.py` carried. `build.py` calls it with that flag, so the flag is the
visible record that DC still carries the national service mix. The correction
is then a diff against a baseline known clean rather than a change hidden
inside a rewrite (S-064).

## Two defects the byte proof caught
**Published totals are not the sum of their parts.** Provider node totals were
being derived by summing components. The components are rounded to the cent and
the totals are published, so long-term care is 28.53 where its parts add to
28.54. The conservation tolerance absorbs a hundredth; the renderer does not,
and it moved a band by a tenth of a unit. Node totals are now carried as
measured figures in their own right. **Standing note candidate: a published
figure is measured, and recomputing it from its parts substitutes our
arithmetic for the source's.**

**A gate matching on prose goes blind when the prose is reworded.** The
declaration check was grepping `declarations` for a substring. Declarations are
now two fields: `declarations` is prose for the artifact, `declared` is keys the
gate matches. The break-test failed to fail until it was pointed at the right
field.

## coverage.py — the acquisition instrument
`check` asks whether the numbers are consistent. It cannot ask whether they
exist, because **absence conserves**: nothing plus nothing balances. DC passes
`check` cleanly and is 26 figures short.

`coverage.py <territory>` walks a ledger left to right and reports every figure
the baseline needs as verified, modelled, unverified, lapsed or missing, with
its source named. Exits non-zero while anything is open. Process written up in
`ACQUISITION.md`.

## Verification, strict (JW ruling, 2026-09-15)
`verified` means a person opened the source and agreed with the number. A
redline does not earn it; shipping does not earn it.

It attaches to a **vintage** and to a **value**, not to the calendar. A figure
signed against FY2024 stays signed until the ledger is re-anchored. Three things
end it, each detected rather than remembered: a new vintage (reports STALE), an
edit after signing (reports LAPSED and **fails the build**), and a corrected
source (cleared by hand). Run `coverage` every build and expect the answer not
to change; when it changes, something happened that should have.

**JW signed the national baseline, 2026-09-15**, on the strength of the endnote
register, two redlines and a shipped draft.

```
national FY2024:  22 verified   2 modelled   2 unverified   3 missing   of 29
DC FY2024:         0 verified   0 modelled  15 unverified  26 missing   of 41
```

**One exclusion from the signature, taken deliberately and flagged.** The
public-company earnings carve is left unsigned on both capitated lanes. EN-43 is
OPEN and states in terms that $0.76 has no primary source. Signing it would
assert that someone opened a source the register says does not exist.

Also open on national: the beneficiary matrix interior, and plan-level detail
under both capitated lanes.

## NAIC — route established, not executed
`NAIC_ROUTE.md`. Health annual statement blank, **Page 7, Analysis of Operations
by Lines of Business**, Title XIX Medicaid column: premium, incurred claims,
administrative expense, net underwriting gain, per licensed entity, filed 1
March for the prior calendar year.

Access: InsData sells Annual Key Statement Pages at **$13.00 per
company-statement**, no refunds. **DISB publishes DC-domiciled health entity
statements free**, so the DC half costs nothing.

**The finding that changes the shape of the job.** Schedule Y Part 1, the
organizational chart, and Schedule T, premiums by state, are both inside the
same $13 Key package as Page 7. The brief scoped the NAIC pull and the SEC
ownership mapping as separate work. They are not — the parent-to-entity chart
ships with the Medicaid column it has to be applied to. SEC filings become the
check on the mapping, not its source.

Expected to bite, reported not worked around: the Title XIX column may carry
state-only programs (DC has exactly this with Alliance and ICP), and statutory
filings are calendar-year incurred against a federal-fiscal-year total
computable spine, which needs a stated bridge.

Sora Shin has been asked to pull the four DC statements from DISB by hand; the
site refuses automated requests. Purchasing and account creation are JW's.

## Naming rule (JW, 2026-09-15)
A plan carries its **present-day name with the former name in parentheses** —
"Wellpoint DC (formerly Amerigroup)" — so a reader recognises it whatever year
the ledger is anchored to. The licensed entity name is unchanged and is what
NAIC and SEC filings are found under. Applied to the DC ledger. Belongs in
`STYLE_GUIDE.md`.

## DC facts established
FY2024 comprehensive plans: AmeriHealth Caritas DC, MedStar Family Choice DC,
Amerigroup DC. Amerigroup became Wellpoint DC on 1 July 2025. HSCSN is the
separately contracted CASSIP plan. DHCF selected UnitedHealthcare for District
Dual Choice from 1 February 2022.

**Unconfirmed and material:** DHCF's current managed care page lists two
comprehensive plans, and a transition transmittal moves enrollees off Wellpoint
with prescriptions honoured through 31 October 2026. If that holds, a DC edition
on FY2024 draws four plans, one of which is leaving while the reader reads it.
Not verified.

## Flagged, not fixed, per instruction
1. **The tracker's State Admin marker holds two different events.** On the
   national panel `−$7.97 State Admin` is $5.07 of administration plus $2.90 of
   Medicare premiums returning to the federal government. Different
   destinations, one label. JW found this on the synthetic panel. National
   tracker is frozen.
2. **Column headings do not come from the View.** The PAYER heading is
   hardcoded "MCO administration" and is false on a jurisdiction with no
   managed care.
3. **Tiny-payer label collision.** At $1.00 lane width the MCO capitation label
   sits behind the dual label (S-089).
4. **Two undeclared allocations removed from the DC ledger**, both recorded as
   absences rather than deleted: the national managed-care service mix, and an
   uncited 75/25 split of the dual and PACE capitation into long-term care and
   wrap-around, which was not on the declared-absent list.

## Carried forward, unresolved
- **S-092 remains open.** Asked at session open; not answered.
- EN-43, the pie cell seed at `sankey.py:505`, the four whitespace strandings.
- Repo privacy: both triggers fired, still unruled. Not raised again per
  instruction.

# SESSION 2026-09-16 — Phase 0 closed, and the instrument audited

## Phase 0, closed
FY2030 to-be moved onto Ledger + View + compose, byte-identical on all three
overhead variants. Proved all three rather than only the one that ships: they
exercise different arithmetic and differ from each other, so the proof is not
passing trivially. HR-1 split three ways — amount and reach to the Ledger,
terminal sub-label and declaration order to the View, `src_x` left in
`outflows.py`. `fed_bite`, `sa_hr1` and `claims_hr1` were three hand-kept totals
on the instance; they now sum from the peels. S-096, S-097 recorded.

## What the audit found
JW asked whether the national figures were sourced or merely typed into an early
script. Both, as it turned out. Tested against MACStats February 2026:

- Medicare premiums $2.90 — exact against Exhibit 17.
- Federal share $64.70 — sound, and better documented than expected: recomputed
  from the four FY2024 CMS-64 quarters in `fmap.py` as 0.6472.
- Administration $5.07 — right arithmetic, wrong name. It is total Medicaid less
  total benefits, so administration $4.32 *plus* Vaccines for Children $0.76.
  S-099. **Not yet relabelled on the artifact.**
- Payer lanes — right, and net of $15.2B of collections spread pro rata.
  Undeclared. S-100. **Not yet declared on the artifact.**
- Provider nodes — cited Exhibit 17, which cannot produce them. Method found in
  `build_xlsx.py`: CMS-64 FFS mix plus an HMA T-MSIS key at CY2021 plus a
  five-number behavioral health carve with no source at all.
- The ledger summed to exactly 100.00 throughout. S-098.

## Corrections made
`provider_mix.py` computes the provider phase from three declared inputs.
MACPAC March 2026 ch.2 adopted for the behavioral health carve (JW, 16 Sep).
Wrap-around $13.33 → $15.33, physicians and clinics $12.63 → $10.79, long-term
care $28.53 → $28.91, hospitals $18.66 → $17.77, Rx $3.76 → $4.11. The
underlying categories did not move; the old carve had compressed two of them to
near-parity. EN-48 written.

## Instrument repairs
- Derived figures inherit verification and must name parents that resolve. 38
  dangling parent references found and fixed. S-095.
- `signatures.py`: signing is a lookup against a written register. The previous
  stamp could not detect a figure changing between sessions and had carried JW's
  15 September signature onto four node totals he had never seen. S-094.
- `agreement()` gates the duplicate `reach` declaration.
- Break tests now nine, all caught.

## Signed
`REVIEW = "2026-09-16 JW"`, 33 figures, on the stacked FY2024 and FY2030
comparison sheets. EN-43 earnings margins still deliberately unsigned.
S-093 established: no signature without a picture.

## DC
Phase 1 opened. Cost allocation re-acquired from Exhibit 16 FY2024 — federal
73.17 / non-federal 26.83, scale $43.72M, administration $5.35 — all reconciling
exactly with what the panel already carried, now with the exhibit named and the
Exhibit 16 dollars lifted into ledger anchors. DC figures remain unsigned.

NAIC: three of four entities in hand, HSCSN absent (a CASSIP contractor
predating MCO regulation; it files no health blank — JW). MedStar Family Choice
Inc is Maryland-domiciled and its Page 7 Title XIX column is Maryland and DC
combined, so DC premium is recoverable from Schedule T and DC claims, admin and
gain are not. Amerigroup's CY2023 filing booked Alliance and ICP inside Title XIX
until DISB made them refile; the amendment is the page to use. Plan-level
underwriting gain dropped from scope (JW). Administrative expense acquired for
AmeriHealth Caritas DC and Wellpoint DC, both years.

## Open, not acted on
- Administration relabel and the collections declaration.
- DC ledger's plan revenues ($425.3M Wellpoint, $411.2M MedStar) trace to an
  uncited constant in `build_sankey_dc.py`. Possible swap, possible older
  vintage; the DHCF report settles it and nobody has opened it.
- `scale` means two things across ledgers; `coverage.py` prints STALE for two
  conditions; the EN-43 cascade is live in the ledger but invisible in coverage.
- New FY2030 label collision: wrap-around pie reaches y=674, two units past the
  behavioral health label. Consequence of the node resize. Presentation, frozen.
- S-092: the co-author has not yet seen the author-page disclosure wording.

## Session handoff streamlined (2026-09-16, JW)
`SESSION_START.md` holds everything stable between sessions; the per-session
brief carries only what changed. `gates.py` replaces seven commands and a table
of expected numbers written in prose — the expectations live next to the gates
and a gate that prints nothing now fails. `standing_index.py` generates
`STANDING_INDEX.md`, one line per standing note, so a session reads a page
instead of 1,292 lines and opens the full note only where it bears. The notes
file stays append-only. `NEXT_SESSION_PROMPT_3.md` retired; prompt 5 supersedes
the unused prompt 4. Read cost at session start falls from about 4,550 lines to
about 800.

---

# Session, 18 September 2026

Closed with all seven gates as expected. The national baseline was re-defined,
rebuilt and re-signed; the manuscript was not touched.

## Gate EXPECT changes, and why

- **`build.py`** — a third frozen advisory. Vaccines for Children and the
  provider tax limits leave the flow within eight units of each other, so their
  markers land four apart on the FY2030 line. Geometry telling the truth, not a
  placement fault; the two are stacked rather than moved. The regex count went
  from 2 to 3.
- **`coverage.py national`** — 21/2/3/3 became 24/2/2/3. Better attested than
  before D-70, not worse: `scale` was signable for the first time.
- **`byteproof.py` RETIRED, `renderproof.py` added.** Byteproof proved the
  Ledger path rendered identically to the old `instances.py` path — migration
  scaffolding, and its premise expired the moment D-70 moved the baseline.
  Keeping it would have meant hand-editing a second copy of every constant so
  it could agree with the first. Replaced by a golden-render register over every
  panel the build emits. S-104.

## Gate defects found and fixed

- `prove.py` addressed peels by list index. When Vaccines for Children became
  `peels[0]`, two of the ten deliberate breaks silently began breaking a
  different peel than the one they named, while still reporting CAUGHT. Now
  addressed by key.
- `prove.py` sections 3 and 4 read the live signature register, so they stopped
  working the moment D-70 legitimately emptied it. Both now plant their own
  fixtures and remove them.
- `prove.py` section 4 expected `scale` to be unverifiable. That was a defect
  encoded as an expectation: `scale` was carried as DERIVED with no parents, so
  it reported "derived from nothing named" and could never be signed. It is
  MEASURED from Exhibit 16 and is now signed.
- The oversight peel stepped the trunk and drew no exit — ten cents left the
  diagram with nothing on the page to say where it went. Caught by eye, not by
  a gate.
- The oversight exit then crossed the administration arrow, caught by
  `crossings.py`. Cause: `resolve_bite_order` deals x slots in terminal-height
  order from `OUTFLOWS`, and the peel had been added to the view without an
  outflow declaration, so it had no terminal to sort on. Fixed by declaring it.
- `build.py` does not rebuild the FY2030 `holds` and `scales` variants in a
  working session, so three panels sat in `reference_renders` on the pre-D-70
  baseline and were blessed into the register as if live. Rebuilt with
  `build.py sensitivity`. The hole in the build is not fixed.

## Own errors, recorded because the pattern matters

Three times in one session a string operation keyed on `SIGNED` also matched
inside `UNSIGNED`, destroying `signatures.py` and requiring a restore from the
tarball. Once with `str.split`, once with `re.sub`. The register is now edited
by locating blocks at line starts. Also invented five decision numbers (D-68 to
D-72) before checking the register, which stood at D-67.

## Not done

The manuscript. It is two rounds behind — the 16 September carve was never
applied to it — and the change map is `CHANGE_MAP_2026-09-18.md`.

# Session manifest — 2026-09-19

## What this session was for

The manuscript. It was two rounds behind and is now current, and ships as
v5.0 (JW, 19 September: whole number, because it goes to early readers).

## Found before anything was changed

**`paper_figs/crops.json` was never committed.** `figurefit` crashes on a clean
pull and `render_v4_1.py` fails. Regenerating with `make_figs.py` returned all
eighteen PNGs byte-identical, so only the crops index was missing. It is in this
commit.

**The FY2030 sources were the FY2024 sources.** `source.federal` was
`FED_M / (HUNDRED_M/100)`, which is sized to the FY2024 vaccine peel of
$0.7619. The FY2030 peel is $0.7557, so $100.0061 arrived at the state agency
instead of $100.00, against D-70. The cent rode the whole tracker: Budgeted
$98.76, Claims Paid $79.38, Delivered $78.39, 21.61 percent. `check` does not
catch it — TOL is $0.02 and the gap is $0.006. **D-76, JW 19 September:
correct the sources.** `source.federal` is now the state residual plus the
FY2030 vaccine peel. The hundred is struck exactly. The line reads $98.75,
$79.37, $78.38 and 21.62 percent. `FED_M` is now imported and unused at line 39
of `ledger_national_2030.py`.

**Six errors in `CHANGE_MAP_2026-09-18.md`, and one omission.** The map rescaled
old rounded values by 0.76 percent instead of re-reading the ledger, which
agrees wherever rounding falls the same way and invents a cent where it does
not. Directed payment caps stay $0.85, not $0.86. Six-month renewals stay $0.75,
not $0.76. Fee-for-service fall is $3.66, not $3.67. FY2030 plan administration
is $4.45, not $4.46. FY2030 claims paid is $79.37. FY2030 public-company
earnings, $0.69 to $0.70, was absent from the map entirely. Proof independent of
the ledger: with the map's $0.86 and $0.76 the seven provision rows sum to
$10.36 against the $10.34 the map itself specifies two rows later.

**The behavioral health / prescription drugs fall rates are an allocation
artifact.** 8.95 and 8.63 percent against the undifferentiated 8.85. Each node's
claims cells miss its column margin by a hundredth in opposite directions,
inside TOL. Not fixed. Declared in note 8.

**DC has no Vaccines for Children peel and no federal oversight peel, and
neither absence is declared.** DC declares nine absences; these are not among
them, and `coverage.py dc` does not list either as a figure the DC baseline
needs, because that list predates D-70/D-71/D-72. The two as-is panels are built
to two different definitions of a complete baseline. Not fixed. DC Phase 1,
scale-and-peels step. DC does pay Medicare premiums, $1.97 measured; it is
invisible only because the State Admin marker still holds two flows.

## Done

- **D-76.** FY2030 sources rebased. Above.
- **D-77, JW 19 September.** Tracker anchor subtitles read "x.xx% less", not
  "% lost". One point in `sankey.py`; every panel goes through it. Zero "% lost"
  and forty-nine "% less" across the thirty SVGs the build emits. Decimals
  unchanged. EN-41 revised.
- **The manuscript, v4.1 to v5.0.** 129 numeric replacements applied by line
  with a printed result per edit, zero missed, seven colliding tokens handled
  positionally. Six prose items written: the vaccine peel and the federal
  oversight peel introduced in section 2, "two things come off the top" now
  three, the lede no longer says the money is followed from the appropriation,
  four captions claiming four anchors say five, Figure 8's caption corrected and
  a paragraph added making the point that the provider tax limit is the only
  provision that takes money before the state has it, and note 2a saying that
  22.21 percent became 21.62 because the definition changed and not the law.
- **Note 8 rewritten** for the three no-longer-identical fall rates and for both
  penny discrepancies.
- **Every figure in the paper is now the figure printed on the diagram.** This
  is a choice: the services table reads $87.07 against its own rows summing to
  $87.08 and its shares to 100.1 percent. One headline was preferred to one
  column adding up. Both cents are in note 8. **Reversible — JW has not ruled.**
- **Page 6's 22-line stranding closed** when the new prose filled it. `EXPECT`
  in `gates.py` updated with the reason. Four strandings remain: 9, 10, 15, 16.
- **Wrap around services paragraph rewritten** (JW, 19 September): heading is
  now "Wrap around services is a catch all category", the comparison with
  physicians and clinics is dropped, and the contents are listed largest first
  with the full composition in new note 5a. The $55.1B / $6.2B split that
  carries the ordering lives in `build_xlsx.py`, not the ledger. It reconciles
  exactly to the ledger's $61,284M, but it is a hand-carried figure and the
  ordering claim rests on it. **S-073 exposure, open.**
- **`DELETE_CANDIDATES_2026-09-19.md`.** Reachability walked from the seven
  gates, not eyeballed. Nine recommended, ten held. **JW, 19 September: every
  whole-number release of the manuscript is kept. Point releases may go.**
  `build_sankey_dc.py` is imported by both DC ledgers and cannot go: the live DC
  panel still reads its constants, including the uncited plan revenues.
- **15 panels re-blessed** with a reason. `build.py sensitivity` was run first so
  the `holds` and `scales` variants were live and not blessed stale.

## Added after the first package

**S-105, JW 19 September: derive in code, never type an output.** Raised against
the FY2030 sources basis line, which quoted "$100.0061" as a literal — the
number whose absence the correction was about.

- `ledger_national_2030.py`. The federal source is now built from four named
  intermediates — `_state_share`, `_fed_share`, `_fed_enters`, and `_superseded`
  carrying the pre-D-76 derivation — and the basis line is an f-string over
  them. Every figure it quotes is recomputed each build, including the
  superseded one. Value bit-identical.
- `ledger_dc_2024.py`. `SCALE = 43.72` was the DC total over a hundred, typed.
  It is now `DC_TOTAL_M / 100.0`. Bit-identical, and `renderproof` confirms it:
  no panel moved. A revised Exhibit 16 would previously have moved every dollar
  on the DC panel and left the scale behind.
- `sankey.py`. The tracker comment quoted 98.75 and 1.25 percent, which the
  source correction had already invalidated once. Reworded to say what the
  anchor means rather than what it currently reads.
- **`typedfigures.py`**, new. Reports every number inside a string or comment in
  the Python sources that equals a figure a ledger derives. Deliberately not a
  gate — a match is not a fault, and SVG opacities are filtered out — but it is
  the instrument for the convention. It reports thirty remaining. The ones worth
  reading are the DC derivation comments at `ledger_dc_2024.py:36-56`, which
  show worked arithmetic in a comment that nothing recomputes.

## Not done, and deliberately

The DHCF report is unopened and the $425.3M / $411.2M question is untouched. DC
Phase 2 signing. DC Phase 1. The collections netting. `legacy_mix=True`. The
author page.

**S-092 is closed.** JW, 19 September: the co-author saw the author-page disclosure
wording and it has been deleted for now. It does not come back as an open item.
The plain-language sentence about plan administration that came out of it is
still unhomed, and still matters once the DC payer lane names actual plans.

**Renamed for the early readers.** `paper_national_v4_1.html` ->
`paper_national_v5_0.html`, `render_v4_1.py` -> `render_v5_0.py`, output
`Medicaid_Dollars_National_DRAFT_v5.0.pdf`. `gates.py` follows. The v4.1 PDF is
untouched and stays; under the 19 September rule the whole-number releases are
the ones kept.

---

# Session — 2026-09-21 · DC sources and the plan question

The DHCF question was answered, and the answer invalidated more than the one
figure it was about. Nothing was drawn. The DC render is byte-identical to the
one this session opened with: `ImageChops.difference` returns an empty bbox and
all seven gates pass.

## The plan figures

**D-78. The $425.3M "Wellpoint DC" lane is a two-plan composite.** Not a swap
and not CY2022. Three of the four constants in `build_sankey_dc.py:21-22` are
exact DHCF CY2023 figures. The fourth is Amerigroup ($317.9M / $260.8M, nine
months) plus her employer ($107.4M / $87.7M, three months) summed and given the
successor plan's name. her employer's administration is a full year of wind-down
against one quarter of revenue, so the lane's retention — $76.8M on $425.3M —
belongs to neither plan. The claims ratio survived the merge almost untouched
(81.9% composite against Amerigroup's 82.0%), which is why no ratio check
caught it.

**D-79. The named-plan block rebases on DHCF CY2024, agreed, not executed.**
DHCF published CY2024 in June 2026, after the last session. Four clean
full-year lines, no composite: Wellpoint $385.8M / $303.9M / $22.2M admin,
AmeriHealth $786.2M / $720.9M / $44.2M, MedStar $403.7M / $374.4M / $24.6M,
HSCSN $180.4M / $180.4M / $20.7M. MedStar's line is District-only, which
retires the Schedule T workaround. **The ledger still carries the CY2023
composite.**

**HSCSN runs a 100% MLR in CY2024.** Claims equal revenue exactly; $20.7M of
administration is funded from reserves. JW: plans take risk with their
capitation revenue, and 2024 was a weird year. It is drawn as measured — no
retention peel, care equal to capitation — and the reserve draw is declared.
`care + adm = cap` does not hold for HSCSN and must not be smoothed.

## Non-Medicaid money inside the plan figures

**D-80. DHCF plan revenue is not Medicaid.** It covers the DCHFP and the
Non-Medicaid MCPs together, and excludes premium tax and risk-share amounts.
Alliance and ICP are locally funded, no federal match, and their money sits
inside every plan figure. FY2024 actual, from the DHCF budget chapter:
Alliance $147.4M, Immigrant Children $19.1M — $166.6M, or $3.81 per $100.

A PMPM-times-enrollment derivation of the same thing gave $121.7M to $143.6M,
16% to 27% low. Discarded. The budget carries both as line items; do not derive
what is appropriated.

**The lane migration is in the chart of accounts.** Both MCO lines go to zero
in FY2026 and an Indigent Care line appears at $121.4M, described as
fee-for-service serving Alliance beneficiaries, falling to $91.9M in FY2027.
Same funder, different lane.

**FY2030 for these programs.** FY2027 enacted restores the Alliance: $38.3M to
remove the age moratorium, enrollment to 133% FPL, full benefits less NEMT —
explicitly one fiscal year, after which adults 21+ are no longer eligible to
enroll. The January 2026 performance testimony's 24% FPL grind-down is
superseded. By FY2030 the Health Care Alliance is a children's programme with
an adult residue. DCFPI reports 19% FPL and an explicit sunset; DHCF's own
testimony says 24% and a closing cohort. Unreconciled; use DHCF's.

**No DC count exists for the §71109 population.** CMS SHO #26-001, 8 April
2026, stops federal match for lawfully present noncitizens from 1 October 2026.
CBO's 100,000 is national. The $2.5M / 250 / 575 figures in the FY2027 budget
are marketplace premium-tax-credit losses, a different population, and will be
misread as the Medicaid count if placed near it.

## The claims allocation

**D-81. DC MCOs pay no long-term care. Hard zero, program design.** All DC
long-term care claims are fee-for-service; non-dual, non-SSI long-term care
does not run through the plans. `legacy_mix=True` currently draws $7.05 per
$100 of MCO long-term care off the national mix — the largest single modelled
flow in the payer column, and it cannot exist. Removing it takes the long-term
care bar from $36.09 to about $28.96.

**Two of four plans yield a measured service split.** AmeriHealth and Wellpoint
are DC-domiciled single-state entities, so their NAIC Statement of Revenue and
Expenses is DC Medicaid and nothing else. MedStar's blank is the combined
Maryland and District book ($960.6M premium against $403.7M of DC revenue) and
Schedule T allocates premium by state, not expense by service by state. HSCSN
files no blank. Coverage: $1,172.0M of $1,756.1M, 67%.

Measured, AmeriHealth + Wellpoint CY2024, against the national mix as applied:
long-term care 0% against 19.4%; prescription drugs 14.21% against 5.2%;
hospital, physician and ER as one block 84.67% against 56.8%.

**The NAIC lines are not comparable across plans.** AmeriHealth books 46.8% to
hospital/medical and 30.2% to other professional; Wellpoint 68.2% and 7.8%.
Combined, 77.05% and 76.04%. Same money, two booking conventions. Only the
combined block is usable, which collapses the hospital / physician separation
at plan resolution. The 1.07% wrap figure is not real: DC covers behavioral
health through the DCHFP at under 10% of medical cost, and the blanks have no
behavioral line, so it hides inside other professional services.

**Encounter data is not public.** It lives in DHCF's MMIS. The performance
report publishes PMPM trends across five service categories — inpatient,
outpatient, emergency, behavioral health, pharmacy — as percentages only. No
levels. Access needs a data request and a use agreement.

## The source column

**D-82. The non-federal share is decomposed, not replaced.** DC's appropriation
splits it across four funds. Dedicated Taxes are provider assessments: a
hospital inpatient provider fee on net patient revenue, a hospital outpatient
provider fee on gross patient revenue, the Healthcare Provider Tax on nursing
facilities, and the ICF-IDD assessment funding the Stevie Sellows Quality
Improvement Fund. The statutes tie them to Medicaid rates — the inpatient fee
exists to hold fee-for-service at 98% of cost. FY2024 $114.647M, doubling in
FY2025 when D.C. Code §44-665 takes effect with amounts owed from 1 October
2024.

Rejected: rebuilding the hundred on the appropriation. It moves the denominator
from $4,372.0M to $4,401.5M, a 0.67% scale shift that moves every figure on the
panel and puts DC on a different denominator from national. The federal FPR
grant ($0.05) and special purpose revenue ($0.09) are sub-pixel and both belong
outside Exhibit 16 anyway.

Adopted: one rule inside the existing State bar. $26.83 = local appropriation
$24.2075 + provider assessments $2.6223. Denominator, scale and federal
untouched.

**Not drawn as a loop.** The assessment base is total patient revenue, not
Medicaid patient revenue, so most of the assessed dollar comes from outside the
hundred. An arrow from Providers back to the source band would assert
circulation that mostly is not there.

**Special purpose revenue is already in the panel.** It is chiefly the Medicaid
Collections–Third Party Liability fund, and Exhibit 16's total is net of the
−$10M collections Exhibit 17 reports. A source band for it would count the
money twice in opposite directions.

## The collections item, reframed

Not a state-variation question. Exhibit 17 carries collections as a standalone
line and declines to place them. The DC ledger nets the $10M onto
fee-for-service anyway — its five FFS nodes sum to $2,250M against Exhibit 17's
$2,260M — and the national pro-rata fold lives in `build_xlsx.py`, outside the
ledger, in a comment reading "collections folded proportionally." Two
undeclared assumptions about a figure both sources report as unallocated. Not a
finding until we establish where recoveries actually come from.

## Changed in the repo

| file | change |
|---|---|
| `ledger_dc_2024.py` | `anchor.budget.dedtax` $114.647M measured; `anchor.state.provider_assessments` and `anchor.state.local_appropriation` derived, parents named, basis warning carried |
| `ledger_dc_2024.py` | four S-105 offenders corrected at the Exhibit 16 and Exhibit 17 derivation comments — the dollars stay typed, the per-$100 shares now point at figure keys |
| `STATE_INTERROGATION.md` | new. Standing questions per phase, seven-rung source ladder, eight traps, all paid for in this session |

## Open, and named so they are not quietly closed

1. **The DC ledger still carries the CY2023 composite** under Wellpoint's name.
   Known wrong, not yet corrected. Highest-priority DC item.
2. **`legacy_mix=True` draws $7.05 of MCO long-term care that cannot exist.**
   Known wrong, not yet corrected. Second highest.
3. **The dedicated tax is in the ledger and nothing draws it.** `compose.py`
   reads exactly `L.sources["federal"]` and `L.sources["state"]` into an
   `Instance` with one `fed` and one `state` field. A third `sources` key would
   pass `check` and be silently dropped by `compose`. `subs_spec` drives tracker
   markers, not source decompositions. Drawing it means widening `Instance`,
   `compose.py` and the source-column code in `sankey.py`.
4. **One S-105 offender remains in `ledger_dc_2024.py`**: `LEGACY_ABSENT` types
   the national oversight peel as $0.10. A real fault — if the national figure
   moves the DC declaration lies. The fix changes rendered text and needs a
   bless, so it was not made at session close.
5. **Vaccines for Children is absent from the DC panel and not declared.**
   Federal oversight *is* declared, contrary to the session brief. One gap, not
   two. The panel declares five absences; reconcile against the nine the brief
   claims.
6. The two-plans-versus-four question on DHCF's current managed care page.
7. Alliance and ICP band treatment: parallel declared band outside the hundred,
   or three sources inside a redefined hundred. Decision not taken.
8. Everything carried in from the 19 September list that this session did not
   touch: DC Phase 2 signing, `build.py sensitivity` before `--bless`, the
   author page, EN-43, the services table cents, the `build_xlsx.py` wrap-around
   split, two DC ledger files and two FY2030 ledger files.
9. **The repo is public and v5.0 has gone to outside readers.** Raised 19
   September, raised again 21 September, not decided.

---

## 2026-09-26 — D-87 through D-89, S-108; the line, the spine, the long tributary

**Decisions**

- **D-87 · The spine moves once, and is frozen again.** State government and
  disbursements each lose 10%; the 50 units recovered go to the LEFT MARGIN.
  PAYER onward is untouched at 1060 / 1300 / 1560 / 1760 / 2180, so the right
  two-thirds of every panel and every crop that cuts it is where it was. The
  boundaries are not derived from anything and never were: 1.2 froze them by
  listing them, and says nothing about where they came from.

- **D-88 · The flow area gains 40 units.** The Medicare Savings tributary runs
  the width of the page now and the rows it passes over have to clear it; at
  the old floor two of them ran into the tracker. H 1376 -> 1416. W and the
  scale stay frozen (1.2, 1.3); H never was, and was extended once before for
  the same kind of reason.

- **D-89 · The Medicare Savings loss leaves the Eligibility Rules bundle.**
  Four of those five levers are dollars that would have bought care. This one
  would have paid a Medicare premium and lands on the dual eligible, and the
  panel now draws that difference — summing it with the other four told the
  reader they were the same kind of loss. Eligibility Rules reads -$6.95; the
  new marker reads -$1.28.

**Standing notes**

- **S-108 · Prose follows the figure.** Where body prose and the figure on the
  page disagree, the PROSE is adjusted to match the figure, not the other way
  round. Always brought to JW for sign-off; never applied silently.

**Also landed**

- The tracker line's ends were re-aligned: the first anchor to SOURCE_X, where
  the money first appears on the canvas, and the last to the CENTRE of the
  beneficiary column rather than the end of the provider column. Attribution
  unchanged — no outflow originates in either vacated stretch.
- The year is a standing label at the left of the line, 40px. The first
  anchor's sub-label carries the basis alone: "Actuals", "Projected under
  prior law". The year was the only place the year appeared on a bare panel.
- The Medicare Savings moratorium is an ordinary tributary reaching the
  BENEFICIARY column. Closes EN-19, open since it was written. The dashed
  incidence treatment tried first was cut: JW, "I hate the dotted line
  treatment, it's a blight."
- Ribbon control points are capped at 340 units downstream (CTRL_MAX). Half
  the run is right for a short hop and wrong for a long one — a tributary
  crossing the page descended so gradually it rode at mid-height through
  everything it passed. Only the Medicaid enrollment rule changes, by 28 units.
- The HR-1 fan now reads a declared terminal height, a mechanism that already
  existed for the ordinary outflows and that the fan never read.

**Brittleness removed**

- `sankey.py` held a SECOND copy of the column spine as xFED..xBE. S-096.
  Derived from `outflows.COLS` now.
- Every peel's `src_x` was an absolute canvas position; they are offsets from
  their own column's left edge via `_at(col, off)`.
- The three pinned peel positions were typed in four files; `views.py` and
  `instances.py` read them from OUTFLOWS.
- `FAN_FLOOR` was a literal with the tracker rule's position copied into a
  comment beside it. RULE_Y is declared with the layout spine and the floor
  derives from it.

**Renumbered.** The 25 September national set was allocated D-78 through D-81,
four days after the 21 September DC session had spent those numbers. DC keeps
78-82; national moved to 83-86. 21 lines across nine files, by line number.
There is no decisions register, which is why this happened twice; one is being
written.

**Carried to the next build**

- **Figure placement, deferred by JW.** Three mismatches stand: page 4 discusses
  Medicare premiums with no figure, page 9 shows Figure 8 while discussing work
  reporting, page 16 discusses "Everything else" with no diagram. Check page 16
  for a detector false positive on the Limits register before moving anything.
  Under S-108 the prose moves, not the figure — with sign-off.
- **All 18 crop boxes are stale.** The canvas is 40 units taller (D-88) and the
  first four columns moved (D-87); 8 of the 18 cut sub-regions left of PAYER.
  Re-cut before judging placement.
- **The Medicare Savings marker is drawn outside the segment it is charged to.**
  It sits on the providers/beneficiaries divider at x=1760, which is where the
  loss LANDS; the $1.28 is subtracted in the Budgeted -> Funding Disbursed
  segment, where the money LEAVES. Both anchors reconcile ($98.75 - $84.47 =
  6.05 + 6.95 + 1.28), but a reader adding the markers between Claims Paid and
  Health Services Delivered will find $0.99 of anchor movement against $2.27 of
  markers. Declared exception to 4.9 in `DECREMENT_X`. Needs either a note on
  the marker or JW's acceptance.
- **Gate 31** not yet written. **E&E caveats** not yet drafted. **Cover
  graphic** in hand.

**D-90 · The artwork is drawn on the page, not on a card.** The panels, the
cover graphic, the comparison sheets and the figure frames were all painted
#faf8f3, which is the colour of the paper's BOXED FURNITURE — callouts, the
limits register — while the page itself is #ffffff. Every figure therefore read
as a tile sitting on the page rather than as part of it. Artwork background and
the label halos are now the page white. Manuscript forked to
`paper_national_v6_1.html` with `render_v6_1.py`; v6.0 kept.

**Beneficiary incidence — designed, not built.** JW asked for the section to be
rewritten beneficiary-centric. The pies cannot carry it: they hold FY2024
COMPOSITION, and the FY2030 pies are FY2024 scaled by one multiplier, so all
four groups fall by 9.83% as an artifact. Allocating the six service falls by
each service's own mix was tried and came out flat, 9.80 to 10.00 percent, a
non-answer dressed as a finding.

What works is allocating the PROVISIONS, which is where the named populations
are. Built in `inc.py` as a declared thought exercise. Margins only get
published; the full cube goes in the footnotes, because the unraked cube
contradicts Figure 11 on every service (long-term care -1.89 against a
published -2.86) and the raked version puts adults at 44.9% of their own
long-term care, which is an artifact of forcing the margins to agree.

`family.py` draws two composite households from it. Not a case, a reference
architecture.

**Statute research, and it moved the answer.**
- §71107 six-month renewals: the adult expansion group at §1902(a)(10)(A)(i)(VIII)
  plus equivalent §1115 populations. CMS SMD 26-001.
- §71119 work reporting: the same group, 19 to 64, not enrolled in Medicare;
  43 states and DC. Non-expansion states are NOT required to implement it.
- So the answer to JW's question is NO: neither provision reaches the
  non-expansion, non-ABD, non-SSI population.
- The IFC (91 FR 33348) excludes parents, guardians, caretaker relatives and
  family caregivers of a dependent child 13 AND UNDER, **or of a disabled
  individual of any age**, and multiple caregivers in one household may
  qualify. A household with a disabled dependent is exempt permanently; a
  household with young children is exempt until a birthday.
- Medicare Savings, 2026: Part B premium $202.90/month, $2,434.80/year; Part B
  deductible $283; Part A deductible $1,736 per benefit period; QMB pays
  premiums, deductibles and coinsurance, SLMB the premium only.

**D-91 CANDIDATE, NOT TAKEN. The Adults row should be two rows.** Exhibit 21,
the row already signed in `ledger_national_2024.py` at vintage FY2023,
publishes FIVE eligibility columns and we summed two of them: Child 15.6%,
**New adult group 22.5%, Other adult 11.7%**, Disabled 28.9%, Aged 21.3%. Its
footnote 4 defines other adults as those under 65 qualifying through a pathway
other than disability or §1902(a)(10)(A)(i)(VIII) — parents and caretakers,
pregnancy. That is precisely the population the two biggest provisions do not
reach.

Splitting it: an expansion adult loses 28.0% of the Medicaid dollars behind
their care; a non-expansion parent loses 4.4%, the same as a child. The 19.9%
we were about to print is the average of two groups with nothing in common
under this statute. No acquisition is needed — the source is already open and
signed. The existing Adults figure will report LAPSED on edit and the two
replacements need a person's signature.

**Also found:** the pie interiors carry no citation. The ledger's own note says
they are fit by iterative proportional fitting from an unsourced seed, and the
cube reads its service-by-group numbers off them. Limits register entry owed.

**`DECISIONS.md` and `decisions_index.py` written**, the register promised at
close. It finds 14 of 90 and says so on its face: the rest were recorded in
formats it does not match. Backfilling is an open item. It reports collisions
by name, which is the failure that produced the D-78 renumber.

**Two deletions added to `DELETE OLD FILES.command`**, which is where they
belong: `render_v6_0.py` and `Medicaid_Dollars_National_v6.0.pdf`.
`paper_national_v6_0.html` is KEPT — whole-number releases are permanent — so
`render_v6_1.py` now takes the manuscript as an optional argument and can
render it after its own renderer is gone.

**Later the same day — the cover, and a defect that had hidden three others**

- **The cover graphic is the taper.** Portrait, in the right half of the
  landscape cover. Built to Section 508 / WCAG 2.1 AA and measured rather than
  asserted: seventeen colour pairs checked against their thresholds. The
  secondary grey was #7a7570 at 4.30:1 and FAILED 1.4.3; darkened to #6f6a64 at
  5.05:1. The FY2024 ghost fill reads 1.43:1, so under 1.4.11 the fill is
  decoration and the BOUNDARY is drawn as a line at 3.13:1. No quantity is
  carried by colour alone (1.4.1) — a greyscale proof loses nothing. The SVG
  carries role="img", title and desc, and the long description is generated
  from the same data so it cannot drift from the picture. `cover_data.py`
  derives every figure on it; nothing is typed (S-105).
  The decrement marks are RHOMBUSES, not squares, and are a fixed size rather
  than sized by amount: a proportional mark makes $0.75 a speck, which is how
  they were getting lost, and grey squares already mean administration.

- **render_v6_0.py wrote its HTML to a temp directory.** Every figure is
  referenced as a relative path, so none of them resolved and Chromium printed
  a paper of broken image icons without complaining. The PDF was 192 kB with
  eighteen figures in it. It is 3.1 MB now.
  The three page/subject mismatches carried forward this morning were an
  artefact of this: figurefit was reading real captions against a document with
  no pictures. Both layout gates are clean and ALL SEVEN GATES ARE GREEN.

- **All 18 crop boxes re-cut** for D-87 and D-88, by piecewise remap of the
  moved column boundaries and the 40-unit canvas, not by eye.

- **Stale figures corrected in prose, six places.** $78.38 -> $78.33 (x4),
  $79.37 -> $79.32, $21.62 -> $21.67. These lapsed under the D-76 correction of
  2026-09-25 and the re-signing never reached the body text. FOR JW SIGN-OFF
  under S-108.

- **The cover stamp was cut.** It said what the cover graphic's own footer says,
  in the same words, and the graphic derives it. FOR JW SIGN-OFF.

## 2026-09-25 — D-83 through D-86, S-106, S-107; Brent's review applied

**Renumbered 2026-09-25, JW.** This set was allocated D-78 through D-81 and
issued four days after the 21 September DC session had already spent those
numbers on the Wellpoint composite, the CY2024 rebase, the DHCF revenue
finding and the MCO long-term care zero. DC allocated first and keeps 78–82;
the national set moves to 83–86, because the error was made here. 21 lines
changed by line number across nine files — a global substitution would have
rewritten the DC entries too. No figure moved.

**Decisions**

- **D-83 · The payer lanes are derived from Exhibit 17 dollars.** They were
  typed at two decimals on the old hundred (40.06 / 10.89 / 41.08) and
  multiplied through when D-70 moved the denominator, while the peels were
  re-derived from Exhibit 16 dollars. Exact figures on one side, twice-rounded
  on the other; the $0.0035 residue sat under `check()`'s $0.02 tolerance and
  surfaced as a services table whose rows summed to $87.08 against a printed
  total of $87.07. Same class as D-76. Collections ($15,201M, $1.60 per $100 —
  third-party liability and estate recoveries, NOT drug rebates) are folded pro
  rata across the capitated and fee-for-service lanes by share of gross, the
  convention the workbook always used and never declared. New module
  `basis_national.py` is the single home for the dollars, the denominator and
  the lane derivation; `provider_mix.py` and `ledger_2030.py` read it instead
  of carrying typed copies. No printed figure moves at two decimals on FY2024.

- **D-84 · Provenance is stamped, not typed.** `release.py` derives the version,
  date and a six-character build id from the content of the figure-bearing
  modules. Cannot come from git: the working copy is a tarball with no `.git`.
  Replaces two typed strings that disagreed with each other by eight days.

- **D-85 · The cover figure is cut.** It was the same file as Figure 1, one page
  later, at a third the size. New cover graphic pending.

- **D-86 · The moratorium labels are renamed.** "Blocked senior enrollment" and
  "Blocked Medicaid enrollment" described people being blocked. The statute
  suspends CMS rules that would have made enrolling easier. Now "Medicare
  Savings rule suspended" and "Medicaid enrollment rule suspended", which is
  what KFF and CRS call them, and what `ramp.py` has called them internally all
  along. Internal keys unchanged — the label string is the join key across ten
  modules; only display strings moved (`outflows.py`, `views.py`).

**Also fixed, no decision number**

- The FY2030 panel never received the D-70 correction. It carried the pre-D-70
  $5.07 overhead bundle and carved the vaccine purchase back out of it three
  ways. The two panels were struck against different definitions of overhead
  and the discrepancy cancelled invisibly. Vaccines now derived from dollars on
  all three variants, so all four panels agree at $100.76 (the "scales" variant
  printed $100.75). Tracker anchors moved: $84.53→$84.47, $79.37→$79.32,
  $78.38→$78.33; headline fall 21.62%→21.67%.

**Standing notes**

- **S-106 · A printed line must add up as a reader adds it up.** All four
  national panels shipped in v5.0 with a tracker line that did not close.
  Caught by JW with a calculator, which is not an instrument. Anchors hold,
  decrements give way, allocated by largest remainder within each segment;
  `build.py` raises rather than warns. `gates.py` pins the count.

- **S-107 · A comparison sheet shows whole artifacts, stacked, and nothing
  else.** Sankey and tracker line together, in register. Two panels means two
  images. Labels `v5.0` and `PROPOSED`.

**Signatures** — 26 of 36 lapsed under D-83, re-signed 2026-09-25 on
`reference_renders/sign_2026-09-25.png`. Three agreements, not one: each figure,
the collections convention, and S-106's anchor-holds rule. Coverage moved 24/2
verified/modelled to 21/5 — the three payer lanes are now MODELLED because the
pro-rata key is ours. The count falling is the honest direction.

**Gate expectations updated** — coverage national counts; `render_v5_0.py`
renamed to `render_v6_0.py`; tracker-line reconciliation pinned at 3.

**Manuscript** — `paper_national_v6_0.html`. Twenty-six review items from Brent
applied. All four whitespace strandings closed by the reflow, with no prose
written to fill them.

**Open at close** — figure placement mismatches on pages 4, 9 and 16 (new, from
the reflow); item 32 (year label, line geometry); gate 31 (caption counts);
item 28 (cover graphic); two E&E caveats to draft; landing-page URL and
repository path are non-functional placeholders and must be real before ship.

---

## 2026-09-26b — v6.2, step 1

**D-91 · The Adults row becomes two rows.** MACStats Exhibit 21, FY2023,
publishes five eligibility columns. This ledger carried four: the two adult
columns were summed. They are not one population and the FY2030 provisions do
not reach them alike, so §71119 and §71107 could not be stated of the group
they actually reach without also asserting them of parents and caretakers.
Exhibit 21 footnote 4 defines "other adults" as those under 65 qualifying
through a pathway other than disability or §1902(a)(10)(A)(i)(VIII).

The two dollar figures are derived in code from the exhibit's own percentages,
22.5 and 11.7 — never typed (S-105). The adult total is unchanged, so the three
rows that did not move keep their 25 September signatures and no column margin
below the row moved. JW pre-signed the two replacement figures in the session
plan: `beneficiaries.row.New adult group` 19.592483560015832 and
`beneficiaries.row.Other adult` 10.188091451208233.

Three sub-decisions taken under the batching rule, recorded rather than asked:

- **The three unmoved rows are left alone.** Deriving all five rows from the
  exhibit's percentages — the fuller S-105 answer — moves Children, Disabled
  and Aged by 0.003, 0.002 and 0.0004 against their signed values, because the
  typed figures were percentage × base rounded to two decimals. That would
  report three figures LAPSED, which is outside the pre-approval. The adult
  split is derived; the other three keep the values that were signed. **Open
  for JW: re-sign the three and derive all five, or leave it.**
- **One declaration, not four.** `ledger_national_2024.ex21_groups()` is now
  the only place the group totals exist. `instances.py` carried the dict twice
  and `ledger_national_2030.py` once; under D-91 all three would have gone on
  publishing a summed adult row while the ledger did not. `sankey.py` and
  `inc.py` read the group set off the composed row margin rather than a list of
  their own.
- **Both adult rows take the seed the single adult column carried.** The IPF
  seed is per-service utilisation and carries no citation. Splitting it would
  invent a pattern; duplicating it splits the adult slice pro rata by margin
  and invents nothing. Declared, and belongs in the Limits register entry step
  3 already calls for.

**Layout consequence.** The beneficiary key went from four entries to five,
332 units to 504, wider than the column: Aged printed past the right edge of
the artifact. The key now wraps on the column's own right edge, measured, so a
sixth group lands correctly without another edit.

**Verification.** `inc.py` reports the new adult group at −28.0% of its own
FY2024 baseline and other adults at −4.4%, the same as children. JW's stated
expectation was about 28% and about 4.4%. Nothing moved by a point.

**Gates** — all seven green. `coverage.py national` expectation moved 21→22
verified of 32 (the row margin gained a figure). Fifteen panels re-blessed.

**Open at close** — see the session report.

**D-93 · The provenance line is stamped, not laid out.** JW reported body text
running into the footer on pages 4, 6 and 8. Cause: `position:fixed; bottom:4mm`
positions against the PAGE AREA in a paged context, not the paper, so the line
sat 4mm above the bottom of the flowing text, inside the column.

The first fix pushed it out with a negative `bottom` and then a transform. Both
made Chromium print the line at the TOP of every page — caught by JW, not by a
detector. Measured afterwards on a probe document: `bottom:-7.5mm`,
`transform:translateY(9mm)` and a negative margin all land at the top, and every
non-negative `bottom` leaves the line inside the text. There is no offset that
works. The band cannot be reserved by moving the footer.

So `render_v6_2.py` stamps the three fields into the margin with pymupdf, from
the same `_FILL` values the manuscript would have carried. `@page` bottom margin
13mm to 18mm; the line sits at 9mm, below the text, with 18.5pt of clearance.

`footerfit.py` is new and gates it. It finds the line by position AND content,
because its own first version took "whatever sits lowest on the page" and went
on reporting clean while the footer was at the top — measuring body text against
body text. It works on text lines rather than blocks: when the two overlap the
extractor merges them into one block and a block-level check cannot see it. It
reproduces the collisions on v6.1 pages 3, 4, 6, 8 and 18 and reports none on
v6.2.

**whitespace.py was blind for the same reason.** The footer was the lowest text
on every page, so `dead_space()` measured from it and returned about one line on
every page of every draft — cover, plates and section ends alike, which is not
possible. Every green it printed was the footer. With the footer gone from the
flow it reports six real strandings, pages 12, 15, 17, 18, 19 and 20. JW is
closing those by hand. The `render_v6_2.py` gate is RED and its EXPECT is NOT
relaxed to hide it.

**D-94 · whitespace.py is rebuilt on content, not on ink.** It reported about
one line of dead space on every page of every draft, including covers, plates
and section ends. Five faults, all of which had to go:

1. It measured down to `FOOT_MM = 13.0`, a typed copy of the `@page` bottom
   margin. D-93 moved that margin to 18mm and this file went on measuring
   against 13. The text bottom is now read off the document.
2. It measured the lowest ink, and the lowest ink was the provenance footer on
   every page. The footer is now excluded by its own text, on the same test
   `footerfit.py` uses.
3. The renderer paints a large unstroked backing fill behind the text area,
   drawn to the page box. Its lower edge is the bottom of the text area on
   every page whether or not any text got there. Excluded.
4. `column-rule` is a hairline drawn to the full height of the column box, not
   to the last line in it, and it straddles the centre, so it poisoned both
   columns at once. Excluded.
5. The raster was sliced at exactly W/2, so that rule fell in either half or
   neither depending on rounding. Columns are now assigned by the x-midpoint of
   each span, and a span that straddles the centre counts for both.

Two things added rather than fixed. `flow_bottom` takes the deepest y that
QUORUM=3 pages independently reach, not the maximum, because one figure
overrunning the text area would otherwise redefine the text area as wherever it
reached and make every other page read short; `overruns` reports those
separately, with a whole line of tolerance, since the notes are set at 7.9pt and
legitimately sit lower than the body. And a blindness check: if the spread of
dead space across pages is under three lines, the file says MEASUREMENT NOT
TRUSTED and fails, because a paginated document has section ends in it and a
flat reading is the signature of measuring to furniture. That check would have
caught the original fault on the day it was written.

Cross-validated: on v6.1 it reports strandings on pages 10, 15 and 16 and the
page 4 overrun, which is the footer collision seen from the other side. On v6.2
it reports seven, pages 5, 12, 15, 17, 18, 19 and 20.

Two of those were mine and are closed: the households figure was 1.29 to 1, took
a page of its own and printed 10.6mm into the footer; `family.py` is now 1.64 to
1 and fills the measure, and `.plate img` came down from 150mm to 145mm. The
remaining seven are prose flow, for JW.

**D-95 · The crops become a family of tapers.** JW: Figures 6, 7, 8, 9 and 11
as horizontal versions of the cover graphic, same style, same compositing,
provision by provision. `taper.py` builds all five from one generator against
`cover_data.load()`; nothing is typed.

Each figure names the provisions it is about and draws the rest of the run
greyed rather than cutting it away, which is what made the crops hard to read:
a crop shows a piece of a picture with no picture around it.

The phase set runs one further up than the cover's. Figure 8's whole subject is
the provider tax leaving the federal column before the two shares merge, and
the cover starts at the state agency by JW's own decision, so a figure in the
cover's language had nowhere to put it. `cover_data.load(federal=True)` prepends
the band and moves that one marker into it. The cover is unchanged.

Two geometries derived rather than typed. Each canvas is sized to its own
labels, then widened to hit one family aspect ratio of 2.9 to 1 at that height,
iterating to a fixed point because widening changes the wrapping. All five
therefore print at 86mm on a 250mm measure under one CSS rule, and none strands
paper beside itself. The rule and the generator have to agree; `whitespace.py`
reports it when they do not.

**Figure 12 is new: `population.py`.** JW's page-14 note asked for the pie
information told from the population's side. Five categories in dollars off the
hundred, each fall split into coverage and rate. The households graphic follows
as Figure 13. The service strip is FY2024 composition only and says so; note 13
says why the cube behind it is not published.

**Figure 3** loses the state agency lane. It began at x=664, inside
STATE_AGENCY (584-844), so it opened on the green block its caption never
mentions. The crop now starts at the disbursement boundary read from
`outflows.COLS`.

**`contrast.py` is new.** Accessibility was asserted in docstrings with typed
ratios, which is the S-105 defect wearing a different hat: the colour constant
moves and the claim beside it goes on reading as though someone checked. Every
custom graphic now measures and prints its ratios at build time. A decorative
fill gets its own verdict rather than a false FAIL, and only where the same
shape is also stroked at a passing ratio.

**Two versions of every custom graphic**, masthead on for standalone use and
off for the in-paper version, across the cover taper, the five tapers and the
population graphic. Each ships its own script, SVG, PNG and generated alt text
in `cover/`; `make_figs.py` builds every one of them in a single command.

**Cost, stated.** The figure-placement detector went from one mismatch to five.
The provision section traded three column-width crops for three full-width
tapers, so the prose for work reporting, provider tax limits, the residual, the
directed payment caps and six-month renewals now sits on pages carrying no
figure. Whitespace strandings went from seven pages to eight, and page 9 is the
worst at 38 lines: the provisions table and Figure 7 do not fit together. Both
are layout, and both are in JW's hand pass.

**D-96 · A section starts a page.** It was true of the first five sections by
accident: four carried an inline `break-before` and the rest happened to fall
right. From page 15 it stopped being true. It is a rule now, `break-before:page`
on `.sechead`, in one place, and the four inline copies are gone.
`sectionfit.py` measures it on the rendered PDF by type size rather than by
wording, and reports NO SECTION HEADS FOUND rather than a pass if the type-size
test ever loses its subject. Twelve of twelve open a page.

**D-97 · The generated figures are drawn at the size of the slot they sit in.**
JW: design the output to fit the context it is already in, do not push the
content around the paper to suit the picture. Every generated figure now works
in millimetres of page at one scale, PXMM = 11.7, with `px()` for type in POINTS
and `mm()` for distances. The first version of `taper.py` used one helper for
both and every layout constant came out at a quarter of its intended size,
because a millimetre and a point are not the same unit and nothing in the code
said which was meant.

Each figure is generated at exactly its slot: Figure 6 at 250 x 119.5mm, the
size of the crop it replaced; Figures 7 and 9 at 118 x 61.6mm; Figures 8, 11,
12, 13 and 14 at 118 x 87.2mm. The manuscript places them at full width of
whatever they sit in and caps nothing, so the picture and the page cannot
disagree about how big the picture is. A figure that outgrows its slot fails the
build with a named message; it is never scaled down until its type stops being
readable.

Three simplifications, all deliberate, all with JW's permission. The in-paper
versions carry no masthead, title, subtitle or footing, because the figcaption
says both and the page carries the masthead; the standalone versions keep all of
it. A narrow taper prints short phase names and drops the "was $X in FY2024"
line, which the ghost edge already says. The population figure drops its FY2024
composition strip, because Figure 4 already divides every service by category
and this figure's question is WHO.

Two layout faults fixed inside the family: the narrow labels moved from one
stack to two columns, because three provisions in a single stack need 74mm of a
62mm slot; and the amount moved above the label rather than beside it, because
a 14mm gutter out of a 55mm column wrapped every label of more than three words.

**The households are two figures.** JW: the pair was squeezed into one landscape
graphic and the people came out flattened. Figures 13 and 14, each the width of
its column, with the reasoning moved out of the picture and into prose beside
it, written from the household's side rather than the ledger's.

**Figure 4 re-cropped.** The payer column is out and the crop opens high enough
to carry the whole beneficiary key. It began at x=1250, inside PAYER
(1060-1300), and at y=100, which sliced the key. Both bounds now read from
`outflows.COLS`.

**figurefit.py taught about generated figures.** It tests a subject by asking
whether that subject's label on a panel falls inside a crop's rectangle. A taper
has no panel behind it, so every provision page reported as carrying no diagram:
the detector missing a new kind of figure, not the page missing a picture. A
generated figure now declares what it shows, from the generator's own focus
lists, and `SUBJECTS` carries the S-108 names rather than two that had stopped
matching anything.

**Where it stands.** One figure/subject mismatch, page 11, six-month renewals:
five provision sections and four figures. Nine whitespace strandings; pages 13
and 18 at 38 lines are the two worth looking at first.

**D-98 · The provisions section is reordered into phase order, and the figures
are trimmed to their own content.** JW, seven instructions in one pass.

*Footer.* The repository path comes off; it will live on the landing page, so
there is one address to fix rather than two. The centre carries `Page x of y`,
stamped per page by `render_v6_2.py`. Both `footerfit.py` and `whitespace.py`
had to be told about it: the page number carries none of the marks the other
two fields do, so the first reported it as body text colliding with the footer
on all 25 pages, and the second measured to it and tripped its own blindness
check. That check firing on the first new footer field it ever met is the
strongest evidence it was worth adding.

*Phase order.* The table and the section ran largest-to-smallest while Figure 6
drew the run in phase order, so the reader met the provisions in two different
orders on facing pages. Both now read provider tax, the residual, work
reporting, six-month renewals, the Medicaid enrollment rule, the directed
payment caps, the Medicare Savings rule. The three detail figures were re-cut to
match: Figure 7 the federal band, Figure 8 the state agency and disbursements,
Figure 9 the payer and claims and beyond. Between them they name all seven, so
no provision is discussed without a picture that has it in colour.

*Page 8.* Figure 6 sits at the head of the section now rather than after the
lede. A spanning element splits a multi-column flow, and with only a lede above
it the second column was balanced into a strip and left empty. At the head of
the page the text flows beneath it into both columns, which is what a
typesetter would have done. `whitespace.py` prints that diagnosis itself now:
a page whose columns both end early while carrying a full-width figure is told
to move the figure up.

*Dead paper inside the diagrams.* `artwhite.py` is new and measures it, because
no instrument here could: a figure drawn on a canvas taller than its content
prints blank paper the page cannot reclaim, since as far as the page is
concerned that blank is part of the picture. JW caught three by eye and each
was costing about 40mm. The generators now trim to their own content and then
trim again against the RENDERED blank, because the layout cursor sits a few
millimetres past the last ink. The cover taper had 24mm of hole where the
masthead used to be; the drawing lifts by exactly what was removed.

*Tables.* Numbered and captioned in the same voice as the figures, above the
rule. Tables 1, 2, 3, 4 and 5. In the payer section the table moved below
*Same work, less pay* so prose separates it from Figure 10, on the standing
rule that a table and a figure should not sit against each other.

*Figure 12 redrawn across the measure.* JW could not tell what it meant, and he
was right: $0.29 against $25.16 is a millimetre of paper. The fall now gets its
own panel at a magnification DERIVED from the data rather than chosen - the
largest fall fills the panel and the factor falls out, currently 4x - with the
scale change said out loud on the figure, a dashed rule joining each bar to its
own enlargement, and the two amounts on staggered lines with a tick down to the
segment each names. Centred on one line they overlapped on every row but the
first.

*The households are set aside* at JW's direction. `family.py` still builds and
still passes; the figures are not in this paper. The beneficiary section closes
by reading Figure 12 instead.

**Gate state.** Figure placement, footer clearance, section rule and diagram
whitespace all clean. Eight whitespace strandings remain, pages 5, 11, 13, 14,
17, 18, 19 and 20; 14 and 20 are the two worth looking at first. 23 pages, down
from 25.

**D-99 · The tables follow the diagram, and the whitespace pass is mostly
mechanical after all.**

*Table 2.* The Medicare Savings rule now reads Beneficiaries, per JW. The
ledger's `cover_data.WHO` is the single declaration and says why: the dollar
would have paid a premium for a person, which is a beneficiary reach; the fact
that it leaves the agency's budget is where it LEAVES, not where it would have
GOT to. `render_v6_2.py` checks every row of Table 2 against that dict at build
time, on the phase rather than the wording, because the table says "Federal
band" where the ledger says "Federal and state shares".

That check immediately found a second disagreement, which is NOT fixed:
six-month renewals reads Payer in the table and Disbursements in the ledger.
The build prints it and declines to pick. **For JW.**

*Table 3 was stale and is now read from the ledger.* Every FY2030 figure in it
was a cent or two out and the rate was 8.85 percent against a ledger that says
8.91. The lanes all move at one rate, and that rate is now computed rather than
typed; claims paid is derived as the three lanes less the two peels, which
reproduces $87.07 and $79.32 exactly. The lede's "falls 8.85 percent" moved
with it.

**Table 4 has the same defect and is NOT fixed.** Its per-service falls are the
figures JW described as already signed, and correcting them to the ledger would
report three signatures LAPSED. The ledger says long-term care falls 9.91
percent against the table's 9.82, and all three uncapped services fall at
exactly 8.91 percent rather than at 8.85, 8.95 and 8.63 - which means note 8's
whole paragraph about a tenth of a point of allocation rounding is describing
something that is no longer in the model. **For JW: this needs a signature.**

*Figure 10* is a custom diagram now, in the same vocabulary as the tapers and
Figure 12: FY2024 outline, FY2030 solid inside it, the fall in the warm colour.
It is built to make the sameness visible rather than each lane legible, because
the finding at the payer is that there is no finding: one rate, printed once,
large, six times over.

*Whitespace.* Eight strandings to three, and the two rules that did it were
both ones JW had already stated.

A page that carries a section head and also ends short is a SHORT SECTION, not
a broken one. The rule that a section opens a page makes them, and "What comes
next" is two paragraphs long by design. Three pages were being flagged for
obeying a rule. `whitespace.py` classes them `short-sec` and exempts them.

The Limits register is a list and may break. `break-inside:avoid` threw nine
rows of prose to the next page whole and left the heading with three lines
under it; the register now spans the measure and breaks between rows.

The rest was moving things: Table 4 below the first paragraph of *What this
means for a provider organization*, which filled a page that was 38 lines
short, and the renewals aside up beside the provision it concerns.

Three remain, all section ends with no head on them: pages 11, 16 and 5.

**Figure 10 redrawn as a funnel.** JW did not like the bar chart, and the
reason it did not work is that a stack of bars is a table with the numbers
taken out: it made the reader do the comparison the picture was supposed to
make. It is now the same shape as everything else in the paper - a band of
money entering on the left, the two peels leaving upward in grey as ordinary
leakage, what is left going on as claims - with FY2024 as the ghost behind and
FY2030 solid in front, hung from the same upper edge, so the gap along the
lower edge IS the law. Only the two capitated lanes narrow at the payer line,
because fee-for-service has no plan in the middle of it.

Two drawing notes worth keeping: the peels are straight tapering wedges rather
than curves, because at two millimetres of paper a curve reads as a hook; and
the year pair is printed on every lane, so no quantity depends on the reader
measuring the ghost.

**D-100 · Figure 10 joins the taper family instead of being its own drawing.**
JW, twice: make it work like six, seven, eight and nine, just for the payer
lane. The bar chart and then the funnel were both new programs answering a
question the family already answers. `payer.py` is deleted.

`taper.py` now takes its phases and its markers from the spec rather than from
module globals, and the payer figure supplies one extra phase and two extra
markers. Palette, ghost-behind-solid, rhombus, two-column labels and slot
arithmetic are the same code, so the figure cannot drift from its siblings.

The extra phase is the payer itself. The band is flat across it, because
nothing has left yet, and then steps down to claims: that step IS the $5.65 the
plans keep, and the two markers under it are its halves. They are drawn in the
focus colour because they are what the figure is ABOUT; grey in this family
means out of focus, not lawful, and the `who` line under each says they are
ordinary leakage under prior law.

Two faults in the family fixed on the way, both of which affected Figures 7 to
9 as well. Markers sharing a phase were drawn on top of each other, because the
marker's x was the phase's x and nothing spread them; they fan by half a
rhombus each now, so a reader can count them. And the last phase label was
shortened to DELIVERED, because BENEFICIARIES and CLAIMS met in the middle of a
118mm measure once a sixth phase was added.

**All seven gates green.** The last three strandings closed, each by a
different rule, and none of them by loosening a detector.

*Page 11, the end of the provisions section.* Four lines of prose, then the
"Why fiscal year 2030" aside running two thirds down one column while the other
held five lines and stopped. The box is `column-span:all` now: across the
measure it is half as tall, and the closing paragraph sits beside rather than
below it. Note that a first attempt at this did nothing, because `wide` was
already a modifier on `.box` with a different meaning and the new rule was
never added; the class is `across`.

*Page 16, the end of the beneficiary section.* Genuinely short of words, so it
got words: two paragraphs on what the coverage-and-rate split means for what a
category can do about it, and on why a state watching its enrolment line will
see the new adult group's $4.83 first and may conclude from that alone that the
law has landed.

*Page 5.* Figure 4 lost the payer column and gained the whole key in this
session, so its crop is nearly square. At 66.7mm it was 69mm wide in a 118mm
column, which put a gap beside it AND left six lines under it. At 78mm it fills
both.

Two fixes tried and reverted, recorded so they are not tried again: pulling
Figure 12 down into its own narrative made three pages worse, and moving the
FY2030 aside earlier took page 11 from 30 lines to 22 but broke a figure and
its subject apart.

**Table 4 and note 8 corrected. No signature was involved and I was wrong to
say one was.** The per-service FY2030 figures are not in `signatures.py` at
all - the register holds claims-cell figures, not these - so correcting them
lapsed nothing. I had asserted a signature constraint without checking the
register, which is the same fault as asserting geometry without rendering.

The table disagreed with the FY2030 panel the paper prints two pages earlier:
the panel says $26.25, $16.01, $37.70, $3.77 and the table said $26.27, $16.02,
$37.73, $3.78. Both now come from the ledger at build time.

Note 8 had to move with it. It explained why wrap around services, behavioral
health and prescription drugs fell at 8.85, 8.95 and 8.63 percent - "a cent of
that allocation sits between those two nodes and moves the rate a tenth of a
point in each direction". In the current ledger all three fall at exactly 8.91
percent. The note was explaining an artefact that is not in the model, and the
finding is stronger without it: three services on one number is a cleaner
statement of "no service-specific finding" than three within a fifth of a point.

**D-101 · Bite and reach are two declarations, and the audit that followed.**

`cover_data.WHO` now carries an optional fourth field, `reach`: where the
dollar would have GOT TO, as against `phase`, where the provision BITES. For
six of seven they are the same, which is why one field did the work of two and
why the build check compared the wrong pair. Six-month renewals is the
exception and the reason the split exists: the person is already enrolled and
attributed to a plan, so what is lost is a premium a PAYER would have received;
work reporting is the opposite case and stops at disbursement. It was declared
at disbursements only because the cover had no payer column, and D-100 gave the
family one. The table and the heading were right; the ledger was wrong.

**`figaudit.py` is new.** `typedfigures.py` finds figures in the CODE that
should have been derived. Nothing looked at the ones in the PROSE, and that is
where every defect below had been sitting. It builds the set of quantities the
ledger can produce, at the precision the paper prints them, and lists every
dollar figure in the document that is not in it. It is a list to read, not a
pass or a fail: the paper also prints statutory amounts and CBO totals this
model never computes.

Found and corrected, all of them stale against the ledger:

- **Table 1** said $29.13, $17.91 and $15.45 where the panel says $29.14,
  $17.90 and $15.44. Rebuilt from the ledger at build time, like Tables 3 and 4.
- **Table 5** said $25.16 for the disabled row where page 6 said $25.17. See
  the row-margin fix below.
- **Behavioral health's fall** read $0.86 in the prose against $0.85 in the
  ledger.
- **Note 9** still divided $8.54 across the categories; the figure is $8.59.
- **The Medicare premiums ribbon** was said to fall to $1.64 in two places. It
  falls to $1.67.
- **$45.69 leaves as claims** was $51.34 minus $5.65, arithmetic on two rounded
  figures. Measured, it is $45.68.

**The row margins are the ledger's, not a re-derivation.** `inc.BY_G` summed
the pie interior, which sits on c24.node's 87.07, while the ledger's signed
group totals sit on 87.0749. Six thousandths of a percent, and enough to print
the disabled row as $25.16 in Figure 12 and $25.17 on page 6: one quantity, two
numbers, one document. The signed margin wins and the interior is raked to it.

**One finding NOT fixed, and it is the largest.** The FY2030 panel draws its
beneficiary pies by scaling FY2024 with a single multiplier - the Limits
register says so, and says it "carries no information about who bears the law".
Figure 12 and Table 5 allocate by the population each statute names. Both are
in the paper. The panel puts the new adult group at $17.66; Figure 12 puts it
at $14.11. Same quantity, $3.55 apart, on facing pages. "The text follows the
diagram" cannot settle this one, because here the diagram carries the weaker
model. **For JW.**

**D-102 · One incidence model, not two.** JW approved. The FY2030 panel drew
its beneficiary rows as the FY2024 shares times one multiplier; inc.py
allocated each provision to the population its statute names. Both were
printed. The panel put the new adult group at $17.66 and Figure 12 put it at
$14.11, on facing pages, and nothing in the repo could see it because the two
models lived in modules that never imported each other.

`incidence.py` is new and holds the allocation. It depends on the raw ledgers
and the pie solver only - not compose, not instances - because
`ledger_national_2030.py` has to call it while compose is still importing, and
a module that reaches back up its own import chain is how one model becomes
two in the first place. `inc.py` is now presentation: the cube printed for
inspection and the names the figures import.

Two sub-cent traps on the way, both the same fault at smaller scale. Recovering
the provision amounts from the composed panel's steps rather than importing
`tobe2030.per100` put the panel at $14.16 and inc.py at $14.11. And passing the
composed node totals rather than the ledger's own moved the fourth decimal.
inc.py now READS the FY2030 margins off the panel and rakes its own coverage
and rate split to them: a published figure is measured, not recomputed.

Fifteen panels re-blessed against a stacked before-and-after, S-093. Nothing
lapsed: no FY2030 beneficiary row is in the signature register.

Downstream, all corrected: Table 5 and Figure 12 regenerated, eight prose
figures that quoted the old allocation, note 13's pool, note 14's coverage and
rate sums, and the Limits register's "Class incidence" entry, which said all
five rows fall by the same 9.83 percent "as an artifact of that scaling". They
now fall at different rates, which is a finding rather than an artifact, and
the entry says what is and is not published instead.

All seven gates green. 22 pages.

**2026-09-27, JW's final markup: 61 annotations applied.**

Structural, on JW's answers: the federal-band figure and the payer figure are
deleted and the rest renumbered 1 to 10; *What the figure says* is cut whole;
the "Why fiscal year 2030" aside becomes note 17, called from the first
paragraph of the section it belongs to; Table 3 moves into the space the payer
figure leaves; Figure 7 moves above the work-reporting heading.

**The detail tapers are cropped to their own phases and carry no grey
diamonds.** The greyed markers were there to keep the whole run visible; JW's
reading is that in a detail view they carry no meaning and read as clutter. The
span is derived rather than declared per figure - first focus phase to last,
one phase forward so the band has somewhere to go, one phase back if that still
leaves fewer than three - which is what puts Figure 8 at disbursements, where
JW asked for it, and keeps the federal and agency phases out of it, which he
also asked for. One rule, both notes.

Two consequences worth recording. A cropped band does not start at $100, so the
"$100" label prints only on the uncropped figure; printing it inside a band
that opens at $84.47 would have been a plain untruth about the picture. And
Figure 7 gained six-month renewals, because with the payer figure gone that
provision had no picture on its page.

**The FY2024 sub-labels came off the band.** They printed grey on dark blue
inside it, where they could not be read. They sit above the band now, under the
phase name and over the figure they qualify.

Corrections made while applying, all flagged on the change list:

- "four different phases" is **five**: federal band, state agency,
  disbursements, claims, beneficiaries.
- The provider-tax sentence carried six marks and lost its subject; split in
  two so "the only provision that changes" has one.
- #50-54 together weaken a claim: "does not have an alternative arrangement
  available on the same terms" becomes "is not likely to have an alternative
  arrangement available at lower prices". The original says substitutes do not
  exist; the new one says cheap substitutes do not. Applied as marked.

**An earlier batch in this pass aborted after a failed match and wrote
nothing**, so three edits I had reported as applied were not. They were caught
by rendering and reading the page rather than by trusting the script's own
output. The lesson is the file write, not the assertion: a batch that exits
before writing loses everything before the failure too.

**`notefit.py` is new.** Nothing was checking the footnote apparatus. It
reports one dangling caller, note 2b, and five orphaned notes - 2, 2a, 6, 7 and
10. Note 6 was orphaned by this pass; the rest predate it. It reports rather
than fails, because which orphans to cut and how to renumber is editorial.

19 pages. One stranding, page 9 at 8 lines.

## 2026-09-27 — v7.0

**Shipped as a whole-number release.** `paper_national_v7_0.html`,
`render_v7_0.py`, VERSION 7.0. Twenty pages, ten figures, five tables.

**The taper family is the paper's diagram language now.** `taperkit.py` holds
the parts, `tapertest.py` checks every figure any generator produces, and
`taper.py`, `population.py` and `cover_taper.py` all draw with them. A state
edition should need a ledger and a spec, not a drawing program.

**JW's leader rule, final form.** If the marker sits anywhere over its own
amount's hit box, the leader goes straight down and stops. Otherwise it drops
and turns to the end of the amount. A line that drops and turns reads as a
route; a line that just drops reads as a pointer, and most of these only ever
needed to be a pointer.

Two things I got wrong on the way, both the same mistake: asked to fix the
placement of the TEXT, I changed the routing of the LINES. First a rail down
the side of each column, then single-row packing that gave seven labels 35mm
each and wrapped "Provider tax limits" to three lines. Both were strictly
better by the collision metric and plainly worse to look at. JW reverted me
twice. `taperkit.pack()` - isotonic regression by pool-adjacent-violators, the
standard answer to this and the one I should have looked up rather than
invented - is in the toolkit, correct and tested, and is NOT wired into any
figure. It waits for a deliberate tuning pass.

**Known and accepted, at JW's direction:** three leaders on Figure 6 cross the
label of the entry above them, in the two columns that stack a second
provision. `tapertest.py` reports them on every run so they cannot quietly
become permanent.

**Gate state.** Six green. `render_v7_0.py` red on two counts, both expected
and neither relaxed: the three Figure 6 crossings, and one whitespace
stranding on page 14, the end of the beneficiary section at 26 lines. Moving
Figure 9 up a section made it 35, so it is left alone.

`DELETE OLD FILES.command` run: sixteen files, including the six crops the
tapers replaced, `payer.py` and its outputs, the three dead cover studies, and
the v6.2 point release. Whole-number releases v5.0, v6.0 and v6.1 are kept.

**v7.1.** JW: fit Figure 9 into the white space on the page before, without
squishing.

Nothing is scaled. The figure is rebuilt 14mm shorter - rows closer, the
magnified bar a millimetre thinner, the rate label nearer its own segment -
and every figure, every label and both panels are still there at full size.
104mm rather than 118mm, which is what let it sit under the prose instead of
taking a page of its own.

The caption came down with it, and carried a defect worth naming: it said the
right panel was enlarged **four times** while the figure, which derives its own
magnification, prints **five**. It had been wrong since the bar scale changed.
The caption no longer states the factor at all; the figure declares it, and
one of the two cannot drift from the other now.

**Nineteen pages, and no whitespace strandings anywhere.** Six gates green.
`render_v7_1.py` is red on one count only, the three known Figure 6 leader
crossings JW has set aside.

**The co-author is out of the working tree.** JW, 27 September. The held bio
file is deleted and the name and employer are redacted from sixteen other
files, in place, to "the co-author" and "her employer". The record of what was
decided and when survives; the personal data does not. Eight of those files
needed a second pass, because a blind substitution left sentences like "the
co-author is the co-author" and lower-case starts mid-paragraph.

**Corrected the same day.** The deletion list entry was first retired on the
reasoning that a list should not name the person it protects. That was wrong in
a way worth writing down: the file had been deleted in the Author's sandbox,
and the LIST is the only thing that acts on JW's machine. Taking the entry off
meant the file would have survived on the working copy while the record said it
was gone. A tidy list that does not delete the file is worse than an untidy one
that does. The entry is back, and comes off after the deletion is committed.

`DELETE OLD FILES.command` also gained a check that runs on BOTH exit paths,
including the "nothing to delete" one: it greps the folder for the name and the
employer afterwards and says so if either is still there. Tested by planting a
file and watching it fire.

**This does not remove her from the repository.** Every past commit still
contains the file, the name and the employer, and the repo is public. Deleting
from the working tree stops future exposure and nothing else. Removing it from
history means making the repo private and rewriting history with
git-filter-repo or BFG, then force-pushing; GitHub also keeps forks and cached
views of deleted content, so private-first is the safe order. Raised with JW at
v7.1 and NOT done here, because rewriting a published history is his call and
not a thing to do inside a packaging step.

---

# 2026-09-27 · The explorer, rebuilt from the ledger

**D-103 · The project's public address, in one place.** Backfilled, not new.
The decision was taken with `landing.py` and recorded only in that module's own
docstring, so `decisions_index.py` — which reads this manifest and nothing else
— reported D-103 as the next free number and would have issued it twice. The
same failure the register exists to prevent, invisible to it because the
register can only see what the manifest says.

What was decided, transcribed from `landing.py`: the URL was a
"[landing page pending]" placeholder in the paper's renderer and absent from
the deck entirely. It now appears in the manuscript footer and on the deck,
which is two artifacts quoting one string, and S-096 says that is one
declaration. `landing.URL` is that declaration; the sentence the deck prints
names the URL so it lives there too. The footer takes the bare address because
a sentence would wrap in small type. Changing it in `landing.py` moves both.

**D-104 · The incidence model must declare what it leaves out.** `incidence.RULES`
covers six of the ledger's seven HR-1 peels. The seventh is correctly absent —
D-89 established that the Medicare Savings moratorium's dollar pays a Medicare
premium rather than buying a service, so it has no service incidence and must
not enter `gross`. Correct, and unasserted: `ledger_national_2030.agreement()`
checks the ledger's HR-1 set against `outflows.OUTFLOWS`, and nothing checked it
against `incidence.py`. An eighth provision landing in the ledger would have
been dropped in silence — `gross` shrinks, `scale` rises from 0.9496, the other
six absorb its dollars pro rata, the cube still sums to the pool and `check()`
still passes. That is D-102 one module over. `incidence.EXCLUDED` now names the
exclusion and its reason, `incidence.coverage()` asserts the two sets agree, and
`build.py` raises on failure. Proved by removing Work reporting from `RULES` and
watching it fire by name.

**D-105 · The explorer is a build target, not a file.** JW approved the whole
shape on 27 September. The predecessor (`medicaid_dollar_explorer.html`, Brent,
August) carried its numbers as a JSON blob pasted into the page, and two things
followed, both invisible. Its national half was struck on the OLD hundred —
$957.4B, administration $5.07, care delivered $86.27 — and went on serving those
for two decision cycles after D-70 and D-83 moved the floor. Its DC half agreed
with `ledger_dc_2024.py` to fifteen significant figures, so a machine had
written it, but a machine writing a number ONCE is not a live connection: DC has
since withdrawn its service allocation and the page went on publishing a DC
service mix (long-term care $35.94, physicians $21.63) that `coverage.py dc`
reports as MISS on every node. A withdrawn figure does not disappear from an
artifact holding its own copy.

`explorer.py` serializes the ledger with provenance on every figure;
`explorer_template.html` holds structure and copy and no figures;
`build_explorer.py` writes one self-contained HTML plus the data separately.

**D-105a · The lever is a visibility control, not a recalculation control.**
JW's reading, and the better one. Selecting a provision greys the rest and
lights that lane from where it leaves the trunk to where it terminates, carrying
its population and service incidence. It generates no arithmetic the paper does
not contain. The alternative — remove the dollars and re-derive — produces 63
subsets, none verified and none signed.

**D-105b · Both figures travel with a provision.** Work reporting leaves the
trunk at $4.11 and only $3.90 of it fails to reach care; the gap is overhead
falling with the loss (`incidence.scale` = 0.9496). Both are true, the paper
prints them in different places, and the page shows both, labelled.

**D-105c · The three FY2030 variants replace the growth slider.** `holds`,
`scales` and `mixed` already exist and are already defensible. The predecessor's
three free sliders — federal cut, backfill, growth — had no relationship to
P.L. 119-21 and let a reader generate any number they liked under the project's
name. Removed.

**D-105d · The fact cards are the deck's own lines, read at build time.** JW:
latest MHPA deck is authoritative. `build_deck.py` writes its heroes as
f-strings off the ledger, so a card taken from `CARDS` moves when the ledger
moves; a transcription would not. `build_deck.slide()` now records its parts
structurally alongside the HTML it already emitted. Nothing the deck renders
changed.

**D-105e · DRAFT — UNPUBLISHED travels the whole way on DC.** JW's call: banner,
a dagger on every figure and tooltip, and a rotated stamp on any print or
export. Declared once on the panel; the page obeys.

**S-109 · A web artifact is proved by rendering it, not by reading it.**
`typedfigures.py` reads source, which is right for the paper: a typed figure is
a literal. A page can produce a number three ways and only one looks like a
literal. The first build of the flow view summed three ROUNDED lane margins in
JavaScript and printed $87.08 where the ledger says 87.074936, which prints
$87.07 — nothing typed, every input serialized, and a one-cent disagreement with
the paper produced by nothing but where the addition happened. `explorerproof.py`
therefore renders the built page, sweeps 32 states (every jurisdiction, year,
variant and lever), harvests every dollar figure on screen and asserts each is
one the ledger serialized. Proved by reinstating the page-side sum and watching
it named. Totals now derive in `explorer.py` at full precision; the page adds
nothing up.

**S-110 · A gate suite must build its own inputs.** `gates.py` ran `build.py`
and went straight to `render_v7_1.py`, whose `figurefit` and `artwhite`
sub-gates read `paper_figs/crops.json` and the generated PNGs. On a clean clone
those do not exist, `figurefit` died on a FileNotFoundError, and four of the six
reported misses were the suite failing to build its own inputs while reporting a
content failure. Detector fixed rather than worked around: `make_figs.py` and
`deckalts.py` are gates now, in dependency order.

**Contrast, narrowly.** JW: do not touch the colours in the sankey or the white
paper. `explorerchrome.py` measures the explorer's own chrome and nothing else —
21 pairs, all meeting WCAG 2.1 AA, measured not asserted. It also fails on any
hex in the template that no pair names, which is how the two loss tints the
chrome had borrowed were caught and moved back to `palette.py`.

**Also changed.** `coverage.rows(L, width=60)` — the 60-character truncation
exists for the terminal and the web inherited it, cutting two reasons off
mid-word. Now a parameter; the terminal report is unchanged.

**Open, and raised rather than fixed.**

- `views.V_DC.strap` still says the DC MCO service mix is a national proxy. The
  ledger withdrew that allocation and the panel now shows it absent. The strap
  describes a model that no longer exists. Editorial, so left alone.
- The deck's `CARE24` ($86.92) and the claims total ($87.07) are different
  figures in different artifacts. Both are ledger-derived and the difference is
  presumably fraud; nobody has written down which one answers "reaches care".
- D-103 was claimed by `landing.py` and recorded nowhere else. Backfilled
  above on 27 September; `decisions_index.py` now reports what it skips
  rather than dropping it (D-108).
- `render_v7_1.py` remains red on stranding (pages 3, 6, 7, 9, 10, 14) and
  leader landing. Unchanged this session.

**D-106 · The diagram goes back, with handles.** JW, 27 September: the first
rebuild replaced the sankey with bar rulers and was a straight loss. The rulers
are more legible per row and say nothing about where anything goes; the diagram
*was* the product. Brent's mechanic is restored — hover or click any band and
that money lights across the whole lifecycle while everything else steps back —
and what is new is that the handles are generated. `sankey.trace` is a context,
not an argument, so a block declares once what it is drawing and every shape
inside inherits; `band()` has twenty-five call sites and threading two
parameters through all of them is twenty-five chances to mislabel a ribbon.
Four dimensions are traceable where the predecessor had one: source, payer,
provision, and the claims fan by lane so following a payer does not stop at the
claims column. The legend is read OUT of the SVG, so a band whose key is not a
figure in the ledger fails the build rather than becoming a dead swatch.

The attributes are inert in print. `renderproof.py` hashes SVG bytes, so it
fired on fifteen panels and its raster diff was empty on every one of them,
which is the proof.

**D-106a · The overlay is a drawing layer, not an arithmetic one.** An earlier
draft of this button said "lift P.L. 119-21 off the diagram". It is false.
Hiding `overlay-hr1` removes the tributaries and leaves the trunk still
stepped, the tracker line still showing every decrement, and long-term care
still at $26.25 rather than $29.14. That control would have taken away the
explanation and kept the consequence, and a reader watching the picture barely
move would have concluded the law does little. Caught by rendering the baseline
layer alone and looking at it. Relabelled "hide the tributaries", with the
caption saying plainly that no layer of this diagram can show prior law and
that the year switch is where that lives.

**D-106b · DC ships with no diagram, declared.** `build.py` renders the DC
panel with `legacy_mix=True` — the flag its own comment marks as uncorrected —
which draws a DC service mix (long-term care $35.85, physicians $21.63) that
`ledger_dc_2024.build()` declares absent on every node. Embedding that plate
would have put a diagram asserting those figures beside a table reading "no
allocation in the ledger", on one screen, and the diagram is the one a reader
believes. It is the predecessor's defect exactly, reintroduced by this session
and caught by `explorerproof.py` rather than by eye.

Rendering DC honestly is not available: `compose()` raises `KeyError` on the
first service node with no allocation, which is what the legacy flag exists to
avoid. The panel therefore carries a stated absence instead of a drawing. **A
payer-column-only panel needs a real change to `sankey.py` and is JW's call.**

**S-111 · A gate that never rebuilds a panel cannot see it move.** `gates.py`
ran `build.py`, which renders the FY2030 mixed panel only; the two sensitivity
variants live behind `build.py sensitivity` and nothing ran it. `renderproof.py`
compares the SVGs on disk, so the stale variant files went on matching their
stale blessing and reported "unchanged" indefinitely. Both had in fact been
wrong since **D-91**: each still drew the beneficiary panel with four
eligibility groups (Children / Adults / Disabled / Aged) against the paper's
five. A false green, which is worse than the false red S-110 fixed, because
nothing draws attention to it. `build.py sensitivity` is a gate now.

**Third named figure source.** `explorerproof.py` accepts figures from
`explorer.py`, from `build_deck.py` and now from `sankey.py`, counted
separately in its report. Naming the sources rather than waiving them keeps the
claim intact: no figure on screen was computed by the page.

**D-107 · One version across all three artifacts, HTML and PDF of each.**
JW, 27 September. The paper carried `release.VERSION`; the deck was
`MHPA_Board_Deck` with no version in the name, so two builds a month apart were
indistinguishable once downloaded; the explorer likewise. All three are
rendered from the same ledger in the same build and a reader handed all three
had no way to tell they belonged together. They now take one version from one
declaration — `release.VERSION`, bumped to 8.0 — and `publish.py` writes six
files: `Medicaid_Dollars_National_v8.0`, `MHPA_Board_Deck_v8.0` and
`medicaid_dollar_explorer_v8.0`, HTML and PDF of each.

`paper_national_v8_0.html` and `render_v8_0.py` are forked from the v7.1 pair;
v7.1 is a point release and may be deleted, v8.0 is a whole number and is kept.

**Two faults the packaging found.**

*The paper's HTML did not survive leaving the repo.* It references its figures
as relative paths, which is right inside the repo and useless outside it: the
first delivered file was 61 kB against a 2,369 kB PDF, and a reader who
downloaded it would have got a document of broken image icons with no warning.
That is the 26 September 192 kB fault arriving a second time by a different
route — the file moves rather than the renderer. `publish.py` now inlines every
relative asset and raises on any it cannot find. The paper's HTML is 2,813 kB.

*The publisher would have forced a false green.* `render_v8_0.py` exits
non-zero on its own layout gates and two of them are honestly red. A publisher
that refuses to write the PDF over them means the only route to a release is to
loosen a detector that is telling the truth. The faults are reported and the
artifact is written.

**Stranding is one page, not six.** The six-page report this session opened
with was the S-110 input-ordering defect: `figurefit` was reading captions
against a document with no pictures in it. With the figures built, page 9
strands seven lines and no other page is over threshold. The leader fault on
`fig6_taper_all.svg` is real and stands — three leaders run through a label.

**`gates.py`** now runs `publish.py`, and `render_v7_1.py` is `render_v8_0.py`.

**Indexer fragility, found and worked around, not fixed.** This decision was
first titled "D-107 · v8.0. One version across all three artifacts", and
`decisions_index.py` dropped it in silence. `clean()` takes the first sentence,
"v8.0." became "v8" after the trailing period is stripped, and the eight-
character minimum discarded it. Any decision title beginning with a decimal
number disappears from the register without a word — the same class as D-103,
which is claimed by `landing.py` and indexed nowhere. The title was reworded.
**The indexer should say what it skipped rather than skipping it quietly**, and
that is a change to a shared instrument, so it is raised not taken.

**D-108 · A detector that discards its own input in silence.**
`decisions_index.py` recognised a D-number, judged its title too short to be a
title, and dropped the whole decision without a word. The length test is right
— it keeps a stray "D-12" in prose out of the index — but failing it was
invisible, and the output looked complete. That is worse than no detector.
`scan()` now returns what it skipped, `DECISIONS.md` carries a Skipped section,
and the command line names each one with the line number and what it read.
Proved by planting a heading titled "v9.1." and watching it reported.

**D-109 · A panel stops where the knowledge stops.** JW approved 27 September.
`legacy_mix` is off.

The flag existed because the renderer could not draw a panel without a service
allocation — `compose()` raised `KeyError` on the first node — so the only way
to get a DC panel at all was to fill the fan from the national mix. Its comment
called it "the visible record that DC is still carrying the national service
mix", which was honest about the choice and did nothing about the artifact: the
drawing still asserted five DC service figures this ledger has withdrawn, and a
reader had no way to know. The explorer would have republished them on the web.

`compose()` now truncates a panel whose fan cannot be drawn. **The test is what
the drawing needs, not a status word** — a value for every node margin and every
lane-by-node cell. DC is the case that forces the distinction: its matrix is
PARTIAL, not UNALLOCATED, because fee-for-service is allocated and the two
capitated lanes are not. A coarser test would have called that drawable and
failed on the first missing cell. When DC's allocation is acquired this reverts
to a full panel with no code change, because the predicate reads the matrix.

`sankey.py` draws the stop where the fan would have been, drops the PROVIDERS
heading rather than leaving a column headed and empty, and pulls the right edge
in. Only the three DC panels moved; the national panels are untouched.

**`check.py` asserts something different about a truncated panel, not nothing.**
It must be truncated WHOLE — every service structure empty, not some of them,
because a half-drawn fan is the failure that could actually reach a reader —
and it must declare a reason. Both proved by planting a node total and by
clearing the declarations.

**Two faults this uncovered, both pre-existing, both fixed.**

*The panel printed $0.00 for figures it declares absent.* `Fig.n` returns 0.0
for an absent figure and the retention labels drew whenever the lane was on, so
the DC panel read "MCO plan administration $0.00" three inches from a
declaration saying that split is not published for DC. An artifact must not
contradict its own register. The labels gate on the value now, and `check.py`
will only allow a retention with no split when a declaration says so.

*Declarations ran off the canvas.* `_draw_absent` drew at a fixed x with no
wrapping, so three of DC's eight declarations were clipped mid-sentence. A
clipped declaration is worse than a missing one: the reader sees a sentence
start and cannot tell it was cut. They wrap to the space actually left.

**Open, and now urgent rather than tidy.** `views.V_DC.strap` still reads
"MCO service mix is a national proxy (modelled)". Until today that was a stale
line. It is now a false statement about the artifact it sits on, because the
panel no longer draws a service mix at all. Editorial, so not changed here.
Proposed: "REDUCED FIDELITY. CMS-64 / MACStats FY2024 DC spine; payer peel DHCF
CY2023. The panel stops at claims: no DC service allocation is published and
none has been estimated. Vintages need re-checking."

**D-110 · Everything on the drawing is a handle.** JW's punch list, 28
September. Brent's page made the payer lanes selectable; this makes the whole
artifact selectable. Handles now sit on the overhead exits, the retention
exits, the provider bars, the beneficiary pies, the grey widgets on the number
line and the anchors. Raster identical on every panel, across four blessings.

**D-110a · A shape can belong to more than one story.** The band from the payer
column to the plan box is BOTH the MCO lane's money and the retention the
number line totals as "MCO Admin". One `data-trace` could not say both, and on
the DC panel — where the split into administration and margin is not published
and only the undifferentiated band is drawn — the "MCO Admin" widget had
nothing to light. Extra memberships go in `data-also`, separated by a pipe
rather than a space, because a provision key contains spaces.

**D-110b · A widget must light something.** `explorer._groups` fails the build
if a mark on the number line names no ribbon the panel draws. It need not light
everything: DC has no federal oversight peel and its "State Admin" mark is
still the total of what it does have. What cannot stand is a control that lights
nothing, which looks broken and lies about what it totals.

**D-110c · Group membership is declared where the ledger does not declare it.**
The HR-1 groups already name their members — `views` carries a `PeelSum` — and
those keys are read rather than restated. The four overhead groups name theirs
only inside a prose label, so the sets are written once in
`explorer.OVERHEAD_GROUPS`. Anchor membership is not written at all: an anchor
lights every key whose own charged phase is at or before it, which the peels
already know.

**D-111 · The punch list.** Two destinations, not six: the diagram, the phases
and the law are one argument read top to bottom, so they are one scrolling page.
The register moved under the summary, where somebody checking a figure will be.
Compare is gone and the District is hidden from the picker — the panel is still
built and still in the payload, so restoring it is putting one option back.

- **The provisions are checkboxes.** Turn them on one at a time and watch them
  sum. All 127 subsets are serialized by `explorer.py`; the page could add the
  selected ones up in two lines and must not, because `explorerproof.py` is
  only worth having if it is never the thing that gets relaxed.
- **The whole drawing dims, not only the tagged shapes.** Selecting "federal
  money" already dimmed every tagged band, but the trunk block, the column
  rules and every label are untagged and stayed at full strength, so the
  picture read as though nothing had happened. That was the real fault behind
  JW's note, not the one the note described.
- **The payer lanes keep their controls and lose their heading.** "Who holds
  it" was my label and it confused the reader it was written for. The diagram's
  own column headers already say DISBURSEMENTS and PAYER; a third word for the
  same phase is one word too many.
- **The overhead note moved under its control** and changes with it.
- The Summary carries the whitepaper, embedded and downloadable with no
  network, its thumbnail rasterized from page one of the very PDF beside it;
  then the deck's own slides, cover excluded, photographed rather than lifted,
  so a change to the deck's stylesheet cannot silently break this page.
- No explorer PDF. It is an interactive page and a flat print was always the
  lesser artifact.

**S-112 · Do not edit a file by index without re-reading it.** Four consecutive
slice edits to `explorer_template.html` were made against a picture of the file
from before the previous edit. One marker matched in the wrong place and pasted
the CSS block and the whole body a second time: one `<style>` open, two closes,
two `<body>` tags, 1,699 lines where there should be 860. The build SUCCEEDED
and wrote a 15 MB file, because `str.replace` filled both copies of the data
marker. `explorerproof.py` renders the page and would have caught a broken
build; a DOUBLED build renders correctly. This is the stale-picture failure
this session opened by finding elsewhere, committed by hand. Repaired by
truncating at the seam and recovering the chrome block from the stale copy.

**D-112 · The plate does not move.** JW, 28 September: the diagram jumped as
the pointer crossed the controls above it, which is worse than untidy — the
band you were aiming at slid out from under the cursor as you reached for it.

The cause was that every control above the plate changes size as you use it.
The caption gains a name and a figure, the clear chip appears and disappears,
the law toggle changes its wording, the overhead note changes length with the
variant. Each reflowed the block and pushed the drawing down or pulled it up.

Fixed by reserving the space rather than by moving the plate somewhere else: a
minimum height on each strip, `visibility` rather than `display` on the chip so
it keeps its box when hidden, the caption's second clause on its own line so it
cannot rewrap, and the law toggle a block with its explanation under it rather
than text flowing around a button. Nothing about what is said changed; only
that saying it no longer moves the picture.

**Measured, not eyed.** The plate's top edge is sampled before and after every
interaction — each trace kind, the law toggle, all three overhead variants.
First pass left 2.3px on the group and anchor captions, which was the minimum
height being a hair under two lines. Second pass is 0.0px on all eight.

**D-112a · The explorer opens on FY2030.** JW: the law is what the reader came
for; FY2024 is the comparison, not the starting point. The cover headline takes
the FY2030 title with it, which also matches the cover taper's own subject.

**D-112b · The Summary no longer offers the board deck.** It is not published.

**D-113 · A label belongs to the thing it names.** JW, 28 September: selecting
a pie greyed out the name of the service it represents, the provider bar's
name, and the tributary's own amount. The blanket dim reached them because
`txt` and `lbg` drew outside any trace block. They inherit `_h()` now, and the
node labels, the pie captions and the tracker marks' leaders, amounts and names
are drawn inside their own trace context. Raster identical. Context that is not
a competing subject — the HR-1 rule and its zone label — dims to .45 rather
than .1, so it stays readable behind a selection.

**D-113a · The big dots do nothing.** An anchor lit everything upstream of it,
which was true and was not intuitive: rolling across the number line flashed
most of the diagram with no way to tell why. The diamonds and squares stay,
because each names one thing.

**Open, and JW's call.**

*The provider tax tributary terminates in the federal column.* Reported as a
regression; it is not one. `renderproof.py` shows every national panel
raster-identical through this whole session, so the drawing has not moved. The
cause is the declaration: `HR1["Provider tax limits"]` is charged FEDERAL and
reaches FEDERAL, and `reach_slot["FEDERAL"]` is x=350. Every tributary
terminates at the reach it declares — that is the standing rule — so this one
stops where the federal match would have been drawn and never crosses the
page. The other six declare downstream reaches and drop to the HR-1 zone,
which is why it reads as the odd one out. Changing it means changing either
the reach (a claim about where the money would have got to) or the rule that
tributaries terminate at their reach. Both are modelling decisions, not
drawing ones.

*The marker also sits on top of Vaccines on the number line.* `render_v8_0.py`
already reports it: "markers Vaccines / Provider Tax sit 4 units apart on the
line." Moving it is `tracker.assign`'s lattice, and it is the same decision as
above — worth taking once, together.

**D-114 · The explorer is 2.3 MB, and opens on a phone.** JW, 28 September:
link the paper, composite the slides.

It was 7 MB and the Open button did nothing on iOS — no error, just a page
that would not start. The weight was 3.2 MB of base64 PDF and 1.5 MB of slide
screenshots, both added the same day at JW's direction and both a straight
substitution of file size for a link.

The paper is linked to the landing page now; its thumbnail stays, because 148
kB of page one is what makes the block worth looking at. The slides are
composited from `build_deck.CARDS` — kicker, hero and body, styled as slides —
rather than photographed. **What the composite drops is each slide's figure,
and that is the point:** the reader has the live diagram one tab away, drawn
from the same ledger, and it is better than a picture of a picture.

The earlier argument for photographing (D-111: a change to the deck's
stylesheet cannot silently break this page) still holds and is answered
differently — the composite takes the deck's DATA, not its CSS, so there is no
stylesheet to break.

Remaining weight is 805 kB of provision subsets, 553 kB of panels and plates,
and 730 kB of fonts. The subsets are the next thing to cut if it has to get
smaller: they are 127 combinations carrying six figures each.

**D-115 · Two arbitrary numbers doing real damage.** JW, 28 September, and he
was right that I was being pedantic about it.

The provider tax tributary read as stopping nowhere — halfway up the federal
column while the other six drop below the HR-1 rule. I defended that as the
reach rule and it was the wrong defence. The reach is FEDERAL and stays
FEDERAL: that is a claim about how far the dollar gets, and it is right. How
far DOWN the tributary hangs is not a claim about anything. It is layout, and
it should say what the other six say, which is that HR-1 takes this out.
`term_y=560` was pinning it. Released to the solver.

Likewise `src_x`: 66 units into the federal column put the bite at x=226
against the vaccine peel's 218, so the two markers landed on top of each other
on the number line and `render_v8_0.py` had been reporting them 4 units apart
every build. Where a tributary leaves the federal stream is equally arbitrary.
Moved to 140 units in. The warning is gone.

**One declaration for one point.** The band bent at the midpoint of the gap,
x=284, while the tracker put the marker at the declared `src_x`. Two numbers
for one place. `sankey` reads the declaration now — but only where there IS a
bite: reading it unconditionally moved the FY2024 federal band for no reason,
which the renderproof diff caught before it was blessed. Nine FY2030 panels
changed; FY2024 and DC are untouched.

**D-116 · The HTML artifacts are for a screen.** JW, 28 September: the deck's
HTML needed white gutters to display right, and the paper needed the same.

Both are laid out for an 11in landscape sheet, and both ran to the very edge of
the browser window with a sideways scroll. A page is a sheet of paper and has
to read as one, which means seeing space on both sides of it.

Neither sheet can reflow — the layout gates measure them at 11in and the
figures are placed against that — so on a narrower window the sheet is SCALED
rather than cropped. `zoom` rather than `transform`, because zoom reflows the
page height with it and a transform leaves a column of dead space below the
document. Stepped breakpoints rather than a `calc()`, so it behaves the same
in every browser, and each breakpoint allows for the gutter as well as the
sheet — the first attempt sized the sheet to the window and the margins then
pushed it back out.

The paper's rules go in **`publish.py`, inside `@media screen`**, injected
during packaging. They cannot reach the PDF: `render_v8_0.py` prints from the
source before any of this runs. Verified at 1000px and 1500px, no horizontal
scroll at either, all ten figures loading.

**D-117 · The whitepaper's own address.** JW, 28 September:
`https://agilian.com/100MedicaidDollarsProject/Whitepaper`. Both the thumbnail
and the Download button in the explorer's Summary point there. Declared in
`build_explorer.py` beside the file it names, so the two cannot drift; the
landing URL stays in `landing.py` and remains a different thing.

**D-118 · The engine stopped being hand-typed.** 26–27 October.

Two declarations in `engine/explorer_engine.html` were maintained by hand:
`GEOM` and `DATA`. Both are now written by exporters — `geometry_export.py`
rewrites the `const GEOM` line, `engine_data_export.py` rewrites `const DATA` —
and neither is edited directly again.

This was not housekeeping. The hand-typed spine had drifted from
`instances.T_SLOT` in three of seven tracker slots and carried an invented
PROVIDERS slot the lattice does not have, which is what dragged directed
payment caps downstream into the fan and made it cross. Every crossing chased
on 26 October looked like a defect in `_place` and not one of them was. And
because nothing carried a ledger figure to the engine, public-company earnings
could not be drawn at all: the paper draws it, the ledger holds it, the engine
had no way of being told.

`engine_data_export.py` refuses to write if a lane's retention does not equal
its administration plus its margin. A split the ledger does not stand behind is
worse than no split.

**D-119 · `anchorproof.py`, a new gate.** Added after documented fraud was
found leaving from white space below the provider bars — anchored to the bottom
of the bar stack, which is under the river and has gaps in it. A tributary that
does not leave the flow tells the reader the money came from nowhere, and no
other gate looks for it. It caught a second one immediately: the directed
payment caps bite was starting fifteen units above the care body, in the gap
the retention had opened.

A tributary may also leave another tributary — plan administration and
shareholder earnings come out of the retention pool, not out of the hundred
directly — so the ends of tributaries count as ground.

**D-120 · Clearance is measured along the curve.** Contract §10 is rewritten.
Two ribbons cross when the longer one is still high where the shorter one
stops; row order cannot fix that because the order is already right, and the
pin could only move a terminal. `ctrlPair(x0,x1,drop)` front-loads the fall and
`dropFor` derives the drop per ribbon from what that ribbon passes under. All
three panels are at zero crossings with no pin doing the work.

`OUTFLOWS["Blocked senior enrollment rule"].term_dy` was changed from an
absolute `term_y` to an offset below the fan top — the absolute value was only
correct on the one panel it was written for — and the engine now ignores it
entirely (JW, 27 October). The paper still reads it and still needs it. The
renders moved 0.1–1.1px and were re-blessed with that as the reason.

**D-121 · Two detector defects, both found while chasing figures.**
`crossings.envelope` bucketed x at four units while a band samples about every
three, so wide bands left empty buckets and any crossing landing in one was
reported as being out in the margin. Every bucket a band spans is filled now;
the paper is still zero across all five panels. And `ENGINE_BODY` was missing
the engine's own service palette, so the envelope stopped at x=1300 and every
body crossing past it was reported.

**D-122 · `exportproof.py`, a new gate.** 27 October. `GEOM` and `DATA` are
inlined in the engine and written by exporters, and that rule needed a gate or
it was a comment. It re-runs both exporters against a copy of the engine and
compares — it never writes to the tree, so a red gate leaves everything exactly
as it found it — and names the drift: a hand edit to one tracker slot comes
back as `/term_slot/BENEFICIARY: engine 2060.0, export 2180.0`, which is the
exact value that cost most of a session when nothing was watching for it.

The exporters take `EXPORTPROOF_ENGINE` to write somewhere other than the
engine. Nothing else sets it.

**D-123 · A failing test about a published paper lives beside the paper.**
JW, 27 October. `render_v8_0.py` had been honestly red for a month over two
real faults in v8.0 — page 9 strands seven lines, three leaders run through
their labels on `fig6_taper_all.svg`. A permanent red is a ghost: every session
reopens it, re-derives what it means, and concludes what the last session
concluded.

The faults are now written down in `RELEASE_v8.0_KNOWN_FAULTS.md`, which
travels with the paper, and `gates.py` PINS them to their exact extent — one
page over threshold, page 9, seven lines; three leader faults across five
diagrams. Green while that is true, red the moment a fault is fixed, a new one
appears, or a count moves. It is an expectation, not a suppression, and the
expectation is that file.

This is a last-of-its-kind problem. v8.0 is the last paper assembled against a
fixed layout; papers after it are generated from the engine, so a fault of this
class becomes a property of the generator and is fixed once.

---

# Session addendum — 2026-10-29 · the DC payer column, re-based

## What changed in the data

The four comprehensive plans moved off DHCF's CY2023 managed care report and
onto **each plan's own CY2024 Title XIX reporting**. That dissolves the
basis-mismatch workaround rather than patching it: the old split had to anchor
HSCSN separately and apportion the residual, because the comprehensive plans'
total capitation revenue carried locally funded Alliance and ICP enrollees and
HSCSN's did not. On the Title XIX column every plan is on one basis and the
special case disappears.

Not the same line in every statement, and the ledger says which per plan:

| plan | premium | care | administration |
|---|---|---|---|
| AmeriHealth | Title XIX column, as filed | Title XIX column | Title XIX column |
| Wellpoint | Title XIX column, **earned** (net premium less the $30.25M change in unearned reserves) | Title XIX column less reinsurance recoveries | entity lines, apportioned by Title XIX's share of earned revenue |
| MedStar | **Schedule T, DC row** — the entity writes $920.1M of Title XIX across two jurisdictions, $545.0M of it in Maryland | entity Title XIX, apportioned by DC's share of Title XIX premium | as care |
| HSCSN | CY2023, DHCF managed care report | CY2023 | **absent** |

Margin is a residual throughout — premium less care less administration.
Nothing publishes a plan's Medicaid margin directly.

## The mixed vintage, declared

HSCSN is a year behind the other three. JW, 2026-10-29: HSCSN is not really an
MCO — it predates the managed care regulations and its reporting obligations
differ in kind, so there is no comparable annual statement and no Title XIX
column to read. It reports everything to DHCF, and that is the acquisition;
it has not been chased. The strap, the ledger note and the provenance record
all say so.

The MCO LANE's administration and margin stay ABSENT even though three of four
plans now publish theirs. The sum of three is a floor, and a floor is not
published as a total.

## Gate expectations moved

- `coverage.py dc`: **15 unverified / 26 missing → 21 / 20.** Six figures
  acquired. Still **0 verified** — acquiring a figure is not a person opening
  its source and agreeing with it, and no District figure is in the signature
  register.
- `teaching_register.json`, `dc_2024`: 65 → 80 entries. Four strings the panel
  no longer draws were removed; nineteen new ones entered as `pending`. Every
  surviving verdict carried forward unchanged and nothing was upgraded, so the
  burndown is not flattered by a data change (254 ported of 606).

## Still red

`renderproof.py`, in the cloud sandbox only: Google Fonts is blocked there and
the national 2030 panels render on a fallback face. Red on a clean tree too —
verified by stashing. **It should be green on a local machine; if it is not,
that is a real finding.**
