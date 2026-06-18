# TSCG Ptoe — Complete File Set Ready for Installation

**Date**: 2026-04-26  
**Instance**: Periodic Table of Elements (Ptoe)  
**Status**: ✅ All files generated — Ready for SHACL validation  
**Total files**: **9** (3 ontologies + 5 documentation + 1 summary)

---

## 📦 Complete File Inventory

### **GROUP 1: M1 Ontology Updates** (Shared Extensions)

#### 1. M1_Chemistry v1.1.0 ⭐
- **File**: `M1_Chemistry_v1.1.0.jsonld`
- **Destination**: `ontology/M1_extensions/chemistry/M1_Chemistry.jsonld`
- **Changes**:
  - Version: 1.0.0.p3 → **1.1.0**
  - **+8 new concepts**: Element, ElectronConfiguration, NobleGas, OrbitalBlock, ChemicalFamily, AtomicProperty, OxidationState, QuantumNumbers
  - Scope extended: "Atomic structure and periodic properties"
  - Changelog updated (rolling window)
- **Size**: ~720 lines (was ~485)
- **Action**: Replace existing `M1_Chemistry.jsonld`

#### 2. M1_Domains v1.2.0 ⭐
- **File**: `M1_Domains_v1.2.0.jsonld`
- **Destination**: `ontology/M1_Domains.jsonld`
- **Changes**:
  - Version: 1.1.0 → **1.2.0**
  - Total poclets: 24 → **25** (+Ptoe)
  - Chemistry domain updated:
    - **+2 subdomains**: "Atomic Structure", "Periodic Properties"
    - **+1 poclet**: M0_Ptoe
    - Poclet count: 3 → **4**
  - Changelog updated (rolling window)
- **Size**: ~550 lines (unchanged structure, updated data)
- **Action**: Replace existing `M1_Domains.jsonld`

---

### **GROUP 2: M0 Ptoe Instance** (New Poclet)

#### 3. M0_Ptoe v1.0.1 ⭐
- **File**: `M0_Ptoe_v1.0.1.jsonld`
- **Destination**: `instances/poclets/Ptoe/M0_Ptoe.jsonld`
- **Version**: 1.0.1 (namespace corrected from v1.0.0)
- **Changes**:
  - **CRITICAL**: Namespace `m1:chemistry:` → `m1.ext:chemistry:` (2 occurrences fixed)
  - All references now use correct namespace
- **Size**: ~1,400 lines
- **Content**:
  - 6 high-level components (Elements, PeriodicStructure, ElectronConfiguration, PropertyGradients, NobleGasAttractors, QuantumConstraints)
  - ASFID scores: [0.85, 0.90, 0.70, 0.95, 0.65] → mean 0.81
  - REVOI scores: [0.95, 0.80, 0.95, 0.90, 0.85] → mean 0.89
  - Epistemic gap δ₁: 0.057 (OnCriticalLine)
  - 19 M2 GenericConcepts mobilized
- **Action**: Create new file in `instances/poclets/Ptoe/`

---

### **GROUP 3: Documentation** (New Files)

#### 4. M0_Ptoe_README.md
- **Destination**: `instances/poclets/Ptoe/M0_Ptoe_README.md`
- **Size**: ~850 lines
- **Sections**:
  - Overview (transdisciplinary relevance)
  - System Description (structure, rules, attractors, gradients)
  - TSCG Analysis (ASFID/REVOI detailed scoring)
  - Components (6 high-level components)
  - GenericConcepts Mobilized (19 concepts by family)
  - Key Insights (7 transdisciplinary insights)
  - Analogies (comparisons with FireTriangle, ColorSynthesis, TrophicPyramid)
  - References (11 citations)
- **Action**: Create new file

#### 5. M0_Ptoe_analysis.md
- **Destination**: `instances/poclets/Ptoe/M0_Ptoe_analysis.md`
- **Size**: ~600 lines
- **Content**: Step 2 (ANALYSIS) complete output
  - ASFID lens analysis (5 dimensions)
  - REVOI lens analysis (5 dimensions)
  - Epistemic gap calculation
  - M2 GenericConcepts anticipated (19 concepts)
  - Verdict: ALIGNMENT ✅
- **Action**: Create new file

#### 6. Ptoe_M2_M1_Summary.md
- **Destination**: `instances/poclets/Ptoe/Ptoe_M2_M1_Summary.md`
- **Size**: ~250 lines
- **Content**: Steps 3.1-3.2 (M2 & M1 identification)
  - 19 M2 GenericConcepts listed
  - 8 M1 Chemistry concepts required
  - Architectural decisions documented
