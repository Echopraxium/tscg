---
name: tscg-generate-Mn-grammars
description: >
  Generate SHACL grammar schemas for TSCG meta-levels M1, M2, and M3. Each level 
  has distinct validation requirements based on its architectural role. Use this 
  skill when Michel mentions "grammaire SHACL pour M1/M2/M3", wants to validate 
  M1 extensions (Biology, Physics, etc.), needs to validate M2 GenericConcepts 
  structure, or must update M3 after foundational changes (e.g., structural 
  grammar migration). The skill presents interactive level selection (M1/M2/M3) 
  unless explicitly specified, then generates comprehensive SHACL constraints with 
  absolute URLs, forbidden patterns, and detailed validation messages.
---

# TSCG Generate Mn Grammars Skill

**Version**: 1.1.0  
**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-05-11  
**Status**: Production

## Purpose

Generate SHACL grammar schemas for TSCG meta-levels M1, M2, and M3. Each level has distinct validation requirements based on its architectural role in the TSCG framework.

## When to Use This Skill

Use this skill when:
- Michel mentions "grammaire SHACL pour M1/M2/M3" or "générer la grammaire"
- Michel asks to "générer la grammaire de M2_GenericConcepts"
- Michel wants to validate M1 extensions (Biology, Physics, etc.)
- Michel says "valider M3_GenesisSpace avec SHACL"
- A new M1 extension is created and needs validation schema
- M2 GenericConcepts structure changes require grammar updates
- M3 foundational properties are modified (e.g., structural grammar migration)

**Interactive Workflow**: The skill will ALWAYS ask the user to select the meta-level (M1, M2, or M3) using interactive buttons, unless the level is explicitly mentioned in the request (e.g., "génère la grammaire SHACL pour M2").

## Prerequisites

**Required Files to Read**:
1. Target ontology file (e.g., `M2_GenericConcepts.jsonld`, `M3_GenesisSpace.jsonld`)
2. `/mnt/project/M0_Instances_Schema_shacl.ttl` (reference for TSCG SHACL patterns)
3. `/mnt/project/Structural_Grammar_Foundation.md` (if working post-migration)
4. `/mnt/project/M2_FormulasReference_v15_10_0.md` (for M2 formula constraints)

**Context Understanding**:
- TSCG architectural levels: M3 (meta-ontology) → M2 (generic concepts) → M1 (domain concepts) → M0 (instances)
- ASFID dimensions: Attractor, Structure, Flow, Information, Dynamics
- REVOI dimensions: Representable, Evolvable, Verifiable, Observable, Interoperable
- Namespace policy: `m3:`, `m2:`, `m1:`, `m0:` (NEVER `tscg:`)
- Base URL: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`

## Workflow: 5 Sequential Steps

### STEP 0: Level Selection (Interactive)

**Goal**: Determine which meta-level (M1, M2, or M3) to generate SHACL schema for.

**Actions**:

1. **Present level options to user** using `ask_user_input_v0`:
   ```
   Question: "Pour quel niveau méta voulez-vous générer la grammaire SHACL ?"
   Options:
   - "M1 - CoreConcepts & Extensions (Domaine)"
   - "M2 - GenericConcepts (Transdisciplinaire)"
   - "M3 - GenesisSpace (Méta-Ontologie)"
   ```

2. **Capture user selection**:
   - User selects one option
   - Extract level number (1, 2, or 3) from selection
   - Store as `target_level` variable for subsequent steps

3. **Determine target files based on level**:
   - **M1**: `M1_CoreConcepts.jsonld` or specific extension (e.g., `M1_Biology.jsonld`)
     - If M1 selected, ask if user wants core or specific extension
   - **M2**: `M2_GenericConcepts.jsonld`
   - **M3**: `M3_GenesisSpace.jsonld`, `M3_EagleEye.jsonld`, `M3_SphinxEye.jsonld`

**Example Interaction**:
```
Claude: "Pour quel niveau méta voulez-vous générer la grammaire SHACL ?"
[Interactive buttons shown]

