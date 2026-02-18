"""
RAG Facade - Public API for Retrieval-Augmented Generation

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import List, Optional, Tuple
from pathlib import Path

from ..core.models import Metaconcept
from ..core.ontology_loader import OntologyLoader
from ..rag.retrieval import (
    OntologyRetriever,
    MetaconceptRetriever,
    RetrievalConfig
)
from ..rag.embeddings import TSCGEmbedder, EmbeddingConfig
from ..rag.vector_store import VectorStore, SearchResult


class RAGFacade:
    """
    Public API for RAG (Retrieval-Augmented Generation) operations.
    
    Provides semantic search over TSCG ontologies and system models
    using vector embeddings and similarity search.
    
    Example:
        >>> rag = RAGFacade()
        >>> rag.index_ontology(loader)
        >>> results = rag.search("feedback control mechanisms")
        >>> for result in results:
        ...     print(f"{result.metadata['label']}: {result.score:.3f}")
    """
    
    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        top_k: int = 5,
        min_score: float = 0.5
    ):
        """
        Initialize RAG facade.
        
        Args:
            embedding_model: Sentence transformer model name
            top_k: Default number of results to return
            min_score: Minimum similarity score threshold
        """
        # Create configuration
        embedding_config = EmbeddingConfig(model=embedding_model)
        retrieval_config = RetrievalConfig(
            embedding_config=embedding_config,
            top_k=top_k,
            min_score=min_score
        )
        
        # Initialize components
        self.embedder = TSCGEmbedder(embedding_config)
        self.ontology_retriever = OntologyRetriever(retrieval_config)
        self.metaconcept_retriever = MetaconceptRetriever(retrieval_config)
        self._indexed = False
    
    def index_ontology(self, loader: OntologyLoader):
        """
        Index all loaded ontologies for semantic search.
        
        Creates vector embeddings for all metaconcepts and stores
        them in the vector database.
        
        Args:
            loader: OntologyLoader with loaded ontologies
        """
        # Index with ontology retriever
        self.ontology_retriever.index_ontology(loader)
        
        # Also add to metaconcept retriever
        metaconcepts = loader.get_metaconcepts()
        self.metaconcept_retriever.add_metaconcepts(metaconcepts)
        
        self._indexed = True
    
    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        layer: Optional[str] = None,
        perspective: Optional[str] = None
    ) -> List[SearchResult]:
        """
        Semantic search for metaconcepts.
        
        Args:
            query: Natural language query
            top_k: Number of results to return
            layer: Filter by layer (M3, M2, M1, M0)
            perspective: Filter by perspective (EagleEye, SphinxEye)
        
        Returns:
            List of SearchResult objects with similarity scores
        
        Raises:
            RuntimeError: If no ontologies have been indexed
        """
        if not self._indexed:
            raise RuntimeError(
                "No ontologies indexed. Call index_ontology() first."
            )
        
        return self.ontology_retriever.search(
            query,
            top_k=top_k,
            layer=layer,
            perspective=perspective
        )
    
    def search_metaconcepts(
        self,
        query: str,
        top_k: Optional[int] = None,
        layer: Optional[str] = None
    ) -> List[Tuple[Metaconcept, float]]:
        """
        Search metaconcepts with full object return.
        
        Args:
            query: Natural language query
            top_k: Number of results
            layer: Filter by layer
        
        Returns:
            List of (Metaconcept, similarity_score) tuples
        """
        if not self._indexed:
            raise RuntimeError(
                "No ontologies indexed. Call index_ontology() first."
            )
        
        return self.metaconcept_retriever.search(query, top_k, layer)
    
    def search_by_formula(
        self,
        formula: str,
        top_k: Optional[int] = None
    ) -> List[Tuple[Metaconcept, float]]:
        """
        Search metaconcepts by tensor formula pattern.
        
        Args:
            formula: Tensor formula pattern (e.g., "A⊗S", "It⊗Im")
            top_k: Number of results
        
        Returns:
            List of (Metaconcept, similarity_score) tuples
        """
        if not self._indexed:
            raise RuntimeError(
                "No ontologies indexed. Call index_ontology() first."
            )
        
        return self.metaconcept_retriever.search_by_formula(formula, top_k)
    
    def find_similar(
        self,
        metaconcept_uri: str,
        top_k: Optional[int] = None
    ) -> List[SearchResult]:
        """
        Find metaconcepts similar to a given one.
        
        Args:
            metaconcept_uri: URI of the reference metaconcept
            top_k: Number of similar metaconcepts to find
        
        Returns:
            List of SearchResult objects
        """
        if not self._indexed:
            raise RuntimeError(
                "No ontologies indexed. Call index_ontology() first."
            )
        
        return self.ontology_retriever.find_similar(metaconcept_uri, top_k)
    
    def get_metaconcepts_by_layer(self, layer: str) -> List[Metaconcept]:
        """
        Get all indexed metaconcepts for a specific layer.
        
        Args:
            layer: Layer (M3, M2, M1, M0)
        
        Returns:
            List of Metaconcept objects
        """
        return self.metaconcept_retriever.get_by_layer(layer)
    
    def save_index(self, filepath: str):
        """
        Save the vector index to disk for later use.
        
        Args:
            filepath: Path to save index (without extension)
        """
        self.ontology_retriever.save_index(filepath)
    
    def load_index(self, filepath: str):
        """
        Load a previously saved vector index.
        
        Args:
            filepath: Path to index file (without extension)
        """
        self.ontology_retriever.load_index(filepath)
        self._indexed = True
    
    def get_stats(self) -> dict:
        """
        Get statistics about the indexed content.
        
        Returns:
            Dictionary with indexing statistics
        """
        return {
            "indexed": self._indexed,
            "metaconcept_count": self.ontology_retriever.get_indexed_count(),
            "embedding_dimension": self.embedder.config.dimension,
            "embedding_model": self.embedder.config.model
        }
