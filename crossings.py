#!/usr/bin/env python3
"""crossings.py — geometric crossing gate for rule 2.9.

    python3 crossings.py                      # every render
    python3 crossings.py national_2030_mixed

JW, 2026-09-03: "The 'wanting to avoid crossings' rule doesn't apply when it's
crossing from the middle of the diagram. Obviously those have to cross and should
cross. The rule is only for tributaries that come off the main streams and are on
the edges. The duals don't become tributaries for the sake of this rule until they
get to the edge to terminate early."

So the rule is scoped by REGION, not by which element it is. Every band has a
stretch inside the main flow body and, if it is a tributary, a stretch out in the
margin above or below it. Crossings are counted ONLY where both curves are in the
margin. A ribbon leaving the middle of the stack has to cut across whatever sits
between it and the edge; that is the flow working, not a layout defect.

The margin is derived from the render, not declared: the main flow body is the
vertical extent of the main lane colours at each x, and anything outside that
envelope is margin.
"""
import itertools
import os
import re
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(REPO, "reference_renders")

# Main flow colours: federal, state, trunk, MCO, dual, FFS. These define the body.
BODY = {"#2f5d74", "#9bb8c4", "#1a6b40", "#3f8f8a", "#9a6fa6", "#5f7f96"}
SAMPLES = 160
PAD = 4.0          # a curve grazing the body edge is still in the body


def _cub(p0, c1, c2, p3, n=SAMPLES):
    return [((1-t)**3*p0[0] + 3*(1-t)**2*t*c1[0] + 3*(1-t)*t*t*c2[0] + t**3*p3[0],
             (1-t)**3*p0[1] + 3*(1-t)**2*t*c1[1] + 3*(1-t)*t*t*c2[1] + t**3*p3[1])
            for t in [i/n for i in range(n+1)]]


def _seg_x(a, b, c, d):
    cr = lambda o, p, q: (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
    return ((cr(c, d, a) > 0) != (cr(c, d, b) > 0)) and \
           ((cr(a, b, c) > 0) != (cr(a, b, d) > 0))


BAND = re.compile(
    r'<path d="M([\d.-]+),([\d.-]+) C([\d.-]+),([\d.-]+) ([\d.-]+),([\d.-]+) '
    r'([\d.-]+),([\d.-]+) L([\d.-]+),([\d.-]+) C[^"]*? ([\d.-]+),([\d.-]+) Z" '
    r'fill="([#\w]+)"')
STROKE = re.compile(
    r'<path d="M([\d.-]+),([\d.-]+) C([\d.-]+),([\d.-]+) ([\d.-]+),([\d.-]+) '
    r'([\d.-]+),([\d.-]+)" fill="none" stroke="([#\w]+)"')


def load(svg):
    """Return [(top_polyline, bottom_polyline, centre, colour, label)]."""
    out = []
    for m in BAND.finditer(svg):
        g = [float(v) for v in m.groups()[:12]]
        x0, y0, c1x, c1y, c2x, c2y, x1, y1, _lx, ly, _bx, y0b = g
        h0, h1 = y0b - y0, ly - y1
        top = _cub((x0, y0), (c1x, c1y), (c2x, c2y), (x1, y1))
        bot = _cub((x0, y0+h0), (c1x, c1y+h0), (c2x, c2y+h1), (x1, y1+h1))
        mid = _cub((x0, y0+h0/2), (c1x, c1y+h0/2), (c2x, c2y+h1/2), (x1, y1+h1/2))
        out.append((top, bot, mid, m.group(13),
                    f"{m.group(13)} ({x0:.0f},{y0:.0f})->({x1:.0f},{y1:.0f})"))
    for m in STROKE.finditer(svg):
        g = [float(v) for v in m.groups()[:8]]
        mid = _cub((g[0], g[1]), (g[2], g[3]), (g[4], g[5]), (g[6], g[7]))
        out.append((mid, mid, mid, m.group(9),
                    f"{m.group(9)} ({g[0]:.0f},{g[1]:.0f})->({g[6]:.0f},{g[7]:.0f}) stroke"))
    return out


def envelope(curves, step=4.0):
    """Vertical extent of the main flow body, per x bucket."""
    env = {}
    for top, bot, _mid, col, _lab in curves:
        if col not in BODY:
            continue
        for (x, yt), (_x2, yb) in zip(top, bot):
            k = int(x // step)
            lo, hi = env.get(k, (1e9, -1e9))
            env[k] = (min(lo, yt), max(hi, yb))
    return env


def in_body(env, x, y, step=4.0):
    e = env.get(int(x // step))
    return e is not None and (e[0] - PAD) <= y <= (e[1] + PAD)


def report(path):
    svg = open(path).read()
    curves = load(svg)
    env = envelope(curves)
    hits = []
    for (t1, b1, m1, c1, l1), (t2, b2, m2, c2, l2) in itertools.combinations(curves, 2):
        # Two ribbons that hand off to each other share an endpoint. The shared
        # point registers as an intersection; it is a join, not a crossing.
        ends1 = (m1[0], m1[-1]); ends2 = (m2[0], m2[-1])
        if any(abs(a[0]-b[0]) < 1.5 and abs(a[1]-b[1]) < 1.5
               for a in ends1 for b in ends2):
            continue
        for i in range(len(m1)-1):
            a, b = m1[i], m1[i+1]
            for j in range(len(m2)-1):
                c, d = m2[j], m2[j+1]
                if not _seg_x(a, b, c, d):
                    continue
                mx, my = (a[0]+b[0]+c[0]+d[0])/4, (a[1]+b[1]+c[1]+d[1])/4
                if in_body(env, mx, my):
                    continue              # rule 2.9c: middle of the diagram is exempt
                hits.append((l1, l2, mx, my))
                break
            else:
                continue
            break
    return hits


def main():
    names = sys.argv[1:] or [f[:-13] for f in sorted(os.listdir(R))
                             if f.endswith("_combined.svg")]
    bad = 0
    for n in names:
        p = os.path.join(R, f"{n}_combined.svg")
        if not os.path.exists(p):
            continue
        h = report(p)
        bad += len(h)
        print(f"{n:28s} {len(h)} crossing(s) in the margin")
        for l1, l2, x, y in h:
            print(f"    at ({x:.0f},{y:.0f})  {l1}  x  {l2}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
