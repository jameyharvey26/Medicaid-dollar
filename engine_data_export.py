#!/usr/bin/env python3
"""engine_data_export.py — the engine's panel data, built from the ledgers.

The engine's `const DATA = {...}` was typed by hand. That is the same leak
`geometry_export.py` was written to close for the spine, and it had the same
consequence: there was no channel from a ledger to the engine, so a figure the
ledger holds could not be drawn at all. Public-company earnings was the one
that made it obvious -- the paper draws it, the ledger carries it, and the
engine had no way to be told about it.

Nothing here is typed. Every number comes off `ledger_*.build()`.

    python3 engine_data_export.py        rewrites the DATA line in the engine

ABSENCE TRAVELS. A payer's retention splits into plan administration and
margin, and for DC neither split is published. That is exported as the
declaration the ledger makes, not as a zero and not as a gap, so the engine can
draw the absence and say so (S-108).
"""
import json
import os
import re

import ledger

REPO = os.path.dirname(os.path.abspath(__file__))
# `exportproof.py` points this at a copy so it can check for drift without
# writing to the tree. Nothing else sets it.
ENGINE = os.environ.get("EXPORTPROOF_ENGINE") or os.path.join(
    REPO, "engine", "explorer_engine.html")

_DATA_LINE = re.compile(r"^const DATA = .*;$", re.M)

# panel key in the engine -> (ledger builder, view)
PANELS = [
    ("US|2024", "ledger_national_2024", None, "US2024", "National", "V_NAT"),
    ("US|2030", "ledger_national_2030", "mixed", "US2030_mixed", "National", "V_2030"),
    ("DC|2024", "ledger_dc_2024", None, "DC2024", "DC", "V_DC"),
]


def fig(f):
    """A figure, or the ledger's own words for why there isn't one."""
    if f is None:
        return None
    if f.status == ledger.ABSENT:
        return {"absent": f.note}
    return round(float(f.n), 4)


def panel(L, code, name, strap, disp):
    lanes = []
    for p in L.payers:
        if getattr(p, "parent", None):
            continue                      # a plan inside a lane, not a lane
        lanes.append({
            "key": p.key, "label": p.label, "kind": p.kind,
            "cap": fig(p.capitation), "care": fig(p.care),
            # the two halves of what the lane kept. Public-company earnings is
            # carved out of margin, so the engine needs the split, not the sum.
            "adm": fig(p.admin), "margin": fig(p.margin),
        })
    cells = {f"{r}|{c}": round(float(v.n), 4)
             for (r, c), v in L.claims.cell.items()}
    return {
        "code": code, "name": name, "strap": strap,
        "sources": {k: round(float(v.n), 4) for k, v in L.sources.items()},
        "peels": [{"label": p.label, "v": round(float(p.amount.n), 4),
                   "kind": p.kind, "charged": p.charged, "reach": p.reach}
                  for p in L.peels],
        "lanes": lanes, "cells": cells, "disp": dict(disp),
        "cols": list(L.claims.cols),
        # what reached a claim. The service mix totals it where the mix is
        # published; where it is not -- DC -- the lane care does, because a
        # missing mix is not a missing claim.
        "claims": round(sum(float(v.n) for v in L.claims.col_margin.values())
                        or sum(float(p.care.n) for p in L.payers
                               if not getattr(p, "parent", None)), 4),
    }


def reconcile(data):
    """What a lane kept must equal what it administered plus what it made.

    The split is the point of the export, so a split that does not add up is
    worse than no split at all: it would put a figure on the plate that the
    ledger never stood behind.
    """
    bad = []
    for key, p in data.items():
        if not p:
            continue
        for l in p["lanes"]:
            kept = l["cap"] - l["care"]
            if isinstance(l["adm"], dict) or isinstance(l["margin"], dict):
                continue
            if abs(l["adm"] + l["margin"] - kept) > 0.0015:
                bad.append("%s %s: kept %.4f, adm+margin %.4f"
                           % (key, l["key"], kept, l["adm"] + l["margin"]))
    return bad


def build():
    import importlib
    import views
    out = {}
    for key, mod, variant, code, name, vname in PANELS:
        m = importlib.import_module(mod)
        L = m.build(variant) if variant else m.build()
        V = getattr(views, vname)
        out[key] = panel(L, code, name, V.strap, V.disp)
    out["DC|2030"] = None     # no FY2030 DC ledger, and the national shape is
    return out                # not a stand-in for one


def main():
    data = build()
    off = reconcile(data)
    if off:
        raise SystemExit("engine_data_export: the retention split does not "
                         "reconcile, so nothing was written:\n  " +
                         "\n  ".join(off))
    line = "const DATA = %s;" % json.dumps(data, separators=(",", ":"))
    src = open(ENGINE).read()
    new, n = _DATA_LINE.subn(lambda _: line, src, count=1)
    if n != 1:
        raise SystemExit("engine_data_export: could not find `const DATA = ...;` "
                         "in engine/explorer_engine.html — the engine must keep "
                         "that declaration on one line so this script can "
                         "replace it.")
    open(ENGINE, "w").write(new)
    live = [k for k, v in data.items() if v]
    absent = sum(1 for k in live for l in data[k]["lanes"]
                 for f in ("adm", "margin") if isinstance(l[f], dict))
    print("  rewrote the DATA line in engine/explorer_engine.html")
    print("  %d panels, %d lane splits declared absent" % (len(live), absent))
    print("  every published split reconciles with what its lane kept")


if __name__ == "__main__":
    main()
