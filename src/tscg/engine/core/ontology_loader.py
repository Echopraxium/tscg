"""
Ontology loader for JSON-LD files

Author: Echopraxium with the collaboration of Claude AI
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS
from .models import OntologyMetadata, Metaconcept, Poclet

# TSCG Namespaces
TSCG_BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
TSCG = Namespace(TSCG_BASE)
M3 = Namespace(TSCG_BASE + "m3:")


class OntologyLoader:
    """Load and parse TSCG ontologies from JSON-LD files"""
    
    def __init__(self):
        self.graphs: Dict[str, Graph] = {}
        self.metadata: Dict[str, OntologyMetadata] = {}
        self.metaconcepts: Dict[str, Metaconcept] = {}
        
    def load(self, filepath: str) -> Graph:
        """Load a JSON-LD ontology file"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"Ontology file not found: {filepath}")
        
        # Create RDF graph
        graph = Graph()
        
        # Bind standard namespaces
        graph.bind("rdf", RDF)
        graph.bind("rdfs", RDFS)
        graph.bind("owl", OWL)
        graph.bind("skos", SKOS)
        graph.bind("tscg", TSCG)
        graph.bind("m3", M3)
        
        # Parse JSON-LD
        try:
            graph.parse(filepath, format="json-ld")
        except Exception as e:
            raise ValueError(f"Failed to parse {filepath}: {e}")
        
        # Extract metadata
        metadata = self._extract_metadata(graph, path.stem)
        
        # Store
        self.graphs[path.stem] = graph
        self.metadata[path.stem] = metadata
        
        # Extract metaconcepts if M2 or M3 layer
        if metadata.layer in ["M2", "M3"]:
            concepts = self._extract_metaconcepts(graph, metadata.layer)
            self.metaconcepts.update(concepts)
        
        return graph
    
    def _extract_metadata(self, graph: Graph, name: str) -> OntologyMetadata:
        """Extract ontology metadata from RDF graph"""
        
        # Try to find ontology IRI
        ontology_iris = list(graph.subjects(RDF.type, OWL.Ontology))
        
        if ontology_iris:
            onto_iri = str(ontology_iris[0])
        else:
            onto_iri = f"{TSCG_BASE}{name}"
        
        # Determine layer from name
        if name.startswith("M3_"):
            layer = "M3"
        elif name.startswith("M2_"):
            layer = "M2"
        elif name.startswith("M1_"):
            layer = "M1"
        elif name.startswith("M0_"):
            layer = "M0"
        else:
            layer = "M2"  # Default
        
        # Get triple count
        triple_count = len(graph)
        
        return OntologyMetadata(
            uri=onto_iri,
            layer=layer,
            triple_count=triple_count
        )
    
    def _extract_metaconcepts(self, graph: Graph, layer: str) -> Dict[str, Metaconcept]:
        """Extract metaconcepts from graph"""
        concepts = {}
        
        # Query for metaconcepts (simplified for prototype)
        # In full version, would use SPARQL
        for subj in graph.subjects(RDF.type, None):
            subj_str = str(subj)
            
            # Skip if not a concept URI
            if not ("#" in subj_str or "/" in subj_str):
                continue
            
            # Get label
            labels = list(graph.objects(subj, RDFS.label))
            if not labels:
                continue
            
            label = str(labels[0])
            
            # Create metaconcept
            concept = Metaconcept(
                uri=subj_str,
                label=label,
                layer=layer
            )
            
            concepts[subj_str] = concept
        
        return concepts
    
    def get_graph(self, name: str) -> Optional[Graph]:
        """Get loaded graph by name"""
        return self.graphs.get(name)
    
    def list_loaded(self) -> List[str]:
        """List names of loaded ontologies"""
        return list(self.graphs.keys())
    
    def get_metaconcepts(self, layer: Optional[str] = None) -> List[Metaconcept]:
        """Get metaconcepts, optionally filtered by layer"""
        if layer:
            return [mc for mc in self.metaconcepts.values() if mc.layer == layer]
        return list(self.metaconcepts.values())
