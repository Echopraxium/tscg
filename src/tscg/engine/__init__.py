"""
TSCG Engine - Core business logic and analysis engine

Provides:
- Ontology loading and manipulation
- SPARQL query execution
- Metrics computation
- Export capabilities
- RAG (Retrieval-Augmented Generation)
- Mathematical operations (future)
- OWL reasoning (future)

Public API via tscg.engine.facade module.

Author: Echopraxium with the collaboration of Claude AI
"""

__version__ = "0.1.0"

# Public API imports for convenience
from .facade import (
    OntologyFacade,
    QueryFacade,
    MetricsFacade,
    ExportFacade,
    RAGFacade
)

__all__ = [
    'OntologyFacade',
    'QueryFacade',
    'MetricsFacade',
    'ExportFacade',
    'RAGFacade'
]
