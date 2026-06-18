"""
test_endpoints.py — Integration tests for bridge_server.py FastAPI endpoints.

Uses FastAPI TestClient (httpx) — no real server needed.
Tests the existing endpoints (/health, /load, /sparql, /hierarchy,
/corpus/load, /corpus/sparql) without modifying any production code.

Author: Echopraxium with the collaboration of Claude AI
"""
import pytest
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIXTURES = pathlib.Path(__file__).parent / 'fixtures'
F_M2     = str(FIXTURES / 'minimal_m2.jsonld')
F_EDU    = str(FIXTURES / 'minimal_m1_edu.jsonld')
F_CHEM   = str(FIXTURES / 'minimal_m1_chem.jsonld')
BASE     = 'https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/'

# ══════════════════════════════════════════════════════════════════
# /health
# ══════════════════════════════════════════════════════════════════

class TestHealth:

    def test_status_ok(self, client):
        r = client.get('/health')
        assert r.status_code == 200
        data = r.json()
        assert data['status'] == 'ok'

    def test_has_rdflib_version(self, client):
        r = client.get('/health')
        assert 'rdflib_version' in r.json()

# ══════════════════════════════════════════════════════════════════
# /load
# ══════════════════════════════════════════════════════════════════

class TestLoad:

    def test_load_valid_file(self, client):
        r = client.post('/load', json={'file_path': F_M2})
        assert r.status_code == 200
        data = r.json()
        assert data['loaded'] is True
        assert data['triples'] > 0

    def test_load_missing_file(self, client):
        r = client.post('/load', json={'file_path': '/nonexistent/file.jsonld'})
        assert r.status_code == 404

    def test_load_returns_objects(self, client):
        r = client.post('/load', json={'file_path': F_M2})
        assert 'objects' in r.json()
        assert len(r.json()['objects']) > 0

    def test_load_owl_thing_in_objects(self, client):
        r = client.post('/load', json={'file_path': F_M2})
        ids = [o['id'] for o in r.json()['objects']]
        assert 'http://www.w3.org/2002/07/owl#Thing' in ids

    def test_load_classes_in_objects(self, client):
        r = client.post('/load', json={'file_path': F_M2})
        labels = [o['label'] for o in r.json()['objects']]
        assert 'Process'   in labels
        assert 'Memory'    in labels
        assert 'Coherence' in labels

# ══════════════════════════════════════════════════════════════════
# /sparql (single file)
# ══════════════════════════════════════════════════════════════════

class TestSparqlEndpoint:

    @pytest.fixture(autouse=True)
    def preload(self, client):
        client.post('/load', json={'file_path': F_M2})

    def test_select_query(self, client):
        r = client.post('/sparql', json={
            'file_path': F_M2,
            'query': 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
                     'SELECT ?label WHERE { ?s rdfs:label ?label }'
        })
        assert r.status_code == 200
        data = r.json()
        assert data['query_type'] == 'SELECT'
        assert data['count'] >= 3

    def test_ask_query(self, client):
        r = client.post('/sparql', json={
            'file_path': F_M2,
            'query': 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
                     'ASK { ?s rdfs:label "Process" }'
        })
        assert r.status_code == 200
        assert r.json()['query_type'] == 'ASK'
        assert r.json()['result'] is True

    def test_invalid_sparql(self, client):
        r = client.post('/sparql', json={
            'file_path': F_M2,
            'query': 'THIS IS NOT SPARQL'
        })
        assert r.status_code == 400

    def test_unloaded_file(self, client):
        r = client.post('/sparql', json={
            'file_path': '/tmp/not_loaded.jsonld',
            'query': 'SELECT ?s WHERE { ?s ?p ?o }'
        })
        assert r.status_code == 404

# ══════════════════════════════════════════════════════════════════
# /hierarchy
# ══════════════════════════════════════════════════════════════════

