# Editorial Standing Notes
*Append-only. Binding on every cycle. Read before drafting.*

Each note: date, role it attaches to, the rule, and where it came from.
A note stays in force until JW retires it. Notes override the charter where they conflict.

---

## Seeded from the corpus review — 2026-08-18

**S-001 · Author · Every forecast carries a when and a who-first.**
The published chapters never say "this may happen." They say late 2025 / early 2026,
low-income working parents with school-aged children, coverage loss from new work
documentation. Prediction with a date and a named population is the firm's differentiator.
*Source: Ch. 5 impact table; Ch. 1 four-month FMAP call.*

**S-002 · Author · The firm takes a position.**
"We are advising our clients to plan for a $60B reduction." Hedged, position-free analysis
is off-brand even when it is safer.
*Source: Ch. 1.*

**S-003 · Author · Non-partisan on motive, unflinching on consequence.**
Describe the mechanism and the cost. Do not editorialize on whether the people doing it are
bad. The 2025 chapters hold this line under real provocation; hold it.
*Source: whole corpus; explicitly claimed as "non-partisan analysis" in the exec summary.*

**S-004 · Author · Human cost gets one clean line, then back to operations.**
"Even though the money never gets to the beneficiaries, the care does." Not a paragraph of
sentiment. One line that lands, then the operational consequence.
*Source: Ch. 4 Harvey quote.*

**S-005 · Copy Editor · No em-dashes in new material.**
JW ruling, 2026-08-18. Supersedes corpus practice, which uses them heavily. Legacy chapters
are not retroactively edited.

**S-006 · Copy Editor · No "it's not X, it's Y" construction, or its variants.**
JW ruling, 2026-08-18.

**S-007 · Copy Editor · No emoji in body text.**
JW ruling, 2026-08-18. Chapter 5's traffic-light probability key is legitimate data
encoding, but the designer renders it as colored shapes with a printed legend, not glyphs.

**S-008 · Copy Editor · Structural repetition is the primary AI tell in this house.**
The OBBBA Action Edition plan reads as machine output because eighteen chapters share
identical Equity Lens text, identical learning objectives, and identical three-phase actions
with only the date changed. If two sections could be swapped without a reader noticing, the
piece goes back to the Author.
*Source: 20250724_Medicaid Playbook Chapter Plans_post-OBBBA.docx.*

**S-009 · Copy Editor · Equity language must carry content.**
On-brand when it names who is affected, how, and what to do. Off-brand as a recurring
section stub. The brand is genuinely justice-driven; ritual undercuts that.

**S-010 · Research Editor · Every footnote points at the document containing the claim.**
Chapter 3 has at least two mismatches: a Guttmacher attribution resolving to a KFF
dashboard, and a CMS health-equity page cited for administrative-procedure timing. Do not
inherit the pattern. Verify each link live.

**S-011 · Research Editor · Re-verify anything with a date on it.**
Statutory deadlines, FMAP figures, enrollment counts, and bill status all decay. Trust
nothing dated before the current session without a fresh check.

**S-012 · Author + Research · Modeled and measured are labeled, always.**
In this firm's voice, flagging a modeled figure is a credibility asset, not a weakness.
Every modeled value is flagged in prose and on the artifact.
*Source: project ledger discipline; DC build convention.*

**S-013 · Author · Never mix denominators.**
A benefits figure over a total-outlays figure is a mixed-basis result and is wrong. State
the basis for every ratio.
*Source: standing project principle.*

**S-014 · Designer · Blue carries 85–90% of every layout. Orange is 1–3 words.**
Orange never behind white text. Orange never in body copy.
*Source: 2025 Brand Guidelines, p. 19 and p. 24.*

**S-015 · Designer · Two type stacks, chosen by output format.**
Jost/Nunito for designed collateral. Century Gothic Bold/Aptos for Microsoft and Google
documents. Do not mix.
*Source: 2025 Brand Guidelines, pp. 21–22.*

**S-016 · Production Manager · Do not summarize the piece back to JW.**
JW will read it. The report covers what changed, what is open, and what should become a
standing note.

