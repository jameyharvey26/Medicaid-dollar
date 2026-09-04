#!/usr/bin/env python3
"""sheet.py — stack N rendered diagrams into one comparison sheet.

Replaces build_pair.py, which hard-coded four panels in a list literal and had
the panel copy, the layout and the output path welded together.

A sheet is a list of PANEL keys. Every panel is declared once in PANELS, the
way outflows are declared once in outflows.py, so the same panel used in three
sheets carries the same kicker, title and caption in all three. Named sets in
SETS are the sheets we build often; anything else is an ad-hoc key list on the
command line.

    python3 sheet.py                              # the default set
    python3 sheet.py --set overhead               # a named set
    python3 sheet.py national_2024 national_2030  # ad-hoc, any order, any N
    python3 sheet.py --list                       # what can be stacked
    python3 sheet.py --set overhead --out foo.png
    python3 sheet.py --set national_dc --blanks    # include declared blanks

Declared-blank panels (S-072) are DROPPED from a named set unless --blanks is
given. A blank is a statement to a reader about why something cannot be built; it
is noise on a working comparison sheet. Naming a blank key explicitly on the
command line always includes it, because that is an explicit ask.

Panels are NEVER rescaled horizontally. Column register between panels is the
whole point of the sheet, and a resize destroys it (S-060, STYLE_GUIDE 1.2/1.3).
A panel rendered at a different pixel width than its neighbours is a defect in
the renderer, not something this script papers over; it is reported and the
sheet still builds so the mismatch is visible.
"""
from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(REPO, "reference_renders")

# ---------------------------------------------------------------- style
BG = (250, 249, 246)
INK = (32, 38, 45)
MUT = (110, 116, 124)
WARM = (139, 90, 90)          # HR-1 warm, STYLE_GUIDE 5.5
GREEN = (43, 105, 92)         # as-is accent
RULE = (206, 203, 196)

PAD, BAND, GAP, FOOT = 40, 132, 30, 96
BLANK_H = 620

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, sz)


FOOTER = ("Columns are in register across every panel. Same column boundaries, "
          "same tracker checkpoints, same scale: 1 dollar is the same width "
          "everywhere.")


# ---------------------------------------------------------------- panels
def panel(png, kicker, title, sub, accent=GREEN, blocked=None):
    """One declared panel. png=None plus blocked=[lines] is a declared blank (S-072)."""
    return dict(png=png, kicker=kicker, title=title, sub=sub,
                accent=accent, blocked=blocked)


