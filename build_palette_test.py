"""Palette proof sheet: payer ramp + five loss treatments, color and grayscale."""
import palette as P

W, H = 1500, 1420
INK, MUT = P.INK, P.MUTED
FONT = "Jost, 'Century Gothic', 'Trebuchet MS', sans-serif"

def txt(x, y, s, sz=13, col=None, anchor="start", weight="normal", italic=False):
    col = col or INK
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    st = ' font-style="italic"' if italic else ''
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{sz}" '
            f'fill="{col}" text-anchor="{anchor}" font-weight="{weight}"{st}>{s}</text>')

def rect(x, y, w, h, fill, tex=None, op=1.0):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity="{op}"/>'
    if tex:
        o += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
              f'fill="url(#{tex})"/>')
    return o

def band(x0, y0, x1, y1, th, fill, tex=None, op=0.92):
    """Bezier flow band."""
    mx = (x0 + x1) / 2
    d = (f'M{x0},{y0} C{mx},{y0} {mx},{y1} {x1},{y1} '
         f'L{x1},{y1+th} C{mx},{y1+th} {mx},{y0+th} {x0},{y0+th} Z')
    o = f'<path d="{d}" fill="{fill}" opacity="{op}"/>'
    if tex:
        o += f'<path d="{d}" fill="url(#{tex})"/>'
    return o

def sheet(gray=False):
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    s.append(P.texture_defs())
    if gray:
        s.append('<filter id="gs"><feColorMatrix type="saturate" values="0"/></filter>')
    s.append(f'<rect width="{W}" height="{H}" fill="#FCFCFB"/>')
    s.append('<g' + (' filter="url(#gs)"' if gray else '') + '>')

    mode = "GRAYSCALE (print / photocopy check)" if gray else "COLOR"
    s.append(txt(40, 46, "Sankey Palette — Proof Sheet", 26, INK, weight="bold"))
    s.append(txt(40, 70, f"Cool = money moving.  Warm = money stopping.  Slate = structural.   [{mode}]",
                 13, MUT, italic=True))

    # ---- Payer families ----
    y = 118
    s.append(txt(40, y, "PAYER FAMILIES — cool = money moving", 14, INK, weight="bold"))
    s.append(txt(40, y + 18, "Family tells you what KIND of payer before you read the label.", 11, MUT, italic=True))
    y += 42
    for title, tbl in [("CARRIERS  (blue / indigo) — reserved", P.PAYER_CARRIER),
                       ("HEALTH-SYSTEM PLANS  (violet / purple) — reserved", P.PAYER_HEALTH_SYSTEM)]:
        s.append(txt(40, y, title, 11, INK, weight="bold"))
        y += 12
        for i, (n, c) in enumerate(tbl.items()):
            cx = 40 + (i % 5) * 288
            cy = y + (i // 5) * 60
            s.append(rect(cx, cy, 266, 26, c))
            s.append(txt(cx, cy + 40, n, 10, MUT))
        y += 128
    s.append(txt(40, y, "LOCAL / REGIONAL  (teal / green) — shared family, ranked by size", 11, INK, weight="bold"))
    y += 12
    for i, c in enumerate(P.PAYER_LOCAL_RAMP):
        cx = 40 + i * 288
        s.append(rect(cx, y, 266, 26, c))
        s.append(txt(cx, y + 40, f"L{i+1}  " + ("largest local" if i == 0 else f"local #{i+1}"), 10, MUT))
    y += 62
    s.append(txt(40, y, "PAYER TYPES — recur across states", 11, INK, weight="bold"))
    y += 12
    for i, (n, c) in enumerate(P.PAYER_TYPE.items()):
        cx = 40 + i * 288
        s.append(rect(cx, y, 266, 26, c))
        s.append(txt(cx, y + 40, n, 10, MUT))
    y += 66

    # ---- Structural ----
    s.append(txt(40, y, "STRUCTURAL — not payers", 14, INK, weight="bold"))
    y += 24
    for i, (k, v) in enumerate([("Fee-for-service", "ffs"), ("Agency / the $100", "agency"),
                                ("Federal source", "federal"), ("State / local source", "local"),
                                ("Administration", "admin"), ("Plan admin & margin", "plan_admin")]):
        cx = 40 + i * 180
        s.append(rect(cx, y, 158, 26, P.STRUCTURAL[v]))
        s.append(txt(cx, y + 40, k, 10, MUT))
    y += 82

    # ---- Loss family ----
    s.append(txt(40, y, "LOSS FAMILY — HR-1 gap bands, never a baseline flow", 14, INK, weight="bold"))
    s.append(txt(40, y + 18, "Texture carries the meaning when colour cannot.", 11, MUT, italic=True))
    y += 40
    order = ["care_foregone", "out_of_pocket", "federal_offset",
             "state_local_offset", "provider_absorbed"]
    for i, k in enumerate(order):
        d = P.LOSS[k]
        cx = 40 + i * 250
        s.append(rect(cx, y, 228, 42, d["fill"], d["texture"]))
        words = d["label"].split()
        l1 = " ".join(words[:3]); l2 = " ".join(words[3:])
        s.append(txt(cx, y + 58, l1, 10, MUT))
        if l2: s.append(txt(cx, y + 71, l2, 10, MUT))
    # counterflow
    s.append(rect(40 + 5 * 250, y, 190, 42, P.COUNTERFLOW["fill"], P.COUNTERFLOW["texture"]))
    s.append(txt(40 + 5 * 250, y + 58, "Rural Health Transf.", 10, MUT))
    s.append(txt(40 + 5 * 250, y + 71, "Program (counterflow)", 10, MUT))
    y += 110

    # ---- Live slice ----
    s.append(txt(40, y, "LIVE SLICE — provider column into the five destinations", 14, INK, weight="bold"))
    y += 26
    x0, x1 = 300, 900
    s.append(rect(x0 - 130, y, 130, 250, P.STRUCTURAL["ffs"], op=0.55))
    s.append(txt(x0 - 124, y + 22, "Hospitals", 13, "#FFFFFF", weight="bold"))
    s.append(txt(x0 - 124, y + 38, "baseline", 10, "#FFFFFF", italic=True))

    # care that still flows (cool)
    s.append(band(x0, y, x1, y, 108, P.PAYER_CARRIER["Centene"], op=0.85))
    s.append(txt(x1 + 14, y + 58, "Care still delivered", 12, INK, weight="bold"))

    # five loss bands
    yy = y + 108
    ty = y + 118
    for k in order:
        d = P.LOSS[k]
        th = 26
        s.append(band(x0, yy, x1, ty, th, d["fill"], d["texture"], op=0.95))
        s.append(txt(x1 + 14, ty + 17, d["label"], 11, MUT))
        yy += th
        ty += th + 4

    s.append('</g></svg>')
    return "\n".join(s)

for g, fn in [(False, "palette_color.svg"), (True, "palette_grayscale.svg")]:
    open(fn, "w").write(sheet(g))

import cairosvg
for fn in ["palette_color", "palette_grayscale"]:
    cairosvg.svg2png(url=f"{fn}.svg", write_to=f"{fn}.png", output_width=1800)
print("rendered")
