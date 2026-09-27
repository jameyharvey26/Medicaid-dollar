import pathlib, sys, tempfile
from playwright.sync_api import sync_playwright
import release
import landing

# D-84. The manuscript carries placeholders; the values are derived here and
# substituted into a temporary copy, so no provenance string is ever typed
# into the source. PAPER_URL now comes from landing.py, which is the single
# declaration the deck reads too (D-103). REPO is deliberately empty: the
# repository path lives on the landing page instead, so there is one address
# to fix rather than two.
# The manuscript, overridable so a retained whole-number release can still be
# rendered after its own renderer is deleted:  python3 render_v7_1.py paper_national_v6_1.html
SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                   else "paper_national_v7_1.html").resolve()
OUT = pathlib.Path(f"Medicaid_Dollars_National_v{release.VERSION}.pdf").resolve()

_FILL = {
    "{{STAMP}}":        release.stamp(),
    "{{RELEASE_DATE}}": release.build_date(),
    "{{BUILD_ID}}":     release.build_id(),
    "{{PAPER_URL}}":    landing.FOOTER,
    # D-98, JW: the repository path comes off the footer. It will live on the
    # landing page instead, so there is one address to fix rather than two.
    "{{REPO}}":         "",
}
_txt = SRC.read_text()
for k, v in _FILL.items():
    _txt = _txt.replace(k, v)
if "{{" in _txt:
    raise SystemExit("unsubstituted placeholder left in the manuscript")
# Beside the manuscript, NOT in a temp directory. Every figure in the paper is
# referenced as a relative path ("paper_figs/..."), so an HTML file written
# anywhere else resolves none of them and Chromium prints a document of broken
# image icons without complaining. Found 2026-09-26: the PDF was 192 kB with
# eighteen figures in it, which is the size of a paper with no pictures.
HTML = SRC.parent / "_render_tmp.html"
HTML.write_text(_txt)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(HTML.as_uri())
    pg.wait_for_timeout(1800)          # let the embedded fonts land
    pg.emulate_media(media="print")
    pg.pdf(path=str(OUT), format="Letter", print_background=True,
           prefer_css_page_size=True)
    b.close()

# D-93. Stamp the provenance line into the paper margin. The browser cannot
# put it there: a fixed element in a paged context is positioned against the
# page area, so every offset that clears the text also leaves the page. Drawn
# here, the band is genuinely reserved - @page's 18mm bottom margin ends the
# text, and this line sits at 9mm, below it, on every page but the cover's
# facing furniture. The three fields are the same _FILL values the manuscript
# would have carried, so there is still one source for them.
# D-99. The table's "would have reached" column is checked against the ledger
# rather than trusted. It disagreed with every diagram on one row for three
# drafts, and nothing in the repo was looking.
import cover_data as _CD
_html = SRC.read_text()
_dis = []
for _lv in _CD.load(federal=True)["levers"]:
    _row = _html.split(f'>{_lv["label"]}</td>')
    if len(_row) < 2:
        continue
    _reach = _row[1].split("<td")[3].split(">", 1)[1].split("<")[0].strip()
    # The two vocabularies are not word-for-word - the table says "Federal
    # band" where the ledger says "Federal and state shares" - so the test is
    # on the phase, not the wording.
    # Against `reach`, not `phase`. The first version of this test compared
    # the table's "would have reached" against where the provision BITES, and
    # reported a disagreement on the one provision where those two genuinely
    # differ. D-101 declares them separately.
    if _reach.split()[0].lower() != _lv["reach"].split()[0].lower():
        _dis.append((_lv["label"], _reach, _lv["phase"]))
if _dis:
    print("TABLE 2 DISAGREES WITH THE LEDGER on where a dollar would have "
          "reached:")
    for _a, _b, _c in _dis:
        print(f'  {_a}: the table says "{_b}", the ledger says "{_c}"')
    print("  The prose follows the diagram by default (S-108). One of the two "
          "is wrong and it is not for this script to pick.")
else:
    print("table 2 agrees with the ledger on every provision's reach")

import pymupdf
MM = 72 / 25.4
_doc = pymupdf.open(OUT)
_left, _right, _up = 15 * MM, 15 * MM, 9 * MM
for _pg in _doc:
    _w, _h = _pg.rect.width, _pg.rect.height
    _y = _h - _up
    _n = _pg.number + 1
    for _txt, _x, _al in ((_FILL["{{STAMP}}"], _left, 0),
                          (f"Page {_n} of {_doc.page_count}", _w / 2, 1),
                          (_FILL["{{PAPER_URL}}"], _w - _right, 2)):
        _len = pymupdf.get_text_length(_txt, fontname="helv", fontsize=6.5)
        _x0 = _x if _al == 0 else (_x - _len / 2 if _al == 1 else _x - _len)
        _pg.insert_text((_x0, _y), _txt, fontname="helv", fontsize=6.5,
                        color=(0.436, 0.436, 0.436))
_doc.saveIncr()
_doc.close()

print("wrote", OUT, OUT.stat().st_size, "bytes")

import subprocess, sys as _s
_w = subprocess.call(["python3","whitespace.py",str(OUT)])
_f = subprocess.call(["python3","figurefit.py",str(OUT),str(SRC)])
_c = subprocess.call(["python3","footerfit.py",str(OUT)])
_x = subprocess.call(["python3","sectionfit.py",str(OUT)])
_a = subprocess.call(["python3","artwhite.py"])
_t = subprocess.call(["python3","tapertest.py"])
_s.exit(_w or _f or _c or _x or _a or _t)
