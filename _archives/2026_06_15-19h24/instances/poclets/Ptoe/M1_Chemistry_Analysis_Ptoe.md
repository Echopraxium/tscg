# M1_Chemistry.jsonld Analysis for Ptoe

**Current Version**: 1.0.0.p3 (2026-02-24)  
**Namespace**: `m1.ext:chemistry:` (NOT `m1:chemistry:`)  
**Date**: 2026-04-26

---

## ✅ Existing Concepts in M1_Chemistry.jsonld

### 1. **ChemicalReaction** (owl:Class)
- **Role**: Generic chemical transformation process
- **Subclasses**: Combustion, Oxidation, Reduction
- **Characterized by**: m2:Process, m2:Transformation, m2:Event
- **Properties**: reactants, products, energyBalance, catalyst, mechanism, rateConstant

### 2. **Combustion** (owl:Class, subclass of ChemicalReaction)
- **Role**: Fire Triangle poclet concept
- **Components**: Fuel, Oxidizer, ActivationEnergy
- **Characterized by**: m2:Process, m2:Dissipation, m2:Synergy, m2:Composition, m2:Trigger, m2:Threshold, m2:Feedback

### 3. **Oxidation** (owl:Class, subclass of ChemicalReaction)
- **Role**: Electron loss / oxygen gain
- **Characterized by**: m2:Process, m2:Transformation

### 4. **Reduction** (owl:Class, subclass of ChemicalReaction)
- **Role**: Electron gain / oxygen loss
- **Characterized by**: m2:Process, m2:Transformation

### 5. **ChemicalSpecies** (owl:Class)
- **Role**: Generic chemical entity (molecule, compound, element, ion)
- **Characterized by**: m2:Component
- **SubTypes (mentioned but not defined)**:
  - `m1:Element` ❌ (referenced but not defined as owl:Class)
  - `m1:Compound`
  - `m1:Ion`
  - `m1:Radical`
- **Properties**: molecularFormula, molecularMass, phase, structure

### 6. **Catalyst** (owl:Class, subclass of ChemicalSpecies)
- **Role**: Species increasing reaction rate
- **Characterized by**: m2:Catalysis, m2:Mediator

### 7. **ReactionMechanism** (owl:Class)
- **Role**: Step-by-step reaction sequence
- **Characterized by**: m2:Process, m2:Path

---

## ❌ Missing Concepts Required for Ptoe

Ptoe (Periodic Table) requires **8 chemistry concepts** that are currently **absent or incomplete** in M1_Chemistry.jsonld:

### 1. **Element** ⚠️
- **Status**: Mentioned in `ChemicalSpecies.subTypes` but NOT defined as `owl:Class`
- **Required for Ptoe**: YES (118 elements are the core components)
- **Recommendation**: Define as `owl:Class` with properties (atomicNumber, symbol, electronConfiguration, etc.)

### 2. **ElectronConfiguration** ❌
- **Status**: NOT present
- **Required for Ptoe**: YES (electron configuration is the "genotype" determining chemical properties)
- **Recommendation**: Define as `owl:Class` with properties (notation, quantumNumbers, shell occupation)

### 3. **NobleGas** ❌
- **Status**: NOT present
- **Required for Ptoe**: YES (noble gases are stability attractors in the periodic table)
- **Recommendation**: Define as `owl:Class` (subclass of Element) with properties (filledShellConfiguration)

### 4. **OrbitalBlock** (or Block) ❌
- **Status**: NOT present
- **Required for Ptoe**: YES (s, p, d, f blocks define modularity of periodic structure)
- **Recommendation**: Define as `owl:Class` with properties (blockType: s/p/d/f, angularMomentum, capacity)

### 5. **ChemicalFamily** (or ElementFamily) ❌
- **Status**: NOT present
- **Required for Ptoe**: YES (alkali metals, halogens, transition metals... are network relationships)
- **Recommendation**: Define as `owl:Class` with properties (groupNumber, valenceElectrons, chemicalSimilarity)

### 6. **AtomicProperty** ❌
- **Status**: NOT present
- **Required for Ptoe**: YES (electronegativity, atomic radius, ionization energy are gradients)
- **Recommendation**: Define as `owl:Class` with properties (propertyType, value, unit, gradient)

### 7. **OxidationState** ⚠️
- **Status**: Mentioned in `Oxidation.properties` but NOT defined as `owl:Class`
- **Required for Ptoe**: YES (oxidation states encode valence information)
- **Recommendation**: Define as `owl:Class` with properties (charge, element, stateType: cation/anion/neutral)

### 8. **QuantumNumbers** ❌
- **Status**: NOT present
- **Required for Ptoe**: YES (n, l, m, s quantum numbers define configuration space)
- **Recommendation**: Define as `owl:Class` with properties (n: principal, l: angular, m: magnetic, s: spin)

---

## 🔧 Proposed Enrichment of M1_Chemistry.jsonld

### Strategy 1: Minimal Enrichment (Add 8 Missing Concepts)

Add the 8 missing concepts to `M1_Chemistry.jsonld` as new `owl:Class` entries following the existing pattern.

**Example structure** (for `Element`):

