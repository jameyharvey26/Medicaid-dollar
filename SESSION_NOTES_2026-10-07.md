# Session handover — 2026-10-07, DC cycle

Gate state at close: **14 green, `render_v8_0.py` red on its two known checks**
(page 9 stranding, three `fig6_taper_all.svg` leaders). That is your expected
state, and it now reproduces from a CLEAN CLONE rather than only from a warm
working copy — see gates.py below.

Everything here was verified with the full suite after each change.
`renderproof.py` is green, so **no national panel moved**.

---

## Copy these over

### `modified/` — replaces the file of the same name at repo root

| file | what changed |
|---|---|
| `gates.py` | `build.py sensitivity` moved ABOVE `renderproof.py`. |
| `ledger_dc_2024.py` | Basis constants removed; now imports them from `basis_dc`. No figure changed. |
| `view.py` | `payer_rows()` rule change; new `collapse_payers` field. |
| `views.py` | New `V_DC_2030` appended. Nothing existing touched. |
| `compose.py` | Calls `V.payer_rows(L)` and passes named rows through. |
| `instances.py` | New `payer_rows` field, defaulted, additive. |

### `new/` — new files at repo root

`basis_dc.py`, `fmap_dc.py`, `tobe2030_dc.py`, `ledger_dc_2030.py`,
`placeholder.py`

### `archive/v8_0/` — new directory at repo root

The MHPA ship, frozen. Register and reference renders as shipped, plus a README
recording their known state. Nothing in it is to be regenerated.

---

## The three defects found and what was done

**1. `renderproof.py` red on a clean clone — NOT a moved panel.**
Six national panels reported MOVED. The committed `reference_renders/` SVGs for
the holds and scales variants are stale; rebuilding them reproduces the blessed
register byte for byte. `renderproof` ran at position 3 and `build.py
sensitivity`, the only thing that rebuilds those panels, ran at position 7. On
your warm tree a previous session had left fresh files, which is why you saw 14
green and a clean clone saw 13. Fixed by reordering. Same defect class as the
two already documented in `gates.py`.

**2. `ledger_dc_2024.py` and a future `ledger_dc_2030.py` would have carried
two copies of the denominator.** Extracted to `basis_dc.py`, the move D-83 made
nationally. Gates confirm the DC panel did not move.

**3. Named DC payers kept disappearing.** `View.expand` was opt-in, so any new
view started collapsed and no gate could object — the ledger was intact and the
drawing was merely poorer. Decomposition is now a property of the data: if the
ledger names the payers, the panel carries them. A view must now say
`collapse_payers` explicitly to draw an aggregate band.

---

## DELETIONS — not executed

Nothing was deleted. One script, matching the repo convention, is included:

**`DELETE STALE REFERENCE RENDERS.command`** — removes the six committed
sensitivity SVGs from `reference_renders/`. They are the only panel SVGs
committed in that directory and they predate the blessed register. The script
carries the sha256 evidence that rebuilt files match the register while the
committed ones match neither, refuses to run unless `archive/v8_0/` is in place,
and tells you what to run afterwards. Safe: `build.py sensitivity` regenerates
them identically.

The gate reorder already fixes the false red on its own. This closes the other
half — a generated file that is committed will go stale again.

**Second item, no script, needs a judgement call rather than a command.** The
provenance comment blocks in `ledger_dc_2024.py` for figures that now live in
`basis_dc.py` were left in place. It is one fact with two declarations and the
next person will edit the wrong one. Recommend trimming them to a pointer, but
that is prose and yours to word.

## State of the DC 2030 work

`ledger_dc_2030.py` stands, composes and renders. `dc_stacked.png` shows DC
FY2024 and DC FY2030 together.

**One measured lever.** Directed payment caps, **$97.04M, 1.63 per $100**,
against the national 0.85 — roughly double. Everything else about it is
modelled.

**Correct an earlier number if it reached anyone:** the "four to five times
national" figure from earlier in the session was wrong. It divided a 2030
numerator by the 2024 hundred. Double is the honest figure.

**The stack of assumptions, in order of how much they move the answer.** Say
this out loud before the panel goes to anyone:

1. Grandfathered base $485.2M — DHCF's planning assumption, per JW.
2. FY2030 hundred $5,950.7M — DC's FY2024 actual grown at 5.272%, the
   prior-law rate implied by the national model's own counterfactual. Derived
   in code from `basis_national.HUNDRED_M` and `tobe2030.TOTAL_30`.
3. Prior-law FY2030 flow — FY2024 composition held, level grown. Every trunk
   and lane figure on the 2030 panel is this assumption.

Each is declared on the ledger and each is a single visible constant.

**Six of seven tributaries are ABSENT** with reasons and acquisition targets.
`placeholder.py` gives them violet geometry carrying no value;
`forbid_in_shipping()` refuses any artifact containing one.

**OPEN, worth $48.5M.** The first year of the directed payment phase-down. CMS's
approval letter gives DC's rating period as the federal fiscal year, which makes
FY2029 the first affected period and FY2030 the second — two steps. DHCF's own
deck says FY2028, which would make it three. Not resolved by assumption. On the
acquisition list.

**OPEN, possibly larger.** HR-1 freezes provider taxes to those "imposed as of
4 July 2025." CMS approved DC's FY2025 directed payment policy on 9 September
2025. Whether a tax approved after the cutoff is "imposed as of" it may govern
whether DC keeps the programme at all, not merely how fast it phases down.

---

## Next, in order

1. **`sankey.py`: subdivide the payer band.** The seven named rows reach the
   Instance; the renderer still draws three aggregate bands. Pure renderer work
   now, data already in place. Two rows are under half a dollar — look at the
   render before believing any label fits.
2. **`compose.py`: consume placeholder geometry.** The six absent levers draw
   as $0.00 hairlines instead of violet bands.
3. **Held figures need the violet treatment too.** On the 2030 panel every
   figure except $1.63 is a carried FY2024 share. "$40.30 MCO capitation" under
   a 2030 heading reads as a projection. The declaration says otherwise but the
   figure talks louder.
4. One layout warning persists: blocked-enrollment terminal block overruns the
   1140 floor by 7px.

---

## Session-close items

**Early-reader feedback is still PARKED.** Restating as standing practice:
(a) "so what do we do" — the paper is descriptive, no implications drawn; its
home is "What comes next". (b) cost-of-care context missing — price,
utilization, coding intensity, acuity mix post-unwinding. (c) weaponization
risk — the overhead band invites "cut MCOs"; the answer is an FFS-vs-MCO admin
counterfactual, not advocacy. (d) inflation — shares unaffected, levels and
per-enrollee figures need a stated deflator. Standing recommendation: keep the
paper neutral, put the MHPA value argument in a separate companion brief.

Item (d) is no longer hypothetical: `tobe2030_dc.DEFLATOR_STATED = None` sits
in the code as the open question, because the FY2030 hundred is built on a
growth rate that blends real and price growth.

Conference feedback from 2026-10-06: audiences asked about the cost side. Your
call was to defer to a future version and add a scope-boundary statement in the
footnotes next cycle.

**Repo privacy:** public by your deliberate choice since 2026-10-06 so sessions
can pull. Re-privatize?
