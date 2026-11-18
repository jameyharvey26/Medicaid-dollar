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
from basis_dc import (DC_ADMIN_M, DC_DEDTAX_M, DC_FED_M, DC_MEDICARE_M,
                      DC_STATE_M, DC_TOTAL_M, DHCF_BUDGET, EX16, EX17,
                      SCALE, DC_CAP_NET_M, DC_FFS_M, DC_FFS_NODES_M, DC_NET,
                      DC_FFS_GROSS_M, DC_CAP_M, DC_COLL_M)

SPINE = "CMS-64 / MACStats FY2024 DC"
# RE-ACQUIRED 2026-09-15. Phase 1 and the first half of Phase 2 of
# ACQUISITION.md. The exhibit publishes dollars, not shares, so DC's cost
# allocation is DERIVED from two measured dollar figures rather than read off
# the page. Recording it as measured would credit the source with a number it
# does not print.
#
#   Total Medicaid, DC, FY 2024   $4,372M   ->  SCALE, below
#     federal                     $3,199M   ->  source.federal
#     state                       $1,173M   ->  source.state
#   State program administration    $234M   ->  peel.admin
#
# The dollars above are measured and are typed. The per-$100 figures are not
# typed anywhere: each is divided by SCALE at the point of use, so a revision
# to a dollar moves the share with it. S-105.
#
# The exhibit's own note: figures may change if a state revises its
# expenditure data after 29 May 2024.

# $M per $1 of the DC hundred. Derived from the measured total, not typed:
# a revised Exhibit 16 moves every per-$100 figure on the DC panel through
# this one line. Convention 2026-09-19, JW: derive in code, never type an
# output. See typedfigures.py.

# RE-ACQUIRED 2026-09-18. Second half of Phase 2 of ACQUISITION.md. Exhibit 17
# is the benefit-category companion to Exhibit 16: same CMS-64 FMR pull, same
# certification date of 3 June 2025, same FY2024 vintage. DC's row reconciles
# to the dollar against Exhibit 16.
#
#   Fee-for-service, nine columns        $2,260M
#   Managed care and premium assistance  $1,802M
#   Medicare premiums and coinsurance       $86M   ->  peel.medicare
#   Collections                            -$10M
#   Total spending on benefits           $4,138M
#   plus state program administration      $234M
#   = total computable, Exhibit 16       $4,372M
#
# The category is "Medicare premiums and coinsurance," not premiums alone.

# ---- the non-federal share is not one kind of money -----------------------
# Exhibit 16 reports a single non-federal share. DC's own appropriation splits
# it across four funds, and one of them is not a general-fund appropriation at
# all: Dedicated Taxes are provider assessments, levied on the hospitals and
# nursing facilities that sit at the right-hand end of this diagram, used as
# the non-federal share, matched, and paid back to those same provider classes.
# D.C. Code sets them out as four instruments: a hospital inpatient provider
# fee on net patient revenue, a hospital outpatient provider fee on gross
# patient revenue, the Healthcare Provider Tax on nursing facilities, and the
# ICF-IDD assessment that funds the Stevie Sellows Quality Improvement Fund.
# The statutes tie them to Medicaid rates explicitly - the inpatient fee exists
# to hold fee-for-service at 98 percent of cost.
#
# Not itemised: no FY2024 breakdown has been found that sums across the four
# instruments, so the band is named in kind and not line by line.
#
# Basis warning. The dedicated-tax figure is an appropriation and the state
# share is CMS-64, so the local-appropriation residual has parents in two
# accountings and is DERIVED, not measured. Cross-checked two ways: dedicated
# taxes are 9.81% of the budget's local funds, which applied to the state share
# agrees with direct division to the cent.


def _x(v, note=""):
    """A figure re-acquired from Exhibit 16. Carries no STALE note."""
    return Fig(v, source=EX16, vintage=V, basis=B, status=MEASURED, note=note)


def _x17(v, note=""):
    """A figure re-acquired from Exhibit 17. Carries no STALE note."""
    return Fig(v, source=EX17, vintage=V, basis=B, status=MEASURED, note=note)
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


# D-150. The lanes come from basis_dc now, net of collections on D-83's
# pro-rata key. They used to be typed here as 1802 and 2250, which carried the
# whole collections line inside the fee-for-service half and, below, inside
# one service node. See basis_dc.py, COLLECTIONS.
mc_total = DC_CAP_NET_M / SCALE
# PACE and the D-SNP wrap are two MODELLED constants, not readings. They are
# netted on the same factor as the lane they are carved out of, so the carve
# does not quietly restore gross dollars to a netted lane.
pace = 15 * DC_NET / SCALE
dsnp = 25 * DC_NET / SCALE
mco_cap = mc_total - pace - dsnp
ffs = DC_FFS_M / SCALE

