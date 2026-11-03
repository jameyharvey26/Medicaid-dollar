# Next session — bring the District up to the national standard

Drafted by Claude on 2 November 2026 at JW's request, after the demo.
Edit it before you use it; it is a starting brief, not a specification.

The demo is done. The engine is committed at `f81da83` and tagged
`demo-2026-10-30` at the version that was shown.

## What "on par with national" actually means

Measured before writing this, by walking the ledgers:

| panel | figures | verified | measured | derived | modelled | absent |
|---|---|---|---|---|---|---|
| national FY2024 | 58 | **37** | 21 | 17 | 18 | 2 |
| national FY2030 | 65 | 0 | 0 | 18 | 45 | 2 |
| DC FY2024 | 55 | **0** | 26 | 11 | 6 | 12 |
| DC FY2030 | 84 | **0** | 8 | 16 | 42 | 18 |

Two findings worth having before anyone starts:

**The District is not behind on modelling.** DC FY2030 is 42 modelled of 84;
national FY2030 is 45 of 65. Proportionally the District is the *less*
modelled of the two. The to-be year is heavily modelled everywhere, which is
what a projection is.

**It is behind on exactly two things.** Nothing is verified — 0 of 139
District figures has been opened at source and signed, against 37 of 58 on
the national as-is. And there are 30 absent figures against the national
panels' 4.

So "catch DC up" is two jobs with different owners, and conflating them is
how this goes wrong.

## Job 1 — acquisition. Mostly NOT research.

The absences cluster tightly. Most of them are one missing figure wearing
several hats:

- **HSCSN's administration/margin split.** Blocks the whole MCO lane total on
  FY2024, because three plans publish it and one does not, and a sum of three
  presented as a total is a floor. HSCSN predates the managed care
  regulations, is not an MCO in the regulatory sense, files no comparable
  annual statement and has no Title XIX column. It reports to DHCF. Nobody
  has asked.
- **Dual and PACE retention.** No DC figure.
- **DHCF's exempt share of expansion adults.** Named in `tobe2030_dc.py` as
  the next acquisition. It is what puts the work-reporting band's ends on the
  default's denominator; until it exists the Arkansas and New Hampshire ends
  are not like-for-like.
- **QMB-only enrollees above 100% FPL.** Turns the seniors lane from an upper
  bound into a figure. DHCF holds it; the monthly enrolment report publishes
  the category as a single count.
- **DHCF's managed-care service split.** Would replace the national service
  shape on District dollars.
- **District renewal and reconsideration volumes.** Would replace the
  national administrative-burden rate on the paperwork lane.
- **Sizing for the three named District provisions** — LTSS home equity cap,
  legal immigrant eligibility, retroactive eligibility. None is sized. The
  immigrant provision is under preliminary injunction and contested.

**Be honest about this list.** Six of those seven are things DHCF holds and
has not published. No amount of web research produces them. The research
deliverable is a *better-evidenced acquisition request* — who at DHCF, which
report, what exactly to ask for — not a number.

**The one that IS research:** the District's own four-year Medicaid
trajectory. `DC_ENGINE_TODO.md` item 6 says the FY2026 PROPOSED budget
Executive Summary volume is the one place it might be, and that it is
UNCHECKED. That is a real, closeable target. Check it first.

## Job 2 — documentation parity. Fully doable here.

National has `ENDNOTES.md`, a generated register where every figure carries
its statute, Federal Register cite, CBO reference and decision id. The
District has `DC_PROVENANCE.md`, which is a narrative trail, not a register.

Bring the District to the national shape: a generated DC endnote register,
from the `Fig` records already in `ledger_dc_2024.py` and
`ledger_dc_2030.py`. The provenance is already attached to the figures — it
is the register that does not exist.

While you are there, `AFTER_THE_DEMO.md` carries four open items from the
engine session, including one JW says I got wrong. Read it.

## The rule that matters most if agents run in parallel

Absence is drawn, never estimated (S-108). A session told to "catch DC up"
will want to fill gaps, and an agent team will want it more.

**The deliverable is a shorter list of absences with named sources against
them — not fewer absences on the plate.** A figure that moves from ABSENT to
MODELLED without an acquisition behind it has made the panel worse while
appearing to make it better. If you cannot source it, say "this is not
published and we are pursuing it", name who holds it, and leave it absent.

Nothing is signed by an agent. `verified` is "YYYY-MM-DD initials" and the
initials belong to a person who opened the source.

## How JW works

One question at a time. Show the picture before any layout claim. Recommend
on methodology, ask on direction — and when you ask, give the options and
your recommendation, not a bare question. Derive in code, never type an
output. Commit at close, not mid-session. Challenge him if a request does not
make sense; he would rather be told no than agreed with.

Plain English about what he would see. Not counters, not metrics, not tool
names.

## Where to start

    git log -1 --stat
    AFTER_THE_DEMO.md        four open items from the engine session
    DC_ENGINE_TODO.md        every assumption currently on the plate
    DC_PROVENANCE.md         what is checked and what is not

Do not run the gates. They take minutes and rebuild the paper.
