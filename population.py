"""Who the law impacts. In the taper's language.

JW's note on page 14: take the information out of the pie charts and tell the
story from the point of view of children, adults, disabled people and the aged,
instead of a crop of six pies that the reader has to translate.

Five populations, not four. D-91 split the summed adult row into the new adult
group and other adults, and that split is the whole finding here: one category
carries almost two thirds of the loss and every other category is reached at
under five percent.

Each row reads in dollars off the hundred, as the households graphic does, and
each loss splits into coverage and rate. Coverage is somebody dropped and their
whole care goes to zero; rate is the same person, still enrolled, with their
provider paid less. They are different events and the picture should not merge
them.

The service strip on the right is FY2024 composition only - what that
population's dollars bought before the law. It carries the same weakness the
pies do: the interiors are IPF-fit from an uncited seed, which is declared in
the Limits register. Nothing here is a claim about which service a population
loses; note 13 says why that cube is not published.

Accessibility (Section 508 / WCAG 2.1 AA). Measured by contrast.py and printed
at build time. The coverage and rate segments differ in value as well as hue,
every figure is printed in text beside its bar, and the whole reads in
greyscale.

Every figure comes from inc.py. Nothing here is typed (S-105).
"""
import os
import contrast
import inc
import resvg_py
from inc import LOSS_G, BY_G, BY_G30, LOSS_G_K, D, S, G, DISP

BLUE = "#17325c"
WARM = "#8B5A5A"
WARMD = "#6f4747"
EDGE = "#5c3a3a"
INK = "#1b1b1b"
MUT = "#6f6a64"
BG = "#ffffff"
RULE = "#ded7c8"
GHOSTL = "#7d8fa3"
COV = "#8B5A5A"          # coverage: somebody dropped
RATE = "#c4a0a0"         # rate: the same person, paid for at less
RATEE = "#6f4747"        # its outline, because the fill alone is 2.4:1
ONBLUE = "#d9e2ee"
F = "Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif"

SVC_FILL = {"Long-term care": "#17325c", "Hospitals": "#3d6180",
            "Other": "#6f9bb0", "Physicians & clinics": "#9dbfcb",
            "Behavioral health": "#c3d7dd", "Rx drugs": "#e0ebee"}

PALETTE = contrast.PALETTE + [
    ("COV, coverage segment", COV, "object"),
    ("RATE, rate segment fill", RATE, "decoration"),
    ("RATEE, its outline", RATEE, "object"),
]

# Reading order: the category that carries the loss first, then the rest by
# how much reached them. The alphabet is not a finding.
ORDER = ["New adult group", "Disabled", "Aged", "Children", "Other adult"]
NOTE = {
    "New adult group": "\u00a771119 and \u00a771107 impact this group and no other",
    "Disabled": "rates, not enrolment: the directed payment cap and the contraction",
    "Aged": "and a $%.2f bill: the Medicare Savings rule suspended" % inc.MSP_BILL,
    "Children": "nothing in the law names children",
    "Other adult": "parents, caretakers, pregnancy \u2014 the work rule passes over them",
}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=14, fill=INK, a="start", w="normal", it=False, ls=0):
    st = ' font-style="italic"' if it else ""
    sp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{a}" font-weight="{w}"{st}{sp}>'
            f'{esc(s)}</text>')


PXMM = 11.7             # one scale for every custom graphic in this project
SPAN_MM, SLOT_MM = 250.0, 96.0
# The magnification is DERIVED, not chosen: the largest fall is made to fill
# the panel and the factor falls out of that. Typing it meant the new adult
# group's $5.48 ran off the end of the paper the first time this was drawn.


def px(pt):
    """Type size, in POINTS of printed page."""
    return round(pt / 72 * 25.4 * PXMM)


def mm(v):
    """A distance on the page, in MILLIMETRES."""
    return round(v * PXMM)


def wrap(s, size, budget):
    out, line = [], ""
    for word in str(s).split():
        trial = (line + " " + word).strip()
        if len(trial) * size * 0.52 > budget and line:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out


