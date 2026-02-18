"""
REPL session context using TSCG Engine Facade

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import Dict, List, Optional, Any
from pathlib import Path

# Use public facade API
from tscg.engine.facade import (
    OntologyFacade,
    QueryFacade,
    MetricsFacade,
    ExportFacade
)


class ReplContext:
    """
    Maintains state for a REPL session.
    
    This context uses tscg.engine.facade exclusively - it doesn't
    access internal engine components directly.
    """
    
    def __init__(self):
        # Facade instances (public API)
        self.ontology = OntologyFacade()
        self.query = QueryFacade()
        self.metrics = MetricsFacade()
        self.export = ExportFacade()
        
        # Session state
        self.current_ontology: Optional[str] = None
        self.variables: Dict[str, Any] = {}
        self.command_history: List[str] = []
        
        # Settings
        self.auto_cache = True
        self.verbose = False
    
    def load_ontology(self, filepath: str):
        """Load an ontology file using the facade"""
        graph = self.ontology.load(filepath)
        
        # Set as current if first loaded
        if not self.current_ontology:
            self.current_ontology = Path(filepath).stem
        
        # Update query facade with new graph
        self.query.set_graph(graph)
        
        return graph
    
    def set_current_ontology(self, name: str):
        """Set the active ontology"""
        graph = self.ontology.get_graph(name)
        if not graph:
            raise ValueError(f"Ontology '{name}' not loaded")
        
        self.current_ontology = name
        self.query.set_graph(graph)
    
    def list_loaded_ontologies(self) -> List[str]:
        """Get list of loaded ontologies"""
        return self.ontology.list_loaded()
    
    def export_current_to_turtle(self, output_path: str) -> bool:
        """Export current ontology to Turtle format"""
        if not self.current_ontology:
            raise RuntimeError("No ontology loaded")
        
        graph = self.ontology.get_graph(self.current_ontology)
        result = self.export.to_turtle(graph, output_path)
        return result.success
    
    def execute_sparql(self, query: str):
        """Execute SPARQL query on current graph"""
        return self.query.execute(query, use_cache=self.auto_cache)
    
    def set_variable(self, name: str, value: Any):
        """Set a session variable"""
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Optional[Any]:
        """Get a session variable"""
        return self.variables.get(name)
    
    def add_to_history(self, command: str):
        """Add command to history"""
        self.command_history.append(command)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        triple_count = 0
        if self.current_ontology:
            graph = self.ontology.get_graph(self.current_ontology)
            if graph:
                triple_count = len(graph)
        
        return {
            "loaded_ontologies": len(self.ontology.list_loaded()),
            "current_ontology": self.current_ontology,
            "triple_count": triple_count,
            "variables": len(self.variables),
            "history_length": len(self.command_history)
        }
