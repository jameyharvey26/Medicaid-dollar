# Architecture: the state series and downstream views

Written 2026-08-29 in answer to two questions from JW: what is the right shape for
50+ state editions, and what is the right shape for views rooted further down the
pipe, such as a plan president's $100.

The short answer: those are **two different axes**, they need **two different
mechanisms**, and the mistake to avoid is treating the second as a special case of
the first.

---

## The two axes

**Axis 1 — geography and year.** Same structure, different numbers. National,
DC, New Jersey, FY2024, FY2030. The node set, the column order and the grammar are
identical; only the ledger changes. This is a **data** problem wearing a code
costume.

**Axis 2 — vantage.** Whose hundred dollars is it? Today every artifact roots at
the state agency and asks how the Medicaid dollar is divided. A plan president's
artifact roots at *their capitation* and asks where their hundred dollars came
from and where it goes. That re-anchors the denominator at a node in the middle of
the flow and expands the graph in both directions around it. It is **not** a config
change, because it changes what $100 means and which columns exist.

`instances.py` currently conflates the two. That was correct for two artifacts. It
will not survive fifty.

---

## The seam to cut now

Split `Instance` into three things that today are one.

```
Ledger   the numbers. Conserved. One per (geography, year, scenario).
           Geography- and vantage-independent. Knows nothing about drawing.

View     the framing. Root node, normalisation, which columns are expanded,
           which are collapsed, labels, titles. Knows nothing about sourcing.

Layout   the drawing. Column boundaries, step schedules, terminals, tracker.
           Already largely in sankey.py and outflows.py.
```

`render(Ledger, View) -> svg`. The national as-is is `View(root="state_agency",
normalise=100)`. The FY2030 to-be is the same View with an overlay. A plan view is
`View(root="plan:fidelis_nj", normalise=100, expand=["providers","upstream_financing"])`.

**Build the seam now. Do not build the graph engine now.** The seam is what makes
fifty states cheap; the re-rooting can wait until the plan product is real, and it
will be a change to `View` alone if the seam is right.

---

## Axis 1: what fifty states actually costs

Rendering is the easy part and is already solved. The work is elsewhere.

### 1. Provenance belongs to the number, not to a separate document

`ENDNOTES.md` is hand-written. At fifty states that is not maintainable, and S-054
("every figure on an artifact has a numbered endnote before it ships") becomes
either a lie or a bottleneck.

So a ledger field stops being a bare float:

```python
Fig(value=40.06, source="CMS-64 FY2024 national totals",
    vintage="FY2024", basis="total computable",
    status="measured", note=None)
```

Endnotes are then **generated** from the ledger. The register stops being a
document someone maintains and becomes a rendering of the data, exactly like the
diagram. A figure without provenance fails the build rather than shipping bare.

This is the single highest-value change on the list and it should happen before
state two, not after state ten.

### 2. Validation runs per state, automatically

Conserved-ledger purity is non-negotiable, and it currently rests on my reading the
output. At fifty states it has to be a test:

- every intermediate sums to its parts
- payer lanes sum to disbursed
- provider nodes sum to claims
- beneficiary shares sum to each node
- the tracker's running balance equals the flow width at each checkpoint
  (STYLE_GUIDE 3.3, currently an eyeball test, should be an assertion)
- no lane silently dropped between as-is and to-be

`check(ledger)` returns a list of failures. `build.py` refuses to emit a state
whose ledger does not balance.

### 3. Absent lanes must collapse, not render empty

Some states are fee-for-service only. Some have no dual-eligible plans. Some have
no state directed payments to cap. A zero-value lane must **disappear**, taking its
label, its node and its tracker row with it. It must not render as a hairline band
with a $0.00 label, and it must not silently rescale its neighbours without saying
so. The renderer needs an explicit "lane absent" path, and the artifact needs to
say the lane is absent rather than leaving the reader to infer it.

### 4. The FY2030 overlay is not uniformly scalable across states

This is the part most likely to be got wrong quietly, and it is a statute question
rather than a data question:

- **Work reporting** applies to the expansion group. Non-expansion states have
  little or no exposure on the largest lane in the whole overlay.
