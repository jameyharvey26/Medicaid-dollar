"""
financing.py - Non-federal share financing assumptions for the $100 Medicaid dollar.

Every value here is a named variable with provenance, vintage, and a footnote key.
Nothing in this file is a derived ledger figure. These are INPUTS, and each one that
is modelled rather than measured must be flagged on the artifact per S-012.

Supports D-39 (provider tax lane splits by what the tax financed), D-40 (second
conserved ledger opening at the state share), D-41 (directed payment lane splits
three ways), D-42 (second ledger carries relief as well as pressure).

Update procedure: change the value, change VINTAGE, change SOURCE, and add a line
to the CHANGELOG at the bottom. Do not change a value without changing its source.
"""

# ---------------------------------------------------------------------------
# FN-1  Provider tax recycling fraction
# ---------------------------------------------------------------------------
# Share of provider tax revenue returned to the SAME providers through a Medicaid
# payment. The complement is the portion that substituted for state general fund,
# which is what moves to the second ledger under D-39.
#
# ORIGIN     MACPAC, 2017.
# VALIDATED  GAO-21-98 (Dec 2020) determined the estimate appropriate after
#            interviews with states and review of additional data.
# CURRENCY   Still in use as a working assumption in GAO-24-106202 (2024), the
#            directed payments report. Not independently re-measured since 2017.
# CAVEAT     Predates the directed payment expansion. Approved services rose from
#            34 in 2017 to 1,667 in 2025 (ASPE 2026). Direction of bias unknown:
#            SDP growth is heavily provider-financed and targeted at the taxed
#            class, which argues the true figure is now HIGHER, not lower.
# STATUS     MODELLED. Flag on artifact and in footnotes.
PROVIDER_TAX_RECYCLE_SHARE = 0.80
PROVIDER_TAX_RECYCLE_VINTAGE = "MACPAC 2017; GAO-21-98 2020; in use GAO-24-106202 2024"

# Complement. Do not hardcode; derive, so the two can never drift apart.
PROVIDER_TAX_GENERAL_SHARE_SUBSTITUTION = 1.0 - PROVIDER_TAX_RECYCLE_SHARE

# ---------------------------------------------------------------------------
# FN-2  Non-federal share composition  (opens the second ledger, D-40)
# ---------------------------------------------------------------------------
# STRUCTURAL SOURCE. National aggregate. Published shares sum to 101 on rounding,
# so they are normalised at use, never at rest.
#
# SOURCE     GAO 2020 (GAO-21-98), state fiscal year 2018, reported via MACPAC.
# BASIS      State fiscal year. NOTE: the $100 ledger is federal fiscal year
#            (D-07). This is a mixed-basis join and must be stated. Most states
#            begin their fiscal year 1 July.
NFS_COMPOSITION_AGGREGATE = {
    "state_general_revenue": 0.68,
    "health_care_related_taxes": 0.17,
    "local_government_igt_cpe": 0.12,
    "other": 0.04,
}
NFS_COMPOSITION_VINTAGE = "GAO-21-98, SFY2018, national aggregate"

# CURRENCY CHECK ONLY. Do not use for ledger arithmetic.
# These are MEDIANS ACROSS STATES. Medians do not sum and do not aggregate;
# they come to 94 for that reason. Their role is to confirm the aggregate above
# has not structurally drifted, and it has not.
# SOURCE   KFF 2025 Medicaid Budget Survey, SFY2026 enacted budgets.
NFS_COMPOSITION_MEDIAN_CHECK = {
    "state_general_revenue": 0.70,
    "health_care_related_taxes": 0.18,
    "local_government_and_other": 0.06,
}
NFS_COMPOSITION_MEDIAN_VINTAGE = "KFF 2025 Medicaid Budget Survey, SFY2026 enacted"

# ---------------------------------------------------------------------------
# FN-3  Directed payment financing mix  (D-41)
# ---------------------------------------------------------------------------
# Share of the SDP non-federal share financed by providers rather than by the
# state's own money. Reported as $8.4B of $12.3B on $35.8B of 2022 SDP spending.
#
# SOURCE   ASPE, August 2026, "An Overview of State-Directed Payments and
#          Medicaid Provider Taxes."
# STATUS   MEASURED for the combined category.
SDP_PROVIDER_FINANCED_SHARE = 8.4 / 12.3          # 0.683
SDP_STATE_GENERAL_FUND_SHARE = 1.0 - SDP_PROVIDER_FINANCED_SHARE
SDP_FINANCING_VINTAGE = "ASPE 2026, CY2022 SDP spending"