**S-017 · All · Brevity beats completeness for this audience.**
Senior decision-makers. When a cut and a caveat compete, cut.

---

## Added in review

*(New notes append below, most recent last. Promotion rule: any correction JW makes twice
gets written here automatically.)*

## Added in review — 2026-08-18 kickoff

**S-018 · Production Manager · GitHub push reminders are event-triggered, not scheduled.**
Remind JW to push when: a renderer or build script changes; a whitepaper section reaches
approved-final; the standing notes gain three or more entries; or a working session ends
with new files in outputs. The reminder comes at the point of change, so it arrives when
there is actually something to save.
*Pending JW approval.*

**S-019 · Designer · Grayscale proofing happens on the raster, never in the SVG.**
`cairosvg` silently ignores `feColorMatrix`, the same class of gotcha as its `paint-order`
failure. Convert the rendered PNG with Pillow instead. Every diagram gets a grayscale check
before it ships, because the deliverable is print.

**S-020 · Designer · Run `audit_state_palette()` before any state build; refuse to render on
an unresolved collision.**
Matches the seven balance checks' behaviour. The audit caught three collisions at kickoff
that were invisible by eye. Ten mutually distinct colours per family is not achievable at
professional saturation — the floor is real, and per-state auditing is what makes the
reserved scheme work.

**S-021 · Designer · Cool = money moving. Warm = money stopping. No exceptions.**
A payer colour drifting into magenta breaks the reader's core legend. Health-system violets
are bounded at hue 288 for exactly this reason.

**S-022 · All · Colours live in `palette.py` and nowhere else.**
Both renderers import it. One place to change a colour; the state series inherits
automatically. Same principle as `inputs.json`.

**S-023 · Research · CBO's behavioural assumptions are already inside its estimates.**
Do not layer an additional state-backfill multiplier on top of CBO provision totals. Check
whether a behavioural response is already priced before modelling it separately.

**S-024 · Author · Never introduce current reported actuals as "old data."**
FY2024 is the most recent complete fiscal year in the February 2026 MACStats. The honest
caveat is mixed vintages inside a composite, not age. Understating the currency of the
baseline undercuts the argument that rests on it.

## Added in review — 2026-08-27 layer session

**S-025 · All · Four layers, and they are separable in that order.**
DATA (ledger values) → LOGIC (what nodes exist, how dollars route) → ENCODING (which
visual property signals which category) → STYLE (palette, type, scale, viewBox, margins).

STYLE swaps freely without touching anything upstream. ENCODING moves *with* LOGIC, because
it carries meaning: if the logic introduces a node type, the encoding must grow a signal for
it. This is why "revert the style but keep the business logic" was not directly executable
in August — the new logic had created node types the old palette had no vocabulary for.

The two-way independence JW originally proposed holds for STYLE↔LOGIC. It does not hold for
ENCODING↔LOGIC. Say which of the four you mean before agreeing that a change is "just
presentation."

**S-026 · Designer · Warm means HR-1 did this. It does not mean money stopped.**
Amends S-021 and D-14. Under the original rule, warm marked any dollar that stopped, which
put warm inside the FY2024 baseline where no policy loss exists. The baseline has ordinary
leakage — plan administration, cost sharing, uncompensated care — and rendering that warm
made the 2024 and HR-1 diagrams non-comparable.

Current rule:
- Baseline leakage renders as **ghosted source colour**: the lane's own hue at ~0.16
  fill-opacity, dashed stroke, hollow destination node. The stopped dollar keeps its lane
  colour, so the reader can still trace which lane it left. Peels **upward**.