- **Provider tax phase-down** applies to expansion states only. Non-expansion
  states are frozen at July 2025 levels, not reduced (EN-6).
- **Directed payment caps** run to 100% of Medicare in expansion states and 110%
  in non-expansion states, and the number of annual steps depends on how far above
  Medicare that state's arrangements start (EN-7).
- **Six-month renewals** apply to the expansion group.

So a non-expansion state's to-be is **structurally different**, not proportionally
smaller. Scaling the national lane mix by a state's share of spending would be
wrong in a way that looks plausible, which is the worst kind of wrong. Each state's
lane vector has to be derived from that state's own expansion status, provider tax
position and SDP arrangements.

### 5. Fidelity will vary and must be declared

DC worked. Small states will not all have payer split, provider mix and
beneficiary shares at the same vintage. The architecture needs a declared fidelity
level per state, shown on the artifact, with a documented degrade path: collapse
the beneficiary pies first, then the provider fan, then the payer split. **Never
fill a gap with a national share applied to a state total.** That is a modelled
value wearing a measured value's clothes, and at fifty states nobody will remember
which ones were real.

### 6. One manifest, machine-generated

Fifty states times two years times three overhead variants is a lot of files.
`MANIFEST` should be emitted by `build.py`, listing every artifact with its
ledger hash, fidelity level, source vintages and build date. Not maintained by
hand.

### Practical order

1. `Fig` with provenance, and generated endnotes.
2. `check(ledger)`, wired into `build.py` as a gate.
3. Convert DC from `build_sankey_dc.py` to a `Ledger` + `View`. **It is the last
   fork and it is already drifting.**
4. A `states/` directory, one ledger file per state, plus the acquisition script
   that populates it from CMS-64 and T-MSIS.
5. Absent-lane handling and fidelity levels.
6. Then states in batches, expansion states first, because their overlay is the
   national one.

---

## Axis 2: views from further down the pipe

The Fidelis NJ example is a different product, and it is worth being clear about
why before any code is written.

### What changes

**The denominator moves.** $100 stops being Medicaid spending and becomes the
plan's capitation revenue. Everything upstream of the plan becomes an *inflow*
question, which the current diagram has never had to answer: which share of that
capitation is federal at New Jersey's FMAP, what share of New Jersey's non-federal
share came from provider taxes versus intergovernmental transfers versus general
fund, and what that means for the plan when HR-1 constrains those sources.

**The resolution shifts.** Upstream columns collapse; the plan's own downstream
detail expands. A plan president does not need six provider nodes; they need their
network, their high-cost categories, their medical loss ratio and their margin.
Administration stops being a $3.47 sliver and becomes a column.

**Competitors appear.** That is a new node class with no analogue in the current
model. It is also the most sensitive thing on the page.

### What that implies

The model has to become a **graph** rather than a fixed column sequence, and the
View has to carry a root plus an expansion policy. That is the real engineering,
and it is why the Ledger / View seam matters more than anything else on this page.

### Two things worth deciding early, because they are not technical

**Whose data is it.** A plan's provider mix, medical loss ratio and margin are not
public at useful resolution. T-MSIS encounter data is partial and lagged. Realistically
this is a **client-supplied-data product**: their numbers, our frame, our sourcing
for everything upstream of them. That is a different trust posture from the
national paper, and the conserved-ledger rules need a statement about how
client-supplied figures are marked, because they are neither measured by us nor
modelled by us.

**Competitor figures raise a publication question** that the national work has
never had to face. Worth settling before it is a live client conversation.

### Sequence

Do not build this until the state series is running. Everything the plan view
needs sits on top of a working per-state ledger, and building the vantage layer
first would mean building it against a model that is about to change under it.

---

## What must not drift

The whole point of this architecture is that these stay true at state fifty as
firmly as they are at state one:

- Column boundaries, scale and tracker geometry identical across every artifact
  (S-060, STYLE_GUIDE 1.2 and 1.3), so any two artifacts can be read side by side.
- One renderer, no forks (S-064).
- Every figure carries provenance and every modelled figure is flagged (S-012,
  S-054).
- No number invented to make a diagram balance (S-029).
