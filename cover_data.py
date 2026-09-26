"""Cover data. Every figure derived from the build; nothing typed (S-105).

Four phases, by their COLUMN heading rather than the tracker's anchor name,
because the cover composites the Sankey's phases and the line's values and the
reader should see one vocabulary. The federal and state-government phases are
left off: JW, the cover carries the ecosystem from the agency down.
"""
import views
from compose import compose
import ledger_national_2024 as NAT
import ledger_national_2030 as N30
import tracker as TR
import outflows as OF

PHASES = [("STATE_AGENCY", "State agency"),
          ("DISBURSE", "Disbursements"),
          ("CLAIMS", "Claims to providers"),
          ("BENEFICIARY", "Beneficiaries")]

# The seven P.L. 119-21 levers, in the order the money meets them, with the
# phase each bites at and who carries the loss. The prose is editorial; every
# number beside it is read from the ledger below.
WHO = {
    "Provider tax limits": ("State agency", "State budgets", "federal match never drawn"),
    "Everything else": ("State agency", "Enrollees", "home equity, cost sharing"),
    "Work reporting": ("Disbursements", "People who will not enroll", "largest single lever"),
    "Six-month renewals": ("Disbursements", "People who will not renew", "coverage lapses at redetermination"),
    "Blocked Medicaid enrollment rule": ("Claims to providers", "People who would have had a paid claim", "2024 rule suspended"),
    "Directed payment caps": ("Claims to providers", "Hospitals, nursing facilities, academic centres", "rates not topped up"),
    "Blocked senior enrollment rule": ("Beneficiaries", "Dual eligibles", "they pay these Medicare costs themselves"),
}
ORDER = ["Provider tax limits", "Everything else", "Work reporting",
         "Six-month renewals", "Blocked Medicaid enrollment rule",
         "Directed payment caps", "Blocked senior enrollment rule"]


def _anchors(cfg):
    cap = {}
    real = TR.ledger
    def spy(subs, mx, mo=None, start=100.0):
        a, m = real(subs, mx, mo, start)
        cap["a"] = a
        return a, m
    TR.ledger = spy
    try:
        import sankey
        sankey.render(cfg)
    finally:
        TR.ledger = real
    return {a["x"]: a["value"] for a in cap["a"]}


def load():
    c24 = compose(NAT.build(), views.V_NAT)
    c30 = compose(N30.build("mixed"), views.V_2030, prior=NAT.build())
    a24, a30 = _anchors(c24), _anchors(c30)
    phases = []
    for col, head in PHASES:
        x = OF.anchor_x(col)
        phases.append(dict(col=col, head=head, v24=a24[x], v30=a30[x]))

    # The seven levers. Six come off the trunk as declared steps; directed
    # payment caps bites at the claims fan and is carried separately.
    # Five of the seven are declared trunk steps. Directed payment caps bites
    # at the claims fan; provider tax limits bites before the agency, so it is
    # a peel rather than a step. All three routes read the same ledger.
    amt = {st[0]: st[2] for st in c30.steps}
    amt[c30.claims_hr1_name] = c30.claims_hr1
    for spec in c30.subs_spec:
        if spec[4] == "Provider Tax":
            amt["Provider tax limits"] = float(spec[1])
    levers = []
    for n in ORDER:
        phase, who, note = WHO[n]
        levers.append(dict(key=n, label=OF.label_of(n), amt=amt[n],
                           phase=phase, who=who, note=note))

    gross = sum(l["amt"] for l in levers)
    net = phases[-1]["v24"] - phases[-1]["v30"]
    return dict(phases=phases, levers=levers, gross=gross, net=net,
                rebate=gross - net)


if __name__ == "__main__":
    d = load()
    for p in d["phases"]:
        print(f"{p['head']:22} {p['v24']:7.2f} -> {p['v30']:7.2f}   -{p['v24']-p['v30']:.2f}")
    print()
    for l in d["levers"]:
        print(f"{l['label']:34} {l['amt']:6.2f}  {l['phase']:20} {l['who']}")
    print(f"\ngross {d['gross']:.2f}   overhead rebate {d['rebate']:.2f}   net at care {d['net']:.2f}")
