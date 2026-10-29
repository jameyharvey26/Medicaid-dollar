#!/bin/bash
#
# FINISH THE 29 OCT UPDATE.command
#
# Double-click this AFTER you have copied the 29 October files into the repo.
# It does the three things that have to happen after those files land, in the
# right order, and tells you plainly whether you are clear to commit.
#
# It changes two files and nothing else: the engine's DATA line and
# DC_PROVENANCE.md. It does not commit, push, or delete anything.
#

REPO_DIR=""

bold=$'\033[1m'; red=$'\033[31m'; grn=$'\033[32m'; ylw=$'\033[33m'; off=$'\033[0m'

cd "${REPO_DIR:-$(dirname "$0")}" || { echo "${red}Cannot find the repo.${off}"; read -r; exit 1; }

echo
echo "${bold}Finishing the 29 October update${off}"
echo "  in $(pwd)"
echo

if [ ! -f engine_data_export.py ] || [ ! -f gates.py ]; then
  echo "${red}This does not look like the repo folder.${off}"
  echo "Put this file inside the Medicaid-dollar folder and run it again."
  echo; read -r -p "Press return to close."; exit 1
fi

PY=python3
command -v $PY >/dev/null 2>&1 || { echo "${red}python3 not found.${off}"; read -r; exit 1; }

# --- 1 ------------------------------------------------------------------
echo "${bold}1 of 3  Putting your ledger's figures back into the engine${off}"
echo "        The engine file was COPIED, not generated, because its drawing"
echo "        code changed. This rewrites its data line from your ledgers."
echo
if $PY engine_data_export.py; then
  echo "${grn}        done${off}"
else
  echo "${red}        FAILED — stop here and send me what it printed.${off}"
  echo; read -r -p "Press return to close."; exit 1
fi
echo

# --- 2 ------------------------------------------------------------------
echo "${bold}2 of 3  Regenerating the provenance record${off}"
echo "        DC_PROVENANCE.md — every DC figure and whether anyone checked it."
echo
$PY dc_provenance.py --write
echo

# --- 3 ------------------------------------------------------------------
echo "${bold}3 of 3  Running the gates. This takes a few minutes.${off}"
echo
$PY gates.py
GATES=$?
echo

echo "============================================================"
if [ $GATES -eq 0 ]; then
  echo "${grn}${bold}All gates green. You are clear to commit.${off}"
  echo
  echo "In GitHub Desktop: review the changes, write a message, Commit to"
  echo "main, then Push origin."
else
  echo "${ylw}${bold}At least one gate is not as expected. Read the list above.${off}"
  echo
  echo "${bold}renderproof is EXPECTED to be red${off} until the six national"
  echo "FY2030 panels are blessed. They moved at commit c518476 on 28"
  echo "October, when HR-1 terminals were pinned to the fan instead of to"
  echo "absolute canvas y so the geometry could be exported to the engine."
  echo "No figure changed; the terminals move about a pixel. The reasoning"
  echo "and the command that closes it are written down in ${bold}RENDER_DEFECTS.md${off}."
  echo
  echo "The three DC panels were blessed on 29 October and should read"
  echo "unchanged. If they do NOT, the DC data has moved again and that is"
  echo "worth looking at before a demo."
  echo
  echo "If anything ELSE is red, do not commit. Send me the list."
fi
echo "============================================================"
echo
read -r -p "Press return to close."
