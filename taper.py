"""The horizontal taper family. Figures 6, 7, 8, 9 and 11.

JW, D-95: the same graphic as the cover, tipped on its side. Same palette, same
compositing, same rhombus for a P.L. 119-21 loss, same FY2024 ghost behind the
FY2030 solid. The cover narrows downward; these narrow rightward, because the
paper is landscape and the eye already reads the panels left to right.

Five figures out of one generator, not five drawings. Each names the provisions
it is about; the rest of the taper is still drawn, greyed, so the reader always
sees the whole run and where the highlighted piece sits in it. That is what a
detail crop used to do by cutting, and cutting is what made the crops hard to
read: a crop shows a piece of a picture with no picture around it.

    Figure 6   all seven provisions, full width
    Figure 7   the three that leave before a claim exists
    Figure 8   provider tax limits, in the federal band
    Figure 9   the three that leave at the payer and at claims
    Figure 11  the three that land on providers and beneficiaries

The phase set runs one further up than the cover's. Figure 8's whole subject is
the provider tax leaving the federal column before the two shares merge, and
the cover starts at the state agency. cover_data.load(federal=True).

Accessibility (Section 508 / WCAG 2.1 AA). Measured by contrast.py and printed
at build time, never asserted here:

  1.4.3   every text colour against the page
  1.4.11  the marker fill and the FY2024 boundary, which is stroked rather than
          left to its tint, so the shape survives without colour
  1.4.1   no quantity carried by colour alone: every phase prints both its
          figures and every highlighted provision prints its own amount and
          name. A greyed provision prints nothing, because it is not the
          subject of that figure and its number is in the figure that is.
  1.1.1   role="img" with title and desc, and a written long description
          emitted beside each file.

Every figure comes from cover_data.load(). Nothing here is typed (S-105).
"""
import os
import cover_data
import inc
import contrast
import taperkit as TK
import resvg_py

D = cover_data.load(federal=True)
PH, LV = D["phases"], D["levers"]
# The ledger's residual is keyed "Other"; the paper calls it Everything else
# everywhere a reader sees it, and S-108 says the prose and the diagrams use
# one name. The cover applies the same map.
DISP = {"Other": "Everything else"}
for _l in LV:
    _l["label"] = DISP.get(_l["label"], _l["label"])
BY_LABEL = {l["label"]: l for l in LV}

BLUE = "#17325c"
WARM = "#8B5A5A"
WARMD = "#6f4747"
EDGE = "#5c3a3a"
INK = "#1b1b1b"
MUT = "#6f6a64"
BG = "#ffffff"
GHOST = "#ccd6e1"
GHOSTL = "#7d8fa3"
GREY = "#b9b4ae"        # a provision this figure is not about
GREYD = "#8c8781"
RULE = "#ded7c8"
ONBLUE = "#d9e2ee"
F = "Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif"

PALETTE = contrast.PALETTE + [
    ("GREY, out-of-focus marker fill", GREY, "decoration"),
    ("GREYD, its outline", GREYD, "object"),
]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=14, fill=INK, a="start", w="normal", it=False, ls=0):
    st = ' font-style="italic"' if it else ""
    sp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{a}" font-weight="{w}"{st}{sp}>'
            f'{esc(s)}</text>')


def wrap(s, size, budget):
    """Greedy wrap on an average glyph width. The same approximation the cover
    uses; it is allowed to be approximate because nothing is justified."""
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


# --------------------------------------------------------------------------
# One px/mm for the whole family, so a type size means the same thing on every
# figure whatever slot it sits in. The canvases below are therefore stated in
# MILLIMETRES OF PAGE, which is what the manuscript actually allocates, and
# converted here. A figure that outgrows its slot fails the build rather than
# being scaled down until its labels stop being readable.
PXMM = 11.7
COL_MM = 118.0          # one column of the two-column landscape grid
SPAN_MM = 250.0         # the full text measure

# Type, in points of printed page. pt -> px is (pt / 72 * 25.4) * PXMM.
def px(pt):
    """Type size, in POINTS of printed page."""
    return round(pt / 72 * 25.4 * PXMM)


