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

## Added in review — 2026-08-27 second session (financing / FMAP)

**S-018 AMENDED · Commits happen at session close, not at mid-session thresholds.**
JW ruling, 2026-08-27. The original note fired a reminder at events: a renderer
change, an approved-final section, three new standing notes, or new files in outputs.
Those events still define what belongs in a commit; they no longer trigger one.

The risk this creates, recorded so it is not rediscovered: reconstructing a session's
decisions at the end is harder than it looks, and this project has already lost work
that way. Mitigation is a **running commit manifest** maintained through the session
and updated as each decision lands, so the close-of-session write is mechanical
rather than a recall exercise. If the manifest is not being kept, the reminder rule
reverts.

**S-033 · All · Plain-language label leads, section number follows.**
Every HR-1 provision is named by what it does. The section number appears in
parentheses at first use within each section of the paper, and in endnotes,
methodology, and the crosswalk. It never leads a sentence, never appears in a
heading, and never stands alone as a lane identifier. Diagram labels carry the plain
label only, with numbers in a footnote block beneath.

Origin: JW, on reading a draft written in section numbers. CBO scores in section
numbers, and letting the source's filing system become the paper's vocabulary makes
the reader do translation the author should have done. This is S-018's
stakeholder-differentiated principle applied to language rather than to dollars.

Extends to statutory versus industry terminology. The audience's term leads; the
statutory term is glossed once at first use. "Community engagement requirement" is
glossed under "work reporting," not the reverse.

Approved lane labels:

| Label | Section | What it does |
|---|---|---|
| Work reporting | §71119 | 80 hrs/month reporting for expansion adults |
| Six-month renewals | §71107 | Expansion adults renew twice yearly |
| Provider tax limits | §71115 | Caps state taxes on providers |
| Directed payment caps | §71116 | Ratchets MCO supplemental payments toward Medicare |
| Blocked senior enrollment rule | §71101 | Blocks 2023 MSP auto-enrollment rule |
| Blocked Medicaid enrollment rule | §71102 | Blocks 2024 E&E streamlining rule |
| Everything else | — | Cost sharing, immigrant eligibility, retroactive coverage, minor items, plus CBO's interaction netting |

The two "Blocked" labels were disambiguated because they render as adjacent bands.
Also note both are *preserved friction* per D-38: nobody loses coverage, but rules
that would have lowered barriers are blocked. That mechanism needs a sentence at
first appearance in Section IV, not just a label. It is one dollar in five at 2029
and a label alone will read as a bureaucratic footnote.

**S-034 · Research · Medians do not aggregate. Check which one a published share is.**
Caught in the second-ledger sourcing. KFF's 2025 Medicaid Budget Survey reports
non-federal share composition as **state medians** (70/18/6, summing to 94). GAO's
SFY2018 figures are a **national aggregate** (68/17/12/4, summing to 101 on
rounding). Only the aggregate can open a conserved ledger. The median is a currency
check confirming the aggregate has not structurally drifted.

Both were tempting because the KFF figure is eight years more current. Using it
would have produced a ledger that could not conserve and a national claim assembled
from state midpoints. Generalisation: before adopting any published share, establish
whether it is an aggregate, a median, or a mean across units, and never mix them in
one denominator. Related to S-013 but distinct: S-013 is about mixed denominators,
this is about mixed estimators on the same denominator.

**S-035 · Research · An unsourced split is `None`, never a plausible number.**
`financing.py` sets `SDP_PROVIDER_TAX_VS_IGT_SPLIT = None` so that any attempt to
render D-41 fails loudly. A plausible placeholder would have balanced and looked
audited, which S-029 identifies as worse than no diagram. Applies to every input
that is genuinely unknown rather than merely modelled: modelled values get a value
and a flag, unknown values get `None` and a hard stop.

## Added in review — 2026-08-27 second session, part 2 (FMAP, basis, second ledger)

**S-036 · All · Recommend on methodology, ask on direction.**
Amends the one-question-at-a-time working rule. Where the call is technical and
Claude has a defensible view, Claude leads with the recommendation and the
reasoning; JW confirms or overrides. Where the call is about what the paper argues,
who it is for, what ships, or anything where Claude's view would substitute for
JW's judgement, Claude asks without a recommendation.

Origin: JW, mid-session, after several consecutive methodological questions were
put to him as open menus. The failure mode this closes is asking as a way of
avoiding a position. One-question-at-a-time still governs; it now governs the
questions that are actually JW's to answer.

Rough line: methodology Claude recommends, editorial direction JW decides.

