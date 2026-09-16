#!/usr/bin/env python3
"""byteproof.py — prove the seam changes nothing.

Renders each artifact twice: once through the existing path
(instances.Instance -> sankey.render) and once through the new one
(Ledger + View -> compose -> sankey.render), and compares the SVG byte for
byte. S-064: a refactor that changes a pixel is not a refactor.

DC is proved on `legacy_mix=True`, which reproduces exactly what
`ledger_dc.py` carried. The correction is then a separate, visible diff
against a baseline that is known clean, rather than a change hidden inside
a rewrite.
"""
import sankey, instances
from compose import compose
from view import View
import ledger_national_2024 as NAT
import ledger_dc_2024 as DC
import ledger_national_2030 as N30
from ledger_2030 import ledger as arith
from tobe2030 import per100

from views import V_NAT, V_DC, V_2030


def svg(cfg):
    base, over = sankey.render(cfg)
    return "\n".join(base) + "\n" + "\n".join(over)


def compare(name, old_cfg, new_cfg):
    a, b = svg(old_cfg), svg(new_cfg)
    if a == b:
        print(f"{name:22} IDENTICAL   {len(a):,} bytes")
        return True
    first = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]),
                 min(len(a), len(b)))
    print(f"{name:22} DIFFERS     old {len(a):,} / new {len(b):,} bytes, "
          f"first at char {first}")
    print("    old: ..." + a[max(0, first-60):first+60].replace("\n", " "))
    print("    new: ..." + b[max(0, first-60):first+60].replace("\n", " "))
    return False


if __name__ == "__main__":
    ok = []
    ok.append(compare("national_2024",
                      instances.AS_IS_2024,
                      compose(NAT.build(), V_NAT)))
    ok.append(compare("dc_2024 (legacy)",
                      instances.as_is_dc(),
                      compose(DC.build(legacy_mix=True), V_DC)))
    # All three overhead variants. They exercise different arithmetic — the
    # lane scaling, the retention carve and the fraud lane each move — so
    # proving only the one that ships would leave two thirds of the ledger
    # untested through the new path.
    prior = NAT.build()
    for v in ("mixed", "holds", "scales"):
        ok.append(compare(f"national_2030 [{v}]",
                          instances.to_be_2030(arith(v), per100),
                          compose(N30.build(v), V_2030, prior=prior)))
    drift = N30.agreement()
    if drift:
        ok.append(False)
        print("\nreach declared twice and the two disagree:")
        for d in drift:
            print("  " + d)
    print("\n" + ("seam is a no-op" if all(ok) else "SEAM CHANGES OUTPUT"))
