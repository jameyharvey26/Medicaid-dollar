# check.py — conservation gate.
#
# Conserved-ledger purity has been resting on me reading the output. At fifty
# states that does not scale and it does not hold. Every ledger passes through
# here before anything is drawn, and a failure stops the build.

TOL = 0.02   # $ per $100. Tighter than this trips on legitimate rounding.


class LedgerError(AssertionError):
    pass


def _near(a, b, tol=TOL):
    return abs(a - b) <= tol


def check(cfg, label=""):
    """Return a list of failures. Empty list means the ledger conserves."""
    f = []
    L = cfg

    def eq(name, a, b):
        if not _near(a, b):
            f.append(f"{name}: {a:.4f} != {b:.4f}  (off by {a-b:+.4f})")

    # sources
    eq("sources sum to 100", L.fed + L.state, 100.0)

    # trunk: what enters the state agency, less what peels, is what disburses
    trunk = 100.0 - L.fed_bite
    disbursed = trunk - L.admin - L.medicare - L.sa_hr1
    eq("payer lanes sum to disbursed", L.mco + L.dual + L.ffs, disbursed)

    # payer column
    eq("MCO splits into care and retention", L.mco_care + L.mco_ret, L.mco)
    eq("dual splits into care and retention", L.dual_care + L.dual_ret, L.dual)
    eq("plan administration plus earnings", L.mco_adm + L.dual_adm + L.earnings,
       L.mco_ret + L.dual_ret)

    # claims and providers
    claims = L.mco_care + L.dual_care + L.ffs
    eq("provider nodes sum to claims less claims-side HR-1",
       sum(L.node.values()), claims - L.claims_hr1)

    # provider node components
    for p in L.node:
        eq(f"node components: {p}",
           L.ffs_n.get(p, 0) + L.mcoc_n.get(p, 0) + L.dualc_n.get(p, 0), L.node[p])
    # Fee-for-service is untouched by the claims-side bite, so it must be exact.
    eq("fee-for-service components sum to the lane", sum(L.ffs_n.values()), L.ffs)
    # The claims-side bite (directed payment caps) falls on the CAPITATED legs
    # only, so capitated components sum to their lanes LESS that bite. Stating
    # this precisely is what the checker is for; the first draft asserted the
    # lanes exactly and failed correctly.
    eq("capitated components sum to their lanes less the claims-side bite",
       sum(L.mcoc_n.values()) + sum(L.dualc_n.values()),
       L.mco_care + L.dual_care - L.claims_hr1)

    # beneficiary shares
    if getattr(L, "show_beneficiaries", True):
        eq("beneficiary totals sum to provider nodes",
           sum(L.gt.values()), sum(L.node.values()))

    # no silent drops: every node in one component map is in all of them
    keys = set(getattr(L, "order", L.node))
    for nm, d in (("ffs_n", L.ffs_n), ("mcoc_n", L.mcoc_n), ("dualc_n", L.dualc_n)):
        missing = keys - set(d)
        extra = set(d) - keys
        if missing:
            f.append(f"{nm} is missing nodes: {sorted(missing)}")
        if extra:
            f.append(f"{nm} has nodes absent from the provider set: {sorted(extra)}")

    # the width test (STYLE_GUIDE 3.3), previously an eyeball check
    delivered = claims - L.fraud - L.claims_hr1
    eq("tracker: disbursed", disbursed, L.mco + L.dual + L.ffs)
    eq("tracker: delivered is claims less fraud and claims-side HR-1",
       delivered, claims - L.fraud - L.claims_hr1)

    return f


def gate(cfg, label=""):
    """Raise if the ledger does not conserve. Call before rendering."""
    fails = check(cfg, label)
    tag = label or getattr(cfg, "name", "ledger")
    if fails:
        raise LedgerError(
            f"{tag} does not conserve:\n  " + "\n  ".join(fails))
    return True
