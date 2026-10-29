# DC × HR-1 — pre-flight for the FY2030 panel

Worked ahead of JW, 28 October 2026. Nothing here is committed, nothing is
signed, and no existing file has been edited. The acquired figures are staged
in `dc_hr1_acquired.py`, which nothing imports, so no gate and no panel moves
until JW has read this.

The session-27-October note set two priorities: fill in the DC FY2024 data, and
draft an FY2030 DC view. This is the second one, taken as far as it goes
without a direction call. Five of the seven levers were ABSENT. Four of them
are now acquirable on District sources, one of the two held levers is settled
against DHCF's own statement, and the thing that was listed as the acquisition
target for the FY2030 denominator appears not to exist in published form.

---

## 1. What is now settled

### §71116 first affected period — the repo is right, DHCF is loose

`tobe2030_dc.FIRST_AFFECTED_FY_DISPUTED` has been open since 7 October. It is
closed on the rule, though not on DHCF's intent.

CMS-2449-P, background: section 71116(b) "requires a phase down beginning with
the first rating period that starts on or after January 1, 2028." DC's rating
period is the federal fiscal year — now confirmed a second time, on a different
document from the one the repo cites: the FY2025 preprint
`DC_Fee_IPH.OPH_New_20241001-20250930` states the rating period as 1 October
2024 to 30 September 2025. The period beginning 1 October 2027 starts before
1 January 2028, so **FY2029 is the first affected period and FY2030 sits at two
steps, 20 points off the base.** `DIRECTED_CUT_M = $97.04M` stands.

DHCF's April 2026 deck and its May 2026 budget testimony both say "10% each
year starting in FY2028". On the rule as written that is a year early. It is
worth one question to DHCF before publication, because a year moves the figure
by $48.5M, but the model should not move to meet it.

### The taper does not terminate by FY2030 — and `DIRECTED_REACHES_LIMIT_BY_FY30` is False, not ABSENT

KFF's analysis of the approved preprints puts **100 percent of DC's hospital SDP
spending above the new limit** — DC and Louisiana are the only two jurisdictions
at 100 percent — because DC's base rate alone already exceeds the Medicare-based
ceiling. On that reading the phase-down runs the whole programme to zero, ten
steps, and FY2030 at two steps is unambiguously partial.

The preprint's own Table 2 gives the post-SDP level as a share of ACR: 97.0%
(DC Healthy Families inpatient), 65.8% (HF outpatient), 95.1% and 79.0%
(CASSIP). Those are shares of commercial, not of Medicare, so the repo's
original question — how far above Medicare — still needs a commercial-to-
Medicare conversion for DC hospitals. **Acquisition target: the RAND Hospital
Price Transparency study's DC relative-price figure.** That is the only piece
missing to state the number of steps to termination.

### The SDP's own federal split is measured

Same preprint: total up to **$485,154,441**, federal **$376,029,678**,
non-federal **$109,124,763** — a 77.51% federal share. The national model sets
`GROSS["Directed payment caps"] = 1.000` by decision (D-41, financing split).
DC does not have to inherit that decision: it has the split. Direction question
below.

### §71115's rate taper does not bind DC at all

The expansion-state safe-harbour schedule steps 5.5% (FY2028), 5.0%, 4.5%,
4.0%, 3.5% (FY2032 and after). DC's hospital provider tax is **3% of net
patient revenue** (DHCF FY2026 budget testimony). Three is below every step in
the schedule, including the floor, so the taper never reaches DC.

DC's entire §71115 exposure is the other half of the section: from 1 October
2026 the District may only collect taxes **imposed as of 4 July 2025**, which
kills the enlarged tax DHCF had filed on 30 June 2025 and was still awaiting
approval on.

This is a finding worth drawing rather than a DC quirk: a jurisdiction can be
fully exposed to §71115 while sitting under every threshold in the published
schedule, because the freeze and the taper are two different instruments and
only one of them is a rate.

---

## 2. What is now acquirable that was ABSENT

### Provider tax limits — DC publishes the bite, in its own budget

`PROVIDER_TAX_CUT_M = None` was absent because the only statement was DHCF's
narrative that the funds revert, with no amount. The amount is in the budget
tables all along, on the Dedicated Taxes line (Table HT0-2):

| | $M |
|---|---|
| FY2024 actual | 114.647 |
| FY2025 actual | 235.337 |
| FY2026 approved | 285.940 |
| FY2027 proposed | 236.167 |

