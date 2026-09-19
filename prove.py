#!/usr/bin/env python3
"""prove.py — demonstrate the Ledger / View seam against the two live ledgers.

Four things, in order:
  1. both ledgers conserve under check()
  2. a deliberately broken ledger fails, and says what broke
  3. the endnote register generates from the ledger
  4. a View reports what the ledger cannot support, instead of inventing it
"""
import copy

import ledger as LD
import ledger_national_2024 as NAT
import ledger_dc_2024 as DC
import ledger_national_2030 as N30
from view import View


def band(t):
    print("\n" + t + "\n" + "-" * len(t))


band("1. conservation")
for mod, name in ((NAT, "national FY2024 as-is"), (DC, "DC FY2024 as-is"),
                  (N30, "national FY2030 to-be")):
    L = mod.build()
    fails = LD.check(L)
    print(f"{name:26} {'CONSERVES' if not fails else 'FAILS'}"
          f"   {len(L.figures())} figures")
    for x in fails:
        print("    " + x)

band("2. a broken ledger must fail")
cases = {}

L = NAT.build()
L.payers[0].capitation = LD.Fig(41.06, source="x", vintage="y", basis="z")
cases["a lane moved by $1.00"] = L

L = NAT.build()
L.claims.cell[("ffs", "Hospitals")] = LD.Fig(9.68, source="x", vintage="y", basis="z")
cases["a filled cell moved by $1.00"] = L


def _peel(L, key):
    """Address a peel by key. It used to be addressed by index, which made the
    detector depend on declaration order: when Vaccines for Children was added
    ahead of administration (D-71), two of these cases silently started
    breaking a different peel than the one they name."""
    return next(x for x in L.peels if x.key == key)


L = NAT.build()
_peel(L, "admin").amount = LD.Fig(6.07, source="x", vintage="y", basis="z")
cases["administration raised by $1.00"] = L

L = NAT.build()
L.payers[0].margin = LD.Fig(0.60, status=LD.MODELLED)      # method stripped
cases["a modelled figure with no method stated"] = L

# The two breaks that only exist on the to-be. A tributary's amount and its
# reach are different facts and each has its own way of going wrong: the first
# stops the ledger conserving, the second does not and would render a terminal
# in the wrong place with every sum still balancing.
L = N30.build()
_t = _peel(L, "Work reporting")
_t.amount = LD.Fig(_t.amount.n + 1.0, status=LD.MODELLED, note="moved")
cases["an HR-1 tributary moved by $1.00"] = L

# The hole this was written to close: a derived figure used to be graded
# verified on sight, with no check that the figures it names even exist.
L = NAT.build()
L.claims.row_margin["ffs"] = LD.Fig.derived(41.08, ("payer.ffs.nonesuch",))
cases["a derived figure naming a parent that is not there"] = L

L = DC.build()
L.declared = []
cases["DC with its declarations removed"] = L

L = DC.build()
L.claims.cell[("mco", "Hospitals")] = LD.Fig(40.00, status=LD.MODELLED,
                                             note="invented")
cases["a cell larger than its row margin"] = L

for name, L in cases.items():
    fails = LD.check(L)
    print(f"{name:42} {'CAUGHT' if fails else '*** PASSED, GATE IS BLIND ***'}")
    for x in fails[:2]:
        print("      " + x)

band("3. a signature must not travel onto a figure that has moved")
# This test used to read the live register, which meant it stopped working the
# moment the register was legitimately emptied (D-70 lapsed all 33). A detector
# must not depend on production state: it plants its own signature at a value
# it knows is wrong, and takes it out again.
import signatures as _SG
_KEY = "claims.cell.mco.Hospitals"
_had = _KEY in _SG.SIGNED
_was = _SG.SIGNED.get(_KEY, NAT.build().figures()[_KEY].n)
_SG.SIGNED[_KEY] = _was + 0.37
_L = NAT.build()
_hits = [x for x in LD.check(_L) if "verified at" in x]
print(f"{'a figure edited since it was agreed':42} "
      f"{'CAUGHT' if _hits else '*** PASSED, GATE IS BLIND ***'}")
for _x in _hits:
    print("      " + _x)
if _had:
    _SG.SIGNED[_KEY] = _was
else:
    del _SG.SIGNED[_KEY]


band("4. a derived figure inherits verification, never assumes it")
# Like section 3, this used to read the live register, so it could only
# demonstrate inheritance while something happened to be signed. D-70 emptied
# the register and the test started reporting WRONG on figures that are fine.
# It now signs its own parents for the length of the test and unsigns them.
import signatures as _S4
_n0 = NAT.build().figures()
# Sign every LEAF — every figure that names no parents — and nothing else.
# That is the cleanest fixture for this question: if the leaves are agreed,
# a derived figure is verified exactly when its own chain resolves to them.
_planted = [k for k, f in _n0.items()
            if not getattr(f, "parents", None) and k not in _S4.SIGNED]
for _k in _planted:
    _S4.SIGNED[_k] = _n0[_k].n
_n = NAT.build().figures()
for _k, _want in (("payer.ffs.care", True),
                  ("beneficiaries.col.Hospitals", True),
                  ("payer.mco.care", False),
                  ("claims.row.mco", False),
                  # scale was False here because it was carried as DERIVED with
                  # no parents, so it reported "derived from nothing named" and
                  # could never be verified. That was a defect encoded as an
                  # expectation. It is MEASURED from Exhibit 16 and signed
                  # 2026-09-18.
                  ("scale", True)):
    _got, _why = LD.verification(_k, _n)
    print(f"  {_k:32} {'verified' if _got else 'not verified':13} "
          f"{'ok' if _got == _want else '*** WRONG ***'}   {_why}")
for _k in _planted:
    del _S4.SIGNED[_k]


band("5. reach declared twice must agree")
_saved = None
import outflows as _OF
_saved = _OF.OUTFLOWS["Six-month renewals"].get("reach")
_OF.OUTFLOWS["Six-month renewals"]["reach"] = "CLAIMS"
_d = N30.agreement()
print(f"{'outflows reach edited behind the ledger':42} "
      f"{'CAUGHT' if _d else '*** PASSED, GATE IS BLIND ***'}")
for x in _d:
    print("      " + x)
_OF.OUTFLOWS["Six-month renewals"]["reach"] = _saved


band("6. generated endnote register, DC")
for line in LD.endnotes(DC.build())[:14]:
    print(line)
print("  ... " + str(len(LD.endnotes(DC.build()))) + " lines total")

band("4. what a view can and cannot draw")
L = DC.build()
for label, v in (
    ("aggregate lanes, fan on", View(expand=[], show_beneficiaries=False)),
    ("payer zoom, fan on", View(expand=["mco", "dual"], show_beneficiaries=False)),
    ("payer zoom, fan off", View(expand=["mco", "dual"], show_beneficiaries=False,
                                 show_claims_fan=False)),
):
    rows = [p.label for p in v.payer_rows(L)]
    print(f"\n{label}")
    print("  payer rows: " + ", ".join(rows))
    u = v.undrawable(L)
    print(f"  undrawable ({len(u)}):")
    for x in u:
        print("    - " + x)
