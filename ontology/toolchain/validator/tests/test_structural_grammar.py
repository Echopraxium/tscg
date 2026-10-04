#!/usr/bin/env python3
"""
test_structural_grammar.py — negative tests for G1–G4 (structural SHACL grammar)
and G1b/G5/G6 (EXT family). WS-5 step 3.

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/toolchain/validator/tests/test_structural_grammar.py

Each test mutates a real file (working copy) IN MEMORY and asserts the exact move
of exactly one shape / check, relative to the unmutated file. Counts are deltas:
frozen values belong to the gate.

Run:  python ontology/toolchain/validator/tests/test_structural_grammar.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from sources import Source  # noqa: E402
from checks import shacl_runner, ext  # noqa: E402

SRC = Source("local")
GRAMMAR = "ontology/toolchain/grammars/M3_Structural_Schema_shacl.ttl"
M2 = "ontology/M2_GenericConcepts.jsonld"
M3 = "ontology/M3_GenesisGrammar.jsonld"
LAYER = {M2: "M2", M3: "M3"}


def _load(rel):
    return json.loads(SRC.read(rel))


def _types(n):
    t = n.get("@type", [])
    return t if isinstance(t, list) else [t]


def _onto(d):
    return next(n for n in d["@graph"] if isinstance(n, dict) and "owl:Ontology" in _types(n))


def _node(d, nid):
    return next(n for n in d["@graph"] if isinstance(n, dict) and n.get("@id") == nid)


def _first_class(d):
    return next(n for n in d["@graph"] if isinstance(n, dict) and _types(n) == ["owl:Class"]
                and "rdfs:comment" in n)


def _shapes(rel, d):
    _f, s = shacl_runner.run(GRAMMAR, SRC.read(GRAMMAR),
                             [(rel, json.dumps(d, ensure_ascii=False))])
    assert s["blind"] == [] or rel == M2, s       # every shape bites on M3
    return s["by_shape"]


def _delta(rel, mutate):
    base = _load(rel)
    mut = copy.deepcopy(base)
    mutate(mut)
    a, b = _shapes(rel, base), _shapes(rel, mut)
    keys = set(a) | set(b)
    return {k: b.get(k, 0) - a.get(k, 0) for k in keys if a.get(k, 0) != b.get(k, 0)}


# -- G1 ---------------------------------------------------------------------------
def test_g1_missing_label():
    assert _delta(M3, lambda d: _onto(d).pop("rdfs:label")) == {"OntologyHeaderShape": 1}


def test_g1_retired_m2_changelog():
    assert _delta(M2, lambda d: _onto(d).__setitem__("m2:changelog", "x")) == {"OntologyHeaderShape": 1}


def test_g1_ontology_type_literal():
    assert _delta(M3, lambda d: _onto(d).__setitem__("m3:ontologyType", {"@value": "Genesis"})) \
        == {"OntologyHeaderShape": 1}


# -- G2 ---------------------------------------------------------------------------
def test_g2_missing_comment():
    assert _delta(M3, lambda d: _first_class(d).pop("rdfs:comment")) == {"TermDocumentationShape": 1}


def test_g2_skos_prefLabel_is_a_label():
    assert _delta(M3, lambda d: _node(d, "m3:CaseStudy").pop("skos:prefLabel")) == {"TermDocumentationShape": 1}


def test_g2_external_term_out_of_scope():
    def m(d):
        d["@graph"].append({"@id": "http://example.org/ext#Foo", "@type": "owl:Class"})
    assert _delta(M3, m) == {}


# -- G3 ---------------------------------------------------------------------------
def test_g3a_subclassof_literal():
    assert _delta(M3, lambda d: _first_class(d).__setitem__(
        "rdfs:subClassOf", {"@value": "m3:Something"})) == {"NoLiteralAxiomObjectShape": 1}


def test_g3b_imports_literal():
    assert _delta(M3, lambda d: _onto(d).__setitem__(
        "owl:imports", [{"@value": "M2_GenericConcepts.jsonld"}])) == {"IriOnlyObjectShape": 1}


# -- G4 ---------------------------------------------------------------------------
def test_g4_date_format():
    assert _delta(M2, lambda d: _onto(d)["m3:changelog"][0].__setitem__(
        "dcterms:date", "05/10/2026")) == {"ChangelogEntryShape": 1}


def test_g4_missing_notes():
    assert _delta(M2, lambda d: _onto(d)["m3:changelog"][0].pop("adms:versionNotes")) \
        == {"ChangelogEntryShape": 1}


def test_g4_closed_extra_property():
    assert _delta(M2, lambda d: _onto(d)["m3:changelog"][0].__setitem__(
        "rdfs:comment", "extra")) == {"ChangelogEntryShape": 1}


# -- EXT: G1b, G5, G6 -----------------------------------------------------------------
def _ext(rel, d, scheme=None):
    f, s = ext.run([(rel, json.dumps(d, ensure_ascii=False), LAYER[rel])],
                   scheme if scheme is not None else SRC.read(ext.SCHEME_HOST),
                   SRC.read(ext.APEX))
    return f, s


def _ext_delta(rel, mutate):
    base = _load(rel)
    mut = copy.deepcopy(base)
    mutate(mut)
    a = _ext(rel, base)[1]["per_layer"][LAYER[rel]]
    b = _ext(rel, mut)[1]["per_layer"][LAYER[rel]]
    return {k: b[k] - a[k] for k in a if a[k] != b[k]}


def test_g1b_type_not_in_scheme():
    assert _ext_delta(M3, lambda d: _onto(d).__setitem__(
        "m3:ontologyType", {"@id": "m3:NotAnOntologyType"})) == {"G1b": 1}


def test_g1b_empty_scheme_is_blind_error():
    empty = json.dumps({"@context": {}, "@graph": []})
    f, _s = _ext(M3, _load(M3), scheme=empty)
    assert any(x["id"] == "G1b" and "blind" in x["message"] for x in f), f


def test_g5_undeclared_standard_term():
    assert _ext_delta(M3, lambda d: _first_class(d).__setitem__(
        "dcterms:bibliographicCitation", "x")) == {"G5": 1}


def test_g6_nonterm_in_owl_namespace():
    assert _ext_delta(M2, lambda d: _first_class(d).__setitem__("owl:notATerm", "x")) == {"G6": 1}


def main() -> int:
    tests = [(n, fn) for n, fn in sorted(globals().items())
             if n.startswith("test_") and callable(fn)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {name}: {exc}")
    print(f"  {len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
