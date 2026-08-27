## Decisions added 2026-08-27 — HR-1 modelling session

### Amendments to existing decisions

**D-01 AMENDED.** $100 = **2029** baseline spending under prior law, not 2028. The headline
anchor moved to 2029 (D-22) and the ledger must sit on the same year; a 2028 base with 2029
losses is a mixed basis. Gap bands still peel off at the point each provision bites.

**D-06 AMENDED (Fork 1).** The fork table still marks Fork 1 OPEN. D-18 resolved it at a 26%
central case with sensitivity at 20% and 35%. D-18 governs; the table is stale and should be
corrected in place.

**D-06 AMENDED (Rural Health Transformation).** No counterflow band. See D-31.

**D-08 AMENDED.** The "2028 is mid-ramp" caveat is obsolete. 2029 is the first full-effect
year, which is why it was chosen. Rewrite the caveat rather than delete it — some provisions
still phase after 2029 (the provider tax safe harbour steps down 0.5%/yr until it reaches
3.5%), so the paper still owes the reader a ramp note, just a different one.

**D-11 AMENDED.** Structure held constant FY2024 → **2029** counterfactual, not 2028.

**D-14 AMENDED.** Warm no longer means "money stopping." Warm means **HR-1 attributable
loss**. Baseline leakage renders as ghosted source colour and peels upward; HR-1 loss renders
warm with texture and peels downward. See standing note S-026.

### New decisions

**D-22 · Scope: every provision with a material Medicaid score**
Work requirements (§71119), provider tax limits (§71115), state directed payments (§71116),
six-month redeterminations (§71107), cost sharing (§71120), immigrant eligibility (§71109),
retroactive coverage (§71112).

**D-23 · Impact year: 2029**
First full-effect year. Chosen over 2034 because it is a year readers can plan against.

**D-24 · Six lanes, not seven**
Own lane: work requirements, provider tax, state directed payments, six-month
redeterminations, immigrant eligibility. "Other provisions" holds cost sharing and
retroactive coverage.

Immigrant eligibility gets its own lane **despite being ~0.8% of the money**, because showing
how small it is relative to the rhetoric is itself the point. At $100 scale it is roughly a
penny — thinner than its own stroke — so it takes a minimum visible width plus a "not to
scale" flag, following the existing documented-fraud band at $0.15.

"Other" is provisional. If the cost-sharing score comes back large, it earns its own lane.

**D-25 · Basis: gross federal up to total**
CBO scores federal dollars; the $100 is federal + state. Gross CBO figures up to total
spending so the loss bands and the ledger share a basis.

**D-26 · FMAP: per provision, not blended**
Applying the blended 64.7% to everything would overstate the expansion-population lanes by
roughly 40% — work requirements land near $500B total instead of ~$362B — because expansion
adults match at 90%, not 64.7%. Author to build a rate-and-rationale table per provision and
bring it to the Executive Producer for approval before it touches the ledger. Financing
provisions (provider tax, state directed payments) do not sit at a single population rate and
need their own treatment.

**D-27 · Annualisation: use CBO's published FY2029 line**
Not the 10-year total divided by ten, and not a ramp allocation — those are fallbacks. Where
CBO does not publish per-section annual detail for a lane, allocate by the provision's
effective-date ramp and flag that lane as modelled.

**D-28 · Interaction adjustment: scale, don't draw**
Provisions are scored independently, so summing them double-counts people who would lose
coverage under more than one. The six lanes are scaled down proportionally to the true total,
with a footnote explaining why the parts exceed the whole. No "double-counted" band on the
master — it is a bookkeeping correction, not a destination, and drawing it invites readers to
treat it as somewhere money went. The provision-decomposition exhibit may show it explicitly.

**D-29 · Financing provisions route three ways**
Provider tax and state directed payment dollars split across: absorbed by providers (rate
cuts), care that does not happen (benefit and eligibility cuts), and unfunded state & local
budget pressure (general-revenue backfill).

Mechanism, recorded because it is easy to get backwards: the provider tax was never state
general revenue. States taxed providers, counted the revenue as the state share, drew federal
match on it, and paid providers back more than they were taxed. When tax capacity shrinks,
the state's general fund is roughly neutral — it was not paying before and is not paying now.
**What disappears is the federal match the tax was leveraging, and it lands on providers as
lost payments.** States face pressure only if they choose to hold spending flat.

The law's moratorium blocks new provider taxes and rate increases on existing ones. It does
not restrict general state taxing power, so general-revenue backfill remains legally
available — politically hard, but on the table. That is the path node 4 represents.

Per D-05, CBO already prices partial non-backfill. Do not apply a further multiplier; this
decision governs routing only, not magnitude.

