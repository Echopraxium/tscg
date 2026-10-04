#!/usr/bin/env python3
"""
test_doc.py — negative tests for the DOC family D1–D7 (WS-5 step 2).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/toolchain/validator/tests/test_doc.py

Every check must be able to FAIL. Each test mutates a real file (working copy) in
memory and asserts that exactly the expected check moves, by the expected amount,
relative to the unmutated file. Counts are compared as DELTAS: the frozen values
belong to the gate (golden_values.json), not to these tests.

Run:  python ontology/toolchain/validator/tests/test_doc.py   (exit 0 iff all pass)
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from sources import Source  # noqa: E402
from checks import doc  # noqa: E402

SRC = Source("local")
M2 = "ontology/M2_GenericConcepts.jsonld"
M3 = "ontology/M3_GenesisGrammar.jsonld"
LAYER = {M2: "M2", M3: "M3"}


def _load(rel):
    return json.loads(SRC.read(rel))


def _occ(rel, d):
    return doc.occurrences(doc.run(rel, json.dumps(d, ensure_ascii=False), LAYER[rel]))


def _delta(rel, mutate):
    base = _load(rel)
    mut = copy.deepcopy(base)
    mutate(mut)
    a, b = _occ(rel, base), _occ(rel, mut)
    keys = set(a) | set(b)
    return {k: b.get(k, 0) - a.get(k, 0) for k in keys if b.get(k, 0) != a.get(k, 0)}


def _onto(d):
    return next(n for n in d["@graph"] if isinstance(n, dict)
                and "owl:Ontology" in (n["@type"] if isinstance(n["@type"], list) else [n["@type"]]))


def _first_class(d):
    return next(n for n in d["@graph"] if isinstance(n, dict) and n.get("@type") == "owl:Class")


def test_d1_bare_key():
    assert _delta(M2, lambda d: _first_class(d).__setitem__("zzBareKey", "x")) == {"D1": 1}


def test_d1_declared_term_is_not_bare():
    def m(d):
        d["@context"]["zzDeclared"] = "http://www.w3.org/2000/01/rdf-schema#comment"
        _first_class(d)["zzDeclared"] = "x"
    assert _delta(M2, m) == {}


def test_d2_vocab():
    assert _delta(M2, lambda d: d["@context"].__setitem__("@vocab", "http://example.org/#")) == {"D2": 1}


def test_d3_named_graph():
    assert _delta(M2, lambda d: d.__setitem__("@id", "urn:test:graph")) == {"D3": 1}


def test_d4_imports_as_string():
    def m(d):
        o = _onto(d)
        imp = o["owl:imports"]
        first = imp[0] if isinstance(imp, list) else imp
        o["owl:imports"] = [first["@id"]]          # string = literal
    assert _delta(M3, m) == {"D4": 1}


def test_d5_other_changelog_key_any_case():
    assert _delta(M2, lambda d: _onto(d).__setitem__("m2:changelog", [])) == {"D5": 1}
    assert _delta(M2, lambda d: _first_class(d).__setitem__("ChangeLog", {})) == {"D5": 1, "D1": 1}


def test_d5_missing_changelog():
    assert _delta(M2, lambda d: _onto(d).pop("m3:changelog")) == {"D5": 1}


def test_d5_bad_entry_shape():
    assert _delta(M2, lambda d: _onto(d)["m3:changelog"][0].pop("dcterms:date")) == {"D5": 1}


def test_d5_retention():
    def m(d):
        log = _onto(d)["m3:changelog"]
        log.extend(copy.deepcopy(log[0]) for _ in range(8 - len(log)))   # 8 entries
    assert _delta(M3, m) == {"D5": 1}                 # M3 limit is 7
    def m2(d):
        log = _onto(d)["m3:changelog"]
        log.extend(copy.deepcopy(log[0]) for _ in range(4 - len(log)))   # 4 entries
    assert _delta(M2, m2) == {"D5": 1}                # M2 limit is 3


def test_d6_lower_layer_key_and_iri():
    assert _delta(M3, lambda d: _first_class(d).__setitem__("m2:hasFamily", "x")) == {"D6": 1}
    assert _delta(M3, lambda d: _first_class(d).__setitem__("rdfs:seeAlso", {"@id": "m2:Layer"})) == {"D6": 1}
    # prose mention is NOT an inversion
    assert _delta(M3, lambda d: _first_class(d).__setitem__("rdfs:comment", "see m2:Layer")) == {}


def test_d7_strict_expansion_fails():
    # the retired CTX-5 alias: a colon-named term not mapping to its own expansion
    assert _delta(M2, lambda d: d["@context"].__setitem__(
        "m3:eagle_eye", "https://example.org/M3_EagleEye.jsonld#")) == {"D7": 1}


def test_d7_remote_context_blocked():
    def m(d):
        d["@context"] = ["https://example.org/remote-context.jsonld", d["@context"]]
    assert "D7" in _delta(M2, m)


def test_d7_missing_pyld_is_an_error():
    saved = sys.modules.get("pyld")
    sys.modules["pyld"] = None
    try:
        f = doc.d7_expand(M2, _load(M2))
    finally:
        if saved is None:
            del sys.modules["pyld"]
        else:
            sys.modules["pyld"] = saved
    assert len(f) == 1 and f[0]["severity"] == "ERROR" and "NOT run" in f[0]["message"], f


def test_unparseable_json():
    f = doc.run("x/M2_Broken.jsonld", "{ nope", "M2")
    assert len(f) == 1 and f[0]["id"] == "D0" and f[0]["severity"] == "ERROR"


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
