#!/usr/bin/env python3
"""deckfit.py - the deck's stranding gate.

The manuscript has whitespace.py and sectionfit.py because a page that
overflows or strands is a defect the eye finds last. The deck now has fixed
slide boxes, which means overflow is silently CLIPPED rather than pushed onto
a following page - worse, not better, unless something measures it.

This measures every slide in a real browser:

  OVERFLOW  content is taller than the box. Something is cut off.
  STRAND    content ends far above the folio. Dead space on a fixed page.

Run after build_deck.py. Exits non-zero on any overflow.
"""
import sys

from playwright.sync_api import sync_playwright

DECK = "file:///mnt/user-data/outputs/MHPA_Board_Deck.html"
STRAND_IN = 1.30          # inches of dead air before it counts as stranding
DPI = 96.0

JS = """
() => Array.from(document.querySelectorAll('.slide')).map((s, i) => {
  const cs = getComputedStyle(s);
  const padTop = parseFloat(cs.paddingTop);
  const box = s.clientHeight;
  const folio = s.querySelector('.folio');
  const limit = folio
    ? folio.getBoundingClientRect().top - s.getBoundingClientRect().top
    : box - parseFloat(cs.paddingBottom);
  // the lowest ink among the slide's own children, folio excluded
  let bottom = padTop;
  for (const el of s.children) {
    if (el.classList.contains('folio')) continue;
    const r = el.getBoundingClientRect();
    const b = r.bottom - s.getBoundingClientRect().top;
    if (b > bottom) bottom = b;
  }
  // With the figure set to absorb slack, the flow always reaches the folio,
  // so trailing space is no longer the measure. The honest number is the
  // height inside the figure frame that the image does not fill.
  let air = 0;
  const fig = s.querySelector('.fig');
  if (fig) {
    const im = fig.querySelector('img');
    if (im) air = fig.clientHeight - im.getBoundingClientRect().height
                  - parseFloat(getComputedStyle(fig).paddingTop) * 2;
  }
  const kick = s.querySelector('.kicker');
  return {
    i,
    name: kick ? kick.textContent.trim()
                : (s.className.includes('cover') ? 'Cover' : 'Contents'),
    box, limit, bottom, air,
    scroll: s.scrollHeight,
  };
})
"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1120, "height": 880})
        pg.goto(DECK)
        pg.wait_for_timeout(2500)
        rows = pg.evaluate(JS)
        b.close()

    faults = 0
    print(f"{'#':>3}  {'slide':44} {'used':>7} {'limit':>7}  verdict")
    print("-" * 86)
    for r in rows:
        used, limit = r["bottom"], r["limit"]
        gap_in = (limit - used) / DPI
        if used > limit + 1 or r["scroll"] > r["box"] + 1:
            v, faults = f"OVERFLOW by {(used - limit) / DPI:.2f}in", faults + 1
        elif r["air"] / DPI > STRAND_IN:
            v = f"air {r['air'] / DPI:.2f}in in the figure frame"
        elif gap_in > STRAND_IN:
            v = f"strand {gap_in:.2f}in"
        else:
            v = "ok"
        print(f"{r['i']:>3}  {r['name'][:44]:44} "
              f"{used / DPI:6.2f}in {limit / DPI:6.2f}in  {v}")
    print("-" * 86)
    print(f"{len(rows)} slides, {faults} overflow(s)")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
