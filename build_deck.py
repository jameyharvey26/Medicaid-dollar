#!/usr/bin/env python3
"""build_deck.py - the MHPA board deck, one slide per white paper section.

The deck is a summary of the white paper and of the model underneath it, so
nothing here is typed. Every figure in the prose is an f-string off the same
ledger modules the paper and the panels read, and every image is produced by
deckalts.py at build time. Change the ledger and this file follows.

One slide per `h2` in paper_national_v7_1.html, in the paper's own order.
"""
import base64
import os

import deckalts as D
from deckalts import (CARE24, CARE30, OVERHEAD24, STATE_ADMIN24, PLAN_KEEP24,
                      FRAUD24, LAW_TOT, law, pay, svc24, svc30, reachgrp,
                      money, NAMED)
import incidence as _I
import landing
from ledger_2030 import ledger as _arith
from tobe2030 import per100

import release
OUT = "/mnt/user-data/outputs/MHPA_Board_Deck.html"
ALTS = "deck_alts"

# ---- derived prose figures ---------------------------------------------
g24 = dict(_I.BY_G)
g30 = {k: f.value for k, f in D.B.beneficiaries.row_margin.items()}
NAG = g24["New adult group"] - g30["New adult group"]
LOSS_PEOPLE = sum(g24.values()) - sum(g30.values())
_al = _I.allocate(_arith("mixed")["node"], dict(per100))
NAG_COV = NAG * _al["loss_k"]["coverage"]["New adult group"] \
    / _al["loss"]["New adult group"]
MSP = law["Blocked senior enrollment rule"]
WORK_PCT = 100 * per100["Work reporting"] / sum(per100.values())
CAP24, CAP30 = pay["24"]["capitated"], pay["30"]["capitated"]
ADM24, ADM30 = pay["24"]["admin"], pay["30"]["admin"]
CLAIMS24 = sum(svc24.values())
CLAIMS30 = sum(svc30.values())
PAYER_RATE = 100 * (CAP24 - CAP30) / CAP24
UNDIFF = 100 * (svc24["Rx drugs"] - svc30["Rx drugs"]) / svc24["Rx drugs"]
DISB24 = pay["24"]["disbursed"]


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


# The deck embeds the BARE renders: the slide carries the title, so the
# figure must not repeat it.
IMG = {f[:-9]: b64(os.path.join(ALTS, f))
       for f in os.listdir(ALTS) if f.endswith("_bare.png")}
IMG["cover_taper"] = b64("paper_figs/cover_taper.png")


def img(key, alt):
    return (f'<img src="data:image/png;base64,{IMG[key]}" alt="{alt}">')


# ---- slides -------------------------------------------------------------
SLIDES = []

# The cover is unnumbered; numbering starts on the contents page, which the
# page() assembly stamps as 1 before any slide() call runs.
_PAGE = [1]


def folio():
    _PAGE[0] += 1
    return (f'<p class="folio"><span>&copy; 2026 Agilian LLC &middot; '
            f'www.agilian.com</span><span>{_PAGE[0]}</span></p>')


# D-105. The explorer's fact cards are the deck's own lines. Taking them by
# re-typing would be two declarations of one sentence (S-096) and, worse, the
# deck's heroes are f-strings off the ledger while a transcription is not: the
# card would go on saying $87.07 after the ledger moved. So the parts are
# recorded here as they are formatted, and `explorer.py` reads CARDS.
# Nothing here changes what the deck renders.
CARDS = []


def slide(kicker, hero, body, figure=None, alt="", note=None, cls=""):
    f = f'<div class="fig">{img(figure, alt)}</div>' if figure else ""
    n = f'<p class="note">{note}</p>' if note else ""
    CARDS.append({"kicker": kicker, "hero": hero, "body": body,
                  "note": note or "", "figure": figure or "", "cls": cls})
    SLIDES.append(f'''<section class="slide {cls}">
  <p class="kicker">{kicker}</p>
  <h2>{hero}</h2>
  {f}
  <div class="body">{body}</div>
  {n}
  {folio()}
</section>''')


