# Questions for JW — in order, one at a time

Written 3 November 2026 by Claude, working without JW, against
`NEXT_SESSION_PROMPT_12.md`. The evidence behind every question is in
`DC_RESEARCH_2026-11-03.md`; bracketed numbers are its source register. The
data points that need a signature rather than a decision are in
`DC_SIGNOFF_LIST.md` and are not repeated here.

Each question states the options and a recommendation. Nothing has been
changed in the engine, the ledgers or the paper. Fourteen questions; the first
six are the ones that change what gets drawn.

---

## Q1 — The leftovers lane. Replace the placeholder with the three derived figures?

`DC_ENGINE_TODO` item 1, the one marked "worst one, fix first". CBO scored all
three named District provisions after all: §71108 at $195M, §71109 at $6.2B,
§71112 at $4.2B over ten years [2][3][4]. Applying the work-reporting
construction — national score as a rate, District denominator — gives, per
$100 of the FY2030 hundred: home equity **0.0030**, immigrant eligibility
**0.0533**, retroactive **0.0406**; together **0.097**, against the
placeholder's **1.0587**. RAND's independent allocation of the immigrant
provision to the District agrees with this derivation to within a tenth.

- **(a) Replace the lane with the three derived figures, drawn as three.**
- (b) Replace with one derived total, 0.097, labelled with the three.
- (c) Keep the placeholder and publish the derivation as a footnote.
- (d) Draw the lane as absence and publish the three in the text.

**Recommendation: (a).** The lane's label already names three provisions. Three
figures make the label true, and the lane stops being a national residual
wearing a District name. (b) loses the point that one of the three is
immaterial and one is ten times the other two. (c) keeps a number on the plate
that measures a different quantity, which is the defect. (d) throws away three
figures we can now defend.

**What (a) costs:** the lane goes from about a dollar to about a dime, so the
District's FY2030 total HR-1 effect falls by roughly one per $100 and the
panel changes shape visibly. I have not drawn it. Say yes and the picture
comes before any claim about it.

---

## Q2 — Which CBO document governs those three scores?

This has to be settled before Q1 is drawn, because the two candidates do not
reconcile.

The to-be ledger is struck on CBO's 28 October 2025 supplemental [1], which
publishes six named lanes and one "Other" at $60.1B and no section detail. The
three scores come from CBO's 21 July 2025 estimate [2]. Those six named lanes
match between the two documents to the tenth, so the vintages agree where they
overlap. But the unlisted Chapter 1 sections sum to roughly $137B against an
"Other" of $60.1B, and CBO publishes no decomposition of the difference —
interactions, re-estimation, or both.

- **(a) Draw the three on the 21 July figures and declare the reconciliation
  gap on the plate.**
- (b) Hold until the 61570 workbook is opened and the gap is understood.
- (c) Treat the three as a share of the $60.1B "Other" instead.

**Recommendation: (a), with (b) running in parallel.** The three sections are
separately scored quantities, not components of a residual, so (c) would
reintroduce exactly the allocation error the District panel exists to refuse.
The gap is real and belongs on the plate as a sentence, not as a reason to
wait. The workbook is one click for you and is blocked for me — see Q13.

---

## Q3 — How does a ten-year score become one fiscal year?

The three scores are ten-year totals. The lanes are drawn at FY2030. I spread
each total evenly over the years it is in force — seven for §71108 from
1 January 2028, nine for §71109 from 1 October 2026, eight for §71112 from
1 January 2027. **That even spread is the one modelled step this derivation
adds, and it is mine, not CBO's.**

- (a) Keep the even spread, declared.
- **(b) Use `phasein.py`'s ramp logic, the same machinery the seven national
  lanes already use, and derive the FY2030 position from the statutory steps.**
- (c) Publish the ten-year figure only and draw no FY2030 lane.

**Recommendation: (b).** The repo already has the apparatus for exactly this
and the national lanes all go through it; a second, simpler rule sitting beside
it is how two answers to one question get into a model. It is more work than
(a) and I have not done it, because the ramp for these three is not in
`phasein.py` yet and adding it is a change to shared code rather than to the
District panel.

---

## Q4 — The Urban Institute band. Does it become the District's work-reporting band?

The best find of the session. Urban's HIPSM run [7] carries a District row and
separates the two levers: six-month redeterminations at −7% / −13% / −13% and
work requirements, incremental, at −17% / −29% / −42% across high, medium and
low mitigation. The repo's `RATE_DEFAULT` of 21.4% sits just under Urban's
high-mitigation combined 24%; `RATE_BAND`'s upper end, New Hampshire at 40%,
sits just under Urban's medium at 42%.

