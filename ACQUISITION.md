# Acquiring a territory's FY2024 baseline

The order is the lifecycle order: left to right, one phase at a time, and a
phase is not left until its own arithmetic closes. Working right to left, or
pulling the interesting numbers first, is how a provider node gets a value
before anyone has established what the denominator is.

`coverage.py <territory>` is the instrument. It reports every figure the
baseline needs as HELD, MODELLED or MISSING with its source named, and exits
non-zero while anything is MISSING. Run it from the first pull, when everything
is missing, not at the end.

**It answers a different question from `check`.** `check` asks whether the
numbers are consistent with each other. A ledger can conserve perfectly and be
half empty, because absence conserves: nothing plus nothing balances. DC
conserves today and is 26 figures short.

---

## Phase 1 · FEDERAL and STATE GOVERNMENT — the cost allocation

**Pull.** CMS-64 / MACStats Exhibit 16: spending by state, category and source
of funds. Take the blended federal share including expansion, and the
non-federal share.

**Close.** Federal plus non-federal is 100. Nothing else in the baseline can be
placed until this holds, because every later figure is a share of it.

**Watch.** The blended rate is not the FMAP. Expansion sits at a different match
and territories are capped differently again. Record which it is in `basis`.

## Phase 2 · STATE AGENCY — the scale and the first peels

**Pull.** Total computable spending, which sets `SCALE` in $M per $1. Then the
administration line, and dual Medicare premiums.

**Close.** Disbursed equals 100 less the peels charged at or before this phase.

**Watch.** Administration is the least-matched money in the program and is not
one rate. If the territory's systems spending is material it belongs in a
sidecar conserving to the administration total, not on the $100.

## Phase 3 · DISBURSE — the lanes

**Pull.** Exhibit 17's managed-care lump and the fee-for-service columns. Carve
PACE and any dual-only capitation out of the lump first; CMS-64 files them
under managed care.

**Close.** The lanes sum to disbursed.

**Watch.** A territory with no managed care has a lane that is a **measured
zero**, not an absence. The two look identical on the page and mean opposite
things, and only the second earns a declaration. Set it wrong and the artifact
says we did not look when in fact there is nothing to look at.

## Phase 4 · DISBURSE, expanded — the named plans

**Pull.** The territory's managed-care performance report for per-plan
capitation revenue and incurred claims.

**Close.** Named plans sum to their aggregate lane.

**Watch.** Basis mismatch. If one plan's revenue is pure Medicaid while the
others carry locally funded enrollees, splitting all of them by raw revenue
under-weights the pure one. Anchor it at its own capitation and split the
residual. A high PMPM at small enrollment is the tell.

## Phase 5 · PAYER — the retention and its split

**Pull.** Claims over revenue per plan gives the care fraction; the remainder is
retention. The split of retention into administration and margin is the NAIC
Title XIX column, not the managed-care report.

**Close.** Administration plus margin equals retention, per plan and in
aggregate.

**Watch.** Retention measured in total with its split unpublished is the normal
state, not a failure. It is declared, and the lane still draws.

## Phase 6 · CLAIMS — the allocation into service categories

**Pull.** Exhibit 17 itemises fee-for-service. The capitated rows are the hard
part and the national mix is not a substitute for them at plan resolution.

**Close.** Row margins sum to care. Any filled row sums to its own margin, and a
partly filled row does not exceed it.

**Watch.** This is where the baseline usually stops. A row left UNALLOCATED is a
legitimate ending state; a row filled from a national share is not.

## Phase 7 · PROVIDERS — the node totals

**Pull.** A node total is only knowable once every row contributing to it is
allocated. Where the capitated rows are absent, the node total is absent too,
and the fee-for-service figure is a floor rather than a total.

**Close.** Node totals, where held, sum to claims less claims-side peels.

**Watch.** Never publish a floor as a total. Long-term care is the node this
bites hardest, because Exhibit 17's LTSS columns are fee-for-service only.

## Phase 8 · BENEFICIARIES

**Pull.** MACStats Exhibit 21 carries eligibility-group totals with a state
dimension. The interior — which group consumes which service — has no state
source.

**Close.** Group totals sum to the same figure the node totals do.

**Watch.** The interior is a declared pattern assumption or it is absent. It is
never a measurement.

---

## How often verification runs, and what makes it lapse

Strict meaning: `verified` records that a person opened the source and agreed
with the number. Nothing else earns it — not a redline, not an endnote, not
having shipped.

But it is not re-earned on a schedule and not on every edit. **Verification
attaches to a vintage and to a value.** A figure signed against MACStats FY2024
stays signed for as long as the ledger is anchored to FY2024. It does not
expire on the calendar, and rebuilding does not touch it.

Three things end it, and each is detected rather than remembered.

- **A new vintage.** Re-anchor the ledger and every figure whose vintage is now
  behind the cycle reports STALE. Sign what still holds; re-pull what does not.
- **An edit after signing.** `sign()` records the value alongside the signature,
  so a figure signed at 28.27 and later changed to 30.00 reports LAPSED and
  **fails the build**. This is the one that would otherwise go unnoticed: the
  source is still named, the date is still there, and the number underneath has
  moved.
- **A correction to the source.** An amended or restated filing invalidates the
  signature the same way an edit does. Clear it by hand.

So: run `coverage` on every build, because it costs nothing and because a
lapsed figure should surface the moment it is created. Expect the answer not to
change between runs. When it does change, something happened that should have.

## The rule the order exists to enforce

A figure enters the ledger with its source, its vintage, its basis and its
status, or it does not enter. `check` refuses a figure without provenance and
`coverage` refuses to call the baseline complete while anything is missing. The
process above is what those two gates are checking; it is written down so the
gates are not the only place it lives.
