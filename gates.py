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
        # Three advisories are expected, all on the frozen list, and all pinned
        # by their text rather than by a count — so a fourth appearing fails
        # here rather than hiding among the ones we already tolerate.
        #
        # The third, the Vaccines / Provider Tax pair at four units apart, is
        # GONE as of D-115 and must stay gone. It was tolerated on 2026-09-18
        # as "the geometry telling the truth", which it was not: where a
        # tributary leaves the federal stream is arbitrary, and the bite was
        # simply declared too close. Moving it cost nothing and the markers no
        # longer stack. An advisory that turns out to be movable is a defect
        # that was being lived with.
        # S-106, JW 25 September. Pinned by count, not by presence: a panel
        # that silently stopped reporting would otherwise pass. Three panels
        # run under `build.py`; the two sensitivity variants are checked when
        # `build.py sensitivity` runs.
        must=["build complete.",
              "State Admin / Eligibility Rules sit 24 units apart",
              "Other reaches y=674, past Behavioral health's name at y=673"],
        forbid=["Vaccines / Provider Tax"],
        regex=[(r"^\s+(?:NOTE|WARNING)\b", 2,
                "exactly the two frozen advisories"),
               (r"tracker line adds up as printed", 3,
                "every panel's tracker line reconciles on its printed figures")],
    ),
    # FALSE GREEN, 27 September. This suite runs build.py, which renders the
    # FY2030 mixed panel only; the two sensitivity variants are behind
    # `build.py sensitivity` and nothing ran it. renderproof.py compares the
    # SVGs ON DISK, so the stale variant files went on matching their stale
    # blessing and reported "unchanged" indefinitely. They had in fact been
    # wrong since D-91: both still drew the beneficiary panel with four
    # eligibility groups (Children / Adults / Disabled / Aged) against the
    # paper's five. A gate that never rebuilds a panel cannot see it move.
    "build.py sensitivity": dict(
        must=["build complete."],
        slow=True,
    ),
    # ORDERING DEFECT, 8 October. crossings.py sat second, above the gate that
    # draws two of the five panels it measures. On a clean clone it reported
    # three clean and two MISSING and the suite read it as a content failure.
    # Same class as the renderproof defect below, and the same fix: build the
    # panel before measuring it.
    "crossings.py": dict(
        must=["dc_2024", "national_2024", "national_2030_holds",
              "national_2030_mixed", "national_2030_scales"],
        regex=[(r"0 crossing\(s\) in the margin", 5, "five panels clean")],
        forbid=["ORPHAN"],
    ),
    # ORDERING DEFECT, 7 October. The FALSE GREEN fix above added
    # `build.py sensitivity` as a gate but placed it BELOW renderproof.py,
    # which is the gate that depends on it. renderproof reads the SVGs on
    # disk; on a clean clone those are the committed reference_renders files,
    # which are stale, so six national panels reported MOVED and the suite
    # accused the national model of drifting when nothing had drifted. On a
    # warm working copy a previous session had left fresh files and it went
    # green, which is why it was only ever seen on a fresh clone. Rebuilding
    # a panel must precede proving it has not moved.
    "renderproof.py": dict(
        # Replaces byteproof.py, whose premise expired with D-70. That gate
        # proved the Ledger path matched the old instances.py path — migration
        # scaffolding. This one proves no panel changed without somebody
        # saying so, which is the question that survives to fifty states.
        must=["no panel changed"],
        forbid=["MOVED", "NEW", "MISSING"],
    ),
    "prove.py": dict(
        must=["CONSERVES"],
        regex=[(r"\bCAUGHT\b", 10, "ten deliberate breaks caught")],
        forbid=["GATE IS BLIND", "WRONG"],
    ),
    "coverage.py national": dict(
        # Re-signed 25 September on reference_renders/sign_2026-09-25.png.
        # Three figures moved from verified to modelled and not by anyone's
        # choice: the three payer lanes now carry a collections fold whose
        # pro-rata key is ours, so MEASURED would overstate what Exhibit 17
        # actually says. The count going DOWN is the honest direction here.
        must=["22 verified", "5 modelled", "2 unverified", "3 missing"],
    ),
    "coverage.py dc": dict(
        must=["0 verified", "0 modelled", "15 unverified", "26 missing"],
    ),
    # ORDERING DEFECT, 27 September. This suite ran build.py and then went
    # straight to render_v7_1.py, whose figurefit and artwhite sub-gates read
    # paper_figs/crops.json and the generated PNGs. On a clean clone those do
    # not exist, figurefit died on a FileNotFoundError, and four of the six
    # reported misses were the suite failing to build its own inputs while
    # reporting a content failure. A detector that misfires gets fixed rather
    # than worked around: the generation steps are gates now, in order.
    "make_figs.py": dict(
        must=["wrote crops.json"],
    ),
    "deckalts.py": dict(
        must=["wrote alt1_governing_number_bare"],
        slow=True,
    ),
    # D-105. The explorer is built from the ledger like everything else, and
    # proved like everything else. build_explorer.py has to run first: the
    # proof renders the built page rather than reading the template, because
    # the failure it exists to catch is arithmetic in the page's own script,
    # which no static read can see.
    # ORDERING DEFECT, 8 October. render_v8_0.py writes the paper PDF into the
    # repo and build_explorer.py embeds page 1 of it, so the renderer has to
    # run first. It was last in the suite. build_explorer.py also read the
    # copy in the outputs directory, which only publish.py writes and which
    # requires the built explorer in turn — a cycle no ordering could satisfy.
    # Fixed in build_explorer.py to read the repo copy. The paper's own layout
    # gates stay honestly red; that is D-107 and not this.
    "render_v8_0.py": dict(
        # 2026-09-26b, D-93. This gate is RED and is expected to be red.
        #
        # whitespace.py has been blind since it was written. The provenance
        # footer was `position:fixed; bottom:4mm`, which in a paged context
        # positions against the CONTENT box, so the footer printed inside the
        # column and was the lowest text block on every page. dead_space()
        # measured from it and returned about one line on every page of every
        # draft this project has ever rendered - cover, plates and section ends
        # alike, which is impossible. Every green this gate printed was the
        # footer, not the text.
        #
        # D-93 moved the footer out of the flow into a reserved band in the
        # bottom margin, which fixed the collisions JW reported on pages 4, 6
        # and 8 and incidentally uncovered the blindness. The detector now sees
        # the text and reports six real strandings that were always there. JW
        # is fixing them by hand. Do not re-green this by loosening the
        # threshold.
        # Both layout gates clean as of 2026-09-26. The four remaining
        # strandings closed with the 09-25 reflow and this EXPECT was never
        # updated to match, which is why the gate read FAIL for a reason that
        # had already been fixed.
        #
        # The three page/subject mismatches closed the same day, and not by
        # moving anything: render_v6_1.py (then v6_0) wrote its HTML to a temp directory,
        # so every relative figure path resolved to nothing and Chromium
        # printed a paper of broken image icons. The PDF was 192 kB. It is
        # 3.1 MB now. figurefit was reading real captions against a document
        # with no pictures in it.
        # The expectation is NOT relaxed to make this green. It reads FAIL
        # until the six strandings are closed in the prose.
        must=["no body page strands more than 6 lines in a column",
              "every subject named in prose appears in a figure on its own page",
              "no body text within 6pt of the footer",
              "every section opens a page",
              "no generated figure carries more than",
              "every leader lands where the rule says"],
        forbid=["mismatch(es)"],
        slow=True,
    ),
    "build_explorer.py": dict(
        must=["medicaid_dollar_explorer.html", "explorer_data.json"],
        slow=True,
    ),
    # D-118, JW 8 October. The refactor to one engine moves the drawing into
    # the browser, and the thing most easily lost in that move is not a figure
    # — prove.py defends those — but a SENTENCE. 591 strings across five
    # panels, of which 400 are the labels and prose that tell a reader what a
    # band means. None of it lives in the ledger, so a second renderer drops
    # it silently and the panel still looks finished. This gate pins every
    # string to a verdict and fails on any string nobody has classified.
    # UPDATED 8 October, same session. The engine now renders headless via
    # engine_texts.py, so `ported` is measured on the two panels the engine
    # draws and still only declared on the other three — the gate names which
    # is which rather than averaging them into one number. Measuring it the
    # first time demoted 25 strings from ported to pending, including the pie
    # key and every per-service loss bar, which had been claimed on the
    # strength of the spike looking finished.
    #
    # A large `pending` count is expected for the whole refactor; that is the
    # burndown, not a fault. Failure means a string nobody has classified, or
    # a string claimed ported that is not on the engine's reading surface.
    "engine_texts.py": dict(
        must=["wrote engine_texts.json"],
        slow=True,
    ),
    "teachingproof.py": dict(
        must=["every teaching string is classified",
              "measured against the engine"],
        regex=[(r"ported \d+ of \d+, \d+ pending", 1, "the burndown reports")],
        forbid=["the register does not account for"],
    ),
    "explorerchrome.py": dict(
        # JW, 27 September: new chrome only. palette.py is not measured here
        # and the sankey and paper palettes are not to be changed.
        must=["meet WCAG 2.1 AA, measured not asserted"],
        forbid=["UNMEASURED"],
    ),
    # D-107. All three artifacts take one version, from release.VERSION, and
    # this builds every one of them HTML and PDF. It runs the paper renderer
    # itself, whose layout gates are honestly red; publish.py reports those
    # and writes the artifact anyway, because the alternative is that the only
    # way to ship is to green a detector that is telling the truth.
    "publish.py": dict(
        must=["Medicaid_Dollars_National_v", "MHPA_Board_Deck_v",
              "medicaid_dollar_explorer_v"],
        regex=[(r"_v\d+\.\d+\.(?:html|pdf)", 5, "five artifacts at one "
                "version: paper HTML and PDF, deck HTML and PDF, explorer HTML")],
        slow=True,
    ),
    "explorerproof.py": dict(
        must=["every figure on screen is one the ledger serialized",
              "no dollar literal in the template"],
        regex=[(r"swept \d+ page states", 1,
                "every year, variant, lever and cumulative selection swept")],
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
