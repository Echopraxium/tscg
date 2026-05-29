# TSCG Automated Migration Report (v3.0.0 - GenesisGrammar + @base)

**Date:** 2026-05-29 18:52:19
**Backup Location:** E:\_00_Michel\_00_Lab\_00_GitHub\tscg\migration_backups\20260529_185213

## Summary

- ✅ **Successful:** 8
- ❌ **Failed:** 1
- 📊 **Total:** 9

## Detailed Results

### AdaptativeImmuneResponse (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- JSON-LD: Fixed @type → owl:Ontology

### BloodPressureControl (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

### ButterflyMetamorphosis (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- JSON-LD: Fixed @type → owl:Ontology

### CellSignalingModes (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

### ColorSynthesis (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- @context: Added missing @base (canonical https://raw.githubusercontent.com/...)
- Federated: Found 4 sub-instances
- Federated: M0_RGB_Additive.jsonld → 2 changes
- Federated: M0_HSL_Additive.jsonld → 2 changes
- Federated: M0_CMY_Subtractive.jsonld → 2 changes
- Federated: M0_CMYK_Subtractive.jsonld → 2 changes

### ComplexChemicalSynapse (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- @context: Added missing @base (canonical https://raw.githubusercontent.com/...)

### CounterPoint (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

### ExposureTriangle (poclet)
**Status:** ✅ Success

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- @context: Added missing @base (canonical https://raw.githubusercontent.com/...)

### FireTriangle (poclet)
**Status:** ❌ Failed

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld
- @context: Added missing @base (canonical https://raw.githubusercontent.com/...)

## Fixes Applied in v3.0.0

1. ✅ Added missing @base in @context (required for TscgOntologyAPIServer/pyoxigraph)
2. ✅ Migrated M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld throughout
3. ✅ All v2.7.0 features maintained (multi-type support, domain migration)

## Next Steps

1. Review this report
2. Test HTML simulations manually (see TEST_CHECKLIST.md)
3. If issues found, restore from backup
4. Manually add m1:domain values for instances without domain
