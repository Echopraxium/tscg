#!/usr/bin/env python3
"""
tscg_validator.py — TscgOntologyValidator engine (WS-5, lot 1: CTX + source switch).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/cli-tools/validator/tscg_validator.py

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

# Families implemented in this lot. The rest are declared so the report shows the
# full family roster with an honest "not yet implemented" status.
_IMPLEMENTED = {"CTX": ctx_check}
_PLANNED = ["FRB", "DUP", "NOT", "STR"]

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


def _tally(findings: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Counts per check id and per severity."""
    by_id: Dict[str, int] = {}
    by_sev: Dict[str, int] = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    for f in findings:
        by_id[f["id"]] = by_id.get(f["id"], 0) + 1
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
    return {"by_id": dict(sorted(by_id.items())), "by_severity": by_sev}


def print_human(source_mode: str, files: List[str],
                findings: List[Dict[str, Any]]) -> None:
    tally = _tally(findings)
    print("=" * 66)
    print(f"  TscgOntologyValidator 0.1.0  |  source={source_mode}  "
          f"|  {len(files)} file(s)")
    print("=" * 66)

    # Family roster
    ctx_findings = [f for f in findings if f["id"].startswith("CTX")]
    real_ctx = [f for f in ctx_findings if f["severity"] != "INFO"]
    print(f"  CTX  : {len(real_ctx)} finding(s)  "
          f"(+{len(ctx_findings) - len(real_ctx)} INFO/advisory)")
    for fam in _PLANNED:
        print(f"  {fam}  : not yet implemented (later lot)")
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
    ap = argparse.ArgumentParser(description="TSCG ontology validator (lot 1: CTX)")
    ap.add_argument("--source", choices=["local", "head", "github"], default="head",
                    help="where to read the corpus from (default: head = authority)")
    ap.add_argument("--layers", default="M3,M2,M1",
                    help="comma list of layers to scan (default M3,M2,M1)")
    ap.add_argument("--file", default=None,
                    help="validate a single relpath (overrides --layers)")
    ap.add_argument("--report", default=None,
                    help="write the machine-readable JSON report to this path")
    args = ap.parse_args(argv)

    source = Source(args.source)
    layers = [x.strip().upper() for x in args.layers.split(",") if x.strip()]
    files = _select_files(source, layers, args.file)
    findings = run_validation(source, files)

    print_human(args.source, files, findings)

    if args.report:
        report = {
            "tool": "TscgOntologyValidator",
            "version": "0.1.0",
            "source": args.source,
            "authority": args.source in ("head", "github"),
            "families_implemented": sorted(_IMPLEMENTED),
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
