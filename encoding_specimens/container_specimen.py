#!/usr/bin/env python3
"""S-039 specimen: the unsized state general fund container (D-47).
ENCODING layer only. Figures read from financing.py / fmap.py."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "repo"))
import financing, fmap, resvg_py

INK, MUTED, PAPER = "#1A2733", "#5A6B7A", "#FFFFFF"
LOSS = "#8B5A5A"
COOL = "#35519E"
RELIEF = "#C4A45C"

opening = financing.second_ledger_opening()
sdp = fmap.sdp_split()
GF_PER100 = opening["state_general_revenue"]          # 23.77
PRESSURE_PER100 = financing.provider_tax_split()["substituting_for_general_fund"]
RELIEF_B = sdp["state_relief"]

W, H = 1500, 640
P = []; A = P.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
A(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
A('<defs>')
A(f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0.55" stop-color="{MUTED}" stop-opacity="1"/>'
  f'<stop offset="1" stop-color="{MUTED}" stop-opacity="0"/></linearGradient>')
A(f'<marker id="ar" markerUnits="userSpaceOnUse" markerWidth="26" markerHeight="22" refX="20" refY="11" orient="auto">'
  f'<path d="M0,0 L20,11 L0,22 z" fill="{INK}"/></marker>')
A('</defs>')
F = 'font-family="Jost, Futura, Helvetica Neue, sans-serif"'

A(f'<g {F}>')
A(f'<text x="60" y="46" font-size="20" font-weight="600" fill="{INK}">'
  f'The state row of the government column</text>')
A(f'<text x="60" y="70" font-size="13" fill="{MUTED}">'
  f'Medicaid&#8217;s general fund share is one claimant among several. Only the shaded band is measured.</text>')

# ---- the container: open frame, no closed right edge, no fill -------------
cx, cy, cw, ch = 360, 118, 760, 340
A(f'<path d="M {cx+cw} {cy} L {cx} {cy} L {cx} {cy+ch} L {cx+cw} {cy+ch}" '
  f'fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="7 5"/>')
A(f'<rect x="{cx+cw-260}" y="{cy-1}" width="260" height="2" fill="url(#fade)"/>')
A(f'<rect x="{cx+cw-260}" y="{cy+ch-1}" width="260" height="2" fill="url(#fade)"/>')
A(f'<text x="{cx+14}" y="{cy+26}" font-size="14" font-weight="600" fill="{INK}">State general fund</text>')
A(f'<text x="{cx+14}" y="{cy+45}" font-size="11.5" fill="{MUTED}">shown for context. Edge is open: this box has no width you can read.</text>')

# ---- the one measured band inside ----------------------------------------
by, bh = cy+112, 76
A(f'<rect x="{cx-150}" y="{by}" width="{150+330}" height="{bh}" fill="{COOL}" fill-opacity="0.85"/>')
A(f'<text x="{cx+18}" y="{by+29}" font-size="13" fill="{PAPER}">Medicaid, state general fund financed</text>')
A(f'<text x="{cx+18}" y="{by+53}" font-size="15" font-weight="600" fill="{PAPER}">${GF_PER100:.2f} per $100</text>')
A(f'<text x="{cx-150}" y="{by-12}" font-size="11.5" fill="{MUTED}">from the $100 ledger &#8212; drawn to scale</text>')

# other claimants: unlabelled, unsized, clearly not flows
for i, lab in enumerate(["other claimants on the same fund", "", ""]):
    yy = cy+230+i*26
    A(f'<line x1="{cx+40}" y1="{yy}" x2="{cx+40+260-i*70}" y2="{yy}" stroke="{MUTED}" '
      f'stroke-width="7" stroke-opacity="0.16" stroke-linecap="round"/>')
A(f'<text x="{cx+40}" y="{cy+222}" font-size="11.5" fill="{MUTED}">'
  f'other claimants &#8212; not sized, not summed, not part of the ledger</text>')

# ---- crossing flows: fixed-width stubs, figures annotated -----------------
sw = 14
ay = cy+ch+66
A(f'<line x1="{cx+120}" y1="{ay}" x2="{cx+120}" y2="{by+bh+6}" stroke="{LOSS}" '
  f'stroke-width="{sw}" marker-end="url(#ar)" stroke-opacity="0.9"/>')
A(f'<text x="{cx+142}" y="{ay-4}" font-size="12.5" fill="{INK}">IN &#8212; provider tax limits re-present a general fund bill</text>')
A(f'<text x="{cx+142}" y="{ay+16}" font-size="14" font-weight="600" fill="{INK}">${PRESSURE_PER100:.2f} per $100</text>')

A(f'<line x1="{cx+600}" y1="{by+bh+6}" x2="{cx+600}" y2="{ay}" stroke="{RELIEF}" '
  f'stroke-width="{sw}" marker-end="url(#ar)"/>')
A(f'<text x="{cx+622}" y="{ay-4}" font-size="12.5" fill="{INK}">OUT &#8212; directed payment caps return state money</text>')
A(f'<text x="{cx+622}" y="{ay+16}" font-size="14" font-weight="600" fill="{INK}">${RELIEF_B:.1f}B over ten years &#9651;</text>')
A(f'<text x="{cx+622}" y="{ay+34}" font-size="11" fill="{LOSS}">UNIT MISMATCH &#8212; not convertible to per $100 from any figure in this repo</text>')

A(f'<text x="{cx+120-40}" y="{ay+40}" font-size="11" fill="{MUTED}">'
  f'Crossing arrows are drawn at one fixed width. Width carries no quantity here; read the figures.</text>')

A(f'<text x="60" y="{H-34}" font-size="11" fill="{MUTED}">'
  f'&#9651; modelled. Nothing enters or leaves the $100 through this box: the general fund share is displaced, not spent twice.</text>')
A('</g></svg>')

svg = "\n".join(P)
open("container_specimen.svg","w").write(svg)
open("container_specimen.png","wb").write(bytes(resvg_py.svg_to_bytes(svg_string=svg, width=2520)))
print(f"GF ${GF_PER100:.2f}/100  pressure ${PRESSURE_PER100:.2f}/100  relief ${RELIEF_B:.1f}B")