DC_2030_BLOCKED = [
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

PANELS = {
    "national_2024": panel(
        "national_baseline.png",
        "AS IS  \u00b7  NATIONAL  \u00b7  FY2024",
        "$100 of Medicaid spending, before P.L. 119-21",
        "CMS-64 FY2024 national totals. Measured, except where flagged.",
        GREEN),

    "national_2030": panel(
        "national_2030_mixed_combined.png",
        "TO BE  \u00b7  NATIONAL  \u00b7  FY2030",
        "$100 of Medicaid spending under prior law, with P.L. 119-21 applied",
        "Every figure modelled. HR-1 lanes CBO Oct 2025; denominator CBO Jan 2025 vintage.",
        WARM),

    "national_2030_mixed": panel(
        "national_2030_mixed_combined.png",
        "TO BE  \u00b7  NATIONAL  \u00b7  FY2030  \u00b7  SPLIT OVERHEAD",
        "Plan administration scales with capitation; state administration holds",
        "The standing assumption (D-63). Health services delivered $77.79.",
        WARM),

    "national_2030_holds": panel(
        "national_2030_holds_combined.png",
        "TO BE  \u00b7  NATIONAL  \u00b7  FY2030  \u00b7  OVERHEAD HOLDS",
        "All overhead held at its FY2024 dollar amount",
        "Sensitivity, not published as an alternative. Health services delivered $77.28.",
        WARM),

    "national_2030_scales": panel(
        "national_2030_scales_combined.png",
        "TO BE  \u00b7  NATIONAL  \u00b7  FY2030  \u00b7  OVERHEAD SCALES",
        "All overhead scales down with the trunk",
        "Sensitivity, not published as an alternative. Health services delivered $77.85.",
        WARM),

    "dc_2024": panel(
        "dc_2024_combined.png",
        "AS IS  \u00b7  DISTRICT OF COLUMBIA  \u00b7  FY2024",
        "$100 of DC Medicaid spending, before P.L. 119-21",
        "REDUCED FIDELITY. Four elements absent and declared on the panel, not estimated.",
        GREEN),

    "dc_2030": panel(
        None,
        "TO BE  \u00b7  DISTRICT OF COLUMBIA  \u00b7  FY2030",
        "Not yet buildable",
        "",
        WARM,
        blocked=DC_2030_BLOCKED),
}

SETS = {
    # The working default: the as-is and the to-be, nothing else. JW, 2026-09-03.
    "working": ["national_2024", "national_2030"],
    # Publication sheet; keeps its declared blank.
    "national_dc": ["national_2024", "national_2030", "dc_2024", "dc_2030"],
    # Overhead sensitivities back EN-17. Buildable, never on the default path.
    "overhead": ["national_2030_holds", "national_2030_mixed", "national_2030_scales"],
}

# Rebuilt by `build.py`. The overhead set is left out: its panels are only
# rendered by `build.py sensitivity`, so rebuilding it here would stale-fail.
# Derived, never hand-listed: a second list of set names is a second thing to
# keep in sync, and it drifted the first time. build.py rebuilds all of these so
# no sheet can go stale behind a render that moved.
WORKING_SETS = list(SETS)

# Publication sets keep their declared blanks: on a sheet that goes to a reader, a
# blank panel is the statement (S-072). Review sets drop them, because a reader is
# not present and the blank is just noise between two things being compared.
PUBLICATION_SETS = {"national_dc"}

DEFAULT_SET = "working"
DEFAULT_OUT = {"working": "sheet_working.png",
               "national_dc": "sheet_national_dc.png",
               "overhead": "sheet_overhead.png"}


# ---------------------------------------------------------------- build
def build(keys, out, blanks=False):
    unknown = [k for k in keys if k not in PANELS]
    if unknown:
        sys.exit(f"unknown panel(s): {', '.join(unknown)}\n"
                 f"known: {', '.join(sorted(PANELS))}")

    if not blanks:
        dropped = [k for k in keys if PANELS[k]["png"] is None]
        if dropped:
            keys = [k for k in keys if PANELS[k]["png"] is not None]
            print(f"  skipped declared blank(s): {', '.join(dropped)}  (--blanks to include)")

    specs = [PANELS[k] for k in keys]
    imgs = []
    for k, s in zip(keys, specs):
        if s["png"] is None:
            imgs.append(None)
            continue
        p = os.path.join(R, s["png"])
        if not os.path.exists(p):
            sys.exit(f"panel '{k}' wants {s['png']}, which is not in reference_renders/.\n"
                     f"run  python3 build.py  first.")
        imgs.append(Image.open(p).convert("RGB"))

    live = [im for im in imgs if im]
    if not live:
        sys.exit("a sheet needs at least one rendered panel.")

    widths = {im.width for im in live}
    if len(widths) > 1:
        print(f"  WARNING  panels differ in pixel width {sorted(widths)}. "
              f"Not rescaling: column register would be lost (S-060). "
              f"Fix the renderer.")

    W = max(widths) + 2 * PAD
    H = PAD + FOOT + sum(BAND + (im.height if im else BLANK_H) + GAP for im in imgs)
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)

    y = PAD
    for im, s in zip(imgs, specs):
        d.text((PAD + 8, y + 14), s["kicker"], font=f(26), fill=s["accent"])
        d.text((PAD + 8, y + 50), s["title"], font=f(46), fill=INK)
        d.text((PAD + 8, y + 104), s["sub"], font=f(22, False), fill=MUT)
        d.line([(PAD, y + BAND - 6), (W - PAD, y + BAND - 6)], fill=RULE, width=2)
        y += BAND
        if im:
            sheet.paste(im, (PAD, y))
            y += im.height + GAP
        else:
            d.rectangle([(PAD, y), (W - PAD, y + BLANK_H)], outline=RULE, width=2)
            for j, ln in enumerate(s["blocked"] or []):
                d.text((PAD + 40, y + 46 + j * 34), ln, font=f(24, False), fill=MUT)
            y += BLANK_H + GAP

    d.line([(PAD, y + 22), (W - PAD, y + 22)], fill=RULE, width=2)
    d.text((PAD + 8, y + 40), FOOTER, font=f(22, False), fill=MUT)

    os.makedirs(R, exist_ok=True)
    path = out if os.path.isabs(out) else os.path.join(R, out)
    sheet.save(path)
    print(f"wrote {path}  ({sheet.width} x {sheet.height})  {len(keys)} panels")
    return path


def main():
    ap = argparse.ArgumentParser(description="stack N rendered diagrams into one sheet")
    ap.add_argument("panels", nargs="*", help="panel keys, in stacking order")
    ap.add_argument("--set", dest="named", help=f"a named set: {', '.join(sorted(SETS))}")
    ap.add_argument("--out", help="output filename (lands in reference_renders/)")
    ap.add_argument("--blanks", action="store_true",
                    help="include declared-blank panels in a named set")
    ap.add_argument("--list", action="store_true", help="list panels and sets, then exit")
    a = ap.parse_args()

    if a.list:
        print("panels:")
        for k in sorted(PANELS):
            src = PANELS[k]["png"] or "declared blank"
            print(f"  {k:24s} {src}")
        print("\nsets:")
        for k, v in SETS.items():
            print(f"  {k:24s} {' '.join(v)}")
        return

    if a.panels:
        # an explicitly named blank is an explicit ask; honour it.
        keys, out, a.blanks = a.panels, a.out or "sheet_custom.png", True
    else:
        name = a.named or DEFAULT_SET
        if name not in SETS:
            sys.exit(f"unknown set '{name}'. known: {', '.join(sorted(SETS))}")
        keys, out = SETS[name], a.out or DEFAULT_OUT.get(name, f"sheet_{name}.png")
        if name in PUBLICATION_SETS:
            a.blanks = True

    build(keys, out, blanks=a.blanks)


if __name__ == "__main__":
    main()
