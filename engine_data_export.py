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
    # Added 2026-10-29 PM. The FY2030 DC panel was `None` here because three
    # of its seven HR-1 lanes carried no figure and this engine has no way to
    # draw absence, so they would have read as costing nothing. Two of the
    # three are now drawn as declared assumptions off the national model and
    # the third -- the seniors lane -- is derived on the District's own
    # QMB-only count. Every assumption says so in its own note, and the notes
    # travel. What is still owed is in DC_ENGINE_TODO.md.
    ("DC|2030", "ledger_dc_2030", None, "DC2030", "DC", "V_DC_2030"),
]


def fig(f):
    """A figure, or the ledger's own words for why there isn't one."""
    if f is None:
        return None
    if f.status == ledger.ABSENT:
        return {"absent": f.note}
    return round(float(f.n), 4)


def plan_colour_map(mod, L):
    import palette as PAL
    names = getattr(mod, "PLAN_PALETTE", None)
    if not names:
        return {}
    size = {}
    for p in L.payers:
        if getattr(p, "parent", None) and p.key in names:
            size[names[p.key]] = float(p.capitation.n)
    plans = [{"name": n, "size": size.get(n, 0.0)} for n in set(names.values())]
    assigned, warnings = PAL.audit_state_palette(plans)
    hard = [w for w in warnings if w.startswith("COLLISION")]
    if hard:
        raise SystemExit(
            "engine_data_export: the state palette collides, so nothing was "
            "written. Two plans a reader cannot tell apart is worse than no "
            "split at all:\n  " + "\n  ".join(hard))
    for w in warnings:
        print("  palette note: " + w)
    return {k: assigned[n] for k, n in names.items() if n in assigned}


def plans_of(L, lane_key, cols=None):
    """The named plans inside a lane, in the order the ledger holds them.

    These were dropped on the floor by this exporter until 28 October: the
    ledger has held them as Payers with `parent` set since the DC panel was
    built, and the engine was never told. A state panel whose payer column
    says only "MCO capitation" is answering a question nobody asks. In a
    state, the plans ARE the payer column.
    """
    out = []
    for p in L.payers:
        if getattr(p, "parent", None) != lane_key:
            continue
        out.append({
            "key": p.key, "label": p.label,
            "entity": getattr(p, "entity", "") or "",
            # the reserved colour travels with the plan, so the engine never
            # has to invent one
            "col": (cols or {}).get(p.key),
            "cap": fig(p.capitation), "care": fig(p.care),
            "adm": fig(p.admin), "margin": fig(p.margin),
        })
    return out


def panel(L, code, name, strap, disp, cols=None):
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
            "plans": plans_of(L, p.key, cols),
        })
    cells = {f"{r}|{c}": round(float(v.n), 4)
             for (r, c), v in L.claims.cell.items()}
    return {
        "code": code, "name": name, "strap": strap,
        "sources": {k: round(float(v.n), 4) for k, v in L.sources.items()},
        # ABSENCE TRAVELS HERE TOO. `p.amount.n` is 0.0 for an absent figure,
        # so this line turns "no DC figure for this lever" into "this lever
        # costs nothing" the moment a panel with absent peels is exported. No
        # national panel has one, so it never fired; the DC FY2030 panel has
        # three. fig() carries the ledger's own words instead.
        "peels": [{"label": p.label, "v": fig(p.amount),
                   "kind": p.kind, "charged": p.charged, "reach": p.reach}
                  for p in L.peels],
        "lanes": lanes, "cells": cells, "disp": dict(disp),
        # Does the service fan rest on an ASSUMPTION? The cells export as bare
        # numbers, so their status would be lost on the way here and the
        # engine would draw an assumed mix exactly as it draws a measured one.
        # The panel that used to say THE FLOW STOPS HERE now draws a fan; it
        # has to say, just as plainly, what that fan is.
        "mix_assumed": any(
            v.status == ledger.MODELLED
            for (r, _c), v in L.claims.cell.items()
            if r in ("mco", "dual")),
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
            # the plans inside a lane must account for the whole lane, or the
            # payer column would draw a sliver of unnamed money with no owner
            ps = [q for q in l.get("plans", [])
                  if not isinstance(q["care"], dict)]
            if ps and len(ps) == len(l.get("plans", [])):
                for field in ("cap", "care"):
                    tot = sum(q[field] for q in ps)
                    if abs(tot - l[field]) > 0.0015:
                        bad.append("%s %s: plans %s %.4f, lane %.4f"
                                   % (key, l["key"], field, tot, l[field]))
    return bad


def build():
    import importlib
    import views
    out = {}
    for key, mod, variant, code, name, vname in PANELS:
        m = importlib.import_module(mod)
        # DC carries the assumed national service mix (JW, 2026-10-29). It is
        # an assumption and every cell it produces says so in its own note,
        # which travels to the engine through fig().
        L = (m.build(variant) if variant
             else m.build(assumed_mix=True) if key.startswith("DC|")
             else m.build())
        V = getattr(views, vname)
        out[key] = panel(L, code, name, V.strap, V.disp,
                         plan_colour_map(m, L))
    # A lane that still carries no figure must not reach the engine as a
    # zero. fig() turns an absent Fig into {"absent": "<why>"} and the engine
    # is not yet taught to draw that in the HR-1 fan, so refuse here rather
    # than ship a lane that reads as costing nothing. With assumed_levers on
    # there are none; turning the switch off will trip this, which is the
    # correct moment to teach the engine placeholders.
    for key, p in out.items():
        if not p:
            continue
        blank = [x["label"] for x in p["peels"]
                 if x["kind"] == "hr1" and isinstance(x["v"], dict)]
        if blank:
            raise SystemExit(
                "engine_data_export: %s carries HR-1 lane(s) with no figure "
                "(%s). The engine cannot draw absence in the fan yet, and a "
                "lane drawn at zero would say the provision costs nothing. "
                "Either leave assumed_levers on or teach the engine "
                "placeholders first." % (key, ", ".join(blank)))
    return out


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
    named = sum(len(l.get("plans", [])) for k in live
                for l in data[k]["lanes"])
    print("  %d panels, %d lane splits declared absent" % (len(live), absent))
    print("  %d named plans inside the payer lanes" % named)
    print("  every published split reconciles with what its lane kept")


if __name__ == "__main__":
    main()
