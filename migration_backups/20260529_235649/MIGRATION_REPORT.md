# TSCG Automated Migration Report (v3.0.0 - GenesisGrammar + @base)

**Date:** 2026-05-29 23:57:13
**Backup Location:** E:\_00_Michel\_00_Lab\_00_GitHub\tscg\migration_backups\20260529_235649

## Summary

- ✅ **Successful:** 25
- ❌ **Failed:** 1
- 📊 **Total:** 26

## Detailed Results

### AdaptativeImmuneResponse (poclet)
**Status:** ✅ Success

### BloodPressureControl (poclet)
**Status:** ✅ Success

### ButterflyMetamorphosis (poclet)
**Status:** ✅ Success

### CellSignalingModes (poclet)
**Status:** ✅ Success

### ColorSynthesis (poclet)
**Status:** ✅ Success

**Modifications:**
- Federated: Found 4 sub-instances
- Federated: M0_RGB_Additive.jsonld → 0 changes
- Federated: M0_HSL_Additive.jsonld → 0 changes
- Federated: M0_CMY_Subtractive.jsonld → 0 changes
- Federated: M0_CMYK_Subtractive.jsonld → 0 changes

### ComplexChemicalSynapse (poclet)
**Status:** ✅ Success

### CounterPoint (poclet)
**Status:** ✅ Success

### ExposureTriangle (poclet)
**Status:** ✅ Success

### FireTriangle (poclet)
**Status:** ✅ Success

### FourStrokeEngine (poclet)
**Status:** ✅ Success

### Kidneys (poclet)
**Status:** ✅ Success

### KindlebergerMinsky (poclet)
**Status:** ✅ Success

### MtgColorWheel (poclet)
**Status:** ✅ Success

### NakamotoConsensus (poclet)
**Status:** ✅ Success

### NuclearReactorsTypology (poclet)
**Status:** ✅ Success

### PhaseTransition (poclet)
**Status:** ✅ Success

### PlateTectonics (poclet)
**Status:** ✅ Success

### Ptoe (poclet)
**Status:** ✅ Success

### Raas (poclet)
**Status:** ✅ Success

### Tpack (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: m3:ontologyType
- @context: Added missing @base (canonical https://raw.githubusercontent.com/...)

### Transistor (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: rdfs:label, rdfs:comment, owl:versionInfo, owl:imports, dcterms:creator, dcterms:created, m3:ontologyType
- JSON-LD: Fixed @type → owl:Ontology

### TrophicPyramid (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: m3:ontologyType

### TvTestPattern (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

### Vco (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: m3:ontologyType

### Yggdrasil (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

### Iching (symbolic_grammar)
**Status:** ❌ Failed

**Modifications:**
- @context: Converted relative URLs to absolute

**Errors:**
- SHACL: SHACL validation failed:
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Message: CRITICAL: m3:ontologyType MUST be one of: m3:Poclet, m3:SystemicFramework, m3:SymbolicSystemGrammar, m3:TscgTool, m3:TransDisclet, m3:Enigma. This is the ONLY valid ontologyType property. Current conformance: 38% poclets (9/24) + 50% others (1/2). 15 poclets + VSM to correct. NEVER use m3:ontologyCategory or m2:ontologyCategory. IMPORTANT: If this validation fails but m3:ontologyType is present, check that 'm3:' namespace in @context uses ABSOLUTE URL (https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#) not relative URL (M3_GenesisGrammar.jsonld#) - pyshacl cannot resolve relative URLs.

## Fixes Applied in v3.0.0

1. ✅ Added missing @base in @context (required for TscgOntologyAPIServer/pyoxigraph)
2. ✅ Migrated M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld throughout
3. ✅ All v2.7.0 features maintained (multi-type support, domain migration)

## Next Steps

1. Review this report
2. Test HTML simulations manually (see TEST_CHECKLIST.md)
3. If issues found, restore from backup
4. Manually add m1:domain values for instances without domain