**S-037 · Research · CBO's section-level narrative uses inconsistent basis language;
check the sum, not the wording.**
In the October 2025 supplemental, six of seven Medicaid sections are described as
decreasing *deficits* and one (71116) as decreasing *federal outlays*. That reads
like a mixed basis and is not. The seven section figures sum to $886.8B, the chapter
DEFICIT total, exactly. Section 71116 has no coverage effect by CBO's own finding,
so its outlay and deficit figures are identical and both descriptions are accurate.

Generalisation: when a source's section-level wording is ambiguous about basis, the
arithmetic against the published total settles it. Do not infer basis from the verb.

**S-038 · Encoding · A lane exempt from the gross-up must not be width-comparable to
lanes that carry it.**
After D-39 and D-41, two lanes (71115, 71116) carry no total-computable band while
five do. That is $332.1B of $886.8B in federal dollars, over a third of the overlay,
drawn on a different basis from its neighbours. Band width is the diagram's primary
encoding, so two adjacent lanes measuring different things is the S-029 failure:
balances, still lies. The encoding layer must make the difference legible before
this renders. Open at the close of this session.

**S-039 · Encoding · An unsized container must not read as a scaled band.**
Per D-47 the state general fund renders as an unsized container around the state
node. Because it carries no scale, a reader will eyeball it against the $100 and
infer a ratio the paper never claimed. It must be visibly a different object from
the Sankey around it: different stroke treatment, no fill that invites width
comparison, and flows crossing its boundary annotated with explicit figures rather
than drawn proportionally. This is an ENCODING-layer rule under D-27's four-layer
split, not a data-layer one.

## Added in review — 2026-08-27, part 3 (framework architecture, overlay encoding)

**S-038 RESOLVED by D-49, and its premise was wrong twice.**
The note said two *lanes* were drawn on a different *basis*. Both halves were wrong:
D-46 had already made the exemption a property of a slice rather than a lane, and the
exempt slices are not on a different basis at all — the federal match is a
total-computable figure. The real difference is composition, and it encodes as an
internal partition rather than as a special treatment for the minority. Corrected
exempt block: $284.7B / 32.1%, not $332.1B / 37.4%.

Generalisation worth keeping: when a note frames something as an incommensurability,
check whether the two things are actually incommensurable before designing around it.
Every fix aimed at the wrong diagnosis here would have encoded a false claim.

**S-039 RESOLVED by D-52.** Open edge, no fill, fixed-width crossings.

**S-040 · All · Look at the current render before designing anything.**
This session designed a layout from scratch across three iterations before JW supplied
`national_baseline.png`, which is the diagram he had been picturing throughout. The
existing render answered questions that were instead put to him as open ones — most
visibly the unit, which the artifact states plainly as dollars per $100.

`build_sankey.py` reproduces it exactly in one command. There was no obstacle other
than not thinking to run it. **First action of any diagram session: run the build and
look at the output.**

**S-041 · Build · The render must land in the repo, not only in outputs.**
Root cause of S-040. `build_sankey.py` writes to `/mnt/user-data/outputs` and nothing
carries the PNGs back, so the current picture of the project exists on JW's machine
and nowhere a session can reach it. Precedent exists for committing renders —
`dc_preview.png` and both palette renders are already tracked.

Fix at the script, not the commit: `build_sankey.py` should copy its renders into the
repo on every run, so a stale reference render becomes impossible rather than merely
unlikely.

**S-042 · Designer · Loss direction is the master's existing grammar, not a new rule.**
The baseline already peels leakage **upward** in grey with the figure labelled above
the peel — Medicare premiums, administration, plan administration, public-company
earnings, documented fraud. S-026's warm-peels-downward rule is therefore a mirror of
an established convention, and the empty canvas below the flow is where the HR-1
overlay goes. Grey up is money the system always lost; warm down is money HR-1 took.

**S-043 · Author · Every figure on the to-be is modelled, including the ordinary ones.**
The as-is is FY2024 actuals. The to-be is a projection of prior law with FY2024
structure held constant (D-11), so the beneficiary pie shares, the payer split and the
provider nodes are all modelled even though they look like plain baseline numbers. The
flag belongs to the whole diagram, not only to the overlay bands, or the to-be borrows
the as-is's authority.

**S-044 · All · A stale in-place entry will be read back as a decision.**
JW specified the architecture at a 2028 anchor. The 2029 amendment (D-22, D-23) had
been recorded only in the 2026-08-27 append while `WHITEPAPER_BRIEF.md`'s D-01 still
read 2028. This is S-032's failure mode reaching the principal rather than the
assistant: the brief carried two answers and the wrong one surfaced.

D-01 is now amended in place. Reinforces S-032's general rule and raises its priority:
amend the earlier entry when a later decision supersedes it, in the same session,
because the append file is not what gets read later.

