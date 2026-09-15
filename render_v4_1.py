import pathlib
from playwright.sync_api import sync_playwright

HTML = pathlib.Path("paper_national_v4_1.html").resolve()
OUT = pathlib.Path("Medicaid_Dollars_National_DRAFT_v4.1.pdf").resolve()

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
_f = subprocess.call(["python3","figurefit.py",str(OUT),"paper_national_v4_1.html"])
_s.exit(_w or _f)