Michel: [Clicks "M2 - GenericConcepts (Transdisciplinaire)"]

Claude: "Parfait ! Je vais générer la grammaire SHACL pour M2_GenericConcepts.jsonld."
[Proceeds to STEP 1]
```

**Special Case - M1 Extensions**:
If user selects M1, present follow-up question:
```
Question: "Voulez-vous générer la grammaire pour M1_CoreConcepts ou une extension spécifique ?"
Options:
- "M1_CoreConcepts (base)"
- "Extension spécifique (Biology, Physics, Chemistry, etc.)"
```

If "Extension spécifique" selected, ask for extension name or present list of available extensions.

**Deliverable**: Confirmed target level (1, 2, or 3) and target ontology file(s).

---

### STEP 1: Ontology Analysis

**Goal**: Understand the target ontology structure and identify validation requirements.

**Actions**:
1. **Read target ontology file**:
   - For M3: `M3_GenesisSpace.jsonld`, `M3_EagleEye.jsonld`, `M3_SphinxEye.jsonld`
   - For M2: `M2_GenericConcepts.jsonld`
   - For M1: `M1_CoreConcepts.jsonld` + specific extension (e.g., `M1_Biology.jsonld`)

2. **Catalog all properties** used in the ontology:
   - Standard properties (owl:, rdfs:, dcterms:, skos:, rdf:)
   - TSCG properties (m3:, m2:, m1:, m0:)
   - Domain-specific properties (m1bio:, m1chem:, m1optics:, etc.)

3. **Identify structural patterns**:
   - Required vs optional properties
   - Cardinality constraints (minCount/maxCount)
   - Datatype constraints (xsd:string, xsd:float, xsd:date, IRI references)
   - Value ranges (e.g., ASFID/REVOI scores: 0.0-1.0)
   - Enum constraints (e.g., m3:ontologyType values)

4. **Document property usage statistics**:
   ```
   Property: m2:hasM3Origin
   Usage: 78/80 GenericConcepts (98%)
   Type: IRI reference to M3 dimensions
   Required: YES
   ```

**Deliverable**: Property catalog with usage statistics and constraints specification.

---

### STEP 2: Constraint Design

**Goal**: Design SHACL constraints specific to the target meta-level.

**Level-Specific Considerations**:

#### M3 - GenesisSpace (Meta-Ontology Layer)

**Focus**: Foundational meta-properties and dimensional framework

**Key Constraints**:
1. **Ontology Type Declaration**:
   - `m3:ontologyType` values: `m3:Poclet`, `m3:SystemicFramework`, `m3:SymbolicSystemGrammar`, `m3:TransDisclet`, `m3:TscgTool`, `m3:Enigma`
   - Cardinality: exactly 1

2. **ASFID/REVOI Dimensions**:
   - Each dimension must be an `owl:ObjectProperty`
   - Domain/Range constraints
   - rdfs:label and rdfs:comment mandatory

3. **Structural Grammar Properties** (post-migration):
   - `hasStructuralGrammarFormula`: IRI or literal
   - `hasStructuralGrammarFormulaInteroperability`: IRI reference
   - No tensor-related properties allowed

4. **Namespace Purity**:
   - Only `m3:` namespace for M3-specific properties
   - Standard namespaces allowed (owl:, rdfs:, rdf:)

**Example Constraint (M3)**:
```turtle
m3:M3DimensionShape
  a sh:NodeShape ;
  sh:targetClass owl:ObjectProperty ;
  sh:property [
    sh:path rdfs:label ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "M3 dimensions MUST have exactly one rdfs:label"
  ] ;
  sh:property [
    sh:path m3:dimensionType ;
    sh:in ( m3:ASFID m3:REVOI ) ;
    sh:minCount 1 ;
    sh:message "M3 dimensions MUST declare dimensionType as ASFID or REVOI"
  ] .