**S-045 · All · Reference renders belong in the repo, or they get re-explained.**
Three times in one session JW had to supply or describe something that existed only
outside the repo: the national baseline render, the overlay grammar schematic, and the
2029 anchor (which was in an append but stale in the brief). Each gap produced work
aimed at the wrong target — a from-scratch layout, a flat bar chart, and a withdrawn
decision (D-51).

The pattern is not forgetfulness, it is that **the picture of the project lives in
JW's head and on his machine, and the repo holds only the code that makes part of it.**
Fix is mechanical, not conversational:

- Every reference render JW works from goes in the repo (S-041 covers the build
  output; this extends it to schematics and hand sketches).
- A design decision is not recorded until it is in `WHITEPAPER_BRIEF.md` or an append
  *and* the superseded entry is amended in place (S-032, S-044).
- When JW has to explain something a second time, that is the signal it was never
  written down. Write it down before continuing.

**S-046 · Designer · The baseline's grammar is the specification.**
Before designing any new diagram element, read what the master already does and mirror
it. The overlay's entire grammar — ribbon leaves a lane, travels, terminates in a small
labelled node beyond a divider rule — was already on the page as upward leakage.
It did not need inventing, only reflecting. Two wrong objects were built this session
by designing from first principles instead of from the existing render.

**S-047 · All · Tense is load-bearing on the to-be.**
The overlay is a projection to 2029. Past-tense copy ("cut," "lost," "was removed")
asserts that something has happened. Future tense throughout the to-be instance
(D-56), paired with the whole-diagram modelled flag (S-043).

**S-048 · Designer · When encodings compete for one channel, remove one.**
Three systems wanted texture: lane identity, destination identity, non-federal share.
The instinct to partition more finely (D-51) made it worse. The fix was noticing that
lane identity was already carried redundantly by the terminal node label, and dropping
it. Ask what is already carried elsewhere before adding a distinction.

**S-049 · Research Editor · The anchor year is a dependency, not a decision.**
The brief recorded 2029 as a decision (D-01, D-22, D-23) with a stated rationale —
first full-effect year. Neither the rationale nor the year had been checked against
the statute's phase-in schedule or against what CBO actually publishes. A decision
whose validity rests on external data is a dependency, and must be recorded with the
source that would confirm or break it. See D-59 to D-62.

Test to apply: if the answer would change when a government document is read, it is
not settled. Write it as provisional and name the document.

**S-050 · Research Editor · Check that a vintage exists before relying on its contents.**
This session asserted that CBO's Medicaid baseline detail would convert modelled
to-be structure into sourced values, reasoning from the June 2024 file. There is no
January 2025 Medicaid detail file (D-61) — the series skips from June 2024 to February
2026, uniquely among the programs in that series. The claim was withdrawn.

Establish that the specific vintage exists before describing what it contains. Series
have gaps, and the gap is not always where you expect it.

## Added in review — 2026-08-29 (audience, and the conservation defect)

**S-051 · All · The reader arrives as a role, and reads one node.**
JW ruling, 2026-08-29. Recorded because it is fundamental to the project and had
never been written down, which is why the first to-be render missed it.

The audience has closed the books on FY2024. They do not need to be told what
happened; they lived it. A state Medicaid director knows what FY2024 cost the
state. An MCO plan president knows what the margin was. A health system CEO knows
what Medicaid did to the payer mix. That lived experience is the anchor, and it is
concrete in a way no projection can be.

What they do not know is what FY2030 will do **to them specifically**. They have
heard national rules of thumb from talking heads. None of it is customised, and
none of it explains the mechanism.

Consequences that bind every artifact:

- Every reader must be able to find their own node, read the change at that node,
  and understand which lever caused it. A diagram that only balances nationally
  has failed this test even if every figure is right.
- The unit of analysis is the role, not the provision. Section IV may walk the
  levers; the diagram must let a role walk itself.
- "The ecosystem will be poorer" is the thing everyone already knows and is
  therefore worth nothing. **How much poorer, at my node, and why** is the paper.
- Cost growth belongs in the frame. Margins compress from both ends: payment
  falls relative to plan, and unit costs rise. A diagram showing only the payment
  side understates what the reader will actually experience, and they will notice.

Named roles to hold in mind: federal government, state legislature / budget
office, state Medicaid agency, managed care plan, fee-for-service provider
(hospital, nursing facility, physician practice, behavioral health), and
beneficiary. Stakeholder-differentiated analysis is the house frame; this note
names who the stakeholders are.

**S-052 · Designer · An overlay that does not narrow the flow is not conserved.**
Origin: JW, 2026-08-29, on the first FY2030 render.