# ===========================================================================
# PLAN-LEVEL FIGURES — each plan's own Title XIX line, CY2024
# ===========================================================================
#
# REPLACES the capitation-revenue split of 2026-09. That split read each
# plan's TOTAL capitation revenue off DHCF's CY2023 managed care report,
# anchored HSCSN separately and apportioned the residual, because the
# comprehensive plans' revenue carried locally funded Alliance and ICP
# enrollees while HSCSN's did not — the basis-mismatch case in
# STATE_PLAYBOOK 3.3.
#
# THAT PROBLEM DISSOLVES on the Title XIX column. Every plan's statement
# reports Medicaid separately from everything else it writes, so all four sit
# on one basis and no plan has to be anchored around the others. The special
# case goes away rather than being worked around, which is why this is a
# better split and not just a newer one.
#
# WHAT EACH PLAN'S FIGURE IS, because it is NOT the same line in each
# statement and a reader is entitled to know which:
#
#   AmeriHealth  a DC-only entity. Its Analysis of Operations publishes the
#                Title XIX column in full, so premium, care and both expense
#                lines are read straight off it. Nothing is apportioned.
#   Wellpoint    a DC-only entity writing commercial business as well. The
#                Title XIX column carries premium and care; the two expense
#                lines are published only for the entity, so they are
#                apportioned by Title XIX's share of earned revenue. The
#                apportionment is MODELLED and is declared.
#   MedStar      NOT a DC-only entity. MedStar Family Choice, Inc. writes
#                $920.1M of Title XIX across two jurisdictions, $545.0M of it
#                in Maryland. The DC figure is Schedule T, whose own note
#                reads "actual premiums per state". Expenses are published
#                for the entity only and are apportioned by DC's share of
#                Title XIX premium. Taking the entity's Title XIX column
#                whole would put Maryland's Medicaid inside DC's hundred.
#   HSCSN        CY2023, AND THIS IS A MIXED VINTAGE ON THE PLATE. See below.
#
# PREMIUM IS EARNED, not written. Wellpoint's Title XIX net premium income is
# $337.6M against a $30.3M change in unearned reserves; the earned figure is
# what the year's care was bought with and what the other plans' figures
# already are.
NAIC24 = ("NAIC annual statement, CY2024, Title XIX Medicaid column, "
          "Analysis of Operations by Lines of Business")
NAIC24_T = ("NAIC annual statement, CY2024, Schedule T, Premiums and Other "
            "Considerations Allocated by States and Territories, District of "
            "Columbia row, Medicaid Title XIX")

# HSCSN, declared rather than quietly mixed. JW, 2026-10-29: HSCSN is not
# really an MCO. It predates the managed care regulations and its reporting
# obligations are different in kind, so there is no CY2024 annual statement to
# read a Title XIX column off. It reports to DHCF, and that is where the
# figure will come from; chasing it is on the acquisition list and is not done
# here. Until then HSCSN sits on CY2023 while the other three sit on CY2024.
#
# This is a real defect in the panel, not a rounding matter: one plan of four
# is a year behind the rest, and a plan president reading their own name will
# be comparing it against figures from a different year.
HSCSN_VINTAGE = "CY2023"
HSCSN_WHY = ("HSCSN predates the managed care regulations and is not an MCO "
             "in the regulatory sense, so it files no comparable annual "
             "statement and has no Title XIX column to read. It reports to "
             "DHCF; that figure has not been acquired. CY2023 stands in, and "
             "this plan is therefore a year behind the other three.")