```

#### M2 - GenericConcepts (Transdisciplinary Patterns Layer)

**Focus**: Atomic transdisciplinary concepts and their formulas

**Key Constraints**:
1. **GenericConcept Structure**:
   - `@type`: Must include `owl:Class` AND `m2:GenericConcept`
   - `rdfs:label`: Exactly 1, PascalCase format
   - `rdfs:comment`: Exactly 1, transdisciplinary definition
   - `m2:conceptFamily`: One of 9 families (Agent, Boundary, Cycle, Flow, Gradient, Hierarchy, Pattern, Resonance, Transformation)

2. **M3 Origin Reference**:
   - `m2:hasM3Origin`: IRI reference to M3 dimension(s)
   - Multiple origins allowed (array format)
   - Must resolve to valid M3 ASFID or REVOI dimension

3. **Structural Grammar Formulas**:
   - `hasStructuralGrammarFormula`: Lambek calculus notation
   - `hasStructuralGrammarFormulaInteroperability`: Cross-domain application patterns
   - Optional but recommended

4. **ASFID/REVOI Scores**:
   - Each GenericConcept SHOULD have scores
   - Format: `m2:asfidScores` / `m2:revoiScores` objects
   - Each dimension score: 0.0-1.0 range

5. **Forbidden Patterns**:
   - No `hasTensorFormula` (obsolete, replaced by structural grammar)
   - No `m1:` properties in M2 (wrong level)
   - No instance-specific properties (those belong in M0)

**Example Constraint (M2)**:
```turtle
m2:GenericConceptShape
  a sh:NodeShape ;
  sh:targetClass m2:GenericConcept ;
  sh:property [
    sh:path m2:hasM3Origin ;
    sh:nodeKind sh:IRI ;
    sh:minCount 1 ;
    sh:message "Every GenericConcept MUST reference at least one M3 dimension via m2:hasM3Origin"
  ] ;
  sh:property [
    sh:path m2:conceptFamily ;
    sh:in ( 
      m2:Agent m2:Boundary m2:Cycle m2:Flow 
      m2:Gradient m2:Hierarchy m2:Pattern 
      m2:Resonance m2:Transformation 
    ) ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "GenericConcept MUST belong to exactly one of 9 concept families"
  ] .
```

#### M1 - CoreConcepts + Extensions (Domain Layer)

**Focus**: Domain-specific concepts extending M2 GenericConcepts

**Key Constraints**:
1. **M1 Concept Structure**:
   - `@type`: Must include `owl:Class`
   - `rdfs:label`: Domain-specific terminology
   - `m1:domain`: Reference to domain in M1_Domains.jsonld
   - `m1:extendsGenericConcept`: IRI reference to M2 GenericConcept

2. **Domain Extension Validation**:
   - Each M1 extension must declare its domain
   - Domain must be registered in M1_Domains.jsonld
   - M1 properties must use appropriate namespace (m1bio:, m1chem:, etc.)

3. **M2 Reference Integrity**:
   - `m1:extendsGenericConcept` must resolve to valid M2 GenericConcept
   - Inherited properties from M2 preserved
   - Domain-specific refinements allowed

4. **Extension-Specific Properties**:
   - Biology: m1bio:organismType, m1bio:cellularLevel, etc.
   - Physics: m1phys:physicalQuantity, m1phys:conservationLaw, etc.
   - Chemistry: m1chem:reactionType, m1chem:bondType, etc.

**Example Constraint (M1)**:
```turtle
m1:DomainConceptShape
  a sh:NodeShape ;
  sh:targetClass owl:Class ;
  sh:property [
    sh:path m1:domain ;
    sh:datatype xsd:string ;
    sh:minCount 1 ;
    sh:message "M1 concepts MUST declare their domain"
  ] ;
  sh:property [
    sh:path m1:extendsGenericConcept ;
    sh:nodeKind sh:IRI ;
    sh:minCount 0 ;
    sh:message "M1 concepts SHOULD reference parent M2 GenericConcept via m1:extendsGenericConcept"
  ] .