def build(masthead=False, furniture=False):
    """Five categories across the full measure, in two panels.

    JW: the decrement bars were not visible and it was not clear what the
    figure meant. They are not visible at the scale of the bar they come off:
    $0.29 against $25.16 is a millimetre of paper. Drawing them larger on the
    same axis would be a lie about the arithmetic, so the fall gets its OWN
    panel at five times the scale, said out loud on the figure, with each
    segment's amount printed against it and a rule joining the two panels so a
    reader can see which piece of which bar has been enlarged.
    """
    W = mm(SPAN_MM)
    M = mm(4)
    left, right = M, W - M
    top = mm(26) if furniture else mm(9)

    GUT = mm(46)                         # the category label gutter
    X0 = left + GUT
    SPLIT = left + mm(150)               # where the magnified panel starts
    BARW = SPLIT - X0 - mm(26)
    K = BARW / max(BY_G.values())
    PANW = right - SPLIT - mm(2)
    MAG = int((PANW / max(LOSS_G.values())) / K)     # whole multiples only
    MK = K * MAG
    ROW = mm(17.6)
    b = []

    b.append(t(X0, top - mm(3.4), "WHAT IMPACTED THEM, PER $100", px(6.6), INK,
               w="bold", ls=1.1))
    b.append(t(SPLIT, top - mm(3.4),
               f"THE FALL, AT {MAG}\u00d7 THE SCALE", px(7.2), WARMD,
               w="bold", ls=1.1))
    # JW: a colour legend. The two segments are named in text beside every bar
    # as well, so the key is a convenience rather than the only way in - 1.4.1.
    _kx = SPLIT + mm(46)
    for _lab, _fill, _edge in (("coverage", COV, EDGE), ("rate", RATE, RATEE)):
        b.append(f'<rect x="{_kx:.1f}" y="{top-mm(6.4):.1f}" width="{mm(4)}" '
                 f'height="{mm(3.4)}" fill="{_fill}" stroke="{_edge}" '
                 f'stroke-width="{mm(0.35):.1f}"/>')
        b.append(t(_kx + mm(5.4), top - mm(3.6), _lab, px(7.6), INK))
        _kx += mm(24)
    b.append(f'<line x1="{SPLIT-mm(5)}" y1="{top-mm(7)}" x2="{SPLIT-mm(5)}" '
             f'y2="{top+ROW*len(ORDER)-mm(3)}" stroke="{RULE}" '
             f'stroke-width="{mm(0.4):.1f}"/>')

    y = top + mm(10)
    for g in ORDER:
        cov, rat = LOSS_G_K["coverage"][g], LOSS_G_K["rate"][g]
        h = mm(7)
        yb = y - mm(4.4)

        b.append(t(X0 - mm(3), y - mm(0.6), g, px(11), INK, "end", "bold"))
        ny = y + mm(3.2)
        for ln in wrap(NOTE[g], px(6.6), GUT - mm(4)):
            b.append(t(X0 - mm(3), ny, ln, px(7.2), MUT, "end", it=True))
            ny += mm(3)

        # Panel one: what reached them. The whole FY2024 bar, with the FY2030
        # remainder solid and the fall left as an outline at true scale, so
        # the reader can see how small it is before it is enlarged.
        b.append(f'<rect x="{X0:.1f}" y="{yb:.1f}" width="{BY_G[g]*K:.1f}" '
                 f'height="{h}" fill="none" stroke="{GHOSTL}" '
                 f'stroke-width="{mm(0.4):.1f}"/>')
        b.append(f'<rect x="{X0:.1f}" y="{yb:.1f}" width="{BY_G30[g]*K:.1f}" '
                 f'height="{h}" fill="{BLUE}"/>')
        b.append(t(X0 + mm(2), y - mm(0.2), f"${BY_G30[g]:.2f}", px(10.5),
                   "#ffffff", w="bold"))
        # Right-aligned in its own column, not hung off the end of the bar:
        # the longest bar put this text on top of the panel divider.
        b.append(t(SPLIT - mm(5), y - mm(0.2), f"of ${BY_G[g]:.2f}", px(8),
                   MUT, "end"))

        # The join: from the end of the FY2030 bar, where the fall begins, to
        # the magnified panel.
        b.append(f'<path d="M{X0+BY_G30[g]*K:.1f},{yb+h+mm(1):.1f} '
                 f'L{SPLIT-mm(3):.1f},{yb+h+mm(1):.1f} L{SPLIT:.1f},{yb:.1f}" '
                 f'fill="none" stroke="{GHOSTL}" stroke-width="{mm(0.3):.1f}" '
                 f'stroke-dasharray="{mm(1)},{mm(1)}"/>')

        # Panel two: the same fall, enlarged, split and labelled. The two
        # amounts sit on two different lines with a tick down to the segment
        # each belongs to. Centred on one line they overlapped on every row
        # but the first, because a $0.15 segment is narrower than the text
        # that names it.
        wc, wr = cov * MK, rat * MK
        b.append(f'<rect x="{SPLIT:.1f}" y="{yb:.1f}" width="{wc:.1f}" '
                 f'height="{h}" fill="{COV}" stroke="{EDGE}" '
                 f'stroke-width="{mm(0.4):.1f}"/>')
        b.append(f'<rect x="{SPLIT+wc:.1f}" y="{yb:.1f}" width="{wr:.1f}" '
                 f'height="{h}" fill="{RATE}" stroke="{RATEE}" '
                 f'stroke-width="{mm(0.4):.1f}"/>')
        # Coverage is labelled ABOVE its segment and rate BELOW its own, so
        # neither leader has to cross the other's text. Staggering them both
        # underneath meant the rate leader ran straight through the coverage
        # label, whichever offsets were used: the two segments sit side by
        # side and their labels cannot both go down without meeting.
        for k, (x0, wseg, amt, lab) in enumerate(
                ((SPLIT, wc, cov, "coverage"), (SPLIT + wc, wr, rat, "rate"))):
            cxm = x0 + wseg / 2
            up = (k == 0)
            _txt = f"\u2212${amt:.2f}  {lab}"
            _w = len(_txt) * px(8) * 0.52
            tx = min(max(cxm + mm(2), SPLIT), right - _w)
            ty = yb - mm(2.2) if up else yb + h + mm(5)
            y0l = yb if up else yb + h
            y1l = ty + mm(1) if up else ty - mm(2.6)
            b.append(f'<path d="M{cxm:.1f},{y0l:.1f} L{cxm:.1f},{y1l:.1f} '
                     f'L{tx-mm(0.8):.1f},{y1l:.1f}" fill="none" '
                     f'stroke="{RATEE}" stroke-width="{mm(0.3):.1f}"/>')
            b.append(t(tx, ty, _txt, px(8), WARMD, "start",
                       "bold" if up else "normal"))
        y += ROW

    ky = y + mm(1)
    b.append(t(left, ky, "Coverage is somebody dropped: they are no longer "
                         "enrolled and the whole of their care goes to zero.",
               px(7.5), INK))
    b.append(t(left, ky + mm(4.2), "Rate is the same person, still enrolled, "
                                   "with their provider paid less. No "
                                   "individual loses a share of their own "
                                   "care.", px(7.5), INK))
    b.append(t(SPLIT, ky, f"The right-hand panel is drawn at {MAG} times the "
                          f"scale of the left.", px(7.5), WARMD, w="bold"))

    y = ky + mm(7)

    head = foot = ""
    if furniture:
        mast = (t(M, mm(7), "AGILIAN", px(7), BLUE, w="bold", ls=2.4)
                + t(M, mm(11), "THE MEDICAID DOLLAR PROJECT", px(7), MUT,
                    ls=1.5)) if masthead else ""
        head = (mast
                + t(M, mm(19), "Who the law impacts", px(17), INK, w="bold")
                + t(M, mm(23.5), "Dollars off the hundred, by eligibility "
                                 "category", px(8.5), MUT)
                + f'<line x1="{M}" y1="{mm(25.5)}" x2="{W-M}" y2="{mm(25.5)}" '
                  f'stroke="{RULE}" stroke-width="{mm(0.4):.1f}"/>')
        fy = y + mm(2)
        foot = (f'<line x1="{M}" y1="{fy:.1f}" x2="{W-M}" y2="{fy:.1f}" '
                f'stroke="{RULE}" stroke-width="{mm(0.4):.1f}"/>'
                + t(M, fy + mm(5),
                    f"${sum(LOSS_G_K['coverage'].values()):.2f} of the fall is "
                    f"coverage and ${sum(LOSS_G_K['rate'].values()):.2f} is "
                    f"rate.", px(7.5), INK))
        y = fy + mm(8)

    H = round(spec_h) if (spec_h := globals().get("_TRIM_H")) else round(y + mm(3))

    desc = ("Who the law impacts. Five eligibility categories. The left panel "
            "shows what impacted each one per $100 of Medicaid spending, with "
            "the FY2030 remainder solid inside the FY2024 outline. The right "
            f"panel shows the fall for each, at {MAG} times the scale, split "
            "into coverage and rate. " + " ".join(
        f"{g}: ${BY_G[g]:.2f} in FY2024 and ${BY_G30[g]:.2f} in FY2030, of "
        f"which ${LOSS_G_K['coverage'][g]:.2f} of the fall is coverage and "
        f"${LOSS_G_K['rate'][g]:.2f} is rate." for g in ORDER)
        + " Composition by service is in Figure 4; the loss is not divided by "
          "service anywhere in this paper.")

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'role="img" aria-labelledby="pt pd">'
           f'<title id="pt">Who the law impacts</title>'
           f'<desc id="pd">{esc(desc)}</desc>'
           f'<rect width="{W}" height="{H}" fill="{BG}"/>'
           + head + "".join(b) + foot + "</svg>")
    return svg, desc, y, H


if __name__ == "__main__":
    os.makedirs("cover", exist_ok=True)
    for name, mast, furn in (("fig9_population", False, False),
                             ("fig9_population_standalone", True, True)):
        svg, desc, deep, H = build(masthead=mast, furniture=furn)
        if deep > H - mm(2):
            raise SystemExit(f"{name}: content reaches {deep:.0f} of {H}px. "
                             f"Simplify it; do not shrink the type.")
        open(f"cover/{name}.svg", "w").write(svg)
        open(f"cover/{name}_alt.txt", "w").write(desc + "\n")
        open(f"cover/{name}.png", "wb").write(
            bytes(resvg_py.svg_to_bytes(svg_string=svg,
                                        width=round(SPAN_MM * 300 / 25.4))))
        print(f"wrote cover/{name}.png  {SPAN_MM:.0f} x {H/PXMM:.0f}mm, "
              f"content ends {deep:.0f} of {H}px")
    print("\n  contrast, measured against the page:")
    w = contrast.report(PALETTE)
    print(f"\n  worst meaningful element {w[0]} at {w[1]:.2f}:1")
