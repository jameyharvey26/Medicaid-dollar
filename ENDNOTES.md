# Endnote register

Numbered endnotes for the national whitepaper. **Every figure that appears on an
artifact has an entry here** (S-054). Entries are append-only and stably numbered;
if a figure changes, amend the entry in place and note the superseding decision
(S-032), never renumber.

Each entry carries: the claim as it appears to the reader, the source, the
vintage, the basis, and whether the value is **measured**, **derived** or
**modelled**. Modelled values are flagged on the artifact as well as here (S-012,
S-043).

`SOURCES.md` holds the document-level register and the URLs. This file keys
individual figures to those documents.

Status key: **M** measured · **D** derived from measured inputs · **P** modelled
projection · **OPEN** not yet sourced, must not be published as stated.

---

## A. The anchor year

**EN-1 · The to-be is anchored to federal fiscal year 2030. | D**
FY2030 is the first fiscal year in which every coverage provision of P.L. 119-21,
Title VII, Subtitle B, Chapter 1 is in force for every state for a full year.
Derived from the statutory phase-in table at EN-2 to EN-8. At FY2030, 62.6% of the
ten-year deficit effect is at full statutory effect, against 20.0% at FY2029.
See `phasein.py`. Decisions D-01, D-08, D-11, D-23 re-anchored; D-62 closed.

**EN-2 · Blocked senior enrollment rule (§71101): effective on enactment, 4 July
2025; no steps; full effect FY2026. | M**
Moratorium on parts of the CMS final rule "Streamlining Medicaid; Medicare Savings
Program Eligibility Determination and Enrollment," 88 Fed. Reg. 65230 (21 Sept
2023), running through the end of fiscal year 2034.

**EN-3 · Blocked Medicaid enrollment rule (§71102): effective on enactment, 4 July
2025; no steps; full effect FY2026. | M**
Moratorium on parts of the CMS final rule on streamlining Medicaid, CHIP and Basic
Health Program application, eligibility determination, enrollment and renewal
processes, 89 Fed. Reg. 22780 (2 Apr 2024), through the end of fiscal year 2034.

**EN-4 · Six-month renewals (§71107): renewals initiated on or after 1 January
2027; one step; full effect FY2028. | M**
Applies to adults eligible through the ACA expansion pathway. CMS Informational
Bulletin, 8 Dec 2025.

**EN-5 · Work reporting (§71119): states must impose from 1 January 2027; good-faith
exemptions expire no later than 31 December 2028; full effect FY2030. | M**
§71119(c), adding §1902(xx)(11)(C)(i) of the Social Security Act. An exemption may
not be renewed beyond 31 Dec 2028. CBO states that states may begin imposing the
requirement from 1 Jan 2027 but must do so by 1 Jan 2029.
**This is the finding that moves the anchor.** 31 Dec 2028 falls one quarter into
FY2030's predecessor year: FY2029 runs 1 Oct 2028 to 30 Sept 2029, so FY2029 is
three-quarters of a universal year for the largest lane. FY2030 is the first full
fiscal year in which no state can hold an exemption.

**EN-6 · Provider tax limits (§71115): applicable percentages fixed for fiscal years
beginning on or after 1 October 2026; expansion-state safe harbour steps down
0.5 percentage points a year; full effect FY2032. | M**
Schedule: FY2028 5.5%, FY2029 5.0%, FY2030 4.5%, FY2031 4.0%, FY2032 3.5% and
thereafter, from a 6.0% base. CMS Dear Colleague letter, 14 Nov 2025; CMS proposed
rule CMS-2452-P, 91 Fed. Reg. 46562 (23 July 2026). Nursing facility and ICF/IID
classes are exempt from the step-down, and non-expansion states are frozen at
July 2025 levels rather than reduced.
**Not decomposed.** The lane blends two mechanisms with different time profiles.
See EN-22.

**EN-7 · Directed payment caps (§71116): non-grandfathered payments capped for
rating periods beginning on or after 4 July 2025; grandfathered payments reduced 10
percentage points a year from the first rating period on or after 1 January 2028;
no statutory year of full effect. | M**
The reduction is 10 percentage points of the original grandfathered dollar amount,
non-compounding, continuing until the payment reaches 100% of the published
Medicare rate in expansion states or 110% in non-expansion states. CBO: payments
above Medicare rates may continue until fiscal year 2028, after which they must be
reduced 10 percentage points annually until they meet the cap. CMS letter of
2 Feb 2026; CMS proposed rule of 20 May 2026.
**The number of steps depends on how far above Medicare each arrangement starts,
which varies by state and provider class, so the statute fixes no year of full
effect.** Modelled at six steps (FY2033) in `phasein.py`; sensitivity at four and
eight steps is carried there.

**EN-8 · Everything else: mixed effective dates; modelled at full effect FY2030. | P**
Residual basket. Cost sharing (§71120) applies to fiscal years beginning on or
after 1 October 2028; alien eligibility (§71109) from 1 October 2026; retroactive
coverage (§71112) from 1 January 2027. Also carries CBO's netting of interactions
among all chapter policies. The residual is provisional; see `fmap.py`.

---

## B. The FY2030 ledger

**EN-9 · FY2030 HR-1 effect on the deficit: $108.152 billion, federal. | M**
CBO, Supplemental Cost Estimate, P.L. 119-21, Title VII, Subtitle B, Chapter 1, as
enacted 4 July 2025, published 28 October 2025, annual table. The same table gives
FY2030 estimated outlays of $111.441 billion and estimated revenues of $3.289
billion. Figures are identical to CBO's July 2025 estimate.
**Basis:** deficit, per D-45. The $3.289 billion wedge is forgone tax revenue from
take-up of employer coverage. It was never a Medicaid dollar and has no node on the
diagram. Chapter totals for 2025–2034 are outlays $914.634B, revenues $27.880B,
deficit $886.754B.

