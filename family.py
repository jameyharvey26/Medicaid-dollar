"""Two households, and what P.L. 119-21 reaches in each.

A declared thought exercise. Every rate is read from inc.py, which allocates
each provision to the population the statute names and then across services by
that population's own measured FY2024 consumption. The households are
composites, not cases: nothing here is a family anyone has met.

Accessibility (Section 508 / WCAG 2.1 AA). The four eligibility-category fills
read 2.29 to 4.73 against white, so they are decoration and never the carrier:
every figure is labelled in text, and its category name is printed. Outlines
and all type are drawn in the darkened variants, 5.42 to 8.23.
"""
import inc, resvg_py, os
from inc import cube, D, G, S, BY_G, per_prov, DISP

TOT = {g: sum(cube[s][g] for s in S) for g in G}
WR = sum(per_prov["Work reporting"][2].values())
RATE = {g: 100 * TOT[g] / BY_G[g] for g in G}
ADULT_EXEMPT = 100 * (TOT["Adults"] - WR) / BY_G["Adults"]
ADULT_FULL = RATE["Adults"]

# Medicare Savings Program, 2026 amounts. What the suspended rule would have paid.
PART_B_MO, PART_B_DED, PART_A_DED = 202.90, 283.0, 1736.0
PART_B_YR = PART_B_MO * 12

W, H = 1500, 1110
BLUE, WARM, WARMD, EDGE = "#17325c", "#8B5A5A", "#6f4747", "#5c3a3a"
INK, MUT, BG, RULE = "#1b1b1b", "#6f6a64", "#ffffff", "#ded7c8"
FILL = {"Children": "#6fa382", "Adults": "#d8a24a",
        "Disabled": "#cf7d4f", "Aged": "#6f6f9e"}
DARK = {"Children": "#3f6f53", "Adults": "#8a6316",
        "Disabled": "#8c4a22", "Aged": "#4b4b73"}
F = "Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif"


def t(x, y, s, size=14, fill=INK, a="start", w="normal", it=False, ls=0):
    st = ' font-style="italic"' if it else ""
    sp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{a}" font-weight="{w}"{st}{sp}>{s}</text>')


def person(x, y, g, scale=1.0):
    """Head and shoulders. Fill is decoration; the outline carries the shape."""
    r = 13 * scale
    hy = y - 30 * scale
    return (f'<circle cx="{x}" cy="{hy}" r="{r}" fill="{FILL[g]}" '
            f'stroke="{DARK[g]}" stroke-width="2.2"/>'
            f'<path d="M{x-23*scale},{y+16*scale} a{23*scale},{26*scale} 0 0 1 '
            f'{46*scale},0 Z" fill="{FILL[g]}" stroke="{DARK[g]}" stroke-width="2.2"/>')


A = dict(
    title="A family of four", sub="No one disabled. Children 15 and 11.",
    people=[
        ("Parent, 36", "Adults", ADULT_EXEMPT, "exempt as a caregiver \u2014 until 2029"),
        ("Parent, 34", "Adults", ADULT_EXEMPT, "exempt as a caregiver \u2014 until 2029"),
        ("Child, 15",  "Children", RATE["Children"], "nothing in the law names children"),
        ("Child, 11",  "Children", RATE["Children"], "the exemption rests on this birthday"),
    ],
    reaches=[
        "Six-month renewals, from January 2027 \u2014 twice the chances to fall out",
        "Enrollment-rule suspensions \u2014 harder to get back in once out",
        "Provider tax limits and the residual \u2014 a smaller program around them",
        "Work reporting from 2029, when the younger child turns 14",
    ],
    hinge=("The exemption expires on a birthday.",
           "The younger child turns 14 in 2029 and both parents move to the 80-hour "
           "standard inside the window this paper covers. Their exposure roughly "
           f"triples, from {ADULT_EXEMPT:.1f}% to {ADULT_FULL:.1f}%."))

B = dict(
    title="A family of five", sub="One disabled child. A dual-eligible grandmother at home.",
    people=[
        ("Parent, 41", "Adults", ADULT_EXEMPT, "exempt as a caregiver \u2014 permanently"),
        ("Parent, 39", "Adults", ADULT_EXEMPT, "exempt as a caregiver \u2014 permanently"),
        ("Child, 9",   "Children", RATE["Children"], "nothing in the law names children"),
        ("Child, 7 \u00b7 disabled", "Disabled", RATE["Disabled"],
         "long-term care and behavioral health"),
        ("Grandmother, 74 \u00b7 dual", "Aged", RATE["Aged"],
         "nursing facility care, and a bill"),
    ],
    reaches=[
        "Six-month renewals and the enrollment-rule suspensions, as next door",
        "Directed payment caps \u2014 the nursing facility's rate, not their coverage",
        "The Medicare Savings rule suspended \u2014 the grandmother's premium",
        "Work reporting never reaches them: a disabled dependent has no age limit",
    ],
    hinge=("The exemption never expires. The bill arrives anyway.",
           "Caring for a disabled dependent carries no age ceiling, so the work rule "
           "passes over this household for good. What reaches it instead is a "
           "transfer: Medicaid stops paying the grandmother's Medicare costs and she "
           "starts."))


