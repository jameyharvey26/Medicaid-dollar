#!/usr/bin/env python3
"""gates.py — run every gate and check it against what it is supposed to say.

Replaces seven commands and a table of expected numbers written out in prose
in the session brief. The expectations live here, next to the thing they
describe, so they cannot quietly go stale in a document nobody updates.

This also enforces the older rule that a gate must be shown to have EXECUTED
rather than merely to have exited zero. Each gate below declares what its
output must contain; a gate that runs, exits clean and prints nothing fails
here, which is the failure mode that has caught us twice.

    python3 gates.py            run everything
    python3 gates.py --quick    skip the two render gates (~2 min faster)
    python3 gates.py --update   reprint the block to paste into EXPECT

A gate whose output has legitimately changed is a decision, not a nuisance.
Update EXPECT deliberately and say so in the manifest.
"""
import re
import subprocess
import sys

# What each gate must print. Substrings, checked in the combined output.
# Regexes where a count matters.
EXPECT = {
    "build.py": dict(
        # Two advisories are expected, both on the frozen list, and both are
        # pinned by their text rather than by a count — so a third appearing
        # fails here rather than hiding among the ones we already tolerate.
        must=["build complete.",
              "State Admin / Eligibility Rules sit 24 units apart",
              "Other reaches y=674, past Behavioral health's name at y=672"],
        regex=[(r"^\s+(?:NOTE|WARNING)\b", 2,
                "exactly the two frozen advisories")],
    ),
    "crossings.py": dict(
        must=["dc_2024", "national_2024", "national_2030_holds",
              "national_2030_mixed", "national_2030_scales"],
        regex=[(r"0 crossing\(s\) in the margin", 5, "five panels clean")],
        forbid=["ORPHAN"],
    ),
    "byteproof.py": dict(
        must=["seam is a no-op"],
        regex=[(r"IDENTICAL", 5, "five comparisons identical")],
    ),
    "prove.py": dict(
        must=["CONSERVES"],
        regex=[(r"\bCAUGHT\b", 10, "ten deliberate breaks caught")],
        forbid=["GATE IS BLIND", "WRONG"],
    ),
    "coverage.py national": dict(
        must=["21 verified", "2 modelled", "3 unverified", "3 missing"],
    ),
    "coverage.py dc": dict(
        must=["0 verified", "0 modelled", "15 unverified", "26 missing"],
    ),
    "render_v4_1.py": dict(
        must=["page 6", "page 9", "page 10", "page 15",
              "every subject named in prose appears in a figure on its own page"],
        slow=True,
    ),
}


def run(cmd):
    p = subprocess.run([sys.executable] + cmd.split(), capture_output=True,
                       text=True, timeout=1800)
    return p.stdout + p.stderr


def check(name, spec, out):
    fails = []
    for s in spec.get("must", []):
        if s not in out:
            fails.append(f"missing from output: {s!r}")
    for s in spec.get("forbid", []):
        if s in out:
            fails.append(f"present and should not be: {s!r}")
    for pat, n, why in spec.get("regex", []):
        got = len(re.findall(pat, out, re.M))
        if got != n:
            fails.append(f"{why}: expected {n}, got {got}")
    return fails


def main():
    quick = "--quick" in sys.argv
    width = max(len(k) for k in EXPECT)
    bad = []
    for name, spec in EXPECT.items():
        if quick and spec.get("slow"):
            print(f"{name:{width}}  skipped (--quick)")
            continue
        out = run(name)
        fails = check(name, spec, out)
        print(f"{name:{width}}  {'ok' if not fails else 'FAIL'}")
        for f in fails:
            print(f"{'':{width}}    {f}")
        if fails:
            bad.append(name)
    print()
    if bad:
        print(f"{len(bad)} gate(s) not as expected: {', '.join(bad)}")
        print("If the change was deliberate, update EXPECT in gates.py and "
              "record it in MANIFEST_SESSION.md.")
        sys.exit(1)
    print("all gates as expected" + (" (render gates skipped)" if quick else ""))


if __name__ == "__main__":
    main()
