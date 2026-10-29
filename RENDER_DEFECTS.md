# Render defects — engine against the paper

Raised by JW, 26 October, reading `engine_vs_paper.html`. Numbered so they can
be closed one at a time and so none of them is lost to a summary.

Three kinds, and the kind decides who fixes it:

- **R** — the renderer draws the wrong thing, or does not draw it.
- **S** — the solver places it badly. These are §10 of the geometry contract.
- **D** — the data never reaches the engine. `explorer.py` builds the payload.

| # | kind | defect | state |
|---|---|---|---|
| 1 | R | Terminal labels paint centred on the ribbon, over it. The solver reserves the block BELOW the band and the renderer ignores that. | fixed |
| 2 | R | The HR-1 rule runs the full canvas width and sits too close to the flow, crossing the source bars and their labels. | fixed |
| 3 | R | Documented fraud was pulled out of the fan. JW: it is a tributary and belongs in it. | fixed |
| 4 | R | The claims lane draws service totals only. The lane × service cross-tab — which capitation lane pays for which service — is in the payload and is dropped. | fixed |
| 5 | R | Provider bars abut. The paper separates them. | fixed |
| 6 | R | Provider tax limits departs from empty space instead of the federal lane. | fixed |
| 7 | R/S | The ordinary outflows (Administration, Federal oversight, Medicare premiums, Vaccines for Children) all leave one x at the top of the trunk, so where in the lifecycle each is charged is lost. Each declares its own `src_x`. | fixed |
| 8 | R | Those outflows terminate mid-phase rather than at the column edge their `term_col` declares. | fixed |
| 9 | R | Their labels use a different idiom from the HR-1 fan. JW: use the HR-1 placement for both. | fixed |
| 10 | R | Vaccines for Children and Medicare premiums RETURN — they terminate upstream of where they leave. `OUTFLOWS.ret` declares it; the engine has no notion of it. | fixed |
| 11 | R | The trunk does not show itself being decremented. The paper fills the vacated space at the bottom of the hundred with sub-rectangles, so the river reads as losing volume. Without it the flow looks broken. | fixed |
| 12 | R | Money leaving the MIDDLE of the diagram (dual MCO plan administration) should open white space where it left. The engine closes up. | fixed |
| 13 | D | Public-company earnings is drawn by the paper and is not in the payload at all. | fixed |
| 14 | S | Medicare Savings sits where the solver could do better. Covered by contract §10 — clearance measured at the terminal rather than along the curve. | fixed |

**13 is not a missing band.** `sankey.py` draws public-company earnings as a
LABEL at the payer column and nothing else, because the figure is a carve out
of MCO retention and `build_xlsx.py` records it as never additive to margin.
Exporting it as a peel would decrement the hundred twice. The fix is to carry
the ledger's `earnings` through `build_explorer.py` into the payload and render
it as a declared annotation at PAYER — a payload change and a conservation
question, not a renderer defect, which is why it is still open.

7–10 are one mechanism: the ordinary outflows want the same treatment the HR-1
fan now has — own `src_x`, terminal from the declaration, solved by `_place`,
labelled the same way — with returns added to it. Do them together.

11 and 12 were one mechanism and are closed together. The trunk now carries
both edges stepping -- ordinary outflows off the top, HR-1 off the bottom, each
at the x it is declared to leave -- so the river visibly loses volume and the
space a bite vacated is where the bite is. Mid-diagram, 12 came out of the
lane × service rework: each lane's cells start below what that lane retained,
so the retention leaves an open gap at the top of its own lane instead of the
stack closing up behind it.

All fourteen are closed.

13 turned out not to be a missing band. The figure is a carve out of MCO
retention, so drawing it as its own ribbon off the hundred would subtract it
twice. The fix was the channel, not the drawing: `engine_data_export.py` now
carries each lane's administration and margin from the ledger, and the payer
column draws the retention pooling and splitting into plan administration and
shareholder earnings. Where the split is not published — DC — the pool runs
through as one hatched band carrying the ledger's own sentence.

14 is contract §10 and was solved by the curve rather than the solver: see
`ctrlPair` / `dropFor` and MANIFEST D-120.

Known and not filed as a defect: on the FY2024 and FY2030 national panels the
Vaccines for Children return label sits tight under the "Federal $65.29" source
label. There is no room for a row between the column headings and that label,
so the solver is doing the best the space allows. Moving the source label, or
giving returns their own band above the headings, would be the fix.

---

## Six national FY2030 panels are unblessed on purpose — 29 October

`renderproof` is red, and will stay red until this is closed. It is not a
fault and it is not noise. Read this instead of re-deriving it every session.

`national_2030_holds`, `national_2030_mixed` and `national_2030_scales`
(combined and overlay, six files) stopped matching the register at commit
**c518476, "Fully rendered web sankey", 28 October**. The register was blessed
at 69f61bf on 28 September. Both facts were established by rebuilding at
69f61bf, where all fifteen panels reproduce byte for byte, and then bisecting
the five commits since.

What moved: `_draw_hr1` stopped pinning HR-1 terminals to an absolute canvas
`term_y` and started pinning them to the fan via `term_dy`, because an
absolute y is only correct on a panel whose flow floor puts the rule where it
was written for and cannot be exported to a renderer whose rule sits
elsewhere. Terminals move about a pixel. **No figure changed** — every
`data-val` on all six files is identical to the register's, and with numbers
masked the files are token-for-token identical. The shift is invisible at
print size; the crop JW looked at on 29 October was at 2x.

So this is the ONE ENGINE port working as intended, caught by the gate that
exists to catch exactly this.

**Open, and JW's to close:** whether the ~1px terminal shift needs saying
anywhere about the frozen v8.0 paper, whose FY2030 figures were rendered with
the old geometry. JW chose on 29 October to leave the six unblessed until he
has looked at that himself, rather than bless them and lose the flag. The DC
panels were blessed separately the same day, with their own reason, using the
`--only` switch added for this.

To close it, once the v8.0 question is settled:

    python3 renderproof.py --bless "c518476: HR-1 terminals pinned to the fan (term_dy) rather than absolute canvas y so the geometry exports to the engine; terminals move ~1px, no figure changed" --only national_2030
