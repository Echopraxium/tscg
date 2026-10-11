#!/usr/bin/env python3
"""
test_m1_combo_punning.py — negative tests for the class/instance rule on M1 combos
(WS-1 B2 lot C2, Debt Overview §8.0f).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/toolchain/validator/tests/test_m1_combo_punning.py

An M1 combo is a DERIVED CLASS: "@type": "owl:Class" + rdfs:subClassOf the combo class.
Typing it as an INSTANCE of m2:GenericConceptCombo / m2:DomainConceptCombo (punning) is
forbidden by M1 SHACL 1.7.0 SHAPE 12 NoComboPunningShape and by check_M1 1.7.0 CMB001.

Each test mutates a real file (working copy) IN MEMORY and asserts the exact move of
exactly one shape / check relative to the unmutated file. Counts are deltas: frozen
values belong to the gate. pyshacl runs as check_M1 runs it (inference="none",
advanced=True, publicID = the IRI the file declares).

Run:  python ontology/toolchain/validator/tests/test_m1_combo_punning.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLCHAIN = HERE.parent.parent
REPO = TOOLCHAIN.parent.parent
GRAMMAR = TOOLCHAIN / "check-M1" / "M1_Schema_shacl.ttl"
CORE = REPO / "ontology" / "M1_CoreConcepts.jsonld"
EXT = REPO / "ontology" / "M1_extensions" / "physics" / "M1_Physics.jsonld"
SH = "http://www.w3.org/ns/shacl#"
SHAPE = "NoComboPunningShape"

_spec = importlib.util.spec_from_file_location("check_M1", TOOLCHAIN / "check-M1" / "check_M1.py")
check_M1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_M1)


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _combo(d, cls):
    """First combo attached to m2:<cls> by rdfs:subClassOf."""
    for n in d["@graph"]:
        sub = n.get("rdfs:subClassOf", [])
        sub = sub if isinstance(sub, list) else [sub]
        if any(check_M1._local_m2(v) == cls for v in sub):
            return n
    raise AssertionError(f"no combo subclassing m2:{cls}")


def _shapes(path, d):
    """Violations per shape name, plus the focus count of SHAPE 12."""
    from pyshacl import validate
    from rdflib import Graph, Namespace, RDF, URIRef
    g = Graph()
    g.parse(data=json.dumps(d, ensure_ascii=False), format="json-ld",
            publicID=check_M1._public_id(path))
    shg = Graph().parse(str(GRAMMAR), format="turtle")
    _c, results, _t = validate(g, shacl_graph=shg, inference="none", advanced=True)
    names = {s: str(o) for s, o in shg.subject_objects(URIRef(SH + "name"))}
    out = Counter()
    for r in results.subjects(RDF.type, URIRef(SH + "ValidationResult")):
        node = results.value(r, URIRef(SH + "sourceShape"))
        seen = set()
        # nested shapes are blank nodes (sh:property, sh:or lists…): climb to the named one
        while node not in names and node not in seen:
            seen.add(node)
            parent = next(shg.subjects(None, node), None)
            if parent is None:
                break
            node = parent
        out[names.get(node, "?")] += 1
    return out, g


def _delta(path, mutate):
    base = _load(path)
    mut = copy.deepcopy(base)
    mutate(mut)
    a, _ = _shapes(path, base)
    b, _ = _shapes(path, mut)
    keys = set(a) | set(b)
    return {k: b.get(k, 0) - a.get(k, 0) for k in keys if a.get(k, 0) != b.get(k, 0)}


def _pun(cls):
    def m(d):
        n = _combo(d, cls)
        assert n["@type"] == "owl:Class", n["@type"]
        n["@type"] = ["owl:Class", "m2:" + cls]
    return m


# -- SHAPE 12 -----------------------------------------------------------------------
def test_shape12_bites_and_is_clean_on_head():
    from rdflib import OWL, RDF
    for path in (CORE, EXT):
        counts, g = _shapes(path, _load(path))
        assert counts.get(SHAPE, 0) == 0, (path.name, counts)
        assert len(set(g.subjects(RDF.type, OWL.Class))) >= 1   # focus nodes exist


def test_shape12_core_generic_combo_punned():
    assert _delta(CORE, _pun("GenericConceptCombo")) == {SHAPE: 1}


def test_shape12_extension_domain_combo_punned():
    assert _delta(EXT, _pun("DomainConceptCombo")) == {SHAPE: 1}


def test_shape12_punned_without_owl_class_is_caught():
    def m(d):
        _combo(d, "DomainConceptCombo")["@type"] = "m2:DomainConceptCombo"
    d = _delta(EXT, m)
    assert d.get(SHAPE) == 1, d


# -- check_M1 CMB001 ------------------------------------------------------------------
def _checker(path, d):
    c = check_M1.M1Checker(path, dry_run=True)
    c.data = d
    c.check_no_combo_punning()
    return c


def test_cmb001_clean_on_head():
    for path in (CORE, EXT):
        assert [i for i in _checker(path, _load(path)).issues if i.code == "CMB001"] == []


def test_cmb001_flags_punning_full_iri_too():
    d = _load(EXT)
    _combo(d, "DomainConceptCombo")["@type"] = ["owl:Class", check_M1.M2_NS + "DomainConceptCombo"]
    assert [i.code for i in _checker(EXT, d).issues] == ["CMB001"]


def test_cmb001_autofix_restores_derived_class():
    d = _load(CORE)
    ref = copy.deepcopy(_combo(d, "GenericConceptCombo"))
    n = _combo(d, "GenericConceptCombo")
    n["@type"] = ["owl:Class", "m2:GenericConceptCombo"]
    n.pop("rdfs:subClassOf")
    c = _checker(CORE, d)
    assert c.fix_combo_punning() == 1
    assert n["@type"] == "owl:Class"
    assert check_M1._local_m2(n["rdfs:subClassOf"]) == "GenericConceptCombo"
    assert c.fix_combo_punning() == 0                      # idempotent
    assert n["@type"] == ref["@type"]


def main() -> int:
    tests = [(n, fn) for n, fn in sorted(globals().items())
             if n.startswith("test_") and callable(fn)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS {name}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FAIL {name}: {e!r}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