```json
{
  "@id": "m1.ext:chemistry:Element",
  "@type": "owl:Class",
  "rdfs:subClassOf": "m1.ext:chemistry:ChemicalSpecies",
  "rdfs:label": "Chemical Element",
  "skos:altLabel": ["Atom", "Elementary Substance"],
  "rdfs:comment": "Pure chemical substance consisting of atoms with the same atomic number Z. Building block of the Periodic Table.",
  "m1.ext:chemistry:properties": {
    "m1.ext:chemistry:atomicNumber": {
      "type": "xsd:integer",
      "range": "[1, 118]",
      "role": "Number of protons (unique identifier)"
    },
    "m1.ext:chemistry:symbol": {
      "type": "xsd:string",
      "format": "1-2 letters",
      "role": "Chemical symbol (e.g., H, He, Li, Be...)"
    },
    "m1.ext:chemistry:electronConfiguration": {
      "type": "m1.ext:chemistry:ElectronConfiguration",
      "role": "Distribution of electrons across orbitals"
    },
    "m1.ext:chemistry:atomicMass": {
      "type": "xsd:float",
      "unit": "u (atomic mass units)",
      "role": "Average mass of isotopes"
    },
    "m1.ext:chemistry:group": {
      "type": "xsd:integer",
      "range": "[1, 18]",
      "role": "Periodic table column (valence configuration)"
    },
    "m1.ext:chemistry:period": {
      "type": "xsd:integer",
      "range": "[1, 7]",
      "role": "Periodic table row (electron shell)"
    },
    "m1.ext:chemistry:block": {
      "type": "m1.ext:chemistry:OrbitalBlock",
      "enum": ["s", "p", "d", "f"],
      "role": "Orbital angular momentum classification"
    }
  },
  "m1.ext:chemistry:examples": [
    {"Z": 1, "symbol": "H", "name": "Hydrogen", "config": "1s¹"},
    {"Z": 6, "symbol": "C", "name": "Carbon", "config": "[He] 2s² 2p²"},
    {"Z": 26, "symbol": "Fe", "name": "Iron", "config": "[Ar] 3d⁶ 4s²"},
    {"Z": 79, "symbol": "Au", "name": "Gold", "config": "[Xe] 4f¹⁴ 5d¹⁰ 6s¹"}
  ],
  "m2:characterizedBy": [
    {"@id": "m2:Component"},
    {"@id": "m2:Identity"},
    {"@id": "m2:Node"}
  ]
}
```

**Estimated Addition**: ~500-600 lines JSON (8 concepts × ~70 lines each)

---

### Strategy 2: Reference-Only (Don't Enrich M1_Chemistry, Define in M0_Ptoe)

Alternative: Define Ptoe-specific concepts **inline** in `M0_Ptoe.jsonld` without modifying `M1_Chemistry.jsonld`.

**Pros**: No need to modify shared M1 extension  
**Cons**: Concepts not reusable for future chemistry poclets (less clean architecturally)

---

## ⚠️ Critical Namespace Issue in M0_Ptoe.jsonld

**Problem**: I generated `M0_Ptoe.jsonld` using namespace `m1:chemistry:` but the actual namespace in `M1_Chemistry.jsonld` is **`m1.ext:chemistry:`**.

**Impact**: All references like `"m1:instanceOf": "m1:chemistry:Element"` are **WRONG** and will fail SHACL validation or runtime resolution.

**Required Fix**: Update `M0_Ptoe.jsonld` to use `m1.ext:chemistry:` namespace throughout.

**Examples of corrections needed**:

```json
// WRONG (current in M0_Ptoe.jsonld)
"m1:chemistry": "M1_extensions/chemistry/M1_Chemistry.jsonld#"
"m1:instanceOf": "m1:chemistry:Element"

// CORRECT
"m1.ext:chemistry": "M1_extensions/chemistry/M1_Chemistry.jsonld#"
"m1:instanceOf": "m1.ext:chemistry:Element"
```

---

## 🎯 Recommended Action Plan

### Option A: Enrich M1_Chemistry.jsonld First (Preferred)

1. ✅ **Enrich M1_Chemistry.jsonld** with 8 missing concepts (I can generate this)
2. ✅ **Update M0_Ptoe.jsonld** with corrected namespace `m1.ext:chemistry:`
3. ✅ **Validate with SHACL**
4. ✅ **Proceed to Step 4 (Simulation)**

**Pros**: Clean architecture, concepts reusable for future chemistry poclets  
**Cons**: Requires modifying shared M1 extension (but this is intended purpose of M1!)

---

### Option B: Inline Definitions in M0_Ptoe (Workaround)

1. ✅ **Define 8 concepts inline** in `M0_Ptoe.jsonld` without namespace (local definitions)
2. ✅ **Validate with SHACL**
3. ✅ **Proceed to Step 4 (Simulation)**
4. ⏸ **Later**: Extract concepts to M1_Chemistry.jsonld for reusability

**Pros**: Faster, no shared file modification  
**Cons**: Less clean, concepts not reusable, violates M1 extension design pattern

---

## 💡 My Recommendation

**Go with Option A** — Enriching M1_Chemistry.jsonld is the architecturally correct approach. The 8 missing concepts are **genuinely reusable** chemistry concepts, not Ptoe-specific. Future poclets (e.g., "AtomicSpectrum", "ChemicalBonding", "CrystalLattice") would also need these concepts.

**Next Steps**:

1. ⏸ **Michel decides**: Option A (enrich M1) or Option B (inline)?
2. ✅ **I generate**:
   - `M1_Chemistry_v1.1.0.jsonld` (with 8 new concepts) — if Option A
   - `M0_Ptoe_v1.0.1.jsonld` (corrected namespace + inline definitions) — if Option B
3. ✅ **Validation SHACL**
4. ✅ **Step 4 (Simulation)**

**Your call, Michel!** 🎯
