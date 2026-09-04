# Session manifest — 2026-08-29

## New modules (the refactor)
| file | what it is |
|---|---|
| `sankey.py` | the renderer. `render(cfg) -> (baseline, overlay)`. All drawing, once. |
| `instances.py` | one `Instance` per artifact: ledger, steps, HR-1 terminals, tracker, titles. |
| `outflows.py` | column boundaries and the outflow ledger. Geometry declared once. |
| `check.py` | conservation gate. Runs before drawing; failure stops the build. |
| `ledger_2030.py` | FY2030 post-HR-1 ledger computation. |
| `ledger_dc.py` | DC FY2024 ledger, reduced fidelity, absences declared. |
| `build.py` | the only entry point. `python3 build.py [2024\|2030\|dc]`. |
| `build_pair.py` | stacked comparison sheet, now four panels. |

## New analysis
| file | what it is |
|---|---|
| `phasein.py` | statutory phase-in table for P.L. 119-21 and the anchor-year cross. |
| `tobe2030.py` | FY2030 numerator, denominator and per-$100 lane split. |

## New documents
| file | what it is |
|---|---|
| `STYLE_GUIDE.md` | binding diagram rules. A violation is a defect, not a preference. |
| `ARCHITECTURE.md` | state series and vantage views. Ledger / View / Layout seam. |
| `ENDNOTES.md` | numbered endnote register, EN-1 to EN-40. |
| `PAPER_PASSAGES.md` | publication-voice prose written as findings land, P-01 to P-03. |
| `MANIFEST_SESSION.md` | this file. |

## Deleted
`build_sankey.py`, `build_tobe_2030.py`, `build_sankey_2030.py`, `_gen_*.py`.
The text-substitution fork is gone (S-064).

`build_sankey_dc.py` is KEPT. It is not superseded: it is the named-plan DC
diagram, which is a different product and the prototype for the vantage layer
(S-070). It is no longer the DC state artifact.

## Renders
`national_2024_*`, `national_2030_{holds,scales,mixed}_*`, `dc_2024_*`,
`national_pair_2024_2030.png`, `sheet_national_dc.png`.

## Decisions and notes added
D-63 split overhead · D-64 bite phases · D-65 provider tax sources federal ·
D-66 the state artifact is the national view.
S-051 through S-072.
EN-1 through EN-40. P-01 through P-03.

## Verification
Refactor proven a no-op: `national_baseline.png` and
`national_2030_mixed_combined.png` both diff to an empty bounding box against
pre-refactor renders. All three instances pass `check.py`.


---

# Session manifest — 2026-09-03

## Changed
| file | what changed |
|---|---|
| `sheet.py` | NEW. Generalised N-panel comparison sheet. Replaces `build_pair.py`. |
| `build.py` | now calls `sheet.py` instead of `build_pair.py`. One line. |
| `STYLE_GUIDE.md` | 6.3 names `sheet.py`; new 6.3a on N panels and no rescaling. |
| `graffle.py` | NEW. Exports a rendered instance SVG to an OmniGraffle document. |

## Deleted — these must be removed, not overwritten
| file | why |
|---|---|
| `build_pair.py` | superseded by `sheet.py`. |
| `reference_renders/national_pair_2024_2030.png` | stale. No builder produced it after `build_pair.py` moved to four panels. Now regenerated on demand as `sheet_national_pair.png`. |

## New renders
`reference_renders/sheet_national_pair.png`, `reference_renders/sheet_overhead.png`.
`sheet_national_dc.png` rebuilt, byte-for-byte unchanged.

## Verification
`sheet.py` proven a no-op on the default set: `sheet_national_dc.png` diffs to an
empty bounding box against the pre-change render (S-064 standard, STYLE_GUIDE 6.5).
Full `python3 build.py` clean; all four instances pass `check.py`.

## Corrected this session
Overhead-scales sensitivity was recorded as $77.91 in D-63, EN-17 and the
`sheet.py` panel caption. The build returns $77.8498 and always has. Verified by an
independent recomputation from `tobe2030.per100` and the FY2024 base reproducing all
three variants to four places, so the build is right and the record was wrong.
Corrected to $77.85, spread $0.57. Origin of $77.91 not reconstructible and not
guessed at. New standing note S-073 on hand-carried figures; the caption rule folds
into S-066.


