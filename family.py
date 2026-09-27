"""Two households, and what P.L. 119-21 reaches in each.

A declared thought exercise. Every figure is read from inc.py, which allocates
each provision to the population the statute names and then across services by
that population's own measured FY2024 consumption. The households are
composites, not cases: nothing here is a family anyone has met.

D-92, three changes from v6.1.

The households are identical except for the disability and the grandmother.
Same parent ages, same children's ages. Anything that differs between the two
columns is therefore the law reaching a difference in the household, not a
difference in how the household was drawn.

Everything is in dollars and cents off the hundred rather than in rates. In
2024 this much of every $100 of Medicaid spending reached people like them; in
2030 this much will. A rate invites a reader to apply it to one person's care,
and it does not mean that.

Each loss splits into coverage and rate. No individual loses a percentage of
their own care - they keep it or they go to zero. Coverage is somebody dropped.
Rate is the same person, still enrolled, with their provider paid less. The two
are different events and a household feels them differently.

Accessibility (Section 508 / WCAG 2.1 AA). The eligibility-category fills are
decoration and never the carrier: every figure is labelled in text and its
category name is printed. Outlines and all type are drawn in the darkened
variants. contrast.py prints the measured ratios.
"""
import inc, resvg_py, os
from inc import (cube, cube_k, D, G, S, BY_G, BY_G30, LOSS_G, LOSS_G_K,
                 per_prov, DISP, MSP_BILL)

# The caregiver exclusion, and what it is worth. Sec. 71119 and Sec. 71107
# reach the new adult group only, so the exemption only has anything to bite
# on there. An exempt parent still carries everything else the law does.
_EXEMPT_OF = ("Work reporting", "Six-month renewals")
NAG = "New adult group"
EXEMPT_REL = sum(v for n, (_, _, cell) in per_prov.items() if n in _EXEMPT_OF
                 for (s, g), v in cell.items() if g == NAG)
ADULT_2030_EXEMPT = BY_G30[NAG] + EXEMPT_REL
ADULT_2030_FULL = BY_G30[NAG]
EXEMPT_COV = LOSS_G_K["coverage"][NAG] - EXEMPT_REL

# Medicare Savings Program, 2026 amounts. What the suspended rule would have paid.
PART_B_MO, PART_B_DED, PART_A_DED = 202.90, 283.0, 1736.0
PART_B_YR = PART_B_MO * 12

# Wider than tall enough to fill the text column at the height the page can
# give it. At 1500 x 1160 the figure was 1.29 to 1, so bounding it to 148mm of
# page height left 59mm of empty paper beside it and whitespace.py flagged the
# gap. 1.64 to 1 fills the measure.
PXMM = 11.7             # one scale for every custom graphic in this project
COL_MM, SLOT_MM = 118.0, 87.2

BLUE, WARM, WARMD, EDGE = "#17325c", "#8B5A5A", "#6f4747", "#5c3a3a"
INK, MUT, BG, RULE = "#1b1b1b", "#6f6a64", "#ffffff", "#ded7c8"
PAPER = "#f5f2ea"
FILL = {"Children": "#6fa382", "New adult group": "#d8a24a",
        "Other adult": "#efd39a", "Disabled": "#cf7d4f", "Aged": "#6f6f9e"}
DARK = {"Children": "#3f6f53", "New adult group": "#8a6316",
        "Other adult": "#8a6316", "Disabled": "#8c4a22", "Aged": "#4b4b73"}
F = "Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif"


def px(pt):
    """Type size, in POINTS of printed page."""
    return round(pt / 72 * 25.4 * PXMM)


def mm(v):
    """A distance on the page, in MILLIMETRES."""
    return round(v * PXMM)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=14, fill=INK, a="start", w="normal", it=False, ls=0):
    st = ' font-style="italic"' if it else ""
    sp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{a}" font-weight="{w}"{st}{sp}>'
            f'{esc(s)}</text>')


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


def person(x, y, g, r):
    """Head and shoulders. Fill is decoration; the outline carries the shape."""
    hy = y - r * 2.2
    return (f'<circle cx="{x:.1f}" cy="{hy:.1f}" r="{r:.1f}" fill="{FILL[g]}" '
            f'stroke="{DARK[g]}" stroke-width="{mm(0.4):.1f}"/>'
            f'<path d="M{x-r*1.75:.1f},{y+r*1.2:.1f} a{r*1.75:.1f},{r*2:.1f} '
            f'0 0 1 {r*3.5:.1f},0 Z" fill="{FILL[g]}" stroke="{DARK[g]}" '
            f'stroke-width="{mm(0.4):.1f}"/>')


