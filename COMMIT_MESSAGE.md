# Engine: stop hand-typing it, and the crossings go away

Three panels at zero crossings, every tributary anchored, 18 gates green.

## The root cause was never the solver

Every crossing chased on 26 October looked like a defect in `_place`, and none
of them was. Two declarations in the engine were maintained by hand — `GEOM`
and `DATA` — and the spine had drifted from `instances.T_SLOT` in three of
seven tracker slots, including an invented PROVIDERS slot the lattice does not
have. That is what sent directed payment caps downstream into the fan.

Both are written by exporters now. `geometry_export.py` rewrites the `const
GEOM` line; `engine_data_export.py` rewrites `const DATA` from the ledgers.
`exportproof.py` fails the suite if either drifts again.

## What the engine draws that it did not

- the lane × service cross-tab in the claims lane: which capitation lane pays
  for which service, which was in the payload and being thrown away
- public-company earnings, and the retention split behind it — and DC's
  declared absence of that split, drawn
- the trunk losing thickness as each cost leaves it, at the x it is charged
- the ordinary outflows through the same row solver as the HR-1 fan, including
  the two that return upstream
- the beneficiaries column, and provider bars at the paper's own width and gap

## Clearance is solved by the curve

`ctrlPair` front-loads a ribbon's fall; `dropFor` derives how much from what
that ribbon passes under. Row order was never wrong and a pin could only move
a terminal. The Medicare Savings pin is now inert in the engine and still read
by the paper.

## New gates

- `anchorproof.py` — every tributary leaves the flow, not white space
- `exportproof.py` — the engine declares nothing of its own

## Two detector defects, fixed

`crossings.envelope` left empty x buckets on wide bands and reported body
crossings as margin crossings. `ENGINE_BODY` was missing the engine's own
service palette.

## v8.0's known faults move out of the suite

`render_v8_0.py` was honestly red for a month over two real faults in a
published paper. They are documented in `RELEASE_v8.0_KNOWN_FAULTS.md` and
pinned to their exact extent in `gates.py`: green while that file is true, red
if a fault is fixed, a new one appears, or a count moves.

See `MANIFEST_SESSION.md` D-118 to D-123 and `SESSION_NOTES_2026-10-27.md`.
