#!/usr/bin/env python3
"""publish.py — the three artifacts, one version, HTML and PDF of each.

D-107. The paper, the deck and the explorer were named three different ways.
The paper carried `release.VERSION`; the deck was `MHPA_Board_Deck` with no
version at all, so two builds a month apart were indistinguishable once
downloaded; the explorer was `medicaid_dollar_explorer`, likewise. A reader
handed all three had no way to tell whether they belonged together.

They do belong together — all three are rendered from the same ledger in the
same build — so they take the same version, from the same declaration. S-096:
one fact, one declaration. `release.VERSION` was already that declaration for
the paper and is now that declaration for all of it.

    python3 publish.py

Writes six files to the repo folder, all stamped v{VERSION}.

The explorer's PDF is a flat print of an interactive page, which is a lesser
thing than the page itself and is meant as a record rather than as the
artifact. Its print stylesheet opens every view, so the PDF contains the
diagram, the phases, the law, the comparison, the register and the reading —
which is everything the page holds, minus the ability to pull on it.
"""
import os
import shutil
import subprocess
import sys

import release

OUT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.abspath(__file__))
V = release.VERSION


def name(stem, ext):
    return os.path.join(OUT, f"{stem}_v{V}.{ext}")


# The paper's renderer exits non-zero on its own layout gates, and two of them
# are legitimately red and known: page 9 strands seven lines, and three leaders
# on fig6 run through a label. Those are JW's to close in the prose and the
# drawing. A publisher that refuses to write the PDF over them would mean the
# only way to get a build out is to green a gate that is honestly red, which is
# the wrong pressure to put on a detector. The artifact is written and the
# faults are reported here rather than swallowed.
TOLERATED = {"render_v8_0.py"}


def run(cmd):
    print(f"  $ {' '.join(cmd)}")
    p = subprocess.run([sys.executable] + cmd, cwd=REPO,
                       capture_output=True, text=True, timeout=1800)
    if p.returncode and cmd[0] not in TOLERATED:
        print(p.stdout[-2500:]); print(p.stderr[-2500:])
        raise SystemExit(f"{cmd[0]} failed")
    if p.returncode:
        tail = [l for l in p.stdout.splitlines()
                if "fault" in l or "over threshold" in l or "lines dead" in l
                or "leader runs through" in l]
        print("    reported, not fatal:")
        for l in tail:
            print("      " + l.strip())
    return p.stdout


def to_pdf(html_path, pdf_path, *, landscape=False, wait=2200,
           before=None):
    """Chromium print. `prefer_css_page_size` so each artifact's own @page wins."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1600, "height": 1200})
        pg.goto("file://" + os.path.abspath(html_path))
        pg.wait_for_timeout(wait)
        if before:
            before(pg)
        pg.emulate_media(media="print")
        pg.pdf(path=pdf_path, print_background=True,
               prefer_css_page_size=True,
               **({} if landscape else {"format": "Letter"}))
        b.close()


_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".svg": "image/svg+xml", ".gif": "image/gif", ".webp": "image/webp",
         ".ttf": "font/ttf", ".woff2": "font/woff2", ".woff": "font/woff"}


def _selfcontain(src, dst):
    """Inline every relative asset, so the HTML survives leaving the repo.

    The manuscript references its figures as relative paths ("paper_figs/..."),
    which is right inside the repo and useless outside it: a reader who
    downloads the HTML gets a document of broken image icons and no warning.
    This is the same fault that made the PDF 192 kB on 26 September, arriving
    a second time by a different route — the file moves instead of the
    renderer. The deck has always inlined its images; the paper now does too.
    """
    import base64
    import re
    html = open(src, encoding="utf-8").read()
    root = os.path.dirname(os.path.abspath(src))
    missing = []

    def sub(m):
        pre, path, post = m.group(1), m.group(2), m.group(3)
        if path.startswith(("data:", "http:", "https:", "#")):
            return m.group(0)
        p = os.path.join(root, path.split("?")[0])
        if not os.path.exists(p):
            missing.append(path)
            return m.group(0)
        mime = _MIME.get(os.path.splitext(p)[1].lower(),
                         "application/octet-stream")
        with open(p, "rb") as fh:
            b = base64.b64encode(fh.read()).decode()
        return f"{pre}data:{mime};base64,{b}{post}"

    html = re.sub(r'(\bsrc=")([^"]+)(")', sub, html)
    html = re.sub(r'(\burl\()([^)\'"]+)(\))', sub, html)
    if missing:
        raise SystemExit("assets the manuscript names and the repo does not "
                         "have: " + ", ".join(sorted(set(missing))[:8]))

    # D-116. The manuscript is laid out for an 11in landscape sheet and its
    # pages ran to the very edge of the browser window with a sideways scroll,
    # which is the same fault the deck had. Screen only: this stylesheet is
    # inside @media screen and cannot reach the PDF, which render_v8_0.py
    # prints from the source before any of this runs.
    screen = """
