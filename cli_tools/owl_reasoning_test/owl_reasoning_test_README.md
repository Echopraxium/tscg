# OWL & RDFS Reasoning Tools

Validation and diagnostic tools for TSCG ontologies using OWL and RDFS reasoning.

## Overview

Two complementary tools for ontology validation:

1. **`rdfs_diagnostic.py`** - RDFS validation & error reporting (⭐ **Start here**)
2. **`test_owl_reasoning.py`** - OWL complete reasoning with Pellet

## Prerequisites

- Java JRE 17+ installed
- Python packages:
  ```bash
  pip install rdflib
  pip install owlready2
  ```

See `TSCG_Prerequisites_Installation.md` for full setup guide.

---

## Tool 1: RDFS Diagnostic (Recommended First)

**Purpose:** Detect and report OWL/RDFS modeling errors before attempting full OWL reasoning.

### Why use this first?

- ✅ More **tolerant** than OWL reasoners (won't crash on errors)
- ✅ Generates **actionable error reports** with fix suggestions
- ✅ Groups errors by type with concrete examples
- ✅ Provides **roadmap for corrections** (Option 2)

### Usage

```bash
# From anywhere in TSCG repository
python cli-tools/owl_reasoning_test/rdfs_diagnostic.py
```

### What it checks

1. **Domain/Range validation** - Detects literal values instead of URI references
2. **SubClassOf relations** - Checks class hierarchy consistency
3. **Functional properties** - Validates property declarations
4. **Inverse properties** - Checks owl:inverseOf correctness
5. **Undefined classes** - Finds referenced but undefined classes

### Output

```
❌ ERRORS (150 total):
  SUBCLASS_LITERAL: 108 occurrences
    • Class: .../Role
      Parent literal: m2:GenericConcept
      Fix: Change subClassOf from literal to URI reference

🔧 ACTIONABLE RECOMMENDATIONS:
  1. Fix 108 rdfs:subClassOf with literal values
     Pattern to replace:
     "rdfs:subClassOf": "m2:GenericConcept"
     →
     "rdfs:subClassOf": {"@id": "m2:GenericConcept"}
```

### Exit codes

- `0` - No errors (warnings OK)
- `1` - Errors found (needs fixing)

---

## Tool 2: OWL Reasoning (After Fixes)

**Purpose:** Complete OWL reasoning validation with Pellet reasoner.

### When to use

Only after **RDFS diagnostic passes** with 0 errors. This tool is strict and will fail with modeling errors.

### Usage

```bash
# From anywhere in TSCG repository
python cli-tools/owl_reasoning_test/test_owl_reasoning.py
```

### What it does

1. Loads `ontology/M2_GenericConcepts.jsonld`
2. Converts JSON-LD → RDF/XML (Owlready2 requirement)
3. Runs Pellet reasoner (10-30 seconds)
4. Checks for **logical inconsistencies**
5. Reports inconsistent classes (if any)

### Expected output (if ontology is clean)

```
✅ NO INCONSISTENCIES FOUND
   Ontology is logically consistent!

Status: ✅ PASSED
```

### Exit codes

- `0` - Ontology consistent
- `1` - Inconsistencies found or errors

---

## Recommended Workflow

### Phase 1: Diagnosis (RDFS)

```bash
# 1. Run RDFS diagnostic
python cli-tools/owl_reasoning_test/rdfs_diagnostic.py > rdfs_report.txt

# 2. Review error report
# 3. Identify patterns (e.g., 108 subClassOf literals)
```

### Phase 2: Corrections

```bash
# 1. Create automated fix script based on report
# 2. Apply fixes incrementally (10-20 at a time)
# 3. Re-run RDFS diagnostic after each batch
# 4. Iterate until 0 errors
```

### Phase 3: OWL Validation

```bash
# Once RDFS passes with 0 errors:
python cli-tools/owl_reasoning_test/test_owl_reasoning.py

# If OWL reasoning passes → ✅ Ready for production
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'rdflib'"

```bash
pip install rdflib
```

### "Java not found" or "JAVA_HOME not set"

See `TSCG_Prerequisites_Installation.md` for Java setup.

### RDFS diagnostic shows 150+ errors

**This is normal for M2 in current state.** These are known modeling issues that need systematic correction. Use the generated report as a roadmap.

### OWL reasoning fails with "Unsupported axiom" warnings

This means RDFS validation hasn't passed yet. **Run RDFS diagnostic first** and fix reported errors before attempting OWL reasoning.

---

## Integration with Pipeline

Both tools can be integrated into the TSCG validation pipeline:

```python
# In tscg-ontology-diagnosis-pipeline (Phase 3: Technical Validation)

# Step 3.1: RDFS Validation
subprocess.run(["python", "cli-tools/owl_reasoning_test/rdfs_diagnostic.py"])

# Step 3.2: OWL Reasoning (only if RDFS passes)
if rdfs_passed:
    subprocess.run(["python", "cli-tools/owl_reasoning_test/test_owl_reasoning.py"])
```

---

## Next Steps

### Immediate

1. ✅ Run RDFS diagnostic on M2
2. 📋 Review error report
3. 🔧 Plan correction strategy

### Short-term

1. Create automated fix scripts
2. Apply corrections incrementally
3. Validate with RDFS after each batch

### Long-term

1. Integrate into CI/CD
2. Add SHACL validation (Phase 3.5)
3. Extend to M1/M3 validation

---

## Files in this directory

- **`rdfs_diagnostic.py`** - RDFS validation & error reporting
- **`test_owl_reasoning.py`** - OWL complete reasoning (Pellet)
- **`README.md`** - This file

---

**Status:** Active tools  
**Last updated:** 2026-05-14  
**Maintainer:** Echopraxium with Claude AI collaboration
