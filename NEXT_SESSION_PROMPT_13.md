# Next session — clear the dangling issues, then the number line and the executive views

Drafted by Claude on 18 November 2026 at JW's request. Edit before use; it is
a brief, not a specification.

The repo is committed at `370c799`, three commits ahead of `origin/main` and
**not pushed**. Push before anything else, or `git log origin/main..main` to
see what is waiting.

Read in this order: this file, then `DECISIONS.md` from **D-133** down (it
runs to D-148), then `SESSION_NOTES_2026-11-03.md`. The three recent commits
carry long messages that are part of the record — `git log -3` is worth the
two minutes.

---

## Where things stand

Three sessions changed the model's spine:

**D-133.** The national lane allocation is READ from CBO's section-by-section
workbook (`cbo61570.py`), not modelled from statutory step schedules. D-37's
premise — that CBO publishes no per-section annual detail — was false. Four of
seven lanes had been mis-allocated by 34–55%, invisibly, because the chapter
total was normalised and always conserved. The published FY2030 figure moved
from $10.34 to $10.07 per $100.

**D-134 / D-136.** The $77.0B by which the workbook and the 28 October
supplemental differ is CBO's interaction netting among Chapter 1 policies. It
reconciles two ways to within $48M. A section-by-section sum overstates the
chapter by about 8% from FY2029 on.

**D-143 to D-145.** The District panel's two composite lanes are gone. Five
District-derived lanes replace them, `ABSENT_LEVERS` is empty, and the drawn
HR-1 total fell 10.3406 → 9.1833 per $100.

**What has NOT happened: nobody has looked at the rendered engine since the
port.** The five lanes are correct in the ledger and unverified on the plate.

---

## The dangling issues, in the order I would take them

### Blocking, because they hide other faults

1. **Run `anchorproof.py` on a machine with a working Playwright.** It drives
   the engine in a browser and the Cowork Linux VM cannot download one
   (D-142). It is the gate that confirms every tributary leaves the flow, and
   it has not run since the five new District lanes were added. Until it
   passes, treat the District FY2030 panel as unrendered. Run the full
   `gates.py` while you are there, not `--quick`.

2. **`teachingproof.py` fails and is meant to.** `_root()` was broken (D-138)
   and the gate was measuring an empty set, so it read green for weeks. Fixed,
   it reports **283 strings the teaching register does not account for**, 14 of
   them claimed as ported where the engine emits no such string. This is
   register debt, not a gate to re-pin — `EXPECT` was deliberately not updated.
   Decide whether to burn it down or to scope the register to what it can
   honestly cover.

3. **`ENDNOTES.md` is hand-maintained and D-133 moved the numbers under it.**
   EN-12 and EN-34 were amended in place per S-032 with the superseding
   decision noted, and **EN-34's balance line carries a CONFIRM AGAINST THE
   REGENERATED TRACKER marker** because it was amended from the ledger rather
   than from a re-render. Confirm it, then sweep the rest of the file: any
   entry quoting a FY2030 lane figure is suspect. A generator for `ENDNOTES.md`
   on the `dc_endnotes.py` pattern would end this class of problem.

### Leaks — numbers that can drift without anything noticing

4. **`DCBANDS` is generated from the ledger and pasted into the engine**
   (D-148). `engine_data_export.py` should emit the bands alongside `DATA`, the
   way `GEOM` and the panel figures already travel. Until it does, a ledger
   change silently leaves the bands stale. The same leak already cost us once:
   `IMPLIED` sat at 0.181112 after the rate moved, putting Arkansas and New
   Hampshire in the wrong places on a correct default (D-147).

5. **The provider tax lane has no band.** Its floor could not be reproduced
   from the current constants, so it was left out rather than typed. Recover
   the FY2027 step derivation or declare the lane bandless on purpose.

6. **`$2.90` is typed in six places** including `ENDNOTES.md` EN-19 and EN-27,
   against `peel.medicare` signed at **2.9231**. S-105 says derive, never type
   an output. Closed as a *range* question at D-131; the typing was never
   fixed.

### Smaller, but each one is a real fault

7. `ledger_dc_2024.py` carries a service-mix comment comparing an FFS share to
   a total share.
8. `DC_NAMED_PROVISIONS` overstates the §71109 injunction's reach. D-129 has
   the three dated facts; the prose does not match them.
9. `decisions_index.py` raises on `max()` of an empty sequence if a manifest
   yields no decisions.
10. The national panels draw a **negative absence**, −$0.146 on FY2024 and
    −$0.142 on FY2030. Pre-existing, identical in the pre-port engine, never
    diagnosed.
