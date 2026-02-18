"""
Query Facade - Public API for SPARQL queries

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import Optional
from rdflib import Graph

from ..analysis.sparql.executor import SPARQLExecutor, SPARQLResult


class QueryFacade:
    """
    Public API for SPARQL query operations.
    
    Example:
        >>> query_api = QueryFacade(graph)
        >>> results = query_api.execute("SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10")
        >>> for row in results.bindings:
        ...     print(row)
    """
    
    def __init__(self, graph: Optional[Graph] = None):
        """
        Initialize the query facade.
        
        Args:
            graph: Optional RDF graph to query. Can be set later with set_graph()
        """
        self._executor = SPARQLExecutor(graph)
    
    def set_graph(self, graph: Graph):
        """
        Set the active graph for queries.
        
        Args:
            graph: RDF graph to query
        """
        self._executor.set_graph(graph)
    
    def execute(self, query: str, use_cache: bool = False) -> SPARQLResult:
        """
        Execute a SPARQL query.
        
        Args:
            query: SPARQL query string
            use_cache: Whether to cache results
        
        Returns:
            SPARQLResult with query results
        
        Raises:
            RuntimeError: If no graph is loaded
            ValueError: If query is invalid
        """
        return self._executor.execute(query, use_cache)
    
    def find_metaconcepts(self, layer: Optional[str] = None) -> SPARQLResult:
        """
        Query all metaconcepts, optionally filtered by layer.
        
        Args:
            layer: Filter by layer (M3, M2, M1, M0)
        
        Returns:
            SPARQLResult with metaconcept data
        """
        return self._executor.query_metaconcepts(layer)
    
    def find_related(self, subject_uri: str) -> SPARQLResult:
        """
        Find all triples related to a given subject.
        
        Args:
            subject_uri: URI of the subject to query
        
        Returns:
            SPARQLResult with related triples
        """
        return self._executor.query_triples_by_subject(subject_uri)
    
    def clear_cache(self):
        """Clear the query result cache"""
        self._executor.query_cache.clear()
