"""
SPARQL query executor

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


@dataclass
class SPARQLResult:
    """Result of a SPARQL query"""
    bindings: List[Dict[str, Any]]
    vars: List[str]
    query: str
    row_count: int
    
    @classmethod
    def from_rdflib(cls, results, query: str):
        """Create from rdflib query results"""
        bindings = []
        vars_list = []
        
        if hasattr(results, 'vars'):
            vars_list = [str(v) for v in results.vars]
        
        for row in results:
            row_dict = {}
            for var in vars_list:
                if var in row:
                    value = row[var]
                    # Convert to string representation
                    row_dict[var] = str(value) if value else None
            bindings.append(row_dict)
        
        return cls(
            bindings=bindings,
            vars=vars_list,
            query=query,
            row_count=len(bindings)
        )


class SPARQLExecutor:
    """Execute SPARQL queries on RDF graphs"""
    
    def __init__(self, graph: Optional[Graph] = None):
        self.graph = graph
        self.query_cache = {}
    
    def set_graph(self, graph: Graph):
        """Set the active graph for queries"""
        self.graph = graph
        # Clear cache when graph changes
        self.query_cache.clear()
    
    def execute(self, query: str, use_cache: bool = False) -> SPARQLResult:
        """Execute a SPARQL query
        
        Args:
            query: SPARQL query string
            use_cache: Whether to cache results
        
        Returns:
            SPARQLResult with query results
        """
        if not self.graph:
            raise RuntimeError("No graph loaded. Use set_graph() first.")
        
        # Check cache
        query_hash = hash(query)
        if use_cache and query_hash in self.query_cache:
            return self.query_cache[query_hash]
        
        # Execute query
        try:
            results = self.graph.query(query)
            sparql_result = SPARQLResult.from_rdflib(results, query)
            
            # Cache if requested
            if use_cache:
                self.query_cache[query_hash] = sparql_result
            
            return sparql_result
        
        except Exception as e:
            raise ValueError(f"SPARQL query failed: {str(e)}\n\nQuery:\n{query}")
    
    def query_metaconcepts(self, layer: Optional[str] = None) -> SPARQLResult:
        """Query all metaconcepts, optionally filtered by layer"""
        
        query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX tscg: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/>
        
        SELECT ?concept ?label
        WHERE {
            ?concept rdfs:label ?label .
            FILTER(isIRI(?concept))
        }
        ORDER BY ?label
        """
        
        return self.execute(query)
    
    def query_triples_by_subject(self, subject_uri: str) -> SPARQLResult:
        """Query all triples for a given subject"""
        
        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?predicate ?object
        WHERE {{
            <{subject_uri}> ?predicate ?object .
        }}
        ORDER BY ?predicate
        """
        
        return self.execute(query)
