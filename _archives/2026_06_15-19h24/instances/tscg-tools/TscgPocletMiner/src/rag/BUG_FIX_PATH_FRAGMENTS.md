# Bug Fix: IGNORED_PATH_FRAGMENTS causing excessive file exclusion

**Date:** 2026-04-06  
**Issue:** RagBuilder.js indexed only 469 files instead of 1342  
**Root cause:** Missing trailing slashes in exclusion patterns  

## 🐛 The Bug

### Original code (WRONG):
```javascript
const IGNORED_PATH_FRAGMENTS = [
  'node_modules', '.git', '__pycache__', 'bin/', 'obj/',
  'db_tscg_rag', '_archives', '_protos',  // ← Missing slashes!
];
```

### How the check works:
```javascript
if (IGNORED_PATH_FRAGMENTS.some(f => rel.includes(f))) continue;
```

### The problem:

Without trailing slashes, patterns match **anywhere** in the path:

**Example with `'bin'`:**
- ✅ `src/bin/tool.py` → Should be excluded → Correctly excluded
- ❌ `docs/combinatorics.md` → Should be included → WRONGLY EXCLUDED (contains "bin")
- ❌ `utils/robin_algo.js` → Should be included → WRONGLY EXCLUDED (contains "bin")
- ❌ `analysis/combine.py` → Should be included → WRONGLY EXCLUDED (contains "bin")

**Example with `'_protos'`:**
- ✅ `ontology/_protos/draft.jsonld` → Should be excluded → Correctly excluded
- ❌ `src/file_protos.py` → Should be included → WRONGLY EXCLUDED (contains "_protos")

**Example with `'_archives'`:**
- ✅ `old/_archives/backup.tar` → Should be excluded → Correctly excluded
- ❌ `utils/parse_archives.js` → Should be included → WRONGLY EXCLUDED (contains "_archives")

## ✅ The Fix

### Corrected code:
```javascript
const IGNORED_PATH_FRAGMENTS = [
  'node_modules/', '.git/', '__pycache__/', 'bin/', 'obj/',
  'db_tscg_rag/', '_archives/', '_protos/',  // ← All have trailing slashes
];
```

### Why this works:

With trailing slashes, patterns only match **directory boundaries**:

- `'bin/'` matches `src/bin/` but NOT `combinatorics` or `robin`
- `'_protos/'` matches `_protos/` but NOT `file_protos.py`
- `'_archives/'` matches `_archives/` but NOT `parse_archives.js`

## 📊 Expected Result

After applying this fix:

```
Before: 469 files indexed (many false exclusions)
After:  ~1342 files indexed (matching Python version)
```

## 🎯 Alignment with Python

Python version uses the same pattern:
```python
IGNORED_PATTERNS = ['bin/', 'obj/', '.git/', '__pycache__/', 'node_modules/', '_protos/']
```

All patterns end with `/` to ensure they match directories only.

## ⚠️ Lessons Learned

When using `string.includes()` for path filtering:
1. **Always use directory delimiters** (`/` or `\\`) in patterns
2. **Test edge cases** where pattern might appear as substring in filenames
3. **Align patterns across implementations** (Python vs JavaScript)

## 🔍 How to verify the fix

After applying this change, rebuild the RAG:

```javascript
const rag = new RagBuilder(repoRoot);
await rag.build(console.log);
```

Expected output:
```
RAG: collecting files from repo…
RAG: ~1342 files found — segmenting…  ← Should match Python
RAG: building TF-IDF index from ~11600 unique chunks…
RAG ready — 1342 files · 11652 chunks · ~4000 dupes · 0 errors
```

The numbers should now match Python's output (±minor parsing differences).
