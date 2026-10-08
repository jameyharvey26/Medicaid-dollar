# placeholder.py — violet stand-ins, so an unfinished panel can be looked at.
#
# JW, 2026-10-07: "put a placeholder in the model until we gather the real
# data, and make the placeholder areas violet so I can always see what's just
# there to make the model work."
#
# THE ONE RULE THIS MODULE EXISTS TO NOT BREAK.
# A placeholder carries NO VALUE. It is geometry and nothing else.
#
# The alternative — a Fig with a stand-in number, coloured violet — was
# considered and rejected. A number flows: it satisfies the matrix predicate,
# it closes conservation, it lands in the coverage register, and it reads as a
# figure to every piece of code downstream. The only thing standing between it
# and a published artifact would be a colour, and colour does not survive a
# greyscale print, a screenshot, or a slide someone rebuilds by hand. Absence
# conserves is the rule the DC panel exists to demonstrate; a violet number is
# still a number.
#
# So the Fig stays ABSENT and the VIEW is told to draw a band where the lane
# would have gone. The ledger cannot be made to lie by looking at the drawing.

from ledger import ABSENT, Fig

# The token. One declaration; the renderer reads it rather than carrying its
# own copy. Chosen to sit outside the panel's palette so it cannot be mistaken
# for a data colour at a glance or in a thumbnail.
VIOLET = "#7C3AED"
VIOLET_HATCH = "#A78BFA"       # hatch stroke, for print and greyscale
LABEL = "placeholder — no figure acquired"


class Placeholder:
    """Geometry for a lane whose figure is ABSENT.

    `width` is a drawing width in the panel's own units, invented so the band
    can be seen. It is NOT a quantity, is never divided by a scale, never
    enters a total, and has no provenance because it is not a claim about
    anything.
    """

    __slots__ = ("key", "label", "width", "why")

    def __init__(self, key: str, label: str, width: float, why: str):
        self.key = key
        self.label = label
        self.width = width
        self.why = why

    @property
    def value(self):
        raise TypeError(
            f"placeholder {self.key!r} has no value and never will. It is "
            "drawing geometry. If you need a number here, acquire one.")

    def __repr__(self):
        return f"Placeholder({self.key!r}, width={self.width}, VIOLET)"


def for_absent(key: str, label: str, fig: Fig, width: float = 2.0):
    """A placeholder for an ABSENT figure, or None if the figure is present.

    Refuses to stand in for a figure that exists: a placeholder over a real
    number would hide the number, which is the opposite failure and just as
    bad.
    """
    if fig.status != ABSENT or not fig.is_absent:
        return None
    return Placeholder(key, label, width, fig.note or LABEL)


def audit(placeholders) -> str:
    """One line per placeholder, for the artifact's own declaration block."""
    if not placeholders:
        return "No placeholders. Every band on this panel is a figure."
    lines = [f"{len(placeholders)} placeholder band(s), drawn in violet, "
             f"carrying no figure:"]
    for p in placeholders:
        lines.append(f"  - {p.label}: {p.why}")
    return "\n".join(lines)


class PlaceholderInShippingArtifact(AssertionError):
    pass


def forbid_in_shipping(placeholders, artifact: str):
    """Gate hook. A placeholder may be looked at; it may not ship.

    Called by the build for anything bound for publication. The check is on
    PRESENCE, not on colour, because the colour is a courtesy to the reader
    and this is a courtesy to everyone downstream of the reader.
    """
    if placeholders:
        keys = ", ".join(p.key for p in placeholders)
        raise PlaceholderInShippingArtifact(
            f"{artifact} carries {len(placeholders)} placeholder band(s) "
            f"({keys}). Placeholders are for looking at an unfinished panel, "
            f"not for publishing one. Acquire the figures or declare the "
            f"absence on the artifact.")
