#!/usr/bin/env python3
"""Bite-point mapping sketch: where each HR-1 lane peels out of the master.
Annotation layer composited onto the real national_baseline.svg, same viewBox.
No band widths drawn: per-$100 values are blocked on the FY2029 denominator."""
import resvg_py, re

BASE = open("render/national_baseline.svg").read()
LOSS, INK, MUT, RELIEF = "#8B5A5A", "#272727", "#6f6f6f", "#C4A45C"
BG = "#faf8f3"

xSG=(300,560); xSA=(560,820); xDI=(820,1060); xCL=(1300,1560)
A=[]; a=A.append
def label(x,y,s,size=13,w="bold",fill=INK,anchor="start",italic=False):
    st=' font-style="italic"' if italic else ''
    a(f'<text x="{x}" y="{y}" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="{size}" '
      f'text-anchor="{anchor}" font-weight="{w}" paint-order="stroke" stroke="{BG}" stroke-width="3.2" '
      f'stroke-linejoin="round" fill="{fill}"{st}>{s}</text>')

a('<g id="overlay-hr1-bitepoints">')

# --- the empty channel HR-1 peels into ---
a(f'<line x1="110" y1="902" x2="2180" y2="902" stroke="{LOSS}" stroke-width="1.1" stroke-dasharray="6 5" stroke-opacity="0.55"/>')
label(120, 896, "HR-1 peels downward into this channel &#8212; grey leakage above is what the system always lost", 13, "bold", LOSS)

MARKS = [
  # x, plain label, where, note, colour
  (xSG[0]+150, 830, "Provider tax limits", "STATE GOVERNMENT &#8212; shrinks the pot before the $100 assembles",
   "federal match peels; state share crosses into the container", LOSS),
  (xSA[0]+118, 200, "Blocked senior enrollment rule", "STATE AGENCY &#8212; rides the existing Medicare premiums arrow",
   "fewer MSP enrollees, so less Medicaid&#8594;Medicare premium", LOSS),
  (xDI[0]+90, 830, "Work reporting", "DISBURSEMENTS &#8212; the dollar never becomes a payment",
   "expansion adults leave; capitation and claims are never made", LOSS),
  (xDI[0]+90, 872, "Six-month renewals", "", "same mechanism, twice-yearly renewal churn", LOSS),
  (xDI[0]+90, 900, "Blocked Medicaid enrollment rule", "", "enrolment lower than prior law would have produced", LOSS),
  (xCL[0]+60, 830, "Directed payment caps", "CLAIMS &#8212; payments to providers are ratcheted down",
   "two slices: provider-financed peels, general-fund slice returns state money", LOSS),
]

# vertical drop rules at each bite column
for x, ycol, name in [(xSG[0]+150,"STATE GOVERNMENT",""),(xSA[0]+118,"",""),(xDI[0]+90,"",""),(xCL[0]+60,"","")]:
    a(f'<line x1="{x}" y1="130" x2="{x}" y2="902" stroke="{LOSS}" stroke-width="1.4" '
      f'stroke-dasharray="4 6" stroke-opacity="0.45"/>')
    a(f'<path d="M{x-7},894 L{x},906 L{x+7},894 Z" fill="{LOSS}"/>')

# --- annotations, stacked below the channel ---
rows = [
 (xSG[0]+150, "Provider tax limits", "bites at STATE GOVERNMENT",
  "Shrinks the non-federal share before the $100 assembles. Only the federal match peels as loss (D-39);",
  "the displaced general fund obligation crosses into the container, which sits in this same column."),
 (xSA[0]+118, "Blocked senior enrollment rule", "bites at STATE AGENCY",
  "Medicare Savings Program enrolment stays lower than prior law. The loss rides the existing",
  "Medicare premiums arrow ($2.90) rather than opening a new path."),
 (xDI[0]+90, "Coverage and preserved-friction lanes",
  "bite at DISBURSEMENTS",
  "Work reporting, six-month renewals, blocked Medicaid enrollment rule, everything else. The dollar never",
  "becomes capitation or a claim, so it peels before the three lanes split. &#8220;Everything else&#8221; is a mixed bucket."),
 (xCL[0]+60, "Directed payment caps", "bites at CLAIMS",
  "Supplemental payments to hospitals and nursing facilities ratchet toward Medicare rates. Provider-financed",
  "slice peels as loss; the general-fund slice returns money to the state and crosses back into the container."),
]
y = 1180
for x, name, where, l1, l2 in rows:
    a(f'<circle cx="128" cy="{y-5}" r="5" fill="{LOSS}"/>')
    label(144, y, name, 15, "bold", INK)
    label(144, y+18, where, 12.5, "bold", LOSS)
    label(560, y, l1, 12.5, "normal", MUT)
    label(560, y+17, l2, 12.5, "normal", MUT)
    y += 46

label(120, y+14, "Bite points only. Band widths are not drawn: per-$100 values at the 2029 anchor are blocked on a total-spending denominator not yet in the repo.",
      12, "normal", LOSS, italic=True)
a('</g>')

ann = "\n".join(A)
out = BASE.replace("</svg>", ann + "\n</svg>")
out = out.replace('viewBox="0 0 2200 1110"', 'viewBox="0 0 2200 1420"')
open("bite_points.svg","w").write(out)
open("bite_points.png","wb").write(bytes(resvg_py.svg_to_bytes(svg_string=out, width=2640)))
print("ok")
