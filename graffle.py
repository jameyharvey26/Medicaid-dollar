#!/usr/bin/env python3
"""graffle.py — convert a rendered instance SVG into an OmniGraffle document.

    python3 graffle.py national_2030_mixed
    python3 graffle.py national_2024 --out foo.graffle

This is an EXPORT, not a second renderer. The SVG remains authoritative: nothing
is ever read back from a .graffle into the ledger, because a figure that can be
typed over in a drawing tool is not a sourced figure (STYLE_GUIDE 6.1, S-073).
The .graffle exists so JW can mark up geometry and leave notes; those notes come
back as instructions, and any change lands in `sankey.py` or `instances.py`.

The SVG's two groups become two OmniGraffle LAYERS, `baseline` and `hr1_overlay`,
so the HR-1 ribbons can be toggled off to see the prior-law diagram underneath.

Known lossy points, all declared rather than silently approximated:
  - The HR-1 hatch fill (`pattern#hr1hatch`) has no OmniGraffle equivalent. It is
    flattened to the warm solid at the pattern's own opacity. Ribbons will read
    slightly flatter than the PNG.
  - SVG elliptical arcs (pie slices) are flattened to cubic beziers.
  - Font falls back to Helvetica; the render specifies Segoe UI first.
"""
import argparse
import math
import os
import plistlib
import re
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(REPO, "reference_renders")

HATCH_SOLID = "#6f4747"
HATCH_OPACITY = 0.55


# ------------------------------------------------------------------ colour
def rgb(c, default=(0, 0, 0)):
    if not c or c in ("none", "transparent"):
        return None
    c = c.strip()
    if c.startswith("url("):
        c = HATCH_SOLID
    if c.startswith("#"):
        h = c[1:]
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    named = {"white": (1, 1, 1), "black": (0, 0, 0), "red": (1, 0, 0)}
    return named.get(c, tuple(v / 255.0 for v in default))


def color_dict(t):
    return {"r": f"{t[0]:.5f}", "g": f"{t[1]:.5f}", "b": f"{t[2]:.5f}", "a": "1"}


def style(fill=None, stroke=None, width=1.0, opacity=None):
    s = {}
    if fill:
        f = {"Color": color_dict(fill)}
        if opacity is not None:
            f["Color"]["a"] = f"{opacity:.3f}"
        s["fill"] = f
    else:
        s["fill"] = {"Draws": "NO"}
    if stroke:
        s["stroke"] = {"Color": color_dict(stroke), "Width": float(width)}
    else:
        s["stroke"] = {"Draws": "NO"}
    return s


# ------------------------------------------------------------------ paths
def arc_to_beziers(x0, y0, rx, ry, rot, large, sweep, x, y):
    """SVG elliptical arc -> list of cubic segments [(c1,c2,end), ...]."""
    if rx == 0 or ry == 0 or (x0 == x and y0 == y):
        return [((x0, y0), (x, y), (x, y))]
    phi = math.radians(rot)
    cs, sn = math.cos(phi), math.sin(phi)
    dx2, dy2 = (x0 - x) / 2.0, (y0 - y) / 2.0
    x1p, y1p = cs * dx2 + sn * dy2, -sn * dx2 + cs * dy2
    rx, ry = abs(rx), abs(ry)
    lam = x1p * x1p / (rx * rx) + y1p * y1p / (ry * ry)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    co = math.sqrt(max(num / den, 0.0))
    if large == sweep:
        co = -co
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx, cyc = cs * cxp - sn * cyp + (x0 + x) / 2.0, sn * cxp + cs * cyp + (y0 + y) / 2.0

    def ang(ux, uy, vx, vy):
        d = (math.hypot(ux, uy) * math.hypot(vx, vy))
        a = math.acos(max(-1.0, min(1.0, (ux * vx + uy * vy) / d))) if d else 0.0
        return -a if ux * vy - uy * vx < 0 else a

    th1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dth = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dth > 0:
        dth -= 2 * math.pi
    elif sweep and dth < 0:
        dth += 2 * math.pi

    n = max(1, int(math.ceil(abs(dth) / (math.pi / 2))))
    out, d = [], dth / n
    t = 4 / 3 * math.tan(d / 4)
    for i in range(n):
        a1, a2 = th1 + i * d, th1 + (i + 1) * d

        def pt(a):
            return (cs * rx * math.cos(a) - sn * ry * math.sin(a) + cx,
                    sn * rx * math.cos(a) + cs * ry * math.sin(a) + cyc)

        def dv(a):
            return (-cs * rx * math.sin(a) - sn * ry * math.cos(a),
                    -sn * rx * math.sin(a) + cs * ry * math.cos(a))

        p1, p2 = pt(a1), pt(a2)
        d1, d2 = dv(a1), dv(a2)
        out.append(((p1[0] + t * d1[0], p1[1] + t * d1[1]),
                    (p2[0] - t * d2[0], p2[1] - t * d2[1]), p2))
    return out