**EN-10 · FY2030 federal Medicaid outlays under prior law: $837 billion. | M**
CBO letter to Ranking Members Boyle and Pallone, 5 March 2025, Table 1, "Outlays
From Accounts Indicated to Be Under the Jurisdiction of the House Committee on
Energy and Commerce," data source *The Budget and Economic Outlook: 2025 to 2035*
(January 2025).
**Vintage is load-bearing.** The score at EN-9 is measured relative to CBO's
January 2025 baseline, so the denominator must be the same vintage (D-60). The
February 2026 baseline already incorporates P.L. 119-21 and would net the cut out
of its own denominator.
**This closes the aggregate half of the D-61 gap.** The component detail
(fee-for-service, managed care, Medicare premiums, institutional long-term care,
home and community-based services, by year) remains unavailable at the January 2025
vintage, because CBO's baseline detail series for Medicaid, publication 51301, runs
June 2024 to February 2026 with no January 2025 issue. D-11 and S-043 therefore
stand: the payer split, provider nodes and beneficiary pies on the to-be are
modelled.

**EN-11 · FY2030 total Medicaid spending under prior law: $1,293.3 billion. | P**
$837 billion federal (EN-10) divided by a 64.72% federal share.
**The federal share is the single modelled step between the two measured figures
at EN-9 and EN-10.** It is the FY2024 CMS-64 all-population blend held constant to
2030 under D-11, and it validates D-10's 64.7%. See `fmap.py`. If the federal share
drifts, every per-$100 figure on the to-be moves with it.

**EN-12 · HR-1 removes $10.26 of every $100 in FY2030. | P**
$132.68 billion of total-computable spending against a $1,293.3 billion
denominator. On a federal-only basis without the gross-up at EN-13 the figure is
$8.36. Composition: work reporting $4.08, blocked senior enrollment rule $1.27,
provider tax limits $1.24, everything else $1.05, blocked Medicaid enrollment rule
$1.03, directed payment caps $0.85, six-month renewals $0.75. See `tobe2030.py`.

**EN-13 · Gross-up from federal dollars to total-computable dollars. | D**
Rates derived from CMS-64 FY2024 National Totals, four quarters, medical assistance
payments only: work reporting and six-month renewals at an 88.05% effective rate
for the expansion group (×1.136); the two blocked enrollment rules at a 58.79%
non-expansion blended rate (×1.701); the residual at the 64.72% all-population
blend (×1.545).
**Two lanes carry no gross-up, by decision.** Provider tax limits (D-39): the tax
was the state's own match funding rather than an expenditure drawing a match, so
there is no federal share to gross up and states face budget pressure rather than
relief. Directed payment caps (D-41): financing is split, and the provider-tax
versus intergovernmental-transfer share is not separated nationally (D-46). See
`fmap.py` and `financing.py`.

**EN-14 · Lane allocation within FY2030. | P**
CBO publishes chapter-level annual figures and section-level ten-year figures, but
no section-level annual detail for any year (D-37). The FY2030 split is therefore
each section's ten-year deficit effect weighted by its statutory ramp position at
FY2030 (EN-2 to EN-8), normalised to the measured FY2030 chapter total at EN-9.
**No provision-level annual figure in this paper is published by CBO.**

---

## C. Overhead and the shape of the flow

**EN-15 · Plan administration falls with capitation. | D**
Managed care administration is a residual inside an actuarially sound capitation
rate and is bounded by the medical loss ratio floor at 42 CFR 438.8, which requires
states to set rates such that plans achieve a minimum medical loss ratio of at
least 85 percent. Administrative load is struck as a percentage of premium, so it
falls with the premium by construction rather than by assumption.
On the to-be, MCO plan administration moves $3.81 → $3.47 and dual-MCO plan
administration $1.04 → $0.95, the same ratio as their capitation bases. **The load
percentage is unchanged; only the base shrinks.**

**EN-16 · State administration is held at its FY2024 dollar amount. | P**
$5.07, unchanged. HR-1 raises state administrative burden rather than lowering it:
six-month renewals double renewal volume for the expansion group, and work
reporting adds a monthly compliance determination with verification, notice and a
30-day cure period. §71119 appropriated $200 million in FY2026 for state systems
work and a further $200 million to CMS for implementation.
**Holding it flat is already generous.** Scaling it down would assert the opposite
of what the statute does. D-63.

**EN-17 · Overhead sensitivity. | P**
Services delivered per $100 in FY2030: overhead held throughout $77.28; overhead
scaled throughout $77.85; split overhead as published $77.79. Spread $0.57 on a
$10.26 reduction, five and a half percent of the cut. All three are build outputs
of `ledger_2030.ledger(variant)`, rendered as `reference_renders/sheet_overhead.png`.
*Corrected 2026-09-03 from $77.91 and a $0.63 spread, which the build has never
produced. See S-073.*
**The overhead assumption is not load-bearing,** and every variant errs in the same
direction, since more overhead shrinkage means more money reaching services.

**EN-18 · Health services delivered fall from $86.27 to $77.79 per $100. | P**
Follows from EN-12 through EN-17 on the conserved ledger. Each lever reduces the
flow at its bite point and everything downstream is drawn narrower (S-052).