The overlay was drawn as warm ribbons peeling off the bottom edge into labelled
terminal nodes, with the baseline geometry left at full width. That is annotation,
not a ledger. It shows $86.27 of services delivered **and** $10.26 removed, from a
$100 that never got smaller. The reader is asked to believe the same dollar did
both. S-029's warning applies in its exact form: it balances, and still lies.

Rule: every lever takes its bite out of the flow at its bite point, and everything
downstream of that bite is drawn narrower. The terminal node receives the bite; it
does not receive a copy of it. Health services delivered must fall.

Corollary worth carrying separately, because it is a finding and not a fix: when
the trunk narrows, fixed costs do not narrow with it. Administration and plan
administration are substantially fixed. If they are held at their FY2024 dollar
values while the trunk shrinks, their SHARE rises and services absorb the entire
reduction. If they are held at their FY2024 RATES, the diagram quietly assumes
overhead scales down with the program, which is the more flattering assumption and
almost certainly the wrong one. This choice must be made explicitly, stated on the
artifact, and is a live question for the paper rather than a modelling detail.

**D-63 · Split overhead is the standing assumption on the to-be.**
JW ruling, 2026-08-29. Supersedes the implicit reading of D-11 that all structure
holds at FY2024 RATES, which was never a considered choice because nothing was
shrinking when D-11 was written.

- **Plan administration SCALES with capitation.** Not a behavioural assumption.
  MCO administration is a residual inside an actuarially sound rate and is bounded
  by the medical loss ratio floor at 42 CFR 438.8, which requires states to set
  rates so plans reach at least 85 percent medical spend. Admin load is struck as
  a percentage of premium, so it falls with the premium by construction.
- **State administration HOLDS at FY2024 dollars.** HR-1 pushes this line up, not
  down: six-month renewals double renewal volume for the expansion group, and
  work reporting adds a monthly compliance determination with verification,
  notice and a 30-day cure period. CMS appropriated $200M in FY2026 Government
  Efficiency Grants because states cannot absorb the systems build. Holding it
  flat is already the generous assumption; scaling it down asserts the opposite
  of what the statute does.

Sensitivity retained, not published as alternatives: overhead holds throughout
gives $77.28 delivered, overhead scales throughout gives $77.85, split gives
$77.79. Full spread $0.57 on a $10.26 reduction, five and a half percent of the cut.

*Corrected 2026-09-03.* This paragraph read $77.91 and a $0.63 spread from
2026-08-29 until 2026-09-03. The build has never produced $77.91:
`ledger_2030.ledger("scales")` returns 77.8498, confirmed by an independent
recomputation from `tobe2030.per100` and the FY2024 base that reproduces all three
variants to four places. The origin of $77.91 could not be reconstructed and is not
guessed at here. Holds and split were correct as written and are unchanged. The
ruling itself is unaffected, and the narrower spread strengthens rather than weakens
the conclusion below.

**Consequence for the methodology, and it is the useful part:** the overhead
assumption is not load-bearing. One line says so and nobody needs to litigate it.
Every variant is conservative in the same direction, since more overhead
shrinkage means more money reaching services, so the paper cannot be accused of
stacking the deck here.

**S-053 · Author · The margin story is not in this ledger, and must not appear to be.**
Every variant holds unit costs flat, because HR-1's score says nothing about them.
A health system reading the to-be sees its bar fall from $18.66 to $16.83 and is
also paying more for labour and supplies than in FY2024. The second effect is
plausibly larger than the first and is entirely outside the conserved ledger.
Cost growth needs its own sourcing and its own artifact. Do not let the Sankey
imply it has been accounted for.

**S-054 · Research Editor · Every figure on an artifact has a numbered endnote before it ships.**
JW, 2026-08-29: the diagrams publish inside a written piece, so a reader who wants
to check a number must be able to look it up. This had not been happening. Figure
provenance was scattered across `SOURCES.md` (documents, not figures), code
comments in `tobe2030.py` and `phasein.py`, and the standing notes. None of it was
numbered, and none of it was keyed to anything a reader sees.

`ENDNOTES.md` is now the register. Rules:

- One entry per figure that appears on an artifact, numbered EN-n, append-only and
  stably numbered. If a figure changes, amend the entry in place and cite the
  superseding decision (S-032). Never renumber.
- Each entry carries the claim as the reader sees it, source, vintage, basis, and a
  status of measured / derived / modelled / OPEN.
- OPEN means not yet sourced. An OPEN figure must not be published as stated, and
  the entry says what is wrong with it.
- The register is written as the figure is produced, not reconstructed at the end.
  Reconstructing provenance is the same failure mode S-018's running manifest
  exists to prevent.

