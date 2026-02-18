"""
TSCG Retrieval - Semantic search over ontologies and system models

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ..core.models import Metaconcept, Poclet
from ..core.ontology_loader import OntologyLoader
from .embeddings import TSCGEmbedder, EmbeddingConfig
from .vector_store import VectorStore, SearchResult


@dataclass
class RetrievalConfig:
    """Configuration for retrieval system"""
    embedding_config: EmbeddingConfig = EmbeddingConfig()
    top_k: int = 5
    min_score: float = 0.5  # Minimum cosine similarity


class OntologyRetriever:
    """
    Semantic search over loaded ontologies.
    
    Indexes all loaded ontologies and enables semantic search
    for metaconcepts, properties, and instances.
    
    Example:
        >>> retriever = OntologyRetriever()
        >>> retriever.index_ontology(loader)
        >>> results = retriever.search("system feedback control")
    """
    
    def __init__(self, config: Optional[RetrievalConfig] = None):
        """
        Initialize retriever.
        
        Args:
            config: Optional retrieval configuration
        """
        self.config = config or RetrievalConfig()
        self.embedder = TSCGEmbedder(self.config.embedding_config)
        self.vector_store = VectorStore(
            dimension=self.config.embedding_config.dimension
        )
        self._indexed_count = 0
    
    def index_ontology(self, loader: OntologyLoader):
        """
        Index all ontologies from a loader.
        
        Creates embeddings for all metaconcepts and stores them
        in the vector store for efficient search.
        
        Args:
            loader: OntologyLoader with loaded ontologies
        """
        metaconcepts = loader.get_metaconcepts()
        
        for mc in metaconcepts:
            # Generate embedding
            embedding = self.embedder.embed_metaconcept(mc)
            
            # Store with metadata
            metadata = {
                "type": "metaconcept",
                "label": mc.label,
                "layer": mc.layer,
                "uri": mc.uri,
                "perspective": mc.perspective,
                "tensor_formula": mc.tensor_formula
            }
            
            self.vector_store.add(mc.uri, embedding, metadata)
            self._indexed_count += 1
        
        print(f"Indexed {self._indexed_count} metaconcepts")
    
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
            top_k: Number of results (default from config)
            layer: Filter by layer (M3, M2, M1, M0)
            perspective: Filter by perspective (EagleEye, SphinxEye)
        
        Returns:
            List of SearchResult objects
        """
        top_k = top_k or self.config.top_k
        
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        
        # Build filter function
        def filter_fn(metadata):
            if layer and metadata.get('layer') != layer:
                return False
            if perspective and metadata.get('perspective') != perspective:
                return False
            return True
        
        # Search
        results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
            filter_fn=filter_fn if (layer or perspective) else None
        )
        
        # Filter by minimum score
        results = [r for r in results if r.score >= self.config.min_score]
        
        return results
    
    def find_similar(
        self,
        metaconcept_uri: str,
        top_k: Optional[int] = None
    ) -> List[SearchResult]:
        """
        Find metaconcepts similar to a given one.
        
        Args:
            metaconcept_uri: URI of the metaconcept
            top_k: Number of results
        
        Returns:
            List of similar metaconcepts
        """
        top_k = top_k or self.config.top_k
        
        # Get embedding
        result = self.vector_store.get(metaconcept_uri)
        if not result:
            raise ValueError(f"Metaconcept not found: {metaconcept_uri}")
        
        embedding, _ = result
        
        # Search (exclude self)
        results = self.vector_store.search(embedding, top_k=top_k + 1)
        results = [r for r in results if r.id != metaconcept_uri]
        
        return results[:top_k]
    
    def get_indexed_count(self) -> int:
        """Get number of indexed metaconcepts"""
        return self._indexed_count
    
    def save_index(self, filepath: str):
        """Save index to disk"""
        self.vector_store.save(filepath)
    
    def load_index(self, filepath: str):
        """Load index from disk"""
        self.vector_store.load(filepath)
        self._indexed_count = self.vector_store.count()


class MetaconceptRetriever:
    """
    Specialized retriever for metaconcept search.
    
    Provides advanced search capabilities specifically for
    TSCG metaconcepts, including formula-based search,
    layer-specific search, and dimensional analysis.
    
    Example:
        >>> retriever = MetaconceptRetriever()
        >>> retriever.add_metaconcepts(metaconcepts)
        >>> results = retriever.search_by_formula("A⊗S")
    """
    
    def __init__(self, config: Optional[RetrievalConfig] = None):
        """Initialize metaconcept retriever"""
        self.config = config or RetrievalConfig()
        self.embedder = TSCGEmbedder(self.config.embedding_config)
        self.vector_store = VectorStore(
            dimension=self.config.embedding_config.dimension
        )
        self.metaconcepts: Dict[str, Metaconcept] = {}
    
    def add_metaconcept(self, metaconcept: Metaconcept):
        """
        Add a metaconcept to the index.
        
        Args:
            metaconcept: Metaconcept to add
        """
        # Generate embedding
        embedding = self.embedder.embed_metaconcept(metaconcept)
        
        # Store
        metadata = {
            "label": metaconcept.label,
            "layer": metaconcept.layer,
            "tensor_formula": metaconcept.tensor_formula
        }
        
        self.vector_store.add(metaconcept.uri, embedding, metadata)
        self.metaconcepts[metaconcept.uri] = metaconcept
    
    def add_metaconcepts(self, metaconcepts: List[Metaconcept]):
        """Add multiple metaconcepts"""
        for mc in metaconcepts:
            self.add_metaconcept(mc)
    
    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        layer: Optional[str] = None
    ) -> List[Tuple[Metaconcept, float]]:
        """
        Search metaconcepts by natural language query.
        
        Args:
            query: Query string
            top_k: Number of results
            layer: Filter by layer
        
        Returns:
            List of (Metaconcept, score) tuples
        """
        top_k = top_k or self.config.top_k
        
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        
        # Build filter
        filter_fn = None
        if layer:
            filter_fn = lambda meta: meta.get('layer') == layer
        
        # Search
        results = self.vector_store.search(
            query_embedding,
            top_k=top_k,
            filter_fn=filter_fn
        )
        
        # Return metaconcepts with scores
        return [
            (self.metaconcepts[r.id], r.score)
            for r in results
            if r.id in self.metaconcepts and r.score >= self.config.min_score
        ]
    
    def search_by_formula(
        self,
        formula_pattern: str,
        top_k: Optional[int] = None
    ) -> List[Tuple[Metaconcept, float]]:
        """
        Search metaconcepts by tensor formula pattern.
        
        Args:
            formula_pattern: Pattern to match (e.g., "A⊗S", "It⊗Im")
            top_k: Number of results
        
        Returns:
            List of (Metaconcept, score) tuples
        """
        # Search using formula as query
        query_text = f"Tensor formula: {formula_pattern}"
        return self.search(query_text, top_k=top_k)
    
    def get_by_layer(self, layer: str) -> List[Metaconcept]:
        """
        Get all metaconcepts for a specific layer.
        
        Args:
            layer: Layer (M3, M2, M1, M0)
        
        Returns:
            List of metaconcepts
        """
        return [
            mc for mc in self.metaconcepts.values()
            if mc.layer == layer
        ]
