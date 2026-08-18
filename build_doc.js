const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, Footer } = require("docx");

const FONT = "Arial";
const NAVY = "1F4E5F";
const GREY = "595959";

const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const P = (t, opts={}) => new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: t, ...opts })] });
const BULLET = (t) => new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 60 },
                                      children: Array.isArray(t) ? t : [new TextRun(t)] });
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
function cell(text, w, { bold=false, fill=null, italic=false, color=null }={}) {
  return new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: fill ? { fill, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text, bold, italics: italic, color: color||undefined, size: 20 })] })],
  });
}
function headerRow(cells, widths) {
  return new TableRow({ tableHeader: true, children: cells.map((c,i)=>cell(c, widths[i], { bold:true, fill:"D5E8F0" })) });
}
function row(cells, widths, opts=[]) {
  return new TableRow({ children: cells.map((c,i)=>cell(c, widths[i], opts[i]||{})) });
}

// ---- Table 1: the $100, decomposed
const cw1 = [3700, 1700, 3960];
const dollarTable = new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: cw1,
  rows: [
    headerRow(["Channel / peel (per $100 total)", "Per $100", "Basis"], cw1),
    row(["Federal contribution (enters from above)", "$64.70", "64.7% benefit share"], cw1),
    row(["State contribution", "$35.30", "35.3%"], cw1),
    row(["= the Medicaid dollar", "$100.00", "the unit of the diagram"], cw1, [{bold:true},{bold:true},{bold:true}]),
    row(["less Administration (state agency)", "\u2212$5.07", "state / program overhead"], cw1),
    row(["less Medicare premiums for duals (agency)", "\u2212$2.90", "Medicaid \u2192 Medicare, peels out"], cw1),
    row(["= disbursed to payers", "$92.03", ""], cw1, [{bold:true},{bold:true},{}]),
    row(["   MCO \u2014 non-dual capitation", "$40.06", "modeled (dashed)"], cw1),
    row(["   Duals \u2014 dual managed-care capitation", "$10.89", "modeled (dashed)"], cw1),
    row(["   Fee-for-service, itemized", "$41.08", "measured (solid)"], cw1),
  ],
});

// ---- Table 2: six provider nodes x three lanes
const cw2 = [2900, 1300, 1300, 1300, 1560];
const provTable = new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: cw2,
  rows: [
    headerRow(["Provider node (per $100 total)", "FFS", "MCO", "Dual", "Total"], cw2),
    row(["Long-term care", "$19.72", "$6.93", "$1.89", "$28.54"], cw2, [{},{},{},{},{bold:true}]),
    row(["Hospitals", "$8.68", "$7.84", "$2.14", "$18.66"], cw2, [{},{},{},{},{bold:true}]),
    row(["Other (net of behavioral)", "$4.95", "$6.59", "$1.79", "$13.33"], cw2, [{},{},{},{},{bold:true}]),
    row(["Physicians & clinics (incl. FQHC)", "$2.87", "$7.68", "$2.08", "$12.63"], cw2, [{},{},{},{},{bold:true}]),
    row(["Behavioral health (cross-cutting)", "$3.48", "$4.74", "$1.29", "$9.51"], cw2, [{},{},{},{},{bold:true}]),
    row(["Rx drugs (net of psychotropics)", "$1.38", "$1.87", "$0.51", "$3.76"], cw2, [{},{},{},{},{bold:true}]),
    row(["Total to providers", "$41.08", "$35.65", "$9.69", "$86.42"], cw2, [{bold:true},{bold:true},{bold:true},{bold:true},{bold:true}]),
    row(["less Documented fraud", "", "", "\u2212$0.15", "$86.27 delivered"], cw2, [{},{},{},{},{bold:true}]),
  ],
});

