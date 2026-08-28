# Decisions added 2026-08-27, second session part 2 — FMAP, basis, second ledger

Follows `WHITEPAPER_BRIEF_APPEND_2026-08-27b.md`. Both of the tasks JW opened the
session with are now closed. Read with S-036 through S-039.

---

## D-43 · Expansion lanes gross up at 88.05%, not 90%

Corrects the two lanes recorded as settled earlier in this session.

The VIII group is not uniformly at 90%. Measured across FY2024 CMS-64 National
Totals:

| | Total computable | Effective federal share |
|---|---:|---:|
| VIII newly eligible | $148.9B | **90.06%** |
| VIII not newly eligible | $37.3B | **80.03%** |
| **VIII group, all** | **$186.2B** | **88.05%** |

Not-newly-eligible is 20% of expansion spending, concentrated in states that covered
adults before the ACA. Sections 71119 and 71107 apply to the expansion adult group as
a whole, not to the newly-eligible subset, so 88.05% is the defensible rate.

The 90.06% measurement independently validates the statutory rate at SSA 1905(y)(1)
showing up in the actual books.

Moves work reporting from $352.2B to $360.0B total computable.

## D-44 · QI carve-out is zero, on structural grounds

Medicare Savings Programs do not share one match rate. QMB and SLMB match at regular
FMAP; QI is 100% federal from a capped allotment (CMS SMD 10-003), so QI dollars
gross up at 1.000 rather than 1.701.

**The carve-out is nonetheless zero.** QI is a capped federal entitlement: states
enrol first-come, first-served and stop when the year's allotment is exhausted.
Blocking a rule that would have raised enrolment produces no federal QI savings,
because the ceiling binds the spending rather than the enrolment. The pot is the same
size either way; it just runs out sooner.

Scale corroborates independently. MACRA allocated $980M for CY2016, so roughly $1B a
year is the entire programme, against a lane scored at $66B over ten years.

**Bound:** if QI were 15% of the lane (its *enrolment* share, and a hard upper bound
since QI pays less per person than QMB) the lane would be $105.3B rather than
$112.3B. Six percent of one lane, under one percent of the overlay.

**Footnote caveat, not modelled:** MACRA established a formula for future allotments.
Whether that formula is responsive to enrolment is unverified. If allotments rise with
prior-year uptake, some QI sensitivity returns over a ten-year window.

**Do not substitute MACPAC's 53/32/15 MSP split.** That is enrolment, not spending;
QMB pays premiums plus all cost sharing while SLMB and QI pay the Part B premium
only. Using it as a spending share would be S-034 one session after writing S-034.

## D-45 · Use CBO's deficit series throughout. Do not adjust, do not scale.

Closes open task 2.

CBO's October 2025 supplemental gives the chapter table as outlays $914.6B, revenue
reduction $27.9B, deficit $886.8B. The seven section figures sum to $886.8B exactly,
so every section-level figure in `ramp.py` is on the deficit basis and the series
conserves against CBO's published total. FY2029 checks the same way: 92.944 − 2.798 =
90.146, which is `ramp.py`'s `FY29_DEFICIT`.

**Mechanism of the wedge.** Deficit equals outlays minus revenues. Coverage loss moves
some people onto employer-based coverage, which is tax-excluded, so revenue falls and
deficit savings land below outlay savings.

**Three lanes are already outlay-equivalent.** Directed payment caps, the blocked
senior enrollment rule, and the residual all have zero coverage effect by CBO's own
findings, so deficit equals outlays for them. That is $275.5B of $886.8B needing no
adjustment and no flag. The entire $27.9B wedge sits in the other four lanes.

**Why not adjust.** CBO publishes no section-level outlay or revenue split, only the
chapter table. A uniform 1.0314 scale-up would be actively wrong, pushing revenue
effects onto three lanes CBO says have none. Any allocation is unsourceable.

**Conceptual argument, which runs the same way.** The ledger traces Medicaid dollars.
The $27.9B is forgone tax revenue from employer coverage take-up. It was never a
Medicaid dollar and has no node in the diagram. Excluding it is right on the merits,
not a concession to data availability.

