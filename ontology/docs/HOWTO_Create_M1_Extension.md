# How to Create M1 Domain Extensions

**Version**: 1.0  
**Date**: 2026-01-17  
**Framework**: TSCG (Transdisciplinary System Construction Game)

---

## Table of Contents

1. Introduction to M1 Extensions
2. Principles of Domain Specialization
3. Step-by-Step Creation Guide
4. Template and Best Practices
5. Validation Checklist
6. Examples

---

## 1. Introduction to M1 Extensions

### What is M1?

**M1** (Narratives layer) is the **domain-specific instantiation** of M2 metaconcepts.

**Role**:
- Bridge between universal patterns (M2) and concrete systems (M0)
- Specialize generic metaconcepts for specific domains
- Add domain vocabulary while maintaining TSCG foundation

### Why Extensions?

**Purity principle**:
- **M2 stays domain-agnostic** (System, Process, Feedback, etc.)
- **M1 specializes** (ChemicalReaction, Enzyme, Market, etc.)
- **M0 instantiates** (Wood fire, E. coli metabolism, Stock exchange, etc.)

**Benefits**:
- Reusable M2 patterns across domains
- Domain experts can create their own M1
- Maintains conceptual rigor of framework

---

## 2. Principles of Domain Specialization

### 2.1 Functor F_instantiate

**Mathematical definition**:
```
F_instantiate : Cat_M2 → Cat_M1_domain
```

**Properties**:
1. **Morphism preservation**: Inherits M2 relationships
2. **Semantic enrichment**: Adds domain-specific properties
3. **Multiple instantiation**: One M2 → Many M1 concepts

**Example**:
```
M2:Process (generic)
  ↓ F_instantiate (Chemistry)
M1:ChemicalReaction (specialized)
  ↓ F_instantiate (Chemistry)
M1:Combustion (further specialized)
```

### 2.2 Inheritance Rules

**MUST inherit**:
- `@type: rdfs:subClassOf` relationship to parent M2
- Tensor formula (ASFID basis)
- Dominant M3 dimensions

**MAY add**:
- Domain-specific properties
- Constraints
- Examples
- Subtypes
- Measurement units

**MUST NOT**:
- Violate M2 semantics
- Change ASFID foundation
- Create isolated concepts (must link to M2)

### 2.3 Vocabulary Guidelines

**Allowed** (domain terms):
- Specialized nouns: Enzyme, Market, Photon, Neuron
- Domain operations: Catalysis, Trading, Refraction
- Domain properties: pH, Price, Wavelength, Synaptic weight

**Forbidden** (would pollute M2):
- Domain terms in M2 (keep M2 pure)
- Overly specific terms in M1 (belongs to M0 instances)

---

## 3. Step-by-Step Creation Guide

### Step 1: Identify Your Domain

**Choose a coherent domain**:
- ✅ Good: Chemistry, Biology, Economics, Engineering, Sociology
- ❌ Too broad: Science, Technology
- ❌ Too narrow: Polymer Chemistry (subclass of Chemistry)

### Step 2: Map M2 to Domain Concepts

**Create mapping table**:

| M2 Metaconcept | Domain Concept(s) | Notes |
|----------------|-------------------|-------|
| Process | ChemicalReaction | Generic transformation |
| Component | ChemicalSpecies | Fuel, O₂, etc. |
| Catalysis | Catalyst | Enzymatic catalysis |
| Feedback | pH Regulation | Buffers, homeostasis |
| ... | ... | ... |

**Questions to ask**:
1. Which M2 metaconcepts are **central** to my domain?
2. Which M2 metaconcepts **don't apply**? (e.g., Memory in simple chemistry)
3. What **domain-specific properties** must I add?

### Step 3: Create Directory Structure

```
tscg/ontology/M1_extensions/{domain}/
├── M1_{Domain}.jsonld          # Main ontology
├── README.md                   # Domain documentation
└── examples/
    ├── {example1}.jsonld       # M0 instances
    ├── {example2}.jsonld
    └── ...
```

### Step 4: Write M1 Ontology (JSON-LD)

**Use template** (see Section 4)

**Key sections**:
1. `@context`: Namespaces (m1, m2, m3)
2. Ontology metadata
3. Class definitions (domain concepts)
4. Properties and constraints
5. Examples

### Step 5: Create M0 Instances (Examples)

**Purpose**:
- Validate M1 concepts
- Demonstrate usage
- Provide pedagogical examples

**Good examples**:
- Canonical (Fire Triangle for Combustion)
- Diverse (different instantiations)
- Well-documented (ASFID states, metaconcepts)

### Step 6: Validate

**Checklist** (see Section 5)

