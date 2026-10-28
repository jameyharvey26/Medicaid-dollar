#!/usr/bin/env python3
"""anchorproof.py — every tributary leaves the river, not the white space.

A tributary carries money OUT of the hundred dollars. Its first point therefore
has to be ON the body of the flow: if it starts anywhere else, the drawing is
telling the reader that the money came from nowhere, and no other gate catches
it. Documented fraud was anchored to the bottom of the provider bar stack --
below the river, past the gaps between the bars -- and it read as floating.

Checked against the engine's own render, with the same body palette and the
same envelope the crossing detector uses, so a palette change moves both
together.

    python3 anchorproof.py
"""
import os
import sys

import crossings
import enginecrossings as ec

PAD = 6.0          # a hairline of slack; a band edge is not a knife edge


def anchored(curves, env, step=4.0):
    """Every non-body band, with whether its first point lies on the body.

    A tributary may also leave another tributary rather than the river itself:
    plan administration and shareholder earnings come out of the pool that the
    lane retentions flow into, not out of the hundred directly. That is still
    an anchored start — the money is accounted for one step upstream — so the
    ends of the tributaries count as ground too.
    """
    ends = []
    for top, bot, _m, col, _l in curves:
        if col in crossings.BODY:
            continue
        ends.append((top[-1][0], min(top[-1][1], bot[-1][1]),
                     max(top[-1][1], bot[-1][1])))

    def on_a_terminal(x, ya, yb):
        return any(abs(x - ex) <= 8 and ya >= e0 - PAD and yb <= e1 + PAD
                   for ex, e0, e1 in ends)

    out = []
    for top, bot, _mid, col, lab in curves:
        if col in crossings.BODY:
            continue
        if "stroke" in (lab or ""):
            # the fold of a return, which starts where its forward band ended.
            # The band is the departure and is checked; the fold is where the
            # money goes afterwards and is not anchored to anything.
            continue
        x, y0 = top[0]
        _x, y1 = bot[0]
        e = env.get(int(x // step))
        ya, yb = min(y0, y1), max(y0, y1)
        ok = (e is not None and e[0] - PAD <= ya and yb <= e[1] + PAD) \
            or on_a_terminal(x, ya, yb)
        out.append((lab or col, x, ya, yb, e, ok))
    return out


def main():
    crossings.BODY = ec.ENGINE_BODY
    wrote = ec.dump()
    bad = 0
    for panel, path in sorted(wrote.items()):
        curves = crossings.load(open(path).read())
        env = crossings.envelope(curves)
        rows = anchored(curves, env)
        loose = [r for r in rows if not r[5]]
        print("  %-24s %d tributaries, %d adrift" % (panel, len(rows), len(loose)))
        for lab, x, ya, yb, e, _ok in loose:
            where = (("flow is %.0f..%.0f there" % e) if e
                     else "no flow there at all") + ", and no tributary ends there"
            print("      %s leaves (%.0f,%.0f..%.0f) -- %s" % (lab, x, ya, yb, where))
        bad += len(loose)
    print("  measured against the engine's own render")
    if bad:
        print("  %d tributary/tributaries leave from nowhere" % bad)
        return 1
    print("  every tributary leaves the flow")
    return 0


if __name__ == "__main__":
    sys.exit(main())
