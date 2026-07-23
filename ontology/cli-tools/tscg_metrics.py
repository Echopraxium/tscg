#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tscg_metrics.py — TSCG corpus metric board (deterministic gauges).

Author : Echopraxium with the collaboration of Claude AI
Version: 1.0.0
Project: TSCG (Transdisciplinary System Construction Game)

WHAT THIS IS
    A read-only measuring instrument. It counts, it never edits.
    Each gauge is a worksite's progress counter: when a worksite ships, its
    gauge reaches its target (usually 0).

WHAT THIS IS NOT
    Not a validator (no SHACL conformance verdict, no golden gate) and not a
    fixer. It is the metric front-end that M0_TscgOntologyValidator will absorb.
    Semantic judgement stays with the human: this tool answers "how many?",
    never "is it right?".

USAGE
    python tscg_metrics.py                      # measure ./ontology (auto-detect)
    python tscg_metrics.py --root path/to/ontology
    python tscg_metrics.py --json               # machine-readable
    python tscg_metrics.py --baseline b.json    # compare against a snapshot
    python tscg_metrics.py --save b.json        # write a snapshot
    python tscg_metrics.py --shacl              # add the SC-1 combo gauge (needs pyshacl)

AUTHORITY REMINDER
    Run this against a checkout of `git HEAD`, never against a stale snapshot.
    Any count produced from a working copy is provisional.
