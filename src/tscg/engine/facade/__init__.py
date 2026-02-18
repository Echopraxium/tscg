"""
TSCG Engine Facade - Public API

This module provides the stable public interface for TSCG Engine.
All public operations should go through these facade classes.

Author: Echopraxium with the collaboration of Claude AI
"""

from .ontology import OntologyFacade
from .query import QueryFacade
from .metrics import MetricsFacade
from .export import ExportFacade

__all__ = [
    'OntologyFacade',
    'QueryFacade',
    'MetricsFacade',
    'ExportFacade'
]
from .rag import RAGFacade

__all__.append('RAGFacade')
