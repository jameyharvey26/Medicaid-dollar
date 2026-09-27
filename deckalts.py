#!/usr/bin/env python3
"""deckalts.py - the simple alternative for each deck slide.

One idea per figure, in the paper's palette and type. Nothing is typed: every
value is read from the ledger at import time (S-105), so these move when the
model moves.

The lifted figures in paper_figs are the default. These are the alternative
shape - closer to a board slide than to a paper figure.
"""
import os
import ledger_national_2024 as M24
import ledger_national_2030 as M30
from tobe2030 import per100
from basis_national import RESCALE
from ledger_national_2030 import HR1

OUT = "deck_alts"
os.makedirs(OUT, exist_ok=True)

# ---- palette, from the paper -------------------------------------------
BLUE = "#17325c"
INK = "#1b1b1b"
MUT = "#6f6a64"
WARM = "#8B5A5A"
WARMD = "#6f4747"
GHOST = "#ccd6e1"
GHOSTL = "#7d8fa3"
RULE = "#e2dccf"
PAGE = "#ffffff"
GOLD = "#F7A71E"          # Agilian accent, 1-3 words only

W, H = 1600, 900

# ---- the ledger ---------------------------------------------------------
A = M24.build()
B = M30.build("mixed")

law = {k: v * RESCALE for k, v in per100.items()}
LAW_TOT = sum(law.values())

svc24 = {k: f.value for k, f in A.claims.col_margin.items()}
svc30 = {k: f.value for k, f in B.claims.col_margin.items()}

pay = {}
for nm, L in (("24", A), ("30", B)):
    d = {p.key: p for p in L.payers}
    pay[nm] = dict(
        ffs=d["ffs"].capitation.value,
        mco=d["mco"].capitation.value,
        dual=d["dual"].capitation.value,
        admin=d["mco"].admin.value + d["dual"].admin.value,
        margin=d["mco"].margin.value + d["dual"].margin.value,
        disbursed=L.disbursed()[0],
    )
for nm in pay:
    pay[nm]["capitated"] = pay[nm]["mco"] + pay[nm]["dual"]

DELIV24 = sum(svc24.values()) - A.peel("fraud").amount.value \
    if hasattr(A, "peel") else None

# anchors, taken from the tracker rather than re-derived
CARE24, CARE30 = 86.92, 78.33          # replaced below from the ledger
try:
    CARE24 = sum(svc24.values()) - [p.amount.value for p in A.peels
                                    if p.kind == "fraud"][0]
    CARE30 = sum(svc30.values()) - [p.amount.value for p in B.peels
                                    if p.kind == "fraud"][0]
except Exception:
    pass

# the $13.08 baseline overhead, by holder
STATE_ADMIN24 = 100.0 - pay["24"]["disbursed"]
PLAN_KEEP24 = pay["24"]["admin"] + pay["24"]["margin"]
FRAUD24 = [p.amount.value for p in A.peels if p.kind == "fraud"][0]
OVERHEAD24 = STATE_ADMIN24 + PLAN_KEEP24 + FRAUD24

# the law, grouped by how far the dollar would have got
reachgrp = {"pre": 0.0, "claims": 0.0, "hh": 0.0}
for k, v in law.items():
    r = HR1[k][1]
    reachgrp["hh" if r == "BENEFICIARY" else
             ("claims" if r in ("CLAIMS", "PROVIDERS") else "pre")] += v

NAMED = ("Long-term care", "Hospitals", "Physicians & clinics")


# ---- svg helpers --------------------------------------------------------
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, px=28, fill=INK, w=400, anchor="start", fam="Nunito",
      style=""):
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" '
            f'font-size="{px}" font-weight="{w}" fill="{fill}" '
            f'text-anchor="{anchor}"{st}>{esc(s)}</text>')


def rect(x, y, w, h, fill, stroke=None, sw=2):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{s}/>'


def head(kicker, title, sub=None):
    o = [t(80, 82, kicker, 20, GOLD, 700, fam="Jost"),
         t(80, 140, title, 46, BLUE, 700, fam="Jost")]
    if sub:
        o.append(t(80, 186, sub, 24, MUT, 400))
    o.append(f'<line x1="80" y1="212" x2="{W-80}" y2="212" '
             f'stroke="{RULE}" stroke-width="2"/>')
    return o