# 1
slide("Section 1 &middot; Introduction",
      f"{money(CARE24)} reaches care today.<br>{money(CARE30)} will by 2030.",
      f"<p>Of every $100 of Medicaid spending, {money(CARE24)} arrives as a "
      f"health service today. Under P.L. 119-21 that becomes {money(CARE30)}. "
      f"The rest runs the program: state and plan administration, Medicare "
      f"premiums returned to the federal government, retained earnings, and a "
      f"small amount of documented fraud.</p>"
      f"<p>Everyone in Medicaid has heard the national number. None of it "
      f"tells you what happens at your own position in the ecosystem. This "
      f"deck does, in one currency: dollars per $100.</p>",
      "alt1_governing_number", "The hundred, twice",
      note="Every figure is read from the model at build time. The ledger "
           "conserves to the cent in both years.")

# 2
slide("Section 2 &middot; The baseline, before the law",
      f"{money(OVERHEAD24)} runs the program &mdash; "
      f"{money(PLAN_KEEP24)} of it through plans.",
      f"<p>Before P.L. 119-21 does anything, this is the hundred a plan "
      f"already works inside. State and program administration takes "
      f"{money(STATE_ADMIN24)}. Plan administration and earnings is "
      f"{money(PLAN_KEEP24)}. Documented fraud is {money(FRAUD24)}.</p>"
      f"<p>This is the starting position every provision in the next eight "
      f"slides is applied to.</p>",
      "alt2_baseline_overhead", "Who holds the $13.08",
      note=f"FY2024 actuals. CMS-64 national totals and MACPAC MACStats, "
           f"February 2026.")

# 3
slide("Section 3 &middot; The national baseline, end to end",
      f"{money(CAP24)} of every $100 arrives through a plan.",
      f"<p>Of the {money(DISB24)} a state agency disburses, "
      f"{money(pay['24']['mco'])} is managed care capitation and "
      f"{money(pay['24']['dual'])} is dual-plan capitation. The remaining "
      f"{money(pay['24']['ffs'])} is fee for service, which passes the payer "
      f"phase untouched because no plan holds it.</p>"
      f"<p>A capitated dollar is committed the day the month starts. A "
      f"fee-for-service dollar is committed only when a claim is filed. That "
      f"is why an enrollment change and a rate change do not feel the same.</p>",
      "alt3_arrives_through_a_plan", "The three lanes",
      note="Dual-plan capitation is carved out because the plans are "
           "different, the populations are more expensive, and the law "
           "treats them differently.")

# 4
slide("Section 4 &middot; The hundred under the law",
      f"{money(reachgrp['pre'])} of the {money(LAW_TOT)} "
      f"leaves before a claim exists.",
      f"<p>Seven provisions remove {money(LAW_TOT)} per $100 by FY2030. "
      f"Where each one leaves decides who can do anything about it.</p>"
      f"<p>{money(reachgrp['pre'])} goes before a claim exists &mdash; "
      f"membership and budget, with nothing to negotiate. "
      f"{money(reachgrp['claims'])} leaves at the claim, which is what a "
      f"provider's accounts receivable sees first. "
      f"{money(reachgrp['hh'])} leaves after the claim, onto a household.</p>",
      "alt4_before_a_claim", "Where the law bites, relative to a claim",
      note="Measured at FY2030, where 62.6 percent of the ten-year effect is "
           "at full force and every provision has started. FY2030 will not be "
           "the worst year.")

# 5
slide("Section 5 &middot; What the law does",
      f"Work reporting is {WORK_PCT:.0f}% of the law.",
      f"<p>The seven provisions, sorted by size. Work reporting alone is "
      f"{money(law['Work reporting'])} of the {money(LAW_TOT)} &mdash; more "
      f"than the next two together &mdash; and it lands at disbursements, "
      f"before a claim is ever filed.</p>"
      f"<p>Each provision leaves at its own phase for its own reason. Work "
      f"reporting hits when a state stops disbursing for people who lose "
      f"coverage to paperwork. Directed payment caps hit only after a claim "
      f"is filed, which is why they land on a provider's books rather than a "
      f"state's budget.</p>",
      "alt5_seven_provisions", "The seven provisions",
      note="Plain-language names lead. Section numbers appear parenthetically "
           "at first use in the white paper.")

