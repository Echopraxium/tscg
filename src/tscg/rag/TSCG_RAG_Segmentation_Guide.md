# TSCG RAG - Intelligent Document Segmentation

**Version:** 0.1.0  
**Author:** Echopraxium with the collaboration of Claude AI

---

## Overview

The TSCG RAG module now includes **intelligent document segmentation** that adapts to different file types, preserving semantic boundaries and document structure.

Instead of using simple character-based chunking, the segmenter:
- **Preserves meaning** by respecting document structure
- **Optimizes retrieval** with semantically coherent chunks
- **Maintains context** by keeping related content together

---

## Segmentation Strategies

### JSON-LD Files (.jsonld)

**Strategy:** Segment by ontology entries

Each entry in the `@graph` array becomes a separate segment, preserving:
- Complete metaconcept definitions
- All properties and relationships
- Ontology structure

**Example:**
```json
{
  "@graph": [
    {"@id": "m2:Attractor", "rdfs:label": "..."},  // Segment 1
    {"@id": "m2:Structure", "rdfs:label": "..."},  // Segment 2
    ...
  ]
}
```

**Benefits:**
- Each segment is a complete, self-contained concept
- No split metaconcept definitions
- Perfect for semantic search of individual concepts

### Markdown Files (.md)

**Strategy:** Segment by sections (headers)

Each markdown section becomes a segment:
- `#` Level 1 headers → Major sections
- `##` Level 2 headers → Subsections
- etc.

**Example:**
```markdown
# Introduction          ← Segment 1 starts
Content here...

## Background          ← Segment 2 starts  
More content...

### Details            ← Segment 3 starts
Detailed info...
```

**Benefits:**
- Preserves document hierarchy
- Keeps related paragraphs together
- Natural semantic boundaries

### Code Files (.py, .cs, .fs)

**Strategy:** Segment by functions/classes

Each function or class becomes a segment:

**Python Example:**
```python
class MyClass:         ← Segment 1
    def __init__(...):
        ...

def my_function():     ← Segment 2
    ...
```

**Benefits:**
- Complete function/class definitions
- Preserves code structure
- Easier to find specific implementations

### Plain Text (.txt)

**Strategy:** Segment by paragraphs with size limits

Groups paragraphs into chunks of ~1500 characters with overlap:

```
Paragraph 1
Paragraph 2           } Segment 1 (with overlap)
────────────
Paragraph 2 (overlap)
Paragraph 3           } Segment 2 (with overlap)
Paragraph 4
────────────
Paragraph 4 (overlap)
Paragraph 5           } Segment 3
```

**Benefits:**
- Respects natural paragraph boundaries
- Maintains context with overlap
- Adaptable chunk sizes

---

## Configuration

```python
from tscg.engine.rag.segmentation import TSCGSegmenter

segmenter = TSCGSegmenter(
    chunk_size=1500,        # Target chunk size (characters)
    chunk_overlap=200,      # Overlap between chunks
    min_chunk_size=100,     # Minimum chunk to keep
    preserve_structure=True # Preserve document structure
)
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chunk_size` | 1500 | Target size for chunks (in characters) |
| `chunk_overlap` | 200 | Overlap between consecutive chunks |
| `min_chunk_size` | 100 | Minimum size to keep a chunk |
| `preserve_structure` | True | Preserve headers, code blocks, etc. |

---

## Usage Examples

### Basic Segmentation

```python
from tscg.engine.rag.segmentation import TSCGSegmenter

segmenter = TSCGSegmenter()

# Segment a file
segments = segmenter.segment_file("M2_MetaConcepts.jsonld")

print(f"Created {len(segments)} segments")
for seg in segments:
    print(f"  - {seg.segment_id}: {seg.char_length} chars")
```

### With RAG Facade

```python
from tscg.engine.facade import RAGFacade

rag = RAGFacade()

# Index directory - segmentation happens automatically
rag.index_directory(
    "/mnt/project",
    extensions=['md', 'jsonld', 'txt'],
    recursive=True
)

# Search returns segments, not full documents
results = rag.search_documents("feedback control", top_k=5)

for result in results:
    print(f"Source: {result.metadata['source']}")
    print(f"Type: {result.metadata['type']}")
    print(f"Score: {result.score:.3f}")
```

### Custom Segmentation

```python
from tscg.engine.rag.segmentation import TSCGSegmenter

# Create custom segmenter
segmenter = TSCGSegmenter(
    chunk_size=2000,     # Larger chunks
    chunk_overlap=300,   # More overlap
    min_chunk_size=200   # Larger minimum
)

# Segment text directly
text = """
# My Document

Some content here...
"""

segments = segmenter.segment_text(
    text,
    source="my_doc.md",
    file_type="md"
)
```

---

## Segment Metadata

Each segment includes rich metadata:

```python
segment = segments[0]

print(segment.text)          # The actual text
print(segment.segment_id)    # Unique ID (e.g., "M2_MetaConcepts_entry_0")
print(segment.start_char)    # Start position in original
print(segment.end_char)      # End position in original
print(segment.char_length)   # Length in characters
print(segment.word_count)    # Word count

# Metadata varies by type
meta = segment.metadata
print(meta['source'])        # Source file
print(meta['type'])          # Segment type (jsonld_entry, markdown_section, etc.)

# Type-specific metadata
if meta['type'] == 'jsonld_entry':
    print(meta['label'])     # Metaconcept label
    print(meta['uri'])       # Metaconcept URI

elif meta['type'] == 'markdown_section':
    print(meta['header'])    # Section header
    print(meta['section_level'])  # Header level (1-6)

elif meta['type'] == 'py_function':
    print(meta['name'])      # Function name
    print(meta['language'])  # Programming language
```

---

## Comparison with Simple Chunking

### Simple Character-Based Chunking ❌

```
Problem: Splits mid-sentence or mid-concept

{
  "@id": "m2:Attractor",
  "rdfs:label": "The Attr────┐  ← Segment 1 ends here
                              │
actor concept represents...───┘  ← Segment 2 starts here
  "tscg:tensorFormula": "A"
}
```

**Issues:**
- Broken JSON
- Incomplete definitions
- Lost semantic meaning

### Intelligent Segmentation ✅

```
Segment 1: Complete entry
{
  "@id": "m2:Attractor",
  "rdfs:label": "The Attractor concept represents...",
  "tscg:tensorFormula": "A"
}

Segment 2: Next complete entry
{
  "@id": "m2:Structure",
  "rdfs:label": "The Structure concept...",
  ...
}
```

**Benefits:**
- ✅ Valid JSON in each segment
- ✅ Complete, searchable concepts
- ✅ Preserved semantic boundaries

---

## Advanced Features

### Filtering by Segment Type

```python
from tscg.engine.facade import RAGFacade

rag = RAGFacade()
rag.index_directory("/mnt/project")

# Search only JSON-LD ontology entries
def jsonld_filter(metadata):
    return metadata.get('type') == 'jsonld_entry'

results = rag.search_documents(
    "attractor dynamics",
    top_k=10,
    filter_fn=jsonld_filter
)

# Search only markdown sections
def markdown_filter(metadata):
    return metadata.get('type') == 'markdown_section'

results = rag.search_documents(
    "architecture guide",
    filter_fn=markdown_filter
)
```

### Large Segment Handling

If a segment exceeds `chunk_size` after initial segmentation, it's automatically split:

```python
# Long markdown section
section_text = "# Very Long Section\n" + ("..." * 2000)

segments = segmenter.segment_text(section_text, "doc.md", "md")

# Will be split into multiple parts:
# doc_sec_0_part_0
# doc_sec_0_part_1
# doc_sec_0_part_2
```

---

## Performance Considerations

### Memory

- Segmentation is done **once** during indexing
- Segments are stored with embeddings in vector store
- Low memory overhead

### Speed

- **JSON-LD:** Fast (one pass, JSON parsing)
- **Markdown:** Fast (regex for headers)
- **Code:** Medium (pattern matching)
- **Plain text:** Fast (paragraph splitting)

### Index Size

Intelligent segmentation typically creates:
- **Fewer segments** than simple chunking (better structure)
- **More meaningful segments** (better retrieval)

**Example:**
- Simple chunking: 1000 chars → many small chunks
- Intelligent: Complete concepts → fewer, larger chunks

---

## Best Practices

1. **Use appropriate chunk_size for your content**
   - Technical docs: 1500-2000 chars
   - Ontologies: Auto-sized per entry
   - Code: Auto-sized per function

2. **Enable preserve_structure** (default: True)
   - Keeps semantic boundaries
   - Better search results

3. **Set min_chunk_size** to avoid tiny segments
   - Default 100 chars is good
   - Increase for technical content

4. **Use overlap** for context preservation
   - 200 chars default works well
   - Increase for dense technical text

---

## Troubleshooting

### Segments too large

```python
# Reduce chunk_size
segmenter = TSCGSegmenter(chunk_size=1000)
```

### Segments too small

```python
# Increase min_chunk_size
segmenter = TSCGSegmenter(min_chunk_size=300)
```

### Missing content in search

```python
# Increase overlap for better context
segmenter = TSCGSegmenter(chunk_overlap=400)
```

### Wrong segmentation strategy

```python
# Force specific file type
segments = segmenter.segment_text(text, "file.xyz", file_type="md")
```

---

## Future Enhancements

Planned improvements:

- [ ] XML/RDF segmentation
- [ ] LaTeX document segmentation
- [ ] Multi-language code detection
- [ ] Semantic similarity-based merging
- [ ] Configurable segmentation rules
- [ ] Custom regex patterns

---

**Ready to use intelligent segmentation in your TSCG RAG system!** 🚀