def column(d, x0, w):
    b = [t(x0, 172, d["title"], 30, BLUE, w="bold"),
         t(x0, 198, d["sub"], 16, MUT)]
    y = 268
    for name, g, rate, note in d["people"]:
        b.append(person(x0 + 30, y, g))
        b.append(t(x0 + 74, y - 22, name, 19, INK, w="bold"))
        b.append(t(x0 + 74, y - 1, note, 15, MUT, it=True))
        b.append(t(x0 + w - 8, y - 14, f"\u2212{rate:.1f}%", 27, WARMD, "end", "bold"))
        b.append(t(x0 + w - 8, y + 6, "of the Medicaid dollars behind their care",
                   13, MUT, "end"))
        b.append(f'<line x1="{x0}" y1="{y+26}" x2="{x0+w}" y2="{y+26}" '
                 f'stroke="{RULE}" stroke-width="1"/>')
        y += 76
    # Both columns start their lower blocks at the same height, so the two
    # households read as a pair rather than as two lists of different lengths.
    y = 268 + 76 * 5 + 14
    b.append(t(x0, y, "WHAT REACHES THEM", 13, INK, w="bold", ls=1.6))
    y += 30
    for line in d["reaches"]:
        cx, cy, r = x0 + 9, y - 6, 8
        b.append(f'<path d="M{cx},{cy-r} L{cx+r},{cy} L{cx},{cy+r} L{cx-r},{cy} Z" '
                 f'fill="{WARM}" stroke="{EDGE}" stroke-width="1.6"/>')
        b.append(t(x0 + 28, y, line, 15.5, INK))
        y += 30
    y += 16
    b.append(f'<rect x="{x0}" y="{y-6}" width="{w}" height="98" fill="#f5f2ea"/>')
    b.append(f'<rect x="{x0}" y="{y-6}" width="5" height="98" fill="{BLUE}"/>')
    b.append(t(x0 + 22, y + 22, d["hinge"][0], 18, BLUE, w="bold"))
    words, line, ly = d["hinge"][1].split(), "", y + 46
    for word in words:
        if len(line + " " + word) * 15 * 0.5 > w - 46 and line:
            b.append(t(x0 + 22, ly, line, 15, INK)); ly += 21; line = word
        else:
            line = (line + " " + word).strip()
    b.append(t(x0 + 22, ly, line, 15, INK))
    return "".join(b)


def build():
    COL = 660
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         t(64, 62, "AGILIAN  \u00b7  THE MEDICAID DOLLAR PROJECT", 13, MUT, ls=2.4),
         t(64, 110, "Two households, and what the law reaches in each", 34, INK, w="bold"),
         f'<line x1="64" y1="132" x2="{W-64}" y2="132" stroke="{RULE}" stroke-width="1.5"/>',
         column(A, 64, COL),
         f'<line x1="{W/2}" y1="150" x2="{W/2}" y2="{H-150}" stroke="{RULE}" stroke-width="1.2"/>',
         column(B, W - 64 - COL, COL)]
    fy = H - 112
    b.append(f'<line x1="64" y1="{fy}" x2="{W-64}" y2="{fy}" stroke="{RULE}" stroke-width="1.5"/>')
    b.append(t(64, fy + 30,
               "The grandmother's bill is not a service anyone stops providing. In 2026 "
               f"the Medicare Savings Programs pay a ${PART_B_MO:.2f} monthly Part B "
               f"premium \u2014 ${PART_B_YR:,.0f} a year \u2014 and, under QMB, the", 16, INK))
    b.append(t(64, fy + 54,
               f"${PART_B_DED:.0f} Part B deductible and the 20 percent coinsurance on "
               f"every outpatient service. A hospital stay adds a ${PART_A_DED:,.0f} Part A "
               "deductible per benefit period.", 16, INK))
    b.append(t(64, fy + 82,
               "Composite households, not cases. Rates are modelled: each provision "
               "allocated to the population the statute names, then across services by "
               "that population's measured FY2024 consumption. See the Limits register.",
               13.5, MUT, it=True))
    desc = ("Two composite households side by side. " + " ".join(
        f"{d['title']}: " + "; ".join(
            f"{n}, {g}, loses {r:.1f} percent of the Medicaid dollars behind their care"
            for n, g, r, _ in d["people"]) for d in (A, B)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
            f'aria-labelledby="ft fd"><title id="ft">Two households, and what P.L. '
            f'119-21 reaches in each</title><desc id="fd">{desc}</desc>' +
            "".join(b) + "</svg>"), desc


os.makedirs("cover", exist_ok=True)
svg, desc = build()
open("cover/family_two_households.svg", "w").write(svg)
open("cover/family_two_households_alt.txt", "w").write(desc + "\n")
open("cover/family_two_households.png", "wb").write(
    bytes(resvg_py.svg_to_bytes(svg_string=svg, width=2100)))
print("wrote cover/family_two_households.png")
print(f"adult exempt {ADULT_EXEMPT:.2f}%  adult full {ADULT_FULL:.2f}%  "
      f"child {RATE['Children']:.2f}%  disabled {RATE['Disabled']:.2f}%  aged {RATE['Aged']:.2f}%")
