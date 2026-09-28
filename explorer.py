"""explorer.py — Ledger -> the explorer's data, with provenance attached.

D-105. The predecessor (`medicaid_dollar_explorer.html`, Brent, August) carried
its numbers as a JSON blob pasted into the page. Two things followed from that
and both were invisible.

The national half was struck on the OLD hundred: $957.4B, administration $5.07,
care delivered $86.27. D-70 moved the strike point to the state agency and put
Vaccines for Children outside it, and D-83 moved the lane derivation into
`basis_national.py`. Nothing told the page. Its national figures had been wrong
for two decision cycles and it went on serving them with confidence.

The DC half agreed with `ledger_dc_2024.py` to fifteen significant figures, so
a machine had written it — but a machine writing a number ONCE is not a live
connection, and DC had meanwhile withdrawn its service allocation. The page
went on printing a DC service mix (long-term care $35.94, physicians $21.63)
that `coverage.py dc` now reports as MISS on every node. A withdrawn figure
does not disappear from a artifact that holds its own copy.

So this module does not produce numbers for anyone to copy. It produces the
data the page reads at build time, and `explorerproof.py` fails the build if a
numeral appears in the template. S-105, applied to the web artifact.

WHAT IS DIFFERENT FROM THE PAPER. The paper prints a figure; the explorer must
also be able to say what KIND of figure it is, because a reader who can hover
every number is entitled to know which ones are measured and which are ours.
Every value below is serialized as an object, never a bare float, and the key
into `Ledger.figures()` travels with it so `ledger.verification` can be walked
for the derived ones. A figure with no value serializes as a declared absence
with its reason, and the page draws a gap rather than a zero.
"""
from __future__ import annotations

import ledger as LD
from ledger import ABSENT, DERIVED, Fig, Ledger, Matrix

# The four states a reader needs to tell apart, and the words the page uses.
# Deliberately not the five-word ledger vocabulary: a reader does not need
# MEASURED vs CLIENT, they need "did somebody publish this, or did we make it".
STATE_WORD = {
    "held": "verified",
    "stale": "recorded, unverified",
    "model": "modelled",
    "lapsed": "signature lapsed",
    "miss": "not acquired",
}


def _state(f: Fig, key: str = "", named=None):
    """The page's one-word grade for a figure, and the reason behind it.

    Same grading `coverage.py` applies, reached through the same predicates so
    the register on the page and the register on the command line cannot
    disagree. A DERIVED figure inherits: arithmetic does not add confidence to
    its inputs.
    """
    if f is None:
        return "miss", ""
    if f.lapsed:
        return "lapsed", f"signed at {f.verified_value}, now {f.value}"
    if f.status == ABSENT:
        return "miss", f.note
    if f.status in LD.SOURCED:
        src = f"{f.source} {f.vintage}".strip()
        return ("held", f"{src}  [{f.verified}]") if f.verified else ("stale", src)
    if f.status == DERIVED:
        chain = "derived from " + ", ".join(f.parents or ("nothing named",))
        if named is None or not key:
            return "stale", chain
        good, why = LD.verification(key, named)
        return ("held", f"{chain}  [{why}]") if good else ("stale", f"{chain} — {why}")
    return ("model" if f.verified else "stale"), f.note


def fig(f: Fig, key: str = "", named=None) -> dict:
    """One figure, with everything a tooltip needs and nothing it does not."""
    if f is None:
        return {"v": None, "state": "miss", "why": "no figure in the ledger",
                "status": ABSENT, "key": key}
    st, why = _state(f, key, named)
    # The grade stays what coverage.py would give it, so the register on the
    # page and the register on the command line tally the same. Only the word
    # differs: an unsigned MODELLED figure is not "recorded" anywhere, it is
    # ours and unsigned, and calling it recorded would credit it to a source.
    word = ("modelled, unsigned" if st == "stale" and f.status == LD.MODELLED
            else STATE_WORD[st])
    out = {
        "v": None if f.is_absent else round(f.value, 4),
        "state": st,
        "word": word,
        "why": why,
        "status": f.status,
        "key": key,
    }
    # Only carried when present, so the payload does not fill with empty
    # strings — this JSON ships inside the page and every byte is downloaded.
    for name, val in (("source", f.source), ("vintage", f.vintage),
                      ("note", f.note), ("verified", f.verified)):
        if val:
            out[name] = val
    if f.parents:
        out["parents"] = list(f.parents)
    return out


