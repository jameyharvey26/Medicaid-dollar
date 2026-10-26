#!/usr/bin/env python3
# engine_texts.py — render the engine headless and write down every string it
# puts on screen, so `teachingproof.py` can measure its `ported` verdicts
# instead of trusting them.
#
# WHY A SEPARATE SCRIPT. teachingproof is a text-set comparison and should stay
# one: cheap, no browser, runs anywhere. Driving chromium is the expensive part
# and it belongs behind its own file so the gate still works on a machine with
# no playwright — it just reports REGISTER ONLY, which is the honest state.
#
# WHAT IT COVERS, AND WHAT IT DOES NOT. The engine draws two panels today, the
# FY2030 national mixed panel and the DC FY2024 panel. The other three are not
# in it yet, so they are absent from the output rather than written empty. An
# empty list would read as "the engine emits nothing for this panel", which is
# a far stronger claim than "nobody has pointed the engine at it".
#
#   python3 engine_texts.py          render and write engine_texts.json
#
# A panel's strings are collected AT THE PUBLISHED DEFAULTS. Moving a control
# changes figures, so a dump taken mid-drag would record $5.40 as though the
# paper said so. The script resets to the published panel before reading.

import json
import os
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(REPO, "engine", "explorer_engine.html")
OUT = os.path.join(REPO, "engine_texts.json")

# The engine's own keys against the panel names the register and build.py use.
# UPDATED 26 October: the engine's controls became two axes, place and year,
# so a panel is a pair. DC|2030 is deliberately absent -- there is no FY2030
# ledger for the District and the engine says so on screen rather than drawing
# one, so there is nothing to compare against.
PANELS = {
    ("US", "2024"): "national_2024",
    ("US", "2030"): "national_2030_mixed",
    ("DC", "2024"): "dc_2024",
}


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  playwright not installed; engine not rendered")
        print("  teachingproof.py will report REGISTER ONLY, which is correct")
        return 0

    if not os.path.exists(ENGINE):
        print("  MISSING  engine/explorer_engine.html")
        return 1

    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1680, "height": 900})
        page.goto("file://" + ENGINE)
        page.wait_for_timeout(1200)

        for (place, year), panel in PANELS.items():
            page.evaluate(
                "a => { document.querySelector(`#place button[data-k=\"${a[0]}\"]`).click();"
                "       document.querySelector(`#year button[data-y=\"${a[1]}\"]`).click(); }",
                [place, year])
            page.wait_for_timeout(500)
            # Back to the published figures before reading anything.
            page.evaluate("() => document.getElementById('reset').click()")
            page.wait_for_timeout(500)
            texts = page.evaluate("""() => {
                const seen = new Set(), out = [];
                for (const el of document.querySelectorAll('svg text, .stn b, .stn span, .drop')) {
                    const t = el.textContent.replace(/\\s+/g, ' ').trim();
                    if (t && !seen.has(t)) { seen.add(t); out.push(t); }
                }
                return out;
            }""")
            out[panel] = texts
            print("  %-22s %4d strings" % (panel, len(texts)))

        browser.close()

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print("  wrote engine_texts.json  (%d panels)" % len(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
