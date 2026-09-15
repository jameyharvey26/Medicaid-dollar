# ledger.py — the conserved numbers, and what is known about each of them.
#
# ARCHITECTURE.md, "The seam to cut now". This module is the Ledger third of
# Ledger / View / Layout. It knows nothing about drawing. Nothing in here
# imports sankey, outflows or instances, and nothing in here has an opinion
# about what should be shown.
#
# Two design decisions carry most of the weight.
#
# 1. A figure is never a bare float. `Fig` carries value, source, vintage,
#    basis and status. An ABSENT figure has value None, not 0.0. That
#    distinction is what lets a lane collapse rather than render as a hairline
#    band with a $0.00 label, and it is what stops an absence from silently
#    conserving (S-071, ARCHITECTURE 3).
#
# 2. An allocation is a `Matrix` with margins and cells, and a cell may be
#    absent on its own. A matrix is therefore COMPLETE, PARTIAL or UNALLOCATED,
#    and the gate asserts something different about each. This is the structure
#    that lets research land one cell at a time: a DHCF service-category report,
#    an encounter extract, a NAIC exhibit or a plan's own submission each fill
#    the cells they cover and leave the rest absent, with no rebuild and no
#    decision about display taken in advance.

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Dict, List, Optional, Tuple

TOL = 0.02          # $ per $100. Matches check.py; tighter trips on rounding.


class LedgerError(AssertionError):
    pass


# ================================ status ==================================
# The status vocabulary is deliberately short. Every figure on every artifact
# in this project is one of these five things and there is no sixth.

MEASURED = "measured"    # read from a source that published this number
DERIVED  = "derived"     # arithmetic on other figures in this ledger
MODELLED = "modelled"    # our assumption, declared, with a stated method
CLIENT   = "client"      # supplied by the subject, neither measured nor
                         # modelled by us (ARCHITECTURE, axis 2)
ABSENT   = "absent"      # not published and not estimated. value is None.

SOURCED = (MEASURED, CLIENT)          # must name a source and a vintage
PRESENT = (MEASURED, DERIVED, MODELLED, CLIENT)


# ================================== Fig ===================================
@dataclass(frozen=True)
class Fig:
    """One number and everything known about it.

    `value` is $ per $100 of the ledger's own denominator unless `basis` says
    otherwise. `value is None` means ABSENT and nothing else may mean it.
    """
    value: Optional[float]
    source: str = ""
    vintage: str = ""
    basis: str = ""
    status: str = MEASURED
    note: str = ""
    parents: Tuple[str, ...] = ()      # for DERIVED, what it was computed from
    # Who looked at the source, and when. A source string says where a figure
    # is supposed to have come from. It does not say that anyone has opened it.
    # Thirteen DC figures carried sources inherited from a builder whose own
    # header said its vintages needed re-checking, and every one of them read
    # as held. Format: "YYYY-MM-DD initials". Empty means recorded but
    # unverified, which is a third state and not the same as either held or
    # missing.
    verified: str = ""
    # The value that was signed off. Verification attaches to a NUMBER, not to
    # a field: a figure signed at 28.27 and later edited to 30.00 is no longer
    # verified, and nothing else in the system would notice. Set by `sign()`,
    # never by hand.
    verified_value: Optional[float] = None

    # ---- construction ---------------------------------------------------
    @staticmethod
    def absent(why: str, note: str = "") -> "Fig":
        return Fig(None, source="", vintage="", basis="", status=ABSENT,
                   note=note or why)

    def sign(self, who: str) -> "Fig":
        """Record that someone opened the source and agreed with this value.

        `who` is "YYYY-MM-DD initials". Verification is valid for the vintage
        the figure declares, so a figure verified against MACStats FY2024 stays
        verified until the ledger is re-anchored to a later vintage. It does
        not expire on the calendar and it does not expire on a rebuild.
        """
        return replace(self, verified=who, verified_value=self.value)

    @property
    def lapsed(self) -> bool:
        """Verified, then changed. The signature no longer covers the value."""
        return bool(self.verified) and self.verified_value != self.value

    @staticmethod
    def derived(value: float, parents, basis: str = "", note: str = "") -> "Fig":
        return Fig(value, status=DERIVED, basis=basis, note=note,
                   parents=tuple(parents))

    # ---- predicates -----------------------------------------------------
    @property
    def is_absent(self) -> bool:
        return self.value is None

    @property
    def n(self) -> float:
        """Numeric value, or 0.0 for an absent figure.

        Used only where an absence has already been accounted for by the
        caller. Anything that sums figures without deciding what to do about
        absence should use `total()` instead, which refuses.
        """
        return 0.0 if self.value is None else self.value

    def __repr__(self):
        if self.is_absent:
            return f"Fig(ABSENT: {self.note})"
        return f"Fig({self.value:.4f} {self.status})"


