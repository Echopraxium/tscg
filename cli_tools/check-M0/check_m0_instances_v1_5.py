#!/usr/bin/env python3
"""
TSCG M0 Instance Checker — v1.5.1
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-06-26

Analyses all M0 instance JSON-LD files and reports their compliance
with the v1.5 conventions (M0_Common namespace, bare numerics, enum IRIs).

Checks performed (each reported as PASS / WARN / FAIL):
  C01  @base present and canonical
  C02  m0: resolves to M0_Common.jsonld# (shared)
  C03  m0.<instance>: local alias present
  C04  m1: absolute URL
  C05  m2: absolute URL
  C06  m3: absolute URL
  C07  Obsolete aliases absent (A_score, m1core:, sm:, ...)
  C08  m1.extensions.<domain>: pattern (no old m1bio:, m1chem:, ...)
  C09  owl:imports includes M0_Common.jsonld
  C10  Score values are bare numerics (not {"@value":..., "@type":xsd:float})
  C11  Enum values are IRIs (not bare strings "Coherent")
  C12  No tensor formula remnants:
         (a) m2:hasTensorFormula absent in ALL graph nodes
         (b) "tensorFormula" key absent in nested objects (NakamotoConsensus pattern)
         (c) "⊗" operator absent from all formula values
  C13  m3:ontologyType absent from sub-nodes (@graph[1+])
  C14  m2:changelog <= 3 entries
  C15  SHACL v1.5 validation (optional — requires pyshacl)

Changes vs v1.5.0:
  C12: Extended to detect tensorFormula in nested objects and ⊗ in formula values

Usage:
    python check_m0_instances_v1_5.py [options]

    --instance NAME     Check only one instance
    --verbose           Full check detail
    --scores            Include parsed score values in output
    --fails             Only show instances with violations
    --no-shacl          Skip pyshacl (faster)
    --shacl-schema PATH Override SHACL schema path
    --json PATH         Write JSON report to file
"""

import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

REPO_ROOT      = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")
INSTANCES_ROOT = REPO_ROOT / "instances"
ONTOLOGY_DIR   = REPO_ROOT / "ontology"
SCRIPT_DIR     = Path(__file__).parent.resolve()

def _find_shacl():
    for candidate in [
        SCRIPT_DIR / "M0_Instances_Schema_shacl_v1.5.ttl",
        SCRIPT_DIR / "M0_Instances_Schema_shacl.ttl",
        SCRIPT_DIR / "M0_Instances_Schema.shacl.ttl",
        ONTOLOGY_DIR / "M0_Instances_Schema_shacl.ttl",
        ONTOLOGY_DIR / "M0_Instances_Schema.shacl.ttl",
    ]:
        if candidate.exists():
            return candidate
    return None

DEFAULT_SHACL = _find_shacl()

BASE_ONTOLOGY  = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
BASE_INSTANCES = "https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/"
M0_COMMON_URL  = BASE_ONTOLOGY + "M0_Common.jsonld#"

INSTANCE_DIRS = {
    "poclet":            (INSTANCES_ROOT / "poclets",                  "m3:Poclet"),
    "systemic_framework":(INSTANCES_ROOT / "systemic-frameworks",      "m3:SystemicFramework"),
    "symbolic_grammar":  (INSTANCES_ROOT / "symbolic-system-grammar", "m3:SymbolicSystemGrammar"),
    "tscg_tool":         (INSTANCES_ROOT / "tscg-tools",               "m3:TscgTool"),
    "transdisclet":      (INSTANCES_ROOT / "transdisclet",             "m3:TransDisclet"),
}

OBSOLETE_ALIASES = {
    "A_score","S_score","F_score","It_score","D_score",
    "R_score","E_score","V_score","O_score","Im_score",
    "m1core","sm",
}

OLD_EXT_ALIASES = {"m1bio","m1chem","m1phys","m1elec","m1mus",
                   "m1myth","m1econ","m1opt","m1photo","m1sysmod",
                   "m1geo","m1edu","m1energy","m1biz"}

