#!/usr/bin/env python3
"""explorerproof.py — no figure reaches the explorer except through the ledger.

S-105 says: derive in code, never type an output, and `typedfigures.py` is the
detection instrument for the paper. This is the instrument for the web
artifact, and it has to work differently, because a web page can produce a
number three ways and only one of them looks like a typed figure in source.

  1. a literal in the template          — a static read catches it
  2. arithmetic in the page's script    — a static read does not
  3. a value correctly serialized       — legitimate

Case 2 is the one that bit. The first build of the flow view summed three
rounded lane margins in JavaScript and printed $87.08 where the ledger says
87.074936, which prints $87.07. Nothing was typed. Every input was serialized.
The page still disagreed with the paper by a cent, because the addition
happened after rounding.

So this gate does not read the template. It RENDERS the built page, walks every
view and every jurisdiction, harvests every dollar figure that actually appears
on screen, and asserts each one is a value `explorer.py` serialized. A figure
the page computed for itself is not in the payload and fails by name.

    python3 explorerproof.py [path/to/medicaid_dollar_explorer.html]
"""
import asyncio
import json
import os
import re
import sys

OUT = "/mnt/user-data/outputs"
DEFAULT = os.path.join(OUT, "medicaid_dollar_explorer.html")

# A dollar figure as the page prints it: $12.34, or −$1.25 with the minus sign
# the page uses. Two decimals, which is every figure the explorer displays.
MONEY = re.compile(r"[\u2212-]?\$(\d[\d,]*\.\d\d)")

# Figures that are true by construction rather than by measurement, and are
# allowed on screen without a matching serialized value. Kept deliberately
# short: each entry is a hole in the instrument and has to earn its place.
ALLOWED = {
    "100.00",     # the hundred. It is the denominator, not a measurement.
}


def harvest(payload) -> set:
    """Every value `explorer.py` serialized, as the page would print it.

    Walks the whole payload rather than naming fields, so a figure added to
    the serializer is covered the day it is added and nobody has to remember
    to extend this list.
    """
    seen = set()

    def walk(x):
        if isinstance(x, dict):
            if "v" in x and isinstance(x.get("v"), (int, float)):
                seen.add(f"{abs(float(x['v'])):.2f}")
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, (int, float)):
            # Bare numbers in the payload are coordinates and scale factors,
            # not figures, but a page that prints one is still printing
            # something the ledger produced. Admitted, and cheap.
            seen.add(f"{abs(float(x)):.2f}")

    walk(payload)
    return seen


async def onscreen(path):
    """Render the page and return {where: [figures]} for every view."""
    from playwright.async_api import async_playwright
    url = "file://" + os.path.abspath(path)
    # D-111. Two views now: the diagram (with the phases and the law
    # under it on one scroll) and the summary (with the register under it).
    views = ["plate", "reading"]
    found = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": 1400, "height": 1000})
        await pg.goto(url)
        await pg.click("#enter")
        await pg.wait_for_timeout(250)
        # The page opens on FY2030 now; the sweep starts from the baseline.
        await pg.select_option("#year", "2024")
        await pg.wait_for_timeout(250)

        async def home():
            # The controls live on the diagram and are hidden on the summary,
            # so come back before touching them.
            await pg.click('nav button[data-v="plate"]')
            await pg.wait_for_timeout(150)

        async def sweep(tag):
            for v in views:
                await pg.click(f'nav button[data-v="{v}"]')
                await pg.wait_for_timeout(120)
                txt = await pg.inner_text("#v-" + v)
                found[f"{tag}/{v}"] = MONEY.findall(txt)

        await sweep("US2024")
        await home()
        await pg.select_option("#year", "2030")
        await pg.wait_for_timeout(200)
        await sweep("US2030/mixed")
        # The law panel lives under the diagram on the same scroll now, so
        # there is no tab to come back to; it is already on screen.
        await pg.click('nav button[data-v="plate"]')
        await pg.wait_for_timeout(150)
        # Every provision alone, and then cumulatively, because the checkbox
        # total is a different figure at every step and each one has to be a
        # figure the ledger serialized.
        levers = await pg.eval_on_selector_all(
            ".lever", "els => els.map(e => e.dataset.key)")
        for lev in levers:
            await pg.click(f'.lever[data-key="{lev}"]')
            await pg.wait_for_timeout(110)
            found[f"US2030/lever/{lev}"] = MONEY.findall(
                await pg.inner_text("#v-law"))
            await pg.click(f'.lever[data-key="{lev}"]')
        for i, lev in enumerate(levers):
            await pg.click(f'.lever[data-key="{lev}"]')
            await pg.wait_for_timeout(110)
            found[f"US2030/cumulative/{i+1}"] = MONEY.findall(
                await pg.inner_text("#v-law"))
        for lev in levers:
            await pg.click(f'.lever[data-key="{lev}"]')
        for var in ("holds", "scales"):
            await home()
            await pg.select_option("#variant", var)
            await pg.wait_for_timeout(200)
            await sweep("US2030/" + var)
        # The District panel is in the payload and is no longer offered in
        # the picker (JW, 28 September), so there is nothing to sweep for it.
        await b.close()
    return found


def main(path=DEFAULT):
    data = json.load(open(os.path.join(OUT, "explorer_data.json")))
    # Two sources, and the gate knows which is which. The serializer produced
    # the first; build_deck.py produced the second off the same ledger, and the
    # fact cards arrive as formatted HTML rather than as fields. Anything in
    # neither was computed by the page itself, which is the thing being caught.
    serialized = harvest({k: v for k, v in data.items() if k != "facts"})
    deck = {f for c in data.get("facts", []) for f in c.get("figures", [])}
    # Third named source: the labels sankey.py drew into the plate, off this
    # same ledger, under renderproof.py and check(). Named rather than waved
    # through, so the split stays visible in this report.
    drawn = {f for p in data["panels"].values()
             for f in (p.get("plate") or {}).get("drawn", [])}
    known = serialized | deck | drawn | ALLOWED
    screen = asyncio.run(onscreen(path))

    bad, total = [], 0
    for where, figs in screen.items():
        for f in figs:
            total += 1
            if f.replace(",", "") not in known:
                bad.append((where, f))

    print(f"swept {len(screen)} page states, {total} figures on screen")
    print(f"  {len(serialized)} distinct values from explorer.py")
    print(f"  {len(deck)} distinct values from build_deck.py (the fact cards)")
    print(f"  {len(drawn)} distinct values from sankey.py (drawn into the plate)")
    if bad:
        print(f"\n{len(bad)} figure(s) the page produced that the ledger did not:")
        for where, f in sorted(set(bad)):
            print(f"  {where:28s} ${f}")
        print("\nA figure on screen that is not in explorer_data.json was "
              "computed by the page. Derive it in explorer.py instead (S-105).")
        return 1

    # The static half. Cheap, and it catches the obvious case the render
    # cannot: a literal sitting in a branch no sweep happened to reach.
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "explorer_template.html")).read()
    lit = [m for m in MONEY.findall(tpl)]
    if lit:
        print(f"\ntemplate carries {len(lit)} literal figure(s): {lit}")
        return 1

    print("every figure on screen is one the ledger serialized")
    print("no dollar literal in the template")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT))