- HR-1 attributable loss renders **warm (#8B5A5A) plus texture**, per D-15. Peels
  **downward**.

Direction and hue both separate the two classes. The overlay reads as something pulling out
the bottom of the model rather than competing with baseline leakage for the top.

Retained from S-021: no baseline flow is ever warm. Dropped from S-021: the claim that all
stopped money is warm.

Known cost of ghosting: ghosted teal and ghosted slate converge in greyscale. If a baseline
diagram must survive monochrome print, apply the D-15 textures to the ghosted bands at low
opacity — lane hue and print survivability are not mutually exclusive.

**S-027 · Designer · One model, three files, identical viewBox.**
Every geography emits `<name>_combined.svg`, `<name>_baseline.svg`, and
`<name>_overlay_hr1.svg` from a single script run. All three carry the same viewBox and the
same coordinates. The singles register when composited because the renderer wrote all three,
not because anyone aligned them.

Structure inside the document:
```
<g id="baseline">      always drawn
<g id="overlay-hr1">   display="none" in the baseline file
<g id="furniture">     headers, balance line, legend
```

Which file goes where: `_combined` for web and slides, where toggling one `display`
attribute gives a live before/after. `_baseline` and `_overlay_hr1` for OmniGraffle,
Illustrator, and print, where the overlay is placed as its own layer.

Circulation rule: `_baseline` is the file that leaves the building. It contains no HR-1
content at all, so unpublished provision estimates cannot escape by someone flipping an
attribute in a file we sent out.

SVG caveat, recorded so it is not rediscovered: SVG has no native layer concept. OmniGraffle
imports `<g>` as a group, not a layer — selectable, hideable, lockable, but not in the layer
palette without one manual promotion. This is why the separate-file emit exists alongside
the combined one.

**S-028 · Designer · resvg is the renderer. cairosvg is not a fallback.**
cairosvg ignores `paint-order="stroke"` and paints the halo stroke over the glyph instead of
behind it, which erodes letterforms from the outside in. It is worst on the pie percentage
labels at 10–11px, which is where it gets reported as "the pies are blurry again."

This has now recurred repeatedly, because every fresh container ships with cairosvg present
and resvg absent, so the next person to render reaches for what is installed.

The build script owns the render step and pins `resvg_py`. If resvg is missing it must fail
loudly, never silently fall back to cairosvg. Minimum output width 2600px for the national
master. Blurry pies should become impossible rather than merely unlikely.

**S-029 · Research · The $10 is not decomposed, and nothing downstream can be drawn until it is.**
D-01 sets $100 as the 2028 prior-law counterfactual with HR-1 flows summing to roughly $90.
As of this session no file in the repo contains a provision-level figure for the missing
$10. `build_sankey.py` holds the FY2024 baseline only.

Forks 1–3 are multiplication rates (26%, ~70/20, ~80/20). They have nothing to multiply
until each in-scope provision has a dollar contribution per $100 in FY2028 and a flag for
whether it is coverage-loss or financing — Fork 1 applies only to the former, per D-18.

Blocked on that single table: the Section IV master with gaps, the Section VI six-provider ×
five-destination fan-out (D-04), the 20/26/35% sensitivity variants (D-18), and the
provision decomposition with its interaction-adjustment line (D-09). One input, four
diagrams.

Do not draw any of them from estimated provision splits. A conserved ledger that balances
against invented components is worse than no diagram, because it looks audited.

**S-030 · All · The repo is `JameyHarvey26/Medicaid-dollar`, branch `main`.**
Recorded because a session was lost to `JameyHarvey/...`, which 404s. Verify against a
tarball fetch (`codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/main`) rather than a
raw file URL — raw 404s identically for private repo, wrong branch, and absent file, so it
cannot tell you which problem you have.

**S-031 · All · Project Files are not the source of truth and drift silently.**
This session found the Project Files copy of `EDITORIAL_STANDING_NOTES.md` short by 38 lines
against the repo — missing the entire kickoff review section from S-018 onward. Reading the
stale copy produced a confidently wrong claim that the editorial team had never made diagram
design decisions, when D-13 through D-15 had done exactly that.

At session start, diff Project Files against a fresh repo pull before reasoning from either.
Where they disagree, the repo wins.

**S-032 · Research · D-06's fork table contradicts D-18 and has not been reconciled.**
D-06 still marks Fork 1 **OPEN**. D-18 resolves it at a 26% central case from the Oregon
HIE, with sensitivity at 20% and 35%. D-18 is later and governing; the D-06 table was never
updated.

Correct the table in `WHITEPAPER_BRIEF.md` rather than carrying two answers. General rule:
when a later decision resolves an earlier one, amend the earlier entry in place and note the
superseding decision number, so the brief has one answer per question.
