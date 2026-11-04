# dc_endnotes.py — the District's numbered endnote register, generated.
#
# PARITY, not duplication. The national whitepaper has `ENDNOTES.md`: every
# figure on an artifact has a stably numbered entry carrying the claim, the
# source, the vintage, the basis and the status (S-054). The District has
# `DC_PROVENANCE.md`, which is a narrative sweep with a table at the end. The
# provenance is already attached to the figures — `ledger.Fig` carries it, and
# `Ledger.figures()` says in its own docstring that it exists "for the
# provenance sweep and for endnote generation". It is the REGISTER that does
# not exist. This generates it.
#
# WHY NUMBERS ARE NOT COMPUTED FROM A SORT. ENDNOTES.md is append-only and
# stably numbered (S-032): "if a figure changes, amend the entry in place and
# note the superseding decision, never renumber." A number derived from the
# current sort order would renumber the whole register the first time a payer
# is added. So the key order lives in `DC_ENDNOTE_KEYS.txt`, which this script
# appends to and never reorders. Delete that file and every DC-EN number in
# every document that cites one becomes wrong.
#
# NOTHING HERE IS SIGNED. `verified` is "YYYY-MM-DD initials" and the initials
# belong to a person who opened the source. This script reports the field; it
# cannot fill it.
#
# Run: python3 dc_endnotes.py            prints the register
#      python3 dc_endnotes.py --write    writes DC_ENDNOTES.md

import importlib
import os
import sys

import ledger as LD

REGISTRY = "DC_ENDNOTE_KEYS.txt"
OUT = "DC_ENDNOTES.md"

PANELS = [
    ("DC24", "DC FY2024 as-is", "ledger_dc_2024", "build", {"legacy_mix": False}),
    ("DC30", "DC FY2030 to-be (DRAFT)", "ledger_dc_2030", "ledger", {}),
]

# ENDNOTES.md's own status key, so a reader moving between the two registers
# does not have to learn a second vocabulary.
MARK = {LD.MEASURED: "M", LD.DERIVED: "D", LD.MODELLED: "P",
        LD.CLIENT: "C", LD.ABSENT: "ABSENT"}

# Human phrasing for the key prefixes. A register entry has to read as a
# claim, not as a variable name.
LANE = {
    "anchor": "Anchor figure",
    "source": "Source of funds",
    "peel": "Peel",
    "payer": "Payer lane",
    "claims": "Claims allocation",
    "beneficiaries": "Beneficiary allocation",
    "scale": "The hundred",
}
FIELD = {
    "capitation": "money in",
    "care": "money reaching care",
    "admin": "plan administration",
    "margin": "plan margin",
}


def claim(key: str) -> str:
    """The entry's headline, built from the key rather than typed."""
    parts = key.split(".")
    head = LANE.get(parts[0], parts[0])
    if parts[0] == "payer" and len(parts) == 3:
        return f"{head}: {parts[1]}, {FIELD.get(parts[2], parts[2])}"
    if parts[0] in ("claims", "beneficiaries"):
        if parts[1] == "cell":
            return f"{head}: {parts[2]} into {'.'.join(parts[3:])}"
        return f"{head}: {parts[1]} margin, {'.'.join(parts[2:])}"
    if len(parts) > 1:
        return f"{head}: {'.'.join(parts[1:])}"
    return head


def load():
    out = []
    for code, label, mod, fn, kw in PANELS:
        m = importlib.import_module(mod)
        out.append((code, label, getattr(m, fn)(**kw)))
    return out


def registry(order_now):
    """Append-only key order. Returns the full list, oldest first."""
    known = []
    if os.path.exists(REGISTRY):
        with open(REGISTRY) as fh:
            known = [ln.strip() for ln in fh if ln.strip()
                     and not ln.startswith("#")]
    seen = set(known)
    added = [k for k in order_now if k not in seen]
    if added:
        with open(REGISTRY, "a") as fh:
            if not known:
                fh.write("# DC endnote key order. APPEND-ONLY. Never reorder, "
                         "never delete a line: DC-EN numbers are this file's "
                         "line positions and documents cite them.\n")
            for k in added:
                fh.write(k + "\n")
    return known + added


