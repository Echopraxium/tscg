"""
test_endpoints.py — Integration tests for tscg_api_server.py FastAPI endpoints.
Migrated from tscg-python-bridge/tests/test_endpoints.py.

Uses FastAPI TestClient (httpx) — no real server needed.

Route changes vs bridge_server.py:
  /load          → /corpus/load      (POST, body: {file_path})
  /sparql        → /corpus/sparql    (POST, body: {query})
  /corpus/list   → response shape changed: {graph_count, graphs:[{iri,name}]}
  /hierarchy     → REMOVED (not in tscg_api_server)
  /health        → field 'rdflib_version' moved to /info
  /corpus/delete → DELETE /corpus/graph  (body: {graph_iri})

Author: Echopraxium with the collaboration of Claude AI
"""
import sys
import pathlib
import pytest

SRC_DIR  = pathlib.Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(SRC_DIR))

FIXTURES = pathlib.Path(__file__).parent / 'fixtures'
F_M2     = str(FIXTURES / 'minimal_m2.jsonld')
F_EDU    = str(FIXTURES / 'minimal_m1_edu.jsonld')
F_CHEM   = str(FIXTURES / 'minimal_m1_chem.jsonld')
BASE     = 'https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/'


# ══════════════════════════════════════════════════════════════════
# GET /health
# ══════════════════════════════════════════════════════════════════

class TestHealth:

    def test_status_ok(self, client):
        r = client.get('/health')
        assert r.status_code == 200
        assert r.json()['status'] == 'ok'

    def test_has_uptime(self, client):
        r = client.get('/health')
        assert 'uptime' in r.json()

    def test_has_graph_count(self, client):
        r = client.get('/health')
        assert 'graph_count' in r.json()

    def test_has_triple_count(self, client):
        r = client.get('/health')
        assert 'triple_count' in r.json()


# ══════════════════════════════════════════════════════════════════
# GET /info
# ══════════════════════════════════════════════════════════════════

class TestInfo:

    def test_has_rdflib_version(self, client):
        r = client.get('/info')
        assert r.status_code == 200
        assert 'rdflib_version' in r.json()

    def test_has_pyoxigraph_version(self, client):
        r = client.get('/info')
        assert 'pyoxigraph_version' in r.json()

    def test_has_base_iri(self, client):
        r = client.get('/info')
        assert r.json()['base_iri'] == BASE

    def test_has_version(self, client):
        r = client.get('/info')
        assert 'version' in r.json()


# ══════════════════════════════════════════════════════════════════
# POST /corpus/load  (replaces /load)
# ══════════════════════════════════════════════════════════════════

class TestCorpusLoad:

    def test_load_valid_file(self, client):
        r = client.post('/corpus/load', json={'file_path': F_M2})
        assert r.status_code == 200
        data = r.json()
        assert data['triples_loaded'] > 0

    def test_load_missing_file(self, client):
        r = client.post('/corpus/load', json={'file_path': '/nonexistent/file.jsonld'})
        assert r.status_code == 404

    def test_load_returns_graph_iri(self, client):
        r = client.post('/corpus/load', json={'file_path': F_M2})
        assert 'graph' in r.json()
        assert '://' in r.json()['graph']

    def test_load_returns_file_name(self, client):
        r = client.post('/corpus/load', json={'file_path': F_M2})
        assert r.json()['file'] == 'minimal_m2.jsonld'


# ══════════════════════════════════════════════════════════════════
# POST /corpus/load-pattern
# ══════════════════════════════════════════════════════════════════

class TestCorpusLoadPattern:

    def test_load_pattern_all_fixtures(self, client):
        r = client.post('/corpus/load-pattern', json={
            'ontology_root': str(FIXTURES),
            'patterns':      ['minimal_*.jsonld'],
            'recursive':     False,
        })
        assert r.status_code == 200
        assert r.json()['files_loaded'] == 3

    def test_load_pattern_has_triples(self, client):
        r = client.post('/corpus/load-pattern', json={
            'ontology_root': str(FIXTURES),
            'patterns':      ['minimal_*.jsonld'],
            'recursive':     False,
        })
        assert r.json()['total_triples'] > 0

    def test_load_pattern_invalid_root(self, client):
        r = client.post('/corpus/load-pattern', json={
            'ontology_root': '/nonexistent/',
            'patterns':      ['*.jsonld'],
        })
        assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════
# GET /corpus/list
# ══════════════════════════════════════════════════════════════════

