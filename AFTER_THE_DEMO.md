# After the demo — one thing to settle, and three to finish

Written 30 October 2026 at JW's request, mid-session, while the demo was being
prepared. JW, on the change described in §1: *"I think you've got that wrong,
but I can't talk about it now."*

The change is IN. This note exists so it gets re-argued with time to do it
properly, not so it stands by default.

**RESOLVED 3 November 2026, D-126.** JW's removal stands and the argument
against it was wrong in a specific way: the caption that was removed reads
"SERVICE MIX ASSUMED / national shape on District dollars", which is the
District's claim and nonsense on a national plate. Nationally the service
TOTALS are measured off Exhibit 17 and what is modelled is the division of
each bar BETWEEN PAYERS — a different statement. The fourth candidate reason
below is the one that holds: the flag is mis-named, not the drawing
mis-declared, and the constant is literally called `MIX_BORROWED` while the
national mix is fitted rather than borrowed. The national panel now gets its
own declaration in its own words, and `ask.js` changes with it, because its
text currently asserts the thing is not declared. The reasoning below is kept
as written, for the record.

---

## 1. SERVICE MIX ASSUMED came off the national panels. JW thinks the
##    reasoning was wrong.

**What changed.** The violet `SERVICE MIX ASSUMED` headline and the per-bar
`mix assumed` tags are no longer drawn on `US|2024` or `US|2030`. The District
panels are untouched — headline, sub-line and five tags, as before. The gate
is `MIX_BORROWED` in `draw()`: `mix_assumed && code starts with DC`.

**JW's instruction**, 30 October: *"in the national view take the purple
SERVICE MIX ASSUMED off the provider column. Its only assumed in DC."*

**The argument I put against it, which JW says is wrong.** Roughly: that
`engine_data_export` sets `mix_assumed` when any capitated cell is MODELLED;
that the national cells are modelled because `ledger_national_2024` carries no
interior for the claims matrix and notes the rendered pies are *"fit by
iterative proportional fitting to both margins from a seed pattern that
carries no citation"*; and that removing the declaration therefore lets the
national plate draw a fitted cross-tab exactly as it draws a measured one,
which is what the flag was put there to prevent.

JW overruled it knowingly and asked for the removal anyway, then said the
reasoning was wrong.

**Candidate reasons it may be wrong — to be tested, not assumed.** Written by
the person who made the argument, so treat them as leads rather than a defence:

- The engine may not draw the fitted interior at all. Check what the provider
  bars' internal division is actually built from: if the payer split within a
  bar comes from `P.cells` as exported, check whether those cells are the IPF
  pies or something measured. The claims matrix note may describe the PAPER's
  pies (fig4b) and not the engine's bars.
- `instances.py` / `provider_mix.py` may carry a measured national split that
  the ledger's `cell={}` comment does not describe.
- The flag may be true nationally for a cell that is not in the drawing.
- "Assumed" in this project may be a term of art meaning BORROWED FROM ANOTHER
  JURISDICTION, in which case national is simply not assumed and the flag is
  mis-named rather than the drawing mis-declared.

**Where the knowledge went in the meantime.** The question box is told, on
every national question, that the service totals are measured off MACStats
Exhibit 17 and that the payer division inside each bar is fitted from an
uncited seed, and that this is not declared on the plate. If §1 resolves the
other way, that text in `ask.js` has to change with it — it currently asserts
the argument JW says is wrong.

---

## 2. Three declarations now live in two places

`engine_data_export.py` flattens the ledgers on the way into the browser and
drops things the engine then has to carry itself:

- **`Fig` provenance.** Every figure in the ledgers carries source, vintage,
  basis, status, parents and `verified`. None of it crosses. The question box
  answers provenance by finding the passage that discusses a figure, rather
  than reading the figure's own record. Carrying `source`/`vintage`/`status`/
  `verified` would let it answer about the exact number on screen.
- **The work-reporting band.** The three rates (CBO implied 0.181112, Arkansas
  0.25, New Hampshire 0.40) are typed into the engine. The implied one is
  derived in `tobe2030_dc.py`.
- **`DC_NAMED_PROVISIONS`.** The three District provisions and their dates are
  typed into the engine. They are declared in `tobe2030_dc.py`.

