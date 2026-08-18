#!/usr/bin/env python3
"""
build_headlines.py  --  fact-sheet sidecar builder for the $100 Medicaid Dollars series.

Philosophy mirror of the conserved ledger, but for a DIFFERENT invariant:
  - ledger.json   is governed by CONSERVATION  (everything sums to $100; derive.py runs balance checks).
  - headlines.json is governed by PROVENANCE    (every value names source, vintage, basis; this script runs provenance checks).

The two are intentionally separate. A headline may sit on a different basis than the
Sankey and is allowed to "depart" from the ledger, PROVIDED its citation is intact.
The only ledger-coupled fact is the leverage ratio (#6), which is a pure function of
the jurisdiction's blended federal share; when a ledger.json is present we cross-check it.

Usage:
    python3 build_headlines.py                         # validate + render every state
    python3 build_headlines.py --state DC              # one state
    python3 build_headlines.py --ledger ledger.json    # also cross-check ledger-derived facts
    python3 build_headlines.py --out out/              # write fact sheets to a dir

Exit code is non-zero if the provenance contract is violated (mirrors a failed balance check).
"""
import argparse
import json
import os
import sys

REQUIRED = ["id", "n", "headline", "stat", "derivation", "basis", "source", "url", "vintage"]
DERIVATIONS = {"ledger", "external", "modeled"}
TAG = {"ledger": "[ledger-derived]", "external": "[external source]", "modeled": "[modeled estimate]"}

# Custom analyses are the per-state, NON-portable track (e.g. DC's economic-ripple work).
# They carry a lighter contract than the 7 portable facts: a stub only needs to declare
# itself; a built analysis must name its derivation, basis, and sources.
CUSTOM_REQUIRED_ALWAYS = ["id", "title", "question", "portable", "status"]
CUSTOM_REQUIRED_IF_BUILT = ["derivation", "basis", "sources"]
CUSTOM_STATUS = {"stub", "draft", "final"}


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def check_provenance(state_code, state):
    """Provenance contract = the headline-layer analog of the seven balance checks."""
    errors, warnings = [], []
    facts = state.get("facts", [])
    if not facts and not state_code.startswith("_"):
        errors.append(f"{state_code}: no facts present")
    seen_n = set()
    for i, f in enumerate(facts):
        where = f"{state_code} fact[{i}] (id={f.get('id', '?')})"
        for key in REQUIRED:
            if key not in f or f[key] in (None, "", []):
                errors.append(f"{where}: missing required field '{key}'")
        d = f.get("derivation")
        if d is not None and d not in DERIVATIONS:
            errors.append(f"{where}: derivation '{d}' not in {sorted(DERIVATIONS)}")
        n = f.get("n")
        if n in seen_n:
            errors.append(f"{where}: duplicate position n={n}")
        seen_n.add(n)
        # A modeled estimate must announce itself somewhere the reader will see it.
        if d == "modeled":
            blob = (f.get("stat", "") + " " + f.get("basis", "")).lower()
            if "estimate" not in blob and "modeled" not in blob:
                warnings.append(f"{where}: derivation=modeled but text never says 'estimate'")
        if not str(f.get("url", "")).startswith(("http://", "https://")):
            warnings.append(f"{where}: url is not a resolvable link")
    return errors, warnings


