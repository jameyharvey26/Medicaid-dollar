"""Which population loses which dollar. One declaration, two callers.

D-102. This model existed twice in the paper and the two disagreed by $3.55.

The FY2030 panel drew its beneficiary pies by scaling FY2024 with one
multiplier, which the Limits register admitted "carries no information about
who bears the law". Figure 12 and Table 5 allocated each provision to the
population the statute names. Both were printed, on facing pages: the panel put
the new adult group at $17.66 and Figure 12 put it at $14.11. Nothing in the
repo could see it, because one lived in instances.py and the other in inc.py
and neither imported the other.

The allocation now lives here and both read it. It deliberately depends on
nothing but the raw ledgers and the pie solver - not compose, not instances -
because instances.py has to call it while compose is still importing, and a
module that reaches back up its own import chain is how one model becomes two.

The rules, unchanged from inc.py where they were written:

  provision -> population   the statute, where it names one; proportional to
                            FY2024 claims where it does not
  population -> service     each population's OWN measured FY2024 consumption
  scale                     overhead falls with the loss, so the service-
                            reaching provisions scale to the dollars that
                            actually fail to reach care

The row margins are the ledger's signed group totals, and the pie interior is
raked to them (D-101). The interior is declared unreliable in note 13; what
matters here is that no two places in the paper disagree about a margin.
"""
import sankey
import ledger_national_2024 as NAT

_L24 = NAT.build()
S = list(_L24.claims.cols)
NODE24 = {k: v.n for k, v in _L24.claims.col_margin.items()}
BY_G = {k: v.n for k, v in _L24.beneficiaries.row_margin.items()}
G = list(BY_G)

_f = sankey._solve_pies(S, NODE24, BY_G)
_raw = {g: sum(NODE24[s] * _f[s][i] for s in S) for i, g in enumerate(G)}
# The pie interior, raked so each row sums to the ledger's signed margin.
D = {s: {g: NODE24[s] * _f[s][i] * BY_G[g] / _raw[g]
         for i, g in enumerate(G)} for s in S}

_claims = sum(BY_G.values())
PROP = {g: BY_G[g] / _claims for g in G}
ONLY = lambda g0: {g: (1.0 if g == g0 else 0.0) for g in G}
CAP_SERVICES = ["Physicians & clinics", "Hospitals", "Long-term care"]

# An HR-1 provision that is deliberately outside this model, and why.
#
# D-104. `RULES` below covers six of the ledger's seven HR-1 peels. The seventh
# is correctly absent: D-89 established that the Medicare Savings moratorium's
# dollar pays a Medicare premium rather than buying a service, so it has no
# service incidence to allocate and it must not enter `gross`.
#
# Correct, and until now unasserted. `ledger_national_2030.agreement()` checks
# the ledger's HR-1 set against `outflows.OUTFLOWS`; nothing checked it against
# this module. An eighth provision landing in the ledger would have been
# dropped here in silence: `gross` would shrink, `scale` would rise, and the
# remaining six would absorb its dollars pro rata. The cube would still sum to
# the pool and `check()` would still pass, because an absence conserves.
# That is the D-102 failure one module over, and this is the instrument.
EXCLUDED = {
    "Blocked senior enrollment rule":
        "D-89. Pays a Medicare premium; reaches BENEFICIARY, not a service. "
        "It has no service incidence and is outside the scaled pool.",
}


def coverage():
    """Assert every HR-1 peel is either allocated here or declared excluded.

    Returns a list of failures, empty when the two sets agree. Called by
    `build.py` alongside `ledger_national_2030.agreement()`.
    """
    from ledger_national_2030 import HR1
    ours = {n for n, _, _, _ in RULES}
    out = []
    for name in sorted(set(HR1) - ours - set(EXCLUDED)):
        out.append(f"{name}: an HR-1 peel this model neither allocates nor "
                   f"declares excluded. Its dollars would be absorbed by the "
                   f"other provisions without trace.")
    for name in sorted(ours & set(EXCLUDED)):
        out.append(f"{name}: both allocated and declared excluded.")
    for name in sorted((ours | set(EXCLUDED)) - set(HR1)):
        out.append(f"{name}: named here, not an HR-1 peel in the ledger.")
    return out

RULES = [
    ("Work reporting",                   ONLY("New adult group"), S, "A1"),
    ("Provider tax limits",              PROP, S,            "A4"),
    ("Everything else",                  PROP, S,            "A4"),
    ("Blocked Medicaid enrollment rule", PROP, S,            "A4"),
    ("Directed payment caps",            None, CAP_SERVICES, "A3"),
    ("Six-month renewals",               ONLY("New adult group"), S, "A5"),
]

# Coverage is somebody dropped and the whole of their care goes to zero; rate
# is the same person, still enrolled, with their provider paid less. The
# residual is classed rate because its largest named components reduce what is
# paid rather than who is enrolled. It is mixed, and the Limits register says so.
KIND = {
    "Work reporting": "coverage",
    "Six-month renewals": "coverage",
    "Blocked Medicaid enrollment rule": "coverage",
    "Provider tax limits": "rate",
    "Everything else": "rate",
    "Directed payment caps": "rate",
}


def allocate(node30, amt):
    """node30: FY2030 service totals. amt: per-provision dollars per $100.

    Returns the cube, the per-population margins and the coverage/rate split.
    """
    pool = sum(NODE24[s] - node30[s] for s in S)
    gross = sum(amt[n] for n, _, _, _ in RULES)
    scale = pool / gross

    cube = {s: {g: 0.0 for g in G} for s in S}
    cube_k = {k: {s: {g: 0.0 for g in G} for s in S}
              for k in ("coverage", "rate")}
    per_prov = {}
    for name, reach, svcs, tag in RULES:
        v = amt[name] * scale
        if reach is None:                  # the cap: named services, all users
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
            cube_k[KIND[name]][s][g] += x

    loss = {g: sum(cube[s][g] for s in S) for g in G}
    return dict(
        pool=pool, gross=gross, scale=scale, cube=cube, cube_k=cube_k,
        per_prov=per_prov, loss=loss,
        by_g30={g: BY_G[g] - loss[g] for g in G},
        loss_k={k: {g: sum(cube_k[k][s][g] for s in S) for g in G}
                for k in ("coverage", "rate")},
    )