"""

import argparse
import collections
import datetime
import json
import os
import re
import sys

VERSION = "1.0.0"

# --------------------------------------------------------------------------
# Canonical file selection
# --------------------------------------------------------------------------
# Excluded: archives, docs copies, reference snapshots, private prototypes,
# per-instance static duplicates, migration backups, and templates. These are
# copies or scratch space; counting them inflates every gauge (a lesson learned
# the hard way — three manual censuses produced three different numbers).
EXCLUDED_PATH_MARKERS = (
    "/_archives/", "/docs/", "/tools/", "_protos", "/static/",
    "migration_backups", "domain_format_fix", "POCLET_TEMPLATE",
    "_Ref", "/Ref/",
)

JSONLD_KEYWORDS = {
    "@id", "@type", "@context", "@graph", "@base", "@vocab", "@value",
    "@language", "@list", "@set", "@none", "@container", "@reverse",
    "@index", "@json", "@nest", "@prefix", "@version", "@protected",
}

# Bare keys that have a well-established standard equivalent (VOC family A).
# Verified 2026-07-22 by semantics AND typing, not by name.
STANDARD_REPLACEABLE = {
    "description": "dcterms:description",
    "examples": "skos:example",
    "example": "skos:example",
    "name": "rdfs:label",
    "label": "rdfs:label",
    "alternative_names": "skos:altLabel",
    "comment": "rdfs:comment",
    "note": "skos:note",
    "rationale": "skos:note",
    "definition": "skos:definition",
    "date": "dcterms:date",
    "version": "owl:versionInfo",
    "title": "dcterms:title",
    "source": "dcterms:source",
    "created": "dcterms:created",
    "modified": "dcterms:modified",
}

# NOT false friends — same name, incompatible semantics. Do NOT map these.
#   status -> adms:status is workflow state (range skos:Concept); TSCG status is
#             an epistemic string ("PROPOSITION"/"VALIDATED").
#   role   -> prov:hadRole is an agent's role in an activity; TSCG role is a
#             primitive's role in a formula.
FALSE_FRIENDS = {"status", "role"}

# Retired D8 serialisation triad (DUP-1). Matched WITH OR WITHOUT an mN prefix:
# the corpus writes "m1:structuralGrammarFormulaRawText", and a prefix-blind
# pattern silently reported 0 — a false negative caught on 2026-07-22.
D8_TRIAD = (
    "structuralGrammarFormulaExpanded",
    "structuralGrammarFormulaTeX",
    "structuralGrammarFormulaRawText",
)

MONOIDAL_OPERATORS = "\u00d7+|\u2297"          # × + | ⊗
TENSOR_OP = "\u2297"                            # ⊗ (retired 2026-07-06)
BARE_SI = re.compile(r"(?<![A-Za-z_])[SI](?![A-Za-z0-9_])")


def is_canonical(path):
    p = path.replace("\\", "/")
    if not p.endswith(".jsonld"):
        return False
    return not any(marker in p for marker in EXCLUDED_PATH_MARKERS)


def layer_of(path):
    m = re.match(r"M([0-3])_", os.path.basename(path))
    return "M" + m.group(1) if m else "M?"


def iter_canonical_files(root):
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            if is_canonical(full):
                yield full


def walk_keys(node, callback, depth=0):
    """Visit every (key, value) pair in a JSON-LD document."""
    if isinstance(node, dict):
        for key, value in node.items():
            callback(key, value, depth)
            walk_keys(value, callback, depth + 1)
    elif isinstance(node, list):
        for item in node:
            walk_keys(item, callback, depth)


def measure(root):
    files = sorted(iter_canonical_files(root))

    M = {
        "_meta": {
            "tool": "tscg_metrics.py",
            "tool_version": VERSION,
            "snapshot_date": datetime.date.today().isoformat(),
            "root": os.path.abspath(root),
            "canonical_files": len(files),
        },
        # VOC — vocabulary hygiene
        "VOC_bare_keys_occurrences": 0,
        "VOC_bare_keys_distinct": 0,
        "VOC_bare_standard_replaceable": 0,
        "VOC_bare_false_friends": 0,
        "VOC_prefixed_but_undefined": 0,
        # CTX — @context / IRI resolution
        "CTX1_undeclared_prefix": 0,
        "CTX4_relative_mN_prefix_files": 0,
        "CTX5_term_name_with_colon": 0,
        # FRB — retired formalism
        "FRB1_tensor_operator": 0,
        "FRB2_legacy_arrow": 0,
        # DUP — retired duplicates
        "DUP1_D8_triad": 0,
        # NOT — notation
        "NOT1_bare_SI_in_atom_formula": 0,
        # STR — structural / cross-file
        "STR_layer_inversion": 0,
        "STR_changelog_forms": {},
        # breakdowns
        "by_layer_bare_keys": {},
        "top_bare_keys": {},
    }

    bare_counter = collections.Counter()
    by_layer = collections.Counter()
    changelog_forms = collections.Counter()

    for path in files:
        layer = layer_of(path)
        layer_num = int(layer[1]) if layer[1].isdigit() else 9
        try:
            raw = open(path, encoding="utf-8").read()
            doc = json.loads(raw)
        except Exception:
            continue

        ctx = doc.get("@context", {})
        ctx = ctx if isinstance(ctx, dict) else {}
        declared_prefixes = {
            k for k, v in ctx.items()
            if isinstance(v, str) and not k.startswith("@")
        }
        declared_terms = set(ctx.keys())

        # --- CTX-4 / CTX-5 (on the @context itself) -----------------------
        for term, value in ctx.items():
            if term in ("m0", "m1", "m2", "m3"):
                if isinstance(value, str) and not value.startswith("http"):
                    M["CTX4_relative_mN_prefix_files"] += 1
            if ":" in term and not term.startswith("@"):
                M["CTX5_term_name_with_colon"] += 1

        # --- FRB (skip changelog prose: a mention in history is not a defect)
        for line in raw.splitlines():
            if '"changes"' in line or "changelog" in line:
                continue
            M["FRB1_tensor_operator"] += line.count(TENSOR_OP)
            M["FRB2_legacy_arrow"] += line.count("\u2297\u21d2") + line.count("(x)=>")

        # --- DUP-1 (prefix-tolerant) --------------------------------------
        for term in D8_TRIAD:
            M["DUP1_D8_triad"] += len(
                re.findall(r'"(?:m[0-3]:)?%s"' % re.escape(term), raw)
            )

        # --- changelog forms ----------------------------------------------
        for form in ("m0:changelog", "m1:changelog", "m2:changelog", "m3:changelog"):
            if re.search(r'"%s"\s*:' % form, raw):
                changelog_forms[form] += 1
        if re.search(r'"changelog"\s*:', raw):
            changelog_forms["metadata.changelog (bare)"] += 1

        # --- properties actually DEFINED in this file ----------------------
        graph = doc.get("@graph", [])
        defined_properties = set()
        if isinstance(graph, list):
            for node in graph:
                if isinstance(node, dict) and "Property" in json.dumps(node.get("@type", "")):
                    defined_properties.add(node.get("@id", ""))

        used_prefixed = set()

        def visit(key, _value, _depth):
            if key in JSONLD_KEYWORDS or key.startswith("@"):
                return
            if ":" in key and not key.startswith("http"):
                prefix = key.split(":", 1)[0]
                if prefix in ("m0", "m1", "m2", "m3"):
                    used_prefixed.add(key)
                    if int(prefix[1]) < layer_num:
                        M["STR_layer_inversion"] += 1
                elif prefix not in declared_prefixes and key not in declared_terms:
                    M["CTX1_undeclared_prefix"] += 1
            elif ":" not in key and key not in declared_terms:
                M["VOC_bare_keys_occurrences"] += 1
                bare_counter[key] += 1
                by_layer[layer] += 1
                if key in STANDARD_REPLACEABLE:
                    M["VOC_bare_standard_replaceable"] += 1
                if key in FALSE_FRIENDS:
                    M["VOC_bare_false_friends"] += 1

        walk_keys(doc.get("@graph", doc), visit)

        # VOC/B1 — prefixed key used but no owl:*Property definition anywhere
        # in this file. (Cross-file definitions are resolved by the validator;
        # here it is a per-file signal, deliberately conservative.)
        for key in used_prefixed:
            if key not in defined_properties:
                M["VOC_prefixed_but_undefined"] += 1

        # --- NOT-1 — bare S/I in ATOM formulas only ------------------------
        # Atom formulas live in m2:hasStructuralGrammarFormula.
        # Combo signatures (m1:structuralGrammarFormula) are NOT in scope:
        # subscripts do not apply to function arguments.
        def visit_formula(key, value, _depth):
            if key.endswith("hasStructuralGrammarFormula") and isinstance(value, str):
                if BARE_SI.search(value):
                    M["NOT1_bare_SI_in_atom_formula"] += 1

        walk_keys(doc.get("@graph", doc), visit_formula)

    M["VOC_bare_keys_distinct"] = len(bare_counter)
    M["by_layer_bare_keys"] = dict(sorted(by_layer.items()))
    M["STR_changelog_forms"] = dict(changelog_forms)
    M["top_bare_keys"] = dict(bare_counter.most_common(25))
    return M


def measure_sc1_combos(root, shacl_path=None):
    """Optional gauge: SC-1 violations on combo signatures (needs pyshacl).

    Counts violations of the three SC-1 rules:
      1. no monoidal operator inside a signature
      2. no bare primitive as an argument
      3. arity: Fm2 >= 2 concepts ; Fm1m2 >= 1 Domain AND >= 1 GenericConcept
    """
    try:
        from rdflib import Graph
        from pyshacl import validate
    except ImportError:
        return {"available": False, "reason": "rdflib/pyshacl not installed"}

    if shacl_path is None:
        shacl_path = os.path.join(root, "cli-tools", "check-M1", "M1_Schema_shacl.ttl")
    if not os.path.exists(shacl_path):
        return {"available": False, "reason": "SHACL not found: %s" % shacl_path}

    import warnings
    warnings.filterwarnings("ignore")

    shapes = Graph()
    shapes.parse(shacl_path, format="turtle")

    total = 0
    per_file = {}
    for path in sorted(iter_canonical_files(root)):
        base = os.path.basename(path)
        if not base.startswith("M1_"):
            continue
        try:
            data = Graph()
            data.parse(path, format="json-ld")
            _c, _g, text = validate(data, shacl_graph=shapes,
                                    advanced=True, inference="none")
        except Exception:
            continue
        hits = len([m for m in re.findall(r"Message: (.{0,60})", text)
                    if "(SC-1)" in m])
        if hits:
            per_file[base.replace(".jsonld", "")] = hits
            total += hits
    return {"available": True, "SC1_combo_violations": total, "per_file": per_file}


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------
GAUGES = [
    ("VOC", "bare keys (occurrences)",        "VOC_bare_keys_occurrences",      "0"),
    ("VOC", "bare keys (distinct)",           "VOC_bare_keys_distinct",         "0"),
    ("VOC", "  of which standard-replaceable","VOC_bare_standard_replaceable",  "-"),
    ("VOC", "  of which false friends",       "VOC_bare_false_friends",         "-"),
    ("VOC", "prefixed but undefined (B1)",    "VOC_prefixed_but_undefined",     "0"),
    ("CTX", "undeclared prefix (CTX-1)",      "CTX1_undeclared_prefix",         "0"),
    ("CTX", "relative mN prefix (CTX-4)",     "CTX4_relative_mN_prefix_files",  "0"),
    ("CTX", "term name with ':' (CTX-5)",     "CTX5_term_name_with_colon",      "0"),
    ("FRB", "tensor operator (live)",         "FRB1_tensor_operator",           "0"),
    ("FRB", "legacy arrow",                   "FRB2_legacy_arrow",              "0"),
    ("DUP", "retired D8 triad",               "DUP1_D8_triad",                  "0"),
    ("NOT", "bare S/I in atom formula (SC-2)","NOT1_bare_SI_in_atom_formula",   "0"),
    ("STR", "layer inversion",                "STR_layer_inversion",            "0"),
]


def render(M, baseline=None, sc1=None):
    meta = M["_meta"]
    out = []
    out.append("=" * 68)
    out.append("TSCG METRIC BOARD  —  %s  (tool v%s)" % (meta["snapshot_date"], meta["tool_version"]))
    out.append("canonical files: %d   root: %s" % (meta["canonical_files"], meta["root"]))
    out.append("=" * 68)
    out.append("%-5s %-34s %8s %8s %7s" % ("FAM", "GAUGE", "VALUE", "TARGET", "DELTA"))
    out.append("-" * 68)
    for family, label, key, target in GAUGES:
        value = M.get(key, 0)
        delta = ""
        if baseline is not None and key in baseline:
            d = value - baseline[key]
            delta = "%+d" % d if d else "="
        out.append("%-5s %-34s %8s %8s %7s" % (family, label, value, target, delta))
    if sc1 and sc1.get("available"):
        value = sc1["SC1_combo_violations"]
        out.append("%-5s %-34s %8s %8s %7s" % ("SC-1", "combo signature violations", value, "0", ""))
    out.append("-" * 68)
    out.append("bare keys by layer : %s" % M.get("by_layer_bare_keys"))
    out.append("changelog forms    : %s" % M.get("STR_changelog_forms"))
    if sc1 and sc1.get("available") and sc1.get("per_file"):
        worst = sorted(sc1["per_file"].items(), key=lambda kv: -kv[1])[:6]
        out.append("SC-1 worst files   : %s" % ", ".join("%s(%d)" % kv for kv in worst))
    return "\n".join(out)


def autodetect_root():
    for candidate in (".", "./ontology", "..", "../ontology"):
        if os.path.isdir(os.path.join(candidate, "M1_extensions")):
            return candidate
        if os.path.exists(os.path.join(candidate, "M2_GenericConcepts.jsonld")):
            return candidate
    return "."


def main():
    ap = argparse.ArgumentParser(description="TSCG corpus metric board")
    ap.add_argument("--root", default=None, help="ontology/ directory (auto-detected by default)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--baseline", help="compare against a saved snapshot")
    ap.add_argument("--save", help="write the snapshot to this file")
    ap.add_argument("--shacl", action="store_true", help="add the SC-1 combo gauge (needs pyshacl)")
    ap.add_argument("--shacl-path", default=None, help="explicit path to M1_Schema_shacl.ttl")
    args = ap.parse_args()

    root = args.root or autodetect_root()
    if not os.path.isdir(root):
        print("ERROR: root not found: %s" % root, file=sys.stderr)
        return 2

    M = measure(root)
    sc1 = measure_sc1_combos(root, args.shacl_path) if args.shacl else None
    if sc1 and sc1.get("available"):
        M["SC1_combo_violations"] = sc1["SC1_combo_violations"]
        M["SC1_per_file"] = sc1["per_file"]

    baseline = None
    if args.baseline:
        try:
            baseline = json.load(open(args.baseline, encoding="utf-8"))
        except Exception as exc:
            print("WARNING: could not read baseline (%s)" % exc, file=sys.stderr)

    if args.save:
        with open(args.save, "w", encoding="utf-8") as fh:
            json.dump(M, fh, indent=2, ensure_ascii=False)

    if args.json:
        print(json.dumps(M, indent=2, ensure_ascii=False))
    else:
        print(render(M, baseline, sc1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