# ---------------------------------------------------------------------------
def _matrix(M: Matrix, named, prefix: str) -> dict:
    """An allocation, with its interior state declared row by row.

    `row_state` is the thing the predecessor had no way to express and the
    reason it published a DC service mix that had been withdrawn. An
    UNALLOCATED row is not a row of zeros.
    """
    return {
        "name": M.name,
        "rows": list(M.rows),
        "cols": list(M.cols),
        "state": M.state,
        "row_state": {r: M.row_state(r) for r in M.rows},
        "row_margin": {r: fig(M.row_margin.get(r), f"{prefix}.row.{r}", named)
                       for r in M.rows},
        "col_margin": {c: fig(M.col_margin.get(c), f"{prefix}.col.{c}", named)
                       for c in M.cols},
        "cell": {f"{r}|{c}": fig(M.get(r, c), f"{prefix}.cell.{r}.{c}", named)
                 for r in M.rows for c in M.cols
                 if not M.get(r, c).is_absent},
        "note": M.note,
    }


def _payer(p, L: Ledger, named) -> dict:
    k = f"payer.{p.key}"
    return {
        "key": p.key, "label": p.label, "kind": p.kind,
        "entity": p.entity, "note": p.note,
        "capitation": fig(p.capitation, f"{k}.capitation", named),
        "care": fig(p.care, f"{k}.care", named),
        "admin": fig(p.admin, f"{k}.admin", named),
        "margin": fig(p.margin, f"{k}.margin", named),
        "children": [c.key for c in L.children(p.key)],
    }


def _peel(x, named) -> dict:
    return {
        "key": x.key, "label": x.label,
        "charged": x.charged, "reach": x.reach, "kind": x.kind,
        "outside": bool(x.outside),
        "amount": fig(x.amount, f"peel.{x.key}", named),
    }


def _totals(L: Ledger, named) -> dict:
    """The panel's headline figures, summed HERE, at full precision.

    The page must not add figures up. Serialization rounds to four places, and
    the page's first draft summed the three rounded lane margins to reach the
    claims total: 35.9234 + 9.7597 + 41.3919 = 87.0750, printed as $87.08,
    against the ledger's own 87.074936, which prints as $87.07. A one-cent
    disagreement between the explorer and the paper, produced by nothing but
    where the addition happened.

    This is the published-totals principle from STATE_PLAYBOOK stated the
    other way round: a total is a figure in its own right and is derived from
    the unrounded values, not recomputed downstream from the rounded ones.
    """
    care = LD.total([f for f in L.claims.row_margin.values()],
                    allow_absent=True)[0]
    inside = [p.amount for p in L.peels if not p.outside]
    peeled = LD.total(inside, allow_absent=True)[0]
    return {
        "claims": fig(Fig.derived(care, [f"claims.row.{r}" for r in L.claims.rows],
                                  note="what reaches a paid claim: the payer "
                                       "lanes' care, summed unrounded"), "", named),
        "peeled": fig(Fig.derived(peeled, [f"peel.{p.key}" for p in L.peels
                                           if not p.outside],
                                  note="everything that leaves the hundred "
                                       "between the state agency and a provider"),
                      "", named),
        "hundred": fig(Fig(100.0, status=DERIVED,
                           note="the hundred, struck at the state agency (D-70). "
                                "True by construction, not by measurement.",
                           parents=("scale",))),
    }


def panel(L: Ledger, code: str, name: str, short: str, *,
          draft: str = "", strap: str = "", disp=None) -> dict:
    """One jurisdiction-year, whole, as the page will read it.

    `draft` is not decoration. A non-empty string here is what makes the page
    stamp the panel, every figure in it, every tooltip, and anything the reader
    exports. A panel is draft or it is not, declared once, at the top.
    """
    named = L.figures()
    return {
        "code": code, "name": name, "short": short,
        "geography": L.geography, "year": L.year, "scenario": L.scenario,
        "draft": draft,
        "strap": strap,
        "note": L.note,
        "scale": fig(L.scale, "scale", named),
        "sources": {k: fig(f, f"source.{k}", named)
                    for k, f in L.sources.items()},
        "peels": [_peel(x, named) for x in L.peels],
        "payers": [_payer(p, L, named) for p in L.payers],
        "lanes": [p.key for p in L.lanes()],
        "nodes": list(L.nodes),
        # The View's display names, so the page calls a node what the paper
        # calls it. "Other" is "Wrap around services" on the national panel
        # and the explorer must not be the one artifact that says "Other".
        "disp": dict(disp or {}),
        "totals": _totals(L, named),
        "claims": _matrix(L.claims, named, "claims"),
        "beneficiaries": (_matrix(L.beneficiaries, named, "beneficiaries")
                          if L.beneficiaries else None),
        "anchors": {k: fig(f, f"anchor.{k}", named)
                    for k, f in L.anchors.items()},
        "currency": currency(L),
        "declarations": list(L.declarations),
    }