# 6
slide("Section 6 &middot; Payer and claims impact",
      "Same work, less pay.",
      f"<p>No provision in P.L. 119-21 addresses managed care directly. "
      f"Premium falls {PAYER_RATE:.2f} percent because fewer people are "
      f"enrolled. Plan administration falls with it, from {money(ADM24)} to "
      f"{money(ADM30)}, because load sits inside the capitation rate as a "
      f"percentage of premium. A smaller base yields a smaller "
      f"administrative dollar with nothing negotiated between payers and "
      f"states.</p>"
      f"<p>Network management, rate setting and regulatory reporting do not "
      f"shrink because membership does. Risk pool mix will shift, because "
      f"eligibility rules remove the members easiest to disenroll, not the "
      f"members most expensive to cover.</p>"
      f"<p>The claims phase is different in kind. Under prior law no money "
      f"left at claims. Under P.L. 119-21, {money(reachgrp['claims'])} "
      f"leaves here &mdash; the only money in the lifecycle removed after the "
      f"point where a service could already have been rendered.</p>",
      "alt6_same_work_less_pay", "Premium and administration, both falling",
      note="Where a plan holds directed payment arrangements the cap is an "
           "instruction to carry out, but the plan rather than the state has "
           "to renegotiate with providers.")

# 7
_named = ", ".join(sorted(NAMED, key=lambda k: -svc24[k])[:2]) \
    + " and " + sorted(NAMED, key=lambda k: -svc24[k])[2]
slide("Section 7 &middot; Provider revenue",
      "Three services fall faster because &sect;71116 names them.",
      f"<p>Long-term care, hospitals, and physicians and clinics carry the "
      f"directed payment cap on top of the general contraction, in proportion "
      f"to how much of each service arrives through a directed payment.</p>"
      f"<p>Wrap around services, behavioral health and prescription drugs "
      f"fall at {UNDIFF:.2f} percent. Three services landing on an identical "
      f"rate to two decimals is the absence of an explanation, not the "
      f"presence of one.</p>"
      f"<p>The rate is a national average. Actual exposure depends on a "
      f"state's expansion status, its managed care penetration, and an "
      f"organization's own payer mix and directed payment position. Two "
      f"hospitals in neighboring states can face materially different "
      f"outcomes from the same statute.</p>",
      "alt7_named_services", "Six services, two kinds of fall",
      note=f"The six services sum to claims paid: {money(CLAIMS24)} in "
           f"FY2024 and {money(CLAIMS30)} in FY2030.")

# 8
slide("Section 8 &middot; Health services to beneficiaries",
      "The new adult group carries most of the loss.<br>"
      "Dual eligibles are left holding an unpaid bill.",
      f"<p>Nothing else in the law is concentrated like this. "
      f"&sect;71119 and &sect;71107 name the population enrolled under "
      f"&sect;1902(a)(10)(A)(i)(VIII) and reach no other, which is why this "
      f"category moves by more than a quarter while every other category "
      f"moves by less than five percent.</p>"
      f"<p>Of the seven provisions, six reduce what somebody is paid. One "
      f"converts a Medicaid payment into a household obligation \u2014 the "
      f"clearest statement in the ledger of what \u201cremoved from "
      f"Medicaid\u201d can mean.</p>",
      "alt8_two_events", "Two different events",
      note="Coverage is somebody dropped and the whole of their care goes to "
           "zero. Rate is the same person, still enrolled, with their "
           "provider paid less. No individual loses a share of their own "
           "care.")

# 9
slide("Section 9 &middot; What comes next",
      "A national average is not a local condition.",
      "",
      "alt9_state_view", "What comes next",
      note="Corrections and challenges are welcome and will be answered in "
           "print.")

