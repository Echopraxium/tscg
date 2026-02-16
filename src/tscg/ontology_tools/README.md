# 🔄 TSCG JSON-LD to OWL Turtle Converter

**Version**: 1.0.0  
**Date**: 2026-02-15  
**Author**: Echopraxium with the collaboration of Claude AI

---

## 📋 Overview

This tool converts all TSCG JSON-LD ontology files (`.jsonld`) to OWL Turtle format (`.ttl`) for use with:
- **Protégé** ontology editor
- **OWL reasoners** (Pellet, HermiT, ELK, etc.)
- **SPARQL** query engines
- **Semantic web** applications

### Why Turtle?

| Feature | JSON-LD | Turtle |
|---------|---------|--------|
| **Protégé support** | Limited | ⭐⭐⭐⭐⭐ Native |
| **Reasoner compatibility** | Requires parsing | ⭐⭐⭐⭐⭐ Direct |
| **Human readability** | Good | ⭐⭐⭐⭐⭐ Excellent |
| **RDF/OWL standard** | Yes | Yes (de facto) |

---

## 🚀 Quick Start

### Repository Structure

Your TSCG project should have this structure:

```
tscg/                         ← GitHub repository root
├── ontology/                 ← TSCG ontologies (M3, M2, M1)
│   ├── M3_EagleEye.jsonld
│   ├── M3_SphinxEye.jsonld
│   ├── M2_MetaConcepts.jsonld
│   └── M1_extensions/
├── system-models/            ← System models (M0 poclets)
│   ├── poclets/
│   └── validation/
└── src/                      
    └── tscg/
        └── ontology_tools/   ← PLACE FILES HERE
            ├── jsonld_to_turtle.py
            ├── requirements.txt
            └── ...
```

### 1. Installation

```bash
# Navigate to the ontology_tools directory
cd src/tscg/ontology_tools

# Install dependencies
pip install -r requirements.txt
```

**Note:** The script automatically detects the TSCG root by searching for `ontology/` and `system-models/` directories, climbing up from `src/tscg/ontology_tools/` → `src/tscg/` → `src/` → `root/`.

### 2. Basic Usage

```bash
# Convert all .jsonld files in ontology/ and system-models/
python jsonld_to_turtle.py

# Preview what would be converted (dry-run)
python jsonld_to_turtle.py --dry-run

# Continue on errors instead of stopping
python jsonld_to_turtle.py --skip-errors
```

### 3. Windows Batch Script

```cmd
REM Double-click to run conversion
_convert_to_turtle.bat
```

---

## 📂 What Gets Converted

The tool recursively scans these directories and all subdirectories:

```
tscg/
├── ontology/
│   ├── M3_EagleEye.jsonld        → M3_EagleEye.ttl
│   ├── M3_SphinxEye.jsonld       → M3_SphinxEye.ttl
│   ├── M3_GenesisSpace.jsonld    → M3_GenesisSpace.ttl
│   ├── M2_MetaConcepts.jsonld    → M2_MetaConcepts.ttl
│   ├── M1_CoreConcepts.jsonld    → M1_CoreConcepts.ttl
│   └── M1_extensions/
│       ├── biology/M1_Biology.jsonld       → M1_Biology.ttl
│       ├── chemistry/M1_Chemistry.jsonld   → M1_Chemistry.ttl
│       ├── mythology/M1_Mythology.jsonld   → M1_Mythology.ttl
│       ├── optics/M1_Optics.jsonld         → M1_Optics.ttl
│       └── photography/M1_Photography.jsonld → M1_Photography.ttl
│
└── system-models/
    ├── poclets/
    │   ├── M0_FireTriangle.jsonld          → M0_FireTriangle.ttl
    │   ├── M0_RAAS.jsonld                  → M0_RAAS.ttl
    │   └── [all other poclets...]
    │
    └── validation/
        └── [validation models...]
```

---

## 🛠️ Advanced Usage

### Command-Line Options

```bash
# Full syntax
python jsonld_to_turtle.py [OPTIONS]

Options:
  --root-dir PATH       Root directory of TSCG project (default: auto-detect)
  --output-dir PATH     Output directory (default: same as input)
  --dry-run            Show what would be converted without converting
  --skip-errors        Continue on errors instead of stopping
  --verbose            Enable detailed logging
  -h, --help           Show help message
```

### Examples

#### Example 1: Preview Conversion

```bash
python jsonld_to_turtle.py --dry-run --verbose
```

**Output:**
```
[DRY-RUN] Would convert: M3_EagleEye.jsonld → M3_EagleEye.ttl
[DRY-RUN] Would convert: M2_MetaConcepts.jsonld → M2_MetaConcepts.ttl
...
```

#### Example 2: Separate Output Directory

```bash
python jsonld_to_turtle.py --output-dir ../turtle-ontologies
```

Creates:
```
turtle-ontologies/
├── ontology/
│   ├── M3_EagleEye.ttl
│   ├── M2_MetaConcepts.ttl
│   └── ...
└── system-models/
    └── ...
```

#### Example 3: Robust Batch Conversion

