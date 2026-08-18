# $100 of Medicaid — Per-State Build Playbook
*A runbook for spinning the national model into a per-state variant. Encodes the process, the
decision points, and JW's standing answers so the next state can be built semi-autonomously.*

DC was the first state built. This document generalizes what we did so the next state (call it
`<ST>`) can be produced with minimal back-and-forth. Where a decision has already been settled,
it's marked **[JW DEFAULT]** — assume that answer unless JW says otherwise. Where a judgment is
genuinely state-specific, it's marked **[ASK / CHECK]**.

---

## 0. Philosophy (the two invariants)

1. **The Sankey is a conserved ledger.** Everything sums to $100 of that jurisdiction's *total*
   Medicaid spending. Nothing enters or leaves un-accounted. Seven balance checks enforce this and
   the build refuses to render if any fail.
2. **Sidecars may depart from the ledger — but only with provenance.** Headlines, custom analyses,
   and the systems-money panel are *not* conserved into the $100. They live outside it and each
   fact must carry **source + vintage + basis**. [JW DEFAULT] Keep the model pure; let sidecars
   depart as long as every departing number is sourced.

> Mental model: the ledger answers "where does a recurring care dollar go." Anything that answers a
> *different* question (what match rate does an admin dollar earn; what's the economic ripple of a
> cut) does not belong inside the conserved flow — it goes in a sidecar.

---

## 1. Data sources (spine vs. enrichment)

```
SPINE  (authoritative, all 51 jurisdictions, conserves):
  CMS-64 / MACStats FY<YYYY>
    Exhibit 16 — spending by state, category, source of funds  -> federal/state split, admin
    Exhibit 17 — total benefit spending by state and category  -> FFS service itemization + MC lump
ENRICHMENT (state-specific, reconciles UP to the spine with documented residuals):
  State Medicaid managed-care performance report   -> per-MCO capitation revenue, claims, admin
  State budget book / agency financial tables       -> program detail, cross-checks
  State PACE page / D-SNP page / BH integration page -> payer landscape
  KFF state fact sheet, Census ACS                   -> headline context (coverage, enrollment)
```

[JW DEFAULT] **CMS-64/MACStats is the spine for every jurisdiction.** The state budget book and
managed-care report are the secondary enrichment layer; detailed branches must **reconcile up** to
the MACStats lane/node totals, and any gap is a **documented residual**, not a silent fudge.

[ASK / CHECK] Pull the current MACStats vintage each cycle — exhibit URLs change yearly.

---

## 2. The phase-column framework (the visual spine)

```
FEDERAL | LOCAL/STATE | <ST> AGENCY | DISBURSEMENTS | PAYER | (CLAIMS) | PROVIDERS | (BENEFICIARIES)
```

[JW DEFAULT] Keep the national framework's columns. Two hard structural rules, both learned the
hard way on DC:

- **RULE A — Fee-for-service has no payer.** FFS splits into its service streams *at the agency*
  (the DISBURSEMENTS column) and runs **straight through the PAYER column unchanged** to the
  providers. No plan-admin peel touches it. The state pays the provider directly.
- **RULE B — MCOs are payers, color-coded into services.** Each MCO sits in the PAYER column,
  receives capitation, **peels its plan administration & margin**, then **splits its remaining
  care into the services it funds** and stays **its own color** all the way into the provider bars,
  so a viewer can read how much each payer contributed to each service.

[JW DEFAULT] Build a **purpose-made, parameterized** per-state script (geometry computed from the
data) rather than hacking the hand-tuned national 2200px SVG. The national file's fixed coordinates
don't survive a different lane/node count. Reuse its palette, fonts, and `band/rect/txt/lbg` helpers
for family resemblance.

---

## 3. Build sequence (pseudocode)