```

---

### STEP 3: SHACL Generation

**Goal**: Generate the actual SHACL .ttl file with comprehensive constraints.

**File Naming Convention**:
- M3: `M3_GenesisSpace_Schema.shacl.ttl`
- M2: `M2_GenericConcepts_Schema.shacl.ttl`
- M1: `M1_CoreConcepts_Schema.shacl.ttl` (or `M1_Biology_Schema.shacl.ttl` for extensions)

**SHACL File Structure**:

```turtle
# TSCG [Level] - SHACL Schema v1.0
# Author: Echopraxium with the collaboration of Claude AI
# Date: YYYY-MM-DD
# Target: [M3_GenesisSpace.jsonld | M2_GenericConcepts.jsonld | M1_CoreConcepts.jsonld]
# Status: Production

@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix m0: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#> .
@prefix m1: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#> .
@prefix m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#> .
@prefix m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#> .

# ============================================
# NAMESPACE POLICY (CRITICAL)
# ============================================
# [Standard namespace documentation from M0 SHACL]

# ============================================
# [LEVEL-SPECIFIC SHAPES]
# ============================================

# [Generate shapes based on Step 2 design]

# ============================================
# FORBIDDEN PATTERNS
# ============================================

# [Level-specific forbidden patterns]

# ============================================
# STATISTICS & CHANGELOG
# ============================================
# [Property coverage statistics]
# 
# CHANGELOG:
# v1.0 (YYYY-MM-DD): Initial [M1/M2/M3] grammar generation
#   - [List of constraint categories]
#   - [Key validation rules]
```

**Critical Generation Rules**:

1. **Absolute URLs**: All namespace declarations must use absolute URLs (not relative):
   ```turtle
   @prefix m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#> .
   # NOT: @prefix m3: <M3_GenesisSpace.jsonld#> .
   ```

2. **Property Paths**: Use correct SHACL syntax for nested properties:
   ```turtle
   sh:property [
     sh:path m3:eagle_eye:Attractor ;  # For nested namespace
     sh:datatype xsd:float ;
   ] ;
   ```

3. **sh:in for Enums**: Use proper list syntax:
   ```turtle
   sh:in ( m2:Agent m2:Boundary m2:Cycle ) ;
   ```

4. **SPARQL Constraints**: For complex validations (optional but powerful):
   ```turtle
   sh:sparql [
     a sh:SPARQLConstraint ;
     sh:message "M2 GenericConcept must have valid M3Origin reference" ;
     sh:select """
       PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
       PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#>
       SELECT $this ?origin
       WHERE {
         $this m2:hasM3Origin ?origin .
         FILTER NOT EXISTS { ?origin a owl:ObjectProperty }
       }
     """
   ] .
   ```

5. **Clear Error Messages**: Each constraint must have informative sh:message:
   ```turtle
   sh:message "CRITICAL: M2 GenericConcept MUST have m2:conceptFamily property with one of 9 family values. Current value missing or invalid. Valid families: Agent, Boundary, Cycle, Flow, Gradient, Hierarchy, Pattern, Resonance, Transformation."
   ```

**Deliverable**: Complete `.shacl.ttl` file ready for validation testing.

---

### STEP 4: Validation & Documentation

**Goal**: Validate the generated SHACL schema and document its usage.

**Actions**:

1. **Self-Validation Check**:
   ```python
   # Quick syntax check - ensure the .ttl file is valid Turtle
   from rdflib import Graph
   
   g = Graph()
   try:
       g.parse("/path/to/Mn_Schema.shacl.ttl", format="turtle")
       print(f"✓ SHACL schema is valid Turtle syntax ({len(g)} triples)")
   except Exception as e:
       print(f"✗ Syntax error: {e}")
   ```

2. **Test Against Target Ontology** (if pyshacl available):
   ```python
   from pyshacl import validate
   
   # Load target ontology
   data_graph = Graph()
   data_graph.parse("M2_GenericConcepts.jsonld", format="json-ld")
   
   # Load SHACL schema
   shacl_graph = Graph()
   shacl_graph.parse("M2_GenericConcepts_Schema.shacl.ttl", format="turtle")
   
   # Validate
   conforms, results_graph, results_text = validate(
       data_graph,
       shacl_graph=shacl_graph,
       inference='rdfs',
       abort_on_first=False
   )
   
   print(f"Validation result: {'✓ CONFORMS' if conforms else '✗ VIOLATIONS'}")
   print(results_text)
   ```

3. **Generate Validation Report**:
   - Count total constraints generated
   - List constraint categories
   - Document property coverage (% of properties validated)
   - Identify any optional vs mandatory distinctions

4. **Create Companion README**:
   - `Mn_Schema_README.md` explaining:
     - Purpose of the schema
     - How to run validation
     - Interpretation of validation errors
     - Maintenance guidelines

**Example README Structure**:
```markdown
# M2 GenericConcepts SHACL Schema

