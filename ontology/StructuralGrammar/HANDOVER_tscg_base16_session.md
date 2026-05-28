# TSCG Session Handover — Base16 Grammar Extension & Hexagonal Grid Visualization

**Date:** 2026-05-27  
**Author:** Echopraxium with the collaboration of Claude AI  
**Project:** TSCG (Transdisciplinary System Construction Game) — https://github.com/Echopraxium/tscg

---

## 1. What Was Accomplished

### 1.1 Theoretical Work — Gs Grammar Extended to Base16

The TSCG foundational alphabet `𝕋₀` was extended from **13 primitives** (5+5+3) to **16 primitives** (5+5+6), establishing the **Base16** canonical form.

**Three new primitives added to `𝕋₀(|)` (Gs — Stereopsis grammar):**

| Index | Symbol | Name | Answers | Theoretical Basis |
|-------|--------|------|---------|-------------------|
| 4 | **K** | Knowledge | "What?" | Cognitive interface — contextualisation of `It` into meaning |
| 5 | **Ss** | Symbol | "Sign?" | Semiotic interface — signifier (Gt) ↔ signified (Gm). Peircean sign. Note: `Ss` notation (not `S`) avoids collision with `St` (Structure/Gt) in hybrid formulas |
| 6 | **L** | Localizability | "Converging?" | Cybernetic interface — discriminates direction of convergence toward `A` by successive state comparison. Ordinal, no metric. Based on Wiener (1948) / Ashby (1956) |

**Final alphabet — 𝕋₀ = Base16:**
```
𝕋₀(×) = {A, St, F, It, D}         5 primitives  Territory (Gt)
𝕋₀(+) = {R, E, V, Ot, Im}         5 primitives  Map (Gm)
𝕋₀(|) = {T, _^, _$, K, Ss, L}     6 primitives  Stereopsis (Gs)
Total: 16 primitives — Base16
```

**Why 5-5-6 asymmetry?** Gs is the inter-grammar axis by nature; the 6th primitive (`L`) encodes the convergence discrimination that requires both Gt and Gm to make sense. The asymmetry is semantically justified.

**Four transcendental questions** of Territory/Map correspondence:
- `T` = When?  
- `K` = What?  
- `Ss` = Sign?  
- `L` = Converging?

**Irreducibility validation:** All three new primitives passed the standard TSCG test (validated across ≥6 unrelated domains).

---

### 1.2 M2 Collision Resolution

Before the extension, 12 concepts shared the formula `S×I` — a collision that undermined semantic precision. The new primitives resolve virtually all collisions in M2 and M1_CoreConcepts.

**Resolutions validated for the [S×I] group (12 concepts):**

| Concept | New Formula |
|---------|-------------|
| Code | `It×Ss` |
| Signature | `It×Ss\|V` |
| Language | `Ss×F\|K` |
| Role | `Ss\|K` |
| Relation | `St×Ss` |
| Channel | `St×F\|Ss` |
| Node/Component | `St×It\|L` |
| Topology/Space/Capacity/Constraint | `St\|L` or `St×It\|L` |
| Homeostasis | `A×St×F\|L` |
| Bifurcation | `D×F\|L` |
| Agent | `St×It×D\|K` |
| Pattern | `St×It×A\|K` |
| Mediator | `F×It\|K` |

**⚠️ PENDING:** Remaining M2/M1_Core formula re-evaluation groups not yet processed:
- `[A×I×S]`, `[D×I×S]`, `[F×I×S]`, `[A×F×S]`, `[D×F]`, `[A×S]`, `[D×F×I]`

---

### 1.3 Ontology Files Updated

#### `M3_BicephalousPerspective.jsonld` → v1.2.0
**Delivered:** `/mnt/user-data/outputs/M3_BicephalousPerspective.jsonld`

