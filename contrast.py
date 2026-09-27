"""Measure WCAG contrast instead of asserting it.

Every custom graphic in this project carries an accessibility claim in its
docstring. Until now the ratios in those claims were typed, which is the same
class of defect as a typed figure (S-105): the colour constant can move and the
claim beside it goes on reading as though someone checked. This computes them.

    python3 contrast.py                       # the project palette
    python3 contrast.py "#6f6a64" "#ffffff"   # one pair

WCAG 2.1 thresholds: 4.5:1 for body text, 3:1 for large text (>= 24px, or
>= 19px bold) and for non-text objects that carry meaning (1.4.11).
"""
import sys


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcolor):
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def verdict(r, kind="text"):
    """kind 'decoration' carries no meaning on its own and has no threshold.

    It is not an excuse. A fill only qualifies when the same shape is also
    drawn as a line that does meet 1.4.11, which is why the FY2024 boundary in
    these graphics is stroked and not left to its tint.
    """
    if kind == "decoration":
        return "n/a  decorative; the stroked boundary carries the shape"
    need = 4.5 if kind == "text" else 3.0
    return ("PASS" if r >= need else "FAIL") + f" (needs {need}:1)"


def report(pairs, bg="#ffffff", out=print):
    """pairs: (name, hex, kind). kind is 'text', 'large' or 'object'."""
    worst = None
    for name, hexc, kind in pairs:
        r = ratio(hexc, bg)
        out(f"    {name:34} {hexc}  {r:6.2f}:1  {verdict(r, kind)}")
        if kind == "decoration":
            continue
        if worst is None or r < worst[1]:
            worst = (name, r)
    return worst


PALETTE = [
    ("INK, body and figures", "#1b1b1b", "text"),
    ("BLUE, headings and totals", "#17325c", "text"),
    ("MUT, secondary type", "#6f6a64", "text"),
    ("WARMD, decrement figures", "#6f4747", "text"),
    ("WARM, marker fill", "#8B5A5A", "object"),
    ("EDGE, marker outline", "#5c3a3a", "object"),
    ("GHOSTL, FY2024 boundary line", "#7d8fa3", "object"),
    ("GHOST, FY2024 fill", "#ccd6e1", "decoration"),
]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(f"{ratio(sys.argv[1], sys.argv[2]):.2f}:1")
    else:
        print("measured against #ffffff\n")
        report(PALETTE)
