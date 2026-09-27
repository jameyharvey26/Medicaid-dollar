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
  # The two PDFs carry the co-author's name and employer on the cover and
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

  # 2026-09-27, JW. The co-author's held bio comes out of the repo. Her name
  # and employer are redacted in place everywhere else; this file is nothing
  # BUT that material, so it goes.
  #
  # The entry stays on the list even though the filename carries her first
  # name. It was taken off once, on the reasoning that a deletion list should
  # not name the person it protects - which meant the file was deleted in the
  # Author's sandbox and NOT on JW's machine, where the list is the only thing
  # that acts. A tidy list that does not delete the file is worse than an
  # untidy one that does. Take it off after the deletion has been committed.
  #
  # Deleting it does not remove it from the repository's HISTORY. Every past
  # commit still contains it and the repo is public, so this stops future
  # exposure and nothing else. Removing it from history needs the repo made
  # private and the history rewritten. Raised with JW at v7.1.
  "AUTHOR_HELD_SHEILA.md"

  # 2026-09-27. Dead exploratory cover studies from before D-95. No script
  # produces them, and tapertest.py reports them as faults on every run
  # because they follow a leader rule that has since changed twice.
  "cover/cover_A_taper.svg"
  "cover/cover_A_taper.png"
  "cover/cover_B_paired.svg"
  "cover/cover_B_paired.png"
  "cover/cover_C_fall.svg"
  "cover/cover_C_fall.png"

  # Superseded by the taper family at v7.0: payer.py was two attempts at a
  # figure the family already makes (D-100), and these crops are the pictures
  # the tapers replaced.
  "payer.py"
  "paper_figs/fig8_payer_2030.png"
  "paper_figs/fig9b_providers_pies_2030.png"
  "paper_figs/fig11_beneficiaries_2030.png"
  "paper_figs/fig12_sources_2030.png"
  "paper_figs/fig13_terminals_2030.png"
  "paper_figs/fig14_terminals_left.png"
  "paper_figs/figB_provisions_with_line.png"

  # v7.0 is a point release superseded within the day. The whole-number
  # release itself is KEPT as paper_national_v7_0.html; only the PDF and the
  # renderer go, and v7.0 still renders with
  #   python3 render_v7_1.py paper_national_v7_0.html
  "render_v7_0.py"
  "Medicaid_Dollars_National_v7.0.pdf"

  # v6.2 is a point release. The whole-number releases stay; this does not.
  "paper_national_v6_2.html"
  "render_v6_2.py"
  "Medicaid_Dollars_National_v6.2.pdf"
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


# ---- did it actually work? --------------------------------------------------
# The list is only as good as what is left on disk afterwards, and the check
# has to run whether or not anything was deleted this time. It did not, once,
# and a file that should have gone stayed for two commits.
leakcheck() {
  local hits
  hits=$(grep -ril "yahyazadeh\|carefirst" . --exclude-dir=.git 2>/dev/null \
         | grep -v "DELETE OLD FILES.command")
  if [ -n "$hits" ]; then
    echo
    echo "WARNING: the co-author's name or employer is still in this folder:"
    echo "$hits" | sed 's/^/   /'
    echo
  fi
}

present=()
for f in "${FILES[@]}"; do
  [ -e "$f" ] && present+=("$f")
done

if [ ${#present[@]} -eq 0 ]; then
  echo "Nothing to delete. Every file on the list is already gone."
  leakcheck
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
leakcheck

read -r -p "Press return to close. "
