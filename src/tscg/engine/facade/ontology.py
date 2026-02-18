"""
Ontology Facade - Public API for ontology operations

This facade provides a clean, stable interface for working with TSCG ontologies.

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import Optional, List
from pathlib import Path
from rdflib import Graph

from ..core.ontology_loader import OntologyLoader
from ..core.models import Metaconcept, OntologyMetadata


class OntologyFacade:
    """
    Public API for ontology operations.
    
    Provides high-level operations for loading, managing, and querying
    TSCG ontologies.
    
    Example:
        >>> ontology = OntologyFacade()
        >>> graph = ontology.load("M3_EagleEye.jsonld")
        >>> metaconcepts = ontology.get_metaconcepts(layer="M3")
    """
    
    def __init__(self):
        """Initialize the ontology facade"""
        self._loader = OntologyLoader()
    
    def load(self, filepath: str) -> Graph:
        """
        Load an ontology file.
        
        Args:
            filepath: Path to JSON-LD ontology file
        
        Returns:
            RDF Graph containing the ontology
        
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file cannot be parsed
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Ontology file not found: {filepath}")
        
        return self._loader.load(filepath)
    
    def get_graph(self, name: str) -> Optional[Graph]:
        """
        Get a loaded ontology graph by name.
        
        Args:
            name: Name of the loaded ontology (stem of filename)
        
        Returns:
            RDF Graph if found, None otherwise
        """
        return self._loader.get_graph(name)
    
    def list_loaded(self) -> List[str]:
        """
        List names of all loaded ontologies.
        
        Returns:
            List of ontology names
        """
        return self._loader.list_loaded()
    
    def get_metadata(self, name: str) -> Optional[OntologyMetadata]:
        """
        Get metadata for a loaded ontology.
        
        Args:
            name: Name of the loaded ontology
        
        Returns:
            OntologyMetadata if found, None otherwise
        """
        return self._loader.metadata.get(name)
    
    def get_metaconcepts(
        self, 
        layer: Optional[str] = None,
        perspective: Optional[str] = None
    ) -> List[Metaconcept]:
        """
        Get metaconcepts from loaded ontologies.
        
        Args:
            layer: Filter by layer (M3, M2, M1, M0)
            perspective: Filter by perspective (EagleEye, SphinxEye, Genesis)
        
        Returns:
            List of Metaconcept objects
        """
        concepts = self._loader.get_metaconcepts(layer)
        
        if perspective:
            concepts = [c for c in concepts if c.perspective == perspective]
        
        return concepts
    
    def get_triple_count(self, name: Optional[str] = None) -> int:
        """
        Get the number of triples in an ontology.
        
        Args:
            name: Ontology name. If None, returns sum of all loaded ontologies.
        
        Returns:
            Number of RDF triples
        """
        if name:
            graph = self.get_graph(name)
            return len(graph) if graph else 0
        
        # Sum all loaded ontologies
        return sum(len(g) for g in self._loader.graphs.values())
