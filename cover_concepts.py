"""Three cover concepts. Portrait. Every figure from cover_data.load()."""
import cover_data, resvg_py, os

D = cover_data.load()
PH, LV = D["phases"], D["levers"]
DISP = {"Other": "Everything else"}
for l in LV:
    l["label"] = DISP.get(l["label"], l["label"])
BY = {p["head"]: [l for l in LV if l["phase"] == p["head"]] for p in PH}

W, H = 1000, 1500
BLUE = "#17325c"; WARM = "#8B5A5A"; WARMD = "#6f4747"
INK = "#1b1b1b"; MUT = "#7a7570"; BG = "#faf8f3"; RULE = "#e2dccf"
PALE = "#c9d3de"
F = "Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif"


def t(x, y, s, size=14, fill=INK, a="start", w="normal", it=False, ls=0):
    st = f' font-style="italic"' if it else ""
    sp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{a}" font-weight="{w}"{st}{sp}>{s}</text>')


def frame(body, title, sub):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>'
            + t(80, 104, "AGILIAN", 13, BLUE, w="bold", ls=3.4)
            + t(80, 128, "THE MEDICAID DOLLAR PROJECT", 13, MUT, ls=2.2)
            + t(80, 196, title, 34, INK, w="bold")
            + t(80, 228, sub, 17, MUT)
            + f'<line x1="80" y1="254" x2="{W-80}" y2="254" stroke="{RULE}" stroke-width="1.3"/>'
            + body
            + f'<line x1="80" y1="{H-96}" x2="{W-80}" y2="{H-96}" stroke="{RULE}" stroke-width="1.3"/>'
            + t(80, H - 68, f"P.L. 119-21 removes ${D['gross']:.2f} of every $100. "
                            f"Overhead falls with it, returning ${D['rebate']:.2f}.", 14, INK)
            + t(80, H - 46, f"${D['net']:.2f} less reaches care. FY2024 actual against FY2030 "
                            f"projected; every figure modelled from CBO and CMS-64.", 13.5, MUT)
            + '</svg>')


# ---------------------------------------------------------------- A. the taper
def concept_a():
    b = []
    X0, K = 232.0, 3.28                     # bar left edge, px per dollar
    ys = [400, 680, 960, 1240]
    pts24, pts30 = [], []
    for p, y in zip(PH, ys):
        pts24.append((X0 + p["v24"] * K, y))
        pts30.append((X0 + p["v30"] * K, y))
    # the 2024 body: what the dollar did
    d = f'M{X0},{ys[0]-70:.0f} L' + " L".join(f"{x:.1f},{y}" for x, y in pts24) \
        + f' L{X0},{ys[-1]}' + " Z"
    b.append(f'<path d="{d}" fill="{PALE}" fill-opacity="0.55"/>')
    # the 2030 body, over it
    d = f'M{X0},{ys[0]-70:.0f} L' + " L".join(f"{x:.1f},{y}" for x, y in pts30) \
        + f' L{X0},{ys[-1]}' + " Z"
    b.append(f'<path d="{d}" fill="{BLUE}" fill-opacity="0.93"/>')
    b.append(t(X0 + 18, ys[0] - 34, "$100", 30, "#ffffff", w="bold"))
    b.append(t(X0 + 18, ys[0] - 14, "of Medicaid spending", 13, "#c6d2e2"))

    for p, y in zip(PH, ys):
        x24, x30 = X0 + p["v24"] * K, X0 + p["v30"] * K
        b.append(f'<line x1="{X0}" y1="{y}" x2="{x24:.1f}" y2="{y}" '
                 f'stroke="{BG}" stroke-width="1.6" stroke-opacity="0.7"/>')
        b.append(t(X0 - 20, y - 26, p["head"].upper(), 11.5, INK, "end", "bold", ls=1.1))
        b.append(t(X0 - 20, y + 2, f"${p['v30']:.2f}", 26, BLUE, "end", "bold"))
        b.append(t(X0 - 20, y + 22, f"was ${p['v24']:.2f}", 12, MUT, "end"))
        # the losses that bite here, in the gap the taper opens
        LX = 620.0
        ly = y + 4
        for l in BY[p["head"]]:
            b.append(f'<rect x="{x30+3:.1f}" y="{ly-10:.0f}" width="{max(l["amt"]*K,3):.1f}" '
                     f'height="12" fill="{WARM}" fill-opacity="0.9"/>')
            b.append(f'<line x1="{x30+l["amt"]*K+8:.1f}" y1="{ly-4:.1f}" x2="{LX-12:.0f}" '
                     f'y2="{ly-4:.1f}" stroke="{RULE}" stroke-width="1"/>')
            b.append(t(LX, ly, f'\u2212${l["amt"]:.2f}', 15, WARMD, w="bold"))
            b.append(t(LX + 62, ly, l["label"], 14, INK))
            b.append(t(LX + 62, ly + 17, l["who"], 12, MUT, it=True))
            ly += 48
    return frame("".join(b), "Where the money stops",
                 "$100 of Medicaid, and the seven cuts of P.L. 119-21")


