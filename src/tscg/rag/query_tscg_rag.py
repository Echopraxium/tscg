#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_tscg_rag.py - Query TSCG RAG database

Usage:
  python query_tscg_rag.py "What is ASFID?"
  python query_tscg_rag.py "feedback control mechanisms" --top-k 10
  python query_tscg_rag.py --interactive

Author: Echopraxium with the collaboration of Claude AI
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict

# ==============================================================================
# CONFIGURATION
# ==============================================================================

DEFAULT_DB_PATH = './db_tscg_rag'
DEFAULT_TOP_K = 5

# ==============================================================================
# ARGUMENT PARSING
# ==============================================================================

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Query TSCG RAG database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python query_tscg_rag.py "What is TSCG?"
  python query_tscg_rag.py "metaconcept tensor formula" --top-k 10
  python query_tscg_rag.py --interactive
  python query_tscg_rag.py "ASFID dimensions" --show-text

INTERACTIVE MODE:
  python query_tscg_rag.py -i
  
  Commands:
    stats       - Show database statistics
    sources     - List source files
    exit/quit   - Exit interactive mode
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Search query"
    )
    
    parser.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"Database path (default: {DEFAULT_DB_PATH})"
    )
    
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of results to return (default: {DEFAULT_TOP_K})"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive mode"
    )
    
    parser.add_argument(
        "--show-text",
        action="store_true",
        help="Show segment text in results"
    )
    
    parser.add_argument(
        "--filter-type",
        help="Filter by segment type (e.g., jsonld_entry, markdown_section)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed information"
    )
    
    return parser.parse_args()

# ==============================================================================
# DATABASE LOADING
# ==============================================================================

def load_database(db_path: str, verbose: bool = False):
    """Load ChromaDB database"""
    if not Path(db_path).exists():
        print(f"❌ Database not found: {db_path}")
        print(f"   Create it first with: python create_tscg_rag.py local")
        return None, None
    
    # Load metadata
    metadata = {}
    metadata_path = Path(db_path) / "metadata.json"
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)
    
    # Load ChromaDB
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        print("📦 Installing chromadb...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "chromadb", "-q"])
        import chromadb
        from chromadb.config import Settings
    
    client = chromadb.PersistentClient(
        path=db_path,
        settings=Settings(anonymized_telemetry=False)
    )
    
    try:
        collection = client.get_collection("tscg_rag")
    except:
        print(f"❌ Collection 'tscg_rag' not found in {db_path}")
        return None, None
    
    if verbose:
        print(f"✓ Loaded database: {db_path}")
        if metadata:
            print(f"  Created: {metadata.get('created_at', 'unknown')}")
            print(f"  Files: {metadata.get('total_files', 'unknown')}")
            print(f"  Segments: {metadata.get('total_segments', 'unknown')}")
    
    return collection, metadata

# ==============================================================================
# EMBEDDINGS
# ==============================================================================

def get_embedder(mode: str, verbose: bool = False):
    """Get embedder based on mode from metadata"""
    if mode == "local" or mode == "all-MiniLM-L6-v2":
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            print("📦 Installing sentence-transformers...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers", "-q"])
            from sentence_transformers import SentenceTransformer
        
        if verbose:
            print("✓ Using local embeddings")
        
        return SentenceTransformer('all-MiniLM-L6-v2')
    
    else:  # Google API
        # Load API key
        for key_path in ['../.api_key', '.api_key']:
            if os.path.exists(key_path):
                with open(key_path) as f:
                    os.environ['GOOGLE_API_KEY'] = f.read().strip()
                break
        
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        except ImportError:
            print("📦 Installing langchain-google-genai...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain-google-genai", "-q"])
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# ==============================================================================
# QUERY FUNCTIONS
# ==============================================================================

def search(collection, embedder, query: str, top_k: int = 5, filter_type: str = None, metadata_info: Dict = None):
    """Search the database"""
    # Generate query embedding
    embedding_mode = metadata_info.get('embedding_model', 'local') if metadata_info else 'local'
    
    if 'MiniLM' in embedding_mode or embedding_mode == 'local':
        query_embedding = embedder.encode([query])[0].tolist()
    else:
        query_embedding = embedder.embed_query(query)
    
    # Build filter
    where_filter = None
    if filter_type:
        where_filter = {"type": filter_type}
    
    # Query
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter
    )
    
    return results

