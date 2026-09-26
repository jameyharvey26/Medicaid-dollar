#!/bin/bash
# DELETE OLD FILES.command
#
# Double-click this. It removes files the last commit superseded, then GitHub
# Desktop shows them as deletions you can commit with everything else.
#
# GitHub Desktop cannot delete files. It only reports what changed on disk. So a
# deletion has to happen in Finder or here, and doing it here means it happens to
# the right list every time instead of by hand, one filename at a time.
#
# Safe by design: it only removes names on the list below, it refuses to run
# anywhere except the repo, and it shows you the list and waits for a yes.

cd "$(dirname "$0")" || exit 1

# ---- the list. Edit this line group when a commit supersedes something. -----
FILES=(
  # 2026-09-18. byteproof.py proved the Ledger path rendered identically to the
  # old instances.py path — migration scaffolding, and its premise expired when
  # D-70 moved the national baseline. renderproof.py replaces it.
  "byteproof.py"
  # The two PDFs carry Sheila Yahyazadeh's name and employer on the cover and
  # the author page. D-68 took her off every artifact; these were deleted rather
  # than re-rendered. Do not regenerate them.
  "Medicaid_Dollars_National_DRAFT_v4.pdf"
  "Medicaid_Dollars_National_TYPST.pdf"

  # 2026-09-26. render_v6_0.py wrote its HTML into a temp directory, so every
  # relative figure path resolved to nothing and Chromium printed the paper as
  # broken image icons without complaining. render_v6_1.py fixes it and now
  # takes the manuscript as an argument, so the retained v6.0 whole-number
  # release still renders:  python3 render_v6_1.py paper_national_v6_0.html
  # paper_national_v6_0.html itself is KEPT — whole-number releases are
  # permanent. Only the renderer and the defective PDF go.
  "render_v6_0.py"
  # 192 kB with eighteen figures in it, which is the size of a paper with no
  # pictures. It has none. Superseded by v6.1 at 3.1 MB. Do not regenerate.
  "Medicaid_Dollars_National_v6.0.pdf"
)

# Superseded earlier and already gone; kept so the script is idempotent if an
# old checkout turns up.
#   Medicaid_Dollars_National_DRAFT_v3.pdf
#   paper_national_v3.html
#   render_v3.py
# ----------------------------------------------------------------------------

echo
echo "Medicaid-dollar cleanup"
echo "Folder: $(pwd)"
echo

# Refuse to run outside the repo. A wildcard delete in the wrong folder is the
# one failure mode worth engineering against.
if [ ! -f "build.py" ] || [ ! -f "instances.py" ]; then
  echo "This does not look like the Medicaid-dollar repo (no build.py)."
  echo "Nothing deleted. Close this window."
  echo
  read -r -p "Press return to close. "
  exit 1
fi

present=()
for f in "${FILES[@]}"; do
  [ -e "$f" ] && present+=("$f")
done

if [ ${#present[@]} -eq 0 ]; then
  echo "Nothing to delete. Every file on the list is already gone."
  echo
  read -r -p "Press return to close. "
  exit 0
fi

echo "These ${#present[@]} file(s) will be moved to the Trash:"
echo
for f in "${present[@]}"; do echo "   $f"; done
echo
read -r -p "Type yes to continue: " answer

if [ "$answer" != "yes" ]; then
  echo
  echo "Cancelled. Nothing deleted."
  echo
  read -r -p "Press return to close. "
  exit 0
fi

# Trash rather than rm, so a mistake is recoverable.
for f in "${present[@]}"; do
  osascript -e "tell application \"Finder\" to delete POSIX file \"$(pwd)/$f\"" \
    >/dev/null 2>&1 || rm -f "$f"
  echo "   removed  $f"
done

echo
echo "Done. Open GitHub Desktop: the deletions are now in your changes list."
echo "Commit them with everything else."
echo
read -r -p "Press return to close. "
