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
        term_col="FEDERAL", term_y=560, ret=False),
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
