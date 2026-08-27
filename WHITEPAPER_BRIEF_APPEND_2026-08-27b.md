# Decisions added 2026-08-27, second session — financing and FMAP

Second session on the same date. Read after `WHITEPAPER_BRIEF_APPEND_2026-08-27.md`,
which governs where the two overlap only for items this file does not amend.

Entered the session on open task 1 (FMAP table per provision, D-26). Task 1 is
partially closed. The session's larger output is a second conserved ledger that did
not exist at the start, arising from a conservation problem in the provider tax lane.

---

## New decisions

### D-39 · Provider tax limits split by what the tax financed

Providers lose the **federal match**, drawn on the first ledger. The general-share
portion is not drawn as a loss band at all; it moves to the second ledger (D-40) as
state budget pressure. This lane is therefore **exempt from D-25's gross-up** and
carries a basis footnote stating so.

**The problem this solves.** D-25 says gross CBO's federal figure up to total
spending. Applied to provider taxes it manufactures a state share that was never
state money. Worked example: a state taxes hospitals $100M, uses it as the state
share, draws match at 60%, pays hospitals $250M. Hospitals net $150M, exactly the
federal match. Remove the tax capacity and federal outlays fall $150M, total
computable falls $250M, and provider net revenue falls $150M. Drawing the $250M band
and routing all of it to loss destinations overstates provider harm by roughly
two-thirds on the second-largest lane. The missing $100M is tax no longer paid and
has no home among D-03's five destinations, because it is not a loss to anyone.

**Split ratio.** 80% recycled to the same providers, 20% substituting for state
general fund. Sourced: MACPAC 2017, assessed as appropriate by GAO (GAO-21-98, 2020)
after state interviews and additional data review, and still applied as a working
assumption in GAO-24-106202 (2024). **Modelled, flagged, and held as the variable
`PROVIDER_TAX_RECYCLE_SHARE` in `financing.py` so it can be updated without a code
search.** Vintage caveat: predates the directed payment expansion; direction of bias
plausibly upward, since SDP growth is heavily provider-financed and targeted at the
taxed class.

**Section VI finding to carry.** Even in the pure recycling case, aggregate net-zero
on the tax side conceals a large redistribution. Every provider in the class pays in
proportion to net patient revenue; payments came back weighted toward Medicaid
volume. A low-Medicaid hospital comes out ahead when both stop. A safety-net hospital
takes the full loss. Aggregate zero, sharply negative at the bottom of the
distribution. That is the opposite of what a reader assumes on hearing a tax was cut.

### D-40 · The state fiscal ledger is a second conserved ledger

Not a memo item on the D-31 pattern. It opens at the **$35.30 state share**,
decomposes it by financing source, and expands outward to what each source displaces.
The two ledgers join at a number the reader already has from the first diagram.

**The mechanism, recorded because JW's first framing had the direction reversed and
the corrected version is the better story.** Nothing flows *out* of the $100. Provider
tax revenue is already inside it, as part of the $35.30. What funds other state
programs is **displacement, not outflow**: the state was going to appropriate general
fund money to Medicaid, provider tax revenue covers that obligation instead, and the
general fund money never enters the ledger and goes to schools or corrections. The
Medicaid ledger is unchanged in size; the state's fiscal position is what moved.

This explains the political behaviour. A provider tax is attractive to a legislature
precisely because it is a Medicaid financing decision that frees non-Medicaid money.
Under HR-1 it does not shrink Medicaid directly; it re-presents a general fund bill
the state stopped receiving years ago. The legislature funds Medicaid from general
revenue, cuts Medicaid, or cuts something else entirely. The third option never
appears in Medicaid coverage data.

**Audience framing (S-018).** Write this as a threat model, not as fiscal analysis.
It is the only mechanism explaining why a plan's capitation rates get cut in 2029
when nothing in HR-1 touches capitation.

**Opening decomposition, per $100** (GAO SFY2018 national aggregate, normalised):
state general revenue $23.77, health care related taxes $5.94, local government
IGT/CPE $4.19, other $1.40. Confirmed structurally current against KFF's 2025 survey
of SFY2026 enacted budgets. See S-034 on why the KFF figures are a check, not a
source.