Test to apply: an MCO president reads $3.47 on the diagram, wants to know why it is
not $3.81, and follows one number to one entry that answers it. If they cannot, the
artifact is not ready.

**S-055 · Designer · Every outflow is a tributary. It leaves the river going downstream.**
JW ruling, 2026-08-29, with a marked-up render. **This governs all outflows on
every artifact in the project, baseline and overlay, national and state.**

The rule, in one line: **an outflow departs the flow at its bite point and
terminates in a node to the RIGHT of that point.** It never travels backward, it
never drops straight down, and it never floats detached from the band it left.

This is how a Sankey works and it is what the baseline already did. The FY2024
master peels administration, plan administration and public-company earnings as
tributaries curving up and to the right into labelled terminals downstream. That
convention carries the reader's eye in one direction and makes the diagram cohere.

The first FY2030 overlay broke it in four ways and the diagram lost its shape:

- Provider tax limits departed the federal band and ran **left** into the margin.
- Four state-agency levers terminated **left of** where they departed, so the
  ribbons ran upstream.
- Directed payment caps dropped **straight down** as a vertical line with no
  horizontal run, reading as a dropped thread rather than a flow.
- Medical cost inflation floated **detached** from the band it was leaving.

The Medicare premiums arrow is a fifth case, pre-existing and inherited: it runs
right to left back to the federal government. Semantically defensible, graphically
the same error. It becomes a downstream tributary and the label carries the
"back to the federal government" meaning instead of the geometry.

Direction still distinguishes the two classes, per S-026 and S-042:
**ordinary leakage peels up and to the right; HR-1 loss peels down and to the
right.** Up versus down carries the class. Left to right is not negotiable for
either.

Corollary: if a mechanism seems to demand a backward or vertical flow, the label
carries the mechanism and the geometry stays downstream. Never the reverse.

**S-056 · Designer · A subtraction that does not narrow the river is not a subtraction.**
JW, 2026-08-29, on the tributary-corrected render. S-052 established that the
levers must reduce the flow. It did not say *where*, and the build satisfied it
arithmetically while failing it visually: the trunk was drawn at full width across
the whole state agency column and the entire HR-1 reduction resolved as one cliff
at the column edge. The ribbons left in the right direction from the right phase,
and the river never got thinner.

Rule: **the flow steps down at each individual bite, at that bite's own x
position, in ledger order.** One step per lever. The reader watches the river
narrow seven times between the federal band and the provider bars, and can stop at
any step and read what was taken there.

Mechanics, so this is reproducible:
- **Ordinary leakage steps the TOP edge down.** Administration and Medicare
  premiums already did this and are unchanged.
- **HR-1 steps the BOTTOM edge up.** Same edge the warm tributaries leave from, so
  the step and the tributary are the same event drawn once.
- Where a lever removes part of a stacked band rather than the whole trunk, the
  bands below it slide up and the outer edge moves. Provider tax limits narrows
  the federal band, the state band slides up, and the combined bottom edge rises
  by the amount taken.

Test to apply: cover everything right of any x on the diagram. The width of the
river at that x must equal the running balance on the tracker below it. If it does
not, the diagram is telling a different story from the ledger.

**S-057 · Designer · A tributary leaves flush with the edge it comes from.**
JW, 2026-08-29. The stepped build drew each warm ribbon starting at the pre-step
bottom edge and extending downward by its own thickness, so every tributary began
one band-width below the river and read as detached. The slice must span
(edge minus thickness) to (edge), so the ribbon and the step are the same pixels.
Same rule for any future outflow, warm or grey.

Second half, from the same review: **a terminal must sit downstream of its bite.**
Blocked senior enrollment bit at x 664 and terminated at 624, which is backward and
is S-055 all over again in a build that was supposed to have fixed it. When
terminal positions are laid out, check each one against its own bite x, not against
the general left-to-right feel of the row.

**S-058 · Research · Normalising to $100 divides inflation out. Do not put it back.**
JW's question, 2026-08-29, and the answer reversed a figure built one turn earlier.
Every per-$100 artifact in this project is an index, not an amount of money.
Anything that scales numerator and denominator equally, price growth above all,
cancels and is simply absent. It is therefore not hiding upstream, and it cannot be
subtracted downstream.

The trap is specific and it caught this project once: a real-world effect the
audience genuinely feels, which the normalisation has legitimately removed, looks
like a gap in the diagram and invites putting it back. Doing so applies a price
level to an index number, which is S-013.

Rule: before adding any quantity to a per-$100 artifact, ask whether it scales the
numerator and the denominator together. If it does, it does not belong on the
diagram at any position. If a version of it does belong, it is a RATIO of two
growth rates, never a level, and it needs both rates on a like-for-like basis.

