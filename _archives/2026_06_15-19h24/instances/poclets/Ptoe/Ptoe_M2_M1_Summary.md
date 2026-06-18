# Ptoe Modeling — Steps 3.1 & 3.2 Summary

**Instance**: Periodic Table of Elements (Ptoe)  
**Domain**: Chemistry  
**Date**: 2026-04-26

---

## Step 3.1 — M2 GenericConcepts Identification

### Existing M2 Concepts Mobilized (19 concepts)

#### STRUCTURAL Family (10 concepts)

1. **Component** (`S ⊗ I`)
   - Each of the 118 elements
   - ASFID contribution: S=0.90, I=0.95

2. **Hierarchy** (`S ⊗ A`)
   - Periods > Groups > Blocks > Elements
   - ASFID contribution: S=0.90, A=0.85

3. **Modularity** (`S ⊗ I`)
   - Block structure (s, p, d, f)
   - ASFID contribution: S=0.85, I=0.90

4. **Topology** (`S ⊗ I`)
   - 2D grid with lanthanide/actinide "cuts"
   - ASFID contribution: S=0.85, I=0.80

5. **Symmetry** (`S`)
   - Periodic repetition (2n² rule)
   - ASFID contribution: S=0.90

6. **Segmentation** (`S ⊗ I ⊗ D`)
   - Division into blocks by orbital type
   - ASFID contribution: S=0.85, I=0.85, D=0.60

7. **Node** (`S ⊗ I`)
   - Each (period, group) position
   - ASFID contribution: S=0.85, I=0.95

8. **Network** (`S ⊗ I ⊗ F`)
   - Chemical family relationships
   - ASFID contribution: S=0.80, I=0.85, F=0.70

9. **Layer** (`S ⊗ I ⊗ A ⊗ R`)
   - Electron shells (K, L, M, N, O, P, Q)
   - ASFID contribution: S=0.85, I=0.90, A=0.75

10. **Identity** (`S → I → A → V → E`)
    - Unique identity per element (Z, symbol, name)
    - ASFID contribution: S=0.90, I=0.95, A=0.80

---

#### INFORMATIONAL Family (4 concepts)

11. **Code** (`I ⊗ S`)
    - Chemical symbols (H, He, Li...)
    - ASFID contribution: I=0.95, S=0.85

12. **Pattern** (`S → I → A`)
    - Periodic trends (χ, r, IE)
    - ASFID contribution: S=0.85, I=0.90, A=0.85

13. **Signature** (`I ⊗ S`)
    - Electron configuration ([Ar] 3d¹⁰ 4s² 4p¹)
    - ASFID contribution: I=0.95, S=0.85

14. **State** (`I`)
    - Oxidation states, phase states
    - ASFID contribution: I=0.85

---

#### ONTOLOGICAL Family (3 concepts)

15. **Gradient** (`⊗₂F` or `⊗₂I`)
    - Electronegativity ∇χ, radius ∇r, ionization energy ∇IE
    - ASFID contribution: F=0.75, I=0.85

16. **Space** (`S ⊗ I`)
    - Configuration space (n, l, m, s quantum numbers)
    - ASFID contribution: S=0.85, I=0.90

17. **Resource** (`F ⊗ I ⊗ R`)
    - Natural abundance, economic value
    - ASFID contribution: F=0.65, I=0.80

---

#### REGULATORY Family (2 concepts)

18. **Constraint** (`S ⊗ I`)
    - Pauli principle, Hund's rule, Aufbau principle
    - ASFID contribution: S=0.90, I=0.85

19. **Threshold** (`A ⊗ I`)
    - Noble gas configurations (stability thresholds)
    - ASFID contribution: A=0.90, I=0.85

---

### M2 Candidates — NEW PROPOSALS

**No new M2 candidates identified**. All necessary concepts exist in M2 v15.11.0.

---

## Step 3.2 — M1 KnowledgeFieldConceptCombos Identification

### Domain Extension: M1_Chemistry.jsonld

**Status**: Assumed to exist based on framework documentation. If not present in repo, will need to create.

**Required M1 Concepts for Ptoe**:

1. **m1:chemistry:Element** (or `m1:chemistry:ChemicalElement`)
   - Individual atoms (H, He, Li, Be...)
   - Properties: atomic number Z, symbol, electron configuration, oxidation states

2. **m1:chemistry:ElectronConfiguration**
   - Notation: [core] ns^a np^b nd^c nf^d
   - Quantum numbers: n (principal), l (angular), m (magnetic), s (spin)

