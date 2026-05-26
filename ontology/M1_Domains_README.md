# M1_Domains.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 1.2.0
**Date**: 2026-04-26
**Layer**: M1 — Domain Registry
**Status**: Active

---

## Overview

`M1_Domains.jsonld` is the **domain registry ontology** for the TSCG M1 layer.
It declares metadata about available knowledge domains, their extensions, and
their relationships to the TSCG hierarchy.

This file serves as a **catalog and index** for M1 domain extensions, providing
a structured overview of which fields of knowledge have been formalized in TSCG.

---

## Position in the Import Hierarchy

```
M3_GrammarFoundation.jsonld  ─┐
M3_EagleEye.jsonld           ─┤→  M3_GenesisGrammar.jsonld
M3_SphinxEye.jsonld          ─┤           ↓ imported by
M3_BicephalousPerspective    ─┘  M2_GenericConcepts.jsonld
                                           ↓ imported by
                                  M1_CoreConcepts.jsonld
                                  M1_Domains.jsonld         ← THIS FILE (peer to CoreConcepts)
                                           ↓ referenced by
                                  M1_Biology.jsonld
                                  M1_Physics.jsonld
                                  M1_xxx.jsonld
```

**Imports**: `M2_GenericConcepts.jsonld`
**Role**: Registry/index for M1 domain extensions

---

## Purpose and Functionality

### **1. Domain Catalog**

M1_Domains maintains a structured registry of knowledge domains that have TSCG
extensions:

```json
{
  "domains": [
    {
      "id": "biology",
      "label": "Biology",
      "ontology": "M1_Biology.jsonld",
      "status": "active",
      "coverage": "comprehensive"
    },
    {
      "id": "physics",
      "label": "Physics",
      "ontology": "M1_Physics.jsonld",
      "status": "active",
      "coverage": "comprehensive"
    }
  ]
}
```

### **2. Extension Metadata**

For each domain, the registry provides:
- **Domain identifier** — canonical short name (e.g., "biology", "physics")
- **Display label** — human-readable name
- **Ontology file** — path to the M1 extension `.jsonld` file
- **Status** — active, development, deprecated
- **Coverage** — comprehensive, partial, experimental
- **Dependencies** — other domains this extension depends on
- **Version** — current version of the domain extension

### **3. Interdomain Relationships**

Documents relationships between knowledge domains:
- **Overlaps** — domains sharing conceptual territory
- **Dependencies** — domains requiring concepts from others
- **Bridges** — transdisciplinary concepts spanning domains

---

## Domain Extension Structure

M1 domain extensions follow a consistent directory structure:

```
ontology/
└── M1_extensions/
    ├── biology/
    │   ├── M1_Biology.jsonld
    │   └── biology_README.md
    ├── physics/
    │   ├── M1_Physics.jsonld
    │   └── physics_README.md
    ├── chemistry/
    │   ├── M1_Chemistry.jsonld
    │   └── chemistry_README.md
    └── ...
```

M1_Domains.jsonld provides the **index** to this structure.

---

## Current Domain Coverage (as of v1.2.0)

### **Natural Sciences**
- ✅ **Biology** — organisms, evolution, cellular systems, physiology
- ✅ **Chemistry** — reactions, thermodynamics, atomic structure, periodic properties
- ✅ **Physics** — mechanics, thermodynamics, electromagnetism, optics
- ✅ **Ecology** — ecosystems, populations, environmental systems
- ✅ **Geology** — earth sciences, tectonics, stratigraphy

### **Formal & Engineering Sciences**
- ✅ **Mathematics** — structures, operations, proofs (referenced, stub)
- ✅ **Electronics** — circuits, signal processing, components
- ✅ **Engineering** — design, optimization, control systems
- ✅ **Computer Science** — algorithms, data structures, architectures
- ✅ **Blockchain** — cryptography, distributed systems, consensus algorithms

### **Social & Human Sciences**
- ✅ **Economics** — markets, production, exchange, value
- ✅ **Education** — pedagogy, learning systems, knowledge transfer
- ✅ **Philosophy** — ontology, epistemology, ethics, logic
- ✅ **Mythology** — cosmology, archetypes, spiritual systems
- ✅ **GameTheory** — strategy, decision theory, equilibria

### **Perceptual & Creative Sciences**
- ✅ **Optics** — color theory, light physics, wave phenomena
- ✅ **Photography** — camera technology, exposure control, image formation
- ✅ **MusicTheory** — acoustics, composition, harmony
- ✅ **Television** — signal transmission, broadcasting, display systems

### **Interdisciplinary**
- ✅ **Neurobiology** — brain, neural circuits, neurochemistry
- ✅ **SystemsTheory** — cybernetics, feedback, emergence

*Legend: ✅ Active registry entry*

---

## Validation Status

**OWL/RDFS Compliance:** ✅ Validated (May 14, 2026)
- RDFS diagnostic: 0 errors (no errors found — already clean)
- OWL Pellet reasoning: PASSED
- Protégé compatibility: Confirmed