**EN-19 · The Medicare premiums lane falls $2.90 → $1.63. | P**
The blocked senior enrollment rule prevents growth in Medicare Savings Program
enrollment that would have occurred under the 2023 rule, so Medicaid does not pay
those premiums. CBO estimates Medicaid enrollment among dual enrollees will be
about 800,000 lower in 2034, with no change in the number of people without health
insurance, because those people remain enrolled in Medicare.
**This reduction does not reach a Medicaid provider.** It lands on dual-eligible
beneficiaries as higher Medicare out-of-pocket costs. $1.27 of the $10.26 behaves
differently from the rest and is currently drawn identically. **OPEN** as a design
question.

---

## D. Baseline (as-is) figures carried into the to-be

**EN-20 · FY2024 structure held constant. | P**
The payer split, provider node values and beneficiary shares on the to-be are the
FY2024 structure projected forward, not sourced 2030 values (D-11, and see EN-10
for why no sourced alternative exists). Underlying vintages: CMS-64 FY2024 national
totals for the ledger; MACStats February 2026 exhibits 16, 17 and 21; eligibility
group shares FY2023; duals CY2022; managed care mix CY2021.
**FY2024 is the most recent complete fiscal year, not old data** (S-024). The
caveat is mixed vintages inside a composite.

---

## E. Open items — must not be published as currently drawn

**EN-21 · Provider-level incidence of the directed payment cap. OPEN**
The cap falls on inpatient hospital services, outpatient hospital services, nursing
facility services and qualified practitioner services at academic medical centers.
CBO estimates federal spending on state-directed payments was $64 billion in 2024.
Neither CBO nor CMS publishes an allocation of the reduction across provider types.
**The current render spreads the $0.85 evenly across all six provider nodes, which
is a placeholder and is wrong for hospitals specifically.** S-029 applies: a ledger
that balances against invented components is worse than no diagram.

**EN-22 · Provider tax lane decomposition. OPEN**
The lane blends the expansion-state phase-down with the national freeze on new and
increased taxes. These have different time profiles: the freeze produces loss only
against a rising baseline, so no first-year effect and a widening gap, while the
phase-down bites in fixed annual steps. Nursing facility and ICF/IID classes are
exempt from the phase-down entirely. The FY2030 weight of 0.60 is the step count
and does not reflect this decomposition.

**EN-23 · Cost growth is outside this ledger. OPEN**
Every figure holds unit costs flat, because the score says nothing about them.
Margin compression as the audience will experience it comes from payment falling
relative to plan **and** unit costs rising, and only the first is here. Requires
separate sourcing and a separate artifact (S-053).

**EN-24 · Lever-to-node linkage. OPEN**
A reader can see their node shrink and can see the seven levers, but not which
lever caused which part of their reduction. Design problem, not a sourcing one.

---

## F. Bite phases (added 2026-08-29, D-64)

**EN-25 · Provider tax limits leave the federal band before the merge. | D**
The mechanism is loss of non-federal share, not loss of a payment. A state with
less provider tax capacity has less to match, so it draws less federal money. The
dollar is never drawn, so it never reaches the state and never enters the $100.
Terminates as *federal match never drawn*. It does not return to the federal
government and does not fund another program; it reduces the deficit, which is what
CBO scored. **UNDERSTATED:** CBO's $182.7B is federal only and D-39 gives this lane
no gross-up, so the state's own lost tax revenue is not in the $1.24. Every other
lane on the combined ledger is grossed up. **OPEN**, see EN-13.

**EN-26 · Four enrollment levers leave at the state agency. | D**
Work reporting, six-month renewals, the blocked Medicaid enrollment rule and the
blocked senior enrollment rule all operate by preventing or ending enrollment. A
person not enrolled generates no capitation payment and no claim, so the dollar
never reaches a payer lane. Drawing these at disbursement, as the first render did,
showed money leaving a lane it had never entered. Corrected.

**EN-27 · The blocked senior enrollment rule is borne by beneficiaries, not
providers. | D**
This lane is entirely dual eligibles. CBO estimates Medicaid enrollment among duals
will be about 800,000 lower in 2034 and that the number of people without health
insurance does not change, because those people keep Medicare. The $1.27 therefore
never reaches a Medicaid provider; it lands on dual-eligible beneficiaries as
higher Medicare out-of-pocket cost. It reduces the Medicare-premium lane from $2.90
to $1.63. **It is the only lever on the diagram whose loss falls outside the
delivery system.**

**EN-28 · Directed payment caps hit the capitated leg, against three named provider
classes. | P**
§71116 names inpatient hospital services, outpatient hospital services, nursing
facility services, and qualified practitioner services at academic medical centers.
State-directed payments are managed care arrangements, so the bite lands on the
capitated leg of the claims fan, not fee-for-service. The $0.85 is apportioned
across hospitals, long-term care and physicians and clinics in proportion to their
capitated claims. **Modelled: CBO publishes no split among the named classes.**
Supersedes the even six-way spread at EN-21, which was a placeholder.

**EN-29 · Documented fraud terminates in providers. | M**
Providers receive the fraud dollars; the money is not services delivered. The
earlier render terminated it in the claims column, which showed the dollar stopping
before anyone received it. Corrected. Not drawn to scale.

**EN-30 · Medical cost inflation is a memo, not a subtraction. | OPEN**
Inflation does not remove a dollar from Medicaid. The dollar still reaches the
provider; it buys less care and covers less of the provider's cost. Drawing it as a
lever would break conservation and would claim Medicaid spent less than it did. It
is therefore rendered grey, dashed and hollow, leaving at the top of the claims
column and terminating as *provider cost*, explicitly outside the $100.
**Not to scale.** The price series is not yet sourced. CMS Office of the Actuary's
National Health Expenditure projections are the right source; the published figures
found so far are spending growth per enrollee rather than pure price growth, and
S-035 forbids substituting a plausible placeholder. **Sizing this band is the
outstanding item.**