---

## 4. Template and Best Practices

### 4.1 M1 Ontology Template

```json
{
  "@context": {
    "m1": "https://github.com/Echopraxium/tscg/blob/main/ontology/M1_extensions/{domain}/M1_{Domain}.jsonld#",
    "m2": "https://github.com/Echopraxium/tscg/blob/main/ontology/TSCG_M2_MetaConcepts_Ontology.jsonld#",
    "m3": "https://github.com/Echopraxium/tscg/blob/main/ontology/M3_Genesis_Space.jsonld#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "dcterms": "http://purl.org/dc/terms/"
  },
  "@graph": [
    {
      "@id": "m1:M1_{Domain}_Ontology",
      "@type": "owl:Ontology",
      "dcterms:title": "TSCG M1 Extension: {Domain}",
      "dcterms:description": "{Description of domain and scope}",
      "dcterms:creator": "{Your name or organization}",
      "dcterms:created": "{YYYY-MM-DD}",
      "owl:versionInfo": "1.0.0",
      "owl:imports": [
        "https://github.com/Echopraxium/tscg/blob/main/ontology/TSCG_M2_MetaConcepts_Ontology.jsonld"
      ],
      "m1:domain": "{domain}",
      "m1:functor": "F_instantiate : M2 → M1_{domain}",
      "m1:scope": [
        "{Topic 1}",
        "{Topic 2}",
        "..."
      ]
    },
    {
      "@id": "m1:{ConceptName}",
      "@type": "owl:Class",
      "rdfs:subClassOf": "m2:{ParentMetaconcept}",
      "rdfs:label": "{Concept Label}",
      "rdfs:comment": "{Description}",
      "m1:instantiatesMetaconcept": ["m2:{MC1}", "m2:{MC2}"],
      "m1:properties": {
        "m1:property1": "{Definition}",
        "m1:property2": "{Definition}"
      },
      "m1:examples": [
        "{Example 1}",
        "{Example 2}"
      ]
    }
  ]
}
```

### 4.2 Best Practices

**Naming conventions**:
- File: `M1_{Domain}.jsonld` (e.g., `M1_Chemistry.jsonld`)
- Namespace: `m1` (short prefix)
- Classes: CamelCase (e.g., `ChemicalReaction`)
- Properties: camelCase (e.g., `m1:molecularFormula`)

**Documentation**:
- Always add `rdfs:comment` (clear, concise)
- Use `skos:altLabel` for synonyms
- Include `m1:examples` (concrete instances)
- Add `rdfs:seeAlso` for related concepts

**Structure**:
- Start with **abstract** concepts (e.g., ChemicalReaction)
- Then **specialize** (e.g., Combustion < ChemicalReaction)
- Avoid deep hierarchies (3-4 levels max)

**ASFID signatures**:
- Optional but recommended
- Helps validate M3→M2→M1 consistency
- Example: `"m1:asfidSignature": "D⊗F (high dynamics, high flow)"`

---

## 5. Validation Checklist

### 5.1 Ontology Structure

- [ ] File named `M1_{Domain}.jsonld`
- [ ] Valid JSON-LD syntax
- [ ] Imports M2 ontology
- [ ] Defines domain namespace (`m1`)
- [ ] Includes ontology metadata (title, creator, date)

### 5.2 Semantic Correctness

- [ ] All domain classes inherit from M2 (`rdfs:subClassOf`)
- [ ] `m1:instantiatesMetaconcept` lists relevant M2 parents
- [ ] No M2 semantics violated
- [ ] Domain terms not in M2 (purity maintained)
- [ ] Consistent tensor formulas (if specified)

### 5.3 Documentation Quality

- [ ] Each class has `rdfs:label` and `rdfs:comment`
- [ ] Examples provided (`m1:examples`)
- [ ] Properties clearly defined
- [ ] README.md created with domain overview

### 5.4 Examples (M0 Instances)

- [ ] At least 1 M0 instance created
- [ ] Instance validates M1 concepts
- [ ] ASFID states computed (Territory & Map)
- [ ] Metaconcepts mobilized listed

### 5.5 Integration

- [ ] Pull request to TSCG repository (if contributing)
- [ ] Tested with TSCG tooling (if available)
- [ ] Peer review (domain expert validation)

---

## 6. Examples

### 6.1 Chemistry Extension (Complete)

**Files**:
- `M1_Chemistry.jsonld`: Ontology
- `M0_FireTriangle_Instance.jsonld`: Example

**Key concepts**:
- ChemicalReaction < m2:Process
- Combustion < ChemicalReaction
- ChemicalSpecies < m2:Component
- Catalyst < m2:Catalysis