# 10
SLIDES.append(f'''<section class="slide closing">
  <p class="kicker">Section 10 &middot; Who wrote this &middot; Limits and sources</p>
  <h2>Every figure carries a source.</h2>
  <div class="cols">
    <div>
      <h3>Jamey Harvey</h3>
      <p class="role">Chief Executive Officer, Agilian LLC</p>
      <p>Jamey led the technology implementation of Obamacare for the District
      of Columbia and served as Deputy Chief Technology Officer for software
      and data for the District government before founding Agilian, a boutique
      firm helping Medicaid beneficiaries stay enrolled.</p>
      <h3 class="sub">How this was built</h3>
      <p>The diagrams are produced by a model the firm wrote. The ledger, the
      geometry and the balance line are code, and every figure in this deck is
      read from that code at build time rather than typed into the prose.
      Claude, made by Anthropic, was used throughout as an analyst and
      drafting partner. No figure was supplied from memory. What this analysis
      claims, and what it declines to claim, was decided by the named
      authors.</p>
    </div>
    <div>
      <h3 class="sub">Limits a board reader should know</h3>
      <ul>
        <li><b>Provider-level incidence beyond the three classes &sect;71116
        names.</b> Three of six services carry no service-specific finding,
        only an undifferentiated rate.</li>
        <li><b>The provider tax lane understates its size.</b> It blends two
        mechanisms without a gross-up to total computable dollars.</li>
        <li><b>Lever-to-node linkage is not shown.</b> A reader can see a
        service fall and cannot see which of the seven provisions did it.</li>
        <li><b>Where a removed dollar lands is not claimed.</b> Care not
        sought, care written off, care paid out of pocket, or a cost a state
        absorbs elsewhere &mdash; no national source splits those four.</li>
      </ul>
      <h3 class="sub">Sources</h3>
      <p>CBO Supplemental Cost Estimate for P.L. 119-21 Title VII Subtitle B
      Chapter 1, 28 October 2025, and the CBO letter of 5 March 2025 for the
      denominator. CMS-64 FY2024 national totals. MACPAC MACStats, February
      2026, Exhibits 16, 17, 18 and 21. P.L. 119-21 itself.</p>
    </div>
  </div>
  <p class="landing">The full white paper, visualization, and data model are
  accessible at <a href="{landing.URL}">{landing.URL}</a></p>
  {folio()}
</section>''')

# ---- appendix: the full model --------------------------------------------
# The deck argues in tapers because a board reader meets this cold. One
# Sankey at the back, for a reader who wants the whole ecosystem. Nothing
# under it but the address, so it cannot run to a second page.
_APX = "fig6_panel_2030"
IMG[_APX] = b64(f"paper_figs/{_APX}.png")
SLIDES.append(f'''<section class="slide appendix">
  <p class="kicker">Appendix One &middot; The full model, FY2030</p>
  <h2>$100 of Medicaid spending, FY2030.</h2>
  <div class="fig wide">{img(_APX, "National panel, FY2030")}</div>
  <p class="landing">The full white paper, visualization, and data model are
  accessible at <a href="{landing.URL}">{landing.URL}</a></p>
  {folio()}
</section>''')


