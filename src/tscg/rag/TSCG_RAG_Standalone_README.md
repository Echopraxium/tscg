# TSCG RAG - Standalone Scripts

**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** February 12, 2026

---

## 📋 Overview

Two standalone Python scripts for creating and querying a RAG (Retrieval-Augmented Generation) database for the TSCG repository:

1. **`create_tscg_rag.py`** - Generate the RAG database
2. **`query_tscg_rag.py`** - Query the database

These scripts combine the best features from:
- ✅ **Intelligent segmentation** (preserves ontology structure)
- ✅ **Simple CLI interface** (api/local modes)
- ✅ **ChromaDB storage** (industry standard)
- ✅ **Minimal dependencies** (no heavy LangChain core)

---

## 🚀 Quick Start

### 1. Create RAG Database

```bash
# Using local embeddings (recommended, no API key needed)
python create_tscg_rag.py local

# Or using Google API embeddings (requires API key)
python create_tscg_rag.py api
```

**Output:**
- Database created in `./db_tscg_rag/`
- Indexes all `.md`, `.jsonld`, `.txt`, `.py`, `.cs`, `.fs` files
- Uses intelligent segmentation by file type

### 2. Query Database

```bash
# Single query
python query_tscg_rag.py "What is TSCG?"

# Interactive mode
python query_tscg_rag.py --interactive

# Show more results
python query_tscg_rag.py "metaconcept tensor formula" --top-k 10

# Show full text
python query_tscg_rag.py "ASFID dimensions" --show-text
```

---

## 📦 Installation

### Minimal Dependencies

```bash
# For local mode (recommended)
pip install sentence-transformers chromadb

# For API mode (optional)
pip install langchain-google-genai chromadb
```

### Full Installation

```bash
pip install sentence-transformers chromadb langchain-google-genai
```

---

## 🎯 Features

### Intelligent Segmentation

The scripts use the same intelligent segmentation from `tscg.engine.rag.segmentation`:

| File Type | Strategy | Example |
|-----------|----------|---------|
| **JSON-LD** | By ontology entries | Each `@graph` entry = 1 segment |
| **Markdown** | By sections | Each header (`#`, `##`) = 1 segment |
| **Code** (.py, .cs, .fs) | By functions/classes | Each function/class = 1 segment |
| **Plain text** | By paragraphs | Paragraphs grouped ~1500 chars with overlap |

### Benefits Over Simple Chunking

❌ **Simple chunking:**
```json
{
  "@id": "m2:Attractor",
  "rdfs:label": "The Attr───┐  ← Segment 1 ends
                            │
actor concept represents...─┘  ← Segment 2 starts
```

✅ **Intelligent segmentation:**
```json
Segment 1 (complete):
{
  "@id": "m2:Attractor",
  "rdfs:label": "The Attractor concept represents...",
  "tscg:tensorFormula": "A"
}

Segment 2 (next complete entry):
{
  "@id": "m2:Structure",
  ...
}
```

---

## 📖 Detailed Usage

### create_tscg_rag.py

```bash
python create_tscg_rag.py local [OPTIONS]
python create_tscg_rag.py api [OPTIONS]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--repo PATH` | `..` | Path to TSCG repository |
| `--db PATH` | `./db_tscg_rag` | Output database path |
| `--extensions EXT...` | `md jsonld txt py cs fs` | File extensions to index |
| `--chunk-size N` | `1500` | Target chunk size (chars) |
| `--chunk-overlap N` | `200` | Overlap between chunks |
| `--api-key PATH` | `.api_key` | API key file (for api mode) |
| `--verbose` | - | Show detailed progress |
| `--update` | - | Update existing database |

**Examples:**