def total(figs, allow_absent: bool = False) -> Tuple[Optional[float], List[Fig]]:
    """Sum figures, returning (value, absentees).

    With `allow_absent` false, any absent member makes the whole sum absent —
    which is the honest answer and the reason this returns None rather than
    quietly summing the rest. With it true, the present members are summed and
    the absentees are handed back so the caller can declare them.
    """
    figs = list(figs)
    gone = [f for f in figs if f.is_absent]
    if gone and not allow_absent:
        return None, gone
    return sum(f.n for f in figs), gone


def provenance_failures(named: Dict[str, Fig]) -> List[str]:
    """Every figure must be able to say where it came from (ARCHITECTURE 1)."""
    out = []
    for key, f in named.items():
        if f.status not in PRESENT + (ABSENT,):
            out.append(f"{key}: unknown status {f.status!r}")
        if f.status in SOURCED and not (f.source and f.vintage):
            out.append(f"{key}: status {f.status} with no source or vintage")
        if f.status == MODELLED and not f.note:
            out.append(f"{key}: modelled with no method stated")
        if f.status == ABSENT and f.value is not None:
            out.append(f"{key}: absent but carries a value")
        if f.status == ABSENT and f.verified:
            out.append(f"{key}: absent but marked verified")
        if f.lapsed:
            out.append(f"{key}: verified at {f.verified_value} but now "
                       f"{f.value}. Re-check or clear the signature.")
        if f.status != ABSENT and f.value is None:
            out.append(f"{key}: no value but not declared absent")
    return out


# ================================= Payer ==================================
@dataclass
class Payer:
    """One lane in the PAYER phase.

    Fee-for-service is a Payer with kind='ffs' and no retention, which is
    STATE_PLAYBOOK Rule A expressed in the data rather than in the renderer.
    A named plan is a Payer with `parent` set to the aggregate lane it rolls
    up to, so the same ledger answers both the aggregate view and the zoom.
    """
    key: str
    label: str
    kind: str                       # 'mco' | 'dual' | 'pace' | 'ffs'
    capitation: Fig
    care: Fig
    admin: Fig = field(default_factory=lambda: Fig.absent("no split"))
    margin: Fig = field(default_factory=lambda: Fig.absent("no split"))
    parent: Optional[str] = None    # aggregate lane this is a child of
    entity: str = ""                # licensed legal entity, for NAIC mapping
    note: str = ""

    @property
    def is_child(self) -> bool:
        return self.parent is not None


# ================================= Matrix =================================
COMPLETE    = "complete"       # every cell present; cells sum to both margins
PARTIAL     = "partial"        # some cells present; they sum to no more than
                               # their margins, the remainder is unallocated
UNALLOCATED = "unallocated"    # no cells; both margins known, interior absent


