#!/usr/bin/env python3
"""
S-038 encoding specimen. ENCODING layer only (D-27 / S-025).
No data-layer values are created here: every figure is read from fmap.py /
financing.py or is a difference of two of them.

Emits encoding_specimen.svg and renders via resvg_py per S-028.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "repo"))

import fmap
import resvg_py

LOSS_ANCHOR = "#8B5A5A"
INK = "#1A2733"
MUTED = "#5A6B7A"
PAPER = "#FFFFFF"

# ---------------------------------------------------------------------------
# DATA LAYER — pulled, not authored.
# ---------------------------------------------------------------------------
sdp = fmap.sdp_split()
L = {l["lane"]: l for l in fmap.LANES} if hasattr(fmap, "LANES") and isinstance(fmap.LANES, list) else None

# lane label, federal $B, total-computable $B, modelled flag, section
ROWS = [
    ("Work reporting",                    317.0, 360.0, True,  "71119"),
    ("Six-month renewals",                 58.0,  65.9, True,  "71107"),
    ("Blocked senior enrollment rule",     66.0, 112.3, False, "71101"),
    ("Blocked Medicaid enrollment rule",   53.6,  91.2, False, "71102"),
    ("Everything else",                    60.1,  92.9, True,  "resid"),
    ("Provider tax limits",               182.7, 182.7, False, "71115"),
    ("Directed payment caps",             102.0, 102.0, False, "71116"),
    ("Directed payment caps",
        round(sdp["general_fund_financed_fed"], 1),
        round(sdp["general_fund_financed_total"], 1), True, "71116"),
]
SLICE_NOTE = {6: "provider and local financed", 7: "state general fund financed"}

TOTAL_FED = sum(r[1] for r in ROWS)
TOTAL_TC = sum(r[2] for r in ROWS)

# ---------------------------------------------------------------------------
# ENCODING
# ---------------------------------------------------------------------------
W, H = 1320, 860
LEFT = 330          # label gutter
RIGHT = 1180
PLOT = RIGHT - LEFT
TOP = 186
ROW_H = 58
GAP = 12
SCALE = PLOT / 400.0   # px per $B, sized so the widest lane fits

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")

parts = []
A = parts.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
A(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

# --- defs: the open (non-federal) hatch, and the exempt terminal rule -------
A('<defs>')
A(f'''<pattern id="nonfed" width="7" height="7" patternUnits="userSpaceOnUse"
        patternTransform="rotate(45)">
      <rect width="7" height="7" fill="{PAPER}"/>
      <line x1="0" y1="0" x2="0" y2="7" stroke="{LOSS_ANCHOR}" stroke-width="1.6"/>
    </pattern>''')
A('</defs>')

# --- furniture -------------------------------------------------------------
A(f'<g id="furniture" font-family="Jost, Futura, Helvetica Neue, sans-serif">')
A(f'<text x="{LEFT}" y="48" font-size="21" font-weight="600" fill="{INK}">'
  f'What each lane takes out of the Medicaid dollar</text>')
for k, line in enumerate([
    'Ten-year total computable spending removed, $ billions. Band width is dollars leaving the ledger.',
    'Solid is the federal share of that loss; open hatch is the state and local share.',
    'Two slices carry no open segment: their non-federal share was provider revenue recycled through',
    'the state, so no state dollar stops with them.']):
    A(f'<text x="{LEFT}" y="{72+k*19}" font-size="13" fill="{MUTED}">{line}</text>')

# scale rule
y0 = TOP - 22
A(f'<line x1="{LEFT}" y1="{y0}" x2="{RIGHT}" y2="{y0}" stroke="{MUTED}" stroke-width="1"/>')
for v in (0, 100, 200, 300, 400):
    x = LEFT + v * SCALE
    A(f'<line x1="{x}" y1="{y0-5}" x2="{x}" y2="{y0}" stroke="{MUTED}" stroke-width="1"/>')
    A(f'<text x="{x}" y="{y0-10}" font-size="11" fill="{MUTED}" text-anchor="middle">${v}B</text>')
A('</g>')

# --- bands -----------------------------------------------------------------
A('<g id="overlay-hr1" font-family="Jost, Futura, Helvetica Neue, sans-serif">')
y = TOP
for i, (label, fed, tc, modelled, sec) in enumerate(ROWS):
    wfed = fed * SCALE
    wtot = tc * SCALE
    wnon = wtot - wfed
    exempt = (wnon < 0.5)

    # label gutter, plain language leads (S-033)
    ty = y + ROW_H / 2 + 1
    sub = SLICE_NOTE.get(i)
    if sub:
        A(f'<text x="{LEFT-16}" y="{ty-7}" font-size="14" fill="{INK}" '
          f'text-anchor="end">{esc(label)}</text>')
        A(f'<text x="{LEFT-16}" y="{ty+10}" font-size="11.5" fill="{MUTED}" '
          f'text-anchor="end">{esc(sub)}</text>')
    else:
        A(f'<text x="{LEFT-16}" y="{ty+4}" font-size="14" fill="{INK}" '
          f'text-anchor="end">{esc(label)}</text>')

    # federal zone: solid
    A(f'<rect x="{LEFT}" y="{y}" width="{wfed:.2f}" height="{ROW_H}" '
      f'fill="{LOSS_ANCHOR}"/>')

    if not exempt:
        # non-federal zone: open hatch, hairline division
        A(f'<rect x="{LEFT+wfed:.2f}" y="{y}" width="{wnon:.2f}" height="{ROW_H}" '
          f'fill="url(#nonfed)" stroke="{LOSS_ANCHOR}" stroke-width="1"/>')
        A(f'<line x1="{LEFT+wfed:.2f}" y1="{y}" x2="{LEFT+wfed:.2f}" y2="{y+ROW_H}" '
          f'stroke="{PAPER}" stroke-width="1.4"/>')
    else:
        # terminal stop-rule: the band ends where the loss ends, and says so
        xe = LEFT + wfed
        A(f'<line x1="{xe:.2f}" y1="{y-4}" x2="{xe:.2f}" y2="{y+ROW_H+4}" '
          f'stroke="{INK}" stroke-width="2.2"/>')
        A(f'<text x="{xe+12:.2f}" y="{y+ROW_H/2+4}" font-size="11.5" fill="{INK}">'
          f'no state dollar stops here</text>')

    # figures at the band end
    xr = LEFT + wtot + (172 if exempt else 12)
    flag = ' \u25b3' if modelled else ''
    A(f'<text x="{xr:.2f}" y="{y+ROW_H/2+4}" font-size="12.5" fill="{INK}">'
      f'${tc:,.1f}B{flag}</text>')

    y += ROW_H + GAP

A('</g>')

# --- totals + footnotes ----------------------------------------------------
yb = y + 14
A(f'<g font-family="Jost, Futura, Helvetica Neue, sans-serif">')
A(f'<line x1="{LEFT}" y1="{yb}" x2="{RIGHT}" y2="{yb}" stroke="{INK}" stroke-width="1"/>')
A(f'<text x="{LEFT}" y="{yb+22}" font-size="13" fill="{INK}">'
  f'Total removed ${TOTAL_TC:,.1f}B \u2014 federal ${TOTAL_FED:,.1f}B, '
  f'state and local ${TOTAL_TC-TOTAL_FED:,.1f}B</text>')
A(f'<text x="{LEFT}" y="{yb+44}" font-size="11" fill="{MUTED}">'
  f'\u25b3 contains a modelled rate or weight. Sections, in order: 71119, 71107, 71101, '
  f'71102, residual, 71115, 71116, 71116.</text>')
A(f'<text x="{LEFT}" y="{yb+62}" font-size="11" fill="{MUTED}">'
  f'Federal figures: CBO supplemental cost estimate, P.L. 119-21, 28 Oct 2025, deficit basis. '
  f'Gross-up rates derived from CMS-64 FY2024 national totals, MAP only.</text>')
A('</g>')
A('</svg>')

svg = "\n".join(parts)
open("encoding_specimen.svg", "w").write(svg)

png = resvg_py.svg_to_bytes(svg_string=svg, width=2640)

open("encoding_specimen.png", "wb").write(bytes(png))
print(f"total computable ${TOTAL_TC:,.1f}B  federal ${TOTAL_FED:,.1f}B  "
      f"non-federal ${TOTAL_TC-TOTAL_FED:,.1f}B")
print("wrote encoding_specimen.svg / .png")
