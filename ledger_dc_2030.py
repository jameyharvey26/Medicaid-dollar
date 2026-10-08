# ledger_dc_2030.py — the District of Columbia FY2030 to-be, in the Ledger shape.
#
# STANDING, NOT PUBLISHING. Every per-$100 figure on this panel is ABSENT, and
# that is not a gap to be filled in later by whoever gets here next — it is the
# honest state of the model today, and the file exists so that the state is
# visible rather than implied.
#
# WHY EVERY SHARE IS ABSENT. A share needs a denominator. D-01 as re-anchored
# makes the FY2030 hundred prior-law FY2030 spending, which nationally comes
# from a CBO baseline at a pre-enactment vintage. There is no CBO District row.
# No pre-enactment DC financial plan reaches FY2030 either: the District's plan
# runs four years, so the last one published before 4 July 2025 stops at FY2029.
# Until that is resolved the DC FY2030 hundred is not struck, `scale` is ABSENT,
# and nothing downstream of it may carry a value. S-109 is the whole reason to
# be strict: a figure divided by the FY2024 hundred is a different hundred, and
# a panel that mixed the two would be wrong in a way no reader could see.
#
# WHAT IS NOT ABSENT. The dollars. `anchors` holds figures on the source's own
# basis in the source's own units, which is exactly what the directed payment
# work produced, so the acquisition is recorded here and signed, and the shares
# derive from it the moment `scale` lands. Nothing has to be re-acquired.
#
# WHAT THIS FILE PROVES. That the DC 2030 panel needs no new ledger machinery:
# the same Ledger, Peel, Fig and Matrix hold a to-be panel for a state, with
# seven HR-1 tributaries whose charge and reach come straight from the national
# model because they are properties of federal statute, not of a jurisdiction.

from ledger import (ABSENT, DERIVED, Fig, Ledger, Matrix, MEASURED, MODELLED,
                    Payer, Peel)

import basis_dc as _B
import fmap_dc as _F
import tobe2030_dc as _T
import ledger_dc_2024 as _AS_IS
import placeholder as _PH

V30 = "FY2030"
B30 = "total computable"

# The charge and reach columns are taken from ledger_national_2030.HR1 without
# change. They are claims about where in the lifecycle a dollar stops, which is
# a property of the statute and of the flow, not of the District. If DC ever
# needs a different answer here, that is a finding about the model and belongs
# in a conversation, not in a quiet edit.
HR1_DC = {
    "Work reporting":                   ("STATE_AGENCY", "DISBURSE"),
    "Six-month renewals":               ("STATE_AGENCY", "PAYER"),
    "Blocked Medicaid enrollment rule": ("STATE_AGENCY", "CLAIMS"),
    "Everything else":                  ("STATE_AGENCY", "STATE_AGENCY"),
    "Blocked senior enrollment rule":   ("STATE_AGENCY", "BENEFICIARY"),
    "Provider tax limits":              ("FEDERAL",      "FEDERAL"),
    "Directed payment caps":            ("CLAIMS",       "PROVIDERS"),
}

TERMINAL_DC = {
    "Work reporting":                   "will not become coverage",
    "Provider tax limits":              "will not be matched",
    "Directed payment caps":            "will not top up hospital rates",
    "Blocked senior enrollment rule":   "will not become premium help",
    "Six-month renewals":               "will not survive renewal",
    "Blocked Medicaid enrollment rule": "will not become enrollment",
    "Everything else":                  "will not become services",
}

NO_HUNDRED = ("No District figure. CBO scores this lever nationally and "
              "publishes no District line; allocating the national score by a "
              "District share would fill a missing figure from somewhere else.")

HUNDRED_NOTE = (
    "MODELLED. DC's FY2024 hundred grown to FY2030 at the prior-law rate "
    "implied by the national model's own counterfactual — basis_national's "
    "FY2024 hundred against tobe2030's FY2030 prior-law total, CBO January "
    "2025 baseline vintage. Derived in code, never typed. Corroborated by, not "
    "derived from, DC's own observed growth of 5.49% on Exhibit 16 FY2022-24. "
    "Superseded when the District's FY2026 Proposed Budget and Financial Plan "
    "(27 May 2025, pre-enactment, four-year trajectory through FY2029) is "
    "acquired.")


def _absent_share(why: str) -> Fig:
    return Fig.absent(why)


def _peel(key: str, label: str) -> Peel:
    charged, reach = HR1_DC[key]
    if key == "Directed payment caps":
        amount = Fig.derived(
            _T.DIRECTED_CUT_PER100,
            ("anchor.sdp.cut_fy2030", "scale"),
            basis="$ per $100 of the FY2030 prior-law DC hundred",
            note="Two steps of the phase-down against the grandfathered base, "
                 "divided by the FY2030 hundred. BOTH parents are modelled: "
                 "the base is DHCF's planning assumption and the hundred is a "
                 "declared growth rate. The figure is no stronger than either.")
    else:
        amount = _absent_share(NO_HUNDRED)
    # The key IS the label. PeelSum in the views resolves tributaries by this
    # string and V.step_x is keyed on it too, so a tidier slug silently
    # detaches the lane from its position and its subtraction.
    return Peel(key, label, amount=amount, charged=charged, reach=reach,
                kind="hr1")


