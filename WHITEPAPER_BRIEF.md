# Whitepaper Brief — National HR-1 Edition

**Working title:** $100 Medicaid Dollars — The National View and the Impact of HR-1
**Executive Producer:** JW
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
$100 = **2028 baseline spending under prior law** (the counterfactual). HR-1 flows sum to
roughly $90, with the remainder rendered as gap bands peeling off at the point each
provision bites.

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
| O-1 | Fork 1 utilization ratio — insured vs uninsured | Research | Section IV modeling |
| O-2 | Print-quality bar: programmatic PDF vs human designer pass | JW | Designer approach |
| O-3 | Byline and credentials | JW | Cover |
| O-4 | Target length (currently scoped ~30–40pp) | JW | Scope |
| O-5 | Subscribe URL + state-request mechanism | JW / marketing | Section VII |
| O-6 | Claude disclosure — needs marketing/legal routing? | JW | Section IX |
| O-7 | Vertical phase-slice render mode does not exist yet | Designer | Sections III & V |
| O-8 | Human-impact sourcing: peer-reviewed only, or broader | JW | Section VI |

---

## Deliverable

Print-ready PDF in the style of the 2025 playbooks. Documents managed in the project;
code and approved-final artifacts pushed to GitHub.
