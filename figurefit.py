"""
figurefit.py — does the figure on a page actually show what the page talks about?

    python3 figurefit.py Medicaid_Dollars_National_DRAFT_v3.pdf paper_national_v3.html

A reader expects the picture to correspond to the topic. When a page discusses a
provision that is not inside the crop shown on that page, the figure is the wrong
view and the reader has to go hunting. That is checkable: the panel SVGs carry the
coordinates of every label, make_figs.py records the box each crop cuts, and the
PDF says which figure landed on which page.

Reports, per page, any subject named in the prose whose label sits outside every
figure on that page.
"""
import json
import os
import re
import sys

import pymupdf

FIGDIR = "paper_figs"
SVG = {"2024": "reference_renders/national_2024_combined.svg",
       "2030": "reference_renders/national_2030_mixed_combined.svg"}

# The subjects a reader would expect to see when the prose names them. Each is a
# phrase that appears in the prose and the label text it corresponds to on a panel.
SUBJECTS = [
    ("Work reporting",                 "Work reporting"),
    ("Blocked senior enrollment",      "Blocked senior enrollment"),
    ("Provider tax limits",            "Provider tax limits"),
    ("Everything else",                "Other"),
    ("Blocked Medicaid enrollment",    "Blocked Medicaid enrollment"),
    ("Directed payment caps",          "Directed payment caps"),
    ("Six-month renewals",             "Six-month renewals"),
    ("Public-company earnings",        "Public-company earnings"),
    ("Plan administration",            "plan administration"),
    ("Medicare premiums",              "Medicare premiums"),
    ("Documented fraud",               "Documented fraud"),
    ("Fee-for-service",                "Fee-for-service"),
]


def label_positions(panel):
    """Every text label on a panel, as (text, x, y) in viewBox units."""
    out = []
    src = open(SVG[panel]).read()
    for m in re.finditer(r'<text[^>]*x="([\d.\-]+)"[^>]*y="([\d.\-]+)"[^>]*>(.*?)</text>',
                         src, re.S):
        txt = re.sub(r"<[^>]+>", " ", m.group(3))
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt:
            out.append((txt, float(m.group(1)), float(m.group(2))))
    return out


def figure_sources(html):
    """Caption number -> (filename, opening words of its caption).

    The opening words matter: a caption that says "Detail from Figure 5" would
    otherwise count the whole panel as present on the page, and the whole panel
    contains everything, so every check would pass. Only a figure whose caption
    begins on the page is actually on the page.
    """
    src = open(html).read()
    out = {}
    for m in re.finditer(r'<img src="paper_figs/([^"]+)"[^>]*>\s*<figcaption>\s*'
                         r'<b>Figure (\d+)\.(.{0,60})', src, re.S):
        head = re.sub(r"<[^>]+>", " ", m.group(3))
        head = re.sub(r"\s+", " ", head).strip()
        out[int(m.group(2))] = (m.group(1), head)
    return out


def main(pdf, html):
    crops = json.load(open(os.path.join(FIGDIR, "crops.json")))
    figs = figure_sources(html)
    labels = {p: label_positions(p) for p in SVG}
    doc = pymupdf.open(pdf)
    problems = []

    for pno, page in enumerate(doc, start=1):
        text = page.get_text()
        flat = re.sub(r"\s+", " ", text)
        boxes = []
        for n, (fn, head) in figs.items():
            probe = "Figure %d. %s" % (n, " ".join(head.split()[:4]))
            if probe in flat and fn in crops:
                boxes.append((n, crops[fn]))
        # Only what the page treats AS ITS SUBJECT counts: a heading or a bold
        # lead-in. A provision named in passing inside a paragraph is a
        # cross-reference, and a reader does not expect a picture for it.
        prominent = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    bold = bool(span["flags"] & 16) or "Bold" in span["font"]
                    if span["size"] >= 10.5 or bold:
                        prominent.append(span["text"])
        # spans arrive fragmented by kerning ("E|v|er|y|thing else"), so join
        # without a separator before matching, then normalise the spacing
        subject_text = re.sub(r"\s+", " ", "".join(prominent)).lower()
        for phrase, label in SUBJECTS:
            if phrase.lower() not in subject_text:
                continue
            seen = False
            for panel in SVG:
                for txt, x, y in labels[panel]:
                    if label.lower() not in txt.lower():
                        continue
                    for n, c in boxes:
                        if c["panel"] != panel:
                            continue
                        x0, y0, x1, y1 = c["box"]
                        if x0 <= x <= x1 and y0 <= y <= y1:
                            seen = True
            if not seen:
                problems.append((pno, phrase, [n for n, _ in boxes]))

    if not problems:
        print("every subject named in prose appears in a figure on its own page")
        return 0
    print("%d page/subject mismatch(es):" % len(problems))
    last = None
    for pno, phrase, figs_on in problems:
        if pno != last:
            shown = ", ".join(map(str, figs_on)) if figs_on else "no figure"
            print("  page %-3d shows %s" % (pno, shown if figs_on == [] else "Figure " + shown))
            last = pno
        print("      discusses %-30s %s" % (phrase, "and shows no diagram" if not figs_on else "not visible in that crop"))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "Medicaid_Dollars_National_DRAFT_v3.pdf",
                  sys.argv[2] if len(sys.argv) > 2 else "paper_national_v3.html"))
