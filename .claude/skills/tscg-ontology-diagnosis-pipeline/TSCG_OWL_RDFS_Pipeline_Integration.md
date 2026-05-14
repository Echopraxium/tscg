# TSCG OWL/RDFS Pipeline Integration Guide

**Date:** 2026-05-14  
**Status:** Production-ready  
**Validation Results:** M2_GenericConcepts.jsonld passed all tests

---

## Overview

This document describes how to integrate the OWL/RDFS validation tools into the TSCG validation pipeline, specifically into Phase 3 (Technical Validation) of the `tscg-ontology-diagnosis-pipeline`.

### Tools to integrate

1. **`rdfs_diagnostic.py`** - RDFS validation & error reporting
2. **`fix_owl_literals.py`** - Automated corrections with dry-run
3. **`test_owl_reasoning.py`** - OWL complete reasoning (Pellet)

### Location

All tools are in: `cli-tools/owl_reasoning_test/`

---

## Integration Points

### 1. Updated Phase 3: Technical Validation

The existing Phase 3 of the ontology diagnosis pipeline should be expanded:

**BEFORE (old Phase 3):**
```
Phase 3: Technical Validation
├── Linter
├── Reasoner (planned)
├── SHACL Validator
└── Unit Tests
```

**AFTER (new Phase 3):**
```
Phase 3: Technical Validation
├── 3.1: Ontology Linter (syntax, structure, TSCG conventions)
├── 3.2: RDFS Diagnostic (OWL modeling errors)
├── 3.3: OWL Reasoning (logical consistency - only if 3.2 passes)
├── 3.4: SHACL Validation (schema compliance)
└── 3.5: Unit Tests (if applicable)
```

---

## Phase 3.2: RDFS Diagnostic

### Purpose

Detect OWL/RDFS modeling errors that prevent proper reasoning:
- Literal values instead of URI references
- Invalid property declarations
- Undefined class references

### Integration

```python
# In tscg-ontology-diagnosis-pipeline or main validation script

import subprocess
import sys

def run_rdfs_diagnostic(ontology_path):
    """Run RDFS diagnostic validation"""
    print("\n🔍 Phase 3.2: RDFS Diagnostic")
    print("-" * 70)
    
    result = subprocess.run(
        ["python", "cli-tools/owl_reasoning_test/rdfs_diagnostic.py"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.returncode != 0:
        print("❌ RDFS validation failed!")
        print("   Run fix script:")
        print(f"   python cli-tools/owl_reasoning_test/fix_owl_literals.py --dry-run")
        return False
    
    print("✅ RDFS validation passed")
    return True
```

### Exit codes

- `0` - No errors (may have warnings)
- `1` - Errors found (validation failed)

### When to run

**Always run before OWL reasoning** - this is a prerequisite check.

---

## Phase 3.3: OWL Reasoning

### Purpose

Validate logical consistency using Pellet reasoner:
- Check for inconsistent classes
- Verify OWL axioms
- Detect logical contradictions

### Integration

```python
def run_owl_reasoning(ontology_path):
    """Run OWL reasoning validation (Pellet)"""
    print("\n🔍 Phase 3.3: OWL Reasoning")
    print("-" * 70)
    
    result = subprocess.run(
        ["python", "cli-tools/owl_reasoning_test/test_owl_reasoning.py"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.returncode != 0:
        print("❌ OWL reasoning failed!")
        return False
    
    print("✅ OWL reasoning passed")
    return True
```

### Exit codes

- `0` - Ontology consistent
- `1` - Inconsistencies found or errors

### When to run

**Only after RDFS diagnostic passes** - OWL reasoners fail on modeling errors.

---

## Complete Phase 3 Workflow

### Sequential execution with gates

