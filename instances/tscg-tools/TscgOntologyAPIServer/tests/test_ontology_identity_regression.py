"""
test_ontology_identity_regression.py — Ontology-identity guard (PEPITE-RT-008).

A governed owl:Ontology subject must be declared in exactly ONE active-corpus
graph. This guards the defect class where a sidecar/reference copy re-declares a
canonical subject from a second graph (PEPITE-RT-008:
ontology/tools/M2_MetaConcepts_Ref.jsonld re-declared m2:M2_GenericConcepts).

Loads every active-corpus *.jsonld (same scope as the running server) into a
fresh in-memory TscgStore and asserts no owl:Ontology subject spans >1 graph.

Author: Echopraxium with the collaboration of Claude AI
"""
import sys
import pathlib
import pytest

SRC_DIR = pathlib.Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(SRC_DIR))
from tscg_api_server import TscgStore

# tests/ -> TscgOntologyAPIServer -> tscg-tools -> instances -> REPO ROOT
REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
SCAN_ROOTS = ('ontology', 'instances')

# Track production scope exactly by importing the server's own filter.
try:
    from tscg_api_server import _in_active_corpus
except Exception:  # pragma: no cover — mirrors _OUT_OF_SCOPE as of HEAD
    _OUT_OF_SCOPE = (
        'migration_backups/', 'domain_format_fix_backups/', '_archives/',
        'docs/', '/static/', '/Ref/', 'reboot-kit/', '.pytest_cache/',
    )

    def _in_active_corpus(path: str) -> bool:
        p = str(path).replace('\\', '/')
        return not any(m in p for m in _OUT_OF_SCOPE)


def _active_jsonld_files():
    out = []
    for root in SCAN_ROOTS:
        base = REPO_ROOT / root
        if base.is_dir():
            for f in base.rglob('*.jsonld'):
                if _in_active_corpus(f.relative_to(REPO_ROOT).as_posix()):
                    out.append(f)
    return out


_DUP_ONTOLOGY = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?ont (COUNT(DISTINCT ?g) AS ?n)
WHERE { GRAPH ?g { ?ont a owl:Ontology } }
GROUP BY ?ont
HAVING (COUNT(DISTINCT ?g) > 1)
"""


@pytest.mark.skipif(not (REPO_ROOT / 'ontology').is_dir(),
                    reason='full repo checkout not available')
def test_no_owl_ontology_subject_spans_multiple_graphs():
    files = _active_jsonld_files()
    assert files, 'no active-corpus .jsonld found — check REPO_ROOT / scan scope'

    store = TscgStore()
    load_failures = []
    for f in files:
        try:
            store.load_file(str(f))
        except Exception as exc:  # load integrity is a different test's concern
            load_failures.append(f'{f.relative_to(REPO_ROOT).as_posix()}: {exc}')

    offenders = []
    for r in store.query(_DUP_ONTOLOGY):
        ont = getattr(r['ont'], 'value', str(r['ont']))
        n = getattr(r['n'], 'value', str(r['n']))
        offenders.append(f'{ont} -> {n} graphs')

    assert not offenders, (
        'owl:Ontology subject(s) in more than one active-corpus graph:\n'
        + '\n'.join('  - ' + o for o in offenders)
        + (f'\n({len(load_failures)} file(s) failed to load)' if load_failures else '')
    )
