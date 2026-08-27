# Setting up the save script

One-time setup. Ten minutes, then saving is a double-click forever after.

---

## Step 1 — Put the script in the repo folder

Find the `Medicaid-dollar` folder on your Mac. That is the folder with `ramp.py`,
`build_sankey.py`, `README.md` and the rest in it.

Drag **`SAVE TO GITHUB.command`** into that folder.

If you would rather keep it somewhere else, like your Desktop, that works too, but
you have to tell it where the repo is. Right-click the script, choose **Open With →
TextEdit**, and near the top change:

    REPO_DIR=""

to the full path, for example:

    REPO_DIR="/Users/jamey/Documents/Medicaid-dollar"

Save and close.

## Step 2 — Make it double-clickable

macOS may have stripped permission to run it when the file came out of the zip. Open
**Terminal** once (Applications → Utilities → Terminal), type `chmod +x ` with a
trailing space, then **drag the script file into the Terminal window**. That fills in
the path for you. Press Return.

It should look roughly like:

    chmod +x /Users/jamey/Documents/Medicaid-dollar/SAVE\ TO\ GITHUB.command

This is the only time you need Terminal.

## Step 3 — Get past Gatekeeper the first time

The first double-click, macOS will refuse to open it because it came from the
internet. **Right-click** the file and choose **Open**, then **Open** again in the
warning box. macOS remembers, and every double-click after that just works.

## Step 4 — Make sure git can reach GitHub without asking for a password

Test it. In the same Terminal window, drag the repo folder in after typing `cd `,
press Return, then run:

    git push

- **No error** — you are set. Done.
- **"could not read Username"** or a password prompt — git has no saved credentials.
  Fix it once by installing **GitHub Desktop** from desktop.github.com and signing
  in. It sets up the credentials that this script then borrows. You do not have to
  use GitHub Desktop afterwards, though it is a reasonable backup when the script
  reports something odd.

Note that GitHub stopped accepting account passwords for this in 2021. If something
prompts you for a password, it wants a personal access token, not your GitHub
password. Signing in through GitHub Desktop avoids the whole business.

---

## Using it

Double-click. It will:

1. Confirm it is in the right repo, on `main`
2. Tell you if GitHub has changes you do not have
3. Show you every file that changed and every changed line
4. Ask before saving anything
5. Ask for a description of what changed
6. Commit and push

**The diff view scrolls with the space bar. Press `q` when you are done reading it.**
That is the one keystroke to remember, and the script says so on screen.

The confirmation step is the point of the whole thing, not a formality. Standing
practice on this project is to verify the diff shows the expected changes and nothing
else before committing. Read it. If a number moved that you did not move, answer `n`.
Nothing is saved and nothing is lost.

## When something goes wrong

Every message the script prints tells you what state things are in. The one worth
knowing in advance: if the **push** fails, the commit already succeeded on your Mac.
Your work is saved. It just has not reached GitHub yet, usually because GitHub moved
ahead of you. The script prints the two commands that fix it.

Nothing this script does can lose work. It only ever adds commits.

## What it will not do

It will not pull, merge, resolve conflicts, create branches, or delete anything. If
you need any of that, it is a conversation with Claude, not a double-click.