## Purpose
Validates the structural and semantic integrity of M2_GenericConcepts.jsonld.

## Usage

### Validation Command
```bash
pyshacl -s M2_GenericConcepts_Schema.shacl.ttl \
        -f human \
        M2_GenericConcepts.jsonld
```

### Expected Output
- ✓ CONFORMS: All 80 GenericConcepts pass validation
- ✗ VIOLATIONS: Shows which concepts fail which constraints

## Constraint Categories
1. **Structural Constraints** (15 shapes)
   - @type validation
   - rdfs:label/comment requirements
   - m2:conceptFamily membership

2. **M3 Reference Integrity** (3 shapes)
   - m2:hasM3Origin validation
   - Valid M3 dimension references

3. **Formula Constraints** (5 shapes)
   - hasStructuralGrammarFormula syntax
   - Lambek calculus notation checks

4. **Forbidden Patterns** (8 shapes)
   - No hasTensorFormula (obsolete)
   - No m1: properties in M2
   - Namespace purity enforcement

## Maintenance
- Update when M2 structure changes
- Re-run validation after M3 migration
- Keep changelog up to date
```

**Deliverable**: Validated SHACL schema + README documenting usage.

---

## Level-Specific Validation Examples

### M3 Example Validation

**Test Case**: Validate M3_EagleEye.jsonld ASFID dimensions

```turtle
# M3_GenesisSpace_Schema.shacl.ttl excerpt
m3:ASFIDDimensionShape
  a sh:NodeShape ;
  sh:targetNode 
    m3:eagle_eye:Attractor 
    m3:eagle_eye:Structure 
    m3:eagle_eye:Flow 
    m3:eagle_eye:Information 
    m3:eagle_eye:Dynamics ;
  sh:property [
    sh:path rdf:type ;
    sh:hasValue owl:ObjectProperty ;
    sh:minCount 1 ;
  ] ;
  sh:property [
    sh:path rdfs:label ;
    sh:datatype xsd:string ;
    sh:pattern "^[A-Z][a-z]+$" ;  # PascalCase
    sh:minCount 1 ;
    sh:maxCount 1 ;
  ] ;
  sh:property [
    sh:path m3:dimensionIndex ;
    sh:datatype xsd:integer ;
    sh:minInclusive 0 ;
    sh:maxInclusive 4 ;
    sh:minCount 1 ;
  ] .
