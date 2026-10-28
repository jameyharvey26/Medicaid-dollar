# Medicaid Dollars, National — v8.0: known layout faults

This file travels with the v8.0 paper. It is the record of what its own layout
gates say about it, so that nobody has to rediscover it, and so that nobody
treats a standing red as a new problem.

`render_v8_0.py` reports two faults on this release. Both are real, both were
known when it was packaged, and neither is being fixed in v8.0.

## 1. Page 9 strands seven lines

The left column of page 9 ends seven lines short against a threshold of six.
No other page is over.

This is a typesetting fault in the prose, not in a figure or a figure's
placement, and closing it means moving text on a page of a paper that has been
published. It is not worth reopening a release for one line.

## 2. Three leaders run through their labels on `fig6_taper_all.svg`

- a leader runs through "People who will not enroll"
- a leader runs through "Medicaid enrollment rule"
- a leader runs through "People who would have had a paid claim"

This is the label-metric fault. The placement solver measures a label as a line
of text; the renderer paints a rectangle behind it. The two disagree, so the
solver reports clearance where a reader sees a collision. The same fault shows
up in the engine, and it is on the open list there.

Fixing it properly means measuring a label once, as the shape that actually
gets painted, and using that measurement everywhere — the paper's figure code
and the engine both. That is its own piece of work, and doing it will change
this diagram.

## Why this is a file and not a standing red

`render_v8_0.py` exits non-zero on its own layout gates. A publisher that
refuses to write the PDF over that means the only route to a release is to
loosen a detector that is telling the truth, so the faults are reported and the
artifact is written.

v8.0 was the last paper assembled against a fixed layout. Papers after it are
generated from the engine, so a fault of this kind becomes a property of the
generator and gets fixed once rather than being carried in a document.

## What the gate suite does with this

`gates.py` pins these two faults exactly. The gate is GREEN while the output
says what this file says: one page over threshold, page 9, seven lines; three
leader faults across five diagrams. It turns RED if a fault is fixed, if a new
one appears, or if the count changes.

So this is not a suppression. It is an expectation, and the expectation is this
file. If the gate goes red, read it against this document and find out which
sentence here stopped being true.