Changes:
- 3 new nodes: `typeK` (idx 4), `typeSs` (idx 5), `typeL` (idx 6)
- `grammar_properties` updated to reflect 16-primitive alphabet
- `transcendental_questions` map: `{T: "When?", K: "What?", Ss: "Sign?", L: "Converging?"}`
- Independence declaration for new primitives
- Cybernetic foundation for `L` citing Wiener 1948 + Ashby 1956
- Changelog entry: v1.2.0

#### `M3_GrammarFoundation.jsonld` → v2.2.0
**Delivered:** `/mnt/user-data/outputs/M3_GrammarFoundation.jsonld`

Changes:
- `three_alphabets.stereopsis` updated (6 primitives)
- `TypeSystem T0` cardinality: 13 → **16** (Base16)
- `MonoidalType` comment updated
- Changelog entry: v2.2.0

**⚠️ STILL NEEDED:**
- `M2_GenericConcepts.jsonld` — formulas for the resolved concepts not yet written
- `M1_CoreConcepts.jsonld` — same
- St/Ot notation convention (9 hybrid formulas affected across corpus — `St` and `Ot` must be indexed in hybrid formulas to avoid collision with `Ss`)

---

### 1.4 Visualization — `tscg_base16_grid.html`

**Delivered:** `/mnt/user-data/outputs/tscg_base16_grid.html`

An interactive 3D visualization of the 16 TSCG primitives using **Three.js r128** (fully inlined, no CDN dependency).

**Architecture:**
- Three.js r128 + OrbitControls: fully inlined from npm package at `/home/claude/package/`
- 16 hexagons (pointy-top), each in its own repositionable Group
- Grammar color coding:
  - `Gt` = blue `#2E86C1`
  - `Gm` = green `#27AE60`
  - `Gs` = orange `#D35400`

**Features:**
- **3 Layout modes** (animated 700ms easeInOut transitions):
  1. **Entrelacé** — interlaced 4×4 hex grid (Gt/Gm interleaved, Gs interspersed)
  2. **Rangées** — rows by grammar (Gt+Gm center rows, Gs in lateral columns)
  3. **Axial** — triangle clusters (Gt trapeze top-left, Gm trapeze top-right, Gs rectangle bottom-center)
- **3 Formula overlays** with colored Bézier tube arcs + operator sprites:
  - Coherence: `A × St × It | R + Ot`
  - Layer: `St × It × A | R`
  - Amplification: `F × It × D | R + Ot`
- Dynamic BufferGeometry connections (update on layout animation)
- CanvasTexture labels with symbol + grammar badge
- Touch support (tap vs drag detection)
- Bottom sheet info panel on hex tap
- Tab bar (formula selector)
- Legend toggle button
- Camera view buttons: ⊞ (front) / ⊤ (top) with easeInOut animation
- ResizeObserver for canvas

---

## 2. Recurring Bug — `THREE is not defined`

**Symptom:** `Uncaught ReferenceError: THREE is not defined` at runtime.

**Root cause history:**
1. First occurrence: `<script src>` CDN tags were still present alongside the dynamic loader → race condition. **Fix:** removed `<script src>` tags.
2. Second occurrence: `tryLoad(0)` was called before `function init()` was parsed — appeared to be a hoisting issue. **Fix:** simplified startup to direct `init()` call at end of script.
3. Third (current) occurrence: Three.js UMD bundle uses `!function(t,e){...}(this, factory)` — in some browser contexts `this` at the top of a `<script>` block is not reliably `window`. **Fix applied:** inserted a safety net line after the Three.js bundle and before OrbitControls:
   ```js
   if(typeof window!=="undefined"&&!window.THREE&&typeof THREE!=="undefined"){window.THREE=THREE;}
   ```

**Current file state:** The safety net has been applied. The file should be tested at `127.0.0.1:8080` to confirm resolution.

**If the bug persists**, the next diagnostic step is to wrap the Three.js UMD call explicitly:
```html
<script>
// Force global assignment
window.THREE = window.THREE || {};
// ... Three.js UMD bundle here, modified to target window explicitly ...
</script>
```
Or better: use the ES module build of Three.js r128 and import it as a module.

---

## 3. Files Delivered This Session