# RESOLVED 2026-08-27 session 2 by D-46: NOT SEPARATED, deliberately.
# The split cannot be closed from published data. MACPAC recommended Congress
# require states to report non-federal share by source (general funds, health
# care taxes, IGTs, CPEs); Congress has not acted, so every published figure
# combines taxes and IGTs. CRS RS22843 gives a partial handle (provider taxes
# were 51% of "other state funds" in SFY2018) but on a different denominator.
#
# For the FIRST ledger the distinction is immaterial: both recycle, both mean
# providers lose only the federal match, both are exempt from D-25's gross-up.
# It matters only for which line of the second ledger receives it, and D-03
# node 4 already reads "state and local". Collapsed to one category nationally.
# Revisit for state editions, where single-state preprints make it tractable
# and where the distinction actually carries information.
SDP_PROVIDER_TAX_VS_IGT_SPLIT = None   # unresolved by decision, NOT blocking

# ---------------------------------------------------------------------------
# FN-4  Ledger anchor  (D-10, unchanged, restated here for the join)
# ---------------------------------------------------------------------------
STATE_SHARE_PER_100 = 35.30
FEDERAL_SHARE_PER_100 = 64.70
LEDGER_VINTAGE = "CMS-64 FY2024 via MACStats Feb 2026; total federal $620.4B"


def second_ledger_opening(state_share=STATE_SHARE_PER_100):
    """Decompose the state share by financing source, normalised to conserve.

    Returns dollars per $100 of total Medicaid spending. Conservation is enforced
    by normalisation, since the published aggregate sums to 101 on rounding.
    """
    total = sum(NFS_COMPOSITION_AGGREGATE.values())
    return {k: state_share * v / total for k, v in NFS_COMPOSITION_AGGREGATE.items()}


def provider_tax_split(state_share=STATE_SHARE_PER_100):
    """D-39. Split provider tax financing into recycled and general-fund-substituting.

    The recycled portion never leaves the first ledger as a loss to anyone: the
    provider stops receiving the payment and stops paying the tax, netting the
    federal match. The substituting portion is real displaced general fund and
    moves to the second ledger.
    """
    tax_dollars = second_ledger_opening(state_share)["health_care_related_taxes"]
    return {
        "recycled_to_same_providers": tax_dollars * PROVIDER_TAX_RECYCLE_SHARE,
        "substituting_for_general_fund": tax_dollars * PROVIDER_TAX_GENERAL_SHARE_SUBSTITUTION,
    }


FOOTNOTES = {
    "FN-1": (
        "Provider tax recycling fraction of 80 percent: MACPAC (2017), assessed as "
        "appropriate by GAO after interviews with states and review of additional "
        "data (GAO-21-98, 2020), and still applied as a working assumption in "
        "GAO-24-106202 (2024). Agilian treats this as a modelled input, not a "
        "measured one, and it predates the growth in state directed payments."
    ),
    "FN-2": (
        "Non-federal share composition: GAO analysis, state fiscal year 2018, "
        "reported via MACPAC. Published shares sum to 101 percent on rounding and "
        "are normalised here. State fiscal year basis; the ledger is federal fiscal "
        "year. Confirmed as structurally current against KFF's 2025 Medicaid Budget "
        "Survey of SFY2026 enacted budgets, which reports state medians rather than "
        "a national aggregate and is therefore used as a check only."
    ),
    "FN-3": (
        "Directed payment financing: ASPE (2026), reporting that more than "
        "two-thirds of the non-federal share of 2022 state directed payments, $8.4 "
        "billion of $12.3 billion, was financed through provider taxes or "
        "intergovernmental transfers. The split between the two is not reported and "
        "remains open."
    ),
}

CHANGELOG = [
    "2026-08-27  Created. FN-1 0.80, FN-2 GAO SFY2018 aggregate, FN-3 ASPE 2026.",
    "2026-08-27  D-46: tax-vs-IGT split collapsed for the national edition.",
]

if __name__ == "__main__":
    print(f"Second ledger opening, per $100 (state share ${STATE_SHARE_PER_100}):")
    for k, v in second_ledger_opening().items():
        print(f"  {k:32} ${v:5.2f}")
    print(f"\nD-39 provider tax split (FN-1 = {PROVIDER_TAX_RECYCLE_SHARE}):")
    for k, v in provider_tax_split().items():
        print(f"  {k:32} ${v:5.2f}")
    print(f"\nD-41 SDP financing (FN-3): provider-financed "
          f"{SDP_PROVIDER_FINANCED_SHARE:.1%}, state general fund "
          f"{SDP_STATE_GENERAL_FUND_SHARE:.1%}")
    print("  tax-vs-IGT split: not separated (D-46); see fmap.sdp_split()")
