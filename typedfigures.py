"""Hard-coded outputs: numbers typed into prose that the code already computes.

A basis line, a note, a comment or a caption that quotes a figure the ledger
derives is a second declaration of that figure. It does not participate in the
build, so nothing makes it move when the figure moves, and it goes quietly
wrong. `signatures.py` catches a signed figure that changed; `check` catches a
ledger that does not balance; neither sees a stale number sitting inside a
string.

This reports every numeric literal inside a string or comment in the Python
sources that equals a value the ledger computes, to two or four decimal places.
It is a reporting instrument, not a gate: a match is not automatically a fault.
Some are correct and deliberate — a note that says what a figure IS, in the same
breath as declaring it. The question to ask of each one is whether it would
still be right if the figure moved. If the answer is no, make it an f-string.

    python3 typedfigures.py            report everything
    python3 typedfigures.py --strict   exit 1 if anything is found

Convention adopted 2026-09-19, JW: derive in code, do not type an output.
"""
import ast
import glob
import os
import re
import sys

SKIP = {"typedfigures.py"}
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})*|\d+)\.(\d{2,4})(?![\w])")

# Values that are not worth reporting: years, section numbers, common integers,
# and anything trivially small. Matching is on the two- or four-decimal string,
# so these are string prefixes of the whole literal.
IGNORE_EXACT = {"0.00", "1.00", "100.00", "0.0000", "1.0000"}

# An opacity or a stroke width that happens to equal a ledger figure is a
# coincidence, and there are enough of them to bury the real ones.
DRAWING = re.compile(r"(opacity|stroke-width|stroke-dasharray|font-size|"
                     r"[xy]\d?|width|height|offset|r)\s*=\s*.?$")


def ledger_values():
    """Every figure the three ledgers derive, keyed by its printed forms."""
    import ledger_national_2024 as N24
    import ledger_national_2030 as N30
    import ledger_dc_2024 as DC

    out = {}

    def take(tag, L):
        figs = L.figures()
        for key, fig in figs.items():
            v = fig.value
            if not isinstance(v, (int, float)):
                continue
            for dp in (2, 4):
                out.setdefault(f"{v:.{dp}f}", set()).add(f"{tag}:{key}")
        # the tracker anchors are derived downstream of the figures and are
        # quoted in prose more often than anything else
        enters = sum(s.value for s in L.sources.values())
        out.setdefault(f"{enters:.2f}", set()).add(f"{tag}:enters")
        out.setdefault(f"{enters:.4f}", set()).add(f"{tag}:enters")

    take("nat24", N24.build())
    take("nat30", N30.build())
    take("dc24", DC.build())
    return out


def literals(path):
    """(lineno, text) for every string literal and every comment in a file."""
    src = open(path, encoding="utf-8").read()
    found = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return found
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            found.append((node.lineno, node.value))
    for i, line in enumerate(src.split("\n"), 1):
        if "#" in line:
            found.append((i, line[line.index("#"):]))
    return found


def main():
    strict = "--strict" in sys.argv
    values = ledger_values()
    hits = []
    for path in sorted(glob.glob("*.py")):
        if os.path.basename(path) in SKIP:
            continue
        for lineno, text in literals(path):
            for m in NUM.finditer(text):
                lit = m.group(0).replace(",", "")
                if lit in IGNORE_EXACT:
                    continue
                if DRAWING.search(text[max(0, m.start() - 24):m.start()]):
                    continue
                if lit in values:
                    ctx = text.strip().replace("\n", " ")
                    if len(ctx) > 64:
                        start = max(0, m.start() - 26)
                        ctx = "…" + ctx[start:start + 62] + "…"
                    hits.append((path, lineno, m.group(0),
                                 sorted(values[lit])[:2], ctx))

    if not hits:
        print("no typed outputs found")
        return 0

    width = max(len(h[0]) for h in hits)
    for path, lineno, lit, who, ctx in hits:
        print(f"{path:{width}}:{lineno:<5} {lit:>10}  {', '.join(who)}")
        print(f"{'':{width}} {'':<5} {ctx}")
    print(f"\n{len(hits)} typed figure(s) that the code also computes.")
    print("A match is not a fault. Ask of each: would it still be right if the")
    print("figure moved? If not, make it an f-string.")
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main())