class TestCorpusList:

    @pytest.fixture(autouse=True)
    def preload(self, client):
        client.post('/corpus/load', json={'file_path': F_M2})

    def test_list_ok(self, client):
        r = client.get('/corpus/list')
        assert r.status_code == 200

    def test_list_has_graphs_key(self, client):
        r = client.get('/corpus/list')
        assert 'graphs' in r.json()

    def test_list_has_graph_count(self, client):
        r = client.get('/corpus/list')
        assert 'graph_count' in r.json()
        assert r.json()['graph_count'] >= 1

    def test_list_graph_has_iri_and_name(self, client):
        r = client.get('/corpus/list')
        g = r.json()['graphs'][0]
        assert 'iri'  in g
        assert 'name' in g


# ══════════════════════════════════════════════════════════════════
# GET /corpus/layers
# ══════════════════════════════════════════════════════════════════

class TestCorpusLayers:

    def test_layers_ok(self, client):
        r = client.get('/corpus/layers')
        assert r.status_code == 200

    def test_layers_has_m2_key(self, client):
        client.post('/corpus/load', json={'file_path': F_M2})
        r = client.get('/corpus/layers')
        assert 'M2' in r.json()

    def test_layers_all_keys_present(self, client):
        r = client.get('/corpus/layers')
        for key in ('M3', 'M2', 'M1', 'M0', 'other'):
            assert key in r.json()


# ══════════════════════════════════════════════════════════════════
# POST /corpus/sparql  (replaces /sparql)
# ══════════════════════════════════════════════════════════════════

class TestCorpusSparql:

    @pytest.fixture(autouse=True)
    def preload(self, client):
        client.post('/corpus/load', json={'file_path': F_M2})

    def test_select_query(self, client):
        r = client.post('/corpus/sparql', json={
            'query': (
                'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
                'SELECT ?label WHERE { GRAPH ?g { ?s rdfs:label ?label } }'
            )
        })
        assert r.status_code == 200
        data = r.json()
        assert data['query_type'] == 'SELECT'
        assert data['count'] >= 3

    def test_ask_query_true(self, client):
        r = client.post('/corpus/sparql', json={
            'query': (
                'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
                'ASK { GRAPH ?g { ?s rdfs:label "Process" } }'
            )
        })
        assert r.status_code == 200
        assert r.json()['query_type'] == 'ASK'
        assert r.json()['result'] is True

    def test_ask_query_false(self, client):
        r = client.post('/corpus/sparql', json={
            'query': (
                'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
                'ASK { GRAPH ?g { ?s rdfs:label "DoesNotExistXYZ" } }'
            )
        })
        assert r.json()['result'] is False

    def test_invalid_sparql(self, client):
        r = client.post('/corpus/sparql', json={'query': 'THIS IS NOT SPARQL'})
        assert r.status_code == 400

    def test_select_results_structure(self, client):
        r = client.post('/corpus/sparql', json={
            'query': 'SELECT ?s WHERE { GRAPH ?g { ?s ?p ?o } } LIMIT 1'
        })
        data = r.json()
        assert 'vars'    in data
        assert 'results' in data
        assert 'count'   in data


# ══════════════════════════════════════════════════════════════════
# POST /iri/expand
# ══════════════════════════════════════════════════════════════════

class TestIriExpand:

    def test_expand_post(self, client):
        r = client.post('/iri/expand', json={
            'compact_iri': 'm2:Process',
            'context': {'m2': 'M2_GenericConcepts.jsonld#'}
        })
        assert r.status_code == 200
        data = r.json()
        assert 'expanded' in data
        assert 'M2_GenericConcepts.jsonld#Process' in data['expanded']

    def test_expand_get(self, client):
        r = client.get('/iri/expand', params={'iri': 'SomeClass'})
        assert r.status_code == 200
        assert BASE in r.json()['expanded']

    def test_expand_absolute_unchanged(self, client):
        iri = 'http://www.w3.org/2002/07/owl#Class'
        r = client.post('/iri/expand', json={'compact_iri': iri, 'context': {}})
        assert r.json()['expanded'] == iri


# ══════════════════════════════════════════════════════════════════
# DELETE /corpus/graph  and  DELETE /corpus/clear
# ══════════════════════════════════════════════════════════════════

class TestCorpusDelete:

    def test_clear_ok(self, client):
        client.post('/corpus/load', json={'file_path': F_M2})
        r = client.request('DELETE', '/corpus/clear')
        assert r.status_code == 200
        assert r.json()['cleared'] is True

    def test_delete_nonexistent_graph_404(self, client):
        r = client.request('DELETE', '/corpus/graph',
                           json={'graph_iri': 'https://example.com/nonexistent'})
        assert r.status_code == 404
