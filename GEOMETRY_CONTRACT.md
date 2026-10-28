# The geometry contract

Written 26 October, before any port code, because the last five rounds of
engine work were me reconstructing this layout from a picture and JW catching
what I got wrong — crossings, anchors, column gaps, ordering, the federal bite
anchored on the wrong band. Each fix revealed the next error because I was
converging on an appearance instead of executing the rules.

This file is the rules. It says what the Python solver takes in, what it emits,
and which parts are frozen. The port executes this; it does not approximate it.

ONE ENGINE means the browser runs this solver and the paper's diagrams are
generated downstream of it (JW, 2026-10-23). So the contract has to be
expressible in both runtimes, and anything in it that is secretly a Python
detail has to be found now rather than at render time.

---

## Which source wins — and this changes when the port finishes

**During the port, the paper wins.** Where the ledger, the engine and the
published diagram disagree on anchoring, termination or wording, the v8.0
FY2030 panel is correct and the engine is wrong. That is not because the paper
is inherently authoritative. It is because it is the only artifact that has
been reasoned through end to end, and the engine is a partial reimplementation
being brought up to it. A disagreement today is a port defect.

**Once the engine is working, this reverses.** The engine becomes the baseline
point of truth: new papers and new renders match the engine's internal logic,
and future paper diagrams are generated downstream of it — which is the whole
point of ONE ENGINE (JW, 2026-10-23). At that moment a disagreement between the
engine and a published panel means the panel is out of date, not that the
engine is wrong.

**The handover is when steps 1–6 of the port are done and the engine renders
every panel the paper does.** Until then, defer to the paper. After it, stop —
and in particular stop treating v8.0's hand-tuning as a specification. Some of
it (the staggered pie columns, the declared nudge at `sankey.py:958`, the
Rx-drugs 30-unit offset) exists because a human was correcting a renderer that
could not yet solve those cases. Once the solver handles them, reproducing the
workaround would be preserving a scar.

JW, 2026-10-26: *"Later once the engine is working, new papers and new renders
should match the internal logic of the engine as a baseline point of truth."*

---

## 1. The spine. Frozen, and not derived from anything.

`outflows.COLS` is the single declaration; `sankey.py` imports it rather than
keeping a second copy, which is S-096 and the reason D-87 once had to be
applied in two files that could have disagreed.

| column | x0 | x1 |
|---|---|---|
| FEDERAL | 160 | 350 |
| STATE_GOVT | 350 | 584 |
| STATE_AGENCY | 584 | 844 |
| DISBURSE | 844 | 1060 |
| PAYER | 1060 | 1300 |
| CLAIMS | 1300 | 1560 |
| PROVIDERS | 1560 | 1760 |
| BENEFICIARY | 1760 | 2180 |

`SOURCE_X = 200` (FEDERAL x0 + 40).

Canvas `W = 2200`. `H = 1416`, and unlike W and the scale, **H was never
frozen** — it has grown when a tributary needed the room. `cY = 540` is the
trunk's centreline. `bw = 18` is node bar width.

**Scale: `ys = 4.4` px per dollar.** One number, everywhere. This is what makes
the columns puzzle pieces: every band is its value times `ys`, so a column's
bands sum to exactly the node feeding it, and there are no gaps between
stacked bands. My engine inserted 4–6px between bands, which is the whole of
the "janky drop-offs" — the ribbon left a contiguous edge and arrived at an
offset one.

## 2. Ribbon shape

`ctrl_x(x0, x1) = x0 + min((x1 - x0) / 2, CTRL_MAX)` with `CTRL_MAX = 340`.

Half the run is right for a short hop and wrong for a long one: a tributary
crossing most of the page descends so gradually it rides at mid-height through
everything it passes and cuts the ribbons that stop short of it. Capping the
control distance makes a long run fall early, then travel flat and low, under
its neighbours. This single constant is doing a large share of the
crossing-avoidance work, and the engine has nothing equivalent.

## 3. Outflow declarations

Every peel is declared in `outflows.OUTFLOWS` with, at minimum:

- `cls` — `ordinary` (overhead, returns) or `hr1` (the law)
- `src` — the column it is charged against
- `edge` — `top`, `bottom`, or `fed_bottom`
- `src_x` — the x at which it leaves the trunk edge, or `None`
- terminal x, fixed by **which column the dollar would have reached**

`src_x` is a declaration, not a computed value. D-115: the band used to bend at
the midpoint of the gap while the tracker put the marker at the declared
`src_x` — two numbers for one point. **The declaration wins.**

## 4. The no-crossing theorem