# ---- page ---------------------------------------------------------------
CSS = """
/* Fixed-size slide boxes. A folio inside the flow rides onto the next
   printed page whenever its slide overspills, which is what put numbers at
   the top of empty pages. The box is the page now: content is clipped to it
   and the folio is anchored to it, so a number can only ever appear at the
   foot of the slide it belongs to. Overflow is caught by the fit check in
   build_deck.py rather than left to the printer. */
:root{
  --blue:#01215E; --paper-blue:#17325c; --ink:#1b1b1b; --mut:#6f6a64;
  --warm:#8B5A5A; --warmd:#6f4747; --gold:#F7A71E; --rule:#e2dccf;
  --page:#ffffff; --deck:#d9d5cc;
  --pw:11in; --ph:8.5in; --mx:0.72in; --mt:0.52in; --mb:0.40in;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:var(--deck);color:var(--ink);
  font-family:'Nunito',system-ui,sans-serif;}
/* D-116, JW 28 September. The stage was a fixed 11in wide with no horizontal
   padding, so on any viewport narrower than 1056px the slides ran to the very
   edge of the window with nothing around them. A slide is a sheet of paper and
   has to read as one, which means seeing space on both sides of it.
   `width:fit-content` lets the padding sit outside the sheet instead of eating
   into it, and the gutter is white rather than the deck grey so the eye reads
   it as margin rather than as more background. */
.stage{width:fit-content;max-width:100%;margin:0 auto;
  padding:30px 34px 60px;background:var(--page);}
/* A slide is 11in = 1056px wide and cannot reflow: the fit checks in this
   file measure it at that size and the figures are placed against it. So on a
   narrower window the sheet is SCALED rather than cropped, which keeps the
   gutter on both sides and means nobody has to scroll sideways to read a
   sentence. Stepped rather than a calc() so it behaves the same everywhere;
   `zoom` is used over `transform` because it reflows the page height with it
   and a transform would leave a column of dead space below the deck. */
@media (max-width:1180px){.stage{zoom:.92;}}
@media (max-width:1080px){.stage{zoom:.84;}}
@media (max-width:1000px){.stage{zoom:.76;}}
@media (max-width:900px){.stage{zoom:.66;}}
@media (max-width:780px){.stage{zoom:.56;}}
@media (max-width:640px){.stage{zoom:.44;padding:16px 14px 40px;}}
.slide{position:relative;width:var(--pw);height:var(--ph);overflow:hidden;
  background:var(--page);border:1px solid var(--rule);
  box-shadow:0 12px 28px rgba(20,25,35,.14);
  padding:var(--mt) var(--mx) calc(var(--mb) + 0.34in);margin:0 auto 26px;
  page-break-after:always;break-after:page;
  /* The figure absorbs the slack. Without this the leftover height pools at
     the foot of the slide and every page strands by an inch or two. */
  display:flex;flex-direction:column;}
.slide:last-of-type{page-break-after:auto;break-after:auto;}
.kicker{font-family:'Jost',sans-serif;font-size:12px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--gold);font-weight:700;margin:0 0 9px;}
h2{font-family:'Jost',sans-serif;font-weight:700;font-size:33px;line-height:1.1;
  color:var(--blue);margin:0 0 18px;}
h3{font-family:'Jost',sans-serif;font-size:19px;color:var(--blue);margin:0 0 3px;}
h3.sub{margin-top:20px;}
.role{font-size:12px;color:var(--warmd);font-weight:700;margin:0 0 8px;
  letter-spacing:.04em;}
.fig{flex:1 1 auto;min-height:0;margin:0 0 16px;
  border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);
  padding:14px 0;display:flex;align-items:center;justify-content:center;}
.fig img{max-width:100%;max-height:100%;width:auto;height:auto;display:block;}
.fig.wide{border:none;padding:4px 0 8px;}
.body{font-size:15px;line-height:1.55;flex:0 0 auto;}
.body p{margin:0 0 11px;}
.note{margin:14px 0 0;padding-top:11px;border-top:1px solid var(--rule);
  font-size:12.5px;font-style:italic;color:var(--mut);line-height:1.45;}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:34px;font-size:13.5px;
  line-height:1.5;flex:1 1 auto;align-content:start;}
.cols ul{margin:0;padding-left:17px;}
.cols li{margin-bottom:8px;}
.landing{margin:16px 0 0;padding:13px 17px;background:#f6f4ef;
  border-left:5px solid var(--gold);font-size:14.5px;line-height:1.5;}
.landing a{color:var(--blue);font-weight:700;word-break:break-all;}
/* anchored to the box, never to the flow */
.folio{position:absolute;left:var(--mx);right:var(--mx);bottom:var(--mb);
  display:flex;justify-content:space-between;align-items:baseline;
  margin:0;padding-top:9px;border-top:1px solid var(--rule);
  font-family:'Jost',sans-serif;font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--mut);}
.folio span:last-child{color:var(--blue);font-weight:700;font-size:13px;
  letter-spacing:0;}
/* cover */
.cover{padding:0;display:grid;grid-template-columns:1.05fr 1fr;
  align-items:stretch;}
.cover .left{padding:0 0.6in;display:flex;flex-direction:column;
  justify-content:center;}
.cover .right{padding:0.3in 0.35in;display:flex;align-items:center;
  justify-content:center;border-left:1px solid var(--rule);}
.cover .right img{max-height:7.6in;width:auto;max-width:100%;display:block;}
.wordmark{font-family:'Jost',sans-serif;font-size:13px;letter-spacing:.34em;
  color:var(--blue);font-weight:700;margin:0 0 5px;}
.project{font-family:'Jost',sans-serif;font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--mut);margin:0 0 24px;}
.cover h1{font-family:'Jost',sans-serif;font-size:46px;line-height:1.02;
  color:var(--blue);font-weight:700;margin:0 0 14px;}
.cover .sub{font-size:15.5px;color:var(--ink);line-height:1.5;margin:0 0 24px;}
.cover .rulebar{width:84px;height:5px;background:var(--gold);margin:0 0 22px;}
.cover .prepared{font-family:'Jost',sans-serif;font-size:12px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--warmd);
  font-weight:700;margin:0 0 5px;}
.cover .byline{font-size:13px;color:var(--mut);}
/* contents */
.toc ol{list-style:none;margin:0;padding:0;flex:1 1 auto;
  display:flex;flex-direction:column;justify-content:center;}
.toc li{display:flex;justify-content:space-between;gap:18px;
  border-bottom:1px solid var(--rule);padding:8px 0;font-size:15px;}
.toc li:last-child{border-bottom:none;}
.toc .n{color:var(--gold);font-weight:700;font-family:'Jost',sans-serif;
  margin-right:11px;}
.toc .idea{color:var(--mut);text-align:right;}
@page{size:11in 8.5in;margin:0;}
@media print{
  body{background:var(--page);}
  .stage{width:auto;padding:0;}
  .slide{border:none;box-shadow:none;margin:0;}
}
"""


