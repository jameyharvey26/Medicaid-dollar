# signing.py — one signing routine, one register per jurisdiction.
#
# WHY THIS MODULE EXISTS. `_sign` lived inside `ledger_national_2024.py` and
# was called only from there. Nothing in it was national — it walks `sources`,
# `scale`, `peels`, `payers` and the matrices and builds its keys from
# structure — but because it lived in the national ledger, the District had no
# signing path at all. `signatures.py` carried no DC entry, and there was
# nowhere for one to go: every District figure read as unverified no matter
# who agreed to what.
#
# ONE REGISTER PER JURISDICTION, D-152, JW 18 November 2026: a state gets its
# own signature process, the same as national. The alternative considered was
# one shared register with panel-prefixed keys, and it is worse for a reason
# worth writing down. The register is a flat `key -> value` map and the
# District reuses national key strings exactly — `scale`, `peel.admin`,
# `peel.medicare`, `payer.ffs.capitation`, `source.federal` and five more. In
# one dict, `scale` is 9501.64 nationally and 43.72 in the District, and
# whichever was written last would silently lapse the other: the 16 September
# failure this whole apparatus exists to prevent, pointed in a new direction.
# Separate registers also mean adding the fifth state is adding a FILE, not
# editing one that four other panels read.
#
# WHAT A SIGNATURE COVERS. Two things, as of 19 November: the number, and the
# provenance behind it — source, vintage and basis, the three fields the
# endnote register prints as a figure's research footnote. Until then only the
# number was watched, so a figure could keep its value and have its source
# rewritten underneath it with the signature riding along onto a claim nobody
# had checked. A register entry may be a bare value, which signs the number
# alone, or `Agreed(value, provenance)`, which signs both.
#
# NOTHING HERE SIGNS ANYTHING. `verified` is "YYYY-MM-DD initials" and the
# initials belong to a person who opened the source. This module matches a
# ledger against what a person already wrote down. `--draft` prints the lines
# for a person to review and paste; it does not write them.
#
#     python3 signing.py dc            draft register lines for the DC panels
#     python3 signing.py national      and for the national FY2024 panel
#     python3 signing.py dc --unsigned only the figures with no entry yet

from collections import namedtuple
from dataclasses import replace

from ledger import MEASURED, MODELLED

# A register entry that binds both halves. `provenance` is Fig.provenance at
# the moment of agreement; `signing.py --draft` computes it for you.
Agreed = namedtuple("Agreed", "value provenance")


def _entry(rec):
    """A register value is either a bare number or an Agreed(value, prov)."""
    if isinstance(rec, Agreed):
        return rec.value, rec.provenance
    return rec, None