- **(a) Adopt Urban's three scenarios as the band's ends and default, and
  demote Arkansas and New Hampshire to corroboration.**
- (b) Keep the CBO-implied default and add Urban's scenarios as marks inside
  the existing band.
- (c) Widen `RATE_BAND` to Urban's low scenario, 55%, and keep everything else.
- (d) Leave the band alone and cite Urban in the text.

**Recommendation: (a).** The present band's ends are two other jurisdictions'
experience; Urban's are a District row from a named model with a published
method, and they separate the two levers the panel draws separately. That is
strictly better evidence for the same shape. Arkansas and New Hampshire become
what they should always have been: two real-world observations that the band
brackets, rather than the band itself.

**But the denominators do not match, and that is the next question.**

---

## Q5 — Whose expansion population?

Urban's implied District expansion base is about **109,000**.
`tobe2030_dc.EXPANSION_AT_RISK` is **78,322** — childless adults 0–133% FPL,
January 2026, after the District's own cut. DHCF's own testimony says
**78,000** subject to the work requirement [9, p.17], which corroborates ours.
Urban's base looks pre-cut and probably includes expansion parents.

- (a) Rebase Urban's percentages onto 78,322 and declare the adjustment.
- **(b) Carry both denominators on the plate and let the band's ends keep
  Urban's, with the mismatch declared exactly as `RATE_BASIS_DIFFERS` declares
  the Arkansas one.**
- (c) Adopt Urban's 109,000 as the denominator throughout.
- (d) Write to Urban and ask what their District base is.

**Recommendation: (b) now, (d) in parallel.** Rebasing someone else's
percentage onto our denominator (a) silently converts their model's result
into ours, and the result would carry our label and their method. (c) throws
away a District count DHCF publishes and we have corroborated twice. The
project already has the vocabulary for an un-reconciled denominator and uses
it on the work-reporting band today; this is the same situation and should
look the same on the plate. (d) is a short email and would settle it.

---

## Q6 — The paperwork lane. Where does the default sit inside the band?

`DC_ENGINE_TODO` item 2 says no District figure for §71102 is derivable. There
is one, published monthly [13]: the District renews ex parte at **67–89%**
across the last eleven months against a national **47–51%**, about 1.6 times
the national rate. Section 71102 blocks a rule whose substance is ex parte
renewal and renewal alignment, so a jurisdiction already doing it voluntarily
has less to lose. **This is the seniors lane's argument, for the same reason,
on a different lane.**

The band's ends are clear: national rate at the top, zero at the bottom. The
default is yours.

- (a) Default at the national rate, band running down to zero. Conservative;
  overstates the District.
- **(b) Default at the national rate scaled by the inverse ex parte ratio
  (about 0.6 of it), band from the national rate down to zero.**
- (c) Default at the midpoint, band to zero.
- (d) Leave the lane ABSENT and publish the ex parte series as the argument.

**Recommendation: (b).** It is the only one of the four where the default is
derived from a District measurement rather than chosen, and the derivation is
one step with a stated basis — the same standard `MSP_MODELLED_STEP` meets.
The scaling is a claim about exposure and not about dollars, and the plate
has to say so.

**One warning that affects all four.** The ex parte rate falls from 89% in
October 2025 to 67% in March 2026 and sits at 70% in June. March 2026 is the
month DHCF's new MMIS went live. A band struck on FY2025 months is a different
band from one struck on FY2026 months, and the FY2026 months are the ones a
FY2030 panel should probably use.

---

## Q7 — The seniors lane. Where does the default sit between 19% and 50%?

`DC_ENGINE_TODO` item 3: the share of the District's QMB-only enrollees above
100% FPL turns the lane from an upper bound into a figure. DHCF holds it and
has not been asked. The band's ends, both published:

- **19%** — the national share of MSP enrolment in the above-100%-FPL tiers,
  SLMB-Plus plus SLMB-Only/QI [14]. What the District would look like above
  the floor if it enrolled there only as other states do.
- **about 50%** — the District's own Medicare income distribution up to 300%
  FPL [15], if participation were flat across the income range. It is not;
  take-up falls as income rises, so this is an upper end by construction.

- (a) Default at 19%, band up to 50%.
- (b) Default at the midpoint, about 34%.
- **(c) Default at 19%, band up to 50%, and name asking DHCF as the
  acquisition that closes it.**
- (d) Leave the lane as the upper bound it is today.

