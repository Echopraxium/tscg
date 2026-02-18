#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_tscg_rag.py - Generate RAG database for TSCG repository

Combines the best of both worlds:
- Intelligent segmentation from tscg.engine.rag.segmentation
- Simple CLI from create_RAG.py
- ChromaDB storage for persistence

Usage:
  python create_tscg_rag.py local        # Local embeddings (recommended)
  python create_tscg_rag.py api          # Google API embeddings
  python create_tscg_rag.py --help       # Show help

Author: Echopraxium with the collaboration of Claude AI
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional
import datetime

# ==============================================================================
# CONFIGURATION
# ==============================================================================

DEFAULT_EXTENSIONS = ['md', 'jsonld', 'txt', 'py', 'cs', 'fs']
IGNORED_PATTERNS = ['bin/', 'obj/', '.git/', '__pycache__/', 'node_modules/']
DEFAULT_DB_PATH = './db_tscg_rag'
DEFAULT_REPO_PATH = '..'

# Chunking configuration
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200
MIN_CHUNK_SIZE = 100

# ==============================================================================
# ARGUMENT PARSING
# ==============================================================================

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate RAG database for TSCG repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python create_tscg_rag.py local           # Use local embeddings (free, recommended)
  python create_tscg_rag.py api             # Use Google API embeddings (quota limited)
  
  python create_tscg_rag.py local --repo /path/to/tscg
  python create_tscg_rag.py local --db ./my_db --chunk-size 2000
  
  python create_tscg_rag.py local --extensions md jsonld txt
  python create_tscg_rag.py local --verbose

