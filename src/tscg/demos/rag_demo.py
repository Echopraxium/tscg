#!/usr/bin/env python3
"""
TSCG RAG Demo - Semantic Search Example

Demonstrates RAG (Retrieval-Augmented Generation) capabilities:
- Indexing ontologies
- Semantic search
- Similarity finding
- Formula-based search

Author: Echopraxium with the collaboration of Claude AI
"""

from pathlib import Path
from tscg.engine.facade import OntologyFacade, RAGFacade


def demo_rag_indexing():
    """Demonstrate indexing ontologies for RAG"""
    print("\n" + "="*70)
    print("  1. RAG Indexing")
    print("="*70)
    
    # Load ontologies
    ontology = OntologyFacade()
    
    project_files = [
        "/mnt/project/M3_EagleEye.jsonld",
        "/mnt/project/M3_SphinxEye.jsonld",
        "/mnt/project/M2_MetaConcepts.jsonld"
    ]
    
    loaded_count = 0
    for filepath in project_files:
        if Path(filepath).exists():
            try:
                ontology.load(filepath)
                loaded_count += 1
                print(f"✓ Loaded: {Path(filepath).stem}")
            except Exception as e:
                print(f"✗ Failed: {filepath} - {e}")
    
    if loaded_count == 0:
        print("⚠ No ontologies loaded, cannot demo RAG")
        return None
    
    # Initialize RAG and index
    print("\nIndexing for semantic search...")
    rag = RAGFacade()
    rag.index_ontology(ontology.loader)
    
    # Get stats
    stats = rag.get_stats()
    print(f"✓ Indexed {stats['metaconcept_count']} metaconcepts")
    print(f"  Model: {stats['embedding_model']}")
    print(f"  Dimension: {stats['embedding_dimension']}")
    
    return rag


def demo_semantic_search(rag: RAGFacade):
    """Demonstrate semantic search"""
    print("\n" + "="*70)
    print("  2. Semantic Search")
    print("="*70)
    
    queries = [
        "feedback control mechanisms",
        "system dynamics and evolution",
        "information processing",
        "structural organization"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = rag.search(query, top_k=3)
        
        if results:
            for i, result in enumerate(results, 1):
                label = result.metadata.get('label', 'Unknown')
                layer = result.metadata.get('layer', '?')
                score = result.score
                print(f"  {i}. {label} (Layer: {layer}) - Score: {score:.3f}")
        else:
            print("  No results found")


def demo_formula_search(rag: RAGFacade):
    """Demonstrate formula-based search"""
    print("\n" + "="*70)
    print("  3. Formula-Based Search")
    print("="*70)
    
    formulas = [
        "A⊗S",      # Attractor ⊗ Structure
        "F⊗D",      # Flow ⊗ Dynamics
        "It⊗Im",    # Territory ⊗ Map (hybrid)
    ]
    
    for formula in formulas:
        print(f"\nFormula: '{formula}'")
        try:
            results = rag.search_by_formula(formula, top_k=3)
            
            if results:
                for i, (metaconcept, score) in enumerate(results, 1):
                    print(f"  {i}. {metaconcept.label} - Score: {score:.3f}")
                    if metaconcept.tensor_formula:
                        print(f"     Formula: {metaconcept.tensor_formula}")
            else:
                print("  No results found")
        except Exception as e:
            print(f"  Error: {e}")


def demo_layer_filtering(rag: RAGFacade):
    """Demonstrate layer-specific search"""
    print("\n" + "="*70)
    print("  4. Layer-Specific Search")
    print("="*70)
    
    query = "system structure"
    
    for layer in ["M3", "M2"]:
        print(f"\nLayer: {layer} - Query: '{query}'")
        results = rag.search(query, top_k=3, layer=layer)
        
        if results:
            for i, result in enumerate(results, 1):
                label = result.metadata.get('label', 'Unknown')
                score = result.score
                print(f"  {i}. {label} - Score: {score:.3f}")
        else:
            print("  No results found")


def demo_save_and_load(rag: RAGFacade):
    """Demonstrate saving and loading index"""
    print("\n" + "="*70)
    print("  5. Save & Load Index")
    print("="*70)
    
    # Save index
    index_path = "/tmp/tscg_rag_index"
    print(f"Saving index to: {index_path}")
    rag.save_index(index_path)
    print("✓ Index saved")
    
    # Create new RAG instance and load
    print("\nLoading index...")
    new_rag = RAGFacade()
    new_rag.load_index(index_path)
    
    stats = new_rag.get_stats()
    print(f"✓ Index loaded: {stats['metaconcept_count']} metaconcepts")
    
    # Test search
    results = new_rag.search("feedback", top_k=2)
    print(f"\nTest search found {len(results)} results")


def main():
    """Run all RAG demos"""
    print("\n" + "="*70)
    print("  TSCG RAG - Semantic Search Demo")
    print("  Retrieval-Augmented Generation")
    print("="*70)
    
    # 1. Index ontologies
    rag = demo_rag_indexing()
    
    if rag is None:
        return
    
    # 2. Semantic search
    demo_semantic_search(rag)
    
    # 3. Formula search
    demo_formula_search(rag)
    
    # 4. Layer filtering
    demo_layer_filtering(rag)
    
    # 5. Save/load
    demo_save_and_load(rag)
    
    print("\n" + "="*70)
    print("  ✓ RAG Demo Completed!")
    print("="*70)
    print("\nKey Features:")
    print("  - Semantic search using vector embeddings")
    print("  - Formula-based metaconcept discovery")
    print("  - Layer and perspective filtering")
    print("  - Persistent index (save/load)")
    print("\nUse Cases:")
    print("  - Finding relevant metaconcepts for system modeling")
    print("  - Discovering similar patterns across domains")
    print("  - LLM-augmented ontology exploration")
    print()


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"\n⚠ Missing dependency: {e}")
        print("\nInstall RAG dependencies with:")
        print("  pip install -e .[rag]")
        print("  or")
        print("  pip install sentence-transformers")
