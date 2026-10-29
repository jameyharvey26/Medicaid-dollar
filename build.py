#!/usr/bin/env python3
"""build.py — render every artifact from one renderer.

Replaces build_sankey.py (script) and build_tobe_2030.py (text-substitution
fork). One renderer in sankey.py, one config per artifact in instances.py.

Usage:  python3 build.py            # everything
        python3 build.py 2024       # one instance
"""
import os, re, shutil, subprocess, sys

import sankey
import instances
import ledger as LD
import views
from compose import compose
from check import gate
from tobe2030 import per100
from ledger_2030 import ledger
import incidence

REPO = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(REPO, "reference_renders")
OUT = os.path.join(REPO, "build_out", "nat")


def wrap(body):
    return (f'<svg viewBox="0 0 {sankey.W} {sankey.H}" width="100%" '
            f'xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>')


def emit(tag, base, over):
    os.makedirs(OUT, exist_ok=True); os.makedirs(REF, exist_ok=True)
    b = '<g id="baseline">\n' + "\n".join(base) + "\n</g>"
    o = '<g id="overlay-hr1">\n' + "\n".join(over) + "\n</g>"
    files = [(f"{tag}_combined", wrap(b + "\n" + o)),
             (f"{tag}_baseline", wrap(b + '\n<g id="overlay-hr1" display="none">\n</g>')),
             (f"{tag}_overlay",  wrap('<g id="baseline" display="none">\n</g>\n' + o))]
    vbs = set()
    for name, doc in files:
        p = os.path.join(OUT, name + ".svg")
        open(p, "w").write(doc)
        vbs.add(re.search(r'viewBox="([^"]+)"', doc).group(1))
        print(f"  svg  {name}.svg  ({len(doc):,} bytes)")
    assert len(vbs) == 1, f"viewBox drift: {vbs}"
    print(f"  ok   viewBox identical across all three: {vbs.pop()}")
    # resvg only, hard-pinned. cairosvg ignores paint-order and erodes the halos.
    import resvg_py
    for name in (f"{tag}_combined",):
        svg = open(os.path.join(OUT, name + ".svg")).read()
        png = resvg_py.svg_to_bytes(svg_string=svg, width=2600)
        open(os.path.join(OUT, name + ".png"), "wb").write(bytes(png))
        print(f"  png  {name}.png  (2600px, resvg)")
    for name, _ in files:
        for ext in (".svg", ".png"):
            src = os.path.join(OUT, name + ext)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(REF, name + ext))


def build_2024():
    # Two gates, and they assert different things. LD.gate is the conserved
    # ledger with its provenance; gate() is the Instance the renderer receives.
    # ARCHITECTURE 2: build.py refuses to emit a ledger that does not balance.
    import ledger_national_2024 as NAT
    L = NAT.build()
    LD.gate(L, "FY2024 as-is ledger")
    cfg = compose(L, views.V_NAT)
    gate(cfg, 'FY2024 as-is')
    base, over = sankey.render(cfg)
    emit("national_2024", base, over)
    # One render, one name. `national_baseline.png` was an alias of this file
    # under its pre-refactor name; sheet.py now asks for the real one. Aliases
    # are how a PNG and its SVG came to disagree about which build they were
    # from, which is a defect the crossing gate cannot see through.


def build_dc():
    # D-109, JW approved 27 September. legacy_mix is OFF.
    #
    # The flag existed because the renderer could not draw a panel without a
    # service allocation — compose() raised KeyError on the first node — so
    # the only way to get a DC panel at all was to fill the fan from the
    # national mix. That made the flag "the visible record that DC is still
    # carrying the national service mix", which was honest about the choice
    # and did nothing about the artifact: the drawing still asserted five DC
    # service figures this ledger has withdrawn, and a reader had no way to
    # know. The explorer would have republished them on the web.
    #
    # compose() now truncates a panel whose fan cannot be drawn, and the
    # drawing says so where the fan would have been. The panel stops where the
    # knowledge stops. When DC's service allocation is acquired, this reverts
    # to a full panel with no code change — the predicate reads the matrix.
    import ledger_dc_2024 as DC
    # The assumed national mix, JW 2026-10-29. D-109 withdrew it on
    # 27 September; it is back as a declared assumption for the demo, with the
    # DC data stipulated as not proofread. It is NOT legacy_mix: that path
    # also folds retention into plan administration and zeroes margin, which
    # would throw away the CY2024 administration and margin work.
    L = DC.build(legacy_mix=False, assumed_mix=True)
    LD.gate(L, "DC FY2024 as-is ledger")
    cfg = compose(L, views.V_DC)
    gate(cfg, "DC FY2024 as-is")
    base, over = sankey.render(cfg)
    emit("dc_2024", base, over)


