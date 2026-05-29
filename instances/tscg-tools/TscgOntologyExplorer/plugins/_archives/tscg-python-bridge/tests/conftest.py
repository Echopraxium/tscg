"""
conftest.py — Shared pytest fixtures for TscgOntologyExplorer bridge tests.
Author: Echopraxium with the collaboration of Claude AI
"""
import sys
import pathlib
import pytest

# ── Make bridge_server importable ──────────────────────────────────
BRIDGE_DIR = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(BRIDGE_DIR))

FIXTURES = pathlib.Path(__file__).parent / 'fixtures'

# ── Constants ──────────────────────────────────────────────────────
BASE_URI  = 'https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/'
OWL_THING = 'http://www.w3.org/2002/07/owl#Thing'

# ── Fixture paths ──────────────────────────────────────────────────
@pytest.fixture
def fixture_m2():
    return str(FIXTURES / 'minimal_m2.jsonld')

@pytest.fixture
def fixture_m1_edu():
    return str(FIXTURES / 'minimal_m1_edu.jsonld')

@pytest.fixture
def fixture_m1_chem():
    return str(FIXTURES / 'minimal_m1_chem.jsonld')

@pytest.fixture
def fixtures_dir():
    return FIXTURES

# ── TscgStore (in-memory) ──────────────────────────────────────────
@pytest.fixture
def empty_store():
    from bridge_server import TscgStore
    return TscgStore()

@pytest.fixture
def store_with_m2(empty_store, fixture_m2):
    empty_store.load_file(fixture_m2)   # graph_uri auto-calculated
    return empty_store

@pytest.fixture
def store_two_graphs(empty_store, fixture_m2, fixture_m1_edu):
    empty_store.load_file(fixture_m2)
    empty_store.load_file(fixture_m1_edu)
    return empty_store

# ── FastAPI TestClient ─────────────────────────────────────────────
@pytest.fixture(scope='session')
def client():
    from fastapi.testclient import TestClient
    import bridge_server
    from bridge_server import app, TscgStore

    # Initialize _tscg_store so corpus endpoints return 200, not 503
    if bridge_server._tscg_store is None:
        bridge_server._tscg_store = TscgStore()   # in-memory store

    with TestClient(app) as c:
        yield c