def _p(label, g, note, y2030=None, cov=None):
    """One person. cov overrides the coverage component when a statutory
    exemption removes part of it. The rate component never moves: an exemption
    from a work rule does not change what a provider is paid."""
    d30 = BY_G30[g] if y2030 is None else y2030
    c = LOSS_G_K["coverage"][g] if cov is None else cov
    return (label, g, d30, note, c, LOSS_G_K["rate"][g])


A = dict(
    key="fig13_household_a",
    title="A family of four",
    sub="No one disabled. Children 15 and 11.",
    people=[
        _p("Parent, 38", NAG, "exempt as a caregiver \u2014 until 2029",
           ADULT_2030_EXEMPT, EXEMPT_COV),
        _p("Parent, 36", NAG, "exempt as a caregiver \u2014 until 2029",
           ADULT_2030_EXEMPT, EXEMPT_COV),
        _p("Child, 15", "Children", "nothing in the law names children"),
        _p("Child, 11", "Children", "the exemption rests on this birthday"),
    ],
    hinge=("The exemption expires on a birthday.",
           "The younger child turns 14 in 2029 and both parents move to the "
           "80-hour standard inside the window this paper covers. What reaches "
           f"people like them falls from ${ADULT_2030_EXEMPT:.2f} to "
           f"${ADULT_2030_FULL:.2f} of every hundred, and almost all of that "
           "second step is coverage."))

B = dict(
    key="fig14_household_b",
    title="The same household, twice different",
    sub="One child disabled. A dual-eligible grandmother at home.",
    people=[
        _p("Parent, 38", NAG, "exempt as a caregiver \u2014 permanently",
           ADULT_2030_EXEMPT, EXEMPT_COV),
        _p("Parent, 36", NAG, "exempt as a caregiver \u2014 permanently",
           ADULT_2030_EXEMPT, EXEMPT_COV),
        _p("Child, 15", "Children", "nothing in the law names children"),
        _p("Child, 11 \u00b7 disabled", "Disabled",
           "long-term care and behavioral health"),
        _p("Grandmother, 74 \u00b7 dual", "Aged",
           "nursing facility care, and a bill"),
    ],
    hinge=("The exemption never expires. The bill arrives anyway.",
           "Caring for a disabled dependent carries no age ceiling, so the "
           "work rule passes over this household for good. What reaches it "
           f"instead is a transfer: ${MSP_BILL:.2f} of every hundred stops "
           "being a Medicaid payment and becomes the grandmother's own "
           "Medicare bill."))