FY2027 lands **$0.83M from the FY2025 actual** — which is DHCF's narrative,
"the Provider Fee Funds revert to the FY2025 level", restated as arithmetic and
confirmed by a second, independent table. The one-year step is
**$49.773M of non-federal money**.

Two cautions. The basis is an appropriation, not CMS-64 — the same warning
`basis_dc` already carries for `DC_DEDTAX_M`, which ties exactly to the FY2024
figure here. And $49.773M is a FY2027 step, not an FY2030 level: the freeze
holds the tax at a nominal FY2025 level while prior law would have grown it, so
the FY2030 gap is **wider** than the FY2027 step, not equal to it. Growing the
step by the prior-law CAGR understates the lever. Direction question below.

### The ACR corroborates, on the payment side

DHCF's FY2027 budget testimony gives net ACR payments to hospitals of $307M
(FY2025 actual), $455M (FY2026 projected), $299M (FY2027 projected), and
attributes the FY2027 fall to the federal limit on the tax. The payment side and
the tax side tell the same story a year apart. Useful as corroboration; I would
not publish off it, because it mixes the tax freeze and the ACR limit in one
number and the panel draws them as two levers.

### Work reporting and six-month renewals — District denominators exist

Both apply to the expansion adult group from 1 January 2027, and DC publishes
that group monthly. From the DHCF enrolment report, January 2026 against
January 2025:

| | Jan 2025 | Jan 2026 |
|---|---|---|
| Childless adult 0–133% FPL | 76,278 | **78,322** |
| Childless adult 134–210% FPL | 16,417 | 1 |
| Parent/caretaker | 36,270 | 29,669 |
| QMB only | 11,622 | **12,880** |
| Dually eligible | 35,726 | 36,243 |
| Senior 65+ | 28,076 | 29,559 |
| Medicaid total | 276,981 | 253,148 |

The 134–210% band going to 1 is not an error and not HR-1: the District cut
childless-adult and parent eligibility to 138% FPL itself, effective 1 January
2026, and auto-enrolled about 15,000 people into the Healthy DC Plan. **The
population exposed to §71119 and §71107 in FY2030 is the ≤138% group, about
78,000, not the ~94,000 the earlier bands would suggest.** A DC panel built off
the FY2024 enrolment mix would overstate both levers by a sixth.

The dollars are published too, in the same budget table that carries the
dedicated taxes — DHCF books the expansion group as its own program line:

| MCO — Childless Adults (Group 8) | $M |
|---|---|
| FY2024 actual | 712.779 |
| FY2025 approved | 931.882 |
| FY2026 proposed | 1,103.824 |

So the two enrolment-side levers can be re-derived entirely on District inputs:
a District denominator, a District per-enrollee figure, and one modelled
disenrolment rate that gets declared on the plate. Nothing is allocated from
CBO. That is the route `tobe2030_dc` said was open, and it is open.

DC's own implementation rules narrow it further, and they are published:
exemptions cover Medicare enrollees, former foster youth, medically frail,
pregnant and post-partum people, and parents and caretaker relatives; DC looks
back one month; non-compliant enrollees get 30 days. Only the rate is missing.

### Blocked senior enrollment rule — a measured denominator

§71101 delays the Medicare Savings Programs rule to after 30 September 2034.
DC's QMB-only enrolment is **12,880** (January 2026), up from 11,622 a year
earlier — rising while total Medicaid fell 24,000. The repo's note that DC's
exposure here may diverge sharply from national is supported by the direction of
travel, not just by the 65+ growth.

### Blocked Medicaid enrollment rule — still the weakest

§71102 delays the eligibility-and-enrolment rule. It is rule-driven on
administrative process rather than on a named population, and I did not find a
District figure or a defensible group mapping. **This one stays ABSENT.**

### The FY2024 beneficiary row, which coverage.py also wants

MACStats FY2023, same vintage as the national Exhibit 21 row:

- Exhibit 21, DC total benefit spending $4,094M — children 10.0%, new adult
  group 18.1%, other adults 11.8%, people with disabilities 35.8%, aged 24.4%;
  dually eligible $1,375M, 33.6%.
- Exhibit 15, full-year-equivalent enrolment, thousands — total 291; child 80,
  new adult 93, other adult 59, disabled 29, aged 31.