# dollars, as filed. S-105: typed once here because they are read off a
# source; every per-$100 figure below is derived.
#
# ONE RULE, D-151. Every plan's figures come from the SAME five lines of the
# SAME column of its own annual statement — the Title XIX Medicaid column of
# the Analysis of Operations by Lines of Business — and are apportioned only
# where that column covers more than the District:
#
#   line 7   total revenues              -> capitation
#   line 17  total hospital and medical  -> care
#   19 + 20  claims adjustment + general administrative -> admin
#   line 21  increase in A&H reserves    -> a deduction, see below
#   line 24  net underwriting gain       -> what the residual must reproduce
#
# Because the statement's own line 24 is line 7 less lines 17 to 22, a margin
# struck as premium less care less administration less reserves EQUALS the
# plan's published Title XIX underwriting gain, exactly. `agreement()` below
# asserts it for every plan, so the construction is checked against the source
# rather than trusted. S-105: the margin is still derived and never typed.
#
# WHAT THIS REPLACES, read from the three filings on 18 November 2026. Three
# plans, three different errors, in three different directions:
#
#   AmeriHealth  line 21 was ignored. The plan booked $5,003,850 against
#                contracts it expected to lose on, entirely to Title XIX, and
#                the statement counts that as a cost of the Medicaid
#                business. The residual did not. Margin was drawn 46% high.
#   Wellpoint    the expense lines were apportioned from the entity total,
#                on a comment saying they are "published for the entity". They
#                are not: the statement prints claims adjustment and general
#                administrative in the Title XIX column, $12,042,234 and
#                $25,404,488. The apportionment was unnecessary and wrong by
#                $766,632.
#   MedStar      revenue came from Schedule T and costs from the Title XIX
#                column, which are not the same quantity: Schedule T is direct
#                premium, the column is net of ceded reinsurance and includes
#                other health care revenue. The two bases differed by
#                $851,976 before apportionment.
#
# MedStar is the only plan needing a share at all. Its Title XIX column is
# Maryland and the District together; Schedule T's District row against the
# column's direct premium is the only published District-specific split.
_MEDSTAR_SHARE = 375_055_803 / 920_065_573

# line 7, total revenues, Title XIX column
_PREM = {
    "amerihealth": 747_775_854,
    "wellpoint":   337_597_417 - 30_252_084,      # net premium less unearned
    "medstar":     920_917_549 * _MEDSTAR_SHARE,  # both jurisdictions, shared
    "hscsn":       184_000_000,                   # CY2023, DHCF report
}
# line 17, total hospital and medical, Title XIX column
_CARE_D = {
    "amerihealth": 649_036_647,
    "wellpoint":   253_829_876 - 863_824,         # subtotal less reinsurance
    "medstar":     821_242_215 * _MEDSTAR_SHARE,
    "hscsn":       154_400_000,                   # CY2023, DHCF report
}
# lines 19 and 20, Title XIX column. Published by column for all three.
_PLAN_ADMIN = {
    "amerihealth": 27_887_325 + 54_960_568,
    "wellpoint":   12_042_234 + 25_404_488,
    "medstar":    (23_370_822 + 69_514_545) * _MEDSTAR_SHARE,
}
# line 21, increase in reserves for accident and health contracts, Title XIX.
# AmeriHealth's is a premium deficiency reserve in full (Part 2D note (a));
# the other two report none (MedStar's Note 30 says so in terms).
_PLAN_RESERVE = {
    "amerihealth": 5_003_850,
    "wellpoint":   0,
    "medstar":     0,
}
# line 24, net underwriting gain, Title XIX column. NOT used to build
# anything — it is what agreement() checks the residual against.
_PLAN_GAIN = {
    "amerihealth": 10_887_464,
    "wellpoint":   16_932_559,
    "medstar":     6_789_967 * _MEDSTAR_SHARE,
}

# ---- to the hundred -------------------------------------------------------
# The plans are scaled to the managed-care lane, which is the CMS-64 figure
# and is the number that belongs to this hundred. A plan's statement and the
# CMS-64 do not agree and never will: different accountings, different year
# boundaries, and the statements carry Alliance and ICP money that is outside
# this hundred entirely (basis_dc, declaration 3). Scaling preserves each
# plan's share of the whole and lets the lane total stay the measured one.
_PREM_T = sum(_PREM.values())
_TO_LANE = (mco_cap * SCALE * 1e6) / _PREM_T

_cap = {k: v * _TO_LANE / 1e6 / SCALE for k, v in _PREM.items()}
_care = {k: v * _TO_LANE / 1e6 / SCALE for k, v in _CARE_D.items()}
_adm = {k: v * _TO_LANE / 1e6 / SCALE for k, v in _PLAN_ADMIN.items()}
_rsv = {k: v * _TO_LANE / 1e6 / SCALE for k, v in _PLAN_RESERVE.items()}
# Margin is what is left of the premium after care and administration, and it
# STAYS that: retention is capitation less care and it has to close, so a
# third component cannot simply be deducted and left undrawn (S-108).
#
# WHAT THE RESERVE IS. AmeriHealth set $5,003,850 aside against Title XIX
# contracts it expected to lose money on — a premium deficiency reserve, Part
# 2D note (a). Its statement counts that as an underwriting deduction, so its
# published Title XIX underwriting gain of $10,887,464 is AFTER it. The money
# did not buy care and is not administration; it stayed with the plan. On a
# panel that asks where the dollar went, it is retained, and in a two-bucket
# retention it belongs here.
#
# So the figure is unchanged and the DESCRIPTION was what was wrong: "margin"
# read as earnings, and for AmeriHealth a third of it is a reserve movement.
# D-151 names the two parts rather than moving the money.
_mgn = {k: _cap[k] - _care[k] - _adm[k] for k in _adm}