// ---- Table 3: beneficiary
const cw3 = [3000, 1400, 2700, 2260];
const benTable = new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: cw3,
  rows: [
    headerRow(["Model group", "Share", "Services consumed (per $100)", "Built from (Ex.21)"], cw3),
    row(["Children", "15.6%", "$13.48", "Children"], cw3),
    row(["Adults (incl. expansion)", "34.2%", "$29.56", "New adult 22.5% + other 11.7%"], cw3),
    row(["Disabled (under 65)", "28.9%", "$24.98", "Disability basis"], cw3),
    row(["Aged (65+)", "21.3%", "$18.41", "Age 65+"], cw3),
    row(["Total (= provider dollars reaching care)", "100%", "$86.42", ""], cw3, [{bold:true},{bold:true},{bold:true},{}]),
  ],
});

// ---- Assumptions
const cwA = [560, 2600, 6200];
const aRows = [
  ["A1","Managed-care service allocation","The $496B capitation lump is a single line in CMS-64. The two modeled lanes (MCO, Duals) are itemized across the provider nodes using the HMA T-MSIS service mix, which prices managed-care encounter utilization at FFS / Medicare fee-schedule rates. Caveat: HMA \u201CProfessional\u201D unbundles hospital-based physician work that CMS-64 bundles into Hospital, so Physicians & clinics is overstated and Hospitals understated relative to CMS-64 convention; the categories do not map one-to-one."],
  ["A2","Eligibility-group vintage","Group spending shares are FY2023 (the latest T-MSIS-based cut) applied to FY2024 totals; T-MSIS lags the CMS-64 category data by about a year."],
  ["A3","Basis: the $100 combined dollar","The unit is $100 of TOTAL Medicaid outlays (benefits + administration), split federal $64.70 / state $35.30 at the 64.7% benefit share. Administration is jointly funded, so the true federal share of the combined dollar is ~64%; the headline 64.7% is used for the entry split. There is no federal-only gross-up: the dollar is the combined sum from the outset."],
  ["A4","FQHC handling (MERGED)","FQHC / clinic is a clean ~$19B line on the FFS side (Exhibit 17) but is not separable in the HMA mix on the capitated side, where it sits inside \u201CProfessional.\u201D Rather than show an FFS-only FQHC node that understates it, FQHC is MERGED into Physicians & clinics \u2014 which completes the clinician figure and is where the capitated FQHC dollars already live."],
  ["A5","Shareholder earnings carve","Net earnings attributable to public MCO-parent shareholders, Medicaid-attributable ($0.76 per $100), must be allocated from 10-K segment data. Highest-uncertainty figure; a subset of margin, never additive."],
  ["A6","Drugs net of rebates","Drugs are shown net of manufacturer rebates (CMS-64 already reports them net), consistent with excluding the rebate loop-back."],
  ["A7","Fraud proxy","Documented fraud uses MFCU recoveries ($1.4B, ~0.15% of benefits = $0.15 per $100), which understate total fraud. Treated as a true loss peeling off providers; drawn not-to-scale."],
  ["A8","Behavioral health (cross-cutting carve)","BH is ~9.3\u201313% of Medicaid spending (APA / Psychiatric Services claims-based review) and Medicaid is the largest U.S. behavioral-health payer (~24% of all national BH spending, MACPAC). BH has no single CMS-64 line \u2014 it sits in inpatient psych (Hospitals), psychiatry / therapy / CMHC (Physicians & clinics), rehab / residential / community / case-management (Other, its largest source), psychotropics (Rx) and a little psychiatric residential (LTC). The $9.51 node (~11% of service dollars) is carved proportionally from those five lines; per-line splits are estimates pending T-MSIS. Its beneficiary pie (heavy Adults + Disabled) is likewise estimated."],
  ["A9","Duals scope & lane","Duals carry Medicaid dollars only; Medicare is excluded throughout. The Duals lane is dual managed-care capitation only (it carries the plan carve); duals\u2019 FFS spending sits in the FFS lane. Medicare premiums for duals ($27.8B) peel out at the agency."],
  ["A10","Reporting-window mismatch","CMS-64 (federal FY), NHE (calendar year), MCO 10-Ks (company FY), the Duals Data Book (CY2022) and the HMA mix (CY2021) use different windows. Anchored to FY2024 where possible; others used as cross-checks."],
  ["A11","Dual capitation split (Lane 2)","Dual managed-care capitation is triangulated at ~$106B (about 21\u201323% of the $496B capitation; band $100\u2013115B) from the CY2022 MedPAC\u2013MACPAC Duals Data Book \u2014 $10.89 per $100 total. The model\u2019s softest number."],
  ["A12","HMA mix vintage","The HMA service mix is CY2021 (disaggregated); the CY2023 update is directionally similar (Professional ~30%). Applied to FY2024 capitation, with the vintage offset footnoted."],
  ["A13","Collections folded","Third-party collections / recoveries (~$15B, ~$1.6 per $100) are folded proportionally into the three payer lanes rather than shown as a separate peel, so the lanes are net of collections."],
];
const assumpTable = new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: cwA,
  rows: [ headerRow(["#","Topic","Decision / gap"], cwA),
          ...aRows.map(r => row(r, cwA, [{bold:true},{bold:true},{}])) ],
});

