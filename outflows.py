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
    "Blocked senior enrollment rule": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=664,
        term_col="STATE_AGENCY", term_y=None, ret=False),
    "Work reporting": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=698,
        term_col="DISBURSE", term_y=None, ret=False),
    "Six-month renewals": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=732,
        term_col="PAYER", term_y=None, ret=False),
    "Blocked Medicaid enrollment rule": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=766,
        term_col="CLAIMS", term_y=None, ret=False),
    "Everything else": dict(
        cls="hr1", src="STATE_AGENCY", edge="bottom", src_x=800,
        term_col="PAYER", term_y=None, ret=False),
    "Directed payment caps": dict(
        cls="hr1", src="CLAIMS", edge="bottom", src_x=1302,
        term_col="PROVIDERS", term_y=None, ret=False),
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
FAN_TIGHT_GAP = 18.0
FAN_FLOOR = 1024.0     # tracker line sits at 1030; labels must clear it


def _label_w(it):
    return max(len(it["name"]) * 12 * 0.55, len(it.get("sub", "")) * 10 * 0.5, 40)


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
            if oy1 > y and oy0 < y + it["th"] + FAN_LABEL_H:
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
                        room = (FAN_LABEL_H + 6) if _overlap(l0, l1, p0b, p1b) else gap
                        ceiling = min(ceiling if ceiling is not None else 1e9,
                                      y_of[p["name"]] - it["th"] - room)
                    else:
                        y = max(y, y_of[p["name"]] + p["th"] + gap)
                p0, p1 = _label_span(p, anchors[p["name"]])
                if _overlap(l0, l1, p0, p1):
                    y = max(y, y_of[p["name"]] + p["th"] + FAN_LABEL_H + 6)
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
        bottom = y_of[it["name"]] + it["th"] + FAN_LABEL_H
        if bottom > FAN_FLOOR:
            warnings.append(f"{it['name']}: terminal block reaches y={bottom:.0f}, "
                            f"past the {FAN_FLOOR:.0f} floor")
    return y_of, anchors, warnings


def fan_rows(items, top=FAN_TOP, obstacles=()):
    """Place terminals with no avoidable crossings, packed as tightly as the
    labels allow. Row spacing relaxes from FAN_MIN_GAP down to FAN_TIGHT_GAP if
    the stack would otherwise run past the tracker; the widest spacing that fits
    wins. If nothing fits, the tightest is returned WITH a warning rather than
    silently overflowing."""
    last = None
    for gap in range(int(FAN_MIN_GAP), int(FAN_TIGHT_GAP) - 1, -2):
        last = _place(items, top, float(gap), tuple(obstacles))
        if not last[2]:
            return last
    return last


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
            key = lambda r: _term_x(r[0])
        for r, x in zip(sorted(grp, key=key), slots):
            out[r[0]] = x
    return [(n, side, v, out.get(n, x)) for n, side, v, x in steps]


def _term_x(name):
    """Terminal x of a declared outflow, from its terminal column."""
    o = OUTFLOWS.get(name)
    if not o:
        return 0
    return COLS.get(o.get("term_col"), (0, 0))[1]
