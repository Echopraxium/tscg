#!/usr/bin/env python3
"""
test_shacl_runner.py — negative tests for the generic SHACL runner (WS-5 step 1).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/toolchain/validator/tests/test_shacl_runner.py

A grammar is worth something only if it can FAIL. Each test below mutates real data
(read from the working copy) in memory, or feeds the runner a broken input, and
checks that the runner says so. Nothing is written to disk.

Run:  python ontology/toolchain/validator/tests/test_shacl_runner.py
      (also collected by pytest if installed). Exit code 0 iff all tests pass.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from sources import Source  # noqa: E402
from checks import shacl_runner  # noqa: E402

SRC = Source("local")
M2 = "ontology/M2_GenericConcepts.jsonld"
M2_GRAMMAR = "ontology/toolchain/check-M2/M2_MonoidalFormula_Schema_shacl.ttl"


def _run(grammar_text, files, grammar="test.ttl"):
    return shacl_runner.run(grammar, grammar_text, files)


def _ids(findings, cid):
    return [f for f in findings if f["id"] == cid]


def test_baseline_m2_clean_and_not_blind():
    f, s = _run(SRC.read(M2_GRAMMAR), [(M2, SRC.read(M2))], M2_GRAMMAR)
    assert s["results"] == 0, s
    assert s["blind"] == [], s
    assert all(n >= 1 for n in s["focus"].values()), s


def test_bare_S_in_formula_is_one_result():
    text = SRC.read(M2)
    assert '"St × It × A | R"' in text, "fixture formula moved: update the test"
    bad = text.replace('"St × It × A | R"', '"S × It × A | R"', 1)
    f, s = _run(SRC.read(M2_GRAMMAR), [(M2, bad)], M2_GRAMMAR)
    v = _ids(f, "SHACL-V")
    # exactly ONE finding per violation (the text report has 2 lines for it)
    assert len(v) == 1, v
    assert v[0]["shape"] == "MonoidalFormulaShape", v[0]
    assert v[0]["severity"] == "ERROR"


def test_tex_guard_bites():
    doc = json.loads(SRC.read(M2))

    def inject(o):
        if isinstance(o, dict):
            if "m2:expression" in o:
                o["m2:expressionTeX"] = "A \\otimes B"
                return True
            return any(inject(v) for v in o.values())
        if isinstance(o, list):
            return any(inject(v) for v in o)
        return False

    assert inject(doc), "no node carries m2:expression any more: update the test"
    f, s = _run(SRC.read(M2_GRAMMAR), [(M2, json.dumps(doc))], M2_GRAMMAR)
    v = _ids(f, "SHACL-V")
    assert len(v) == 1 and v[0]["shape"] == "NoTeXSerialisationShape", v


def test_blind_shape_is_reported():
    ttl = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <urn:test:> .
ex:Blind a sh:NodeShape ; sh:targetClass ex:NoSuchClass ;
  sh:property [ sh:path ex:p ; sh:minCount 1 ] ."""
    f, s = _run(ttl, [(M2, SRC.read(M2))])
    assert s["results"] == 0
    b = _ids(f, "SHACL-BLIND")
    assert len(b) == 1 and b[0]["node"].endswith("Blind") and b[0]["severity"] == "WARNING", f


def test_missing_pyshacl_is_an_error_not_zero():
    saved = sys.modules.get("pyshacl")
    sys.modules["pyshacl"] = None  # makes `from pyshacl import validate` raise ImportError
    try:
        f, s = _run(SRC.read(M2_GRAMMAR), [(M2, SRC.read(M2))], M2_GRAMMAR)
    finally:
        if saved is None:
            del sys.modules["pyshacl"]
        else:
            sys.modules["pyshacl"] = saved
    e = _ids(f, "SHACL-000")
    assert len(e) == 1 and e[0]["severity"] == "ERROR", f
    assert s["not_run"] == 1 and s["results"] == 0


def test_unparseable_grammar_is_an_error():
    f, s = _run("this is not turtle ;;;", [(M2, SRC.read(M2))])
    assert len(_ids(f, "SHACL-000")) == 1 and "error" in s, f


def test_unparseable_data_is_an_error():
    f, s = _run(SRC.read(M2_GRAMMAR), [("x/M2_Broken.jsonld", "{ not json")], M2_GRAMMAR)
    assert len(_ids(f, "SHACL-000")) == 1 and s["not_run"] == 1, f


def test_public_id_uses_declared_base():
    text = json.dumps({"@context": {"@base": "https://example.org/onto/"}})
    assert shacl_runner.public_id("a/b/M1_X.jsonld", text) == "https://example.org/onto/M1_X.jsonld"
    assert shacl_runner.public_id("a/b/M1_X.jsonld", "{}") == shacl_runner.RAW_BASE + "a/b/M1_X.jsonld"


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
