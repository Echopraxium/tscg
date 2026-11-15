#!/usr/bin/env python3
"""
TSCG M0 Instance Checker — v1.8.1 (C03: an acronym name gives an all-lowercase alias)
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-06-26

Analyses all M0 instance JSON-LD files and reports their compliance
with the v1.5 conventions (M0_Common namespace, imports, no deprecated terms).

Checks performed (each reported as PASS / WARN / FAIL):
  C01  @base present and canonical
  C02  m0: resolves to M0_Common.jsonld# (shared)
  C03  m0.<instance>: local alias present. The alias is the instance name in
       camelCase; a name written entirely in capitals (an acronym: VCO, RAAS, TPACK,
       VSM) gives an all-lowercase alias (m0.vco) — naming norm, Michel 2026-11-15:
       file names keep the acronym in capitals (M0_VCO.jsonld), the ontology alias is
       in lowercase. Before 1.8.1 C03 expected m0.vCO.
  C04  m1: absolute URL
  C05  m2: absolute URL
  C06  m3: absolute URL
  C07  Obsolete aliases absent (A_score, m1core:, sm:, ...)
  C08  m1.extensions.<domain>: pattern (no old m1bio:, m1chem:, ...)
  C09  owl:imports includes M0_Common.jsonld
  C10  RETIRED 2026-11-15 (score values as bare numerics — the scores are deprecated)
  C11  RETIRED 2026-11-15 (enum values as IRIs — the enumerations were all score classes)
  C12  No tensor formula remnants:
         (a) m2:hasTensorFormula absent in ALL graph nodes
         (b) "tensorFormula" key absent in nested objects (NakamotoConsensus pattern)
         (c) "U+2297" (tensor-product) operator absent from all formula values
  C13  m3:ontologyType absent from sub-nodes (@graph[1+])
  C14  m3:changelog <= 3 entries (m2:changelog retired: FAIL)
  C15  SHACL v1.5 validation (optional — requires pyshacl)
  C16  No use of a deprecated M0_Common term. The deprecated set is READ from
       M0_Common.jsonld (nodes with owl:deprecated true), never hardcoded. A use is
       a "m0:<term>" key anywhere in @graph or in @context, or a "m0:<term>" IRI
       value ({"@id": ...} or a bare string). Added 2026-11-15 with the deprecation
       of the scoring family (evaluation is outside the model: CH4 §6).

Changes vs v1.7.0 (2026-11-15):
  C10, C11 retired with the scoring family they checked (deprecated in M0_Common:
  a model is not legitimate to evaluate itself). C16 guards against any use of a
  deprecated term. --scores removed (nothing left to show).
Changes vs v1.5.0:
  C12: Extended to detect tensorFormula in nested objects and U+2297 in formula values

Usage:
    python check_m0_instances_v1_5.py [options]

    --instance NAME     Check only one instance
    --verbose           Full check detail
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

# Paths are resolved by tscg_paths (see ontology/toolchain/tscg_paths.py).
# The former hardcoded REPO_ROOT = Path("E:/_00_Michel/...") is gone: the repo
# root is now discovered by walking UP from this file until a directory holding
# both ontology/ and instances/ is found. The script is therefore relocatable and
# machine-independent. Override with the TSCG_REPO_ROOT env var if ever needed.
# --- bootstrap: tscg_paths lives one level up, in ontology/toolchain/ ----------
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))
# ------------------------------------------------------------------------------
from tscg_paths import (                      # noqa: E402
    REPO_ROOT, ONTOLOGY_DIR, INSTANCES_ROOT, TOOLCHAIN_DIR,
    BASE_ONTOLOGY, BASE_INSTANCES, INSTANCE_DIRS, find_schema, verify_layout,
)

SCRIPT_DIR = TOOLCHAIN_DIR

DEFAULT_SHACL = find_schema(
    "M0_Instances_Schema_shacl_v1.5.ttl",
    "M0_Instances_Schema_shacl.ttl",
    "M0_Instances_Schema.shacl.ttl",
    script_dir=_Path(__file__).parent,
)

M0_COMMON_URL = BASE_ONTOLOGY + "M0_Common.jsonld#"

# NOTE: INSTANCE_DIRS now lives in tscg_paths. It also fixes a SILENT BUG: this
# script used to look for "symbolic-system-grammar" (SINGULAR) while the real
# directory is "symbolic-system-grammars" (PLURAL). discover_instances() skips a
# non-existent base_dir without a word, so the whole SymbolicSystemGrammar
# category — Iching, TriskeleToolchain — was never checked. verify_layout() now
# reports any missing compartment instead of swallowing it.

OBSOLETE_ALIASES = {
    "A_score","S_score","F_score","It_score","D_score",
    "R_score","E_score","V_score","O_score","Im_score",
    "m1core","sm",
}

OLD_EXT_ALIASES = {"m1bio","m1chem","m1phys","m1elec","m1mus",
                   "m1myth","m1econ","m1opt","m1photo","m1sysmod",
                   "m1geo","m1edu","m1energy","m1biz"}

M0_COMMON_FILE = ONTOLOGY_DIR / "M0_Common.jsonld"


def load_deprecated_terms(path: Path = M0_COMMON_FILE) -> frozenset:
    """C16: the deprecated M0_Common terms, read from the owning file.

    Returns the compact names ("m0:scoreA", ...) of every @graph node whose
    owl:deprecated is true. Never hardcoded: deprecating a term in M0_Common is
    enough for C16 to guard it. An unreadable M0_Common raises (a crashed check
    must not look like a pass).
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = set()
    for node in data.get("@graph", []):
        dep = node.get("owl:deprecated") if isinstance(node, dict) else None
        if isinstance(dep, dict):
            dep = dep.get("@value")
        if dep is True or (isinstance(dep, str) and dep.lower() == "true"):
            out.add(node.get("@id"))
    return frozenset(x for x in out if isinstance(x, str) and x.startswith("m0:"))


