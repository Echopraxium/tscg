"""
Tests for TSCG Engine Facades

Author: Echopraxium with the collaboration of Claude AI
"""

import pytest
from pathlib import Path
from tscg.engine.facade import OntologyFacade, QueryFacade, MetricsFacade, ExportFacade
from tscg.engine.core.models import ASFIDScore, REVOIScore


def test_ontology_facade_creation():
    """Test creating an OntologyFacade"""
    facade = OntologyFacade()
    assert facade is not None
    assert len(facade.list_loaded()) == 0


def test_asfid_score_overall():
    """Test ASFID score calculation"""
    asfid = ASFIDScore(
        attractor=0.9,
        structure=0.8,
        flow=0.9,
        information=0.85,
        dynamics=0.9
    )
    
    assert asfid.overall == pytest.approx(0.87, abs=0.01)


def test_revoi_score_overall():
    """Test REVOI score calculation"""
    revoi = REVOIScore(
        representability=0.9,
        evolvability=0.8,
        verifiability=0.85,
        observability=0.9,
        interoperability=0.85
    )
    
    assert revoi.overall == pytest.approx(0.86, abs=0.01)


def test_metrics_facade_creation():
    """Test creating a MetricsFacade"""
    facade = MetricsFacade()
    assert facade is not None


def test_export_facade_creation():
    """Test creating an ExportFacade"""
    facade = ExportFacade()
    assert facade is not None


# Integration tests (requires actual ontology files)

@pytest.mark.skipif(
    not Path("/mnt/project/M3_EagleEye.jsonld").exists(),
    reason="M3_EagleEye.jsonld not found in project"
)
def test_load_ontology_integration():
    """Integration test: load M3_EagleEye ontology"""
    facade = OntologyFacade()
    graph = facade.load("/mnt/project/M3_EagleEye.jsonld")
    
    assert graph is not None
    assert len(graph) > 0
    assert "M3_EagleEye" in facade.list_loaded()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
