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
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
import datetime

# Force UTF-8 output so emoji characters render correctly on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ==============================================================================
# CONFIGURATION
# ==============================================================================

DEFAULT_EXTENSIONS = ['md', 'jsonld', 'txt', 'py', 'cs', 'fs']
IGNORED_PATTERNS = ['bin/', 'obj/', '.git/', '__pycache__/', 'node_modules/']
DEFAULT_DB_PATH = './db_tscg_rag'

# Script lives at <repo_root>/src/tscg/rag/create_tscg_rag.py
# Walk up: rag/ -> tscg/ -> src/ -> repo_root/
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_REPO_PATH = str(_REPO_ROOT)

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

    parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Skip compressing the database to .tar.gz after creation"
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


def _source_prefix(source: str) -> str:
    """Return a globally unique prefix for segment IDs: stem + 6-char path hash."""
    path_hash = hashlib.md5(source.encode()).hexdigest()[:6]
    return f"{Path(source).stem}_{path_hash}"


# OWL/RDF infrastructure types that carry no RAG value as standalone segments
_SKIP_TYPES = {
    "owl:ObjectProperty", "owl:DatatypeProperty", "owl:AnnotationProperty",
    "owl:TransitiveProperty", "owl:SymmetricProperty", "owl:FunctionalProperty",
    "owl:Ontology", "skos:ConceptScheme", "rdf:Property",
}


def _entry_to_text(entry: dict, layer: str) -> str | None:
    """
    Convert a JSON-LD @graph entry to a natural-language summary for embedding.
    Returns None for OWL infrastructure entries that should be skipped.
    """
    # Normalise @type to a set of strings
    raw_type = entry.get("@type", "")
    types = set(raw_type if isinstance(raw_type, list) else [raw_type])

    # Skip pure OWL/RDF infrastructure
    if types & _SKIP_TYPES:
        return None

    parts = []

    # ── Name ──────────────────────────────────────────────────────────────────
    label = entry.get("rdfs:label", "")
    if isinstance(label, dict):
        label = label.get("@value", "")
    if not label:
        entry_id = entry.get("@id", "")
        label = entry_id.split(":")[-1].replace("_", " ") if entry_id else ""
    if not label:
        return None

    # ── Family / perspective (M2) ─────────────────────────────────────────────
    subclass = entry.get("rdfs:subClassOf", "")
    families = []
    for s in (subclass if isinstance(subclass, list) else [subclass]):
        if isinstance(s, str) and s not in ("m2:MetaConcept", "m2:MetaconceptPair",
                                             "m2:MetaconceptCombo", ""):
            families.append(s.split(":")[-1])
    perspective = entry.get("m2:perspective", "")

    header = f"{label} [{layer}"
    if families:
        header += f" / {families[0]}"
    if perspective:
        header += f" / {perspective}"
    header += "]"
    parts.append(header)

    # ── Tensor formula ────────────────────────────────────────────────────────
    formula = (entry.get("m2:hasTensorFormula")
               or entry.get("m3:tensorFormula")
               or entry.get("tscg:tensorFormula", ""))
    if formula:
        dominant = entry.get("m2:hasDominantM3", [])
        if isinstance(dominant, str):
            dominant = [dominant]
        dim_names = [d.split(":")[-1] for d in dominant if isinstance(d, str)]
        if dim_names:
            parts.append(f"Tensor formula: {formula} ({', '.join(dim_names)})")
        else:
            parts.append(f"Tensor formula: {formula}")

    # ── Definition ────────────────────────────────────────────────────────────
    comment = entry.get("rdfs:comment") or entry.get("dcterms:description", "")
    if isinstance(comment, dict):
        comment = comment.get("@value", "")
    if comment:
        parts.append(f"Definition: {comment}")

    # ── Polarity / epistemic gap ──────────────────────────────────────────────
    polarity = entry.get("m2:hasPolarity", "")
    gap = entry.get("m2:hasEpistemicGap", "")
    meta = []
    if polarity:
        meta.append(f"Polarity: {polarity}")
    if gap != "":
        meta.append(f"Epistemic gap: {gap:.2f}" if isinstance(gap, float) else f"Epistemic gap: {gap}")
    if meta:
        parts.append(" | ".join(meta))

    # ── Examples ─────────────────────────────────────────────────────────────
    examples = entry.get("m2:hasExample", []) or entry.get("m3:dimensionExamples", [])
    if isinstance(examples, str):
        examples = [examples]
    if examples:
        parts.append(f"Examples: {'; '.join(str(e) for e in examples[:4])}")

    # ── M3 dimension symbol ───────────────────────────────────────────────────
    symbol = entry.get("m3:dimensionSymbol", "")
    if symbol:
        parts.append(f"Symbol: {symbol}")

    # Need at least a definition or formula to be worth indexing
    if len(parts) < 2:
        return None

    return "\n".join(parts)


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
        """Segment JSON-LD by ontology entries, converting each to natural language."""
        import json

        segments = []

        # Infer TSCG layer from filename prefix (M0_, M1_, M2_, M3_)
        stem = Path(source).stem.upper()
        layer = "M2"  # default
        for prefix in ("M3_", "M2_", "M1_", "M0_"):
            if stem.startswith(prefix):
                layer = prefix.rstrip("_")
                break

        try:
            data = json.loads(text)

            if isinstance(data, dict) and '@graph' in data:
                for i, entry in enumerate(data['@graph']):
                    # Convert to natural language; skip OWL infrastructure entries
                    nl_text = _entry_to_text(entry, layer)
                    if nl_text is None:
                        continue

                    label = entry.get('rdfs:label', {})
                    if isinstance(label, dict):
                        label = label.get('@value', f'entry_{i}')

                    segment = Segment(
                        text=nl_text,
                        metadata={
                            'source': source,
                            'type': 'jsonld_entry',
                            'label': str(label),
                            'uri': entry.get('@id', f'entry_{i}'),
                            'entry_index': i,
                            'layer': layer,
                        },
                        start_char=0,
                        end_char=len(nl_text),
                        segment_id=f"{_source_prefix(source)}_entry_{i}"
                    )
                    segments.append(segment)
            else:
                # Single object — one segment
                nl_text = _entry_to_text(data, layer) or json.dumps(data, indent=2, ensure_ascii=False)
                segment = Segment(
                    text=nl_text,
                    metadata={'source': source, 'type': 'jsonld_document', 'layer': layer},
                    start_char=0,
                    end_char=len(nl_text),
                    segment_id=f"{_source_prefix(source)}_full"
                )
                segments.append(segment)

        except json.JSONDecodeError:
            segments = self._segment_plain(text, source)

        return segments
    
    def _segment_markdown(self, text: str, source: str) -> List[Segment]:
        """Segment markdown by sections, preserving parent-header breadcrumb."""
        import re

        segments = []
        lines = text.split('\n')
        current_section = []
        current_header = None
        current_start = 0
        char_pos = 0

        # Track header hierarchy: level (1-6) -> header text
        header_stack: dict = {}

        # Tag files under ontology/docs as authoritative ontology documentation
        source_path = Path(source)
        is_ontology_doc = 'ontology' in source_path.parts and 'docs' in source_path.parts

        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

        def breadcrumb() -> str:
            """Return 'GrandParent > Parent > Current' from the header stack."""
            return ' > '.join(header_stack[lvl] for lvl in sorted(header_stack))

        def flush(section_lines, header, start, end):
            if not section_lines:
                return
            section_text = '\n'.join(section_lines)
            if len(section_text) < self.min_chunk_size:
                return
            crumb = breadcrumb()
            meta = {
                'source': source,
                'type': 'markdown_section',
                'header': header or 'intro',
                'breadcrumb': crumb,
            }
            if is_ontology_doc:
                meta['ontology_doc'] = True
            # Prepend breadcrumb to text when it adds context
            if crumb and crumb != (header or ''):
                full_text = f"[{crumb}]\n{section_text}"
            else:
                full_text = section_text
            segments.append(Segment(
                text=full_text,
                metadata=meta,
                start_char=start,
                end_char=end,
                segment_id=f"{_source_prefix(source)}_sec_{len(segments)}"
            ))

        for line in lines:
            line_length = len(line) + 1
            header_match = header_pattern.match(line)

            if header_match:
                flush(current_section, current_header, current_start, char_pos)

                level = len(header_match.group(1))
                current_header = header_match.group(2).strip()

                # Drop all headers at same level or deeper, then set current
                for lvl in list(header_stack.keys()):
                    if lvl >= level:
                        del header_stack[lvl]
                header_stack[level] = current_header

                current_section = [line]
                current_start = char_pos
            else:
                current_section.append(line)

            char_pos += line_length

        flush(current_section, current_header, current_start, char_pos)

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
                            segment_id=f"{_source_prefix(source)}_{current_type}_{len(segments)}"
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
                segment_id=f"{_source_prefix(source)}_{current_type or 'code'}_{len(segments)}"
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
                    segment_id=f"{_source_prefix(source)}_chunk_{len(segments)}"
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
                segment_id=f"{_source_prefix(source)}_chunk_{len(segments)}"
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

