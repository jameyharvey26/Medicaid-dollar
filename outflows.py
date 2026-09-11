# outflows.py — the outflow ledger.
#
# JW, 2026-08-29: "We really need to store the beginnings and endpoints of the
# outflows in the ledger so that we don't keep getting confused like that."
#
# Every outflow on every artifact is declared here once: where it leaves the
# flow, which edge it leaves from, and where it terminates. Both builders read
# this. Nothing about an outflow's geometry is written twice, so the two
# diagrams cannot drift apart the way Medicare premiums did.

# Column boundaries. These are the spine of the whole layout: checkpoints,
# terminals and right-aligned labels all key off them.
COLS = {
    "FEDERAL":     (110, 300),
    "STATE_GOVT":  (300, 560),
    "STATE_AGENCY": (560, 820),
    "DISBURSE":    (820, 1060),
    "PAYER":       (1060, 1300),
    "CLAIMS":      (1300, 1560),
    "PROVIDERS":   (1560, 1760),
    "BENEFICIARY": (1760, 2180),
}

# class:   "ordinary" = exists under prior law | "hr1" = P.L. 119-21
# edge:    "top" = peels up (ordinary) | "bottom" = peels down (HR-1)
# ret:     True = returns to an earlier column. The ONLY sanctioned exception to
#          S-055's downstream rule, and only where the money genuinely goes back.
OUTFLOWS = {
    # ---- ordinary leakage, both diagrams --------------------------------
    "Administration": dict(
        cls="ordinary", src="STATE_AGENCY", edge="top", src_x=615,
        term_col="STATE_AGENCY", term_y=250, ret=False),
    "Medicare premiums": dict(
        cls="ordinary", src="STATE_AGENCY", edge="top", src_x=715,
        term_col="FEDERAL", term_y=134, ret=True),
    "MCO plan administration": dict(
        cls="ordinary", src="PAYER", edge="top", src_x=None,
        term_col="PAYER", term_y=None, ret=False),
    "Dual MCO plan administration": dict(
        cls="ordinary", src="PAYER", edge="top", src_x=None,
        term_col="PAYER", term_y=None, ret=False),
    "Public-company earnings": dict(
        cls="ordinary", src="PAYER", edge="top", src_x=None,
        term_col="PAYER", term_y=None, ret=False),
    "Documented fraud": dict(
        cls="ordinary", src="CLAIMS", edge="bottom", src_x=1306,
        term_col="PROVIDERS", term_y=880, ret=False),

    # ---- HR-1, FY2030 only ----------------------------------------------
    # Provider tax limits sources from the FEDERAL band in the FEDERAL column.
    # The state band does NOT slide up to close the space: the gap between the
    # two bands IS the federal match that will never be drawn, and it stays
    # open through the state government column.
    "Provider tax limits": dict(
        cls="hr1", src="FEDERAL", edge="fed_bottom", src_x=176,
        term_col="FEDERAL", term_y=560, ret=False, label_side="end"),
    # THE FIVE STATE-AGENCY LEVERS, IN SOURCE ORDER (JW, 2026-09-11).
    # Source order equals terminal order, which is what fan_rows needs to pack
    # them without crossings once the terminals spread across four columns
    # (S-085). "Everything else" declares no reach, terminates shortest, and
    # therefore peels FIRST and takes the row nearest the HR-1 rule, where it
    # costs the least height.
    #
    # `label` is what the artifact prints. It exists because "Other" is already
    # the internal key of the wrap-around-services provider node, and two
    # different things under one string is how a detector goes blind (S-079,
    # S-076). One name, declared once, in one place.
    "Work reporting": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=664,
        term_col="DISBURSE", term_y=None, ret=False,
        reach="DISBURSE"),
    "Six-month renewals": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=698,
        term_col="PAYER", term_y=None, ret=False,
        reach="PAYER"),
    "Blocked Medicaid enrollment rule": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=732,
        term_col="CLAIMS", term_y=None, ret=False,
        reach="CLAIMS"),
    "Everything else": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=766,
        term_col="STATE_AGENCY", term_y=None, ret=False, label="Other"),
    "Blocked senior enrollment rule": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=800,
        term_col="STATE_AGENCY", term_y=None, ret=False,
        reach="STATE_AGENCY", label="Blocked senior enrollment",
        # Above its own terminal rather than below it (JW, 2026-09-11). It and
        # "Other" both stop at the state agency edge, so their blocks sat one on
        # top of the other at the bottom of the fan; lifting this one over its
        # terminal separates them. It crosses a neighbouring ribbon on the way
        # up, which JW has accepted.
        label_dy=-52),
    "Directed payment caps": dict(
        cls="hr1", src="CLAIMS", edge="bottom", src_x=1302,
        term_col="PROVIDERS", term_y=None, ret=False,
        # Its block sat twelve units under Blocked Medicaid's and immediately to
        # the right of it, so the two read as one label and the caps looked like
        # a clause of the enrollment rule (JW, 2026-09-11).
        label_dy=-30),
}

