# How to commit this bundle

Repo: `JameyHarvey26/Medicaid-dollar`, branch `main`. Note the "26".

## What is in here

| File | Action | Note |
|---|---|---|
| `EDITORIAL_STANDING_NOTES.md` | **REPLACE** | Full file. Append-only content added at the bottom: S-018 amendment, S-033, S-034, S-035. Nothing above was edited. 249 lines in, 318 lines out. |
| `WHITEPAPER_BRIEF_APPEND_2026-08-27b.md` | **NEW** | D-39 through D-42, corrections to D-26 and `ramp.py`, task 1 status. |
| `HANDOFF_2026-08-27b.md` | **NEW** | Session handoff. |
| `financing.py` | **NEW** | Sourced financing assumptions. Run directly to print figures. |
| `SAVE TO GITHUB.command` | **NEW** | Double-click save script. Put it in the repo folder. See `SAVE_SCRIPT_SETUP.md` first. |
| `SAVE_SCRIPT_SETUP.md` | **NEW** | One-time setup for the script, in plain language. |
| `ramp.py` | **REPLACE** | Comment-only change. Two correction flags added. **No value changed; output is byte-identical.** |

Note the `b` suffix on the two dated files. There is already a
`WHITEPAPER_BRIEF_APPEND_2026-08-27.md` and a `HANDOFF_2026-08-27.md` from the
earlier session on the same date. Do not overwrite them.

## Before committing

Verify the diff shows what it should and nothing else:

    git diff --stat
    git diff ramp.py

`ramp.py` should show only added comment lines. If any number changed, stop.

## Sanity check

    python3 financing.py
    python3 ramp.py

`financing.py` should print the second ledger opening ($23.77 / $5.94 / $4.19 /
$1.40), the D-39 split ($4.75 recycled, $1.19 displaced), and a BLOCKING line about
the tax-vs-IGT split. That BLOCKING line is intentional, not an error.

`ramp.py` should still total 90.15 across seven lanes.

## Suggested commit message

    Financing model: D-39..D-42, second state fiscal ledger, FMAP table partial

    - D-39 provider tax lane splits by what the tax financed; exempt from D-25
    - D-40 second conserved ledger opening at the $35.30 state share
    - D-41 directed payments split three ways; tax-vs-IGT split blocking
    - D-42 second ledger carries relief as well as pressure
    - S-033 plain-language labels lead, section numbers secondary
    - S-034 medians do not aggregate; S-035 unsourced splits are None
    - S-018 amended: commit at session close with a running manifest
    - financing.py: sourced assumptions as named updatable variables
    - Flags D-26/ramp.py outlay-vs-deficit basis mismatch ($8.6B on 71119)
    - Flags ramp.py 0.40 provider tax weight as two blended mechanisms

## After committing

**Refresh Project Files from GitHub.** They were badly stale at session start:
standing notes 94 lines against 249, and a pre-refactor `build_sankey.py`. Reading
the stale copy has already produced one confidently wrong claim (S-031).

## After this, use the script

`SAVE TO GITHUB.command` replaces these instructions for future sessions. Set it up
once per `SAVE_SCRIPT_SETUP.md` and every later save is a double-click that shows you
the diff and asks before committing.