**No corrections needed** — M1_Domains.jsonld was already OWL-compliant.

For validation details, see: `CLAUDE.md` and `M0_Instances_Schema_shacl.ttl`.

---

## Ontology Statistics

**Classes:** 0 (pure registry, no new classes defined)
**Properties:** 0 (uses existing M2/M3 properties)
**Imports:** M2_GenericConcepts.jsonld
**Triples:** ~50-100 (metadata annotations)

**Note:** M1_Domains is a **metadata-only** ontology — it documents the domain
structure without defining new conceptual types.

---

## Usage Examples

### **1. Domain Discovery**

Applications can query M1_Domains to discover available extensions:

```sparql
SELECT ?domain ?label ?ontology
WHERE {
  ?domain rdf:type m1:Domain ;
          rdfs:label ?label ;
          m1:hasOntologyFile ?ontology .
}
```

### **2. Dependency Resolution**

Before loading a domain extension, check its dependencies:

```sparql
SELECT ?dependency
WHERE {
  m1:domain:Biology m1:dependsOn ?dependency .
}
```

### **3. Status Checking**

Verify which domains are production-ready:

```sparql
SELECT ?domain ?status
WHERE {
  ?domain rdf:type m1:Domain ;
          m1:developmentStatus ?status .
  FILTER (?status = "active")
}
```

---

## Design Principles

### **1. Single Source of Truth**

M1_Domains is the **authoritative registry** for TSCG domain coverage.
All domain metadata lives here — extensions should not duplicate this
information.

### **2. Machine-Readable**

The registry is designed for programmatic access:
- Structured JSON-LD format
- Consistent property names
- SPARQL-queryable

### **3. Human-Readable**

Despite being machine-processable, the registry remains clear for humans:
- Natural language labels
- Descriptive comments
- Logical organization

### **4. Extensible**

New domains can be added without breaking existing structure:
- No hardcoded assumptions
- Flexible metadata schema
- Version-controlled updates

---

## Role in TSCG Workflow

### **During Development**

1. **Adding a new domain:**
   - Create `M1_NewDomain.jsonld` extension
   - Register in `M1_Domains.jsonld`
   - Document in domain README
   - Update this README's coverage list

2. **Domain version updates:**
   - Update extension file
   - Increment version in `M1_Domains.jsonld`
   - Document changes in extension changelog

### **During Instance Creation (M0)**

When creating instances, M1_Domains helps identify which extension to use:

```
System to model: "E. coli glucose metabolism"
Query M1_Domains → identifies M1_Biology.jsonld
Import M1_Biology → access DNA_Replication, Glycolysis, etc.
Create instance → M0_Ecoli_Glucose_Metabolism.jsonld
```

### **During Validation**

The validation pipeline checks:
- All domains listed in M1_Domains have corresponding ontology files
- All M1 extension files reference M1_Domains for metadata
- No orphaned extensions (files not in registry)
- No broken dependencies (domain requires nonexistent domain)

---

## Future Extensions

### **Planned Additions**

1. **Coverage metrics** — percentage of domain formalized in TSCG
2. **Maturity levels** — alpha, beta, stable, mature
3. **Citation metadata** — key references for each domain
4. **Expert contacts** — domain specialists for validation
5. **Cross-domain mappings** — concept equivalences between domains

### **Integration Goals**

- **Automatic documentation generation** — README updates from M1_Domains data
- **Dashboard visualization** — interactive domain coverage map
- **Dependency graphs** — visual representation of domain relationships

---

## Maintenance Guidelines

### **When to Update M1_Domains**

Update this registry when:
- ✅ A new M1 domain extension is added
- ✅ A domain extension changes status (development → active)
- ✅ Domain dependencies are added or removed
- ✅ Domain metadata changes (coverage level, version)

### **What NOT to Put in M1_Domains**

Don't include:
- ❌ Actual domain concepts (those go in M1_Extensions)
- ❌ M2 GenericConcepts metadata (already in M2)
- ❌ M0 instance lists (instances are independent files)
- ❌ Detailed domain theories (those go in domain READMEs)

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **1.2.0** | 2026-04-26 | Added Ptoe to Chemistry. Updated Chemistry subdomains. Chemistry instanceCount: 3→4. M1_Chemistry enriched to v1.1.0. |
| **1.1.0** | 2026-04-19 | Added Blockchain domain (6 subdomains). First instance: M0_NakamotoConsensus. |
| **1.0.0** | 2026-04-18 | Initial complete registry: 20 primary domains, 26 total instances. Based on exhaustive corpus analysis. |

---

## See Also

- `M1_CoreConcepts.jsonld` — M1 core concept categories
- `M1_Biology.jsonld` — Biological domain concepts
- `M1_Physics.jsonld` — Physical domain concepts
- `M2_GenericConcepts.jsonld` — Transdisciplinary derived types
- `M3_GenesisGrammar.jsonld` — Structural grammar foundation
- `CLAUDE.md` — Modeling conventions and authoring rules

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI — May 2026*