# Which column each subtraction is charged to on the bottom tracker. The amount
# is right-aligned to that column's right edge, so a reader can drop a vertical
# line from any subtraction on the flow to its figure on the tracker.
TRACKER_COL = {
    "Administration": "STATE_AGENCY",
    "Medicare premiums": "STATE_AGENCY",
    "MCO plan administration": "PAYER",
    "Dual MCO plan administration": "PAYER",
    "Public-company earnings": "PAYER",
    "Documented fraud": "CLAIMS",
    "Provider tax limits": "FEDERAL",
    "Blocked senior enrollment rule": "STATE_AGENCY",
    "Work reporting": "STATE_AGENCY",
    "Six-month renewals": "STATE_AGENCY",
    "Blocked Medicaid enrollment rule": "STATE_AGENCY",
    "Everything else": "STATE_AGENCY",
    "Directed payment caps": "CLAIMS",
}

# Tracker checkpoints. Shared furniture, identical on every artifact (S-060).
# $100 sits under the FEDERAL column, before federal and state combine.
# Health services delivered sits on the providers / beneficiaries boundary.
TRACKER_CPS_X = [205, 820, 1300, 1760]


def col_right(name, inset=8):
    """Right edge of a column, for right-aligned tracker figures."""
    return COLS[name][1] - inset


# ==========================================================================
# Fan layout: no avoidable crossings.
#
# JW, 2026-09-03: "when the diagram is drawn the software should make its best
# effort not to cross the tributaries, unless it's mathematically unfeasible to
# avoid it."
#
# WHY THIS IS ALWAYS SOLVABLE FOR A FAN, and why the claims fan is different.
# Tributaries in a fan leave a common edge, so their vertical order at the source
# is fixed by their bite x and is a TOTAL order. Only one end is pinned. Two
# ribbons cross exactly when their x-spans overlap and their vertical order flips
# between source and terminal, so preserving the source order everywhere removes
# every crossing. The constraints therefore can never contradict each other and a
# fan has no unavoidable crossings.
#
# The main lanes in the CLAIMS column are pinned at BOTH ends: each payer lane
# has a fixed origin and each provider node a fixed position, and the two
# orderings genuinely disagree. No reordering fixes that, and it should not be
# "fixed" — the tangle is the finding. This module does not touch those. It
# governs declared outflows only.
# ==========================================================================

FAN_TOP = 800.0        # first terminal row, below the HR-1 rule at y=788
FAN_MIN_GAP = 40.0     # floor between consecutive rows
FAN_LABEL_H = 45.0     # name + sub + amount
# Floor on row spacing when the stack must compress. It can go this tight without
# looking cramped because the gap only ever applies between two ribbons whose
# LABELS do not overlap in x; where labels do overlap, the 45px label block sets
# the spacing instead. The widest gap that clears the tracker always wins.
FAN_TIGHT_GAP = 8.0
FAN_FLOOR = 1100.0     # tracker rule sits at 1106; labels must clear it


FAN_LABEL_H_TIGHT = 30.0   # name and amount share a line; sub below


def _text_w(s, size, pad=4):
    """Width of a rendered label INCLUDING the background box the renderer paints
    behind it. Must stay in step with `sankey.lbg`: a solver measuring a narrower
    box than the one drawn will hand back a layout that overlaps."""
    return len(s) * size * 0.56 + pad * 2


