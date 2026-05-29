# TSCG Automated Migration Report (v3.0.0 - GenesisGrammar + @base)

**Date:** 2026-05-30 00:00:08
**Backup Location:** E:\_00_Michel\_00_Lab\_00_GitHub\tscg\migration_backups\20260529_235954

## Summary

- ✅ **Successful:** 28
- ❌ **Failed:** 0
- 📊 **Total:** 28

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

### Transistor (poclet)
**Status:** ✅ Success

### TrophicPyramid (poclet)
**Status:** ✅ Success

### TvTestPattern (poclet)
**Status:** ✅ Success

### Vco (poclet)
**Status:** ✅ Success

### Yggdrasil (poclet)
**Status:** ✅ Success

### Iching (symbolic_grammar)
**Status:** ✅ Success

**Modifications:**
- @context: Converted relative URLs to absolute

### Triz (systemic_framework)
**Status:** ✅ Success

**Modifications:**
- @context: Converted relative URLs to absolute

### Vsm (systemic_framework)
**Status:** ✅ Success

**Modifications:**
- @context: Converted relative URLs to absolute

## Fixes Applied in v3.0.0

1. ✅ Added missing @base in @context (required for TscgOntologyAPIServer/pyoxigraph)
2. ✅ Migrated M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld throughout
3. ✅ All v2.7.0 features maintained (multi-type support, domain migration)

## Next Steps

1. Review this report
2. Test HTML simulations manually (see TEST_CHECKLIST.md)
3. If issues found, restore from backup
4. Manually add m1:domain values for instances without domain