**S-059 · Author · Prose gets written when the finding lands, not at drafting time.**
JW, 2026-08-29, asking for the normalisation finding to be worked into the paper.
There was no paper to work it into: the repo held the brief, four appends, standing
notes and endnotes, and not one line of publication-voice text. Every finding so
far exists only as a decision record, which means drafting will be a reconstruction
exercise and reconstruction is how this project has lost work before (S-018).

`PAPER_PASSAGES.md` is now the register. Same discipline as the endnotes: when a
finding is settled, the passage that carries it to the reader is written then, in
voice, tagged with the section it belongs to. Numbered P-nn, append-only.

This is not drafting the paper. It is refusing to let the paper start from zero.

**S-060 · Designer · The balance tracker is shared furniture. Its geometry does not move.**
JW, 2026-08-29: the FY2030 money line had drifted out of alignment with the columns
above it and out of harmony with the FY2024 master.

The FY2024 tracker is not laid out by eye. **Checkpoints sit on column boundaries**
and **deltas sit between them**: $100 at 560 where the federal and state dollars
combine at the state agency, disbursed at 820, claims paid at 1300, health services
delivered at 1560. Deltas at 690, 1060 and 1430. Type is 36px on the values, 25px
on the labels, 24px on the deltas, r=11 on the nodes.

Because the two diagrams are a pair read side by side, **every one of those numbers
is fixed across every instance**, national and state, as-is and to-be. A reader
tracking the same checkpoint between the two diagrams must find it in the same
place. Any geography or year that needs a checkpoint the master does not have puts
the extra information in the delta, never by moving or adding a node.

The FY2030 instance adds one thing the master does not have: HR-1 deltas alongside
ordinary leakage. Both rows sit **above** the line, HR-1 over ordinary, so the
checkpoint labels below keep the master's clear band. Direction carries class here
as it does on the flow.

**S-061 · Designer · Tracker subtractions are charged to their column, right aligned.**
JW, 2026-08-29. A subtraction on the tracker sits under the column where the money
actually leaves the flow, right aligned to that column's right edge, with a
plain-language label beneath the figure. The reader can then drop a vertical line
from any outflow on the diagram straight down to its number. Centred deltas floating
between checkpoints carried no information about where the money went.

Colour is fixed and is not a per-diagram choice: line, dots and checkpoint values
BLACK; ordinary subtractions GREY above the line; HR-1 subtractions warm #8B5A5A
below the line. Red stays on the flow for fraud and never appears on the tracker.

**S-062 · Designer · Medicare premiums is the only sanctioned return flow.**
It peels flush off the top edge like any other ordinary outflow, then curves back
to the federal lane with an arrowhead, because the money genuinely returns to the
federal government. Declared `ret=True` in `outflows.py`. No other outflow may
travel backward, and a new one may only do so if the money really goes back.

The deeper fix is the ledger itself: `outflows.py` now declares every outflow's
source column, source edge and terminal column once, and both builders read it.
Medicare premiums had drifted into two different treatments in two builders and
nobody caught it for three sessions, which is what happens when geometry is written
twice.

**S-063 · All · STYLE_GUIDE.md is the standing answer to "why did that drift".**
The last several rounds of corrections were all one correction: rules that existed
in JW's head, or in a single note, and were not written where the work happens.
`STYLE_GUIDE.md` collects them. A render that violates it is a defect, not a
preference, and none of those rules should need to be given again.

Corollary, and it is the one that matters most going forward: **a change to shared
furniture rolls through every builder in the same pass.** The FY2024 master and the
FY2030 builder are one system. A fix applied to one is a defect in the other until
it is applied there too.

**S-064 · Designer · One renderer, many instances. No builder forks another.**
JW, 2026-08-29. Executed as a no-op refactor with pixel-diff proof.

`build_tobe_2030.py` used to read `build_sankey.py` as a string and run about
twenty text substitutions on it before executing the result. Every substitution
was a verbatim copy of a line from the master, so every change to the master
silently stopped matching or matched something subtly different. That is the
mechanism behind Medicare premiums, the bottom tracker and documented fraud each
ending up with two different treatments in two diagrams. It was not carelessness,
it was the architecture.

New shape:

- `sankey.py` — `render(cfg) -> (baseline, overlay)`. All drawing, once.
- `instances.py` — one `Instance` per artifact. Ledger values, trunk step
  schedule, HR-1 terminals, tracker rows, kicker and title.
- `outflows.py` — column boundaries and the outflow ledger. Geometry declared
  once and read by the renderer.
- `ledger_2030.py` — the FY2030 post-HR-1 ledger computation.
- `build.py` — the only entry point. `python3 build.py` renders everything.

