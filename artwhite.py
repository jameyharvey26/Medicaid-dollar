"""Is there dead paper inside the diagrams themselves?

whitespace.py measures the page. This measures the pictures on it, which is a
different fault and was invisible to every instrument in the repo: a figure
drawn on a canvas taller than its own content prints blank paper that the page
has no way to reclaim, because as far as the page is concerned that blank is
part of the picture. JW caught three of them by eye - Figures 6, 8 and 11 - and
each one was costing the page around 40mm.

    python3 artwhite.py [dir]

Reports, per generated PNG, the uniform margin of background at each edge. The
generators trim their own canvases to content now, so this should report
nothing; it exists so that the next figure drawn to a typed height is caught
here rather than by a reader.

Crops of a panel are exempt. A crop is a window onto a drawing and its margin
is the drawing's own composition, not slack.
"""
import glob
import os
import sys

from PIL import Image

# A figure is entitled to its own margin, so the threshold is not zero. It is
# set at the widest margin any of these graphics deliberately carries; past
# that, the blank is canvas the content never used, which is the fault this
# file is for.
MAX_MM = 10.0
PXMM_PRINT = 300 / 25.4  # the generators raster at 300dpi
BG = (255, 255, 255)
TOL = 6                 # a pixel this close to white counts as background


def blank_run(im, edge):
    """How many rows or columns of uniform background sit at this edge."""
    w, h = im.size
    px = im.load()
    n = 0
    if edge in ("top", "bottom"):
        rows = range(h) if edge == "top" else range(h - 1, -1, -1)
        for y in rows:
            if any(abs(px[x, y][c] - BG[c]) > TOL
                   for x in range(0, w, 3) for c in range(3)):
                break
            n += 1
    else:
        cols = range(w) if edge == "left" else range(w - 1, -1, -1)
        for x in cols:
            if any(abs(px[x, y][c] - BG[c]) > TOL
                   for y in range(0, h, 3) for c in range(3)):
                break
            n += 1
    return n


def main(d="cover"):
    bad = seen = 0
    for path in sorted(glob.glob(os.path.join(d, "*.png"))):
        if "_standalone" in path:
            continue                       # not placed on a page
        im = Image.open(path).convert("RGB")
        seen += 1
        for edge in ("top", "bottom", "left", "right"):
            run_mm = blank_run(im, edge) / PXMM_PRINT
            if run_mm > MAX_MM:
                bad += 1
                print(f"  {os.path.basename(path):34} {run_mm:5.1f} mm of dead "
                      f"paper at the {edge}")
    if not seen:
        print(f"\nNO GENERATED FIGURES FOUND in {d}/. This file cannot report "
              f"on pictures it cannot see.")
        return 1
    print(f"\n{bad} edge(s) carry more than {MAX_MM:.0f}mm of dead paper, "
          f"over {seen} figures" if bad else
          f"\nno generated figure carries more than {MAX_MM:.0f}mm of dead "
          f"paper at any edge, over {seen} figures")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "cover"))
