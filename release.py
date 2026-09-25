# release.py — what this build is, in one place.
#
# D-79. The cover and the sources register both used to carry typed strings:
# "Working draft v5.0, 19 September 2026" on the cover and "matched to build
# main@2026-09-11" in the register. They disagreed with each other by eight
# days and both were stale, because a typed string does not move when the
# build moves. S-105 applies to prose exactly as it applies to figures.
#
# The build identifier cannot come from git. The working copy is pulled as a
# tarball and has no .git directory, so anything asking the repository for a
# commit fails or, worse, silently reports the wrong thing. It is derived
# instead from the content of the modules that determine what the panels and
# the paper say: change any of them and the identifier changes, change none of
# them and it does not. That is the property the register needs — an
# identifier a reader can quote back, that maps to exactly one artifact.

import hashlib
import pathlib
import datetime

VERSION = "6.0"

# The modules a figure can move through. Deliberately not every file in the
# repo: a change to a gate or a test does not change what the paper says, and
# folding them in would churn the identifier for no reader-visible reason.
_SOURCES = [
    "basis_national.py", "ledger.py", "ledger_national_2024.py",
    "ledger_national_2030.py", "ledger_2030.py", "ledger_dc_2024.py",
    "provider_mix.py", "tobe2030.py", "phasein.py", "ramp.py",
    "compose.py", "view.py", "views.py", "sankey.py", "tracker.py",
]

_HERE = pathlib.Path(__file__).resolve().parent


def build_id() -> str:
    """Six hex characters over the content of the figure-bearing modules."""
    h = hashlib.sha256()
    for name in sorted(_SOURCES):
        p = _HERE / name
        if p.exists():
            h.update(name.encode())
            h.update(p.read_bytes())
    return h.hexdigest()[:6]


def build_date() -> str:
    """The newest modification date among those modules, not today's date.

    Rendering the paper twice on different days must not change what the
    footer says, or the stamp reports when it was printed rather than what it
    was printed from.
    """
    times = [(_HERE / n).stat().st_mtime for n in _SOURCES if (_HERE / n).exists()]
    d = datetime.date.fromtimestamp(max(times)) if times else datetime.date.today()
    return f"{d.day} {d:%B} {d.year}"


def stamp() -> str:
    """The footer line. 'v6.0 · 25 September 2026 · build a3f9c1'."""
    return f"v{VERSION} \u00b7 {build_date()} \u00b7 build {build_id()}"


def register_line() -> str:
    """The sentence that closes the sources paragraph in Limits and sources."""
    return (f"Full register at the address on the back page, matched to "
            f"build {build_id()} of {build_date()}.")


if __name__ == "__main__":
    print(stamp())
    print(register_line())
