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
import views
from compose import compose
import ledger_national_2024 as NAT, ledger_national_2030 as N30

import incidence

c24 = compose(NAT.build(), views.V_NAT)
c30 = compose(N30.build("mixed"), views.V_2030, prior=NAT.build())

# D-102. The allocation itself moved to incidence.py, because instances.py has
# to read it while compose is still importing and this module cannot be
# imported from there. What is left here is the presentation: the cube printed
# for inspection, and the names the figures import.
G, S, D = incidence.G, incidence.S, incidence.D
BY_G = incidence.BY_G
DISP = {"Other": "Wrap around"}

# The SAME amounts the FY2030 ledger allocates with, imported rather than
# recovered from the composed panel's steps. Recovering them gave figures a
# cent or two different, which put the panel at $14.16 and this module at
# $14.11 - the $3.55 problem again, two orders of magnitude smaller and just
# as wrong. One input, one model, one number.
from tobe2030 import per100 as amt

_A = incidence.allocate(c30.node, amt)
cube, cube_k, per_prov = _A["cube"], _A["cube_k"], _A["per_prov"]
pool, gross, scale = _A["pool"], _A["gross"], _A["scale"]

# The FY2030 margins are READ OFF THE PANEL, not recomputed here. Both come
# from incidence.allocate, but the panel's call passes the FY2030 ledger's own
# node totals and this one passes the composed panel's, which differ in the
# fourth decimal - enough to print $14.16 there and $14.11 here. A published
# figure is measured, not recomputed: the panel publishes it, so this module
# takes it and rakes its own split to match.
BY_G30 = dict(c30.gt)
LOSS_G = {g: BY_G[g] - BY_G30[g] for g in G}
LOSS_G_K = {k: {g: _A["loss_k"][k][g] * (LOSS_G[g] / _A["loss"][g])
                for g in G} for k in ("coverage", "rate")}
RULES, KIND = incidence.RULES, incidence.KIND
MSP_BILL = amt["Blocked senior enrollment rule"]      # a bill, not a service

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