def ledger() -> Ledger:
    as_is = _AS_IS.build()

    HELD = ("MODELLED by composition-held. The FY2024 share is carried to "
            "FY2030 unchanged on the stated assumption that the shape of the "
            "dollar does not move, only its level. Not a projection of this "
            "figure; no DC source projects it.")

    def _held(f: Fig) -> Fig:
        if f.is_absent:
            return f
        return Fig(f.value, source=f.source, vintage=f"{f.vintage} held to {V30}",
                   basis=f.basis, status=MODELLED, note=HELD)


    # ---- anchors: dollars, which we do have ------------------------------
    anchors = {
        "sdp.grandfathered": Fig(
            _T.GRANDFATHERED_M, source=_T.SDP_SOURCE, vintage="FY2025",
            basis="state directed payments, $M, approved by CMS",
            status=MODELLED,
            note="DHCF's own planning assumption, used on JW's instruction "
                 "2026-10-07 and footnoted as an assumption. DHCF states the "
                 "provider fee funds revert to the FY2025 level in FY2027 "
                 "because taxes are frozen at their 4 July 2025 level. The "
                 "FY2026 projection of $658.7M would give a larger base and "
                 "the grandfathering window appears to permit it, but it "
                 "rested on a CMS approval still outstanding in April 2026."),
        "sdp.cut_fy2030": Fig.derived(
            _T.DIRECTED_CUT_M,
            ("anchor.sdp.grandfathered",),
            basis="reduction in state directed payments, FY2030, $M",
            note="Two steps of 10 percentage points off the grandfathered "
                 "total. DC's rating period is the federal fiscal year, "
                 "established from CMS's approval letter, control name "
                 "DC_Fee_IPH_New_20231001-20240930. The statute bites on "
                 "rating periods beginning on or after 1 January 2028, so "
                 "FY2028 (beginning 1 October 2027) is too early and FY2029 "
                 "is the first affected period. DISPUTED: DHCF's April 2026 "
                 "deck says FY2028, which would make FY2030 the third step "
                 "and the reduction $145.56M. Unresolved; on the acquisition "
                 "list."),
        "fmap.regular": Fig(
            _F.FMAP_DC, source=_F.FMAP_SOURCE, vintage="statutory",
            basis="federal share of regular-match expenditure",
            status=MEASURED,
            note="Fixed at 70 percent by statute, not computed from the "
                 "per-capita-income formula. This is the single largest "
                 "driver of DC's divergence from the national figure on every "
                 "enrollment-side lever."),
        "fmap.expansion": Fig(
            _F.FMAP_EXPANSION, source=_F.FMAP_SOURCE, vintage="statutory",
            basis="federal share, newly eligible adults",
            status=MEASURED),
    }

    # ---- the seven tributaries -------------------------------------------
    peels = [_peel(k, k) for k in HR1_DC]

    # ---- the as-is peels, carried ----------------------------------------
    # A to-be panel draws the whole flow, not only the tributaries HR-1 opens:
    # administration and the Medicare premium return exist in FY2030 whatever
    # the law does. They are carried from the as-is ledger with ABSENT amounts
    # rather than dropped, because dropping them would silently redraw the
    # panel's spine, and rather than copied forward at their FY2024 values,
    # because an FY2024 share is not an FY2030 share and nothing has projected
    # them. They become placeholder bands like the rest.
    peels += [Peel(p.key, p.label,
                   amount=_held(p.amount),
                   charged=p.charged, reach=p.reach, kind=p.kind)
              for p in as_is.peels]

    # ---- the prior-law FY2030 flow: composition held, level grown ---------
    #
    # JW, 2026-10-07. HR-1 subtracts from a prior-law FY2030 FLOW, not from a
    # total. We have a FY2030 hundred and one lever; without a trunk there is
    # nothing for the lever to come out of, and an absent trunk renders as zero
    # because Fig.n returns 0.0 — which turns "we do not know" into "nothing",
    # the exact substitution this panel exists to refuse.
    #
    # THE ASSUMPTION, stated once and in one place: the SHAPE of DC's Medicaid
    # dollar is unchanged between FY2024 and FY2030; only its size moves. One
    # assumption, visible on the artifact, and a reader who disagrees can say
    # so and redo it.
    #
    # Why this is cheap to express: a share is scale-free. Holding composition
    # constant means every per-$100 figure carries across UNCHANGED, so the
    # FY2024 figures are reused directly rather than recomputed. The growth is
    # already in SCALE30 and nowhere else.
    #
    # WHAT IT IGNORES, and these are real: DC's enrolment growth is
    # concentrated among people aged 65+, dual-eligible and PACE capitation is
    # rising far faster than the rest of the book, and the District enacted its
    # own eligibility reductions for FY2026. Every one of those changes the
    # shape, not just the size. The assumption is a floor to draw from, not a
    # forecast.
    payers = [Payer(p.key, p.label, p.kind,
                    capitation=_held(p.capitation),
                    care=_held(p.care),
                    parent=p.parent, entity=p.entity)
              for p in as_is.payers]

    nodes = list(as_is.nodes)
    claims = Matrix(
        "claims", rows=[p.key for p in payers], cols=nodes,
        row_margin={p.key: _absent_share(NO_HUNDRED) for p in payers},
        col_margin={n: _held(as_is.claims.col_margin[n])
                    if n in as_is.claims.col_margin
                    else _absent_share(NO_HUNDRED) for n in nodes},
        note="Interior unallocated, as in FY2024: DC publishes no service "
             "allocation and none has been estimated.")

    return Ledger(
        geography="District of Columbia",
        year=V30,
        scenario="to_be",
        scale=Fig(_T.SCALE30, source=_T.CAGR_SOURCE, vintage=V30,
                  basis="$M of prior-law DC Medicaid per $1, FY2030",
                  status=MODELLED, note=HUNDRED_NOTE),
        sources={k: _held(v) for k, v in as_is.sources.items()},
        anchors=anchors,
        peels=peels,
        payers=payers,
        nodes=nodes,
        claims=claims,
        declared=[
            "dc2030.hundred_modelled_national_rate",
            "dc2030.levers_five_of_seven_absent",
            "dc2030.provider_tax_coupled_undetermined",
            "dc2030.directed_payment_first_year_disputed",
            "dc2030.service_allocation_absent",
            "dc2030.composition_held_from_fy2024",
        ],
        declarations=[
            HUNDRED_NOTE,
            "Five of the seven HR-1 tributaries have no District figure. CBO "
            "scores the levers nationally and publishes no District line; "
            "allocating the national score by any District share would fill a "
            "missing figure from somewhere else, which this panel exists to "
            "refuse. Each absent lever records what would be needed to derive "
            "it from District sources.",
            "Provider tax limits and directed payment caps are coupled in the "
            "District and are not coupled in the national model. DC's "
            "directed payments are financed by a hospital provider tax, and "
            "the tax freeze returns the programme to its FY2025 level in "
            "FY2027, before the phase-down begins. The second lever's base is "
            "set by the first. The coupling is declared and not modelled, "
            "because the FY2027 revert has no published dollar figure.",
            "The first year of the directed payment phase-down is disputed. "
            "On the rating period established from CMS's approval letter it "
            "is FY2029; DHCF's own budget deck says FY2028. One step is "
            "$48.5M. Not resolved by assumption.",
            "No DC service allocation is published and none has been "
            "estimated, so the claims fan is unallocated, as in FY2024.",
            "The prior-law FY2030 flow holds the FY2024 composition and grows "
            "only the level. Every trunk and lane figure on this panel is that "
            "assumption, not a projection: no DC source projects them. It "
            "ignores known shape changes — enrolment growth concentrated among "
            "people aged 65+, dual-eligible capitation rising faster than the "
            "rest of the book, and the District's own FY2026 eligibility "
            "reductions.",
        ],
        note="Structure standing, figures absent. See basis_dc, fmap_dc and "
             "tobe2030_dc for the dollars that are held.")


