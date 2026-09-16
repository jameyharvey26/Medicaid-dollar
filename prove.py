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

L = NAT.build()
L.peels[0].amount = LD.Fig(6.07, source="x", vintage="y", basis="z")
cases["administration raised by $1.00"] = L

L = NAT.build()
L.payers[0].margin = LD.Fig(0.60, status=LD.MODELLED)      # method stripped
cases["a modelled figure with no method stated"] = L

# The two breaks that only exist on the to-be. A tributary's amount and its
# reach are different facts and each has its own way of going wrong: the first
# stops the ledger conserving, the second does not and would render a terminal
# in the wrong place with every sum still balancing.
L = N30.build()
L.peels[0].amount = LD.Fig(L.peels[0].amount.n + 1.0, status=LD.MODELLED,
                           note="moved")
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
import signatures as _SG
_was = _SG.SIGNED["claims.cell.mco.Hospitals"]
_SG.SIGNED["claims.cell.mco.Hospitals"] = _was + 0.37     # the pre-MACPAC value
_L = NAT.build()
_hits = [x for x in LD.check(_L) if "verified at" in x]
print(f"{'a figure edited since it was agreed':42} "
      f"{'CAUGHT' if _hits else '*** PASSED, GATE IS BLIND ***'}")
for _x in _hits:
    print("      " + _x)
_SG.SIGNED["claims.cell.mco.Hospitals"] = _was


band("4. a derived figure inherits verification, never assumes it")
_n = NAT.build().figures()
for _k, _want in (("payer.ffs.care", True),
                  ("beneficiaries.col.Hospitals", True),
                  ("payer.mco.care", False),
                  ("claims.row.mco", False),
                  ("scale", False)):
    _got, _why = LD.verification(_k, _n)
    print(f"  {_k:32} {'verified' if _got else 'not verified':13} "
          f"{'ok' if _got == _want else '*** WRONG ***'}   {_why}")


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
