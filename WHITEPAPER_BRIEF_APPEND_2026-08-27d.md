# Decisions added 2026-08-27, part 3 — framework architecture and overlay encoding

Follows `WHITEPAPER_BRIEF_APPEND_2026-08-27c.md`. This session was scoped to the
ENCODING layer (D-27 / S-025). No data-layer values were created. Read with S-040
through S-044.

---

## D-48 · One master framework, two instances: as-is and to-be

JW, on seeing that the session had been designing a layout from scratch rather than
against the existing render.

**As-is.** The FY2024 baseline currently emitted by `build_sankey.py`. Eight columns
(FEDERAL, STATE GOVERNMENT, STATE AGENCY, DISBURSEMENTS, PAYER, CLAIMS, PROVIDERS,
BENEFICIARIES), grey leakage peeling **upward** with figures labelled above the peel,
and the balance line $100.00 → $92.03 → $86.42 → $86.27.

**To-be.** The *same* framework, same columns, same geometry, redrawn with projected
**2029 prior-law** data. The $100 still conserves. Onto that second instance rides the
HR-1 overlay: warm bands peeling **downward** out of the $100 at the point each
provision bites.

**The overlay rides on the master.** It is not a separate diagram on shared rails and
not a companion exhibit. Closes the question left open earlier in this session.

**Why this works.** The two instances are comparable because the skeleton is identical
by construction, not because anyone aligned them — the same argument S-027 makes for
the three-file emit, applied one level up.

**Anchor year is 2029, not 2028.** JW said 2028 in setting out the architecture and
corrected to 2029 on challenge. D-01 has been amended in place accordingly (S-032's
rule), since the 2029 amendment had been living only in the 2026-08-27 append while
the brief still read 2028. That stale entry is the most likely source of the slip.

**Consequence that must be flagged on the artifact.** The as-is is FY2024 actuals. The
to-be is a projection of prior law, so *every* figure on it is modelled — not only the
overlay bands but the ordinary-looking baseline numbers too (MCO capitation,
long-term care, the beneficiary pie shares), because D-11 holds FY2024 structure
constant and applies it to a projected total. Without a whole-diagram flag the to-be
will read with the same authority as the as-is.

## D-49 · Overlay width encodes what leaves the Medicaid dollar, not what CBO scored

JW ruling. Resolves S-038.

**Rejected framing.** S-038 described the two exempt lanes as drawn "on a different
basis" from their neighbours. They are not. Run D-39's own worked example: when tax
capacity is removed, the dollars that actually leave the ledger and land somewhere are
the federal match. That is a total-computable figure. All seven lanes are already
commensurable and band width can keep one meaning throughout.

**What actually differs is composition.** Five lanes lose federal and state money
together. Two slices lose federal money only, because their non-federal share was
provider revenue recycled through the state and was never state money to lose.

This matters because every fix aimed at a *basis* problem — a second scale, a separate
register, a hatched void where the gross-up "should" be — encodes a claim D-39 says is
false. A void tells the reader the state share was incomputable. It is computable. It
is zero, on the merits.

**Encoding.** Every loss band carries an internal partition at its federal fraction:
federal share solid warm, non-federal share same hue, open, hatched, hairline-divided.
The partition sits at 88.05% / 88.05% / 58.79% / 58.79% / 64.72% on the five grossed
lanes and at 100% on the two exempt slices, so the open segment is structurally
absent. Absence of a zone reads as absence. A narrower band would read as less money,
which is the lie.

**JW's rationale for the basis choice:** what leaves the Medicaid dollar is the wisdom
readers want, and the federal figure is not built to communicate it.

**Not carried into the paper:** the stronger claim that CBO's basis is designed to
obscure. CBO scores federal because its remit is the federal budget, and the same
document publishes the detail this analysis depends on. The defensible sentence is
that the federal figure is the one that circulates and understates what leaves the
system, so a reader working from headlines has part of the picture. S-003.

## D-50 · The exemption is a property of a slice, not of a lane

S-038 was written after D-39 and D-41, when the whole directed payment lane was
exempt. **D-46 split it**: $102.0B provider-financed stays exempt, $47.4B
general-fund-financed grosses up to $73.2B. Any lane-level encoding rule will be wrong
on §71116 the day it renders.