**Basis warning.** State budget data runs on state fiscal years; the ledger runs on
federal fiscal years (D-07). Most states begin 1 July. This is a mixed-basis join and
must be stated on the artifact. Separately, "Medicaid's share of state budgets"
differs by roughly half depending on whether federal funds are counted; MACStats
publishes both for that reason. Whichever is chosen will be quoted without the
qualifier, so the artifact must carry it.

**This is structurally a state-edition exhibit.** Nationally it resolves to one flat
sentence. Louisiana, New York and Texas are entirely different stories, and those are
the stories a multi-state plan needs. Build it nationally per D-21, but write the
national instance knowing it is the weakest instance and say so.

### D-41 · Directed payment caps split by financing source, three ways

- **Provider tax financed.** As D-39. Taxed providers lose the federal match and stop
  paying the tax. State neutral. No gross-up.
- **IGT financed.** A public hospital or county transfers its own funds; cut the
  payment and the transfer stops. Loss is the federal match, same arithmetic, but the
  absorbing entity is a **local** government. Routes to a different line of the second
  ledger. D-03 node 4 already says "state and local," which was the right instinct
  before there was a reason for it.
- **State general fund financed.** The state share was real money that reached
  providers. Providers lose the full amount, federal and state. D-25's gross-up
  applies at full strength. **And the state does not face pressure; it saves money.**

**Financing mix:** roughly 68% provider-financed, 32% state general fund. Sourced to
ASPE (2026): $8.4B of $12.3B of the non-federal share of $35.8B in 2022 SDP spending.
Corroborated by MACPAC 2024, which found 26 of the 29 arrangements exceeding $1B/year
were financed by provider taxes or IGTs, and 24 of those targeted hospital systems.

**BLOCKING GAP.** ASPE reports provider tax and IGT combined. D-41 needs them apart,
because tax routes to the state line and IGT to the local line. CRS RS22843 gives a
partial handle (provider taxes were 51% of "other state funds" in SFY2018) but on a
different denominator. Held as `None` in `financing.py` per S-035; the D-41 render
cannot proceed until this is sourced.

**Lane shape note.** §71116 does not eliminate directed payments; it ratchets the
ceiling toward Medicare rates (110% in non-expansion states) at 10 percentage points
a year. This is a partial reduction of a continuing payment, a different shape from
the provider tax lane, and the encoding must not make them look alike.

### D-42 · The second ledger carries both directions

Relief renders as well as pressure. Provider tax limits create state pressure;
general-fund-financed directed payment cuts create state relief. A pressure-only
ledger is arithmetically wrong and a state budget office reader will catch it. The
net depends entirely on a state's financing mix, which is itself the argument for the
state series.

**Two consequences.**

1. **Diagram type conflict with D-40, unresolved.** D-40 describes a fan-out from a
   single trunk. A Sankey fan-out cannot render a negative band; relief flows the
   wrong way. D-42 has therefore made the second ledger closer to a two-sided
   sources-and-uses balance than to a Sankey. Both are drawable, not by the same
   renderer, and one of them is not a Sankey. **Open. Resolve before build.**
2. **Headline risk in netting.** If the second ledger nets small, the sentence that
   escapes is "HR-1 is roughly neutral for state budgets," which is false in every
   individual state and only arithmetically true in an aggregate nobody lives in.
   Gross flows must be visually dominant over the net.

---

## Corrections to existing material

**D-26 CORRECTION · its illustrative figures sit on the outlay basis.**
D-26 says the blend would put work reporting near $500B instead of ~$362B. Both are
computed from **$325.6B**, CBO's federal *outlay* reduction for §71119 (CRS R48755):
325.6 ÷ 0.647 = 503.2 and 325.6 ÷ 0.900 = 361.8. The FY2029 allocation and `ramp.py`
use **$317.0B**, the *deficit* effect. So the brief and the allocation already sit on
two different bases for the same section, an $8.6B wedge.

