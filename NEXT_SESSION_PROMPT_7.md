Picking up the Medicaid dollar project.

Pull JameyHarvey26/Medicaid-dollar, branch main. Read `SESSION_START.md` and
follow it. It carries the build, the gates, the read list, the house rules and
the commit rules. This brief carries only what changed and what this session is
for. Where the two disagree, this one is newer — say so rather than picking.

`SESSION_START.md` §8 is out of date in two more places since 18 September: the
manuscript is now `paper_national_v5_0.html` and the renderer `render_v5_0.py`,
and page 6's whitespace stranding is closed, so four remain and not five. Read
`MANIFEST_SESSION.md` from the 19 September entry down before you believe
anything else in it.

## Do not ask me about these

S-092 is closed. Sheila saw the author-page disclosure and we deleted it. It is
not an open item and it does not come back.

The working record still carries her name, her employer and her bio in
`WHITEPAPER_BRIEF.md`, `MANIFEST_SESSION.md` and the handoff files, and the repo
is public. Still out of scope unless I say otherwise.

The manuscript shipped as v5.0 and went to early readers. Leave it alone this
session unless a DC finding forces a national figure to move, which it should
not.

## Ask me one thing, first

**The DHCF report.** Has anyone opened it? The DC ledger carries plan revenues
of $425.3M for Wellpoint and $411.2M for MedStar, and they trace to an uncited
constant in `build_sankey_dc.py` — a pre-ledger script that both DC ledgers
still import. Wellpoint's own CY2023 Medicaid premium is $280.7M. MedStar's DC
Medicaid is $425.0M, within $0.3M of the figure sitting under Wellpoint's name.
Either two plans are swapped or all three are CY2022. Do not model around it and
do not pick the likelier explanation. Everything below waits on the answer.

## This session: DC, and nothing else

Work `ACQUISITION.md` in its own order. Do not jump to the interesting numbers.

**1. Scale and the peels.** Two findings from 19 September are open here and
should be taken first, because they decide what a complete DC baseline even is.

The DC panel has no Vaccines for Children peel and no federal oversight peel,
and neither absence is declared. DC declares nine absences; these are not among
them. `coverage.py dc` does not list either figure as one the DC baseline needs,
because that list predates D-70, D-71 and D-72. The two as-is panels are
currently built to two different definitions of a complete baseline. Vaccines
for Children is federal money and appears in DC's CMS-64, so its absence is
probably a gap rather than a zero — but establish that, do not assume it.

DC does pay Medicare premiums, $1.97 per $100, measured. It is invisible on the
line only because the State Admin marker still holds administration and Medicare
premiums under one label. That is the §8 frozen item. Unfreeze it here or say
why not.

**2. The lanes.** Then **3. the named plans**, which is where the DHCF answer
lands. HSCSN is a CASSIP contractor with no NAIC health blank and should appear
as its own entity class between the MCOs and the dual plan. MedStar is
Maryland-domiciled; only Schedule T premium is recoverable for DC. Wellpoint DC
needs the amended CY2023 filing — the original mis-booked DC Healthcare Alliance
and Immigrant Children's Program funds. AmeriHealth Caritas DC is clean.

Then **4. the payer splits**, then **5. the claims allocation**.

**Then DC Phase 2 signing.** Acquired, unsigned, held back on 18 September
because its scale and administration read against a denominator D-70 moved.
Re-check them against the current definition before asking me to sign anything.
S-093 holds: no signature without a stacked before/after picture at full width.

## New since you last worked on this

**S-105. Derive in code, never type an output.** A figure the build computes
must not also be typed — not in a basis line, not in a note, not in a comment,
not as a constant standing in for arithmetic. `typedfigures.py` reports every
number inside a string or comment that equals something a ledger derives. It is
not a gate and a match is not a fault; the question is whether the number would
still be right if the figure moved. Thirty remain. **The worst of them are the
DC derivation comments at `ledger_dc_2024.py:36-56`**, which show worked
arithmetic in a comment that nothing recomputes, and you are about to edit that
exact block. Fix them as you pass through.

**D-76.** The FY2030 sources were the FY2024 sources, so $100.0061 arrived at
the state agency instead of $100.00. Corrected. The FY2030 line now reads
$98.75, $79.37, $78.38 and 21.62 percent. `check` did not catch it: TOL is $0.02
and the gap was $0.006. Assume the DC ledger has the same class of error until
you have looked.

**D-77.** Tracker anchor subtitles read "x.xx% less", not "% lost". Decimals
unchanged. One point in `sankey.py`; every panel goes through it.

`paper_figs/crops.json` is now committed. It was missing, and `figurefit`
crashed on a clean pull.

## Open, and not to be quietly closed

- The collections netting. Nationally $15.2B spread pro rata across both lanes;
  in DC the whole $10M is netted onto fee-for-service alone. Opposite treatments
  of the same money in one paper. **This one is DC's and it is in scope this
  session.** Endnote unless you can show me otherwise.
- Two DC ledger files and two FY2030 ledger files coexist with unclear division
  of responsibility. `instances.py` imports `ledger_dc`, `build.py` imports
  `ledger_dc_2024`. Settle it while you are in there.
- `build_sankey_dc.py` cannot be deleted while both DC ledgers import it. The
  point of Phase 1 is to make that deletion possible.
- The services table reads $87.07 against its own rows summing to $87.08, and
  its shares to 100.1 percent. Every figure in the paper is the figure printed
  on the diagram; that was my choice, note 8 carries both cents, and it is
  reversible. Do not reverse it without asking.
- The wrap-around ordering in the body text rests on a $55.1B / $6.2B split that
  lives in `build_xlsx.py`, not the ledger. It reconciles to the dollar, but it
  is hand-carried. S-073 exposure.
- `build.py` does not rebuild the FY2030 `holds` and `scales` variants in a
  working session, so they can sit stale and be blessed as if live. Run
  `build.py sensitivity` before `renderproof.py --bless`. Found 18 September,
  still not fixed.
- The author page: one four-line bio on an otherwise empty page, 29 dead lines.
  The plan administration sentence from the deleted disclosure is still unhomed
  and matters more once the DC payer lane names actual plans.
- EN-43, the public-company earnings carve, deliberately unsigned.
- `legacy_mix=True` stays on. The seam has an absent-lane path and no
  absent-node path. That is work.
- **The repo is public and v5.0 has gone to outside readers.** Raised 19
  September, not decided.

## House rules I want held to this session

Pull, build, look at the diagram, then change something — in that order. Show me
the picture with any layout claim. One question at a time. Recommend on
methodology, ask on direction. Run the detector, not the eye — and when the
detector is wrong, fix the detector rather than the number it flagged. No
hand-carried figures: if it is in prose or a caption it must be derivable from
the ledger.
