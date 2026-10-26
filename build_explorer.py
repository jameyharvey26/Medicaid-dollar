#!/usr/bin/env python3
"""build_explorer.py — the public explorer, built from the ledger.

D-105. Writes ONE self-contained HTML file. Every number in it is serialized
by `explorer.py` at build time from the same ledgers the paper and the deck
read; `explorer_template.html` contains no numerals, and `explorerproof.py`
fails the build if one appears. That is S-105 applied to the web artifact, and
it is the whole point of the rewrite: the predecessor held its own copy of the
numbers and went on serving a superseded hundred for two decision cycles with
no way for anything in the repo to notice.

WHAT SHIPS
    medicaid_dollar_explorer.html   one file, fonts and images inlined,
                                    emailable, no network at runtime
    explorer_data.json              the same payload, separately, so a
                                    reviewer can diff the data without
                                    diffing a megabyte of base64

Panels: national FY2024, national FY2030 in all three variants, and DC FY2024
marked draft. DC FY2030 is out of scope — there is no DC 2030 ledger.
"""
import base64
import json
import os
import re
import sys

import explorer as X
import views
from landing import URL
import release

REPO = os.path.dirname(os.path.abspath(__file__))
OUT = "/mnt/user-data/outputs"
TEMPLATE = os.path.join(REPO, "explorer_template.html")

# JW, 27 September: banner, every figure and tooltip, and stamped on any
# export or print. Declared once; the panel carries it and the page obeys.
DC_DRAFT = "DRAFT \u2014 UNPUBLISHED"

VARIANTS = {
    "mixed": ("Mixed", "Administration holds; plan retention scales with "
                       "capitation. The paper's default."),
    "holds": ("Overhead holds", "Administration and plan retention both hold "
                                "at their FY2024 dollars as the program shrinks."),
    "scales": ("Overhead scales", "Administration and plan retention both "
                                  "scale down with the program."),
}


def b64(path, mime):
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode()


# D-114. The slides are composited in HTML, not photographed.
#
# The first build screenshotted every slide, which was faithful and cost 1.5 MB
# of PNG on top of a 3.2 MB embedded PDF. The explorer would not open on a
# phone. JW, 28 September: link the paper, composite the slides.
#
# `build_deck.CARDS` already carries each slide's parts, and its heroes are
# f-strings off the ledger, so a composite moves when the ledger moves exactly
# as a photograph would. What the composite leaves out is the slide's figure,
# and that is the point: the reader has the live diagram one tab away, drawn
# from the same ledger, and it is better than a picture of a picture.

def payload():
    from ledger_national_2024 import build as n24
    from ledger_national_2030 import build as n30
    from ledger_dc_2024 import build as dc24

    panels, provs = {}, {}

    NAT = "/home/claude/nat"

    L24 = n24()
    panels["US2024"] = X.panel(
        L24, "US2024", "United States", "National",
        strap=views.V_NAT.strap, disp=views.V_NAT.disp)
    panels["US2024"]["plate"] = X.plate(
        os.path.join(NAT, "national_2024_combined.svg"), L24, V=views.V_NAT)

    for v, (label, note) in VARIANTS.items():
        L = n30(v)
        code = f"US2030_{v}"
        p = X.panel(L, code, "United States", "National",
                    strap=views.V_2030.strap, disp=views.V_2030.disp)
        provs[code] = X.provisions(L)
        p["plate"] = X.plate(
            os.path.join(NAT, f"national_2030_{v}_combined.svg"), L, provs[code], V=views.V_2030)
        p["variant"] = v
        p["variant_label"] = label
        p["variant_note"] = note
        panels[code] = p

    LDC = dc24()
    panels["DC2024"] = X.panel(
        LDC, "DC2024", "District of Columbia", "DC",
        draft=DC_DRAFT, strap=views.V_DC.strap, disp=views.V_DC.disp)
    # D-109. DC has a plate again, and an honest one. `build.py` renders it
    # with `legacy_mix=False` now: compose() truncates a panel whose service
    # fan cannot be drawn, and the drawing states the absence where the fan
    # would have been. The figures this page showed for DC services until this
    # session — long-term care $35.85, physicians $21.63 — were the national
    # mix wearing DC's name, and they are gone from both the diagram and the
    # table. The two now agree, which is the whole point.
    panels["DC2024"]["plate"] = X.plate(
        os.path.join(NAT, "dc_2024_combined.svg"), LDC, V=views.V_DC)

    return {
        "url": URL,
        "draft_mark": DC_DRAFT,
        "panels": panels,
        "provisions": provs,
        "variants": {k: {"label": a, "note": b} for k, (a, b) in VARIANTS.items()},
        "facts": X.facts(),
        "palette": palette(),
        "titles": {
            "US2024": views.V_NAT.title,
            "DC2024": views.V_DC.title,
            "US2030": views.V_2030.title,
        },
        "kickers": {
            "US2024": views.V_NAT.kicker,
            "DC2024": views.V_DC.kicker,
            "US2030": views.V_2030.kicker,
        },
    }