@dataclass
class Matrix:
    """An allocation with two margins and an interior that may be absent.

    Used for payer-by-service (the claims fan) and for group-by-service (the
    beneficiary pies). Both margins are figures in their own right and carry
    their own provenance; the interior is separate and usually weaker.
    """
    name: str
    rows: List[str]
    cols: List[str]
    row_margin: Dict[str, Fig]
    col_margin: Dict[str, Fig]
    cell: Dict[Tuple[str, str], Fig] = field(default_factory=dict)
    note: str = ""

    def get(self, r: str, c: str) -> Fig:
        return self.cell.get((r, c), Fig.absent("cell not filled"))

    def row_cells(self, r: str) -> List[Fig]:
        return [self.get(r, c) for c in self.cols]

    def col_cells(self, c: str) -> List[Fig]:
        return [self.get(r, c) for r in self.rows]

    def row_state(self, r: str) -> str:
        present = [f for f in self.row_cells(r) if not f.is_absent]
        if not present:
            return UNALLOCATED
        return COMPLETE if len(present) == len(self.cols) else PARTIAL

    @property
    def state(self) -> str:
        states = {self.row_state(r) for r in self.rows}
        if states == {COMPLETE}:
            return COMPLETE
        if states == {UNALLOCATED}:
            return UNALLOCATED
        return PARTIAL

    def unallocated_rows(self) -> List[str]:
        return [r for r in self.rows if self.row_state(r) == UNALLOCATED]


# ================================= Peel ===================================
@dataclass
class Peel:
    """Money leaving the flow, charged to a phase.

    `charged` is the phase the subtraction is booked against. `reach` is how
    far down the lifecycle the money would have got had it not left, which is
    a separate claim and is what the terminal answers (S-085, S-086).
    """
    key: str
    label: str
    amount: Fig
    charged: str                    # FEDERAL | STATE_AGENCY | DISBURSE | PAYER | CLAIMS
    reach: str = ""
    kind: str = "admin"             # admin | return | fraud | hr1


PHASES = ("FEDERAL", "STATE_GOVERNMENT", "STATE_AGENCY", "DISBURSE",
          "PAYER", "CLAIMS", "PROVIDERS", "BENEFICIARIES")

# Peels charged at or before DISBURSE come out before the payer lanes are
# struck. Peels charged later come out of a lane that has already been drawn.
PRE_DISBURSE = ("FEDERAL", "STATE_GOVERNMENT", "STATE_AGENCY", "DISBURSE")


# ================================ Ledger ==================================
@dataclass
class Ledger:
    geography: str
    year: str
    scenario: str                   # 'as_is' | 'to_be'
    scale: Fig                      # $M per $1 of the normalized hundred
    sources: Dict[str, Fig]         # 'federal', 'state'
    peels: List[Peel]
    payers: List[Payer]
    nodes: List[str]                # provider node keys, in reading order
    claims: Matrix                  # payer x provider node
    beneficiaries: Optional[Matrix] = None      # group x provider node
    declarations: List[str] = field(default_factory=list)   # prose, for the artifact
    # Machine-checkable declarations. The gate matches on these keys rather than
    # grepping the prose, because a substring match makes the gate depend on how
    # a sentence happens to be worded, which is how a detector goes quietly
    # blind. Prose is for the reader; keys are for the build.
    declared: List[str] = field(default_factory=list)
    note: str = ""

    # ---- derived reads --------------------------------------------------
    def payer(self, key: str) -> Payer:
        for p in self.payers:
            if p.key == key:
                return p
        raise KeyError(key)

    def lanes(self) -> List[Payer]:
        """The aggregate lanes: payers that are not children of another."""
        return [p for p in self.payers if not p.is_child]

    def children(self, key: str) -> List[Payer]:
        return [p for p in self.payers if p.parent == key]

    def peels_at(self, *phases) -> List[Peel]:
        return [x for x in self.peels if x.charged in phases]

    def disbursed(self) -> Tuple[Optional[float], List[Fig]]:
        pre = [x.amount for x in self.peels_at(*PRE_DISBURSE)]
        s, gone = total(pre, allow_absent=False)
        return (None if s is None else 100.0 - s), gone

    def figures(self) -> Dict[str, Fig]:
        """Every figure in the ledger, keyed, for the provenance sweep and
        for endnote generation. One place, so nothing is exempt by being
        forgotten."""
        out: Dict[str, Fig] = {"scale": self.scale}
        for k, f in self.sources.items():
            out[f"source.{k}"] = f
        for x in self.peels:
            out[f"peel.{x.key}"] = x.amount
        for p in self.payers:
            out[f"payer.{p.key}.capitation"] = p.capitation
            out[f"payer.{p.key}.care"] = p.care
            out[f"payer.{p.key}.admin"] = p.admin
            out[f"payer.{p.key}.margin"] = p.margin
        for m in [self.claims] + ([self.beneficiaries] if self.beneficiaries else []):
            for r, f in m.row_margin.items():
                out[f"{m.name}.row.{r}"] = f
            for c, f in m.col_margin.items():
                out[f"{m.name}.col.{c}"] = f
            for (r, c), f in m.cell.items():
                out[f"{m.name}.cell.{r}.{c}"] = f
        return out