```bash
python jsonld_to_turtle.py --skip-errors --verbose > conversion.log 2>&1
```

---

## 📊 Conversion Report

The tool generates a detailed report:

```
======================================================================
TSCG JSON-LD to OWL Turtle Converter v1.0.0
======================================================================
Root directory: /path/to/tscg
Target directories: ontology, system-models

Scanning for .jsonld files...
Found 58 .jsonld files

Starting conversion...
----------------------------------------------------------------------
[1/58] Processing...
Converting: ontology/M3_EagleEye.jsonld
  ✓ Created: ontology/M3_EagleEye.ttl

[2/58] Processing...
Converting: ontology/M2_MetaConcepts.jsonld
  ✓ Created: ontology/M2_MetaConcepts.ttl

...

======================================================================
CONVERSION SUMMARY
======================================================================
Files found:     58
Files converted: 58
Files failed:    0
Files skipped:   0
======================================================================
✓ All files converted successfully!
```

---

## 🔍 Verifying Conversion

### Method 1: Protégé

1. Open Protégé
2. File → Open...
3. Select any `.ttl` file
4. Verify:
   - Classes hierarchy loads
   - Properties are visible
   - Annotations preserved

### Method 2: rdflib (Python)

```python
from rdflib import Graph

g = Graph()
g.parse("ontology/M2_MetaConcepts.ttl", format="turtle")
print(f"Loaded {len(g)} triples")

# Query example
for s, p, o in g.triples((None, None, None)):
    print(f"{s} -- {p} --> {o}")
    break  # Just show first triple
```

### Method 3: Apache Jena (Command Line)

```bash
# Validate Turtle syntax
riot --validate ontology/M2_MetaConcepts.ttl

# Query with SPARQL
sparql --data=ontology/M2_MetaConcepts.ttl --query=query.rq
```

---

## ⚠️ Troubleshooting

### Problem: "rdflib not found"

**Solution:**
```bash
pip install rdflib
```

### Problem: UTF-8 Encoding Errors

The tool handles UTF-8 automatically, but if you see errors:

1. Check that `.jsonld` files are **valid UTF-8**
2. Use `--skip-errors` to continue past problematic files
3. Check the log for specific files causing issues

### Problem: Invalid JSON-LD Syntax

**Solution:** The tool will report which files failed to parse. Fix these manually:

```bash
# Validate JSON-LD with online tool
https://json-ld.org/playground/

# Or use Python
python -m json.tool file.jsonld
```

### Problem: Missing Files

The tool expects this directory structure:
```
tscg/                         ← Repository root
├── ontology/                 ← Must exist
├── system-models/            ← Must exist  
└── src/tscg/ontology_tools/  ← You are here
```

**The script auto-detects the root** by searching for `ontology/` and `system-models/` directories up to 5 levels above the current location.

If running from a different location or non-standard structure:
```bash
python jsonld_to_turtle.py --root-dir /path/to/tscg
```

---

## 🔧 Integration with Protégé

### Step 1: Convert Files

```bash
python jsonld_to_turtle.py
```

### Step 2: Open in Protégé

1. Launch Protégé
2. **File → Open...**
3. Navigate to `ontology/M2_MetaConcepts.ttl`
4. Click **Open**

### Step 3: Enable Reasoner

1. **Reasoner → Pellet** (or HermiT, ELK)
2. **Reasoner → Start Reasoner**
3. Wait for classification
4. View inferred hierarchy: **Entities → Classes**

### Step 4: Verify Imports

If ontologies import each other:
- Protégé should auto-load imported ontologies
- Check **Active Ontology** tab to verify all imports loaded

---

## 📝 Logging

Each conversion creates a timestamped log file:

```
tscg/
└── conversion_20260215_143052.log
```

This contains:
- Detailed conversion progress
- Warnings and errors
- UTF-8 encoding issues
- File paths and statistics

---

## 🎯 Next Steps After Conversion

1. **Load in Protégé** to visualize ontology structure
2. **Run OWL reasoner** to detect:
   - Inconsistencies
   - Implicit subsumptions
   - Unsatisfiable classes
3. **Execute SPARQL queries** for analysis
4. **Validate** with SHACL shapes (if defined)

---

## 🐛 Known Limitations

1. **No validation of OWL DL compliance** (just format conversion)
2. **Large files** (>50MB) may be slow
3. **Circular imports** not handled specially (Protégé handles these)
4. **Custom JSON-LD contexts** may need manual review

---

## 📚 References

- **RDFLib Documentation**: https://rdflib.readthedocs.io/
- **OWL Turtle Syntax**: https://www.w3.org/TR/turtle/
- **Protégé Wiki**: https://protegewiki.stanford.edu/
- **TSCG Framework**: https://github.com/Echopraxium/tscg

---

## 📜 License

MIT License - Same as TSCG Framework

---

## 🤝 Contributing

Issues and improvements welcome! Submit to TSCG GitHub repository.

---

**Last Updated**: 2026-02-15  
**Compatibility**: Python 3.8+, rdflib 7.0+  
**TSCG Version**: 15.1.0