def find_deprecated_uses(data: dict, deprecated: frozenset) -> list:
    """C16: every use of a deprecated term in an instance (keys and IRI values)."""
    uses = []

    def walk(o, where):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in deprecated:
                    uses.append(f"{where}:{k}")
                if k == "@id" and isinstance(v, str):
                    if v in deprecated:
                        uses.append(f"{where}:@id={v}")
                    continue          # counted once, not again as a bare string
                walk(v, where)
        elif isinstance(o, list):
            for v in o:
                walk(v, where)
        elif isinstance(o, str) and o in deprecated:
            uses.append(f"{where}:value={o}")

    ctx = data.get("@context", {})
    for c in (ctx if isinstance(ctx, list) else [ctx]):
        if isinstance(c, dict):
            uses += [f"@context:{k}" for k in c if k in deprecated]
    walk(data.get("@graph", []), "@graph")
    return uses

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

    def __init__(self, path: Path, name: str, itype: str, deprecated: frozenset = frozenset()):
        self.path = path
        self.name = name
        self.itype = itype
        self.deprecated = deprecated

    def _camel(self):
        import re as _re
        if len(self.name) > 1 and self.name.isupper():
            return self.name.lower()          # acronym: VCO -> vco (1.8.1)
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

        # ── C10, C11: retired 2026-11-15 (see the module docstring) ──────────

        # ── C16: no use of a deprecated M0_Common term ───────────────────────
        uses = find_deprecated_uses(data, self.deprecated)
        if uses:
            shown = ", ".join(uses[:6]) + (f" (+{len(uses) - 6})" if len(uses) > 6 else "")
            rep.checks.append(Check("C16","No deprecated M0 term", FAIL,
                                    f"{len(uses)} use(s): {shown}"))
        else:
            rep.checks.append(Check("C16","No deprecated M0 term", PASS))

        # ── C12: No tensor formula remnants (v1.5.1 — extended) ──────────────
        # Detects three patterns:
        #   (a) m2:hasTensorFormula key in any graph node       (AdaptativeImmuneResponse)
        #   (b) "tensorFormula" key in nested concept objects   (NakamotoConsensus)
        #   (c) "U+2297" operator in any string value              (both)
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

        # (c) "U+2297" tensor product operator in any formula value
        raw_str = json.dumps(graph, ensure_ascii=False)
        if "\u2297" in raw_str:  # U+2297 tensor-product operator
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
        # WS-1 lot 1e (2026-09-30): the changelog container is m3:changelog;
        # m2:changelog is retired and reported as a FAIL if it reappears.
        cl = ontology.get("m3:changelog")
        if "m2:changelog" in ontology:
            rep.checks.append(Check("C14","changelog <= 3 entries", FAIL, "m2:changelog is retired: use m3:changelog"))
        elif isinstance(cl, list):
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
    ("C12","No tensor remnants"),
    ("C13","ontologyType only in @graph[0]"),
    ("C14","changelog <= 3 entries"),
    ("C15","SHACL v1.5"),
    ("C16","No deprecated M0 term"),
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


def print_verbose(rep: InstanceReport):
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
    parser = argparse.ArgumentParser(description="TSCG M0 Instance Checker v1.8.1")
    parser.add_argument("--instance",    metavar="NAME")
    parser.add_argument("--verbose",     action="store_true")
    parser.add_argument("--fails",       action="store_true")
    parser.add_argument("--no-shacl",    action="store_true")
    parser.add_argument("--shacl-schema", metavar="PATH")
    parser.add_argument("--json",        metavar="PATH")
    args = parser.parse_args()

    shacl_schema = Path(args.shacl_schema) if args.shacl_schema else DEFAULT_SHACL
    run_shacl    = not args.no_shacl

    print("=" * 70)
    print("TSCG M0 INSTANCE CHECKER — v1.8.1")
    print("=" * 70)

    deprecated = load_deprecated_terms()   # C16: read from M0_Common, never hardcoded
    print(f"C16: {len(deprecated)} deprecated M0_Common term(s) guarded")

    instances = list(discover_instances(only_name=args.instance))
    if not instances:
        print(f"\n[WN] No JSON-LD files found for: {args.instance or 'any instance'}")
        return 1

    print(f"\nChecking {len(instances)} instance(s)...\n")

    reports = []
    for jsonld_path, name, itype in instances:
        checker = InstanceChecker(jsonld_path, name, itype, deprecated)
        rep     = checker.run(run_shacl=run_shacl, shacl_schema=shacl_schema)
        reports.append(rep)
        overall = rep.status_summary()
        icon    = {"PASS":"OK","WARN":"WN","FAIL":"XX","N/A":"--"}.get(overall, "--")
        print(f"  [{icon}] {name:<28} [{itype}]")

    if args.verbose:
        for r in reports:
            print_verbose(r)
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