# ------------------------------------------------------- B. the paired reading
def concept_b():
    b = []
    X0, X1 = 150.0, 820.0
    K = (X1 - X0) / 100.0
    ys = [396, 664, 932, 1200]
    for p, y in zip(PH, ys):
        b.append(t(X0, y - 46, p["head"].upper(), 14, INK, w="bold", ls=1.6))
        b.append(f'<line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{RULE}" stroke-width="1"/>')
        a, c = X0 + p["v30"] * K, X0 + p["v24"] * K
        b.append(f'<line x1="{a:.1f}" y1="{y}" x2="{c:.1f}" y2="{y}" stroke="{WARM}" stroke-width="9"/>')
        b.append(f'<circle cx="{c:.1f}" cy="{y}" r="9" fill="{PALE}" stroke="{BLUE}" stroke-width="2"/>')
        b.append(f'<circle cx="{a:.1f}" cy="{y}" r="11" fill="{BLUE}"/>')
        b.append(t(a - 20, y + 7, f"${p['v30']:.2f}", 24, BLUE, "end", "bold"))
        b.append(t(c + 20, y + 6, f"${p['v24']:.2f}", 15, MUT))
        b.append(t((a + c) / 2, y - 18, f'\u2212${p["v24"]-p["v30"]:.2f}', 15, WARMD, "middle", "bold"))
        ly = y + 34
        for l in BY[p["head"]]:
            b.append(f'<rect x="{X0:.0f}" y="{ly-9:.0f}" width="{l["amt"]*K:.1f}" height="11" '
                     f'fill="{WARM}" fill-opacity="0.8"/>')
            b.append(t(X0 + l["amt"] * K + 12, ly, f'\u2212${l["amt"]:.2f}', 14, WARMD, w="bold"))
            b.append(t(X0 + l["amt"] * K + 72, ly, l["label"], 13.5, INK))
            b.append(t(X0 + l["amt"] * K + 72, ly + 16, l["who"], 12, MUT, it=True))
            ly += 42
    b.append(f'<circle cx="{X0+6}" cy="306" r="8" fill="{BLUE}"/>')
    b.append(t(X0 + 24, 311, "FY2030 projected", 13, BLUE, w="bold"))
    b.append(f'<circle cx="{X0+186}" cy="306" r="7" fill="{PALE}" stroke="{BLUE}" stroke-width="2"/>')
    b.append(t(X0 + 202, 311, "FY2024 actual", 13, MUT))
    return frame("".join(b), "Four phases, two futures",
                 "Each bar below a phase is one lever of P.L. 119-21")


# ----------------------------------------------------------- C. the vertical fall
def concept_c():
    b = []
    XC, XW, K = 300.0, 168.0, 62.0         # column x, width, px per dollar of HEIGHT
    AX, NX = 494.0, 600.0
    y = 330.0
    b.append(t(XC, y - 22, "$100", 32, INK, w="bold"))
    b.append(t(XC + 104, y - 22, "enters the state agency", 14, MUT))
    last = None
    for l in LV:
        if l["phase"] != last:
            y += 16
            b.append(f'<line x1="80" y1="{y-10:.1f}" x2="{W-80}" y2="{y-10:.1f}" '
                     f'stroke="{RULE}" stroke-width="1.2"/>')
            b.append(t(XC - 24, y + 6, l["phase"].upper(), 11.5, MUT, "end", "bold", ls=1.4))
            last = l["phase"]
        h = l["amt"] * K
        adv = max(h, 50.0)
        b.append(f'<rect x="{XC:.0f}" y="{y:.1f}" width="{XW:.0f}" height="{h:.1f}" '
                 f'fill="{WARM}" fill-opacity="0.88"/>')
        cy = y + adv / 2
        b.append(t(AX, cy + 1, f'\u2212${l["amt"]:.2f}', 17, WARMD, w="bold"))
        b.append(t(NX, cy - 5, l["label"], 15, INK))
        b.append(t(NX, cy + 13, l["who"], 12, MUT, it=True))
        y += adv + 4
    y += 16
    hr = D["rebate"] * K
    adv = max(hr, 50.0)
    b.append(f'<rect x="{XC:.0f}" y="{y:.1f}" width="{XW:.0f}" height="{hr:.1f}" '
             f'fill="{PALE}" fill-opacity="0.9"/>')
    cy = y + adv / 2
    b.append(t(AX, cy + 1, f'+${D["rebate"]:.2f}', 16, MUT, w="bold"))
    b.append(t(NX, cy - 5, "Overhead falls with it", 15, INK))
    b.append(t(NX, cy + 13, "less money to administer", 12, MUT, it=True))
    y += adv + 22
    b.append(f'<line x1="80" y1="{y-11:.1f}" x2="{W-80}" y2="{y-11:.1f}" '
             f'stroke="{INK}" stroke-width="1.8"/>')
    b.append(f'<rect x="{XC:.0f}" y="{y:.1f}" width="{XW:.0f}" height="78" fill="{BLUE}"/>')
    b.append(t(AX, y + 48, f"${D['net']:.2f}", 36, BLUE, w="bold"))
    b.append(t(NX, y + 34, "less reaches care", 17, INK, w="bold"))
    b.append(t(NX, y + 56, "in FY2030, out of every hundred dollars", 13, MUT))
    return frame("".join(b), "Seven cuts, one hundred dollars",
                 "Read down: where P.L. 119-21 takes it, and who carries it")


os.makedirs("cover", exist_ok=True)
for nm, fn in (("A_taper", concept_a), ("B_paired", concept_b), ("C_fall", concept_c)):
    s = fn()
    open(f"cover/cover_{nm}.svg", "w").write(s)
    open(f"cover/cover_{nm}.png", "wb").write(
        bytes(resvg_py.svg_to_bytes(svg_string=s, width=1400)))
    print("wrote", nm)
