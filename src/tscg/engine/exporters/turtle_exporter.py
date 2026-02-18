"""
Export ontologies to Turtle (TTL) format

Author: Echopraxium with the collaboration of Claude AI
"""

from pathlib import Path
from typing import Literal, Optional
from dataclasses import dataclass
from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS


@dataclass
class ExportResult:
    """Result of an export operation"""
    path: str
    triples_count: int
    format: str
    success: bool = True
    message: Optional[str] = None


class TurtleExporter:
    """Export RDF graphs to Turtle format"""
    
    # TSCG namespaces
    TSCG_BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
    
    def __init__(self):
        pass
    
    def export(
        self,
        graph: Graph,
        output_path: str,
        prefixes: Literal["compact", "full", "minimal"] = "compact"
    ) -> ExportResult:
        """Export RDF graph to Turtle format
        
        Args:
            graph: RDF graph to export
            output_path: Path to output file
            prefixes: Prefix binding style
        
        Returns:
            ExportResult with export details
        """
        
        # Bind namespaces based on prefix style
        if prefixes in ["compact", "full"]:
            self._bind_standard_prefixes(graph)
            self._bind_tscg_prefixes(graph)
        
        # Serialize to Turtle
        try:
            turtle_str = graph.serialize(format='turtle')
            
            # Write to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(turtle_str)
            
            return ExportResult(
                path=str(output_file),
                triples_count=len(graph),
                format="turtle",
                success=True,
                message=f"Exported {len(graph)} triples to {output_file.name}"
            )
        
        except Exception as e:
            return ExportResult(
                path=output_path,
                triples_count=0,
                format="turtle",
                success=False,
                message=f"Export failed: {str(e)}"
            )
    
    def _bind_standard_prefixes(self, graph: Graph):
        """Bind standard W3C prefixes"""
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("owl", OWL)
        graph.bind("skos", SKOS)
        graph.bind("xsd", "http://www.w3.org/2001/XMLSchema#")
        graph.bind("dc", "http://purl.org/dc/elements/1.1/")
        graph.bind("dcterms", "http://purl.org/dc/terms/")
    
    def _bind_tscg_prefixes(self, graph: Graph):
        """Bind TSCG-specific namespaces"""
        TSCG = Namespace(self.TSCG_BASE)
        graph.bind("tscg", TSCG)
        graph.bind("m3", Namespace(self.TSCG_BASE + "m3:"))
        graph.bind("m2", Namespace(self.TSCG_BASE + "m2:"))
        graph.bind("asfid", Namespace(self.TSCG_BASE + "m3:eagle_eye#"))
        graph.bind("revoi", Namespace(self.TSCG_BASE + "m3:sphinx_eye#"))
