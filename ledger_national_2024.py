# ledger_national_2024.py — the national as-is, in the Ledger shape.
#
# Same numbers as instances.AS_IS_2024. Nothing is revalued here; this is the
# existing ledger expressed with its provenance attached, so the register can
# be generated rather than maintained and so a figure without a source fails
# the build.
#
# Where a figure's provenance is weaker than the artifact currently implies,
# it is written down as it is rather than as we would like it. EN-43 is the
# example: the $0.76 earnings carve has no primary source, and it now says so
# in the ledger instead of in a document beside it.

from ledger import (ABSENT, CLIENT, DERIVED, Fig, Ledger, MEASURED, MODELLED,
                    Matrix, Payer, Peel)

CMS64 = "CMS-64 FY2024 national totals"
V = "FY2024"
B = "total computable"

NODES = ["Long-term care", "Hospitals", "Other", "Physicians & clinics",
         "Behavioral health", "Rx drugs"]

_ffs = {"Long-term care": 19.72, "Hospitals": 8.68, "Other": 4.95,
        "Physicians & clinics": 2.87, "Behavioral health": 3.48, "Rx drugs": 1.38}
_mco = {"Long-term care": 6.93, "Hospitals": 7.84, "Other": 6.59,
        "Physicians & clinics": 7.68, "Behavioral health": 4.74, "Rx drugs": 1.87}
_dual = {"Long-term care": 1.89, "Hospitals": 2.14, "Other": 1.79,
         "Physicians & clinics": 2.08, "Behavioral health": 1.29, "Rx drugs": 0.51}
# Published node totals. NOT the sum of the three components: the components
# are rounded to the cent and the totals are published, so long-term care is
# 28.53 where its parts add to 28.54. Deriving the total from the parts moved a
# band by a tenth of a unit and the byte-identity proof caught it. The gate's
# tolerance absorbs the difference; the renderer does not.
_node = {"Long-term care": 28.53, "Hospitals": 18.66, "Other": 13.33,
         "Physicians & clinics": 12.63, "Behavioral health": 9.51,
         "Rx drugs": 3.76}


def _m(v, note=""):
    return Fig(v, source=CMS64, vintage=V, basis=B, status=MEASURED, note=note)


# JW, 2026-09-15: the national baseline has been through the endnote register,
# two redlines and a shipped draft. Signed as verified against the FY2024
# vintage. Re-anchoring to a later vintage, or editing any figure, ends the
# signature automatically.
#
# ONE EXCLUSION, and it is deliberate. The public-company earnings carve is
# EN-43, which is OPEN and which states in terms that $0.76 has no primary
# source behind it. Signing it would assert that someone opened a source that
# the endnote register says does not exist. It stays unsigned until the NAIC
# and 10-K work closes it.
REVIEW = "2026-09-15 JW"
UNSIGNED = {"payer.mco.margin", "payer.dual.margin"}


def _sign(L: Ledger) -> Ledger:
    """Sign every measured and modelled figure except the EN-43 carve."""
    def s(f, key):
        if key in UNSIGNED or f.status not in (MEASURED, MODELLED):
            return f
        return f.sign(REVIEW)

    for k in L.sources:
        L.sources[k] = s(L.sources[k], f"source.{k}")
    L.scale = s(L.scale, "scale")
    for pl in L.peels:
        pl.amount = s(pl.amount, f"peel.{pl.key}")
    for p in L.payers:
        for fld in ("capitation", "care", "admin", "margin"):
            setattr(p, fld, s(getattr(p, fld), f"payer.{p.key}.{fld}"))
    for m in [L.claims] + ([L.beneficiaries] if L.beneficiaries else []):
        for k in list(m.row_margin):
            m.row_margin[k] = s(m.row_margin[k], f"{m.name}.row.{k}")
        for k in list(m.col_margin):
            m.col_margin[k] = s(m.col_margin[k], f"{m.name}.col.{k}")
        for k in list(m.cell):
            m.cell[k] = s(m.cell[k], f"{m.name}.cell.{k[0]}.{k[1]}")
    return L