**EN-31 · "Everything else" cannot yet be placed. | OPEN**
The basket carries provisions that bite in at least four different phases,
including the home equity limit, alien eligibility, expansion FMAP for emergency
Medicaid, the nursing facility staffing rule moratorium, reductions in state
Medicaid costs, prohibited entities, the FMAP incentive sunset, the uniform tax
waiver requirement, demonstration budget neutrality, cost sharing, and adjustments
to home and community-based services, plus CBO's netting of interactions across the
whole chapter. Some run opposite to others. CBO publishes one net figure for all of
it. Drawn as a single ribbon at the state agency, labelled "Other" and carrying
three of the basket's contents as examples: *e.g. home equity, cost sharing*
(JW, 2026-09-11, replacing "mixed phases — UNRESOLVED"). It declares no reach, so
it terminates at its own column's edge rather than claiming a destination it
cannot support, and it peels first.

The examples are illustrative and the ribbon does not say so on its face. Until
the basket is decomposed, this endnote is the only place a reader can learn that
"Other" is a net of at least eleven provisions biting in at least four phases,
some of them running opposite to each other.

**EN-32 · Bottom tracker separates ordinary leakage from HR-1. | D**
Grey figures above the line are leakage that exists under prior law. Warm figures
below the line are HR-1. $100.00 prior law, less $6.70 ordinary and $9.41 HR-1, is
$83.89 disbursed; less $5.11 ordinary is $78.77 claims paid; less $0.85 HR-1 is
$77.93 to providers; less $0.14 ordinary is $77.79 health services delivered.

**EN-33 · QUEUED, not yet built: medical inflation in the beneficiary pies. | OPEN**
JW, 2026-08-29. The pies currently show who consumes each service in dollar shares.
If inflation is visible only as a memo band on the flow, the pies will still read as
though a 2030 dollar buys what a 2024 dollar bought. Raise this when the pies are
next worked.

**EN-34 · The flow steps down at each bite. | D**
Reading the trunk left to right, per $100: 100.00 enters; provider tax limits
narrows the federal band by 1.24 and the state band slides up, leaving 98.76 at
the state agency; administration takes 5.07 and Medicare premiums 1.63 from the
top edge; the blocked senior enrollment rule (1.27), work reporting (4.08),
six-month renewals (0.75), the blocked Medicaid enrollment rule (1.03) and the
residual (1.05) each step the bottom edge up in turn, leaving 83.89 disbursed.
Width at any point on the diagram equals the running balance on the tracker
beneath it (S-056).

**EN-30 AMENDED · Medical cost growth, drawn to scale as a memo. | P**
Supersedes the not-to-scale placeholder.
**Source:** CMS Office of the Actuary, National Health Expenditure Projections
2025-2034: per-enrollee Medicaid spending growth averages 5.8 percent a year over
2025-2033. Compounded over FY2024 to FY2030 gives a factor of 1.4025.
**Basis warning, and it decides what the copy may claim.** 5.8 percent is
per-enrollee *spending* growth, blending price with utilisation and intensity. It
is not a pure price index, and used as a deflator it overstates pure medical price
inflation. It is the right measure for "what will it cost a provider to deliver the
FY2024 bundle of care in FY2030" and the wrong measure for "what happened to
prices". The artifact says the former.
**Magnitude:** $77.93 reaching providers in FY2030 buys $55.56 of care at FY2024
cost levels. The memo is $22.37 per $100, more than twice the entire HR-1
reduction of $10.26. **This is the finding, not a footnote.**
**Drawn as:** three grey ribbons leaving the MCO capitation, dual MCO capitation
and fee-for-service lanes in proportion to their share of claims, merging into one
band, landing with providers as documented fraud does, and subtracted after "to
providers" on the tracker. To scale. Never netted into the $100.

**EN-30 AMENDED AGAIN · Medical cost growth is WITHDRAWN from the artifact. OPEN**
Raised by JW, 2026-08-29: if CBO and CMS project absolute dollars that rise even as
enrollment falls, have they already priced medical cost growth upstream, and is
subtracting it at the end a double count?

**Finding, and it is not the double count.** CBO's January 2025 baseline runs
federal Medicaid from $656B in FY2025 to $837B in FY2030, 5.0 percent a year
compound, and prior-law enrollment is roughly flat across that window, so the
denominator is a fully inflated FY2030 dollar. But normalising to $100 puts
inflation in the numerator and the denominator equally, and it cancels. It is not
concealed in the federal, state or state agency columns; it has been divided out
of all of them.

So the $22.37 was not double counted. It was a **mixed-basis error (S-013)**: it
applied a price level to an index number. The $100 is a unit, not an amount of
money, and the FY2024 as-is is normalised to $100 as well, so "what a 2030 dollar
buys at 2024 cost" has no referent. The honest per-$100 comparison is $86.27
delivered under prior law against $77.79 under HR-1, with inflation already absent
from both sides.

**What the real quantity is.** Margin compression is the GAP between payment growth
and provider input-cost growth, not the whole of cost growth. Order of magnitude is
a few points cumulative over six years, not forty.

**Why it cannot be built yet.** CBO's 5.0 percent and CMS OACT's 5.8 percent are
both projections of *spending* by two agencies. Neither measures what it costs a
provider to deliver care. Differencing them would be S-034: two estimators of one
quantity treated as measures of two.