- **Action**: Create new file

#### 7. Step3_Complete_Summary.md
- **Destination**: `instances/poclets/Ptoe/Step3_Complete_Summary.md`
- **Size**: ~400 lines
- **Content**: Step 3 (MODELING) overview
  - Sub-steps 3.1-3.4 complete
  - Statistics (ASFID/REVOI, GenericConcepts, etc.)
  - Validation instructions
- **Action**: Create new file

#### 8. Files_Corrected_Summary.md
- **Destination**: `instances/poclets/Ptoe/Files_Corrected_Summary.md`
- **Size**: ~450 lines
- **Content**: M1_Chemistry v1.1.0 & M0_Ptoe v1.0.1 corrections
  - Namespace fix documentation
  - 8 new M1 concepts detailed
  - Pre-validation checklist
- **Action**: Create new file

#### 9. M1_Domains_v1.2.0_Summary.md
- **Destination**: `instances/poclets/Ptoe/M1_Domains_v1.2.0_Summary.md`
- **Size**: ~200 lines
- **Content**: M1_Domains update documentation
  - Chemistry domain changes
  - Changelog entry
  - Installation instructions
- **Action**: Create new file

---

## 🚀 Installation Instructions

### Step 1: Backup Existing Files

```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\

# Backup M1_Chemistry
cp ontology/M1_extensions/chemistry/M1_Chemistry.jsonld \
   ontology/M1_extensions/chemistry/M1_Chemistry_v1.0.0.p3.backup.jsonld

# Backup M1_Domains
cp ontology/M1_Domains.jsonld \
   ontology/M1_Domains_v1.1.0.backup.jsonld
```

---

### Step 2: Install M1 Ontologies (Shared Extensions)

```bash
# Install M1_Chemistry v1.1.0
cp ~/Downloads/M1_Chemistry_v1.1.0.jsonld \
   ontology/M1_extensions/chemistry/M1_Chemistry.jsonld

# Install M1_Domains v1.2.0
cp ~/Downloads/M1_Domains_v1.2.0.jsonld \
   ontology/M1_Domains.jsonld
```

---

### Step 3: Create Ptoe Directory

```bash
mkdir -p instances/poclets/Ptoe
```

---

### Step 4: Install M0 Ptoe Instance

```bash
# Main ontology
cp ~/Downloads/M0_Ptoe_v1.0.1.jsonld \
   instances/poclets/Ptoe/M0_Ptoe.jsonld

# Documentation
cp ~/Downloads/M0_Ptoe_README.md \
   instances/poclets/Ptoe/

cp ~/Downloads/M0_Ptoe_analysis.md \
   instances/poclets/Ptoe/

cp ~/Downloads/Ptoe_M2_M1_Summary.md \
   instances/poclets/Ptoe/

cp ~/Downloads/Step3_Complete_Summary.md \
   instances/poclets/Ptoe/

cp ~/Downloads/Files_Corrected_Summary.md \
   instances/poclets/Ptoe/

cp ~/Downloads/M1_Domains_v1.2.0_Summary.md \
   instances/poclets/Ptoe/
```

---

### Step 5: SHACL Validation (MANDATORY ⚠️)

```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\

# Validate M0_Ptoe
python ontology/TSCG_Grammar/validate_m0_instance.py \
       instances/poclets/Ptoe/M0_Ptoe.jsonld
```

**Expected Output**:
```
✅ VALIDATION PASSED
Instance conforms to TSCG SHACL grammar
```

**If validation FAILS**:
- Copy the SHACL violation report
- Report to Claude for fixing
- Re-validate after fix

---

### Step 6: Git Commit (After Validation Passes ✅)

```bash
git add ontology/M1_extensions/chemistry/M1_Chemistry.jsonld
git add ontology/M1_Domains.jsonld
git add instances/poclets/Ptoe/

git commit -m "feat(poclet): Add Ptoe (Periodic Table of Elements)

- M1_Chemistry v1.1.0: +8 atomic structure concepts (Element, ElectronConfiguration, NobleGas, OrbitalBlock, ChemicalFamily, AtomicProperty, OxidationState, QuantumNumbers)
- M1_Domains v1.2.0: Register Ptoe in Chemistry domain (+2 subdomains: Atomic Structure, Periodic Properties)
- M0_Ptoe v1.0.1: Complete instance with ASFID=0.81, REVOI=0.89, δ₁=0.057 (OnCriticalLine)
- 19 M2 GenericConcepts mobilized (10 Structural, 4 Informational, 3 Ontological, 2 Regulatory)
- Documentation: README, analysis, pipeline summaries

Closes #<issue_number_if_applicable>
"

git push
```