def check_custom(state_code, state):
    """Validate the per-state custom analyses (the non-portable track). Stubs pass with
    just the declaration; only status in {draft, final} must carry full provenance."""
    errors, warnings = [], []
    for i, c in enumerate(state.get("custom_analyses", [])):
        where = f"{state_code} custom[{i}] (id={c.get('id', '?')})"
        for key in CUSTOM_REQUIRED_ALWAYS:
            if key not in c or c[key] in (None, "", []):
                errors.append(f"{where}: missing required field '{key}'")
        status = c.get("status")
        if status is not None and status not in CUSTOM_STATUS:
            errors.append(f"{where}: status '{status}' not in {sorted(CUSTOM_STATUS)}")
        if status in ("draft", "final"):
            for key in CUSTOM_REQUIRED_IF_BUILT:
                if key not in c or c[key] in (None, "", []):
                    errors.append(f"{where}: status={status} but missing '{key}'")
            d = c.get("derivation")
            if d is not None and d not in DERIVATIONS:
                errors.append(f"{where}: derivation '{d}' not in {sorted(DERIVATIONS)}")
        # These live here precisely BECAUSE they don't port. If one truly ports, it belongs
        # in the shared 7-fact set instead.
        if c.get("portable") is True:
            warnings.append(f"{where}: marked portable=true \u2014 a portable item belongs in the shared 7-fact set, not custom_analyses.")
    return errors, warnings
    """Best-effort: locate a blended federal share in an unknown ledger schema. Returns float or None."""
    candidates = [
        ("blended_federal_share",), ("federal_share",), ("fed_share",),
        ("sources", "federal_share"), ("sources", "blended_federal_share"),
        ("meta", "federal_share"),
    ]
    for path in candidates:
        cur = ledger
        ok = True
        for k in path:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                ok = False
                break
        if ok and isinstance(cur, (int, float)):
            return float(cur) if cur <= 1 else float(cur) / 100.0
    return None


def cross_check_ledger(state_code, state, ledger):
    """Only ledger-derived facts get reconciled to the ledger. Others are deliberately left alone."""
    notes = []
    fed = find_federal_share(ledger)
    for f in state.get("facts", []):
        if f.get("derivation") != "ledger":
            continue
        chk = f.get("ledger_check")
        if not chk:
            continue
        if fed is None:
            notes.append(f"{state_code}/{f['id']}: ledger.json present but no federal-share field located; skipped cross-check.")
            continue
        expected = chk.get("expected")
        tol = chk.get("tolerance_pp", 0.5) / 100.0
        if expected is not None and abs(fed - expected) > tol:
            notes.append(
                f"{state_code}/{f['id']}: DRIFT \u2014 ledger federal share {fed:.3f} vs headline {expected:.3f} "
                f"(> {tol*100:.1f}pp). Recompute the ratio before publishing."
            )
        else:
            notes.append(f"{state_code}/{f['id']}: ledger cross-check OK (federal share {fed:.3f}).")
    return notes


def _render_findings(findings, depth=0):
    """Flatten a nested findings dict/list into readable markdown bullets."""
    lines, pad = [], "  " * depth
    if isinstance(findings, dict):
        for k, v in findings.items():
            label = str(k).replace("_", " ")
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}- **{label}:**")
                lines.extend(_render_findings(v, depth + 1))
            else:
                lines.append(f"{pad}- **{label}:** {v}")
    elif isinstance(findings, list):
        for item in findings:
            if isinstance(item, (dict, list)):
                lines.extend(_render_findings(item, depth))
            else:
                lines.append(f"{pad}- {item}")
    return lines