def _block_h(it):
    """Height of a terminal's label block.

    A tributary's amount may ride on the name's line or sit under the sub-label
    (JW, 2026-09-11). Which one is SOLVED per tributary, not chosen: the compact
    form buys 11 units of height and costs width, so it is worth taking only
    where the stack would otherwise run past the floor. Either way the amount
    stays inside its own block, directly under its own terminal, so it cannot
    read as belonging to the tributary below it.
    """
    return FAN_LABEL_H_TIGHT if it.get("compact") else FAN_LABEL_H


def _label_w(it):
    # The PRINTED name, not the key. The two diverged the moment `label` landed,
    # and a solver measuring a string the artifact never shows is a solver
    # working on the wrong diagram.
    nm = it.get("label") or it["name"]
    if it.get("compact"):
        nm = f"{nm}  \u2212${it.get('amt', 0):.2f}"
    # ONE METRIC, the renderer's. The solver used 0.55/0.50 while `sankey.lbg`
    # draws its background at 0.56 plus 8 units of padding, so the solver
    # believed every label was narrower than the box actually painted for it.
    # Harmless while the sub-label was always the widest line and the slack
    # absorbed it; it stopped being harmless the moment amounts were folded onto
    # names. The six-month renewals amount was sitting under the background of
    # Blocked Medicaid's sub-label, greyed out and unreadable, while the solver
    # reported the two labels 25 units clear of each other.
    return max(_text_w(nm, 12), _text_w(it.get("sub", ""), 10), 40)


def _label_span(it, anchor=None):
    """Approximate x-extent of a terminal's label block, for collision testing."""
    w = _label_w(it)
    if (anchor or it.get("anchor")) == "end":
        return it["xt"] - 8 - w, it["xt"] - 8
    return it["xt"], it["xt"] + w


def _overlap(a0, a1, b0, b1):
    return not (a1 <= b0 or b1 <= a0)


def fan_tiers(items):
    """items: [{name, xb, xt, y_src, th}] sharing one source edge.

    Returns {name: tier}. Tier 0 is the top row. A tributary is placed below
    every tributary it would otherwise cross.
    """
    # Walk the source edge from the TOP down. Whatever leaves higher stays higher.
    order = sorted(items, key=lambda i: i["y_src"])
    tier = {}
    for idx, a in enumerate(order):
        above = [b["name"] for b in order[:idx]
                 if _overlap(a["xb"], a["xt"], b["xb"], b["xt"])]
        tier[a["name"]] = 1 + max([tier[n] for n in above], default=-1)
    return tier


def _clear_obstacles(it, y, anchor, obstacles):
    """Push a terminal below any diagram furniture it would land on. The fan does
    not know what else is drawn, so the renderer declares keep-out boxes."""
    l0, l1 = _label_span(it, anchor)
    x0, x1 = min(l0, it["xt"]), max(l1, it["xt"] + 6)
    for _ in range(len(obstacles) + 1):
        moved = False
        for (o0, oy0, o1, oy1) in obstacles:
            if not _overlap(x0, x1, o0, o1):
                continue
            if oy1 > y and oy0 < y + it["th"] + _block_h(it):
                y = oy1 + 8
                moved = True
        if not moved:
            break
    return y