# coverage.py's vocabulary onto the page's. Written out rather than lowercased,
# because MODELLED and MISSING do not lowercase onto `model` and `miss` and a
# silent mismatch here grades every missing figure as present. It did: the DC
# register first reported 0 of 41 missing against coverage.py's 26.
_REGISTER_WORD = {"HELD": "held", "STALE": "stale", "MODELLED": "model",
                  "MISSING": "miss", "LAPSED": "lapsed"}


import re as _re

# What a trace key means to a reader, per dimension. The keys come from the
# SVG, which got them from `sankey.trace` blocks, which got them from the
# ledger. Nothing here invents a key; this is only the word for one.
TRACE_LABEL = {
    "federal": "Federal money", "state": "Non-federal money",
    "mco": "MCO capitation", "dual": "Dual MCO capitation",
    "ffs": "Fee-for-service",
}
# JW, 28 September. The payer lanes keep their controls and lose their name:
# the diagram's own column headers already say DISBURSEMENTS and PAYER, and a
# third word for the same phase is one word too many. An empty string here
# means the page draws the swatches with no heading over them.
KIND_LABEL = {"source": "Where it comes from", "payer": "",
              "provision": "Provisions"}


# D-110. What a number-line widget selects.
#
# The grey marks on the tracker are TOTALS of things the flow draws separately:
# "MCO Admin" is one mark and three ribbons. Clicking the mark should light all
# three, which needs the membership somewhere.
#
# The HR-1 groups already declare theirs — `views` names them in a `PeelSum`,
# and those keys are read below rather than restated. The overhead groups name
# their members only inside a prose label ("plan administration + earnings"),
# so the set is written here, once, and nowhere else. If a fourth thing ever
# joins plan retention, this is the line that has to change, and
# `plate()` fails the build if it names a ribbon the drawing does not have.
OVERHEAD_GROUPS = {
    "Vaccines": ("vfc",),
    "State Admin": ("admin", "oversight", "medicare"),
    # On a panel where the split into administration and margin is published,
    # the three exits light. Where it is not — DC — only the undifferentiated
    # retention bands do, and the mark still totals what is drawn.
    "MCO Admin": ("mco_adm", "dual_adm", "earnings",
                  "retention_mco", "retention_dual"),
    "Fraud": ("fraud",),
}

# An anchor is a running total, so it lights everything that has happened up to
# it. Cumulative, in tracker order, built below rather than listed.
ANCHOR_ORDER = ("$100 Medicaid", "Actuals", "Projected under",
                "Budgeted to Medicaid", "Funding Disbursed", "Claims Paid",
                "Health Services")


