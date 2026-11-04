# The District, brought up to the national standard — research, 3 November 2026

Worked by Claude against `NEXT_SESSION_PROMPT_12.md`, without JW present. The
brief said: for each absence, do not stop at naming who holds the number —
hunt for analogues, older vintages, federal collections and other
jurisdictions, and build a defensible band with named ends that can become a
slider. That is what this is.

**Nothing here is signed.** `signatures.py` still carries no District entry.
Every figure below names a source and a vintage, and not one of them has been
opened and agreed by a person. `DC_SIGNOFF_LIST.md` is the list of what needs
JW's signature; `DC_QUESTIONS_FOR_JW.md` is the question queue, in order.

Source numbers in brackets key to the register at the end.

---

## 0. One constraint found the hard way

Both shells available to an agent in this project — the cloud container and
the Linux VM on the laptop — refuse outbound HTTPS to anything outside an
allowlist. `rand.org` and `cbo.gov` both answered `connect_rejected`. So no
document can be downloaded and parsed with `pdftotext` or `pandas`.

What does work: open the document in the in-app browser and drive the page's
own `pdfjsLib` to pull text page by page; for a workbook, load JSZip and
SheetJS from a CDN and read the sheets in the page. Every PDF and every XLSX
cited below was read that way, including a 402-page budget volume on Box and a
ZIP annex on rand.org. It is slower than a download and it leaves no local
copy, which is a verification problem rather than a reading problem.

The one thing it could not do is the CBO workbook at [2], because `cbo.gov`
also refuses the browser's fetch from a different origin and WebFetch will not
convert an `.xlsx`. That is the single most important document still unopened.

---

## 1. The three named District provisions are now sized

`DC_ENGINE_TODO.md` item 1 — "**Worst one. Fix first.**" — is the leftovers
lane carrying a national residual's rate under a District label. The brief
named closing it as the single highest-value item: *if CBO scored any of the
three nationally, the work-reporting construction applies directly.*

**CBO scored all three.**

| § | provision | CBO ten-year |
|---|---|---|
| 71108 | home equity cap at $1,000,000 for LTSS eligibility | **$195M** |
| 71109 | alien / qualified-immigrant eligibility | **$6.2B** |
| 71112 | retroactive coverage cut to one month (expansion) / two (other) | **$4.2B** |

Two independent secondary sources agree on all three [3][4]. The primary is
CBO, *Estimated Budgetary Effects of P.L. 119-21 … Relative to CBO's January
2025 Baseline*, 21 July 2025, publication 61570 [2], which CRS names as the
source of its own budget figures [5]. **It has not been opened** — see §0.

Paragon [3] is on the same vintage as this repo for the six lanes CBO's 28
October supplemental does publish: 317.0 / 58.0 / 182.7 / 149.4 / 53.6 / 66.0,
matching `tobe2030.TEN_YR` to the tenth. KFF [4] is NOT — it carries 326 / 63
/ 191 / 149 / 56 / 66, a pre-enactment vintage. **Do not mix the two.**

### The derivation, in the shape the work-reporting lever already uses

National score read as a RATE over a national denominator this repo already
carries, applied to the District's own denominator. Nothing allocated by share
of anything else.

| provision | national denominator | District denominator | DC / national |
|---|---|---|---|
| 71108 | `basis_national.LTC_FFS_M` = $194,580M (institutional LTSS + HCBS, fee-for-service, Exhibit 17) | $1,236M (`ledger_dc_2024._ffs_n["Long-term care"]`) | 0.63521% |
| 71109 | `basis_national.HUNDRED_M` = $950,164M | `basis_dc.DC_TOTAL_M` = $4,372M | 0.46013% |
| 71112 | `basis_national.HUNDRED_M` | `basis_dc.DC_TOTAL_M` | 0.46013% |

| provision | District, ten years | District, FY2030 | per $100 of the FY2030 hundred |
|---|---|---|---|
| 71108 home equity | $1.239M | $0.177M | **0.0030** |
| 71109 immigrant eligibility | $28.528M | $3.170M | **0.0533** |
| 71112 retroactive | $19.326M | $2.416M | **0.0406** |
| **together** | | | **0.097** |

(FY2030 figures spread the ten-year total over the years each provision is in
force — seven for 71108 from 1 January 2028, nine for 71109 from 1 October
2026, eight for 71112 from 1 January 2027. That spreading is a modelled step
and is the one place this derivation adds an assumption; Q3 asks about it.)

### What the lane carries today, and why this is not simply "eleven times too big"

The lane is drawn at the national `Everything else` rate, **1.0587 per $100**
rebased. The three named provisions come to **0.097**. But the national lane
is a residual covering a dozen other sections too — 71103, 71106, 71110,
71111, 71114, 71117, 71118, 71120, 71121 — while the District lane carries
three named provisions and nothing else. They are not the same quantity, which
is exactly what `DC_ENGINE_TODO` item 1 says. The placeholder is not eleven
times too large as a measure of the same thing; it is a measure of a different
thing. Replacing it does two jobs at once: it shrinks the lane to about a
tenth, and it makes the lane mean what its label says.