def _place(items, top, gap, obstacles):
    """Place terminals top-down in source order.

    A terminal is pushed below ONLY the terminals it actually conflicts with:
    below a ribbon whose x-span it overlaps (or they would cross), and below a
    label block whose x-span its own label overlaps. Two tributaries far apart
    horizontally may share a height. That is what keeps the fan shallow enough to
    fit above the tracker, and it is why an earlier version that floored every row
    against every previous row overflowed.
    """
    # Pinned tributaries (an ordinary outflow whose terminal is already fixed,
    # e.g. documented fraud) take part in the ordering but are never moved. They
    # must be participants, not keep-out boxes: an obstacle can only push a
    # neighbour DOWN, and the correct answer is sometimes to push it UP.
    order = sorted(items, key=lambda i: i["y_src"])
    y_of, anchors, placed = {}, {}, []
    for it in order:
        if it.get("fixed_y") is not None:
            y_of[it["name"]] = it["fixed_y"]
            anchors[it["name"]] = it.get("anchor") or "start"
            placed.append(it)
    for it in order:
        if it.get("fixed_y") is not None:
            continue
        # Labels sit to the RIGHT of their terminal by default: that is the
        # reading direction and it keeps the label downstream of the bite like the
        # ribbon itself. Flipping left is a concession, taken only when it clearly
        # buys height, because a left label reaches back over the ribbon and can
        # push the rows beneath it further down than it saves.
        best, best_y = None, None
        for cand in ([it["anchor"]] if it.get("anchor") else ["start", "end"]):
            l0, l1 = _label_span(it, cand)
            if l0 < COLS["FEDERAL"][0]:
                continue
            y = top
            ceiling = None
            for p in placed:
                if _overlap(it["xb"], it["xt"], p["xb"], p["xt"]):
                    if p["y_src"] > it["y_src"]:
                        # p leaves BELOW this one, so it must stay below: this
                        # tributary is capped above p rather than floored below it.
                        # The cap must clear p's LABEL too where the two labels
                        # share x, or the ribbons separate and the words collide.
                        p0b, p1b = _label_span(p, anchors[p["name"]])
                        room = (_block_h(p) + 6) if _overlap(l0, l1, p0b, p1b) else gap
                        ceiling = min(ceiling if ceiling is not None else 1e9,
                                      y_of[p["name"]] - it["th"] - room)
                    else:
                        y = max(y, y_of[p["name"]] + p["th"] + gap)
                p0, p1 = _label_span(p, anchors[p["name"]])
                if _overlap(l0, l1, p0, p1):
                    y = max(y, y_of[p["name"]] + p["th"] + _block_h(p) + 6)
            y = _clear_obstacles(it, y, cand, obstacles)
            if ceiling is not None and y > ceiling:
                # Obstacles pushed it past a tributary it must stay above. Sit on
                # the ceiling; the crossing gate will report it if that is wrong.
                y = max(top, ceiling)
            if best_y is None or y < best_y - 1.0:
                best, best_y = cand, y
        anchors[it["name"]] = best or "start"
        y_of[it["name"]] = best_y if best_y is not None else top
        placed.append(it)

    warnings = []
    for it in items:
        bottom = y_of[it["name"]] + it["th"] + _block_h(it)
        if bottom > FAN_FLOOR:
            warnings.append(f"{it['name']}: terminal block reaches y={bottom:.0f}, "
                            f"past the {FAN_FLOOR:.0f} floor")
    return y_of, anchors, warnings


def fan_rows(items, top=FAN_TOP, obstacles=()):
    """Place terminals with no avoidable crossings, packed as tightly as the
    labels allow.

    Two things give, in this order, because they cost the reader different
    amounts. Row spacing relaxes from FAN_MIN_GAP to FAN_TIGHT_GAP first: it
    changes nothing about how a label reads. Only if that is not enough does the
    solver start folding amounts onto their names, deepest row first, one
    tributary at a time — because the compact form is slightly harder to read and
    should be spent where it buys the most and nowhere else. The widest spacing
    with the fewest folded labels that fits, wins.

    If nothing fits, the tightest arrangement is returned WITH its warnings
    rather than silently overflowing.
    """
    obs = tuple(obstacles)

    def solve(compact, gap):
        for it in items:
            it["compact"] = it["name"] in compact
        return _place(items, top, float(gap), obs)

    def sweep(compact):
        last = None
        for gap in range(int(FAN_MIN_GAP), int(FAN_TIGHT_GAP) - 1, -2):
            last = solve(compact, gap)
            if not last[2]:
                return last, True
        return last, False

    res, ok = sweep(frozenset())
    if ok:
        return res + (frozenset(),)

    # Deepest first: the rows that overrun are the ones worth compacting, and
    # compacting a row that already fits spends legibility for nothing.
    #
    # More compaction is NOT monotonically better and the search must not assume
    # it is. A folded label is wider, so past a point folding one more row
    # creates a fresh x-overlap and the stack gets DEEPER: measured 2026-09-11,
    # four folded rows bottom out at 1116 and seven at 1138. So every attempt is
    # scored and the shallowest is kept, rather than the last one tried.
    depth = res[0]
    by_depth = sorted((it["name"] for it in items),
                      key=lambda n: -depth.get(n, 0.0))

    def _deepest(r):
        return max((r[0][it["name"]] + it["th"] + _block_h(it)) for it in items)

    best, best_d, best_c = res, None, frozenset()
    for k in range(1, len(by_depth) + 1):
        compact = frozenset(by_depth[:k])
        cand, ok = sweep(compact)
        if ok:
            return cand + (compact,)
        for it in items:
            it["compact"] = it["name"] in compact
        d = _deepest(cand)
        if best_d is None or d < best_d:
            best, best_d, best_c = cand, d, compact
    for it in items:
        it["compact"] = it["name"] in best_c
    return best + (best_c,)


