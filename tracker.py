#!/usr/bin/env python3
"""tracker.py — the bottom ledger, on one lattice, for every diagram.

JW, 2026-09-03. The tracker stops being four fixed milestones and becomes a
running ledger: a dot wherever a number changes, and nowhere else. 2024 has
fewer dots than 2030 because it has fewer bites, and the gaps ARE the comparison.

ONE COLUMN SYSTEM. The flow columns are the system. Their right edges are the
endpoints and their centres are the connectors, so a column splits into two
sub-columns and can carry up to two subtractions. Nothing else is a position.

SLOT RULE. A subtraction is charged to the column where the money leaves the
flow, and it takes a slot in that column: the right edge if it is the only one,
centre then right edge if there are two. Tributaries terminate on the same slot,
so the tracker and the ribbons stop answering different questions.

THE LAST SUBTRACTION always lands on the delivered dot at the centre of the
beneficiary column. It is the most important dot on the artifact, and putting the
final subtraction there means the value never has to be printed twice.

CLASSES carry colour, in the dots, the values and the amounts alike:
    hr1 brown | admin grey | fraud red
"""
from outflows import COLS, TRACKER_ANCHORS, anchor_x

# ---- palette -------------------------------------------------------------
INK = "#111418"
HR1 = "#8B5A5A"
ADMIN = "#5c6169"      # darkened from #8e9298 at JW's instruction
FRAUD = "#b23a32"
SUBTLE = "#54585f"     # darkened from #6f6f6f

COLOUR = {"hr1": HR1, "admin": ADMIN, "fraud": FRAUD}

# ---- geometry ------------------------------------------------------------
from outflows import RULE_Y   # declared with the layout spine, not here
BY = RULE_Y + 82.0     # the ledger line, at its established offset below the rule
AMT_Y = -116.0         # subtraction amount, in the span it was taken in
AMT_LAB_Y = -96.0
AMT_LAB_Y2 = -78.0     # second label row, when two labels would collide
VAL_Y = -22.0          # the running balance, on its dot
VAL_STAGGER = -58.0    # second row, when two dots sit too close to share one
# Three rows below the line, each with one job, because sharing a row breaks the
# moment a year has more bites in it.
NAME_Y = 32.0          # balance's phase name
NAME_LEAD = 26.0       # second line of a two-line phase name
PCT_Y = 30.0           # percentage lost, measured from the LAST title line
SHORT_Y = 102.0        # bite's short name, its own row
SHORT_LEAD = 26.0      # second line of a wrapped short name
TITLE_PX = 22
SHORT_PX = 22
PCT_PX = 15
VAL_W = 156.0          # approximate width of a $NN.NN at 36px
START_COL = "FEDERAL"  # $100 sits at this column's centre
FINAL_COL = "BENEFICIARY"


def centre(col):
    a, b = COLS[col]
    return (a + b) / 2.0


def edge(col):
    return float(COLS[col][1])


def lattice():
    """Every candidate slot, left to right. Nothing may sit off it."""
    out = []
    for col in COLS:
        out += [centre(col), edge(col)]
    return sorted(set([float(COLS[c][0]) for c in COLS] + out))


def assign(subtractions):
    """subtractions: [(label, amount, cls, column, short)] in flow order.

    Each bite owns a column. Its SUBTRACTION dot sits at that column's left edge
    and its BALANCE dot at the right edge, so the line alternates bite, balance,
    bite, balance. The last balance is forced to the delivered dot at the centre
    of the beneficiary column.

    Where two bites share a column the column splits at its centre and each half
    is treated the same way.
    """
    live = [s for s in subtractions if s[1] > 0.004]
    out = []
    for i, rec in enumerate(live):
        lab, amt, cls, col, short = rec
        # A column carrying k bites divides into 2k-1 equal steps, giving 2k
        # alternating slots: bite, balance, bite, balance. The sub-columns are
        # invisible — no rule is drawn for them — but the cadence never breaks,
        # however many bites land in one column. k=1 collapses to the column's
        # own edges, which is why the simple case still reads as the lattice.
        share = [k for k, r in enumerate(live) if r[3] == col]
        k = len(share); n = share.index(i)
        a, b = float(COLS[col][0]), float(COLS[col][1])
        step = (b - a) / (2 * k - 1)
        lo, hi = a + 2 * n * step, a + (2 * n + 1) * step
        out.append(dict(x_sub=lo, x_edge=hi, label=lab, short=short,
                        amount=amt, cls=cls))

    # Balances are placed only once every bite anchor is known, because a balance
    # must land strictly between its own bite and the next one. The sub-column's
    # right edge is preferred — it keeps the balance on the lattice where it can
    # — and the midpoint is the fallback when the next bite sits on that edge.
    for i, rec in enumerate(out):
        if i == len(out) - 1:
            rec["x_bal"] = centre(FINAL_COL)
            continue
        nxt = out[i + 1]["x_sub"]
        rec["x_bal"] = (rec["x_edge"] if rec["x_sub"] < rec["x_edge"] < nxt
                        else (rec["x_sub"] + nxt) / 2.0)
    return out


