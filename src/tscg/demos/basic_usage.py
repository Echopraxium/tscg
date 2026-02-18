#!/usr/bin/env python3
"""
TSCG Engine - Basic Usage Demo

This demonstrates programmatic usage of the TSCG Engine through its facade API.

Author: Echopraxium with the collaboration of Claude AI
"""

from pathlib import Path
from tscg.engine.facade import (
    OntologyFacade,
    QueryFacade,
    MetricsFacade,
    ExportFacade
)
from tscg.engine.core.models import ASFIDScore, REVOIScore


def demo_ontology_loading():
    """Demonstrate ontology loading"""
    print("\n" + "="*70)
    print("  1. Loading Ontologies")
    print("="*70)
    
    ontology = OntologyFacade()
    
    # Try to load from project files
    project_files = [
        "/mnt/project/M3_EagleEye.jsonld",
        "/mnt/project/M3_SphinxEye.jsonld",
    ]
    
    for filepath in project_files:
        if Path(filepath).exists():
            try:
                graph = ontology.load(filepath)
                name = Path(filepath).stem
                print(f"✓ Loaded: {name} ({len(graph)} triples)")
            except Exception as e:
                print(f"✗ Failed: {filepath} - {e}")
        else:
            print(f"⚠ Not found: {filepath}")
    
    print(f"\nTotal loaded: {len(ontology.list_loaded())} ontologies")
    return ontology


def demo_sparql_queries(ontology: OntologyFacade):
    """Demonstrate SPARQL queries"""
    print("\n" + "="*70)
    print("  2. SPARQL Queries")
    print("="*70)
    
    # Get first loaded ontology
    loaded = ontology.list_loaded()
    if not loaded:
        print("No ontologies loaded")
        return
    
    graph = ontology.get_graph(loaded[0])
    query_api = QueryFacade(graph)
    
    # Simple query
    sparql = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?concept ?label
    WHERE {
        ?concept rdfs:label ?label .
        FILTER(isIRI(?concept))
    }
    LIMIT 5
    """
    
    print(f"Executing query on: {loaded[0]}")
    results = query_api.execute(sparql)
    
    print(f"\nResults: {results.row_count} rows")
    for i, row in enumerate(results.bindings[:5], 1):
        print(f"  {i}. {row.get('label', 'N/A')}")


def demo_metrics():
    """Demonstrate metrics computation"""
    print("\n" + "="*70)
    print("  3. Metrics Computation")
    print("="*70)
    
    metrics = MetricsFacade()
    
    # Sample ASFID scores (from butterfly metamorphosis example)
    asfid = ASFIDScore(
        attractor=0.95,
        structure=0.88,
        flow=0.92,
        information=0.85,
        dynamics=0.90
    )
    
    print(f"ASFID Scores: Overall = {asfid.overall:.2f}")
    
    # Compute orthogonality
    report = metrics.asfid_orthogonality(asfid)
    
    print(f"\nOrthogonality Analysis:")
    print(f"  Most orthogonal: {report.most_orthogonal_pair} (sim={report.min_similarity:.3f})")
    print(f"  Least orthogonal: {report.least_orthogonal_pair} (sim={report.max_similarity:.3f})")
    print(f"  Average orthogonality: {report.average_orthogonality:.3f}")
    print(f"  Condition number: {report.condition_number:.2f}")


def demo_export(ontology: OntologyFacade):
    """Demonstrate export functionality"""
    print("\n" + "="*70)
    print("  4. Export to Turtle")
    print("="*70)
    
    loaded = ontology.list_loaded()
    if not loaded:
        print("No ontologies loaded")
        return
    
    graph = ontology.get_graph(loaded[0])
    export_api = ExportFacade()
    
    output_path = f"/tmp/{loaded[0]}_export.ttl"
    result = export_api.to_turtle(graph, output_path)
    
    if result.success:
        print(f"✓ {result.message}")
        print(f"  Path: {result.path}")
    else:
        print(f"✗ Export failed: {result.message}")


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("  TSCG Engine - Programmatic Usage Demo")
    print("  Using Facade API Pattern")
    print("="*70)
    
    # 1. Load ontologies
    ontology = demo_ontology_loading()
    
    # 2. SPARQL queries
    demo_sparql_queries(ontology)
    
    # 3. Metrics
    demo_metrics()
    
    # 4. Export
    demo_export(ontology)
    
    print("\n" + "="*70)
    print("  ✓ Demo completed!")
    print("="*70)
    print("\nKey takeaways:")
    print("  - All operations use facade API (tscg.engine.facade)")
    print("  - No direct access to internal engine components")
    print("  - Clean, stable public interface")
    print("  - Perfect for programmatic use in scripts, notebooks, etc.")
    print()


if __name__ == "__main__":
    main()
