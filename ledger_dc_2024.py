# ledger_dc_2024.py — the District of Columbia as-is, in the Ledger shape.
#
# WORKING. Every vintage in here is inherited from `ledger_dc.py`, whose own
# header says it is likely stale on several axes and that all vintages need
# re-checking before DC ships. Nothing here has been re-acquired yet. This
# file exists to prove the framework holds the shape JW asked for, not to
# publish a number.
#
# The shape it proves: named plans are Payers with `parent` set, so the same
# ledger answers the aggregate view and the zoom without a second graph and
# without the View being able to invent anything. Their capitation is measured.
# Their fan into provider nodes is absent, and absent is a state the matrix
# can hold, so research can fill it cell by cell whenever it lands.
#
# Two things that were in `ledger_dc.py` are deliberately not carried forward:
#
#   1. The national managed-care service mix applied to DC's plan care. It
#      would draw four plans with identical service profiles once the lane is
#      expanded, and HSCSN is a paediatric SSI plan. S-068.
#   2. The 75/25 split of dual and PACE capitation into long-term care and
#      wrap-around. It has no source and was not on the declared-absent list.
#
# Both now sit as unfilled cells with the absence declared.

from ledger import (Fig, Ledger, MEASURED, MODELLED, Matrix, Payer, Peel,
                    DERIVED)

SCALE = 43.72                # $M per $1 of the DC hundred
SPINE = "CMS-64 / MACStats FY2024 DC"
MCR = "DHCF managed care performance report"
V = "FY2024"
VMC = "CY2023"
B = "total computable"
STALE = ("Vintage inherited from build_sankey_dc.py and not re-acquired. "
         "Must be re-checked before DC ships.")

NODES = ["Long-term care", "Hospitals", "Physicians & clinics",
         "Wrap around services", "Rx drugs"]


def _s(v, note=""):
    return Fig(v, source=SPINE, vintage=V, basis=B, status=MEASURED,
               note=(note + " " + STALE).strip())


def _mc(v, note=""):
    return Fig(v, source=MCR, vintage=VMC, basis="capitation revenue",
               status=MEASURED, note=(note + " " + STALE).strip())


# ---- plan-level capitation ------------------------------------------------
# HSCSN is anchored at its own Medicaid capitation and the residual is split
# among the comprehensive plans by capitation-revenue share, because HSCSN's
# revenue is pure Medicaid while the comprehensive plans' still carries
# locally-funded Alliance and ICP enrollees. Splitting all four by raw revenue
# under-weights HSCSN (STATE_PLAYBOOK 3.3, the basis-mismatch case).
_rev = {"amerihealth": 841.0, "wellpoint": 425.3, "medstar": 411.2}
_clm = {"amerihealth": 755.5, "wellpoint": 348.5, "medstar": 379.6,
        "hscsn": 154.4}
_hscsn_rev = 184.0

mc_total = 1802 / SCALE
pace = 15 / SCALE
dsnp = 25 / SCALE
mco_cap = mc_total - pace - dsnp
ffs = 2250 / SCALE

_hscsn_cap = _hscsn_rev / SCALE
_resid = mco_cap - _hscsn_cap
_revT = sum(_rev.values())
_cap = {k: _rev[k] / _revT * _resid for k in _rev}
_cap["hscsn"] = _hscsn_cap
_care = {k: _cap[k] * (_clm[k] / (_rev[k] if k in _rev else _hscsn_rev))
         for k in _cap}

PLANS = [
    ("amerihealth", "AmeriHealth Caritas DC", "AmeriHealth Caritas District of Columbia, Inc."),
    ("wellpoint", "Wellpoint DC (formerly Amerigroup)", "Amerigroup District of Columbia, Inc."),
    ("medstar", "MedStar Family Choice DC", "MedStar Family Choice DC"),
    ("hscsn", "HSCSN", "Health Services for Children with Special Needs, Inc."),
]

RENAME = ("Amerigroup DC was renamed Wellpoint DC on 1 July 2025. A plan carries "
          "its present-day name with the former name in parentheses, so a reader "
          "recognises it today whatever year the ledger is. The licensed entity "
          "name is unchanged and is what NAIC and SEC filings are found under. "
          "DHCF's current managed care page lists two comprehensive plans, which "
          "suggests a consolidation after the ledger year; not yet confirmed.")