## 3. The canvas and the geometry contract — CLOSED, 3 November 2026. D-132.

**This section was wrong twice, and the corrections are the answer.**

It said the engine "crops it to 200 and draws a 1820-unit canvas". The width is
right and the canvas is not: the engine computes
`xBE = [BENEFICIARY.x0, BENEFICIARY.x0 + (PROVIDERS.x1 - PROVIDERS.x0)]`, so
1760 + 200 = **1960**. The figure 1820 appears nowhere in the engine.

It also implied something was lost. Nothing is. The engine moves the
termination slot in with the edge —
`Object.assign({}, GEOM.term_slot, {BENEFICIARY: W})` — so the Medicare
Savings lever, the one lever whose loss lands outside the delivery system,
still terminates exactly where it should relative to the surface it lands in.
The narrow column holds the anchor; it simply has no room for pies.

**And that is what JW wants.** His direction, 3 November 2026: the population
pies and the aligned number line go in the PRINTED Sankeys; in the interactive
version they become a separate view, **not yet designed**. So the print
surface should be wide and the app surface narrow, and he reserves the right
to change the sizes again — "so I wouldn't create a bunch of inflexible rules
about canvas sizes."

**So neither artifact follows the other and neither is an exception.** The
contract was pinning the wrong thing: `BENEFICIARY` sat in the frozen spine
table beside seven flow columns, with `W = 2200` frozen next to it, which made
a presentation choice look like structure.

`GEOMETRY_CONTRACT.md` §1a now separates them. The surface's LEFT EDGE is
frozen at `PROVIDERS.x1`, its existence is frozen because a lever terminates
in it, and the alignment of the pies to the number line beneath them is frozen
because that is what makes the surface readable. Its WIDTH is free, `W` is
derived from it rather than declared, and the two widths in use — 420 for
paper, 200 for the engine — are recorded as renderer choices rather than as a
disagreement.

## 4. $2.90–$5.40 — CLOSED, 3 November 2026. There was never a range.

JW's instruction on the finding below: leave $2.90 alone, confirm its source,
close this item.

**The pair appears exactly once in the repo: in the heading of this section.**
Nowhere else, in any form. The two numbers were never related to each other.

**$2.90 is `peel.medicare`.** Medicare premiums and coinsurance that Medicaid
pays on behalf of dual eligibles — a lane on the as-is diagram with nothing to
do with work reporting. It appears under that description in `build_doc.js`,
`build_xlsx.py`, `README.md`, `encoding_specimens/bite_points.py`, the August
whitepaper brief, and at EN-19 and EN-27.

**$5.40 appears once, in a code comment**, at `engine_texts.py` line 20, as an
invented example of the figure you would wrongly record if you dumped the
engine's text while a slider was mid-drag:

> A panel's strings are collected AT THE PUBLISHED DEFAULTS. Moving a control
> changes figures, so a dump taken mid-drag would record $5.40 as though the
> paper said so.

Which is the most likely account of how the "range" came to be written down:
two unrelated numbers read off a screen, one of them a control caught in
motion, recorded afterwards as a pair.

**The source for $2.90, confirmed.** MACPAC, MACStats Exhibit 17, Total
Medicaid Benefit Spending by State and Category, FY 2024, published February
2026 — Medicare premiums and coinsurance, $27,774M, over the national hundred.
`status=measured`, and **signed: `verified = "2026-09-18 JW"`** at
2.923074332431033. Nothing to acquire.

**One defect found while confirming it, and it is not closed by this item.**
The signed value is **$2.9231**. `SIGNING_2026-09-18.md` records the move:
`peel.medicare | 2.90 | **2.92** | moved`. So $2.90 is the pre-re-acquisition
figure and it is still typed in all six places listed above, including both
endnotes, which read "falls $2.90 → $1.63". The lane is right; the number
printed beside it is a cent stale, in documents a reader would take as
authoritative. `typedfigures.py` is the gate for this and already reports
typed outputs across the builders. Raised separately; this section is closed.

**And the item this section was really worrying about stands.** Whatever the
work-reporting slider's travel is, it is not this. It is the rate band —
default, then the observed ends — and `tobe2030_dc.RATE_BAND` is where that
lives.
