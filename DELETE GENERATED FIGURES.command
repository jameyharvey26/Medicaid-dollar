#!/bin/bash
# DELETE GENERATED FIGURES.command
#
# JW, 27 September 2026. A crop of a diagram that is generated from code does
# not belong in the repository. The panel moves, the crop does not, and the
# manuscript publishes a stale number with nothing in the repo able to tell.
# Every file removed below is reproduced byte-identically by:
#
#     python3 build.py        # renders the panels into reference_renders/
#     python3 make_figs.py    # crops and generates everything in paper_figs/
#     python3 deckalts.py     # renders the deck figures into deck_alts/
#
# That was tested, not assumed: these four directories were deleted whole and
# rebuilt, and every file listed here came back with the same checksum.
#
# AFTER RUNNING THIS, render_v7_1.py WILL FAIL until build.py and make_figs.py
# have run. That is the correct dependency order and it is the point: the
# manuscript should not be renderable from pictures nobody can reproduce.
#
# Run from the repository root.

set -u
cd "$(dirname "$0")"

if [ ! -f build.py ] || [ ! -f make_figs.py ]; then
  echo "Not in the repository root — build.py and make_figs.py not found."
  exit 1
fi

echo "Removing generated figure artifacts."
echo

# ---------------------------------------------------------------------------
# 1. paper_figs/ — every figure the manuscript references.
#    21 crops registered in crops.json, four generated custom figures copied
#    from cover/, the cover taper, and crops.json itself. All from make_figs.py.
# ---------------------------------------------------------------------------
rm -f paper_figs/crops.json
rm -f paper_figs/fig1_panel_2024.png
rm -f paper_figs/fig2_sources.png
rm -f paper_figs/fig3_payer.png
rm -f paper_figs/fig4_providers.png
rm -f paper_figs/fig4b_providers_pies.png
rm -f paper_figs/fig5_numberline.png
rm -f paper_figs/fig6_panel_2030.png
rm -f paper_figs/fig6_taper_all.png
rm -f paper_figs/fig7_lanes_2030.png
rm -f paper_figs/fig7_taper_upstream.png
rm -f paper_figs/fig8_payer_2030.png
rm -f paper_figs/fig8_taper_claims.png
rm -f paper_figs/fig9_population.png
rm -f paper_figs/fig9_providers_2030.png
rm -f paper_figs/fig9b_providers_pies_2030.png
rm -f paper_figs/fig10_numberline_2030.png
rm -f paper_figs/fig11_beneficiaries_2030.png
rm -f paper_figs/fig12_sources_2030.png
rm -f paper_figs/fig13_terminals_2030.png
rm -f paper_figs/fig14_terminals_left.png
rm -f paper_figs/figA_lines_pair.png
rm -f paper_figs/figB_provisions_with_line.png
rm -f paper_figs/cover_taper.png
rm -f paper_figs/cover_taper_alt.txt

# ---------------------------------------------------------------------------
# 2. cover/ — the generators' own output. taper.py, population.py and
#    cover_taper.py write here; make_figs.py copies four of them onward.
# ---------------------------------------------------------------------------
rm -f cover/cover_taper.png cover/cover_taper.svg cover/cover_taper_alt.txt
rm -f cover/cover_taper_standalone.png cover/cover_taper_standalone.svg
rm -f cover/cover_taper_standalone_alt.txt
rm -f cover/fig6_taper_all.png cover/fig6_taper_all.svg
rm -f cover/fig6_taper_all_alt.txt
rm -f cover/fig7_taper_upstream.png cover/fig7_taper_upstream.svg
rm -f cover/fig7_taper_upstream_alt.txt
rm -f cover/fig8_taper_claims.png cover/fig8_taper_claims.svg
rm -f cover/fig8_taper_claims_alt.txt
rm -f cover/fig9_population.png cover/fig9_population.svg
rm -f cover/fig9_population_alt.txt
rm -f cover/fig9_population_standalone.png
rm -f cover/fig9_population_standalone.svg
rm -f cover/fig9_population_standalone_alt.txt

# ---------------------------------------------------------------------------
# 3. reference_renders/ — the three panels build.py renders, and the two
#    contact sheets it assembles from them.
#    sign_*.png are NOT removed. See the note at the foot of this script.
# ---------------------------------------------------------------------------
rm -f reference_renders/national_2024_baseline.svg
rm -f reference_renders/national_2024_overlay.svg
rm -f reference_renders/national_2024_combined.svg
rm -f reference_renders/national_2024_combined.png
rm -f reference_renders/national_2030_mixed_baseline.svg
rm -f reference_renders/national_2030_mixed_overlay.svg
rm -f reference_renders/national_2030_mixed_combined.svg
rm -f reference_renders/national_2030_mixed_combined.png
rm -f reference_renders/dc_2024_baseline.svg
rm -f reference_renders/dc_2024_overlay.svg
rm -f reference_renders/dc_2024_combined.svg
rm -f reference_renders/dc_2024_combined.png
rm -f reference_renders/sheet_working.png
rm -f reference_renders/sheet_national_dc.png

# ---------------------------------------------------------------------------
# 4. deck_alts/ — the deck figures, both framings, from deckalts.py.
# ---------------------------------------------------------------------------
rm -f deck_alts/*.png deck_alts/*.svg

# ---------------------------------------------------------------------------
# 5. Loose renders at the repository root.
# ---------------------------------------------------------------------------
rm -f _render_tmp.html
rm -f palette_color.png palette_grayscale.png     # build_palette_test.py
rm -f sheet_all.png                               # sheet.py, when present

echo
echo "Done. Rebuild with:"
echo "    python3 build.py && python3 make_figs.py && python3 deckalts.py"
echo

# ===========================================================================
# HELD BACK — four groups NOT deleted, and why.
#
# A. reference_renders/sign_*.png
#       sign_2024.png, sign_2030.png, sign_2026-09-25.png,
#       sign_2026-09-26_D91.png, sign_2026-09-26_D102.png
#    These are not derived figures. They are the comparison sheets a signature
#    was agreed on, and signatures.py and gates.py cite them BY FILENAME as the
#    artifact of that agreement (S-093). Deleting them breaks the provenance
#    chain for every signed figure in the model. They should be kept
#    permanently, the way whole-number manuscript releases are.
#
# B. reference_renders/national_2030_holds_* and national_2030_scales_*
#    Eight files. build.py renders three panels — 2024, 2030_mixed and dc — and
#    produces NEITHER of these variants. Nothing in the repo regenerates them,
#    so deleting them destroys them. Worse: `sheet.py --set overhead` asks for
#    national_2030_holds_combined.png, which means build.py ALREADY FAILS on a
#    clean tree, at the overhead contact sheet, with:
#
#        panel 'national_2030_holds' wants national_2030_holds_combined.png,
#        which is not in reference_renders/.
#
#    Also reference_renders/sheet_overhead.png, which is downstream of it.
#    Either build.py should render the variants or sheet.py should stop asking
#    for them. Until that is settled these stay, because they are the only
#    copies that exist.
#
# C. paper_figs/fig13_households.png and fig15_households.png
#    Built by family.py, which make_figs.py deliberately does not run: the
#    households are set aside for a later edition (D-92, JW 2026-09-26).
#    They regenerate with `python3 family.py`, so they are safe to delete —
#    but they belong to a parked feature rather than to this build, and that
#    is a decision rather than hygiene.
#
# D. Medicaid_Dollars_National_v*.pdf
#    Whole-number releases are kept permanently.
# ===========================================================================