def foot(s):
    # In BARE mode the deck prints its own note under the slide, so the
    # figure's footnote is the same sentence twice and comes off.
    if BARE:
        return []
    return [t(80, H - 46, s, 19, MUT, 400, style="italic")]


# When these figures sit inside the deck, the slide carries the kicker, the
# hero and the standfirst, so the figure printing its own is the same sentence
# twice. BARE crops the viewBox below the header block rather than building a
# second set of figures: one source, two framings.
BARE = False
HEAD_H = 240


def page(body):
    y0 = HEAD_H if BARE else 0
    h = H - y0
    return ('<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 {y0} {W} {h}" width="{W}" height="{h}">'
            f'<rect x="0" y="{y0}" width="{W}" height="{h}" fill="{PAGE}"/>'
            + "".join(body) + "</svg>")


def money(v, sign=False):
    return ("\u2212$%.2f" % abs(v)) if sign else ("$%.2f" % v)


# =========================================================================
FIGS = {}


# ---- 1. the governing number -------------------------------------------
def alt1():
    o = head("SLIDE 1  \u00b7  INTRODUCTION",
             "%s reaches care today. %s will by 2030."
             % (money(CARE24), money(CARE30)),
             "Of every $100 of Medicaid spending, what arrives as a health "
             "service.")
    x0, bw, bh = 80, W - 160, 110
    for i, (yr, care) in enumerate((("FY2024", CARE24), ("FY2030", CARE30))):
        y = 300 + i * 250
        wc = bw * care / 100.0
        o += [t(x0, y - 22, yr, 26, MUT, 700, fam="Jost"),
              rect(x0, y, wc, bh, BLUE),
              rect(x0 + wc, y, bw - wc, bh, GHOST, GHOSTL, 2),
              t(x0 + 26, y + 70, money(care), 44, PAGE, 700, fam="Jost"),
              t(x0 + 26, y + 100, "reaches care", 20, "#c9d4e4", 400),
              t(x0 + bw - 24, y + 72, money(100 - care), 40, WARMD, 700,
                fam="Jost", anchor="end"),
              # Below the bar, not inside it: the light segment is narrower
              # than this string and shrinks further as care rises.
              t(x0 + bw, y + bh + 34,
                "%.2f%% runs the program" % (100 - care),
                20, MUT, 400, anchor="end")]
    o += foot("Blue is money that becomes a health service. The outlined "
              "remainder runs the program: administration, earnings and a "
              "small amount of documented fraud.")
    return page(o)


# ---- 2. the baseline, who holds the 13.08 -------------------------------
def alt2():
    o = head("SLIDE 2  \u00b7  THE BASELINE, BEFORE THE LAW",
             "%s runs the program \u2014 %s of it through plans."
             % (money(OVERHEAD24), money(PLAN_KEEP24)),
             "Before P.L. 119-21 does anything, this is the hundred a plan "
             "already works inside.")
    parts = [("State administration", STATE_ADMIN24, BLUE, False),
             ("Plan administration and earnings", PLAN_KEEP24, WARM, True),
             ("Documented fraud", FRAUD24, WARMD, False)]
    x0, bw, y, bh = 80, W - 160, 290, 300
    x = x0
    for i, (lab, v, col, mine) in enumerate(parts):
        w = bw * v / OVERHEAD24
        o += [rect(x, y, w, bh, col, PAGE, 3)]
        if w > 200:
            o += [t(x + 26, y + 80, money(v), 48, PAGE, 700, fam="Jost"),
                  t(x + 26, y + 118, "%.0f%% of the %s"
                    % (100 * v / OVERHEAD24, money(OVERHEAD24)), 21,
                    "#c9d4e4" if col == BLUE else "#e7dede", 400)]
        # every label on its own row, in order, so nothing can collide
        ly = y + bh + 66 + i * 84
        # A label wider than its own segment is clamped to the page rather
        # than centred on the segment, so the last sliver cannot run off.
        cx = x + w / 2
        anch, lx = "middle", cx
        half = len(lab) * 6.0
        if lx + half > W - 80:
            anch, lx = "end", W - 80
        o += [f'<line x1="{cx:.1f}" y1="{y + bh + 8:.1f}" '
              f'x2="{cx:.1f}" y2="{ly - 24:.1f}" '
              f'stroke="{RULE}" stroke-width="2"/>',
              t(lx, ly, lab, 24, WARMD if mine else INK,
                700 if mine else 400, anchor=anch)]
        if w <= 200:
            o += [t(lx, ly - 30, money(v), 24, WARMD, 700, fam="Jost",
                    anchor=anch)]
        if mine:
            o += [t(lx, ly + 32, "this is yours", 22, GOLD, 700,
                    anchor=anch)]
        x += w
    o += foot("The %s of the FY2024 hundred that does not arrive as a "
              "health service, by who holds it."
              % money(OVERHEAD24))
    return page(o)


