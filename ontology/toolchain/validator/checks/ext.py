"""
checks/ext.py — EXT family: cross-file graph checks G1b, G5, G6 (WS-5, step 3).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/toolchain/validator/checks/ext.py

WHY NOT SHACL
-------------
A SHACL run sees one file at a time. These checks compare each file with ANOTHER
file (the apex M3_GrammarFoundation, or the file hosting m3:TscgOntologyTypeScheme),
so they are written here, in the same engine, run by the same command
(tscg_validator.py --ext). DETECTION ONLY.

Checks
------
G1b  m3:ontologyType value of a file's owl:Ontology node is not a member
     (skos:inScheme) of m3:TscgOntologyTypeScheme. The scheme is read from its host
     file through the same source; an empty scheme is an ERROR (a check that cannot
     fail is blind). Presence of the property is G1 (SHACL).
G5   EXT-1: a standard term used in the selected files but not declared in the apex
     (ExternalVocabularyPolicy: external terms are declared ONCE in the apex).
G6   EXT-2: a "term" in a standard namespace that is not a term of it (e.g. the
     owl:<key> terms minted by @vocab owl#).
G5/G6 use EXACTLY the definitions of tscg_metrics.measure_ext (constants imported
from tscg_metrics, so there is one definition): one finding per distinct IRI, with
the files using it. Parity: run on M3,M2,M1 they equal the tscg_metrics EXT gauges.
"""

from __future__ import annotations

import collections
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))   # ontology/toolchain/
import tscg_metrics as _tm  # noqa: E402  (single definition of the EXT vocabularies)

from .shacl_runner import public_id  # noqa: E402

SCHEME_HOST = "ontology/M3_GenesisGrammar.jsonld"
M3_NS = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#"
SCHEME_IRI = M3_NS + "TscgOntologyTypeScheme"
ONTOLOGY_TYPE = M3_NS + "ontologyType"
APEX = "ontology/" + _tm.APEX_FILE


def _finding(cid: str, severity: str, relpath: str, node: str, message: str,
             **extra: Any) -> Dict[str, Any]:
    f = {"id": cid, "severity": severity, "file": relpath, "node": node,
         "message": message}
    f.update({k: v for k, v in extra.items() if v is not None})
    return f


def _graph(relpath: str, text: str):
    from rdflib import Graph
    logging.getLogger("rdflib").setLevel(logging.ERROR)
    g = Graph()
    g.parse(data=text, format="json-ld", publicID=public_id(relpath, text))
    return g


def _is_member(iri: str) -> bool:
    """Same closed-namespace membership test as tscg_metrics.measure_ext."""
    from rdflib.namespace import RDF, RDFS, OWL, DCTERMS, SKOS
    closed = [(str(RDF), RDF), (_tm.NS_RDFS, RDFS), (str(OWL), OWL),
              (str(DCTERMS), DCTERMS), (str(SKOS), SKOS)]
    for base, ns in closed:
        if iri.startswith(base):
            try:
                ns[iri[len(base):]]
                return True
            except Exception:
                return False
    return True    # membership not verifiable (ADMS, schema.org…)


def scheme_members(scheme_text: str) -> set:
    from rdflib import URIRef
    from rdflib.namespace import SKOS
    g = _graph(SCHEME_HOST, scheme_text)
    return {str(c) for c in g.subjects(SKOS.inScheme, URIRef(SCHEME_IRI))}


def apex_declared(apex_text: str) -> set:
    from rdflib import URIRef
    from rdflib.namespace import RDF
    g = _graph(APEX, apex_text)
    return {str(s) for s, o in g.subject_objects(RDF.type)
            if isinstance(o, URIRef) and str(o) in _tm.DECLARING_TYPES}


