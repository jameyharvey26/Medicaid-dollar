# teachingproof.py — nothing the diagram teaches disappears without somebody
# saying so.
#
# WHY THIS EXISTS. The panels carry two kinds of content. The figures, which
# the ledger owns and `prove.py` already defends, and the SENTENCES, which
# until now only `sankey.py` owned: the column sub-labels that name what a
# column does, the reach clause on every HR-1 bite, the disclaimers that stop
# a reader misreading a band. 155 text elements on the FY2030 national panel,
# of which 30 are prose. None of it is in the ledger, so a second renderer
# loses it silently and the panel still looks finished.
#
# JW, 8 October, on the refactor to one engine: "the spike has lost a lot of
# information that was in the diagrams that I don't want to lose."
#
# WHAT IT DOES. Extracts every text string the Python renderer emits, panel by
# panel, and checks each one against a register that says what has happened to
# it. Three verdicts, and every string must carry one:
#
#   ported   the engine emits this string too
#   pending  it has not been ported yet — the burndown
#   layout   it is not a string to copy but placement behaviour (a leader, a
#            halo, a collision rule) and porting it means porting the rule
#
# A string the register has never seen FAILS. That is the whole point: new
# teaching added to sankey.py during the refactor cannot quietly go unported,
# and teaching deleted from sankey.py cannot quietly go unmissed.
#
# This gate does not read the engine yet. It cannot: the engine is a spike in
# a browser and there is no headless render of it in the build. When there is,
# `_engine_texts` stops returning None and the `ported` verdicts start being
# checked rather than trusted. Until then this is a register gate, and it is
# honest about that in its own output.

import json
import os
import re
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(REPO, "teaching_register.json")

# Where build.py leaves the composed panels. Same files renderproof.py reads.
PANELS = {
    "national_2024": "nat/national_2024_combined.svg",
    "national_2030_mixed": "nat/national_2030_mixed_combined.svg",
    "national_2030_holds": "nat/national_2030_holds_combined.svg",
    "national_2030_scales": "nat/national_2030_scales_combined.svg",
    "dc_2024": "nat/dc_2024_combined.svg",
}

VERDICTS = ("ported", "pending", "layout")


def _root():
    """Where build.py actually writes the panels.

    This read dirname(REPO), which is only build.py's OUT when the repo happens
    to sit at a particular path. On a clean clone checked out anywhere else the
    gate reported every panel MISSING and told the user to run build.py, which
    they had just run. Read the declaration instead of assuming it.
    """
    try:
        with open(os.path.join(REPO, "build.py"), encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r'\s*OUT\s*=\s*["\'](.+?)["\']', line)
                if m:
                    return os.path.dirname(m.group(1))
    except OSError:
        pass
    return os.path.dirname(REPO)


def panel_texts(path):
    """Every string the panel puts in front of a reader, in document order.

    Normalised only for whitespace and entities — NOT for case or punctuation.
    'Wrap around services*' and 'Wrap around services' are different strings
    and the asterisk is a footnote marker that means something.
    """
    with open(path, encoding="utf-8") as fh:
        svg = fh.read()
    out, seen = [], set()
    for raw in re.findall(r"<text[^>]*>(.*?)</text>", svg, re.S):
        t = re.sub(r"<[^>]+>", "", raw)
        t = (t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
              .replace("&#8722;", "\u2212").replace("&#183;", "\u00b7"))
        t = " ".join(t.split())
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def classify(t):
    """What kind of teaching this is, for the burndown breakdown."""
    if "$" in t:
        return "figure"
    if len(t) > 18:
        return "prose"
    return "label"


ENGINE_TEXTS = os.path.join(REPO, "engine_texts.json")
_ENGINE_CACHE = {}


def _engine_texts(panel):
    """The engine's strings for the same panel, from `engine_texts.py`.

    Returns None for a panel the engine has not been pointed at yet — which is
    not the same as the engine emitting nothing, and the gate reports the two
    differently. A panel absent from the dump leaves its `ported` verdicts
    declared; a panel present has every one of them measured.
    """
    if not _ENGINE_CACHE:
        if not os.path.exists(ENGINE_TEXTS):
            _ENGINE_CACHE["__none__"] = True
            return None
        with open(ENGINE_TEXTS, encoding="utf-8") as fh:
            _ENGINE_CACHE.update(json.load(fh))
    texts = _ENGINE_CACHE.get(panel)
    return texts if texts is not None else None