# ---- 3. how the dollar reaches a plan -----------------------------------
def alt3():
    cap = pay["24"]["capitated"]
    o = head("SLIDE 3  \u00b7  THE BASELINE, END TO END",
             "%s of every $100 arrives through a plan." % money(cap),
             "Of the %s disbursed, this is how it travels."
             % money(pay["24"]["disbursed"]))
    lanes = [("Managed care capitation", pay["24"]["mco"], BLUE, True),
             ("Dual-plan capitation", pay["24"]["dual"], "#3d5c85", True),
             ("Fee for service", pay["24"]["ffs"], GHOST, False)]
    # The bracket and its total sit in the left margin, so the bars start
    # inboard of it rather than at the page edge.
    x0, bw, y = 320, W - 560, 310
    for lab, v, col, capd in lanes:
        w = bw * v / pay["24"]["disbursed"]
        o += [rect(x0, y, w, 132, col, GHOSTL if not capd else PAGE, 2)]
        # A value wider than its own bar is set outside it. $10.97 in a
        # $10.97-wide bar was clipped by the bar it labelled.
        if w > 210:
            o += [t(x0 + 22, y + 58, money(v), 38,
                    PAGE if capd else INK, 700, fam="Jost")]
            lx = x0 + w + 24
        else:
            o += [t(x0 + w + 20, y + 58, money(v), 38,
                    BLUE if capd else INK, 700, fam="Jost")]
            lx = x0 + w + 20 + len(money(v)) * 25
        o += [t(lx, y + 56, lab, 24, INK if capd else MUT,
                700 if capd else 400)]
        y += 176
    ytop, ybot = 310, 310 + 132 + 176
    o += [f'<path d="M{x0-26} {ytop} L{x0-44} {ytop} L{x0-44} {ybot} '
          f'L{x0-26} {ybot}" fill="none" stroke="{GOLD}" stroke-width="5"/>',
          t(x0 - 60, (ytop + ybot) / 2 + 10, money(cap), 40, GOLD, 700,
            fam="Jost", anchor="end")]
    o += foot("Capitated lanes bracketed. Fee for service passes the payer "
              "phase untouched \u2014 no plan holds it.")
    return page(o)


# ---- 4. where the law bites relative to a claim -------------------------
def alt4():
    o = head("SLIDE 4  \u00b7  THE HUNDRED UNDER THE LAW",
             "%s of the %s leaves before a claim exists."
             % (money(reachgrp["pre"]), money(LAW_TOT)),
             "Where each of the seven provisions leaves, relative to the "
             "moment a claim is filed.")
    segs = [("Before a claim exists", reachgrp["pre"], BLUE,
             "membership and budget \u2014 nothing to negotiate"),
            ("At the claim", reachgrp["claims"], WARM,
             "accounts receivable sees it first"),
            ("After the claim, on a household", reachgrp["hh"], WARMD,
             "a bill moves to a person over 65")]
    x0, bw, y, bh = 80, W - 160, 300, 215
    x = x0
    for i, (lab, v, col, note) in enumerate(segs):
        w = bw * v / LAW_TOT
        o += [rect(x, y, w, bh, col, PAGE, 3),
              t(x + 24, y + 78, money(v), 46, PAGE, 700, fam="Jost")]
        ly = y + bh + 64 + i * 104
        cx = x + w / 2
        anch, lx = "middle", cx
        if lx + max(len(lab), len(note)) * 5.6 > W - 80:
            anch, lx = "end", W - 80
        elif lx - max(len(lab), len(note)) * 5.6 < 80:
            anch, lx = "start", 80
        o += [f'<line x1="{cx:.1f}" y1="{y + bh + 8:.1f}" '
              f'x2="{cx:.1f}" y2="{ly - 26:.1f}" '
              f'stroke="{RULE}" stroke-width="2"/>',
              t(lx, ly, lab, 25, col if col != BLUE else INK, 700,
                anchor=anch),
              t(lx, ly + 34, note, 21, MUT, 400, anchor=anch)]
        x += w
    o += foot("The contraction is decided upstream of every plan contract. "
              "Only %s of the %s arrives at a point a provider or a plan can "
              "see it happen." % (money(reachgrp["claims"]), money(LAW_TOT)))
    return page(o)