TOC = [
    ("1", "Introduction",
     f"{money(CARE24)} reaches care today"),
    ("2", "The baseline, before the law",
     f"{money(OVERHEAD24)} runs the program"),
    ("3", "The national baseline, end to end",
     f"{money(CAP24)} arrives through a plan"),
    ("4", "The hundred under the law",
     f"{money(reachgrp['pre'])} leaves before a claim"),
    ("5", "What the law does",
     f"Work reporting is {WORK_PCT:.0f}% of it"),
    ("6", "Payer and claims impact", "Same work, less pay"),
    ("7", "Provider revenue", "Three services are named"),
    ("8", "Health services to beneficiaries", "A bill moves"),
    ("9", "What comes next", "A national average is not a local condition"),
    ("10", "Who wrote this &middot; Limits and sources", "Sources and limits"),
    ("A1", "The full model, FY2030", "The whole ecosystem, on one page"),
]

toc_rows = "\n".join(
    f'<li><span><span class="n">{n}</span>{t}</span>'
    f'<span class="idea">{i}</span></li>' for n, t, i in TOC)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$100 Medicaid Dollars &mdash; MHPA Board Edition</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="stage">

<section class="slide cover">
  <div class="left">
    <p class="wordmark">AGILIAN</p>
    <p class="project">The Medicaid Dollar Project</p>
    <div class="rulebar"></div>
    <h1>$100 Medicaid<br>Dollars</h1>
    <p class="sub">The national view, and what P.L.&nbsp;119-21 will do to it
    by fiscal year 2030. Every figure is dollars per $100 of Medicaid
    spending.</p>
    <p class="prepared">Prepared for the MHPA Board of Directors</p>
    <p class="byline">Jamey Harvey &middot; Agilian LLC</p>
  </div>
  <div class="right">{img('cover_taper', 'Where the money stops')}</div>
</section>

<section class="slide toc">
  <p class="kicker">Contents</p>
  <h2>Ten sections, one idea each.</h2>
  <ol>{toc_rows}</ol>
  <p class="folio"><span>&copy; 2026 Agilian LLC &middot; www.agilian.com</span><span>1</span></p>
</section>

{"".join(SLIDES)}

</div>
</body>
</html>
"""

if __name__ == "__main__":
    open(OUT, "w", encoding="utf-8").write(HTML)
    print("wrote", OUT, f"({len(HTML)//1024} KB)")