```

**Expected Result**:
```
✓ m3:eagle_eye:Attractor validates successfully
✓ m3:eagle_eye:Structure validates successfully
✓ m3:eagle_eye:Flow validates successfully
✓ m3:eagle_eye:Information validates successfully
✓ m3:eagle_eye:Dynamics validates successfully
```

### M2 Example Validation

**Test Case**: Validate GenericConcept "Catalyst" structure

```turtle
# M2_GenericConcepts_Schema.shacl.ttl excerpt
m2:GenericConceptShape
  a sh:NodeShape ;
  sh:targetClass m2:GenericConcept ;
  sh:property [
    sh:path m2:conceptFamily ;
    sh:in ( 
      m2:Agent m2:Boundary m2:Cycle m2:Flow 
      m2:Gradient m2:Hierarchy m2:Pattern 
      m2:Resonance m2:Transformation 
    ) ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "GenericConcept MUST belong to exactly one of 9 families"
  ] ;
  sh:property [
    sh:path m2:hasM3Origin ;
    sh:nodeKind sh:IRI ;
    sh:minCount 1 ;
    sh:message "GenericConcept MUST reference at least one M3 dimension"
  ] .
```

**Test Data** (from M2_GenericConcepts.jsonld):
```json
{
  "@id": "m2:Catalyst",
  "@type": ["owl:Class", "m2:GenericConcept"],
  "rdfs:label": "Catalyst",
  "m2:conceptFamily": {"@id": "m2:Agent"},
  "m2:hasM3Origin": [
    {"@id": "m3:eagle_eye:Attractor"},
    {"@id": "m3:eagle_eye:Dynamics"}
  ]
}
```

**Expected Result**:
```
✓ m2:Catalyst has valid conceptFamily (Agent)
✓ m2:Catalyst has valid M3 origins (2 dimensions)
✓ m2:Catalyst conforms to GenericConceptShape
```

### M1 Example Validation

**Test Case**: Validate M1_Biology extension concept

```turtle
# M1_Biology_Schema.shacl.ttl excerpt
m1bio:BiologyConceptShape
  a sh:NodeShape ;
  sh:targetClass owl:Class ;
  sh:property [
    sh:path m1:domain ;
    sh:hasValue "Biology" ;
    sh:minCount 1 ;
    sh:message "M1 Biology concepts MUST have m1:domain = 'Biology'"
  ] ;
  sh:property [
    sh:path m1:extendsGenericConcept ;
    sh:nodeKind sh:IRI ;
    sh:minCount 0 ;  # Optional but recommended
  ] ;
  sh:property [
    sh:path m1bio:organismType ;
    sh:in ( m1bio:Prokaryote m1bio:Eukaryote ) ;
    sh:minCount 0 ;
  ] .
```

**Test Data** (from M1_Biology.jsonld):
```json
{
  "@id": "m1bio:Enzyme",
  "@type": "owl:Class",
  "rdfs:label": "Enzyme",
  "m1:domain": "Biology",
  "m1:extendsGenericConcept": {"@id": "m2:Catalyst"},
  "m1bio:molecularFunction": "Catalysis"
}
```

**Expected Result**:
```
✓ m1bio:Enzyme has valid domain (Biology)
✓ m1bio:Enzyme extends valid M2 concept (Catalyst)
✓ m1bio:Enzyme conforms to BiologyConceptShape
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Relative URLs in Namespace Declarations
**Problem**: `@prefix m2: <M2_GenericConcepts.jsonld#> .`  
**Solution**: Always use absolute URLs:
```turtle
@prefix m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#> .
```

### Pitfall 2: Overly Strict Constraints
**Problem**: Requiring properties that are actually optional  
**Solution**: Use `sh:minCount 0` for optional properties, add sh:message explaining when to use them

### Pitfall 3: Missing Forbidden Pattern Checks
**Problem**: Not catching obsolete properties like `hasTensorFormula`  
**Solution**: Always include negative constraints with `sh:not`:
```turtle
sh:not [
  sh:property [
    sh:path m2:hasTensorFormula ;
    sh:minCount 1
  ]
] ;
sh:message "FORBIDDEN: hasTensorFormula is obsolete. Use hasStructuralGrammarFormula instead."
```

