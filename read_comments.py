"""
Read JW's PDF comments and report each one against the text it sits on.

    python3 read_comments.py <commented.pdf>

Highlights, underlines and strikeouts resolve to the exact marked text.
Sticky notes resolve to the nearest text block in the same column, because
the page is two-column and a full-width band would straddle both.
"""
import sys
import pymupdf

MARKUP = {8, 9, 10, 11}          # highlight, underline, squiggly, strikeout


def nearest_block(page, rect):
    blocks = [b for b in page.get_text("blocks") if b[6] == 0 and b[4].strip()]
    if not blocks:
        return ""
    cx = (rect.x0 + rect.x1) / 2
    same_col = [b for b in blocks if b[0] - 12 <= cx <= b[2] + 12]
    pool = same_col or blocks

    def gap(b):
        dx = max(b[0] - rect.x1, rect.x0 - b[2], 0)
        dy = max(b[1] - rect.y1, rect.y0 - b[3], 0)
        return (dy, dx)

    return min(pool, key=gap)[4].replace("\n", " ").strip()


def main(path):
    doc = pymupdf.open(path)
    n = 0
    for pno, page in enumerate(doc, start=1):
        for an in page.annots() or []:
            body = (an.info.get("content") or "").strip()
            if not body:
                continue
            n += 1
            r = an.rect
            if an.type[0] in MARKUP:
                anchor, how = page.get_textbox(r).replace("\n", " ").strip(), "marked text"
            else:
                anchor, how = nearest_block(page, r), "nearest block"
            print("=" * 74)
            print("#%-3d page %-3d %-11s by %s"
                  % (n, pno, an.type[1], an.info.get("title") or "?"))
            print("  COMMENT : %s" % body)
            print("  ON (%s): %s" % (how, anchor[:300] or "<nothing>"))
    print("=" * 74)
    print("%d comment(s) read from %s" % (n, path))
    if n == 0:
        print("No annotations found. If the file was flattened or printed to PDF, "
              "the comments were baked into the page and are gone.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Medicaid_Dollars_National_DRAFT.pdf")