def fan_crossings(items, y_of):
    """Pairs that still cross after placement. Used by check.py as a gate."""
    out = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            if not _overlap(a["xb"], a["xt"], b["xb"], b["xt"]):
                continue
            src = a["y_src"] - b["y_src"]
            trm = (y_of[a["name"]] + a["th"] / 2) - (y_of[b["name"]] + b["th"] / 2)
            if src * trm < 0:
                out.append((a["name"], b["name"]))
    return out


# Step names on the trunk map to their declared outflow.
STEP_OUTFLOW = {"admin": "Administration", "medicare": "Medicare premiums"}


def resolve_bite_order(steps):
    """Rule 2.9 applied to the ORDINARY peels, where the fix is bite order.

    Administration and Medicare premiums both peel UP off the same trunk edge, so
    whichever peels first sits above the other for the rest of its life. Medicare
    premiums returns to the federal lane high on the canvas; administration
    terminates lower. With administration peeling first the two were forced to
    swap places and crossed, every render, on both diagrams.

    Nothing in the ledger cares which peels first: they leave the same trunk in
    the same column and the tracker reports them as one subtraction. So the x
    SLOTS stay fixed and the outflows are dealt into them in terminal-height
    order, topmost terminal first. This is the same invariant as fan_rows —
    source order equals terminal order — solved on the other axis, because here
    the terminals are what is pinned and the sources are free.
    """
    out = dict()
    for side in ("top", "bot"):
        grp = [r for r in steps if r[1] == side]
        if len(grp) < 2:
            continue
        slots = sorted(r[3] for r in grp)
        if side == "top":
            # Ordinary peels: terminals are pinned heights, sources are free.
            # Deal the slots out topmost-terminal-first.
            key = lambda r: (OUTFLOWS.get(STEP_OUTFLOW.get(r[0], r[0]), {})
                             .get("term_y", 0) or 0)
        else:
            # HR-1 tributaries: terminal HEIGHT is solved later, but terminal X is
            # fixed by which column the dollar would have reached. Whatever stops
            # SOONER left-to-right must also start sooner, or the fan is forced to
            # fold back over itself and the solver pays for it in depth.
            # HR-1 tributaries: terminal HEIGHT is solved later, but terminal X
            # is fixed by where the dollar would have reached. Whatever stops
            # SOONER left-to-right must also start sooner, or the fan folds back
            # over itself and the solver pays for it in depth.
            #
            # This also forces the fan's row order, which is not a preference and
            # cannot be tuned: a tributary that peels first leaves LOWEST on the
            # trunk edge and must stay lowest for the rest of its life, so the
            # shortest-reaching tributary is always the deepest row. Measured
            # 2026-09-11: reversing the rule costs 9 margin crossings, excepting
            # the no-reach tributary costs 3, and pinning that tributary's row
            # under the HR-1 rule costs the same 3, because it peels highest and
            # every earlier tributary is then above it at its own terminal.
            #
            # Reads _terminus_x, not term_col: since S-085 those differ for any
            # tributary declaring a reach, and the slot order must follow the
            # terminal the reader actually sees.
            # Where two tributaries reach the SAME column the sort is a tie, and
            # a tie left to a stable sort is decided by whatever order the
            # declarations happen to sit in — which is not a decision, it is an
            # accident that looks like one. Declaration order is the tie-break,
            # explicitly, so moving a tributary in this file moves it on the
            # canvas and nothing else does.
            _decl = {n: i for i, n in enumerate(OUTFLOWS)}
            key = lambda r: (_canvas_term_x(r[0]), _decl.get(r[0], 0))
        for r, x in zip(sorted(grp, key=key), slots):
            out[r[0]] = x
    return [(n, side, v, out.get(n, x)) for n, side, v, x in steps]


