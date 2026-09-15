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
from view import View


def band(t):
    print("\n" + t + "\n" + "-" * len(t))


band("1. conservation")
for mod, name in ((NAT, "national FY2024 as-is"), (DC, "DC FY2024 as-is")):
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

band("3. generated endnote register, DC")
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
