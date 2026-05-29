# TSCG Automated Migration Report (v3.0.0 - GenesisGrammar + @base)

**Date:** 2026-05-29 18:58:22
**Backup Location:** E:\_00_Michel\_00_Lab\_00_GitHub\tscg\migration_backups\20260529_185817

## Summary

- ✅ **Successful:** 8
- ❌ **Failed:** 1
- 📊 **Total:** 9

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
**Status:** ❌ Failed

**Errors:**
- SHACL: SHACL validation failed:
Constraint Violation in NodeConstraintComponent (http://www.w3.org/ns/shacl#NodeConstraintComponent):
	Message: m0:asfidScores is recommended for poclets (50% have scores) - detailed ASFID scoring. Also applicable to other instance types.
		Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):

## Fixes Applied in v3.0.0

1. ✅ Added missing @base in @context (required for TscgOntologyAPIServer/pyoxigraph)
2. ✅ Migrated M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld throughout
3. ✅ All v2.7.0 features maintained (multi-type support, domain migration)

## Next Steps

1. Review this report
2. Test HTML simulations manually (see TEST_CHECKLIST.md)
3. If issues found, restore from backup
4. Manually add m1:domain values for instances without domain
