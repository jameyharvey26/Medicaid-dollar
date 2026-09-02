# build_pair.py — stack the FY2024 as-is over the FY2030 to-be, columns in register.
#
# The two builders share a viewBox width of 2200 and render at the same pixel
# width, so every column boundary lands on the same x in both. This script must
# never rescale either image horizontally, or that register is lost (S-060).

from PIL import Image, ImageDraw, ImageFont
import os

REPO = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(REPO, "reference_renders")
BG   = (250, 249, 246)
INK  = (32, 38, 45)
MUT  = (110, 116, 124)
WARM = (139, 90, 90)
RULE = (206, 203, 196)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def f(sz, bold=True): return ImageFont.truetype(F if bold else FR, sz)

PANELS = [
    ("national_baseline.png", "AS IS  \u00b7  NATIONAL  \u00b7  FY2024",
     "$100 of Medicaid spending, before P.L. 119-21",
     "CMS-64 FY2024 national totals. Measured, except where flagged.", (43,105,92)),
    ("national_2030_mixed_combined.png", "TO BE  \u00b7  NATIONAL  \u00b7  FY2030",
     "$100 of Medicaid spending under prior law, with P.L. 119-21 applied",
     "Every figure modelled. HR-1 lanes CBO Oct 2025; denominator CBO Jan 2025 vintage.", WARM),
    ("dc_2024_combined.png", "AS IS  \u00b7  DISTRICT OF COLUMBIA  \u00b7  FY2024",
     "$100 of DC Medicaid spending, before P.L. 119-21",
     "REDUCED FIDELITY. Four elements absent and declared on the panel, not estimated.", (43,105,92)),
    (None, "TO BE  \u00b7  DISTRICT OF COLUMBIA  \u00b7  FY2030",
     "Not yet buildable",
     "", WARM),
]

BLOCKED = [
    "This panel is blank on purpose.",
    "",
    "DC-specific HR-1 lane values do not exist yet, and the national lane mix cannot be",
    "scaled to DC. Work reporting and six-month renewals fall on the expansion group; the",
    "provider tax phase-down applies to expansion states only; the directed payment cap runs",
    "to a different Medicare threshold over a different number of steps depending on where",
    "DC's arrangements start. A non-expansion or differently-positioned jurisdiction's to-be",
    "is structurally different, not proportionally smaller (S-067).",
    "",
    "Scaling the national vector would produce a panel that looked entirely plausible and was",
    "wrong. It is left blank until DC's own lane vector is derived.",
]

imgs = []
for fn, k, t, sub, acc in PANELS:
    imgs.append(Image.open(os.path.join(R, fn)).convert("RGB") if fn else None)
ref = next(i for i in imgs if i)
W = ref.width + 80
PAD, BAND, GAP, FOOT = 40, 132, 30, 96
BLANK_H = 620
H = PAD + FOOT + sum(BAND + (im.height if im else BLANK_H) + GAP for im in imgs)
sheet = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(sheet)


def band(y, kicker, title, sub, accent):
    d.text((PAD + 8, y + 14), kicker, font=f(26), fill=accent)
    d.text((PAD + 8, y + 50), title, font=f(46), fill=INK)
    d.text((PAD + 8, y + 104), sub, font=f(22, False), fill=MUT)
    d.line([(PAD, y + BAND - 6), (W - PAD, y + BAND - 6)], fill=RULE, width=2)


y = PAD
for im, (fn, k, t, sub, acc) in zip(imgs, PANELS):
    band(y, k, t, sub, acc)
    y += BAND
    if im:
        sheet.paste(im, (PAD, y)); y += im.height + GAP
    else:
        d.rectangle([(PAD, y), (W - PAD, y + BLANK_H)], outline=RULE, width=2)
        for j, ln in enumerate(BLOCKED):
            d.text((PAD + 40, y + 46 + j * 34), ln, font=f(24, False), fill=MUT)
        y += BLANK_H + GAP

d.line([(PAD, y + 22), (W - PAD, y + 22)], fill=RULE, width=2)
d.text((PAD + 8, y + 40),
       "Columns are in register across every panel. Same column boundaries, same tracker "
       "checkpoints, same scale: 1 dollar is the same width everywhere.",
       font=f(22, False), fill=MUT)

out = os.path.join(R, "sheet_national_dc.png")
sheet.save(out)
print(f"wrote {out}  ({sheet.width} x {sheet.height})")
