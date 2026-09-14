# Whitepaper Brief — National HR-1 Edition

**Working title:** $100 Medicaid Dollars — The National View and the Impact of HR-1
**Executive Producer:** JW
**Byline:** Jamey Harvey, Sheila Yahyazadeh  *(amended 2026-09-11, D-67)*
**Kickoff:** 2026-08-18
**Status:** structure approved, research in progress, no drafting started

---

## Purpose

A tool Medicaid and insurance professionals can use to explain what is happening
upstream and downstream of their own position in the ecosystem, and what HR-1 does to
their organization and their teams.

**Audience:** Medicaid and insurance professionals and executives. Expert in their own
lane, novice in adjacent ones. A hospital CFO knows DSH and does not know capitation
mechanics. Terms of art stay; each gets one clean gloss at first use.

**Series:** national first, then District of Columbia, then states where Agilian clients
operate plans.

---

## Decisions made at kickoff

### D-01 · The $100 unit under HR-1
**AMENDED 2026-08-27 (see D-22, D-23) and re-confirmed 2026-08-27 part 3.**
$100 = **2029 baseline spending under prior law** (the counterfactual), not 2028. 2029 is
the first full-effect year; a 2028 base carrying 2029 overlay figures would not sit on one
year. HR-1 flows sum to roughly $90, with the remainder rendered as gap bands peeling off
at the point each provision bites.

**PROVISIONAL pending verification (D-62, S-049).** The 2029 anchor rests on D-08's
claim that 2029 is the first full-effect year. That has not been checked against the
statutory phase-in schedule, and it is not true for at least two lanes: the provider
tax safe harbour and directed payment caps both ratchet in annual steps past 2029.
Settle by building the phase-in table from the enacted text of P.L. 119-21. The
denominator is available for any candidate year 2025–2035; the year is not constrained
by data availability. See `SOURCES.md`.

The ledger stays conserved: **$100 = dollars still flowing + dollars that stopped.**
The gaps *are* the conservation. Missing width becomes literally visible.

### D-02 · Cost shift, not savings
A dollar HR-1 removes does not vanish. It continues as uncompensated care, local
government burden, or unmet need. Gap bands **route to destination nodes past the provider
column** rather than terminating at the edge of the diagram. This is the distinguishing
feature of the piece.

### D-03 · Five destination nodes
1. Care that does not happen
2. Paid out of pocket by patients
3. Absorbed by federal offset programs
4. Unfunded state & local budget pressure
5. Absorbed by providers (bad debt & charity)

Node 4 exists specifically because JW asked that the state-match decision be shown as a
visible fork rather than a hidden assumption. The diagram does not assume whether states
can or will come up with the match.

### D-04 · Aggregate on the master, fan-out in Section VI
Section IV's master diagram carries the five destinations in aggregate (12 bands at the
right edge, legible in print). Section VI gets a dedicated fan-out: six provider nodes
against five destinations, where the outline already asks for the provider breakdown.

Caveat to carry into Section VI: the utilization drop almost certainly varies by service
type. Nursing home care does not stop the way a deferred specialist visit does. The
fan-out is explicitly modeled and flagged as such.

### D-05 · CBO's backfill assumption is used as-is
CBO already assumes partial state backfill inside its estimate — it expects states will not
replace all lost provider tax revenue and will instead cut provider rates or tighten
eligibility. That behavioral response is baked into the provision totals. **Do not apply an
additional backfill multiplier; it would double-count.**

### D-06 · The uncompensated-care catch rate is built bottom-up, not assumed
Three forks, each with its own literature:

| Fork | Question | Status |
|---|---|---|
| 1 | Does the care happen at all? | **OPEN** — need a defensible insured-vs-uninsured utilization figure |
| 2 | Of care delivered, who pays? | ~70% uncompensated, ~20% out of pocket (Urban, MEPS, stable pre- and post-ACA) |
| 3 | Of uncompensated care, who absorbs it? | ~80% offset by government funds; ~20% true provider bad debt & charity |

JW's original 20% instinct lands at **Fork 3** — the provider-absorbed residual.

**Finding that should become a section of the paper:** the ~80% public offset was measured
under conditions HR-1 is actively dismantling. The offset channels are Medicaid DSH, state
and local indigent care, and public hospital support — and the provider tax cap constrains
exactly the money states use to fund them. More uncompensated care arriving alongside less
capacity to defray it. The Rural Health Transformation Program partially offsets and belongs
in the diagram as a labeled counterflow, not silently netted.

