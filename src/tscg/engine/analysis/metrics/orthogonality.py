"""
Orthogonality metrics for state space vectors

Author: Echopraxium with the collaboration of Claude AI
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy.spatial.distance import cosine


@dataclass
class OrthogonalityReport:
    """Report on orthogonality analysis"""
    matrix: np.ndarray
    labels: List[str]
    most_orthogonal_pair: Tuple[str, str]
    least_orthogonal_pair: Tuple[str, str]
    min_similarity: float
    max_similarity: float
    average_orthogonality: float
    condition_number: float
    
    def __str__(self) -> str:
        """String representation of report"""
        lines = []
        lines.append("Orthogonality Analysis Report")
        lines.append("=" * 50)
        lines.append(f"Most orthogonal: {self.most_orthogonal_pair} (sim={self.min_similarity:.3f})")
        lines.append(f"Least orthogonal: {self.least_orthogonal_pair} (sim={self.max_similarity:.3f})")
        lines.append(f"Average orthogonality: {self.average_orthogonality:.3f}")
        lines.append(f"Condition number: {self.condition_number:.2f}")
        return "\n".join(lines)


class OrthogonalityAnalyzer:
    """Compute orthogonality metrics for state space vectors"""
    
    def compute_matrix(
        self, 
        state_vectors: Dict[str, np.ndarray]
    ) -> Tuple[np.ndarray, List[str]]:
        """Compute pairwise orthogonality (cosine similarity) matrix
        
        Args:
            state_vectors: Dictionary mapping labels to vector arrays
        
        Returns:
            Tuple of (similarity_matrix, labels)
        """
        labels = list(state_vectors.keys())
        n = len(labels)
        matrix = np.eye(n)  # Diagonal is 1.0 (perfect similarity with self)
        
        for i, label_i in enumerate(labels):
            for j, label_j in enumerate(labels):
                if i != j:
                    vec_i = state_vectors[label_i]
                    vec_j = state_vectors[label_j]
                    
                    # Cosine similarity (1 - cosine distance)
                    # High similarity = low orthogonality
                    similarity = 1.0 - cosine(vec_i, vec_j)
                    matrix[i, j] = similarity
        
        return matrix, labels
    
    def analyze(
        self, 
        matrix: np.ndarray, 
        labels: List[str]
    ) -> OrthogonalityReport:
        """Analyze orthogonality matrix
        
        Args:
            matrix: Similarity matrix
            labels: Labels for matrix dimensions
        
        Returns:
            OrthogonalityReport with analysis results
        """
        n = len(labels)
        
        # Find most/least orthogonal pairs (excluding diagonal)
        min_sim = 1.0
        max_sim = 0.0
        min_pair = None
        max_pair = None
        
        for i in range(n):
            for j in range(i+1, n):
                sim = matrix[i, j]
                if sim < min_sim:
                    min_sim = sim
                    min_pair = (labels[i], labels[j])
                if sim > max_sim:
                    max_sim = sim
                    max_pair = (labels[i], labels[j])
        
        # Average off-diagonal similarity
        mask = ~np.eye(n, dtype=bool)
        avg_similarity = matrix[mask].mean()
        avg_orthogonality = 1.0 - avg_similarity
        
        # Condition number (measure of how well-conditioned the matrix is)
        eigenvalues = np.linalg.eigvalsh(matrix)
        condition_number = max(abs(eigenvalues)) / min(abs(eigenvalues))
        
        return OrthogonalityReport(
            matrix=matrix,
            labels=labels,
            most_orthogonal_pair=min_pair,
            least_orthogonal_pair=max_pair,
            min_similarity=min_sim,
            max_similarity=max_sim,
            average_orthogonality=avg_orthogonality,
            condition_number=condition_number
        )
    
    def analyze_scores(
        self,
        scores: Dict[str, float]
    ) -> OrthogonalityReport:
        """Analyze orthogonality from score dictionary (e.g., ASFID or REVOI)
        
        For a single poclet, converts scores to unit vectors for analysis.
        
        Args:
            scores: Dictionary of dimension -> score (0.0-1.0)
        
        Returns:
            OrthogonalityReport
        """
        # Convert scores to vectors
        # For single poclet, treat each dimension as a vector
        # This is a simplified approach for the prototype
        
        vectors = {}
        for dim, score in scores.items():
            # Create a unit vector in the dimension's direction
            vec = np.zeros(len(scores))
            idx = list(scores.keys()).index(dim)
            vec[idx] = score
            vectors[dim] = vec
        
        matrix, labels = self.compute_matrix(vectors)
        return self.analyze(matrix, labels)
