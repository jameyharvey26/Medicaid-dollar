"""Does every footnote have a caller, and every caller a footnote?

Nothing was checking. Six drafts of cutting and rewriting have left notes with
nothing pointing at them and at least one pointer with no note behind it, and
neither shows up in a render: an orphaned note prints as a paragraph a reader
never has cause to read, and a dangling superscript prints as a number that
goes nowhere.

    python3 notefit.py <manuscript.html>

Callers are `<sup>N</sup>` in the body. Notes are `<p><b>N.</b>` in the Notes
section. A note may also be called by name in prose - "for the reason in note
13" - so that form counts as a caller too; the register does exactly this.

Reports rather than fails. Which orphans to cut and how to renumber is an
editorial decision, not one for a build script.
"""
import re
import sys


def main(path):
    s = open(path).read()
    i = s.index('<h2 class="sec">Notes</h2>')
    body, notes = s[:i], s[i:]

    sup = set(re.findall(r"<sup>(\d+[a-z]?)</sup>", body))
    named = set(re.findall(r"note (\d+[a-z]?)", body))
    used = sup | named
    have = set(re.findall(r"<p><b>(\d+[a-z]?)\.</b>", notes))

    def order(x):
        return (int(re.sub(r"\D", "", x)), x)

    dangling = sorted(used - have, key=order)
    orphan = sorted(have - used, key=order)

    if dangling:
        print("DANGLING - called in the text, no note behind it:")
        for n in dangling:
            print(f"  note {n}")
    if orphan:
        print("ORPHANED - a note nothing points at:")
        for n in orphan:
            print(f"  note {n}")
    if not dangling and not orphan:
        print(f"every note has a caller and every caller a note, "
              f"{len(have)} notes")
    else:
        print(f"\n{len(have)} notes, {len(used)} called. Which orphans to cut "
              f"and how to renumber is editorial.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