def mm(v):
    """A distance on the page, in MILLIMETRES.

    Kept separate from px() on purpose. The first draft of this file used one
    helper for both and every layout constant came out at a quarter of its
    intended size, because a millimetre and a point are not the same unit and
    nothing in the code said which one was meant.
    """
    return round(v * PXMM)


FIGS = {
    # slot: the space the manuscript already gives this figure. JW: design the
    # output to fit the context it is in, do not push the content around the
    # paper to suit the picture.
    "fig6_taper_all": dict(
        mm=(SPAN_MM, 119.5), layout="wide",
        title="Where the money stops",
        sub="$100 of Medicaid, and the seven provisions of P.L. 119-21",
        focus=None),
    # D-98. The three detail figures now cut the run by PHASE, in the order the
    # money meets the provisions, because that is the order the section reads
    # in and the order Figure 6 draws. Between them they name all seven: no
    # provision is discussed without a picture that has it in colour.
    # JW deleted the federal-band figure: the provider tax section carries no
    # picture now, and Figure 6 is where the federal band is read.
    "fig7_taper_upstream": dict(
        mm=(COL_MM, 87.2), layout="narrow",
        title="The state agency and disbursements",
        sub="Three provisions leave before a payer sees the money",
        focus=["Everything else", "Work reporting", "Six-month renewals"]),
    "fig8_taper_claims": dict(
        mm=(COL_MM, 87.2), layout="narrow",
        title="Claims, and the people beyond them",
        sub="Three provisions leave at or after the point of a claim",
        focus=["Medicaid enrollment rule suspended",
               "Directed payment caps", "Medicare Savings rule suspended"]),
    # JW: the landing figure was a duplicate of the claims figure - same three
    # provisions, same phases, same picture under a different title - and is
    # deleted. Figures after it renumber.
}

# On a column figure there is not room for five phase names AND five pairs of
# figures AND a full label list. The simplification is deliberate and JW
# approved it: a narrow taper prints the value at every phase, names every
# phase, and drops the "was $X in FY2024" line, which the ghost edge already
# says and the caption repeats.
SHORT = {"Federal and state shares": "FEDERAL", "State agency": "AGENCY",
         "Disbursements": "DISBURSED", "The payer": "PAYER",
         "Claims to providers": "CLAIMS", "Beneficiaries": "DELIVERED"}


# D-100. Figure 10 is a member of this family, not a second drawing program.
# JW: make it work like six, seven, eight and nine, just for the payer lane.
# So the generator takes its phases and its markers from the spec, and the
# payer figure supplies one extra phase and two extra markers. Everything
# else - the palette, the ghost behind the solid, the rhombus, the two label
# columns, the slot arithmetic - is the same code.
#
# The extra phase is the payer itself. The band is flat across it, because
# nothing has left yet, and then steps down to claims: that step IS the
# $5.65 the plans keep. The two markers under it are the halves of it.
def payer_view():
    """The five phases with the payer inserted, and its two peels as markers.

    The peels are ordinary leakage under prior law, not P.L. 119-21, and the
    figure says so in the `who` line under each one. They are drawn in the
    focus colour because they are what this figure is ABOUT; grey in this
    family means out of focus, not lawful.
    """
    c24, c30 = inc.c24, inc.c30
    ph = []
    for p in PH:
        ph.append(p)
        if p["head"] == "Disbursements":
            ph.append(dict(p, head="The payer"))
    lv = list(LV) + [
        dict(label="Plan administration", amt=c24.adm_marg,
             phase="The payer",
             who=f"non-dual and dual plans; ${c30.adm_marg:.2f} in FY2030"),
        dict(label="Public-company earnings", amt=c24.earnings,
             phase="The payer",
             who=f"retained at the traded plans; ${c30.earnings:.2f} in FY2030"),
    ]
    return ph, lv