NOTES:
  • Local mode: Uses sentence-transformers (no API key needed)
  • API mode: Requires Google API key in .api_key file
  • Segmentation strategies:
    - JSON-LD: By ontology entries (@graph)
    - Markdown: By sections (headers)
    - Code: By functions/classes
    - Plain text: By paragraphs with overlap
        """
    )
    
    parser.add_argument(
        "mode",
        choices=["local", "api"],
        help="Embedding mode: 'local' (sentence-transformers) or 'api' (Google)"
    )
    
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO_PATH,
        help=f"Path to TSCG repository (default: {DEFAULT_REPO_PATH})"
    )
    
    parser.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"Database output path (default: {DEFAULT_DB_PATH})"
    )
    
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=DEFAULT_EXTENSIONS,
        help=f"File extensions to index (default: {' '.join(DEFAULT_EXTENSIONS)})"
    )
    
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        help=f"Target chunk size in characters (default: {CHUNK_SIZE})"
    )
    
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=CHUNK_OVERLAP,
        help=f"Overlap between chunks (default: {CHUNK_OVERLAP})"
    )
    
    parser.add_argument(
        "--api-key",
        help="Path to API key file (for api mode)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress"
    )
    
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update existing database (incremental)"
    )
    
    return parser.parse_args()

# ==============================================================================
# INTELLIGENT SEGMENTATION (from tscg.engine.rag.segmentation)
# ==============================================================================

class Segment:
    """A document segment/chunk"""
    def __init__(self, text: str, metadata: Dict, start_char: int, end_char: int, segment_id: str):
        self.text = text
        self.metadata = metadata
        self.start_char = start_char
        self.end_char = end_char
        self.segment_id = segment_id
    
    @property
    def char_length(self):
        return len(self.text)
    
    @property
    def word_count(self):
        return len(self.text.split())


class TSCGSegmenter:
    """
    Intelligent segmentation for TSCG documents.
    
    Strategies:
    - JSON-LD: By ontology entries
    - Markdown: By sections
    - Code: By functions/classes
    - Plain text: By paragraphs
    """
    
    def __init__(self, chunk_size=1500, chunk_overlap=200, min_chunk_size=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def segment_file(self, filepath: str) -> List[Segment]:
        """Segment a file based on its type"""
        path = Path(filepath)
        
        # Read with encoding fallback
        encodings = ['utf-8', 'latin-1', 'cp1252']
        text = None
        
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    text = f.read()
                break
            except (UnicodeDecodeError, LookupError):
                continue
        
        if text is None:
            raise ValueError(f"Cannot decode file: {filepath}")
        
        # Choose strategy based on extension
        ext = path.suffix.lstrip('.')
        
        if ext in ['jsonld', 'json']:
            return self._segment_jsonld(text, str(path))
        elif ext in ['md', 'markdown']:
            return self._segment_markdown(text, str(path))
        elif ext in ['py', 'cs', 'fs']:
            return self._segment_code(text, str(path), ext)
        else:
            return self._segment_plain(text, str(path))
    
    def _segment_jsonld(self, text: str, source: str) -> List[Segment]:
        """Segment JSON-LD by ontology entries"""
        import json
        
        segments = []
        
        try:
            data = json.loads(text)
            
            if isinstance(data, dict) and '@graph' in data:
                # Segment each graph entry
                for i, entry in enumerate(data['@graph']):
                    entry_text = json.dumps(entry, indent=2, ensure_ascii=False)
                    
                    label = entry.get('rdfs:label', {})
                    if isinstance(label, dict):
                        label = label.get('@value', f'entry_{i}')
                    
                    segment = Segment(
                        text=entry_text,
                        metadata={
                            'source': source,
                            'type': 'jsonld_entry',
                            'label': str(label),
                            'uri': entry.get('@id', f'entry_{i}'),
                            'entry_index': i
                        },
                        start_char=0,
                        end_char=len(entry_text),
                        segment_id=f"{Path(source).stem}_entry_{i}"
                    )
                    
                    segments.append(segment)
            else:
                # Single object - one segment
                segment = Segment(
                    text=text,
                    metadata={
                        'source': source,
                        'type': 'jsonld_document'
                    },
                    start_char=0,
                    end_char=len(text),
                    segment_id=f"{Path(source).stem}_full"
                )
                segments.append(segment)
        
        except json.JSONDecodeError:
            # Fallback to plain text
            segments = self._segment_plain(text, source)
        
        return segments
    
    def _segment_markdown(self, text: str, source: str) -> List[Segment]:
        """Segment markdown by sections"""
        import re
        
        segments = []
        lines = text.split('\n')
        current_section = []
        current_header = None
        current_start = 0
        char_pos = 0
        
        header_pattern = re.compile(r'^#{1,6}\s+(.+)$')
        
        for line in lines:
            line_length = len(line) + 1
            header_match = header_pattern.match(line)
            
            if header_match:
                # Save previous section
                if current_section and len('\n'.join(current_section)) >= self.min_chunk_size:
                    section_text = '\n'.join(current_section)
                    segment = Segment(
                        text=section_text,
                        metadata={
                            'source': source,
                            'type': 'markdown_section',
                            'header': current_header or 'intro'
                        },
                        start_char=current_start,
                        end_char=char_pos,
                        segment_id=f"{Path(source).stem}_sec_{len(segments)}"
                    )
                    segments.append(segment)
                
                # Start new section
                current_section = [line]
                current_header = header_match.group(1).strip()
                current_start = char_pos
            else:
                current_section.append(line)
            
            char_pos += line_length
        
        # Add last section
        if current_section and len('\n'.join(current_section)) >= self.min_chunk_size:
            section_text = '\n'.join(current_section)
            segment = Segment(
                text=section_text,
                metadata={
                    'source': source,
                    'type': 'markdown_section',
                    'header': current_header or 'conclusion'
                },
                start_char=current_start,
                end_char=char_pos,
                segment_id=f"{Path(source).stem}_sec_{len(segments)}"
            )
            segments.append(segment)
        
        return segments if segments else self._segment_plain(text, source)
    
    def _segment_code(self, text: str, source: str, language: str) -> List[Segment]:
        """Segment code by functions/classes"""
        import re
        
        # Simple patterns for functions/classes
        if language == 'py':
            patterns = [(r'^class\s+\w+.*?:', 'class'), (r'^def\s+\w+.*?:', 'function')]
        elif language in ['cs', 'fs']:
            patterns = [(r'^\s*class\s+\w+', 'class'), (r'^\s*public\s+\w+\s+\w+\(', 'method')]
        else:
            return self._segment_plain(text, source)
        
        segments = []
        lines = text.split('\n')
        current_block = []
        current_type = None
        current_start = 0
        char_pos = 0
        
        for line in lines:
            line_length = len(line) + 1
            matched = False
            
            for pattern, block_type in patterns:
                if re.match(pattern, line):
                    # Save previous block
                    if current_block and len('\n'.join(current_block)) >= self.min_chunk_size:
                        block_text = '\n'.join(current_block)
                        segment = Segment(
                            text=block_text,
                            metadata={
                                'source': source,
                                'type': f'{language}_{current_type}',
                                'language': language
                            },
                            start_char=current_start,
                            end_char=char_pos,
                            segment_id=f"{Path(source).stem}_{current_type}_{len(segments)}"
                        )
                        segments.append(segment)
                    
                    current_block = [line]
                    current_type = block_type
                    current_start = char_pos
                    matched = True
                    break
            
            if not matched:
                current_block.append(line)
            
            char_pos += line_length
        
        # Add last block
        if current_block and len('\n'.join(current_block)) >= self.min_chunk_size:
            block_text = '\n'.join(current_block)
            segment = Segment(
                text=block_text,
                metadata={
                    'source': source,
                    'type': f'{language}_{current_type or "code"}',
                    'language': language
                },
                start_char=current_start,
                end_char=char_pos,
                segment_id=f"{Path(source).stem}_{current_type or 'code'}_{len(segments)}"
            )
            segments.append(segment)
        
        return segments if segments else self._segment_plain(text, source)
    
    def _segment_plain(self, text: str, source: str) -> List[Segment]:
        """Segment plain text by paragraphs"""
        segments = []
        paragraphs = text.split('\n\n')
        
        current_chunk = []
        current_length = 0
        current_start = 0
        char_pos = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                char_pos += 2
                continue
            
            para_length = len(para)
            
            if current_length + para_length > self.chunk_size and current_chunk:
                # Save chunk
                chunk_text = '\n\n'.join(current_chunk)
                segment = Segment(
                    text=chunk_text,
                    metadata={
                        'source': source,
                        'type': 'text_chunk'
                    },
                    start_char=current_start,
                    end_char=char_pos,
                    segment_id=f"{Path(source).stem}_chunk_{len(segments)}"
                )
                segments.append(segment)
                
                # Start new chunk with overlap
                if self.chunk_overlap > 0 and current_chunk:
                    current_chunk = [current_chunk[-1], para]
                    current_length = len(current_chunk[-2]) + para_length
                else:
                    current_chunk = [para]
                    current_length = para_length
                
                current_start = char_pos
            else:
                current_chunk.append(para)
                current_length += para_length
            
            char_pos += para_length + 2
        
        # Add last chunk
        if current_chunk and len('\n\n'.join(current_chunk)) >= self.min_chunk_size:
            chunk_text = '\n\n'.join(current_chunk)
            segment = Segment(
                text=chunk_text,
                metadata={
                    'source': source,
                    'type': 'text_chunk'
                },
                start_char=current_start,
                end_char=char_pos,
                segment_id=f"{Path(source).stem}_chunk_{len(segments)}"
            )
            segments.append(segment)
        
        return segments

# ==============================================================================
# EMBEDDINGS
# ==============================================================================

def get_embeddings(mode: str, api_key_path: Optional[str] = None, verbose: bool = False):
    """Get embeddings model based on mode"""
    if mode == "local":
        print("🔧 Using LOCAL embeddings (sentence-transformers)...")
        try:
            from sentence_transformers import SentenceTransformer
            if verbose:
                print("  ✓ sentence-transformers found")
        except ImportError:
            print("📦 Installing sentence-transformers...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers", "-q"])
            from sentence_transformers import SentenceTransformer
            print("  ✓ sentence-transformers installed")
        
        return SentenceTransformer('all-MiniLM-L6-v2')
    
    else:  # api mode
        print("🔧 Using GOOGLE API embeddings...")
        
        # Load API key
        if api_key_path and os.path.exists(api_key_path):
            key_file = api_key_path
        elif os.path.exists('../.api_key'):
            key_file = '../.api_key'
        elif os.path.exists('.api_key'):
            key_file = '.api_key'
        else:
            print("❌ No API key found. Place it in .api_key or ../.api_key")
            return None
        
        with open(key_file, 'r') as f:
            api_key = f.read().strip()
        
        os.environ['GOOGLE_API_KEY'] = api_key
        
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
# DOCUMENT COLLECTION
# ==============================================================================

def collect_files(repo_path: str, extensions: List[str], ignored_patterns: List[str], verbose: bool = False) -> List[str]:
    """Collect all files to index"""
    repo = Path(repo_path)
    
    if not repo.exists():
        print(f"❌ Repository not found: {repo_path}")
        return []
    
    files = []
    
    for ext in extensions:
        pattern_files = list(repo.rglob(f"*.{ext}"))
        
        # Filter ignored patterns
        filtered = []
        for f in pattern_files:
            rel_path = str(f.relative_to(repo))
            if not any(pattern in rel_path for pattern in ignored_patterns):
                filtered.append(f)
        
        files.extend(filtered)
        
        if verbose:
            print(f"  {ext}: {len(filtered)} files")
    
    return [str(f) for f in files]

# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main():
    """Main function"""
    args = parse_arguments()
    
    print("\n" + "="*70)
    print("  TSCG RAG Database Generator")
    print("="*70)
    print(f"Mode: {args.mode.upper()}")
    print(f"Repository: {args.repo}")
    print(f"Database: {args.db}")
    print(f"Extensions: {', '.join(args.extensions)}")
    print("="*70)
    
    # 1. Collect files
    print("\n📁 Collecting files...")
    files = collect_files(args.repo, args.extensions, IGNORED_PATTERNS, args.verbose)
    
    if not files:
        print("❌ No files found to index")
        return 1
    
    print(f"✓ Found {len(files)} files to index")
    
    # 2. Initialize segmenter
    print("\n🔧 Initializing segmenter...")
    segmenter = TSCGSegmenter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        min_chunk_size=MIN_CHUNK_SIZE
    )
    print(f"  Chunk size: {args.chunk_size} chars")
    print(f"  Overlap: {args.chunk_overlap} chars")
    
    # 3. Segment all files
    print("\n📄 Segmenting files...")
    all_segments = []
    
    for i, filepath in enumerate(files, 1):
        try:
            segments = segmenter.segment_file(filepath)
            all_segments.extend(segments)
            
            if args.verbose or i % 10 == 0:
                fname = Path(filepath).name
                print(f"  [{i}/{len(files)}] {fname}: {len(segments)} segments")
        
        except Exception as e:
            print(f"  ⚠️  Error segmenting {Path(filepath).name}: {e}")
            continue
    
    print(f"\n✓ Created {len(all_segments)} segments from {len(files)} files")
    print(f"  Average: {len(all_segments)/len(files):.1f} segments/file")
    
    # 4. Initialize embeddings
    print("\n🧠 Initializing embeddings...")
    embedder = get_embeddings(args.mode, args.api_key, args.verbose)
    
    if embedder is None:
        print("❌ Failed to initialize embeddings")
        return 1
    
    # 5. Create database
    print("\n🗄️  Creating ChromaDB database...")
    
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
        path=args.db,
        settings=Settings(anonymized_telemetry=False)
    )
    
    collection = client.get_or_create_collection(
        name="tscg_rag",
        metadata={"hnsw:space": "cosine"}
    )
    
    # 6. Add segments to database
    print("\n💾 Adding segments to database...")
    
    batch_size = 50 if args.mode == "local" else 5
    total_added = 0
    
    for i in range(0, len(all_segments), batch_size):
        batch = all_segments[i:i+batch_size]
        
        # Prepare batch data
        texts = [seg.text for seg in batch]
        metadatas = [seg.metadata for seg in batch]
        ids = [seg.segment_id for seg in batch]
        
        # Generate embeddings
        if args.mode == "local":
            embeddings = embedder.encode(texts).tolist()
        else:
            embeddings = [embedder.embed_query(text) for text in texts]
        
        # Add to collection
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        total_added += len(batch)
        
        if args.verbose or total_added % 100 == 0:
            print(f"  Added {total_added}/{len(all_segments)} segments...")
    
    print(f"\n✓ Added {total_added} segments to database")
    
    # 7. Save metadata
    metadata = {
        "mode": args.mode,
        "repo_path": args.repo,
        "extensions": args.extensions,
        "total_files": len(files),
        "total_segments": len(all_segments),
        "chunk_size": args.chunk_size,
        "chunk_overlap": args.chunk_overlap,
        "created_at": datetime.datetime.now().isoformat(),
        "embedding_model": "all-MiniLM-L6-v2" if args.mode == "local" else "gemini-embedding-001"
    }
    
    os.makedirs(args.db, exist_ok=True)
    with open(f"{args.db}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    # 8. Summary
    print("\n" + "="*70)
    print("  ✅ TSCG RAG Database Created Successfully!")
    print("="*70)
    print(f"\n📊 Statistics:")
    print(f"  Files indexed: {len(files)}")
    print(f"  Segments created: {len(all_segments)}")
    print(f"  Average segments/file: {len(all_segments)/len(files):.1f}")
    print(f"  Database path: {args.db}")
    print(f"  Embedding mode: {args.mode.upper()}")
    print("\n💡 Next steps:")
    print(f"  1. Query the database with query_tscg_rag.py")
    print(f"  2. Integrate with your application")
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
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
