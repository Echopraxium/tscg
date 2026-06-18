"""
conftest.py — Shared pytest fixtures for TscgOntologyAPIServer tests.
Migrated from tscg-python-bridge/tests/conftest.py (bridge_server → tscg_api_server).

Author: Echopraxium with the collaboration of Claude AI
"""
import sys
import pathlib
import pytest

# ── Make tscg_api_server importable from tests/ ───────────────────
SRC_DIR  = pathlib.Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(SRC_DIR))

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
    from tscg_api_server import TscgStore
    return TscgStore()

@pytest.fixture
def store_with_m2(empty_store, fixture_m2):
    empty_store.load_file(fixture_m2)
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
    import tscg_api_server
    from tscg_api_server import app, TscgStore

    # Initialise _tscg_store so endpoints return 200, not 503
    if tscg_api_server._tscg_store is None:
        tscg_api_server._tscg_store = TscgStore()   # in-memory

    with TestClient(app) as c:
        yield c
