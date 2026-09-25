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
   Sheila has seen the disclosure wording on the author page.
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

**S-092 remains open.** The draft has been shared with Sheila. Sharing is not review, and the
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
- S-092: Sheila has not yet seen the author-page disclosure wording.

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

**S-092 is closed.** JW, 19 September: Sheila saw the author-page disclosure
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
months) plus CareFirst ($107.4M / $87.7M, three months) summed and given the
successor plan's name. CareFirst's administration is a full year of wind-down
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

## 2026-09-25 — D-78 through D-81, S-106, S-107; Brent's review applied

**Decisions**

- **D-78 · The payer lanes are derived from Exhibit 17 dollars.** They were
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

- **D-79 · Provenance is stamped, not typed.** `release.py` derives the version,
  date and a six-character build id from the content of the figure-bearing
  modules. Cannot come from git: the working copy is a tarball with no `.git`.
  Replaces two typed strings that disagreed with each other by eight days.

- **D-80 · The cover figure is cut.** It was the same file as Figure 1, one page
  later, at a third the size. New cover graphic pending.

- **D-81 · The moratorium labels are renamed.** "Blocked senior enrollment" and
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

**Signatures** — 26 of 36 lapsed under D-78, re-signed 2026-09-25 on
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
