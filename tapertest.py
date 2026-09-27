"""Check every taper diagram, without looking at it.

JW: there will be a lot of these, vertical and horizontal, and one set per
state edition. Every layout fault found so far has been found by eye - text
printed on top of art, a label running off the canvas, a leader drawn through
the line above it, a figure drawn on paper taller than its own content. None
of them showed up in any instrument, because the instruments measure the PAGE
and these are faults inside the picture.

    python3 tapertest.py [dir]

Reads the generated SVGs rather than the scripts, so it checks what was
actually drawn and works the same for a state edition that draws its own.
Four tests:

  off-canvas   a text element whose box leaves the viewBox. An SVG has no
               page boundary, so this does not clip - it simply does not draw,
               which is how a label goes missing without anything failing.
  overlap      two text elements whose boxes intersect. This is the "$25.17
               printed on top of the outline" fault, and the "leader through
               the label above it" fault seen from the text's side.
  leader       every leader ends at one END OF AN AMOUNT, the end nearest its
               own marker. That is the rule; this is whether the drawing kept
               it.
  on-the-line  a leader that passes through a text box. JW's rule is that the
               lines go down first and the type is then placed clear of them;
               this is whether the placement held. Z-order saves the
               legibility of the glyph but not the look of a rule running out
               of a word.
  empty        a figure with no text at all, which means the generator ran and
               produced furniture.

Boxes are estimated from the font size and the same average glyph width the
generators wrap with, so the overlap test is approximate in the same direction
the layout is. It is tuned to catch a collision a reader would see, not to
prove two glyphs never touch.
"""
import glob
import os
import re
import sys

import taperkit as TK

TEXT = re.compile(
    r'<text x="([-\d.]+)" y="([-\d.]+)"[^>]*font-size="([\d.]+)"[^>]*'
    r'text-anchor="(\w+)"[^>]*>(.*?)</text>')
VIEWBOX = re.compile(r'viewBox="0 0 ([\d.]+) ([\d.]+)"')
# Only an unfilled path is a leader. The first version of this matched any
# path with two corners in it and so measured the rhombus markers themselves,
# then reported the figure for failing a rule about a line it had not drawn.
PATH = re.compile(r'<path d="(M[^"]+)"[^>]*fill="none"')
PT = re.compile(r'[ML]([-\d.]+),([-\d.]+)')
# A leader may also be a plain horizontal rule, which is how the vertical
# cover taper draws it.
LINE = re.compile(
    r'<line x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"')
# One level of translate, which is how a figure with its masthead removed
# lifts the rest of the drawing into the space. Ignoring it made every element
# inside the group look as though it had left the canvas.
GROUP = re.compile(r'<g transform="translate\(([-\d.]+),([-\d.]+)\)">(.*?)</g>',
                   re.S)
AMOUNT = re.compile(r"^\u2212\$[\d.]+$")
PAD = 2.0               # a couple of pixels of slack before calling a touch


def flatten(svg):
    """Apply one level of translate, so coordinates mean what they render."""
    def sub(m):
        dx, dy, inner = float(m.group(1)), float(m.group(2)), m.group(3)
        inner = TEXT.sub(
            lambda t: t.group(0).replace(f'x="{t.group(1)}"',
                                         f'x="{float(t.group(1))+dx:.1f}"', 1)
                              .replace(f'y="{t.group(2)}"',
                                       f'y="{float(t.group(2))+dy:.1f}"', 1),
            inner)
        return inner
    return GROUP.sub(sub, svg)


def boxes(svg):
    out = []
    for x, y, size, anchor, txt in TEXT.findall(svg):
        x, y, size = float(x), float(y), float(size)
        w = TK.width(re.sub(r"&[a-z]+;", "x", txt), size)
        x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle"
                                          else x - w)
        out.append((x0, y - size * 0.78, x0 + w, y + size * 0.24, txt))
    return out


def seg_hits(ax, ay, bx, by, x0, y0, x1, y1):
    """Does the segment cross the box? Clipped, not bounded."""
    x0, y0, x1, y1 = x0 + PAD, y0 + PAD, x1 - PAD, y1 - PAD
    if x1 <= x0 or y1 <= y0:
        return False
    t0, t1 = 0.0, 1.0
    dx, dy = bx - ax, by - ay
    for p, q in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
        if p == 0:
            if q < 0:
                return False
            continue
        r = q / p
        if p < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return False
    return True


