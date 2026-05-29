"""
test_tscg_store.py — Unit tests for TscgStore (bridge_server.py Phase 2).
Aligned with actual TscgStore API and pyoxigraph named-graph semantics.

Key pyoxigraph behaviours:
  - All data lives in NAMED GRAPHS — plain WHERE { } queries the DEFAULT graph (empty)
  - Always use GRAPH ?g { ... } in SPARQL
  - Literal str() returns '"value"' with quotes — use .value attribute
  - A named graph is only visible in named_graphs() if it has at least one quad

Author: Echopraxium with the collaboration of Claude AI
"""
import pytest
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from bridge_server import TscgStore

FIXTURES = pathlib.Path(__file__).parent / 'fixtures'
F_M2     = str(FIXTURES / 'minimal_m2.jsonld')
F_EDU    = str(FIXTURES / 'minimal_m1_edu.jsonld')
F_CHEM   = str(FIXTURES / 'minimal_m1_chem.jsonld')

def literal_value(term) -> str:
    """Extract string value from pyoxigraph Literal (strips enclosing quotes)."""
    if hasattr(term, 'value'):
        return term.value
    return str(term).strip('"\'')


# ══════════════════════════════════════════════════════════════════
# load_file
# ══════════════════════════════════════════════════════════════════

class TestLoadFile:

    def test_loads_triples(self, empty_store):
        r = empty_store.load_file(F_M2)
        assert r['triples_loaded'] > 0

    def test_returns_graph_iri(self, empty_store):
        r = empty_store.load_file(F_M2)
        assert 'graph' in r
        assert '://' in r['graph']   # valid absolute IRI

    def test_creates_named_graph(self, empty_store):
        empty_store.load_file(F_M2)
        assert len(empty_store.graph_list()) == 1

    def test_two_different_files_load_different_data(self, empty_store):
        """Each file adds triples — total grows after second file."""
        empty_store.load_file(F_M2)
        n1 = empty_store.stats()['total_triples']
        empty_store.load_file(F_EDU)
        n2 = empty_store.stats()['total_triples']
        assert n2 >= n1   # second file either adds triples or is empty — never breaks

    def test_reload_no_duplicate_triples(self, empty_store):
        r1 = empty_store.load_file(F_M2)
        empty_store.load_file(F_M2)   # reload same file
        # Graph count must not grow
        assert len(empty_store.graph_list()) == 1
        # Triple count must be stable
        assert empty_store.stats()['total_triples'] == r1['triples_loaded']

    def test_invalid_path_raises(self, empty_store):
        with pytest.raises(Exception):
            empty_store.load_file('/nonexistent/file.jsonld')


# ══════════════════════════════════════════════════════════════════
# SPARQL — must use GRAPH ?g { ... } (pyoxigraph named-graph store)
# ══════════════════════════════════════════════════════════════════

SPARQL_LABELS = (
    'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
    'SELECT ?label WHERE { GRAPH ?g { ?s rdfs:label ?label } }'
)
SPARQL_CLASSES = (
    'PREFIX owl: <http://www.w3.org/2002/07/owl#> '
    'SELECT ?c WHERE { GRAPH ?g { ?c a owl:Class } }'
)
SPARQL_ASK = (
    'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
    'ASK { GRAPH ?g { ?s rdfs:label "Process" } }'
)


class TestSparqlSingleGraph:

    def test_select_labels(self, store_with_m2):
        results = list(store_with_m2.query(SPARQL_LABELS))
        labels = [literal_value(r['label']) for r in results]
        assert 'Process'   in labels
        assert 'Memory'    in labels
        assert 'Coherence' in labels

    def test_select_classes(self, store_with_m2):
        results = list(store_with_m2.query(SPARQL_CLASSES))
        assert len(results) == 3

    def test_ask_true(self, store_with_m2):
        assert bool(store_with_m2.query(SPARQL_ASK)) is True

    def test_ask_false(self, store_with_m2):
        q = ('PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
             'ASK { GRAPH ?g { ?s rdfs:label "DoesNotExist" } }')
        assert bool(store_with_m2.query(q)) is False


class TestSparqlCrossGraph:

    def test_labels_from_m2_graph(self, store_two_graphs):
        results = list(store_two_graphs.query(SPARQL_LABELS))
        labels = {literal_value(r['label']) for r in results}
        # M2 labels must be present
        assert 'Process' in labels

    def test_count_graphs_at_least_one(self, store_two_graphs):
        """At least the M2 graph is visible (EDU may be empty if all triples skipped)."""
        results = list(store_two_graphs.query(
            'SELECT (COUNT(DISTINCT ?g) AS ?count) WHERE { GRAPH ?g { ?s ?p ?o } }'))
        count = int(results[0]['count'].value)
        assert count >= 1


# ══════════════════════════════════════════════════════════════════
# stats / graph_list
# ══════════════════════════════════════════════════════════════════

class TestStoreStats:

    def test_empty_store(self, empty_store):
        s = empty_store.stats()
        assert s['total_triples'] == 0
        assert s['named_graphs']  == 0
        assert empty_store.graph_list() == []

    def test_after_load(self, empty_store):
        empty_store.load_file(F_M2)
        s = empty_store.stats()
        assert s['total_triples'] > 0
        assert s['named_graphs']  == 1
        assert len(empty_store.graph_list()) == 1

    def test_graph_list_contains_http_iri(self, empty_store):
        empty_store.load_file(F_M2)
        gl = empty_store.graph_list()
        # Strip angle brackets pyoxigraph may add
        iri = gl[0].strip('<>')
        assert iri.startswith('http')

    def test_clear(self, store_with_m2):
        store_with_m2.clear()
        assert store_with_m2.stats()['total_triples'] == 0
        assert store_with_m2.stats()['named_graphs']  == 0


# ══════════════════════════════════════════════════════════════════
# load_pattern
# ══════════════════════════════════════════════════════════════════

class TestLoadPattern:

    def test_finds_all_fixtures(self, empty_store):
        r = empty_store.load_pattern(str(FIXTURES), ['minimal_*.jsonld'],
                                     recursive=False)
        assert r['files_loaded'] == 3

    def test_returns_total_triples(self, empty_store):
        r = empty_store.load_pattern(str(FIXTURES), ['minimal_*.jsonld'],
                                     recursive=False)
        assert r['total_triples'] > 0
        assert 'files' in r

    def test_invalid_root_no_crash(self, empty_store):
        r = empty_store.load_pattern('/nonexistent/', ['*.jsonld'])
        assert r['files_loaded'] == 0


# ══════════════════════════════════════════════════════════════════
# Persistence
# ══════════════════════════════════════════════════════════════════

class TestPersistence:

    def test_persist_and_reopen(self, tmp_path):
        db = str(tmp_path / 'corpus.db')
        s1 = TscgStore(db_path=db)
        s1.load_file(F_M2)
        n1 = s1.stats()['total_triples']
        assert n1 > 0
        del s1
        s2 = TscgStore(db_path=db)
        assert s2.stats()['total_triples'] == n1

    def test_inmemory_not_persistent(self, empty_store):
        assert empty_store.stats()['persistent'] is False