**Footnote carries:** chapter Medicaid outlay reduction is $914.6B, 3.1% above the
deficit total; the difference is a revenue effect rather than Medicaid spending; not
allocable by section from published data.

**D-26 CORRECTION, confirmed.** CBO states 71119 decreases deficits by $317.0B. The
$325.6B figure appears nowhere in the supplemental; it came from CRS. Strike it from
D-26 and recompute both illustrative figures off $317.0B.

**No rework.** `ramp.py`'s figures were correct; only the label and D-26's citation
were wrong.

## D-46 · Directed payment lane splits two ways nationally, not three

Implements D-41. Financing mix from ASPE (2026): $8.4B of $12.3B of the non-federal
share of 2022 SDP spending was provider-tax or IGT financed, so 68.3% provider-
financed and 31.7% state general fund.

| Slice | Federal | Treatment |
|---|---:|---|
| Provider and local government financed | $102.0B | No gross-up. Providers lose the federal match (D-39 logic). |
| State general fund financed | $47.4B | Grosses up to **$73.2B** total computable. Produces **$25.8B of state RELIEF**. |

**Tax and IGT are not separated, by decision.** The split cannot be closed from
published data: MACPAC recommended Congress require states to report non-federal share
by source and Congress has not acted, so every published figure combines them. For the
first ledger the distinction is immaterial. It matters only for which line of the
second ledger receives it, and D-03 node 4 already reads "state and local". Revisit
for state editions, where single-state preprints make it tractable and where the
distinction carries information.

**Rate on the general-fund slice: the all-population blend (64.72%).** MODELLED. SDPs
cover hospital, nursing facility and academic-medical-centre physician services used
across every eligibility group, and no payment-weighted managed care rate is
published. Flag on artifact.

**Lane shape.** Section 71116 does not eliminate directed payments; it ratchets the
ceiling toward Medicare rates (110% in non-expansion states) at 10 percentage points a
year from FY2028. A partial reduction of a continuing payment, not a payment stopping.

**The finding this produces.** $25.8B of relief sits against roughly $1.19 per $100 of
provider-tax pressure, in the opposite direction. HR-1 does not do one thing to state
budgets: it sends a bill on one lane and a refund on another, and the net depends
entirely on how a given state financed its share. Same law, opposite signs. This is
the strongest single argument for the state series.

## D-47 · The state general fund is an unsized container inside the government column, state row

**Amends and supersedes D-40's structure.** The second ledger is not a companion
exhibit. It is a property of one cell in the main diagram.

**Structure.** The state general fund renders as a container drawn around the state
node in the government column. Medicaid's general-fund-financed share is the one band
inside it that carries a number. Everything upstream of that cell and everything
downstream of it — MCOs, providers, claims — stays Medicaid-only. The $100 conserves
untouched because nothing was added to it.

**The container is not sized.** Other claimants on the general fund are context, not
flows. No NASBO figure, no state-fiscal-year basis conflict with D-07, no
with-or-without-federal-funds trap. It also removes a headline risk: an unsized
container cannot generate "Medicaid is X% of state budgets," the sentence most likely
to escape the exhibit without its qualifier.

**Conservation rationale.** Admitting schools and corrections as *flows* would put
dollars into the ledger that never leave through a Medicaid lane, breaking the
non-negotiable. Containment rather than flow keeps the ledger intact while still
showing the lane passing through a box visibly larger than itself. Same move D-31
already uses for grant programmes sitting alongside rather than inside.

**Two boundary crossings carry the exhibit:**
- **In:** provider tax limits push roughly $1.19 per $100 of previously displaced
  obligation back onto the general fund.
- **Out:** directed payment cuts on general-fund-financed arrangements return money,
  $25.8B federal-equivalent at ten years.

**Rationale, JW:** a governor is an audience for the state editions, and inside their
own lane they want their whole picture. Medicaid is one claimant among several in the
government column, state row — and only there.

**Encoding consequence:** see S-039. Because the container has no scale, the crossing
flows must be annotated with explicit figures rather than drawn proportionally, and
the container must be visibly a different object from the Sankey around it.