def compress_db(db_path: str, verbose: bool = False) -> tuple:
    """Compress the ChromaDB directory to a .tar.gz archive for git storage."""
    import tarfile
    db = Path(db_path).resolve()
    archive_path = db.parent / f"{db.name}.tar.gz"

    if verbose:
        print(f"  Compressing {db.name}/ → {archive_path.name} ...")

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(db, arcname=db.name)

    size_mb = archive_path.stat().st_size / (1024 * 1024)
    return str(archive_path), size_mb


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

    # Deduplicate segments with identical content (same file in multiple directories)
    seen_hashes = set()
    unique_segments = []
    for seg in all_segments:
        h = hashlib.md5(seg.text.encode()).hexdigest()
        if h not in seen_hashes:
            seen_hashes.add(h)
            unique_segments.append(seg)
    duplicates_removed = len(all_segments) - len(unique_segments)
    if duplicates_removed:
        print(f"  Removed {duplicates_removed} duplicate segments (same content, different paths)")
    all_segments = unique_segments

    print(f"  Unique segments: {len(all_segments)} | Average: {len(all_segments)/len(files):.1f} segments/file")
    
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
    
    # 8. Compress database (default: on)
    archive_info = ""
    if not args.no_compress:
        print("\n🗜️  Compressing database for git storage...")
        archive_path, size_mb = compress_db(args.db, args.verbose)
        archive_info = f"  Archive: {archive_path} ({size_mb:.1f} MB)"
        print(f"✓ Compressed → {Path(archive_path).name} ({size_mb:.1f} MB)")
        print(f"  Tip: add '{Path(args.db).name}/' to .gitignore and commit the .tar.gz")

    # 9. Summary
    print("\n" + "="*70)
    print("  ✅ TSCG RAG Database Created Successfully!")
    print("="*70)
    print(f"\n📊 Statistics:")
    print(f"  Files indexed: {len(files)}")
    print(f"  Segments created: {len(all_segments)}")
    print(f"  Average segments/file: {len(all_segments)/len(files):.1f}")
    print(f"  Database path: {args.db}")
    print(f"  Embedding mode: {args.mode.upper()}")
    if archive_info:
        print(archive_info)
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