### D-07 · Basis is federal fiscal year
Matches CBO's own convention and the CMS-64 basis of the ledger.

### D-08 · 2028 is mid-ramp, and the paper says so
CBO: outlays fall **$46.7B in FY2027, $62.7B in FY2028, $92.9B in FY2029.** 2028 sits about
two-thirds up the ramp. A full-phase callout is required so no reader mistakes mid-ramp for
the endpoint.

### D-09 · Provision decomposition does not sum cleanly
Provisions interact — someone who loses coverage to work requirements cannot also lose it to
six-month renewals. Present each provision's independent contribution plus an interaction
adjustment line, with a note on why the parts exceed the whole.

### D-10 · Baseline vintage: FY2024, and it is current
The national build is on CMS-64 FY2024 from the February 2026 MACStats. Total spend
$957.4B, benefits $908.8B, federal share 64.7%.

**Section II must not introduce this as "older data."** It is the most recent complete
fiscal year available. The honest caveat is the mixed vintages inside the composite:
HMA payer mix CY2021, group shares FY2023, duals CY2022. State those plainly.

Note for the Author: the federal share fell from 69% (FY2023) to 64.7% (FY2024) as the
FFCRA enhanced match unwound. A build sitting on FY2023 would have had a structurally wrong
federal-local split and every leverage figure with it.

### D-11 · Structure held constant from FY2024 to the 2028 counterfactual
Per-$100 shares are treated as stable; structural shares move slowly. Absolute 2028 dollar
magnitudes appear in a sidebar table sourced to CBO, so projection uncertainty sits in one
labeled place instead of spreading through every band.

### D-12 · Section VI uses the six ledger nodes
Long-term care, Hospitals, Physicians & clinics, Wrap around services, Behavioral health,
Rx drugs. The ad hoc Providers/Doctors/Hospitals/FQHCs list is withdrawn.

FQHCs cannot be separated from Physicians & clinics without new data. Possible **sourced
sidecar callout** on FQHC exposure if the research supports it — to be brought forward
concretely, not decided in the abstract.

### D-13 · Diagrams may leave brand guidelines
Clarity and consistency outrank branding inside the Sankey. Page furniture stays on brand.