def dots(subtractions, start=100.0):
    """Returns (balances, bites).

    balances: [(x, value)] all black, the running total.
    bites:    [(x, amount, cls, short, label)] coloured, one per subtraction.
    """
    placed = assign(subtractions)
    balances = [(centre(START_COL), start)]
    bites, r = [], start
    for p in placed:
        r -= p["amount"]
        bites.append((p["x_sub"], p["amount"], p["cls"], p["short"], p["label"]))
        balances.append((p["x_bal"], r))
    return balances, bites


def named(balances, bites):
    """Which dots carry a phase name. Derived, never hand-placed.

    Disbursed  = the dot at the disbursement boundary.
    Claims paid = the last dot at or before the claims column's right edge.
    Delivered  = the final dot.
    """
    lab = {}
    dis = edge("STATE_AGENCY")
    for x, _v in balances:
        if abs(x - dis) < 1:
            lab[x] = ["Disbursed"]
    cl = edge("CLAIMS")
    cand = [x for x, _v in balances[1:-1] if x <= cl]
    if cand:
        lab.setdefault(max(cand), ["Claims paid"])
    lab[balances[-1][0]] = ["Health Services", "delivered"]
    return lab


def value_rows(seq):
    """Which dots' values need the second row. Two dots closer than a value is
    wide cannot both sit on the same line; the later one steps up."""
    rows, last = {}, None
    for x, _v, _c in seq:
        if last is not None and x - last < VAL_W:
            rows[x] = VAL_STAGGER
            last = None          # the one after it can come back down
        else:
            rows[x] = VAL_Y
            last = x
    return rows


def text_w(text, px):
    """Advance width of a bold DejaVu string. One estimator, used everywhere in
    this file, so two placers can never disagree about how wide a label is."""
    return len(text) * px * 0.53


def neighbour_room(x, dot_xs):
    """How far a label centred on the dot at `x` may reach to either side before
    it passes under the NEXT DOT along.

    This is the ownership rule. Everything below the line is centred on a dot,
    so a label reaching past its neighbour's dot stops reading as its own dot's
    label and starts reading as that neighbour's. FY2030 'Eligibility Rules'
    spanned 634-832 around a bite dot at 733 with balance dots at 647 and 820 on
    either side: 'Eligibility' sat under one and 'Rules' under the other, and the
    row read as annotation on 'Disbursed'. Nothing was overprinted -- the three
    rows are at different heights -- which is why an eye passed it and a span
    test catches it.

    The measure is the DOT, not the neighbour's label span: dots are the lattice
    (4.4), labels are not, and a rule written against label spans changes answer
    every time a word changes.
    """
    left = [d for d in dot_xs if d < x - 0.5]
    right = [d for d in dot_xs if d > x + 0.5]
    room = []
    if left:
        room.append(x - max(left))
    if right:
        room.append(min(right) - x)
    return min(room) if room else 1e9


def wrap_short(short, room, px=SHORT_PX):
    """Break a bite's short name onto as few lines as its dot's room allows.

    Returns a list of lines. Raises if a single word still overruns: at that
    point the name is too long for the lattice and the fix is the name, not the
    layout, and the build should say so rather than draw it anyway (S-071).
    """
    lines, cur = [], ""
    for wd in short.split():
        trial = (cur + " " + wd).strip()
        if cur and text_w(trial, px) / 2.0 > room:
            lines.append(cur)
            cur = wd
        else:
            cur = trial
    if cur:
        lines.append(cur)
    over = [ln for ln in lines if text_w(ln, px) / 2.0 > room]
    if over:
        raise ValueError(
            f"tracker: short name {short!r} does not fit its dot: "
            f"{over!r} needs {max(text_w(ln, px) / 2.0 for ln in over):.0f} units "
            f"of half-width and the neighbouring dots leave {room:.0f}. "
            f"Shorten the name in instances.py:subs_spec (STYLE_GUIDE 4.8).")
    return lines