def build(name, spec, masthead=False, furniture=False):
    """One taper.

    `furniture` draws the masthead, title, subtitle and footing. The version
    that goes in the paper does not have them: the figcaption is the title and
    the page carries the masthead, so drawing them again both repeats the
    reader and steals the room the picture needs. The standalone version, for
    a deck or a one-pager, has all of it.
    """
    mmw, mmh = spec["mm"]
    narrow = spec["layout"] == "narrow"
    top_pad = mm(30) if furniture else mm(2)
    foot_pad = mm(18) if furniture else 0
    # D-98. The slot height is a CEILING, not a target. Drawing every figure
    # to the full height of its slot left dead paper inside the picture, which
    # a reader reads as part of the figure and a typesetter reads as a figure
    # that is bigger than it needs to be. The canvas is trimmed to its own
    # content on the second pass; `mmh` only says how much room the page can
    # spare, and the build fails if the content wants more.
    PHS, LVS = spec.get("view", (PH, LV))

    # JW: crop each detail figure to its own phases, and no grey diamonds. A
    # provision that this figure is not about is now absent, not greyed - the
    # grey markers were meant to keep the whole run visible, and JW's reading
    # is that they carry no meaning in a detail view and read as clutter.
    #
    # The span is derived, not declared per figure: first focus phase to last,
    # then one phase forward so the band has somewhere to go, then one phase
    # back if that still leaves fewer than three. That is what puts Figure 9 at
    # disbursements rather than at claims, which is where JW asked for it, and
    # it keeps the federal and agency phases out of Figure 8, which is what he
    # asked for there. One rule, both notes satisfied.
    if spec["focus"]:
        _heads = [p["head"] for p in PHS]
        _hit = [i for i, h in enumerate(_heads)
                if any(l["phase"] == h and l["label"] in spec["focus"]
                       for l in LVS)]
        lo, hi = min(_hit), max(_hit)
        if hi < len(PHS) - 1:
            hi += 1
        if hi - lo < 2 and lo > 0:
            lo -= 1
        PHS = PHS[lo:hi + 1]
        LVS = [l for l in LVS if l["label"] in spec["focus"]]
    W = round(mmw * PXMM)
    H = spec.get("_h") or (round(mmh * PXMM) + top_pad + foot_pad)
    focus = spec["focus"]
    is_focus = (lambda lab: True) if focus is None else (lambda lab: lab in focus)

    M = mm(4.5)
    left, right = M, W - M
    head_h = mm(14)                      # phase name + value above the band
    top = top_pad + head_h
    band = mm(11) if narrow else mm(22)
    K = band / 100.0
    n = len(PHS)
    step = (right - left) / (n - 1)
    xs = [left + step * i for i in range(n)]

    b = []

    def shape(key):
        pts = [(x, top + p[key] * K) for x, p in zip(xs, PHS)]
        return (f'M{left:.1f},{top:.1f} L'
                + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
                + f' L{right:.1f},{top:.1f} Z')

    b.append(f'<path d="{shape("v24")}" fill="{GHOST}" fill-opacity="0.75"/>')
    b.append('<path d="M'
             + " L".join(f"{x:.1f},{top + p['v24'] * K:.1f}"
                         for x, p in zip(xs, PHS))
             + f'" fill="none" stroke="{GHOSTL}" stroke-width="{mm(0.45):.1f}"/>')
    b.append(f'<path d="{shape("v30")}" fill="{BLUE}"/>')

    # Only the uncropped figure starts at $100. A detail figure that opens at
    # disbursements opens at $84.47, and printing $100 inside it would be a
    # plain untruth about the band the reader is looking at.
    if PHS[0]["head"] == PH[0]["head"]:
        b.append(t(left + mm(2.5), top + mm(6.4), "$100", px(13), "#ffffff",
                   w="bold"))
    if not narrow:
        b.append(t(left + mm(2.5), top + mm(10), "of Medicaid spending",
                   px(6), ONBLUE))

    for i, (x, p) in enumerate(zip(xs, PHS)):
        y24 = top + p["v24"] * K
        b.append(f'<line x1="{x:.1f}" y1="{top:.1f}" x2="{x:.1f}" '
                 f'y2="{y24:.1f}" stroke="{BG}" stroke-width="{mm(0.45):.1f}" '
                 f'stroke-opacity="0.85"/>')
        # On a column figure the interior labels are centred on their own
        # phase line, because start-anchored CLAIMS and end-anchored
        # BENEFICIARIES met in the middle of a 118mm measure.
        if i == 0:
            hx, anchor = x, "start"
        elif i == n - 1:
            hx, anchor = right, "end"
        else:
            hx, anchor = (x, "middle") if narrow else (x, "start")
        lab = SHORT[p["head"]] if narrow else p["head"].upper()
        # JW: the FY2024 line used to print INSIDE the band, grey on dark
        # blue, where it could not be read. It sits above the band now, under
        # the phase name and over the figure it qualifies.
        b.append(t(hx, top - mm(12.4), lab, px(6.2), INK, anchor, "bold",
                   ls=0.8))
        if not narrow:
            b.append(t(hx, top - mm(8), f"was ${p['v24']:.2f} in FY2024",
                       px(5.6), MUT, anchor))
        b.append(t(hx, top - mm(1.6), f"${p['v30']:.2f}", px(11), BLUE,
                   anchor, "bold"))

    rows = {p["head"]: [l for l in LVS if l["phase"] == p["head"]] for p in PHS}
    # JW: the leaders were crowded once the figures were cropped. More air
    # between the band and the label block, which the slot now has room for.
    BLOCK = top + band + (mm(12) if narrow else mm(11))
    deepest = BLOCK

    # Back to the arrangement JW approved: two label columns on a narrow
    # figure, one column per phase on a wide one, diagonal leaders, every
    # leader meeting the END of its own amount. The single-row packing tried
    # in between made seven labels share 250mm and wrap to three lines each,
    # which is worse than the fault it was fixing. taperkit.pack is kept for
    # when the placement is tuned deliberately.
    rows = {p["head"]: [l for l in LVS if l["phase"] == p["head"]] for p in PHS}
    BLOCK = top + band + (mm(12) if narrow else mm(11))
    leads, texts = [], []
    deepest = BLOCK

    if narrow:
        picked = []
        for x, p in zip(xs, PHS):
            here = rows[p["head"]]
            for k, l in enumerate(here):
                off = (k - (len(here) - 1) / 2) * mm(4.4)
                picked.append((x + off, p, l))
        on_list = [(x, p, l) for x, p, l in picked if is_focus(l["label"])]
        NCOL = 2 if len(on_list) > 1 else 1
        col_x = [left + ((right - left) / NCOL) * c for c in range(NCOL)]

        # A column starts clear of the leaders that pass it. A leader drops
        # vertically at its own marker before turning, so a marker sitting to
        # the RIGHT of a later column's left edge sends its line down through
        # that column's text - which is the line through 'Medicare Savings
        # rule suspended'. Moving the text is the fix; moving the line was
        # not.
        half = -(-len(on_list) // NCOL)
        for c in range(1, NCOL):
            passing = [x for k, (x, _, _) in enumerate(on_list)
                       if min(k // half, NCOL - 1) < c]
            if passing:
                col_x[c] = max(col_x[c], max(passing) + mm(4))
        CW = right - col_x[-1] - mm(2)
        ycol = [BLOCK] * NCOL
        for x, p, l in picked:
            on = is_focus(l["label"])
            my = top + p["v30"] * K + mm(3.4)
            b.append(TK.diamond(x, my, mm(1.8), WARM if on else GREY,
                                EDGE if on else GREYD))
            if not on:
                continue
            k_on = on_list.index((x, p, l))
            c = min(k_on // half, NCOL - 1)
            cx0, ly = col_x[c], ycol[c]
            amt = f'\u2212${l["amt"]:.2f}'
            leads.append(TK.leader(x, my + mm(1.8), cx0, amt, px(9.5), ly))
            texts.append(t(cx0, ly, amt, px(9.5), WARMD, w="bold"))
            yy = ly + mm(4.1)
            for ln in wrap(l["label"], px(8.5), CW):
                texts.append(t(cx0, yy, ln, px(8.5), INK))
                yy += mm(3.6)
            for ln in wrap(l["who"], px(6.4), CW):
                texts.append(t(cx0, yy + mm(0.4), ln, px(6.4), MUT, it=True))
                yy += mm(2.9)
            ycol[c] = yy + mm(1.4)
        deepest = max(ycol)
    else:
        for i, (x, p) in enumerate(zip(xs, PHS)):
            # The block sits under its own phase. JW's straight-down rule
            # does the work that pushing the column sideways was trying to do,
            # and pushing it sideways narrowed the measure until the labels
            # would not fit the slot.
            cx0 = left + ((right - left) / n) * i
            cw = (right - left) / n - mm(6)
            ly = BLOCK
            for l in rows[p["head"]]:
                on = is_focus(l["label"])
                my = top + p["v30"] * K + mm(3.4)
                b.append(TK.diamond(x, my, mm(2.0), WARM if on else GREY,
                                    EDGE if on else GREYD))
                if not on:
                    continue
                amt = f'\u2212${l["amt"]:.2f}'
                leads.append(TK.leader(x, my + mm(2.0), cx0, amt, px(10), ly))
                texts.append(t(cx0, ly, amt, px(10), WARMD, w="bold"))
                yy = ly + mm(4.6)
                for ln in wrap(l["label"], px(8.5), cw):
                    texts.append(t(cx0, yy, ln, px(8.5), INK))
                    yy += mm(4.2)
                for ln in wrap(l["who"], px(6.4), cw):
                    texts.append(t(cx0, yy + mm(0.6), ln, px(6.4), MUT,
                                   it=True))
                    yy += mm(3.4)
                ly = yy + mm(4)
            deepest = max(deepest, ly)
    b += leads + texts

    # JW: say what the two blues mean. Dark is the FY2030 band with the law
    # applied; the pale edge behind it is FY2024, and because the FY2030
    # projection before HR-1 is FY2024 structure carried forward (note 2a),
    # the gap between them IS P.L. 119-21 rather than six years of drift.
    ky = deepest + mm(6)
    kx = left
    for _lab, _fill, _stroke in (
            (f"FY2030 projected spend, after P.L. 119-21", BLUE, None),
            (f"Money impacted by P.L. 119-21", GHOST, GHOSTL)):
        _st = (f' stroke="{_stroke}" stroke-width="{mm(0.4):.1f}"'
               if _stroke else "")
        b.append(f'<rect x="{kx:.1f}" y="{ky-mm(2.6):.1f}" width="{mm(5)}" '
                 f'height="{mm(3.4)}" fill="{_fill}"{_st}/>')
        b.append(t(kx + mm(6.6), ky, _lab, px(7), INK))
        kx += mm(9) + TK.width(_lab, px(7))
    deepest = ky + mm(2)

    head = ""
    foot = ""
    if furniture:
        mast = (t(M, mm(7), "AGILIAN", px(7), BLUE, w="bold", ls=2.4)
                + t(M, mm(11), "THE MEDICAID DOLLAR PROJECT", px(7), MUT, ls=1.5)) \
            if masthead else ""
        head = (mast
                + t(M, mm(20), spec["title"], px(18), INK, w="bold")
                + t(M, mm(25), spec["sub"], px(8.5), MUT)
                + f'<line x1="{M}" y1="{mm(28)}" x2="{W-M}" y2="{mm(28)}" '
                  f'stroke="{RULE}" stroke-width="{mm(0.4):.1f}"/>')
        fy = H - mm(14)
        note = ("Greyed markers are the other provisions of P.L. 119-21, drawn "
                "so the whole run stays visible."
                if focus else
                f"P.L. 119-21 removes ${D['gross']:.2f} of every $100. "
                f"Overhead is assumed to fall with it, returning "
                f"${D['rebate']:.2f}.")
        foot = (f'<line x1="{M}" y1="{fy:.1f}" x2="{W-M}" y2="{fy:.1f}" '
                f'stroke="{RULE}" stroke-width="{mm(0.4):.1f}"/>'
                + t(M, fy + mm(5), note, px(7.5), INK)
                + t(M, fy + mm(10), "FY2024 actual against FY2030 projected "
                                     "under prior law. Every figure modelled "
                                     "from CBO and CMS-64.", px(6.6), MUT, it=True))
        H = max(H, round(fy + mm(13)))

    shown = [l for l in LVS if is_focus(l["label"])]
    desc = (f"{spec['title']}. A horizontal band of $100 of Medicaid spending, "
            f"narrowing left to right as it passes {len(PHS)} phases. "
            + " ".join(f"At {p['head'].lower()}, ${p['v30']:.2f} remains in "
                       f"FY2030 against ${p['v24']:.2f} in FY2024."
                       for p in PHS)
            + " Marked below the band: "
            + "; ".join(f"{l['label']}, ${l['amt']:.2f}, at {l['phase'].lower()}, "
                        f"carried by {l['who'].lower()}" for l in shown)
            + (". The remaining provisions of P.L. 119-21 are marked but not "
               "labelled here; they are named in Figure 6." if focus else "."))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'role="img" aria-labelledby="t_{name} d_{name}">'
           f'<title id="t_{name}">{esc(spec["title"])}</title>'
           f'<desc id="d_{name}">{esc(desc)}</desc>'
           f'<rect width="{W}" height="{H}" fill="{BG}"/>'
           + head + "".join(b) + foot + "</svg>")
    return svg, desc, deepest, H


def main():
    os.makedirs("cover", exist_ok=True)
    for name, spec in FIGS.items():
        spec["_h"] = None
        _, _, deepest, H = build(name, spec)          # measure
        room = round(spec["mm"][1] * PXMM) + mm(2)
        if deepest > room:
            raise SystemExit(
                f"{name}: the labels reach {deepest:.0f}px in a slot "
                f"{spec['mm'][0]:.0f} x {spec['mm'][1]:.0f} mm, which holds "
                f"{room:.0f}px. Simplify the figure or ask JW for a bigger "
                f"slot; do NOT shrink the type to make it fit.")
        spec["_h"] = round(deepest + mm(2))           # then trim to content
        svg, desc, deepest, H = build(name, spec)
        # Then trim again, on the RENDERED picture rather than on the layout
        # cursor. `deepest` is where the next label would start, which is a few
        # millimetres past the last ink, and that slack printed as dead paper
        # inside the figure. artwhite.py measures the blank; this closes it to
        # the 3mm of air a figure is entitled to.
        import artwhite
        _png = bytes(resvg_py.svg_to_bytes(
            svg_string=svg, width=round(spec["mm"][0] * 300 / 25.4)))
        open("/tmp/_trim.png", "wb").write(_png)
        from PIL import Image as _I
        _blank = artwhite.blank_run(_I.open("/tmp/_trim.png").convert("RGB"),
                                    "bottom") / artwhite.PXMM_PRINT
        if _blank > 3.0:
            spec["_h"] = int(spec["_h"] - mm(_blank - 3.0))
            svg, desc, deepest, H = build(name, spec)
        open(f"cover/{name}.svg", "w").write(svg)
        open(f"cover/{name}_alt.txt", "w").write(desc + "\n")
        open(f"cover/{name}.png", "wb").write(
            bytes(resvg_py.svg_to_bytes(svg_string=svg,
                                        width=round(spec["mm"][0] * 300 / 25.4))))
        sa, _, _, _ = build(name, spec, masthead=True, furniture=True)
        open(f"cover/{name}_standalone.svg", "w").write(sa)
        open(f"cover/{name}_standalone.png", "wb").write(
            bytes(resvg_py.svg_to_bytes(svg_string=sa,
                                        width=round(spec["mm"][0] * 300 / 25.4))))
        print(f"wrote cover/{name}.png  slot {spec['mm'][0]:.0f}x"
              f"{spec['mm'][1]:.0f}mm  labels end {deepest:.0f} of {room:.0f}px")
    print("\n  contrast, measured against the page:")
    worst = contrast.report(PALETTE, out=lambda s: print(s))
    print(f"\n  worst meaningful element {worst[0]} at {worst[1]:.2f}:1")


if __name__ == "__main__":
    main()
