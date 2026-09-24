# Interrogating a state

`ACQUISITION.md` says what order to acquire in. `STATE_PLAYBOOK.md` says how to
build once you have it. This file is the third thing: what to *ask*, where the
answers live, and which traps have already caught us once.

It is written from the DC build. Every trap below is one we fell into, not one
we imagined.

---

## The governing rule

**A state that matches the national mix is a state you have not measured.**

Divergence is the product. If a state's numbers depart from national averages,
the finding is not an error to reconcile — it is the reason the panel exists.
The obligation is to establish *why*, from the state's program design, and say
so. "It differs from national" is never itself a reason to distrust a figure.

Corollary: never use the national mix as a stand-in for a state figure. An
absent cell is a declarable state. A national proxy wearing state clothes is
not.

---

## Source ladder

Work down. Each rung answers questions the rung above cannot.

| # | Source | Answers |
|---|---|---|
| 1 | CMS-64 / MACStats Exhibits 16, 17 | the spine: total, federal/non-federal, lanes |
| 2 | State agency managed care performance or quality report | plan roster, per-plan revenue, claims, administration |
| 3 | State budget chapter for the Medicaid agency | fund structure, program line items, out-year plan |
| 4 | NAIC health blanks, via the state insurance regulator | per-plan service split |
| 5 | State code | what the assessments and dedicated funds actually are |
| 6 | Agency oversight / performance testimony | policy changes, projections, enrollment |
| 7 | Independent state fiscal analyst | cross-check; expect disagreement with rung 6 |

---

## Standing questions, in phase order

### Sources and the non-federal share

- **Is the non-federal share one kind of money?** Exhibit 16 reports a single
  figure. The state's own appropriation usually splits it across several funds.
  Pull the budget chapter and look at the fund table before accepting a
  two-source column.
- **Are there provider assessments?** Most states have them. They are levied on
  providers, used as the non-federal share, matched, and paid back to the same
  provider classes. Identify the instruments in state code — do not label a band
  you cannot name.
- **Is there a special purpose revenue line?** If it is collections or
  third-party liability recovery, it is probably *already* in the panel, netted
  on the uses side. Putting it in sources too counts the money twice in opposite
  directions.
- **Do the two accountings reconcile?** Budget gross will not equal CMS-64 net.
  Quantify the gap before using either. Any figure with parents in both is
  DERIVED, never measured.

### Scale and peels

- Does the state have every peel the national panel has? Vaccines for Children
  and federal oversight are the two that go missing silently.
- Is an absence a gap or a true zero? Establish it. Do not assume either.

### Lanes

- **Which programs run through managed care, and which do not?** This is where
  states differ most. Long-term care is the usual divider.
- **Is anything moving between lanes?** Mid-year or mid-period lane migrations
  show up in the budget as one line going to zero and another appearing.

### Named plans

- **Get the plan roster for the exact year.** Entries and exits mid-year are
  common, and produce partial-year filings.
- **Check the report vintage.** Ours was two editions stale, and the newer one
  had four clean lines where the old one had a composite.
- **Does any plan figure fail to match a published line?** If so, suspect a
  sum. Test every pairwise combination of the published rows against it.
- **Is the revenue figure Medicaid?** State agencies commonly administer
  locally funded coverage programs through the same plans, and report the
  combined revenue. That money is not Medicaid and cannot sit inside the
  hundred.
- **What does the agency exclude?** Premium tax, risk corridors and risk-share
  amounts are routinely excluded from "revenue" without the word appearing in
  the table header.

### Payer retention

- Does any plan run at or above 100% MLR? If so its administration is funded
  from reserves, not from the dollar, and `care + adm = cap` stops holding.
  Draw it as measured and declare it. Do not smooth it.
- Is retention administration, margin, or both? A plan with a large operating
  gain and small administration draws a fat peel for the wrong reason. Check
  whether an accrued risk-corridor liability sits behind it.

### Claims allocation

- **NAIC blanks work only for single-state domiciled entities.** A plan
  domiciled elsewhere files a combined book and its service split is not
  recoverable at state level. Schedule T allocates premium by state, not
  expense by service by state.
- **Some plan types file no health blank at all.** Special-needs and
  pre-regulation contractors are the usual cases.
- **NAIC service lines are not comparable across plans.** Hospital/medical
  benefits versus other professional services is a booking convention. Test it:
  if the two lines differ wildly across plans but their *sum* is stable, the
  split is convention, and only the combined block is usable.
- **Where does behavioral health sit?** The blanks have no behavioral line, so
  it hides inside other professional services. A state that carves behavioral
  health out of managed care will show it in fee-for-service instead.
- **Is encounter data public?** Usually not. Expect the performance report to
  publish trends by service category without levels. Percentages cannot be
  turned into dollars without the base.
- **Are collections allocated to a lane?** The exhibits usually decline to
  place them. If our ledger places them anyway, that is our assumption and must
  be declared as one.

### To-be year

- **Does the state publish a multi-year financial plan reaching our to-be
  year?** If so it is a primary, local, on-vintage source and beats any national
  projection applied to a state.
- **What is scheduled to change?** Eligibility thresholds, lane migrations and
  program sunsets are usually already in statute or in the enacted budget.
  Check the *enacted* version — proposed budgets get amended, sometimes
  reversing direction entirely.
- **Do federal and state changes interact on the same date?** They often do,
  and the interaction is usually the finding.

---

## Traps, each one paid for

1. **The composite lane.** A plan figure that matches nothing may be two
   partial-year plans summed and given the successor's name. The claims ratio
   can survive the merge almost untouched while the administrative ratio is
   wrecked, so a ratio check will not catch it. Test for sums.
2. **The stale report.** Check for a newer edition before building on one.
3. **Non-Medicaid money inside Medicaid figures.** Locally funded programs
   administered through the same plans.
4. **The national proxy.** See the governing rule.
5. **Deriving what is appropriated.** If the budget carries the program as a
   line item, use it. A PMPM-times-enrollment derivation of a line that exists
   in the budget was 16% to 27% low in DC.
6. **Point-in-time enrollment times an annual PMPM.** Wrong whenever enrollment
   moved during the year, which is always.
7. **Double-counting a netted figure.** See special purpose revenue above.
8. **Treating a state difference as an error.** See the governing rule.

---

## What "done" looks like for a phase

Every figure names a source, a vintage and a basis. Every absence is declared
on the artifact. Every derived figure resolves to parents that exist. Nothing
in a caption or a comment is a number the build also computes (S-105). And for
every place the state departs from national, there is a sentence saying why,
sourced to the state's own program design.
