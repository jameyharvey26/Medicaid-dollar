#!/usr/bin/env python3
"""engine_fonts.py — put the two typefaces inside the engine.

The engine linked Jost and Nunito from Google Fonts. That is fine on a desk
and not fine in a room: on a bad connection, or on a machine behind a filter,
the whole thing falls back to a system sans and every layout figure the panel
reports is then measuring the wrong typeface. A demo file should not have a
dependency the room can break.

So the fonts travel inside the file, from paper_fonts/, which is the same
pair the paper renders with and the same pair build_explorer.py already
embeds. One source for the typeface, as for everything else.

    python3 engine_fonts.py        inline them (idempotent)

Idempotent on purpose: it detects its own marker and does nothing rather than
stacking a second copy, so it is safe to run from a build step.
"""
import base64
import os
import re
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(REPO, "engine", "explorer_engine.html")
FONTS = os.path.join(REPO, "paper_fonts")
MARK = "<!-- fonts inlined by engine_fonts.py -->"
LINK = re.compile(r'\s*<link[^>]*fonts\.googleapis\.com[^>]*>\s*')


def face(name, filename):
    """ONE blob per family, not one per weight.

    The first cut of this declared a separate @font-face for each weight the
    engine asks for, which embedded the same 270KB of Nunito three times and
    took the file to 1.8MB. A weight RANGE on a single face gets the same
    result -- the browser synthesises the heavier cuts from the one outline,
    exactly as it did when a Google weight failed to load -- at a third of
    the size.
    """
    path = os.path.join(FONTS, filename)
    b64 = base64.b64encode(open(path, "rb").read()).decode("ascii")
    return (f"@font-face{{font-family:'{name}';font-style:normal;"
            f"font-weight:100 900;font-display:block;"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype')}}")


def main():
    src = open(ENGINE).read()
    if MARK in src:
        print("  fonts already inlined; nothing to do")
        return 0
    if not LINK.search(src):
        print("  no Google Fonts link found and no marker — check the engine "
              "by hand rather than letting this guess")
        return 1
    css = (f"\n{MARK}\n<style>\n"
           + face("Jost", "Jost.ttf") + "\n"
           + face("Nunito", "Nunito.ttf") + "\n"
           + "</style>\n")
    out = LINK.sub(css, src, count=1)
    open(ENGINE, "w").write(out)
    kb = (len(out) - len(src)) / 1024
    print(f"  inlined Jost and Nunito into engine/explorer_engine.html "
          f"(+{kb:,.0f} KB)")
    print("  the engine no longer needs a network connection to look right")
    return 0


if __name__ == "__main__":
    sys.exit(main())