def short_lines(balances, bites):
    """{bite x: [line, ...]} for every bite, wrapped to fit the lattice."""
    dots_x = sorted({x for x, _v in balances} | {b[0] for b in bites})
    return {x: wrap_short(short, neighbour_room(x, dots_x))
            for x, _a, _c, short, _lab in bites}


def two_rows(items, pad=10.0):
    """items: [(x, text, px)] -> {x: row} where row is 0 or 1. Anything that
    would overlap its neighbour on row 0 drops to row 1."""
    rows, spans = {}, []
    for x, text, px in items:
        w = len(text) * px * 0.53
        l0, l1 = x - w/2 - pad, x + w/2 + pad
        r = 0
        for (p0, p1, pr) in spans:
            if not (l1 <= p0 or p1 <= l0) and pr == r:
                r = 1
        spans.append((l0, l1, r))
        rows[x] = r
    return rows


def label_rows(placed, seq):
    """Amount labels drop to a second row where they would collide. A label is
    centred in its span when it fits, and right-aligned to its dot when it does
    not, because the dot is the thing it is describing."""
    rows, spans = {}, []
    for i, (x, lab, _a, _c) in enumerate(placed):
        x0 = seq[i][0]
        w = len(lab) * 13 * 0.52
        if (x - x0) > w + 12:
            anchor, l0, l1 = "middle", (x0+x)/2 - w/2, (x0+x)/2 + w/2
        else:
            anchor, l0, l1 = "end", x - 6 - w, x - 6
        row = AMT_LAB_Y
        for (p0, p1, pr) in spans:
            if not (l1 <= p0 or p1 <= l0) and pr == row:
                row = AMT_LAB_Y2
        spans.append((l0, l1, row))
        rows[x] = (anchor, row)
    return rows


# ===========================================================================
# THE FOUR-ANCHOR LEDGER  (JW, 2026-09-04)
#
# Supersedes the running-ledger model above: a dot wherever a number changes
# (S-074) becomes four fixed anchors plus one marker per decrement. The anchors
# are the same four on every diagram, so a reader can lay two panels side by
# side and compare like with like. All summing — the running balance and the
# percentage lost — happens at the anchors and nowhere else.
#
# Anchors are large filled circles. Decrement markers are smaller, and carry
# their class in their SHAPE as well as their colour:
#     HR-1 rhombus | administration square | fraud triangle
# ===========================================================================
AGILIAN_BLUE = "#17325c"

ANCHOR_R = 18.0
ANCHOR_VAL_Y = -36.0       # the running balance, above its anchor
ANCHOR_VAL_PX = 34
ANCHOR_NAME_Y = 40.0
ANCHOR_NAME_LEAD = 28.0
ANCHOR_NAME_PX = 23
ANCHOR_PCT_Y = 28.0        # measured from the LAST name line

# ANCHORS READ BELOW THE LINE, DECREMENTS READ ABOVE IT.
# Every anchor-against-marker collision was a collision between two different
# KINDS of statement sharing one strip of canvas: where the money has got to, and
# what was taken out of it. Separating them by side removes the whole class at
# once and leaves only marker-against-marker, which is a real crowding problem
# rather than an artefact of the layout. It also means the line reads as a
# sentence: balances underneath, deductions overhead.
# The band ABOVE the line is 82 units deep — the rule at RULE_Y closes it — which
# is room for exactly one row of anything, so a marker that needs to step out of
# another's way has nowhere above to go. The band BELOW is 152 and can carry two
# tiers, so that is where the reading happens. Only the anchors' VALUES stay
# above, where nothing competes with them.
MARK_R = 11.0
MARK_AMT_Y = 34.0          # amount, below the line
MARK_NAME_Y = 56.0         # name, beneath the amount
MARK_TIER = 56.0           # a whole marker block steps DOWN when it would collide
MARK_AMT_PX = 20
MARK_NAME_PX = 17