SCORE_PROPS = [
    "m0:scoreA","m0:scoreS","m0:scoreF","m0:scoreIt","m0:scoreD",
    "m0:scoreR","m0:scoreE","m0:scoreV","m0:scoreO","m0:scoreIm",
    "m0:asfidMean","m0:revoiMean","m0:epistemicGap",
    "m0:focalScore","m0:focalBias","m0:stereopsicDepth",
]

ENUM_PROPS = {
    "m0:spectralClass": "m0:spectralClass.",
    "m0:focalClass":    "m0:focalClass.",
    "m0:scoringStatus": "m0:scoringStatus.",
}

# ============================================================================
# CHECK RESULT
# ============================================================================

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
NA   = "N/A"

@dataclass
class Check:
    code:    str
    name:    str
    status:  str = NA
    detail:  str = ""

@dataclass
class InstanceReport:
    name:          str
    itype:         str
    path:          Path
    checks:        list = field(default_factory=list)
    scores:        dict = field(default_factory=dict)
    shacl_status:  str  = NA
    shacl_msg:     str  = ""
    parse_error:   str  = ""

    def status_summary(self):
        statuses = {c.status for c in self.checks}
        if FAIL in statuses: return FAIL
        if WARN in statuses: return WARN
        if PASS in statuses: return PASS
        return NA

    def count(self, status):
        return sum(1 for c in self.checks if c.status == status)


# ============================================================================
# CHECKER
# ============================================================================

