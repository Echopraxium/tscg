"""
checks/shacl_runner.py — generic SHACL runner (WS-5, step 1: "job one").

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/toolchain/validator/checks/shacl_runner.py

ONE runner for every layer, parameterised by a grammar (a Turtle shapes file) and the
files it targets. Adding a grammar = adding a .ttl and one line in GRAMMARS, never a
new script. DETECTION ONLY: nothing is written to the corpus.

What it does the same way for every layer
-----------------------------------------
* data graph parsed from the file TEXT handed over by the source switch (so
  --source head validates HEAD, not a stale disk copy), with the IRI the file
  declares for itself (@context @base + file name) as publicID — same reason as
  check_M1._public_id: a filesystem-minted base breaks cross-file IRIs;
* the grammar itself is read through the same source (HEAD grammar on HEAD data);
* pyshacl with inference="none", advanced=False — exactly like check_M1.run_shacl
  (the gate's reference); never mix with "rdfs", the counts differ;
* ONE finding per sh:ValidationResult, read from the RESULTS GRAPH. Never scrape the
  text report: check_M1 counts the lines "Message:" AND "Focus Node:", so each
  violation is counted twice (measured 2026-10-03: 688 lines = 344 results);
* anti-blindness: for every node shape that declares a target, its focus nodes are
  counted over the whole run. A targeted shape with 0 focus nodes validates nothing
  while reporting CONFORMS (SHAPE 9 lesson) -> SHACL-BLIND;
* a missing pyshacl, an unparseable grammar or an unparseable data file is an ERROR,
  never "0 violations".

Finding ids
-----------
SHACL-V   one sh:ValidationResult (severity from sh:resultSeverity)
SHACL-000 the grammar could not be run on this file (tool missing, parse error)
SHACL-BLIND  a targeted node shape matched 0 focus nodes over the run  -> WARNING
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional, Tuple

# Layer -> grammar files (repo-relative). The single place where a grammar is wired.
# M3: none yet (WS-5 step 3). M2: the 2 targeted SC-2 shapes only — NOT an M2 grammar.
GRAMMARS: Dict[str, List[str]] = {
    "M1": ["ontology/toolchain/check-M1/M1_Schema_shacl.ttl"],
    "M0": ["ontology/toolchain/check-M0/M0_Instances_Schema_shacl.ttl"],
    "M2": ["ontology/toolchain/check-M2/M2_MonoidalFormula_Schema_shacl.ttl"],
}

RAW_BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/"

_SEVERITY = {"Violation": "ERROR", "Warning": "WARNING", "Info": "INFO"}


def _finding(cid: str, severity: str, relpath: str, node: str, message: str,
             **extra: Any) -> Dict[str, Any]:
    f = {"id": cid, "severity": severity, "file": relpath, "node": node,
         "message": message}
    f.update({k: v for k, v in extra.items() if v is not None})
    return f


def public_id(relpath: str, text: str) -> str:
    """The IRI the file declares for itself: @context @base + file name.
    Fallback: its published URL (repo-relative path under RAW_BASE)."""
    name = relpath.rsplit("/", 1)[-1]
    try:
        ctx = json.loads(text).get("@context", {})
        base = ctx.get("@base") if isinstance(ctx, dict) else None
        if base:
            return str(base) + name
    except Exception:
        pass
    return RAW_BASE + relpath


def _local(term: Any) -> str:
    s = str(term)
    for sep in ("#", "/"):
        if sep in s:
            s = s.rsplit(sep, 1)[-1] or s
    return s


class Grammar:
    """A parsed shapes graph plus the per-shape focus-node tally of a run."""

    def __init__(self, relpath: str, text: str) -> None:
        from rdflib import Graph  # import here: a missing rdflib is reported, not raised
        self.relpath = relpath
        self.graph = Graph()
        self.graph.parse(data=text, format="turtle")
        self.focus: Dict[str, int] = {s: 0 for s in self.targeted_shapes()}

    # -- shapes ------------------------------------------------------------------
    def node_shapes(self) -> List[Any]:
        from rdflib import RDF, Namespace
        SH = Namespace("http://www.w3.org/ns/shacl#")
        return sorted(set(self.graph.subjects(RDF.type, SH.NodeShape)), key=str)

    def _targets(self, shape: Any) -> List[Tuple[str, Any]]:
        from rdflib import RDF, RDFS, Namespace
        SH = Namespace("http://www.w3.org/ns/shacl#")
        out: List[Tuple[str, Any]] = []
        for kind in ("targetClass", "targetNode", "targetSubjectsOf", "targetObjectsOf"):
            for o in self.graph.objects(shape, SH[kind]):
                out.append((kind, o))
        # implicit class target: a shape that is also an rdfs:Class
        if (shape, RDF.type, RDFS.Class) in self.graph:
            out.append(("targetClass", shape))
        for o in self.graph.objects(shape, SH.target):   # SHACL-AF / SPARQL target
            out.append(("target", o))
        return out

    def targeted_shapes(self) -> List[str]:
        return [str(s) for s in self.node_shapes() if self._targets(s)]

    def shape_label(self, shape_iri: str) -> str:
        return _local(shape_iri)

    def count_focus(self, data: Any) -> None:
        """Add this data graph's focus nodes to the per-shape tally."""
        from rdflib import RDF, RDFS, URIRef
        for s in self.node_shapes():
            key = str(s)
            if key not in self.focus:
                continue
            nodes = set()
            for kind, o in self._targets(s):
                if kind == "targetNode":
                    if (o, None, None) in data or (None, None, o) in data:
                        nodes.add(o)
                elif kind == "targetSubjectsOf":
                    nodes.update(data.subjects(o, None))
                elif kind == "targetObjectsOf":
                    nodes.update(data.objects(None, o))
                elif kind == "targetClass":
                    classes = {o} | set(data.transitive_subjects(RDFS.subClassOf, o))
                    for c in classes:
                        nodes.update(data.subjects(RDF.type, c))
                else:  # sh:target (SHACL-AF): not countable statically -> never called blind
                    nodes.add(URIRef("urn:tscg:uncountable-target"))
            self.focus[key] += len(nodes)

    def node_shape_of(self, source_shape: Any) -> Any:
        """Walk sh:property / sh:node / logical lists up to a node shape that has a target."""
        from rdflib import Namespace
        SH = Namespace("http://www.w3.org/ns/shacl#")
        seen, frontier = set(), [source_shape]
        targeted = set(self.focus)
        while frontier:
            cur = frontier.pop()
            if cur in seen:
                continue
            seen.add(cur)
            if str(cur) in targeted:
                return cur
            for p in (SH.property, SH.node, SH["not"]):
                frontier.extend(self.graph.subjects(p, cur))
            frontier.extend(self.graph.subjects(None, cur))   # list cells of sh:or/sh:and
        return source_shape


