#!/usr/bin/env python3
"""
check_M1.py — TSCG M1 Layer Validation & Correction Script
===========================================================
Author  : Echopraxium with the collaboration of Claude AI
Version : 1.4.0
Date    : 2026-05-26
Location: cli_tools/check-M1/check_M1.py

Usage
-----
  python check_M1.py                          # Validate all M1 files
  python check_M1.py --dry-run               # Show issues without fixing
  python check_M1.py --file M1_Geology.jsonld # Single file
  python check_M1.py --file M1_Geology.jsonld --dry-run
  python check_M1.py --shacl                  # Also run SHACL validation
  python check_M1.py --report                 # Save HTML/text report

Options
-------
  --dry-run        Show issues only, do not write corrections
  --file PATH      Validate/fix a single M1 file
  --shacl          Run SHACL validation (requires pyshacl)
  --report         Save validation report to check_M1_report.txt
  --no-color       Disable colored terminal output
  -v, --verbose    Show all checks (including passed)
"""

import argparse
import json
import os
import re
import sys
import datetime
from pathlib import Path
from typing import List, Tuple, Optional

# ── ANSI colours ──────────────────────────────────────────────────────────────
USE_COLOR = True

def clr(code, text):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

OK   = lambda t: clr("32", f"✅ {t}")
WARN = lambda t: clr("33", f"⚠️  {t}")
ERR  = lambda t: clr("31", f"❌ {t}")
FIX  = lambda t: clr("34", f"🔧 {t}")
INFO = lambda t: clr("36", f"ℹ️  {t}")
HDR  = lambda t: clr("1",  t)

# ── Constants ──────────────────────────────────────────────────────────────────
ONTOLOGY_BASE   = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
EXPECTED_CREATOR = "Echopraxium with the collaboration of Claude AI"
GENESIS_GRAMMAR  = "M3_GenesisGrammar.jsonld"
GENESIS_SPACE    = "M3_GenesisSpace.jsonld"         # FORBIDDEN (old name)


# Map: filename → relative path from ontology/ base dir
# Core files are at root; extensions are in M1_extensions/<domain>/
M1_FILES = {
    "M1_CoreConcepts.jsonld":      "M1_CoreConcepts.jsonld",
    "M1_Domains.jsonld":           "M1_Domains.jsonld",
    "M1_Biology.jsonld":           "M1_extensions/biology/M1_Biology.jsonld",
    "M1_Chemistry.jsonld":         "M1_extensions/chemistry/M1_Chemistry.jsonld",
    "M1_Economics.jsonld":         "M1_extensions/economics/M1_Economics.jsonld",
    "M1_Education.jsonld":         "M1_extensions/education/M1_Education.jsonld",
    "M1_Electronics.jsonld":       "M1_extensions/electronics/M1_Electronics.jsonld",
    "M1_EnergyGenerators.jsonld":  "M1_extensions/energy_generators/M1_EnergyGenerators.jsonld",
    "M1_Geology.jsonld":           "M1_extensions/geology/M1_Geology.jsonld",
    "M1_music.jsonld":             "M1_extensions/music/M1_music.jsonld",
    "M1_Mythology.jsonld":         "M1_extensions/mythology/M1_Mythology.jsonld",
    "M1_Optics.jsonld":            "M1_extensions/optics/M1_Optics.jsonld",
    "M1_Photography.jsonld":       "M1_extensions/photography/M1_Photography.jsonld",
    "M1_Physics.jsonld":           "M1_extensions/physics/M1_Physics.jsonld",
    "M1_SystemicModeling.jsonld":  "M1_extensions/system_modeling/M1_SystemicModeling.jsonld",
}

# Core files that don't need m3:eagle_eye / m3:sphinx_eye in @context
M1_CORE_FILES = {"M1_CoreConcepts.jsonld", "M1_Domains.jsonld"}

# ── Issue class ────────────────────────────────────────────────────────────────
class Issue:
    def __init__(self, severity: str, code: str, message: str,
                 fix: Optional[str] = None, auto_fixable: bool = False):
        self.severity    = severity       # "ERROR" | "WARNING" | "INFO"
        self.code        = code
        self.message     = message
        self.fix         = fix            # description of fix if auto_fixable
        self.auto_fixable = auto_fixable

    def __str__(self):
        icon = {"ERROR": ERR, "WARNING": WARN, "INFO": INFO}[self.severity]
        return icon(f"[{self.code}] {self.message}")

