# Change list — v6.1 to v6.2

Every edit below is one of JW's 77 PDF annotations, a consequence of D-91, or
one of the numbered steps in the session plan. Three are marked CORRECTED or
FLAGGED and are the ones to read first.

## Applied edits

- **#1** — strike 'to run'
- **#2-3** — strike the 'stated once' line and the per-hundred-dollars paragraph; the unit note survives in note 2
- **#5** — 'comes from' -> 'originates'
- **#6-7** — two strikeouts left a fragment; reconstructed to one sentence keeping what survived
- **#8** — strike 'the one flow that travels backward'
- **#9-10-11** — strike 'the program pays' and 'and because it is federal'
- **#13** — strike 'which matters later'
- **#14-15** — strike the ribbons clause and the documented-fraud sentence from the Figure 4 caption
- **#16** — strike the 'most useful thing on that phase' opener
- **#17-21** — tense to past, 'in 2024' inserted, second sentence struck
- **D-91a** — D-91: five eligibility columns, not four. The two adult columns are published separately because the law does not reach them alike
- **#22-30** — 'Why fiscal year 2030' and the two-provisions paragraph lifted out of the diagram page
- **#22-30b** — the aside box lands at the end of the section, in the style of 'A national average is not a local condition'; the two provisions are named
- **#39a** — S-108 taxonomy: the table row takes the diagram's name
- **#39b** — S-108 taxonomy
- **#39c** — S-108 taxonomy
- **#39d** — S-108: 'blocked senior enrollment' was a third name for the same provision
- **#39e** — S-108
- **#39f** — S-108
- **#31** — the provider-tax aside becomes a footnote
- **#31b** — the aside's content moves to note 11
- **#32-37** — five marks on one sentence; punctuation repaired and the anchor sentence struck
- **#40** — 'dollar' -> 'money'
- **#41-42** — struck clause replaced by JW's sentence; 'of it' -> 'its Medicaid spend'
- **#43-46** — CORRECTED against JW's note: the note as written reversed the service lists and said the section reaches beneficiary groups, which it does not
- **#47** — the six-month renewals aside, placed with the provision it concerns
- **css** — reduction columns get a negative sign and the loss colour
- **#50-52** — payer table: modeled-rate column dropped, FALL renamed REDUCTION, figures negative and red
- **#48-49** — 'care, directly'; strike 'still'
- **#53-56** — two stickies reconstructed into one sentence as JW specified; 'negotiated between payers and states'; 'did' -> 'does'
- **#57-60** — 'And the risk pool's mix shifts' -> 'Risk pool mix will shift'; 'cheapest' -> 'who are most expensive'
- **#61-64** — 'and' -> 'but'; renegotiation clause rewritten; closing sentence bolded
- **#66** — Figure 11 caption cut to roughly half length
- **#67-69** — CORRECTED against JW's two notes, which had the service lists reversed; the rounding clause moves to note 8, where it already sits
- **#70** — provider table: same rename and treatment, modeled-rate column kept
- **#71-72** — comma to full stop, new sentence opening 'Other variables include whether'
- **#73** — JW's addition, hedged: 'most experts are predicting' asserts a survey of expert opinion the paper cannot source. Written as a widely expected consequence and footnoted. FLAGGED FOR JW
- **#76** — 'The per-state series' -> 'The view at the State level'
- **#77** — struck sentence replaced with JW's
- **note5** — D-91: five eligibility columns
- **note9** — D-91
- **note9b** — D-91
- **limits** — D-91
- **notes-new** — notes 11 and 12 added for the provider-tax aside and the consolidation sentence
- **#74-75** — the beneficiary section rewritten from the ledger's side to the beneficiary's side and organised by population, per JW's page-14 note; the pie crop replaced by the two-households graphic
- **limits-lede** — three entries added
- **limits-3** — the three Limits entries step 3 calls for
- **notes-13-16** — notes 13 to 16: the cube with its contradiction declared, the coverage/rate classification, the statutory basis, and the 2026 Medicare amounts
- **figB_provisions_with_line.png** — JW: Figures 6 to 9 and 11 rebuilt as horizontal versions of the cover graphic, same palette and compositing
- **fig14_terminals_left.png** — Figure 7 as a taper; the out-of-focus provisions are greyed rather than cropped out
- **fig12_sources_2030.png** — Figure 8 as a taper. The phase set runs one further up than the cover's, because this figure's whole subject is above where the cover starts
- **fig13_terminals_2030.png** — Figure 9 as a taper
- **fig9b_providers_pies_2030.png** — Figure 11 as a taper, with the payer column out of it as JW asked on page 13
- **fig15_households.png** — JW's page-14 note answered directly: the pie information told from the population's side, as Figure 12. The households graphic follows as Figure 13

## Custom graphics, D-95

Each ships as a repo artifact: its own script, SVG, PNG and generated alt text
in `cover/`, with contrast measured by `contrast.py` and printed at build time.
Two versions of each, masthead on for standalone use and off for the paper.
`make_figs.py` builds all of them in one command.

| Figure | Script | What changed |
| --- | --- | --- |
| 6 | `taper.py` | all seven provisions on the band |
| 7 | `taper.py` | the three that leave before a claim exists |
| 8 | `taper.py` | the federal band, one phase above where the cover starts |
| 9 | `taper.py` | the payer and claims phases |
| 11 | `taper.py` | what lands on providers and beneficiaries; payer column out |
| 12 | `population.py` | NEW. The pies read from the population's side |
| 13 | `family.py` | the two households, renumbered from 12 |
| cover | `cover_taper.py` | masthead cropped for the cover, kept for standalone |
| 3 | `make_figs.py` | state agency lane cropped out |

## Annotations not applied as an edit

- **#38** p11 — KEPT. Figure 6 still prints the residual's examples, so the
  sentence is still doing work.

## Open for JW

1. Eight whitespace strandings. Page 9 is the worst at 38 lines: the provisions
   table and Figure 7 do not fit together.
2. Five figure/subject mismatches, up from one. Three column-width crops became
   three full-width tapers and the provision prose lost its figures.
3. The page-13 consolidation sentence: hedged, note 12.
4. D-91: derive all five eligibility rows and re-sign three figures, or leave it.
5. The AI section says every figure is read from the code at build time. It is not.
6. Landing page URL and repository path.
7. AUTHOR_HELD_SHEILA.md in a public repo.
8. The Medicare Savings marker sits on a divider it is not subtracted at.

