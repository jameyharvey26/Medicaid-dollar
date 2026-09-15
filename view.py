# view.py — the framing. Knows nothing about sourcing.
#
# ARCHITECTURE.md: `render(Ledger, View) -> svg`. A View says what to show and
# how to frame it. It never holds a number, and a change to a View can never
# change what conserves.
#
# The expand flag lives here rather than in the Ledger because expanding a
# payer lane into its named plans does not re-root the diagram and does not
# change what $100 means. It shows detail the ledger already holds. Re-rooting
# — a plan president's own hundred dollars — is the other axis and is not this.

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ledger import Ledger, UNALLOCATED


@dataclass
class View:
    root: str = "state_agency"          # what the hundred dollars is of
    normalise: float = 100.0
    expand: List[str] = field(default_factory=list)   # payer lane keys to open
    collapse: List[str] = field(default_factory=list) # phases to fold shut
    show_beneficiaries: bool = True
    show_claims_fan: bool = True        # ribbons payer -> provider node
    labels: Dict[str, str] = field(default_factory=dict)
    kicker: str = ""
    title: str = ""
    strap: str = ""
    # ---- presentation payload -------------------------------------------
    # These are framing, not numbers. They were fields on Instance, where they
    # sat beside the ledger values and made it impossible to tell which half of
    # the config was a claim about the world and which half was a decision
    # about the page. Amounts inside `steps` and `subs_spec` are keys or are
    # supplied by the composer from the Ledger, never typed in here.
    cp0_label: List[str] = field(default_factory=lambda: ["$100 Medicaid", "Dollars"])
    centre: tuple = ("100 Dollars of", "Medicaid Spending")
    disp: Dict[str, str] = field(default_factory=dict)
    step_x: Dict[str, int] = field(default_factory=dict)   # peel key -> trunk x
    subs_spec: List[tuple] = field(default_factory=list)
    hr1_term: Dict[str, tuple] = field(default_factory=dict)

    # ---- what the layout is actually asked to draw ----------------------
    def payer_rows(self, L: Ledger):
        """The lanes as this view wants them: expanded into named plans where
        asked, aggregate otherwise."""
        rows = []
        for lane in L.lanes():
            kids = L.children(lane.key)
            if lane.key in self.expand and kids:
                rows.extend(kids)
            else:
                rows.append(lane)
        return rows

    def fan_state(self, L: Ledger, payer_key: str) -> str:
        """Whether a fan can be drawn out of this payer, and if not, why not.

        The View asks; the Ledger answers. A view never fills a cell, so a
        fan that cannot be drawn is reported rather than invented.
        """
        if not self.show_claims_fan:
            return "suppressed"
        if payer_key in L.claims.rows:
            return L.claims.row_state(payer_key)
        parent = L.payer(payer_key).parent
        if parent and parent in L.claims.rows:
            # the aggregate lane has an allocation but this child does not
            return UNALLOCATED
        return UNALLOCATED

    def undrawable(self, L: Ledger) -> List[str]:
        """Every element this view asks for that the ledger cannot support.

        The layout calls this before drawing and the caller decides what to do
        about it. Deciding here would be a display decision taken inside the
        framing layer, which is the thing the seam exists to prevent.
        """
        out = []
        for p in self.payer_rows(L):
            if self.fan_state(L, p.key) == UNALLOCATED:
                out.append(f"claims fan out of {p.key}: no allocation in the ledger")
        if self.show_beneficiaries and L.beneficiaries is None:
            out.append("beneficiary shares: no matrix in the ledger")
        for p in self.payer_rows(L):
            if p.admin.is_absent and p.margin.is_absent and p.kind != "ffs":
                out.append(f"retention split for {p.key}: not in the ledger")
        return out
