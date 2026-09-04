# How to commit — 2026-08-27, session 2 part 2

Use `SAVE TO GITHUB.command` in the repo folder. Read the diff before confirming.

| File | Action | Note |
|---|---|---|
| `fmap.py` | **NEW** | Per-lane FMAP rates. Raw CMS-64 quarters embedded so rates recompute. |
| `WHITEPAPER_BRIEF_APPEND_2026-08-27c.md` | **NEW** | D-43 through D-47, closed task tables. |
| `HANDOFF_2026-08-27c.md` | **NEW** | Session handoff. |
| `EDITORIAL_STANDING_NOTES.md` | **REPLACE** | Append-only. S-036 to S-039 added at the bottom. 318 lines in, 363 out. |
| `financing.py` | **REPLACE** | D-46 resolution of the tax-vs-IGT split. Comment and print changes; no value changed. |

Note the `c` suffix. There are already `...-2026-08-27.md` and `...-2026-08-27b.md`
files from earlier sessions today. Do not overwrite them.

## Sanity check before confirming

    python3 fmap.py
    python3 financing.py
    python3 ramp.py

- `fmap.py` prints the four derived rates (64.72 / 90.06 / 88.05 / 58.79) and the
  seven-lane table with five rates, one "no gross-up", one "split".
- `financing.py` prints the second ledger opening and no longer prints a BLOCKING line.
- `ramp.py` still totals 90.15. It is unchanged this round.

If any number moved in `ramp.py`, stop.

## Suggested commit message

    FMAP table and basis reconciliation closed; second ledger restructured

    - D-43 expansion lanes at 88.05% not 90% (VIII group is not uniform)
    - D-44 QI carve-out zero on structural grounds (capped allotment)
    - D-45 use CBO deficit series throughout; task 2 closed
    - D-46 directed payment lane splits two ways; $25.8B state relief
    - D-47 state general fund is an unsized container, government/state cell
    - S-036 recommend on methodology, ask on direction
    - S-037 CBO basis wording is inconsistent; check the sum not the verb
    - S-038, S-039 two open encoding risks recorded
    - fmap.py: per-lane rates derived from CMS-64 FY2024 primary data
    - Confirms D-26's $325.6B came from CRS, not CBO; strike it

## After committing

Refresh Project Files from GitHub. They were 318 lines behind at session start.
