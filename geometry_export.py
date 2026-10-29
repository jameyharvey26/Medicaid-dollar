#!/usr/bin/env python3
# geometry_export.py — the spine, written out once for the engine to read.
#
# STEP 1 OF THE PORT (GEOMETRY_CONTRACT.md §8). The columns, the scale and the
# ribbon shape are declared in Python today and the browser needs the same
# numbers. The wrong fix is to type them into the engine: that is S-096, the
# same nine numbers in two files, and it is exactly how D-87 came to need
# applying twice in places that could have disagreed.
#
# So Python stays the single declaration and this script exports it. The engine
# reads the export. Nothing is typed twice, and a change to COLS reaches the
# browser by rebuilding rather than by remembering.
#
#   python3 geometry_export.py        writes engine/geometry.json
#
# This script deliberately computes nothing. If a value here needed deriving,
# it would belong in the module it comes from, not in the exporter.

import json
import os
import re

import outflows as OF
import sankey
from instances import T_SLOT

# Keys of an OUTFLOWS entry the engine needs. Listed rather than copied wholesale
# so that adding a Python-only field to OUTFLOWS does not silently become part of
# the engine's contract.
_OF_KEYS = ("cls", "src", "edge", "src_x", "term_col", "term_y", "ret",
            "term_dy", "reach", "label", "label_side", "label_dy")

REPO = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(REPO, "engine", "geometry.json")
# `exportproof.py` points this at a copy so it can check for drift without
# writing to the tree. Nothing else sets it.
ENGINE = os.environ.get("EXPORTPROOF_ENGINE") or os.path.join(
    REPO, "engine", "explorer_engine.html")

# The engine runs from file://, where fetch() of a sibling JSON is blocked, so
# the spine has to be inlined in the page. It was inlined BY HAND, which is the
# S-096 leak this script exists to close: the export was written and the engine
# went on carrying a stale copy, and that is how `REACHX` came to disagree with
# the tracker lattice in three of seven slots without anything failing. The
# exporter now rewrites the line. Nobody types the spine.
_GEOM_LINE = re.compile(r"^const GEOM = .*;$", re.M)


def _inject(geom):
    if not os.path.exists(ENGINE):
        return "SKIPPED (engine not present)"
    src = open(ENGINE).read()
    line = "const GEOM = %s;" % json.dumps(geom, separators=(",", ":"))
    new, n = _GEOM_LINE.subn(lambda _: line, src, count=1)
    if n != 1:
        raise SystemExit("geometry_export: could not find `const GEOM = ...;` "
                         "in engine/explorer_engine.html — the engine must keep "
                         "that declaration on one line so this script can "
                         "replace it.")
    if new == src:
        return "unchanged"
    open(ENGINE, "w").write(new)
    return "rewrote the GEOM line in"


def main():
    geom = {
        # §1 the spine. frozen, not derived from anything.
        "cols": {k: list(v) for k, v in OF.COLS.items()},
        "source_x": OF.SOURCE_X,
        "canvas": {"w": sankey.W, "h": sankey.H},
        # one number, everywhere: this is what makes the columns puzzle pieces
        "ys": sankey.ys,
        "bw": sankey.bw,
        "centre_y": sankey.cY,
        # §2 ribbon shape. the cap is what makes a long tributary fall early
        # and then travel flat and low, under its neighbours, instead of
        # riding at mid-height and cutting everything that stops short of it.
        "ctrl_max": sankey.CTRL_MAX,
        # §5 the fan
        "fan": {
            "top": OF.FAN_TOP,
            "min_gap": OF.FAN_MIN_GAP,
            "tight_gap": OF.FAN_TIGHT_GAP,
            "label_h": OF.FAN_LABEL_H,
            "label_h_tight": OF.FAN_LABEL_H_TIGHT,
            "rule_y": OF.RULE_Y,
            "floor": OF.FAN_FLOOR,
            "stack_top": sankey.FAN_STACK_TOP,
        },
        # the two source bar tops, read from render() rather than guessed
        "source_tops": {"federal": 126.0, "state": 655.0},
        # §6 THE TRACKER LATTICE. instances.T_SLOT, verbatim.
        #
        # A tributary's terminal x is not a free choice and it is not a column
        # coordinate: it is the tracker slot of the subtraction the tributary
        # belongs to, so the ribbon lands where its money is accounted for
        # (instances.py, S-075/S-085). The engine hand-built its own table off
        # column edges and got three of seven slots wrong, including an invented
        # PROVIDERS slot. There is no PROVIDERS edge here and that is deliberate:
        # the lattice has six slots, the drawing has eight columns, and a reach
        # with no slot rides the slot of the column it is CHARGED at. That rule
        # is the export's, not the reader's to guess — see `term_fallback`.
        "term_slot": {k: float(v) for k, v in T_SLOT.items()},
        "term_fallback": "charged",
        # §7 the outflow declarations. outflows.OUTFLOWS, the table that says
        # where each tributary leaves the trunk (`src_x`, `edge`), how far it
        # runs (`reach`), where it is pinned if it is pinned (`term_y`), and
        # what the artifact PRINTS (`label`) as against its internal key. The
        # printed name is what a reader sees, so it belongs here and not in a
        # renderer constant (S-079).
        #
        # `term_dy` is a pin: a declared terminal height, given as an offset
        # BELOW the fan's first row so that it survives the rule moving. Any
        # remaining absolute `term_y` belongs to an ordinary outflow that is
        # not a fan participant and is not a pin for this purpose.
        # ALIASES ARE EXCLUDED. A state edition that renames a lane adds a key
        # to OUTFLOWS pointing at geometry that is already exported under the
        # national name. Exporting both would put a second entry in the
        # engine's spine for one position on the flow, and the engine would
        # carry a District editorial decision as though it were geometry.
        # The rename belongs to the view, not to the spine.
        "outflows": {
            name: {k: d[k] for k in _OF_KEYS if d.get(k) is not None}
            for name, d in OF.OUTFLOWS.items() if name not in OF.ALIASES
        },
    }
    # The fan's first row sits this far below the HR-1 rule. sankey._draw_hr1
    # declares it as `top=rule_y+18`; the engine had typed 40.
    geom["fan"]["top_off"] = sankey.FAN_TOP_OFF
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(geom, fh, indent=1)
    print("  wrote engine/geometry.json")
    print("  %s engine/explorer_engine.html" % _inject(geom))
    print("  cols %d, ys %.2f, bw %d, ctrl_max %.0f, rule_y %.0f"
          % (len(geom["cols"]), geom["ys"], geom["bw"],
             geom["ctrl_max"], geom["fan"]["rule_y"]))
    print("  term slots %d (no PROVIDERS edge, by design), outflows %d, "
          "printed names %d"
          % (len(geom["term_slot"]), len(geom["outflows"]),
             sum(1 for d in geom["outflows"].values() if "label" in d)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