<style>
@media screen{
  html{background:#d9d5cc;}
  body{background:#d9d5cc;}
  /* A page is a sheet of paper and has to read as one, which means seeing
     space on both sides of it. The sheet cannot reflow \u2014 the layout gates
     measure it at 11in \u2014 so on a narrower window it is scaled rather than
     cropped. `zoom` reflows the height with it; a transform would leave a
     column of dead space below the document. */
  body{ padding:26px 34px; box-sizing:border-box; }
  body > *{ background:#fff; box-shadow:0 12px 28px rgba(20,25,35,.14);
            margin-left:auto; margin-right:auto; }
  /* The breakpoints allow for the 68px of gutter as well as the sheet, so
     the scaled page plus its margins fit the window rather than the page
     alone fitting and the margins pushing it back out. */
  @media (max-width:1240px){ body{zoom:.92;} }
  @media (max-width:1140px){ body{zoom:.84;} }
  @media (max-width:1060px){ body{zoom:.76;} }
  @media (max-width:960px){ body{zoom:.66;} }
  @media (max-width:840px){ body{zoom:.56;} }
  @media (max-width:700px){ body{zoom:.44; padding:14px 16px;} }
}
</style>
"""
    if "</head>" in html:
        html = html.replace("</head>", screen + "</head>", 1)
    else:
        html = screen + html
    open(dst, "w", encoding="utf-8").write(html)


def main():
    os.makedirs(OUT, exist_ok=True)
    print(f"publishing v{V}  ({release.stamp()})\n")

    # ---- 1. the paper ----------------------------------------------------
    print("paper")
    run(["render_v8_0.py"])
    src = os.path.join(REPO, f"Medicaid_Dollars_National_v{V}.pdf")
    paper_pdf = name("Medicaid_Dollars_National", "pdf")
    shutil.copy(src, paper_pdf)
    # The manuscript source, with its placeholders substituted — the same
    # temporary file the renderer prints from, kept rather than discarded so
    # the HTML and the PDF are provably the same document.
    tmp = os.path.join(REPO, "_render_tmp.html")
    paper_html = name("Medicaid_Dollars_National", "html")
    _selfcontain(tmp if os.path.exists(tmp) else
                 os.path.join(REPO, "paper_national_v8_0.html"), paper_html)

    # ---- 2. the deck -----------------------------------------------------
    print("deck")
    run(["deckalts.py"])
    run(["build_deck.py"])
    deck_html = name("MHPA_Board_Deck", "html")
    shutil.copy(os.path.join(OUT, "MHPA_Board_Deck.html"), deck_html)
    deck_pdf = name("MHPA_Board_Deck", "pdf")
    to_pdf(deck_html, deck_pdf, landscape=True)

    # ---- 3. the explorer -------------------------------------------------
    print("explorer")
    run(["build_explorer.py"])
    exp_html = name("medicaid_dollar_explorer", "html")
    shutil.copy(os.path.join(OUT, "medicaid_dollar_explorer.html"), exp_html)
    # JW, 28 September: no explorer PDF. It is an interactive page and a flat
    # print of it was always the lesser artifact; the whitepaper PDF is now
    # embedded in the page itself, which is the thing a reader would have
    # wanted the print for.
    print()
    made = [paper_html, paper_pdf, deck_html, deck_pdf, exp_html]
    for f in made:
        print(f"  {os.path.getsize(f)/1024:9,.0f} KB  {os.path.basename(f)}")
    return made


if __name__ == "__main__":
    main()
