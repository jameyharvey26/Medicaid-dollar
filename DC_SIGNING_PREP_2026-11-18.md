# Preparing the District signatures — what has to be fixed before anyone signs

Written 18 November 2026 by Claude, working §1 of `NEXT_SESSION_PROMPT_13_1.md`.
Nothing here is signed and nothing here proposes that Claude sign anything.
`verified` is "YYYY-MM-DD initials" and the initials belong to a person who
opened the source.

Read with `DC_SIGNOFF_LIST.md`, which is the tiered worklist this amends.

---

## The short version

The 41 MEASURED District figures are **not yet a signable set**, for four
separate reasons, and one of them is structural: `_sign` is not wired into the
District ledgers at all, so a filled register would currently do nothing.

Of the 26 measured figures on DC FY2024:

| | figures | state |
|---|---|---|
| signable once the register is wired | 13 | sources reconcile exactly; see §3 |
| status is wrong — not measured | 4 | §4.1 |
| plate value is not what the source prints | 9 | §4.2 |

The 15 measured figures on DC FY2030 are anchors with named sources and are in
better shape; none has been opened this session.

---

## 1. The structural blocker: DC has no signing path

`_sign` is defined **inside `ledger_national_2024.py`** (line 135) and called
only from that module's `build()`. `ledger_dc_2024.py`, `ledger_dc_2030.py`,
`ledger_dc.py` and `ledger_national_2030.py` contain no reference to
`signatures`, `SIGNED`, `UNSIGNED` or `REVIEW`.

So the gap is not only that `signatures.py` carries no DC entry. There is
nowhere for a DC entry to be read. Adding DC lines to `SIGNED` today would
change nothing on the plate and `coverage.py` would go on reporting every DC
figure as STALE.

Two things have to happen, in this order:

**1a. Lift `_sign` out of `ledger_national_2024.py`.** It is generic — it walks
`sources`, `scale`, `peels`, `payers` and the matrices and builds keys from
structure. Nothing in it is national. It belongs in `ledger.py` or a small
`signing.py`, taking the register as an argument.

**1b. Namespace the register.** `SIGNED` is a flat `key -> value` dict, and the
District reuses national key strings exactly:

    scale · peel.admin · peel.medicare · payer.ffs.capitation ·
    payer.ffs.care · payer.dual.capitation · payer.dual.care ·
    payer.mco.capitation · source.federal · source.state

If DC lines were added to the same dict, `scale` would be signed at 9501.64 for
the national panel and 43.72 for the District, and whichever was written last
would silently LAPSE the other. The whole point of the register is that it
cannot silently carry a signature onto a number nobody has seen; a flat
namespace reintroduces exactly that failure in a new direction.

**Recommended convention: the one already in use.** `DC_ENDNOTE_KEYS.txt` keys
every District figure as `DC24:<key>` / `DC30:<key>`. Use the same panel prefix
in the register, and give the national panel `NAT24:` on the same move, so no
key is ambiguous and the register reads the same way as the endnote registry.
That is a mechanical rename of 36 existing national lines, and the national
values do not move, so it costs no new signature — but it does touch
`ledger_national_2024._sign`, so it is a change to make deliberately and prove
byte-identical before the DC lines go in.

This is a decision, not a cleanup. Next free number is **D-150**.

---

## 2. The census, as the ledgers stand

41 MEASURED figures, matching the table in the brief. Full key/value/source
listing was generated from `Ledger.figures()`; DC-EN numbers are
`DC_ENDNOTE_KEYS.txt` line positions.

| panel | figures | measured | derived | modelled | absent | signed |
|---|---|---|---|---|---|---|
| DC FY2024 | 55 | 26 | 11 | 6 | 12 | 0 |
| DC FY2030 | 96 | 15 | 23 | 40 | 18 | 0 |

---

## 3. What reconciles exactly, and is signable once §1 is done