**Carrying a data-quality footnote that has to be declared, not smoothed:** DC's
reported new-adult-group enrolment differs from the CMS-64 benchmark by more
than 20 percent — average monthly enrolment 33 percent below it. And the two
sources disagree about the size of the expansion group: Exhibit 21 puts it at
18.1% of spending, DHCF's own Group 8 line is $712.8M on a $4,372M hundred,
16.3%. Different vintages and different bases, but a reader will notice.

---

## 3. What I expected to find and did not

**The FY2030 denominator's supersession target appears not to exist.**
`tobe2030_dc.SUPERSEDED_BY` puts the DC FY2026 Proposed Budget and Financial
Plan's four-year plan FY2026–FY2029 on the acquisition list, to replace the
national-implied 5.272% CAGR. The DHCF chapter of that volume (`ht0_dhcf_
chapter_2026m`) carries FY2024 actual, FY2025 approved and FY2026 proposed and
stops. The FY2027 volume's DHCF chapter stops at FY2027. DC publishes its
four-year financial plan at District and fund level, not as an agency-level
Medicaid trajectory.

I have not exhausted Volume 1, so this is "not found where it should be", not
"proved absent". But the plan should be to keep the national-implied rate and
rewrite `SUPERSEDED_BY` as a declared finding rather than a standing to-do.

Also missing: no District-published HR-1 coverage-loss estimate exists. DHCF's
budget materials quantify the SDP and the tax and say nothing about enrolment
effects of the federal law. The third-party state-level estimates that do exist
are national models allocated down, which is the move this panel refuses.

---

## 4. Three things the national seven levers do not carry, which DC needs

1. **Home equity cap for LTSS**, $1M, from 1 January 2028. DC's aged share of
   spending is 24.4% and its disabled share 35.8% — both well above national —
   so a long-term-care eligibility lever may matter more here than in the
   national panel, where it sits inside "Everything else".
2. **Non-citizen eligibility restriction**, 1 October 2026 — **under preliminary
   injunction**, suspended pending federal litigation, per DHCF's February 2026
   advisory session. `DC_ONLY_NOTED` records the provision but not that its
   status is contested. A panel drawn today has to say so.
3. **Retroactive coverage**, 1 January 2027: one month for expansion adults, two
   months for everyone else. `DC_ONLY_NOTED` has 30 and 60 days, which is the
   same rule in different units.

---

## 5. Direction questions

Standing format. Question, options, strengths and weaknesses, recommendation.

### Q1. Where does the disenrolment rate for the two enrolment levers come from?

Everything else about §71119 and §71107 in DC is now measured. The one modelled
step is what share of the ~78,000 expansion adults lose coverage by FY2030.

- **(a) A declared flat assumption, chosen by us.** Honest, one constant, easy
  to re-run. But it is a number we invented, and a reader will ask why that one.
- **(b) The observed Arkansas and New Hampshire experience.** Empirical, and the
  only real-world evidence of a work-reporting requirement at scale. But both
  ran under different rules, for months not years, and neither had DC's
  exemption set.
- **(c) The participation loss implied by CBO's national score, applied as a
  rate to DC's own denominator.** Consistent with the national panel, and a rate
  is not a dollar allocation. But it is close enough to one that the distinction
  has to be argued on the plate, and the panel exists partly to refuse that
  move.
- **(d) Leave both levers ABSENT.** Unimpeachable. Also leaves the two largest
  enrolment levers blank on a panel whose purpose is to show HR-1 in DC.

**Recommendation: (a), with (b) setting the range.** Publish a range, not a
point — low and high from the Arkansas/New Hampshire experience, panel drawn at
the midpoint, both ends on the plate. It keeps the modelled step visible,
survives a hostile reader, and re-runs on one constant. (c) is the one I would
avoid: it buys consistency with the national panel at the cost of the argument
the DC panel is built to make.

### Q2. What is "Everything else" in a District panel?

Nationally it is a residual defined by what CBO scored, and a residual cannot be
re-derived from District sources because it is not a thing.

- **(a) Leave it ABSENT.** Honest and empty.
- **(b) Drop the lane from the DC panel.** Cleanest picture. Breaks the
  one-to-one correspondence with the national panel that makes the two
  comparable.
- **(c) Keep the lane, rename it for DC, and fill it with the three named
  District provisions above** — home equity, non-citizen eligibility,
  retroactive coverage — declaring on the plate that it is not the national
  residual and the two are not comparable lane-to-lane.