# The standing year label. JW, 2026-09-25: the year came out of the first
# anchor's sub-label, where it was the second of three lines of small type in
# the most crowded corner of the panel, and becomes a label on the line itself.
# It reads at the LEFT END of the line, left-aligned in the margin the line
# vacated when its first anchor moved right to the source bar — which is the
# room that move creates and the reason to make it first.
YEAR_PX = 40
YEAR_X = 20.0              # canvas margin; the line now starts at SOURCE_X
YEAR_DY = 14.0             # baseline below BY, so the label centres on the line
YEAR_PAD = 14.0            # clear air between the label and the first anchor


def year_fits(text, x_anchor, px=YEAR_PX):
    """Half-true is not good enough here: the year is set large and the anchor
    circle is fixed, so the build must say so rather than letting a big label
    run under the first dot. Returns the overrun in units, 0 when it fits."""
    right = YEAR_X + text_w(text, px)
    return max(0.0, right - (x_anchor - ANCHOR_R - YEAR_PAD))


def ledger(subtractions, marker_x, marker_origin=None, start=100.0):
    """(anchors, marks).

    anchors: [dict(x, name=[lines], value)] — the four, always.
    marks:   [dict(x, amount, cls, short)] — one per live decrement, placed by
             outflows.decrement_x, which reads the Sankey's own geometry.

    An anchor's value is the start less every decrement that has already been
    taken by the time the flow reaches it. Nothing is summed anywhere else.

    WHICH decrements those are is read from each decrement's ORIGIN — the point
    at which the money leaves the flow — and never from its marker's x. The two
    were the same thing until S-085 moved the eligibility terminals out to the
    reach each blocked dollar declares, which pushed that marker's midpoint past
    the Funding Disbursed anchor and made the line report $92.06 disbursed on a
    panel whose trunk narrows to $83.89. Position is a claim about the flow's
    geometry; attribution is a claim about the ledger. A marker may move anywhere
    the geometry sends it and the arithmetic must not follow it.
    """
    live = [s for s in subtractions if s[1] > 0.004]
    marks = sorted(
        [dict(x=marker_x[s[4]], amount=s[1], cls=s[2], short=s[4]) for s in live],
        key=lambda m: m["x"])
    origin = dict(marker_origin or {})
    anchors = []
    for col, name in TRACKER_ANCHORS:
        x = anchor_x(col)
        anchors.append(dict(
            x=x, name=list(name),
            value=start - sum(m["amount"] for m in marks
                              if origin.get(m["short"], m["x"]) < x)))
    _reconcile(anchors, marks, origin, start)
    return anchors, marks