From `outflows.py`, and this is the part I invented a worse version of:

> Tributaries in a fan leave a common edge, so their vertical order at the
> source is fixed by their bite x and is a TOTAL order. Only one end is pinned.
> Two ribbons cross exactly when their x-spans overlap and their vertical order
> flips between source and terminal, so preserving the source order everywhere
> removes every crossing. The constraints can never contradict each other and a
> fan has no unavoidable crossings.

Two solvers apply it on opposite axes:

- **`resolve_bite_order`** — ordinary peels. Terminals are pinned heights,
  sources are free. The x slots stay fixed and outflows are dealt into them in
  terminal-height order, topmost terminal first.
- **`fan_rows` / `_place`** — HR-1 tributaries. Terminal x is pinned by reach;
  terminal height is solved. Whatever stops sooner left-to-right must start
  sooner, or the fan folds back over itself.

**The claims fan is the exception and must not be "fixed".** Those lanes are
pinned at both ends — each payer lane has a fixed origin, each provider node a
fixed position — and the two orderings genuinely disagree. No reordering helps.
*The tangle is the finding.* `outflows.py` does not touch those, and neither
may the port.

## 5. Row packing

`_place` pushes a terminal below **only the terminals it actually conflicts
with**: below a ribbon whose x-span it overlaps, and below a label block whose
x-span its own label overlaps. Two tributaries far apart horizontally may share
a height. That is what keeps the fan shallow enough to fit above the tracker;
an earlier version that floored every row against every previous row
overflowed.

Pinned tributaries (documented fraud) take part in the ordering but never move.
They are participants, not keep-out boxes — an obstacle can only push a
neighbour down, and the right answer is sometimes to push it up.

Labels sit to the **right** of their terminal by default: reading direction,
and it keeps the label downstream of the bite like the ribbon. Flipping left is
a concession taken only when it clearly buys height.

What gives, in order, because the two cost the reader differently:

1. Row spacing relaxes `FAN_MIN_GAP 40` → `FAN_TIGHT_GAP 8`. Changes nothing
   about how a label reads.
2. Only then does the solver fold amounts onto names, **deepest row first, one
   tributary at a time**, because the compact form is harder to read and should
   be spent where it buys most.

The widest spacing with the fewest folded labels that fits, wins. If nothing
fits, the tightest arrangement is returned **with its warnings** rather than
silently overflowing.

Constants: `FAN_TOP 800`, `FAN_LABEL_H 45`, `FAN_LABEL_H_TIGHT 30`,
`RULE_Y 1146`, `FAN_FLOOR = RULE_Y - 6`, `FAN_STACK_TOP 806`.

## 6. Collisions are reported, not nudged — with a documented exception

`tracker.collisions()` detects and reports; `sankey.py` prints
`WARNING anchor labels overlap`. The marker rule places by geometry and does
not negotiate.

**This changes under one engine, deliberately** (JW, 2026-10-26). Report-only
works when a consultant iterates before anyone sees the panel. It does not work
for ~10,000 end users dragging sliders through layouts nobody has looked at. So
avoidance runs automatically in interactive mode and reports how hard it had to
work; declared nudges remain a publishing act and end users never get them.
Recorded here because it reverses a position the project took on purpose.

## 7. What the solver needs from a panel

From `render(cfg)`: `fed, state, admin, medicare, mco, dual, ffs, mco_ret,
dual_ret, earnings, adm_marg, mco_adm, dual_adm, mco_care, dual_care, node,
fraud, ffs_n, mcoc_n, dualc_n, gt, order, disp, oversight, fed_outside,
fed_bite, fed_bite_name, truncated, show_beneficiaries`.

Note `truncated` and `show_beneficiaries`: a heading over an empty column reads
as a column the drawing forgot to fill (D-109), so on a truncated panel the
heading is omitted and the absence stated below.

## 8. Port order, and what each step is checked by

1. **COLS, ys, bw, cY, ctrl_x** into a shared declaration both runtimes read.
   No behaviour change; `renderproof` must stay green.
2. **Contiguous stacking.** Bands abut. Column sums equal their feeding node.
   Checked by eye and by `crossings.py` once ported.
3. **`resolve_bite_order`** for the ordinary peels above the river.
4. **`fan_rows` / `_place`** for the HR-1 fan, including obstacles, pinned
   terminals, the two-stage relaxation, and the warnings.
5. **`crossings.py` against the engine**, the way `engine_texts.py` lets
   `teachingproof` measure the engine. Until this exists, no claim that the
   engine does not cross is worth anything — mine were made by eye and were
   wrong twice.