**What would close it.** A CMS market basket index. CMS publishes input-price
indices for hospitals, skilled nursing facilities and other settings to drive
Medicare payment updates. Those measure provider input costs directly, against
CBO's payment path as the denominator. Like-for-like, and sourceable.

**EN-35 · The FY2030 balance tracker reads against the same checkpoints as FY2024. | D**
$100.00 prior law, less $6.70 ordinary leakage and $9.41 HR-1, gives $83.89
disbursed; less $5.11 ordinary gives $78.77 claims paid; less $0.14 ordinary and
$0.85 HR-1 gives $77.79 health services delivered. Checkpoints and type sizes are
the FY2024 master's, unchanged, so the two diagrams can be read as a pair (S-060).
Under prior law the same four checkpoints read $100.00, $92.03, $86.42, $86.27.

**EN-36 · Provider tax limits source from the federal band. | D**
D-65, JW ruling 2026-08-29. The lane is federal match never drawn, so it departs
the FEDERAL band in the FEDERAL column, upstream of the point where federal and
state dollars combine. The state band does not slide up to close the space: the
$1.24 gap between the two bands through the state government column is the match
that will never be drawn. Earlier renders sourced it from the state share, which
was wrong about who loses the dollar.

**EN-37 · Tracker figures by column, FY2024 and FY2030. | D**
FY2024: $100.00; state agency less $7.97 administration and Medicare premiums;
$92.03 disbursed; payer less $5.61 plan administration and earnings; $86.42 claims
paid; claims less $0.15 documented fraud; $86.27 health services delivered.
FY2030: $100.00; federal less $1.24 provider tax limits; state agency less $6.70
ordinary and $8.17 HR-1; $83.89 disbursed; payer less $5.11; $78.77 claims paid;
claims less $0.14 fraud and $0.85 directed payment caps; $77.79 delivered.

**EN-36 AMENDED · Provider tax limits leave halfway down the federal slope. | D**
Refines EN-36. The slice departs at the midpoint of the federal share's descent
from the source bar to the trunk, where it can be seen coming out, and drops
steeply to a terminal right aligned on the state government / state agency
boundary. The federal band is drawn in two segments so the narrowing is visible at
the point it happens rather than inferred from a gap further along.

**EN-38 · One-cent conservation defect in the FY2024 dual-plan lane. OPEN**
Found 2026-08-29 by `check.py` on its first run, having been present in the
baseline throughout. The FY2024 dual MCO care components sum to $9.70 while the
dual care lane is stated at $9.69. Source rounding in the CMS-64 derivation.

It is inside the $0.02 tolerance and invisible on the artifact. It is still a
conservation failure, and under S-029 it should be reconciled against CMS-64
rather than tolerated indefinitely. It propagates into FY2030 as a $0.009
discrepancy between the directed payment cap applied to provider nodes and the
same figure on the tracker.

**Recorded because it was found by the checker rather than by reading the diagram,
which is the entire argument for having one.**

**EN-39 · DC FY2024 ships at reduced fidelity. Four elements absent. | P**
Built in the national view (D-66) so it registers against the national pair.
Conserves under `check.py`. Per $100 of DC Medicaid spending: federal $73.17,
local $26.83; administration $5.35, Medicare premiums $1.97; managed care $40.30,
PACE and D-SNP $0.91, fee-for-service $51.46; disbursed $92.68, claims paid and
health services delivered both $87.83.

**Absent and declared on the artifact, not estimated (S-071):**
1. Beneficiary shares. DC group totals not in hand, so the column is omitted.
2. Behavioral health as a separate provider node. Folded into wrap-around
   services in the DC source, so DC shows five nodes rather than six. The dollars
   are present; the split is not.
3. Public-company earnings and dual-plan retention. No DC figure.
4. Documented fraud. No DC figure.

**Modelled within what is shown:** the MCO care to service mix is a national
proxy, and the PACE / D-SNP split of 75 percent long-term care and 25 percent wrap
is modelled.

**Vintages need re-checking before DC goes to any reader.** JW notes DC is likely
stale on several axes. The spine is CMS-64 / MACStats FY2024, the payer peel is
DHCF CY2023, and the service mix proxy is national. Claims paid equals health
services delivered only because fraud is absent, which will change if a DC figure
is found.

**EN-40 · DC FY2030 is not yet buildable. OPEN**
DC-specific HR-1 lane values do not exist and the national lane vector cannot be
scaled to DC (S-067). Work reporting and six-month renewals fall on the expansion
group; the provider tax phase-down applies to expansion states only; the directed
payment cap runs to a different Medicare threshold over a number of steps that
depends on where DC's arrangements start. The panel ships blank with the reason
printed in it (S-072).


**EN-41 · Running loss percentages on the tracker. | P**
The "% lost" under each balance dot is 100 minus that balance. On a $100 ledger
the percentage lost and the dollars lost are the same number, so this row restates
the balance rather than adding a fact; it is carried because it is the form the
finding is quoted in. FY2024 ends at 13.73%; FY2030 under P.L. 119-21 at 22.21%.
Both derive from the ledgers already sourced at EN-01 through EN-17. No new
vintage. Added 2026-09-03.

**EN-37 AMENDED · The FY2030 tracker lights an intermediate balance at $92.06. | D**
Refines EN-37, which ran the state agency column together as "less $6.70 ordinary
and $8.17 HR-1". The rebuilt tracker (S-074) puts a dot wherever a number changes,
so that column now reads as two bites with a balance between them: $98.76 less
$6.70 administration and Medicare premiums gives **$92.06**, and $92.06 less $8.17
work reporting, renewals, enrollment rules and other gives $83.89 disbursed. No
figure moved; a figure that was previously implicit is now printed, and it is
listed here because it is printed. Added 2026-09-04.