```python
def phase_3_technical_validation(ontology_path):
    """
    Phase 3: Technical Validation
    Sequential execution with failure gates
    """
    
    # Phase 3.1: Ontology Linter
    print("\n" + "=" * 70)
    print("PHASE 3: TECHNICAL VALIDATION")
    print("=" * 70)
    
    # 3.1: Linter
    if not run_linter(ontology_path):
        return False  # GATE: Stop if linter fails
    
    # 3.2: RDFS Diagnostic
    if not run_rdfs_diagnostic(ontology_path):
        print("\n⚠️  RDFS errors detected - fix before OWL reasoning")
        print("   Suggested workflow:")
        print("   1. python cli-tools/owl_reasoning_test/fix_owl_literals.py --dry-run")
        print("   2. Review changes")
        print("   3. python cli-tools/owl_reasoning_test/fix_owl_literals.py")
        print("   4. Re-run validation")
        return False  # GATE: Stop if RDFS fails
    
    # 3.3: OWL Reasoning (only if RDFS passed)
    if not run_owl_reasoning(ontology_path):
        return False  # GATE: Stop if reasoning fails
    
    # 3.4: SHACL Validation
    if not run_shacl_validation(ontology_path):
        return False
    
    # 3.5: Unit Tests (if applicable)
    if has_unit_tests(ontology_path):
        if not run_unit_tests(ontology_path):
            return False
    
    print("\n" + "=" * 70)
    print("✅ PHASE 3: TECHNICAL VALIDATION PASSED")
    print("=" * 70)
    return True
```

---

## Error Handling & User Guidance

### RDFS errors detected

When RDFS diagnostic fails:

```
❌ RDFS validation failed: 172 errors found

🔧 Suggested workflow:
   1. Preview fixes:
      python cli-tools/owl_reasoning_test/fix_owl_literals.py --dry-run
   
   2. If preview looks good, apply:
      python cli-tools/owl_reasoning_test/fix_owl_literals.py
   
   3. Re-run validation:
      python cli-tools/owl_reasoning_test/rdfs_diagnostic.py
   
   4. Expected: 0 errors

⚠️  Manual review recommended before applying automated fixes
```

### OWL reasoning failures

When OWL reasoning fails:

```
❌ OWL reasoning failed: Inconsistent classes found

🔍 Debug steps:
   1. Check Pellet output for specific errors
   2. Review "Reparenting" warnings (usually harmless)
   3. Look for circular dependencies or contradictory axioms
   4. Consult ontology_linter output for structural issues

📚 See: cli-tools/owl_reasoning_test/README.md
```

---

## Integration with Existing Pipeline Skill

### Update `tscg-ontology-diagnosis-pipeline-SKILL.md`

Add to **Phase 3** section:

```markdown
## Phase 3: Technical Validation

### 3.1: Ontology Linter
- Syntax validation
- Structure checks
- TSCG conventions

### 3.2: RDFS Diagnostic ⭐ NEW
- OWL modeling errors
- Literal → URI reference issues
- Property declaration validation
- **Tool:** `rdfs_diagnostic.py`
- **Exit gate:** Must pass before 3.3

### 3.3: OWL Reasoning ⭐ NEW
- Logical consistency (Pellet)
- Inconsistency detection
- Axiom validation
- **Tool:** `test_owl_reasoning.py`
- **Prerequisite:** 3.2 must pass

### 3.4: SHACL Validation
- Schema compliance
- Constraint checking

### 3.5: Unit Tests
- If applicable
```

---

## Prerequisites Check

### Before using OWL/RDFS tools

```python
def check_prerequisites():
    """Check if OWL/RDFS tools are ready"""
    
    # Check Java
    java_check = subprocess.run(["java", "-version"], 
                               capture_output=True)
    if java_check.returncode != 0:
        print("❌ Java not found - required for OWL reasoning")
        print("   See: TSCG_Prerequisites_Installation.md")
        return False
    
    # Check rdflib
    try:
        import rdflib
    except ImportError:
        print("❌ rdflib not installed")
        print("   Install: pip install rdflib")
        return False
    
    # Check owlready2
    try:
        import owlready2
    except ImportError:
        print("❌ owlready2 not installed")
        print("   Install: pip install owlready2")
        return False
    
    return True
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: TSCG Ontology Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Setup Java
      uses: actions/setup-java@v2
      with:
        distribution: 'temurin'
        java-version: '17'
    
    - name: Install dependencies
      run: |
        pip install rdflib owlready2
    
    - name: Run RDFS Diagnostic
      run: |
        python cli-tools/owl_reasoning_test/rdfs_diagnostic.py
    
    - name: Run OWL Reasoning
      run: |
        python cli-tools/owl_reasoning_test/test_owl_reasoning.py
      if: success()  # Only if RDFS passed
```