**Recommendation: (c).** 19% is the end with a mechanism behind it — it is
what the rest of the country actually does above the floor — and a default at
the end rather than in the middle says honestly that we do not know where
inside the band it sits. A midpoint (b) would be a point estimate wearing a
band's clothes.

---

## Q8 — `AFTER_THE_DEMO` §1. I think you were right and the reasoning was wrong in a specific way.

You said removing the violet `SERVICE MIX ASSUMED` headline from the national
panels was correct and that the argument against it was wrong, but could not
say why at the time. I have now read what the engine actually draws.

**What is true.** The national FY2024 panel's claims matrix has 18 cells: the
six fee-for-service cells are MEASURED and the twelve managed-care and dual
cells are MODELLED. `mix_assumed` is therefore true nationally, and the engine
does draw those cells — each provider bar is divided between lanes by
`M.P.cells[lane|name]`. So the mechanism in the original argument was right:
the national plate does draw a fitted interior.

**What was wrong.** The caption that was removed does not describe the national
panel's assumption. It reads `SERVICE MIX ASSUMED / national shape on District
dollars — not a DC measurement`. On a national panel the second line is
nonsense, and the first is the wrong claim: nationally the service TOTALS are
measured off Exhibit 17 and what is modelled is the division of each bar
BETWEEN PAYERS. Those are different statements. The engine's own question box
already says this correctly and says, in its own words, that it "is NOT
declared on the national plate".

**So the defect is that one flag carries two different claims.** The constant
is even named `MIX_BORROWED`, which is the DC claim; the national mix is not
borrowed, it is fitted. Your fourth candidate reason — that "assumed" is a
term of art meaning borrowed from another jurisdiction, and the flag is
mis-named rather than the drawing mis-declared — is the one that holds.

- **(a) Keep the removal and give the national panel its own declaration in
  its own words: service totals measured, payer split within each bar
  modelled.**
- (b) Keep the removal and leave the national panel undeclared, with the
  question box carrying it.
- (c) Restore a national caption with corrected wording and keep one flag.

**Recommendation: (a).** It keeps your instruction, fixes the real defect, and
stops the national plate drawing a fitted cross-tab as if it were measured.
`ask.js` then needs its text changed to match, because it currently asserts
that the thing is not declared.

---

## Q9 — The District's four-year plan: cross-check, or supersession?

`DC_ENGINE_TODO` item 6 is checked and the answer is negative. The Executive
Summary volume does not carry a District Medicaid trajectory, in the FY2026 or
the FY2027 edition [12], and it does not by design: the financial plan projects
by appropriation title, not by programme.

What it does carry is Human Support Services federal and private resources,
FY2027 to FY2030, implying about **2.0% a year**, against `PRIOR_LAW_CAGR` of
**5.27%**. DHCF's Federal Medicaid Payments are about 85% of that line. But
the FY2027 plan is post-enactment: it already carries the District's own
eligibility cut and the ACR limitation, so it is a to-be trajectory, not the
prior-law counterfactual the hundred needs.

- **(a) Keep `PRIOR_LAW_CAGR`; use the HSS series as a cross-check on the
  FY2030 TO-BE total and say what it shows.**
- (b) Replace `PRIOR_LAW_CAGR` with the HSS-implied rate.
- (c) Build a District prior-law rate from the FY2026 PROPOSED volume, which
  was transmitted 27 May 2025 and is pre-enactment.

**Recommendation: (a), and close `SUPERSEDED_BY`.** (b) would put a post-law
growth rate on a prior-law denominator, which breaks the one thing the
denominator is for. (c) is what `SUPERSEDED_BY` currently names, and the
negative finding above means it would give an appropriation-title series, not
a Medicaid one — the supersession note should be rewritten to say so rather
than left pointing at a document that does not contain what it promises. The
cross-check in (a) is genuinely interesting: the District's own post-law plan
grows its health federal resources at 2% while our prior-law counterfactual
grows at 5.3%, and the gap is roughly the size of the law.

---

## Q10 — The FY2030 zeros in the District's dedicated-tax table

The FY2027 Approved financial plan shows both hospital directed-payment
provider fee funds at **0** in FY2030, after step-downs in FY2029, and the
inpatient bed tax at 0 as well [12, Tables 2-3 and 3-16]. The Revenue chapter
of the same volume says the inpatient fee "is forecasted to remain flat at
$87.0 million level from FY 2026 through FY 2030". The District's own document
contradicts itself across two chapters. Table 3-16 labels the column "FY 2030
Certified Revenues", which suggests the zeros mean *not certified beyond
statutory authority* rather than *forecast to stop*.

- **(a) Treat the FY2030 zeros as non-certification, use the FY2029
  step-downs as the real signal, and footnote the contradiction.**
- (b) Treat the zeros as a forecast and draw the lane to zero at FY2030.
- (c) Ask the OCFO which reading is right.

**Recommendation: (a), with (c) as a short email.** Reading a certification
boundary as a forecast would put the District's hospital financing at zero in
the panel's own year on the strength of a table that another chapter
contradicts. The FY2029 step-downs — 86,985 to 78,286 and 35,185 to 29,540 —
are the part that looks like the ACR limitation arriving, and they are
checkable against DHCF's own testimony, which attributes a $169M FY2027 fall
to exactly that [10, p.6].

---

## Q11 — The §71109 status line says "preliminary injunction". On the evidence I can find, that is not true for the District.

`DC_NAMED_PROVISIONS` says the legal-immigrant provision is suspended by a
preliminary injunction pending federal litigation. The injunction I found is
*Neighborhood House v. HHS*, W.D. Wash., No. C26-3006 TSZ, 30 September 2026
[18]. It enjoins HHS as to **qualified noncitizen SSI recipients in
Washington**, statewide in Washington, and the court expressly declined to go
nationwide.

- **(a) Correct the status line to say the provision is in force in the
  District, with the Washington injunction named as the live litigation.**
- (b) Leave it as it is until the DHCF February 2026 advisory note it rests on
  is re-read.
- (c) Drop the status note entirely.

**Recommendation: (a), but you decide after checking what DHCF actually said.**
This is the one place where I am contradicting a note in the repo on the
strength of a search rather than a document in hand, and the original note
cites a DHCF advisory session I have not seen. If DHCF said something broader,
that is a fact about guidance rather than about an injunction, and the line
should say which it is.

---

## Q12 — A legal fact that moved five days ago

On 29 October 2026 Judge Stearns in the District of Massachusetts vacated
CMS's definition of "medically frail" in the work-requirement interim final
rule, said he would issue the permanent injunction the states requested, and
gave states a six-month stay on enforcing medical-frailty determinations [17].
Twenty-five states **and the District of Columbia** were plaintiffs. Whether
the relief is nationwide is not in the reporting I can reach, and I do not have
the docket.

The exempt share is one of the inputs to the work-reporting band, and its
largest single component is medical frailty.

- (a) Note it in the text and leave the band alone.
- **(b) Note it on the plate, as a dated line saying the exemption definition
  is in litigation and the band predates the ruling.**
- (c) Hold the work-reporting band until the ruling settles.

**Recommendation: (b).** The panel already declares what it does not know; a
quantity whose statutory definition changed last week is exactly that, and a
reader in a District meeting is likely to know about the case. (c) would stop
the work for something that may take a year.

---

## Q13 — An operational one. I cannot download anything.

Both shells available to me refuse outbound HTTPS to anything outside an
allowlist; `rand.org` and `cbo.gov` both answered `connect_rejected`. I worked
around it by driving the in-app browser's own PDF and spreadsheet readers,
which is how every document in this research was read — including a 402-page
budget volume and a ZIP annex. It works, but it leaves no local copy, which
means nothing I read can be re-opened by the next session or checked against.

- **(a) Allowlist the domains this project actually uses: cbo.gov, rand.org,
  urban.org, kff.org, macpac.gov, medicaid.gov, cms.gov, dhcf.dc.gov,
  cfo.dc.gov, dccouncil.gov, census.gov.**
- (b) You download the handful of documents that matter and drop them in the
  repo.
- (c) Leave it; the browser route works.

**Recommendation: (a), and (b) for the CBO workbook today.** The workbook at
[2] is the primary source for all three figures in Q1 and is the one document
the browser route could not reach.

---

## Q14 — Two items from `AFTER_THE_DEMO` I did not resolve

**§3, the geometry contract.** `GEOMETRY_CONTRACT.md` gives BENEFICIARY 420
units against PROVIDERS' 200; the engine crops to 200 and draws an 1820-unit
canvas. I have not touched it and have no view worth having without seeing
both renders side by side. **Question: do you want the paper to follow the
engine, or the engine declared an exception?** I would need to draw both
before saying anything.

**§4, the $2.90–$5.40 range.** I went looking for it deliberately and found
nothing: no CBO document, no secondary source, no state analysis using those
numbers for work reporting. On the evidence, `AFTER_THE_DEMO`'s conclusion
stands — it has no source in this repo and none outside it that I can find, and
it should stay out of the slider. **Question: do you remember where it came
from?** If it was a spike artifact, the note can be closed.
