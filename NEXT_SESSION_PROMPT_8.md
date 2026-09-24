Picking up the Medicaid dollar project.

Pull JameyHarvey26/Medicaid-dollar, branch main. Read `SESSION_START.md` and
follow it. Then read `MANIFEST_SESSION.md` from the 21 September entry down.
Where that entry and anything older disagree, the 21 September entry is newer —
say so rather than picking.

## This session is national, not DC

I am on a deadline with the national paper. DC is parked. Do not open the DC
panel, do not rebase the plans, do not start the source-column rendering work,
and do not ask me about any of it unless a national figure forces it.

If you need to know what state DC is in, the 21 September manifest entry
carries it. It is parked mid-stride on purpose and I know exactly where.

## What I want to know first

Tell me what state the national paper is actually in. v5.0 shipped to early
readers. Before I write against it I want to know what in it is still soft —
not a list of everything, the two or three things that would embarrass me if a
reader found them.

Start with the ones already named:

- `build.py` does not rebuild the FY2030 `holds` and `scales` variants in a
  working session, so they can sit stale and be blessed as if live. Run
  `build.py sensitivity` before `renderproof.py --bless`. Found 18 September,
  still not fixed, and I have now blessed renders twice since.
- The wrap-around ordering in the body text rests on a $55.1B / $6.2B split
  that lives in `build_xlsx.py`, not the ledger. S-073 exposure.
- The collections fold. `build_xlsx.py` spreads $15.2B pro rata across both
  lanes, in a comment, outside the ledger. Exhibit 17 declines to place
  collections at all. That is our assumption wearing a measurement's clothes
  and it is national, so it is in scope.
- The services table reads $87.07 against its own rows summing to $87.08.
  Note 8 carries both cents. My choice, reversible, do not reverse without
  asking.
- EN-43, the public-company earnings carve, deliberately unsigned.
- `legacy_mix=True` stays on. The seam has an absent-lane path and no
  absent-node path.
- The author page: one four-line bio on an otherwise empty page, 29 dead lines.
  The plan administration sentence from the deleted disclosure is still
  unhomed.

## Do not ask me about these

S-092 is closed and does not come back. Sheila's name, employer and bio are
still in the working record and the repo is still public. Out of scope unless
I say otherwise.

## The one thing I keep not deciding

The repo is public and v5.0 has gone to outside readers. You have raised it
twice. Raise it once more, early, with a recommendation and what it costs, and
I will decide.

## House rules

Pull, build, look at the diagram, then change something — in that order. Show
me the picture with any layout claim. One question at a time. Recommend on
methodology, ask on direction. Run the detector, not the eye — and when the
detector is wrong, fix the detector rather than the number it flagged. No
hand-carried figures. Commit at session close only.
