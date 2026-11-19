# signatures_dc.py — who signed what on the District panels, and at which
# value and which source.
#
# The District's own register. See `signing.py` for why each jurisdiction has
# one rather than sharing national's: the District reuses national key strings
# exactly — `scale`, `peel.admin`, `payer.ffs.capitation` and more — so one
# shared dict would let a District signature silently lapse a national one.
#
# EMPTY ON PURPOSE, 19 November 2026. The mechanism exists; the signatures do
# not. `verified` is "YYYY-MM-DD initials" and the initials belong to a person
# who opened the source. Claude drafted the candidate lines and checked their
# arithmetic; nobody has opened MACStats Exhibit 16 or Exhibit 17 for this
# panel yet.
#
# S-093, JW 16 September: no signature without a stacked before-and-after of
# every panel the change touches, rendered full width, with the changed
# figures named above it. `reference_renders/diffs/` holds them. The register
# is the record that this happened.
#
# WHAT A LINE MEANS. `Agreed(value, provenance)` says a person opened the
# source and agreed with BOTH: the number, and where it says it came from.
# The provenance is a fingerprint of source, vintage and basis — the three
# fields the endnote register prints as the figure's research footnote. If
# either moves, the figure is not re-signed: the build reports it LAPSED and
# fails. Correcting a figure costs a deliberate line here, which is the point.
#
# TO PRODUCE CANDIDATE LINES:
#
#     python3 signing.py dc --unsigned
#
# That prints the value, the fingerprint and the head of the source for every
# signable District figure with no entry yet. It writes nothing.

from signing import Agreed  # noqa: F401  (register lines use it)

REVIEW = "2026-11-19 JW"

# Deliberately unsigned. A figure goes here when its own endnote says no
# primary source exists, so signing it would assert that someone opened a
# document the register says does not exist — the national panel's two EN-43
# earnings margins are the precedent.
#
# The District has no such case today. The four figures that looked like
# candidates on 18 November — the folded managed-care, dual and PACE lanes —
# were a different problem: they were marked MEASURED and are not
# measurements, and D-151 reclassified them rather than declining to sign
# them. UNSIGNED means a person deliberately declined; those had not reached
# the point where anyone could.
UNSIGNED = frozenset()

# WHERE TO START, from DC_SIGNOFF_LIST.md Tier 1, in the order a signature
# matters most. These are the readings everything else on the two District
# panels divides through or derives from:
#
#   anchor.ex16.total / .federal / .state and scale
#       The District hundred. MACStats Exhibit 16, FY2024, DC row. One source,
#       one reading, four numbers, and every per-$100 figure on both panels
#       divides through it.
#   anchor.ex17.ffs_gross / .managed_care / .collections
#       The Exhibit 17 reconciliation. Signing these is agreeing that the
#       benefit categories sum to Exhibit 16's total to the dollar, which the
#       ledger asserts and which now closes in code.
#   claims.cell.ffs.*
#       The five service nodes, mapped from Exhibit 17's nine published
#       columns. The MAPPING is a judgement and needs agreeing, not just the
#       dollars; it is written out in basis_dc.py.
#   peel.admin, peel.medicare
#       State program administration and Medicare premiums, both Exhibit 16/17
#       readings.
#   anchor.budget.dedtax
#       The provider-tax lane's base year, from DHCF's own budget chapter.
SIGNED = {}
