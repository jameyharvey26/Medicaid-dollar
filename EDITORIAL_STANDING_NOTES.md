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
