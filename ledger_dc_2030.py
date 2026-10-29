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
    "DC provisions not separately scored": ("STATE_AGENCY", "STATE_AGENCY"),
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
    "DC provisions not separately scored": "will not become services",
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
    "SUPERSESSION HUNTED AND NOT FOUND, 2026-10-29: both DHCF agency "
    "chapters, the FY2026 budget testimony, the FY2026 budget slides and the "
    "June 2025 MCAC budget presentation all stop at the budget year, and the "
    "District publishes its four-year plan at District and fund level rather "
    "than as an agency Medicaid trajectory. Not proved absent — the Executive "
    "Summary volume of the FY2026 Proposed budget is unchecked. The "
    "national-implied rate stands until then.")


def _absent_share(why: str) -> Fig:
    return Fig.absent(why)


# The four levers derived on District inputs, 2026-10-29. Each names its own
# parents so the provenance graph carries the chain, and each says in its note
# which step is modelled — because on this panel that is the whole question.
_DERIVED = {
    "Directed payment caps": (
        _T.DIRECTED_CUT_PER100, ("anchor.sdp.cut_fy2030", "scale"),
        "Two steps of the phase-down against the grandfathered base, divided "
        "by the FY2030 hundred. BOTH parents are modelled: the base is DHCF's "
        "planning assumption and the hundred is a declared growth rate. The "
        "figure is no stronger than either. The first affected period is "
        "FY2029, resolved on CMS-2449-P against DHCF's own FY2028 statement."),
    "Provider tax limits": (
        _T.PROVIDER_TAX_PER100, ("anchor.tax.prior_law_fy2030",
                                 "anchor.tax.frozen_level", "scale"),
        "The divergence between a prior-law tax base grown to FY2030 and a "
        "line frozen at the FY2025 level, because section 71115 freezes the "
        "tax in NOMINAL terms and the gap therefore widens every year. "
        "MODELLED in one step: that the tax base would have tracked Medicaid "
        "spending, so it grows at the same rate as the hundred. The measured "
        "FY2027 step of $49.77M is the floor and is drawn beside it. "
        "Published at the NON-FEDERAL level: DC's dedicated tax draws match, "
        "so the total-computable effect is larger, and the multiplier is "
        "declared absent rather than guessed (fmap_dc, D-39 divergence)."),
    "Work reporting": (
        _T.WORK_REPORTING_PER100, ("anchor.expansion.fy2030",
                                   "anchor.rate.default", "scale"),
        "DC's own expansion-group spending at FY2030, times a disenrolment "
        "rate. Nothing is allocated from CBO: the denominator is DHCF's Group "
        "8 program line and the population is DHCF's monthly enrolment "
        "report. The ONE modelled step is the rate, which is published as a "
        "band with a declared default inside it."),
    "Six-month renewals": (
        _T.RENEWALS_PER100, ("anchor.expansion.fy2030", "anchor.rate.default",
                             "scale"),
        "Same population, same denominator, same modelled rate as work "
        "reporting, at the share CBO's own score implies for this lever. "
        "Effective 1 January 2027, twelve-month certification to six."),
}