**Properties added**:
- `m1:reactants`, `m1:products`
- `m1:energyBalance`
- `m1:ignitionTemperature`

### 6.2 Biology Extension (Hypothetical)

**Key concepts**:
- BiologicalProcess < m2:Process
  - Metabolism < BiologicalProcess
    - Photosynthesis < Metabolism
    - Respiration < Metabolism
- Organism < m2:System
- Cell < m2:Component
- Enzyme < m2:Catalysis

**Properties to add**:
- `m1:geneticCode` (DNA sequence)
- `m1:proteinStructure`
- `m1:metabolicRate`

### 6.3 Economics Extension (Hypothetical)

**Key concepts**:
- EconomicProcess < m2:Process
  - Trade < EconomicProcess
  - Investment < EconomicProcess
- Market < m2:System
- Agent < m2:Agent (already in M2!)
- Price < m2:Signal

**Properties to add**:
- `m1:currency`
- `m1:elasticity`
- `m1:marketCapitalization`

---

## 7. Common Pitfalls

### ❌ Pitfall 1: Polluting M2

**Bad**:
```json
{
  "@id": "m2:Enzyme",  // ❌ Domain-specific term in M2
  "@type": "m2:MetaConcept"
}
```

**Good**:
```json
{
  "@id": "m1:Enzyme",  // ✅ Domain-specific term in M1
  "rdfs:subClassOf": "m2:Catalysis"
}
```

### ❌ Pitfall 2: Ignoring M2 Inheritance

**Bad**:
```json
{
  "@id": "m1:Combustion",
  "@type": "owl:Class"
  // ❌ No link to M2!
}
```

**Good**:
```json
{
  "@id": "m1:Combustion",
  "rdfs:subClassOf": "m2:Process",
  "m1:instantiatesMetaconcept": ["m2:Process", "m2:Dissipation"]
}
```

### ❌ Pitfall 3: Overly Deep Hierarchies

**Bad**:
```
Process → ChemicalReaction → Combustion → OrganicCombustion → 
  WoodCombustion → OakWoodCombustion  // ❌ Too deep!
```

**Good**:
```
Process → ChemicalReaction → Combustion
  (OakWood fire is M0 instance, not M1 class)
```

### ❌ Pitfall 4: Missing ASFID Foundation

**Bad**:
```json
{
  "@id": "m1:Combustion",
  "m1:temperature": "High"  // ❌ No ASFID reference
}
```

**Good**:
```json
{
  "@id": "m1:Combustion",
  "m1:asfidSignature": "High A, Medium S, High F, Medium I, High D",
  "m1:temperature": "Above ignition point (threshold)"
}
```

---

## 8. Resources

### TSCG Core Ontologies

- **M3**: `/ontology/M3_Genesis_Space.jsonld`
- **M2**: `/ontology/TSCG_M2_MetaConcepts_Ontology.jsonld`
- **Template**: `/ontology/M1_extensions/template/M1_Template.jsonld`

### Reference M1 Extensions

- **Chemistry**: `/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld`
- (More to come: Biology, Economics, Engineering, etc.)

### Validation Tools

- JSON-LD validator: https://json-ld.org/playground/
- RDF validator: (TSCG tooling - future)

### Community

- GitHub: https://github.com/Echopraxium/tscg
- Discussions: [link to discussions]
- Contributions: Pull requests welcome!

---

## 9. Next Steps

After creating your M1 extension:

1. **Test** with M0 instances (real examples)
2. **Document** in README.md
3. **Share** with TSCG community (optional)
4. **Iterate** based on feedback
5. **Publish** to domain-specific community

---

## 10. FAQ

**Q: Can I create M1 extension for my niche domain?**
A: Yes! As long as it's coherent and inherits from M2.

**Q: Must I use all M2 metaconcepts?**
A: No, only relevant ones. Chemistry doesn't use Memory or Learning, for example.

**Q: Can I combine multiple domains?**
A: Yes (e.g., Biochemistry = Chemistry + Biology), but keep it coherent.

**Q: What if my domain needs a new M2 metaconcept?**
A: Propose it! If genuinely universal (not domain-specific), it may be added to M2.

**Q: Can I have multiple M1 files for one domain?**
A: Recommended to keep it in one file unless very large. Use subdirectories for subtopics if needed.

**Q: How do I handle units and measurements?**
A: Use standard ontologies (QUDT for units) or define domain-specific properties with `xsd:float` + unit annotation.

---

**END OF GUIDE**

**Version**: 1.0  
**Author**: TSCG Project  
**License**: Open for community use  
**Contributions**: Welcome via GitHub pull requests