# ── Checker ───────────────────────────────────────────────────────────────────
class M1Checker:

    def __init__(self, path: Path, dry_run: bool = False, verbose: bool = False):
        self.path     = path
        self.dry_run  = dry_run
        self.verbose  = verbose
        self.issues: List[Issue] = []
        self.data: Optional[dict] = None
        self.content: str = ""
        self.modified = False

    # ── Load ──────────────────────────────────────────────────────────────────
    def load(self) -> bool:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.content = f.read()
            self.data = json.loads(self.content)
            return True
        except json.JSONDecodeError as e:
            self.issues.append(Issue("ERROR", "JSON001",
                f"JSON parse error: {e}", auto_fixable=False))
            return False
        except FileNotFoundError:
            self.issues.append(Issue("ERROR", "IO001",
                f"File not found: {self.path}", auto_fixable=False))
            return False

    # ── Save ──────────────────────────────────────────────────────────────────
    def save(self):
        if self.modified and not self.dry_run:
            with open(self.path, "w", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(self.data, ensure_ascii=False, indent=2))

    # ── Checks (non-mutating) → Issue list ───────────────────────────────────
    def check_crlf(self):
        if b"\r\n" in self.path.read_bytes():
            self.issues.append(Issue("ERROR", "ENC001",
                "CRLF line endings detected",
                fix="Convert to LF", auto_fixable=True))

    def check_context(self):
        ctx  = self.data.get("@context", {})
        fname = self.path.name
        is_extension = fname not in M1_CORE_FILES

        # Keys required in ALL M1 files
        base_keys = ["@base", "m1", "m2", "rdf", "rdfs", "owl", "xsd", "dcterms", "skos"]
        # Keys required only in extension files (which reference M3 dimensions)
        ext_keys  = ["m3", "m3:eagle_eye", "m3:sphinx_eye"]

        for key in base_keys:
            if key not in ctx:
                self.issues.append(Issue("WARNING", "CTX001",
                    f"@context missing key: '{key}'", auto_fixable=False))
        if is_extension:
            for key in ext_keys:
                if key not in ctx:
                    self.issues.append(Issue("WARNING", "CTX001",
                        f"@context missing key (extension): '{key}'", auto_fixable=False))

        # @base must point to ontology root
        base = ctx.get("@base", "")
        if base and base != ONTOLOGY_BASE:
            self.issues.append(Issue("ERROR", "CTX002",
                f"@base incorrect: {base}",
                fix=f"Set @base to {ONTOLOGY_BASE}", auto_fixable=True))

        # m3 must point to GenesisGrammar, not GenesisSpace
        m3 = ctx.get("m3", "")
        if GENESIS_SPACE in m3:
            self.issues.append(Issue("ERROR", "CTX003",
                f"m3 context points to M3_GenesisSpace (obsolete): {m3}",
                fix=f"Replace GenesisSpace with GenesisGrammar",
                auto_fixable=True))

    def check_ontology_node(self):
        graph = self.data.get("@graph", [])
        ont_nodes = [n for n in graph if n.get("@type") == "owl:Ontology"]
        if not ont_nodes:
            self.issues.append(Issue("ERROR", "ONT001",
                "No owl:Ontology node found in @graph", auto_fixable=False))
            return
        ont = ont_nodes[0]

        # Creator
        creator = ont.get("dcterms:creator", "")
        if creator != EXPECTED_CREATOR:
            self.issues.append(Issue("ERROR", "ONT002",
                f"dcterms:creator incorrect: '{creator}'",
                fix=f"Set to '{EXPECTED_CREATOR}'", auto_fixable=True))

        # Created date format
        created = ont.get("dcterms:created", "")
        if created and not re.match(r"^\d{4}-\d{2}-\d{2}$", created):
            self.issues.append(Issue("WARNING", "ONT003",
                f"dcterms:created not ISO 8601: '{created}'", auto_fixable=False))

        # versionInfo format
        version = ont.get("owl:versionInfo", "")
        if not re.match(r"^\d+\.\d+\.\d+$", str(version)):
            self.issues.append(Issue("ERROR", "ONT004",
                f"owl:versionInfo not semver: '{version}'", auto_fixable=False))

        # m3:ontologyType
        if "m3:ontologyType" not in ont:
            self.issues.append(Issue("ERROR", "ONT005",
                "m3:ontologyType missing from owl:Ontology node",
                fix="Add m3:ontologyType", auto_fixable=False))

        # owl:imports must not reference GenesisSpace
        imports = ont.get("owl:imports", [])
        if isinstance(imports, str):
            imports = [imports]
        for imp in imports:
            if GENESIS_SPACE in str(imp):
                self.issues.append(Issue("ERROR", "ONT006",
                    f"owl:imports references M3_GenesisSpace: {imp}",
                    fix="Replace with M3_GenesisGrammar.jsonld",
                    auto_fixable=True))

        # m2:changelog format (should be array)
        changelog = ont.get("m2:changelog")
        if changelog is not None and not isinstance(changelog, list):
            self.issues.append(Issue("WARNING", "ONT007",
                "m2:changelog should be an array of objects [{version, date, changes}]",
                auto_fixable=False))

    def check_generic_concept_combos(self):
        graph = self.data.get("@graph", [])
        for node in graph:
            ntype = node.get("@type", [])
            if isinstance(ntype, str):
                ntype = [ntype]
            # Exact match on type — avoid substring issues
            if "m2:GenericConceptCombo" not in ntype:
                continue
            nid = node.get("@id", "?")

            # rdfs:subClassOf
            subclass = node.get("rdfs:subClassOf")
            if subclass is None:
                self.issues.append(Issue("ERROR", "GCC001",
                    f"GenericConceptCombo missing rdfs:subClassOf: {nid}",
                    fix="Add rdfs:subClassOf: m2:GenericConceptCombo",
                    auto_fixable=False))

            # structuralGrammarFormula
            formula = node.get("m1:structuralGrammarFormula", "")
            if not formula:
                self.issues.append(Issue("WARNING", "GCC002",
                    f"GenericConceptCombo missing m1:structuralGrammarFormula: {nid}",
                    auto_fixable=False))
            elif not re.match(r"^Fm2[²]?\(", formula):
                self.issues.append(Issue("WARNING", "GCC003",
                    f"GenericConceptCombo formula not Fm2(...): {nid} → {formula[:50]}",
                    auto_fixable=False))

            # No ⊗
            if "⊗" in formula:
                self.issues.append(Issue("ERROR", "GCC004",
                    f"⊗ tensor notation in formula: {nid}",
                    fix="Replace ⊗ with × / + / |", auto_fixable=True))

    def check_kfcc_nodes(self):
        graph = self.data.get("@graph", [])
        for node in graph:
            ntype = node.get("@type", [])
            if isinstance(ntype, str):
                ntype = [ntype]
            # Exact match — avoid substring match with KnowledgeFieldConceptCombo
            if "m2:KnowledgeFieldConceptCombo" not in ntype:
                continue
            nid = node.get("@id", "?")

            # rdfs:subClassOf → must CONTAIN m2:KnowledgeFieldConceptCombo
            # (may be string OR array if node also has semantic domain subClassOf)
            subclass = node.get("rdfs:subClassOf")
            if subclass is None:
                self.issues.append(Issue("ERROR", "KFCC001",
                    f"KFCC missing rdfs:subClassOf: {nid}",
                    fix="Add m2:KnowledgeFieldConceptCombo to rdfs:subClassOf",
                    auto_fixable=True))
            else:
                # Normalize to list for uniform check
                sub_list = subclass if isinstance(subclass, list) else [subclass]
                sub_vals = [s.get("@id", s) if isinstance(s, dict) else s for s in sub_list]
                if not any("KnowledgeFieldConceptCombo" in str(v) for v in sub_vals):
                    self.issues.append(Issue("ERROR", "KFCC001b",
                        f"KFCC rdfs:subClassOf does not include m2:KnowledgeFieldConceptCombo: {nid}",
                        fix="Add m2:KnowledgeFieldConceptCombo to rdfs:subClassOf array",
                        auto_fixable=True))

            # NOTE: m2:knowledgeField is NOT a defined M2 property.
            # The KFCC is identified by @type + rdfs:subClassOf only.

            # structuralGrammarFormula
            formula = node.get("m1:structuralGrammarFormula", "")
            if not formula:
                self.issues.append(Issue("WARNING", "KFCC003",
                    f"KFCC missing m1:structuralGrammarFormula: {nid}",
                    auto_fixable=False))
            elif not re.match(r"^Fm1m2\(", formula):
                self.issues.append(Issue("WARNING", "KFCC004",
                    f"KFCC formula not Fm1m2(...): {nid} → {formula[:50]}",
                    auto_fixable=False))

            # No ⊗
            if "⊗" in formula:
                self.issues.append(Issue("ERROR", "KFCC005",
                    f"⊗ tensor notation in formula: {nid}",
                    fix="Replace ⊗ with × / + / |", auto_fixable=True))

    def check_forbidden_patterns(self):
        """Check forbidden patterns as JSON property KEYS (not text content)."""

        # Collect all property keys used in the document (recursive)
        def collect_keys(obj):
            keys = set()
            if isinstance(obj, dict):
                for k, v in obj.items():
                    keys.add(k)
                    keys.update(collect_keys(v))
            elif isinstance(obj, list):
                for item in obj:
                    keys.update(collect_keys(item))
            return keys

        all_keys = collect_keys(self.data)
        content_str = json.dumps(self.data)

        # Check forbidden property keys
        forbidden_keys = {
            "m2:characterizedBy": "deprecated — use m1:structuralGrammarFormula",
            "m2:hasTensorFormula": "obsolete — use m1:structuralGrammarFormula",
            "asfidSignature":      "deprecated — use m1:structuralGrammarFormula",
        }
        for key, reason in forbidden_keys.items():
            if key in all_keys:
                self.issues.append(Issue("ERROR", "FRBDN001",
                    f"Forbidden property key '{key}': {reason}",
                    fix=f"Remove '{key}'", auto_fixable=False))

        # tensorFormula as a KEY (not in string values/changelog)
        tensor_keys = [k for k in all_keys if "tensorFormula" in k
                       and k != "m1:structuralGrammarFormula"]
        for k in tensor_keys:
            self.issues.append(Issue("ERROR", "FRBDN001",
                f"Forbidden property key '{k}' (tensorFormula) — use m1:structuralGrammarFormula",
                auto_fixable=False))

        # m1core: as a prefix in keys
        m1core_keys = [k for k in all_keys if k.startswith("m1core:")]
        for k in m1core_keys:
            self.issues.append(Issue("ERROR", "FRBDN003",
                f"Deprecated namespace key '{k}' — use m1:",
                fix="Replace m1core: with m1:", auto_fixable=True))

        # ORIVE as a value/text (should be REVOI)
        if '"ORIVE"' in content_str or "'ORIVE'" in content_str or ":ORIVE" in content_str:
            self.issues.append(Issue("ERROR", "FRBDN002",
                "ORIVE terminology found — use REVOI",
                fix="Replace ORIVE with REVOI", auto_fixable=True))

        # GenesisSpace in URIs (not just text)
        if GENESIS_SPACE in content_str:
            # Check if it's in a URI context (not just a comment mentioning it)
            import re as _re
            if _re.search(rf'["\'].*{re.escape(GENESIS_SPACE)}.*["\']', content_str):
                self.issues.append(Issue("ERROR", "FRBDN004",
                    f"M3_GenesisSpace URI found (obsolete)",
                    fix="Replace with M3_GenesisGrammar", auto_fixable=True))

        # ⊗ as value in any string
        if "⊗" in content_str:
            self.issues.append(Issue("ERROR", "FRBDN005",
                "⊗ tensor notation found in file",
                fix="Replace ⊗ with × / + / |", auto_fixable=False))

    def check_namespace_convention(self):
        """Extension files must use m1:extension:<domain>: namespace pattern."""
        fname = self.path.name
        if fname in ("M1_CoreConcepts.jsonld", "M1_Domains.jsonld"):
            return

        ctx = self.data.get("@context", {})
        # Check that no old-style dot namespaces exist (m1.ext:)
        for key in ctx:
            if "m1.ext" in key or ("m1:" in key and key not in
                    ("m1:extension:biology", "m1:extension:chemistry",
                     "m1:extension:economics", "m1:extension:education",
                     "m1:extension:electronics", "m1:extension:energy_generators",
                     "m1:extension:geology", "m1:extension:music",
                     "m1:extension:mythology", "m1:extension:optics",
                     "m1:extension:photography", "m1:extension:physics",
                     "m1:extension:systemic_modeling", "m1:extension:political_science",
                     "m1:extension:philosophy", "m1:extension:education")):
                if "m1:extension:" not in key and key.startswith("m1:"):
                    self.issues.append(Issue("WARNING", "NS001",
                        f"Possible non-standard prefix key in @context: '{key}'",
                        auto_fixable=False))

    # ── Auto-fixes (mutating) ─────────────────────────────────────────────────
    def fix_crlf(self):
        raw = self.path.read_bytes()
        if b"\r\n" in raw:
            self.path.write_bytes(raw.replace(b"\r\n", b"\n"))
            with open(self.path, "r", encoding="utf-8") as f:
                self.content = f.read()
            self.data = json.loads(self.content)
            return True
        return False

    def fix_genesis_space(self):
        """Replace M3_GenesisSpace with M3_GenesisGrammar everywhere."""
        if GENESIS_SPACE not in self.content:
            return False
        self.content = self.content.replace(GENESIS_SPACE, GENESIS_GRAMMAR)
        self.data = json.loads(self.content)
        self.modified = True
        return True

    def fix_orive(self):
        if "ORIVE" not in self.content:
            return False
        self.content = self.content.replace("ORIVE", "REVOI")
        self.data = json.loads(self.content)
        self.modified = True
        return True

    def fix_m1core_namespace(self):
        if "m1core:" not in self.content:
            return False
        self.content = self.content.replace("m1core:", "m1:")
        self.data = json.loads(self.content)
        self.modified = True
        return True

    def fix_creator(self):
        graph = self.data.get("@graph", [])
        changed = False
        for node in graph:
            if node.get("@type") == "owl:Ontology":
                if node.get("dcterms:creator") != EXPECTED_CREATOR:
                    node["dcterms:creator"] = EXPECTED_CREATOR
                    changed = True
        if changed:
            self.modified = True
        return changed

    def fix_base_url(self):
        ctx = self.data.get("@context", {})
        if ctx.get("@base") != ONTOLOGY_BASE:
            ctx["@base"] = ONTOLOGY_BASE
            self.modified = True
            return True
        return False

    def fix_kfcc_subclassof(self):
        """Add m2:KnowledgeFieldConceptCombo to rdfs:subClassOf of all KFCC nodes."""
        MARKER = "m2:KnowledgeFieldConceptCombo"
        graph = self.data.get("@graph", [])
        count = 0
        for node in graph:
            ntype = node.get("@type", [])
            if isinstance(ntype, str): ntype = [ntype]
            if MARKER not in ntype:
                continue
            sub = node.get("rdfs:subClassOf")
            if sub is None:
                node["rdfs:subClassOf"] = MARKER
                count += 1
            elif isinstance(sub, str):
                if sub != MARKER:
                    node["rdfs:subClassOf"] = [MARKER, sub]
                    count += 1
            elif isinstance(sub, list):
                vals = [s.get("@id", s) if isinstance(s, dict) else s for s in sub]
                if not any("KnowledgeFieldConceptCombo" in str(v) for v in vals):
                    node["rdfs:subClassOf"] = [MARKER] + sub
                    count += 1
        if count:
            self.modified = True
        return count


        changed = False
        graph = self.data.get("@graph", [])
        for node in graph:
            if node.get("@type") == "owl:Ontology":
                imports = node.get("owl:imports", [])
                if isinstance(imports, str):
                    imports = [imports]
                new_imports = []
                for imp in imports:
                    if GENESIS_SPACE in str(imp):
                        new_imp = str(imp).replace(GENESIS_SPACE, GENESIS_GRAMMAR)
                        new_imports.append(new_imp)
                        changed = True
                    else:
                        new_imports.append(imp)
                if changed:
                    node["owl:imports"] = new_imports
        if changed:
            self.modified = True
        return changed

    # ── Run all checks ────────────────────────────────────────────────────────
    def run(self) -> bool:
        """Load, check, optionally fix, save. Returns True if file is clean."""
        if not self.load():
            return False

        # CRLF fix first (before JSON parsing)
        crlf_bytes = b"\r\n" in self.path.read_bytes()
        if crlf_bytes:
            if not self.dry_run:
                self.fix_crlf()
                print(FIX(f"  CRLF → LF"))
            else:
                self.issues.append(Issue("ERROR", "ENC001",
                    "CRLF line endings", fix="Convert to LF", auto_fixable=True))

        # All checks
        self.check_context()
        self.check_ontology_node()
        self.check_generic_concept_combos()
        self.check_kfcc_nodes()
        self.check_forbidden_patterns()
        self.check_namespace_convention()

        # Auto-fixes (if not dry-run)
        if not self.dry_run:
            fixes_applied = []
            if self.fix_genesis_space():
                fixes_applied.append("M3_GenesisSpace → M3_GenesisGrammar")
            if self.fix_orive():
                fixes_applied.append("ORIVE → REVOI")
            if self.fix_m1core_namespace():
                fixes_applied.append("m1core: → m1:")
            if self.fix_creator():
                fixes_applied.append("dcterms:creator corrected")
            if self.fix_base_url():
                fixes_applied.append("@base corrected")
            if self.fix_imports_genesis():
                fixes_applied.append("owl:imports GenesisSpace → GenesisGrammar")
            n = self.fix_kfcc_subclassof()
            if n:
                fixes_applied.append(f"rdfs:subClassOf += m2:KnowledgeFieldConceptCombo ({n} nodes)")

            for fix_msg in fixes_applied:
                print(FIX(f"  {fix_msg}"))

            self.save()

        return len([i for i in self.issues if i.severity == "ERROR"]) == 0