### An independent check that lands within ten per cent

RAND's state-level allocation [6] gives the District's immigrant-eligibility
impact as **−$11.5M cumulative through 2030**. This derivation gives $28.528M
over ten years, which over FY2027–FY2030 is about **$12.7M**. Two different
methods, two different denominators, one answer within a tenth. That is the
strongest corroboration anywhere in the District work.

### A band for 71108, because the District is not the nation on home values

$195M nationally is a small number, and the District's share of it on an LTSS
denominator is $1.24M over ten years. But a $1,000,000 home equity cap does
not bite equally everywhere. ACS 2024 one-year, table B25075 [16]:

| owner-occupied units valued at $1,000,000 or more | share |
|---|---|
| District of Columbia | 40,303 of 134,836 = **29.89%** |
| United States | 6,937,364 of 86,635,504 = **8.01%** |
| ratio | **3.73×** |

So the band runs **$1.24M (national rate) to $4.62M (national rate × the
District's home-value ratio)** over ten years, i.e. 0.0030 to 0.0111 per $100.
**Declared, not like-for-like**, in the same way `RATE_BASIS_DIFFERS` is
declared for work reporting: home VALUE is not home EQUITY, and Medicaid LTSS
applicants are poorer, older and far more often renters than the owner
population the ACS table describes. The ends are named observations; the
non-comparability is stated; nothing is a point estimate with no provenance.

At either end the lane is between a third of a cent and a cent per $100. **The
finding may be that this provision is immaterial at District scale**, and
saying so with a band is better than drawing it.

---

## 2. A published District band for the two enrolment levers

The best single find of the session. Urban Institute's HIPSM run [7] carries a
District of Columbia row and separates the two levers.

**Table 3 — both levers, average monthly expansion enrolment, 2028**

| scenario | DC | % |
|---|---|---|
| high mitigation | −27,000 | −25% |
| medium mitigation | −46,000 | −41% |
| low mitigation | −60,000 | −55% |

**Appendix Table A.2 — separated**

| | high | medium | low |
|---|---|---|---|
| six-month redeterminations only | −8k (−7%) | −14k (−13%) | −14k (−13%) |
| work requirements, incremental after redeterminations | −19k (−17%) | −32k (−29%) | −46k (−42%) |

Against what the repo has today:

| | rate | basis |
|---|---|---|
| `RATE_DEFAULT` (work + renewals) | **21.42%** | share of expansion-group SPENDING, CBO-implied |
| Urban, high mitigation | 24% | share of expansion ENROLMENT |
| Arkansas 2018 | 25% | coverage loss among those SUBJECT |
| New Hampshire 2019 | 40% | coverage loss among those SUBJECT |
| Urban, medium mitigation | 41% (42% as the two components sum) | share of expansion enrolment |
| Urban, low mitigation | 55% | share of expansion enrolment |

The repo's declared default sits just under Urban's high-mitigation scenario,
and `RATE_BAND`'s upper end (New Hampshire, 40%) sits just under Urban's
medium. (Urban's combined medium reads 41% in Table 3 and 42% as the sum of
its two components in Table A.2; the difference is rounding in their own
tables, not a disagreement.) The band already drawn is, without anyone having known it, roughly
Urban's high-to-medium range. **Arkansas and New Hampshire stop being the band
and become corroboration of it**, which is a better place for them: they are
two observations from two other jurisdictions, and this is a District row from
a named model.

**The denominators still differ and the plate has to say so.** Urban's implied
District expansion base is about **109,000** (27/0.25, 46/0.41 and 60/0.55 all
land there). `tobe2030_dc.EXPANSION_AT_RISK` is **78,322** — childless adults
0–133% FPL, January 2026, after the District's own cut. Urban's base looks
pre-cut and probably includes expansion parents. Until that is reconciled the
percentages cannot be multiplied against 78,322. Q2 asks about it.

Urban also report that 60–70% of the combined decline is the work-requirements
provision, which the District rows bear out (29 of 42 at medium).

RAND [6] is a third voice and the most extreme: work requirements alone take
**−45,800** District enrollees by 2034, which against 78,322 is 58%.

### The exempt share: bounded, not found

`EXEMPT_SHARE` is still `None`. What was found bounds it.

DHCF's own performance oversight testimony, 29 January 2026, p.17 [9]:
approximately 271,000 in DC Medicaid as of November 2025, "including **78,000
childless adults with income from 0-138 percent of FPL who will be subject to
work requirements**. We anticipate that of this group, **28 percent could
potentially meet the requirement based on their income** – which is at least
44 percent of FPL. The remaining **56,000 beneficiaries may require other
community engagement activities or an exemption**."

78,000 corroborates `EXPANSION_AT_RISK = 78,322` to the rounding. The 28% is
income-based auto-satisfaction, not exemption — so it bounds the exempt share
from above at **56,000 / 78,000 = 71.8%**, and no further. DHCF lists the
exemption categories and publishes no count in any of them.

Urban's national components, for the interior [7]: medically frail
automatically identifiable at about **21%** under a broad definition and about
**8%** under a conservative one; 34% or more would meet a "serious or complex"
standard. Not a District figure, and only one of several exemption categories.

**And the definition moved five days ago.** On 29 October 2026 Judge Richard
Stearns, D. Mass., vacated CMS's definition of "medically frail" in the
interim final rule and said he would issue the permanent injunction the states
requested; 25 states and the District of Columbia were plaintiffs; the court
gave states a six-month stay on enforcing medical-frailty determinations
[17]. Whether the relief is nationwide is not stated in the reporting. **Any
exempt-share band drawn this week is drawn on a definition that is in motion**,
and the panel has to say so.

---

## 3. The paperwork lane gets a District rate — and it runs the same way the seniors lane does

`DC_ENGINE_TODO` item 2 says the §71102 lane carries the national rate because
"there is no District figure and none is derivable from published sources".
There is one, and it is published monthly.

CMS, *Medicaid and CHIP Eligibility Operations and Enrollment Snapshot*,
"Coverage Retention and Disenrollment Rates by State" [13]:

| month | DC due for renewal | DC renewed | DC **ex parte** | DC procedural | national ex parte | national procedural |
|---|---|---|---|---|---|---|
| Oct 2024 | 34,577 | 91% | **85%** | 5% | — | — |
| Aug 2025 | 20,662 | 78% | **71%** | 13% | 50% | 12% |
| Sep 2025 | 18,749 | 89% | **85%** | 7% | 50% | 14% |
| Oct 2025 | 32,663 | 92% | **89%** | 5% | 49% | 13% |
| Nov 2025 | 24,480 | 88% | **84%** | 8% | 51% | 13% |
| Dec 2025 | 33,408 | 89% | **86%** | 7% | 48% | 15% |
| Jan 2026 | 18,735 | 86% | **84%** | 10% | 47% | 15% |
| Feb 2026 | 18,682 | 87% | **84%** | 8% | 47% | 15% |
| Mar 2026 | 18,078 | 73% | **67%** | 16% | 48% | 15% |
| Apr 2026 | 16,604 | 78% | **72%** | 13% | 47% | 15% |
| May 2026 | 13,652 | 81% | **77%** | 11% | 48% | 15% |
| Jun 2026 | 16,766 | 75% | **70%** | 15% | 47% | 15% |

**The District renews ex parte at about 1.6 times the national rate.** Section
71102 blocks a rule whose substance is ex parte renewal, renewal alignment,
the reconsideration period and ABD interviews. A jurisdiction already doing
most of that voluntarily has less to lose from the block.

**This is structurally the same argument as the seniors lane.** There, the
District already enrols QMB to 300% FPL against a federal floor of 100%, so
its exposure to a blocked streamlining rule is below its share of enrolment,
and `MSP_EXPOSURE_BAND` runs from the drawn figure down to zero. Here, the
District already renews automatically at well above the national rate, for the
same kind of reason. Two lanes, one finding: **the District has already done
by its own choice much of what the blocked federal rules would have
required.** That is a paper passage, not a patch.

So the paperwork lane can stop carrying a bare national rate and carry a band
of the `MSP_EXPOSURE_BAND` shape: national rate at the top (the District
behaves like the average), zero at the bottom (the District has already
captured everything the rule would have delivered), with the ex parte ratio as
the stated reason the default sits below the middle. Q4 asks where the default
goes.

**The trend is not noise and should not be averaged away.** The ex parte rate
falls from 89% in October 2025 to 67% in March 2026 and sits at 70% in June.
March 2026 is the month DHCF's new MMIS went live — Gainwell go-live 1 March,
first payments 13 March, and DHCF's own warning that "DHCF reporting and data
availability may be delayed as the MMIS transition will impact the Medicaid
data warehouse" [9, p.16]. It is also the first full year of the District's
own eligibility cut. A band struck on FY2025 months is a different band from
one struck on FY2026 months.

DC MAGI application processing, October 2024 [13]: 25% within 24 hours, 21% in
1–7 days, 32% in 8–30, 8% in 31–45, **14% over 45 days**.

---

## 4. HSCSN's administration and margin — DC_ENGINE_TODO item 8 is closed

Not through NAIC. DHCF publishes it. *District of Columbia CY2024 Medicaid
Managed Care Performance Report*, June 2026, p.9 [11], sourced to "MCP Annual
Statement as of December 31, 2024, filed by the MCPs with the DISB":

| MCP | revenue | claims | administrative | operating margin |
|---|---|---|---|---|
| Amerigroup | $385.8M | $303.9M | $22.2M | $59.6M |
| AmeriHealth | $786.2M | $720.9M | $44.2M | $21.1M |
| **HSCSN** | **$180.4M** | **$180.4M** | **$20.7M** | **$(20.6)M** |
| MedStar | $403.7M | $374.4M | $24.6M | $4.6M |
| total | $1,756.1M | $1,579.6M | $111.7M | $64.7M |

So `payer.mco.admin` and `payer.mco.margin` need no longer be ABSENT on the
grounds that three plans of four publish and one does not. Four things travel
with the figures:

1. **Basis.** Statutory annual statement, CALENDAR year, incurred. The spine
   is CMS-64, federal fiscal year, total computable. `NAIC_ROUTE.md` §6's
   bridge rule applies to these exactly as it would to a Page 7 pull.
2. **MedStar's row is its District line of business only**, and its
   administration is shared with Maryland and allocated.
3. **CY2024 is an outlier year for HSCSN**: MLR 100%, operating loss $20.6M,
   attributed to "a few high-cost gene therapy and hemophilia cases". CY2023
   was MLR 84% with administration at 16%. A split struck on CY2024 alone
   draws a loss year as if it were the shape of the lane.
4. **The report contradicts itself.** Its CASSIP chart shows administration
   and operating margin together at 0% for CY2024 because the chart forces MLR
   plus the rest to 100%. The table shows $20.7M on $180.4M, which is 11.5%.
   Use the table.

Also from the same report: in CY2024 the District spent about **$1.8 billion**
on services administered by the MCPs, about 90% ($1.6bn) on the three
comprehensive plans and about 10% ($180M) on the HSCSN risk-sharing contract
(p.4); Mercer's operating-margin benchmark for the District is **about 2
percent** (p.8); FFY2024 target MLR is about **93%** for DCHFP and
Non-Medicaid and about **90%** for CASSIP, with risk corridors outside ±2%
(p.11).

**Item 4, the managed-care service split, is still open.** The CY2024 report
publishes PMPM LEVELS by population (TANF adult $509.53, children $259.19, SSI
adult $1,786.70, Alliance $398.57, ICP $246.47) and year-on-year PMPM GROWTH
by service category (inpatient, outpatient, emergency, behavioural health,
pharmacy) — but not category levels. Next targets named: the Mercer rate
certification, and the EQRO Annual Technical Reports for 2022 to 2025, all
four of which are posted [20].

---

## 5. The seniors lane: a band for QMB-only above 100% FPL

`DC_ENGINE_TODO` item 3 says this turns the lane from an upper bound into a
figure, and that DHCF holds it. DHCF probably does. In the meantime the band
has two named ends.

**The lower end, 19%.** KFF's state table on MSP enrolment by type of
assistance, CCW 20% sample, 2021 [14], confirms the District's structure from
the outside: DC is **100%** in the Part A and B premium-and-cost-sharing
column, with 70 people in the Part B-only column; "QMB is the sole program in
DC, with expanded eligibility". Nationally the two above-100%-FPL tiers —
SLMB-Plus at 4% and SLMB-Only/QI at 15% — are **19%** of MSP enrolment. That
is what the District would look like above the federal floor if it enrolled
there only to the extent other states do through SLMB and QI.

**The upper end, about 50%.** KFF's distribution of people with Medicare by
FPL, 2024 [15], District row: under 100% 20,000; 100–199% 12,200; 200–399%
15,100; 400%+ 39,400; total 86,700. Splitting the 200–399% band evenly to
approximate a 300% ceiling gives about 39,750 District Medicare beneficiaries
at or below 300% FPL, of whom about **19,750, or 49.7%, are above 100%**. That
is the share if participation were flat across the income range it is not;
take-up falls as income rises, so this is an upper end by construction.

`MSP_DENOMINATOR` is 12,880 QMB-only, January 2026, against about 39,750
Medicare beneficiaries under 300% FPL — a participation rate near a third,
which is itself worth a sentence in the paper.

Q5 asks where the default goes inside 19%–50%.

---

## 6. ACR_TO_MEDICARE_RATIO — the acquisition `tobe2030_dc.py` names is closed

The file says: "ACQUISITION: open the annex and read the DC row, or establish
that there is not one." There is one. RAND, *Prices Paid to Hospitals by
Private Health Plans*, Round 5.1, supplemental annex [8], sheet "Table 2.
States", 2022 data:

| District of Columbia, private allowed / simulated Medicare allowed | |
|---|---|
| overall | **241.20%** |
| inpatient | 235.66% |
| outpatient | 249.13% |
| **inpatient facility** | **246.48%** |
| **outpatient facility** | **263.39%** |
| professional | 177.11% |

**Declare the sample.** The District's row rests on $6.36M of total private
allowed amount, **91 inpatient stays** and **918 outpatient services**. The
ratio is good to no better than that.

Applied to `SDP_PCT_OF_ACR`, already in the repo from the approved preprint:

| programme | % of ACR | × DC ACR/Medicare | = % of Medicare |
|---|---|---|---|
| DC Healthy Families inpatient | 97.0% | 246.48% | **239.1%** |
| DC Healthy Families outpatient | 65.8% | 263.39% | **173.3%** |
| CASSIP inpatient | 95.1% | 246.48% | **234.4%** |
| CASSIP outpatient | 79.0% | 263.39% | **208.1%** |

All four clear the 100%-of-Medicare expansion-state ceiling by a wide margin.
This **confirms KFF's "100 percent of DC's hospital SDP spending is above the
new limit" on District evidence** rather than on KFF's conversion, and it
confirms `DIRECTED_REACHES_LIMIT_BY_FY30 = False`: on the repo's reading of the
step — ten points of the ORIGINAL dollar amount a year, CMS's own worked
example — the programme runs ten steps to zero and never meets the ceiling on
the way down, because the base rate alone already clears it.

---

## 7. The District's own four-year plan: checked, and it is not there

`DC_ENGINE_TODO` item 6 records the FY2026 PROPOSED budget Executive Summary
as the one place a District four-year Medicaid trajectory might be, and as
UNCHECKED. It is now checked, in both the FY2026 and the FY2027 volumes [12].

**It is not there, and it is not there by design.** The District's financial
plan projects by APPROPRIATION TITLE, not by programme. There is no Medicaid
line and no agency line at four years, in either volume. Federal Medicaid
Payments is named as a component of the Federal and Private Resources Fund and
then folded into Federal Grants in Table 2-5. The agency chapters (HT0) stop
at the budget year, as already established.

What the FY2027 Approved volume does carry, FY2027 to FY2030 ($000s):

| | FY2027 approved | FY2028 | FY2029 | FY2030 |
|---|---|---|---|---|
| Human Support Services, federal and private (Table 2-5) | 4,687,533 | 4,780,760 | 4,876,019 | 4,973,179 |
| Human Support Services, local funds (Table 2-2) | 2,568,417 | 2,407,673 | 2,471,373 | 2,497,816 |

DHCF's own FY2027 Federal Medicaid Payments are $3,966.246M, about 85% of that
federal HSS line. So the federal HSS trajectory is a **District-sourced growth
rate of about 2.0% a year to FY2030** — against `PRIOR_LAW_CAGR` of **5.27%**.
That gap is mostly the law: the FY2027 Approved plan is post-enactment and
already carries the District's own eligibility cut and the ACR limitation, so
it is a TO-BE trajectory, not the prior-law counterfactual the hundred needs.
It belongs as a cross-check on the FY2030 to-be, not as a replacement for
`PRIOR_LAW_CAGR`. Q6 asks what to do with it.

Two further things from the same volume, both District-sourced and both on
lanes the national model handles with CBO ramps. Table 2-3, dedicated taxes
($000s):

| dedicated tax | FY2027 | FY2028 | FY2029 | FY2030 |
|---|---|---|---|---|
| Inpatient Hospital **Directed Payment** Provider Fee Fund | 86,985 | 86,985 | 78,286 | **0** |
| Outpatient Hospital **Directed Payment** Provider Fee Fund | 35,280 | 35,185 | 29,540 | **0** |
| Inpatient Hospital Bed Tax & Provider Fee → Hospital Fund | 14,900 | 14,900 | 14,900 | **0** |
| Healthcare Provider Tax → Nursing Facility Quality of Care | 22,001 | 22,441 | 22,890 | 23,347 |
| ICF-IDD Assessment → Stevie Sellows | 5,388 | 5,388 | 5,388 | 5,388 |
| sales and insurance premium → Healthy DC Fund | 96,165 | 98,089 | 75,470 | 67,247 |

**Do not take the FY2030 zeros at face value.** The Revenue chapter of the same
volume says the inpatient fee "is forecasted to remain flat at $87.0 million
level from FY 2026 through FY 2030" while Table 2-3 shows zero in FY2030 — the
District's own document contradicts itself in two chapters. Table 3-16 labels
the column "FY 2030 Certified Revenues", so the zeros most likely mean *not
certified beyond statutory authority*, not *forecast to stop*. The FY2029
step-downs — 78,286 and 29,540 — are a different matter and may well be the
ACR limitation arriving. Q7 asks about it.

And DHCF's own four-year statement, in words, from the performance oversight
testimony [9, p.3]: "our Medicaid budget continues to grow at an annual rate
that is over five times the amount of revenue growth for the city … when you
compare DHCF's approved budgets to the next year's projected growth, the gap
averages more than $141 million in local funds. Funding that gap over the
four-year financial plan would require an allocation of $566 million."

---

## 8. RAND's state allocation gets the District wrong on two lanes, and we can say why

RAND [6] is the only published state-by-state allocation of the law. Its
Table 2.1 codes the District as **"Use of SDPs: No"** and **"Use of Provider
Taxes: No"**, so its Tables B.4 and B.5 give the District exactly zero on
both. The same report, at p.49, says 45 states *and the District of Columbia*
had active provider taxes.

The reason the provider-tax zero is defensible on RAND's own terms and still
wrong for this model: **RAND models provider taxes only through the
hold-harmless taper**, 6% down to 3.5%, and exempts nursing-facility and ICF
taxes. The District's hospital tax is 3% of net patient revenue, below every
step — which is exactly the finding already written into `tobe2030_dc.py`
(`TAPER_BINDS_DC`). RAND did not model the FREEZE, and the freeze is where the
District's entire §71115 exposure sits.

On state directed payments RAND is simply wrong. The District has CMS-approved
inpatient and outpatient directed-payment preprints and two dedicated funds
named after them, visible in its own budget at §7 above, and DHCF attributes a
$169M fall in its FY2027 budget to "projected lower spending for the Average
Commercial Rate (ACR) funding mechanism for hospitals due to limitations in
recently passed federal legislation effective October 1, 2026" [10, p.6].

**This belongs in the paper.** The only published state-level allocation of
P.L. 119-21 misses the District's two financing lanes, and the reason is that
it models the rate instruments and not the freeze. That is a general point
about allocating a national score to a state, which is the thesis the District
panel exists to carry.

### RAND's District rows, for the record

Cumulative $M, state Medicaid fund / state general fund:

| table | provision | 2028 | 2030 | 2034 |
|---|---|---|---|---|
| B.1 | all studied | −498.3 / +50.3 | **−1,706.1 / +172.3** | −4,774.3 / +463.2 |
| B.3 | work requirements | −385.7 / +38.6 | −1,456.8 / +145.7 | −4,163.6 / +416.4 |
| B.4 | provider taxes | 0 | 0 | 0 |
| B.5 | state directed payments | 0 | 0 | 0 |
| B.6 | more-frequent redeterminations | −108.8 / +10.9 | −233.5 / +23.4 | −540.7 / +54.1 |
| B.7 | emergency FMAP | 0 | 0 | 0 |
| B.8 | address verification | 0 | −23.5 / +6.2 | −132.9 / +35.3 |
| B.9 | good-faith waiver | 0 | −0.3 / −0.3 | −19.3 / −19.3 |
| B.10 | immigrant eligibility | −5.5 / +1.6 | **−11.5 / +3.3** | −26.2 / +7.6 |
| B.11 | cost sharing | −1.3 / +0.1 | −3.8 / +0.4 | −9.0 / +0.9 |
| B.12 | HCBS waivers | +3.4 / −0.9 | +23.8 / −6.3 | +100.0 / −26.6 |
| B.13 | Rural Health Transformation | 0 | 0 | 0 |

B.14, relative importance for the District, 2025–2034: work requirements
**86.63%**, redeterminations **11.25%**, other 2.12%, everything else zero.
B.15, enrolment change by 2034: good-faith waiver −400, redetermination
−5,400, **work requirements −45,800**, qualified immigrants −300, deduplicated
total **−51,300**. RAND puts the District among four jurisdictions losing more
than 20% of Medicaid enrolment.

RAND excluded retroactive coverage because its $4.2B score is below their $5B
threshold, and did not model the eligibility-and-enrolment rule at all. Use
version 2: v1 had a coding error corrected in June 2026.

---

## 9. Two defects found in the repo

**9.1 A comment in `ledger_dc_2024.py` compares two different denominators.**
At the ASSUMED SERVICE MIX block it reads: "DC's own fee-for-service mix is
nothing like the national one — 55 percent of its FFS dollar is long-term care
against about 20 percent nationally." On the repo's own constants the national
FFS long-term-care share is **48.64%** (`LTC_FFS_M` 194,580 over `FFS_TOTAL_M`
400,002), not 20%. The 20% is long-term care as a share of the whole national
hundred (194,580 / 950,164 = 20.48%). The sentence compares a share of
fee-for-service to a share of total spending.

The point survives, in two correct forms: **the District's fee-for-service
dollar is 54.93% long-term care against 48.64% nationally**, and **long-term
care is 28.3% of the District's total Medicaid against 20.5% nationally**. It
is a comment, not a figure, so nothing drawn is wrong — but it is a sentence a
reader could repeat.

**9.2 `DC_NAMED_PROVISIONS` says the immigrant provision is under a
preliminary injunction.** The injunction found is *Neighborhood House and
Mariia Matsai v. HHS*, W.D. Wash., No. C26-3006 TSZ, Judge Zilly, 30 September
2026 [18]. It enjoins HHS from enforcing the 8 April 2026 SHO letter and from
terminating Medicaid funding **for qualified noncitizen SSI recipients in
Washington**. It is statewide in Washington and expressly not nationwide, and
the court declined to go further. On the evidence found, **§71109 is not
enjoined as to the District**. The repo's note may rest on something DHCF said
at its February 2026 advisory session that has since been overtaken, or on a
different case not found here. Either way the status line needs re-checking
before it is drawn. Q8.

---

## 10. What is still absent after all this

- **Dual and PACE retention.** No District figure found. The route remains
  `NAIC_ROUTE.md`: UnitedHealthcare's District Dual Choice wrap sits inside a
  multi-state entity's Title XIX column and has to come out of Schedule T; the
  PACE figure is DHCF's. Neither was reachable from published material.
- **DHCF's managed-care service split.** See §4. The report publishes PMPM
  levels by population and growth by service category, not category levels.
  Unworked targets: the Mercer rate certification, the four EQRO Annual
  Technical Reports [20].
- **The exempt share itself.** Bounded above at 71.8% by DHCF's own 28/56,000
  split, with the medically-frail component in litigation. See §2.
- **CBO publication 61570's workbook [2].** The primary for all three named
  provisions. Blocked by the egress allowlist; JW can open it in one click.
- **The District's own prior-law four-year trajectory.** Checked and not
  published. See §7.

---

## 10b. The brief's leads, worked and reported

`NEXT_SESSION_PROMPT_12.md` named seven leads "as leads, not as known
contents". Each was tried. What they turned out to hold:

| lead | outcome |
|---|---|
| CMS unwinding data, 2023–24 | **Paid off, and better than expected.** Not the unwinding files but the monthly *Eligibility Operations and Enrollment Snapshot*, which runs to June 2026 and carries District renewal volumes, ex parte rates and procedural disenrolment against the national figures in the same document. §3. |
| Actuarial rate certifications | **Not found public.** DHCF's managed care contract is posted in a redacted "PUBLIC" version whose rate exhibits are not in it; there is no rate certification on the agency's site. The Mercer certification remains the right target and has to be asked for. |
| EQRO annual technical reports | **Negative, and the lead can be closed.** The 2025 Annual Technical Report is 145 pages and contains no PMPM, no service-category spending and no rate build-up. The District's EQRO reports are quality and access, not cost. The 2022–2024 reports are the same series. |
| T-MSIS / TAF and DQ Atlas | **Not reachable.** The TAF research identifiable files need a data use agreement; DQ Atlas publishes data-quality assessments rather than the service-category and plan-level spending the lane needs. This is an acquisition with a procurement in front of it, not a search. |
| DC Council Committee on Health oversight responses | **Partly paid off.** DHCF's own oversight testimony [9] is where the 78,000 / 28% / 56,000 work-requirement split and the four-year $141M/$566M gap statement come from. The Committee's pre-hearing question responses themselves were not reached. |
| `NAIC_ROUTE.md`, re-read for the dual and PACE lanes | **Still the only route, and still unexecuted.** Nothing published closes dual or PACE retention for the District. UnitedHealthcare's District Dual Choice Medicaid wrap sits inside a multi-state entity and has to come out of Schedule T; the PACE figure is DHCF's. §10. |
| Other jurisdictions as analogues; older vintages | **Paid off twice.** Urban's three mitigation scenarios replace Arkansas-and-New-Hampshire as the work-reporting band (§2), and KFF's 2021 MSP distribution supplies the lower end of the QMB band (§5). |

And one lead the brief did not name that paid off more than any of them: the
in-app browser as a document reader. Every finding above was read that way.

## Source register

1. CBO, *Supplemental Cost Estimate: Public Law 119-21, Title VII, Subtitle B,
   Chapter 1, Medicaid*, 28 October 2025.
   https://www.cbo.gov/system/files/2025-10/PL-119-21-Medicaid%20_0.pdf
   — the vintage the to-be ledger is struck on. Six named lanes plus "Other"
   at $60.1B. No section detail for 71108, 71109 or 71112.
2. CBO, *Estimated Budgetary Effects of P.L. 119-21 … Relative to CBO's
   January 2025 Baseline*, 21 July 2025, publication 61570.
   https://www.cbo.gov/publication/61570 — workbook
   `https://www.cbo.gov/system/files/2025-07/61570-pl119-21-2025Recon-CLB.xlsx`
   **NOT OPENED.** The primary for §1.
3. Paragon Health Institute, *What Made It Into Law: Health Provisions of the
   One Big Beautiful Bill*, states it uses CBO's 21 July 2025 projections.
   https://paragoninstitute.org/medicaid/what-made-it-into-law-health-provisions-of-the-one-big-beautiful-bill/
4. KFF, *Health Provisions in the 2025 Federal Budget Reconciliation Law*.
   https://www.kff.org/medicaid/health-provisions-in-the-2025-federal-budget-reconciliation-law/
   — **different vintage**; see §1.
5. CRS, *Health Provisions in P.L. 119-21, the FY2025 Reconciliation Law*,
   R48633, 18 August 2025. https://www.congress.gov/crs-product/R48633
6. RAND, *State-Level Impacts of Key Medicaid Provisions in the One Big
   Beautiful Bill Act*, RR-A4098-1-v2 (revised June 2026).
   https://www.rand.org/pubs/research_reports/RRA4098-1-v2.html
7. Urban Institute, *Projected Reductions in Medicaid Expansion Enrollment
   Under OBBBA's Work Requirements and Six-Month Redeterminations*, March 2026.
   https://www.urban.org/research/publication/projected-reductions-medicaid-expansion-enrollment-under-obbbas-work
8. RAND, *Prices Paid to Hospitals by Private Health Plans*, Round 5.1,
   RR-A1144-2-v2, supplemental annex ZIP, sheet "Table 2. States".
   https://www.rand.org/content/dam/rand/pubs/research_reports/RRA1100/RRA1144-2-v2/RAND_RRA1144-3-v2.annex.zip
9. DHCF, *Testimony for Performance Oversight Hearing*, 29 January 2026.
   https://dhcf.dc.gov/sites/default/files/dc/sites/dhcf/release_content/attachments/DHCF%202026%20Performance%20Testimony%201.29.26.pdf
10. DHCF, *Testimony for Committee on Health Budget Hearing*, 29 April 2026.
    https://dhcf.dc.gov/sites/default/files/dc/sites/dhcf/release_content/attachments/DHCF%20FY2027%20Budget%20Testimony%20COH.pdf
11. DHCF, *District of Columbia CY2024 Medicaid Managed Care Performance
    Report*, June 2026.
    https://dhcf.dc.gov/sites/default/files/dc/sites/dhcf/page_content/attachments/FINAL%20CY2024%20MC%20Performance%20Report%20%2806%2008%2026%29.pdf
12. Government of the District of Columbia, *FY 2027 Approved Budget and
    Financial Plan, Volume 1 — Executive Summary*, 21 August 2026, Tables 2-2,
    2-3, 2-5, 3-12, 3-16. https://app.box.com/s/queqbf6mvyvfg4ifye5o5ztq67ops99d
    FY2026 equivalent: https://app.box.com/s/3fwa2n22w8vz006vgsclkpjszxuw07l6
    Agency chapter HT0, FY2027:
    https://cfo.dc.gov/sites/default/files/dc/sites/ocfo/publication/attachments/ht0_dhcf_chapter_2027a.pdf
13. CMS, *Medicaid and CHIP Eligibility Operations and Enrollment Snapshot*,
    monthly. Example:
    https://www.medicaid.gov/resources-for-states/downloads/eligib-oper-and-enrol-snap-jun2026.pdf
    (substitute `oct2024`, `aug2025` … `jun2026` for the other months).
14. KFF, *Distribution of Medicare Beneficiaries Enrolled in the Medicare
    Savings Programs, by Type of Assistance Received*, CCW 20% sample, 2021.
    https://www.kff.org/medicare/state-indicator/distribution-of-medicare-beneficiaries-enrolled-in-the-medicare-savings-programs-by-type-of-assistance-received/
15. KFF, *Distribution of People with Medicare by Federal Poverty Level*,
    2024. https://www.kff.org/medicare/state-indicator/distribution-of-people-with-medicare-by-fpl/
16. U.S. Census Bureau, American Community Survey 2024 one-year estimates,
    table B25075, Value of owner-occupied housing units, via Census Reporter.
    https://api.censusreporter.org/1.0/data/show/latest?table_ids=B25075&geo_ids=04000US11,01000US
17. Healthcare Dive, *Judge strikes down CMS "medical frailty" policy for
    Medicaid work requirements*, 30 October 2026, reporting Judge Richard D.
    Stearns, D. Mass., 29 October 2026.
    https://www.healthcaredive.com/news/judge-strikes-down-cms-medical-frailty-policy-medicaid-work-requirements/873284/
    **Case caption and docket not yet obtained.**
18. *Neighborhood House and Mariia Matsai v. HHS*, W.D. Wash., No. C26-3006
    TSZ, order of 30 September 2026.
    https://nohla.org/wordpress/wp-content/uploads/2026/09/2026-09-30-NeighborhoodHouse-v-HHS-Preliminary-Relief-Order.pdf
19. CMS, State Health Official letter SHO 26-001, *Section 71109:
    Implementation of "Alien Medicaid Eligibility"*, 8 April 2026.
    https://www.medicaid.gov/federal-policy-guidance/downloads/sho26001.pdf
    **NOT YET READ.**
20. DHCF, Medicaid Reports index, carrying the Annual Technical Reports for
    2022 to 2025 and the managed care performance reports.
    https://dhcf.dc.gov/page/medicaid-reports
