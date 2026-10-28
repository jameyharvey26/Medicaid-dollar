# Session notes, 27 October

## Where the port stands

The engine renders US×2024, US×2030 and DC×2024 at **zero crossings**, every
tributary anchored to the flow, and the teaching burndown unchanged at 257/591.
Gates: **18, all green.** `teachingproof.py` went green on its own when the
HR-1 labels became two lines — the register's verdicts never needed re-signing,
the plate needed to agree with them. `render_v8_0.py` is green because its two
real faults are now PINNED to their exact extent and written down in
RELEASE_v8.0_KNOWN_FAULTS.md, which travels with the paper. It turns red if a
fault is fixed, a new one appears, or a count moves.

## What changed, in one line each

- `GEOM` and `DATA` in the engine are written by exporters now. Do not hand-edit
  either line. See MANIFEST D-118.
- `anchorproof.py` is a new gate: every tributary must leave the flow.
- Clearance is solved by the curve (`dropFor`), not by pins. Contract §10.
- Public-company earnings is drawn, with the retention split behind it.
- The claims lane draws the lane × service cross-tab, not service totals.
- The ordinary outflows go through the same row solver as the HR-1 fan.

## JW's priorities for the next session

1. **Fill in the DC data**, as fast as it can be done. DC currently declares
   more absences than any other panel: no administration/margin split on plan
   retention, no dual or PACE retention figure, and no service mix at all —
   $36.37 of the claims column is drawn hatched and labelled ABSENT. Every one
   of those is a figure that exists somewhere and has not been found, not a
   figure that cannot exist.
2. **A draft FY2030 DC view.** There is no FY2030 DC ledger and the panel says
   so in as many words. The national FY2030 shape is explicitly not a stand-in:
   the District's own levers are measured for one provision and absent for the
   rest, so projecting the national shape would invent six figures nobody has.
   A DRAFT view has to say which of its numbers are modelled and which are
   measured, on the plate, in the same way absence is drawn.

Both are ledger work before they are drawing work. The channel exists now —
`engine_data_export.py` carries whatever the ledger holds — so a figure added
to `ledger_dc_2024.py` reaches the panel without touching the engine.

## Open, in the order I would take them

1. **The pies.** Step 6 of the port, still not started, and now the only thing
   the paper draws that the engine does not. `DRAWN_TO` in the engine clamps
   any terminal that would land past the provider bars into them — Medicare
   Savings and fraud both stop there. Delete that constant when the pies land
   and the ribbons go back to their full length.
2. **Point the engine at `national_2030_holds` and `national_2030_scales`**, so
   `teachingproof` measures five panels instead of three.
3. **The label metric.** What is left of §10. `_blockH` / `_labelW` approximate
   what the halo paints; labels are rectangles and the drop rule does not touch
   them. The Vaccines / Federal crowding noted in RENDER_DEFECTS is this.
4. **The redistribution rule.** Untouched this session. When a peel moves, the
   engine rescales the lanes proportionally and declares that on screen. Work it
   through all twelve peels before proposing anything.
5. **The handover.** Not yet. The engine still does not render every panel the
   paper does. When it does, flip the authority rule in GEOMETRY_CONTRACT and
   say so explicitly.

## A rule about published papers

A test that fails about a PUBLISHED artifact belongs in a readme beside that
artifact, not in the running suite (JW, 27 October). A permanent red costs more
than it is worth: every session reopens it, re-derives what it means, and
concludes what the last session concluded. Pin the fault to its exact extent so
the gate still notices a change, and write the explanation where the next
reader of the paper will find it.

Papers after v8.0 are generated from the engine, so faults of that kind become
properties of the generator and get fixed once instead of being carried in a
document.

## Rules this session added to the list

- **Look at every panel, not the one you are working on.** Pulling fraud out of
  the fan collapsed both FY2024 panels to an empty viewBox, and nothing caught
  it because the crossing detector does not read the viewBox. Found it by
  building a comparison page, not by testing.
- **A hand-typed input reads as an algorithm defect.** Every crossing chased on
  26 October looked like a bug in `_place`; none of them was.