This confirms 90% was D-26's intended rate. It is also **direct evidence for open
task 2**: the outlay-to-deficit gap is attributable at section level, not spread
evenly. Testable hypothesis: the wedge concentrates in sections with revenue
interactions. Note that several secondary summaries (Families USA, Paragon, Applied
Policy) label their columns as federal outlays while reporting §71101 at $66.008B and
§71102 at $53.6B, the same figures the allocation treats as deficit effects. Some
sections may carry no wedge at all.

**`ramp.py` CORRECTION · the 0.40 weight on provider taxes blends two mechanisms.**
The phase-down (6.0% stepping to 3.5% by FY2032) applies **only to expansion states**
and **exempts nursing facility and ICF/IID taxes**. Non-expansion states are
**frozen** at July 2025 levels, not reduced, and lose only against a rising baseline,
which produces no year-one effect and widens over time. Two different time profiles
should not share a weight. Value left unchanged pending decomposition; flagged in the
file.

---

## Task 1 status (D-26 FMAP table)

| Lane | Rate | Status |
|---|---|---|
| Work reporting (§71119) | **90%** | Settled. Expansion adults + 1115 MEC-equivalent. §1905(y)(1) SSA; CRS R48633; CMS CIB 11/18/2025. |
| Six-month renewals (§71107) | **90%** | Settled. Same population, §1902(e)(14)(L); CMS SMDL #26-001. |
| Provider tax limits (§71115) | **n/a** | Resolved by D-39. No gross-up applies. |
| Directed payment caps (§71116) | **split** | Resolved in principle by D-41; blocked on the tax-vs-IGT split. |
| Blocked senior enrollment rule (§71101) | **open** | Needs non-expansion blended federal share. Note QMB/SLMB at regular FMAP but **QI is 100% federal** (CMS SMD 10-003), so part of this lane grosses up at 1.000. |
| Blocked Medicaid enrollment rule (§71102) | **open** | Needs the same figure. CBO's narrative names provisions weighted toward aged, blind and disabled enrollees, so the rate sits **below** 64.7%, not at it. CHIP/BHP contamination looks small: the scored provisions CBO describes are Medicaid. |
| Everything else | 64.7% provisional | Mixed residual (D-35); flag modelled. |

**Shared blocking dependency.** Three lanes now wait on one number: the
**non-expansion blended federal share**. Derivable from CMS-64 given FY2024 new adult
group total computable spending, since total federal share (64.7%) and the expansion
rate (90%) are both known. FY2023 is **unusable** for this derivation because the
FFCRA enhanced match ran through December 2023, which is D-10's own warning applied
to us. Requires the quarterly CMS-64 New Adult Group expenditure files from
MBES/CBES, a file pull rather than a search.

**Admin-match caveat for both settled lanes.** CBO's scores for §71119 and §71107 are
net of increased state administrative cost, which matches at 50% rather than 90%.
Grossing a net figure at the benefit rate is wrong in a known direction. CBO does not
break it out; footnote rather than adjust.

---

## Closed, do not reopen

- **Erin Henderson interview.** Closed 2026-08-27, first session. Not resurfaced.
- **Immigrant eligibility lane.** Footnote, not a lane. D-24 as amended.

## Open, in priority order

1. Non-expansion blended federal share (unblocks three lanes). CMS-64 file pull.
2. Outlay-versus-deficit reconciliation at section level (D-36, open task 2), now
   with a testable hypothesis from the D-26 correction.
3. Provider tax versus IGT split of SDP financing (unblocks D-41 render).
4. Second ledger diagram type: fan-out versus two-sided balance (D-40/D-42 conflict).
5. Decompose the `ramp.py` provider tax weight into expansion phase-down and
   non-expansion freeze.
6. MMIS/systems share of the CMS-64 administrative line (D-32).
7. RHTP appropriation amount and period, and DC eligibility (D-31).
8. Sensitivity range for the work reporting ramp weight (0.60 / 0.75 / 0.90).