def render_markdown(state_code, state, recon_notes):
    dn = state.get("display_name", state_code)
    out = [f"# {dn} \u2014 Medicaid headline facts", ""]
    facts = sorted(state.get("facts", []), key=lambda x: x.get("n", 0))
    for f in facts:
        out.append(f"**{f['n']}. {f['headline']}** {f['stat']}")
        out.append("")
    out.append("---")
    out.append("")
    out.append("## Sources & basis")
    out.append("")
    for f in facts:
        out.append(f"**{f['n']}. {f['id']}** {TAG.get(f['derivation'], '')}  ")
        out.append(f"- Basis: {f['basis']}  ")
        out.append(f"- Source: {f['source']}  ")
        out.append(f"- Vintage: {f['vintage']}  ")
        out.append(f"- Link: {f['url']}")
        out.append("")
    if recon_notes:
        out.append("## Reconciliation notes (methodology, not for the infographic)")
        out.append("")
        for r in recon_notes:
            out.append(f"- {r}")
        out.append("")
    customs = state.get("custom_analyses", [])
    if customs:
        out.append("## Custom analyses (state-specific \u2014 NOT portable across states)")
        out.append("")
        for c in customs:
            status = c.get("status", "")
            dtag = TAG.get(c.get("derivation", ""), "")
            out.append(f"### {c.get('title', c.get('id', '?'))}  [{status}]{(' ' + dtag) if dtag else ''}")
            if c.get("question"):
                out.append(f"*Question:* {c['question']}")
                out.append("")
            if status == "stub":
                out.append("> STUB \u2014 to be built for this state. The question is carried as a placeholder; "
                           "numbers and even the binding factors must be re-derived locally (see custom_analysis_library).")
                out.append("")
                continue
            if c.get("basis"):
                out.append(f"*Basis:* {c['basis']}")
                out.append("")
            if c.get("findings"):
                out.extend(_render_findings(c["findings"]))
                out.append("")
            srcs = c.get("sources", [])
            if srcs:
                out.append("*Sources:*")
                for s in srcs:
                    if isinstance(s, dict):
                        nm, u = s.get("name", "source"), s.get("url", "")
                        out.append(f"- {nm}{(' \u2014 ' + u) if u else ''}")
                    else:
                        out.append(f"- {s}")
                out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--headlines", default=os.path.join(os.path.dirname(__file__), "headlines.json"))
    ap.add_argument("--ledger", default=None, help="optional path to ledger.json for cross-checking ledger-derived facts")
    ap.add_argument("--state", default=None, help="limit to one state code, e.g. DC")
    ap.add_argument("--out", default=None, help="directory to write per-state fact sheets")
    args = ap.parse_args()

    data = load(args.headlines)
    states = data.get("states", {})
    if args.state:
        states = {k: v for k, v in states.items() if k == args.state}
        if not states:
            print(f"No such state: {args.state}", file=sys.stderr)
            return 2
    else:
        # Keys beginning with "_" are templates/stubs (e.g. _TEMPLATE); skip unless asked for by name.
        states = {k: v for k, v in states.items() if not k.startswith("_")}

    ledger = load(args.ledger) if args.ledger and os.path.exists(args.ledger) else None
    if args.ledger and ledger is None:
        print(f"NOTE: ledger '{args.ledger}' not found; running standalone (no cross-check).")

    all_errors, all_warnings = [], []
    for code, st in states.items():
        errs, warns = check_provenance(code, st)
        all_errors += errs
        all_warnings += warns
        cerrs, cwarns = check_custom(code, st)
        all_errors += cerrs
        all_warnings += cwarns

    print("=" * 64)
    print("PROVENANCE CONTRACT")
    print("=" * 64)
    if all_errors:
        for e in all_errors:
            print("  FAIL:", e)
    else:
        n_facts = sum(len(s.get("facts", [])) for s in states.values())
        n_custom = sum(len(s.get("custom_analyses", [])) for s in states.values())
        print(f"  PASS: {n_facts} portable fact(s) + {n_custom} custom analysis/analyses across {len(states)} state(s); all required fields present.")
    for w in all_warnings:
        print("  warn:", w)

    if ledger is not None:
        print("\n" + "=" * 64)
        print("LEDGER CROSS-CHECK (ledger-derived facts only)")
        print("=" * 64)
        for code, st in states.items():
            for note in cross_check_ledger(code, st, ledger):
                print("  ", note)

    if all_errors:
        print("\nProvenance contract violated \u2014 not rendering. Fix the fields above.", file=sys.stderr)
        return 1

    recon = data.get("reconciliation_notes", [])
    if args.out:
        os.makedirs(args.out, exist_ok=True)
    print("\n" + "=" * 64)
    print("RENDER")
    print("=" * 64)
    for code, st in states.items():
        md = render_markdown(code, st, recon)
        if args.out:
            path = os.path.join(args.out, f"headlines_{code}.md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(md)
            print(f"  wrote {path}")
        else:
            print("\n" + md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