class TestHierarchy:

    @pytest.fixture(autouse=True)
    def preload(self, client):
        client.post('/load', json={'file_path': F_EDU})

    def test_returns_pairs(self, client):
        r = client.get('/hierarchy', params={'file_path': F_EDU})
        assert r.status_code == 200
        data = r.json()
        assert 'pairs' in data

    def test_external_parents_present(self, client):
        """External parents (m2:Process, m2:Memory) must be in external_parents."""
        r = client.get('/hierarchy', params={'file_path': F_EDU})
        data = r.json()
        assert 'external_parents' in data
        ext_ids = [ep['id'] for ep in data['external_parents']]
        assert len(ext_ids) > 0

# ══════════════════════════════════════════════════════════════════
# /corpus/load  and  /corpus/sparql
# ══════════════════════════════════════════════════════════════════

class TestCorpusEndpoints:
    """
    Real API: single store 'default'. corpus_name in requests is accepted
    but ignored — always the same store. SPARQL returns corpus='default'.
    DELETE /corpus/{name} clears the whole store (always 200).
    SPARQL row keys: may be 'label' or '?label' depending on pyoxigraph version.
    Literal values include xsd type: '"Process"^^<xsd:string>'.
    """

    LOAD_BODY = {
        'corpus_name': 'default',
        'ontology_root': str(FIXTURES),
        'patterns': ['minimal_*.jsonld'],
        'recursive': False,
    }

    def _clean_label(self, v: str) -> str:
        """Strip quotes and xsd type suffix from pyoxigraph Literal string."""
        chars = '"' + "'"
        v = v.strip(chars)
        if '^^<' in v:
            v = v.split('^^<')[0].strip(chars)
        return v

    def test_corpus_load_status(self, client):
        r = client.post('/corpus/load', json=self.LOAD_BODY)
        assert r.status_code == 200

    def test_corpus_load_files_count(self, client):
        r = client.post('/corpus/load', json=self.LOAD_BODY)
        assert r.json()['files_loaded'] == 3

    def test_corpus_load_has_triples(self, client):
        r = client.post('/corpus/load', json=self.LOAD_BODY)
        assert r.json().get('total_triples', 0) > 0

    def test_corpus_list_has_default(self, client):
        client.post('/corpus/load', json=self.LOAD_BODY)
        r = client.get('/corpus/list')
        assert r.status_code == 200
        names = [c['name'] for c in r.json()['corpora']]
        assert 'default' in names

    def test_corpus_list_has_graphs_key(self, client):
        r = client.get('/corpus/list')
        assert 'graphs' in r.json()

    def test_corpus_sparql_status(self, client):
        client.post('/corpus/load', json=self.LOAD_BODY)
        r = client.post('/corpus/sparql', json={
            'corpus_name': 'default',
            'query': 'SELECT ?s WHERE { GRAPH ?g { ?s ?p ?o } } LIMIT 1'
        })
        assert r.status_code == 200

    def test_corpus_sparql_select_structure(self, client):
        client.post('/corpus/load', json=self.LOAD_BODY)
        r = client.post('/corpus/sparql', json={
            'corpus_name': 'default',
            'query': 'SELECT ?s WHERE { GRAPH ?g { ?s ?p ?o } } LIMIT 1'
        })
        data = r.json()
        assert data['query_type'] == 'SELECT'
        assert 'results' in data
        assert 'count' in data

    def test_corpus_sparql_finds_labels(self, client):
        client.post('/corpus/load', json=self.LOAD_BODY)
        r = client.post('/corpus/sparql', json={
            'corpus_name': 'default',
            'query': (
                'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
                'SELECT ?label WHERE { GRAPH ?g { ?s rdfs:label ?label } }'
            )
        })
        data = r.json()
        assert data['count'] > 0
        row = data['results'][0]
        # Key may be 'label' or '?label'
        key = 'label' if 'label' in row else '?label'
        labels = {self._clean_label(r[key]) for r in data['results']}
        assert 'Process' in labels

    def test_corpus_sparql_invalid_query(self, client):
        r = client.post('/corpus/sparql', json={
            'corpus_name': 'default',
            'query': 'THIS IS NOT SPARQL'
        })
        assert r.status_code == 400

    def test_corpus_delete_ok(self, client):
        r = client.delete('/corpus/anything')
        assert r.status_code == 200