```bash
# Basic usage
python create_tscg_rag.py local

# Custom repository path
python create_tscg_rag.py local --repo /path/to/tscg

# Only markdown and JSON-LD
python create_tscg_rag.py local --extensions md jsonld

# Larger chunks
python create_tscg_rag.py local --chunk-size 2000 --chunk-overlap 300

# API mode with custom key
python create_tscg_rag.py api --api-key /path/to/.api_key

# Verbose output
python create_tscg_rag.py local --verbose
```

### query_tscg_rag.py

```bash
python query_tscg_rag.py "QUERY" [OPTIONS]
python query_tscg_rag.py --interactive
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--db PATH` | `./db_tscg_rag` | Database path |
| `--top-k N` | `5` | Number of results |
| `--interactive` / `-i` | - | Interactive mode |
| `--show-text` | - | Show full segment text |
| `--filter-type TYPE` | - | Filter by segment type |
| `--verbose` | - | Show detailed information |

**Examples:**

```bash
# Simple query
python query_tscg_rag.py "What is TSCG?"

# More results
python query_tscg_rag.py "feedback control" --top-k 10

# Show full text
python query_tscg_rag.py "ASFID dimensions" --show-text

# Filter by type
python query_tscg_rag.py "metaconcept" --filter-type jsonld_entry

# Interactive mode
python query_tscg_rag.py -i
```

---

## 🎮 Interactive Mode

```bash
$ python query_tscg_rag.py --interactive

======================================================================
  TSCG RAG - Interactive Query Mode
======================================================================
Commands: 'stats', 'sources', 'exit'
Or enter a search query
======================================================================

❓ Query: What is ASFID?

🔍 Searching...

1. M3_EagleEye.jsonld [jsonld_entry] - Score: 0.892
   Label: ASFID Dimensions
   URI: http://tscg.org/m3/eagle_eye#ASFID
   Excerpt: The ASFID dimensions represent the Territory perspective...

2. TSCG_Documentation.md [markdown_section] - Score: 0.845
   Section: ASFID Overview
   Excerpt: ASFID stands for Attractor, Structure, Flow...

❓ Query: stats

📊 Database Statistics
============================================================
Created: 2026-02-12T14:30:00
Repository: ..
Embedding mode: LOCAL
Chunk size: 1500
Chunk overlap: 200

Total segments: 487
Total files: 56

Segments by type:
  jsonld_entry: 245
  markdown_section: 156
  text_chunk: 58
  py_function: 28

❓ Query: exit

👋 Goodbye!
```

---

## 📊 Output Structure

### Database Directory

```
db_tscg_rag/
├── chroma.sqlite3          # ChromaDB storage
├── metadata.json           # Database metadata
└── ...                     # ChromaDB internal files
```

### metadata.json

```json
{
  "mode": "local",
  "repo_path": "..",
  "extensions": ["md", "jsonld", "txt", "py", "cs", "fs"],
  "total_files": 56,
  "total_segments": 487,
  "chunk_size": 1500,
  "chunk_overlap": 200,
  "created_at": "2026-02-12T14:30:00",
  "embedding_model": "all-MiniLM-L6-v2"
}
```

---

## 🔧 Advanced Usage

### Custom Segmentation

Modify chunk parameters for different needs:

```bash
# Small chunks for precise retrieval
python create_tscg_rag.py local --chunk-size 1000 --chunk-overlap 100

# Large chunks for more context
python create_tscg_rag.py local --chunk-size 2500 --chunk-overlap 500

# No overlap (faster, less context)
python create_tscg_rag.py local --chunk-size 1500 --chunk-overlap 0
```

### Filter by Segment Type

```bash
# Only JSON-LD ontology entries
python query_tscg_rag.py "attractor" --filter-type jsonld_entry

# Only markdown sections
python query_tscg_rag.py "architecture" --filter-type markdown_section

# Only code segments
python query_tscg_rag.py "function" --filter-type py_function
```

### Update Existing Database

```bash
# Add new files to existing database
python create_tscg_rag.py local --update
```

---

## 🆚 Comparison with Other Scripts