### D-14 · Three payer families
- **Carriers** — blue/indigo. Reserved per national parent.
- **Health-system plans** — violet/purple. Reserved. Provider-sponsored plans from national
  hospital brands (MedStar, Johns Hopkins, Mayo, UPMC, Geisinger, Children's National).
- **Local/regional** — teal/green ramp, shared family, ranked by size within the state.
- **Payer types** (PACE, D-SNP) — desaturated slate, fixed regardless of operator.

Rule: **cool = money moving, warm = money stopping.** No baseline flow is ever warm; no loss
band is ever cool. Fee-for-service stays neutral slate because it is not a payer.

HSCSN reclassified from local to health-system (Children's National). DC therefore has zero
true "local" plans.

### D-15 · Loss family encoding
Anchor `#8B5A5A`. Five treatments varying in value **and texture**, so absence reads in
grayscale print and photocopies where hue carries nothing. Verified.

### D-16 · Print bar: publish-ready programmatic PDF
HTML with print CSS, Jost and Nunito embedded, rendered to PDF. Clean, on-brand, correct
type and colour. A designer would notice it was not laid out by hand; the readership will
not. **Build toward a finished PDF, not a designer handoff package.** Designer decisions
optimise for what renders reliably in print CSS.

### D-17 · Byline and author bios
**AMENDED 2026-09-11 by D-67. The co-author is Sheila Yahyazadeh.**
Jamey Harvey and Sheila Yahyazadeh.

**Sheila Yahyazadeh (as supplied by JW; one typo fix marked):**
> Sheila Yahyazadeh is the Chief External Operations Officer for CareFirst BlueCross
> BlueShield Community Health Plan Maryland. She has over a decade of experience working
> with government health programs including Marketplace, Medicaid, and Medicare. She
> specializes in business strategy, growth operations, innovation, and partnership building.
> Sheila is passionate about elevating the voice of consumers and the community to improve
> equitable access to care. Through partnerships with providers, community stakeholders,
> startups, and the state, she has built pathways to care access [for] historically
> underserved and disadvantaged communities. Prior to joining CareFirst BCBS, Sheila led
> strategic campaigns and CX initiatives for Fortune 100 healthcare clients. She also
> spearheaded a health innovation team that brought together cross functional expertise in
> AI/machine learning, creative services, and UX/UI to reimagine how healthcare is
> delivered. Sheila is committed to innovation as an advisor to start-up founders. She has a
> bachelor's in Human and Global Security as well as a Master's degree in Public
> Administration and Health Policy from American University. She is first generation
> American, daughter to Peruvian and Iranian parents. She is also a certified Health Coach,
> Yoga Instructor, and an avid traveler.

*Copy Editor: "pathways to care access or historically underserved" reads as a typo for
"for"; inserted. "creatives services" closed to "creative services". Nothing else touched.*

**Editorial note — the bio needs no regional variant, which is a change from the previous
co-author.** It opens on a current operating role at a Medicaid managed care organisation
and never depends on a local signal a reader outside the region would have to decode. It
runs as written in the national edition and in every state edition.

**Two substantive hooks in her background, replacing the two D-17 previously carried:**
1. She sits inside a Medicaid plan today, in external operations. The payer column and the
   plan checklist in Section V are the parts of this paper most exposed to being wrong about
   how a plan actually behaves, and she is a primary source on both.
2. Partnership building with providers, community stakeholders and the state speaks directly
   to Section VII, where the paper has to say what a contraction does to access without
   a sourced routing model behind it.

**One layout consequence.** The bio runs roughly twice the length of Jamey's. Either trim
for the national edition or extend Jamey's to match; the decision belongs at layout and the
bio is carried verbatim until then.

**Superseded, recorded rather than deleted (S-032).** Erin Henderson was co-author from
kickoff on 2026-08-18 until 2026-09-11. Her bio, the Ward Four / Ward Five DC framing, the
D-SNP credibility hook for Section IV and the Community of Hope FQHC hook for the provider
sections all came off the board with her and must not be relied on anywhere downstream. The
closed interview (see the 2026-08-27 appends) is now moot rather than closed.

**Jamey Harvey (as supplied by JW; two typo fixes marked):**
> Jamey Harvey is a Ward Four resident and the CEO of Agilian LLC, a boutique CBE firm
> helping Medicaid beneficiaries stay enrolled. Jamey got into Medicaid when [he] led the
> technology implementation of Obamacare in the District. Previous to starting Agilian,
> Jamey was the Deputy Chief Technology Officer for software and data during the Williams
> Administration. Jamey is a seven-time entrepreneur and the author of "Wired for White:
> Confessions from Silicon Valley on the technology of racism," scheduled to be published in
> 2028. Jamey has a degree in political theory from UC Santa Cruz and two kids in college.

*Copy Editor: inserted "he" after "when"; closed the space in "seven- time".*

**WITHDRAWN 2026-09-11 by D-67.** The Ward Four / Ward Five pairing was an asset of the
previous byline and cannot be reconstructed. The DC edition now has one resident author, and
the local credential it leans on has to be found somewhere other than the bios.

**Raised once, JW's call:** *Wired for White* in the byline is authentic and on-brand for a
justice-driven firm, and hiding it would be its own kind of tell. It also signals something
about the author before a reader reaches the analysis, in a paper that holds non-partisan
framing on motive (S-003) and travels to plans across many political geographies.
**Recommendation: keep it.** A variant without it is a two-minute change if a particular
edition calls for one.

**AMENDED 2026-09-11 by D-67.** The bios no longer close in parallel: Jamey's ends on two
kids in college, Sheila's on parentage, a health coaching certification and travel. The
humanising function survives and the symmetry does not. Do not manufacture the symmetry by
editing either bio.

### D-67 · The co-author is Sheila Yahyazadeh
JW, 2026-09-11. Recorded here because five places in the brief and the appends cite
D-67 as the superseding decision and none of them stated it. A reference with no
definition is the same defect as a stale in-place entry (S-044), read from the other
end: the next person to follow the citation finds nothing.

Erin Henderson was co-author from kickoff on 2026-08-18. The byline is now Jamey
Harvey and Sheila Yahyazadeh, Jamey leading, on the cover and on the author page. Bio
supplied verbatim by JW and amended into D-17. The interview closure recorded in the
2026-08-27 appends is moot rather than closed, and the two credibility hooks it left
standing are withdrawn and replaced; see D-17 as amended.

**Disclosure, added by the Author and open for JW's ruling.** A sitting officer of a
Medicaid managed care organisation is now a co-author of a paper that prints a plan
administration band and a public-company earnings band. The rendered author page
carries four lines stating the role, that CareFirst BlueCross BlueShield Community
Health Plan Maryland is a nonprofit and therefore outside the $0.76 public-company
earnings figure (EN-43 as amended), and that the plan administration band is a
national aggregate from CMS-64 and MACStats containing no plan-specific figure. All
three statements check against the build. Two open questions belong to JW: whether the
disclosure sits at the foot of the author page or on the cover, and whether the
co-author reviews the wording before it ships. It should not ship unreviewed.

### D-18 · Fork 1 utilization drop: 26% central case
Source: Oregon Health Insurance Experiment (Finkelstein et al., NEJM 2013). Medicaid
coverage raised annual medical spending across Rx, office visits, ED, and hospital
admissions by $1,172, about 35% over control. Inverted: uninsured spending runs ~74% of
insured, a **26% drop** on coverage loss.

Why it transfers well: the study population is able-bodied uninsured adults below 100% FPL
who wanted coverage — close to a direct match for the expansion adults that work
requirements and six-month renewals actually hit. Duals and LTSS beneficiaries are largely
exempt from those provisions, so the usual population-mismatch objection mostly does not
apply. It is also lottery-randomised, so the claim is causal, not associational.

- **Central case 26%. Sensitivity at 20% and 35%.**
- Applies to **coverage-loss provisions only.** Financing cuts do not work through
  utilization and need separate treatment.
- Observational comparisons show far larger gaps (e.g. insured vs uninsured diabetes
  spending of $13,706 vs $4,367 below 138% FPL). **Cite as an upper bound; do not average
  with the RCT.** Selection confounds it — sicker people obtain coverage.

**Counterintuitive finding for Section VI:** Oregon raised ED visits ~40%. Coverage
*increases* emergency department use; it does not reduce it. Many readers hold the opposite
belief, and the paper should correct it explicitly.

### D-19 · Section VI human-impact sourcing
CBO and CMS for coverage loss and uncompensated care. **Peer-reviewed only** for mortality
or morbidity. Nothing from advocacy modelling on contested health outcomes. Keeps S-003
intact: unflinching on consequence, without reaching past what survives scrutiny.
*Claude default, not a JW ruling — flag on review.*

### D-20 · Section VII CTA — interim, with a spec for marketing
No subscribe form or state-request form exists yet.

**Interim (ships without new infrastructure):** CTA points at `communications@agilian.com`
with a stated subject-line convention for state requests, matching what the published
chapters already do.

**Spec for marketing:** one landing page, two actions — subscribe to the series, and
request a state. State field as a **dropdown**, so responses arrive clean rather than as
free text. Mirrors the 2025 playbook sign-up flow that fed `Playbook Sign-ups.xlsx`.

If the page lands before publication, swap the email CTA for the URL. **This is no longer a
publication blocker.**

### D-21 · Length
Build full (~30–40pp), then cut. Cutting is easier than expanding, and the national edition
sets the template for the state series.
*Claude default, not a JW ruling — flag on review.*

---

## Structure

| § | Content | Diagram |
|---|---|---|
| I | Introduction: the research, who it is for, objectives | — |
| II | End-to-end national baseline, phase by phase | FY2024 master |
| III | Phase-shift breakdowns, baseline | Vertical slices |
| IV | Overall impact of HR-1, by root cause, left to right | 2028 HR-1 master |
| V | Phase-shift breakdowns under HR-1 | HR-1 vertical slices |
| VI | Provider revenue loss + human impact; baseline vs HR-1 | Six-node fan-out |
| VII | Afterword: state series, DC next, subscribe & request | — |
| VIII | Endnote citations | — |
| IX | How Claude AI was used | — |

*(Outline had two Section VIIIs; renumbered.)*

Sections III and V are structurally parallel by design, which collides with standing note
S-008. Each subsection must carry a distinct analytical claim rather than a template with
numbers swapped. **Section V will be returned if it reads as Section III with red bands.**

---

## Open items

| # | Item | Owner | Blocking |
|---|---|---|---|

| O-6 | Claude disclosure — needs marketing/legal routing? | JW | Section IX |
| O-7 | Vertical phase-slice render mode does not exist yet | Designer | Sections III & V |
| O-9 | Provision-level 2028 split — CBO gives 10-yr totals by provision, FY totals in aggregate | Research | Section IV root-cause bars |
| O-10 | Landing page build | Marketing | Section VII (interim in place) |

*Closed at kickoff: O-1 (D-18), O-2 (D-16), O-4 (D-21), O-5 (D-20), O-8 (D-19).*

---

## Deliverable

Print-ready PDF in the style of the 2025 playbooks. Documents managed in the project;
code and approved-final artifacts pushed to GitHub.