**D-30 · Split ratio: flat one-third each for national**
Unlike Forks 1–3, this split has no literature — it depends on fifty separate political
situations. A flat third is the honest expression of that uncertainty for a national average.

**Must be flagged on the artifact and in footnotes as illustrative, not modelled.** A flat
one-third will otherwise be quoted back as a finding.

State editions replace it with that state's actual posture. This is a large part of what
STATE_PLAYBOOK is for.

**D-31 · Grant programmes sit outside the ledger**
Standing rule, covering the Rural Health Transformation Program and any future grant.

Grants are one-time, appropriation-based, and not care. Drawing RHTP as a counterflow band
would put it on the same footing as service dollars and imply it offsets lost care. It does
not: a hospital with a transformation grant and reduced supplemental payments has new capital
and less operating revenue. It is also finite where the rest of the diagram is annual
run-rate — mixed basis.

Treatment: a labelled memo item alongside the diagram giving amount, period, and an explicit
statement that it does not offset the service-dollar losses shown. State editions show zero
where the state received nothing, which is itself informative.

**D-32 · Administration splits into two nodes**
`Administration $5.07` becomes ongoing administration + systems and one-time investment,
summing to $5.07 so conservation holds. Sourceable, since the CMS-64 reports MMIS separately
from general operations.

Rationale is the state series: a state mid-MMIS-build is structurally different from one that
finished five years ago, and today that difference is invisible. Note that IT money is
*inside* the ledger (matched CMS-64 administrative expenditure) while grants are *outside* it
(separate appropriation) — they are not the same kind of money and must not share a node.

Size the systems slice from the CMS-64 before drawing; if it is a few tenths of a dollar it
needs the same not-to-scale treatment as the immigrant eligibility lane.

**D-33 · Section V carries three short checklists**
States, plans, providers — one short list each. Per S-018, a dollar means something different
depending on who holds it, and the checklist is where that gets concrete.

Watch D-21: three lists will push on length. Keep each to four or five items rather than
trimming the analysis ahead of them.

**D-34 · State editions inherit structure, not assumptions**
All state editions inherit the ledger architecture, lane definitions, encoding, and layer
rules. Routing assumptions are set per state. Local editions may add exhibits answering local
questions that the national edition does not carry.

DC was simply the first modelled, not a template. Note that DC is not a state and its FMAP is
statutory at 70% rather than formula-driven, so D-26's gross-up does not transfer to it
unchanged.

### Open research tasks arising

1. CBO FY2029 annual lines by section for all seven provisions (D-27).
2. Cost-sharing (§71120) score — not yet located; determines whether D-24's "Other" holds.
3. FMAP table per provision with rationale, for approval (D-26).
4. Reconcile three provider-tax figures now in circulation: $191.1B (CRS), $182.7B (CBO
   supplemental, §71115), ~$226B (Commonwealth, "provider tax changes"). Different scopes
   and vintages; the paper needs one and a footnote explaining the others.
5. MMIS/systems share of the CMS-64 administrative line (D-32).
6. RHTP appropriation amount and period, and whether DC is eligible (D-31).

### Closed items

**Erin Henderson interview — not planned. Closed 2026-08-27.**
Previously carried as an open item. Closed at the Executive Producer's direction: an interview
is unlikely to be available, and no source can supply what the placeholder in D-30 stands in
for. Nobody knows how plans and states will respond, and they will respond differently from
one another — the flat one-third split is the honest expression of that, not a stopgap
awaiting better information.

This is a closure, not a deferral. Do not resurface it as an open item.

Two consequences to carry:
- **D-17 is unaffected.** Erin remains co-author. Co-authorship does not depend on an
  interview and the byline stands unless separately revisited.
- **D-19 needs a source check.** If Section VI's human-impact sourcing was leaning on her
  first-hand plan-side and FQHC experience, that section needs an alternative source. Verify
  before drafting Section VI rather than at review.

Note for the record: what an interview could have contributed is decision *structure* — which
levers a plan actually holds when directed payments are capped, which are contractually or
regulatorily foreclosed, and in what order they get pulled. That is mechanism, not prediction,
and it is the class of knowledge that corrected the provider-tax model in this same session.
If the opportunity arises incidentally it remains worth an hour. It is not a blocker and
should not be tracked as one.

---

## Revisions later the same session, after retrieving the CBO source

The decisions above were made before CBO's Supplemental Cost Estimate for P.L. 119-21
(Title VII, Subtitle B, Chapter 1, Medicaid; October 28, 2025) was in hand. Retrieving it
overturned three of them. Amendments follow and govern.

**Source of record:** CBO Supplemental Cost Estimate, 28 Oct 2025, measured against the
January 2025 baseline, covering 2025-2034. CBO notes the amounts match its July 2025
estimate.