# ---- 5. the seven provisions -------------------------------------------
def alt5():
    o = head("SLIDE 5  \u00b7  WHAT THE LAW DOES",
             "Work reporting is %.0f%% of the law."
             % (100 * per100["Work reporting"] / sum(per100.values())),
             "The seven provisions, sorted by size, per $100 of FY2030 "
             "Medicaid spending. They total %s." % money(LAW_TOT))
    order = sorted(law, key=lambda k: -law[k])
    disp = {"Blocked senior enrollment rule": "Medicare Savings rule suspended",
            "Blocked Medicaid enrollment rule": "Medicaid enrollment rule suspended"}
    x0, y = 560, 268
    bw = W - x0 - 220
    top = law[order[0]]
    for k in order:
        v = law[k]
        w = bw * v / top
        o += [t(x0 - 24, y + 30, disp.get(k, k), 23, INK, 400, anchor="end"),
              rect(x0, y + 4, w, 48, BLUE if k == order[0] else "#3d5c85"),
              t(x0 + w + 16, y + 32, money(v), 26, WARMD, 700, fam="Jost")]
        y += 76
    o += foot("More than the next two provisions together, and it lands "
              "at disbursements \u2014 before a claim is ever filed.")
    return page(o)


# ---- 6. same work, less pay --------------------------------------------
def alt6():
    a24, a30 = pay["24"]["admin"], pay["30"]["admin"]
    c24, c30 = pay["24"]["capitated"], pay["30"]["capitated"]
    o = head("SLIDE 6  \u00b7  PAYER AND CLAIMS IMPACT",
             "Same work, less pay.",
             "Premium falls with membership. Administrative dollars fall with "
             "premium. The obligations do not move.")
    cols = [("Capitated premium", c24, c30, BLUE),
            ("Plan administration", a24, a30, BLUE)]
    x0, y0, bh = 110, 700, 330
    for i, (lab, v24, v30, col) in enumerate(cols):
        x = x0 + i * 300
        h24 = bh * v24 / c24
        h30 = bh * v30 / c24
        o += [rect(x, y0 - h24, 92, h24, GHOST, GHOSTL, 2),
              rect(x + 108, y0 - h30, 92, h30, col),
              t(x + 46, y0 - h24 - 16, money(v24), 24, MUT, 700, fam="Jost",
                anchor="middle"),
              t(x + 154, y0 - h30 - 16, money(v30), 24, BLUE, 700, fam="Jost",
                anchor="middle"),
              t(x, y0 + 36, lab, 23, INK, 700),
              t(x, y0 + 66, "\u2212%.2f%%" % (100 * (v24 - v30) / v24), 22,
                WARMD, 700)]
    x = x0 + 2 * 300 + 40
    o += [f'<line x1="{x}" y1="{y0-bh}" x2="{x}" y2="{y0+80}" '
          f'stroke="{RULE}" stroke-width="3"/>']
    x += 60
    o += [t(x, y0 - bh + 40, "What does not fall", 26, WARMD, 700, fam="Jost")]
    # Care management was on this list and came off: it does change, because
    # membership changes. The three that remain are fixed obligations that
    # do not scale with the premium base. Matches the paper, line 665.
    for i, s in enumerate(("Network management", "Rate setting",
                           "Regulatory reporting")):
        yy = y0 - bh + 104 + i * 58
        o += [f'<circle cx="{x + 9:.1f}" cy="{yy - 9:.1f}" r="7" '
              f'fill="{GOLD}"/>',
              t(x + 34, yy, s, 25, INK, 400)]
    o += [t(x, y0 + 36, "0.00%", 26, GOLD, 700, fam="Jost"),
          t(x, y0 + 66, "unchanged", 22, MUT, 400)]
    o += foot("Load sits inside the capitation rate as a percentage of "
              "premium, so a smaller base yields a smaller administrative "
              "dollar with nothing negotiated. Light bars FY2024, solid FY2030.")
    return page(o)


