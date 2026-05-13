# TSCG Ontology Linter

Validates JSON-LD ontology files for syntax, semantics, and TSCG conventions.

## Features

✅ **7 validation checks:**
1. JSON syntax
2. JSON-LD structure (@context, @graph, @base)
3. RDF parsing
4. OWL semantics (classes, properties, domain/range)
5. TSCG conventions (naming, terminology)
6. Import resolution
7. Namespace consistency

✅ **TSCG-specific checks:**
- Legacy "tensor" terminology detection
- Ambiguous "I" in formulas (should be It/Im)
- @base suffix validation
- M0/M1/M2/M3 naming conventions

## Installation

```bash
pip install rdflib --break-system-packages
```

## Usage

### Single file
```bash
python ontology_linter.py M2_GenericConcepts.jsonld
```

### Directory (all .jsonld files)
```bash
python ontology_linter.py ontology/
```

### Filter by layer
```bash
# M2 only
python ontology_linter.py ontology/ --layer M2

# M3 only
python ontology_linter.py ontology/ --layer M3

# M1 only
python ontology_linter.py ontology/ --layer M1

# M0 only
python ontology_linter.py ontology/ --layer M0
```

### Dry-run (preview without execution)
```bash
# See what files would be checked
python ontology_linter.py ontology/ --dry-run

# Dry-run with layer filter
python ontology_linter.py ontology/ --layer M2 --dry-run
```

### Strict mode (fail on warnings)
```bash
python ontology_linter.py M2_GenericConcepts.jsonld --strict
```

### Output formats

#### Text (default)
```bash
python ontology_linter.py ontology/
```

#### JSON
```bash
python ontology_linter.py ontology/ --format json --output report.json
```

#### Markdown report
```bash
python ontology_linter.py ontology/ --format markdown --output lint_report.md
```

### Combined examples
```bash
# M2 layer with markdown report
python ontology_linter.py ontology/ --layer M2 --format markdown --output m2_report.md

# Strict validation on M3 with JSON output
python ontology_linter.py ontology/ --layer M3 --strict --format json --output m3_strict.json

# Dry-run to preview M1 files
python ontology_linter.py ontology/ --layer M1 --dry-run
```

## Output

### Example: Passed
```
======================================================================
Linting: M2_GenericConcepts.jsonld
======================================================================

[1/7] JSON Syntax...
[2/7] JSON-LD Structure...
[3/7] RDF Parsing...
[4/7] OWL Semantics...
[5/7] TSCG Conventions...
[6/7] Import Resolution...
[7/7] Namespace Consistency...

======================================================================
REPORT: M2_GenericConcepts.jsonld
======================================================================

✓ INFO:
   ✓ Valid JSON syntax
   ✓ @context present
   ✓ @base in @context (correct)
   ✓ @graph with 120 items
   ✓ Parsed as RDF: 850 triples
   ✓ OWL Classes: 108
   ✓ OWL Properties: 15
   ✓ Imports declared: 1
     ✓ M3_GenesisGrammar.jsonld
   ✓ Namespaces defined: 5

📊 STATISTICS:
   graph_items: 120
   triples: 850
   classes: 108
   properties: 15
   namespaces: 5

✅ PASSED
```

### Example: Warnings
```
⚠️  WARNINGS (3):
   • Found 26 occurrences of 'tensor' (should use 'monoidal product' or 'structural grammar')
   • Ambiguous 'I' in formula (use It or Im): D ⊗ I ⊗ F
   • Import not found: M3_GenesisSpace.jsonld

⚠️  PASSED WITH WARNINGS
```

### Example: Errors
```
❌ ERRORS (2):
   • Invalid JSON syntax: Expecting ',' delimiter: line 45 column 5
   • RDF parsing failed: Invalid @context

❌ FAILED
```

## Exit Codes

- `0` - All checks passed (or warnings in non-strict mode)
- `1` - Errors found (or warnings in strict mode)

## Checks Performed

### 1. JSON Syntax
- Valid JSON format
- Encoding (UTF-8)

### 2. JSON-LD Structure
- `@context` present
- `@base` placement (should be in @context, not root)
- `@graph` present
- Ontology metadata (owl:Ontology, versionInfo)

### 3. RDF Parsing
- Can be parsed as RDF graph
- Triple count

### 4. OWL Semantics
- Class and property counts
- Domain/range references valid
- No undefined terms (except standard namespaces)

### 5. TSCG Conventions
- Filename follows M0_/M1_/M2_/M3_ pattern
- No legacy "tensor" terminology
- No ambiguous "I" in formulas (M2)
- @base doesn't have /ontology/ suffix

### 6. Import Resolution
- owl:imports declared
- Import files exist locally

### 7. Namespace Consistency
- Namespace URIs end with # or /
- Namespace count

## Integration

### Pre-commit Hook
```bash
#!/bin/bash
python cli-tools/ontology-linter/ontology_linter.py ontology/ --strict
```

### CI/CD (GitHub Actions)
```yaml
- name: Lint Ontologies
  run: |
    pip install rdflib
    python cli-tools/ontology-linter/ontology_linter.py ontology/ --strict
```

## Development

Extend checks by adding methods to `OntologyLinter` class:
```python
def _check_custom_rule(self, data: Dict):
    # Your custom validation
    if condition:
        self.warnings.append("Custom warning message")
```

## License

Part of TSCG project.
