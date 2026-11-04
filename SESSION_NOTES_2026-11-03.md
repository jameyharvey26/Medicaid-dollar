# Session notes, 3 November

## What this file is for

`434b2d1` carries 5,983 lines of District work under a commit message about
`NEXT_SESSION_PROMPT_12.md`. The message is not wrong, it is incomplete: the
commit it was written for was reset and re-made with a session's worth of
staged work folded into it. Rather than rewrite a commit already on the
remote, the record is written down here. This file is the description
`434b2d1` should have carried.

## The headline, so it is not buried

**No ledger value changed.** `ledger_dc_2024.py`, `ledger_dc_2030.py`,
`basis_dc.py`, `tobe2030_dc.py` and `phasein.py` are untouched. Every figure
below is a decision recorded in `MANIFEST_SESSION.md` and a finding written up
in `DC_RESEARCH_2026-11-03.md`. **Nothing is drawn in `engine/explorer_engine.html`
and nothing is written into the paper.** The one engine artefact in this commit
is a preview copy, named as such.

**No District figure is signed. 0 of 139** — 0 of 55 on `DC24`, 0 of 84 on
`DC30`. `signatures.py` carries no DC entry. Measured says where a number came
from; verified says a named person opened the source and agreed with it.

**The gates were not run.** JW's instruction for this session was explicit.
Nothing here claims a green gate and nothing should be read as having passed
one.

## Decisions: D-118 to D-132

Fifteen, all in `MANIFEST_SESSION.md` under the 3 November heading, all
regenerated into `DECISIONS.md`. In brief:

- **D-118, D-119, D-120** — the District's leftovers lane stops carrying the
  national residual's rate and becomes three named provisions (§71108, §71109,
  §71112) as three derived figures, on CBO's 21 July vintage, positioned in
  FY2030 through the statutory step schedules rather than a flat spread.
  Closes `DC_ENGINE_TODO` item 1, the one marked "Worst one. Fix first."
- **D-121, D-122, D-130** — the work-reporting band gains a third named end
  (Urban's low-mitigation 55%), carries both denominators with the mismatch
  declared, and drives a medically-frail exclusion share from 10.0% to 21% so
  the new CMS frailty rule can be modelled in and out.
- **D-123, D-124** — §71102 splits into two lanes by mechanism, renewal
  automation and post-termination recovery, struck on FY2026 months from March
  forward. Closes `DC_ENGINE_TODO` item 2.
- **D-125** — the seniors lane defaults at 19% with a band to about 50%, and
  names DHCF's own count as the acquisition that closes it.
- **D-126** — the national panel gets its own service-mix declaration;
  `MIX_BORROWED` stays the District's claim. Closes `AFTER_THE_DEMO` §1.
- **D-127, D-128** — `PRIOR_LAW_CAGR` stands at 5.27% and `SUPERSEDED_BY` is
  closed; the FY2030 zeros in the dedicated-tax tables are read as a
  certification boundary, not a forecast. Closes `DC_ENGINE_TODO` item 6,
  negatively — the growth rate was checked and did not move.
- **D-129** — the §71109 status line carries three dated facts rather than
  resolving them, including the Washington-only injunction.
- **D-131** — `AFTER_THE_DEMO` §4 closed: $2.90–$5.40 was never a range.
- **D-132** — the beneficiary column leaves the frozen spine table and becomes
  an anchored but unsized surface. Closes `AFTER_THE_DEMO` §3.

`AFTER_THE_DEMO` §2 is untouched and still open.

## New files

| File | What it is |
|---|---|
| `DC_RESEARCH_2026-11-03.md` | The findings, with a numbered 20-document source register. |
| `DC_QUESTIONS_FOR_JW.md` | The questions as asked, with options and recommendations. |
| `DC_SIGNOFF_LIST.md` | Three tiers of items needing a named signature. |
| `dc_endnotes.py` | Generates `DC_ENDNOTES.md` from `Ledger.figures()`. |
| `DC_ENDNOTES.md` | 139 numbered entries. Generated — do not hand-edit. |
| `DC_ENDNOTE_KEYS.txt` | **APPEND-ONLY.** DC-EN numbers are this file's line positions. Delete it and every citation in every document becomes wrong. |

`dc_endnotes.py` is the District's parity with the national `ENDNOTES.md`
under S-054. The provenance was already attached to the figures; it was the
register that did not exist.

## The preview engine

`engine/explorer_engine_PREVIEW_2026-11-03.html` is a patched copy of
`engine/explorer_engine.html`, carrying a violet banner saying so. It draws
D-118's three provision lanes, D-123's two §71102 lanes, the extended
work-reporting band, and assumption detents under every slider that has them.

It also carries **two fixes to real engine bugs that live only in this copy**:

1. **Retention re-allocation.** Moving the MCO admin slider scaled every cell
   by a ratio, which made the Sankey drop in steps. It now carries a delta.
2. **The MCO claims fan.** Claims forked from the payer's running cursor
   rather than each plan's own, so an MCO's claims did not leave its own bar
   in its own colour. It now tracks per-plan and per-lane cursors separately.

Both are faults in the shipped engine. Porting them across is next session's
work and is not done here.

## Register repair

`DECISIONS.md` is generated wholly from `MANIFEST_SESSION.md`, and sessions
had been replacing the manifest rather than appending to it. Regenerating
dropped 40 entries. Recovered by backfilling them under dated headings;
verified idempotent. `MANIFEST_SESSION.md` now declares itself append-only.
`DECISIONS.md` stands at 55 decisions, highest D-132.

A latent fault in `decisions_index.py` is raised and not fixed: `max()` on an
empty sequence raises if a manifest yields no decisions.

## Raised, not fixed

- `peel.medicare` is signed at **2.9231** but **$2.90** is still typed in six
  places, including `ENDNOTES.md` EN-19 and EN-27. S-105 says derive, never
  type an output.
- `ledger_dc_2024.py` carries a service-mix comment comparing an FFS share to
  a total share.
- `DC_NAMED_PROVISIONS` overstates the §71109 injunction's reach.
- The national panels draw a negative absence, −$0.146 on FY2024 and −$0.142
  on FY2030. Pre-existing and identical in the unmodified engine. Untouched.
- `COMMIT_REVIEW_2026-11-03.html` was committed by accident in `434b2d1`. It is
  generated by a scratch script and goes stale as soon as anything upstream of
  it moves. Untracked and ignored in this commit; the file stays on disk.

## Still open from the research

`EXEMPT_SHARE` is narrowed but not bounded. Dual and PACE retention, and the
DHCF managed-care service split, are still absent. CBO workbook 61570 is still
unopened — the egress proxy refuses cbo.gov, and the allowlist request is
D-Q13 on the sign-off list.