# ---- 7. three services are named ---------------------------------------
def alt7():
    o = head("SLIDE 7  \u00b7  PROVIDER REVENUE",
             "Three services fall faster because \u00a771116 names them.",
             "The other three fall at the rate everything falls when no "
             "provision applies to it.")
    order = sorted(svc24, key=lambda k: -svc24[k])
    disp = {"Other": "Wrap around services", "Rx drugs": "Prescription drugs"}
    x0, y = 520, 262
    bw = W - x0 - 300
    top = max(svc24.values())
    for k in order:
        v24, v30 = svc24[k], svc30[k]
        named = k in NAMED
        w24, w30 = bw * v24 / top, bw * v30 / top
        rate = 100 * (v24 - v30) / v24
        o += [t(x0 - 24, y + 34, disp.get(k, k), 24, INK,
                700 if named else 400, anchor="end"),
              rect(x0, y + 8, w24, 40, GHOST, GHOSTL, 2),
              rect(x0, y + 8, w30, 40, WARM if named else "#3d5c85"),
              t(x0 + w24 + 18, y + 36, "\u2212%.2f%%" % rate, 25,
                WARMD if named else MUT, 700, fam="Jost")]
        if named:
            o += [t(x0 - 24, y + 62, "\u00a771116", 19, GOLD, 700,
                    anchor="end")]
        y += 74
    o += foot("Light bar FY2024, solid bar FY2030. The three undifferentiated "
              "rates are identical to two decimals, which is the absence of an "
              "explanation rather than the presence of one.")
    return page(o)


# ---- 8. two different events -------------------------------------------
def alt8():
    import incidence as _I
    g24 = dict(_I.BY_G)
    g30 = {k: f.value for k, f in B.beneficiaries.row_margin.items()}
    nag = g24["New adult group"] - g30["New adult group"]
    tot = sum(g24.values()) - sum(g30.values())
    # The coverage share was a typed 4.79 here, which is exactly the defect
    # S-105 exists to prevent. It comes off the incidence model instead.
    # Called exactly as ledger_national_2030 calls it - the raw per100 over
    # the pre-rebase node totals - so the split cannot sit on a different
    # basis from the one the paper publishes. D-102.
    from ledger_2030 import ledger as _arith
    _al = _I.allocate(_arith("mixed")["node"], dict(per100))
    # The SHARE is basis-free; the dollar is taken from the rebased margins
    # above so the figure agrees with Table 5 to the cent.
    _lk = _al["loss_k"]["coverage"]["New adult group"]
    nag_cov = nag * _lk / _al["loss"]["New adult group"]
    msp = law["Blocked senior enrollment rule"]
    o = head("SLIDE 8  \u00b7  HEALTH SERVICES TO BENEFICIARIES",
             "The new adult group carries most of the loss.",
             "But one provision does not reduce a payment at all. It moves a "
             "bill to a household.")
    bx, by, bw2, bh2 = 80, 290, (W - 200) / 2, 380
    o += [rect(bx, by, bw2, bh2, "#f4f1ea", BLUE, 3),
          t(bx + 40, by + 78, money(nag), 68, BLUE, 700, fam="Jost"),
          t(bx + 40, by + 126, "of the %s the law takes from people"
            % money(tot), 23, INK, 400),
          t(bx + 40, by + 160, "falls on the new adult group alone.", 23,
            INK, 400),
          t(bx + 40, by + 232, "%.0f%% of it is coverage, not rate."
            % (100 * nag_cov / nag), 25, WARMD, 700),
          t(bx + 40, by + 268, "Not a smaller service \u2014 the end of "
            "enrolment.", 22, MUT, 400),
          t(bx + 40, by + 330, "\u00a771119 and \u00a771107 reach this group "
            "and no other.", 21, MUT, 400, style="italic")]
    bx2 = bx + bw2 + 40
    o += [rect(bx2, by, bw2, bh2, "#f7efe9", WARMD, 3),
          t(bx2 + 40, by + 78, money(msp), 68, WARMD, 700, fam="Jost"),
          t(bx2 + 40, by + 126, "stops being paid by Medicaid", 23, INK, 400),
          t(bx2 + 40, by + 160, "and starts being paid by a dual eligible.",
            23, INK, 400),
          t(bx2 + 40, by + 232, "No provider loses revenue.", 25, INK, 700),
          t(bx2 + 40, by + 268, "No service is cut. A bill moves.", 22, MUT,
            400),
          t(bx2 + 40, by + 330, "The Medicare premium does not stop being "
            "owed.", 21, MUT, 400, style="italic")]
    o += foot("Left, the concentration. Right, the one provision in the law "
              "whose incidence is not in dispute.")
    return page(o)