# ================================= check ==================================
def _near(a, b, tol=TOL):
    return abs(a - b) <= tol


def check(L: Ledger) -> List[str]:
    """Return a list of failures. Empty means the ledger conserves.

    Replaces the eyeball test at STYLE_GUIDE 3.3 with an assertion, and adds
    the thing the old gate could not express: whether an allocation is
    complete, partial or unallocated, and what conservation means in each case.
    """
    f: List[str] = []

    def eq(name, a, b):
        if a is None or b is None:
            f.append(f"{name}: cannot be checked, a term is absent")
        elif not _near(a, b):
            f.append(f"{name}: {a:.4f} != {b:.4f}  (off by {a-b:+.4f})")

    # ---- 1. provenance. A figure without it fails the build. -------------
    f += provenance_failures(L.figures())

    # ---- 2. sources ------------------------------------------------------
    s, gone = total(L.sources.values())
    eq("sources sum to 100", s, 100.0)

    # ---- 3. lanes sum to what was disbursed ------------------------------
    disb, gone = L.disbursed()
    if gone:
        f.append("disbursed cannot be struck: absent peels "
                 + ", ".join(g.note for g in gone))
    lane_caps, lane_gone = total([p.capitation for p in L.lanes()])
    if lane_gone:
        f.append("payer lanes cannot be summed: "
                 + ", ".join(g.note for g in lane_gone))
    eq("payer lanes sum to disbursed", lane_caps, disb)

    # ---- 4. each payer splits into care and retention --------------------
    for p in L.payers:
        if p.care.is_absent or p.capitation.is_absent:
            f.append(f"payer {p.key}: capitation or care absent, lane cannot be drawn")
            continue
        ret = p.capitation.n - p.care.n
        if p.admin.is_absent and p.margin.is_absent:
            if p.kind != "ffs" and ret > TOL:
                # legitimate: retention is measured, its split is not. This is
                # declared, not a failure, but it must be declared.
                if p.key not in L.declared:
                    f.append(f"payer {p.key}: retention {ret:.2f} is undivided "
                             f"and the split is not declared")
        else:
            parts, _ = total([x for x in (p.admin, p.margin) if not x.is_absent],
                             allow_absent=True)
            eq(f"payer {p.key}: admin + margin == retention", parts, ret)

    # ---- 5. children roll up to their parent -----------------------------
    for parent in L.lanes():
        kids = L.children(parent.key)
        if not kids:
            continue
        s, gone = total([k.capitation for k in kids])
        if gone:
            f.append(f"lane {parent.key}: child capitation absent, cannot roll up")
        else:
            eq(f"lane {parent.key}: children sum to the lane", s, parent.capitation.n)

    # ---- 6. the claims matrix -------------------------------------------
    M = L.claims
    for r in M.rows:
        margin = M.row_margin.get(r)
        if margin is None or margin.is_absent:
            f.append(f"claims matrix: row {r} has no margin")
            continue
        st = M.row_state(r)
        got, _ = total([x for x in M.row_cells(r) if not x.is_absent], allow_absent=True)
        if st == COMPLETE:
            eq(f"claims row {r} sums to its margin", got, margin.n)
        elif st == PARTIAL and got - margin.n > TOL:
            f.append(f"claims row {r}: filled cells {got:.4f} exceed the "
                     f"margin {margin.n:.4f}")
    for c in M.cols:
        margin = M.col_margin.get(c)
        if margin is None or margin.is_absent:
            continue
        cells = [x for x in M.col_cells(c) if not x.is_absent]
        if len(cells) == len(M.rows):
            got, _ = total(cells)
            eq(f"claims column {c} sums to its margin", got, margin.n)

    # a node that exists must be a column, and a column must be a node
    missing = set(L.nodes) - set(M.cols)
    extra = set(M.cols) - set(L.nodes)
    if missing:
        f.append(f"claims matrix is missing provider nodes: {sorted(missing)}")
    if extra:
        f.append(f"claims matrix has columns that are not provider nodes: {sorted(extra)}")
    # and a lane that pays claims must be a row
    paying = {p.key for p in L.lanes()}
    if set(M.rows) != paying:
        f.append(f"claims matrix rows {sorted(M.rows)} do not match the "
                 f"paying lanes {sorted(paying)}")

    # ---- 7. claims and the tracker --------------------------------------
    care, care_gone = total([p.care for p in L.lanes()])
    if care_gone:
        f.append("claims total cannot be struck: absent care figures")
    claims_peels, cp_gone = total([x.amount for x in L.peels_at("CLAIMS")],
                                  allow_absent=True)
    # The invariant that survives a partly filled interior: the ROW MARGINS
    # sum to claims however much of the matrix is allocated. Asserting the
    # column totals instead would make conservation depend on how much
    # research has landed, which would mean a ledger stopped balancing because
    # we learned less than we hoped. Per-column sums are checked at section 6
    # wherever a column is fully filled.
    row_margins, rm_gone = total([M.row_margin[r] for r in M.rows
                                  if r in M.row_margin], allow_absent=False)
    if rm_gone:
        f.append("claims cannot be summed: a row margin is absent")
    elif care is not None:
        eq("claims matrix row margins sum to care less claims-side peels",
           row_margins, care - claims_peels)

    # ---- 8. the beneficiary matrix, where present ------------------------
    if L.beneficiaries:
        B = L.beneficiaries
        sr, gr = total(list(B.row_margin.values()), allow_absent=False)
        sc, gc = total(list(B.col_margin.values()), allow_absent=False)
        if gr or gc:
            f.append("beneficiary matrix: a margin is absent")
        else:
            eq("beneficiary margins agree", sr, sc)
        for r in B.rows:
            if B.row_state(r) == COMPLETE:
                got, _ = total(B.row_cells(r))
                eq(f"beneficiary row {r} sums to its margin", got, B.row_margin[r].n)

    # ---- 9. absence is declared, never inferred --------------------------
    for key, fig in L.figures().items():
        if fig.is_absent and not fig.note:
            f.append(f"{key}: absent with nothing said about why")
    for r in M.unallocated_rows():
        if f"claims:{r}" not in L.declared:
            f.append(f"claims row {r} is unallocated and not declared")

    return f


