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
from outflows import COLS

# ---- palette -------------------------------------------------------------
INK = "#111418"
HR1 = "#8B5A5A"
ADMIN = "#5c6169"      # darkened from #8e9298 at JW's instruction
FRAUD = "#b23a32"
SUBTLE = "#54585f"     # darkened from #6f6f6f

COLOUR = {"hr1": HR1, "admin": ADMIN, "fraud": FRAUD}

# ---- geometry ------------------------------------------------------------
RULE_Y = 1030.0        # the hairline that closes the flow area
BY = 1112.0            # the ledger line
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
