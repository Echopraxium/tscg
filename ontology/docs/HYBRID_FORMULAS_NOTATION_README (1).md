# TSCG Notation Convention: Hybrid Formulas and REVOI Standard

**TSCG Framework - Encoding Standards**  
**Version:** 14.3.1  
**Date:** 2026-01-30  
**Author:** Echopraxium with the collaboration of Claude AI

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [The Encoding Problem](#the-encoding-problem)
3. [REVOI Standard (Without Circumflex)](#revoi-standard-without-circumflex)
4. [Hybrid Formulas: The I Ambiguity](#hybrid-formulas-the-i-ambiguity)
5. [Solution: Im and It Notation](#solution-im-and-it-notation)
6. [Implementation Examples](#implementation-examples)
7. [Complete Notation Reference](#complete-notation-reference)
8. [Migration Guide](#migration-guide)

---

## 🎯 Overview

This document establishes the **official notation convention** for TSCG framework formulas, particularly addressing:

1. The replacement of **REVOÎ** (with circumflex accent) by **REVOI** (without accent)
2. The disambiguation of **I** (Information) in hybrid formulas through **Im** and **It** subscripts

These conventions ensure:
- **Encoding stability** across all JSON-LD files
- **Mathematical clarity** in bicephalous (dual-perspective) formulas
- **Consistency** throughout the TSCG framework

---

## ⚠️ The Encoding Problem

### Root Cause

The **Î** character (I with circumflex, Unicode U+00CE) causes **encoding conflicts** when mixed with mathematical symbols in the same JSON-LD file:

- **Î** = U+00CE (Latin Extended, low range)
- **⊗** = U+2297 (Mathematical Operators, high range)
- **δ** = U+03B4 (Greek, middle range)

### Observed Corruption

When these characters coexist in JSON files, serialization/deserialization operations cause corruption:

```
INTENDED:  "basis": "REVOÎ"
CORRUPTED: "basis": "REVOÃŽ"

INTENDED:  "formula": "A⊗S⊗F"
CORRUPTED: "formula": "AâŠ—SâŠ—F"
```

### Impact on Framework

- JSON validation failures
- Data loss during file operations
- Inconsistent rendering across tools
- Maintenance complexity

---

## ✅ REVOI Standard (Without Circumflex)

### Decision

**Replace all instances of REVOÎ with REVOI throughout the TSCG framework.**

### Rationale

1. **Encoding Stability**: Latin I (U+0049) is compatible with all mathematical symbols
2. **Simplicity**: No diacritical marks = no encoding edge cases
3. **Readability**: "REVOI" is equally readable and unambiguous
4. **Consistency**: Matches ASFID naming pattern (no accents)

### Scope

This change applies to:
- All JSON-LD ontology files (M2_MetaConcepts.jsonld, M3_*.jsonld, etc.)
- All documentation (README.md files)
- All theoretical formulations
- All code and scripts

### Before/After

```json
// BEFORE (deprecated)
{
  "basis": "REVOÎ",
  "formula": "R⊗Î⊗V"
}

// AFTER (official standard)
{
  "basis": "REVOI",
  "formula": "R⊗I⊗V"
}
```

---

## 🔀 Hybrid Formulas: The I Ambiguity

### The Problem

In **hybrid formulas** combining both ASFID (Territory) and REVOI (Map) dimensions, the letter **I** becomes ambiguous:

- **ASFID** contains **I** = Information (Territory measurement)
- **REVOI** contains **I** = Interoperability (Map quality)

When both appear in the same formula, **which I is which?**

### Example: Domain Metaconcept

The Domain metaconcept uses a **hybrid tensor product** ASFID⊗REVOI:

```
Domain = A⊗S⊗F⊗I⊗D⊗R⊗E⊗V⊗O⊗I
                  ↑               ↑
                  ?               ?
         Which I is this?   Which I is this?
```

This creates **semantic ambiguity** that must be resolved.

---

## ✅ Solution: Im and It Notation

### Convention

When **I** from both ASFID and REVOI appear in the same formula, use **subscript disambiguation**:

| Symbol | Meaning | Origin | Full Name |
|--------|---------|--------|-----------|
| **It** | Information (Territory) | ASFID | Information measured in physical systems |
| **Im** | Interoperability (Map) | REVOI | Interoperability of conceptual models |

### Mnemonic

- **It** = Information in **T**erritory (Eagle Eye perspective)
- **Im** = Interoperability in **M**ap (Sphinx Eye perspective)

### When to Use

**Use subscripts ONLY when both I's appear in the same formula.**

- ✅ **Hybrid formulas**: Use It and Im
- ❌ **Pure ASFID formulas**: Use plain I (no subscript needed)
- ❌ **Pure REVOI formulas**: Use plain I (no subscript needed)

---

## 📐 Implementation Examples

### Example 1: Domain Metaconcept (Hybrid)

**Full Tensor Product** (before reduction):

```
Domain = A⊗S⊗F⊗It⊗D⊗R⊗E⊗V⊗O⊗Im
         └─────ASFID─────┘ └────REVOI────┘
         (Territory)       (Map)
```

**Reduced via SVD to 5D**:

```
Domain ≈ σ₁|u₁⟩⊗|v₁⟩ + σ₂|u₂⟩⊗|v₂⟩ + σ₃|u₃⟩⊗|v₃⟩ + σ₄|u₄⟩⊗|v₄⟩ + σ₅|u₅⟩⊗|v₅⟩

Where:
  uᵢ ∈ ASFID space (contains It)
  vᵢ ∈ REVOI space (contains Im)
```

### Example 2: Pure Territory Formula (No Subscript)

**Process Metaconcept** (pure ASFID):

```
Process = D⊗I⊗F
            ↑
     Plain I (no ambiguity - only ASFID present)
```

### Example 3: Pure Map Formula (No Subscript)

**ValueSpace Metaconcept** (pure REVOI):

```
ValueSpace = O⊗R⊗I⊗V⊗E
                 ↑
          Plain I (no ambiguity - only REVOI present)
```

### Example 4: Hypothetical Hybrid Formula

If a future metaconcept combined ASFID's Information with REVOI's Interoperability:

```
HypotheticalMetaconcept = It⊗Im⊗D⊗R
                          ↑  ↑
                         Territory Map
                         (ASFID)  (REVOI)
```

---

## 📚 Complete Notation Reference

### M3 Basis Vectors

**Eagle Eye (Territory - ASFID)**:
- **A** = Attractor
- **S** = Structure
- **F** = Flow
- **It** = Information (use subscript in hybrid formulas)
- **D** = Dynamics

**Sphinx Eye (Map - REVOI)**:
- **R** = Representability
- **E** = Evolvability
- **V** = Verifiability
- **O** = Observability
- **Im** = Interoperability (use subscript in hybrid formulas)

### Tensor Product Notation

| Context | Notation | Example |
|---------|----------|---------|
| Unicode | ⊗ | A⊗S⊗F |
| LaTeX | \otimes | A \otimes S \otimes F |
| ASCII | (x) | A (x) S (x) F |

### Subscript Notation

| Context | It Notation | Im Notation |
|---------|-------------|-------------|
| Unicode | I_t or Iₜ | I_m or Iₘ |
| LaTeX | I_t | I_m |
| ASCII | I_t | I_m |
| JSON (plain) | It | Im |

**Recommendation for JSON-LD**: Use **It** and **Im** without subscript characters to avoid encoding issues.

---

## 🔄 Migration Guide

### Step 1: Replace REVOÎ with REVOI

**Files affected**:
- M2_MetaConcepts.jsonld
- M3_GenesisSpace.jsonld
- M3_SphinxEye.jsonld
- All M0 poclets using Sphinx Eye perspective
- All documentation

**Method**:
```python
import json

with open('file.jsonld', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all REVOÎ variants
content = content.replace('REVOÎ', 'REVOI')
content = content.replace('REVOÃŽ', 'REVOI')  # corrupted form
content = content.replace('REVOÃ', 'REVOI')   # another corrupted form

with open('file.jsonld', 'w', encoding='utf-8') as f:
    f.write(content)
```

### Step 2: Identify Hybrid Formulas

Search for formulas containing dimensions from **both** ASFID and REVOI:

```bash
grep -E "(A|S|F|I|D).*(R|E|V|O|I)" file.jsonld
```

### Step 3: Add Subscripts to Hybrid I's

For each hybrid formula identified:

1. Determine which I is from ASFID (Territory) → **It**
2. Determine which I is from REVOI (Map) → **Im**
3. Update the formula

**Example transformation**:

```json
// BEFORE
{
  "formula": "A⊗S⊗F⊗I⊗D⊗R⊗E⊗V⊗O⊗I"
}

// AFTER
{
  "formula": "A⊗S⊗F⊗It⊗D⊗R⊗E⊗V⊗O⊗Im",
  "notation": {
    "It": "Information (Territory/ASFID)",
    "Im": "Interoperability (Map/REVOI)"
  }
}
```

### Step 4: Update Documentation

Update all README files, theoretical documents, and papers to reflect:
- REVOI standard (no circumflex)
- It/Im convention for hybrid formulas

### Step 5: Validate

After migration:

```python
import json

# Check encoding
with open('file.jsonld', 'r') as f:
    content = f.read()
    
# Should find none of these
assert 'REVOÎ' not in content
assert 'REVOÃŽ' not in content
assert 'âŠ—' not in content

# Validate JSON
with open('file.jsonld', 'r') as f:
    data = json.load(f)  # Should not raise error
    
print("✅ Migration successful")
```

---

## 📋 Checklist for New Formulas

When creating a new metaconcept or formula:

- [ ] Does it use only ASFID dimensions? → Use plain **I**
- [ ] Does it use only REVOI dimensions? → Use plain **I**
- [ ] Does it combine ASFID + REVOI? → Use **It** and **Im**
- [ ] Have you documented which is which in the JSON?
- [ ] Have you tested JSON validation?
- [ ] Is the formula consistent with existing conventions?

---

## 🔍 Examples in M2 Metaconcepts

### Current Hybrid Metaconcept: Domain

```json
{
  "@id": "m2:Domain",
  "m2:hasTensorFormula": "A⊗S⊗F⊗It⊗D⊗R⊗E⊗V⊗O⊗Im",
  "m2:hasPolarity": "hybrid",
  "m2:perspective": "bicephalous_fusion",
  "m2:tensorType": "hybrid",
  "m2:notation": {
    "It": "Information measured in Territory (ASFID - Eagle Eye)",
    "Im": "Interoperability of Map models (REVOI - Sphinx Eye)"
  },
  "m2:5DReduction": {
    "description": "Reduced from 10D (5 ASFID + 5 REVOI) to 5D via SVD",
    "dominantModes": "First 2-3 modes capture 80%+ variance"
  }
}
```

### Pure Territory Metaconcept: Process

```json
{
  "@id": "m2:Process",
  "m2:hasTensorFormula": "D⊗I⊗F",
  "m2:hasPolarity": "dual",
  "m2:perspective": "dual",
  "m2:eagleView": {
    "basis": "ASFID",
    "formula": "D⊗I⊗F",
    "note": "I = Information (plain, no subscript - only ASFID present)"
  }
}
```

### Pure Map Metaconcept: ValueSpace

```json
{
  "@id": "m2:ValueSpace",
  "m2:hasTensorFormula": "O⊗R⊗I⊗V⊗E",
  "m2:hasPolarity": "neutral",
  "m2:perspective": "map",
  "m2:sphinxView": {
    "basis": "REVOI",
    "formula": "O⊗R⊗I⊗V⊗E",
    "note": "I = Interoperability (plain, no subscript - only REVOI present)"
  }
}
```

---

## 🎯 Summary

### Key Decisions

1. **REVOI Standard**: Replace all REVOÎ with REVOI (no circumflex accent)
2. **Hybrid Notation**: Use It (Territory) and Im (Map) when both I's appear together
3. **Pure Formulas**: Use plain I when only one basis (ASFID or REVOI) is present

### Benefits

- ✅ **Encoding stability**: No more UTF-8 corruption issues
- ✅ **Mathematical clarity**: No ambiguity about which I is meant
- ✅ **Framework consistency**: Uniform notation across all files
- ✅ **Future-proof**: Extensible to other potential conflicts

### When in Doubt

**Simple rule**: If you can see dimensions from **both** ASFID and REVOI in the same formula, use **It** and **Im**. Otherwise, use plain **I**.

---

## 📖 References

### TSCG Framework Documents

- `M2_MetaConcepts.jsonld` - Metaconcept ontology
- `M3_GenesisSpace.jsonld` - Bicephalous architecture
- `M3_EagleEye.jsonld` - ASFID basis (Territory)
- `M3_SphinxEye.jsonld` - REVOI basis (Map)
- `ENCODING_CORRESPONDANCES.txt` - Complete character mapping reference
- `TSCG_Map_Territory_Theoretical_Foundation.md` - Philosophical basis

### Related Decisions

- **v14.3.1**: REVOI standard adopted
- **v14.3.1**: It/Im notation convention established
- **v14.3.0**: Domain metaconcept introduced (first hybrid)

---

## 🏷️ Metadata

**Document ID:** TSCG-NOTATION-HYBRID-FORMULAS  
**Version:** 1.0.0  
**Status:** OFFICIAL STANDARD  
**Applies to:** TSCG Framework v14.3.1+  
**Created:** 2026-01-30  
**Author:** Echopraxium with the collaboration of Claude AI

---

**End of README**
