# compose.py — render(Ledger, View) -> Instance -> svg.
#
# The Layout third of the seam is `sankey.py` and `outflows.py` and is not
# being rewritten. This module is the joint: it reads a Ledger and a View and
# produces the `Instance` the existing renderer already takes.
#
# Doing it this way rather than rewriting the renderer is deliberate. S-064's
# verification standard for a refactor of this kind is: render before, refactor,
# render after, diff. A refactor that changes a pixel is not a refactor. With
# the composer in between, the ledger can be proved byte-identical through the
# new path before anything downstream is touched, and any later change to a
# number then shows up as a diff against a known-clean baseline instead of
# being lost inside a rewrite.
#
# Every value on the Instance comes from the Ledger. Every label, coordinate
# and title comes from the View. Nothing is typed in here.

from instances import Instance
from ledger import Ledger
from view import View


def _peel(L: Ledger, key: str) -> float:
    for p in L.peels:
        if p.key == key:
            return p.amount.n
    return 0.0


def compose(L: Ledger, V: View) -> Instance:
    M = L.claims
    lane = {p.key: p for p in L.lanes()}

    def cells(row):
        return {c: M.get(row, c).n for c in L.nodes}

    mco, dual, ffs = lane["mco"], lane["dual"], lane["ffs"]

    steps = []
    for p in L.peels:
        if p.key in V.step_x:
            side = "top" if p.kind in ("admin", "return") else "bot"
            steps.append((p.key, side, p.amount.n, V.step_x[p.key]))

    node = {c: M.col_margin[c].n for c in L.nodes}

    # A lane collapses when the ledger says there is nothing in it. Two
    # different facts both produce that: a MEASURED zero, which is a state with
    # no managed care, and an ABSENT capitation, which is a state where we do
    # not know. Both must disappear from the drawing; only the second is a gap,
    # and only the second earns a line in the declarations.
    collapsed = [p.key for p in (mco, dual, ffs)
                 if p.capitation.is_absent or abs(p.capitation.n) < 0.005]

    return Instance(
        name=L.geography.lower().replace(" ", "_") + "_" + L.year,
        fed=L.sources["federal"].n, state=L.sources["state"].n,
        admin=_peel(L, "admin"), medicare=_peel(L, "medicare"),
        mco=mco.capitation.n, dual=dual.capitation.n, ffs=ffs.capitation.n,
        mco_ret=mco.capitation.n - mco.care.n,
        dual_ret=dual.capitation.n - dual.care.n,
        earnings=mco.margin.n + dual.margin.n,
        adm_marg=mco.admin.n + dual.admin.n,
        mco_adm=mco.admin.n, dual_adm=dual.admin.n,
        mco_care=mco.care.n, dual_care=dual.care.n,
        node=node,
        fraud=_peel(L, "fraud"),
        ffs_n=cells("ffs"), mcoc_n=cells("mco"), dualc_n=cells("dual"),
        collapsed=collapsed,
        gt=({g: f.n for g, f in L.beneficiaries.row_margin.items()}
            if (L.beneficiaries and V.show_beneficiaries) else {}),
        steps=steps,
        subs_spec=V.subs_spec,
        hr1_term=dict(V.hr1_term),
        order=list(L.nodes),
        disp=dict(V.disp),
        show_beneficiaries=bool(V.show_beneficiaries and L.beneficiaries),
        absent=list(L.declarations) if not V.show_beneficiaries else [],
        cp0_label=list(V.cp0_label),
        centre=V.centre,
        kicker=V.kicker, title=V.title, strap=V.strap,
    )


def render(L: Ledger, V: View):
    """The signature ARCHITECTURE.md asks for."""
    import sankey
    return sankey.render(compose(L, V))
