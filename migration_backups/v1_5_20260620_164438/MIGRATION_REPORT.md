# TSCG M0 Migration Report — v1.5.0

**Date:** 2026-06-20 16:45:00
**Summary:** ✅ 36 success  ❌ 0 failed  📊 36 total

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

### AdaptativeImmuneResponse (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### BloodPressureControl (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### ButterflyMetamorphosis (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### CellSignalingModes (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### CMY_Subtractive (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.cMY_Subtractive:
- @context: Removed legacy entry 'm0:color_synthesis'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- @context: Removed obsolete alias 'D_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### CMYK_Subtractive (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.cMYK_Subtractive:
- @context: Removed legacy entry 'm0:color_synthesis'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- @context: Removed obsolete alias 'D_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### ColorSynthesis (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### HSL_Additive (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.hSL_Additive:
- @context: Removed legacy entry 'm0:color_synthesis'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- @context: Removed obsolete alias 'D_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### RGB_Additive (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.rGB_Additive:
- @context: Removed legacy entry 'm0:color_synthesis'
- @context: Removed obsolete alias 'F_score'
- @context: Removed obsolete alias 'E_score'
- @context: Removed obsolete alias 'O_score'
- @context: Removed obsolete alias 'S_score'
- @context: Removed obsolete alias 'V_score'
- @context: Removed obsolete alias 'Im_score'
- @context: Removed obsolete alias 'A_score'
- @context: Removed obsolete alias 'It_score'
- @context: Removed obsolete alias 'R_score'
- @context: Removed obsolete alias 'D_score'
- owl:imports: Added M0_Common.jsonld
- Bare numerics: 1 score(s) converted

### ComplexChemicalSynapse (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Counterpoint (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: Added m0.counterpoint:

### ExposureTriangle (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### FireTriangle (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### FourStrokeEngine (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Kidneys (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### KindlebergerMinsky (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### MtgColorWheel (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### NakamotoConsensus (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### NuclearReactorsTypology (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### PhaseTransition (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### PlateTectonics (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Ptoe (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Raas (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Tpack (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Transistor (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### TrophicPyramid (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### TvTestPattern (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Vco (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Yggdrasil (poclet)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Triz (systemic_framework)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### Triz_Examples (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

**Modifications:**
- @context: m0: added → M0_Common.jsonld#
- @context: Added m0.triz_Examples:
- @context: Added missing m3:
- @context: Added missing rdf:
- @context: Added missing rdfs:
- @context: Added missing owl:
- @context: Added missing xsd:
- @context: Added missing dcterms:
- @context: Added missing skos:
- @context: Added @base
- owl:imports: Added M0_Common.jsonld

### Vsm (systemic_framework)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### TscgOntologyAPIServer (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### TscgOntologyExplorer (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### TscgPocletGenerator (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

### TscgPocletMiner (tscg_tool)
**Status:** ✅ Success  |  **SHACL:** ✅ PASS

