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

from dataclasses import replace

import provider_mix as PM
from ledger import (ABSENT, CLIENT, DERIVED, Fig, Ledger, MEASURED, MODELLED,
                    Matrix, Payer, Peel)

CMS64 = "CMS-64 FY2024 national totals"
V = "FY2024"
B = "total computable"

NODES = ["Long-term care", "Hospitals", "Other", "Physicians & clinics",
         "Behavioral health", "Rx drugs"]

# The provider phase is computed, not pasted. See provider_mix.py for the
# three sources, their three vintages, and the behavioral health mapping.
_ffs, _mco, _dual, _node = PM.FFS_N, PM.MCO_N, PM.DUAL_N, PM.NODE


def _m(v, note=""):
    return Fig(v, source=CMS64, vintage=V, basis=B, status=MEASURED, note=note)


# Signing is a lookup, not a stamp. See signatures.py for why. The register
# holds the exact value each figure was agreed at; a figure that has moved
# since is not signed, and `check` fails the build rather than letting a
# signature travel onto a number nobody has seen.
from signatures import REVIEW, SIGNED, UNSIGNED


def _sign(L: Ledger) -> Ledger:
    """Attach the register's signature to every figure still at its signed value."""
    def s(f, key):
        if key in UNSIGNED or f.status not in (MEASURED, MODELLED):
            return f
        if key not in SIGNED:
            return f                      # never signed; coverage reports it
        signed_at = SIGNED[key]
        if f.value is None or abs(f.value - signed_at) > 1e-9:
            # Moved since it was agreed. Record the signature AND the old
            # value so `lapsed` fires and names both numbers.
            return replace(f, verified=REVIEW, verified_value=signed_at)
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
              capitation=_m(40.06), care=Fig.derived(35.65, ("payer.mco.capitation", "payer.mco.admin",
                                       "payer.mco.margin")),
              admin=Fig(3.81, source="EN-15", vintage=V, basis=B, status=MEASURED),
              margin=Fig(0.60, status=MODELLED,
                         note="EN-43. Public-company earnings $0.76 in total, carved "
                              "across the two capitated lanes in proportion to plan "
                              "administration. The $0.76 itself has no primary source; "
                              "the intended derivation is a segment-level allocation "
                              "from the Medicaid segments of the publicly traded "
                              "plans' 10-K filings, and that work is open.")),
        Payer("dual", "Dual MCO capitation", "dual",
              capitation=_m(10.89), care=Fig.derived(9.69, ("payer.dual.capitation", "payer.dual.admin",
                                      "payer.dual.margin")),
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
        # Derived, and modelled all the way down: no one publishes a
        # national split of capitation by service, so a node total cannot be
        # measured. The cent on long-term care is a rounding residue, not a
        # published figure disagreeing with its parts.
        col_margin={k: Fig.derived(
            v, tuple(f"claims.cell.{r}.{k}" for r in ("mco", "dual", "ffs")),
            note="Rounded node totals forced to the money arriving; the "
                 "residue falls on the largest upward rounding.")
            for k, v in _node.items()},
        cell={**{("ffs", k): _m(v) for k, v in _ffs.items()},
              **{("mco", k): Fig(v, status=MODELLED,
                                 note="HMA T-MSIS managed-care key, CY2021, "
                                      "less the MACPAC behavioral health "
                                      "carve, CY2023. provider_mix.py.")
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
        col_margin={k: Fig.derived(_node[k], (f"claims.col.{k}",)) for k in NODES},
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