def _groups(svg: str, L: Ledger, V=None) -> dict:
    """trace key -> the keys it lights, for every group and anchor drawn."""
    import re
    have = {v.replace("&amp;", "&")
            for v in _re.findall(r'data-trace="([^"]*)"', svg)}
    for v in _re.findall(r'data-also="([^"]*)"', svg):
        have.update(x.replace("&amp;", "&") for x in v.split("|"))
    out = {}

    for g, members in OVERHEAD_GROUPS.items():
        if g in have:
            # A group must light SOMETHING. It need not light everything: a
            # jurisdiction can legitimately lack a member — DC has no federal
            # oversight peel — and the mark on its number line is still the
            # total of what it does have. What cannot stand is a widget that
            # lights nothing at all, which is a control that lies about what
            # it totals and looks broken to the reader.
            present = [m for m in members if m in have]
            if not present:
                raise LD.LedgerError(
                    f"the number line draws the group {g!r} and this panel "
                    f"draws none of {list(members)}. A widget that lights "
                    f"nothing is a widget that lies about what it totals.")
            out[g] = present

    # HR-1 groups: the View already names its members.
    if V is not None:
        from view import PeelSum
        for lab, amt, cls, col, short in V.subs_spec:
            if isinstance(amt, PeelSum) and short in have:
                out[short] = [k for k in amt.keys if k in have]

    # An anchor lights everything that has happened up to it, which means every
    # key whose own phase is at or before the anchor's. The phase comes from
    # the ledger — a peel knows where it is charged — not from a list here.
    import outflows as OF
    order = list(OF.COLS)
    idx = {c: i for i, c in enumerate(order)}
    phase = {}
    for p in L.peels:
        phase[p.key] = idx.get(p.charged, 0)
    for k in ("federal", "state"):
        phase[k] = 0
    for k in ("mco", "dual", "ffs"):
        phase[k] = idx["DISBURSE"]
    for k in ("mco_adm", "dual_adm", "earnings"):
        phase[k] = idx["PAYER"]
    for c in L.nodes:
        phase[c] = idx["PROVIDERS"]

    at = {"$100 Medicaid": "STATE_GOVT", "Actuals": "STATE_GOVT",
          "Projected under": "STATE_GOVT", "Budgeted to Medicaid": "STATE_AGENCY",
          "Funding Disbursed": "DISBURSE", "Claims Paid": "CLAIMS",
          "Health Services": "BENEFICIARY"}
    for a in ANCHOR_ORDER:
        if a not in have:
            continue
        cut = idx[at[a]]
        out[a] = sorted(k for k, ph in phase.items()
                        if ph <= cut and k in have)
    return out


def plate(svg_path: str, L: Ledger, prov: dict = None, V=None) -> dict:
    """The real diagram, and the handles a reader can pull on.

    D-106. This is the predecessor's best idea, restored. Brent's page gave
    every band in the SVG the name of what flowed through it, so hovering one
    ribbon lit that payer's money across the whole lifecycle. The first
    rebuild dropped the diagram for bar rulers, which was a straight loss: the
    rulers are more legible per row and say nothing about where anything goes.

    What is different now is that the handles are generated. `sankey.trace`
    writes them at render time from the ledger's own keys, so the legend below
    is read out of the SVG rather than maintained beside it, and a band whose
    key is not a figure in this ledger fails here rather than becoming a dead
    swatch.

    The plate keeps its `baseline` and `overlay-hr1` groups, so the page can
    lift the law off the diagram and put it back — which the paper cannot do
    on a printed page and is the clearest thing the web adds.
    """
    svg = open(svg_path).read()
    named = L.figures()
    # The labels sankey.py drew, so `explorerproof.py` can tell a figure the
    # renderer computed off this ledger from one the page invented. Same
    # device as the deck's fact cards: a named third source, not a blanket
    # exemption. The SVG itself is gated by renderproof.py and check().
    drawn = sorted(set(_re.findall(r"\$(\d[\d,]*\.\d\d)", svg)))
    figs = {}
    for p in L.payers:
        figs[p.key] = fig(p.capitation, f"payer.{p.key}.capitation", named)
    for k, f in L.sources.items():
        figs[k] = fig(f, f"source.{k}", named)
    for p in L.peels:
        figs[p.key] = fig(p.amount, f"peel.{p.key}", named)

    # The whole element, then its attributes. Matching an ordered sequence of
    # them assumes `sankey.py` emits fill before the handles, which it happens
    # to do and is not obliged to keep doing.
    seen, legend = set(), []
    for m in _re.finditer(r'<(?:path|rect)\b[^>]*\bdata-trace=[^>]*>', svg):
        el = m.group(0)
        key = _re.search(r'data-trace="([^"]*)"', el).group(1)
        kind = _re.search(r'data-kind="([^"]*)"', el).group(1)
        cm = _re.search(r'\bfill="([^"]*)"', el)
        color = cm.group(1) if cm else "#888888"
        key = key.replace("&amp;", "&")
        if (key, kind) in seen:
            continue
        seen.add((key, kind))
        if kind in ("group", "anchor", "node", "retention", "peel"):
            # Selectable, but not a legend swatch: these are reached by
            # clicking the drawing itself, which is where they live.
            continue
        f = figs.get(key)
        if kind == "provision" and prov:
            f = next((l["amount"] for l in prov["lanes"] if l["key"] == key), None)
        if f is None:
            raise LD.LedgerError(
                f"the diagram traces {key!r} as a {kind} and this ledger has "
                f"no such figure. A band a reader can pull on must resolve to "
                f"something the ledger can explain.")
        legend.append({"key": key, "kind": kind, "color": color,
                       "label": TRACE_LABEL.get(key, key), "fig": f})

    order = {"source": 0, "payer": 1, "provision": 2}
    legend.sort(key=lambda r: (order.get(r["kind"], 9), r["label"]))
    return {"svg": svg, "legend": legend, "drawn": drawn,
            "groups": _groups(svg, L, V),
            "kinds": [{"kind": k, "label": KIND_LABEL[k]}
                      for k in ("source", "payer", "provision")
                      if any(r["kind"] == k for r in legend)]}