## OmniGraffle export
`python3 graffle.py national_2030_mixed` -> `reference_renders/national_2030_mixed.graffle`.
333 objects: 100 rects, 84 beziers, 16 lines, 4 circles, 129 text. Element count
reconciles against the SVG exactly, no silent drops. SVG groups become OmniGraffle
layers `baseline` and `overlay-hr1`, so HR-1 can be switched off.

Export only. Nothing is ever read back from a .graffle into the ledger: a figure
that can be typed over in a drawing tool is not a sourced figure (S-073). Markup
comes back as instructions and lands in `sankey.py` or `instances.py`.

Verified by reading the plist back, reconstructing SVG from the stored bounds and
UnitPoints, and re-rendering: geometry matches the original. NOT verified inside
OmniGraffle itself, which is not available in this container. The specific
unverified item is whether OmniGraffle reads Bezier `UnitPoints` in the same
[start, c1, c2, end, ...] order this writes.


## Fan layout — no avoidable crossings (STYLE_GUIDE 2.9)
`outflows.fan_tiers` / `fan_rows` / `fan_crossings` added. `instances.hr1_term`
drops its hand-assigned row and is now `(terminal x, sub)`; terminal Y is solved
per render. `sankey._draw_hr1` calls the solver and ASSERTS zero crossings, so a
crossing fails the build. `build.py` now rebuilds every sheet in `sheet.SETS`,
which it had stopped doing when `all` became the default set.

Before: 8 crossing pairs among the five state-agency tributaries. After: 0, no
layout warnings. Detector self-tested against the old hand-assigned rows: it
reports the crossing they produced.

Change is confined to the FY2030 panel: sheet diff bounding box (318, 2393, 2273,
3015). FY2024 and DC panels bit-identical.


## Rule 2.9 extended to ALL outflows
The first pass applied it only to `_draw_hr1`. Ordinary outflows were on a separate
path with hardcoded terminals and never went through the solver.

- `outflows.resolve_bite_order` — Administration and Medicare premiums peel from
  the same trunk edge; whichever terminates higher now peels first. Fixes a
  crossing present on all three diagrams.
- `sankey` — each peel records its OWN origin. Medicare's origin was read off
  administration's step, which is what made the order un-swappable.
- `fan_rows` — pinned participants. Documented fraud enters the solve with a fixed
  terminal so tributaries can be capped ABOVE it, not just floored below it.
- Provider keep-out boxes narrowed from bar +/-70 to bar +/-8; the padding was
  pushing terminals down needlessly.

Verified with a geometric detector (`xdetect.py`, sampled bezier centrelines,
segment intersection). Before: ADMIN x MEDI on all three, plus FRAUD x 2 HR-1
ribbons on FY2030. After: zero on national_2024, all three FY2030 variants, and
dc_2024.

OPEN: the directed-payment-caps and documented-fraud LABEL blocks are now adjacent
and cramped, and the DPC terminal sits close under the Rx drugs bar. Uncrossed but
not yet comfortable. Not touched further without JW.


## Rule 2.9 scoped to the margin (2.9c)
`crossings.py` added: geometric gate over every render. Derives the main-flow body
envelope from the render's own lane colours and counts intersections only outside
it. Joins (ribbons handing off at a shared endpoint) are not crossings.

Reads 0 in the margin on national_2024, all three FY2030 variants, and dc_2024.
The dual-retain / MCO-care crossing is correct and retained under 2.9c.

DELETED: `reference_renders/national_2030_{combined.svg,combined.png,baseline.svg}`
— stale, from before the overhead variants; no builder produces them and
`crossings.py` was reporting against them.


## Tracker rebuilt as a ledger (STYLE_GUIDE 4, rewritten)
`tracker.py` NEW: lattice, slot assignment, invisible sub-columns, balance/bite
placement, row de-collision. `sankey.py` tracker block replaced. `instances.py`
gains `subs_spec` — the subtraction ledger (label, amount, class, charged column,
short name) — from which BOTH the tracker slots and the tributary terminals derive,
so they cannot disagree.

FY2024: 4 balances (205, 820, 1300, 1970), 3 bites (560, 1060, 1560).
FY2030: 7 balances, 6 bites, state agency subdivided.
Fraud recharged from CLAIMS to PROVIDERS — providers receive it. Its tracker
amount is now red, having been grey while red on the flow.

## Session close
Full `build.py` clean. `crossings.py` reads 0 in the margin on all five renders.
`check.py` passes on all instances.

OPEN, not fixed: on FY2030 the bite short names still overlap the phase names at
that density. FY2024 is clean. Agreed with JW to fix when FY2030 is taken up.