6. Pies last. They are a separate visualization and need
   `beneficiaries.cell` exported from `sankey.py` first.

## 9. Known hazards in the port

- **`renderproof` goes red across every panel** the moment geometry moves, by
  design, and is then blessed in bulk — which is exactly the window in which
  something is lost quietly. `teachingproof` exists for that window; keep it
  measuring.
- **The scale is one number.** Any floor on band height (the engine's minimum
  visible band) breaks `sum(bands) == node` and must be declared on the panel
  every time it fires, which is already the rule.
- **The paper's names differ from the ledger's.** "Other" vs "Everything else",
  "Medicare Savings rule suspended" vs "Blocked senior enrollment rule". The
  plate's terminal sub-label is what a reader sees and the paper is
  authoritative. CLOSED for the printed NAME on 26 Oct: `label` is declared in
  `outflows.OUTFLOWS`, exported, and read by the engine. The terminal
  SUB-CLAUSE is still a JavaScript constant (`PAPERCLAUSE`); it lives in
  `instances.hr1_term` on the paper side and has not been moved.
- **A hand-typed input reads as an algorithm defect.** Every crossing chased on
  26 Oct looked like a bug in `_place` and not one of them was. `REACHX`,
  `ANCH`, the bite x's and the HR-1 rule height were all typed into the engine
  instead of exported, and each wrong number surfaced as a ribbon crossing
  somewhere else entirely. Before touching the solver, check that what it is
  being fed came out of `geometry_export.py`.

## 10. MOSTLY CLOSED: clearance is measured along the curve now

**27 Oct.** The ribbon case is solved, and not where we expected. `_place` was
never going to fix it: the row ORDER was already right and a pin can only move
a terminal, not the curve between. What decides whether two ribbons cross is
how steeply the longer one leaves — and shortening its leading control point
does nothing, because the trailing one moves with it and the curve stays
symmetric.

The fall has to be made ASYMMETRIC. `ctrlPair(x0,x1,drop)` pulls both control
points up against the departure as `drop` goes to 1, so the ribbon dives at
once and runs flat the rest of the way. `dropFor` derives it per ribbon from
what that ribbon actually passes under: wherever it crosses the terminal of
something that stops sooner and sits higher, it must already be `CLEAR` units
below that terminal when it gets there. It takes the gentlest drop that
satisfies every such constraint, so a ribbon with nothing to clear keeps the
plate's default shape.

All three panels are at zero crossings with no pin doing the work.

What this leaves open, which is the rest of the old §10:

- The label metric. `_blockH` / `_labelW` approximate what the halo paints, and
  the Python comment records an amount sitting invisibly under another label's
  background while the solver reported 25 units of clearance. Labels, unlike
  ribbons, are rectangles and the drop rule does not touch them.
- `outflows.OUTFLOWS["Blocked senior enrollment rule"].term_dy`, the pin, is no
  longer load-bearing in the engine. Whether the PAPER still needs it is a
  question for after the handover, and removing it there is a decision, not a
  cleanup.

## 10a. HISTORICAL: `_place` measures clearance at the wrong place

`_place` keeps one terminal clear of another by comparing their TERMINAL
heights and flooring the second by `gap`. That is not where two ribbons
conflict. They conflict out along the curve — typically where the
longer-reaching ribbon passes the shorter one's terminal x, which may be a
thousand units upstream of its own terminal and far below the height the
solver compared.

Three things in this system are workarounds for that one gap:

- `outflows.OUTFLOWS["Blocked senior enrollment rule"].term_dy`, the pin. Its
  own comment says the solver "places by bite order and cannot know" that
  directed payment caps bites higher. A solver that measured the curve would
  know, and the pin could go.
- The right-edge constraint added to the engine's `_place` but absent from the
  Python, which has only a left-edge test.
- The label metric. `_blockH` / `_labelW` approximate what the halo paints, and
  the Python comment records an amount sitting invisibly under another label's
  background while the solver reported 25 units of clearance. Three labels on
  the engine's US×2030 panel currently sit over their own ribbons — visible,
  not reported.

**When to do it:** after the pies (§8 step 6) and after the engine is pointed
at `national_2030_holds` and `national_2030_scales`, so that five panels are
measured rather than three — a clearance solver is only as good as the cases it
is tested against. Do it BEFORE the handover declaration, not after: once the
engine is the baseline, a hand-tuned pin in the paper becomes a specification
rather than a workaround, and v8.0's hand-tuning is explicitly not that.

Estimated a day. It replaces the pin, the right-edge special case and the label
metric with one measurement, and it is the last thing standing between the
engine's fan and the paper's.
