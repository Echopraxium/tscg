"""
TSCG Engine RAG - Retrieval-Augmented Generation

This module provides RAG capabilities for TSCG ontologies and system models:
- Semantic search over ontologies
- Vector embeddings for metaconcepts and poclets
- Contextual retrieval for LLM augmentation
- Knowledge base indexing

Author: Echopraxium with the collaboration of Claude AI
"""

from .retrieval import OntologyRetriever, MetaconceptRetriever
from .embeddings import TSCGEmbedder
from .vector_store import VectorStore

__all__ = [
    'OntologyRetriever',
    'MetaconceptRetriever',
    'TSCGEmbedder',
    'VectorStore'
]
