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

# D-95. The horizontal taper family runs one phase further up than the cover
# does. Figure 8's whole subject is the provider tax leaving the federal column
# BEFORE the two shares merge, and the cover deliberately starts at the agency,
# so a figure in the cover's language had nowhere to put it. load(federal=True)
# prepends the band and moves the provider tax marker into it. The cover itself
# is unchanged: JW, the cover carries the ecosystem from the agency down.
FED_PHASE = ("FEDERAL", "Federal and state shares")

PHASES = [("STATE_AGENCY", "State agency"),
          ("DISBURSE", "Disbursements"),
          ("CLAIMS", "Claims to providers"),
          ("BENEFICIARY", "Beneficiaries")]

# The seven P.L. 119-21 levers, in the order the money meets them, with the
# phase each bites at and who carries the loss. The prose is editorial; every
# number beside it is read from the ledger below.
# D-101. Each provision declares TWO places, and they are not the same thing.
#
#   phase    where the provision BITES: where the ribbon peels off the trunk,
#            and where its marker sits on every diagram.
#   reach    where the dollar WOULD HAVE GOT TO if the law had not taken it.
#            This is the column Table 2 prints, and the italic line under each
#            label on the panels.
#
# For six of the seven they are the same phase, which is why one field did the
# work of two for so long and why the first version of the build check
# compared the wrong pair. Six-month renewals is the exception and the reason
# this split exists: the person is already enrolled and already attributed to
# a plan, so what is lost is a premium a PAYER would have received. Work
# reporting is the opposite case - people who never enrol, so the dollar stops
# at disbursement and never reaches a payer at all. Collapsing the two erased
# the distinction this paper spends a page making.
#
# It was declared at disbursements only because the cover taper had no payer
# column to put it in. D-100 gave the family one.
#
# The Medicare Savings rule (D-99) is the same shape the other way round: it
# leaves the agency's budget and reaches a beneficiary, and Table 2 prints the
# reach. render_v6_2.py checks the manuscript against `reach`, not `phase`.
WHO = {
    "Provider tax limits": ("State agency", "State budgets", "federal match never drawn", "Federal band"),
    "Everything else": ("State agency", "Enrollees", "home equity, cost sharing"),
    "Work reporting": ("Disbursements", "People who will not enroll", "largest single lever"),
    "Six-month renewals": ("Disbursements", "People who will not renew", "coverage lapses at redetermination", "Payer"),
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


def load(federal=False):
    c24 = compose(NAT.build(), views.V_NAT)
    c30 = compose(N30.build("mixed"), views.V_2030, prior=NAT.build())
    a24, a30 = _anchors(c24), _anchors(c30)
    phases = []
    for col, head in ([FED_PHASE] + PHASES if federal else PHASES):
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
        row = WHO[n]
        phase, who, note = row[0], row[1], row[2]
        reach = row[3] if len(row) > 3 else phase
        if federal and n == "Provider tax limits":
            phase = FED_PHASE[1]
        levers.append(dict(key=n, label=OF.label_of(n), amt=amt[n],
                           phase=phase, who=who, note=note, reach=reach))

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
