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
scaled throughout $77.91; split overhead as published $77.79. Spread $0.63 on a
$10.26 reduction, six percent of the cut.
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

**EN-26 · Four enrolment levers leave at the state agency. | D**
Work reporting, six-month renewals, the blocked Medicaid enrollment rule and the
blocked senior enrollment rule all operate by preventing or ending enrolment. A
person not enrolled generates no capitation payment and no claim, so the dollar
never reaches a payer lane. Drawing these at disbursement, as the first render did,
showed money leaving a lane it had never entered. Corrected.

**EN-27 · The blocked senior enrollment rule is borne by beneficiaries, not
providers. | D**
This lane is entirely dual eligibles. CBO estimates Medicaid enrolment among duals
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
it. Currently drawn as a single ribbon at the state agency and labelled UNRESOLVED
on the artifact.

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
enrolment falls, have they already priced medical cost growth upstream, and is
subtracting it at the end a double count?

**Finding, and it is not the double count.** CBO's January 2025 baseline runs
federal Medicaid from $656B in FY2025 to $837B in FY2030, 5.0 percent a year
compound, and prior-law enrolment is roughly flat across that window, so the
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
