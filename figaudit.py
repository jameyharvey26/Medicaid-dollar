"""Every dollar figure the paper prints, against the ledger that computed it.

The manuscript carries its figures as literals. `typedfigures.py` finds the
ones in the CODE that should have been derived; nothing looked at the ones in
the PROSE, and two tables had been quietly disagreeing with the panel on the
facing page for several drafts before a reordering put the rows next to each
other and made it visible.

    python3 figaudit.py <rendered.pdf>

Builds the set of quantities the ledger can produce, at the precision the paper
prints them, then reports every distinct dollar figure in the document that is
NOT in that set. A figure being absent does not make it wrong - the paper also
prints statutory amounts, Medicare premiums and CBO totals that this model
never computes - so the output is a list to read, not a pass or a fail. What it
catches is the figure that used to come from the ledger and no longer matches
it.
"""
import re
import sys
from collections import defaultdict

import pymupdf

import inc

MONEY = re.compile(r"\$\d[\d,]*(?:\.\d\d)?")


def ledger_values():
    """Everything the model can say, keyed by its printed form."""
    c, d = inc.c24, inc.c30
    v = defaultdict(list)

    def add(x, what):
        v[f"${x:,.2f}"].append(what)
        if abs(x - round(x)) < 5e-3:
            v[f"${round(x):,.0f}"].append(what)

    for nm, x in (("ffs", c.ffs), ("mco", c.mco), ("dual", c.dual),
                  ("plan admin", c.adm_marg), ("earnings", c.earnings),
                  ("mco admin", c.mco_adm), ("dual admin", c.dual_adm),
                  ("fraud", c.fraud), ("medicare premiums", c.medicare),
                  ("admin", c.admin), ("oversight", c.oversight)):
        add(x, f"FY2024 {nm}")
    for nm, x in (("ffs", d.ffs), ("mco", d.mco), ("dual", d.dual),
                  ("plan admin", d.adm_marg), ("earnings", d.earnings),
                  ("fraud", d.fraud), ("medicare premiums", d.medicare)):
        add(x, f"FY2030 {nm}")
    for k in c.node:
        add(c.node[k], f"FY2024 {k}")
        add(d.node[k], f"FY2030 {k}")
        add(c.node[k] - d.node[k], f"fall in {k}")
    add(sum(c.node.values()) - c.fraud, "FY2024 services delivered")
    add(sum(d.node.values()) - d.fraud, "FY2030 services delivered")
    add(c.ffs + c.mco + c.dual - c.adm_marg - c.earnings, "FY2024 claims paid")
    add(d.ffs + d.mco + d.dual - d.adm_marg - d.earnings, "FY2030 claims paid")
    for g in inc.G:
        add(inc.BY_G[g], f"FY2024 {g}")
        add(inc.BY_G30[g], f"FY2030 {g}")
        add(inc.LOSS_G[g], f"fall for {g}")
        add(inc.LOSS_G_K["coverage"][g], f"coverage fall for {g}")
        add(inc.LOSS_G_K["rate"][g], f"rate fall for {g}")
    add(sum(inc.LOSS_G_K["coverage"].values()), "coverage fall, total")
    add(sum(inc.LOSS_G_K["rate"].values()), "rate fall, total")
    add(inc.pool, "the pool the provision logic allocates")
    add(inc.MSP_BILL, "the Medicare Savings bill")

    import cover_data
    D = cover_data.load(federal=True)
    for l in D["levers"]:
        add(l["amt"], f"provision: {l['label']}")
    for p in D["phases"]:
        add(p["v24"], f"anchor FY2024 {p['head']}")
        add(p["v30"], f"anchor FY2030 {p['head']}")
    add(D["gross"], "removed by the law")
    add(D["rebate"], "overhead returned")
    return v


def main(pdf):
    known = ledger_values()
    doc = pymupdf.open(pdf)
    seen = defaultdict(list)
    for n, page in enumerate(doc, start=1):
        for m in MONEY.finditer(re.sub(r"\s+", " ", page.get_text())):
            seen[m.group(0)].append(n)

    matched, unmatched = [], []
    for fig, pages in sorted(seen.items(),
                             key=lambda kv: -len(set(kv[1]))):
        (matched if fig in known else unmatched).append((fig, sorted(set(pages))))

    print(f"{len(seen)} distinct dollar figures in the document\n")
    print(f"{len(matched)} reproduce a ledger quantity exactly")
    print(f"{len(unmatched)} do not, and want reading:\n")
    for fig, pages in unmatched:
        print(f"  {fig:>12}  pages {', '.join(map(str, pages))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
