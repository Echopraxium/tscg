#!/usr/bin/env python3
"""
tscg_validator.py — TscgOntologyValidator engine (WS-5: CTX, AXIS, DOC D1–D7, generic SHACL runner).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.3.0
Home   : ontology/toolchain/validator/tscg_validator.py

Implements the design spec (ontology/docs/_01_Worksite/
TSCG_OntologyValidator_Worksite_README.md v0.1.0), §8 first target:
CTX family + --source switch. FRB / DUP / NOT / STR are stubbed for later lots.

HARD GUARD (spec §1): DETECTION ONLY. This engine never writes to the corpus.
Findings may carry a proposed_diff; applying it is the human's job, through the
normal pipeline.

Usage
-----
  python tscg_validator.py                       # --source head --layers M3,M2,M1
  python tscg_validator.py --source local
  python tscg_validator.py --source github --layers M1
  python tscg_validator.py --report report.json
  python tscg_validator.py --file ontology/M1_CoreConcepts.jsonld
  python tscg_validator.py --shacl --layers M2          # registered grammar(s) of each layer
  python tscg_validator.py --shapes check-M3/X.ttl --layers M3   # any grammar, any files

SHACL (0.2.0, WS-5 step 1): --shacl runs the grammar(s) registered per layer in
checks/shacl_runner.GRAMMARS; --shapes runs one given grammar on the selected files
(path repo-relative, or relative to ontology/toolchain/). One finding per
sh:ValidationResult, focus nodes counted per shape, a 0-focus shape is SHACL-BLIND,
a missing pyshacl is an ERROR. Opt-in: the default run is unchanged (CTX + AXIS).

DOC (0.3.0, WS-5 step 2): --doc runs the document-plane checks D1–D7 of the WS-5
scoping note §3.1 (checks/doc.py). D1 findings are one per (file, bare key) with a
`count`; the summary and the JSON report give OCCURRENCES per check and per layer.

Exit code: 0 iff no findings of severity ERROR. (Golden integration across all four
layers arrives with the FRB/DUP/NOT/STR lots; lot 1 reports raw CTX counts and does
NOT touch golden_values.json.)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import Source, classify_layer  # noqa: E402
from checks import ctx as ctx_check  # noqa: E402
from checks import axis as axis_check  # noqa: E402
from checks import shacl_runner  # noqa: E402
from checks import doc as doc_check  # noqa: E402

# Families implemented in this lot. The rest are declared so the report shows the
# full family roster with an honest "not yet implemented" status.
_IMPLEMENTED = {"CTX": ctx_check, "AXIS": axis_check}
_PLANNED = ["FRB", "DUP", "NOT", "STR"]
_VERSION = "0.3.0"

_SEV_ORDER = {"ERROR": 0, "WARNING": 1, "INFO": 2}


def _select_files(source: Source, layers: List[str], single: str | None) -> List[str]:
    if single:
        return [single]
    manifest = source.manifest()
    picked = []
    for rel in manifest:
        layer = classify_layer(rel)
        if layer in layers:
            picked.append(rel)
    return sorted(picked)


def run_validation(source: Source, files: List[str]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for rel in files:
        try:
            text = source.read(rel)
        except (FileNotFoundError, OSError) as exc:
            findings.append({"id": "SRC-000", "severity": "ERROR", "file": rel,
                             "node": "-", "message": f"cannot read from source: {exc}"})
            continue
        for fam in _IMPLEMENTED.values():
            findings.extend(fam.run(rel, text))
    return findings


def _resolve_grammar(path: str) -> str:
    """Accept a repo-relative path, or one relative to ontology/toolchain/."""
    p = path.replace("\\", "/")
    if p.startswith("ontology/"):
        return p
    return "ontology/toolchain/" + p.lstrip("./")


def run_doc(source: Source, files: List[str]) -> tuple:
    """Document plane D1–D7. Returns (findings, {layer: {check: occurrences}})."""
    findings: List[Dict[str, Any]] = []
    per_layer: Dict[str, Dict[str, int]] = {}
    for rel in files:
        try:
            text = source.read(rel)
        except (FileNotFoundError, OSError):
            continue  # already reported as SRC-000 by run_validation
        layer = classify_layer(rel) or "?"
        f = doc_check.run(rel, text, layer)
        findings.extend(f)
        bucket = per_layer.setdefault(layer, {})
        for cid, n in doc_check.occurrences(f).items():
            bucket[cid] = bucket.get(cid, 0) + n
    return findings, {k: dict(sorted(v.items())) for k, v in sorted(per_layer.items())}


def run_shacl(source: Source, files: List[str], layers: List[str],
              shapes: str | None) -> tuple:
    """Run grammar(s) over the selected files. Returns (findings, stats list)."""
    if shapes:
        plan = [(_resolve_grammar(shapes), files)]
    else:
        plan = []
        for layer in layers:
            layer_files = [f for f in files if classify_layer(f) == layer]
            if not layer_files:
                # A grammar run on 0 files would call every shape "blind": skip it.
                continue
            grammars = shacl_runner.GRAMMARS.get(layer, [])
            if not grammars:
                # Say it: an unmeasured layer must not look like a clean one.
                plan.append((None, layer))
            for g in grammars:
                plan.append((g, layer_files))
    findings: List[Dict[str, Any]] = []
    stats: List[Dict[str, Any]] = []
    for grammar, gfiles in plan:
        if grammar is None:
            stats.append({"grammar": f"(no grammar registered for {gfiles})",
                          "error": "NOT INSTRUMENTED — nothing was validated"})
            continue
        try:
            gtext = source.read(grammar)
        except (FileNotFoundError, OSError) as exc:
            findings.append({"id": "SHACL-000", "severity": "ERROR", "file": grammar,
                             "node": "-", "message": f"grammar not readable: {exc}"})
            stats.append({"grammar": grammar, "error": str(exc)})
            continue
        pairs = []
        for rel in gfiles:
            try:
                pairs.append((rel, source.read(rel)))
            except (FileNotFoundError, OSError) as exc:
                findings.append({"id": "SRC-000", "severity": "ERROR", "file": rel,
                                 "node": "-", "message": f"cannot read from source: {exc}"})
        f, s = shacl_runner.run(grammar, gtext, pairs)
        findings.extend(f)
        stats.append(s)
    return findings, stats


def _tally(findings: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Counts per check id and per severity."""
    by_id: Dict[str, int] = {}
    by_sev: Dict[str, int] = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for f in findings:
        by_id[f["id"]] = by_id.get(f["id"], 0) + 1
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
    return {"by_id": dict(sorted(by_id.items())), "by_severity": by_sev}