```
BUILD_STATE(<ST>):

  # ---- 3.1 SPINE LEDGER (per $100 of total Medicaid) ----
  SCALE = total_medicaid_$M / 100           # everything divides by this
  fed, state         = federal_share, local_share          # Exhibit 16 (blended, incl expansion)
  admin              = state_program_admin / SCALE          # Exhibit 16 admin line
  medicare_premiums  = dual_medicare_premiums / SCALE       # leakage back to federal; from Exhibit 17
  mc_total           = managed_care_lump / SCALE            # Exhibit 17 managed-care line (INCLUDES PACE + dual + ABD)
  ffs                = (ffs_service_total) / SCALE          # Exhibit 17 FFS columns minus medicare premiums, net of collections
  disbursed          = 100 - admin - medicare_premiums
  ASSERT fed + state == 100
  ASSERT mc_total + ffs == disbursed

  # ---- 3.2 FFS ITEMIZATION (measured, from Exhibit 17) ----
  ffs_node = {
    Long-term care:       institutional_LTSS + HCBS_LTSS,
    Physicians & clinics: physician + other_practitioner + clinic/health_center,
    Hospitals:            inpatient + outpatient hospital,
    Wrap around services: dental + other_acute + (collections folded here, usually negative),
    Rx drugs:             prescribed_drugs                 # OUTPATIENT PHARMACY ONLY (see node-scope rules)
  }
  ASSERT sum(ffs_node) == ffs
  # NOTE: behavioral health is usually NOT its own Exhibit-17 line; it's embedded in clinic/physician/other.

  # ---- 3.3 PAYER SPLIT (enrichment: state MC performance report) ----
  carve PACE (and any tiny dual-only capitation) OUT of mc_total first:
      pace    = pace_capitation / SCALE        # [CHECK] order-of-magnitude ok if program is new/small
      mco_cap = mc_total - pace                # the comprehensive plans
  for each comprehensive MCO p:
      cap[p]  = revenue[p] / sum(revenue) * mco_cap        # split by CY capitation-revenue share
  # *** BASIS-MISMATCH FIX (learned on DC/HSCSN) ***
  # If one plan's reported revenue is on a DIFFERENT basis than the others — e.g. a Medicaid-only
  # special-needs plan whose revenue is pure Medicaid, while the comprehensive plans' revenue still
  # carries locally-funded (Alliance/state-only) enrollees — then splitting ALL plans by raw revenue
  # UNDER-WEIGHTS the Medicaid-only plan. Instead: ANCHOR that plan at its actual Medicaid capitation
  # and split the Medicaid residual among the rest.
  #   anchor_cap = special_plan_medicaid_capitation / SCALE
  #   cap[special] = anchor_cap
  #   for p in comprehensive: cap[p] = revenue[p]/sum(comp revenue) * (mco_cap - anchor_cap)
  # [CHECK] A very high PMPM at small enrollment (special-needs/SSI children) is the tell: the dollar
  # total can look small even when the rate is several times the comprehensive plans'. Verify the
  # plan's total against the source before trusting a proportional split.
      care[p] = cap[p] * (claims[p] / revenue[p])          # claims/revenue = the medical (care) fraction
      admin_margin[p] = cap[p] - care[p]                   # peeled in PAYER column
  ASSERT sum(cap) == mco_cap

  # ---- 3.4 MCO -> SERVICE MIX (MODELED proxy — flag it) ----
  mix = national_managed_care_service_mix     # behavioral folded into Physicians & clinics
  mco_contrib[p][s] = care[p] * mix[s]        # each MCO's dollars across services
  # [JW DEFAULT] flag this as modeled on the artifact + footnote; encounter data would replace it
  # and (in most states) shift MCO dollars toward acute (hospitals/physicians/Rx) and away from LTC.

  # ---- 3.5 PACE -> 100% LONG-TERM CARE ----
  node[Long-term care] += pace                # [JW DEFAULT] PACE is a separate payer, all to LTC

  # ---- 3.6 PROVIDER NODES = FFS (measured) + each MCO (modeled, colored) + PACE (LTC only) ----
  node[s] = ffs_node[s] + sum_p mco_contrib[p][s] (+ pace if s == Long-term care)

  # ---- 3.7 SEVEN BALANCE CHECKS (refuse to render on any fail) ----
  ASSERT sources sum to 100
  ASSERT uses (admin + medicare + mc_total + ffs) == 100
  ASSERT lanes == disbursed
  ASSERT MCO caps sum to mco_cap
  ASSERT FFS nodes sum to ffs
  ASSERT each MCO: care + admin_margin == cap
  ASSERT provider nodes sum to care delivered (ffs + mco_care + pace)

  # ---- 3.8 RENDER ----
  # [JW DEFAULT] Order payers in the PAYER column SMALLEST -> LARGEST, top to bottom (PACE at top,
  #   biggest comprehensive plan at the bottom). Route PACE's band to the TOP of the LTC node so it
  #   stays a clean short path. Float tiny-payer labels above the lane if they'd collide.
  draw phases; FFS through payer unchanged (Rule A); MCOs colored into services (Rule B);
  PACE as its own thin payer band -> LTC; legend "WHO PAYS (colour)"; footnotes for every proxy.
  render PNG -> eyeball -> fix collisions -> copy to outputs -> present.
```

---

## 4. Payer landscape scan (run EVERY state — the "what's hiding" checklist)

The managed-care lump hides things. Before finalizing, scan the state's delivery system and decide
where each piece goes. DC answers shown as the worked example.