Corrected figures: the exempt block is **$284.7B, 32.1% of the overlay** — not
$332.1B / 37.4% as S-038 records.

## D-51 · Composition partition renders on the lane trunk only

The five destinations already carry their own textures (D-15). A band carrying a
destination texture *and* a federal/non-federal hatch is two texture systems in one
shape, and the fan-out is where it turns to noise. This is where JW's
too-busy concern actually bites.

Partition on the trunk, before the fan-out; destination texture owns everything after
it. Composition is a property of where the dollar left, destination of where it
landed. One shape, one encoding each. Preferred over reducing the partition's
contrast, which would cost legibility to buy tidiness.

## D-52 · Container encoding: open edge, no fill, fixed-width crossings

Resolves S-039. Container sits around the **State band in the STATE GOVERNMENT
column** — the one place the state holds money as its own before it merges into the
$100.

- **Open edge.** Top and bottom rules dash outward and fade; there is no right-hand
  boundary. Nothing terminates, so there is nothing to measure against the $100. This
  is preferred to a closed box with a "not to scale" caption, which invites the
  eyeball comparison and then denies it in small type.
- **No fill, cool outline.** Warm is reserved for HR-1 loss (S-026) and the container
  is not a loss. An unfilled frame also cannot read as a band, because every band in
  this diagram is a filled area.
- **One measured band inside**, carrying Medicaid's general-fund-financed share.
  Other claimants render as faint unlabelled marks: context, not flows.
- **Fixed-width crossings.** Both boundary arrows drawn at one width, stated on the
  artifact, so width carries no quantity anywhere inside the object.

## D-53 · The to-be gets a second balance line

The as-is carries $100.00 → $92.03 → $86.42 → $86.27. The to-be carries a parallel
warm readout beneath it showing the same $100 under HR-1. That readout is the sentence
the paper exists to produce and is a stronger close than any auxiliary exhibit.

---

## Correction carried from this session

**`ramp.py` and the overlay are in ten-year billions; the diagram is in dollars per
$100.** The existing master is per-$100 throughout, including the balance line, so the
overlay must be too. Earlier work this session in ten-year $B was in the wrong
currency and is superseded.

**Open data-layer gap.** Converting overlay lanes to per-$100 at the 2029 anchor
requires total FY2029 Medicaid spending as a denominator. It is not in the repo:
`STATE_SHARE_PER_100` is a share, not a base, and `ramp.py` reports billions. One
figure from CBO's Medicaid baseline. Not filled, per S-035.

## Reconciliation produced while working the encoding

Ten-year total computable removed **$1,080.2B** — federal **$886.8B**, state and local
**$193.4B**. The federal side closes on CBO's published total by construction; the
non-federal side is the sum of the five derived gross-ups. Candidate headline and a
standing balance check: if a future edit breaks composition, the $193.4B moves.

## Open at session close

1. Per-$100 denominator for FY2029 (above). Blocks the overlay render.
2. Bite-point mapping: which column each of the seven lanes peels from.
3. Whether the BENEFICIARIES pie panel survives on the to-be.
4. Carried forward from part 2: decompose the `ramp.py` provider tax weight; strike
   $325.6B from D-26; MMIS share (D-32); RHTP (D-31); §71119 ramp sensitivity;
   `build_sankey_dc.py` three-file emit.

---

# Overlay grammar — added after JW supplied `layered_hr1_overlay_1.png`

This section supersedes D-51 and the flat-bar treatment sketched earlier in the
session. Both were built without having seen the overlay schematic and got the object
wrong.

## D-54 · HR-1 loss travels; it does not stack

The overlay is a **mirror of the baseline's existing leakage grammar**, not a panel
attached beneath the diagram.

The baseline already peels leakage **upward**: a ribbon leaves a lane, crosses the
flow, and terminates in a small node with its label above it — plan administration,
cost sharing, uncompensated care, sitting under a divider rule marked NORMAL LEAKAGE.

HR-1 loss peels **downward** on exactly the same grammar: a ribbon leaves the lane it
is subtracted from, travels across the flow, and terminates in a node below a divider
rule marked HR-1 OVERLAY. Baseline geometry is untouched.

The mirror is the argument. Above the line is what the system has always lost. Below
the line is what HR-1 will take. A bar chart bolted under the diagram throws that away.

