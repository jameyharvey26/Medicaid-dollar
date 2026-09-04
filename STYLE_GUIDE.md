# Diagram style guide

Binding on every artifact in the project: national and state, as-is and to-be.
Written 2026-08-29 after a run of corrections that were all the same correction.

The point of this file is that none of the rules below should ever need to be
given again. If a render violates one, that is a defect, not a preference.

---

## 1. The spine

**1.1 Columns are the spine.** Every x position on the page derives from a column
boundary in `outflows.py: COLS`. Terminals, tracker checkpoints, right-aligned
figures and label anchors all key off them. Nothing is placed by eye.

**1.2 Column boundaries are frozen across all instances.** 110 / 300 / 560 / 820 /
1060 / 1300 / 1560 / 1760 / 2180. A reader comparing two artifacts must find the
same column in the same place.

**1.3 Scale is frozen.** One dollar is the same number of pixels in every artifact,
so bands can be compared by eye between diagrams without adjustment.

---

## 2. Outflows

**2.1 Declare before drawing.** Every outflow is declared in `outflows.py` with its
source column, source edge and terminal column. Geometry is never written twice.
This file exists because Medicare premiums drifted into two different treatments in
two builders and nobody noticed for three sessions.

**2.2 Tributaries run downstream.** An outflow departs at its bite point and
terminates to the RIGHT of it. Never backward, never straight down, never detached.
(S-055)

**2.3 Direction carries class.** Ordinary leakage peels UP and to the right. HR-1
loss peels DOWN and to the right. Left-to-right is not negotiable for either.

**2.4 Flush attachment.** A tributary of thickness t leaving an edge at y spans
(y − t) to (y). The ribbon and the step down are the same pixels. (S-057)

**2.5 The return exception, and it is the only one.** An outflow may curve back to
an earlier column ONLY where the money genuinely returns there. Medicare premiums
is the sole current case: it peels flush off the top edge like any ordinary
outflow, then returns to the federal lane with an arrowhead. `ret=True` in the
ledger. Everything else is downstream. (S-062)

**2.6 Check each terminal against its own bite x.** Not against the general
left-to-right feel of the row. This has been got wrong twice. (S-057)

**2.7 Terminals stay inside their column.** Fraud terminates ON the providers /
beneficiaries boundary and does not cross into the beneficiary column, because
providers are who receive it. A terminal that spills into the next column is
claiming something about that column.

**2.8 Outflow paths do not tangle with node bars.** Drop clear of the fan early
rather than cutting across it.

**2.9 No avoidable crossings.** Tributaries leaving a common edge must not cross
one another. Their vertical order at the source is set by their bite x; that order
is preserved all the way to their terminals. Terminal heights are SOLVED at render
time by `outflows.fan_rows`, never hand-assigned — hand-assigned rows are how the
FY2030 fan came to cross itself in five places. A crossing that survives the solver
fails the build.

Two tributaries whose x-spans do not overlap cannot cross, so they may share a
height. Labels sit to the right of their terminal by default and flip left only
where that buys height. Terminals also clear declared keep-out boxes for furniture
already on the canvas, so a tributary never lands on a node label.

**2.9b The rule governs EVERY outflow, not just HR-1.** It was first written for
the HR-1 fan and that was a mistake: administration and Medicare premiums crossed
on every render of both diagrams for weeks. Where terminals are free the solver
moves them (`fan_rows`); where terminals are pinned and the sources are free it
moves the bite order instead (`resolve_bite_order`), which is the same invariant
solved on the other axis. An outflow whose terminal is already fixed — documented
fraud — enters the solve as a PINNED PARTICIPANT, never as a keep-out box: a
keep-out can only push a neighbour down, and the right answer is sometimes to push
it up. That distinction is what let directed payment caps cross fraud.

**2.9c The rule is scoped by REGION, not by element.** It applies to a tributary
only once it is out in the MARGIN above or below the flow body. A ribbon leaving
from the middle of the stack has to cut across whatever sits between it and the
edge, and that crossing is the flow working, not a defect: dual-plan
administration crossing the MCO care lane on its way up is correct and stays. A
band is not a tributary for the purpose of this rule until it reaches the margin
to terminate early. `crossings.py` derives the body envelope from the render and
counts only intersections outside it.

**2.9a This rule governs declared outflows, not the main lanes.** In the CLAIMS
column every payer lane is pinned at both ends — a fixed origin and a fixed
provider node — and the two orderings genuinely disagree. Those crossings cannot be
removed by reordering anything, and they should not be: the tangle is the finding.
The rule exists to remove crossings that are artefacts of layout, not crossings
that are facts about the money.

---

