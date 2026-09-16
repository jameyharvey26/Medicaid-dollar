#!/usr/bin/env python3
"""coverage.py — is this jurisdiction's baseline actually complete?

`check(ledger)` answers a different question. It asks whether the numbers we
have are consistent with each other. A ledger can conserve perfectly and still
be half empty, because absence conserves: nothing plus nothing balances.

This asks whether we have the numbers at all, phase by phase, left to right,
and reports each required figure as HELD, MODELLED or MISSING with its source
named. It is the acquisition instrument for a new territory and it is meant to
be run from the first pull, when everything is MISSING, rather than at the end.

    python3 coverage.py dc
    python3 coverage.py national

Exit code is 1 while anything is MISSING, so it can gate an acquisition the
way crossings.py gates a render.
"""
import sys

import ledger as LD
from ledger import ABSENT, MEASURED, MODELLED, CLIENT, DERIVED, UNALLOCATED

# Three states, not two. A figure with a source nobody has opened this cycle
# is not held and is not missing. Reporting it as held is how a stale baseline
# passes as a finished one.
HELD, STALE, MODEL, MISS = "HELD", "STALE", "MODELLED", "MISSING"
LAPSED = "LAPSED"


def _state(fig, cycle=None, key=None, named=None):
    if fig is None:
        return MISS, ""
    if fig.lapsed:
        return LAPSED, f"signed at {fig.verified_value}, now {fig.value}"
    if fig.verified and cycle and fig.vintage and fig.vintage != cycle:
        return STALE, (f"{fig.source} {fig.vintage}".strip()
                       + f" — signed against {fig.vintage}, cycle is {cycle}")
    if fig.status == ABSENT:
        return MISS, fig.note
    if fig.status in (MEASURED, CLIENT):
        src = f"{fig.source} {fig.vintage}".strip()
        return (HELD, f"{src}  [{fig.verified}]") if fig.verified else (STALE, src)
    if fig.status == DERIVED:
        # A derived figure used to be graded HELD on sight. Arithmetic does
        # not add confidence to its inputs, so it now inherits: verified when
        # everything it was computed from is, and unverified otherwise, with
        # the first unsigned ancestor named so the reader knows what to go and
        # check rather than being told a sum is fine.
        chain = "derived from " + ", ".join(fig.parents or ("nothing named",))
        if named is None:
            return STALE, chain
        good, why = LD.verification(key, named)
        return (HELD, f"{chain}  [{why}]") if good else (STALE, f"{chain} — {why}")
    return (MODEL if fig.verified else STALE), fig.note


def rows(L):
    """Every figure the baseline needs, in lifecycle order."""
    out = []
    # Identity, not equality: two figures can carry the same value and the
    # same provenance and still be different figures in different phases.
    named = L.figures()
    bykey = {id(f): k for k, f in named.items()}

    def add(phase, item, fig):
        st, why = _state(fig, key=bykey.get(id(fig)), named=named)
        out.append((phase, item, st, why))

    add("FEDERAL", "federal share", L.sources.get("federal"))
    add("STATE GOVERNMENT", "non-federal share", L.sources.get("state"))
    add("STATE AGENCY", "scale ($M per $1)", L.scale)
    for p in L.peels:
        if p.charged in ("FEDERAL", "STATE_GOVERNMENT", "STATE_AGENCY"):
            add("STATE AGENCY", p.label.lower(), p.amount)

    for lane in L.lanes():
        add("DISBURSE", f"{lane.key} capitation", lane.capitation)
    for lane in L.lanes():
        kids = L.children(lane.key)
        if kids:
            for k in kids:
                add("DISBURSE", f"  {k.key} capitation (named plan)", k.capitation)
        elif lane.kind in ("mco", "dual", "pace"):
            out.append(("DISBURSE", f"  named plans under {lane.key}", MISS,
                        "lane not expanded: no plan-level detail in the ledger"))

    for p in L.payers:
        if p.kind == "ffs":
            continue
        add("PAYER", f"{p.key} plan administration", p.admin)
        add("PAYER", f"{p.key} margin / earnings", p.margin)

    M = L.claims
    for r in M.rows:
        st = M.row_state(r)
        if st == UNALLOCATED:
            out.append(("CLAIMS", f"{r} into service categories", MISS,
                        "no allocation in the ledger"))
        else:
            worst = HELD
            src = set()
            rank = {HELD: 0, MODEL: 1, STALE: 2, LAPSED: 3, MISS: 4}
            for c in M.cols:
                f = M.get(r, c)
                s, why = _state(f)
                if rank[s] > rank[worst]:
                    worst = s
                if s != MISS:
                    src.add(why)
            out.append(("CLAIMS", f"{r} into service categories", worst,
                        "; ".join(sorted(src))[:60]))

    for c in L.nodes:
        add("PROVIDERS", f"{c} total", M.col_margin.get(c))

    for p in L.peels:
        if p.charged in ("CLAIMS", "PROVIDERS"):
            add("PROVIDERS", p.label.lower(), p.amount)
    if not any(p.key == "fraud" for p in L.peels):
        out.append(("PROVIDERS", "documented fraud", MISS,
                    "no figure in the ledger"))

    B = L.beneficiaries
    if B is None:
        out.append(("BENEFICIARIES", "eligibility group totals", MISS,
                    "no matrix in the ledger"))
        out.append(("BENEFICIARIES", "group by service interior", MISS,
                    "no matrix in the ledger"))
    else:
        for g in B.rows:
            add("BENEFICIARIES", f"{g} total", B.row_margin.get(g))
        out.append(("BENEFICIARIES", "group by service interior",
                    MISS if B.state == UNALLOCATED else MODEL,
                    B.note[:60]))
    return out


def report(L, title=""):
    r = rows(L)
    print(f"\nBASELINE COVERAGE — {title or L.geography} {L.year}")
    print("=" * 76)
    phase = None
    for ph, item, st, why in r:
        if ph != phase:
            print(f"\n{ph}")
            phase = ph
        mark = {HELD: "  ok  ", STALE: " STALE", MODEL: " ~mod ",
                LAPSED: "LAPSED", MISS: " MISS "}[st]
        print(f"  [{mark}] {item:44} {why[:44]}")
    n = {k: sum(1 for x in r if x[2] == k)
         for k in (HELD, STALE, MODEL, LAPSED, MISS)}
    print("\n" + "-" * 76)
    print(f"  {n[HELD]} verified   {n[MODEL]} modelled   {n[STALE]} unverified"
          f"   {n[MISS]} missing   of {len(r)} figures the baseline needs")
    if n[LAPSED]:
        print(f"  {n[LAPSED]} figure(s) LAPSED: signed off, then changed.")
    if n[MISS] or n[STALE]:
        print(f"  Baseline INCOMPLETE. {n[MISS]} not acquired, "
              f"{n[STALE]} carrying a source nobody has opened this cycle.")
    return n[MISS] + n[STALE] + n[LAPSED]


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "dc"
    if which == "dc":
        import ledger_dc_2024 as M
        L = M.build()
    elif which == "national":
        import ledger_national_2024 as M
        L = M.build()
    else:
        import synth
        L = synth.build_ledger(which)
    sys.exit(1 if report(L) else 0)