The District panel's spine closes to the dollar against Exhibit 16. Every
figure below was checked by multiplying the per-$100 value on the plate by
`SCALE` and comparing against the published dollars:

    claims.cell.ffs.Long-term care        1,236.0000  $M
    claims.cell.ffs.Physicians & clinics    406.0000  $M
    claims.cell.ffs.Hospitals               297.0000  $M
    claims.cell.ffs.Wrap around services    222.0000  $M
    claims.cell.ffs.Rx drugs                 89.0000  $M
                                          ----------
    five-node sum                         2,250.0000
    payer.ffs.capitation                  2,250.0000  (agrees)
    payer.mco.capitation + payer.dual.capitation
                                          1,802.0000  (Exhibit 17 managed care)
    peel.medicare                            86.0000
    peel.admin                              234.0000
                                          ----------
    total                                 4,372.0000  = Exhibit 16 total

Thirteen candidates, grouped as they should be signed:

- **Group A — the hundred (Tier 1.1).** `DC24:anchor.ex16.total` 4372.0 ·
  `DC24:anchor.ex16.federal` 3199.0 · `DC24:anchor.ex16.state` 1173.0 ·
  `DC24:scale` 43.72. One source, one reading, four numbers.
- **Group B — the two peels.** `DC24:peel.admin` ($234M, Exhibit 16) ·
  `DC24:peel.medicare` ($86M, Exhibit 17).
- **Group C — the FFS service split (Tier 1.3).** The five `claims.cell.ffs.*`
  cells, plus `payer.ffs.capitation` and `payer.ffs.care`, which are the same
  $2,250M read twice.
- **Group D — the dedicated-tax base (Tier 1.4).** `DC24:anchor.budget.dedtax`
  114.647, DHCF (HT0) FY2024 actual.

**But Group C carries an undeclared convention.** Exhibit 17 prints
fee-for-service at **$2,260M** and collections at **−$10M** (the comment block
in `ledger_dc_2024.py` lines 60-66 says so). The ledger uses $2,250M. The whole
collections line has therefore been netted into fee-for-service, and nothing in
the repo says so: there is no DC analogue of **D-83**, which governs the same
question nationally by folding collections pro rata across the capitated and
fee-for-service lanes by each lane's share of gross.

So the District silently uses a *different* collections convention from the
national panel. Signing Group C means agreeing to that convention, and it is
not written down anywhere to agree to. **This needs a decision before the
signature, not after.** Either adopt D-83's pro-rata key for DC too, or declare
the all-to-FFS fold deliberately and say why.

Eleven of the thirteen above also carry the wrong source string. They are built
by `_s()`, which stamps `SPINE = "CMS-64 / MACStats FY2024 DC"` and appends
*"Vintage inherited from build_sankey_dc.py and not re-acquired. Must be
re-checked before DC ships."* That source line names no exhibit, no table and
no publication date — nothing a signer can open. The arithmetic above shows
they are in fact Exhibit 17 readings. The module already has `_x17()` for
exactly this ("A figure re-acquired from Exhibit 17. Carries no STALE note").
**Re-source them through `_x17` before signing**; it is a label fix, not a
value change, and it removes a STALE note that would otherwise sit on a signed
figure.

---

## 4. What is not signable as it stands

### 4.1 Four figures are marked MEASURED and are not measurements

`mco_cap` is built at `ledger_dc_2024.py:121-125`:

    mc_total = 1802 / SCALE      # Exhibit 17, measured
    pace     =   15 / SCALE      # MODELLED, its own note says "Order of magnitude"
    dsnp     =   25 / SCALE      # MODELLED, "Medicaid wrap around a Medicare Advantage D-SNP"
    mco_cap  = mc_total - pace - dsnp

and then:

| key | value | built from |
|---|---|---|
| `DC24:payer.mco.capitation` | $1,762M | 1802 − 15 − 25 |
| `DC24:payer.dual.capitation` | $40M | 15 + 25 |
| `DC24:payer.dual.care` | $40M | same |

Each is stamped MEASURED by `_s()`. No source prints $1,762M and no source
prints $40M. **Exhibit 17 prints $1,802M**; the split into PACE and the D-SNP
wrap is two typed constants that the ledger itself marks MODELLED when it draws
them as their own lanes at lines 484-500.