def agreement(tol=1e-6):
    """Every plan's residual margin IS its published gain plus its reserve.

    The check that makes the residual a reading rather than an estimate. It
    compares on filed dollars, before the scaling to the CMS-64 lane, because
    the scaling is ours and the agreement is the statement's.
    """
    out = []
    for k in _PLAN_GAIN:
        got = _PREM[k] - _CARE_D[k] - _PLAN_ADMIN[k]
        want = _PLAN_GAIN[k] + _PLAN_RESERVE[k]
        if abs(got - want) > max(tol, abs(want) * 1e-9):
            out.append(f"{k}: residual {got:,.2f} against published "
                       f"{want:,.2f}, off by {got - want:,.2f}")
    if out:
        raise AssertionError(
            "plan margin no longer reproduces the filed underwriting "
            "gain plus the filed reserve movement:\n  "
            + "\n  ".join(out))
    return len(_PLAN_GAIN)


agreement()

# retained for the legacy byte-identity path only
_rev = {"amerihealth": 841.0, "wellpoint": 425.3, "medstar": 411.2}
_clm = {"amerihealth": 755.5, "wellpoint": 348.5, "medstar": 379.6,
        "hscsn": 154.4}
_hscsn_rev = 184.0

# The fourth field is the plan's RESERVED name in palette.py. A plan's colour
# is held by its national parent across every state build, so a reader
# following the series recognises AmeriHealth in DC and in Louisiana, and
# multi-state comparisons work (JW ruling, 2026-08-18). The name is a fact
# about the plan and belongs here with its other identity; the colour itself
# lives in palette.py and nowhere else.
PLANS = [
    ("amerihealth", "AmeriHealth Caritas DC",
     "AmeriHealth Caritas District of Columbia, Inc.", "AmeriHealth Caritas"),
    ("wellpoint", "Wellpoint DC (formerly Amerigroup)",
     "Amerigroup District of Columbia, Inc.", "Elevance / Wellpoint"),
    ("medstar", "MedStar Family Choice DC", "MedStar Family Choice DC",
     "MedStar Family Choice"),
    ("hscsn", "HSCSN", "Health Services for Children with Special Needs, Inc.",
     "Children's National / HSCSN"),
]

# the dual lane's two, which the palette holds by TYPE rather than by parent
PLAN_PALETTE = {k: n for k, _l, _e, n in PLANS}
PLAN_PALETTE.update({"united": "D-SNP", "pace": "PACE"})

RENAME = ("Amerigroup DC was renamed Wellpoint DC on 1 July 2025. A plan carries "
          "its present-day name with the former name in parentheses, so a reader "
          "recognises it today whatever year the ledger is. The licensed entity "
          "name is unchanged and is what NAIC and SEC filings are found under. "
          "DHCF's current managed care page lists two comprehensive plans, which "
          "suggests a consolidation after the ledger year; not yet confirmed.")