LEGACY_ABSENT = [
    "Beneficiary shares: DC group totals not in hand, column omitted",
    "Behavioral health: folded into wrap-around services in the DC source",
    "Public-company earnings and dual-plan retention: no DC figure",
    "Documented fraud: no DC figure",
]

# The two allocations carried by ledger_dc.py, reproduced verbatim for the
# byte-identity proof and for no other purpose.
_NATMIX = {"Long-term care": 8.82, "Hospitals": 9.98,
           "Physicians & clinics": 9.76 + 6.03,
           "Wrap around services": 8.38, "Rx drugs": 2.38}


def _legacy_alloc():
    t = sum(_NATMIX.values())
    care = sum(_care.values())
    mco_n = {p: care * _NATMIX[p] / t for p in NODES}
    dual_n = {p: 0.0 for p in NODES}
    dual_n["Long-term care"] = (pace + dsnp) * 0.75
    dual_n["Wrap around services"] = (pace + dsnp) * 0.25
    return mco_n, dual_n


def _cells(ffs_n, legacy):
    c = {("ffs", k): _s(v) for k, v in ffs_n.items()}
    if not legacy:
        return c
    mco_n, dual_n = _legacy_alloc()
    c.update({("mco", k): Fig(v, status=MODELLED, note="national mix, legacy")
              for k, v in mco_n.items()})
    c.update({("dual", k): Fig(v, status=MODELLED, note="75/25, legacy")
              for k, v in dual_n.items()})
    return c


def _cols(ffs_n, legacy):
    if not legacy:
        return {}
    mco_n, dual_n = _legacy_alloc()
    return {k: Fig.derived(ffs_n[k] + mco_n[k] + dual_n[k], ("cells",))
            for k in NODES}