| Feature | create_RAG.py | create_RAG_lan.py | **create_tscg_rag.py** ✅ |
|---------|--------------|-------------------|---------------------------|
| Segmentation | RecursiveCharacterTextSplitter | Manual paragraphs | **Intelligent by type** |
| JSON-LD | Simple chunks | Not supported | **By ontology entries** |
| Markdown | Simple chunks | Not supported | **By sections** |
| Code | Simple chunks | Not supported | **By functions/classes** |
| Dependencies | LangChain (heavy) | ChromaDB + ST | **Minimal** |
| CLI | api/local ✅ | api/local ✅ | **api/local** ✅ |
| Embeddings | Google or Local | Google or Local | **Google or Local** |

---

## 💡 Tips & Best Practices

### 1. Use Local Mode First

```bash
# No API key needed, works offline
python create_tscg_rag.py local
```

### 2. Test with Small Corpus

```bash
# Index only markdown files first
python create_tscg_rag.py local --extensions md
```

### 3. Adjust Chunk Size

- **Small chunks (1000)**: More precise, more segments
- **Medium chunks (1500)**: Balanced (recommended)
- **Large chunks (2500)**: More context, fewer segments

### 4. Use Interactive Mode for Exploration

```bash
python query_tscg_rag.py -i
```

### 5. Filter Results by Type

```bash
# Find only ontology concepts
python query_tscg_rag.py "metaconcept" --filter-type jsonld_entry
```

---

## 🐛 Troubleshooting

### Database not found

```bash
❌ Database not found: ./db_tscg_rag
   Create it first with: python create_tscg_rag.py local
```

**Solution:** Run `create_tscg_rag.py` first

### No results found

**Possible causes:**
1. Query too specific
2. Wrong filter type
3. Database empty

**Solutions:**
- Try broader queries
- Remove `--filter-type`
- Check database with `stats` command

### API key errors (api mode)

```bash
❌ No API key found. Place it in .api_key or ../.api_key
```

**Solution:** Create `.api_key` file with your Google API key

### Import errors

```bash
📦 Installing sentence-transformers...
```

**Note:** Dependencies auto-install on first run

---

## 📝 Example Workflow

```bash
# 1. Create database (one-time)
python create_tscg_rag.py local --verbose

# Output:
# ✓ Found 56 files to index
# ✓ Created 487 segments from 56 files
# ✓ Added 487 segments to database

# 2. Query the database
python query_tscg_rag.py "What is the bicephalous architecture?"

# 3. Explore interactively
python query_tscg_rag.py -i

❓ Query: stats
❓ Query: ASFID dimensions
❓ Query: sources
❓ Query: exit

# 4. Update with new files
python create_tscg_rag.py local --update
```

---

## 🎓 How It Works

### 1. Segmentation

```python
# Intelligent segmentation by file type
if file.endswith('.jsonld'):
    segments = segment_by_ontology_entries(file)
elif file.endswith('.md'):
    segments = segment_by_sections(file)
elif file.endswith('.py'):
    segments = segment_by_functions(file)
else:
    segments = segment_by_paragraphs(file)
```

### 2. Embedding

```python
# Generate vector embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # or Google API
embeddings = embedder.encode(segments)
```

### 3. Storage

```python
# Store in ChromaDB
collection.add(
    embeddings=embeddings,
    documents=texts,
    metadatas=metadatas,
    ids=segment_ids
)
```

### 4. Query

```python
# Semantic search
query_embedding = embedder.encode(query)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=top_k
)
```

---

## 📚 Additional Resources

- **TSCG Repository:** https://github.com/Echopraxium/tscg
- **ChromaDB Docs:** https://docs.trychroma.com/
- **Sentence Transformers:** https://www.sbert.net/

---

**Ready to create your TSCG RAG database!** 🚀

```bash
python create_tscg_rag.py local
python query_tscg_rag.py --interactive
```
