# Next session — a draft FY2030 DC panel, fast

Pull fresh. `pip install resvg_py pymupdf --break-system-packages`, install
playwright chromium, then `python3 gates.py`. **Expect 18 green on your
machine.** If `renderproof` is red, that is the Google Fonts fallback and it
means your fonts are not resolving — chase that before anything else, because
every layout gate downstream of it is then measuring the wrong thing.

Read `MANIFEST_SESSION.md` from the bottom. The 29 October addendum is the
one that matters: the DC payer column was re-based on each plan's CY2024
Title XIX reporting, and the DC panel now carries an ASSUMED national service
mix. `DC_PROVENANCE.md` is generated — `python3 dc_provenance.py --write` —
and it is the thing I read before showing anyone the DC numbers.

Two gate expectations moved on 29 October and both are written down:
`coverage.py dc` is 21 unverified / 20 missing, and `teaching_register.json`
dc_2024 is 93 entries. Do not re-bless anything without a reason.

**Before you commit: the DC FY2024 blessed render is stale.** The data moved
and nobody re-blessed it from a machine where the fonts resolve.

    python3 renderproof.py --bless "DC payer column re-based on CY2024 Title XIX"

---

## What I want: a DRAFT FY2030 DC panel I can drive in a room. This week.

Four of the seven HR-1 lanes are already derived on District inputs —
work reporting $2.95, provider tax limits $1.95, directed payment caps $1.63,
six-month renewals $0.54 per $100. The panel builds today:

    python3 -c "import build; build.build_dc_2030()"

It writes to `drafts/`, outside the blessed register, on purpose.

### 1. The fast route, and I have already made this decision once

Three lanes carry no District figure and the panel draws them as absence. On
27 September D-109 pulled the national service mix off the DC FY2024 panel;
on 29 October I put it back as an explicit declared assumption, because for a
demo a drawn panel that says what it assumed beats a truthful blank.

**Do the same thing to the three absent FY2030 lanes.** Derive them from
`ledger_national_2030` the way `ledger_dc_2024._assumed_shares()` derives the
service mix from `ledger_national_2024` — in code, never typed, so they move
if the national model moves. Mark every one MODELLED, and draw ASSUMED on the
plate the way the FY2024 provider column now carries SERVICE MIX ASSUMED.

That unblocks the engine too, and that is the real prize: the engine cannot
show DC FY2030 at all right now, and the reason is not the data, it is that
the engine has no way to DRAW absence. Give the lanes assumed figures and the
engine can render the panel this week. Teaching it violet placeholders is the
right long-term fix and it is not what I need by Friday.

Keep the switch explicit and named — `assumed_levers`, parallel to
`assumed_mix` — so turning it off returns the honest absent panel. I want
both, and I want to be able to show the difference.

### 2. Section 71101 should be derived, not assumed

It already has a measured District denominator: QMB-only enrolment, 12,880 in
January 2026, rising while total Medicaid fell 24,000. It needs a rate, and
the rate route is the one we settled for work reporting — a band with the
CBO-implied rate as the declared default. Do that one properly rather than
folding it in with the assumed two.

### 3. Three plate defects on the draft panel, worst first

- **Absent levers draw as −$0.00.** `placeholders()` exists in
  `ledger_dc_2030.py` and the view is not calling it. A zero where we mean
  "we do not know" is the one substitution this whole panel exists to refuse,
  and it is currently on the plate. Fix this even if item 1 makes it moot for
  the default view, because the honest view has to be right too.
- The declarations column overruns the plate and collides with the Medicare
  Savings terminal and the tracker. It needs pagination, not a smaller font.
- "Medicare Savings rule suspended" overlaps the panel edge.

### 4. Then the engine

Point `engine_data_export.py` at `ledger_dc_2030` and add the `DC|2030` panel.
It is currently `None` with a comment explaining why. The explanatory card the
engine shows for that cell has been corrected and will need correcting again
once the panel exists.

---

## Open decisions I owe you an answer on. Ask me at the top of the session.

1. **The lane colour.** The plans now carry their reserved palette colours and
   the aggregate MCO lane is still teal — which is the LOCAL family colour, so
   an aggregate currently reads as a local plan. Claude's recommendation is to
   make the aggregate neutral. It is shared with the national panels, so it is
   not a DC-only change.
2. **The redistribution rule.** `ledger_dc_2030` rescales the held FY2024
   lanes proportionally onto the struck FY2030 disbursement, declared on the
   plate and applied only there. It is NOT a decision on the general rule, and
   the general rule is still open across all twelve peels.
3. **`audit_state_palette` does not implement its own swap rule.** It detects
   a collision and refuses; the documented behaviour is that the smaller plan
   shifts to its designated alternate. DC does not collide, so this is free
   today and bites on the first state that does.
4. **DHCF's FY2028 against the statute's FY2029** on the directed payment
   phase-down. One step is $48.5M. Worth putting to DHCF before publication.

## Standing, and raise these at close every session

- Nothing District is signed. **0 of 55 FY2024 figures and 0 of 67 FY2030
  figures are verified** — not one District figure is in `signatures.py`.
  Every demo carries the stipulation that the DC data is not proofread.
- HSCSN is on CY2023 while the other three plans are CY2024. It is not an MCO
  in the regulatory sense and files no comparable statement; it reports to
  DHCF and that figure has not been chased. One plan of four is a year behind.
- Acquisitions still open: the RAND annex Table 7 DC row (commercial price as
  a percentage of Medicare, which would give the §71116 termination year on
  District evidence), the Executive Summary volume of the FY2026 PROPOSED
  budget (the only place a District four-year Medicaid trajectory might be),
  DC's exempt share of expansion adults, and HSCSN's CY2024 Title XIX figures
  from DHCF.
- Early-reader feedback from 28 September is still parked: no "so what do we
  do", no cost-of-care context, the overhead band's weaponisation risk, and
  the missing deflator.
- The repo is public by my choice of 6 October. Ask me at close whether to
  re-privatise.

## How I work

One question at a time. Show me the picture before any layout claim.
Recommend on methodology, ask on direction — and when you ask, give me the
options and your recommendation, not a bare question. Derive in code, never
type an output. Commit at close, not mid-session. Challenge me if a request
does not make sense; I would rather be told no than agreed with.
