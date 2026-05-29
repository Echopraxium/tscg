# TSCG Automated Migration Report (v3.0.0 - GenesisGrammar + @base)

**Date:** 2026-05-29 18:45:36
**Backup Location:** E:\_00_Michel\_00_Lab\_00_GitHub\tscg\migration_backups\20260529_184531

## Summary

- ✅ **Successful:** 0
- ❌ **Failed:** 1
- 📊 **Total:** 1

## Detailed Results

### AdaptativeImmuneResponse (poclet)
**Status:** ❌ Failed

**Modifications:**
- JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld

## Fixes Applied in v3.0.0

1. ✅ Added missing @base in @context (required for TscgOntologyAPIServer/pyoxigraph)
2. ✅ Migrated M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld throughout
3. ✅ All v2.7.0 features maintained (multi-type support, domain migration)

## Next Steps

1. Review this report
2. Test HTML simulations manually (see TEST_CHECKLIST.md)
3. If issues found, restore from backup
4. Manually add m1:domain values for instances without domain