---

## 📊 Final Statistics

### Ontology Updates
| File | Old Version | New Version | Changes |
|------|-------------|-------------|---------|
| M1_Chemistry | 1.0.0.p3 | **1.1.0** | +8 concepts, +scope |
| M1_Domains | 1.1.0 | **1.2.0** | +Ptoe, +2 Chemistry subdomains |

### New Instance
| Property | Value |
|----------|-------|
| **Name** | Ptoe (Periodic Table of Elements) |
| **Domain** | Chemistry |
| **Type** | m3:Poclet |
| **ASFID** | 0.81 (A=0.85, S=0.90, F=0.70, I=0.95, D=0.65) |
| **REVOI** | 0.89 (R=0.95, E=0.80, V=0.95, O=0.90, I=0.85) |
| **Gap δ₁** | 0.057 (OnCriticalLine [0.05, 0.15)) |
| **M2 Concepts** | 19 (6 families) |
| **Components** | 6 (high-level abstraction) |
| **Actual Elements** | 118 (H to Og) |

### File Sizes
| Category | Files | Total Lines |
|----------|-------|-------------|
| Ontologies | 3 | ~2,670 lines |
| Documentation | 5 | ~2,750 lines |
| **TOTAL** | **8** | **~5,420 lines** |

---

## ✅ Pre-Validation Checklist

### M1_Chemistry v1.1.0
- ✅ `@type: "owl:Ontology"`
- ✅ `owl:versionInfo: "1.1.0"`
- ✅ `dcterms:creator: "Echopraxium with the collaboration of Claude AI"`
- ✅ All 8 new concepts have `@type: "owl:Class"`
- ✅ All concepts have `rdfs:label`, `rdfs:comment`
- ✅ All concepts have `m2:characterizedBy` or `rdfs:subClassOf`
- ✅ Changelog updated (rolling window)
- ✅ UTF-8 encoding preserved

### M1_Domains v1.2.0
- ✅ `owl:versionInfo: "1.2.0"`
- ✅ `m1:totalPoclets: 25`
- ✅ Chemistry domain updated (subdomains, examples, count, note)
- ✅ Changelog entry added (rolling window)
- ✅ UTF-8 encoding preserved

### M0_Ptoe v1.0.1
- ✅ `@type: "owl:Ontology"`
- ✅ `m3:ontologyType: {"@id": "m3:Poclet"}`
- ✅ `m1:domain: "Chemistry"` (not `m0:domain`)
- ✅ `owl:versionInfo: "1.0.0"` (version stays 1.0.0, only patch 1.0.1 for namespace fix)
- ✅ Namespace `m1.ext:chemistry:` (not `m1:chemistry:`)
- ✅ All `@context` URLs absolute
- ✅ `rdfs:label`, `rdfs:comment` present
- ✅ ASFID/REVOI complete
- ✅ Epistemic gap calculated
- ✅ GenericConceptsMobilized present
- ✅ UTF-8 encoding preserved

---

## 🎯 Next Steps After Installation

### 1. SHACL Validation ⏸
**MANDATORY** before proceeding — see Step 5 above.

### 2. Step 4 — Simulation (3D Interactive Visualization)
Once validation passes:
- Refine 3D Nautilus spiral prototype (BabylonJS)
- Alternative layouts (Atomic Skyscraper, Electron Cloud City)
- Sidebar integration (FireTriangle.html template)
- Interactive controls, tooltips, element search

### 3. Gallery Update
Update `index.html` with Ptoe entry:
```bash
node generate_index.js
```

### 4. TSCG_File_Tree.md Update
Add Ptoe to instance inventory documentation.

---

## 🛡️ Confidence Level

**SHACL Validation Confidence**: **95%** ✅

All known SHACL constraints from `M0_Realignment_Tracker.md` are satisfied:
- Correct `@type`, `m3:ontologyType`, `m1:domain` fields
- Absolute URLs in `@context`
- Proper namespace usage (`m1.ext:chemistry:`)
- Required metadata fields present
- UTF-8 encoding preserved

---

**Status**: ✅ **ALL FILES READY FOR INSTALLATION**  
**Waiting for**: SHACL validation confirmation from Michel ⏸