def gate(L: Ledger, label: str = "") -> bool:
    fails = check(L)
    tag = label or f"{L.geography} {L.year} {L.scenario}"
    if fails:
        raise LedgerError(f"{tag} does not conserve:\n  " + "\n  ".join(fails))
    return True


# ============================== endnotes ==================================
def endnotes(L: Ledger) -> List[str]:
    """Generate the sourcing register from the ledger.

    ENDNOTES.md stops being a document someone maintains and becomes a
    rendering of the data, the same way the diagram is (ARCHITECTURE 1).
    Grouped by status so the limits read as a block rather than scattered.
    """
    figs = L.figures()
    out = []
    for st, head in ((MEASURED, "Measured"), (CLIENT, "Supplied by the subject"),
                     (MODELLED, "Modelled"), (ABSENT, "Not published")):
        block = {k: v for k, v in figs.items() if v.status == st}
        if not block:
            continue
        out.append(f"## {head}")
        for k, v in sorted(block.items()):
            if st == ABSENT:
                out.append(f"- {k}: absent. {v.note}")
            else:
                bits = [b for b in (v.source, v.vintage, v.basis) if b]
                seen = (f" Verified {v.verified}." if v.verified
                        else " NOT VERIFIED.")
                tail = f" — {v.note}" if v.note else ""
                out.append(f"- {k} = {v.value:.2f}. " + "; ".join(bits) + "."
                           + seen + tail)
    return out
