# TSCG Automated Migration Report (v3.0.0 - GenesisGrammar + @base)

**Date:** 2026-05-29 19:58:40
**Backup Location:** E:\_00_Michel\_00_Lab\_00_GitHub\tscg\migration_backups\20260529_195831

## Summary

- ✅ **Successful:** 19
- ❌ **Failed:** 1
- 📊 **Total:** 20

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

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: m3:ontologyType

### Kidneys (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: rdfs:label, rdfs:comment, owl:versionInfo, owl:imports, dcterms:creator, dcterms:created, m3:ontologyType
- JSON-LD: Fixed @type → owl:Ontology

### KindlebergerMinsky (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: m3:ontologyType

### MtgColorWheel (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: m3:ontologyType

### NakamotoConsensus (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

### NuclearReactorsTypology (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- JSON-LD: Fixed @type → owl:Ontology

### PhaseTransition (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: m3:ontologyType

### PlateTectonics (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

### Ptoe (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

### Raas (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- Removed stray root-level properties: m3:ontologyType
- JSON-LD: Fixed @type → owl:Ontology

### Theremin (poclet)
**Status:** ❌ Failed

**Errors:**
- JSON-LD not found: E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\poclets\Theremin\M0_Theremin.jsonld

## Fixes Applied in v3.0.0

1. ✅ Added missing @base in @context (required for TscgOntologyAPIServer/pyoxigraph)
2. ✅ Migrated M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld throughout
3. ✅ All v2.7.0 features maintained (multi-type support, domain migration)

## Next Steps

1. Review this report
2. Test HTML simulations manually (see TEST_CHECKLIST.md)
3. If issues found, restore from backup
4. Manually add m1:domain values for instances without domain
