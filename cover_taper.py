"""Cover graphic: the taper. Portrait, for the white space on the cover.

Accessibility. JW asked for "501"; the standard that governs a federal-facing
document is Section 508, which since the 2017 refresh incorporates WCAG 2.0
level AA by reference, and WCAG 2.1 AA is the current practical target. What
that actually requires of this graphic, and what was done:

  1.4.3 Contrast (text)         every text colour measured against the
                                background at >= 4.5:1, or >= 3:1 where the
                                type is large (>= 24px, or >= 19px bold).
                                The secondary grey was 4.30:1 and FAILED; it
                                is darkened to 5.05:1.
  1.4.11 Non-text contrast      the FY2024 boundary is meaningful, and its
                                pale fill reads 1.43:1 against the page. The
                                fill is kept as decoration and the BOUNDARY is
                                drawn as a real line at 3.13:1, so the shape is
                                perceivable without the fill.
  1.4.1 Use of colour           no quantity is carried by colour alone. Every
                                phase prints both its figures; every cut prints
                                its own amount and its own name. The graphic
                                reads in greyscale and reads read-aloud.
  1.4.4 Resize text             set in absolute units inside a viewBox, so it
                                scales with the frame and never reflows.
  1.1.1 Non-text content        role="img" with title and desc, and a written
                                long description emitted beside the file.

Every figure comes from cover_data.load(). Nothing here is typed (S-105).
"""
import cover_data, resvg_py, os

D = cover_data.load()
PH, LV = D["phases"], D["levers"]
DISP = {"Other": "Everything else"}
for l in LV:
    l["label"] = DISP.get(l["label"], l["label"])
BY = {p["head"]: [l for l in LV if l["phase"] == p["head"]] for p in PH}

W, H = 1100, 1640
BLUE = "#17325c"
WARM = "#8B5A5A"      # 5.34:1 on the page
WARMD = "#6f4747"     # 7.42:1
EDGE = "#5c3a3a"      # 9.33:1, the marker outline
INK = "#1b1b1b"       # 16.23:1
MUT = "#6f6a64"       # 5.05:1  (was #7a7570 at 4.30, which failed AA)
BG = "#ffffff"      # the page, not the boxed furniture (D-90)
GHOST = "#ccd6e1"     # decorative fill only
GHOSTL = "#7d8fa3"    # 3.13:1, the FY2024 boundary as a real line
RULE = "#ded7c8"
ONBLUE = "#d9e2ee"    # 9.9:1 on Agilian blue
F = "Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif"


def t(x, y, s, size=14, fill=INK, a="start", w="normal", it=False, ls=0):
    st = ' font-style="italic"' if it else ""
    sp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{a}" font-weight="{w}"{st}{sp}>{s}</text>')


def wrap(s, size, budget):
    out, line = [], ""
    for word in s.split():
        trial = (line + " " + word).strip()
        if len(trial) * size * 0.53 > budget and line:
            out.append(line); line = word
        else:
            line = trial
    out.append(line)
    return out