if __name__ == "__main__":
    L = ledger()
    print(f"{L.geography} {L.year} [{L.scenario}]")
    print(f"  scale            {'ABSENT' if L.scale.is_absent else L.scale.value}")
    print(f"  payer lanes      {len(L.lanes())} aggregate, "
          f"{len(L.payers) - len(L.lanes())} named children")
    print(f"  provider nodes   {len(L.nodes)}  (claims interior: {L.claims.state})")
    print(f"  tributaries      {len(L.peels)}")
    for p in L.peels:
        held = "dollars held" if p.label == "Directed payment caps" else "absent"
        print(f"     {p.label:<34} {p.charged:<14} -> {p.reach:<14} {held}")
    print(f"  anchors          {len(L.anchors)} (dollars, signed-able)")
    for k, f in L.anchors.items():
        print(f"     {k:<22} {f.value:>10,.2f}  {f.status}")
    print(f"  declared keys    {len(L.declared)}")


def placeholders(L=None):
    """Violet geometry for every tributary whose figure is ABSENT.

    Drawing only. Nothing here is a quantity; see placeholder.py. The width is
    uniform because an unacquired lever has no size — varying the widths would
    be inventing a ranking we do not have.
    """
    L = L or ledger()
    out = []
    for p in L.peels:
        ph = _PH.for_absent(p.key, p.label, p.amount, width=2.0)
        if ph is not None:
            out.append(ph)
    return out


if __name__ == "__main__":
    ph = placeholders()
    print()
    print(_PH.audit(ph))
    print(f"\n  token {_PH.VIOLET} (hatch {_PH.VIOLET_HATCH})")
    try:
        ph[0].value
    except TypeError as e:
        print(f"  value access refused: {e}")
    try:
        _PH.forbid_in_shipping(ph, "DC FY2030 panel")
    except _PH.PlaceholderInShippingArtifact as e:
        print(f"\n  shipping gate: REFUSED\n    {e}")