```
[ ] Comprehensive MCOs        -> PAYER column, one colored bar each (from MC performance report)
                                 DC: AmeriHealth Caritas, Wellpoint/Elevance, MedStar Family Choice
[ ] Special-needs plan        -> its own payer bar if separately capitated
                                 DC: HSCSN (CASSIP, Children's National) ~10% of MC lump
[ ] PACE                      -> SEPARATE payer -> 100% LTC. CMS-64 files it under managed care,
                                 so carve it OUT of the lump. DC: Edenbridge (Element Care/Edenbridge
                                 Health), Wards 7&8, tiny/new. [JW DEFAULT] always its own band.
[ ] Dual-eligible D-SNP       -> SEPARATE capitated payer: give it its OWN thin band carved from the
                                 lump (like PACE), flowing to the Medicaid services duals actually use
                                 -- LTSS (LTC) + dental/behavioral (wrap). Medicare pays the acute care
                                 so the band stays THIN even though the program is a major one. TRACK IT;
                                 do not let it drop when restructuring the payer column. BEWARE a budget-
                                 book "Dual Choice" line that bundles Medicare A/B/D -- not the Medicaid #.
                                 DC: UnitedHealthcare "District Dual Choice"; ~$25M Medicaid wrap (MODELED,
                                 ~$0.57). Most dual LTSS is still FFS in the LTC node (optional plan,
                                 partial enrollment). ($305M total-program figure incl Medicare = the
                                 earlier over-count; do not use it.)
[ ] Behavioral health         -> [CHECK] carved IN to MCOs, or FFS via a state BH agency/ASO, or PHP?
                                 DC: historically FFS via DBH-certified providers (MHRS/ASURS/FSMHC);
                                 MCO carve-in was PAUSED Feb 2024, so FY2024 = transitional FFS lane
                                 embedded in the existing nodes. Watch for the carve-in completing.
[ ] NEMT (transportation)     -> usually a BROKER/ASO (not a risk payer); a vendor inside FFS/MCO.
                                 DC: MTM. Footnote, not a lane.
[ ] Dental / vision / pharmacy-> [CHECK] carved in or out? DC: carved IN to MCOs (no separate PBM/DBM).
[ ] ACOs / CINs / VBP         -> downstream PROVIDER arrangements, not payer lanes, unless the state
                                 has true risk-bearing Medicaid ACOs. DC: none as payers.
[ ] IDD / HCBS waivers        -> FFS HCBS inside the LTC node (run by a disability agency). DC: DDS IDD waiver.
[ ] Locally-funded programs   -> EXCLUDE from the federal-Medicaid spine. DC: Alliance / ICP (local $).
```

[JW DEFAULT] Only things that are **separately capitated risk-bearing payers** earn their own band
(MCOs, special-needs plan, PACE, and — if material — a dual sliver). Brokers, ASOs, CINs, and FFS
delivery systems are vendors/arrangements inside existing lanes, noted in footnotes.

---

## 5. Node-scope rules (what each provider node does and does NOT include)

```
Rx drugs        = OUTPATIENT PHARMACY BENEFIT ONLY. Often NET of rebates (rebates show up as the
                  negative "collections" line). UNDERSTATES true drug spend badly.
Hospitals       = INCLUDES drugs administered in the facility (inpatient + hospital outpatient).
Physicians&clinics = INCLUDES office/clinic-administered drugs (J-codes).
=> Drug dollars are scattered across Rx + Hospitals + Physicians + (un-itemized) MCO lump.
LTSS / LTC      = Exhibit 17 LTSS columns are FEE-FOR-SERVICE ONLY. Managed LTSS, dual-plan LTSS,
                  ABD-plan LTSS, and PACE are all in the managed-care lump, NOT the FFS LTC node.
                  => FFS LTC is a FLOOR, not the total. The all-in figure needs CMS/T-MSIS LTSS data.
Behavioral health = usually embedded (no separate Exhibit-17 line); folded into Physicians&clinics
                  in the modeled MCO mix. Track the state's carve-in status.
```

[JW DEFAULT] State each node's scope explicitly in footnotes. These scope facts are the source of
the recurring "the visible number understates X" headlines (LTC, drugs).

---

## 6. Headlines sidecar (`headlines.json` + `build_headlines.py`)

Separate from the conserved ledger. Invariant = **PROVENANCE**, not conservation. Schema requires
`id, n, headline, stat, derivation, basis, source, url, vintage`; `derivation in {ledger, external,
modeled}`; the validator fails nonzero on any violation (the headline-layer analog of balance checks).