def build(d, masthead=False, furniture=False):
    """One household, in one column of the two-column grid.

    JW: the pair was squeezed into a single landscape graphic and the people
    came out flattened. They are two figures now, each the width of the column
    it sits in, and the reasoning that was crammed into the picture is prose
    beside it, where a reader can read it.
    """
    W = mm(COL_MM)
    M = mm(3)
    left, right = M, W - M
    top = mm(24) if furniture else mm(2)
    b = []

    b.append(t(left, top + mm(4), d["title"], px(10.5), BLUE, w="bold"))
    b.append(t(left, top + mm(8), d["sub"], px(6.6), MUT, it=True))

    y = top + mm(15)
    for name, g, d30, note, cov, rat in d["people"]:
        b.append(person(left + mm(2.6), y + mm(1.2), g, mm(1.8)))
        b.append(t(left + mm(7), y, name, px(8), INK, w="bold"))
        b.append(t(right, y, f"${BY_G[g]:.2f} \u2192 ${d30:.2f}", px(8.5),
                   BLUE, "end", "bold"))
        b.append(t(left + mm(7), y + mm(3.2), note, px(6.2), MUT, it=True))
        b.append(t(right, y + mm(3.2),
                   f"\u2212${cov:.2f} coverage \u00b7 \u2212${rat:.2f} rate",
                   px(6.2), WARMD, "end"))
        b.append(f'<line x1="{left}" y1="{y+mm(4.9):.1f}" x2="{right}" '
                 f'y2="{y+mm(4.9):.1f}" stroke="{RULE}" '
                 f'stroke-width="{mm(0.25):.1f}"/>')
        y += mm(8.6)

    y += mm(2)
    lines = wrap(d["hinge"][1], px(6.6), W - mm(11))
    bh = mm(6.4) + len(lines) * mm(3.1)
    b.append(f'<rect x="{left}" y="{y-mm(3.4):.1f}" width="{right-left}" '
             f'height="{bh:.1f}" fill="{PAPER}"/>')
    b.append(f'<rect x="{left}" y="{y-mm(3.4):.1f}" width="{mm(1.1)}" '
             f'height="{bh:.1f}" fill="{BLUE}"/>')
    b.append(t(left + mm(3.4), y, d["hinge"][0], px(7.4), BLUE, w="bold"))
    ly = y + mm(3.9)
    for ln in lines:
        b.append(t(left + mm(3.4), ly, ln, px(6.6), INK))
        ly += mm(3.1)
    y = max(y - mm(3.4) + bh, ly)

    head = foot = ""
    if furniture:
        mast = (t(M, mm(7), "AGILIAN", px(7), BLUE, w="bold", ls=2.4)
                + t(M, mm(11), "THE MEDICAID DOLLAR PROJECT", px(7), MUT,
                    ls=1.5)) if masthead else ""
        head = (mast + t(M, mm(19), "Two households, and what the law reaches",
                         px(11), INK, w="bold")
                + f'<line x1="{M}" y1="{mm(22)}" x2="{W-M}" y2="{mm(22)}" '
                  f'stroke="{RULE}" stroke-width="{mm(0.4):.1f}"/>')
        fy = y + mm(3)
        foot = (f'<line x1="{M}" y1="{fy:.1f}" x2="{W-M}" y2="{fy:.1f}" '
                f'stroke="{RULE}" stroke-width="{mm(0.4):.1f}"/>'
                + t(M, fy + mm(4.6), "Composite households, not cases. Every "
                                     "figure is dollars off the hundred that "
                                     "reached people in that category, not a "
                                     "per-person amount.", px(6.2), MUT,
                    it=True))
        y = fy + mm(8)

    H = round(mm(SLOT_MM) + top + mm(2)) if not furniture else round(y + mm(3))

    desc = (f"{d['title']}. {d['sub']} " + " ".join(
        f"{n}, {g}: ${BY_G[g]:.2f} of every $100 of Medicaid spending reached "
        f"people in this category in 2024 and ${d30:.2f} will in 2030, of "
        f"which ${c:.2f} of the fall is coverage and ${r:.2f} is rate."
        for n, g, d30, _, c, r in d["people"])
        + " " + d["hinge"][0] + " " + d["hinge"][1])

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'role="img" aria-labelledby="h_{d["key"]} c_{d["key"]}">'
           f'<title id="h_{d["key"]}">{esc(d["title"])}</title>'
           f'<desc id="c_{d["key"]}">{esc(desc)}</desc>'
           f'<rect width="{W}" height="{H}" fill="{BG}"/>'
           + head + "".join(b) + foot + "</svg>")
    return svg, desc, y, H


if __name__ == "__main__":
    os.makedirs("cover", exist_ok=True)
    for d in (A, B):
        for name, mast, furn in ((d["key"], False, False),
                                 (d["key"] + "_standalone", True, True)):
            svg, desc, deep, H = build(d, masthead=mast, furniture=furn)
            if deep > H - mm(1):
                raise SystemExit(f"{name}: content reaches {deep:.0f} of {H}px "
                                 f"in a {COL_MM:.0f} x {SLOT_MM:.0f} mm slot. "
                                 f"Simplify it; do not shrink the type.")
            open(f"cover/{name}.svg", "w").write(svg)
            open(f"cover/{name}_alt.txt", "w").write(desc + "\n")
            open(f"cover/{name}.png", "wb").write(
                bytes(resvg_py.svg_to_bytes(svg_string=svg,
                                            width=round(COL_MM * 300 / 25.4))))
            print(f"wrote cover/{name}.png  content ends {deep:.0f} of {H}px")
    import contrast
    print("\n  contrast, measured against the page:")
    _w = contrast.report(contrast.PALETTE)
    print(f"\n  worst meaningful element {_w[0]} at {_w[1]:.2f}:1")
