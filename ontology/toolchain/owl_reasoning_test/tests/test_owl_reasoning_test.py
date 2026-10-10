"""
Tests for owl_reasoning_test.py 2.0.0 (2026-10-10).

Import resolution is pure Python and always runs. The reasoning tests need Java + Pellet:
they are SKIPPED (never passed) when the reasoner cannot run (exit 3, environment error).
Run from the repository root:  python -m pytest -q ontology/toolchain/owl_reasoning_test/tests
"""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent))
import owl_reasoning_test as ort  # noqa: E402

FIX = "ontology/toolchain/owl_reasoning_test/tests/fixtures/"


def test_imports_resolved_locally_and_removed():
    g, merged, unresolved = ort.load_with_imports(ROOT / "ontology/M3_GenesisGrammar.jsonld", ROOT)
    names = sorted(f.name for f in merged)
    assert unresolved == []
    assert names == sorted(["M3_GenesisGrammar.jsonld", "M3_GrammarFoundation.jsonld", "M3_EagleEye.jsonld",
                            "M3_SphinxEye.jsonld", "M3_BicephalousPerspective.jsonld"])
    assert not any(str(p) == ort.OWL_IMPORTS for _, p, _ in g)


def test_isolated_ignores_imports():
    _, merged, unresolved = ort.load_with_imports(ROOT / "ontology/M3_GenesisGrammar.jsonld", ROOT,
                                                  follow_imports=False)
    assert len(merged) == 1 and unresolved == []


def test_unresolved_import_is_an_error(monkeypatch):
    monkeypatch.chdir(ROOT)
    assert ort.main(["--file", FIX + "bad_import.jsonld", "--list-imports"]) == 2


def test_missing_file_is_an_error(monkeypatch):
    monkeypatch.chdir(ROOT)
    assert ort.main(["--file", "ontology/M9_DoesNotExist.jsonld"]) == 2


def test_inconsistent_ontology_fails(monkeypatch):
    monkeypatch.chdir(ROOT)
    rc = ort.main(["--file", FIX + "inconsistent.jsonld"])
    if rc == 3:
        pytest.skip("reasoner unavailable here (Java/Pellet): environment error, not a pass")
    assert rc == 1, "a deliberately inconsistent ontology must FAIL (exit 1)"
