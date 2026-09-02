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

**4.1 Shared furniture. Its geometry never moves.** (S-060)

**4.2 Checkpoints:** $100 at 205 under the FEDERAL column, before federal and state
combine. Disbursed at 820. Claims paid at 1300. Health services delivered at 1760,
on the providers / beneficiaries boundary.

**4.3 Subtractions are charged to the column where the money leaves,** and RIGHT
ALIGNED to that column's right edge minus 8. A reader can drop a vertical line from
any outflow on the flow straight down to its figure. (S-061)

**4.4 Every subtraction carries a plain-language label** under the figure, in the
same voice as the flow labels.

**4.5 Colour:** line, dots and checkpoint values are BLACK (#111418). Ordinary
subtractions are GREY (#8e9298) ABOVE the line. HR-1 subtractions are the diagram's
warm red-brown (#8B5A5A) BELOW the line. Red is reserved for fraud on the flow and
is never used on the tracker.

**4.6 Type:** 36px checkpoint values, 25px checkpoint labels, 24px subtraction
figures, 12px subtraction labels, r=11 nodes. Fixed.

**4.7 Rows:** subtraction figure at by−58 and label at by−40 for ordinary; figure
at by+28 and label at by+46 for HR-1; checkpoint labels at by+80. Nothing is placed
between the value row and the line.

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
`outflows.py` declares geometry; `build.py` is the only entry point. No builder
forks another and no builder text-substitutes another. A new state edition is a
config. (S-064)

**6.5 A refactor that changes a pixel is not a refactor.** Render before, change,
render after, diff the PNGs, expect an empty difference bounding box.

**6.4 Nothing is added to a per-$100 artifact without asking whether it scales the
numerator and denominator together.** If it does, it is already absent and cannot
be put back. (S-058)