def build() -> Ledger:
    payers = [
        Payer("mco", "MCO capitation", "mco",
              capitation=_m(40.06), care=Fig.derived(35.65, ("mco.capitation", "mco.retention")),
              admin=Fig(3.81, source="EN-15", vintage=V, basis=B, status=MEASURED),
              margin=Fig(0.60, status=MODELLED,
                         note="EN-43. Public-company earnings $0.76 in total, carved "
                              "across the two capitated lanes in proportion to plan "
                              "administration. The $0.76 itself has no primary source; "
                              "the intended derivation is a segment-level allocation "
                              "from the Medicaid segments of the publicly traded "
                              "plans' 10-K filings, and that work is open.")),
        Payer("dual", "Dual MCO capitation", "dual",
              capitation=_m(10.89), care=Fig.derived(9.69, ("dual.capitation", "dual.retention")),
              admin=Fig(1.04, source="EN-15", vintage=V, basis=B, status=MEASURED),
              margin=Fig(0.16, status=MODELLED, note="EN-43, as above.")),
        Payer("ffs", "Fee-for-service", "ffs",
              capitation=_m(41.08), care=_m(41.08,
                  "Rule A: fee-for-service has no payer and no retention. It runs "
                  "through the payer phase unchanged."),
              admin=Fig.absent("fee-for-service has no plan administration"),
              margin=Fig.absent("fee-for-service has no margin")),
    ]

    claims = Matrix(
        name="claims",
        rows=["mco", "dual", "ffs"],
        cols=NODES,
        row_margin={"mco": Fig.derived(35.65, ("payer.mco.care",)),
                    "dual": Fig.derived(9.69, ("payer.dual.care",)),
                    "ffs": Fig.derived(41.08, ("payer.ffs.care",))},
        col_margin={k: _m(v, "published node total") for k, v in _node.items()},
        cell={**{("ffs", k): _m(v) for k, v in _ffs.items()},
              **{("mco", k): Fig(v, status=MODELLED,
                                 note="Managed-care service mix. Carried from the "
                                      "national managed-care allocation.")
                 for k, v in _mco.items()},
              **{("dual", k): Fig(v, status=MODELLED,
                                  note="Dual-plan service mix, same basis.")
                 for k, v in _dual.items()}},
    )

    groups = {"Children": 13.48, "Adults": 29.56, "Disabled": 24.98, "Aged": 18.41}
    beneficiaries = Matrix(
        name="beneficiaries",
        rows=list(groups),
        cols=NODES,
        row_margin={g: Fig(v, source="MACStats Exhibit 21", vintage="FY2023",
                           basis="eligibility group totals", status=MEASURED)
                    for g, v in groups.items()},
        col_margin={k: Fig.derived(_node[k], ("claims.cols",)) for k in NODES},
        cell={},   # interior not carried here: see note
        note="Interior unallocated in this ledger. The rendered pies are fit by "
             "iterative proportional fitting to both margins from a seed pattern "
             "that carries no citation. MACStats Exhibit 18 publishes the national "
             "cross-tab directly and is the candidate replacement; it is a "
             "fee-for-service basis and would not cover the capitated half. "
             "Unruled.",
    )

    return _sign(Ledger(
        geography="United States",
        year="FY2024",
        scenario="as_is",
        scale=Fig(1.0, source=CMS64, vintage=V,
                  basis="normalised to $100 of total computable Medicaid spending",
                  status=DERIVED),
        sources={"federal": _m(64.70, "blended federal share"),
                 "state": _m(35.30, "non-federal share")},
        peels=[
            Peel("admin", "Administration", _m(5.07), "STATE_AGENCY",
                 reach="STATE_AGENCY", kind="admin"),
            Peel("medicare", "Medicare premiums", _m(2.90), "STATE_AGENCY",
                 reach="STATE_AGENCY", kind="return"),
            Peel("fraud", "Documented fraud", _m(0.15,
                 "providers receive it, it is not services delivered"),
                 "PROVIDERS", reach="PROVIDERS", kind="fraud"),
        ],
        payers=payers,
        nodes=NODES,
        claims=claims,
        beneficiaries=beneficiaries,
        declarations=[
            "beneficiaries: the interior of the group-by-service allocation is "
            "unallocated in the ledger.",
        ],
    ))
