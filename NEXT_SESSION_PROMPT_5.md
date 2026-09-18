Picking up the Medicaid dollar project.

Pull JameyHarvey26/Medicaid-dollar, branch main. Read `SESSION_START.md` and
follow it. It carries the build, the gates, the read list, the house rules and
the commit rules. This brief carries only what changed and what this session is
for. Where the two disagree, this one is newer — say so rather than picking.

## Ask me three things, one at a time

**S-092.** Has Sheila seen the disclosure wording on the author page?

**The DHCF report.** Has anyone opened it? The DC ledger carries plan revenues
of $425.3M for Wellpoint and $411.2M for MedStar, traced to an uncited constant
in `build_sankey_dc.py`. Wellpoint's own CY2023 Medicaid premium is $280.7M.
MedStar's DC Medicaid is $425.0M — within $0.3M of the figure sitting under
Wellpoint's name. Either two plans are swapped or all three are CY2022. Do not
model around it and do not pick the likelier explanation.

**C-07.2.** grep "Medicaid dollar" singular. Count matching lines, not
occurrences — two lines carry it twice. It was 32 lines across 18 files, zero in
the live manuscript. Report before drafting.

## Where things stand

Phase 0 closed 16 September. The national baseline was re-sourced against
MACStats February 2026 and re-signed at `2026-09-16 JW`, 33 figures, on the
stacked comparison sheets. The provider phase now computes in `provider_mix.py`
from three declared inputs; the MACPAC CY2023 behavioral health carve replaced
five hand-set numbers and moved four nodes. See EN-48.

DC Phase 1 is open. Cost allocation is done and re-acquired from Exhibit 16
FY2024 — federal 73.17, non-federal 26.83, scale $43.72M, administration $5.35 —
with the Exhibit 16 dollars in the ledger as anchors. All of it unsigned.

NAIC is done as far as it goes. AmeriHealth Caritas DC and Wellpoint DC have
administrative expense for both years, DC-only. MedStar Family Choice Inc is
Maryland-domiciled, so its Page 7 Title XIX is Maryland and DC together: DC
premium comes from Schedule T, and DC claims, admin and gain are not in the
filings at all. HSCSN files no health blank. Use the amended Amerigroup CY2023
filing, never the original — DISB made them refile because Alliance and ICP were
booked inside Title XIX.

## This session

**DC Phase 1, continued.** Next is scale and the peels, then the lanes, then the
named plans, then the payer splits, then the claims allocation, in the
`ACQUISITION.md` order. Do not jump to the interesting numbers.

`legacy_mix=True` stays on. My ruling of 16 September: leave DC borrowing the
national service mix until its own figures land, then turn the flag off in one
move. Note it is not a flag any more — turning it off does not render, because
`_cols()` correctly returns nothing once the capitated rows are unallocated and
`compose` raises instead of declaring the absence. The seam has an absent-lane
path and no absent-node path. That is work.

HSCSN gets its own entity class in the DC payer lane, between the MCOs and the
dual plan, on a DHCF basis that must be declared as different from its
neighbours.

**Three national items left open on purpose.** In this order, and show me each
before applying it.

1. The administration relabel. $5.07 is administration $4.32 plus Vaccines for
   Children $0.76. The artifact calls the whole thing state programme overhead.
   Recommend relabel or split, and show the picture either way.
2. The collections declaration. The payer lanes are net of $15.2B of collections
   spread pro rata across capitation and fee-for-service. Recoveries fall on
   fee-for-service far more than on capitation. Endnote unless you can show me
   otherwise.
3. `scale` means two things across the two ledgers.