def check(path):
    svg = flatten(open(path).read())
    m = VIEWBOX.search(svg)
    W, H = (float(m.group(1)), float(m.group(2))) if m else (0, 0)
    bs = boxes(svg)
    bad = []

    if not bs:
        return [f"{os.path.basename(path)}: no text at all"]

    for x0, y0, x1, y1, txt in bs:
        if x0 < -PAD or x1 > W + PAD or y0 < -PAD or y1 > H + PAD:
            bad.append(f"{os.path.basename(path)}: {txt[:34]!r} leaves the "
                       f"canvas")

    for i, a in enumerate(bs):
        for b in bs[i + 1:]:
            if (a[0] < b[2] - PAD and b[0] < a[2] - PAD
                    and a[1] < b[3] - PAD and b[1] < a[3] - PAD):
                bad.append(f"{os.path.basename(path)}: {a[4][:26]!r} overlaps "
                           f"{b[4][:26]!r}")

    # Every leader should land on one end of an amount, whichever is nearer
    # the marker it came from.
    amounts = [b for b in bs if AMOUNT.match(b[4].replace("&minus;", "\u2212"))]
    # Every corner of every unfilled path, so a leader can be tested segment
    # by segment. Testing its bounding box instead called an L-shaped leader a
    # collision with everything in the rectangle it happened to span, which is
    # most of the figure.
    polys = [[(float(x), float(y)) for x, y in PT.findall(d)]
             for d in PATH.findall(svg)]
    leaders = [(p[0][0], p[0][1], p[-1][0], p[-1][1]) for p in polys if p]
    # For a plain horizontal rule the endpoints carry no order, and the first
    # version of this took x1 as the marker. On the vertical taper the line is
    # short and x1 already sits past the marker, so a leader that obeys the
    # rule was reported as breaking it. The marker end is simply the endpoint
    # FARTHER from the label.
    for a, b, c, d in LINE.findall(svg):
        x1, y1, x2, y2 = float(a), float(b), float(c), float(d)
        if abs(y1 - y2) > 1:
            continue
        near_amt = [q for q in amounts if abs((q[1] + q[3]) / 2 - y1) < 14]
        if not near_amt:
            continue
        q = min(near_amt, key=lambda q: min(abs(q[0] - x2), abs(q[2] - x2)))
        cen = (q[0] + q[2]) / 2
        mx, ex = (x1, x2) if abs(x1 - cen) > abs(x2 - cen) else (x2, x1)
        # A horizontal rule at the same height as an amount is not
        # necessarily a leader to it: the taper body is drawn with them too.
        # Only a line that actually ARRIVES at one end of the amount is one.
        if min(abs(ex - q[0]), abs(ex - q[2])) > TK.mm(4):
            continue
        leaders.append((mx, y1, ex, y1))
        polys.append([(mx, y1), (ex, y1)])
    for mx, my, ex, ey in leaders:
        near = [a for a in amounts if abs((a[1] + a[3]) / 2 - ey) < 14]
        if not near:
            continue
        a = min(near, key=lambda a: min(abs(a[0] - ex), abs(a[2] - ex)))
        # The rule is "the end of the amount", and the end is where the
        # amount stops being the only thing on its line. On the vertical
        # taper the label runs on from the amount, so the end of the amount
        # is the start of a word and a leader has to stop at the front of it;
        # on the horizontal ones the amount has its line to itself. Inferred
        # from the drawing rather than declared, so a state edition that
        # lays out either way is checked correctly without telling this file
        # which it chose.
        # JW's rule has two cases. A leader whose marker sits over its own
        # amount goes straight down and stops inside the hit box; only one
        # that has to travel is held to landing on the end.
        if abs(mx - ex) < 1 and a[0] - TK.mm(1.5) <= ex <= a[2] + TK.mm(1.5):
            continue
        size = (a[3] - a[1]) / 1.02
        # Inline means the amount's OWN label runs on from it: something on
        # the same baseline, close, AND nothing starting under it at its own
        # left edge. Without that second half, a neighbouring block packed
        # alongside looked like a continuation and every leader in a
        # single-row layout was judged against the wrong end.
        follows = any(q is not a
                      and abs((q[1] + q[3]) / 2 - (a[1] + a[3]) / 2) < 6
                      and 0 < q[0] - a[2] < TK.mm(6) for q in bs)
        stacked = any(q is not a and abs(q[0] - a[0]) < TK.mm(1.5)
                      and 0 < q[1] - a[3] < TK.mm(6) for q in bs)
        inline = follows and not stacked
        want = a[0] if inline else TK.attach(mx, a[0], a[4], size)[0]
        if abs(ex - want) > TK.mm(3.5):
            bad.append(f"{os.path.basename(path)}: leader for {a[4]!r} lands "
                       f"at {ex:.0f}, not the end nearest its marker "
                       f"({want:.0f})")
    # Does any leader run through any label? Segment by segment.
    seen = set()
    for poly in polys:
        for (ax, ay), (bx, by) in zip(poly, poly[1:]):
            for bx0, by0, bx1, by1, txt in bs:
                if AMOUNT.match(txt.replace("&minus;", "\u2212")):
                    continue              # a leader ends AT its own amount
                if seg_hits(ax, ay, bx, by, bx0, by0, bx1, by1) \
                        and txt not in seen:
                    seen.add(txt)
                    bad.append(f"{os.path.basename(path)}: a leader runs "
                               f"through {txt[:30]!r}")
    return bad


def main(d="cover"):
    files = [f for f in sorted(glob.glob(os.path.join(d, "*.svg")))
             if "_standalone" not in f]
    if not files:
        print(f"NO DIAGRAMS FOUND in {d}/. This file cannot check drawings it "
              f"cannot see.")
        return 1
    bad = []
    for f in files:
        bad += check(f)
    for line in bad:
        print("  " + line)
    print(f"\n{len(bad)} fault(s) across {len(files)} diagrams" if bad else
          f"\nno text leaves its canvas, no two labels collide and every "
          f"leader lands where the rule says, across {len(files)} diagrams")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "cover"))