Deleted: `build_sankey.py`, `build_tobe_2030.py`, `build_sankey_2030.py`, and the
`_gen_*.py` files the substitution step used to leave behind.

**A new state edition is now a config, not a fork.** `build_sankey_dc.py` is the
last remaining copy and should be converted the same way before the state series
starts, or it will drift exactly as the FY2030 fork did.

Two guarantees the refactor buys, both enforced in code rather than by discipline:

- A change to shared furniture reaches every artifact, because there is only one
  copy of it.
- `_draw_hr1` asserts that each terminal is downstream of its own bite x, so
  S-057's backward-terminal error now fails the build instead of shipping.

Verification standard for any future refactor of this kind: render before,
refactor, render after, and diff the PNGs. Both artifacts came back with an empty
difference bounding box. A refactor that changes a pixel is not a refactor.

**S-065 · All · Geography and vantage are two axes, not one.**
JW, 2026-08-29, asking for the state-series architecture and for views rooted
further down the pipe (a plan president's $100).

Geography and year vary the NUMBERS while the structure holds. Vantage varies the
STRUCTURE: it moves the denominator to a node in the middle of the flow and expands
the graph around it. Treating vantage as a special case of geography would put the
re-rooting logic inside fifty state configs.

`ARCHITECTURE.md` is the plan. The seam to cut now is Ledger / View / Layout, where
`Instance` today conflates all three. Build the seam, not the graph engine: the
seam is what makes fifty states cheap, and the re-rooting becomes a change to View
alone if the seam is right.

**S-066 · Research Editor · Provenance belongs to the number, not to a document.**
`ENDNOTES.md` is hand-maintained. At fifty states that makes S-054 either a lie or
a bottleneck. Ledger fields become `Fig(value, source, vintage, basis, status)` and
the endnote register is GENERATED from them, exactly as the diagram is. A figure
without provenance fails the build instead of shipping bare.

This is the highest-value change on the list and it belongs before state two.

**S-067 · Research Editor · The FY2030 overlay is not proportionally scalable across states.**
Recorded because it is the error most likely to pass unnoticed. Work reporting and
six-month renewals apply to the expansion group; the provider tax phase-down
applies to expansion states only, with non-expansion states frozen rather than
reduced; the directed payment cap runs to 100% of Medicare in expansion states and
110% in non-expansion states, over a number of steps that depends on where that
state's arrangements start.

A non-expansion state's to-be is therefore **structurally different, not
proportionally smaller**. Scaling the national lane mix by a state's share of
spending is wrong in a way that looks entirely plausible. Each state's lane vector
must be derived from that state's own expansion status, provider tax position and
SDP arrangements.

**S-068 · Research Editor · Never fill a state gap with a national share.**
Fidelity will vary by state. The degrade path is to collapse detail, in order:
beneficiary pies, then the provider fan, then the payer split, with the level
declared on the artifact. Applying a national percentage to a state total produces
a modelled value wearing a measured value's clothes, and at fifty states nobody
will remember which ones were real. S-029 and S-035 in a new setting.

**S-069 · Research Editor · Conservation is a build gate, not a reading.**
`check.py` runs before anything is drawn and refuses to emit a ledger that does not
conserve. It asserts sources, trunk, payer split, claims, provider node components,
beneficiary totals, absence of silent drops, and the width test that STYLE_GUIDE
3.3 previously left to the eye.

Two things it did on its first run, both of which justify it:

- It found a one-cent defect in the FY2024 dual lane that has been shipping since
  the baseline was built (EN-38).
- It failed on the FY2030 capitated lanes because my first draft of the invariant
  was wrong, not the ledger. Writing the checker forced the invariant to be stated
  precisely: the claims-side bite falls on capitated legs only, so capitated
  components sum to their lanes LESS that bite, while fee-for-service is exact.

That second one is the real argument. A conserved ledger that has never been
written down as assertions is a ledger whose rules nobody has had to state.

**S-070 · Designer · DC is a vantage view, not a geography view.**
Found on starting the DC conversion, and it revises ARCHITECTURE.md's sequencing.

`build_sankey_dc.py` is not the national diagram with DC numbers. It has six
columns rather than eight, no claims column and no beneficiary column, five
provider nodes rather than six, a different canvas and a different scale, and a
payer column expanded into four NAMED PLANS colour-coded through to the provider
bars.

That last feature is the Fidelis-style vantage view, arriving one axis earlier than
the architecture assumed. So DC is two changes at once, geography and vantage, and
converting it is not the cheap seam test I told JW it would be.

The consequence for the state series: **the state artifact must be the national
view with state numbers**, or it cannot be read against the national pair, which is
the whole point of frozen columns and scale (S-060, STYLE_GUIDE 1.2, 1.3). The
named-plan DC diagram stays as a separate product and becomes the prototype for the
vantage layer.

**S-071 · All · Absent data is absent, declared on the artifact, and looked for later.**
JW ruling, 2026-08-29: "if data is missing, I think we should have them just be
absent, and make a note to look for them later."

Standing behaviour, now enforced in the renderer:

- A lane or column with no figure is OMITTED. Not zero-height, not a $0.00 label,
  not a national percentage applied to a state total (S-068).
- Every omission is listed on the artifact under "NOT SHOWN, and not estimated",
  with the reason, so the reader sees the hole rather than inferring it.
- Every omission gets an endnote so it can be chased.

`sankey.py` now guards the beneficiary column, public-company earnings, dual-plan
retention and documented fraud, and takes the provider node set from the instance
rather than assuming six.

**D-66 · The state artifact is the national view with state numbers.**
Confirmed by building DC. A state edition that changes columns cannot be read
against the national pair, which is the entire purpose of frozen column boundaries
and frozen scale (S-060). The named-plan DC diagram is a separate product and the
prototype for the vantage layer (S-070).

**S-072 · Production · A blocked artifact ships as a declared blank, not as a guess.**
The DC FY2030 panel on the stacked sheet is blank on purpose, with the reason
printed in it. That is more useful to a reader than an absent panel and far more
honest than a plausible one. Same principle as S-071, one level up.


**S-073 · All · A figure that travels by hand travels wrong, and takes new
artifacts with it.**
2026-09-03. D-63's sensitivity paragraph recorded overhead-scales at $77.91. The
build has never produced that number; it returns $77.85. The error sat unnoticed
for five days because it belonged to the one variant that is not published, so
nothing rendered it and nobody read it against a diagram.

It had already spread. The panel caption in `sheet.py` for `national_2030_scales`
was written by copying the figure out of D-63, so the sheet's own header
contradicted the sheet's own tracker on the same panel. That is the failure mode,
not the six cents: a hand-carried figure seeds every artifact built afterwards, and
each copy looks like corroboration.

Two consequences. **Sensitivities get rendered, not just recorded** — an unpublished
variant with no artifact has nothing to check it against, which is exactly how this
survived. `sheet.py --set overhead` now exists for that. **Panel captions must read
from the ledger, not restate it.** Any figure typed into a caption is a second
source of truth for a number that already has one. Folded into S-066: when `Fig`
lands, a caption interpolates the field and a caption carrying a bare literal fails
the build.

**S-074 · All · The tracker is a ledger, not a set of milestones.**
2026-09-03. JW marked up the 2024 panel and the architecture fell out of it. A dot
wherever a number changes and nowhere else; balance dots always black; bite dots
coloured by class. The alternation of HR-1 and admin down the line is not a design
choice, it is what the lifecycle does, and the tracker now shows it.

The move that made it general was JW's: the column slots are not a hard rule. A
column subdivides into as many invisible sub-columns as the cadence needs. That is
why a 2026 or 2036 view with a different number of bites needs no new code.

**S-075 · All · Terminals and the tracker must answer the same question.**
2026-09-03. My tributary terminals encoded how far a dollar would have travelled;
the tracker encoded where the money left the flow. For most outflows those
coincide, so nothing looked wrong. For the five state-agency levers they diverged
completely, which is why JW read the anchors as arbitrary — they were answering a
question he was not asking. Terminals now ride the tracker lattice. The reach
survives as a phrase in each sub-label, where it is legible.

A side effect worth keeping: because the five levers now land in one column, they
stack CONTIGUOUSLY and their thicknesses add by eye to the column's subtraction.
That was JW's original request weeks earlier, which I could not satisfy while they
were scattered. The right fix for a layout problem was a data-architecture fix.

**S-076 · All · Judge crossings by region, not by element.**
2026-09-03. Rule 2.9 was written for the HR-1 fan and applied to one of two code
paths, so administration and Medicare premiums crossed on every render for weeks
while I reported zero crossings. Two lessons, and the second is the real one.
A rule applied to one path is worse than no rule, because it looks handled. And a
detector that only checks what I thought to check will confirm whatever I already
believe — mine tested three tagged colours and reported clean while a crossing sat
in plain sight. `crossings.py` now samples every band on the canvas and scopes the
rule to the margin, because a ribbon leaving the middle of the stack HAS to cut
across whatever lies between it and the edge. That crossing is the flow working.

**S-077 · All · Show the picture.**
2026-09-03. JW: "how can i tell if you don't show me the picture." I twice
described geometry in prose instead of rendering it and twice was wrong. Any claim
about what a diagram looks like ships with the diagram, or a crop of it with the
thing circled.