**EN-42 · The FY2024 as-is spine, payer lanes and provider nodes. | M / D**
These are the measured figures the reader meets first, and they are carried
forward unchanged onto the to-be under EN-20.

*Spine.* Federal $64.70, state $35.30 per $100 total computable. Federal share
64.7%, MACStats February 2026 Exhibit 16 (spending by source of funds), FY2024.
Independently recomputed from CMS-64 National Totals for the four FY2024 quarters
as 0.6472 — see `fmap.py: BLENDED_ALL`, which carries the raw quarterly inputs so
the rate can be recomputed rather than trusted. **Measured.**

*Anchors.* Total Medicaid spending $957.4B (Exhibit 16); total benefit spending
$908.8B (Exhibit 17). Every per-$100 figure below is a share of the total
computable ledger, not of benefits alone.

*Payer lanes.* MCO capitation $40.06, dual-MCO capitation $10.89, fee-for-service
$41.08. Sum $92.03, which is the disbursed balance at EN-37. **Derived** from
MACStats February 2026 Exhibit 17, FY2024.

*Provider nodes.* Long-term care $28.91, hospitals $17.77, wrap-around services
$15.33, physicians and clinics $10.79, behavioral health $9.51, prescription drugs
$4.11. Sum $86.42, which is the claims-paid balance at EN-37 before documented
fraud. **Modelled**, and see EN-48: no source publishes a national split of
capitation by service category, so a node total cannot be measured. Exhibit 17
sources the fee-for-service half only. "Wrap-around services" is the
plain-language label for the residual category (S-033); it is a residual by
construction and conserves the column.

*Beneficiary shares.* The pie splits by eligibility group and dual status are
MACStats February 2026 Exhibit 21, **FY2023** — a year older than the rest of the
ledger. This is the mixed-vintage caveat already stated at EN-20 and it is
restated here because the shares are printed on the artifact.

Added 2026-09-04. Previously covered only by class at EN-20, which stated the
vintages without carrying the figures; 5.4 requires the figures themselves.

**EN-43 · Public-company earnings $0.76. OPEN**
Printed on both national panels as a subset of the payer margin, alongside plan
administration $4.85 ($3.81 non-dual MCO plus $1.04 dual-MCO, both at EN-15). The
two together are the $5.61 taken at the payer column on the FY2024 tracker.

**$0.76 is an estimate with no primary source behind it.** Plan administration is
sourced; the earnings carve out of margin is not. The intended derivation is a
segment-level allocation from the Medicaid segments of the publicly traded plans'
10-K filings, and that work has not been done.

Consequences, stated rather than buried. The $5.61 total is sound because it is
the measured margin; only the split between administration and earnings inside it
rests on an estimate. Nothing downstream of the payer column depends on the split,
so no balance on the tracker and no provider node moves if the carve changes. But
the artifact currently draws a labelled $0.76 with the same weight as measured
figures beside it, and that is what S-012 and S-043 exist to prevent.

**Must not ship as currently drawn.** Either the 10-K carve is done, or the
earnings label comes off and the payer column shows the undivided $5.61 margin
with the split declared absent on the artifact (S-071). Recommend the second for
the freeze and the first afterwards: an absent split declared is honest at any
vintage, and the carve is a week of filings work that should not gate the
presentation layer. Added 2026-09-04.

**EN-44 · The FY2030 payer lanes and provider nodes as drawn. | P**
Printed on the to-be panel and listed here because they are printed. None is a
sourced 2030 value; each is a build output of the conserved ledger, and the method
behind it is already sourced at EN-12 through EN-20.

*Payer lanes.* MCO capitation $36.52, dual-MCO capitation $9.93, fee-for-service
$37.44. Sum $83.89, the disbursed balance.

*Provider nodes.* Long-term care $25.75, hospitals $16.71, wrap-around services
$12.15, physicians and clinics $11.22, behavioral health $8.67, prescription drugs
$3.43. Sum $78.77, the claims-paid balance before directed payment caps and
documented fraud.

*Payer margin.* Plan administration $3.47 non-dual and $0.95 dual (EN-15), and
public-company earnings $0.69.

Each is the FY2024 figure under EN-42 carried forward at held structure (EN-20)
and narrowed by the lever incidence at EN-14. **Every one of these is modelled and
none is measured**, which is why the panel strap reads "Every figure modelled"
rather than flagging them individually (S-012).

The node values are the figures a reader will take personally — a health system
reads its own bar falling $17.77 → $15.90 — and the incidence behind that fall is
the open item at EN-21 and EN-24. The figure is sound as a share of the conserved
ledger; what it does not yet say is which lever took it.

$0.69 inherits **EN-43 OPEN**: it is $0.76 carried forward, and $0.76 is an
estimate with no primary source. It must not ship while EN-43 is open.
Added 2026-09-04.

**EN-43 AMENDED · Public-company earnings is scoped to public companies. | OPEN, not blocking**
JW ruling, 2026-09-04: "Its labeled as public earnings. Why would we worry about
earnings at non profits. Just source it to the public reporting."

Supersedes the coverage concern in EN-43 as written. Plans that file nothing
comparable were never in scope for this figure; the band is named for what it
counts. What remains is a straightforward sourcing task — the Medicaid segment
disclosures in the SEC 10-K filings of the publicly traded plans, summed and
reconciled to the payer margin — not a question about whether the figure can
exist. **EN-43 no longer blocks the presentation freeze**: it is a ledger value
awaiting its source, not a presentation-layer decision, and the recommendation to
strip the label is withdrawn.