**The seven canonical questions** (re-answer per state; DC framings shown as the template):
```
1. How big is the program in absolute $?                ("Nearly $5 billion a year.")
2. How big relative to the local budget?                ("Almost a quarter of the city budget.")
3. What is this state unusually heavy/light on?         ("No state leans harder on long-term care.")
4. Coverage / uninsured trend.                          ("Near-universal — but the gap just doubled.")
5. Share of population on Medicaid.                      ("More than one in three Washingtonians.")
6. The match math (LEDGER-coupled fact).                ("For every local dollar the federal
                                                          government sends almost three.")
7. Exposure to federal cuts (modeled).                  ("The bite deepens fast — ~1 in 25 by 2027...")
```

[JW DEFAULT] framing preferences:
- **State perspective, not national.** Frame cuts/effects from the jurisdiction's seat.
- **Care basis** for cut math (then gross up to total program $ if needed).
- **Drop cumulative** framings; use per-year.
- Say **"the federal government sends,"** not "Washington" (esp. for DC).
- **Punchy** headline, precise sub-stat.
- Fact #6 is the only ledger-coupled headline; `ledger_check` cross-checks it against the ledger's
  blended federal share (tolerance ~0.5pp).

---

## 7. Custom-analysis library (non-portable, per-state)

`headlines.json -> custom_analysis_library` holds reusable *types* of analysis that are NOT portable
across states. Each requires `id, title, question, portable:false, status`; draft/final also need
`derivation, basis, sources`. The validator warns if `portable:true` is set.

```
economic_ripple   (DC = filled example, status draft): tax-base + health-workforce effects of a cut.
                  DC specifics that make it non-portable: Home Rule Act bars taxing non-resident
                  wages (>60% of workforce), >50% of property tax-exempt, regional leakage to MD/VA
                  => own-source revenue loss is structurally muted/exported. Scaled from Commonwealth
                  Fund IMPLAN ratios (~$1.30 GDP, ~$0.10 state/local tax per $1 federal cut).
```

[JW DEFAULT] Anything state-idiosyncratic goes here, explicitly flagged `portable:false`, never in
the shared 7-fact spine.

---

## 8. Systems-money sidecar (enhanced-match administration)

[JW DEFAULT] Do NOT force one-time IT/systems money onto the conserved $100. It's a different match
ratio AND a different time-base (lumpy capital vs. recurring). Put it in its own panel that conserves
to the **admin total** (not to $100), with its own basis.

```
Administration splits by federal match rate (Section 1903(a)(3), confirmed current):
  Operating administration ........ 50% federal   (routine ops — the LEAST-matched dollars)
  Systems M&O ...................... 75% federal   (ongoing operation of MMIS/E&E systems)
  Systems DDI (one-time builds) .... 90% federal   (design/dev/install — the MOST-matched; lumpy)
Insight: admin spans 50-90% federal, BRACKETING the care blend. DDI (90%) ties expansion care.
```
[ASK / CHECK] The three-way split values need a **CMS-64 administrative-line / APD pull** per state;
until then they're illustrative. A prototype three-way sub-peel exists in the DC builder but [JW
LEANING] it belongs in the sidecar, not on the main flow (the DDI sliver is ~invisible at conserved
scale and the lumpiness breaks cross-year comparability).

---

## 9. Known proxies & flags (always surface on the artifact)

```
* MCO -> service mix      = MODELED (national managed-care mix). Replace with state encounter data.
* PACE $                  = order-of-magnitude if program is new/small.
* Dual D-SNP              = small Medicaid-only; folded/footnoted.
* Admin three-way split   = ILLUSTRATIVE pending CMS-64/APD.
* Alliance/local $        = folded for proportion only where it bleeds into MC revenue figures.
* Rx node                 = net of rebates; understates drug spend.
```

---

## 10. Engineering norms

```
* Single source of truth: raw inputs at the top of the builder; no magic numbers buried in render code.
* grep -nE before any refactor to catch variable-name collisions (the national `L`-as-loop-var bug
  silently clobbered the ledger handle once).
* Multi-substitution patch scripts: guard with .count() so a rename hits the expected number of sites.
* Always: edit -> run builder (must PASS all balance/provenance checks) -> cairosvg render ->
  view PNG -> fix collisions -> cp to /mnt/user-data/outputs -> present_files.
* Render is cheap; iterate on layout collisions visually rather than reasoning about pixels blind.
```

---

## 11. One-line summary for the next state

> Pull MACStats Exhibits 16 & 17 for `<ST>`; build the conserved $100 spine; itemize FFS to the five
> nodes; pull the state MC performance report to split the managed-care lump by per-plan capitation
> revenue and peel each plan's admin via claims/revenue; carve PACE out as its own payer to LTC; fan
> MCO care into services with the national mix (flagged modeled); run the seven balance checks; run
> the payer-landscape checklist; write the seven headlines with JW's framings into the provenance
> sidecar; keep systems money and any ripple analysis in sidecars. Flag every proxy on the artifact.
