# After the demo — one thing to settle, and three to finish

Written 30 October 2026 at JW's request, mid-session, while the demo was being
prepared. JW, on the change described in §1: *"I think you've got that wrong,
but I can't talk about it now."*

The change is IN. This note exists so it gets re-argued with time to do it
properly, not so it stands by default.

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

## 3. The canvas no longer matches the geometry contract

`GEOMETRY_CONTRACT.md` gives BENEFICIARY 420 units against PROVIDERS' 200. The
engine now crops it to 200 and draws a 1820-unit canvas, which is what let the
plate scale up inside the panel. Decide whether the paper follows or the engine
is a declared exception, and write it down either way.

## 4. $2.90–$5.40 has no source in this repo

The national work-reporting range the engine carried from the spike appears in
no ledger — not `tobe2030`, not `ledger_national_2030`. It has been replaced by
the rate band (default → Arkansas → New Hampshire). If it turns out to be a real
CBO uncertainty range, it belongs as a fourth mark inside that band rather than
as the slider's travel: the band answers what happened when states did this,
which is a different question from how uncertain CBO is about its own score.
