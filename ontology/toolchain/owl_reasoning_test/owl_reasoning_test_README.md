# OWL & RDFS Reasoning Tools

Validation and diagnostic tools for TSCG ontologies using OWL and RDFS reasoning.

## Overview

Two complementary tools for ontology validation:

1. **`rdfs_diagnostic.py`** - RDFS validation & error reporting (⭐ **Start here**)
2. **`owl_reasoning_test.py`** - OWL complete reasoning with Pellet (imports resolved locally)

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
python ontology/toolchain/owl_reasoning_test/rdfs_diagnostic.py
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
# From anywhere in the TSCG repository; --file is relative to the repository root
python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py --file ontology/M3_GenesisGrammar.jsonld
python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py --file ontology/M2_GenericConcepts.jsonld --isolated
python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py --file ontology/M1_CoreConcepts.jsonld --list-imports
```

### What it does (2.0.0, 2026-10-10)

1. Reads the file (JSON-LD) **and, transitively, its `owl:imports`** from the working
   copy: an import IRI under `https://raw.githubusercontent.com/Echopraxium/tscg/main/`
   is read from the matching local file. Everything is merged into one graph and the
   `owl:imports` triples are removed, so Owlready2 fetches nothing from the web.
   (Before 2.0.0, Owlready2 downloaded the imports as raw JSON-LD and failed with
   "NTriples parsing error … line 1": no file with imports could be reasoned.)
   An import that cannot be resolved locally is an **error**, never skipped.
   `--isolated` reasons on the file alone; `--list-imports` stops after resolution.
2. Converts the merged graph to RDF/XML in the system temp directory (Owlready2 requirement)
3. Runs Pellet (10–30 seconds)
4. Reports a **global inconsistency** or **unsatisfiable classes** as FAILED

### Expected output (if the ontology is clean)

```
Status    : ✅ PASSED — no inconsistency, no unsatisfiable class
```

### Exit codes

- `0` — consistent
- `1` — inconsistent (global inconsistency or unsatisfiable classes)
- `2` — input error (file not found, JSON-LD not parseable, import not resolvable)
- `3` — reasoner / environment error (Java, owlready2). Before 2.0.0 a global
  inconsistency was wrongly reported here, as "Java not installed".

### Tests

```bash
python -m pytest -q ontology/toolchain/owl_reasoning_test/tests
```

Import resolution always runs; the negative test (`fixtures/inconsistent.jsonld`, which
MUST fail) is skipped — never passed — when Java/Pellet cannot run.

---

## Recommended Workflow

### Phase 1: Diagnosis (RDFS)

```bash
# 1. Run RDFS diagnostic
python ontology/toolchain/owl_reasoning_test/rdfs_diagnostic.py > rdfs_report.txt

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
python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py --file ontology/M2_GenericConcepts.jsonld

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
subprocess.run(["python", "ontology/toolchain/owl_reasoning_test/rdfs_diagnostic.py"])

# Step 3.2: OWL Reasoning (only if RDFS passes)
if rdfs_passed:
    subprocess.run(["python", "ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py", "--file", "ontology/M2_GenericConcepts.jsonld"])
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
- **`owl_reasoning_test.py`** - OWL complete reasoning (Pellet), imports resolved locally
- **`tests/`** - pytest suite (import resolution, negative test on an inconsistent fixture)
- **`README.md`** - This file

---

**Status:** Active tools  
**Last updated:** 2026-05-14  
**Maintainer:** Echopraxium with Claude AI collaboration