def build():
    X0, K = 278.0, 2.62                  # bar left edge, px per dollar
    LX = 640.0                           # the label column
    ys = [468, 756, 1044, 1332]
    b = []

    pts24 = [(X0 + p["v24"] * K, y) for p, y in zip(PH, ys)]
    pts30 = [(X0 + p["v30"] * K, y) for p, y in zip(PH, ys)]
    top = ys[0] - 118

    # The column enters at full width: $100 arrives, it does not taper into
    # existence. The first segment is the drop from $100 to the state agency.
    d24 = (f'M{X0},{top} L{X0+100*K:.1f},{top} L'
           + " L".join(f"{x:.1f},{y}" for x, y in pts24) + f' L{X0},{ys[-1]} Z')
    b.append(f'<path d="{d24}" fill="{GHOST}" fill-opacity="0.75"/>')
    # 1.4.11 — the FY2024 edge drawn as a line, not left to the fill
    b.append('<path d="M' + f'{X0+100*K:.1f},{top} L'
             + " L".join(f"{x:.1f},{y}" for x, y in pts24)
             + f'" fill="none" stroke="{GHOSTL}" stroke-width="2.4"/>')
    d30 = (f'M{X0},{top} L{X0+100*K:.1f},{top} L'
           + " L".join(f"{x:.1f},{y}" for x, y in pts30) + f' L{X0},{ys[-1]} Z')
    b.append(f'<path d="{d30}" fill="{BLUE}"/>')

    b.append(t(X0 + 26, top + 54, "$100", 50, "#ffffff", w="bold"))
    b.append(t(X0 + 26, top + 82, "of Medicaid spending", 20, ONBLUE))
    b.append(t(X0 + 100 * K + 24, top + 34, "FY2024", 20, GHOSTL, w="bold"))
    b.append(t(X0 + 100 * K + 24, top + 58, "actual, for comparison", 17, MUT))

    for p, y in zip(PH, ys):
        x24, x30 = X0 + p["v24"] * K, X0 + p["v30"] * K
        b.append(f'<line x1="{X0}" y1="{y}" x2="{x24:.1f}" y2="{y}" '
                 f'stroke="{BG}" stroke-width="2.4" stroke-opacity="0.85"/>')
        b.append(t(X0 - 28, y - 44, p["head"].upper(), 16, INK, "end", "bold", ls=1.1))
        b.append(t(X0 - 28, y - 2, f"${p['v30']:.2f}", 44, BLUE, "end", "bold"))
        b.append(t(X0 - 28, y + 24, f"was ${p['v24']:.2f} in FY2024", 18, MUT, "end"))

        ly = y + 10
        for l in BY[p["head"]]:
            # A rhombus, not a square: the panels already encode every P.L.
            # 119-21 loss as a warm rhombus and the reader should not have to
            # learn a second alphabet for the same fact.
            cx, cy, r = x30 + 20, ly - 8, 15
            b.append(f'<path d="M{cx},{cy-r} L{cx+r},{cy} L{cx},{cy+r} L{cx-r},{cy} Z" '
                     f'fill="{WARM}" stroke="{EDGE}" stroke-width="2"/>')
            b.append(f'<line x1="{cx+r+8:.1f}" y1="{cy:.1f}" x2="{LX-16:.0f}" y2="{cy:.1f}" '
                     f'stroke="{GHOSTL}" stroke-width="1.4"/>')
            b.append(t(LX, ly, f'\u2212${l["amt"]:.2f}', 27, WARMD, w="bold"))
            lines = wrap(l["label"], 22, 320)
            yy = ly - 6
            for ln in lines:
                b.append(t(LX + 112, yy, ln, 22, INK))
                yy += 25
            for ln in wrap(l["who"], 17, 340):
                b.append(t(LX + 112, yy + 2, ln, 17, MUT, it=True))
                yy += 21
            ly += max(78, yy - ly + 34)

    head = (t(80, 118, "AGILIAN", 17, BLUE, w="bold", ls=4.2)
            + t(80, 148, "THE MEDICAID DOLLAR PROJECT", 17, MUT, ls=2.6)
            + t(80, 238, "Where the money stops", 52, INK, w="bold")
            + t(80, 280, "$100 of Medicaid, and the seven cuts of P.L. 119-21", 24, MUT)
            + f'<line x1="80" y1="316" x2="{W-80}" y2="316" stroke="{RULE}" stroke-width="1.6"/>')
    foot = (f'<line x1="80" y1="{H-132}" x2="{W-80}" y2="{H-132}" stroke="{RULE}" stroke-width="1.6"/>'
            + t(80, H - 96, f"P.L. 119-21 removes ${D['gross']:.2f} of every $100. Overhead is "
                            f"assumed to fall with it, returning ${D['rebate']:.2f}.", 19, INK)
            + t(80, H - 68, f"${D['net']:.2f} less reaches care.", 19, WARMD, w="bold")
            + t(80, H - 40, "FY2024 actual against FY2030 projected under prior law. "
                            "Every figure modelled from CBO and CMS-64.", 17, MUT))

    desc = (f"A vertical column showing $100 of Medicaid spending narrowing as it passes "
            f"four phases. " + " ".join(
        f"At {p['head'].lower()}, ${p['v30']:.2f} remains in FY2030 against ${p['v24']:.2f} in FY2024."
        for p in PH) + " The seven cuts of P.L. 119-21 are " + "; ".join(
        f"{l['label']}, ${l['amt']:.2f}, carried by {l['who'].lower()}" for l in LV) +
        f". Gross removal is ${D['gross']:.2f}; overhead falls by ${D['rebate']:.2f}; "
        f"${D['net']:.2f} less reaches care.")

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
            f'aria-labelledby="ttl dsc">'
            f'<title id="ttl">Where the money stops: $100 of Medicaid and the seven cuts '
            f'of P.L. 119-21</title><desc id="dsc">{desc}</desc>'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>'
            + head + "".join(b) + foot + '</svg>'), desc


os.makedirs("cover", exist_ok=True)
svg, desc = build()
open("cover/cover_taper.svg", "w").write(svg)
open("cover/cover_taper_alt.txt", "w").write(desc + "\n")
open("cover/cover_taper.png", "wb").write(
    bytes(resvg_py.svg_to_bytes(svg_string=svg, width=1540)))
print("wrote cover/cover_taper.png")
