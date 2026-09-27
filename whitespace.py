"""
whitespace.py — measure dead space on every page of a rendered PDF.

The eye is not a detector. crossings.py gates geometry; this gates layout.

    python3 whitespace.py Medicaid_Dollars_National_DRAFT_v3.pdf

Reports, per page, the tallest run of empty space at the foot of each column and
of the page. Fails on anything over the threshold, which is expressed in text
lines rather than millimetres because that is the unit a reader perceives.
"""
import sys
import re
import pymupdf

LINE_MM = 5.15          # 9.7pt body at 1.5 line-height
MARGIN_MM = 14.0        # @page top margin, used only for the side-gap test
FOOTER_MARKS = ("build ", "pending]")   # the stamped provenance line
# The centre field is a page number and carries none of those marks. It sits
# on the same baseline, so it became the lowest ink on every page and the
# blindness check fired - correctly, and on something this file would once
# have measured to without noticing.
PAGENO = re.compile(r"^Page \d+ of \d+$")
QUORUM = 3              # pages that must agree before a y counts as the text bottom
MAX_DEAD_LINES = 6      # a column may end this many lines short, no more
MAX_SIDE_MM = 25         # horizontal slack beside a page-spanning figure
MAX_TERMINAL_LINES = 20  # a page that ends a section may run shorter, but not by much
EXEMPT = {"cover", "last", "plate", "short-sec"}  # white space by design
PT_PER_MM = 72 / 25.4


def columns(page):
    """Left and right column x-bounds for the two-column landscape grid."""
    w = page.rect.width
    mid = w / 2
    return [(0, mid), (mid, w)]


def content_spans(page):
    """Every inked thing on the page that is part of the flow, as (x0, y0, x1, y1).

    Text lines, figures, and rules. NOT the provenance line, which is stamped
    into the margin and is not content; and not the page's own white backing
    rectangle, which an object scan would otherwise count as ink covering
    everything. The footer is excluded by its own text, in the bottom band, on
    the same test footerfit.py uses - never by position alone.
    """
    floor = page.rect.height * 0.85
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            txt = "".join(sp["text"] for sp in line["spans"]).strip()
            if not txt:
                continue
            if line["bbox"][1] > floor and (
                    any(m in txt for m in FOOTER_MARKS) or PAGENO.match(txt)):
                continue
            out.append(tuple(line["bbox"]))
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            out.append((r.x0, r.y0, r.x1, r.y1))
    page_area = page.rect.width * page.rect.height
    for d in page.get_drawings():
        r = d["rect"]
        if r.width < 0.5 and r.height < 0.5:
            continue
        # Furniture, not content. Two kinds, and both used to make every page
        # of this document read as full:
        #
        # The backing panel. The renderer paints a large unstroked fill behind
        # the text area. It is drawn to the page box, so its lower edge is the
        # bottom of the text area on every page whether or not any text got
        # that far - which is why this file reported 0.0 lines dead everywhere.
        #
        # The column rule. `column-rule` is a hairline drawn to the full height
        # of the column box, not to the last line in it. Same failure, and it
        # straddles the centre, so it poisoned both columns at once.
        if d.get("fill") is not None and d.get("stroke") is None \
                and r.width * r.height > page_area * 0.25:
            continue
        if r.width < 2.0 and r.height > 40.0:
            continue
        out.append((r.x0, r.y0, r.x1, r.y1))
    return out


def flow_bottom(doc):
    """The y the flowing text actually stops at, read off the document.

    This used to be a typed constant, FOOT_MM, holding a copy of the @page
    bottom margin. Two declarations of one geometry: the margin moved from
    13mm to 18mm under D-93 and this file went on measuring against 13, which
    put a line of phantom slack on every page. It is measured now.

    Measured by quorum, not by the maximum. A single element that overruns the
    text area - a plate figure printing into the margin - would otherwise
    define the text area as wherever it happens to reach, and every other page
    on the document would then read as short by that overrun. The bottom is
    the deepest y that several pages independently reach, because in a document
    this long several pages run full. `overruns` reports the rest, which is a
    finding rather than a nuisance.
    """
    deep = sorted((max((sp[3] for sp in content_spans(pg)), default=0.0)
                   for pg in doc), reverse=True)
    for cand in deep:
        if sum(1 for v in deep if v > cand - 2.0) >= QUORUM:
            return cand
    return deep[0] if deep else 0.0


def overruns(doc, bottom, slack=None):
    """Pages carrying something below the text area. Usually a figure.

    The slack is a whole line, not a hair. `bottom` is where pages of BODY type
    stop, and the notes are set at 7.9pt on tighter leading, so their last line
    legitimately sits a few points lower without having left the text area. A
    two-point tolerance called that an overrun. What this is for is a figure
    printing into the margin, which is measured in centimetres.
    """
    if slack is None:
        slack = LINE_MM * PT_PER_MM
    out = []
    for n, pg in enumerate(doc, start=1):
        d = max((sp[3] for sp in content_spans(pg)), default=0.0)
        if d > bottom + slack:
            out.append((n, (d - bottom) / PT_PER_MM))
    return out


