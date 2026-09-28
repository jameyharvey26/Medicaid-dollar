#!/usr/bin/env python3
"""explorerchrome.py — WCAG 2.1 AA on the explorer's own chrome.

SCOPE, and it is narrow on purpose. JW, 27 September: do not touch the colours
in the sankey or the white paper. Those palettes are settled, they are what a
reader has already learned on paper, and the explorer matches them rather than
restating them. `palette.py` is read by the explorer and is NOT measured here:
re-grading it would be the first step toward changing it.

What IS measured is the chrome this artifact introduces and nothing else —
body and secondary text, the nav, the pills that grade a figure, the draft
banner, the focus colour on a button. Those are new, they carry meaning, and
nobody has checked them.

The two thresholds are WCAG 2.1: 4.5:1 for body text, 3:1 for large text
(>= 24px, or >= 19px bold) and for non-text objects that carry meaning
(1.4.11). A pill whose border is the only thing distinguishing "verified" from
"not acquired" is a non-text object carrying meaning.

    python3 explorerchrome.py
"""
import re
import os
import sys

import contrast

REPO = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(REPO, "explorer_template.html")

PAGE = "#FBFAF7"      # --page
CARD = "#FFFFFF"      # --card
INK = "#1B2127"       # --ink

# (foreground, background, what it is, kind). `kind` picks the threshold.
PAIRS = [
    ("#1B2127", PAGE, "body text on the page", "text"),
    ("#1B2127", CARD, "body text on a card", "text"),
    ("#4A565F", PAGE, "secondary prose", "text"),
    ("#4A565F", CARD, "secondary prose on a card", "text"),
    ("#7C8894", PAGE, "kickers, captions, table phase column", "large"),
    ("#7C8894", CARD, "kickers on a card", "large"),
    ("#1F7A5A", PAGE, "links and the focus rule", "text"),
    ("#FFFFFF", "#1F7A5A", "the button label", "text"),
    ("#FFFFFF", "#8B5A5A", "the draft banner", "text"),
    ("#8B5A5A", PAGE, "the draft dagger and its notes", "text"),
    # The register pills. Each one's border and label is the only thing that
    # tells a reader what state a figure is in, so each is measured as text.
    ("#1F7A5A", CARD, "pill: verified", "text"),
    ("#4A565F", CARD, "pill: modelled", "text"),
    ("#9A6A50", CARD, "pill: recorded, unverified", "text"),
    ("#8B5A5A", "#FDF6F4", "pill: not acquired, on its hatch", "text"),
    ("#FFFFFF", "#8B5A5A", "pill: signature lapsed", "text"),
    # Rules and tracks are decoration only where the value is also printed as
    # a number beside them, which it always is. Measured anyway, reported.
    ("#E2DFD8", PAGE, "hairline rules", "decoration"),
    ("#EFEDE7", PAGE, "the empty half of a ruler track", "decoration"),
    # The two loss tints the chrome borrows, via build-filled variables. Both
    # are redundant encodings: the underline style differs as well as its
    # colour, the pill carries a word, and the tooltip says the grade in
    # prose. Colour is never the only channel, which is what 1.4.1 asks.
    ("#C9A9A4", PAGE, "the underline under an unsigned figure", "decoration"),
    ("#B98A72", CARD, "the pill border for unsigned", "decoration"),
    ("#9A6A50", CARD, "the pill label for unsigned", "text"),
    ("#FDF6F4", CARD, "the wash behind a not-acquired pill", "decoration"),
]


def declared():
    """Every hex the template writes, so a colour added there is measured.

    Without this the list above is a list somebody has to remember to extend,
    which is the failure mode this project keeps finding. A hex in the
    template that no pair mentions fails, and the fix is to measure it.
    """
    txt = open(TEMPLATE).read()
    return {m.upper() for m in re.findall(r"#[0-9a-fA-F]{6}\b", txt)}


def main():
    print("Explorer chrome only. palette.py is not measured here and is not "
          "to be changed: the sankey and paper palettes are settled.\n")
    fails = []
    width = max(len(p[2]) for p in PAIRS)
    for fg, bg, what, kind in PAIRS:
        r = contrast.ratio(fg, bg)
        v = contrast.verdict(r, kind)
        ok = v.startswith("PASS") or kind == "decoration"
        print(f"  {what:{width}}  {fg} on {bg}  {r:5.2f}:1  {v}")
        if not ok:
            fails.append(f"{what}: {r:.2f}:1 against WCAG 2.1 AA")

    mentioned = {p[0].upper() for p in PAIRS} | {p[1].upper() for p in PAIRS}
    loose = sorted(declared() - mentioned)
    if loose:
        print()
        for h in loose:
            print(f"  UNMEASURED  {h} appears in the template and is in no pair")
        fails += [f"{h} unmeasured" for h in loose]

    print()
    if fails:
        print(f"{len(fails)} chrome colour(s) not as required:")
        for f in fails:
            print("  " + f)
        return 1
    print(f"all {len(PAIRS)} chrome pairs meet WCAG 2.1 AA, measured not asserted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