## D-55 · What the terminal nodes carry: where, why, how much

JW ruling. Each overlay node answers three things:

1. **Where the money is subtracted** — carried by the *departure point*, i.e. which
   lane the ribbon leaves and at which column it leaves it (the bite-point mapping,
   below). Not restated in the label.
2. **Why** — the mechanism, in plain language, as the node label (S-033).
3. **How much** — the figure, per $100 at the 2029 anchor.

**Consequence: D-15's five loss destinations are not the overlay's terminal nodes.**
"Care not delivered / paid out of pocket / absorbed by providers / unfunded state
pressure / federal offsets" answers *who ate it*. These nodes answer *where it was
subtracted and why*. A diagram can carry one set of terminal nodes without a second
fan, and JW has chosen the subtraction set. Where the who-ate-it question goes —
D-38's friction exhibit, a second fan, or dropped — is **open**.

## D-56 · Future tense throughout

The overlay is a **projection to 2029**, not a report of something that has happened.
All overlay copy — node labels, annotations, the second balance line, and the body
text describing them — is written in the future tense. "Will not become capitation,"
"reduces," "phases down." Not "cut," "lost," "was removed."

This applies to the whole to-be instance, not only the overlay bands, and pairs with
S-043: every figure on the to-be is modelled.

## D-57 · One texture system, and it means non-federal share

**D-51 is withdrawn.** It proposed partitioning on the lane trunk before the fan-out.
On a travelling ribbon there is no trunk-then-fan-out — the ribbon is the whole
journey — so the proposal does not apply to the actual object.

The real problem is that three encodings were competing for one channel:

- lane identity (per-ribbon texture, as in the schematic)
- destination identity (D-15's five textures)
- non-federal share (D-49's composition partition)

**Resolution: remove a system rather than add one.** Lane identity is already carried
unambiguously by the terminal node and its label directly beneath it, so per-ribbon
texture is redundant. Drop it. Texture then means exactly one thing.

**Encoding.** The composition partition runs **lengthwise along the ribbon** for its
full journey: solid warm on the federal side, open on the non-federal side, hairline
division between. The two exempt slices (provider tax limits, provider-financed
directed payments) run solid edge to edge, so absence of the open zone reads as
absence — D-49's rule, ported to a travelling ribbon.

## D-58 · Bite-point mapping — where each ribbon departs

Derived against the real geometry in `build_sankey.py`. Four bite points, not one.

| Departs at | Lanes | Why there |
|---|---|---|
| **STATE GOVERNMENT** | Provider tax limits | Shrinks the non-federal share before the $100 assembles. Only the federal match departs as loss (D-39); the displaced general fund obligation crosses into the container, which sits in this same column (D-52). |
| **STATE AGENCY** | Blocked senior enrollment rule (§71101) | MSP moratorium. MSP dollars are what the existing grey Medicare premiums arrow ($2.90) already represents, so this loss **rides an existing path** rather than opening a new one. |
| **DISBURSEMENTS** | Work reporting, six-month renewals, blocked Medicaid enrollment rule, everything else | Coverage and preserved-friction lanes. The dollar will never become capitation or a fee-for-service claim, so it must depart *before* the three lanes split — drawing it after would assert a lane split for spending that never happens. |
| **CLAIMS** | Directed payment caps (both slices) | Supplemental payments to providers ratchet toward Medicare rates. The general-fund slice returns money to the state, crossing back to the container right-to-left against the direction of flow. |

**What this buys the paper.** "HR-1 reduces Medicaid by about a tenth" is four
mechanisms hitting four parts of the system. A hospital CFO reads CLAIMS and STATE
GOVERNMENT; a state budget director reads STATE GOVERNMENT only; a plan reads
DISBURSEMENTS. Stakeholder differentiation falls out of the geometry instead of being
asserted in prose.

**Two soft spots, flagged not resolved.** "Everything else" is a mixed bucket — cost
sharing bites at CLAIMS, retroactive coverage at DISBURSEMENTS — and is placed whole
at DISBURSEMENTS rather than split on no evidence. And §71101 riding the Medicare
premiums arrow is inference from what MSP pays for; it is sound but CBO says nothing
about where a dollar sits in a flow diagram.

---

# Anchor-year dependency — data availability findings

Raised by JW at session close: the anchor year is not a decision the brief can make,
it is an external dependency on what CBO publishes. "We can't declare data into being."
Correct, and it reframes D-01.

## D-59 · The 2029 anchor was a real decision, not a misstatement

Verified against the record. `WHITEPAPER_BRIEF_APPEND_2026-08-27.md` opens with
**D-01 AMENDED** — $100 = 2029 baseline spending under prior law, not 2028 — because
the headline anchor moved to 2029 (D-22) and the ledger must sit on the same year.
D-08 was amended alongside it, D-11 moved to the 2029 counterfactual, D-23 set the
impact year at 2029.

JW's "2028" this session was a read-back of the stale in-place D-01 entry, not a
change of mind. S-044 is therefore understated: the brief was not merely stale, it was
actively misleading, and the error was caught only because the appends happened to be
grepped. Had they not been, a 2028 diagram would have been built on JW's own
instruction, sourced from his own superseded document.

## D-60 · The counterfactual is fixed by the score, not chosen

The P.L. 119-21 supplemental cost estimate states that it covers 2025–2034 **relative
to the January 2025 baseline**. That fixes the to-be denominator: it must be the
January 2025 vintage. The February 2026 baseline already incorporates HR-1 — CBO
lowered its 2026–2035 Medicaid projection to reflect the Act's provisions — so using
it would net the cut out of its own denominator. Basis discipline (S-013), not
preference.

## D-61 · There is no January 2025 Medicaid detail file

**Finding, and it constrains the to-be.** CBO's baseline detail series (publication
51301) has no January 2025 Medicaid vintage. Every other program in the series does —
SNAP, SSI, TANF, Pell, Social Security, SSDI. Medicaid runs June 2024 → **February
2026**. Consistent with HMA's note that the February 2026 release was the first
Medicare and Medicaid baseline publication since January 2025.

So the component detail (fee-for-service, managed care, Medicare premiums,
institutional long-term care, home- and community-based care, by year) is available in
neither usable form:

| Vintage | Basis | Problem |
|---|---|---|
| June 2024 detail | Pre-HR-1 — correct | Superseded. CBO's January 2025 revision raised the ten-year Medicaid projection by ~$817B / 12%. Component splits from June 2024 under a January 2025 total is a mixed-basis error. |
| February 2026 detail | Current vintage | Contains HR-1. Not the counterfactual. |

**What does exist at the right vintage is the aggregate.** January 2025 Budget
Projections (publication 51118) carries Medicaid outlays by fiscal year at the same
vintage the score is measured against. The per-$100 denominator is therefore
obtainable for **any** candidate year 2025–2035.

**Correction.** Earlier this session it was suggested that the baseline detail table
would convert much of D-11's held-constant structure into sourced values. That was
reasoning from the June 2024 file's contents without checking whether a January 2025
equivalent existed. It does not. **D-11 stands and S-043 stands**: the payer split,
provider nodes and beneficiary pie shares on the to-be remain modelled.

## D-62 · What actually settles the anchor year

Since the denominator is available for every candidate year and per-section annual
detail is published for **no** year (D-37), the year does not turn on data
availability. It turns on how much of the overlay is at full statutory effect.

**And 2029 is not obviously that year.** D-08 calls it "the first full-effect year,"
which is not true for at least two lanes: the provider tax safe harbour steps down in
annual increments, and directed payments ratchet toward Medicare rates annually. Both
run past 2029. `ramp.py` carries 0.40 and 0.25 for these lanes, and the provider tax
weight has an in-file comment stating 0.40 is not settled.

**Outstanding work to settle it — step 2, not started:**

1. Build the statutory phase-in table from the enacted text of P.L. 119-21: for each
   of the seven provisions, effective date, step schedule, and year of full effect.
   Sourceable from the law; not modelled.
2. Cross it against the candidate years. For each, compute the share of the ten-year
   overlay at full effect versus mid-ramp.
3. Choose. This step contains a directional judgment reserved to JW: how far past a
   reader's planning horizon to reach in exchange for a cleaner picture.

**Until step 2 is done, D-01's 2029 anchor should be read as provisional-pending-
verification rather than settled.** It may well survive; it has not been tested against
the statute.