HEAD_PT = 18.0          # h2.sec is 21pt; nothing else in the paper is near it


def _has_section_head(page):
    """Does this page open a section? Type size, not wording (sectionfit.py)."""
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                if span["text"].strip() and span["size"] >= HEAD_PT:
                    return True
    return False


def _spans(page):
    """Does this page carry something wider than one column?"""
    w = page.rect.width
    return any(sp[2] - sp[0] > w * 0.6 for sp in content_spans(page))


def dead_space(page, bottom):
    """Millimetres of empty space below the last content in each column.

    Per column, by the x-midpoint of each span: a span that straddles the
    centre (a page-spanning figure, a section head, a table) belongs to both,
    because it fills both columns at that height. The old version sliced the
    raster at exactly W/2 and the column rule, which is drawn on that line,
    could be counted in either half or neither depending on rounding.
    """
    mid = page.rect.width / 2
    deepest = [None, None]
    for x0, y0, x1, y1 in content_spans(page):
        cols = ([0, 1] if x0 < mid - 2 and x1 > mid + 2
                else [0] if (x0 + x1) / 2 < mid else [1])
        for c in cols:
            if deepest[c] is None or y1 > deepest[c]:
                deepest[c] = y1
    return [max(0.0, (bottom - (d if d is not None else 0.0)) / PT_PER_MM)
            for d in deepest]


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
    bottom = flow_bottom(doc)
    if bottom <= 0:
        print("no content found; nothing to measure")
        return 1
    over = overruns(doc, bottom)
    print("text area ends at y=%.1f, measured off the document" % bottom)
    for n, mm in over:
        print("  page %-3d runs %.1f mm PAST the text area" % (n, mm))
    print()
    bad, _ALL, hints = [], [], []
    print("%-5s %10s %10s %8s  %-7s %s"
          % ("page", "left", "right", "side", "kind", "verdict"))
    for n, page in enumerate(doc, start=1):
        left, right = (v / LINE_MM for v in dead_space(page, bottom))
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
        if kind not in EXEMPT:
            _ALL.append(worst)
        # D-99. A page that CARRIES a section head and also ends short is a
        # short section, not a broken one: the rule that a section opens a page
        # (D-96) creates them, and "What comes next" is two paragraphs long by
        # design. It gets the whole page. A page that ends short WITHOUT a head
        # on it is a section that ran out halfway down a page of its own, which
        # is the fault this file is looking for.
        if kind in ("sec-end", "body") and _has_section_head(page):
            kind = "short-sec"
        limit = MAX_TERMINAL_LINES if kind == "sec-end" else MAX_DEAD_LINES
        side = side_gaps(page)
        flag = (kind not in EXEMPT and worst > limit) or side > MAX_SIDE_MM
        if flag:
            bad.append((n, left, right, side))
        print("%-5d %7.1f ln %7.1f ln %6.0f mm  %-7s %s"
              % (n, left, right, side, kind, "DEAD" if flag else "ok"))
    print()

    # The blindness check. This file reported about one line of dead space on
    # every page of every draft for weeks, because the footer was the lowest
    # ink on the page and it was measuring to that. A real document has section
    # ends and full pages in it, so the spread across pages is never near zero.
    # If it is, the measurement has attached itself to furniture again and the
    # honest answer is that this file does not know, not that the layout is
    # clean.
    spread = max(_ALL) - min(_ALL) if _ALL else 0.0
    if spread < 3.0:
        print("MEASUREMENT NOT TRUSTED: every page reads within %.1f lines of "
              "every other.\n  A paginated document has section ends in it. "
              "This is the signature of\n  measuring to a repeated element "
              "rather than to the text." % spread)
        return 1

    if over:
        print("%d page(s) print below the text area:" % len(over))
        for n, mm in over:
            print("  page %-3d overruns by %.1f mm" % (n, mm))
        print()
    if bad or over:
        print("%d page(s) over threshold (body %d lines, section end %d):"
              % (len(bad), MAX_DEAD_LINES, MAX_TERMINAL_LINES))
        for n, l, r, side in bad:
            if side > MAX_SIDE_MM:
                print("  page %-3d %.0f mm dead beside a full-width figure "
                      "(portrait art spanned the page)" % (n, side))
            else:
                which = "both columns" if min(l, r) > MAX_DEAD_LINES else (
                    "left column" if l > r else "right column")
                print("  page %-3d %.0f lines dead, %s" % (n, max(l, r), which))
        return 1
    print("no body page strands more than %d lines in a column, "
          "and nothing prints below the text area" % MAX_DEAD_LINES)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else "Medicaid_Dollars_National_DRAFT_v3.pdf"))
