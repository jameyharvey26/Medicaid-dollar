#!/bin/bash
#
# SAVE TO GITHUB.command
#
# Double-click this file to commit and push the Medicaid dollar project.
# It shows you what changed and asks before doing anything.
#
# One-time setup is in SAVE_SCRIPT_SETUP.md.
#

# ---------------------------------------------------------------------------
# SETTING: where the repo lives on this Mac.
#
# Leave this alone if you keep this script INSIDE the repo folder.
# Otherwise put the full path between the quotes, e.g.
#   REPO_DIR="/Users/jamey/Documents/Medicaid-dollar"
# ---------------------------------------------------------------------------
REPO_DIR=""

EXPECTED_REMOTE="Medicaid-dollar"
EXPECTED_BRANCH="main"

# ---------------------------------------------------------------------------

bold=$'\033[1m'; red=$'\033[31m'; grn=$'\033[32m'; ylw=$'\033[33m'; off=$'\033[0m'

say()  { printf "%s\n" "$*"; }
head1() { printf "\n%s%s%s\n" "$bold" "$*" "$off"; }
ok()   { printf "%s  OK  %s %s\n" "$grn" "$off" "$*"; }
warn() { printf "%s WARN %s %s\n" "$ylw" "$off" "$*"; }

# Keep the window open no matter how we exit, so errors are readable.
finish() {
  printf "\n%s----------------------------------------------------------%s\n" "$bold" "$off"
  say "Press Return to close this window."
  read -r _
  exit "${1:-0}"
}
fail() { printf "\n%s STOP %s %s\n" "$red" "$off" "$*"; finish 1; }

clear
head1 "Medicaid dollar — save to GitHub"

# --- 1. Find the repo ------------------------------------------------------

if [ -z "$REPO_DIR" ]; then
  REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
fi

cd "$REPO_DIR" 2>/dev/null || fail "Can't find the folder:
    $REPO_DIR
  Open this script in TextEdit and set REPO_DIR to the right path."

git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || fail "This folder is not a git repository:
    $REPO_DIR
  Either move this script into the Medicaid-dollar folder, or set
  REPO_DIR near the top of this file to point at it."

# Move to the repo root in case the script sits in a subfolder.
cd "$(git rev-parse --show-toplevel)" || fail "Could not reach the repository root."
say "Folder:  $(pwd)"

# --- 2. Check it is the right repo and the right branch --------------------

REMOTE_URL="$(git remote get-url origin 2>/dev/null)"
case "$REMOTE_URL" in
  *"$EXPECTED_REMOTE"*) ok "Repository is $EXPECTED_REMOTE" ;;
  "") fail "This repository has no 'origin' remote set up." ;;
  *)  warn "Remote does not look like $EXPECTED_REMOTE:"
      say  "         $REMOTE_URL"
      printf "\n  Continue anyway? [y/N] "
      read -r a; case "$a" in [Yy]*) ;; *) say "Stopped."; finish 0;; esac ;;
esac

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$BRANCH" != "$EXPECTED_BRANCH" ]; then
  warn "You are on branch '$BRANCH', not '$EXPECTED_BRANCH'."
  printf "  Continue anyway? [y/N] "
  read -r a; case "$a" in [Yy]*) ;; *) say "Stopped."; finish 0;; esac
else
  ok "Branch is $EXPECTED_BRANCH"
fi

# --- 3. Is anything actually changed? --------------------------------------

if [ -z "$(git status --porcelain)" ]; then
  head1 "Nothing to save."
  say "Every file here already matches GitHub."
  finish 0
fi

# --- 4. Warn if GitHub has moved ahead -------------------------------------

say ""
say "Checking GitHub..."
if git fetch --quiet origin "$BRANCH" 2>/dev/null; then
  BEHIND="$(git rev-list --count HEAD..origin/"$BRANCH" 2>/dev/null || echo 0)"
  if [ "${BEHIND:-0}" -gt 0 ]; then
    warn "GitHub has $BEHIND commit(s) you don't have locally."
    say  "         Pushing may be rejected. If it is, that's not a"
    say  "         disaster — nothing is lost, it just needs a pull first."
  else
    ok "Up to date with GitHub"
  fi
else
  warn "Couldn't reach GitHub to check. Carrying on."
fi

# --- 5. Show exactly what will be saved ------------------------------------

head1 "Files that changed"
git status --short

head1 "Size of the changes"
git diff --stat HEAD

head1 "Line-by-line changes"
say "(Space = next page, q = done reading)"
say ""
sleep 1
if command -v less >/dev/null 2>&1; then
  git --no-pager diff HEAD --color=always | less -R
else
  git --no-pager diff HEAD --color=always | cat
fi

# --- 6. Confirm ------------------------------------------------------------

head1 "Ready to save"
say "Read the changes above. If anything looks wrong — a number you"
say "didn't change, a file you didn't touch — answer no and stop."
say ""
printf "  Save these changes to GitHub? [y/N] "
read -r a
case "$a" in [Yy]*) ;; *) say ""; say "Stopped. Nothing was saved."; finish 0;; esac

# --- 7. Commit message -----------------------------------------------------

DEFAULT_MSG="Session update $(date '+%Y-%m-%d')"
head1 "Commit message"
say "Describe what changed. Press Return on its own to use:"
say "  \"$DEFAULT_MSG\""
say ""
printf "  Message: "
read -r MSG
[ -z "$MSG" ] && MSG="$DEFAULT_MSG"

# --- 8. Do it --------------------------------------------------------------

head1 "Saving"

git add -A || fail "Could not stage the changes."
ok "Staged"

git commit -m "$MSG" || fail "Could not commit."
ok "Committed"

say ""
say "Pushing to GitHub..."
if git push origin "$BRANCH"; then
  ok "Pushed to GitHub"
  head1 "Done."
  say "Saved as: $MSG"
  say ""
  say "$(git log -1 --format='%h  %ad' --date=format:'%d %b %Y, %-I:%M %p')"
else
  printf "\n%s STOP %s The commit was saved on this Mac but the push failed.\n" "$red" "$off"
  say ""
  say "Nothing is lost. The usual cause is that GitHub has changes"
  say "you don't have yet. To fix it, run this in Terminal from"
  say "the repo folder:"
  say ""
  say "    git pull --rebase origin $BRANCH"
  say "    git push origin $BRANCH"
  say ""
  say "Or ask Claude, mentioning that the push was rejected."
  finish 1
fi

finish 0