**Recommendation: (c).** The provisions are real, they are DC's, they have dates
and they have populations; and the alternative is a blank lane next to six full
ones. The declaration does the work that the shared name would otherwise do
falsely.

### Q3. How does the provider tax lever reach FY2030?

We have a measured FY2027 step of $49.773M and no FY2030 figure.

- **(a) Carry the FY2027 step forward unchanged.** Measured at both ends.
  Understates FY2030, because the freeze is nominal and prior law would have
  grown the base.
- **(b) Grow the step by the prior-law CAGR.** Consistent with the denominator.
  Still understates: it grows the gap at trend when the gap itself widens at
  trend on a frozen base.
- **(c) Derive it properly — prior-law tax base grown to FY2030, less the frozen
  FY2025 level.** Correct in structure, and it makes the lever's shape
  (divergence from a frozen line) visible rather than flat. One more modelled
  assumption: that the tax base would have tracked spending.
- **(d) Hold ABSENT until DHCF publishes an FY2030 figure.** It will not.

**Recommendation: (c), with (a) drawn beside it as the floor.** The structural
point — a frozen nominal cap bites harder every year — is one of the few places
where this panel can show a mechanism rather than a number, and it is exactly
what a DC audience of hospital and plan executives will want to see.

### Q4. Do the two coupled levers get modelled in sequence, and in which order?

`PROVIDER_TAX_COUPLED_TO_DIRECTED = True` is declared and not modelled. The
sequence now looks established: the tax freeze bites in FY2027 and sets the base
at the FY2025 level; the §71116 taper then runs 10 points a year on the
grandfathered amount from FY2029.

The risk is double counting. $485.2M is already the post-revert base, so the
directed-payment lever's $97.04M is a cut to money the provider-tax lever has
already reduced. Added naively the two overstate.

**Recommendation: model the sequence explicitly, in code, with an assertion that
the directed-payment base is the post-freeze base and not the FY2026 projection,
and a comment saying so at both ends.** This is the architectural finding the
7 October note flagged — most expansion states finance directed payments with a
provider tax, so whatever is built here is the shared code the second state
needs.

### Q5. Does the DC directed-payment lane take the national `GROSS = 1.000`?

D-41 sets it to 1.000 nationally because SDP financing is split. DC publishes
its split: 77.51% federal on the FY2025 preprint.

- **(a) Keep 1.000**, inherit the national decision, stay comparable.
- **(b) Use DC's measured 77.51%**, because it exists and the whole point of a
  state panel is that state facts beat national decisions.

**Recommendation: (b), and treat it as a candidate to re-open D-41 nationally.**
If the national 1.000 is a decision taken in the absence of a split, a measured
split in the first state panel is evidence about the national model, not just
about DC.

---

## 6. If the answers are yes, what moves

| File | Change |
|---|---|
| `tobe2030_dc.py` | `FIRST_AFFECTED_FY_DISPUTED` → resolved, with the CMS-2449-P citation; `DIRECTED_REACHES_LIMIT_BY_FY30` → False, KFF-sourced; `PROVIDER_TAX_CUT_M` → derived per Q3; coupling modelled per Q4; `SUPERSEDED_BY` → finding, not to-do |
| `fmap_dc.py` | DC SDP gross-up per Q5 |
| `ledger_dc_2030.py` | lever rows for work reporting, six-month renewals, blocked senior rule; "Everything else" renamed per Q2 |
| `ledger_dc_2024.py` | beneficiary row from MACStats Exhibits 21 and 15, with the benchmark footnote declared |
| new | the modelled/measured distinction has to be drawn on the plate, as absence is — the 27 October note is explicit that a DRAFT view says which is which |

Everything acquired above is staged in `dc_hr1_acquired.py` with its source on
each line. Nothing imports it. `coverage.py dc` still reports 26 missing,
because nothing has been wired in.

## 7. Still absent after all this

- §71102's affected groups in DC — no mapping found.
- DC hospital commercial-to-Medicare ratio, which is what would let the SDP
  taper be shown as terminating or not by a specific year.
- A District FY2030 prior-law denominator; the national-implied CAGR stands.
- The FY2024 plan-retention split, dual and PACE retention, and the service mix
  — priority 1 from 27 October, untouched here, and still the larger hole.