11. `engine/explorer_engine_PREVIEW_2026-11-03.html` is now fully superseded —
    everything in it is ported. Delete it, or it will be read as current.
12. A stray `Claude outputs/` folder sits untracked in the repo root from a
    mis-pathed write. Delete it.
13. `medicaid_dollar_explorer.html` and `explorer_data.json` are regenerated
    and untracked, as they have always been. Decide once whether that is
    deliberate and write it down.

### Still open from earlier, unchanged

- `AFTER_THE_DEMO` **§2** — three declarations living in two places. §1, §3
  and §4 are closed.
- `DC_ENGINE_TODO` items **3, 4, 5, 7, 8**. Items 1, 2 and 6 are closed; item
  1's closure is what D-143 implements.
- **D-130's medical-frailty control is not drawn.** The decision exists, the
  band exists in prose, the control does not.
- `EXEMPT_SHARE` narrowed but not bounded. Dual and PACE retention, and the
  DHCF managed-care service split, still absent.
- **0 of 151 District figures are signed.** `signatures.py` carries no DC
  entry. Measured says where a number came from; verified says a named person
  opened the source and agreed with it. This is the single largest gap between
  the District and the national panels and no amount of modelling closes it.

---

## The work JW actually wants: the number line and the executive views

### The number line

It already exists in three places and they are not the same thing:
`make_figs.py` emits `fig5_numberline.png` and `fig10_numberline_2030.png`;
`compose.py` and `instances.py` carry its configuration; `explorer.py` has its
own; and `GEOMETRY_CONTRACT.md` §1a freezes the **pie-to-number-line
alignment** on the beneficiary surface. "Wire it up" should mean one number
line, built from the ledger, used by the paper, the engine and the explorer —
the same move `geometry_export.py` and `engine_data_export.py` made for the
spine and the panel data.

Start by reading those four and writing down where they disagree. Do not start
by drawing.

Note D-132: the beneficiary column is an **anchored but unsized surface**. Its
left edge and the pie-to-number-line alignment are frozen; its width is a
renderer's choice. The paper draws 420 and the engine 200, and both are
correct. Whatever the number line becomes must hold under both.

### The executive views

**ASK JW WHAT THIS MEANS BEFORE BUILDING ANYTHING.** It is not defined
anywhere in the repo and it is the one item in this brief with no prior
decision behind it. Worth settling in the first ten minutes:

- Who is the reader, and what decision are they making?
- Is it a new panel, a new view of an existing panel, or a new artifact
  (deck, one-pager, a lens in the engine like the three already there)?
- Does it show the hundred, the taper, the levers, or the beneficiaries?
- National, District, or both — and if both, what happens to the panels where
  the District has no figure?

The engine already has three lenses on a panel (D-ae72184 era) and a place/year
pair of control axes. If the executive view is a fourth lens, it is cheap. If
it is a new artifact, it needs its own ledger path and its own gate, and that
is a different size of job.

---

## Rules that still apply

- **S-105**: derive in code, never type an output. Two live violations are
  listed above (items 4 and 6).
- **S-108**: absence is drawn, never estimated. The District panel now has no
  absent levers, which makes this easier to forget, not harder.
- **S-032**: `ENDNOTES.md` and `DC_ENDNOTES.md` are append-only and stably
  numbered. `DC_ENDNOTE_KEYS.txt` is the registry; DC-EN numbers are its line
  positions and documents cite them. **Never reorder or delete a line.**
- **S-054**: every figure on an artifact has an endnote.
- Nothing an agent produces is signed. `verified` is "YYYY-MM-DD initials" and
  the initials belong to a person who opened the source.
- A gate whose output has legitimately changed is a decision, not a nuisance.
  Update `EXPECT` deliberately and record it in `MANIFEST_SESSION.md`.
- `MANIFEST_SESSION.md` is **append-only**. It was replaced wholesale by
  successive sessions once and cost 40 decisions, recovered by backfill.

## Environment notes that cost time last session

- The Cowork Linux VM has no Playwright browser and cannot download one.
  `render_v8_0.py`, `anchorproof.py` and `engine_texts.py` all need one.
  `resvg-py`, `pymupdf` and `playwright` itself install from pip there; the
  browser does not.
- `cbo.gov` refuses the egress proxy for direct download. The workbook was
  retrieved through the in-app browser against the page's own origin. The data
  is transcribed in `cbo61570.py` and does not need fetching again.
- `git` cannot remove its own `.git/index.lock` in a connected folder until
  file deletion is approved for that folder. Approve it at the start of a
  session that will commit, or git leaves locks that break later commands.