### Pitfall 4: Incorrect SPARQL Syntax
**Problem**: SPARQL constraint with wrong namespace prefixes  
**Solution**: Always redeclare prefixes inside SPARQL SELECT:
```turtle
sh:select """
  PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
  SELECT $this ?prop
  WHERE { $this ?prop ?value }
"""
```

---

## Integration with Other Skills

### With `tscg-tensor-to-structural-grammar-migration`
- **Before migration**: SHACL allows `hasTensorFormula`
- **After migration**: SHACL forbids `hasTensorFormula`, requires `hasStructuralGrammarFormula`
- **Update trigger**: Run this skill after Phase 1 (M3 migration) to update M3 SHACL schema

### With `tscg-instance-pipeline`
- New M0 instances validated against `M0_Instances_Schema.shacl.ttl`
- New M1 concepts validated against `M1_CoreConcepts_Schema.shacl.ttl`
- Ensures conformance throughout instance creation pipeline

### With `tscg-create-instance-simulation`
- Simulation references validated M0 instances
- SHACL ensures M0 instances have required properties for simulation (domain, scores, etc.)

---

## Output Format

For each generated schema, provide:

1. **SHACL .ttl File**: Complete, validated SHACL schema
2. **Statistics Summary**: 
   ```
   M2_GenericConcepts_Schema.shacl.ttl Statistics:
   - Total shapes: 23
   - Property constraints: 147
   - Forbidden patterns: 12
   - Property coverage: 94% (17/18 M2 properties validated)
   - Target classes: owl:Class, m2:GenericConcept
   ```

3. **README Documentation**: Usage guide and maintenance instructions

4. **Validation Report** (if tested):
   ```
   Validation against M2_GenericConcepts.jsonld:
   ✓ 78/80 GenericConcepts conform
   ✗ 2 violations:
     - m2:Oscillator: missing m2:hasM3Origin
     - m2:Feedback: invalid m2:conceptFamily value
   ```

---

## Maintenance Guidelines

### When to Regenerate SHACL Schema

1. **Major M2/M3 Refactoring**: After structural grammar migration, ontologyType additions, etc.
2. **New M1 Extensions**: When adding M1_Geology.jsonld, create M1_Geology_Schema.shacl.ttl
3. **Property Additions**: When new TSCG properties are introduced at any level
4. **Validation Coverage Gaps**: When manual testing reveals unvalidated edge cases

### Version Control

- Track SHACL schema versions alongside ontology versions
- Example: `M2_GenericConcepts.jsonld v2.1.0` → `M2_GenericConcepts_Schema.shacl.ttl v2.1.0`
- Keep changelog synchronized with ontology changes

---

## Critical Success Factors

✅ **DO**:
- Read the target ontology FIRST before designing constraints
- Use absolute URLs for all namespace declarations
- Test the generated SHACL against the actual ontology
- Document constraint rationale in sh:message
- Include both positive (required) and negative (forbidden) constraints
- Maintain property coverage statistics

❌ **DON'T**:
- Generate SHACL without analyzing the target ontology structure
- Use relative URLs in namespace declarations
- Create overly permissive constraints (defeats validation purpose)
- Forget to validate the SHACL schema itself (syntax errors)
- Ignore forbidden patterns (legacy properties must be caught)
- Leave constraints undocumented (sh:message is mandatory)

---

## Skill Completion Checklist

Before marking the skill execution complete, ensure:

- [ ] Level selected interactively (M1/M2/M3) or extracted from explicit request (Step 0)
- [ ] Target ontology file(s) identified based on level (Step 0)
- [ ] Target ontology analyzed (Step 1)
- [ ] Constraints designed for correct meta-level (Step 2)
- [ ] SHACL .ttl file generated with absolute URLs (Step 3)
- [ ] SHACL schema validated (syntax check at minimum) (Step 4)
- [ ] README documentation created (Step 4)
- [ ] Statistics summary provided (output format)
- [ ] Integration with migration skill noted (if M3 schema)
- [ ] Changelog entry added to SHACL file