**One consequence, and it is a labelling matter.** The payer margin $5.61 is
measured and conserves. If $0.76 counts only public-company retention, then
retention by nonprofit and provider-sponsored plans has nowhere else to sit and is
inside the $4.85 band, which the artifact labels as plan administration. No figure
is wrong and no balance moves; the label claims something narrower than what it
holds. Carried as a wording fix, not a sourcing gap.

Status until the carve is done: the $0.76 and $0.69 stay on the artifacts,
**modelled and flagged** (S-012, S-043), with this entry as the endnote.
Added 2026-09-04.

**EN-45 · Directed payment caps come out of managed care, not fee-for-service. | D**
JW, 2026-09-04, reading the diagram: "Do Directed payment caps really subtract
only from Fee for service, which is what the diagram looks like?" They do not, and
the diagram said they did.

A state directed payment is defined at 42 CFR 438.6(c) as a contract arrangement
that directs an MCO's, PIHP's or PAHP's expenditures. It is a managed-care
instrument by construction: the state directs what the plan pays its network. There
is no fee-for-service counterpart, because in fee-for-service there is no plan
contract to direct — the state is already setting the rate it pays directly.

The $0.85 bite was carved off the bottom edge of the fee-for-service band at the
claims column, so the artifact told the reader the opposite of what the instrument
is. Corrected 2026-09-04: the ribbon now leaves the **top edge of the managed-care
block**. The bottom edge was measured at y=553.8 with the fee-for-service lane
beginning at exactly 553.8 — no gap — so a bite taken there sits on a shared edge
and reads as either lane; the top edge has peeled-off white space above it and is
unambiguous. The ribbon crosses the fee-for-service lane on its way down, which is
a body crossing and correct (S-076, STYLE_GUIDE 2.9c).

**No figure moved.** $0.85 is unchanged, the claims-column subtraction is
unchanged, every balance on the tracker is unchanged, and conservation is
unchanged. What changed is which lane the reader sees it leave.

*Limitation, declared.* State directed payments apply across both MCO capitation
and dual-MCO capitation. The ledger does not decompose the $0.85 between them, so
the ribbon leaves the combined managed-care block at a single edge rather than
being split in proportion. Decomposing it needs SDP preprint data by plan type and
is not currently sourced — related to EN-21 and EN-22, and it should not be filled
in with a share (S-068). Added 2026-09-04.

**EN-37 AMENDED (2) · The FY2030 line reports $78.77 at Claims Paid. | D**
The four-anchor line (S-082) replaces the running ledger, and the anchors sit on
column LEFT edges — where money arrives — rather than wherever a number last
changed. "Claims Paid" therefore moves from the claims column's right edge to its
left edge, and reports $78.77 rather than $77.93.

Both figures are true of their own point: $78.77 is what enters the claims column,
$77.93 was what left it after directed payment caps. **No ledger figure moved.**
The same six decrements at the same amounts, conservation unchanged, and
$77.79 delivered. $92.06, $98.76 and $77.93 no longer appear on the artifact,
since the line now sums only at its four anchors. Added 2026-09-04.

**EN-46 · The beneficiary overlay: dollars out of each service. | M**
Beside each service's beneficiary pie on any panel carrying decrements, a bar and
a figure give the fall in that service's delivered dollars against prior law:
long-term care −$2.78, hospitals −$1.95, wrap around services −$1.18, physicians
and clinics −$1.41, behavioural health −$0.84, prescription drugs −$0.33. The six
sum to $8.49, which is the fall in health services delivered from $86.27 to
$77.79 less rounding at the second decimal.

*Basis.* Each figure is the FY2024 node less the FY2030 node, both read live from
the build; `instances.to_be_2030` takes its prior-law totals by reference from
`AS_IS_2024.node` rather than by transcription, so the overlay and the FY2024
panel cannot disagree (S-073).

*Scale, declared.* The bars carry their own scale, 34px per dollar, and it is NOT
the flow's scale. The decrements are an order of magnitude smaller than the nodes
and are invisible at the flow's px-per-dollar. All six share one scale and the
legend prints a $1.00 reference bar, because a bar on an undeclared scale invites
the comparison it is least able to support.

*Why dollars and not percentages (JW).* The pies already carry percentages, based
on each service's own dollars. A second percentage on the same mark, based on a
different quantity, is how a reader comes to read one as the other.

*Limitation, declared.* Only three of the six fall at a statute-specific rate.
§71116 names inpatient and outpatient hospital, nursing facility, and qualified
practitioner services at academic medical centres, so the directed-payment bite
lands on hospitals, long-term care, and physicians and clinics. **AMENDED
2026-09-11: the three rates were listed in the wrong order.** Read live from the
build, the falls are long-term care 9.73%, hospitals 10.43%, and physicians and
clinics 11.14% of their prior-law totals. The original text paired 9.73% with
hospitals and 10.43% with long-term care. `PAPER_PASSAGES.md` had the ordering
right and this note had it wrong, which is the S-073 failure in its purest form:
the figures were correct and the mapping was carried by hand. Wrap around services,
behavioural health and prescription drugs all fall at exactly 8.85%, which is the
undifferentiated eligibility-side rate and carries no service-specific finding.
This is EN-21's limit made visible; the overlay does not claim otherwise and the
three residual bars should not be read as a result. Added 2026-09-11.