# S-106, JW 25 September. A reader with a calculator reads the tracker line
# left to right: an anchor, less the decrements drawn between it and the next
# one, equals the next anchor. The arithmetic above is exact and every figure
# was then rounded to the cent on its own, so the printed line could disagree
# with itself by a penny while every underlying figure was right. It did, on
# the FY2030 panels: $98.75 less $6.05 less $8.24 printed an anchor of $84.47
# against a reader's $84.46.
#
# The ANCHORS are the published figures and do not move. Each decrement
# carries a `display` value, allocated by largest remainder within its own
# segment so the printed decrements sum to the printed fall between the two
# anchors that bracket them. A decrement's display never departs from its own
# value by more than a cent; if it would, that is not rounding and the build
# says so rather than adjusting it.
#
# Attribution is by ORIGIN, never by marker x — the same rule the anchors use,
# and for the same reason (S-085).
def _reconcile(anchors, marks, origin, start):
    bounds = [None] + [a["x"] for a in anchors]
    prev_val, prev_x = start, None
    for a in anchors:
        seg = [m for m in marks
               if (prev_x is None or origin.get(m["short"], m["x"]) >= prev_x)
               and origin.get(m["short"], m["x"]) < a["x"]]
        target = round(round(prev_val, 2) - round(a["value"], 2), 2)
        if seg:
            cents = [int(m["amount"] * 100 // 1) for m in seg]
            need = int(round(target * 100)) - sum(cents)
            order = sorted(range(len(seg)),
                           key=lambda i: -(seg[i]["amount"] * 100 - cents[i]))
            for i in order[:max(need, 0)]:
                cents[i] += 1
            for i in order[len(order) + min(need, 0):]:
                cents[i] -= 1
            for m, c in zip(seg, cents):
                m["display"] = c / 100.0
                if abs(m["display"] - m["amount"]) > 0.0101:
                    raise ValueError(
                        f"tracker line: {m['short']} would have to print "
                        f"${m['display']:.2f} against its value of "
                        f"${m['amount']:.4f}. That is not rounding.")
        prev_val, prev_x = a["value"], a["x"]
    for m in marks:
        m.setdefault("display", m["amount"])


def unreconciled(anchors, marks, origin=None, start=100.0):
    """Printed anchors against printed decrements. [] when the line adds up.

    Reads the same two structures the renderer draws from, so it asserts what
    the reader sees rather than what the ledger holds.
    """
    origin = dict(origin or {})
    out, prev_val, prev_x = [], start, None
    for a in anchors:
        seg = [m for m in marks
               if (prev_x is None or origin.get(m["short"], m["x"]) >= prev_x)
               and origin.get(m["short"], m["x"]) < a["x"]]
        lhs = round(round(prev_val, 2)
                    - sum(round(m.get("display", m["amount"]), 2) for m in seg), 2)
        rhs = round(a["value"], 2)
        if abs(lhs - rhs) > 0.0001:
            out.append(f"{' / '.join(a['name'])}: ${rhs:.2f} printed, "
                       f"${lhs:.2f} on the line's own figures "
                       f"({' '.join('-$%.2f' % m.get('display', m['amount']) for m in seg)})")
        prev_val, prev_x = a["value"], a["x"]
    return out


def mark_tiers(marks, anchors=(), pad=16.0):
    """{short: tier} — 0 for the first row above the line, 1 for the next.

    A marker keeps its geometric x; only its LABEL BLOCK moves, and only upward.
    Where two decrements genuinely occupy the same span of the flow — state
    administration and the eligibility rules both terminate on the state agency's
    right edge — the honest answer is to stack them, not to slide one of them
    somewhere it does not belong.
    """
    # The anchors' NAMES occupy the first tier before any marker does: they are
    # fixed furniture and a decrement gives way to them, never the other way
    # round. Seeding them here is what stops "State Admin" sliding under
    # "Funding Disbursed" — two different kinds of statement, and the separation
    # only works if the test knows about both.
    tiers = {}
    spans = [(a["x"] - max(text_w(l, ANCHOR_NAME_PX) for l in a["name"]) / 2 - 6,
              a["x"] + max(text_w(l, ANCHOR_NAME_PX) for l in a["name"]) / 2 + 6, 0)
             for a in anchors]
    for m in marks:
        w = max(text_w(m["short"], MARK_NAME_PX),
                text_w(f"-${m.get('display', m['amount']):.2f}", MARK_AMT_PX))
        l0, l1 = m["x"] - w / 2 - pad, m["x"] + w / 2 + pad
        t = 0
        while t < 2 and any(t == pt and not (l1 <= p0 or p1 <= l0)
                            for p0, p1, pt in spans):
            t += 1
        spans.append((l0, l1, t))
        tiers[m["short"]] = t
    return tiers


def shape_gap(marks, minimum=30.0):
    """Markers whose SHAPES would touch. Reported, never silently moved."""
    out = []
    for a, b in zip(marks, marks[1:]):
        if b["x"] - a["x"] < minimum:
            out.append((a["short"], b["short"], b["x"] - a["x"]))
    return out


def collisions(anchors, marks, pad=14.0):
    """Label spans on the line that overlap. The marker rule places by geometry
    and does not negotiate, so where two markers genuinely belong in the same
    place this REPORTS rather than silently nudging one of them somewhere it
    does not belong."""
    # Markers live above the line now, so they cannot collide with anchor names.
    items = [(a["x"], max(text_w(l, ANCHOR_NAME_PX) for l in a["name"]), a["name"][0])
             for a in anchors]
    items.sort()
    out = []
    for (x0, w0, n0), (x1, w1, n1) in zip(items, items[1:]):
        gap = (x1 - w1 / 2) - (x0 + w0 / 2)
        if gap < pad:
            out.append((n0, n1, gap))
    return out
