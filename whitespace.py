"""
whitespace.py — measure dead space on every page of a rendered PDF.

The eye is not a detector. crossings.py gates geometry; this gates layout.

    python3 whitespace.py Medicaid_Dollars_National_DRAFT_v3.pdf

Reports, per page, the tallest run of empty space at the foot of each column and
of the page. Fails on anything over the threshold, which is expressed in text
lines rather than millimetres because that is the unit a reader perceives.
"""
import sys
import pymupdf

LINE_MM = 5.15          # 9.7pt body at 1.5 line-height
MARGIN_MM = 14.0        # @page top margin
FOOT_MM = 13.0          # @page bottom margin
MAX_DEAD_LINES = 6      # a column may end this many lines short, no more
MAX_SIDE_MM = 25         # horizontal slack beside a page-spanning figure
MAX_TERMINAL_LINES = 20  # a page that ends a section may run shorter, but not by much
EXEMPT = {"cover", "last", "plate"}   # pages whose white space is by design
PT_PER_MM = 72 / 25.4


def columns(page):
    """Left and right column x-bounds for the two-column landscape grid."""
    w = page.rect.width
    mid = w / 2
    return [(0, mid), (mid, w)]


def dead_space(page, dpi=72):
    """Millimetres of empty space below the lowest inked pixel in each column.

    Measured on the raster rather than on PDF objects, because the renderer
    emits a full-page white rectangle that an object scan counts as content.
    """
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
    W, H = pix.width, pix.height
    buf = pix.samples
    top = int(MARGIN_MM * dpi / 25.4)
    bot = H - int(FOOT_MM * dpi / 25.4)
    out = []
    for x0f, x1f in ((0.0, 0.5), (0.5, 1.0)):
        x0, x1 = int(W * x0f), int(W * x1f)
        last = top
        for y in range(top, bot):
            row = buf[y * W + x0: y * W + x1]
            if min(row) < 245:          # anything not near-white is ink
                last = y
        out.append(max(0.0, (bot - last) * 25.4 / dpi))
    return out


def side_gaps(page, dpi=72):
    """Worst horizontal dead space beside a figure whose frame spans the text
    width while its artwork does not.

    Measured off the caption rule rather than off the image, because the image
    is the narrow part. Checking the image width asks the wrong object: a
    portrait crop centred in a full-width frame is narrow by definition, so an
    image-width test declares it a column figure and says nothing.
    """
    text_w = page.rect.width - 2 * MARGIN_MM * PT_PER_MM
    rules = [d["rect"] for d in page.get_drawings()
             if d["rect"].height < 3 and d["rect"].width > text_w * 0.9]
    worst = 0.0
    for rule in rules:
        widest = 0.0
        for im in page.get_images(full=True):
            for r in page.get_image_rects(im[0]):
                if r.y1 <= rule.y0 and rule.y0 - r.y1 < 8:   # art sits on the rule
                    widest = max(widest, r.width)
        if widest:
            worst = max(worst, (rule.width - widest) / PT_PER_MM)
    return worst


def is_plate(page):
    """A full-page figure page: one big image and almost no body text."""
    imgs = page.get_images(full=True)
    if not imgs:
        return False
    tall = any(r.height > page.rect.height * 0.45
               for im in imgs for r in page.get_image_rects(im[0]))
    words = len(page.get_text().split())
    return tall and words < 120


def starts_section(page):
    """Does this page open a new section? Then the page before it ends one, and
    some slack there is honest rather than padding the prose.

    Detected by type size rather than by a label, because the labels were
    editorial scaffolding and could be removed. A detector tied to wording
    breaks the moment the wording changes.
    """
    if is_plate(page):
        return True
    d = page.get_text("dict")
    for block in d["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                if span["text"].strip():
                    return span["size"] >= 18
    return False


def main(path):
    doc = pymupdf.open(path)
    n_pages = len(doc)
    bad = []
    print("%-5s %10s %10s %8s  %-7s %s"
          % ("page", "left", "right", "side", "kind", "verdict"))
    for n, page in enumerate(doc, start=1):
        left, right = (v / LINE_MM for v in dead_space(page))
        if n == 1:
            kind = "cover"
        elif n == n_pages:
            kind = "last"
        elif is_plate(page):
            kind = "plate"
        elif n < n_pages and starts_section(doc[n]):
            kind = "sec-end"
        else:
            kind = "body"
        worst = max(left, right)
        limit = MAX_TERMINAL_LINES if kind == "sec-end" else MAX_DEAD_LINES
        side = side_gaps(page)
        flag = (kind not in EXEMPT and worst > limit) or side > MAX_SIDE_MM
        if flag:
            bad.append((n, left, right, side))
        print("%-5d %7.1f ln %7.1f ln %6.0f mm  %-7s %s"
              % (n, left, right, side, kind, "DEAD" if flag else "ok"))
    print()
    if bad:
        print("%d body page(s) over the %d-line threshold:" % (len(bad), MAX_DEAD_LINES))
        for n, l, r, side in bad:
            if side > MAX_SIDE_MM:
                print("  page %-3d %.0f mm dead beside a full-width figure "
                      "(portrait art spanned the page)" % (n, side))
            else:
                which = "both columns" if min(l, r) > MAX_DEAD_LINES else (
                    "left column" if l > r else "right column")
                print("  page %-3d %.0f lines dead, %s" % (n, max(l, r), which))
        return 1
    print("no body page strands more than %d lines in a column" % MAX_DEAD_LINES)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else "Medicaid_Dollars_National_DRAFT_v3.pdf"))
