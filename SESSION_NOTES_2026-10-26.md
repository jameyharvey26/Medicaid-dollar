# Session, 26 October — the one-engine port begins

Nothing here is committed. JW is committing it.

## What this session decided

**ONE ENGINE** (JW, 23 Oct, confirmed 26 Oct). The browser renderer becomes the
source of diagrams and future paper diagrams are generated downstream of it.
The paper-generating system gets refactored to work that way, not the reverse.

Two audiences, and they are not the same user:
- ~10,000 **end users** of the web app who play with variables and build
  scenarios. They never author papers and **never get to nudge layout**.
- **Agilian consultants only**, who use the system to create papers. A nudge is
  a publishing act and belongs to a view, not to a scenario export.

Each view in the app has an official default set of configurations and data —
"reset to the paper" is the whole model that produced the published figures,
not just the numbers.

Also ruled this session:
- The DC strap's national-proxy clause was false and is replaced by what the
  panel actually draws. DC is no longer blocked from the picker.
- The canvas grows to its content in interactive mode; nothing is suppressed to
  fit a box. A band below the visible floor is drawn at the floor and
  **declared on the panel every time it fires**.
- Zoom by column, so a small lane can be read at its true proportion rather
  than only at a floor.
- Where the ledger, the engine and the paper disagree, **the paper's anchoring
  and termination are correct**.

## What landed

| file | state |
|---|---|
| `views.py` | edited — DC strap wording |
| `build_explorer.py` | edited — reads the paper from the repo, not from outputs |
| `gates.py` | edited — gate order fixed; three gates added |
| `teachingproof.py` | new — the teaching-loss gate |
| `teaching_register.json` | new — 591 strings, each with a verdict |
| `engine_texts.py` | new — headless engine render so the above can measure |
| `enginecrossings.py` | new — runs `crossings.report` against the engine |
| `geometry_export.py` | new — exports the spine to `engine/geometry.json` |
| `GEOMETRY_CONTRACT.md` | new — what the solver takes and emits |
| `engine/explorer_engine.html` | new — the engine |
| `engine/geometry.json` | generated — do not hand-edit |

Gate suite: **16 gates, 15 green**, `render_v8_0.py` honestly red on its two
v8.0 layout checks (D-107, out of this cycle). Verified from a clean clone.

Two ordering defects fixed and one of my own diagnoses corrected: reordering
`build_explorer.py` against `publish.py` could never have worked, because
publish requires the built explorer in its own `must`. `render_v8_0.py` writes
the paper into the repo and build_explorer now reads it there.

## Where the port is (GEOMETRY_CONTRACT.md §8)

1. Constants into a shared declaration — **done**
2. Contiguous stacking — **done**. This was the "janky drop-offs": bands had
   4–6px gaps, so a ribbon left a contiguous edge and arrived at an offset one.
3. `resolve_bite_order` for the ordinary peels — **done**
4. `fan_rows` / `_place` — **done**, including the two-stage relaxation, the
   non-monotonic fold search, pinned-not-keep-out fraud, and the renderer's
   label metric
5. `crossings.py` against the engine — **done**, see below
6. Pies — **not started**. Needs `beneficiaries.cell` exported from `sankey.py`
   first; the cross-tab is computed in the renderer and never leaves it.

## START HERE NEXT SESSION

`python3 enginecrossings.py` reports **1 crossing** on `national_2030_mixed`,
0 on the other two panels. It is a bug in my translation of `_place`, not in
the algorithm.

```
at (1592,1063)  Medicare Savings (602,724)->(2060,1186)
              x Directed payment caps (1300,702)->(1760,1186)
```

Both terminals land on y=1186 although their x-spans overlap, which `_place`
should forbid: `_ov(it.xb, it.xt, pz.xb, pz.xt)` is true, `pz.y_src < it.y_src`,
so the second should floor below the first at `y_of[pz] + pz.th + gap`. It does
not. Suspects, in the order I would check them:

- `y_src` is now a cross-fan **rank**, not a y. Peels charged at different
  columns are different fans and their source heights are not comparable, so I
  rank by terminal x. The ceiling branch still reads `y_src` as if it were a
  height; that may be the whole bug.
- The sweep relaxes gap 40 → 8 and returns the first arrangement with no
  warnings. A row pair that shares a height produces no warning, so nothing
  stops it.
- `_blockH` / `_labelW` use the engine's font metric, which must stay in step
  with what the halo actually paints — the Python comment records an amount
  sitting invisibly under another label's background while the solver reported
  25 units of clearance.

JW, 26 Oct: *"There are a lot of those kinds of problems."* Expect more of this
class once the first is fixed.

## Two things found while packaging, both fixed

- `teachingproof._root()` located the panels as `dirname(REPO)`, which is only
  `build.py`'s `OUT` when the repo sits at one particular path. On a clean
  clone anywhere else the gate reported every panel MISSING and told you to run
  `build.py`, which you had just run. It now reads the declaration out of
  `build.py` instead of assuming it. Worth knowing that `build.py`'s `OUT` is
  still a hardcoded absolute path.
- The register's verdicts depend on whether the fan solver folded a label,
  because a folded label is one string ("Six-month renewals −$0.75") where an
  unfolded one is two. A layout change can therefore move a string between
  ported and pending without anything being lost. Not wrong, but the burndown
  will wobble by one or two for layout reasons; don't read small moves as
  progress.

VERIFIED: full gate suite run from a clean clone with these files — 16 gates,
15 green, `render_v8_0.py` honestly red on its two v8.0 checks.

## Known divergences from the paper, deliberate or not yet closed

- **Right-edge constraint.** I added one to `_place`; the Python has only a
  left-edge test because its canvas was sized around the finished fan. If the
  paper starts taking diagrams from the engine, the Python probably wants the
  same test.
- **Paper names live in JavaScript.** "Other" vs "Everything else", "Medicare
  Savings rule suspended" vs "Blocked senior enrollment rule". The plate's
  terminal sub-label is what a reader sees and the paper is authoritative; this
  mapping belongs in the ledger, not in a renderer constant.
- **Report-don't-nudge is reversed in interactive mode**, on purpose, recorded
  in the contract §6.
- **Pies absent** — the whole right-hand third of the paper's panel.
- **The redistribution rule is still mine.** When a peel moves, the engine
  rescales the lanes proportionally and declares that on screen. The ledger's
  `reach` field may answer this properly and has not been worked through all
  twelve peels. This is the open modelling question, not a layout one.

## Teaching burndown

`teachingproof.py`: **257 ported of 591, 323 pending, 11 layout.**
Measured against the engine on `dc_2024`, `national_2024`,
`national_2030_mixed`. Declared only on `national_2030_holds` and
`national_2030_scales` — the engine has not been pointed at those.

The gate fired correctly twice this session on my own breakage: once when
splitting the toggles broke the harness, once when it demoted 25 strings I had
claimed as ported on the strength of the spike looking finished.

A string that is only a figure must match an element exactly; a string carrying
words may match the panel's reading surface. `$26.25` was passing as the
long-term-care pie total because the engine draws that same number as a service
band — same number, different object, and its own loss bar `−$2.89` failed in
the same breath, which is how it was caught.
