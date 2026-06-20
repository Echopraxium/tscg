# TSCG M0 Migration Report — v1.5.0

**Date:** 2026-06-20 16:53:40
**Summary:** ✅ 1 success  ❌ 0 failed  📊 1 total

---

## Changes applied

- `m0:` → `M0_Common.jsonld#` (shared canonical)
- `m0.<instance>:` added (local namespace)
- `m1.extensions.<domain>:` (canonical dot-separated)
- Obsolete score aliases removed (A_score...)
- `owl:imports M0_Common.jsonld` added
- Score values → bare numerics
- Enum values → IRI objects (`{@id: m0:spectralClass.Coherent}`)
- `m2:hasTensorFormula` → `m2:hasStructuralGrammarFormula`
- `m3:ontologyType` removed from sub-nodes
- `m2:changelog` truncated to 3 entries

---

## Detailed Results

### HSL_Additive (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: Added m0.hslAdditive:

