"""Does any body text reach the provenance line?

The footer used to be `position:fixed; bottom:4mm`. In a paged context a fixed
element is positioned against the PAGE AREA, not the paper, so that put it 4mm
above the bottom of the flowing text — inside the column — and the last line of
a page was set straight through it. D-93 stamps it into the margin instead.

This measures the result rather than trusting the arithmetic, and it works on
text lines rather than blocks, because when the two overlap the extractor
merges them into one block and a block-level check cannot tell them apart.

The footer is identified by its own text. The first version of this file took
"whatever sits lowest on the page", and when the footer jumped to the top of
every page it went on reporting a clean result by measuring body text against
body text. A detector that cannot tell it has lost its subject is not one.

    python3 footerfit.py <rendered.pdf> [clearance_pt]
"""
import sys
import pymupdf

CLEAR = 6.0          # points of air the footer is entitled to
MARKS = ("build ", "pending]")


def lines(page):
    """Every text line on the page as (y0, y1, text)."""
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            txt = "".join(s["text"] for s in line["spans"]).strip()
            if txt:
                out.append((line["bbox"][1], line["bbox"][3], txt))
    return out


def main(path, clear=CLEAR):
    doc = pymupdf.open(path)
    bad = pages_with_footer = 0
    for pno, page in enumerate(doc, start=1):
        ls = lines(page)
        # Both tests, not either: the marks alone match body prose (the
        # sourcing paragraph names the build), and position alone was the
        # failure this file exists to avoid.
        floor = page.rect.height * 0.85
        foot = [l for l in ls
                if l[0] > floor and any(m in l[2] for m in MARKS)]
        if not foot:
            continue
        pages_with_footer += 1
        ftop = min(l[0] for l in foot)
        fbot = max(l[1] for l in foot)
        for y0, y1, txt in ls:
            # Anything on the footer's own baseline IS the footer. The centre
            # field is a page number, which carries none of the marks the
            # left and right fields do, and the first version of this test
            # reported it as body text colliding with itself on every page.
            if y1 > ftop - 1 and y0 < fbot + 1:
                continue
            if y1 > ftop - clear:
                bad += 1
                print(f"  page {pno:2}  text reaches y={y1:.1f}, footer starts "
                      f"at y={ftop:.1f}   {txt[:56]!r}")
    if not pages_with_footer:
        print("\nFOOTER NOT FOUND on any page. It is missing or has moved; "
              "this file cannot report on a line it cannot locate.")
        return 1
    print(f"\n{bad} footer collision(s) at {clear:.0f}pt clearance"
          f", over {pages_with_footer} pages" if bad else
          f"\nno body text within {clear:.0f}pt of the footer, "
          f"over {pages_with_footer} pages")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else CLEAR))