def build(legacy_mix: bool = False) -> Ledger:
    """`legacy_mix=True` reproduces exactly what `ledger_dc.py` carried: the
    national managed-care service mix applied to DC's plan care, and the
    undeclared 75/25 split of the dual and PACE lanes. It exists so the
    refactor can be proved byte-identical before the correction is made, per
    S-064. It is not a fallback and nothing should ship from it."""
    payers = []

    payers.append(Payer(
        "mco", "MCO capitation", "mco",
        capitation=_s(mco_cap, "Managed-care lump less PACE and the D-SNP wrap."),
        care=Fig.derived(sum(_care.values()), ("plan care",)),
        admin=(Fig(mco_cap - sum(_care.values()), status=MODELLED,
                   note="legacy: whole retention labelled plan administration")
               if legacy_mix else
               Fig.absent("No DC figure divides plan retention into "
                          "administration and margin. The retention total is "
                          "measured; its split is not published.")),
        margin=(Fig(0.0, status=MODELLED, note="legacy: no earnings carve")
                if legacy_mix else Fig.absent("See admin."))))

    for key, label, entity in PLANS:
        note = RENAME if key == "wellpoint" else ""
        payers.append(Payer(
            key, label, "mco", parent="mco",
            capitation=_mc(_cap[key], note),
            care=_mc(_care[key], "Care fraction is the plan's own incurred "
                                 "claims over its capitation revenue."),
            admin=Fig.absent(f"{key}: retention is measured, its split into "
                             f"administration and margin is not published."),
            margin=Fig.absent(f"{key}: see admin."),
            entity=entity))

    payers.append(Payer(
        "dual", "Dual and PACE capitation", "dual",
        capitation=_s(pace + dsnp),
        care=_s(pace + dsnp, "No DC retention figure for these lanes, so "
                             "capitation runs through to care."),
        admin=(Fig(0.0, status=MODELLED, note="legacy: no dual retention")
               if legacy_mix else
               Fig.absent("No DC retention figure for the dual or PACE lanes.")),
        margin=(Fig(0.0, status=MODELLED, note="legacy: no dual earnings")
                if legacy_mix else Fig.absent("See admin."))))
    payers.append(Payer(
        "united", "UnitedHealthcare District Dual Choice", "dual", parent="dual",
        capitation=Fig(dsnp, source="DC budget book", vintage=V,
                       basis="Medicaid wrap only", status=MODELLED,
                       note="Medicaid wrap around a Medicare Advantage D-SNP. "
                            "Medicare pays the acute care, so the Medicaid band "
                            "is thin. A budget-book Dual Choice line that bundles "
                            "Medicare A/B/D is not this number."),
        care=Fig(dsnp, status=MODELLED, note="No retention figure; capitation "
                                             "runs through to care."),
        entity="UnitedHealthcare Insurance Company"))
    payers.append(Payer(
        "pace", "PACE", "pace", parent="dual",
        capitation=Fig(pace, source=SPINE, vintage=V, basis=B, status=MODELLED,
                       note="Order of magnitude. Edenbridge is new and small. "
                            "CMS-64 files PACE under managed care, so it is "
                            "carved out of the lump."),
        care=Fig(pace, status=MODELLED, note="No retention figure.")))

    payers.append(Payer(
        "ffs", "Fee-for-service", "ffs",
        capitation=_s(ffs), care=_s(ffs, "Rule A: no payer, no retention."),
        admin=Fig.absent("fee-for-service has no plan administration"),
        margin=Fig.absent("fee-for-service has no margin")))

    _ffs_n = {"Long-term care": 1236 / SCALE, "Physicians & clinics": 406 / SCALE,
              "Hospitals": 297 / SCALE, "Wrap around services": 222 / SCALE,
              "Rx drugs": 89 / SCALE}

    claims = Matrix(
        name="claims",
        rows=["mco", "dual", "ffs"],
        cols=NODES,
        row_margin={"mco": Fig.derived(sum(_care.values()), ("payer.mco.care",)),
                    "dual": Fig.derived(pace + dsnp, ("payer.dual.care",)),
                    "ffs": Fig.derived(ffs, ("payer.ffs.care",))},
        col_margin=_cols(_ffs_n, legacy_mix),
        cell=_cells(_ffs_n, legacy_mix),
        note="Fee-for-service itemises from the spine. The capitated rows are "
             "unallocated: DC does not publish managed-care spending by service "
             "category, and the national mix is not a substitute at plan "
             "resolution. Candidate sources not yet worked: DHCF encounter data, "
             "plan financial filings, MLR reporting, NAIC Title XIX exhibits.",
    )

    return Ledger(
        geography="District of Columbia",
        year="FY2024",
        scenario="as_is",
        scale=Fig(SCALE, source=SPINE, vintage=V,
                  basis="$M of total computable DC Medicaid per $1",
                  status=MEASURED, note=STALE),
        sources={"federal": _s(73.17, "blended, including expansion"),
                 "state": _s(26.83, "local share")},
        peels=[
            Peel("admin", "Administration", _s(234 / SCALE), "STATE_AGENCY",
                 reach="STATE_AGENCY", kind="admin"),
            Peel("medicare", "Medicare premiums", _s(86 / SCALE), "STATE_AGENCY",
                 reach="STATE_AGENCY", kind="return"),
        ],
        payers=payers,
        nodes=NODES,
        claims=claims,
        beneficiaries=None,
        declared=([] if legacy_mix else
                  ["claims:mco", "claims:dual"]) + [
            "mco", "dual", "ffs", "amerihealth", "wellpoint", "medstar",
            "hscsn", "united", "pace"],
        declarations=LEGACY_ABSENT if legacy_mix else [
            "claims row mco: DC does not publish managed-care spending by "
            "service category. The fan out of the capitated lanes is absent.",
            "claims row dual: as above, for the D-SNP wrap and PACE.",
            "mco: plan retention is measured in total; its split into "
            "administration and margin is not published for DC.",
            "dual: no retention figure for the D-SNP wrap or PACE.",
            "amerihealth, wellpoint, medstar, hscsn: retention split not published.",
            "united, pace: retention split not published.",
            "Behavioral health is not a separate node. The DC source folds it "
            "into wrap-around services and into the capitated lump.",
            "Documented fraud: no DC figure.",
            "Beneficiary shares: no matrix built. MACStats Exhibit 21 carries a "
            "state dimension and is the route in.",
        ],
        note="Every vintage inherited and unverified. " + STALE,
    )