TOK = re.compile(r"([MmLlHhVvCcSsQqAaZz])|(-?\d*\.?\d+(?:e-?\d+)?)")


def parse_path(d):
    """-> list of subpaths, each a list of ('M'|'C', points...) in absolute coords."""
    toks = [(a or b) for a, b in TOK.findall(d)]
    i, cur, start = 0, (0.0, 0.0), (0.0, 0.0)
    subs, seg, cmd = [], [], None

    def num():
        nonlocal i
        v = float(toks[i]); i += 1
        return v

    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]; i += 1
        rel = cmd.islower()
        c = cmd.upper()
        if c == "M":
            if seg:
                subs.append(seg)
            x, y = num(), num()
            if rel:
                x, y = cur[0] + x, cur[1] + y
            cur = start = (x, y)
            seg = [("M", cur)]
            cmd = "l" if rel else "L"
        elif c == "L":
            x, y = num(), num()
            if rel:
                x, y = cur[0] + x, cur[1] + y
            seg.append(("C", cur, (x, y), (x, y)))
            cur = (x, y)
        elif c == "H":
            x = num()
            x = cur[0] + x if rel else x
            seg.append(("C", cur, (x, cur[1]), (x, cur[1])))
            cur = (x, cur[1])
        elif c == "V":
            y = num()
            y = cur[1] + y if rel else y
            seg.append(("C", cur, (cur[0], y), (cur[0], y)))
            cur = (cur[0], y)
        elif c == "C":
            p = [(num(), num()) for _ in range(3)]
            if rel:
                p = [(cur[0] + a, cur[1] + b) for a, b in p]
            seg.append(("C", p[0], p[1], p[2]))
            cur = p[2]
        elif c == "A":
            rx, ry, rot, la, sw, x, y = (num(), num(), num(), num(), num(), num(), num())
            if rel:
                x, y = cur[0] + x, cur[1] + y
            for c1, c2, e in arc_to_beziers(cur[0], cur[1], rx, ry, rot, int(la), int(sw), x, y):
                seg.append(("C", c1, c2, e))
            cur = (x, y)
        elif c == "Z":
            if cur != start:
                seg.append(("C", cur, start, start))
            cur = start
        else:
            num()
    if seg:
        subs.append(seg)
    return subs


# ------------------------------------------------------------------ graphics
class Doc:
    def __init__(self):
        self.g, self.nid = [], 0

    def _id(self):
        self.nid += 1
        return self.nid

    def add(self, d, layer):
        d["ID"] = self._id()
        d["Layer"] = layer
        self.g.append(d)

    def rect(self, x, y, w, h, st, layer, rx=0):
        self.add({"Class": "ShapedGraphic",
                  "Shape": "RoundRect" if rx else "Rectangle",
                  "Bounds": f"{{{{{x:.2f}, {y:.2f}}}, {{{max(w,0.01):.2f}, {max(h,0.01):.2f}}}}}",
                  "Style": st}, layer)

    def circle(self, cx, cy, r, st, layer):
        self.add({"Class": "ShapedGraphic", "Shape": "Circle",
                  "Bounds": f"{{{{{cx-r:.2f}, {cy-r:.2f}}}, {{{2*r:.2f}, {2*r:.2f}}}}}",
                  "Style": st}, layer)

    def line(self, x1, y1, x2, y2, st, layer):
        self.add({"Class": "LineGraphic",
                  "Points": [f"{{{x1:.2f}, {y1:.2f}}}", f"{{{x2:.2f}, {y2:.2f}}}"],
                  "Style": st}, layer)

    def bezier(self, subs, st, layer):
        for seg in subs:
            pts = [p for p in seg[0][1:]]
            for s in seg[1:]:
                pts.extend(s[1:])
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            x0, y0, w, h = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
            w, h = max(w, 0.01), max(h, 0.01)
            unit = [f"{{{(p[0]-x0)/w:.5f}, {(p[1]-y0)/h:.5f}}}" for p in pts]
            self.add({"Class": "ShapedGraphic", "Shape": "Bezier",
                      "Bounds": f"{{{{{x0:.2f}, {y0:.2f}}}, {{{w:.2f}, {h:.2f}}}}}",
                      "ShapeData": {"UnitPoints": unit, "PathIsClosed": "YES"},
                      "Style": st}, layer)

    def text(self, x, y, s, size, col, anchor, bold, italic, layer):
        s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if not s.strip():
            return
        w = max(len(s) * size * 0.62, 12)
        align = {"start": 0, "middle": 2, "end": 1}.get(anchor, 0)
        ox = {"start": 0, "middle": -w / 2, "end": -w}[anchor if anchor in
                                                       ("start", "middle", "end") else "start"]
        face = "Helvetica"
        if bold and italic:
            face = "Helvetica-BoldOblique"
        elif bold:
            face = "Helvetica-Bold"
        elif italic:
            face = "Helvetica-Oblique"
        rtf = (r"{\rtf1\ansi\ansicpg1252\deff0{\fonttbl\f0\fnil " + face + r";}"
               r"{\colortbl;\red" + str(int(col[0] * 255)) + r"\green" +
               str(int(col[1] * 255)) + r"\blue" + str(int(col[2] * 255)) + r";}"
               r"\pard\qc\f0\fs" + str(int(round(size * 2))) + r"\cf1 " +
               s.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}") + "}")
        self.add({"Class": "ShapedGraphic", "Shape": "Rectangle",
                  "Bounds": f"{{{{{x+ox:.2f}, {y-size:.2f}}}, {{{w:.2f}, {size*1.5:.2f}}}}}",
                  "Style": {"fill": {"Draws": "NO"}, "stroke": {"Draws": "NO"}},
                  "FitText": "YES", "Wrap": "NO",
                  "Text": {"Text": rtf, "Align": align, "VerticalPad": 0}}, layer)


