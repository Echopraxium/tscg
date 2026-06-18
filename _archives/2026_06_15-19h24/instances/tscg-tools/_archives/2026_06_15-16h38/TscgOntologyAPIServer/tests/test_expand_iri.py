"""
test_expand_iri.py — Unit tests for _expand_iri (tscg_api_server.py).
Migrated from tscg-python-bridge/tests/test_expand_iri.py.

Covers all three strategies:
  Strategy 1 — Longest exact prefix match
  Strategy 2 — Shared namespace inference (dotted prefixes)
  Strategy 3 — @base fallback

Author: Echopraxium with the collaboration of Claude AI
"""
import sys
import pathlib
import pytest

SRC_DIR = pathlib.Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(SRC_DIR))
from tscg_api_server import _expand_iri

BASE = 'https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/'


# ══════════════════════════════════════════════════════════════════
# Strategy 1 — Longest exact prefix match
# ══════════════════════════════════════════════════════════════════

class TestStrategy1ExactPrefix:

    def test_simple_m2_prefix(self):
        ctx = {'m2': 'M2_GenericConcepts.jsonld#'}
        assert _expand_iri('m2:Process', ctx, BASE) == \
               BASE + 'M2_GenericConcepts.jsonld#Process'

    def test_m1_edu_compound_prefix(self):
        """m1:edu prefix with colon — Strategy 1 should match."""
        ctx = {'m1:edu': 'M1_extensions/education/M1_Education.jsonld#'}
        result = _expand_iri('m1:edu:PedagogicalStrategy', ctx, BASE)
        assert result == BASE + 'M1_extensions/education/M1_Education.jsonld#PedagogicalStrategy'

    def test_m1_edu_vs_m1_ambiguity(self):
        """Longer prefix m1:edu must win over shorter m1."""
        ctx = {
            'm1':     'M1_CoreConcepts.jsonld#',
            'm1:edu': 'M1_extensions/education/M1_Education.jsonld#',
        }
        result = _expand_iri('m1:edu:LearningTheory', ctx, BASE)
        assert 'M1_Education.jsonld' in result
        assert 'LearningTheory' in result

    def test_absolute_prefix_uri(self):
        """Prefix that already has http:// — must not double-expand."""
        ctx = {'owl': 'http://www.w3.org/2002/07/owl#'}
        assert _expand_iri('owl:Class', ctx, BASE) == \
               'http://www.w3.org/2002/07/owl#Class'

    def test_rdfs_prefix(self):
        ctx = {'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'}
        assert _expand_iri('rdfs:label', ctx, BASE) == \
               'http://www.w3.org/2000/01/rdf-schema#label'

    def test_relative_prefix_resolved_against_base(self):
        """Relative prefix URI resolved against @base."""
        ctx = {'m2': 'M2_GenericConcepts.jsonld#'}
        result = _expand_iri('m2:Coherence', ctx, BASE)
        assert result.startswith('https://')
        assert 'M2_GenericConcepts.jsonld#Coherence' in result


# ══════════════════════════════════════════════════════════════════
# Strategy 2 — Shared namespace inference (dotted prefixes)
# ══════════════════════════════════════════════════════════════════

class TestStrategy2SharedNamespace:

    def test_chemistry_dotted_prefix(self):
        CHEM_URI = BASE + 'M1_extensions/chemistry/M1_Chemistry.jsonld#'
        ctx = {'m1.ext:chemistry:chemistry': CHEM_URI}
        result = _expand_iri('m1.ext:chemistry:ChemicalReaction', ctx, '')
        assert result == CHEM_URI + 'ChemicalReaction'

    def test_chemistry_combustion(self):
        CHEM_URI = BASE + 'M1_extensions/chemistry/M1_Chemistry.jsonld#'
        ctx = {'m1.ext:chemistry:chemistry': CHEM_URI}
        result = _expand_iri('m1.ext:chemistry:Combustion', ctx, '')
        assert result == CHEM_URI + 'Combustion'

    def test_strategy2_does_not_match_unrelated(self):
        """Strategy 2 must not match when namespace parts differ."""
        ctx = {'m1.ext:chemistry:chemistry': 'https://example.com/chemistry#'}
        result = _expand_iri('m1.ext:biology:Cell', ctx, '')
        assert 'chemistry' not in result


# ══════════════════════════════════════════════════════════════════
# Strategy 3 — @base fallback
# ══════════════════════════════════════════════════════════════════

class TestStrategy3BaseFallback:

    def test_bare_name_with_base(self):
        result = _expand_iri('SomeClass', {}, BASE)
        assert result == BASE + 'SomeClass'

    def test_relative_iri_with_base(self):
        result = _expand_iri('./M1_Biology.jsonld', {}, BASE)
        assert result.startswith('https://')

    def test_no_prefix_no_base_returns_as_is(self):
        """When no context and no base — return unchanged (graceful degradation)."""
        result = _expand_iri('UnresolvableTerm', {}, '')
        assert result == 'UnresolvableTerm'


# ══════════════════════════════════════════════════════════════════
# Edge cases
# ══════════════════════════════════════════════════════════════════

class TestEdgeCases:

    def test_already_absolute_iri_unchanged(self):
        iri = 'http://www.w3.org/2002/07/owl#Class'
        assert _expand_iri(iri, {}, BASE) == iri

    def test_https_iri_unchanged(self):
        iri = BASE + 'M2.jsonld#Process'
        assert _expand_iri(iri, {}, BASE) == iri

    def test_empty_string_returns_empty(self):
        assert _expand_iri('', {}, BASE) == ''

    def test_none_returns_none(self):
        assert _expand_iri(None, {}, BASE) is None

    def test_owl_thing_valid(self):
        ctx = {'owl': 'http://www.w3.org/2002/07/owl#'}
        result = _expand_iri('owl:Thing', ctx, BASE)
        assert result == 'http://www.w3.org/2002/07/owl#Thing'

    def test_empty_context_uses_base(self):
        result = _expand_iri('m2:Process', {}, BASE)
        assert result == BASE + 'm2:Process'

    def test_prefix_with_empty_uri_skipped(self):
        """Empty prefix URI in context must not produce invalid IRI."""
        ctx = {'m2': ''}
        result = _expand_iri('m2:Process', ctx, BASE)
        assert result != 'Process'
        assert 'Process' in result