def _peel(key: str, label: str) -> Peel:
    charged, reach = HR1_DC[key]
    if key in _DERIVED:
        value, parents, note = _DERIVED[key]
        amount = Fig.derived(
            value, parents,
            basis="$ per $100 of the FY2030 prior-law DC hundred",
            note=note)
    else:
        # the reason is the lever's own, not a generic one: two of these are
        # rule-driven and the third is a renamed lane, and they are absent for
        # three different reasons.
        amount = _absent_share(_T.ABSENT_LEVERS.get(key, NO_HUNDRED))
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
                 "is the first affected period. RESOLVED 2026-10-29 on "
                 "CMS-2449-P, which states the test in exactly those terms, "
                 "and on a second confirmation of the rating period from the "
                 "FY2025 preprint. DHCF's own deck says FY2028, which would "
                 "make FY2030 the third step and the reduction $145.56M; the "
                 "model does not move to meet it, and the question is worth "
                 "putting to DHCF before publication."),
        "tax.prior_law_fy2030": Fig.derived(
            _T.PROVIDER_TAX_PRIOR_LAW_FY30_M,
            ("anchor.tax.base_fy2026",),
            basis="dedicated tax revenue under prior law, FY2030, $M",
            note="The FY2026 approved level grown at the prior-law rate. "
                 "MODELLED: that the tax base tracks Medicaid spending."),
        "tax.base_fy2026": Fig(
            _T.DEDTAX_M[2026], source=_T.DEDTAX_SOURCE, vintage="FY2026",
            basis="dedicated taxes, approved, $M", status=MEASURED,
            note="DHCF Table HT0-2, which carries four years on one table. "
                 "The FY2024 cell on this line is identical to "
                 "basis_dc.DC_DEDTAX_M, which is how we know the budget "
                 "table and the basis read the same line. APPROPRIATION "
                 "basis, not CMS-64 — the warning basis_dc already carries."),
        "tax.frozen_level": Fig(
            _T.DEDTAX_M[2025], source=_T.DEDTAX_SOURCE, vintage="FY2025",
            basis="dedicated taxes, actual, $M, frozen in nominal terms",
            status=MEASURED,
            note="Section 71115 freezes collection at taxes imposed as of "
                 "4 July 2025. DHCF's FY2027 proposed figure of $236.167M "
                 "lands within $0.83M of this, which is DHCF's narrative — "
                 "'the Provider Fee Funds revert to the FY2025 level' — "
                 "restated as arithmetic and confirmed by a second table."),
        "expansion.fy2030": Fig.derived(
            _T.DC_EXPANSION_FY30_M,
            ("anchor.expansion.fy2024",),
            basis="expansion-group spending, FY2030, $M",
            note="Grown at the same prior-law rate as the hundred, so the "
                 "lever and its denominator sit on one counterfactual."),
        "expansion.fy2024": Fig(
            _T.GROUP8_MCO_FY24_M, source=_T.GROUP8_SOURCE, vintage="FY2024",
            basis="MCO - Childless Adults (Group 8), actual, $M",
            status=MEASURED,
            note="DHCF books the expansion group as its own program line. "
                 "DISAGREEMENT, declared: this is 16.3 percent of the DC "
                 "hundred, where MACStats Exhibit 21 puts the new adult "
                 "group at 18.1 percent of benefit spending. Different "
                 "vintages and different bases, and a reader will notice."),
        "expansion.at_risk": Fig(
            float(_T.EXPANSION_AT_RISK), source=_T.ENROL_SOURCE,
            vintage="January 2026",
            basis="childless adults 0-133% FPL, enrolled", status=MEASURED,
            note="NOT the FY2024 mix. The District cut childless adult and "
                 "parent eligibility to 138% FPL itself, effective 1 January "
                 "2026, and auto-enrolled about 15,000 people into the "
                 "Healthy DC Plan; the 134-210% band reads 1 against 16,417 "
                 "a year earlier. A panel built off the FY2024 bands would "
                 "overstate both enrolment levers by about a sixth."),
        "rate.default": Fig(
            _T.RATE_DEFAULT, source=_T.RATE_DEFAULT_SOURCE, vintage=V30,
            basis="share of expansion-group spending lost to the two "
                  "enrolment levers",
            status=MODELLED,
            note="THE ONE MODELLED STEP in both enrolment levers. Default is "
                 "the rate implied by CBO's own national score, derived from "
                 "figures already in this repo and typed nowhere; a rate is "
                 "not a dollar allocation, and that distinction belongs on "
                 "the plate. Published as a band running up to the New "
                 "Hampshire outcome, with Arkansas between. THE ENDS ARE NOT "
                 "LIKE-FOR-LIKE: the default is a share of expansion-group "
                 "spending, which includes people the requirement exempts, "
                 "while the observed ends are coverage loss among those "
                 "SUBJECT. DC's exempt share is the next acquisition."),
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
    # COMPOSITION HELD MEANS SHARES OF DISBURSED, NOT SHARES OF THE HUNDRED.
    #
    # Until four levers were derived this distinction cost nothing: no lever
    # had a value, so nothing was subtracted before disbursement and the two
    # readings gave the same number. With work reporting, six-month renewals
    # and the provider tax now biting at or before DISBURSE, they do not.
    # Holding the FY2024 figures unchanged would have the lanes sum to the
    # FY2024 disbursed while the trunk had already been reduced — the panel
    # fails its own conservation check by exactly the levers' total, which is
    # how this was found.
    #
    # So the held lanes are rescaled onto the struck disbursement. This is not
    # a new rule; it is what "the shape of the dollar does not move, only its
    # level" already says. It is also the first concrete instance of the
    # REDISTRIBUTION RULE listed open on 27 October, and it is deliberately
    # the narrowest possible one: proportional, declared on the plate, and
    # applied only here. It does NOT settle that rule — a peel that moves for
    # a reason specific to one lane should not be spread across all of them,
    # and working that through all twelve peels is still open.
    # Ledger.disbursed() returns None while any pre-disbursement peel is
    # absent, which is correct for the conserving gate and useless here: on
    # this panel three of them are absent by design and always will be until
    # they are acquired. The struck figure is 100 less the peels that DO carry
    # a value, which is exactly what the drawing subtracts, so it is computed
    # the same way here rather than inferred from a gate that cannot run.
    from ledger import PRE_DISBURSE as _PRE
    _taken = sum(x.amount.n for x in peels
                 if x.charged in _PRE and not x.outside
                 and not x.amount.is_absent)
    _disbursed = 100.0 - _taken
    _lane_total = sum(p.capitation.n for p in as_is.lanes())
    _REDIST = 1.0 if _lane_total <= 0 else _disbursed / _lane_total

    def _scaled(f: Fig) -> Fig:
        h = _held(f)
        if h.is_absent or _REDIST == 1.0:
            return h
        return Fig(h.value * _REDIST, source=h.source, vintage=h.vintage,
                   basis=h.basis, status=MODELLED,
                   note=h.note + " Rescaled onto the FY2030 disbursement, "
                                 "which the HR-1 levers have already reduced.")

    payers = [Payer(p.key, p.label, p.kind,
                    capitation=_scaled(p.capitation),
                    care=_scaled(p.care),
                    parent=p.parent, entity=p.entity)
              for p in as_is.payers]

    nodes = list(as_is.nodes)
    # The rows are the PAYING LANES, not every payer. `payers` carries the
    # named plans as children of the mco lane, and a child does not pay claims
    # in its own right on this matrix — the as-is ledger has carried three
    # rows throughout. Building the matrix off `payers` put nine rows against
    # three lanes, which conserves arithmetically (absent plus absent balances)
    # and is wrong the moment anything draws it. Found 2026-10-29, the first
    # time anything built this panel.
    _rows = list(as_is.claims.rows)
    claims = Matrix(
        "claims", rows=_rows, cols=nodes,
        row_margin={r: _absent_share(NO_HUNDRED) for r in _rows},
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
            # THE AS-IS DECLARATIONS TRAVEL WITH THE AS-IS FIGURES. This panel
            # carries FY2024's payers, nodes and claims forward under held
            # composition; it was carrying the figures and dropping the
            # declarations that excuse their absences, so every undivided
            # retention read as undeclared. Found 2026-10-29, the first time
            # anything gated this ledger.
            *as_is.declared,
            "dc2030.hundred_modelled_national_rate",
            "dc2030.levers_three_of_seven_absent",
            "dc2030.provider_tax_coupled_modelled_in_sequence",
            "dc2030.provider_tax_published_non_federal",
            "dc2030.directed_payment_first_year_resolved",
            "dc2030.enrolment_rate_band_with_default",
            "dc2030.rate_band_ends_not_like_for_like",
            "dc2030.residual_lane_renamed_for_dc",
            "dc2030.service_allocation_absent",
            "dc2030.composition_held_from_fy2024",
            # the claims fan is unallocated, as in FY2024, and says so per row
            "claims:mco", "claims:dual", "claims:ffs",
        ],
        declarations=[
            HUNDRED_NOTE,
            # carried from the as-is panel with the figures it excuses
            "Public-company earnings and dual-plan retention: no DC figure",
            "The payer lanes are the FY2024 composition rescaled "
            "proportionally onto the FY2030 disbursement, which the HR-1 "
            "levers have already reduced. Proportional because the stated "
            "assumption is that the shape of the dollar does not move, only "
            "its level; no lane is claimed to absorb more of a lever than "
            "another. A lever that falls on one lane in particular would "
            "break that, and would be drawn differently.",
            "Four of the seven HR-1 tributaries are now derived on District "
            "inputs and three remain absent. Nothing on this panel is "
            "allocated from CBO's national score: the denominators are "
            "DHCF's, the dollars are DHCF's, and where a rate is modelled it "
            "is declared as one. The three absent levers are absent for "
            "three different reasons, and each records what would be needed "
            "to derive it from District sources.",
            "Section 71102, the blocked eligibility-and-enrolment rule, is "
            "left absent deliberately. Its effect falls on process rather "
            "than on a nameable group, and the people affected are those who "
            "would have enrolled or stayed enrolled under easier mechanics — "
            "a counterfactual, not a row in any District report. A "
            "provision-by-provision mapping of our own would be a modelled "
            "step with no source behind it.",
            "The residual lane is renamed for the District. Nationally it is "
            "a remainder defined by what CBO scored, which cannot be "
            "re-derived from District sources because it is not a thing. The "
            "DC lane carries three named District provisions instead — the "
            "LTSS home equity cap, the legal immigrant eligibility "
            "restriction, and retroactive coverage — and is NOT comparable "
            "lane-to-lane with the national residual. None is sized, so the "
            "lane's amount stays absent. The immigrant provision is under a "
            "preliminary injunction and its status is contested.",
            "The two enrolment levers rest on one modelled step: the share of "
            "the expansion group that does not survive them. It is published "
            "as a band with a declared default inside it, and the default is "
            "the rate implied by CBO's own score rather than a figure of our "
            "choosing. THE BAND'S ENDS ARE NOT LIKE-FOR-LIKE WITH ITS "
            "DEFAULT: the default is a share of expansion-group spending, "
            "which includes people the requirement exempts, while the "
            "Arkansas and New Hampshire outcomes are coverage loss among "
            "those subject to the requirement. Until the District's exempt "
            "share is established the upper end is an upper bound.",
            "Provider tax limits and directed payment caps are coupled in the "
            "District and are not coupled in the national model. DC's "
            "directed payments are financed by a hospital provider tax, the "
            "tax freeze returns the programme to its FY2025 level in FY2027, "
            "and the phase-down then runs on that reverted base from FY2029. "
            "The coupling is now MODELLED IN SEQUENCE. The two lanes do not "
            "double-count because they are not the same dollar: the tax "
            "lever is non-federal FINANCING that will not be collected and "
            "leaves at state government, the directed payment lever is a "
            "PAYMENT that will not be made and leaves at claims. Two stages "
            "of one event, drawn where the money actually stops.",
            "The provider tax lever is published at the NON-FEDERAL level. "
            "In the District the dedicated tax is the non-federal share and "
            "it draws federal match, so a dollar of tax never collected "
            "costs more than a dollar of Medicaid. The multiplier is not "
            "established and is declared absent rather than guessed. This is "
            "a divergence from the national treatment, not an application "
            "of it.",
            "Section 71115's rate taper does not reach the District at all. "
            "The expansion-state safe harbour steps down to 3.5 percent by "
            "FY2032 and DC's hospital tax is 3 percent of net patient "
            "revenue, below every step including the floor. The District's "
            "entire exposure is the freeze on taxes not imposed as of 4 July "
            "2025. A jurisdiction can be fully exposed to the section while "
            "sitting under every threshold in its schedule.",
            "The first year of the directed payment phase-down is FY2029, "
            "resolved on the rule. CMS-2449-P states that the phase-down "
            "begins with the first rating period starting on or after "
            "1 January 2028, and DC's rating period is the federal fiscal "
            "year, confirmed on two documents. A period beginning 1 October "
            "2027 starts too early. DHCF's own budget materials say FY2028, "
            "which would make FY2030 the third step and the reduction "
            "$145.56M; the disagreement is recorded rather than averaged, "
            "and the model does not move to meet it.",
            "The phase-down does not terminate by FY2030. KFF's analysis of "
            "the approved preprints puts 100 percent of the District's "
            "hospital directed payment above the new limit, because the base "
            "rate alone already exceeds the Medicare-based ceiling, so the "
            "programme runs down over ten steps and FY2030 at two is "
            "partial. Stating the termination YEAR on District evidence "
            "rather than on KFF's conversion needs DC hospitals' commercial "
            "price as a percentage of Medicare, which is not yet acquired.",
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
        held = "DERIVED" if p.key in _DERIVED else (
            "absent" if p.amount.is_absent else "held")
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
