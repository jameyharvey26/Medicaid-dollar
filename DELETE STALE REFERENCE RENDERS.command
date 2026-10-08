#!/bin/bash
# DELETE STALE REFERENCE RENDERS.command
#
# Session of 7 October 2026, DC cycle. ONE item, and it is the committed SVGs
# for the two FY2030 sensitivity variants.
#
# WHAT IS WRONG WITH THEM. These six files are the only panel SVGs committed in
# reference_renders/; everything else in that directory is generated and
# gitignored. They are also STALE: they predate the register blessed on
# 28 September 2026. Rebuilding them with
#
#     python3 "build.py" sensitivity
#
# reproduces render_register/ byte for byte. That was tested, not assumed —
# sha256 of each rebuilt file matches the register, while the committed file
# matches neither:
#
#   national_2030_holds_baseline    committed 1e54a97f…  register db920689…  rebuilt db920689…
#   national_2030_holds_combined    committed 5c8b7985…  register 660992b2…  rebuilt 660992b2…
#   national_2030_holds_overlay     committed bdc5993d…  register 8ef7d6db…  rebuilt 8ef7d6db…
#   national_2030_scales_baseline   committed f8180db7…  register 54f66333…  rebuilt 54f66333…
#   national_2030_scales_combined   committed daf958da…  register 961b72da…  rebuilt 961b72da…
#   national_2030_scales_overlay    committed 2b0115af…  register 898f01e4…  rebuilt 898f01e4…
#
# So the code and the register agree and NO NATIONAL FIGURE HAS MOVED. Only the
# committed files were out of date.
#
# WHY THIS MATTERS RATHER THAN BEING TIDINESS. On a clean clone renderproof.py
# read these stale files and reported six national panels MOVED. On a warm
# working copy a previous session had already rebuilt them, so it went green.
# The suite therefore accused the national model of drifting, but only for
# someone who had just cloned. gates.py has been reordered so that
# `build.py sensitivity` runs BEFORE renderproof.py, which fixes the false red
# whether or not these files are removed. Removing them closes the other half:
# a generated file that is committed will go stale again.
#
# SAFE TO RUN. The six files are preserved as shipped in archive/v8_0/, and
# `python3 "build.py" sensitivity` regenerates them identically. Run the build
# afterwards or renderproof.py will report them missing.
#
# Run from the repository root.

set -u
cd "$(dirname "$0")"

if [ ! -f build.py ] || [ ! -d reference_renders ]; then
  echo "Not in the repository root — build.py or reference_renders/ not found."
  exit 1
fi

if [ ! -d archive/v8_0/reference_renders ]; then
  echo "archive/v8_0/reference_renders/ not found."
  echo "These files are preserved there as shipped. Copy archive/v8_0/ into the"
  echo "repository before running this, or the v8.0 copies are not retained."
  exit 1
fi

echo "Removing six stale committed sensitivity renders."
echo "Preserved as shipped in archive/v8_0/reference_renders/."
echo

rm -f reference_renders/national_2030_holds_baseline.svg
rm -f reference_renders/national_2030_holds_combined.svg
rm -f reference_renders/national_2030_holds_overlay.svg
rm -f reference_renders/national_2030_scales_baseline.svg
rm -f reference_renders/national_2030_scales_combined.svg
rm -f reference_renders/national_2030_scales_overlay.svg

echo "Done. Now run:"
echo
echo "    python3 \"build.py\" sensitivity"
echo "    python3 gates.py"
echo
echo "Expected after that: 14 green, render_v8_0.py red on its two known checks."