LEGACY_ABSENT = [
    "Federal oversight: fraud control units and survey and certification are "
    "reported nationally only, so the national panel's $0.10 has no DC "
    "counterpart and this hundred contains none of it",
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


# ===========================================================================
# THE ASSUMED SERVICE MIX — JW, 2026-10-29
# ===========================================================================
#
# D-109 withdrew the national managed-care mix from this panel on 27 September
# and compose() has truncated the fan ever since. JW has asked for it back as
# an explicit assumption for the demo, with the DC data stipulated as not
# proofread and not final.
#
# THIS IS NOT A MEASUREMENT AND MUST NEVER BE READ AS ONE. The District
# publishes no managed-care spending by service category. Every capitated cell
# below is the NATIONAL shape imposed on DC's dollars.
#
# WHAT IT GETS WRONG, named rather than left for a reader to discover:
#
#   HSCSN is a paediatric plan for children with special needs. Giving it the
#   national mix draws it with the same long-term-care and hospital profile as
#   three comprehensive adult plans. It is the figure on this panel most
#   likely to be wrong, and most likely to be spotted by someone who knows DC.
#
#   DC's own fee-for-service mix is nothing like the national one — 55 percent
#   of its FFS dollar is long-term care against about 20 percent nationally.
#   A jurisdiction whose measured half diverges that far is unlikely to match
#   on the half we cannot see.
#
#   Behavioral health is not a DC node. The District folds it into wrap-around
#   services, so the national BH and Other columns are folded there too rather
#   than being dropped or given a node DC does not have.
#
# S-105: derived from ledger_national_2024, never typed. If the national mix
# is re-acquired, DC's assumption moves with it instead of silently aging.
ASSUMED_MIX_NOTE = (
    "ASSUMED, NOT MEASURED. The District publishes no managed-care spending "
    "by service category. The capitated rows carry the NATIONAL mix imposed "
    "on DC's dollars. HSCSN is a paediatric special-needs plan and is drawn "
    "with an adult comprehensive profile; DC's own measured fee-for-service "
    "mix diverges sharply from national, so the unmeasured half probably "
    "does too.")

# national Other and Behavioral health both land in DC's wrap-around node
_FOLD = {"Other": "Wrap around services",
         "Behavioral health": "Wrap around services"}


def _assumed_shares():
    """The national capitated mix as shares of one, on DC's five nodes."""
    import ledger_national_2024 as _N
    _L = _N.build()
    tot = {}
    for (r, c), v in _L.claims.cell.items():
        if r in ("mco", "dual"):
            tot[c] = tot.get(c, 0.0) + float(v.n)
    whole = sum(tot.values())
    out = {n: 0.0 for n in NODES}
    for c, v in tot.items():
        out[_FOLD.get(c, c)] += v / whole
    return out


def _cells(ffs_n, legacy, assumed=False):
    # Exhibit 17's nine published columns, mapped to the five District nodes
    # in basis_dc and netted on the collections factor. _s() stamped these
    # with the generic spine source and a STALE note until 18 November, which
    # named no document a signer could open; they are Exhibit 17 readings and
    # now say so. Parity with the national panel's `_m()` cells.
    c = {("ffs", k): _x17(v, "Mapped from Exhibit 17's nine fee-for-service "
                             "columns; the mapping is in basis_dc.py. Netted "
                             "on the collections factor, D-150.")
         for k, v in ffs_n.items()}
    if assumed and not legacy:
        sh = _assumed_shares()
        mco_care, dual_care = sum(_care.values()), pace + dsnp
        for n in NODES:
            c[("mco", n)] = Fig(mco_care * sh[n], source="ledger_national_2024",
                                vintage="FY2024", basis=B, status=MODELLED,
                                note=ASSUMED_MIX_NOTE)
            c[("dual", n)] = Fig(dual_care * sh[n],
                                 source="ledger_national_2024",
                                 vintage="FY2024", basis=B, status=MODELLED,
                                 note=ASSUMED_MIX_NOTE)
        return c
    if not legacy:
        return c
    mco_n, dual_n = _legacy_alloc()
    c.update({("mco", k): Fig(v, status=MODELLED, note="national mix, legacy")
              for k, v in mco_n.items()})
    c.update({("dual", k): Fig(v, status=MODELLED, note="75/25, legacy")
              for k, v in dual_n.items()})
    return c


def _cols(ffs_n, legacy, assumed=False):
    if assumed and not legacy:
        sh = _assumed_shares()
        mco_care, dual_care = sum(_care.values()), pace + dsnp
        return {n: Fig.derived(
                    ffs_n[n] + mco_care * sh[n] + dual_care * sh[n],
                    tuple(f"claims.cell.{r}.{n}" for r in ("mco", "dual", "ffs")),
                    basis=B, note=ASSUMED_MIX_NOTE)
                for n in NODES}
    if not legacy:
        return {}
    mco_n, dual_n = _legacy_alloc()
    return {k: Fig.derived(
                ffs_n[k] + mco_n[k] + dual_n[k],
                tuple(f"claims.cell.{r}.{k}" for r in ("mco", "dual", "ffs")))
            for k in NODES}


def build(legacy_mix: bool = False, assumed_mix: bool = False) -> Ledger:
    """`legacy_mix=True` reproduces exactly what `ledger_dc.py` carried: the
    national managed-care service mix applied to DC's plan care, and the
    undeclared 75/25 split of the dual and PACE lanes. It exists so the
    refactor can be proved byte-identical before the correction is made, per
    S-064. It is not a fallback and nothing should ship from it."""
    payers = []

    payers.append(Payer(
        "mco", "MCO capitation", "mco",
        capitation=Fig(mco_cap, source=EX17, vintage=V, basis=B,
                       status=MODELLED,
                       note="Exhibit 17's $1,802M of managed care, net of "
                            "the collections fold (D-150), less the PACE and "
                            "D-SNP carves, which are MODELLED. Nothing "
                            "publishes this figure; MEASURED until "
                            "18 November 2026. D-151."),
        care=Fig.derived(sum(_care.values()),
                         tuple(f"payer.{k}.care" for k in _care)),
        admin=(Fig(mco_cap - sum(_care.values()), status=MODELLED,
                   note="legacy: whole retention labelled plan administration")
               if legacy_mix else
               Fig.absent("Three of the four plans now publish their "
                          "administration and margin on their Title XIX "
                          "column, but HSCSN does not, so the LANE total is "
                          "still not known. Published as absent rather than "
                          "as the sum of three, which would be a floor "
                          "presented as a total. " + HSCSN_WHY)),
        margin=(Fig(0.0, status=MODELLED, note="legacy: no earnings carve")
                if legacy_mix else Fig.absent("See admin."))))

    # STATUS, D-151. These were MEASURED until 18 November. They are not
    # measurements: every plan figure on this plate is its filed Title XIX
    # figure multiplied by `_TO_LANE`, which is ours, and no statement
    # contains the resulting number — AmeriHealth files $747.776M and the
    # plate draws $814.071M. A signature on a MEASURED figure asserts that a
    # person opened a source and agreed with THAT number, so MEASURED here
    # would put a signature on a figure nobody can open. MODELLED, with the
    # filed figure named in the note, is what the plate actually holds.
    # The readings themselves stay MEASURED and signable, one level up, in
    # `anchor.ex17.*` and in each plan's own statement.
    PLAN_BASIS = {
        "amerihealth": ("Title XIX column, published in full. Nothing "
                        "apportioned. Filed Title XIX total revenues "
                        "$747,775,854.", NAIC24, MODELLED),
        "wellpoint":   ("Title XIX column throughout — premium, care, and "
                        "BOTH expense lines, which the statement prints by "
                        "column and which this ledger apportioned from the "
                        "entity total until D-151. Filed Title XIX total "
                        "revenues $307,345,333.", NAIC24, MODELLED),
        "medstar":     ("Title XIX column, apportioned: the entity writes "
                        "Title XIX in Maryland as well, and Schedule T's "
                        "District row against the column's direct premium is "
                        "the only published District split. Revenue and costs "
                        "now share one basis, which they did not until "
                        "D-151.", NAIC24_T, MODELLED),
        "hscsn":       (HSCSN_WHY, MCR, MODELLED),
    }
    for key, label, entity, _pal in PLANS:
        why, src, st = PLAN_BASIS[key]
        note = ((RENAME + " ") if key == "wellpoint" else "") + why
        vint = HSCSN_VINTAGE if key == "hscsn" else "CY2024"
        scaled = (" Scaled to the CMS-64 managed-care lane, which is the "
                  "figure that belongs to this hundred; a plan's statement "
                  "and the CMS-64 do not agree and never will.")

        def _f(v, extra=""):
            return Fig(v, source=src, vintage=vint, basis=B, status=st,
                       note=(note + " " + extra + scaled).strip())

        if key in _adm:
            admin = _f(_adm[key], "Claims adjustment plus general "
                                  "administrative expenses.")
            _res_m = _PLAN_RESERVE.get(key, 0)
            _split = (
                f" Of this, ${_res_m:,.0f} of filed dollars is an increase in "
                f"reserves for accident and health contracts — a premium "
                f"deficiency reserve in full — and the remainder is the "
                f"plan's published Title XIX net underwriting gain of "
                f"${_PLAN_GAIN[key]:,.0f}. Retained either way; not earnings "
                f"in full. D-151." if _res_m else
                f" The plan reports no reserve movement on Title XIX, so this "
                f"IS its published net underwriting gain of "
                f"${_PLAN_GAIN[key]:,.0f} of filed dollars. D-151.")
            margin = Fig.derived(
                _mgn[key], (f"payer.{key}.capitation", f"payer.{key}.care",
                            f"payer.{key}.admin"),
                basis=B,
                note="Residual: premium less care less administration. "
                     "Nothing publishes a District margin directly." + _split)
        else:
            admin = Fig.absent(
                f"{key}: retention is measured, its split into administration "
                f"and margin is not published. " + HSCSN_WHY)
            margin = Fig.absent(f"{key}: see admin.")

        payers.append(Payer(
            key, label, "mco", parent="mco",
            capitation=_f(_cap[key]),
            care=_f(_care[key], "Incurred benefits."),
            admin=admin, margin=margin,
            entity=entity))

    _DUALNOTE = ("D-151. PACE and the D-SNP wrap are two MODELLED constants "
                 "and their sum is one too: no source publishes a $40M "
                 "District dual-and-PACE line. Exhibit 17 publishes $1,802M "
                 "of managed care and nothing below it. MEASURED until "
                 "18 November, which would have put a signature on a "
                 "subtraction of two estimates.")
    payers.append(Payer(
        "dual", "Dual and PACE capitation", "dual",
        capitation=Fig(pace + dsnp, source=EX17, vintage=V, basis=B,
                       status=MODELLED, note=_DUALNOTE),
        care=Fig(pace + dsnp, source=EX17, vintage=V, basis=B,
                 status=MODELLED,
                 note="No DC retention figure for these lanes, so capitation "
                      "runs through to care. " + _DUALNOTE),
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
        capitation=Fig(ffs, source=EX17, vintage=V, basis=B, status=MODELLED,
                       note="D-83 as applied by D-150. Exhibit 17's nine "
                            "fee-for-service columns of $2,260M, net of the "
                            "collections fold. The dollars are measured; the "
                            "fold is ours. Same construction and same status "
                            "as the national panel's lane."),
        care=Fig(ffs, source=EX17, vintage=V, basis=B, status=MODELLED,
                 note="Rule A: fee-for-service has no payer and no "
                      "retention. It runs through the payer phase "
                      "unchanged."),
        admin=Fig.absent("fee-for-service has no plan administration"),
        margin=Fig.absent("fee-for-service has no margin")))

    # Derived from Exhibit 17's nine published columns in basis_dc, netted on
    # the same factor as the lane. These were typed here until 18 November,
    # and the wrap-around figure carried a $10M reduction nothing recorded.
    _ffs_n = {k: v / SCALE for k, v in DC_FFS_NODES_M.items()}

    claims = Matrix(
        name="claims",
        rows=["mco", "dual", "ffs"],
        cols=NODES,
        row_margin={"mco": Fig.derived(sum(_care.values()), ("payer.mco.care",)),
                    "dual": Fig.derived(pace + dsnp, ("payer.dual.care",)),
                    "ffs": Fig.derived(ffs, ("payer.ffs.care",))},
        col_margin=_cols(_ffs_n, legacy_mix, assumed_mix),
        cell=_cells(_ffs_n, legacy_mix, assumed_mix),
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
        scale=Fig(SCALE, source=EX16, vintage=V,
                  basis="$M of total computable DC Medicaid per $1",
                  status=MEASURED,
                  note="Total Medicaid, DC, FY 2024: $4,372M."),
        anchors={
            "ex16.total": _x(DC_TOTAL_M,
                             "Total Medicaid, DC, FY 2024, $M."),
            "ex16.federal": _x(DC_FED_M,
                               "Federal share of total Medicaid, DC, "
                               "FY 2024, $M."),
            "ex16.state": _x(DC_STATE_M,
                             "Non-federal share of total Medicaid, DC, "
                             "FY 2024, $M."),
            # Exhibit 17's own three lines, put on the register 18 November
            # 2026 (D-150). They were arithmetic inside basis_dc and a
            # comment in this file, so Tier 1.2 of DC_SIGNOFF_LIST asked for
            # a signature on figures that were not figures. These are pure
            # readings — the signable form of the reconciliation — and every
            # lane below is derived or modelled from them.
            "ex17.ffs_gross": _x17(
                DC_FFS_GROSS_M,
                "Fee-for-service, the sum of Exhibit 17's nine published "
                "columns, DC, FY 2024, $M. The nine and their mapping to the "
                "five District nodes are in basis_dc.py."),
            "ex17.managed_care": _x17(
                DC_CAP_M,
                "Managed care and premium assistance, DC, FY 2024, $M. "
                "Exhibit 17 publishes nothing below this line: the PACE and "
                "D-SNP carves under it are modelled."),
            "ex17.collections": _x17(
                DC_COLL_M,
                "Collections — third-party liability, estate and other "
                "recoveries, NOT drug rebates — reported as a single "
                "unallocated negative. The source declines to say which lane "
                "recovered the money, so it is folded pro rata by share of "
                "gross (D-83, applied to the District by D-150). Reported "
                "here, not drawn."),
            "budget.dedtax": Fig(
                DC_DEDTAX_M, source=DHCF_BUDGET, vintage=V,
                basis="dedicated taxes, appropriated, $M",
                status=MEASURED,
                note="Provider assessments earmarked to Medicaid: hospital "
                     "inpatient and outpatient provider fees, the Healthcare "
                     "Provider Tax on nursing facilities, and the ICF-IDD "
                     "assessment. Doubles in FY2025 when D.C. Code sec. 44-665 "
                     "takes effect with amounts owed from 1 October 2024."),
            "state.provider_assessments": Fig.derived(
                DC_DEDTAX_M / SCALE,
                ("anchor.budget.dedtax", "anchor.ex16.total"),
                basis="non-federal share, provider assessments",
                note="The part of the non-federal share raised by assessing "
                     "providers rather than appropriated from the general "
                     "fund. Enters the hundred at the source column and "
                     "returns to the same provider classes at the claims "
                     "column, but the assessment base is total patient "
                     "revenue, not Medicaid patient revenue, so most of the "
                     "assessed dollar comes from outside this hundred. Not "
                     "drawn as a loop for that reason."),
            "state.local_appropriation": Fig.derived(
                (DC_STATE_M - DC_DEDTAX_M) / SCALE,
                ("anchor.ex16.state", "anchor.budget.dedtax",
                 "anchor.ex16.total"),
                basis="non-federal share, general fund",
                note="Residual. Parents sit in two accountings - a CMS-64 "
                     "state share less an appropriated dedicated-tax figure - "
                     "so this is derived and may not be signed as measured."),
        },
        sources={"federal": Fig.derived(
                     73.17, ("anchor.ex16.federal", "anchor.ex16.total"),
                     basis="blended, including expansion",
                     note="$3,199M federal of $4,372M total Medicaid, "
                          "Exhibit 16. Not the FMAP: DC's statutory rate and "
                          "its expansion rate both sit inside this blend."),
                 "state": Fig.derived(
                     26.83, ("anchor.ex16.state", "anchor.ex16.total"),
                     basis="non-federal share",
                     note="$1,173M non-federal of $4,372M total Medicaid, "
                          "Exhibit 16.")},
        peels=[
            Peel("admin", "Administration",
                 _x(DC_ADMIN_M / SCALE,
                    "State program administration, Exhibit 16. Federal $145M, "
                    "non-federal $89M, a 62/38 split against the 73/27 blend "
                    "on benefits: administration is the least-matched money in "
                    "the program."),
                 "STATE_AGENCY", reach="STATE_AGENCY", kind="admin"),
            Peel("medicare", "Medicare premiums",
                 _x17(DC_MEDICARE_M / SCALE,
                      "Medicare premiums and coinsurance, Exhibit 17. DC pays "
                      "Part A and Part B premiums for its dual enrollees; the "
                      "money returns to the federal government and buys no "
                      "Medicaid service."),
                 "STATE_AGENCY",
                 reach="STATE_AGENCY", kind="return"),
        ],
        payers=payers,
        nodes=NODES,
        claims=claims,
        beneficiaries=None,
        declared=([] if (legacy_mix or assumed_mix) else
                  ["claims:mco", "claims:dual"]) + [
            "mco", "dual", "ffs", "amerihealth", "wellpoint", "medstar",
            "hscsn", "united", "pace"],
        declarations=LEGACY_ABSENT if legacy_mix else [
            (ASSUMED_MIX_NOTE if assumed_mix else
             "claims row mco: DC does not publish managed-care spending by "
             "service category. The fan out of the capitated lanes is absent."),
            ("The capitated fan is an ASSUMPTION and the panel says so "
             "wherever it is drawn." if assumed_mix else
             "claims row dual: as above, for the D-SNP wrap and PACE."),
            "mco: plan retention is measured in total; its split into "
            "administration and margin is not published for DC.",
            "dual: no retention figure for the D-SNP wrap or PACE.",
            "amerihealth, wellpoint, medstar: administration and margin are "
            "taken from each plan's own CY2024 Title XIX reporting. Margin is "
            "a residual — premium less care less administration — because "
            "nothing publishes a plan's Medicaid margin directly.",
            "MIXED VINTAGE ON THIS PLATE. Three plans are CY2024 and HSCSN is "
            "CY2023. " + HSCSN_WHY,
            "The plans are scaled to the CMS-64 managed-care lane. A plan's "
            "annual statement and the CMS-64 are different accountings on "
            "different year boundaries, and the statements carry locally "
            "funded Alliance and ICP money that is outside this hundred. "
            "Scaling preserves each plan's share and keeps the lane total the "
            "measured one.",
            "MedStar Family Choice, Inc. is not a DC-only entity: it writes "
            "$920.1M of Title XIX across two jurisdictions, $545.0M of it in "
            "Maryland. Its District figure is Schedule T, not its Title XIX "
            "column, and its expenses are apportioned by DC's share of "
            "Title XIX premium.",
            "united, pace: retention split not published.",
            "Behavioral health is not a separate node. The DC source folds it "
            "into wrap-around services and into the capitated lump.",
            "Documented fraud: no DC figure.",
            "Beneficiary shares: no matrix built. MACStats Exhibit 21 carries a "
            "state dimension and is the route in.",
        ],
        note="Every vintage inherited and unverified. " + STALE,
    )
