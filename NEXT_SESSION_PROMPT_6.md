Picking up the Medicaid dollar project.

Pull JameyHarvey26/Medicaid-dollar, branch main. Read `SESSION_START.md` and
follow it. It carries the build, the gates, the read list, the house rules and
the commit rules. This brief carries only what changed and what this session is
for. Where the two disagree, this one is newer — say so rather than picking.

Note `SESSION_START.md` §8 is now partly wrong: `byteproof.py` no longer exists
and `scale` no longer means two things. Read `MANIFEST_SESSION.md` from the
18 September entry down before you believe anything else in it.

## Ask me two things, one at a time

**The DHCF report.** Has anyone opened it? The DC ledger carries plan revenues
of $425.3M for Wellpoint and $411.2M for MedStar, traced to an uncited constant
in `build_sankey_dc.py`. Wellpoint's own CY2023 Medicaid premium is $280.7M.
MedStar's DC Medicaid is $425.0M — within $0.3M of the figure sitting under
Wellpoint's name. Either two plans are swapped or all three are CY2022. Do not
model around it and do not pick the likelier explanation.

**The working record.** D-68 took Sheila off every artifact, but
`WHITEPAPER_BRIEF.md`, `MANIFEST_SESSION.md` and the handoff files still carry
her name, her employer and her bio verbatim, and the repo is public. That was
declared out of scope on the day. It still is unless I say otherwise.

## What happened on 18 September

**The $100 moved.** D-70: it is struck at the state agency, where the money
becomes a Medicaid dollar, not at appropriation. Denominator $957,403M →
$950,164M. The federal column now carries more than $100 and exactly $100
arrives. Vaccines for Children, $0.76 and wholly federal, peels off the top of
the federal column, never blends, terminates at CDC (D-71, EN-49). The old
$5.07 administration split into administration $4.25 and federal oversight
$0.10 (D-72, EN-50). The tracker starts at $100.76 and gained a fifth anchor,
"Budgeted to Medicaid" (D-73, D-74). Losses are measured from the hundred, so
the vaccine is not a loss and the FY2030 provider tax is (D-75).

Read `WHITEPAPER_BRIEF_APPEND_2026-09-18.md` for all of it. D-68 and D-69
concern authorship and the limits register; the rest is the above.

**Signed.** 36 figures at `2026-09-18 JW` on the stacked sheets. Coverage reads
24 verified, 2 modelled, 2 unverified, 3 missing. The two unverified are the
modelled plan margins and are correctly unsigned.

**`byteproof.py` is gone, `renderproof.py` replaces it.** A golden-render
register over every panel the build emits, with a difference image and a
bounding box on failure. Blessing carries a reason. It runs at session close,
not on every build. S-104. If it fails and every change was intended:
`python3 renderproof.py --bless "why"`.

## This session

**The manuscript, and nothing else until it is done.**

It is TWO rounds behind. It shipped 15 September and never received the
16 September behavioural health carve, so it still says $28.53 long-term care
and $12.63 physicians against figures now reading $29.13 and $10.87. Round A
moved four nodes by up to two dollars in opposite directions; round B is a
uniform 0.76 percent rescale. `CHANGE_MAP_2026-09-18.md` has all 144
replacements with line numbers.

Apply it BY LINE. Seven tokens collide — the new value of one figure is the old
value of another. `$0.75` becomes `$0.76`, which is the old earnings figure,
which becomes `$0.77`, and `$0.76` is also the new vaccine peel. A global
find-and-replace corrupts the file silently and the gates will not catch it.

Keep the text and the layout as they are. Change numbers, and change prose only
where a number's meaning changed or a new path appears. The figures are already
regenerated and `figurefit` passes.

Six things need a sentence, not a number, and they are listed at the end of the
change map. The one I care most about: the FY2030 headline falls from 22.21
percent lost to 21.61, because the vaccine money stopped counting as a loss.
The law did not change. Our definition did. Say so.

## Then, in this order

1. **DC Phase 2 signing.** Acquired, unsigned, deliberately held back on
   18 September because its scale and administration are read against the
   denominator D-70 moved. Re-check them against the new definition before
   asking me to sign anything.
2. **DC Phase 1 continued**, in `ACQUISITION.md` order: scale and the peels,
   then the lanes, then the named plans, then the payer splits, then the claims
   allocation. Do not jump to the interesting numbers.

## Open, and not to be quietly closed

- The collections netting. Nationally $15.2B spread pro rata across both lanes;
  in DC the whole $10M is netted onto fee-for-service alone. Opposite treatments
  of the same money in one paper. Endnote unless you can show me otherwise.
- The plan administration sentence from the old author-page disclosure, still
  unhomed. It matters more once the DC payer lane names actual plans.
- `build.py` does not rebuild the FY2030 `holds` and `scales` variants in a
  working session, so they can sit stale in `reference_renders` and be blessed
  as if live. Found 18 September, not fixed.
- The author page: one four-line bio on an otherwise empty page, 29 dead lines.
  Left until the national presentation layer is opened.
- EN-43, the public-company earnings carve, deliberately unsigned.
- `legacy_mix=True` stays on. Turning it off does not render: `_cols()`
  correctly returns nothing once the capitated rows are unallocated and
  `compose` raises instead of declaring the absence. The seam has an absent-lane
  path and no absent-node path. That is work.

## House rules I want held to this session

Show me the picture with any layout claim. One question at a time. Recommend on
methodology, ask on direction. Run the detector, not the eye — and when the
detector is wrong, fix the detector rather than the number it flagged.
