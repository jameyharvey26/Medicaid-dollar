Picking up the Medicaid dollar project. The national paper is at v4.1 and is done.
Phase 0 is nearly closed. One piece of it remains and then Phase 1.

## Before anything else

**Upload what Sora found.** I asked Sora Shin to pull four DC health entity annual
statements from DISB. If they are not already in this chat, ask me for them before
starting the NAIC work. The four are AmeriHealth Caritas District of Columbia Inc,
Amerigroup District of Columbia Inc (the plan is now Wellpoint DC), MedStar Family
Choice DC, and Health Services for Children with Special Needs Inc, CY2024 and
CY2023 if posted. If she came back empty, say so and stop rather than substituting
a source.

**Ask me S-092.** Has Sheila seen the disclosure wording on the author page? Keep
asking until I say yes. One line, then move on.

**Run the C-07.2 scan.** grep for "Medicaid dollar" singular. It was 32 instances
across 18 files, zero in the live manuscript. Report the number before drafting.

## Get the build up

Pull fresh from JameyHarvey26/Medicaid-dollar, branch main, note the "26". Then
`pip install resvg_py pymupdf playwright --break-system-packages`.

```
python3 build.py        five panels, one expected NOTE about State Admin and
                        Eligibility Rules sitting 24 units apart. Not to be fixed.
python3 crossings.py    0 on all five, and no ORPHAN lines.
python3 byteproof.py    must print "seam is a no-op". If it does not, the seam
                        has drifted and that is the first thing to fix.
python3 prove.py        both ledgers conserve; six deliberate breaks all caught.
python3 coverage.py national     22 verified, 2 modelled, 2 unverified, 3 missing
python3 coverage.py dc            0 verified, 0 modelled, 15 unverified, 26 missing
python3 render_v4_1.py  both gates print. Whitespace flags pages 6, 9, 10, 15.
                        Figurefit clean. If only one gate prints, the `or`
                        short-circuit is back.
```

Look at `reference_renders/sheet_working.png` and `dc_2024_combined.png` before
writing a sentence about either. That is S-040.

`python3 synth.py none` and `python3 synth.py thin` regenerate the two synthetic
fixtures. They are working files. Do not commit their renders; `crossings.py`
reports them as orphans, correctly.

## Read

`EDITORIAL_CHARTER.md` first and completely. Then `ARCHITECTURE.md`. Then
`ACQUISITION.md`, which is new and is the process for populating a territory.
Then `MANIFEST_SESSION.md` from the 2026-09-15b entry. Then `NAIC_ROUTE.md`,
`STATE_PLAYBOOK.md`, `ENDNOTES.md`, `EDITORIAL_STANDING_NOTES.md`,
`STYLE_GUIDE.md`.

Where the brief and the charter disagree, the charter wins. Where the playbook
and the architecture disagree, raise it rather than picking one. The playbook's
standing default to build a per-state script is superseded by the seam; flag any
others.

## What this session is for

**First, close Phase 0.** The FY2030 to-be has to render through Ledger + View +
compose with byte-identical output. It is the last of the three. It is harder than
the other two because the HR-1 tributaries carry geometry as well as amounts:
`hr1_term`, the reach slots and `sa_hr1` sit half in `outflows.py`. Do not move
geometry to fix an arithmetic problem or the reverse.

Phase 0 closes when all three artifacts rebuild byte-identically, the endnote
register regenerates from the ledger, and `check` fails a ledger I deliberately
break. The first, third and fourth are done.

**Second, Phase 1 — the DC spine.** Retire `ledger_dc.py` and
`build_sankey_dc.py`. Re-acquire from CMS-64 / MACStats at current vintage, phase
by phase, in the order `ACQUISITION.md` sets out: cost allocation first, then the
scale and the peels, then the lanes, then the named plans, then the payer splits,
then the claims allocation. Do not jump to the interesting numbers.

`ledger_dc_2024.py` currently builds with `legacy_mix=True` inside `build.py`.
That flag is the visible record that DC still carries the national service mix.
Turning it off is a ledger correction and changes the panel; it is not layout.