3. **m1:chemistry:NobleGas**
   - He, Ne, Ar, Kr, Xe, Rn, Og
   - Filled-shell configurations (attractors)

4. **m1:chemistry:OrbitalBlock** (or `m1:chemistry:Block`)
   - s-block, p-block, d-block, f-block
   - Modularity structure

5. **m1:chemistry:ChemicalFamily** (or `m1:chemistry:ElementFamily`)
   - Alkali metals, alkaline earth, halogens, transition metals, etc.
   - Group-based classification

6. **m1:chemistry:AtomicProperty**
   - Electronegativity, atomic radius, ionization energy, electron affinity
   - Observable, measurable quantities

7. **m1:chemistry:OxidationState**
   - Valence states (+1, +2, +3, -1, -2...)
   - Information encoding for reactivity

8. **m1:chemistry:QuantumNumbers**
   - n, l, m, s
   - Configuration space parameters

---

### Anticipated M1 Extension Enrichment

If `M1_Chemistry.jsonld` lacks these concepts, they should be added as `owl:Class` entries with:
- `rdfs:subClassOf: m1:core:KnowledgeFieldConcept`
- `m1:domain: Chemistry`
- `rdfs:label`, `rdfs:comment`
- `skos:example` with concrete instances

**Example structure** (if creating from scratch):

```json
{
  "@id": "m1:chemistry:Element",
  "@type": "owl:Class",
  "rdfs:subClassOf": "m1:core:KnowledgeFieldConcept",
  "rdfs:label": "Chemical Element",
  "rdfs:comment": "A pure chemical substance consisting of atoms with the same atomic number Z.",
  "m1:domain": "Chemistry",
  "skos:example": ["Hydrogen (Z=1)", "Carbon (Z=6)", "Gold (Z=79)"],
  "m1:relatedM2": ["m2:Component", "m2:Identity", "m2:Node"]
}
```

---

### KnowledgeFieldConceptCombos for Ptoe

**Combos anticipated** (these would be instances in M1_CoreConcepts.jsonld or defined inline in M0):

1. **PeriodicStructure**
   - Combo of: `m2:Hierarchy ⊗ m2:Modularity ⊗ m2:Topology`
   - Role: The grid organization itself
   - ASFID signature: S=0.90, I=0.85, A=0.80

2. **ElectronicArchitecture**
   - Combo of: `m2:Layer ⊗ m2:Constraint ⊗ m2:Signature`
   - Role: Quantum mechanical basis for structure
   - ASFID signature: S=0.85, I=0.95, A=0.85

3. **PropertyGradient**
   - Combo of: `m2:Gradient ⊗ m2:Pattern ⊗ m2:Topology`
   - Role: Directional trends across table
   - ASFID signature: F=0.75, I=0.85, S=0.80

---

### Decision Points for Michel ⏸

**Question 1**: Do we model individual elements (H, He, Li...) as 118 separate M0 components in the JSON-LD, or represent them abstractly as a set?

**Option A** (Abstract): 
```json
"components": [
  {
    "@id": "m0:Ptoe:Elements",
    "rdfs:label": "118 Chemical Elements",
    "m1:instanceOf": "m1:chemistry:Element",
    "m0:cardinality": 118,
    "asfidContribution": {"S": 0.90, "I": 0.95}
  }
]
```

**Option B** (Explicit — ~300 lines JSON):
```json
"components": [
  {"@id": "m0:Ptoe:H", "rdfs:label": "Hydrogen", "m1:Z": 1, ...},
  {"@id": "m0:Ptoe:He", "rdfs:label": "Helium", "m1:Z": 2, ...},
  ...118 entries
]
```

**Recommendation**: **Option A** for M0 (minimal + complete), with Option B as supplementary data file if needed for simulation.

**Question 2**: Dynamics score — confirm D=0.65 (static table) or D=0.75 (discovery process)?

**Your decision needed before finalizing JSON-LD.**

---

## Next Steps

1. ✅ M2 identification complete (19 concepts, no new candidates)
2. ✅ M1 identification complete (8 chemistry concepts required)
3. ⏸ **AWAIT MICHEL'S DECISIONS** on Questions 1 & 2
4. → Generate M0_Ptoe.jsonld (Step 3.3)
5. → Generate M0_Ptoe_README.md (Step 3.4)
6. → SHACL validation (Step 3.5)
