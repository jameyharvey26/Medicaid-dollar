# landing.py - the project's public address, in one place.
#
# D-103. The URL was a "[landing page pending]" placeholder in render_v7_1.py
# and absent from the deck entirely. It now appears in the paper footer and on
# the deck, which is two artifacts quoting one string; S-096 says that is one
# declaration, not two. Change it here and both follow.
#
# The sentence the deck prints is here too, for the same reason: it names the
# URL, so it cannot live in a module that does not own it.

URL = "https://agilian.com/100MedicaidDollarsProject"

# What the deck says about it, in full. JW's wording, 27 September 2026.
DECK_LINE = ("The full white paper, visualization, and data model are "
             f"accessible at {URL}")

# The footer of the manuscript takes the bare address; the footer is set in
# small type and a sentence there would wrap.
FOOTER = URL