| File | Location | Status |
|------|----------|--------|
| `M3_BicephalousPerspective.jsonld` v1.2.0 | `/mnt/user-data/outputs/` | ✅ Complete |
| `M3_GrammarFoundation.jsonld` v2.2.0 | `/mnt/user-data/outputs/` | ✅ Complete |
| `tscg_base16_grid.html` | `/mnt/user-data/outputs/` | ⚠️ THREE bug persists — needs local test |
| This handover document | `/home/claude/HANDOVER_tscg_base16_session.md` | ✅ |

---

## 4. Pending Work (Priority Order)

### Immediate
1. **Test `tscg_base16_grid.html` locally** at `127.0.0.1:8080` to confirm the THREE safety net resolves the bug. If not, investigate the UMD `this` binding issue.

### Short-term
2. **Update `M2_GenericConcepts.jsonld`** with new formulas for all resolved collision concepts (use the table in §1.2 above as source).
3. **Update `M1_CoreConcepts.jsonld`** with same formulas where applicable.
4. **Apply St/Ot notation convention** across corpus — 9 hybrid formulas need `St` → `St` (indexed) and `Ot` → `Ot` (indexed) to avoid collision with `Ss` in formula strings.
5. **Continue M2 collision resolution** for remaining groups: `[A×I×S]`, `[D×I×S]`, `[F×I×S]`, `[A×F×S]`, `[D×F]`, `[A×S]`, `[D×F×I]`.

### Medium-term
6. **SHACL realignment** — `M0_Instances_Schema.shacl.ttl` partially updated; estimated 10–12h total work remaining.
7. **Zenodo v4.0 preprint** — article drafted at ~11,300 words; v3.0 DOI `10.5281/zenodo.18471860` active. Integrate Base16 findings into the article.
8. **Corpus realignment tracker** — remaining M0 instances need `@type: owl:Ontology`, correct `m3:ontologyType`, REVOI terminology, and short-key ASFID/REVOI aliases in `@context`.

---

## 5. Key Technical Notes

### Three.js Inline Workflow
- Source files at: `/home/claude/package/build/three.min.js` and `/home/claude/package/examples/js/controls/OrbitControls.js`
- These were obtained via `npm pack three@0.128.0` in a previous session
- **Always inline** — CDNs are blocked in the Claude container environment
- CDN URL that works in production (outside container): `unpkg.com/babylonjs@6.26.0/babylon.js` (for BabylonJS productions), NOT `cdn.babylonjs.com`

### Notation Convention for Hybrid Formulas
- When `St` (Structure, Gt) and `Ss` (Symbol, Gs) both appear in a formula, use subscript notation: `Stᴳᵗ` or simply keep as `St` (it's already differentiated by convention)
- The key rule: in formula strings, `S` alone is ambiguous → always write `St` or `Ss`

### Base16 Algebra
- The extension is a **free monoidal extension** — algebraically sound
- The 3 new primitives are independent (no derivability from existing primitives)
- `L` was originally considered as "Groundedness" or "Origin" — both were rejected (Groundedness risks Hilbert-space trap; Origin suggests metric/spatial notion). **"Localizability"** was chosen as the correct name: ordinal convergence discrimination without metric assumptions.

---

## 6. Repository Context

```
Local path:   E:\_00_Michel\_00_Lab\_00_GitHub\tscg\
GitHub:       https://github.com/Echopraxium/tscg
Base URI:     https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/
```

**Relevant files in repo:**
- `ontology/M3_BicephalousPerspective.jsonld` — needs update from delivered v1.2.0
- `ontology/M3_GrammarFoundation.jsonld` — needs update from delivered v2.2.0
- `ontology/M2_GenericConcepts.jsonld` — v15.10.1 (formulas for new concepts pending)
- `ontology/M1_CoreConcepts.jsonld` — v2.1.0 (formulas pending)
- `instances/` — TSCG instance simulations

---

*Handover generated by Claude AI (Sonnet 4.6) — 2026-05-27*
