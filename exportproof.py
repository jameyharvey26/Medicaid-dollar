#!/usr/bin/env python3
"""exportproof.py — the engine carries no declaration of its own.

`engine/explorer_engine.html` inlines two declarations, `const GEOM` and
`const DATA`, because it runs from file:// where fetching a sibling JSON is
blocked. Both are written by exporters and neither is edited by hand.

That rule needs a gate or it is a comment. Both lines WERE maintained by hand,
and the consequence was not cosmetic: the spine had drifted from
`instances.T_SLOT` in three of seven tracker slots and carried a PROVIDERS slot
the lattice does not have, which is what sent a tributary downstream into the
fan and made it cross. Every crossing chased that day looked like a defect in
the row solver and none of them was. Meanwhile nothing carried a ledger figure
to the engine at all, so a number the paper draws could not be drawn here.

This re-runs both exporters against a copy and compares. It never writes to the
engine, so a red gate leaves the tree exactly as it found it.

    python3 exportproof.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(REPO, "engine", "explorer_engine.html")

LINES = {
    "GEOM": (re.compile(r"^const GEOM = (.*);$", re.M), "geometry_export.py"),
    "DATA": (re.compile(r"^const DATA = (.*);$", re.M), "engine_data_export.py"),
}


def declared(src, name):
    m = LINES[name][0].search(src)
    if not m:
        raise SystemExit("exportproof: no `const %s = ...;` line in the engine. "
                         "The exporters replace that line, so it has to stay on "
                         "one line and keep its name." % name)
    return json.loads(m.group(1))


def main():
    live = open(ENGINE).read()
    work = tempfile.mkdtemp(prefix="exportproof-")
    try:
        # the exporters write in place, so they run against a copy of the tree's
        # engine and the real one is never touched by this gate
        shutil.copy(ENGINE, os.path.join(work, "explorer_engine.html"))
        env = dict(os.environ, EXPORTPROOF_ENGINE=os.path.join(work, "explorer_engine.html"))
        stale = []
        for name, (_rx, script) in LINES.items():
            r = subprocess.run([sys.executable, os.path.join(REPO, script)],
                               cwd=REPO, env=env, capture_output=True, text=True)
            if r.returncode:
                print("  %-22s FAILED TO RUN" % script)
                print("      " + (r.stderr.strip().splitlines() or ["(no output)"])[-1])
                stale.append(name)
                continue
            fresh = declared(open(os.path.join(work, "explorer_engine.html")).read(), name)
            if fresh == declared(live, name):
                print("  %-22s %s matches" % (script, name))
            else:
                print("  %-22s %s IS STALE" % (script, name))
                for where in difference(declared(live, name), fresh):
                    print("      " + where)
                stale.append(name)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    if stale:
        print("  the engine's %s no longer matches what the ledgers and the "
              "spine say" % " and ".join(stale))
        print("  run the exporter rather than editing the engine")
        return 1
    print("  the engine declares nothing of its own")
    return 0


def difference(a, b, path="", out=None):
    """Where two declarations disagree, in words, shallowest first."""
    out = [] if out is None else out
    if len(out) >= 8:
        return out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append("%s/%s only in the export" % (path, k))
            elif k not in b:
                out.append("%s/%s only in the engine" % (path, k))
            else:
                difference(a[k], b[k], "%s/%s" % (path, k), out)
    elif a != b:
        out.append("%s: engine %r, export %r" % (path or "/", a, b))
    return out


if __name__ == "__main__":
    sys.exit(main())