This is a status error, not a magnitude error. Signing one would assert that
someone opened a document reporting a figure that is a subtraction of two
estimates. The correct treatment is DERIVED with `parents` naming the Exhibit
17 line and the two modelled constants, so they inherit their standing through
`coverage.verification()` the way the rest of the derived figures do — which
also means they stop being eligible for a signature and start being honest
about why.

### 4.2 Nine plan figures are rescaled and are +9.16% against the filings

Every per-plan figure is multiplied by `_TO_LANE` (`ledger_dc_2024.py:228`):

    _TO_LANE = (mco_cap * SCALE * 1e6) / sum(_PREM.values())
             = 1,762,000,000 / 1,614,177,271
             = 1.091578

| plan | Title XIX premium as filed | on the plate |
|---|---|---|
| AmeriHealth | $747.776M | $816.256M |
| Wellpoint | $307.345M | $335.491M |
| MedStar | $375.056M | $409.403M |
| HSCSN (CY2023 stand-in) | $184.000M | $200.850M |

The reason is good and the note on each figure discloses it in full: a plan's
statement and the CMS-64 do not agree and never will, so the plans are scaled
to the lane and keep their shares. But the *status* is MEASURED, and a
signature on a MEASURED figure asserts someone opened a source and agreed with
**that number**. No statement contains $816.256M.

Three further consequences:

- The scaling factor has `mco_cap` in its numerator, so the PACE "order of
  magnitude" $15M propagates into all nine plan figures. The sensitivity is
  small — PACE at $5M or $30M moves AmeriHealth by +0.57% / −0.85% — so this is
  a provenance problem, not an accuracy one. Worth saying out loud because the
  reverse would be worse.
- `DC_SIGNOFF_LIST` 1.5 asks for a signature on the filed figures
  ($747.776M etc.). Those are right (see §5) and they are **not what is drawn**.
  Tier 1.5 should be split into two signatures: the readings, and the scaling
  convention.
- The same treatment as §4.1 applies: DERIVED with the filed figure and
  `_TO_LANE`'s inputs as parents.

### 4.3 The `UNSIGNED` analogue

Nationally, `payer.dual.margin` and `payer.mco.margin` are deliberately unsigned
because EN-43 states the $0.76 has no primary source. **The District has no
exact analogue** — no measured DC figure's endnote says its source does not
exist. The nearest cases are the four in §4.1, and the right answer there is
reclassification, not `UNSIGNED`. Do not create a DC `UNSIGNED` set for them:
`UNSIGNED` means "a person deliberately declined to sign this", and these have
not reached the point where anyone could.

`DC24:payer.hscsn.*` is a different matter again — it is already MODELLED (a
CY2023 figure standing in for CY2024), which is Tier 1.6's question, and
`DC_SIGNOFF_LIST` 2.1 offers the CY2024 replacement.

---

## 5. One source opened: AmeriHealth Caritas DC, CY2024

The NAIC annual statement is in the project files
(`AmeriHealthCaritasDC_CY2024.pdf`). Every figure `ledger_dc_2024._PREM`,
`_CARE_D` and `_PLAN_ADMIN` take from it was checked against the filing:

| ledger constant | value | where it is in the statement | agrees |
|---|---|---|---|
| `_PREM["amerihealth"]` | 747,775,854 | Analysis of Operations by Lines of Business, line 1, Title XIX column; also U&I Exhibit Part 1 line 8, and Schedule T DC row | yes |
| `_CARE_D["amerihealth"]` | 649,036,647 | same schedule, line 17 "Total hospital and medical"; also Part 2 line 12.4 incurred benefits | yes |
| `_PLAN_ADMIN["amerihealth"]` | 27,887,325 + 54,960,568 | same schedule, lines 19 and 20, Title XIX column | yes |

The comment "change in unearned reserves: 0" is also correct (line 2 is zero).

**One defect found.** The ledger computes plan margin as a residual,
`capitation − care − admin`. On AmeriHealth's filed dollars that is

    747,775,854 − 649,036,647 − 27,887,325 − 54,960,568 = 15,891,314

