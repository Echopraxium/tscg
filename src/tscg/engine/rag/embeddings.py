"""
TSCG Embedder - Generate semantic embeddings for TSCG entities

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import List, Dict, Optional
import numpy as np
from dataclasses import dataclass

from ..core.models import Metaconcept, Poclet, ASFIDScore, REVOIScore


@dataclass
class EmbeddingConfig:
    """Configuration for embedding generation"""
    model: str = "sentence-transformers/all-MiniLM-L6-v2"
    dimension: int = 384
    normalize: bool = True


class TSCGEmbedder:
    """
    Generate semantic embeddings for TSCG entities.
    
    Supports:
    - Metaconcepts (based on label, definition, formula)
    - Poclets (based on description, instances)
    - ASFID/REVOI scores (numerical embeddings)
    
    Example:
        >>> embedder = TSCGEmbedder()
        >>> embedding = embedder.embed_metaconcept(metaconcept)
        >>> # embedding is 384-dimensional vector
    """
    
    def __init__(self, config: Optional[EmbeddingConfig] = None):
        """
        Initialize embedder.
        
        Args:
            config: Optional embedding configuration
        """
        self.config = config or EmbeddingConfig()
        self._model = None  # Lazy load
    
    def _load_model(self):
        """Lazy load embedding model"""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.config.model)
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. "
                    "Install with: pip install sentence-transformers"
                )
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector (normalized if config.normalize=True)
        """
        self._load_model()
        embedding = self._model.encode(text, convert_to_numpy=True)
        
        if self.config.normalize:
            embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def embed_metaconcept(self, metaconcept: Metaconcept) -> np.ndarray:
        """
        Generate embedding for a metaconcept.
        
        Combines:
        - Label
        - Definition (if available)
        - Tensor formula (if available)
        - Layer information
        
        Args:
            metaconcept: Metaconcept to embed
        
        Returns:
            Embedding vector
        """
        # Build text representation
        text_parts = [metaconcept.label]
        
        if metaconcept.definition:
            text_parts.append(metaconcept.definition)
        
        if metaconcept.tensor_formula:
            text_parts.append(f"Formula: {metaconcept.tensor_formula}")
        
        text_parts.append(f"Layer: {metaconcept.layer}")
        
        if metaconcept.perspective:
            text_parts.append(f"Perspective: {metaconcept.perspective}")
        
        combined_text = " | ".join(text_parts)
        return self.embed_text(combined_text)
    
    def embed_poclet(self, poclet: Poclet) -> np.ndarray:
        """
        Generate embedding for a poclet.
        
        Combines:
        - Name
        - Description
        - Domain
        - ASFID/REVOI scores
        
        Args:
            poclet: Poclet to embed
        
        Returns:
            Embedding vector
        """
        text_parts = [poclet.name]
        
        if poclet.description:
            text_parts.append(poclet.description)
        
        if poclet.domain:
            text_parts.append(f"Domain: {poclet.domain}")
        
        # Add score information
        if poclet.asfid_scores:
            text_parts.append(f"ASFID: {poclet.asfid_scores.overall:.2f}")
        
        if poclet.revoi_scores:
            text_parts.append(f"REVOI: {poclet.revoi_scores.overall:.2f}")
        
        combined_text = " | ".join(text_parts)
        return self.embed_text(combined_text)
    
    def embed_asfid(self, asfid: ASFIDScore) -> np.ndarray:
        """
        Generate embedding from ASFID scores.
        
        Creates a numerical embedding directly from scores.
        Pads to match model dimension if needed.
        
        Args:
            asfid: ASFID scores
        
        Returns:
            Embedding vector
        """
        # Create 5D vector from scores
        scores_vector = np.array([
            asfid.attractor,
            asfid.structure,
            asfid.flow,
            asfid.information,
            asfid.dynamics
        ])
        
        # Pad to match embedding dimension
        if len(scores_vector) < self.config.dimension:
            padding = np.zeros(self.config.dimension - len(scores_vector))
            scores_vector = np.concatenate([scores_vector, padding])
        
        if self.config.normalize:
            scores_vector = scores_vector / np.linalg.norm(scores_vector)
        
        return scores_vector
    
    def embed_revoi(self, revoi: REVOIScore) -> np.ndarray:
        """
        Generate embedding from REVOI scores.
        
        Args:
            revoi: REVOI scores
        
        Returns:
            Embedding vector
        """
        # Create 5D vector from scores
        scores_vector = np.array([
            revoi.representability,
            revoi.evolvability,
            revoi.verifiability,
            revoi.observability,
            revoi.interoperability
        ])
        
        # Pad to match embedding dimension
        if len(scores_vector) < self.config.dimension:
            padding = np.zeros(self.config.dimension - len(scores_vector))
            scores_vector = np.concatenate([scores_vector, padding])
        
        if self.config.normalize:
            scores_vector = scores_vector / np.linalg.norm(scores_vector)
        
        return scores_vector
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts efficiently.
        
        Args:
            texts: List of texts to embed
        
        Returns:
            Matrix of embeddings (shape: [len(texts), dimension])
        """
        self._load_model()
        embeddings = self._model.encode(texts, convert_to_numpy=True)
        
        if self.config.normalize:
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms
        
        return embeddings
