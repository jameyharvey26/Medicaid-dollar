import pathlib, tempfile
from playwright.sync_api import sync_playwright
import release

# D-79. The manuscript carries placeholders; the values are derived here and
# substituted into a temporary copy, so no provenance string is ever typed
# into the source. PAPER_URL and REPO are deliberately non-functional
# placeholders: the landing page is not stood up and the repository path is
# not final. Both are open items and must be real before this ships.
SRC = pathlib.Path("paper_national_v6_0.html").resolve()
OUT = pathlib.Path(f"Medicaid_Dollars_National_v{release.VERSION}.pdf").resolve()

_FILL = {
    "{{STAMP}}":        release.stamp(),
    "{{RELEASE_DATE}}": release.build_date(),
    "{{BUILD_ID}}":     release.build_id(),
    "{{PAPER_URL}}":    "[landing page pending]",
    "{{REPO}}":         "[repository pending]",
}
_txt = SRC.read_text()
for k, v in _FILL.items():
    _txt = _txt.replace(k, v)
if "{{" in _txt:
    raise SystemExit("unsubstituted placeholder left in the manuscript")
HTML = pathlib.Path(tempfile.mkdtemp()) / "paper.html"
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

print("wrote", OUT, OUT.stat().st_size, "bytes")

import subprocess, sys as _s
_w = subprocess.call(["python3","whitespace.py",str(OUT)])
_f = subprocess.call(["python3","figurefit.py",str(OUT),str(SRC)])
_s.exit(_w or _f)