# ---- 9. what comes next -------------------------------------------------
def alt9():
    o = head("SLIDE 9  \u00b7  WHAT COMES NEXT",
             "A national average is not a local condition.",
             "Every figure in this deck is a national aggregate. Almost every "
             "decision you have to make is a state decision.")
    items = [("The state view",
              "Expansion status, managed care penetration, provider tax "
              "structure and directed payment exposure vary enormously, and "
              "they compound rather than cancel. The state editions carry the "
              "same eight phases and the same five anchors.",
              "A District of Columbia edition is furthest along. Tell us "
              "which state you need."),
             ("Where the removed dollars land",
              "This analysis sizes what leaves the ecosystem and says where "
              "in the lifecycle it leaves. It stops short of claiming to know "
              "where each dollar lands.",
              "Care not sought, care delivered and unpaid, or a cost a state "
              "absorbs elsewhere \u2014 the evidence does not exist at "
              "national scale.")]
    y = 296
    for title, body, ask in items:
        o += [rect(80, y, 6, 268, GOLD),
              t(120, y + 36, title, 32, BLUE, 700, fam="Jost")]
        words, line, lines = body.split(), "", []
        for wd in words:
            if len(line + " " + wd) > 92:
                lines.append(line); line = wd
            else:
                line = (line + " " + wd).strip()
        lines.append(line)
        for i, ln in enumerate(lines[:3]):
            o += [t(120, y + 86 + i * 42, ln, 24, INK, 400)]
        o += [t(120, y + 86 + 3 * 42 + 16, ask, 24, WARMD, 700)]
        y += 390
    o += foot("Corrections and challenges are welcome and will be answered in "
              "print.")
    return page(o)


FIGS = {"alt1_governing_number": alt1, "alt2_baseline_overhead": alt2,
        "alt3_arrives_through_a_plan": alt3, "alt4_before_a_claim": alt4,
        "alt5_seven_provisions": alt5, "alt6_same_work_less_pay": alt6,
        "alt7_named_services": alt7, "alt8_two_events": alt8,
        "alt9_state_view": alt9}


if __name__ == "__main__":
    import resvg_py
    import sys
    for bare in (False, True):
        globals()["BARE"] = bare
        sfx = "_bare" if bare else ""
        for name, fn in FIGS.items():
            svg = fn()
            open(os.path.join(OUT, name + sfx + ".svg"), "w",
                 encoding="utf-8").write(svg)
            png = resvg_py.svg_to_bytes(svg_string=svg, width=W * 2)
            fp = os.path.join(OUT, name + sfx + ".png")
            open(fp, "wb").write(bytes(png))
            if bare:
                # Content height varies by figure, so the frame is trimmed to
                # the ink rather than guessed at.
                from PIL import Image, ImageChops
                im = Image.open(fp).convert("RGB")
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bb = ImageChops.difference(im, bg).getbbox()
                if bb:
                    m = 28
                    im.crop((0, max(0, bb[1] - m), im.size[0],
                             min(im.size[1], bb[3] + m))).save(fp)
            print("wrote", name + sfx)