def entry(n, code, label, key, f):
    mark = MARK.get(f.status, f.status)
    val = "ABSENT" if f.is_absent else f"{float(f.value):,.4f}"
    # The anchors are published dollars; everything else is struck on the
    # hundred. The basis string is what says which, so the unit is read off it
    # rather than guessed from the key.
    unit = "" if (f.is_absent or "$M" in (f.basis or "")) else " per $100"
    head = f"**DC-EN-{n} · {claim(key)} — {label}: {val}{unit}. | {mark}**"
    body = []
    if f.source:
        body.append(f"Source: {f.source}.")
    if f.vintage:
        body.append(f"Vintage: {f.vintage}.")
    if f.basis:
        body.append(f"Basis: {f.basis}.")
    if f.parents:
        body.append("Derived from: " + ", ".join(f"`{p}`" for p in f.parents) + ".")
    note = " ".join((f.note or "").split())
    if note:
        body.append(note)
    body.append(f"Verified: {f.verified or '**no**'}.")
    body.append(f"Ledger key: `{code}:{key}`.")
    return head + "\n" + " ".join(body) + "\n"


def report():
    panels = load()
    order_now = [f"{code}:{k}"
                 for code, _lab, L in panels
                 for k in sorted(L.figures().keys())]
    order = registry(order_now)
    num = {k: i + 1 for i, k in enumerate(order)}

    A = [
        "# DC endnote register",
        "",
        "Numbered endnotes for the District panels. **Every figure that "
        "appears on a District artifact has an entry here**, on the same rule "
        "as `ENDNOTES.md` (S-054). Generated by `dc_endnotes.py` from the "
        "`Fig` records in the ledgers. Do not hand-edit: re-run it.",
        "",
        "Numbering is append-only and stable (S-032). The order lives in "
        "`DC_ENDNOTE_KEYS.txt` and a DC-EN number is that file's line "
        "position. If a figure changes, the entry changes in place and keeps "
        "its number.",
        "",
        "`DC_PROVENANCE.md` is the narrative companion: it says what was "
        "chosen and what is missing, and why. This file keys individual "
        "figures to their sources.",
        "",
        "Status key: **M** measured · **D** derived from measured inputs · "
        "**P** modelled · **C** supplied by the subject · **ABSENT** not "
        "published and not estimated.",
        "",
        "**No District figure in this project is signed.** `signatures.py` "
        "carries no DC entry, so every `Verified` line below reads **no** — "
        "including for figures that are measured, correct and "
        "uncontroversial. Measured says where a number came from. Verified "
        "says a named person opened the source and agreed with it.",
        "",
        "---",
        "",
    ]
    for code, label, L in panels:
        figs = L.figures()
        counts = {}
        for f in figs.values():
            counts[f.status] = counts.get(f.status, 0) + 1
        signed = sum(1 for f in figs.values() if f.verified)
        A += [f"## {label}  (`{code}`)", "",
              "  ·  ".join(f"**{counts.get(k, 0)}** {k}"
                           for k in (LD.MEASURED, LD.DERIVED, LD.MODELLED,
                                     LD.CLIENT, LD.ABSENT)),
              "", f"**{signed} of {len(figs)} figures signed by a person.**",
              ""]
        for key in sorted(figs):
            full = f"{code}:{key}"
            A.append(entry(num[full], code, label, key, figs[key]))
        A.append("")
    return "\n".join(A)


if __name__ == "__main__":
    text = report()
    if "--write" in sys.argv:
        with open(OUT, "w") as fh:
            fh.write(text)
        print(f"wrote {OUT} ({len(text.splitlines())} lines)")
    else:
        print(text)
