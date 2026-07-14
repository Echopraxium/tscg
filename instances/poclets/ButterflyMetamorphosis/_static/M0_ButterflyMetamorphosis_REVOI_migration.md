# M0_ButterflyMetamorphosis — Migration Patch (ORIVE → REVOI + Structural Grammar)

**Pipeline:** tscg-ontology-diagnosis-pipeline · **Phase:** 2 (execution) → awaiting Phase 4 (your semantic approval)
**Target:** `M0_ButterflyMetamorphosis.jsonld` (currently v1.1.1) → **v1.2.0**
**Status of numeric values:** ⚠️ **PROVISIONAL** (REVOI scores + δ₁ improvised, to refute)

This patch is a reviewable draft. On your approval I generate the full migrated `.jsonld` + README (Phase 5).

---

## 1. Rulings applied (your Phase-4 authority)

| Decision | Ruling |
|----------|--------|
| Sphinx basis | **REVOI = { R, E, V, O, Im }** = Representability · Evolvability · Verifiability · Observability · Interoperability |
| ORIVE Validity / Expressiveness / Reproducibility | **Obsolete** — removed (were never REVOI axes) |
| M2 Switch / Mode / Latency | **Obsolete** |
| M2 Cycle | Not in M2 v16.16.0 → remapped (my call, **to confirm**) |
| Notation | `m0:tensorFormula` (⊗) → `m0:hasStructuralGrammarFormula` (×, \|) |

**Also flagged (M2-side, for when you touch M2 v16.16.0):** `R` is glossed as *Reproducibility* in `bicephalousArchitecture`, `m2:hasEpistemicGap`, and the ontology `rdfs:comment` — residue to clean; the correct gloss is **Representability**.

---

## 2. Header node — field changes (`m0:ButterflyMetamorphosis:ButterflyMetamorphosis`)

```diff
- "owl:versionInfo": "1.1.1",
+ "owl:versionInfo": "1.2.0",
- "m0:oriveMean": 0.88,
+ "m0:revoiMean": 0.84,
- "m0:epistemicGap": 0.25,
+ "m0:epistemicGap": 0.22,
- "dcterms:modified": "2026-04-20",
+ "dcterms:modified": "2026-07-07",
```

Prepend to `m2:changelog`:

```json
{
  "version": "1.2.0",
  "date": "2026-07-07",
  "changes": "MIGRATION: ORIVE -> REVOI (R/E/V/O/Im per M2 v16.16.0). Obsolete axes (Validity, Expressiveness, Reproducibility) removed; Sphinx scores re-derived (PROVISIONAL). M2 activation set updated: Switch/Mode/Cycle/Latency retired; added Behavior, Step, Stase, Potentialization. tensorFormula (⊗) -> hasStructuralGrammarFormula (×, |)."
}
```

---

## 3. REVOI analysis — replace the whole ORIVE block

Rename the class node:

```diff
- "@id": "m0:ORIVEAnalysis", "rdfs:label": "ORIVE Analysis (Sphinx Eye - Map Perspective)",
- "rdfs:comment": "Five-dimensional evaluation of conceptual model quality: Observability, Reproducibility, Interoperability, Validity, Expressiveness."
+ "@id": "m0:REVOIAnalysis", "rdfs:label": "REVOI Analysis (Sphinx Eye - Map Perspective)",
+ "rdfs:comment": "Five-dimensional evaluation of Map quality: Representability, Evolvability, Verifiability, Observability, Interoperability (M2 v16.16.0)."
```

Replace the five `m0:orive_*` nodes with these five (⚠️ scores provisional):

```json
{ "@id": "m0:revoi_representability", "@type": ["m0:REVOIAnalysis"], "rdfs:label": "Representability (R)",
  "m0:score": 0.90, "m0:dominantM3": "m3:sphinx_eye:Representability",
  "rdfs:comment": "The 6-pole model is elegantly encodable/nameable: established terminology (instar, ecdysis, eclosion), canonical diagrams, formal lifecycle notation. High semantic decodability." },

{ "@id": "m0:revoi_evolvability", "@type": ["m0:REVOIAnalysis"], "rdfs:label": "Evolvability (E)",
  "m0:score": 0.74, "m0:dominantM3": "m3:sphinx_eye:Evolvability",
  "rdfs:comment": "The model is a settled paradigm; moderate capacity to reconfigure as molecular/evo-devo observations accumulate (histogenesis detail, holometaboly origin still refine it)." },

{ "@id": "m0:revoi_verifiability", "@type": ["m0:REVOIAnalysis"], "rdfs:label": "Verifiability (V)",
  "m0:score": 0.92, "m0:dominantM3": "m3:sphinx_eye:Verifiability",
  "rdfs:comment": "Strongly testable against Territory: hormonal manipulations (JH analogs), imaginal-disc fate maps, temperature/emergence timing models yield falsifiable predictions. (Inherits the strength formerly mislabelled 'Validity'.)" },

{ "@id": "m0:revoi_observability", "@type": ["m0:REVOIAnalysis"], "rdfs:label": "Observability (O)",
  "m0:score": 0.85, "m0:dominantM3": "m3:sphinx_eye:Observability",
  "rdfs:comment": "External morphology and behaviour directly observable across all poles; internal reorganization (hormone titres, disc activity, gene expression) requires instrumentation." },

{ "@id": "m0:revoi_interoperability", "@type": ["m0:REVOIAnalysis"], "rdfs:label": "Interoperability (Im)",
  "m0:score": 0.78, "m0:dominantM3": "m3:sphinx_eye:Interoperability",
  "rdfs:comment": "Strong integration within life sciences (evo-devo, endocrinology, cell biology, ecology); moderate beyond (systems biology, biomechanics); low with quantum biology / cosmology." }
```