// ---- Sources
const cwS = [4400, 1400, 3560];
const sRows = [
  ["MACStats Feb 2026, Ex.17 \u2014 Total Benefit Spending by Category","FY2024","macpac.gov"],
  ["MACStats Feb 2026, Ex.16 \u2014 Spending by Source of Funds","FY2024","macpac.gov"],
  ["MACStats Feb 2026, Ex.21 \u2014 Eligibility Group & Dually Eligible Status","FY2023","macpac.gov"],
  ["MACPAC news release \u2014 $957.4B total, 64.7% federal","FY2024","macpac.gov"],
  ["CMS National Health Expenditure Highlights \u2014 Medicaid $931.7B","CY2024","cms.gov"],
  ["HMA, \u201CNew Insights on Medicaid Spending\u201D \u2014 T-MSIS service mix (MC allocation key)","CY2021/23","healthmanagement.com"],
  ["MedPAC\u2013MACPAC Duals Data Book \u2014 dual Medicaid $197.4B; Ex.12 / 16 / 18","CY2022","medpac.gov"],
  ["HHS-OIG MFCU Annual Report \u2014 $1.4B recovered","FY2024","oig.hhs.gov"],
  ["Psychiatric Services (APA) \u2014 Medicaid behavioral health = 9.3\u201313% of spending","review","psychiatryonline.org"],
  ["MACPAC \u2014 Medicaid = ~24% of all U.S. behavioral-health spending","current","macpac.gov"],
  ["Georgetown CCF \u2014 Big Five Medicaid MLR (Centene 90.9%, Molina 89.7%)","2024","ccf.georgetown.edu"],
  ["Centene Corp SEC filings \u2014 Medicaid HBR & SG&A","FY2024","sec.gov EDGAR"],
];
const srcTable = new Table({
  width: { size: 9360, type: WidthType.DXA }, columnWidths: cwS,
  rows: [ headerRow(["Source","Vintage","Domain"], cwS),
          ...sRows.map(r => row(r, cwS)) ],
});

