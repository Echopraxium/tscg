"""
Export Facade - Public API for ontology export

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import Literal
from pathlib import Path
from rdflib import Graph

from ..exporters.turtle_exporter import TurtleExporter, ExportResult


class ExportFacade:
    """
    Public API for ontology export operations.
    
    Example:
        >>> export_api = ExportFacade()
        >>> result = export_api.to_turtle(graph, "output.ttl")
        >>> if result.success:
        ...     print(f"Exported {result.triples_count} triples")
    """
    
    def __init__(self):
        """Initialize the export facade"""
        self._turtle_exporter = TurtleExporter()
    
    def to_turtle(
        self,
        graph: Graph,
        output_path: str,
        prefixes: Literal["compact", "full", "minimal"] = "compact"
    ) -> ExportResult:
        """
        Export RDF graph to Turtle format.
        
        Args:
            graph: RDF graph to export
            output_path: Path to output file
            prefixes: Prefix binding style
        
        Returns:
            ExportResult with export details
        """
        return self._turtle_exporter.export(graph, output_path, prefixes)
    
    def to_file(
        self,
        graph: Graph,
        output_path: str,
        format: str = "turtle"
    ) -> ExportResult:
        """
        Export RDF graph to a file in specified format.
        
        Args:
            graph: RDF graph to export
            output_path: Path to output file
            format: RDF serialization format (turtle, xml, n3, etc.)
        
        Returns:
            ExportResult with export details
        """
        if format.lower() in ["turtle", "ttl"]:
            return self.to_turtle(graph, output_path)
        
        # For other formats, use rdflib directly
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            serialized = graph.serialize(format=format)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(serialized)
            
            return ExportResult(
                path=str(output_file),
                triples_count=len(graph),
                format=format,
                success=True,
                message=f"Exported {len(graph)} triples to {output_file.name}"
            )
        
        except Exception as e:
            return ExportResult(
                path=output_path,
                triples_count=0,
                format=format,
                success=False,
                message=f"Export failed: {str(e)}"
            )