def print_human(source_mode: str, files: List[str],
                findings: List[Dict[str, Any]],
                shacl_stats: List[Dict[str, Any]] | None = None,
                doc_stats: Dict[str, Dict[str, int]] | None = None) -> None:
    tally = _tally(findings)
    print("=" * 66)
    print(f"  TscgOntologyValidator {_VERSION}  |  source={source_mode}  "
          f"|  {len(files)} file(s)")
    print("=" * 66)

    # Family roster
    ctx_findings = [f for f in findings if f["id"].startswith("CTX")]
    real_ctx = [f for f in ctx_findings if f["severity"] != "INFO"]
    print(f"  CTX  : {len(real_ctx)} finding(s)  "
          f"(+{len(ctx_findings) - len(real_ctx)} INFO/advisory)")
    for fam in _PLANNED:
        print(f"  {fam}  : not yet implemented (later lot)")
    if doc_stats is not None:
        checks = [f"D{i}" for i in range(1, 8)]
        print("  DOC  : document plane D1–D7, occurrences per layer")
        print("         layer " + " ".join(f"{c:>6}" for c in checks))
        for layer, counts in doc_stats.items():
            print(f"         {layer:<5} " + " ".join(f"{counts.get(c, 0):>6}" for c in checks))
    for s in shacl_stats or []:
        if "error" in s:
            print(f"  SHACL: {s['grammar']}  NOT RUN ({s['error']})")
            continue
        print(f"  SHACL: {s['grammar']}")
        print(f"         {s['files']} file(s) | {s['results']} result(s) | "
              f"{s['not_run']} not run | {len(s['blind'])} blind shape(s) | "
              f"{s['untargeted_shapes']} untargeted (referenced) shape(s)")
        for shape, n in s["focus"].items():
            hits = sum(1 for f in findings if f["id"] == "SHACL-V"
                       and f.get("grammar") == s["grammar"] and f.get("shape") == shape)
            flag = "  <-- BLIND" if n == 0 else ""
            print(f"           {shape:<40} focus {n:>5}  results {hits:>5}{flag}")
    print("-" * 66)

    # by check id
    print("  by check id:")
    for cid, n in tally["by_id"].items():
        print(f"    {cid:<10} {n}")
    print("-" * 66)

    # findings, ERROR/WARNING first, INFO last
    ordered = sorted(findings, key=lambda f: (_SEV_ORDER.get(f["severity"], 9),
                                              f["file"], f["id"]))
    for f in ordered:
        mark = {"ERROR": "X", "WARNING": "!", "INFO": "i"}.get(f["severity"], "?")
        print(f"  [{mark}] {f['id']:<9} {f['file']}")
        print(f"        {f['node']}: {f['message']}")
    print("-" * 66)
    s = tally["by_severity"]
    print(f"  TOTAL: {s['ERROR']} ERROR | {s['WARNING']} WARNING | {s['INFO']} INFO")
    print("=" * 66)


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TSCG ontology validator (CTX, AXIS, SHACL)")
    ap.add_argument("--source", choices=["local", "head", "github"], default="head",
                    help="where to read the corpus from (default: head = authority)")
    ap.add_argument("--layers", default="M3,M2,M1",
                    help="comma list of layers to scan (default M3,M2,M1)")
    ap.add_argument("--file", default=None,
                    help="validate a single relpath (overrides --layers)")
    ap.add_argument("--doc", action="store_true",
                    help="also run the document-plane checks D1–D7 (checks/doc.py)")
    ap.add_argument("--shacl", action="store_true",
                    help="also run the SHACL grammar(s) registered for each selected layer")
    ap.add_argument("--shapes", default=None,
                    help="run THIS grammar (.ttl) on the selected files (implies --shacl)")
    ap.add_argument("--report", default=None,
                    help="write the machine-readable JSON report to this path")
    args = ap.parse_args(argv)

    source = Source(args.source)
    layers = [x.strip().upper() for x in args.layers.split(",") if x.strip()]
    files = _select_files(source, layers, args.file)
    findings = run_validation(source, files)
    shacl_stats = None
    doc_stats = None
    if args.doc:
        df, doc_stats = run_doc(source, files)
        findings.extend(df)
    if args.shacl or args.shapes:
        sf, shacl_stats = run_shacl(source, files, layers, args.shapes)
        findings.extend(sf)

    print_human(args.source, files, findings, shacl_stats, doc_stats)

    if args.report:
        report = {
            "tool": "TscgOntologyValidator",
            "version": _VERSION,
            "source": args.source,
            "authority": args.source in ("head", "github"),
            "families_implemented": sorted(_IMPLEMENTED) + ["DOC", "SHACL"],
            "doc_occurrences": doc_stats,
            "shacl": shacl_stats,
            "families_planned": _PLANNED,
            "files": files,
            "tally": _tally(findings),
            "findings": findings,
        }
        Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                     encoding="utf-8")
        print(f"  report written: {args.report}")

    errors = sum(1 for f in findings if f["severity"] == "ERROR")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