Build the DC beneficiary pies. Row margin from DC's own service totals, column
margin from DC's own eligibility-group totals in MACStats Exhibit 21, seed from
the national cross-tab in Exhibit 18. Both margins are DC's; only the consumption
pattern is inherited. It goes in an endnote as a pattern assumption with both
margins named. My ruling, 15 September: some insight declared as an assumption
beats no insight.

Close the declared gaps in this order: behavioral health as its own provider node,
then the retention peels, then documented fraud. Do not close them with a national
share. Absent stays absent and gets declared on the artifact.

**Third, NAIC, once Sora's files are in hand.** Read Page 7, Analysis of
Operations by Lines of Business, Title XIX Medicaid column, for each of the four
entities: premium, incurred claims, administrative expense, net underwriting gain.
Check whether Alliance and ICP are booked in that column before aggregating.
Recover United's DC Medicaid wrap from Schedule T or declare it absent. Then tell
me the DC plan-level premium and gain with the exhibit named and the vintage
given. That closes the DC half of Pre-Phase 0.

If the NAIC result changes a number on the national panels, stop and tell me
before rendering anything.

## Verification

`verified` is strict: a person opened the source and agreed with the number. A
redline does not earn it. I signed the national FY2024 baseline on 15 September
on the strength of the endnote register, two redlines and a shipped draft. The
EN-43 earnings carve is deliberately left unsigned on both capitated lanes,
because EN-43 says in terms that the $0.76 has no primary source.

A signature attaches to a vintage and a value. Re-anchoring reports STALE; editing
a signed figure reports LAPSED and fails the build. Sign DC figures as you verify
them, one at a time, with the date and initials of whoever opened the source.

## Do not

Do not start Phase 2, the DC to-be. Do not start Phase 3, the payer zoom data.
Do not start Phase 4, the DC manuscript. Do not touch the national presentation
layer, meaning layout, typography and crops; a ledger correction is a different
thing. Do not re-propose the Typst port. Do not begin state two.

Four things are flagged and are not to be fixed without my say:
the tracker's State Admin marker holding both administration and Medicare
premiums under one label; column headings not coming from the View; the
tiny-payer label collision at $1.00 lane width; and the four whitespace
strandings.

If the work turns up a figure that is wrong or a label the ledger does not
support, stop and tell me. Do not fix it.

## House rules

The charter governs. Reader first. Never make the reader feel stupid or
overwhelmed. Cut anything whose real content is how rigorous we were. State the
positive figure before the decrement. Limits go in footnotes. No rhetorical
flourishes. American spelling. Phases, not columns. Ecosystem, not system. Never
"the Medicaid dollar" in body prose. A plan carries its present-day name with the
former name in parentheses.

Geometry drives arithmetic on the tracker line. Run the detector, not the eye.
Never fill a data gap with a share. Fix the wrong rule rather than clamping the
symptom. Verify that a gate executed, not just that it exited zero. A published
figure is measured; recomputing it from its parts substitutes our arithmetic for
the source's.

## Working style

Recommend on methodology, ask on direction. Lead with your view and the
reasoning. One question at a time, and wait. Show me the picture: any claim about
what a diagram looks like ships with the diagram or a crop with the thing
circled. When you present a file, check it is where you say it is.

A refactor this size wants batch edits. Apply and verify one change at a time,
match across line wrapping, never abort the run on one miss, print a per-edit
result. A batch reported as complete is not proven complete.

## At commit

Build the delete list from what is actually in the repo, not what is in your
working folder. `Medicaid_Dollars_National_DRAFT_v3.pdf`, `paper_national_v3.html`
and `render_v3.py` went on the list two commits ago and are still there; check
before adding anything. Working files stay out. Zip everything including
`reference_renders`, `paper_figs` and `paper_fonts`; omitting a directory makes
its contents look deleted in GitHub Desktop. Commit at session end, not
mid-session. Running manifest as we go. I use GitHub Desktop and I will not use
the terminal.

## Standing

The repo is public and the v4.1 draft is outside the firm. Both triggers on the
privacy reminder have fired and I have not ruled. Do not raise it again unless
I do.