def palette():
    """The page's colors, from palette.py. JW, 27 September: the sankey and
    paper palettes are not to be touched. Nothing here defines a color; it
    reads the ones already declared so the explorer's flow matches the
    diagrams a reader has already seen on paper."""
    import palette as P
    return {
        "structural": dict(P.STRUCTURAL),
        "carrier": dict(P.PAYER_CARRIER),
        "health_system": dict(P.PAYER_HEALTH_SYSTEM),
        "local": list(P.PAYER_LOCAL_RAMP),
        "type": dict(P.PAYER_TYPE),
        "loss": {k: v["fill"] for k, v in P.LOSS.items()},
        "loss_label": {k: v["label"] for k, v in P.LOSS.items()},
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    data = payload()

    import palette as PAL
    # The whitepaper itself, embedded. JW, 28 September: it must work with no
    # network. The thumbnail is page 1 of the very PDF beside it, rasterized
    # here rather than kept as a separate image that could drift from it.
    import pymupdf
    # ORDERING DEFECT, 8 October. This read OUT, which only publish.py writes
    # to — and publish.py requires the built explorer, so the two could never
    # be ordered. render_v8_0.py writes the paper into the REPO; read it there,
    # where it exists before either of them runs, and fall back to OUT for a
    # warm working copy whose repo build has been cleaned.
    paper = os.path.join(REPO, f"Medicaid_Dollars_National_v{release.VERSION}.pdf")
    if not os.path.exists(paper):
        paper = os.path.join(OUT, f"Medicaid_Dollars_National_v{release.VERSION}.pdf")
    if not os.path.exists(paper):
        raise SystemExit("the paper has not been rendered; run render_v8_0.py "
                         "before build_explorer.py")
    _d = pymupdf.open(paper)
    _thumb = _d[0].get_pixmap(dpi=110).tobytes("png")
    # D-117, JW 28 September. The whitepaper's own address, given by JW for
    # the webmaster to serve. Declared here beside the file it points at so
    # the two cannot drift; the landing URL stays in landing.py and is a
    # different thing.
    PAPER_URL = "https://agilian.com/100MedicaidDollarsProject/Whitepaper"
    data["paper"] = {
        "url": PAPER_URL,
        "pages": _d.page_count,
        "file": os.path.basename(paper),
        "thumb": "data:image/png;base64," + base64.b64encode(_thumb).decode(),

    }

    assets = {
        # The two loss tints the chrome borrows for "unsigned" and "not
        # acquired". Read from palette.py, never typed into the template:
        # one declaration, and the explorer is not allowed a second.
        "LOSS_CARE_FOREGONE": PAL.LOSS["care_foregone"]["fill"],
        "LOSS_OUT_OF_POCKET": PAL.LOSS["out_of_pocket"]["fill"],
        "JOST": b64(os.path.join(REPO, "paper_fonts/Jost.ttf"), "font/ttf"),
        "NUNITO": b64(os.path.join(REPO, "paper_fonts/Nunito.ttf"), "font/ttf"),
        "TAPER": b64(os.path.join(REPO, "cover/cover_taper.png"), "image/png"),
    }

    tpl = open(TEMPLATE).read()
    blob = json.dumps(data, separators=(",", ":"))
    html = tpl.replace("/*__EXPLORER_DATA__*/null", blob)
    for k, v in assets.items():
        html = html.replace(f"__{k}__", v)

    if "__EXPLORER_DATA__" in html or re.search(r"__[A-Z]+__", html):
        raise SystemExit("template placeholder left unfilled")

    hp = os.path.join(OUT, "medicaid_dollar_explorer.html")
    jp = os.path.join(OUT, "explorer_data.json")
    open(hp, "w").write(html)
    open(jp, "w").write(json.dumps(data, indent=1))
    print(f"wrote {hp}  ({len(html)/1024:.0f} KB)")
    print(f"wrote {jp}  ({len(blob)/1024:.0f} KB of data)")
    return hp


if __name__ == "__main__":
    main()