class InstanceChecker:

    def __init__(self, path: Path, name: str, itype: str):
        self.path = path
        self.name = name
        self.itype = itype

    def _camel(self):
        import re as _re
        parts = _re.split(r'[_\-]', self.name)
        if len(parts) > 1:
            return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])
        return self.name[0].lower() + self.name[1:]

    def run(self, run_shacl=True, shacl_schema=None) -> InstanceReport:
        rep = InstanceReport(name=self.name, itype=self.itype, path=self.path)

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            rep.parse_error = str(e)
            for code, name in CHECKS_META:
                rep.checks.append(Check(code, name, FAIL, f"Parse error: {e}"))
            return rep

        ctx      = data.get("@context", {})
        graph    = data.get("@graph", [])
        ontology = graph[0] if graph else {}

        # ── C01 ───────────────────────────────────────────────────────────────
        base = ctx.get("@base", "")
        if base == BASE_ONTOLOGY:
            rep.checks.append(Check("C01","@base canonical", PASS))
        elif base and "Echopraxium/tscg" in base:
            rep.checks.append(Check("C01","@base canonical", WARN, f"Non-standard: {base}"))
        elif base:
            rep.checks.append(Check("C01","@base canonical", FAIL, f"Wrong @base: {base}"))
        else:
            rep.checks.append(Check("C01","@base canonical", FAIL, "@base absent"))

        # ── C02 ───────────────────────────────────────────────────────────────
        m0_val = ctx.get("m0", "")
        if m0_val == M0_COMMON_URL:
            rep.checks.append(Check("C02","m0: = M0_Common#", PASS))
        elif "M0_Common" in m0_val:
            rep.checks.append(Check("C02","m0: = M0_Common#", WARN, f"Non-canonical: {m0_val}"))
        elif m0_val:
            rep.checks.append(Check("C02","m0: = M0_Common#", FAIL, f"m0: → {m0_val}"))
        else:
            rep.checks.append(Check("C02","m0: = M0_Common#", FAIL, "m0: absent"))

        # ── C03 ───────────────────────────────────────────────────────────────
        camel     = self._camel()
        local_key = f"m0.{camel}"
        local_val = ctx.get(local_key, "")
        if local_val and BASE_INSTANCES in local_val and "M0_" in local_val:
            rep.checks.append(Check("C03","m0.<inst>: local alias", PASS, f"{local_key}"))
        elif local_val:
            rep.checks.append(Check("C03","m0.<inst>: local alias", WARN, f"Unexpected IRI: {local_val}"))
        else:
            rep.checks.append(Check("C03","m0.<inst>: local alias", FAIL, f"Missing: {local_key}"))

        # ── C04–C06 ───────────────────────────────────────────────────────────
        STD_NS = {
            "C04": ("m1", BASE_ONTOLOGY + "M1_CoreConcepts.jsonld#"),
            "C05": ("m2", BASE_ONTOLOGY + "M2_GenericConcepts.jsonld#"),
            "C06": ("m3", BASE_ONTOLOGY + "M3_GenesisGrammar.jsonld#"),
        }
        for code, (alias, expected) in STD_NS.items():
            val = ctx.get(alias, "")
            label = f"{alias}: absolute URL"
            if val == expected:
                rep.checks.append(Check(code, label, PASS))
            elif val.startswith("http"):
                rep.checks.append(Check(code, label, WARN, f"{alias}: {val}"))
            elif val:
                rep.checks.append(Check(code, label, FAIL, f"{alias}: relative URL"))
            else:
                rep.checks.append(Check(code, label, FAIL, f"{alias}: absent"))

        # ── C07 ───────────────────────────────────────────────────────────────
        found_obsolete = [a for a in OBSOLETE_ALIASES if a in ctx]
        if found_obsolete:
            rep.checks.append(Check("C07","No obsolete aliases", FAIL, f"Found: {', '.join(found_obsolete)}"))
        else:
            rep.checks.append(Check("C07","No obsolete aliases", PASS))

        # ── C08 ───────────────────────────────────────────────────────────────
        old_ext = [a for a in OLD_EXT_ALIASES if a in ctx]
        new_ext = [k for k in ctx if k.startswith("m1.extensions.")]
        if old_ext:
            rep.checks.append(Check("C08","m1.extensions. pattern", FAIL, f"Old aliases: {', '.join(old_ext)}"))
        else:
            rep.checks.append(Check("C08","m1.extensions. pattern", PASS,
                                    f"{len(new_ext)} extension(s)" if new_ext else "None needed"))

        # ── C09 ───────────────────────────────────────────────────────────────
        imports = ontology.get("owl:imports", [])
        if isinstance(imports, str): imports = [imports]
        if any("M0_Common" in str(i) for i in imports):
            rep.checks.append(Check("C09","owl:imports M0_Common", PASS))
        else:
            rep.checks.append(Check("C09","owl:imports M0_Common", FAIL, "M0_Common not in imports"))

        # ── C10 ───────────────────────────────────────────────────────────────
        typed_scores = [p for p in SCORE_PROPS
                        if isinstance(ontology.get(p), dict) and "@value" in ontology[p]]
        if typed_scores:
            rep.checks.append(Check("C10","Score bare numerics", FAIL, f"Typed: {', '.join(typed_scores)}"))
        else:
            rep.checks.append(Check("C10","Score bare numerics", PASS))

        for prop in SCORE_PROPS:
            val = ontology.get(prop)
            if isinstance(val, (int, float)):
                rep.scores[prop] = val
            elif isinstance(val, dict) and "@value" in val:
                try: rep.scores[prop] = float(val["@value"])
                except: pass

        # ── C11 ───────────────────────────────────────────────────────────────
        string_enums = []
        for prop, prefix in ENUM_PROPS.items():
            val = ontology.get(prop)
            if isinstance(val, str) and not val.startswith(prefix):
                string_enums.append(f"{prop}={val!r}")
        if string_enums:
            rep.checks.append(Check("C11","Enum values as IRIs", FAIL, f"String values: {', '.join(string_enums)}"))
        else:
            rep.checks.append(Check("C11","Enum values as IRIs", PASS))

        # ── C12: No tensor formula remnants (v1.5.1 — extended) ──────────────
        # Detects three patterns:
        #   (a) m2:hasTensorFormula key in any graph node       (AdaptativeImmuneResponse)
        #   (b) "tensorFormula" key in nested concept objects   (NakamotoConsensus)
        #   (c) "⊗" operator in any string value               (both)
        tensor_issues = []

        # (a) Direct m2:hasTensorFormula property on any graph node
        for i, node in enumerate(graph):
            if "m2:hasTensorFormula" in node:
                label = node.get("rdfs:label", node.get("@id", f"node[{i}]"))
                tensor_issues.append(f"m2:hasTensorFormula in '{label}'")

        # (b) "tensorFormula" key in any nested object (recursive scan)
        def _scan_tensor_key(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "tensorFormula":
                        tensor_issues.append(f"tensorFormula key at {path}")
                    else:
                        _scan_tensor_key(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    _scan_tensor_key(item, f"{path}[{idx}]")

        for i, node in enumerate(graph):
            _scan_tensor_key(node, f"@graph[{i}]")

        # (c) "⊗" tensor product operator in any formula value
        raw_str = json.dumps(graph)
        if "\u2297" in raw_str:  # ⊗ = U+2297
            count = raw_str.count("\u2297")
            tensor_issues.append(f"\u2297 operator found ({count} occurrence(s)) — migrate to \u00d7/+/|")

        # Deduplicate preserving order
        tensor_issues = list(dict.fromkeys(tensor_issues))

        if tensor_issues:
            summary = "; ".join(tensor_issues[:3])
            if len(tensor_issues) > 3:
                summary += f" (+{len(tensor_issues)-3} more)"
            rep.checks.append(Check("C12","No tensor remnants", FAIL, summary))
        else:
            rep.checks.append(Check("C12","No tensor remnants", PASS))

        # ── C13 ───────────────────────────────────────────────────────────────
        subnode_ont_type = []
        for i, node in enumerate(graph[1:], start=1):
            if "m3:ontologyType" in node:
                label = node.get("rdfs:label", node.get("@id", f"node[{i}]"))
                subnode_ont_type.append(str(label))
        if subnode_ont_type:
            rep.checks.append(Check("C13","ontologyType only in @graph[0]", FAIL,
                                    f"Found in: {', '.join(subnode_ont_type)}"))
        else:
            rep.checks.append(Check("C13","ontologyType only in @graph[0]", PASS))

        # ── C14 ───────────────────────────────────────────────────────────────
        cl = ontology.get("m2:changelog")
        if isinstance(cl, list):
            if len(cl) > 3:
                rep.checks.append(Check("C14","changelog <= 3 entries", FAIL, f"{len(cl)} entries"))
            else:
                rep.checks.append(Check("C14","changelog <= 3 entries", PASS, f"{len(cl)} entr{'y' if len(cl)==1 else 'ies'}"))
        else:
            rep.checks.append(Check("C14","changelog <= 3 entries", NA, "absent (optional)"))

        # ── C15 ───────────────────────────────────────────────────────────────
        if run_shacl:
            schema = shacl_schema or DEFAULT_SHACL
            if schema and schema.exists():
                passed, msg = self._run_shacl(schema)
                status = PASS if passed is True else (FAIL if passed is False else WARN)
                rep.shacl_status = status
                rep.shacl_msg    = msg
                rep.checks.append(Check("C15","SHACL v1.5", status, msg[:120]))
            else:
                rep.checks.append(Check("C15","SHACL v1.5", NA, f"Schema not found"))

        return rep

    def _run_shacl(self, schema):
        import subprocess
        try:
            result = subprocess.run(
                ["pyshacl", "-s", str(schema), "-df", "json-ld", str(self.path)],
                capture_output=True, text=True, cwd=str(ONTOLOGY_DIR), timeout=30
            )
            if "Conforms: True" in result.stdout:
                return True, "Conforms"
            lines = result.stdout.split("\n")
            msgs  = [l for l in lines if "Message:" in l or "Constraint Violation" in l]
            return False, "; ".join(msgs[:3]) if msgs else result.stdout[:300]
        except subprocess.TimeoutExpired:
            return None, "pyshacl timeout"
        except Exception as e:
            return None, str(e)


# ============================================================================
# CHECK METADATA
# ============================================================================

CHECKS_META = [
    ("C01","@base canonical"),
    ("C02","m0: = M0_Common#"),
    ("C03","m0.<inst>: local alias"),
    ("C04","m1: absolute URL"),
    ("C05","m2: absolute URL"),
    ("C06","m3: absolute URL"),
    ("C07","No obsolete aliases"),
    ("C08","m1.extensions. pattern"),
    ("C09","owl:imports M0_Common"),
    ("C10","Score bare numerics"),
    ("C11","Enum values as IRIs"),
    ("C12","No tensor remnants"),
    ("C13","ontologyType only in @graph[0]"),
    ("C14","changelog <= 3 entries"),
    ("C15","SHACL v1.5"),
]

STATUS_ICON = {PASS: "OK", WARN: "WN", FAIL: "XX", NA: "--"}


# ============================================================================
# DISCOVERY
# ============================================================================

def discover_instances(only_name=None):
    seen = set()
    for itype, (base_dir, _) in INSTANCE_DIRS.items():
        if not base_dir.exists():
            continue
        for d in sorted(base_dir.iterdir()):
            if not d.is_dir() or d.name.startswith("_"):
                continue
            jsonld_files = sorted(d.glob("M0_*.jsonld"))
            if not jsonld_files:
                continue
            for jsonld in jsonld_files:
                name = jsonld.stem[3:]
                if only_name and name != only_name and d.name != only_name:
                    continue
                key = str(jsonld)
                if key not in seen:
                    seen.add(key)
                    yield jsonld, name, itype
        for jsonld in sorted(base_dir.glob("M0_*.jsonld")):
            name = jsonld.stem[3:]
            if only_name and name != only_name:
                continue
            key = str(jsonld)
            if key not in seen:
                seen.add(key)
                yield jsonld, name, itype


# ============================================================================
# OUTPUT
# ============================================================================

def print_summary_table(reports):
    CODES = [c for c,_ in CHECKS_META]
    icons = {PASS:"OK", WARN:"WN", FAIL:"XX", NA:"--"}
    print(f"\n{'─'*95}")
    print(f"{'Instance':<22} {'Type':<18} " + " ".join(f"{c:>4}" for c in CODES) + "  Status")
    print(f"{'─'*95}")
    for r in reports:
        chk = {c.code: c.status for c in r.checks}
        cols = " ".join(f"{icons.get(chk.get(code, NA), '--'):>4}" for code in CODES)
        overall = r.status_summary()
        ov_icon = {"PASS":"OK","WARN":"WN","FAIL":"XX","N/A":"--"}.get(overall, "--")
        print(f"  {r.name:<20} {r.itype:<18} {cols}  {ov_icon} {overall}")
    print(f"{'─'*95}")


def print_verbose(rep: InstanceReport, show_scores=False):
    overall = rep.status_summary()
    icon = {"PASS":"OK","WARN":"WN","FAIL":"XX","N/A":"--"}.get(overall, "--")
    print(f"\n{'='*70}")
    print(f"  {rep.name}  [{rep.itype}]  -> [{icon}] {overall}")
    print(f"  {rep.path}")
    print(f"{'='*70}")
    if rep.parse_error:
        print(f"  XX PARSE ERROR: {rep.parse_error}")
        return
    for c in rep.checks:
        icon = {"PASS":"OK","WARN":"WN","FAIL":"XX","N/A":"--"}.get(c.status, "--")
        line = f"  [{icon}] [{c.code}] {c.name}"
        if c.detail:
            line += f"\n         {c.detail}"
        print(line)
    if show_scores and rep.scores:
        print(f"\n  Scores:")
        for k, v in rep.scores.items():
            print(f"    {k}: {v:.3f}")


def print_compact_fails(reports):
    failed = [r for r in reports if r.status_summary() == FAIL]
    if not failed:
        print("\n[OK] All instances compliant.")
        return
    for r in failed:
        fails = [c for c in r.checks if c.status == FAIL]
        print(f"\n[XX] {r.name} [{r.itype}] — {len(fails)} FAIL(s):")
        for c in fails:
            print(f"   [{c.code}] {c.name}: {c.detail}")


def write_json_report(reports, path):
    def ser_rep(r):
        return {
            "name": r.name, "type": r.itype, "path": str(r.path),
            "status": r.status_summary(),
            "counts": {"pass": r.count(PASS), "warn": r.count(WARN), "fail": r.count(FAIL)},
            "checks": [{"code":c.code,"name":c.name,"status":c.status,"detail":c.detail} for c in r.checks],
            "scores": r.scores,
            "shacl":  {"status": r.shacl_status, "message": r.shacl_msg},
        }
    out = {
        "generated": datetime.now().isoformat(),
        "total": len(reports),
        "summary": {
            "pass": sum(1 for r in reports if r.status_summary() == PASS),
            "warn": sum(1 for r in reports if r.status_summary() == WARN),
            "fail": sum(1 for r in reports if r.status_summary() == FAIL),
        },
        "instances": [ser_rep(r) for r in reports],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nJSON report: {path}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="TSCG M0 Instance Checker v1.5.1")
    parser.add_argument("--instance",    metavar="NAME")
    parser.add_argument("--verbose",     action="store_true")
    parser.add_argument("--scores",      action="store_true")
    parser.add_argument("--fails",       action="store_true")
    parser.add_argument("--no-shacl",    action="store_true")
    parser.add_argument("--shacl-schema", metavar="PATH")
    parser.add_argument("--json",        metavar="PATH")
    args = parser.parse_args()

    shacl_schema = Path(args.shacl_schema) if args.shacl_schema else DEFAULT_SHACL
    run_shacl    = not args.no_shacl

    print("=" * 70)
    print("TSCG M0 INSTANCE CHECKER — v1.5.1")
    print("C12 extended: hasTensorFormula + tensorFormula key + ⊗ operator")
    print("=" * 70)

    instances = list(discover_instances(only_name=args.instance))
    if not instances:
        print(f"\n[WN] No JSON-LD files found for: {args.instance or 'any instance'}")
        return 1

    print(f"\nChecking {len(instances)} instance(s)...\n")

    reports = []
    for jsonld_path, name, itype in instances:
        checker = InstanceChecker(jsonld_path, name, itype)
        rep     = checker.run(run_shacl=run_shacl, shacl_schema=shacl_schema)
        reports.append(rep)
        overall = rep.status_summary()
        icon    = {"PASS":"OK","WARN":"WN","FAIL":"XX","N/A":"--"}.get(overall, "--")
        print(f"  [{icon}] {name:<28} [{itype}]")

    if args.verbose:
        for r in reports:
            print_verbose(r, show_scores=args.scores)
    elif args.fails:
        print_compact_fails(reports)
    else:
        print_summary_table(reports)

    n_pass = sum(1 for r in reports if r.status_summary() == PASS)
    n_warn = sum(1 for r in reports if r.status_summary() == WARN)
    n_fail = sum(1 for r in reports if r.status_summary() == FAIL)

    print(f"\n{'='*70}")
    print(f"RESULTS: [OK] {n_pass} PASS  [WN] {n_warn} WARN  [XX] {n_fail} FAIL  (total: {len(reports)})")

    fail_by_check = {}
    for r in reports:
        for c in r.checks:
            if c.status == FAIL:
                fail_by_check[c.code] = fail_by_check.get(c.code, 0) + 1
    if fail_by_check:
        print(f"\nPer-check failure counts:")
        for code, cname in CHECKS_META:
            count = fail_by_check.get(code, 0)
            if count:
                print(f"  [{code}] {cname}: {count} FAIL(s)")

    if args.json:
        write_json_report(reports, Path(args.json))

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