def display_results(results, show_text: bool = False, verbose: bool = False):
    """Display search results"""
    if not results['documents'] or not results['documents'][0]:
        print("  No results found")
        return
    
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), 1):
        # Calculate similarity score (cosine distance -> similarity)
        similarity = 1 - dist
        
        source = Path(meta.get('source', 'unknown')).name
        seg_type = meta.get('type', 'unknown')
        
        print(f"\n{i}. {source} [{seg_type}] - Score: {similarity:.3f}")
        
        # Show metadata
        if 'label' in meta:
            print(f"   Label: {meta['label']}")
        if 'header' in meta:
            print(f"   Section: {meta['header']}")
        if 'uri' in meta:
            print(f"   URI: {meta['uri']}")
        
        # Show text excerpt or full text
        if show_text:
            print(f"   Text:\n{'-'*60}")
            print(doc)
            print('-'*60)
        else:
            excerpt = doc[:200].replace('\n', ' ')
            print(f"   Excerpt: {excerpt}...")
        
        if verbose:
            print(f"   Metadata: {meta}")

def show_stats(collection, metadata):
    """Show database statistics"""
    data = collection.get()
    
    print("\n📊 Database Statistics")
    print("="*60)
    
    if metadata:
        print(f"Created: {metadata.get('created_at', 'unknown')}")
        print(f"Repository: {metadata.get('repo_path', 'unknown')}")
        print(f"Embedding mode: {metadata.get('mode', 'unknown').upper()}")
        print(f"Chunk size: {metadata.get('chunk_size', 'unknown')}")
        print(f"Chunk overlap: {metadata.get('chunk_overlap', 'unknown')}")
    
    print(f"\nTotal segments: {len(data['documents'])}")
    print(f"Total files: {metadata.get('total_files', 'unknown')}")
    
    if data['metadatas']:
        # Count by type
        from collections import Counter
        type_counts = Counter(m.get('type', 'unknown') for m in data['metadatas'])
        
        print("\nSegments by type:")
        for seg_type, count in type_counts.most_common():
            print(f"  {seg_type}: {count}")

def show_sources(collection):
    """Show source files"""
    data = collection.get()
    
    if not data['metadatas']:
        print("No sources found")
        return
    
    sources = set(Path(m.get('source', '')).name for m in data['metadatas'])
    
    print(f"\n📚 Source Files ({len(sources)})")
    print("="*60)
    
    for i, source in enumerate(sorted(sources)[:30], 1):
        print(f"  {i:2}. {source}")
    
    if len(sources) > 30:
        print(f"  ... and {len(sources) - 30} more")

# ==============================================================================
# INTERACTIVE MODE
# ==============================================================================

def interactive_mode(collection, embedder, metadata, args):
    """Interactive query mode"""
    print("\n" + "="*70)
    print("  TSCG RAG - Interactive Query Mode")
    print("="*70)
    print("Commands: 'stats', 'sources', 'exit'")
    print("Or enter a search query")
    print("="*70)
    
    while True:
        try:
            query = input("\n❓ Query: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if query.lower() == 'stats':
                show_stats(collection, metadata)
                continue
            
            if query.lower() == 'sources':
                show_sources(collection)
                continue
            
            # Search
            print(f"\n🔍 Searching...")
            results = search(collection, embedder, query, args.top_k, args.filter_type, metadata)
            display_results(results, args.show_text, args.verbose)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main function"""
    args = parse_arguments()
    
    # Load database
    collection, metadata = load_database(args.db, args.verbose)
    
    if collection is None:
        return 1
    
    # Get embedder
    mode = metadata.get('embedding_model', 'local') if metadata else 'local'
    embedder = get_embedder(mode, args.verbose)
    
    # Interactive mode
    if args.interactive:
        interactive_mode(collection, embedder, metadata, args)
        return 0
    
    # Single query mode
    if not args.query:
        print("❌ No query provided. Use --interactive or provide a query.")
        print("   Example: python query_tscg_rag.py 'What is TSCG?'")
        return 1
    
    print(f"\n🔍 Searching for: '{args.query}'")
    print(f"   Top-k: {args.top_k}")
    if args.filter_type:
        print(f"   Filter: {args.filter_type}")
    
    results = search(collection, embedder, args.query, args.top_k, args.filter_type, metadata)
    display_results(results, args.show_text, args.verbose)
    
    print()
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
