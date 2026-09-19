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
B = "money budgeted to Medicaid at the state agency"

EX16 = ("MACPAC, MACStats: Medicaid and CHIP Data Book, Exhibit 16, Medicaid "
        "Spending by State, Category, and Source of Funds, FY 2024, published "
        "February 2026; MACPAC analysis of CMS-64 FMR net expenditure data as "
        "of 3 June 2025")
EX17 = ("MACPAC, MACStats: Medicaid and CHIP Data Book, Exhibit 17, Total "
        "Medicaid Benefit Spending by State and Category, FY 2024, published "
        "February 2026; same CMS-64 pull as Exhibit 16")

# D-70. The $100 is struck where the money becomes a Medicaid dollar: at the
# state agency, budgeted and cost-allocated. It is NOT struck at appropriation.
# Exhibit 16, total row, FY2024, in millions:
#
#   benefits                              908,839
#   state programme administration         40,360
#   Medicaid Fraud Control Units              497   } federal oversight, 75% FFP
#   survey and certification of facilities    468   }
#   ------------------------------------------------
#   the hundred                           950,164
#   Vaccines for Children                   7,239     100% federal, D-71
#   ------------------------------------------------
#   total Medicaid                        957,403
#
# The old hundred was the bottom line. Fifteen percent of the first decrement
# the reader met was a vaccine purchase wearing the word overhead. S-099.
BENEFITS_M   = 908839.0
ADMIN_M      = 40360.0
MFCU_M, SNC_M = 497.0, 468.0
VFC_M        = 7239.0
MEDICARE_M   = 27774.0            # Exhibit 17, Medicare premiums and coinsurance
FED_M, ST_M  = 620355.0, 337048.0 # Exhibit 16, total row, both columns

HUNDRED_M = BENEFITS_M + ADMIN_M + MFCU_M + SNC_M     # 950,164
PER_DOLLAR = HUNDRED_M / 100.0                        # $M per $1 of the hundred
OLD_HUNDRED_M = HUNDRED_M + VFC_M                     # what the panel used to be
RESCALE = OLD_HUNDRED_M / HUNDRED_M                   # x1.00762


def _per100(m: float) -> float:
    return m / PER_DOLLAR


def _rebase(L):
    """Every figure below the state agency was struck against the old hundred.
    Changing the denominator is a change of units, not of measurement, so each
    one moves by the same factor. Sources and peels are not touched here: they
    are re-derived from Exhibit 16 dollars above."""
    def r(f):
        return f if f.value is None else replace(f, value=f.value * RESCALE)
    for p in L.payers:
        for fld in ("capitation", "care", "admin", "margin"):
            setattr(p, fld, r(getattr(p, fld)))
    for m in [L.claims] + ([L.beneficiaries] if L.beneficiaries else []):
        for d in (m.row_margin, m.col_margin, m.cell):
            for k in list(d):
                d[k] = r(d[k])
    for x in L.peels:
        if x.key == "fraud":
            x.amount = r(x.amount)
    return L


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

    return _sign(_rebase(Ledger(
        geography="United States",
        year="FY2024",
        scenario="as_is",
        scale=Fig(PER_DOLLAR, source=EX16, vintage=V,
                  basis="$M per $1 of the hundred budgeted to Medicaid",
                  status=MEASURED,
                  note="$950,164M read from Exhibit 16 and divided by 100. It "
                       "was carried as DERIVED, which made it report 'derived "
                       "from nothing named' and left it unsignable."),
        # These sum to 100.76, not 100. The vaccine money peels before the
        # hundred is struck, so more enters than is budgeted. D-70, S-102.
        sources={"federal": Fig(_per100(FED_M), source=EX16, vintage=V, basis=B,
                                status=MEASURED,
                                note="federal appropriation entering, $620,355M. "
                                     "Not the blended share: once the vaccine "
                                     "money peels, the dollar the agency holds "
                                     "is 64.53 percent federal."),
                 "state": Fig(_per100(ST_M), source=EX16, vintage=V, basis=B,
                              status=MEASURED,
                              note="non-federal appropriation entering, $337,048M")},
        peels=[
            Peel("vfc", "Vaccines for Children",
                 Fig(_per100(VFC_M), source=EX16, vintage=V, basis=B,
                     status=MEASURED,
                     note="EN-49. $7,239M, 100 percent federal, dash in the "
                          "state column. Never cost-allocated, so it cannot "
                          "peel off blended money. Terminates at CDC; the doses "
                          "reach providers as goods and the administration fee "
                          "is already inside the hundred."),
                 "FEDERAL", reach="FEDERAL", kind="return", outside=True),
            Peel("admin", "Administration",
                 Fig(_per100(ADMIN_M), source=EX16, vintage=V, basis=B,
                     status=MEASURED,
                     note="state programme administration only, $40,360M"),
                 "STATE_AGENCY", reach="STATE_AGENCY", kind="admin"),
            Peel("oversight", "Federal oversight",
                 Fig(_per100(MFCU_M + SNC_M), source=EX16, vintage=V, basis=B,
                     status=MEASURED,
                     note="EN-50. Fraud Control Units $497M and survey and "
                          "certification $468M, both matched at 75 percent, "
                          "drawn as one arrow."),
                 "STATE_AGENCY", reach="STATE_AGENCY", kind="admin"),
            Peel("medicare", "Medicare premiums",
                 Fig(_per100(MEDICARE_M), source=EX17, vintage=V, basis=B,
                     status=MEASURED,
                     note="Medicare premiums and coinsurance, $27,774M"),
                 "STATE_AGENCY", reach="STATE_AGENCY", kind="return"),
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
    )))
