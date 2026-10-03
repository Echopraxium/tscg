#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tscg_metrics.py — TSCG corpus metric board (deterministic gauges).

Author : Echopraxium with the collaboration of Claude AI
Version: 1.4.0
Project: TSCG (Transdisciplinary System Construction Game)

CHANGELOG
    1.4.0 (2026-10-03) — WS-5 / WS-2 lot CTX-5. Two gauges redefined (keys
        kept for baseline compatibility):
        CTX4_relative_mN_prefix_files — now counts ANY @context term whose
            IRI mapping (string or {"@id"}) has no scheme, not only m0..m3.
            JSON-LD never resolves a term mapping against @base: rdflib
            leaves the IRI relative and pyld rejects the file. Found by
            'm1core': 'M1_CoreConcepts.jsonld#' (M1_Economics), invisible to
            the old m0..m3-only test. Target 0.
        CTX5_term_name_with_colon — a compact-IRI term name now counts only
            when it does NOT map to its own expansion (JSON-LD 1.1 §4.1.2).
            Pure type coercions ("rdfs:range": {"@type": "@id"}) and terms
            whose @id equals prefix-expansion + local name are legal and no
            longer counted (5 such terms on 2026-10-03). Target 0.
    1.3.0 (2026-09-30) — WS-1 lot 1i. New gauge STR_imports_literal: number
        of owl:imports values written as plain strings. A string is a
        JSON-LD literal, so no reasoner follows the import; the target
        form is an IRI {"@id": ...}. Target 0.
    1.2.0 (2026-09-30) — WS-1 lot 1h. Two graph-based gauges (need rdflib;
        shown as n/a without it, like SC-1 without pyshacl):
        EXT1_standard_term_undeclared — a real external term (DCMI, SKOS,
            ADMS, schema.org…) or an OWL 2 built-in annotation property,
            used as a predicate or as an rdf:type object in the canonical
            graph, but not declared in the apex M3_GrammarFoundation.
            Target 0 (reached by lot 1h).
        EXT2_nonterm_in_standard_namespace — an IRI in a standard
            namespace that is not a term of it (e.g. the owl:<key>
            minted by '@vocab': owl#, dcterms:documentation, a datatype
            used as a class). Target 0 (reached by B1/B2/vestiges).
        The OWL 2 reserved AXIOM vocabulary (rdf:type, rdfs:subClassOf,
        owl:imports, owl:Class…) is the language itself and is never
        counted: OWL 2 Structural Specification §5.1-§5.6 forbid
        declaring it. Counts are DISTINCT TERMS, measured on the parsed
        graph (what a reasoner sees), not on the JSON text.
    1.1.0 (2026-07-24) — WS-0/SC-2. Gauge renamed
        NOT1_bare_SI_in_atom_formula -> NOT1_bare_SI_in_monoidal_formula.
        'atom' carried three senses in this corpus: the GENERATOR sense that
        M3_GenesisGrammar defines ('MonoidalTypes are the atomic, irreducible
        elements'), the non-combo sense used here, and the domain sense in
        M1_Chemistry. Only the second was wrong. Verified: the old key appears
        in NO golden_values.json entry, so no reference breaks — but a local
        baseline.json saved with --save will show one gauge gone and one new.
        The ban on 'atom' is a TOOLING constraint (forbidden_in: metric_names),
        never a corpus-wide ban: M1_Chemistry's domain prose is legitimate.

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

VERSION = "1.4.0"

# --------------------------------------------------------------------------
# Canonical file selection
# --------------------------------------------------------------------------
# Excluded: archives, docs copies, reference snapshots, private prototypes,
# per-instance static duplicates, migration backups, and templates. These are
# copies or scratch space; counting them inflates every gauge (a lesson learned
# the hard way — three manual censuses produced three different numbers).
EXCLUDED_PATH_MARKERS = (
    "/_archives/", "/docs/", "/ref_tool_links/", "_protos", "/static/",
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
ABSOLUTE_IRI = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")   # has a scheme
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
        "NOT1_bare_SI_in_monoidal_formula": 0,
        # STR — structural / cross-file
        "STR_layer_inversion": 0,
        "STR_changelog_forms": {},
        "STR_imports_literal": 0,
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
            if term.startswith("@"):
                continue
            iri = value if isinstance(value, str) else (
                value.get("@id") if isinstance(value, dict) else None)
            # CTX-4: any term whose IRI mapping is relative (no scheme).
            # JSON-LD 1.1 never resolves a term mapping against @base: rdflib
            # leaves it relative, pyld rejects the file.
            if isinstance(iri, str) and not iri.startswith("@") \
                    and not ABSOLUTE_IRI.match(iri):
                M["CTX4_relative_mN_prefix_files"] += 1
            # CTX-5: a term in the form of a compact IRI is legal only when it
            # maps to its own expansion (JSON-LD 1.1 §4.1.2): no @id at all
            # (a type coercion such as "rdfs:range": {"@type": "@id"}), or an
            # @id equal to prefix-expansion + local name.
            if ":" in term:
                prefix, local = term.split(":", 1)
                expansion = ctx.get(prefix)
                expansion = expansion if isinstance(expansion, str) else (
                    expansion.get("@id") if isinstance(expansion, dict) else None)
                own = (expansion + local) if isinstance(expansion, str) else None
                if iri is not None and iri != own:
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

        # --- STR — owl:imports written as strings (literals) ---------------
        def visit_imports(key, value, _depth):
            if key == "owl:imports":
                values = value if isinstance(value, list) else [value]
                M["STR_imports_literal"] += sum(isinstance(v, str) for v in values)

        walk_keys(doc, visit_imports)

        # VOC/B1 — prefixed key used but no owl:*Property definition anywhere
        # in this file. (Cross-file definitions are resolved by the validator;
        # here it is a per-file signal, deliberately conservative.)
        for key in used_prefixed:
            if key not in defined_properties:
                M["VOC_prefixed_but_undefined"] += 1

        # --- NOT-1 — bare S/I in MONOIDAL formulas only ------------------------
        # Monoidal formulas live in m2:hasStructuralGrammarFormula.
        # Combo signatures (m1:structuralGrammarFormula) are NOT in scope:
        # subscripts do not apply to function arguments.
        def visit_formula(key, value, _depth):
            if key.endswith("hasStructuralGrammarFormula") and isinstance(value, str):
                if BARE_SI.search(value):
                    M["NOT1_bare_SI_in_monoidal_formula"] += 1

        walk_keys(doc.get("@graph", doc), visit_formula)

    M["VOC_bare_keys_distinct"] = len(bare_counter)
    M["by_layer_bare_keys"] = dict(sorted(by_layer.items()))
    M["STR_changelog_forms"] = dict(changelog_forms)
    M["top_bare_keys"] = dict(bare_counter.most_common(25))
    return M


# --------------------------------------------------------------------------
# EXT — external terms (WS-1 lot 1h). Graph-based: needs rdflib.
# --------------------------------------------------------------------------
TSCG_BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/"
APEX_FILE = "M3_GrammarFoundation.jsonld"
NS_RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_RDFS = "http://www.w3.org/2000/01/rdf-schema#"
NS_OWL = "http://www.w3.org/2002/07/owl#"
NS_XSD = "http://www.w3.org/2001/XMLSchema#"
RESERVED_NS = (NS_RDF, NS_RDFS, NS_OWL, NS_XSD)

# OWL 2 Structural Specification §5.5 — the only reserved IRIs that MAY be
# declared (as annotation properties). They must be declared in the apex.
BUILTIN_ANNOTATION = {NS_RDFS + t for t in ("label", "comment", "seeAlso", "isDefinedBy")} | \
    {NS_OWL + t for t in ("deprecated", "versionInfo", "priorVersion",
                          "backwardCompatibleWith", "incompatibleWith")}

# The language itself (OWL 2 §5.1-§5.6: MUST NOT be declared). Never counted.
LANGUAGE_VOCAB = {NS_RDF + t for t in ("type", "first", "rest", "nil", "List")} | \
    {NS_RDFS + t for t in ("subClassOf", "subPropertyOf", "domain", "range",
                           "Literal", "Datatype")} | \
    {NS_OWL + t for t in (
        "imports", "versionIRI", "inverseOf", "oneOf", "equivalentClass",
        "equivalentProperty", "disjointWith", "unionOf", "intersectionOf",
        "complementOf", "sameAs", "differentFrom", "members", "distinctMembers",
        "propertyChainAxiom", "propertyDisjointWith", "hasKey", "disjointUnionOf",
        "Thing", "Nothing", "Class", "Ontology", "NamedIndividual",
        "ObjectProperty", "DatatypeProperty", "AnnotationProperty",
        "SymmetricProperty", "AsymmetricProperty", "TransitiveProperty",
        "FunctionalProperty", "InverseFunctionalProperty", "ReflexiveProperty",
        "IrreflexiveProperty", "Restriction", "AllDisjointClasses",
        "AllDifferent", "topObjectProperty", "bottomObjectProperty",
        "topDataProperty", "bottomDataProperty")}

# Restriction vocabulary: language ONLY on a node typed owl:Restriction.
# (Elsewhere, e.g. a bare 'cardinality' key under '@vocab': owl#, it is a
# minted non-term and counts in EXT-2.)
RESTRICTION_VOCAB = {NS_OWL + t for t in (
    "onProperty", "someValuesFrom", "allValuesFrom", "hasValue", "hasSelf",
    "cardinality", "minCardinality", "maxCardinality", "qualifiedCardinality",
    "minQualifiedCardinality", "maxQualifiedCardinality", "onClass",
    "onDataRange")}

DECLARING_TYPES = {NS_OWL + t for t in (
    "AnnotationProperty", "ObjectProperty", "DatatypeProperty", "Class")}


def measure_ext(root):
    """EXT-1 / EXT-2 on the parsed canonical graph. Returns a dict."""
    try:
        import logging
        logging.getLogger("rdflib").setLevel(logging.ERROR)
        from rdflib import Graph, URIRef
        from rdflib.namespace import RDF, OWL, DCTERMS, SKOS
    except ImportError:
        return {"EXT1_standard_term_undeclared": "n/a",
                "EXT2_nonterm_in_standard_namespace": "n/a"}

    # namespaces whose membership rdflib can verify (closed namespaces)
    closed = [(str(RDF), RDF), (NS_RDFS, None), (str(OWL), OWL),
              (str(DCTERMS), DCTERMS), (str(SKOS), SKOS)]

    def is_member(iri):
        from rdflib.namespace import RDFS as _RDFS
        for base, ns in closed:
            if iri.startswith(base):
                ns = ns if ns is not None else _RDFS
                try:
                    ns[iri[len(base):]]
                    return True
                except Exception:
                    return False
        return True     # membership not verifiable (ADMS, schema.org…)

    declared = set()
    used = collections.defaultdict(set)          # iri -> files
    files = sorted(iter_canonical_files(root))
    parse_failures = 0
    for path in files:
        g = Graph()
        try:
            g.parse(path, format="json-ld")
        except Exception:
            parse_failures += 1
            continue
        restrictions = set(g.subjects(RDF.type, OWL.Restriction))
        name = os.path.basename(path)
        for s, p, o in g:
            p = str(p)
            if not (p in RESTRICTION_VOCAB and s in restrictions):
                used[p].add(name)
            if p == str(RDF.type) and isinstance(o, URIRef):
                used[str(o)].add(name)
                if name == APEX_FILE and str(o) in DECLARING_TYPES:
                    declared.add(str(s))

    ext1, ext2 = {}, {}
    for iri, where in used.items():
        if iri.startswith(TSCG_BASE):
            continue
        if iri.startswith(RESERVED_NS):
            if iri in LANGUAGE_VOCAB:
                continue
            if iri in BUILTIN_ANNOTATION:
                if iri not in declared:
                    ext1[iri] = sorted(where)
                continue
            ext2[iri] = sorted(where)               # reserved but not usable
        elif not is_member(iri):
            ext2[iri] = sorted(where)
        elif iri not in declared:
            ext1[iri] = sorted(where)
    return {
        "EXT1_standard_term_undeclared": len(ext1),
        "EXT2_nonterm_in_standard_namespace": len(ext2),
        "EXT_parse_failures": parse_failures,
        "EXT1_terms": dict(sorted(ext1.items())),
        "EXT2_terms": dict(sorted(ext2.items())),
    }


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
    ("CTX", "relative term IRI (CTX-4)",      "CTX4_relative_mN_prefix_files",  "0"),
    ("CTX", "invalid ':' term (CTX-5)",       "CTX5_term_name_with_colon",      "0"),
    ("FRB", "tensor operator (live)",         "FRB1_tensor_operator",           "0"),
    ("FRB", "legacy arrow",                   "FRB2_legacy_arrow",              "0"),
    ("DUP", "retired D8 triad",               "DUP1_D8_triad",                  "0"),
    ("NOT", "bare S/I in monoidal formula (SC-2)","NOT1_bare_SI_in_monoidal_formula",   "0"),
    ("STR", "layer inversion",                "STR_layer_inversion",            "0"),
    ("STR", "owl:imports as string (1i)",     "STR_imports_literal",            "0"),
    ("EXT", "std term undeclared (EXT-1)",    "EXT1_standard_term_undeclared",  "0"),
    ("EXT", "non-term in std ns (EXT-2)",     "EXT2_nonterm_in_standard_namespace", "0"),
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
        if baseline is not None and key in baseline \
                and isinstance(value, int) and isinstance(baseline[key], int):
            d = value - baseline[key]
            delta = "%+d" % d if d else "="
        out.append("%-5s %-34s %8s %8s %7s" % (family, label, value, target, delta))
    if sc1 and sc1.get("available"):
        value = sc1["SC1_combo_violations"]
        out.append("%-5s %-34s %8s %8s %7s" % ("SC-1", "combo signature violations", value, "0", ""))
    out.append("-" * 68)
    out.append("bare keys by layer : %s" % M.get("by_layer_bare_keys"))
    out.append("changelog forms    : %s" % M.get("STR_changelog_forms"))
    if M.get("EXT1_terms"):
        out.append("EXT-1 undeclared   : %s" % ", ".join(M["EXT1_terms"]))
    if M.get("EXT_parse_failures"):
        out.append("EXT parse failures : %d file(s) not parsed" % M["EXT_parse_failures"])
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
    M.update(measure_ext(root))
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