DRAFTS = "drafts"


def emit_draft(tag, base, over):
    """Render a draft panel outside the blessed register."""
    import resvg_py
    os.makedirs(DRAFTS, exist_ok=True)
    body = ('<g id="baseline">\n' + "\n".join(base) + "\n</g>\n"
            '<g id="overlay-hr1">\n' + "\n".join(over) + "\n</g>")
    # A declarations band is laid out at render time and the canvas grows by
    # what it actually used. wrap() is for register panels, whose height is
    # fixed on purpose; a draft may be as tall as it needs to be.
    extra = getattr(sankey, "EXTRA_H", 0.0)
    if extra:
        doc = (f'<svg viewBox="0 0 {sankey.W} {sankey.H + extra:.0f}" '
               f'width="100%" xmlns="http://www.w3.org/2000/svg">\n'
               f'<rect width="{sankey.W}" height="{sankey.H + extra:.0f}" '
               f'fill="#ffffff"/>\n{body}\n</svg>')
    else:
        doc = wrap(body)
    svg_p = os.path.join(DRAFTS, tag + ".svg")
    open(svg_p, "w").write(doc)
    png = resvg_py.svg_to_bytes(svg_string=doc, width=2600)
    open(os.path.join(DRAFTS, tag + ".png"), "wb").write(bytes(png))
    print(f"  draft  {svg_p} and {tag}.png  (not blessed, not compared)")


def build_dc_2030():
    """The DC FY2030 to-be panel. DRAFT.

    Added 2026-10-29. The view has existed since the DC 2030 ledger was stood
    up; nothing built it, because with one lever of seven derived there was
    nothing to look at. With four derived there is.

    It does NOT go in the render register yet. A panel carrying three violet
    placeholders is for looking at, not for blessing, and placeholder.py
    refuses to let it ship. Blessing it would pin an unfinished picture as the
    thing every later render is compared against.
    """
    import ledger_dc_2024 as DC
    import ledger_dc_2030 as DC30
    L = DC30.ledger()

    # THE CONSERVING GATE CANNOT PASS AND SHOULD NOT. Three of the seven HR-1
    # lanes carry no figure, so disbursed cannot be struck and the lanes
    # cannot be summed against it. That is the panel's whole point: it says
    # what it does not know. Forcing LD.gate green would mean giving the three
    # absent lanes a value, which is the substitution this edition exists to
    # refuse.
    #
    # So the faults are PINNED to their exact extent, per JW's rule of
    # 27 October: the check still runs, and anything beyond this list — or
    # anything that disappears from it — fails the build. Acquiring one of the
    # three levers will trip this deliberately, and that is the signal to
    # re-pin and, when the last one lands, to go back to LD.gate.
    # 29 October PM: with every lever carrying a figure and the service fan
    # carried forward, the pinned faults are GONE and this ledger conserves
    # like any other. So it goes back to LD.gate, which is what the pin
    # always said should happen when the last one landed.
    #
    # With assumed_levers OFF the panel returns to declared absence and the
    # faults return with it, so the pinned set is kept for that path rather
    # than deleted. Two routes, each gated on its own terms; neither can
    # quietly become the other.
    if DC30.assumed_levers():
        LD.gate(L, "DC FY2030 to-be ledger [assumed levers]")
    else:
        EXPECTED = {
            "disbursed cannot be struck",
            "payer lanes sum to disbursed",
            "claims matrix: row mco has no margin",
            "claims matrix: row dual has no margin",
            "claims matrix: row ffs has no margin",
            "claims cannot be summed",
        }
        seen = LD.check(L)
        unpinned = [x for x in seen
                    if not any(x.startswith(e) for e in EXPECTED)]
        if unpinned:
            raise LD.LedgerError(
                "DC FY2030 to-be ledger has faults beyond the pinned set:\n  "
                + "\n  ".join(unpinned))

    # NO PRIOR. The national to-be panel passes its FY2024 ledger so the
    # drawing can show where each node sat before. DC cannot: its FY2024
    # service allocation is withdrawn (legacy_mix=False), so there are no
    # prior node margins to compare against. Passing the as-is ledger anyway
    # fails on the first node it reads, which is the right behaviour — the
    # comparison does not exist and is not drawn.
    cfg = compose(L, views.V_DC_2030)
    gate(cfg, "DC FY2030 to-be")
    base, over = sankey.render(cfg)
    # NOT through emit(). emit() copies into reference_renders, which is the
    # blessed register, and a draft panel there reads as a NEW panel to
    # renderproof and as an ORPHAN to crossings — which is exactly what it
    # did the first time this ran. A draft is for looking at. It goes to
    # drafts/ and nothing compares it to anything.
    emit_draft("dc_2030_draft", base, over)