---

## Performance Considerations

### Execution times (M2_GenericConcepts.jsonld)

- **RDFS Diagnostic:** ~2 seconds
- **OWL Reasoning (Pellet):** ~1 second
- **Fix script:** ~0.5 seconds

**Total Phase 3.2 + 3.3:** ~3.5 seconds

### Optimization for large ontologies

For ontologies >500 classes:
- Consider parallel execution of independent checks
- Cache reasoning results if ontology unchanged
- Use incremental validation for minor edits

---

## Testing the Integration

### Validation test suite

```bash
# Test 1: Clean ontology (should pass all)
python cli-tools/owl_reasoning_test/rdfs_diagnostic.py
python cli-tools/owl_reasoning_test/test_owl_reasoning.py

# Test 2: Ontology with errors (should fail RDFS, suggest fixes)
# (Use M2 backup file from before fixes)
python cli-tools/owl_reasoning_test/rdfs_diagnostic.py \
  --file ontology/M2_GenericConcepts.backup_20260514_171657.jsonld

# Test 3: Dry-run fix script
python cli-tools/owl_reasoning_test/fix_owl_literals.py --dry-run

# Test 4: Apply fixes and re-validate
python cli-tools/owl_reasoning_test/fix_owl_literals.py
python cli-tools/owl_reasoning_test/rdfs_diagnostic.py
```

---

## Rollout Plan

### Phase 1: M2 (DONE ✅)

- ✅ RDFS diagnostic: 0 errors
- ✅ OWL reasoning: PASSED
- ✅ Backup created
- ✅ Documentation complete

### Phase 2: M1 Extensions (NEXT)

Apply same workflow to 15 M1 files:
1. Run RDFS diagnostic on each
2. Generate error reports
3. Apply fixes where needed
4. Validate with OWL reasoning

### Phase 3: M3 Layers

- M3_EagleEye.jsonld
- M3_SphinxEye.jsonld
- M3_GenesisGrammar.jsonld

### Phase 4: Pipeline Integration

- Update `tscg-ontology-diagnosis-pipeline` skill
- Add to main linter
- CI/CD integration

---

## Known Issues & Solutions

### Issue 1: "Reparenting" warnings in OWL reasoning

**Status:** Expected behavior, not an error

Pellet optimizes class hierarchies by removing redundant parent relationships.

**Example:**
```
* Owlready * Reparenting Layer: 
  {Segmentation, GenericConcept} => {Segmentation}
```

**Explanation:** If `Segmentation` is a subclass of `GenericConcept`, then `Layer` only needs `Segmentation` as parent.

**Action:** None required - this is correct inference.

---

### Issue 2: Temp files left behind

**Status:** Normal, cleaned up automatically

Files like `temp_ontology.rdf` are created temporarily and deleted after reasoning.

**If not deleted:** Safe to remove manually.

---

## Success Metrics

### M2_GenericConcepts.jsonld Results

**Before integration:**
- ❌ 172 RDFS errors
- ❌ 11 warnings
- ❌ OWL reasoning failed
- ❌ 150+ Pellet "Unsupported axiom" warnings

**After integration:**
- ✅ 0 RDFS errors
- ✅ 0 warnings  
- ✅ OWL reasoning: PASSED
- ✅ Pellet: 0.88 seconds, no errors
- ✅ Logically consistent ontology

**Time to fix:** ~45 minutes (with automated script)

---

## References

- **Tools README:** `cli-tools/owl_reasoning_test/README.md`
- **Prerequisites:** `TSCG_Prerequisites_Installation.md`
- **Pipeline Skill:** `tscg-ontology-diagnosis-pipeline-SKILL.md`
- **Backup file:** `ontology/M2_GenericConcepts.backup_20260514_171657.jsonld`

---

## Next Steps

1. ✅ **Document integration** (this file)
2. ⏳ **Update pipeline skill** with Phase 3.2 & 3.3
3. ⏳ **Apply to M1 extensions** (15 files)
4. ⏳ **CI/CD integration**
5. ⏳ **Team training** on new tools

---

**Maintainer:** Echopraxium with Claude AI collaboration  
**Last Updated:** 2026-05-14  
**Status:** Production-ready