# ── SHACL validation ──────────────────────────────────────────────────────────
def run_shacl(file_path: Path, shacl_path: Path) -> Tuple[bool, List[str]]:
    try:
        from pyshacl import validate
        conforms, _, results_text = validate(
            str(file_path),
            shacl_graph=str(shacl_path),
            data_graph_format="json-ld",
            shacl_graph_format="turtle",
            inference="none",
        )
        violations = []
        if not conforms:
            for line in results_text.split("\n"):
                if "Message:" in line or "Focus Node:" in line:
                    violations.append(line.strip())
        return conforms, violations
    except ImportError:
        return None, ["pyshacl not installed — run: pip install pyshacl"]
    except Exception as e:
        return False, [f"SHACL error: {e}"]

# ── Report ────────────────────────────────────────────────────────────────────
def save_report(results: list, report_path: Path):
    lines = [
        "TSCG M1 Layer Validation Report",
        f"Generated: {datetime.datetime.now().isoformat()}",
        "=" * 60,
        "",
    ]
    total_errors = total_warnings = 0
    for fname, issues, shacl_ok, shacl_violations in results:
        errors   = [i for i in issues if i.severity == "ERROR"]
        warnings = [i for i in issues if i.severity == "WARNING"]
        total_errors   += len(errors)
        total_warnings += len(warnings)
        status = "✅ CLEAN" if not errors else f"❌ {len(errors)} errors"
        lines.append(f"{'─'*60}")
        lines.append(f"{fname}  [{status}]  {len(warnings)} warnings")
        for issue in issues:
            icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}[issue.severity]
            lines.append(f"  {icon} [{issue.code}] {issue.message}")
            if issue.fix:
                lines.append(f"     → FIX: {issue.fix}")
        if shacl_violations:
            lines.append("  SHACL violations:")
            for v in shacl_violations:
                lines.append(f"    {v}")
        lines.append("")
    lines.append("=" * 60)
    lines.append(f"TOTAL: {total_errors} errors, {total_warnings} warnings")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(INFO(f"Report saved: {report_path}"))

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    global USE_COLOR

    parser = argparse.ArgumentParser(
        description="TSCG M1 Layer Validation & Correction Script v1.0.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--dry-run",  action="store_true",
        help="Show issues without applying corrections")
    parser.add_argument("--file", type=str, metavar="PATH",
        help="Validate/fix a single M1 file")
    parser.add_argument("--shacl", action="store_true",
        help="Run SHACL validation (requires pyshacl)")
    parser.add_argument("--report", action="store_true",
        help="Save validation report to check_M1_report.txt")
    parser.add_argument("--no-color", action="store_true",
        help="Disable colored output")
    parser.add_argument("-v", "--verbose", action="store_true",
        help="Show all checks including passed ones")
    args = parser.parse_args()

    if args.no_color:
        USE_COLOR = False

    # Resolve script directory (SHACL lives next to this script)
    script_dir = Path(__file__).parent
    shacl_path = script_dir / "M1_Schema.shacl.ttl"

    # Determine files to process
    if args.file:
        target = Path(args.file)
        if not target.exists():
            # Try relative to script dir
            target = script_dir / args.file
        if not target.exists():
            print(ERR(f"File not found: {args.file}"))
            sys.exit(1)
        files = [target]
    else:
        # Auto-detect: look for ontology/ directory containing M1_CoreConcepts.jsonld
        candidates = [
            script_dir.parent.parent / "ontology",   # cli_tools/check-M1/ → repo/ontology/
            script_dir.parent / "ontology",           # one level up
            Path.cwd() / "ontology",                  # cwd/ontology/
            Path.cwd(),                               # current dir
            script_dir,
        ]
        base_dir = None
        for c in candidates:
            if (c / "M1_CoreConcepts.jsonld").exists():
                base_dir = c
                break
        if base_dir is None:
            print(ERR("Cannot find M1_CoreConcepts.jsonld. Run from repo root or use --file."))
            print(INFO("  Expected location: <repo>/ontology/M1_CoreConcepts.jsonld"))
            sys.exit(1)

        print(INFO(f"  Ontology base: {base_dir}\n"))
        files = []
        missing = []
        for fname, relpath in M1_FILES.items():
            full = base_dir / relpath
            if full.exists():
                files.append(full)
            else:
                missing.append(f"{fname} ({relpath})")
        if missing:
            for m in missing:
                print(WARN(f"Not found (skipped): {m}"))

    # Header
    mode = "DRY-RUN" if args.dry_run else "VALIDATION + AUTO-FIX"
    print(HDR(f"\n{'='*60}"))
    print(HDR(f"  TSCG M1 Layer Check — {mode}"))
    print(HDR(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"))
    print(HDR(f"{'='*60}\n"))

    results = []
    all_clean = True

    for fpath in files:
        print(HDR(f"\n── {fpath.name} " + "─" * max(0, 50 - len(fpath.name))))
        checker = M1Checker(fpath, dry_run=args.dry_run, verbose=args.verbose)
        clean = checker.run()

        # Print issues
        errors   = [i for i in checker.issues if i.severity == "ERROR"]
        warnings = [i for i in checker.issues if i.severity == "WARNING"]
        infos    = [i for i in checker.issues if i.severity == "INFO"]

        if not errors and not warnings:
            if args.verbose:
                print(OK("  All checks passed"))
            else:
                print(OK("  Clean"))
        else:
            for issue in errors:
                print(f"  {issue}")
                if issue.fix:
                    print(INFO(f"      → {issue.fix}"))
            for issue in warnings:
                print(f"  {issue}")
            if args.verbose:
                for issue in infos:
                    print(f"  {issue}")

        # SHACL
        shacl_conforms, shacl_violations = None, []
        if args.shacl:
            if not shacl_path.exists():
                print(WARN(f"  SHACL schema not found: {shacl_path}"))
            else:
                print(INFO("  Running SHACL validation..."))
                shacl_conforms, shacl_violations = run_shacl(fpath, shacl_path)
                if shacl_conforms is True:
                    print(OK("  SHACL: conforms"))
                elif shacl_conforms is False:
                    print(ERR(f"  SHACL: {len(shacl_violations)} violations"))
                    for v in shacl_violations[:10]:
                        print(f"    {v}")
                else:
                    for v in shacl_violations:
                        print(WARN(f"  {v}"))

        # Summary line
        e_str = f"{len(errors)} error(s)" if errors else ""
        w_str = f"{len(warnings)} warning(s)" if warnings else ""
        summary = ", ".join(filter(None, [e_str, w_str])) or "clean"
        print(INFO(f"  → {summary}"))

        if errors:
            all_clean = False

        results.append((fpath.name, checker.issues, shacl_conforms, shacl_violations))

    # Global summary
    total_e = sum(len([i for i in r[1] if i.severity=="ERROR"])   for r in results)
    total_w = sum(len([i for i in r[1] if i.severity=="WARNING"]) for r in results)
    print(HDR(f"\n{'='*60}"))
    print(HDR(f"  SUMMARY: {len(results)} files | {total_e} errors | {total_w} warnings"))
    if args.dry_run:
        print(INFO("  DRY-RUN: no files were modified"))
    print(HDR(f"{'='*60}\n"))

    if args.report:
        report_path = script_dir / "check_M1_report.txt"
        save_report(results, report_path)

    sys.exit(0 if all_clean else 1)


if __name__ == "__main__":
    main()
