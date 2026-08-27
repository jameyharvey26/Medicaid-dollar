# Commit — 2026-08-27

Repo: `JameyHarvey26/Medicaid-dollar`, branch `main`.

## Three files

| File | Where it goes | Action |
|---|---|---|
| `build_sankey.py` | repo root | **overwrite** |
| `EDITORIAL_STANDING_NOTES.md` | repo root | **overwrite** (already merged — do not paste by hand) |
| `WHITEPAPER_BRIEF_APPEND_2026-08-27.md` | repo root | **new file** |

`EDITORIAL_STANDING_NOTES.md` is the complete file: the existing 132 lines plus new notes
S-025..S-032. Overwriting is correct.

The brief append is kept as a **separate file**, not merged into `WHITEPAPER_BRIEF.md`,
because it amends five existing decisions (D-01, D-06, D-08, D-11, D-14) and supersedes two
of its own (D-22, D-24, D-28). Folding it in means editing decisions already on the record —
an Executive Producer call, not an automated merge.

## Steps (GitHub Desktop)

1. Copy the three files into your local `Medicaid-dollar` folder. Replace when asked.
2. Open GitHub Desktop — three changed files, one of them new.
3. Check the `EDITORIAL_STANDING_NOTES.md` diff: **additions only**. If any existing line
   shows as deleted, stop.
4. Commit with the message below, then **Push origin**.
5. Set the repo back to private: Settings -> General -> Danger Zone.

## Commit message

    Layer separation, resvg pin, and HR-1 modelling decisions

    - build_sankey.py emits three files on an identical viewBox: combined,
      baseline-only, overlay-hr1-only. Baseline and overlay are sibling <g>
      groups; the baseline file carries display="none" on the overlay, so it
      holds no HR-1 content and is safe to circulate.
    - viewBox registration assertion across the three emits.
    - Render step moved into the build script and pinned to resvg_py, hard exit
      if absent. cairosvg ignores paint-order and erodes the pie percentage
      halos. Width 2600px.
    - Standing notes S-025..S-032.
    - Brief append: D-22..D-38 plus amendments to D-01, D-06, D-08, D-11, D-14.
      Lanes now follow CBO's scored sections rather than public salience;
      interaction scaling dropped as unnecessary; friction exhibit added.

    Source of record for all HR-1 figures: CBO Supplemental Cost Estimate for
    P.L. 119-21, Title VII, Subtitle B, Chapter 1, 28 October 2025.

    No ledger value changed. Baseline balance line unchanged:
    100.00 -> 92.03 -> 86.42 -> 86.27.

## Rebuild

    pip install resvg-py
    SANKEY_OUT=. python3 build_sankey.py

## Where this picks up

Five open research tasks are listed at the end of the brief append. The critical path is
the statutory effective-date ramps per section — without them the 2029 allocation can't be
built, and without that the overlay stays empty.
