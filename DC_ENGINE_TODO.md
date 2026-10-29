# What the District panels assume, and what would replace it

Written 29 October 2026, when DC FY2024 and DC FY2030 went into the web
explorer alongside the two national panels.

JW's instruction for the demo was: where the District has no answer, assume it
works like the national model, draw it, say so, and keep a list. This is the
list. Everything on it is drawn on the plate today and every one of these
assumptions declares itself wherever it appears — in the panel's own notes, in
the engine's payload, and on the paper plate's declarations band.

Nothing here is signed. **No District figure in either panel has been opened
at source and agreed by a person.** Every demo carries that stipulation.

---

## 1. The leftovers lane carries a national number under a District label

**Worst one. Fix first.**

`DC provisions not separately scored` is drawn at the national `Everything
else` lane's share of each Medicaid dollar. Those are not the same quantity
and the lane is not a smaller version of the national one:

- Nationally the lane is a RESIDUAL — what CBO scored, less the named levers.
  A residual cannot be re-derived from District sources because it is a
  remainder rather than a thing.
- The District lane carries three NAMED District provisions instead: the LTSS
  home equity cap, the legal immigrant eligibility restriction, and
  retroactive coverage. None of the three is sized. The immigrant provision is
  under a preliminary injunction and its status is contested.

So the figure drawn is a placeholder with a national number on it.

**What replaces it:** a District dollar figure for each of the three
provisions, or a decision that the lane is drawn as absence and the engine is
taught to draw absence. The paper renderer already draws it as a violet
placeholder with no value attached; the engine cannot yet, which is the only
reason the number is there. Turning `assumed_levers` off in `ledger_dc_2030`
returns the honest panel today, and `engine_data_export` refuses to export it
rather than shipping a lane that reads as zero.

## 2. The paperwork lane is the national rate on District dollars

`Blocked Medicaid enrollment rule` is drawn at the national share of each
Medicaid dollar. The assumption is that the District's enrolment mechanics
behave like the national average.

There is no District figure and none is derivable from published sources: the
rule's effect falls on process — interviews, renewal alignment, the
reconsideration period, CHIP lockouts — and the people affected are those who
WOULD HAVE enrolled or stayed enrolled under easier mechanics. They are a
counterfactual, not a row in DHCF's enrolment report.

**What replaces it:** a District-specific administrative-burden estimate, which
would need DHCF's own renewal and reconsideration volumes. Nobody has asked
them.

## 3. The seniors lane is an upper bound

`Blocked senior enrollment rule` IS derived on District inputs — the District's
own QMB-only enrolment as a share of the national QMB-only count, applied to
CBO's score. Both counts are published, and they were checked to be the same
definition before they were divided.

But it is an upper bound, for a District reason. The District runs the QMB
group ONLY, at 300% of the poverty line against a federal floor of 100%. It
has therefore already enrolled much of the population a blocked federal
streamlining rule would have reached, so its true exposure is lower than its
share of enrolment implies. The band runs from the figure drawn DOWN to zero.

**What replaces it:** how many of the District's QMB-only enrollees sit above
100% FPL. DHCF holds it. It is not in the monthly enrolment report, which
publishes the category as a single count.

## 4. The service fan is the national shape on District dollars

Both District panels. The District publishes no managed-care spending by
service category, so the capitated rows are drawn on the national mix. This is
declared on the plate — SERVICE MIX ASSUMED, and `mix assumed` under every
capitated band — and it is one assumption, not two: FY2030 rescales FY2024's
fan rather than making a second one.

**What replaces it:** a District managed-care service split. DHCF does not
publish one; whether it holds one has not been asked.

## 5. The FY2030 shape is the FY2024 shape

Composition held, level grown. Every FY2030 lane and node is the FY2024 share
on a FY2030 hundred.

What that ignores, and these are real: the District's enrolment growth is
concentrated among people aged 65 and over; dual-eligible and PACE capitation
is rising far faster than the rest of the book; and the District enacted its
own eligibility reductions effective 1 January 2026. Each of those changes the
shape, not just the size.

## 6. The FY2030 hundred is modelled on a national growth rate

The District's FY2024 total grown at the prior-law rate implied by the national
model's own counterfactual. The District's own four-year trajectory was hunted
on 29 October and not found: DHCF's agency chapters, the FY2026 budget
testimony and slides, and the June 2025 MCAC presentation all stop at the
budget year.

**What replaces it:** the Executive Summary volume of the FY2026 PROPOSED
budget, which is the one place a District four-year Medicaid trajectory might
be. Unchecked.

## 7. The levers redistribute proportionally

When the HR-1 levers reduce the disbursement, every lane and every service cell
is rescaled by the same proportion, and the directed payment caps are spread
proportionally across the capitated leg.

That is the narrowest possible rule and it is declared on the plate, but it is
not right. A directed payment cap falls on hospital rates in particular, not
evenly across long-term care and pharmacy. The general redistribution rule is
still open across all twelve peels.

## 8. HSCSN is a year behind

Three of the four District plans are on their own CY2024 Title XIX reporting.
HSCSN is on CY2023. It predates the managed care regulations, is not an MCO in
the regulatory sense, files no comparable annual statement, and has no Title
XIX column to read. It reports to DHCF and that figure has not been chased.

Because of it, the MCO lane's administration and margin split is published as
ABSENT rather than as the sum of three plans, which would be a floor presented
as a total.

---

## Other things the engine still cannot do

- **Draw absence in the HR-1 fan.** The paper renderer draws a violet
  placeholder carrying no value; the engine would draw a zero. Until it can,
  `assumed_levers` has to stay on for the District's FY2030 panel to appear at
  all. `engine_data_export` refuses rather than exporting a blank lane.
- **The DC FY2030 paper panel is not blessed** and cannot be: `placeholder.py`
  refuses to ship a panel carrying a placeholder, and the engine's teaching
  text is gated against blessed panels only. `engine_texts.PANELS` therefore
  still has three entries, not four, on purpose.