def run_on_file(grammar: Grammar, relpath: str, text: str) -> List[Dict[str, Any]]:
    """Validate ONE file against ONE grammar. Returns findings (one per result)."""
    try:
        from rdflib import Graph, RDF, Namespace
        from pyshacl import validate
    except ImportError as exc:
        return [_finding("SHACL-000", "ERROR", relpath, "-",
                         f"pyshacl/rdflib not installed ({exc}): the grammar "
                         f"{grammar.relpath} was NOT run. This is not 0 violations.")]
    SH = Namespace("http://www.w3.org/ns/shacl#")

    data = Graph()
    try:
        data.parse(data=text, format="json-ld", publicID=public_id(relpath, text))
    except Exception as exc:
        return [_finding("SHACL-000", "ERROR", relpath, "-",
                         f"data not parseable as JSON-LD, grammar {grammar.relpath} "
                         f"NOT run: {exc}")]

    grammar.count_focus(data)
    try:
        _conforms, results, _text = validate(data, shacl_graph=grammar.graph,
                                             inference="none")
    except Exception as exc:
        return [_finding("SHACL-000", "ERROR", relpath, "-",
                         f"pyshacl crashed on {grammar.relpath}: {exc}")]

    findings: List[Dict[str, Any]] = []
    for r in sorted(results.subjects(RDF.type, SH.ValidationResult), key=str):
        sev = results.value(r, SH.resultSeverity)
        src = results.value(r, SH.sourceShape)
        msg = results.value(r, SH.resultMessage)
        path = results.value(r, SH.resultPath)
        val = results.value(r, SH.value)
        shape = grammar.node_shape_of(src) if src is not None else None
        findings.append(_finding(
            "SHACL-V", _SEVERITY.get(_local(sev), "ERROR"), relpath,
            str(results.value(r, SH.focusNode)),
            str(msg) if msg is not None else f"{_local(results.value(r, SH.sourceConstraintComponent))}",
            grammar=grammar.relpath,
            shape=grammar.shape_label(shape) if shape is not None else None,
            path=_local(path) if path is not None else None,
            value=str(val) if val is not None else None,
        ))
    return findings


def run(grammar_relpath: str, grammar_text: str,
        files: Iterable[Tuple[str, str]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Run one grammar over (relpath, text) pairs.

    Returns (findings, stats). stats = {grammar, files, results, focus{shape: n},
    blind[shape...]}. SHACL-BLIND findings are appended for targeted shapes whose
    focus count stayed at 0 over the whole run (a shape may legitimately match only
    some files, so blindness is judged on the run, not per file)."""
    try:
        grammar = Grammar(grammar_relpath, grammar_text)
    except ImportError as exc:
        f = _finding("SHACL-000", "ERROR", grammar_relpath, "-",
                     f"rdflib not installed ({exc}): grammar NOT run.")
        return [f], {"grammar": grammar_relpath, "error": str(exc)}
    except Exception as exc:
        f = _finding("SHACL-000", "ERROR", grammar_relpath, "-",
                     f"grammar is not parseable Turtle: {exc}")
        return [f], {"grammar": grammar_relpath, "error": str(exc)}

    findings: List[Dict[str, Any]] = []
    n_files = 0
    for relpath, text in files:
        n_files += 1
        findings.extend(run_on_file(grammar, relpath, text))

    blind = [s for s, n in grammar.focus.items() if n == 0]
    for s in blind:
        findings.append(_finding(
            "SHACL-BLIND", "WARNING", grammar_relpath, grammar.shape_label(s),
            f"targeted shape matched 0 focus nodes over {n_files} file(s): it validates "
            f"nothing and would report CONFORMS. Fix its target or retire it."))

    stats = {
        "grammar": grammar_relpath,
        "files": n_files,
        "results": sum(1 for f in findings if f["id"] == "SHACL-V"),
        "not_run": sum(1 for f in findings if f["id"] == "SHACL-000"),
        "focus": {grammar.shape_label(s): n for s, n in sorted(grammar.focus.items())},
        "blind": [grammar.shape_label(s) for s in blind],
        "untargeted_shapes": len(grammar.node_shapes()) - len(grammar.focus),
    }
    return findings, stats
