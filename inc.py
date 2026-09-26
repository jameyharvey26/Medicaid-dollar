"""Provision x service x population. A declared thought exercise, not a finding.

The cube the paper has never built. Three axes, one declared rule each:

  provision -> population   the statute, where it names one (A1, A2, A3, A5);
                            proportional to FY2024 claims where it does not (A4)
  population -> service     each population's OWN FY2024 consumption mix, read
                            off the measured pies
  scale                     overhead falls with the loss, so the service-
                            reaching provisions scale to the $8.60 that
                            actually fails to reach care (A6)

DEPARTURE, and it has to be declared. The published model spreads every
eligibility-side loss across the six services at one undifferentiated rate,
population-blind. This exercise does the opposite: a provision that removes
adults removes ADULT dollars, so it takes more from hospitals than from
long-term care. The two cannot both be right. They reconcile only at the
total, $8.60, and nowhere in between (A7).
"""
import views, sankey
from compose import compose
import ledger_national_2024 as NAT, ledger_national_2030 as N30

c24 = compose(NAT.build(), views.V_NAT)
c30 = compose(N30.build("mixed"), views.V_2030, prior=NAT.build())
f = sankey._solve_pies(c24.order, c24.node, c24.gt)
G = ["Children", "Adults", "Disabled", "Aged"]
S = c24.order
DISP = {"Other": "Wrap around"}

# measured: FY2024 dollars, by service and group
D = {s: {g: c24.node[s] * f[s][i] for i, g in enumerate(G)} for s in S}
BY_G = {g: sum(D[s][g] for s in S) for g in G}
claims = sum(BY_G.values())
prop = {g: BY_G[g] / claims for g in G}

amt = {st[0]: st[2] for st in c30.steps}
amt[c30.claims_hr1_name] = c30.claims_hr1
for spec in c30.subs_spec:
    if spec[4] == "Provider Tax":
        amt["Provider tax limits"] = float(spec[1])

ONLY = lambda g0: {g: (1.0 if g == g0 else 0.0) for g in G}
CAP_SERVICES = ["Physicians & clinics", "Hospitals", "Long-term care"]

RULES = [
    ("Work reporting",                   ONLY("Adults"), S,            "A1"),
    ("Provider tax limits",              prop,           S,            "A4"),
    ("Everything else",                  prop,           S,            "A4"),
    ("Blocked Medicaid enrollment rule", prop,           S,            "A4"),
    ("Directed payment caps",            None,           CAP_SERVICES, "A3"),
    ("Six-month renewals",               ONLY("Adults"), S,            "A5"),
]

pool = sum(c24.node[s] - c30.node[s] for s in S)
gross = sum(amt[n] for n, _, _, _ in RULES)
scale = pool / gross

cube = {s: {g: 0.0 for g in G} for s in S}
per_prov = {}
for name, reach, svcs, tag in RULES:
    v = amt[name] * scale
    if reach is None:                      # the cap: named services, all users
        tot = sum(D[s][g] for s in svcs for g in G)
        cell = {(s, g): v * D[s][g] / tot for s in svcs for g in G}
    else:
        cell = {}
        for g in G:
            gv = v * reach[g]
            if gv <= 0:
                continue
            tot = sum(D[s][g] for s in svcs)
            for s in svcs:
                cell[(s, g)] = gv * D[s][g] / tot
    per_prov[name] = (v, tag, cell)
    for (s, g), x in cell.items():
        cube[s][g] += x

if __name__ == "__main__":
    print(f"pool ${pool:.2f}   gross ${gross:.2f}   scale {scale:.4f}\n")
    W = 13
    print(f"{'service':22}" + "".join(f"{g:>{W}}" for g in G) + f"{'total':>9}")
    for s in S:
        row = [cube[s][g] for g in G]
        print(f"{DISP.get(s,s):22}"
              + "".join(f"{-r:8.2f} {100*r/D[s][g]:4.1f}%" for r, g in zip(row, G))
              + f"{-sum(row):9.2f}")
    print(f"{'ALL SERVICES':22}"
          + "".join(f"{-sum(cube[s][g] for s in S):8.2f} "
                    f"{100*sum(cube[s][g] for s in S)/BY_G[g]:4.1f}%" for g in G)
          + f"{-pool:9.2f}")
    print(f"\n{'FY2024 baseline':22}" + "".join(f"{BY_G[g]:8.2f}      " for g in G)
          + f"{claims:9.2f}")
    print("\nseparately, a bill rather than a service:")
    print(f"  Medicare Savings suspension  -{amt['Blocked senior enrollment rule']:.2f}"
          f"  -> Aged [A2]")
    print("\nprovision totals (net of overhead):")
    for n, (v, tag, _) in per_prov.items():
        print(f"  {n:34} -{v:5.2f}  [{tag}]")
