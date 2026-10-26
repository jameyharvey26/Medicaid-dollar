#!/usr/bin/env python3
"""enginecrossings.py — run crossings.py's detector against the engine's render.

STEP 5 OF THE PORT (GEOMETRY_CONTRACT.md §8). Until this existed, every claim
that the engine's tributaries did not cross was made by eye, by me, and was
wrong twice: once with an invented ordering and once with a detector I wrote
myself that matched sample points by nearest-x and reported ten crossings on a
picture that had none.

So nothing new is written here. The engine emits sankey's path grammar, this
script dumps its SVG headless, and `crossings.report` — the detector that has
gated the paper since September — reads it. The rule being enforced is still
JW's, scoped by REGION: a ribbon leaving the middle of the stack has to cut
across whatever sits between it and the edge, and that is the flow working, not
a defect. Only crossings where BOTH curves are out in the margin count.

    python3 enginecrossings.py

The one thing that must be supplied is the body palette. `crossings.BODY` is
sankey's six main-flow hexes; the engine draws the same six lanes in the
explorer's palette, and the envelope is derived from whichever set is on the
page. Everything else — the sampling, the join exemption, the margin test — is
untouched.
"""
import os
import sys

import crossings

REPO = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(REPO, "engine", "explorer_engine.html")
OUT = os.path.join(REPO, "engine_renders")

PANELS = {("US", "2024"): "national_2024",
          ("US", "2030"): "national_2030_mixed",
          ("DC", "2024"): "dc_2024"}

# The engine's main-flow lanes, the same six the paper's BODY names.
ENGINE_BODY = {"#3D6E8C", "#A8BFCE", "#1F7A5A", "#4A54A8", "#6F80C4", "#8494A6"}


def dump():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    written = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1900, "height": 1200})
        pg.goto("file://" + ENGINE)
        pg.wait_for_timeout(1200)
        for (place, year), panel in PANELS.items():
            pg.evaluate(
                "a => { document.querySelector(`#place button[data-k=\"${a[0]}\"]`).click();"
                "       document.querySelector(`#year button[data-y=\"${a[1]}\"]`).click(); }",
                [place, year])
            pg.wait_for_timeout(500)
            pg.evaluate("() => document.getElementById('reset').click()")
            pg.wait_for_timeout(400)
            svg = pg.evaluate("() => document.querySelector('#plate svg').outerHTML")
            # fills that are patterns carry no colour the envelope can use; they
            # are tributaries, never body, so a flat loss hex is the honest
            # substitute and keeps the grammar parseable.
            svg = svg.replace('fill="url(#hr1)"', 'fill="#8B5A5A"')
            svg = svg.replace('fill="url(#ab)"', 'fill="#7C3AED"')
            path = os.path.join(OUT, f"{panel}_combined.svg")
            with open(path, "w") as fh:
                fh.write(svg)
            written[panel] = path
        br.close()
    return written


def main():
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("  playwright not installed; engine not rendered")
        return 0

    if not os.path.exists(ENGINE):
        print("  MISSING  engine/explorer_engine.html")
        return 1

    written = dump()
    crossings.BODY = ENGINE_BODY
    bad = 0
    for panel, path in sorted(written.items()):
        hits = crossings.report(path)
        bad += len(hits)
        print(f"  {panel:24s} {len(hits)} crossing(s) in the margin")
        for l1, l2, x, y in hits[:6]:
            print(f"      at ({x:.0f},{y:.0f})  {l1}  x  {l2}")
    print("  measured by crossings.report, the paper's own detector")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