def run(files: Iterable[Tuple[str, str, Optional[str]]], scheme_text: str,
        apex_text: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """files: (relpath, text, layer). Returns (findings, stats)."""
    try:
        from rdflib import URIRef
        from rdflib.namespace import RDF, OWL
    except ImportError as exc:
        return [_finding("EXT-000", "ERROR", "-", "-",
                         f"rdflib not installed ({exc}): EXT NOT run.")], {"error": str(exc)}

    findings: List[Dict[str, Any]] = []
    try:
        members = scheme_members(scheme_text)
        declared = apex_declared(apex_text)
    except Exception as exc:
        return [_finding("EXT-000", "ERROR", SCHEME_HOST, "-",
                         f"cannot parse the scheme host / apex: {exc}")], {"error": str(exc)}
    if not members:
        findings.append(_finding("G1b", "ERROR", SCHEME_HOST, SCHEME_IRI,
                                 "m3:TscgOntologyTypeScheme has 0 members on this source: "
                                 "G1b cannot fail, it is blind."))

    used: Dict[str, Dict[str, set]] = collections.defaultdict(
        lambda: collections.defaultdict(set))          # layer -> iri -> files
    checked_types = 0
    for relpath, text, layer in files:
        layer = layer or "?"
        try:
            g = _graph(relpath, text)
        except Exception as exc:
            findings.append(_finding("EXT-000", "ERROR", relpath, "-",
                                     f"not parseable as JSON-LD, EXT NOT run on it: {exc}"))
            continue
        # G1b
        for onto in g.subjects(RDF.type, OWL.Ontology):
            for t in g.objects(onto, URIRef(ONTOLOGY_TYPE)):
                checked_types += 1
                if str(t) not in members:
                    findings.append(_finding(
                        "G1b", "ERROR", relpath, str(onto),
                        f"m3:ontologyType <{t}> is not a concept of "
                        f"m3:TscgOntologyTypeScheme ({len(members)} members).", layer=layer))
        # G5/G6 usage (same rule as tscg_metrics.measure_ext)
        restrictions = set(g.subjects(RDF.type, OWL.Restriction))
        name = relpath.rsplit("/", 1)[-1]
        for s, p, o in g:
            ps = str(p)
            if not (ps in _tm.RESTRICTION_VOCAB and s in restrictions):
                used[layer][ps].add(name)
            if p == RDF.type and isinstance(o, URIRef):
                used[layer][str(o)].add(name)

    per_layer: Dict[str, Dict[str, int]] = {}
    for layer, iris in sorted(used.items()):
        g5 = g6 = 0
        for iri, where in sorted(iris.items()):
            kind = None
            if iri.startswith(_tm.TSCG_BASE):
                continue
            if iri.startswith(_tm.RESERVED_NS):
                if iri in _tm.LANGUAGE_VOCAB:
                    continue
                if iri in _tm.BUILTIN_ANNOTATION:
                    kind = None if iri in declared else "G5"
                else:
                    kind = "G6"
            elif not _is_member(iri):
                kind = "G6"
            elif iri not in declared:
                kind = "G5"
            if kind == "G5":
                g5 += 1
                findings.append(_finding(
                    "G5", "ERROR", ", ".join(sorted(where)), iri,
                    "EXT-1: standard term used but not declared in the apex "
                    f"({_tm.APEX_FILE}): declare it once there (ExternalVocabularyPolicy).",
                    layer=layer, files=sorted(where)))
            elif kind == "G6":
                g6 += 1
                findings.append(_finding(
                    "G6", "ERROR", ", ".join(sorted(where)), iri,
                    "EXT-2: not a term of its standard namespace (typically a bare key "
                    "turned into <ns><key> by @vocab): declare a TSCG term instead.",
                    layer=layer, files=sorted(where)))
        per_layer[layer] = {"G5": g5, "G6": g6}
    for layer in per_layer:
        per_layer[layer]["G1b"] = sum(1 for f in findings
                                      if f["id"] == "G1b" and f.get("layer") == layer)

    # corpus-wide DISTINCT IRIs (an IRI used in two layers counts once): the unit of
    # the tscg_metrics EXT gauges, for parity checks.
    distinct = {k: len({f["node"] for f in findings if f["id"] == k}) for k in ("G5", "G6")}
    stats = {"scheme_members": len(members), "apex_declared": len(declared),
             "distinct_all_layers": distinct,
             "ontology_types_checked": checked_types, "per_layer": per_layer}
    return findings, stats
