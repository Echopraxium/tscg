# Namespace Collision Fix - Cell Signaling Modes

**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-01-22  
**Issue**: Namespace collision in M0_CellSignalingModes.jsonld

---

## Problem Identified

The original `M0_CellSignalingModes.jsonld` file had a **namespace collision** where the prefix `m1` was defined twice:

```json
"@context": {
  "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
  "m1": "https://github.com/Echopraxium/tscg/blob/main/ontology/M1_extensions/biology/M1_Biology.jsonld#",
  ...
}
```

This is invalid JSON-LD because:
1. **Duplicate keys** are not allowed in JSON objects
2. The second definition **overwrites** the first
3. References to `m1:` concepts become **ambiguous**

---

## Solution Implemented

### 1. Separate Namespace Prefixes

Created distinct prefixes for each ontology layer:

```json
"@context": {
  "m0": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/cell_signaling/M0_CellSignalingModes.jsonld#",
  "m1core": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
  "m1bio": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld#",
  "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#",
  ...
}
```

**Rationale**:
- `m1core`: Generic transdisciplinary concepts (oscillators, filters, switches, etc.)
- `m1bio`: Biology-specific concepts (hormones, receptors, cells, tissues, etc.)
- Clear semantic distinction between layers

### 2. Created M1_Biology.jsonld Extension

A new biology domain extension was created at:
`/ontology/M1_extensions/biology/M1_Biology.jsonld`

**Contents**:
- **Cellular Communication Patterns**: Autocrine, Paracrine, Neuroendocrine, Endocrine
- **Biological Structures**: Cell, Tissue, Organ, Receptor, Hormone
- **Physiological Processes**: Signal Transduction, Homeostasis, Metabolism
- **Regulatory Mechanisms**: Feedback Loops, Diffusion Gradients, Morphogens
- **Systems**: Hypothalamus-Pituitary Axis, Blood Circulation, Immune Response

Each concept includes:
- `rdfs:label` and `rdfs:comment` (documentation)
- `m1bio:m2Basis` (linkage to M2 metaconcepts)
- `m1bio:examples` (concrete instances)
- Domain-specific properties (spatial/temporal ranges, mechanisms)

### 3. Updated M0_CellSignalingModes.jsonld

The corrected poclet file now:
- Uses `m1core:` for core transdisciplinary concepts
- Uses `m1bio:` for biology-specific concepts
- Uses `m2:` for metaconcepts
- Uses `m0:` for poclet-specific definitions

---

## Usage Guidelines

### When to use each namespace:

#### `m1core:` (M1_CoreConcepts.jsonld)
Use for **generic transdisciplinary patterns**:
- `m1core:Oscillator` - Any periodic behavior
- `m1core:Filter` - Any selective transmission
- `m1core:Switch` - Any state transition mechanism
- `m1core:Amplifier` - Any signal boosting
- `m1core:Channel` - Any transmission pathway

#### `m1bio:` (M1_Biology.jsonld)
Use for **biology-specific concepts**:
- `m1bio:AutocrineSignaling` - Specific signaling mode
- `m1bio:Hormone` - Biological signaling molecule
- `m1bio:Receptor` - Biological detection structure
- `m1bio:Cell` - Fundamental biological unit
- `m1bio:Homeostasis` - Biological regulation principle

#### `m2:` (M2_MetaConcepts.jsonld)
Use for **universal metaconcepts**:
- `m2:Component` - Elementary parts of any system
- `m2:Balance` - Equilibrium between factors
- `m2:Trade-off` - Exchange under constraints
- `m2:Signal` - Information carrier
- `m2:Feedback` - Output-to-input loop

---

## File Structure

```
ontology/
├── M1_CoreConcepts.jsonld              # Generic transdisciplinary concepts
├── M2_MetaConcepts.jsonld              # Universal metaconcepts
│
├── M1_extensions/
│   └── biology/
│       └── M1_Biology.jsonld           # ✅ NEW: Biology-specific concepts
│
└── poclets/
    └── cell_signaling/
        └── M0_CellSignalingModes.jsonld  # ✅ CORRECTED: Uses m1core + m1bio
```

---

## Namespace Resolution Rules

### Priority Order:
1. **m0:** - Poclet-specific instances (highest priority, most specific)
2. **m1bio:** - Domain-specific concepts (biology layer)
3. **m1core:** - Generic transdisciplinary concepts (core patterns)
4. **m2:** - Universal metaconcepts (foundation layer)

### Example Resolution:

```json
{
  "@id": "m0:AutocrineSignaling",
  "@type": "m1bio:AutocrineSignaling",     // Biology-specific class
  "m0:metaconceptInstantiation": "m2:Component",  // Universal metaconcept
  "m0:patternBasis": "m1core:FeedbackLoop"  // Generic pattern
}
```

**Interpretation**:
- This is an **instance** (`m0:`) of Autocrine Signaling
- It is a **biology-specific type** (`m1bio:`)
- It instantiates a **universal metaconcept** (`m2:Component`)
- It uses a **generic pattern** (`m1core:FeedbackLoop`)

---

## Benefits of This Approach

1. **No Collision**: Each namespace has unique prefix
2. **Clear Semantics**: Domain specificity is explicit
3. **Modularity**: Biology extension can be updated independently
4. **Reusability**: Other domains (chemistry, optics) can create similar extensions
5. **Scalability**: Framework can grow without namespace conflicts

---

## Standard URI Patterns

All TSCG ontologies follow this URI structure:

```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
├── M2_MetaConcepts.jsonld                 → m2:
├── M1_CoreConcepts.jsonld                 → m1core:
├── M1_extensions/
│   ├── biology/M1_Biology.jsonld          → m1bio:
│   ├── chemistry/M1_Chemistry.jsonld      → m1chem:
│   ├── optics/M1_Optics.jsonld            → m1opt:
│   └── photography/M1_Photography.jsonld  → m1photo:
└── poclets/
    └── {domain}/M0_{PocletName}.jsonld    → m0:
```

---

## Files Delivered

1. **M1_Biology.jsonld** - New biology domain extension
   - URI: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld`
   - Prefix: `m1bio:`
   - Version: 1.0.0

2. **M0_CellSignalingModes.jsonld** - Corrected poclet
   - URI: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/cell_signaling/M0_CellSignalingModes.jsonld`
   - Uses: `m0:`, `m1core:`, `m1bio:`, `m2:`
   - Version: 1.0.0

---

## Validation Checklist

✅ No duplicate keys in `@context`  
✅ All namespace prefixes are unique  
✅ URIs use `raw.githubusercontent.com` (not `github.com/blob`)  
✅ M1_Biology.jsonld imports M1_CoreConcepts.jsonld and M2_MetaConcepts.jsonld  
✅ All biological concepts have `m1bio:` prefix  
✅ Generic concepts use `m1core:` prefix  
✅ Metaconcepts use `m2:` prefix  
✅ Poclet instances use `m0:` prefix  

---

## Next Steps

1. **Validate** M1_Biology.jsonld with JSON-LD validator
2. **Upload** to GitHub repository at correct path
3. **Update** other biological poclets to use `m1bio:` prefix
4. **Create** similar extensions for other domains:
   - `M1_Chemistry.jsonld` → `m1chem:`
   - `M1_Thermodynamics.jsonld` → `m1thermo:`
   - `M1_Ecology.jsonld` → `m1eco:`

---

**Issue**: Resolved ✅  
**Impact**: High - Enables proper separation of generic vs domain-specific concepts  
**Compatibility**: Requires update of any code/tools referencing old `m1:` prefix in biological contexts
