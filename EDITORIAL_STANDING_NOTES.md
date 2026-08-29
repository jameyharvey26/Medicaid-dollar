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