def currency(L: Ledger) -> list:
    """The register, generated. Same rows `coverage.py` prints."""
    import coverage
    out = []
    for ph, it, st, why in coverage.rows(L):
        key = st.strip().upper()
        if key not in _REGISTER_WORD:
            raise LD.LedgerError(f"coverage.py grades {it!r} as {st!r}, which "
                                 f"the explorer has no word for")
        out.append({"phase": ph, "item": it, "state": _REGISTER_WORD[key],
                    "word": STATE_WORD[_REGISTER_WORD[key]], "why": why})
    return out


def _inc(v, key: str, what: str) -> dict:
    """An incidence figure. MODELLED, and it says so.

    None of these is published by anybody. They are `incidence.py` putting the
    ledger's provision dollars through the allocation rules D-102 settled, and
    a reader hovering one is entitled to be told that rather than being shown
    a number with the same weight as a CMS-64 line.
    """
    return fig(Fig(round(v, 4), status=LD.MODELLED,
                   note=what + ". incidence.py: provision to population by the "
                               "statute where it names one, proportional to "
                               "FY2024 claims where it does not; population to "
                               "service by that population's own measured "
                               "FY2024 consumption."))


def _sub_inc(v, what: str) -> dict:
    """A subset figure, without the full incidence paragraph.

    `_inc` attaches the whole allocation method to every figure, which is right
    for the seven a reader can hover one at a time. Repeated across 127 subsets
    and six populations it was 1.7 MB of identical prose in a file that has to
    be downloaded. The method is stated once on the panel; these carry what
    they are.
    """
    return {"v": round(v, 4), "state": "stale", "word": "modelled, unsigned",
            "why": what + " \u2014 incidence.py", "status": LD.MODELLED,
            "key": ""}


def facts() -> list:
    """The deck's own lines, as the deck formats them.

    JW, 27 September: the MHPA board deck is authoritative for the explorer's
    conclusions. It is the right choice for a reason beyond editorial taste —
    `build_deck.py` writes its heroes as f-strings off the ledger, so a card
    taken from `CARDS` moves when the ledger moves. A card transcribed into
    this file would not, and would go on asserting a superseded figure in
    exactly the way the predecessor asserted $86.27.

    Importing `build_deck` rebuilds the deck as a side effect. That is
    tolerable and deliberate: it means the explorer cannot be built from a
    deck that would not itself build.
    """
    import contextlib, io, re
    with contextlib.redirect_stdout(io.StringIO()):
        import build_deck

    # The figures each card prints, recorded. A card arrives as formatted HTML
    # rather than as figures, so `explorerproof.py` would see numbers on screen
    # that are in no serialized field and could not tell them from numbers the
    # page invented. Harvesting them here says which artifact computed them:
    # build_deck.py, off this same ledger. The gate then has two sources it
    # will accept and still fails anything belonging to neither.
    money = re.compile(r"[\u2212-]?\$(\d[\d,]*\.\d\d)")
    out = []
    for c in build_deck.CARDS:
        if c["cls"] == "appendix":
            continue
        text = " ".join((c["kicker"], c["hero"], c["body"], c["note"] or ""))
        out.append({"kicker": c["kicker"], "hero": c["hero"],
                    "body": c["body"], "note": c["note"],
                    "figures": sorted(set(money.findall(text)))})
    return out


