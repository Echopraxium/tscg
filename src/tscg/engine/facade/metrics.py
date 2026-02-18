"""
Metrics Facade - Public API for metrics computation

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import Dict
import numpy as np

from ..analysis.metrics.orthogonality import (
    OrthogonalityAnalyzer,
    OrthogonalityReport
)
from ..core.models import ASFIDScore, REVOIScore


class MetricsFacade:
    """
    Public API for metrics computation.
    
    Provides high-level operations for computing various metrics on
    TSCG system models.
    
    Example:
        >>> metrics = MetricsFacade()
        >>> asfid = ASFIDScore(attractor=0.95, structure=0.88, ...)
        >>> report = metrics.compute_orthogonality(asfid.to_dict())
    """
    
    def __init__(self):
        """Initialize the metrics facade"""
        self._ortho_analyzer = OrthogonalityAnalyzer()
    
    def compute_orthogonality(
        self,
        scores: Dict[str, float]
    ) -> OrthogonalityReport:
        """
        Compute orthogonality metrics for a set of scores.
        
        Args:
            scores: Dictionary mapping dimension labels to scores
                   (e.g., {"A": 0.95, "S": 0.88, ...})
        
        Returns:
            OrthogonalityReport with analysis results
        """
        return self._ortho_analyzer.analyze_scores(scores)
    
    def compute_orthogonality_matrix(
        self,
        state_vectors: Dict[str, np.ndarray]
    ) -> OrthogonalityReport:
        """
        Compute orthogonality matrix for state space vectors.
        
        Args:
            state_vectors: Dictionary mapping labels to vector arrays
        
        Returns:
            OrthogonalityReport with matrix and analysis
        """
        matrix, labels = self._ortho_analyzer.compute_matrix(state_vectors)
        return self._ortho_analyzer.analyze(matrix, labels)
    
    def asfid_orthogonality(self, asfid: ASFIDScore) -> OrthogonalityReport:
        """
        Compute orthogonality for ASFID scores.
        
        Args:
            asfid: ASFIDScore object
        
        Returns:
            OrthogonalityReport
        """
        return self.compute_orthogonality(asfid.to_dict())
    
    def revoi_orthogonality(self, revoi: REVOIScore) -> OrthogonalityReport:
        """
        Compute orthogonality for REVOI scores.
        
        Args:
            revoi: REVOIScore object
        
        Returns:
            OrthogonalityReport
        """
        return self.compute_orthogonality(revoi.to_dict())
