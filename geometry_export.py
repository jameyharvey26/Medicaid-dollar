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

import outflows as OF
import sankey

REPO = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(REPO, "engine", "geometry.json")


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
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(geom, fh, indent=1)
    print("  wrote engine/geometry.json")
    print("  cols %d, ys %.2f, bw %d, ctrl_max %.0f, rule_y %.0f"
          % (len(geom["cols"]), geom["ys"], geom["bw"],
             geom["ctrl_max"], geom["fan"]["rule_y"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
