"""Shared parts for taper diagrams, vertical and horizontal.

JW: there will be a lot of these, on the cover and in the body, and in every
state edition. The things that keep going wrong are not the arithmetic - that
comes off the ledger - but the same half-dozen layout decisions made slightly
differently each time: what unit a number is in, where a leader attaches, how
wide a label will print, whether the canvas is bigger than its content.

So they live here once. `taper.py` and `cover_taper.py` draw with these, and
`tapertest.py` checks every figure any of them produces against the same
invariants. A state edition should need a ledger and a spec, not a new
drawing program.

Two units, kept apart on purpose. `px(pt)` is a TYPE SIZE in points of printed
page; `mm(v)` is a DISTANCE in millimetres. One helper did both once and every
layout constant came out at a quarter of its intended size, because a
millimetre and a point are not the same unit and nothing in the code said
which was meant.
"""

PXMM = 11.7             # canvas pixels per millimetre of printed page
GLYPH = 0.52            # average glyph width as a fraction of type size

BLUE = "#17325c"
WARM = "#8B5A5A"
WARMD = "#6f4747"
EDGE = "#5c3a3a"
INK = "#1b1b1b"
MUT = "#6f6a64"
BG = "#ffffff"
RULE = "#ded7c8"
GHOST = "#ccd6e1"
GHOSTL = "#7d8fa3"
ONBLUE = "#d9e2ee"
F = "Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif"


def px(pt):
    """Type size, in POINTS of printed page."""
    return round(pt / 72 * 25.4 * PXMM)


def mm(v):
    """A distance on the page, in MILLIMETRES."""
    return round(v * PXMM)


def width(text, size):
    """How wide a string will print, near enough to place a leader against."""
    return len(str(text)) * size * GLYPH


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=14, fill=INK, a="start", w="normal", it=False, ls=0):
    st = ' font-style="italic"' if it else ""
    sp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{a}" font-weight="{w}"{st}{sp}>'
            f'{esc(s)}</text>')


def wrap(s, size, budget):
    """Greedy wrap on the average glyph width. Nothing here is justified, so
    the approximation is allowed to be one."""
    out, line = [], ""
    for word in str(s).split():
        trial = (line + " " + word).strip()
        if width(trial, size) > budget and line:
            out.append(line)
            line = word
        else:
            line = trial
    if line:
        out.append(line)
    return out


def attach(mx, x0, text, size):
    """Where a leader meets its amount: ALWAYS the end.

    The rule was first written as "the end nearest the diamond", and drawing
    it showed why that does not work: the near end alternates between the
    minus sign and the last digit from one row to the next, so the leaders
    stop in a ragged line and the eye reads the inconsistency before it reads
    the figure. They all meet the last digit now, and a leader that has to
    come from the left travels under its own row to get there rather than
    stopping short.

    Returns (x, side); side is +1 because the line always approaches the
    right-hand edge, so the caller offsets outward by a hair and does not
    print through the glyph.
    """
    return (x0 + width(text, size), +1)


def pack(desired, widths, lo, hi):
    """Place boxes as near their desired left edges as possible, in order,
    without overlap, inside [lo, hi]. Returns each box's left edge.

    This is isotonic regression under an order constraint, solved by the
    pool-adjacent-violators algorithm: the standard answer to label placement
    of this shape, and the method d3's label layouts and the cartographic
    labelling literature use. Written out rather than invented, because what
    was invented in its place moved the LINES to dodge the text instead of
    moving the text.

    Subtracting the width of everything before a box turns "must not overlap"
    into "must be non-decreasing", which is what PAVA solves. O(n), and
    optimal for total squared displacement.
    """
    n = len(desired)
    if not n:
        return []
    total = sum(widths)
    pre, acc = [], 0.0
    for w in widths:
        pre.append(acc)
        acc += w
    if total >= hi - lo:                      # no slack: lay them out packed
        return [lo + p for p in pre]

    want = [desired[i] - pre[i] for i in range(n)]
    vals, wts = [], []
    for v in want:
        vals.append(v)
        wts.append(1)
        while len(vals) > 1 and vals[-2] > vals[-1]:
            v2, w2 = vals.pop(), wts.pop()
            v1, w1 = vals.pop(), wts.pop()
            vals.append((v1 * w1 + v2 * w2) / (w1 + w2))
            wts.append(w1 + w2)
    flat = []
    for v, w in zip(vals, wts):
        flat += [v] * w
    out = [flat[i] + pre[i] for i in range(n)]

    # Slide the whole solution back inside the measure. PAVA respects the
    # order and the widths but knows nothing about the edges of the paper,
    # and a pooled block can carry the first label off the left of the
    # canvas - where it does not clip, it simply does not draw.
    if out[0] < lo:
        out = [v + (lo - out[0]) for v in out]
    if out[-1] + widths[-1] > hi:
        out = [v - (out[-1] + widths[-1] - hi) for v in out]
    if out[0] < lo:                          # cannot satisfy both: pack tight
        out = [lo + p for p in pre]
    return out


def leader(mx, my, x0, text, size, ly, rail=None, stroke=GHOSTL, w=None):
    """A leader from a marker to the end of its own amount.

    Routed down a rail rather than run diagonally across the label block. A
    diagonal is shorter and looks better in isolation, and it crossed the
    labels of every entry it passed on the way: descending inside a column of
    text means descending THROUGH it. The rail is a vertical clear of the
    widest label, so the only thing the line crosses is the empty paper to the
    right of its own amount.

    Without a rail it falls back to a stub and one diagonal, which is right
    when there is nothing between the marker and the amount.
    """
    # JW's rule: if the amount can be reached by going straight down, go
    # straight down and stop. A line that drops and then turns reads as a
    # route; a line that just drops reads as a pointer, and most of these only
    # ever needed to be a pointer. The turn is for the ones that genuinely
    # have to travel - a marker sitting outside its own amount's hit box.
    x1 = x0 + width(text, size)
    ay = ly - mm(1.2)
    if x0 - mm(1) <= mx <= x1 + mm(1):
        d = f"M{mx:.1f},{my:.1f} L{mx:.1f},{ay:.1f}"
    else:
        ax, side = attach(mx, x0, text, size)
        ax += side * mm(1.6)
        # The turn sits just above the amount's own line, so the vertical does
        # the travelling and the diagonal is short. Turning early and running
        # a long diagonal put a line through the label of every entry it
        # passed on the way.
        turn = ay - mm(1.1)
        d = f"M{mx:.1f},{my:.1f} L{mx:.1f},{turn:.1f} L{ax:.1f},{ay:.1f}"
    return (f'<path d="{d}" fill="none" stroke="{stroke}" '
            f'stroke-width="{w or mm(0.28):.1f}"/>')


def diamond(cx, cy, r, fill=WARM, edge=EDGE, w=None):
    """The decrement mark. Fixed size, never proportional: a proportional
    mark makes a small value disappear."""
    return (f'<path d="M{cx:.1f},{cy-r:.1f} L{cx+r:.1f},{cy:.1f} '
            f'L{cx:.1f},{cy+r:.1f} L{cx-r:.1f},{cy:.1f} Z" '
            f'fill="{fill}" stroke="{edge}" stroke-width="{w or mm(0.4):.1f}"/>')


def svg(name, title, desc, w, h, body, bg=BG):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t_{name} d_{name}">'
            f'<title id="t_{name}">{esc(title)}</title>'
            f'<desc id="d_{name}">{esc(desc)}</desc>'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>'
            + body + "</svg>")