def build_2030(variant="mixed"):
    # Through the seam, as the two as-is panels are. Three gates and they
    # assert different things: LD.gate is the conserved ledger with its
    # provenance, agreement() is the reach declared here against the reach
    # outflows draws with, and gate() is the Instance the renderer receives.
    import ledger_national_2024 as NAT
    import ledger_national_2030 as N30
    drift = N30.agreement()
    if drift:
        raise LD.LedgerError("HR-1 reach is declared in the ledger and in "
                             "outflows and they disagree:\n  "
                             + "\n  ".join(drift))
    # D-104. And the fourth: every HR-1 peel is either allocated by the
    # incidence model or declared outside it. An unallocated provision does
    # not fail any of the three above, because its dollars are absorbed by
    # the others and the cube still conserves.
    gaps = incidence.coverage()
    if gaps:
        raise LD.LedgerError("HR-1 provisions the incidence model neither "
                             "allocates nor excludes:\n  " + "\n  ".join(gaps))
    L = N30.build(variant)
    LD.gate(L, f"FY2030 to-be ledger [{variant}]")
    cfg = compose(L, views.V_2030, prior=NAT.build())
    gate(cfg, f'FY2030 to-be [{variant}]')
    base, over = sankey.render(cfg)
    emit(f"national_2030_{variant}", base, over)
    # No `national_2030_combined.png` alias. sheet.py's "national_2030" panel
    # already points at the mixed render, so the alias was consumed by nothing,
    # and copying a PNG forward under a name whose SVG was NOT rebuilt is what
    # left an orphan combined.svg for crossings.py to find.


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "2024"):
        print("FY2024 as-is"); build_2024()
    if which in ("all", "2030"):
        # Split overhead only. The holds/scales sensitivities are settled (D-63,
        # EN-17) and are not rebuilt in a working session; `python3 build.py
        # sensitivity` renders all three when the endnote needs re-checking.
        print("FY2030 to-be [mixed]"); build_2030("mixed")
    if which == "sensitivity":
        for v in ("holds", "scales", "mixed"):
            print(f"FY2030 to-be [{v}]"); build_2030(v)
        subprocess.run([sys.executable, os.path.join(REPO, "sheet.py"),
                        "--set", "overhead"], check=True)
    if which in ("all", "dc"):
        print("DC FY2024 as-is"); build_dc()
    if which == "all":
        # Every declared set is rebuilt, so no sheet in reference_renders/ can go
        # stale behind a render that moved. Adding a set to sheet.py:SETS is
        # enough; nothing here needs touching.
        import sheet as _sheet
        for _name in _sheet.WORKING_SETS:
            subprocess.run([sys.executable, os.path.join(REPO, "sheet.py"),
                            "--set", _name], check=True)
    print("build complete.")
