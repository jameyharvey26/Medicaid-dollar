# Next session — Medicaid Dollar Project, national panel

Pull fresh, `pip install resvg_py pymupdf --break-system-packages`, install
playwright chromium, then `python3 gates.py`. **All seven should be green.**
If `render_v6_1.py` fails, check `pymupdf` is installed before anything else —
without it both layout gates crash before they run.

Read `MANIFEST_SESSION.md` from 2026-09-26 first. D-87 through D-90 and S-108
landed, the 25 September national set was renumbered from D-78..81 to
D-83..86, and the manuscript moved to `paper_national_v6_1.html` with
`render_v6_1.py`. `DECISIONS.md` is now the register — read the highest number
off it before you allocate anything, and do not allocate from a gap.

Run `DELETE OLD FILES.command` before you commit: `render_v6_0.py` and
`Medicaid_Dollars_National_v6.0.pdf` are on the list for 2026-09-26. Deletions
go on that list, never in the chat.

We are building **v6.2**. Nothing below is started. Do these in this order.

## 1. The Adults row becomes two rows. D-91.

This is first because every number in items 2 and 3 depends on it.

Exhibit 21 — the row already signed in `ledger_national_2024.py` at vintage
FY2023 — publishes five eligibility columns and we summed two. Split Adults
into **New adult group 22.5%** and **Other adult 11.7%**, derived from the
exhibit's percentages in code, not typed. The Adults figure is signed, so it
reports LAPSED on edit; I sign the two replacements, you do not.

Then the downstream: the pie interiors are IPF-fit to both margins, so a fifth
row changes the fit, every panel carrying beneficiaries re-renders, and
everything re-blesses. Layout gates last.

## 2. The beneficiary section, and the two households.

`inc.py` has the cube, `family.py` the graphic. Publish **margins only** in the
body — per-service falls, which are already signed, and per-population totals
from the provision logic. The full cube goes in a footnote with the
contradiction declared: unraked it disagrees with Figure 11 on every service,
raked it puts adults at 44.9% of their own long-term care.

Changes I want:
- Make the two households **identical except for the disability and the
  grandmother**. Same parent ages, same children's ages. It becomes a
  controlled comparison: one exemption expires on a birthday, the other never
  does.
- Express everything in **dollars and cents off the hundred**, not rates. In
  2024 this much reached people like them; in 2030 this much.
- **No individual loses a percentage of their care.** They keep it or they go
  to zero. Split each group's loss into coverage — someone dropped — and rate
  — same person, provider paid less. The numbers are in `inc.py`.
- The aside box carries the assumption set. Footnote the rest.

## 3. A family of tapers.

Figures 6, 7, 8, 9 and 11 all become generated infographics in the cover's
language — horizontal versions of the taper, provision by provision — not
crops of the master panel. One idea each. Each gets its own script, PNG, SVG
and generated alt text in the repo, like `cover_taper.py`. Section 508 / WCAG
AA, measured not asserted, as the cover was.

Crop the AGILIAN / THE MEDICAID DOLLAR PROJECT header out of the **cover**
version of the taper. Keep it on the standalone.

## 4. JW's 77 PDF annotations.

They are in `Medicaid_Dollars_National_v6_1_JW_comments.pdf`. Extract them with
pymupdf — the sticky notes are not in the text layer. Apply all of them, fix
the punctuation the PDF selection broke, and bring every change back to me for
sign-off under S-108. Two need reconstruction rather than a clean cut: the
page 4 strikeouts leave a fragment, and the two page 12 stickies read as
"Load sits inside the capitation rate **allowed to Payers** as a percentage of
**premiums**."

**Correction to my own notes:** on pages 11 and 13 I had the top three and
bottom three the wrong way round. The three carrying the directed payment cap
are physicians and clinics, hospitals and long-term care. The three carrying
only the general contraction are wrap around services, behavioral health and
prescription drugs. §71116 does not reach beneficiary groups at all.

## 5. Footer collisions.

Body text runs into the footer on pages 4, 6 and 8. It needs a real margin
rule, not a nudge. Layout gates run last, after every geometry change.

## Standing, and I want these raised at close every session until they are real

- The landing-page URL and repository path are still placeholders. The footer
  of v6.1 reads `[landing page pending]` and `[repository pending]`. The paper
  cannot ship.
- The repo is still public and `AUTHOR_HELD_SHEILA.md` and the handoff files
  carry a named third party's employer and bio.
- The Medicare Savings marker sits on the providers/beneficiaries divider but
  is subtracted in the disbursement segment. Declared exception in
  `DECREMENT_X`. Needs a note on the marker or my acceptance.
- `DECISIONS.md` finds 14 of 90. Backfilling the rest is open.
- The pie interiors carry no citation — IPF-fit from an unsourced seed, and the
  cube reads off them. Limits register entry owed.

## Working style

One question at a time. Show me the picture before any layout claim. Recommend
on methodology, ask on direction. Prose follows the figure, always to me for
sign-off. Derive in code, never type an output. Commit at close, not
mid-session.
