#!/bin/bash
#
# BLESS THE DC PANEL.command
#
# Double-click this ONLY after you have looked at the diffs renderproof named
# and agree the DC panel should look the way it now looks.
#
# Blessing records the current picture as the one every future render is
# compared against. It is a deliberate act and it is yours to make, which is
# why it is a separate file from FINISH THE 29 OCT UPDATE.command.
#
# It blesses the THREE DC panels and nothing else. That is what --only dc_2024
# does, and it matters: on 29 October nine panels had moved, for two unrelated
# reasons, and blessing all nine under this reason would have filed a false
# reason against six national panels. See RENDER_DEFECTS.md.
#
# Running it twice is harmless. If the DC panels have not moved since the last
# blessing, it rewrites the same bytes and the same reason.
#

REPO_DIR=""
bold=$'\033[1m'; red=$'\033[31m'; grn=$'\033[32m'; off=$'\033[0m'
cd "${REPO_DIR:-$(dirname "$0")}" || { echo "${red}Cannot find the repo.${off}"; read -r; exit 1; }

REASON="DC payer column re-based on CY2024 Title XIX reporting; service fan drawn on an assumed national mix and declared ASSUMED, NOT MEASURED on the plate; plans on reserved palette colours. No DC figure is signed."

echo
echo "${bold}About to bless the current renders with this reason:${off}"
echo "  $REASON"
echo
echo "Have you LOOKED at the diff images renderproof named?"
echo "They are in reference_renders/diffs/."
echo
read -r -p "Type  yes  to bless, anything else to cancel: " ans
[ "$ans" = "yes" ] || { echo "Cancelled. Nothing changed."; read -r; exit 0; }

python3 renderproof.py --bless "$REASON" --only dc_2024
echo
echo "${grn}Blessed.${off} Now double-click FINISH THE 29 OCT UPDATE.command again"
echo "to confirm the gates are green before you commit."
echo
read -r -p "Press return to close."