def sign(L, register):
    """Attach `register`'s signatures to every figure still as it was agreed.

    `register` is a module carrying REVIEW, SIGNED and UNSIGNED. A figure that
    has moved — in value or in provenance — is NOT signed: the signature and
    what was agreed are both recorded on it so `lapsed` fires and whatever is
    reporting can name both. The build fails rather than letting a signature
    travel onto a number nobody has seen.
    """
    REVIEW = register.REVIEW
    SIGNED = register.SIGNED
    UNSIGNED = getattr(register, "UNSIGNED", frozenset())

    def s(f, key):
        if key in UNSIGNED or f.status not in (MEASURED, MODELLED):
            return f
        if key not in SIGNED:
            return f                      # never signed; coverage reports it
        want, prov = _entry(SIGNED[key])
        if f.value is None or abs(f.value - want) > 1e-9:
            return replace(f, verified=REVIEW, verified_value=want,
                           verified_source=prov)
        if prov is not None and prov != f.provenance:
            return replace(f, verified=REVIEW, verified_value=f.value,
                           verified_source=prov)
        return f.sign(REVIEW, prov)

    # ANCHORS, and a gap found on 19 November. `_sign` never walked them.
    # `Ledger.figures()` has keyed them as `anchor.*` since they were
    # introduced, so the endnote register prints them and `coverage.py` grades
    # them — but no register entry could ever attach to one, in any
    # jurisdiction. They are the published dollars everything else divides
    # through: the District hundred, Exhibit 17's three lines, the dedicated
    # tax base. The figures most worth a signature were the ones that could
    # not carry one.
    for k in L.anchors:
        L.anchors[k] = s(L.anchors[k], f"anchor.{k}")
    for k in L.sources:
        L.sources[k] = s(L.sources[k], f"source.{k}")
    L.scale = s(L.scale, "scale")
    for pl in L.peels:
        pl.amount = s(pl.amount, f"peel.{pl.key}")
    for p in L.payers:
        for fld in ("capitation", "care", "admin", "margin"):
            setattr(p, fld, s(getattr(p, fld), f"payer.{p.key}.{fld}"))
    for m in [L.claims] + ([L.beneficiaries] if L.beneficiaries else []):
        for k in list(m.row_margin):
            m.row_margin[k] = s(m.row_margin[k], f"{m.name}.row.{k}")
        for k in list(m.col_margin):
            m.col_margin[k] = s(m.col_margin[k], f"{m.name}.col.{k}")
        for k in list(m.cell):
            m.cell[k] = s(m.cell[k], f"{m.name}.cell.{k[0]}.{k[1]}")
    return L


# ---------------------------------------------------------------------------
# drafting — print, never write


def draft(L, register=None, only_unsigned=False):
    """Register lines for the signable figures on a ledger.

    Signable means MEASURED or MODELLED: a derived figure inherits its
    standing from its parents and signing one asserts nothing new, and an
    absent figure has nothing to agree to. Each line carries the value, the
    provenance fingerprint, and the head of the source so a reader can see
    what they would be agreeing to without opening the register's own file.
    """
    SIGNED = getattr(register, "SIGNED", {}) if register else {}
    UNSIGNED = getattr(register, "UNSIGNED", frozenset()) if register else frozenset()
    out = []
    for key, f in sorted(L.figures().items()):
        if f.status not in (MEASURED, MODELLED) or key in UNSIGNED:
            continue
        if only_unsigned and key in SIGNED:
            continue
        state = "already in the register" if key in SIGNED else "NOT YET SIGNED"
        head = " ".join((f.source or "no source named").split())[:72]
        out.append((key, f, state, head))
    return out


def _print_draft(name, L, register, only_unsigned):
    rows = draft(L, register, only_unsigned)
    print(f"\n# {name} — {len(rows)} signable figure(s)")
    print("# Review each against its source, then paste into the register.")
    print("# Claude cannot sign. The initials in REVIEW belong to whoever "
          "opened these.")
    for key, f, state, head in rows:
        print(f"\n    # {head}")
        print(f"    # {f.status}, {f.vintage or 'no vintage'} — {state}")
        print(f"    {key!r}: Agreed({f.value!r}, {f.provenance!r}),")


if __name__ == "__main__":
    import importlib
    import sys

    which = sys.argv[1] if len(sys.argv) > 1 else "dc"
    only_unsigned = "--unsigned" in sys.argv

    PANELS = {
        "dc": [("DC FY2024", "ledger_dc_2024", "build", {"legacy_mix": False},
                "signatures_dc"),
               ("DC FY2030", "ledger_dc_2030", "ledger", {}, "signatures_dc")],
        "national": [("national FY2024", "ledger_national_2024", "build", {},
                      "signatures")],
    }
    if which not in PANELS:
        sys.exit(f"unknown jurisdiction {which!r}; try: {', '.join(PANELS)}")

    for label, mod, fn, kw, reg in PANELS[which]:
        L = getattr(importlib.import_module(mod), fn)(**kw)
        try:
            R = importlib.import_module(reg)
        except ImportError:
            R = None
        _print_draft(label, L, R, only_unsigned)
    print("\n# Nothing above is signed.")