**Displacement mechanism, retained from D-40 and unchanged.** Nothing flows *out* of
the $100. Provider tax revenue is already inside it. What funds other state programmes
is displacement: the state was going to appropriate general fund money to Medicaid,
provider tax revenue covers that obligation instead, and the general fund money never
enters the ledger. Under HR-1 that re-presents a general fund bill the state stopped
receiving years ago.

---

## Task 1 — CLOSED

| Lane | § | Rate | Factor | Fed $B | Total $B |
|---|---|---:|---:|---:|---:|
| Work reporting | 71119 | 88.05% | 1.136 | 317.0 | 360.0 |
| Six-month renewals | 71107 | 88.05% | 1.136 | 58.0 | 65.9 |
| Blocked Medicaid enrollment rule | 71102 | 58.79% | 1.701 | 53.6 | 91.2 |
| Blocked senior enrollment rule | 71101 | 58.79% | 1.701 | 66.0 | 112.3 |
| Everything else | resid | 64.72% | 1.545 | 60.1 | 92.9 |
| Provider tax limits | 71115 | n/a | n/a | 182.7 | no band (D-39) |
| Directed payment caps | 71116 | split | — | 149.4 | see D-46 |

Derived rates, from CMS-64 FY2024 National Totals, four quarters, MAP only:
all-population blend 64.72% (validates D-10), VIII newly eligible 90.06% (validates
the statutory rate), VIII group effective 88.05%, non-expansion blended 58.79%.

**Scope note.** The CMS-64 New Adult Group dataset is Medical Assistance Payments
only. Federal MAP is $595.0B against MACStats' $620.4B total federal, so ~$25B of
federal administration sits outside it. Correct basis for benefit-loss lanes. WRONG
basis for D-32.

**FFCRA caveat, measured not assumed.** QE 12/31/2023 carries residual enhanced match;
non-expansion computes to 60.28% there against 58.2–58.5% in the three clean quarters.
Full-FY2024 58.79% retained for D-07 consistency; clean-quarter alternative (58.31%)
held in `fmap.py` so the choice is visible.

**Admin-match caveat, footnote not adjustment.** CBO's scores for 71119 and 71107 are
net of increased state administrative cost, which matches at 50% rather than 88%.
Grossing a net figure at the benefit rate is wrong in a known direction. CBO does not
break it out.

**Data quality.** Oregon QE 9/30/2024 and Louisiana QE 6/30/2024 report VIII spending
at implausible shares of their own state totals, almost certainly prior-period
adjustments. The national aggregate absorbs them; a state edition would not.

## Task 2 — CLOSED

See D-45.

---

## New code

`fmap.py`. Per-lane rates with the raw CMS-64 quarters embedded so every rate
recomputes rather than being trusted. Run directly for the table. `financing.py`
updated for D-46.

## Open at session close

1. **Encoding: two lanes carry no total-computable band while five do** (S-038).
   $332.1B of $886.8B drawn on a different basis from its neighbours. Highest risk to
   the artifact; ahead of anything left in the numbers.
2. **Encoding: unsized container must not read as a scaled band** (S-039).
3. Decompose the `ramp.py` provider tax weight into expansion phase-down and
   non-expansion freeze (flagged in file, value unchanged).
4. Strike $325.6B from D-26 and recompute its illustrative figures off $317.0B.
5. MMIS/systems share of the CMS-64 administrative line (D-32) — note this needs a
   different data source than `fmap.py`, which excludes administration.
6. RHTP appropriation amount and period, and DC eligibility (D-31).
7. Sensitivity range for the work reporting ramp weight (0.60 / 0.75 / 0.90).
8. `build_sankey_dc.py` still not on the three-file emit.

**Nothing is blocked on data.** What remains is construction and encoding.

## Closed, do not reopen

- Erin Henderson interview. Not planned.
- Immigrant eligibility lane. Footnote, not a lane.
- Provider tax versus IGT split, nationally. D-46; state editions only.
- Push-to-GitHub workflow. `SAVE TO GITHUB.command` is in the repo and working.