def label_of(name):
    """What the artifact prints for an outflow. The key is the identity, the
    label is the printed name, and where no label is declared they are the same
    string — so there is never a second name to fall out of step."""
    return OUTFLOWS.get(name, {}).get("label") or name


# ---------------------------------------------------------------------------
# DECREMENT MARKER PLACEMENT (JW, 2026-09-04)
#
# The number line is a summary of the Sankey and must line up with it vertically.
# A decrement marker therefore sits midway between where its money LEAVES the
# flow and the end of the segment it is CHARGED to, both read from the geometry
# already declared above, so the marker cannot drift away from the ribbon it
# summarises.
#
# A bundled decrement takes the earliest origin of its members and the furthest
# forward termination. A leg that returns upstream is excluded from the
# termination: Medicare premiums goes back to the federal column, and its
# midpoint would sit behind its own origin.
DECREMENT_MEMBERS = {
    "Provider Tax":      ("Provider tax limits",),
    "State Admin":       ("Administration", "Medicare premiums"),
    "Eligibility Rules": ("Blocked senior enrollment rule", "Work reporting",
                          "Six-month renewals", "Blocked Medicaid enrollment rule",
                          "Everything else"),
    "MCO Admin":         ("MCO plan administration", "Dual MCO plan administration",
                          "Public-company earnings"),
    "Payment Caps":      ("Directed payment caps",),
    "Fraud":             ("Documented fraud",),
}


def _origin_x(name):
    o = OUTFLOWS[name]
    if o.get("src_x") is not None:
        return float(o["src_x"])
    # No declared x: the money starts leaving at its source column's left edge.
    return float(COLS[o["src"]][0])


def _canvas_term_x(name):
    """Where the tributary's TERMINAL sits on the canvas: its declared reach, or
    the column it is charged to where it declares none (S-085).

    Deliberately separate from `_terminus_x`, which answers the number line's
    question. Peel order has to follow the terminal a reader can see, or the fan
    folds back over itself; the marker's span has to follow the ledger. One
    function serving both is what put the eligibility rhombus at 1112, and
    pointing them back at one function again put six crossings in the fan."""
    o = OUTFLOWS[name]
    return float(COLS[o.get("reach") or o["term_col"]][1])


def _terminus_x(name):
    """How far a decrement's SPAN runs on the number line: to the end of the
    column it is charged to.

    This is not the same question as where the tributary's terminal goes on the
    canvas, and conflating them is what broke it. The canvas terminal answers
    "where would this dollar have arrived", which is the reach (S-085). The
    number line answers "over what stretch of the flow was this money taken
    out", which ends where its charged segment ends and never travels with the
    reach. Routing the reach into both sent the eligibility rhombus from 742 to
    1112, past the anchor that had already subtracted it, and needed a clamp to
    drag it back — two pieces of machinery to undo one wrong answer.

    Ordinary outflows stop at the right edge of the column they reach."""
    o = OUTFLOWS[name]
    col = TRACKER_COL[name] if o["cls"] == "hr1" else o["term_col"]
    return float(COLS[col][1])


def decrement_span(short):
    """(origin, terminus) for a decrement, from the declared outflow geometry."""
    members = DECREMENT_MEMBERS[short]
    origins = [_origin_x(n) for n in members]
    forward = [n for n in members if not OUTFLOWS[n].get("ret")]
    termini = [_terminus_x(n) for n in (forward or members)]
    return min(origins), max(termini)


def decrement_x(short):
    """Midway between where the money leaves the flow and the end of the segment
    it is charged to, both read from the declared outflow geometry (4.9)."""
    a, b = decrement_span(short)
    return (a + b) / 2.0


# The four anchors. Identical on every diagram, past, present and future: they are
# what lets a reader lay two panels side by side (S-060). Each sits on the LEFT
# EDGE of the column whose state it reports, which is where that money arrives.
TRACKER_ANCHORS = [
    ("FEDERAL",     ["$100 Medicaid", "Dollars"]),
    ("DISBURSE",    ["Funding Disbursed"]),
    ("CLAIMS",      ["Claims Paid"]),
    ("BENEFICIARY", ["Health Services", "Delivered"]),
]