---

## 4. M2 GenericConcept activation — remap

**Remove** nodes: `m0:m2_switch`, `m0:m2_mode`, `m0:m2_cycle`, `m0:m2_latency`.
**Keep & convert** (drop `m0:tensorFormula`, add `m0:hasStructuralGrammarFormula`):

| Node | dominance | `m0:hasStructuralGrammarFormula` |
|------|-----------|----------------------------------|
| m2_transformation | 0.96 | `D × S × I` |
| m2_emergence | 0.94 | `I × S × D` |
| m2_regulation | 0.93 | `A × S × F` |
| m2_threshold | 0.89 | `A × I` |
| m2_layer | 0.87 | `St × It × A \| R` |
| m2_memory | 0.75 | `∫(D−F)dτ` |

**Add** four nodes (all present in M2 v16.16.0):

```json
{ "@id": "m0:m2_behavior", "@type": ["m0:M2GenericConceptActivation"],
  "m0:GenericConcept": "m2:Behavior", "m0:dominance": 0.92,
  "rdfs:comment": "The lifecycle as an ordered network of Steps (6 poles). M2 v16.16.0 discoveryContext explicitly cites butterfly metamorphosis. Replaces Mode (the 6 discrete operational states).",
  "m0:hasStructuralGrammarFormula": "S × D × F" },

{ "@id": "m0:m2_step", "@type": ["m0:M2GenericConceptActivation"],
  "m0:GenericConcept": "m2:Step", "m0:dominance": 0.86,
  "rdfs:comment": "Each pole is a Step (Node specialized for sequential context). M2 v16.16.0 example: 'Butterfly egg stage'. The inter-Step transitions absorb the former Switch semantics (with Threshold).",
  "m0:hasStructuralGrammarFormula": "S × I × D" },

{ "@id": "m0:m2_stase", "@type": ["m0:M2GenericConceptActivation"],
  "m0:GenericConcept": "m2:Stase", "m0:dominance": 0.82,
  "rdfs:comment": "Imaginal discs as F=0 dormant potential, reversible (S × A, D absent = reversible by construction). Replaces the retired candidate 'Latency' — dormancy half.",
  "m0:hasStructuralGrammarFormula": "S × A" },

{ "@id": "m0:m2_potentialization", "@type": ["m0:M2GenericConceptActivation"],
  "m0:GenericConcept": "m2:Potentialization", "m0:dominance": 0.80,
  "rdfs:comment": "Activation of dormant imaginal discs at emergence: F=0 -> F_active. Replaces the retired candidate 'Latency' — activation half.",
  "m0:hasStructuralGrammarFormula": "A × D × F | _^" }
```

**Retirement note (Latency):** the candidate is not lost but *absorbed* — its two semantic halves (dormancy / activation) are now covered by the existing pair **Stase** + **Potentialization** in M2 v16.16.0. No new M2 candidate needed.

---

## 5. Bicephalous synthesis — update

```diff
- "m0:mapStrength": 0.88,
+ "m0:mapStrength": 0.84,
- "m0:epistemicGap": 0.25,
+ "m0:epistemicGap": 0.22,
```

`m0:keyCouplings` referenced old-ORIVE letters (S⊗R = "Structural reproducibility", etc.). Re-derived onto REVOI (⊗ → ×, provisional):

```json
"m0:keyCouplings": [
  "S × R: 0.92 (structure is highly representable)",
  "I × V: 0.92 (information basis is verifiable)",
  "S × O: 0.90 (structural states observable)",
  "D × E: 0.74 (temporal model moderately evolvable)",
  "I × Im: 0.78 (informational cross-domain interoperability)"
]
```

---

## 6. validation_result — contributions

```diff
- "M2_validation": ["Transformation","Emergence","Mode","Switch","Layer","Cycle","Regulation"],
- "M2_candidates": ["Latency"],
+ "M2_validation": ["Transformation","Emergence","Regulation","Threshold","Layer","Behavior","Step","Memory"],
+ "M2_reused_from_v16_16_0": ["Stase","Potentialization"],
+ "M2_candidates": [],
+ "M2_retired": ["Switch","Mode","Cycle","Latency (absorbed by Stase + Potentialization)"],
```

Update `m0:overallStatus`: `"... (ASFID: 0.95, ORIVE: 0.88)"` → `"... (ASFID: 0.95, REVOI: 0.84 provisional)"`.

---

## 7. Phase 3 (to run in your repo — I cannot here)

```bash
python cli-tools/ontology-linter/ontology_linter.py <M0 file> --strict
python cli-tools/owl_reasoning_test/rdfs_diagnostic.py
python cli-tools/owl_reasoning_test/test_owl_reasoning.py
shacl validate --shapes ontology/TSCG_Grammar/M0_*_Schema.ttl --data <M0 file>
```

I ran only a JSON-syntax check on the equivalent sim data. The linter / Pellet / SHACL gates remain yours.