**D-22 AMENDED · Lanes follow CBO's sections, not public salience.**
The original seven were chosen by prominence in coverage of the law. CBO scores six sections
plus a residual, and the overlap is only partial: cost sharing (§71120), immigrant
eligibility (§71109) and retroactive coverage (§71112) receive no separate CBO line, while
two sections carrying $119.6B were not on the list at all.

Lanes, all ten-year, all sourced:

| Lane | Section | 10-yr |
|---|---|---|
| Work requirements | §71119 | $317.0B |
| Provider taxes | §71115 | $182.7B |
| State directed payments | §71116 | $149.4B |
| MSP rule moratorium | §71101 | $66.0B |
| Six-month redeterminations | §71107 | $58.0B |
| Eligibility/enrollment rule moratorium | §71102 | $53.6B |
| Other policies + interactions | — | $60.1B |

These sum to $886.8B, CBO's stated total, exactly.

**D-24 AMENDED · Immigrant eligibility lane dropped.**
Reverses the earlier ruling that it gets its own lane to show how small it is. The only
available figure is KFF's ~$6B on a different basis, which would make it the one unsourced
band in an otherwise fully sourced diagram, resting a rhetorical point on the weakest number
on the page. Handled as a footnote noting its size instead. The point still gets made; it
just gets made in prose.

**D-28 OBSOLETE · No interaction scaling.**
The decision assumed the parts would exceed the whole and the lanes would need scaling down.
They do not. CBO carries interactions inside the residual bucket, and the sections sum
exactly to the total. Delete the scaling. Replace with a footnote stating that CBO nets
interactions separately, so the lanes are additive as published.

**D-35 · The residual bucket must be labelled honestly.**
It is not "small provisions." It holds cost sharing, immigrant eligibility, retroactive
coverage, the remaining minor policies, *and* the interaction netting. Label it as everything
else plus the arithmetic, not as a tidy remainder.

**D-36 · Basis: section figures are deficit effects; the ledger is outlays.**
Over ten years CBO reports outlays down $914.6B and the deficit down $886.8B — a ~$28B gap
that is the revenue reduction. Revenue has no place in a spending diagram. Reconcile before
converting to the $100 basis. Same issue at 2029: outlays -$92.9B, deficit -$90.1B. The
outlay figure is the correct one for this ledger.

**D-37 · 2029 annual detail is not published per section.**
CBO gives the year-by-year table in aggregate only. FY2029 outlays fall $92.9B, about 10% of
the ten-year total — which is why D-27's rejection of divide-by-ten was right. Every lane
falls to ramp allocation from the statutory effective dates and must be flagged modelled on
the artifact. Only the annual total is sourced.

**D-38 · Second exhibit: the same dollars cut by mechanism.**
Three tiers, stacked to one total:

- **Eligibility change** — people who no longer qualify.
- **Added friction** — new administrative barriers. Work requirements' 2.8M from added
  application steps (against 2.9M for not meeting the requirement), and §71107's 70%
  procedural share.
- **Preserved friction** — §71101 and §71102. Nobody loses coverage; rules that would have
  lowered barriers are blocked, so enrollment that would have happened does not.

Not one undifferentiated block. Segmenting keeps every piece traceable to a specific CBO
paragraph, and the three tiers are genuinely different mechanisms — an informed reader will
see that immediately, and burying it makes the whole exhibit attackable on its softest
component. A reader who rejects the third tier can still accept the first two.

**Methodological limit, non-negotiable:** every split above is stated by CBO in *people*, not
dollars. Converting to dollars requires assuming procedurally-removed enrollees cost about
the same as ineligible ones. That is likely wrong — procedurally-removed enrollees are
plausibly healthier and cheaper, since sicker people have more contact with the system and
more reason to complete paperwork. Publish the people split as the people split. Hold any
dollar version as modelled and flagged, or omit it.

The apportionment across sections is Agilian's, assembled from CBO's paragraphs. It is not a
CBO figure and must never be presented as one.

### Research task list, revised

Closed by the CBO fetch:
- Cost-sharing score — no separate line exists; it sits in the residual.
- Provider tax reconciliation — $182.7B is the deficit effect, $191.1B the outlay effect.
  Different measures, not competing estimates.
- FY2029 anchor — outlays -$92.9B.

Still open:
1. Statutory effective-date ramps per section, for the 2029 allocation (D-37). Next fetch;
   mechanical.
2. FMAP table per provision with rationale, for approval (D-26).
3. Outlay-versus-deficit reconciliation at section level (D-36).
4. MMIS/systems share of the CMS-64 administrative line (D-32).
5. RHTP appropriation amount and period, and whether DC is eligible (D-31).
