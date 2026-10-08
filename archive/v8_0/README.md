# archive/v8_0 — the MHPA ship, frozen

v8.0 is the version shipped for MHPA and is FROZEN as of 2026-10-06. Nothing in
this directory is to be regenerated, re-blessed or edited. It exists so that
work on later versions cannot silently alter what was shipped.

## What is here

- `render_register/` — the blessed panel register as of 2026-09-28.
- `reference_renders/` — the panel SVGs as committed at the ship.

## Known state at freeze, recorded rather than fixed

Six files in `reference_renders/` are STALE relative to the register they were
blessed against: `national_2030_holds_{baseline,combined,overlay}.svg` and
`national_2030_scales_{baseline,combined,overlay}.svg`. Rebuilding them with
`build.py sensitivity` reproduces the register byte for byte, so the register
and the code agree and no national figure moved. Only the committed files were
stale.

They are preserved here AS SHIPPED. Do not regenerate them in this directory.
Removing them from the working tree is a separate decision and belongs on a
deletion list for JW, not here.

## What this does not cover

The paper, deck and explorer artifacts are not copied here. If v8.0's outputs
need to be reproducible from this directory rather than from the tag, that is a
further step and has not been taken.