## 3. The flow narrows

**3.1 Every subtraction steps the flow.** One step per lever, at that lever's own x,
in ledger order. Not one cliff at a column edge. (S-056)

**3.2 Ordinary steps the top edge down. HR-1 steps the bottom edge up.**

**3.3 The width test.** Cover everything right of any x. The width of the river
there must equal the running balance on the tracker below it.

**3.4 Where a lever takes part of a stacked band, the gap is the point.** Provider
tax limits leaves HALFWAY DOWN THE SLOPE of the federal share, so the slice can be
seen coming out, and the federal band is drawn in two segments to make that
visible. The state band does NOT slide up to close the space. The gap that opens
from the midpoint onward IS the federal match that will never be drawn. It
terminates right aligned on the state government / state agency boundary. (D-65)

**3.5 Step x positions for administration and Medicare premiums are fixed at 615
and 715 in every instance.** They are far enough apart that the Medicare return
curve clears the administration band. HR-1 bottom steps interleave around them and
must never displace them. Moving those two is what fouled the FY2030 return path.

---

## 4. The bottom tracker

Rewritten 2026-09-03 (JW). The tracker was four fixed milestones with subtractions
annotated around them. It is now a running ledger. Everything in the old 4.1-4.7
is superseded.

**4.1 A dot only where a number changes.** 2024 lights four balances, 2030 lights
seven. Nothing is padded to make the two match; the gaps ARE the comparison.

**4.2 Two kinds of dot, alternating: balance, bite, balance, bite.**
BALANCE dots are the running total and are ALWAYS BLACK — dot, value and
percentage — however the bite that produced them was coloured. BITE dots are
coloured by class and carry their amount above and a short name below, both
centred on the dot, never on the span.

**4.3 Classes carry colour, everywhere they appear.**
HR-1 brown #8B5A5A · admin grey #5c6169 · fraud red #b23a32.

**4.4 The lattice.** A bite is charged to the column where the money leaves the
flow. Its BITE dot sits at that column's left edge and its BALANCE dot at the
right edge. Fixed ends: $100 at the centre of the FEDERAL column, health services
delivered at the centre of the BENEFICIARY column. The delivered dot carries the
last bite, so the final figure is printed once, and it is the most important dot
on the artifact.

**4.5 Invisible sub-columns.** A column carrying k bites divides into 2k-1 equal
steps, giving 2k alternating slots. No rule is drawn for the subdivision. At k=1
it collapses to the column's own edges. This is what lets a future year carry any
number of bites without breaking the cadence.

**4.6 A balance lands strictly between its own bite and the next.** It takes its
sub-column's right edge when that falls clear, and the midpoint when it does not.
Without this the plain rule stacks a balance dot on the following bite dot.

**4.7 Three rows below the line, each with one job:** phase name, then percentage
lost beneath it, then bite short names on their own row. Sharing a row breaks as
soon as a year has more bites in it.

---

## 5. Type and colour on the flow

**5.1 Plain language leads, section numbers follow.** (S-033)

**5.2 Future tense on the to-be.** (D-56)

**5.3 Modelled values are flagged** on the artifact and in `ENDNOTES.md`. (S-012)

**5.4 Every figure on an artifact has a numbered endnote before it ships.** (S-054)

**5.5 Palette:** federal blue, state pale blue, the green trunk, MCO teal, dual
purple, FFS slate, admin grey, fraud red, HR-1 warm #8B5A5A with #6f4747 nodes and
a 45-degree hatch. Grey dashed and hollow means memo, outside the ledger.

---

## 6. Working rules

**6.1 Run the build and look at the output before designing anything.** (S-040)

**6.2 Renders land in `reference_renders/`.** (S-041)

**6.3 One renderer, many instances.** `sankey.py` draws; `instances.py` configures;
`outflows.py` declares geometry; `sheet.py` stacks rendered panels for comparison;
`build.py` is the only entry point. No builder forks another and no builder
text-substitutes another. A new state edition is a config. (S-064)

**6.3a Comparison sheets take N panels and never rescale one.** A sheet is a list
of panel keys declared once in `sheet.py: PANELS`. Panels are pasted at native
pixel width, because horizontal register between panels is the entire reason the
sheet exists (1.2, 1.3, S-060). If two panels come back at different widths, that
is a renderer defect and `sheet.py` reports it rather than resizing to hide it.

**6.5 A refactor that changes a pixel is not a refactor.** Render before, change,
render after, diff the PNGs, expect an empty difference bounding box.

**6.4 Nothing is added to a per-$100 artifact without asking whether it scales the
numerator and denominator together.** If it does, it is already absent and cannot
be put back. (S-058)
