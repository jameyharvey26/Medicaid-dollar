#!/usr/bin/env python3
"""build.py — render every artifact from one renderer.

Replaces build_sankey.py (script) and build_tobe_2030.py (text-substitution
fork). One renderer in sankey.py, one config per artifact in instances.py.

Usage:  python3 build.py            # everything
        python3 build.py 2024       # one instance
"""
import os, re, shutil, subprocess, sys

import sankey
import instances
from check import gate
from tobe2030 import per100
from ledger_2030 import ledger

REPO = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(REPO, "reference_renders")
OUT = "/home/claude/nat"


def wrap(body):
    return (f'<svg viewBox="0 0 {sankey.W} {sankey.H}" width="100%" '
            f'xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>')


def emit(tag, base, over):
    os.makedirs(OUT, exist_ok=True); os.makedirs(REF, exist_ok=True)
    b = '<g id="baseline">\n' + "\n".join(base) + "\n</g>"
    o = '<g id="overlay-hr1">\n' + "\n".join(over) + "\n</g>"
    files = [(f"{tag}_combined", wrap(b + "\n" + o)),
             (f"{tag}_baseline", wrap(b + '\n<g id="overlay-hr1" display="none">\n</g>')),
             (f"{tag}_overlay",  wrap('<g id="baseline" display="none">\n</g>\n' + o))]
    vbs = set()
    for name, doc in files:
        p = os.path.join(OUT, name + ".svg")
        open(p, "w").write(doc)
        vbs.add(re.search(r'viewBox="([^"]+)"', doc).group(1))
        print(f"  svg  {name}.svg  ({len(doc):,} bytes)")
    assert len(vbs) == 1, f"viewBox drift: {vbs}"
    print(f"  ok   viewBox identical across all three: {vbs.pop()}")
    # resvg only, hard-pinned. cairosvg ignores paint-order and erodes the halos.
    import resvg_py
    for name in (f"{tag}_combined",):
        svg = open(os.path.join(OUT, name + ".svg")).read()
        png = resvg_py.svg_to_bytes(svg_string=svg, width=2600)
        open(os.path.join(OUT, name + ".png"), "wb").write(bytes(png))
        print(f"  png  {name}.png  (2600px, resvg)")
    for name, _ in files:
        for ext in (".svg", ".png"):
            src = os.path.join(OUT, name + ext)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(REF, name + ext))


def build_2024():
    gate(instances.AS_IS_2024, 'FY2024 as-is')
    base, over = sankey.render(instances.AS_IS_2024)
    emit("national_2024", base, over)
    shutil.copy2(os.path.join(REF, "national_2024_combined.png"),
                 os.path.join(REF, "national_baseline.png"))


def build_dc():
    cfg = instances.as_is_dc()
    gate(cfg, "DC FY2024 as-is")
    base, over = sankey.render(cfg)
    emit("dc_2024", base, over)


def build_2030(variant="mixed"):
    L = ledger(variant)
    cfg = instances.to_be_2030(L, per100)
    gate(cfg, f'FY2030 to-be [{variant}]')
    base, over = sankey.render(cfg)
    emit(f"national_2030_{variant}", base, over)
    if variant == "mixed":
        shutil.copy2(os.path.join(REF, "national_2030_mixed_combined.png"),
                     os.path.join(REF, "national_2030_combined.png"))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "2024"):
        print("FY2024 as-is"); build_2024()
    if which in ("all", "2030"):
        # Split overhead only. The holds/scales sensitivities are settled (D-63,
        # EN-17) and are not rebuilt in a working session; `python3 build.py
        # sensitivity` renders all three when the endnote needs re-checking.
        print("FY2030 to-be [mixed]"); build_2030("mixed")
    if which == "sensitivity":
        for v in ("holds", "scales", "mixed"):
            print(f"FY2030 to-be [{v}]"); build_2030(v)
        subprocess.run([sys.executable, os.path.join(REPO, "sheet.py"),
                        "--set", "overhead"], check=True)
    if which in ("all", "dc"):
        print("DC FY2024 as-is"); build_dc()
    if which == "all":
        # Every declared set is rebuilt, so no sheet in reference_renders/ can go
        # stale behind a render that moved. Adding a set to sheet.py:SETS is
        # enough; nothing here needs touching.
        import sheet as _sheet
        for _name in _sheet.WORKING_SETS:
            subprocess.run([sys.executable, os.path.join(REPO, "sheet.py"),
                            "--set", _name], check=True)
    print("build complete.")