# ---------------------------------------------------------------------------
def provisions(L30: Ledger) -> dict:
    """The seven P.L. 119-21 lanes, and where each one's dollar stops.

    Two amounts per provision and they are different questions. `amount` is
    what leaves the trunk. `allocated` is what fails to reach a service, which
    is smaller because overhead falls with the loss (`incidence.scale`). The
    paper prints them in different places; the page shows both, labelled,
    because a reader selecting a lane can see both ends of it at once.

    The seventh carries neither an incidence nor a service: D-89 says the
    Medicare Savings moratorium's dollar pays a Medicare premium. It is listed
    with `excluded` set and the reason attached, so the page can show a lever
    that visibly does not move the service cube — which is the clearest
    statement of D-89 anywhere in the project.
    """
    import incidence as INC
    from ledger_national_2030 import HR1

    gaps = INC.coverage()
    if gaps:
        raise LD.LedgerError("incidence does not cover the ledger's HR-1 "
                             "peels:\n  " + "\n  ".join(gaps))

    named = L30.figures()
    amt = {p.key: p.amount.n for p in L30.peels if p.kind == "hr1"}
    node30 = {k: v.n for k, v in L30.claims.col_margin.items()}
    r = INC.allocate(node30, amt)

    from views import SUB_2030
    out = []
    for key in SUB_2030:                      # declaration order, S-085
        p = next(x for x in L30.peels if x.key == key)
        row = {
            "key": key, "label": p.label,
            "sub": SUB_2030[key],
            "charged": p.charged, "reach": p.reach,
            "amount": fig(p.amount, f"peel.{p.key}", named),
            "excluded": key in INC.EXCLUDED,
            "why_excluded": INC.EXCLUDED.get(key, ""),
        }
        if key in r["per_prov"]:
            v, tag, cell = r["per_prov"][key]
            row["tag"] = tag
            row["kind"] = INC.KIND[key]
            # Every one of these is a figure, not a float. The page has exactly
            # one function that writes a number and it takes a figure; a bare
            # float here would have to be formatted in the template, which is
            # the hole S-105 exists to close.
            row["allocated"] = _inc(v, key, "what fails to reach a service")
            row["by_population"] = {
                g: _inc(sum(x for (s, gg), x in cell.items() if gg == g), key,
                        f"{key} allocated to {g} by the rule the statute names")
                for g in INC.G}
            row["by_service"] = {
                s: _inc(sum(x for (ss, g), x in cell.items() if ss == s), key,
                        f"{key} landing on {s}, by each population's own "
                        f"measured FY2024 consumption")
                for s in INC.S}
        out.append(row)

    # D-111. Every subset, precomputed. JW asked for checkboxes a reader turns
    # on one at a time to watch the total build, which means a figure for each
    # of the 127 combinations. The page could add the selected ones up in two
    # lines of JavaScript; it must not. `explorerproof.py` fails on any figure
    # on screen that the ledger did not produce, and that gate is only worth
    # having if it is never the thing that gets relaxed. Seven provisions is a
    # small number and this is cheap.
    import itertools
    keys = [l["key"] for l in out]
    subsets = {}
    for n in range(1, len(keys) + 1):
        for combo in itertools.combinations(sorted(keys), n):
            leaves = sum(amt[k] for k in combo)
            reaches = sum(r["per_prov"][k][0] for k in combo
                          if k in r["per_prov"])
            subsets["|".join(combo)] = {
                "n": len(combo),
                "leaves": fig(Fig(round(leaves, 4), status=DERIVED,
                                  note="what these provisions remove from the "
                                       "flow, added from the ledger's own "
                                       "per-provision figures",
                                  parents=tuple(f"peel.{k}" for k in combo))),
                "allocated": _sub_inc(reaches, "what these provisions take "
                                                "that would have bought care"),
                "by_population": {
                    g: _sub_inc(sum(x for k in combo if k in r["per_prov"]
                                    for (s, gg), x in r["per_prov"][k][2].items()
                                    if gg == g),
                                f"what these provisions take from {g}")
                    for g in INC.G},
            }

    return {
        "lanes": out,
        "subsets": subsets,
        "pool": _inc(r["pool"], "", "the FY2030 service shortfall: what the "
                                    "law removes that would have bought care"),
        "gross": _inc(r["gross"], "", "the six allocated provisions, before "
                                      "overhead falls away with the loss"),
        "scale": round(r["scale"], 6),
        "loss_by_population": {
            g: _inc(r["loss"][g], "", f"total FY2030 loss carried by {g}")
            for g in INC.G},
        "loss_by_kind": {
            k: _inc(sum(d.values()), "",
                    "coverage is somebody dropped and the whole of their care "
                    "goes to zero; rate is the same person, still enrolled, "
                    "with their provider paid less")
            for k, d in r["loss_k"].items()},
        "populations": list(INC.G),
        "services": list(INC.S),
        "reach_of": {k: v[1] for k, v in HR1.items()},
    }
