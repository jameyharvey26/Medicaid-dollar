"""Does every section start a page?

D-96. It is a rule of these white papers, not a preference: a reader who puts
the paper down and picks it up again finds a section boundary where a page
boundary is. It held for the first five sections by accident - four carried an
inline break-before and the rest happened to fall right - and broke from page
15 onward, where a section head landed halfway down a page under the tail of
the section before it.

    python3 sectionfit.py <rendered.pdf>

A section head is found by type size, not by wording, for the same reason
whitespace.py detects one that way: the labels are editorial and can change,
and a detector tied to wording breaks the moment the wording does.

The test is that a section head is the FIRST content on its page. Anything
printed above it belongs to the section before, which is the failure.
"""
import re
import sys
import pymupdf

HEAD_PT = 18.0          # h2.sec is 21pt; nothing else in the paper is near it
FOOTER_MARKS = ("build ", "pending]")
PAGENO = re.compile(r"^Page \d+ of \d+$")


def lines(page):
    """(y0, y1, size, text) for every text line, footer excluded."""
    floor = page.rect.height * 0.85
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = [sp for sp in line["spans"] if sp["text"].strip()]
            if not spans:
                continue
            txt = "".join(sp["text"] for sp in spans).strip()
            if line["bbox"][1] > floor and (
                    any(m in txt for m in FOOTER_MARKS) or PAGENO.match(txt)):
                continue
            out.append((line["bbox"][1], line["bbox"][3],
                        max(sp["size"] for sp in spans), txt))
    return sorted(out)


def main(path):
    doc = pymupdf.open(path)
    heads = bad = 0
    for pno, page in enumerate(doc, start=1):
        ls = lines(page)
        for i, (y0, y1, size, txt) in enumerate(ls):
            if size < HEAD_PT:
                continue
            heads += 1
            above = [l for l in ls[:i] if l[1] <= y0 + 1]
            if above:
                bad += 1
                print(f"  page {pno:2}  section {txt[:38]!r} opens at y={y0:.0f} "
                      f"with {len(above)} line(s) above it, from "
                      f"{above[-1][3][:34]!r}")
    if not heads:
        print("\nNO SECTION HEADS FOUND. The type-size test has lost its "
              "subject; this file cannot report on a rule it cannot see.")
        return 1
    print(f"\n{bad} section(s) do not open a page, of {heads}" if bad else
          f"\nevery section opens a page, {heads} of {heads}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