**EN-47 · FY2030 beneficiary-class shares are carried forward, not modelled. | M**
`instances.to_be_2030` builds the FY2030 beneficiary-class split by taking the
FY2024 split — children $13.48, adults $29.56, disabled $24.98, aged $18.41 — and
scaling all four by the ratio of total provider spend. One multiplier, four
classes. Every class therefore falls by exactly 9.83%, which is an artifact of the
scaling and not a finding about incidence.

This is why the beneficiary overlay is per SERVICE and not per beneficiary class:
drawn per class it would produce four identical bars and invite the reader to
conclude that P.L. 119-21 falls evenly across children, adults, the disabled and
the aged. There is no basis for that claim either way.

*Status.* Declared modelled and added to the acquisition list. HR-1 incidence by
eligibility category is not currently sourced and must not be derived from the
national lane vector or from any share (S-068, S-071).

*Not on the artifact.* The FY2030 panel briefly carried a NOT SHOWN block naming
this gap and EN-31's; JW removed it, 2026-09-11. So the only warning a reader gets
that the four beneficiary pies do not carry HR-1 incidence is this endnote. Worth
re-raising before the paper ships, because the pies are the part of the panel a
reader is most likely to read incidence off. Added 2026-09-11.


**EN-48 · The provider phase is modelled, and here is the model. | D**
Added 2026-09-16, replacing an allocation that was carried in the workbook
builder and cited nowhere the reader could see it.

No source publishes national Medicaid spending by service category with
capitation distributed across services. MACStats Exhibit 17 reports managed care
as a single $496.1 billion line; Exhibit 18 also treats it as its own category.
So the six provider nodes are modelled, three inputs at three vintages, and the
model lives in `provider_mix.py`.

*Fee-for-service half.* CMS-64 service categories, FY2024. These sum to
$400,002 million, which is Exhibit 17's gross fee-for-service total to the
dollar. **Measured.**

*Capitated half.* Health Management Associates, "New Insights on Medicaid
Spending", a T-MSIS service mix at **CY2021**, three years older than the rest of
the ledger. It prices managed-care encounters at fee-for-service and Medicare
rates. **Modelled.** Direction of its known bias, stated rather than buried:
HMA's professional category unbundles hospital-based physician work that CMS-64
bundles into hospital, so physicians and clinics is overstated and hospitals
understated against CMS-64 convention.

*Behavioral health.* MACPAC, March 2026 Report to Congress, Chapter 2, Table 2-8
and Figure 2-1, CY2023 T-MSIS — the first national claims-based estimate of
Medicaid behavioral health spending since 2015. MACPAC publishes a split by care
setting, not by the categories this diagram uses; the mapping is ours and is
written out in `provider_mix.py` so a reader can disagree with it. Four
differences of basis, none resolvable by arithmetic: MACPAC counts any claim
carrying a behavioral health diagnosis in any position, which overstates; it
covers non-dually-eligible enrollees only, which understates; it is CY2023; and
its denominator is service-related spending of $642.3 billion rather than this
ledger's $957.4 billion total computable. For the last reason the carve's total
is held at this ledger's basis and only its distribution is taken from MACPAC.
MACPAC's own total is $95.3 billion against this ledger's $91.0 billion —
agreement to about five percent across two bases, which is the most the source
can be asked to say.

Long-term care takes no carve. MACPAC's care settings do not identify long-term
care, so there is no basis for one. **That is an absence, not a zero.**

*What this changed.* Behavioral health was previously carved mostly out of
wrap-around services. MACPAC finds that nearly half of behavioral health spending
occurs in non-hospital outpatient settings, with community mental health centers
and federally qualified health centers on top — all clinician settings. The carve
therefore reverses, and wrap-around services and physicians and clinics change
places. **The underlying categories did not move.** Before behavioral health is
removed from anything, wrap-around is $16.95 and physicians and clinics $14.72;
the previous carve compressed them to near-parity and the correction stops doing
so. The state of the world did not change. Our description of it did.

*Rounding.* The six exact node values sum to $86.4200, which is the money
arriving from the payer phase. Rounded individually they sum to $86.43, so one
cent is returned by trimming the node with the largest upward rounding. Earlier
editions described this as published totals disagreeing with rounded parts. That
was wrong: nothing here is published.

**EN-49 · Vaccines for Children.** The programme is authorised in the Medicaid
statute at section 1928 of the Social Security Act and is financed entirely by
the federal government; Exhibit 16 reports $7,239M for FY2024 with a dash in the
state column. OMB allocates the funds through CMS to CDC, CDC purchases the doses
at contract prices and distributes them free to enrolled providers through the
63 state, local and territorial immunisation programmes. A provider cannot be
paid for the vaccine product and cannot charge a patient for it. The only
Medicaid payment in the transaction is the fee for administering the shot, which
is a claim and is counted in physicians and clinics. The dose is outside the
hundred; the shot is inside it. Sources: MACPAC, MACStats Exhibit 16, February
2026; CDC, About the Vaccines for Children Program; CMS, Coverage and Payment of
Vaccines and Vaccine Administration under Medicaid, CHIP and BHP.

**EN-50 · Federal oversight.** The $0.10 peel is two published lines of Exhibit
16 drawn as one arrow: state Medicaid Fraud Control Units, $497M, and survey and
certification of nursing and intermediate care facilities, $468M. Both are
matched at 75 percent federal, so both sit inside the blended dollar and peel
where administration peels. MACPAC reports them nationally only; the exhibit
notes that state-level estimates exist but are not shown. They are therefore
absent from every state panel rather than apportioned, and a state panel's
administration figure excludes them. The FY2024 Fraud Control Unit figure is
itself an estimate carried forward from the FY2025 CMS budget justification,
because the FY2026 justification does not report actual FY2024 spending.
