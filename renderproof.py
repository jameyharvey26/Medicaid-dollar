#!/usr/bin/env python3
"""renderproof.py — no panel changes without somebody saying so.

Replaces byteproof.py, which proved that the Ledger path rendered identically
to the old instances.py path. That was migration scaffolding and it expired the
moment D-70 moved the national baseline: keeping it would have meant hand-
editing a second copy of every constant so it could agree with the first.

The question worth asking is not "does the new path match the old path" but
"did any panel change that nobody intended to change". The distinction matters
because of what the other gates do NOT cover:

    check      protects the arithmetic
    coverage   protects the provenance
    signatures protect a figure's value
    crossings  protects one named geometric fault

None of them protects the picture. A signature says a person agreed that
long-term care is $29.13. It says nothing about whether the label is still
attached to the right band, whether a terminal slid behind a column rule, or
whether a pie lost a slice. Those are eye failures, and the eye stops scaling
at about five panels. At fifty-three, eyeballing is sampling, not verification.

So: every panel the build emits is hashed and kept. Any panel whose bytes move
fails this gate by name, and a difference image with a bounding box is written
so the change can be looked at rather than guessed at. Blessing is deliberate
and carries a reason, exactly like a signature.

    python3 renderproof.py                    check every panel
    python3 renderproof.py --bless "reason"   accept what changed
    python3 renderproof.py --bless "reason" --only dc_2024
                                              accept one group, with its own
                                              reason, leaving the rest alone

Two things this cannot do, stated so nobody expects them. It tells you a panel
moved; it never tells you the movement was wrong. And it fires on every
intended change, so it belongs at session close rather than on every build —
a gate that people re-bless without looking is worse than no gate.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
RENDERS = ROOT / "reference_renders"
REGISTER = ROOT / "render_register"
INDEX = REGISTER / "index.json"
DIFFS = RENDERS / "diffs"


def panels():
    return sorted(p for p in RENDERS.glob("*.svg"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load():
    if not INDEX.exists():
        return {}
    return json.loads(INDEX.read_text())


def diff_image(name):
    """Rasterise the blessed panel and the current one and show where they
    differ. The bounding box is the point: it turns 'something moved' into
    'this moved, here'."""
    try:
        from PIL import Image, ImageChops
        import resvg_py
    except ImportError:
        return None
    old_svg, new_svg = REGISTER / f"{name}.svg", RENDERS / f"{name}.svg"
    if not old_svg.exists():
        return None
    DIFFS.mkdir(parents=True, exist_ok=True)
    pngs = []
    for tag, src in (("old", old_svg), ("new", new_svg)):
        out = DIFFS / f"_{name}_{tag}.png"
        out.write_bytes(bytes(resvg_py.svg_to_bytes(
            svg_string=src.read_text(), width=1400)))
        pngs.append(Image.open(out).convert("RGB"))
    a, b = pngs
    if a.size != b.size:
        return f"canvas resized {a.size} -> {b.size}"
    box = ImageChops.difference(a, b).getbbox()
    if box is None:
        return "bytes differ but the raster is identical (whitespace or ordering)"
    stack = Image.new("RGB", (a.width, a.height * 2 + 12), "white")
    stack.paste(a, (0, 0))
    stack.paste(b, (0, a.height + 12))
    out = DIFFS / f"{name}_diff.png"
    stack.save(out)
    for p in DIFFS.glob("_*.png"):
        p.unlink()
    return f"changed region x{box[0]}-{box[2]} y{box[1]}-{box[3]}  ->  {out.name}"


def check():
    reg = load()
    now = {p.stem: digest(p) for p in panels()}
    moved, new, gone = [], [], []
    for name, h in now.items():
        entry = reg.get(name)
        if entry is None:
            new.append(name)
        elif entry["sha"] != h:
            moved.append(name)
    for name in reg:
        if name not in now:
            gone.append(name)

    print(f"{len(now)} panel(s) emitted, {len(reg)} in the register\n")
    for name in sorted(now):
        if name in moved:
            note = diff_image(name)
            print(f"  MOVED      {name}")
            if note:
                print(f"             {note}")
        elif name in new:
            print(f"  NEW        {name}   (never blessed)")
        else:
            print(f"  unchanged  {name}")
    for name in sorted(gone):
        print(f"  MISSING    {name}   (blessed but no longer emitted)")

    bad = len(moved) + len(new) + len(gone)
    print()
    if not bad:
        print(f"every panel matches the register, blessed "
              f"{reg[next(iter(reg))]['blessed'] if reg else '-'}")
        print("no panel changed")
        return 0
    print(f"{bad} panel(s) not as blessed: "
          f"{len(moved)} moved, {len(new)} new, {len(gone)} missing")
    print("Look at the diffs. If every change was intended, re-bless with a "
          "reason:\n    python3 renderproof.py --bless \"why\"")
    return 1


def bless(reason, only=None):
    """Record the current panels as the ones to compare against.

    `only` blesses a subset whose stem contains that string, leaving every
    other entry in the register exactly as it was. Added 29 October, when
    nine panels moved for two unrelated reasons in one session: the DC data
    re-base and the 28 October term_y -> term_dy geometry refactor. Blessing
    all nine under one reason would have filed a false reason against six
    national panels, which is the opposite of what this register is for.
    One fact, one declaration (S-105) applies to blessings too.
    """
    if not reason.strip():
        print("a blessing needs a reason. Nothing written.")
        return 1
    stamp = subprocess.run(["date", "+%Y-%m-%d"], capture_output=True,
                           text=True).stdout.strip()
    REGISTER.mkdir(exist_ok=True)
    reg = load() if only else {}
    taking = [p for p in panels() if only is None or only in p.stem]
    if only and not taking:
        print(f"no emitted panel matches --only {only!r}. Nothing written.")
        return 1
    for p in taking:
        shutil.copy2(p, REGISTER / p.name)
        reg[p.stem] = dict(sha=digest(p), blessed=stamp, reason=reason)
    if only is None:
        for stale in REGISTER.glob("*.svg"):
            if stale.stem not in reg:
                stale.unlink()
    INDEX.write_text(json.dumps(reg, indent=2, sort_keys=True) + "\n")
    if DIFFS.exists() and only is None:
        shutil.rmtree(DIFFS)
    print(f"blessed {len(taking)} panel(s) at {stamp}"
          + (f", matching {only!r}" if only else ""))
    print(f"reason: {reason}")
    for p in taking:
        print(f"   {p.stem}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--bless":
        argv = sys.argv[2:]
        only = None
        if "--only" in argv:
            i = argv.index("--only")
            only = argv[i + 1] if i + 1 < len(argv) else ""
            del argv[i:i + 2]
            if not only:
                print("--only needs a panel name or a fragment of one.")
                sys.exit(1)
        sys.exit(bless(" ".join(argv), only))
    sys.exit(check())
