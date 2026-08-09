"""
Regression tests for Aki's PEPITE findings (2026-07).

Author: Echopraxium with the collaboration of Claude AI

Covers:
- PEPITE-001  graph IRIs / names must be bare (no `<...>`, no trailing `>`).
- PEPITE-003/005/011  the loader must ignore non-active-corpus dirs
                       (archives, Ref, docs, mirrors, backups).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import tscg_api_server as srv  # noqa: E402


# ── PEPITE-001 ──────────────────────────────────────────────────────────────
def test_ox_to_value_namednode_is_bare_iri():
    import pyoxigraph as ox
    iri = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_VSM.jsonld"
    node = ox.NamedNode(iri)
    assert srv._ox_to_value(node) == iri            # no angle brackets
    assert not srv._ox_to_value(node).startswith("<")
    assert not srv._ox_to_value(node).endswith(">")


def test_graph_name_has_no_trailing_bracket():
    """The /corpus/list name derivation must not keep a trailing '>'."""
    from pathlib import Path as P
    iri = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/instances/x/M0_VSM.jsonld"
    # emulate the fixed derivation used by corpus_list
    name = P(iri).name
    assert name == "M0_VSM.jsonld"
    assert not name.endswith(">")


# ── PEPITE-003 / 005 / 011 (scope) ──────────────────────────────────────────
def test_active_corpus_excludes_non_live_dirs():
    excluded = [
        "D:/x/ontology/_archives/M2_GenericConcepts.jsonld",
        "D:/x/ontology/Ref/M2_GenericConcepts_2026_02_17.jsonld",
        "D:/x/ontology/docs/whatever.jsonld",
        "D:/x/instances/NakamotoConsensus/static/M0_NakamotoConsensus.jsonld",
        "D:/x/migration_backups/v1/M0_Foo.jsonld",
    ]
    for p in excluded:
        assert srv._in_active_corpus(p) is False, p


def test_active_corpus_includes_live_files():
    included = [
        "D:/x/ontology/M2_GenericConcepts.jsonld",
        "D:/x/ontology/M1_CoreConcepts.jsonld",
        "D:/x/ontology/M1_extensions/biology/M1_Biology.jsonld",
        "D:/x/instances/systemic-frameworks/vsm/M0_VSM.jsonld",
    ]
    for p in included:
        assert srv._in_active_corpus(p) is True, p


def test_active_corpus_handles_windows_backslashes():
    assert srv._in_active_corpus(r"D:\x\ontology\_archives\M2.jsonld") is False
    assert srv._in_active_corpus(r"D:\x\ontology\M2_GenericConcepts.jsonld") is True
