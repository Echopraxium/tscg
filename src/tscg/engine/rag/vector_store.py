"""
Vector Store - Store and search embeddings

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import List, Dict, Tuple, Optional, Any
import numpy as np
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class SearchResult:
    """Result from vector similarity search"""
    id: str
    score: float  # Cosine similarity score
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None


class VectorStore:
    """
    In-memory vector store for semantic search.
    
    Stores embeddings with metadata and provides similarity search.
    Future: Can be backed by FAISS, Chroma, or other vector databases.
    
    Example:
        >>> store = VectorStore(dimension=384)
        >>> store.add("mc_001", embedding, {"label": "Attractor", "layer": "M3"})
        >>> results = store.search(query_embedding, top_k=5)
    """
    
    def __init__(self, dimension: int = 384):
        """
        Initialize vector store.
        
        Args:
            dimension: Embedding dimension
        """
        self.dimension = dimension
        self.vectors: Dict[str, np.ndarray] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
    
    def add(
        self,
        id: str,
        embedding: np.ndarray,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add embedding to store.
        
        Args:
            id: Unique identifier
            embedding: Embedding vector
            metadata: Optional metadata dictionary
        """
        if embedding.shape[0] != self.dimension:
            raise ValueError(
                f"Embedding dimension {embedding.shape[0]} "
                f"doesn't match store dimension {self.dimension}"
            )
        
        self.vectors[id] = embedding
        self.metadata[id] = metadata or {}
    
    def add_batch(
        self,
        ids: List[str],
        embeddings: np.ndarray,
        metadata: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Add multiple embeddings efficiently.
        
        Args:
            ids: List of unique identifiers
            embeddings: Matrix of embeddings (shape: [n, dimension])
            metadata: Optional list of metadata dictionaries
        """
        if len(ids) != embeddings.shape[0]:
            raise ValueError("Number of IDs must match number of embeddings")
        
        metadata = metadata or [{} for _ in ids]
        
        for id, embedding, meta in zip(ids, embeddings, metadata):
            self.add(id, embedding, meta)
    
    def search(
        self,
        query: np.ndarray,
        top_k: int = 5,
        filter_fn: Optional[callable] = None
    ) -> List[SearchResult]:
        """
        Search for most similar vectors.
        
        Args:
            query: Query embedding
            top_k: Number of results to return
            filter_fn: Optional function to filter results by metadata
                      (e.g., lambda meta: meta['layer'] == 'M3')
        
        Returns:
            List of SearchResult objects, sorted by similarity (high to low)
        """
        if len(self.vectors) == 0:
            return []
        
        # Compute cosine similarities
        similarities = []
        for id, vector in self.vectors.items():
            # Apply filter if provided
            if filter_fn and not filter_fn(self.metadata[id]):
                continue
            
            # Cosine similarity
            similarity = np.dot(query, vector) / (
                np.linalg.norm(query) * np.linalg.norm(vector)
            )
            similarities.append((id, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k results
        results = []
        for id, score in similarities[:top_k]:
            results.append(SearchResult(
                id=id,
                score=float(score),
                metadata=self.metadata[id],
                embedding=self.vectors[id]
            ))
        
        return results
    
    def get(self, id: str) -> Optional[Tuple[np.ndarray, Dict[str, Any]]]:
        """
        Get embedding and metadata by ID.
        
        Args:
            id: Identifier
        
        Returns:
            Tuple of (embedding, metadata) or None if not found
        """
        if id not in self.vectors:
            return None
        
        return self.vectors[id], self.metadata[id]
    
    def delete(self, id: str):
        """
        Remove embedding from store.
        
        Args:
            id: Identifier to remove
        """
        if id in self.vectors:
            del self.vectors[id]
            del self.metadata[id]
    
    def count(self) -> int:
        """Get number of vectors in store"""
        return len(self.vectors)
    
    def list_ids(self) -> List[str]:
        """Get all IDs in store"""
        return list(self.vectors.keys())
    
    def save(self, filepath: str):
        """
        Save store to disk.
        
        Args:
            filepath: Path to save file (.npz for vectors, .json for metadata)
        """
        path = Path(filepath)
        
        # Save vectors
        np.savez_compressed(
            path.with_suffix('.npz'),
            **self.vectors
        )
        
        # Save metadata
        with open(path.with_suffix('.json'), 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def load(self, filepath: str):
        """
        Load store from disk.
        
        Args:
            filepath: Path to load file (without extension)
        """
        path = Path(filepath)
        
        # Load vectors
        vectors_data = np.load(path.with_suffix('.npz'))
        self.vectors = {key: vectors_data[key] for key in vectors_data.files}
        
        # Load metadata
        with open(path.with_suffix('.json'), 'r') as f:
            self.metadata = json.load(f)
    
    def clear(self):
        """Clear all vectors and metadata"""
        self.vectors.clear()
        self.metadata.clear()
