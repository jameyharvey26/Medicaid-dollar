# Next session — bring the District up to the national standard

Drafted by Claude on 2 November 2026 at JW's request, after the demo, and
revised once after he pushed back on the first draft's pessimism. Edit before
use; it is a brief, not a specification.

The engine is committed at `f81da83`, tagged `demo-2026-10-30` at the version
that was shown.

## What "on par with national" actually means

Measured by walking the ledgers, not assumed:

| panel | figures | verified | measured | derived | modelled | absent |
|---|---|---|---|---|---|---|
| national FY2024 | 58 | **37** | 21 | 17 | 18 | 2 |
| national FY2030 | 65 | 0 | 0 | 18 | 45 | 2 |
| DC FY2024 | 55 | **0** | 26 | 11 | 6 | 12 |
| DC FY2030 | 84 | **0** | 8 | 16 | 42 | 18 |

**The District is not behind on modelling.** DC FY2030 is 42 modelled of 84;
national FY2030 is 45 of 65. Proportionally the District is the *less*
modelled panel. A to-be year is heavily modelled everywhere; that is what a
projection is.

It is behind on two things: nothing is verified — 0 of 139 District figures
has been opened at source and signed, against 37 of 58 on the national as-is
— and there are 30 absent figures against the national panels' 4.

## The method this project already has for a missing figure

This is the important part, and the first draft of this brief got it wrong by
treating every absence as something to file a request about.

The work-reporting lever had no District figure. What was built instead:
CBO's national score read as a RATE, applied to the District's own expansion
spending for the default, with the only two real-world observations of a work
requirement at scale — Arkansas 2018 at 25%, New Hampshire 2019 at 40% — as
the band's ends. The range and the default both became the slider. The same
shape appears twice more: the seniors lane runs from its drawn figure down to
zero, and `MSP_EXPOSURE_BAND` is declared as (0.0, 1.0) with its meaning
written out.

**That is the pattern. Use it.** For each absence, the question is not only
"who holds the number" but "what is the most defensible band, what sits at
each end, what goes in the middle, and can it be a control?" An honest band
with named ends and a declared default is not estimation — it is this
project's own established way of drawing a quantity nobody has published.

What remains forbidden is a point estimate with no provenance presented as a
figure. A band whose ends are named observations is the opposite of that.

## Hunt harder, and wider

The first draft said no amount of searching would produce these. JW's push-
back: there are analogues, older vintages, presentations, and federal
collections that nobody has tried. He is right. Leads worth working — flagged
as leads, not as known contents:

- **T-MSIS.** The TAF research files and DQ Atlas carry eligibility group,
  service category and managed-care plan fields at state level. If DHCF
  reports it to CMS, it may be reachable without DHCF.
- **CMS unwinding data, 2023–24.** Monthly state-level renewal outcomes,
  procedural terminations, reconsideration volumes, published per state. This
  speaks directly to the paperwork lane, which currently carries the national
  administrative-burden rate.
- **Actuarial rate certifications.** DHCF's capitation rate development books
  routinely break rates by service category and carry an administrative load
  assumption. These are often public and would touch both the service fan and
  the admin/margin split.
- **EQRO annual technical reports** and **DC Council Committee on Health
  performance oversight pre-hearing questions.** Oversight responses often
  contain exactly the operational counts that published reports aggregate
  away.
- **`NAIC_ROUTE.md`**, already in this repo: Page 7 of the health annual
  statement, Title XIX column, priced at $13 a statement. Written for
  underwriting gain; re-read it for the dual and PACE lanes.
- **Other jurisdictions as analogues.** For an exempt share: Arkansas,
  Georgia Pathways and New Hampshire published exemption data. For QMB-only
  above the federal floor: other states that raised the MSP threshold.
- **Older vintages.** A 2019 figure with a stated basis beats an absence, if
  it is labelled as what it is.

**And one that is the existing method applied again.** The three named
District provisions — LTSS home equity cap, legal immigrant eligibility,
retroactive eligibility — are unsized, and the lane currently carries the
national residual's rate, which is a different quantity. If CBO scored any of
them nationally, the work-reporting construction applies directly: national
score as a rate, District denominator, declared band. That would replace a
placeholder with three derived figures and is the single highest-value thing
on this list.

## The absences, so the hunt has targets

- HSCSN's administration/margin split. Blocks the MCO lane total on FY2024,
  because three plans publish it and one does not, and a sum of three
  presented as a total is a floor.
- Dual and PACE retention. No DC figure.
- DHCF's exempt share of expansion adults. Named in `tobe2030_dc.py` as the
  next acquisition; it is what puts the work-reporting band's ends on the
  default's denominator.
- QMB-only enrollees above 100% FPL. Turns the seniors lane from an upper
  bound into a figure.
- DHCF's managed-care service split. Would replace the national service shape
  on District dollars.
- District renewal and reconsideration volumes.
- Sizing for the three named provisions above.
- The District's own four-year Medicaid trajectory. `DC_ENGINE_TODO.md` item
  6 records the FY2026 PROPOSED budget Executive Summary as the one place it
  might be, and as UNCHECKED. Cheap; check it early.

## Documentation parity

National has `ENDNOTES.md`, a generated register carrying each figure's
statute, Federal Register cite, CBO reference and decision id. The District
has `DC_PROVENANCE.md`, a narrative trail. Generate the District's register
from the `Fig` records already in `ledger_dc_2024.py` and
`ledger_dc_2030.py`. The provenance is attached to the figures already; it is
the register that does not exist.

`AFTER_THE_DEMO.md` carries four open items from the engine session,
including one JW says I got wrong. Read it.

## The rules that matter if agents run in parallel

Absence is drawn, never estimated (S-108). A band with named ends satisfies
that; a point estimate with no provenance does not. If the band cannot be
defended, say "this is not published and we are pursuing it", name who holds
it, and leave it absent.

Every new band declares its ends, its default, its basis, and whether the
ends are like-for-like with the default. The work-reporting band says its
ends are coverage loss among those subject while its default is a share of
expansion spending, and that they are not comparable until the exempt share
exists. Match that standard.

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
    tobe2030_dc.py           the band method, around RATE_BAND
    NAIC_ROUTE.md            a priced route somebody already worked out

Do not run the gates. They take minutes and rebuild the paper.