but the statement's own Title XIX **net underwriting gain is $10,887,464**
(line 24). The difference is exactly **$5,003,850**, which is line 21,
*Increase in reserves for accident and health contracts* — and the statement's
Part 2D says the whole of it is a **premium deficiency reserve**, booked
entirely to Title XIX.

The residual omits a Title XIX underwriting deduction the plan actually
recorded. On the plate, `DC24:payer.amerihealth.margin` is drawn at **$17.347M**
against a filed-and-rescaled **$11.886M** — the margin is overstated by about
**46%**.

It is currently DERIVED, so it is not itself a signature candidate, but it
inherits from three figures that are, and it is drawn. Two possible
resolutions, and this is JW's call:

1. **Take the published number.** Use line 24 where a plan publishes it, and
   let margin stop being a residual for the plans that do.
2. **Keep the residual, add the deduction.** Subtract line 21 as a fourth
   term, which keeps one construction across all four plans whether or not
   each publishes a Title XIX underwriting gain.

Either way the figure on the plate moves, which is a decision before any
AmeriHealth signature, and the other three plans need the same check — Wellpoint
and MedStar both carry apportioned expense lines, so the residual may miss
different things there.

---

## 6. The order of work this implies

1. **D-150: namespace the signature register** and lift `_sign` out of
   `ledger_national_2024`. Prove byte-identical on the national panels.
2. **Decide the District collections convention** (§3) — D-83's pro rata, or
   a declared all-to-FFS fold.
3. **Re-source the eleven `_s()` figures through `_x17()`** (§3).
4. **Reclassify the four status errors** (§4.1) and the nine rescaled plan
   figures (§4.2) as DERIVED with parents.
5. **Settle the plan-margin construction** (§5) and re-check Wellpoint,
   MedStar and HSCSN the same way.
6. **Then** render the S-093 stacked before-and-after and sign Groups A-D.

Steps 2 through 5 all move figures on the plate. Doing them after a signature
would cost the signature; `_sign` would report LAPSED and the build would fail,
which is the apparatus working, but it is a wasted sitting of JW's time.

Items 6 and 3 of the brief's own dangling list — the `$2.90` typing and the
`ENDNOTES.md` sweep — remain worth doing before step 6 for the same reason.

## 7. What was not done

- No external source was fetched. §5 used a filing already in the project.
  Wellpoint, MedStar, the MACStats exhibits, the DHCF budget tables and every
  DC FY2030 anchor are still unopened by a person or by Claude.
- No S-093 render was produced. `render_v8_0.py` and `anchorproof.py` need a
  Playwright browser the Cowork Linux VM cannot download (D-142), and the
  District FY2030 panel has not been rendered since the five new lanes landed.
  Treat it as unrendered.
- No register lines were written to `signatures.py`. There is nowhere to put
  them until step 1.

---

## 8. Gate state at the end of this session

`python3 gates.py` (full, not `--quick`) on the Cowork VM. **No ledger figure
moved this session** — nothing in this document edits a ledger. The gates were
run to establish the baseline the signing work starts from.

Three pip packages were missing on the VM and were installed
(`resvg-py`, `pymupdf`, `playwright`). That alone took the failure count from
**11 to 7**: `build.py`, `build.py sensitivity`, `deckalts.py` and
`build_explorer.py` were failing on `ModuleNotFoundError`, not on anything
about the model. Worth knowing before the next session spends time on them.

Still passing: `crossings.py`, `renderproof.py`, `prove.py`, `coverage.py`
national **and dc**, `explorerchrome.py`, `exportproof.py`.

Still failing, all for known reasons:

| gate | why |
|---|---|
| `make_figs.py`, `render_v8_0.py`, `engine_texts.py`, `anchorproof.py`, `explorerproof.py`, `publish.py` | need a Playwright browser. D-142 confirmed again this session: `python3 -m playwright install chromium` fails at download on the VM. |
| `teachingproof.py` | deliberate. D-138; `EXPECT` was not re-pinned. 283 unaccounted strings is register debt. |

So **`anchorproof.py` has still not run since the five District lanes landed**,
and the District FY2030 panel is still unrendered. That is unchanged from the
brief and is still the first blocking item.