ATTR = re.compile(r'([a-zA-Z_][\w:.-]*)="([^"]*)"')  # names carry digits: x1, y2


def attrs(tag):
    return dict(ATTR.findall(tag))


def convert(svg_path, out_path):
    src = open(svg_path).read()
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', src)
    W, H = (int(vb.group(1)), int(vb.group(2))) if vb else (2200, 1240)

    doc = Doc()
    layer = 0
    layers_seen = ["baseline"]
    body = re.sub(r"<defs>.*?</defs>", "", src, flags=re.S)

    for m in re.finditer(r'<(g|rect|line|circle|path|text)\b([^>]*?)(/?)>'
                         r'(?:([^<]*)</text>)?', body, re.S):
        tag, raw, _, inner = m.group(1), m.group(2), m.group(3), m.group(4)
        a = attrs("<" + tag + raw + ">")
        if tag == "g":
            gid = a.get("id", "")
            if gid and gid not in layers_seen:
                layers_seen.append(gid)
            layer = layers_seen.index(gid) if gid in layers_seen else layer
            continue

        op = a.get("opacity") or a.get("fill-opacity")
        op = float(op) if op else None
        fill_raw = a.get("fill")
        if fill_raw and fill_raw.startswith("url("):
            op = HATCH_OPACITY
        fill = rgb(fill_raw) if fill_raw is not None else (rgb("#000") if tag == "text" else None)
        stroke = rgb(a.get("stroke")) if a.get("stroke") else None
        sw = float(a.get("stroke-width", 1) or 1)
        st = style(fill, stroke, sw, op)

        try:
            if tag == "rect":
                doc.rect(float(a["x"]), float(a["y"]), float(a["width"]),
                         float(a["height"]), st, layer, float(a.get("rx", 0) or 0))
            elif tag == "line":
                doc.line(float(a["x1"]), float(a["y1"]), float(a["x2"]),
                         float(a["y2"]), style(None, stroke or (0, 0, 0), sw, op), layer)
            elif tag == "circle":
                doc.circle(float(a["cx"]), float(a["cy"]), float(a["r"]), st, layer)
            elif tag == "path":
                if a.get("d"):
                    doc.bezier(parse_path(a["d"]), st, layer)
            elif tag == "text":
                doc.text(float(a.get("x", 0)), float(a.get("y", 0)), (inner or "").strip(),
                         float(a.get("font-size", 12)), fill or (0, 0, 0),
                         a.get("text-anchor", "start"),
                         a.get("font-weight") == "bold",
                         a.get("font-style") == "italic", layer)
        except (KeyError, ValueError) as e:
            print(f"  skipped <{tag}>: {e}")

    plist = {
        "GraphDocumentVersion": 12,
        "ApplicationVersion": ["com.omnigroup.OmniGrafflePro", "7.0"],
        "ReadOnly": "NO",
        "CanvasSize": f"{{{W}, {H}}}",
        "CanvasColor": {"w": "1"},
        "GridInfo": {"ShowsGrid": "NO"},
        "Layers": [{"Lock": "NO", "Name": n, "Print": "YES", "View": "YES"}
                   for n in layers_seen],
        "GraphicsList": doc.g,
    }
    with open(out_path, "wb") as fh:
        plistlib.dump(plist, fh, fmt=plistlib.FMT_XML)
    return len(doc.g), layers_seen, (W, H)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("instance", nargs="?", default="national_2030_mixed")
    ap.add_argument("--out")
    a = ap.parse_args()
    svg = os.path.join(R, f"{a.instance}_combined.svg")
    if not os.path.exists(svg):
        sys.exit(f"no such render: {svg}\nrun  python3 build.py  first.")
    out = a.out or os.path.join(R, f"{a.instance}.graffle")
    n, layers, size = convert(svg, out)
    print(f"wrote {out}")
    print(f"  {n} objects, layers {layers}, canvas {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
