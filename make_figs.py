from PIL import Image
import os, json

CROPS = {}   # figure file -> (x0, y0, x1, y1) in panel viewBox units, plus source panel

SRC = "reference_renders/national_2024_combined.png"
OUT = "paper_figs"
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert("RGB")
W, H = im.size
S = W / 2200.0          # viewBox units -> png px


def crop(name, x0, y0, x1, y1):
    CROPS[name] = dict(panel="2024", box=[x0, y0, x1, y1])
    box = (int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S))
    box = (max(0, box[0]), max(0, box[1]), min(W, box[2]), min(H, box[3]))
    c = im.crop(box)
    c.save(os.path.join(OUT, name))
    print(name, c.size)


# Fig 1 — the whole panel
CROPS["fig1_panel_2024.png"] = dict(panel="2024", box=[0, 0, 2200, 1376])
im.save(os.path.join(OUT, "fig1_panel_2024.png"))
print("fig1_panel_2024.png", im.size)

# Fig 2 — sources through the state agency: the two source bands, administration
#         and the Medicare premiums return flow.
crop("fig2_sources.png", 60, 80, 900, 780)

# Fig 3 — the payer column: three lanes in, margin peeling up and out.
crop("fig3_payer.png", 640, 90, 1400, 780)

# Fig 4 — provider bars.
crop("fig4_providers.png", 1250, 120, 1772, 900)

# Fig 5 — the number line, full width.
crop("fig5_numberline.png", 0, 1090, 2190, 1400)

# ---- FY2030 -------------------------------------------------------------
SRC30 = "reference_renders/national_2030_mixed_combined.png"
im30 = Image.open(SRC30).convert("RGB")
W3, H3 = im30.size
S3 = W3 / 2200.0


def crop30(name, x0, y0, x1, y1):
    CROPS[name] = dict(panel="2030", box=[x0, y0, x1, y1])
    box = (int(x0 * S3), int(y0 * S3), int(x1 * S3), int(y1 * S3))
    box = (max(0, box[0]), max(0, box[1]), min(W3, box[2]), min(H3, box[3]))
    c = im30.crop(box)
    c.save(os.path.join(OUT, name))
    print(name, c.size)


CROPS["fig6_panel_2030.png"] = dict(panel="2030", box=[0, 0, 2200, 1376])
im30.save(os.path.join(OUT, "fig6_panel_2030.png"))
print("fig6_panel_2030.png", im30.size)

crop30("fig7_lanes_2030.png",   60, 600, 1800, 1120)   # the warm HR-1 ribbons
crop30("fig8_payer_2030.png",  620,  90, 1800, 1065)   # payer column under the law
crop30("fig9_providers_2030.png", 1250, 120, 1772, 900)
crop30("fig10_numberline_2030.png", 0, 1104, 2190, 1400)

# ---- charter figures ----------------------------------------------------
# C-08.3: the two balance lines stacked, so the difference is read not described.
a = Image.open(os.path.join(OUT, "fig5_numberline.png"))
b = Image.open(os.path.join(OUT, "fig10_numberline_2030.png"))
gap = 26
pair = Image.new("RGB", (max(a.width, b.width), a.height + gap + b.height), "#faf8f3")
pair.paste(a, (0, 0))
pair.paste(b, (0, a.height + gap))
pair.save(os.path.join(OUT, "figA_lines_pair.png"))
print("figA_lines_pair.png", pair.size)

# C-08.2 / #34 / #73: provider bars WITH the beneficiary pies beside them.
crop("fig4b_providers_pies.png", 1250, 100, 2200, 910)
crop30("fig9b_providers_pies_2030.png", 1250, 100, 2200, 910)

# Section VII needs the FY2030 beneficiary column on its own.
crop30("fig11_beneficiaries_2030.png", 1745, 100, 2200, 910)

# FY2030 detail crops, parallel to the FY2024 set.
crop30("fig12_sources_2030.png", 60, 80, 950, 1120)

# The right-hand terminals: where the remaining provisions actually land.
crop30("fig14_terminals_left.png",   60, 540, 1250, 1120)
crop30("fig13_terminals_2030.png", 950, 540, 1900, 1120)

# The provisions crop with the FY2030 balance line beneath it, so the reader can
# see the provisions and the totals they produce in one figure.
a = Image.open(os.path.join(OUT, "fig7_lanes_2030.png"))
b = Image.open(os.path.join(OUT, "fig10_numberline_2030.png"))
sc = a.width / b.width
b2 = b.resize((a.width, int(b.height * sc)))
gap = 18
comb = Image.new("RGB", (a.width, a.height + gap + b2.height), "#faf8f3")
comb.paste(a, (0, 0))
comb.paste(b2, (0, a.height + gap))
comb.save(os.path.join(OUT, "figB_provisions_with_line.png"))
print("figB_provisions_with_line.png", comb.size)


# figB is the provisions crop with the balance line stacked under it; for the purpose
# of "is the thing being discussed visible", it covers the provisions crop's box.
CROPS["figB_provisions_with_line.png"] = dict(panel="2030", box=list(CROPS["fig7_lanes_2030.png"]["box"]))
CROPS["figA_lines_pair.png"] = dict(panel="2024", box=[0, 1090, 2190, 1400])

with open(os.path.join(OUT, "crops.json"), "w") as f:
    json.dump(CROPS, f, indent=1, sort_keys=True)
print("wrote crops.json with", len(CROPS), "entries")