def _emits(engine, t):
    """Does the engine put this string in front of a reader?

    Not a set membership test, because the two renderers break text into
    elements differently and the reader cannot see element boundaries.
    sankey.py draws "Federal  $65.29" as one <text>; the engine draws "Federal"
    and "$65.29" as two, side by side. Same sentence on the page, and a gate
    that called that a loss would fire on every label and be ignored within a
    week — which is worse than no gate.

    So the comparison is made against the panel's reading surface: every string
    in document order, joined. A register string counts as emitted when it
    appears there. This is deliberately generous about WHERE the words are, and
    that generosity is the gap `crossings.py` and the eye still have to cover.

    THE GENEROSITY IS SCOPED, AND HERE IS WHY. Surface matching is safe for a
    string carrying words, because "Dual MCO capitation $9.99" appearing
    anywhere on the panel is almost certainly the band it names. It is close to
    meaningless for a string that is ONLY a figure. "$26.25" matches wherever
    $26.25 lands, and it caught us: the paper draws it as the long-term-care
    pie total, the engine draws it as the long-term-care service band, same
    number attached to a different object, and the surface test called that
    ported. Its own loss bar "-$2.89" was correctly caught as missing in the
    same breath, which is how we noticed.

    A bare figure therefore has to match an element exactly. That costs about a
    dozen strings off the ported count and is the difference between a number
    that means something and one that flatters us.
    """
    norm = " ".join(t.split())
    if not re.search(r"[A-Za-z]", norm):
        # Nothing but a figure: no content to tie it to a position, so demand
        # that the engine emits it as its own element.
        return norm in {" ".join(s.split()) for s in engine}
    return norm in " ".join(engine)


def load_register():
    if not os.path.exists(REGISTER):
        return {}
    with open(REGISTER, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    reg = load_register()
    root = _root()
    missing_file = []
    unclassified = []
    totals = {v: 0 for v in VERDICTS}
    by_kind = {}
    checked_engine = False
    measured = set()

    for panel, rel in PANELS.items():
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            missing_file.append(panel)
            continue

        texts = panel_texts(path)
        entries = reg.get(panel, {})
        eng = _engine_texts(panel)
        if eng is not None:
            checked_engine = True
            measured.add(panel)

        for t in texts:
            verdict = entries.get(t)
            if verdict not in VERDICTS:
                unclassified.append((panel, t))
                continue
            totals[verdict] += 1
            kind = classify(t)
            by_kind.setdefault(kind, {v: 0 for v in VERDICTS})
            by_kind[kind][verdict] += 1
            if verdict == "ported" and eng is not None and not _emits(eng, t):
                unclassified.append((panel, t + "  [claimed ported, engine does not emit it]"))

        gone = [t for t in entries if t not in texts]
        for t in gone:
            unclassified.append((panel, t + "  [in the register, no longer drawn]"))

        print("%-22s %4d strings" % (panel, len(texts)))

    if missing_file:
        print()
        for p in missing_file:
            print("  MISSING  %s  run python3 build.py" % p)
        return 1

    print()
    for kind in ("figure", "label", "prose"):
        row = by_kind.get(kind, {v: 0 for v in VERDICTS})
        tot = sum(row.values())
        print("  %-7s ported %3d  pending %3d  layout %3d  of %3d"
              % (kind, row["ported"], row["pending"], row["layout"], tot))

    total = sum(totals.values())
    print()
    print("  every teaching string is classified")
    print("  ported %d of %d, %d pending, %d layout"
          % (totals["ported"], total, totals["pending"], totals["layout"]))
    if measured:
        print("  measured against the engine: %s" % ", ".join(sorted(measured)))
    unmeasured = [p for p in PANELS if p not in measured and p not in missing_file]
    if unmeasured:
        print("  DECLARED ONLY, engine has not been pointed at these: %s"
              % ", ".join(sorted(unmeasured)))
    if not checked_engine:
        print("  REGISTER ONLY: no headless engine render at all, so every "
              "'ported' is declared and not measured")

    if unclassified:
        print()
        print("  %d string(s) the register does not account for:" % len(unclassified))
        for panel, t in unclassified[:40]:
            print("    %-22s %s" % (panel, t[:96]))
        if len(unclassified) > 40:
            print("    ... and %d more" % (len(unclassified) - 40))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