---

## Example Invocations

**Generate M2 SHACL Schema**:
```
Michel: "Peux-tu générer la grammaire SHACL pour GenericConcepts ?"
Claude: [Executes tscg-generate-Mn-grammars skill]

Claude: "Pour quel niveau méta voulez-vous générer la grammaire SHACL ?"
[Shows interactive buttons: M1 / M2 / M3]

Michel: [Selects "M2 - GenericConcepts (Transdisciplinaire)"]

Claude: "Parfait ! Je vais générer la grammaire SHACL pour M2_GenericConcepts.jsonld."
→ Reads M2_GenericConcepts.jsonld (STEP 1)
→ Catalogs 80 GenericConcepts and their properties
→ Designs constraints for M2 level (conceptFamily, hasM3Origin, etc.) (STEP 2)
→ Generates M2_GenericConcepts_Schema.shacl.ttl (STEP 3)
→ Creates M2_Schema_README.md (STEP 4)
→ Provides statistics summary
```

**Generate M1 Extension Schema**:
```
Michel: "J'ai créé M1_Geology.jsonld, il faut la grammaire SHACL"
Claude: [Executes tscg-generate-Mn-grammars skill]

Claude: "Pour quel niveau méta voulez-vous générer la grammaire SHACL ?"
Michel: [Selects "M1 - CoreConcepts & Extensions (Domaine)"]

Claude: "Voulez-vous générer la grammaire pour M1_CoreConcepts ou une extension spécifique ?"
Michel: [Selects "Extension spécifique"] → "M1_Geology"

Claude: "Je vais générer la grammaire SHACL pour M1_Geology.jsonld."
→ Reads M1_Geology.jsonld (STEP 1)
→ Identifies domain-specific properties (m1geo:*) (STEP 2)
→ Validates M2 concept extensions
→ Generates M1_Geology_Schema.shacl.ttl (STEP 3)
→ Tests against M1_Geology.jsonld (STEP 4)
```

**Update M3 Schema Post-Migration**:
```
Michel: "La migration structurelle est finie, il faut mettre à jour le SHACL de M3"
Claude: [Executes tscg-generate-Mn-grammars skill]

Claude: "Pour quel niveau méta voulez-vous générer la grammaire SHACL ?"
Michel: [Selects "M3 - GenesisSpace (Méta-Ontologie)"]

Claude: "Je vais générer la grammaire SHACL pour M3_GenesisSpace.jsonld."
→ Reads updated M3_GenesisSpace.jsonld (with structural grammar properties) (STEP 1)
→ Adds constraints for hasStructuralGrammarFormula (STEP 2)
→ Adds forbidden patterns for hasTensorFormula
→ Generates M3_GenesisSpace_Schema.shacl.ttl v2.0.0 (STEP 3)
→ Documents migration-related changes in changelog (STEP 4)
```

**Quick Invocation (Level Known)**:
```
Michel: "Génère la grammaire SHACL pour M2"
Claude: [Executes skill, skips interactive selection since level is explicit]
→ Proceeds directly to STEP 1 with M2_GenericConcepts.jsonld
```

---

## Changelog

**v1.1.0 (2026-05-11)**: Interactive level selection
- **BREAKING CHANGE**: Added STEP 0 for explicit level selection (M1/M2/M3)
- Uses `ask_user_input_v0` tool for interactive level choice
- Workflow now 5 steps instead of 4 (0 → 1 → 2 → 3 → 4)
- Special handling for M1 extensions (core vs specific extension)
- Updated example invocations to show interactive flow
- Updated completion checklist

**v1.0.0 (2026-05-11)**: Initial skill creation
- Complete 4-step workflow (Analysis → Design → Generation → Validation)
- Level-specific constraint design (M1, M2, M3)
- Integration with structural grammar migration
- Comprehensive examples and pitfall documentation
- README generation for each schema
- Statistics tracking and validation reporting