const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: FONT, color: NAVY },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: FONT, color: "000000" },
        paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: "bul", levels: [{ level:0, format: LevelFormat.BULLET, text:"\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 260 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [ new Paragraph({ alignment: AlignmentType.CENTER,
      children: [ new TextRun({ text: "$100 Medicaid Dollars \u2014 Methodology & Sources   |   FY2024   |   page ", size: 16, color: GREY }),
                  new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }) ] }) ] }) },
    children: [
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "$100 Medicaid Dollars", bold: true, size: 44, font: FONT })] }),
      new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "DRAFT V.4 \u2014 Public Comment", bold: true, size: 22, color: "C0392B" })] }),
      new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Methodology, Data Sources & Assumptions", size: 28, color: NAVY })] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: "Federal fiscal year 2024  \u00b7  prepared for the $100 Medicaid Dollars infographic  \u00b7  the unit is $100 of total (federal + state) Medicaid spending", italics: true, color: GREY, size: 20 })] }),

      H1("1. Purpose and scope"),
      P("This document records every source and modeling decision behind the Medicaid dollar-flow infographic, so the figures can be audited and reproduced. The companion workbook (medicaid_dollar_data.xlsx) holds the live numbers; this document explains where they come from and the judgment calls made to assemble them."),
      P("The infographic traces a single $100 \u2014 the combined federal-and-state Medicaid dollar \u2014 from the point where the two streams merge, through the state agency, across three payer lanes, to providers, and finally read as the share of services consumed by each beneficiary group. It is the Medicaid analogue of the employer-sponsored \u201C$100 healthcare dollar\u201D reference, one year more current."),

      H1("2. Time period and headline reconciliation"),
      P("FY2024 is the most recent year with actual (not projected) federal data across all the sources the model needs: CMS-64 expenditure reporting, MFCU fraud recoveries, and insurer 10-Ks. Calendar-2025 figures exist only as actuarial projections, so they are excluded."),
      P("The totals that appear in the sources reconcile as follows:"),
      BULLET("Total Medicaid spending, benefits plus administration: $957.4B (MACStats Exhibit 16) \u2014 this is the $100 unit."),
      BULLET("Benefit spending only: $908.8B (Exhibit 17) \u2014 the basis for the channel, provider, and beneficiary splits ($94.93 per $100)."),
      BULLET("Federal share 64.7% (about $620B), state share 35.3% \u2014 down from a 69% federal share in FY2023 as the enhanced pandemic match unwound."),
      BULLET("NHE (calendar 2024) reports Medicaid at $931.7B on a different accounting basis; used only as a cross-check, not as a model input."),

      H1("3. The $100 Medicaid dollar"),
      P("Unlike the earlier draft, which started from a federal $100 and grew it by the state match, the diagram now starts from the combined dollar: $64.70 of federal money enters from above and merges with $35.30 of state money to make the $100 Medicaid dollar. Naming the combined sum \u2014 not the federal piece \u2014 as \u201Cthe Medicaid dollar\u201D is the key reframing, and it keeps the unit comparable to the employer dollar."),
      P("The 64.7% / 35.3% split is the published federal share of benefit spending. Because administration is jointly funded on a different match, the exact federal share of the combined dollar is closer to ~64%; the headline 64.7% is used for the entry split (Assumption A3). Match rates vary by state, which is where the supplementary state-fork views diverge from this national average."),

      H1("4. From the $100 to the payer lanes"),
      P("Two losses peel off sequentially at the state agency before any care is bought: administration ($5.07, state and program overhead) and Medicare premiums Medicaid pays on behalf of dual eligibles ($2.90, which is Medicaid paying Medicare, not Medicaid buying care). The remaining $92.03 is disbursed across three payer lanes that are kept separate all the way to the provider phase."),
      dollarTable,
      new Paragraph({ spacing: { before: 120, after: 120 }, children: [new TextRun({ text: "Fee-for-service is a pass-through, not a payer: its dollars reach providers unchanged, and it is the only measured lane (solid in the infographic). The two capitation lanes are modeled (drawn dashed) and retain administration, margin, and shareholder earnings before paying providers (Section 6). Third-party collections (~$1.6 per $100) are folded proportionally into the three lanes (Assumption A13).", size: 22 })] }),
      H2("Splitting the dual managed-care lane"),
      P("The dual lane is the model\u2019s softest number, because CMS-64 does not separate dual from non-dual capitation. It is triangulated from the CY2022 MedPAC\u2013MACPAC Duals Data Book: total Medicaid spending on duals was $197.4B (of which $194.7B full-benefit); 43% of duals had some comprehensive managed care; even duals classified as fee-for-service still ran 12% of their Medicaid dollars through capitation; and the 2.0 million fee-for-service full-benefit duals accounted for $58.3B. Cross-checking those pieces brackets dual managed-care capitation at about $100\u2013115B, central estimate ~$106B \u2014 roughly 21\u201323% of the $496B, or $10.89 per $100 (Assumption A11)."),

      H1("5. Providers"),
      P("Every payer lane is itemized into the same six provider nodes \u2014 Long-term care, Hospitals, Other, Physicians & clinics, Behavioral health, and Rx drugs \u2014 ordered largest to smallest, so the payer mix reaching each provider type stays visible. The two managed-care lanes and the FFS lane use different methods, reflecting the data that exists."),
      provTable,
      H2("Fee-for-service lane (measured)"),
      P("The CMS-64 service categories in Exhibit 17 collapse onto the nodes directly: Hospital to Hospitals; Physician, Other practitioner and Clinic & health center (incl. FQHC) to Physicians & clinics; Institutional plus home-and-community-based LTSS to Long-term care; Drugs (net of rebates) to Rx drugs; and Dental plus Other acute (which bundles transportation, DME, EPSDT, therapies, hospice, and lab) to Other. Long-term care dominates the FFS lane at roughly half of it, because the most expensive Medicaid populations \u2014 the aged and disabled \u2014 remain heavily fee-for-service."),
      H2("Managed-care lanes (modeled via the HMA T-MSIS key)"),
      P("Because CMS-64 reports capitation as one line, the MCO and dual lanes are allocated across the nodes using the HMA \u201CNew Insights on Medicaid Spending\u201D service mix, derived from T-MSIS encounter records priced at FFS and Medicare fee-schedule rates. The CY2021 mix \u2014 Professional 25.1%, SNF/HCBS 19.7%, Inpatient 15.4%, Other 13.2%, Outpatient 8.4%, Pharmacy 7.9%, Dental 4.8% \u2014 maps to the nodes (Inpatient + Outpatient to Hospitals; Professional to Physicians & clinics; SNF/HCBS to Long-term care; Pharmacy to Rx; Dental, Other and the residual to Other)."),
      H2("FQHCs are merged into Physicians & clinics"),
      P("FQHC / clinic is a clean ~$19B line on the fee-for-service side, but on the capitated side it is not separable in the HMA mix \u2014 those dollars sit unlabeled inside \u201CProfessional.\u201D A standalone FQHC node would therefore show only its FFS slice and understate it by more than half. Folding FQHC into Physicians & clinics completes the clinician figure and is where the capitated FQHC dollars already live (Assumption A4)."),
      H2("Behavioral health is broken out as a cross-cutting node"),
      P("Behavioral health is roughly 9.3\u201313% of Medicaid spending and Medicaid is the nation\u2019s largest behavioral-health payer, but it is not a single CMS-64 line \u2014 it is smeared across inpatient psychiatric care (in Hospitals), outpatient psychiatry / therapy / community mental-health clinics (in Physicians & clinics), the Medicaid-specific rehabilitative / residential / community / case-management services (in Other, its single largest source), psychotropic drugs (in Rx), and a little psychiatric residential care (in LTC). The model carves a Behavioral health node of $9.51 per $100 (~11% of service dollars) proportionally from those five lines, so it is visible as its own tributary. The cross-line split is an estimate that T-MSIS claims tagged by diagnosis would refine; \u201COther\u201D is the largest contributor but is not the whole story (Assumption A8)."),
      H2("Two honest caveats"),
      BULLET("The HMA \u201CProfessional\u201D bucket unbundles hospital-based physician work that CMS-64 bundles into the hospital figure, so on the managed-care side Physicians & clinics is overstated and Hospitals understated; the two lanes are not measured on identical definitions (Assumption A1)."),
      BULLET("\u201COther\u201D ($13.33, net of behavioral health) remains a CMS-64 catch-all \u2014 dental plus \u201Cother acute\u201D (NEMT, DME, lab/imaging, therapies, EPSDT/preventive, hospice, case management) \u2014 which the source does not itemize. Per-service amounts inside it are rough ranges only."),
      P("After all peels, $86.42 of every $100 reaches providers: $41.08 through fee-for-service, $35.65 through MCOs, and $9.69 through dual plans. Documented fraud of $0.15 then peels off, leaving $86.27 delivered. The $86.42 is the base for the beneficiary phase."),

      H1("6. Leakages"),
      H2("Plan-retained (true loss)"),
      P("Of every dollar of capitation, managed-care plans deliver roughly 89 cents of care (the medical loss ratio), retain about 9 cents for administration, and keep a thin underwriting margin of about 2 cents (the federal MLR floor is 85%). This carve applies to both capitated lanes: the dual plans (D-SNPs and MLTSS) retain on the same terms as the non-dual MCOs. Across the two lanes it removes $5.61 of every $100 as a true loss that peels up off the flow before providers are paid \u2014 of which $4.85 is plan administration and $0.76 is the public-company shareholder-earnings carve, a subset of margin, never added on top, and the highest-uncertainty figure in the model (Assumption A5). The $4.85 of plan administration is itself split by lane in proportion to retention: $3.81 from the non-dual MCO lane and $1.04 from the dual-MCO lane (D-SNPs and MLTSS), so the dual plans show their administrative carve explicitly rather than buried in the combined figure. Duals\u2019 fee-for-service spending carries no carve and sits in the FFS lane."),
      H2("Documented fraud (true loss)"),
      P("Medicaid Fraud Control Units recovered $1.4B in FY2024 \u2014 about 0.15% of benefits, or $0.15 per $100. This is a recoveries figure and understates total fraud, but it is the documented number and is shown as a small true-loss arrow off providers, drawn not-to-scale (Assumption A7). The earlier draft\u2019s PERM improper-payment overlay was removed in this version: improper payments are largely paperwork and eligibility-verification errors, not money that bought no care, and they confused the loss narrative."),

      H1("7. Beneficiaries"),
      P("The final phase changes units: instead of dollars paid, it reads as the share of Medicaid-funded services consumed by each group, Medicaid dollars only. The base is the $86.42 that actually reaches providers, and the FY2023 group shares are applied to it. Grouping is by basis of eligibility (Exhibit 21), not by enrollment pathway."),
      benTable,
      new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: "Per-service pies, balanced not assumed.", bold: true, size: 22 })] }),
      P("An earlier draft applied one set of group shares to every service \u2014 which wrongly implied that long-term care was only ~21% aged. In this version each service\u2019s beneficiary split is fit by iterative proportional fitting (IPF) to two hard constraints \u2014 the service dollar totals (rows) and the group spending totals (columns) \u2014 seeded with established utilization patterns. The result reconciles to both margins and is far more realistic: long-term care reads ~90% Disabled + Aged, behavioral health ~79% Adults + Disabled, and physicians / clinics tilt toward Children + Adults. The within-cell pattern is still an estimate; an exact service \u00d7 group cross-tab (T-MSIS) would firm it. The pies are a re-expression of provider dollars, not a measured money flow."),
      new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: "Aged-blind-disabled vs. SSI.", bold: true, size: 22 })] }),
      P("\u201CAged, blind, and disabled\u201D is an eligibility category; SSI is one pathway into it, not a separate group. SSI recipients are therefore distributed by age \u2014 SSI-disabled into Disabled, SSI-aged into Aged. Age breaks ties, so a 65+ disabled person counts as Aged (Disabled is effectively under-65), and some functionally disabled people enrolled through the ACA expansion pathway are counted as Adults in the source data \u2014 a documented boundary (Assumption A2)."),
      P("The beneficiary axis is orthogonal to the duals payer lane: a 70-year-old dual appears in the Aged group here and in the duals lane upstream with no double-count, because upstream measures dollars administered and this phase measures services consumed."),

      H1("8. Assumptions and mapping decisions"),
      assumpTable,

      H1("9. Sources"),
      P("All sources accessed 8 June 2026. Federal fiscal year unless noted."),
      srcTable,
    ],
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync("/home/claude/medicaid_dollar_methodology.docx", buf); console.log("saved docx"); });
