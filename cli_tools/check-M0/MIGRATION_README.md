# TSCG M0 Migration Guide — v1.5.0

**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-06-20  
**Location:** `cli_tools/check-M0/`

---

## Overview

This guide documents the migration of all TSCG M0 instance files (`M0_*.jsonld`) from
legacy namespace conventions to the **v1.5 canonical architecture** introduced on 2026-06-19.

The central change is the creation of `ontology/M0_Common.jsonld` as the **single source
of truth** for all shared M0 properties (scores, epistemic gap, focal score, enum types).
This replaces the phantom `M0_Poclet#` target that each instance was previously forced to
re-declare independently.

---

## Files in this directory

| File | Purpose |
|---|---|
| `migrate_m0_to_v1_5.py` | Migration script — applies all v1.5 transformations |
| `check_m0_instances_v1_5.py` | Checker script — diagnoses v1.5 compliance (15 checks) |
| `M0_Instances_Schema_shacl_v1.5.ttl` | SHACL grammar — formal validation schema |
| `MIGRATION_README.md` | This file |

---

## What changed in v1.5

### 1. Namespace split: `m0:` is now shared, not local

**Before (legacy):** each instance declared `m0:` pointing to *itself*.

```json
"@context": {
  "m0": "https://.../instances/poclets/FireTriangle/M0_FireTriangle.jsonld#"
}
```

This caused 320+ redundant property re-declarations across the corpus
(every instance re-defined `A_score`, `S_score`, etc. locally).

**After (v1.5):** `m0:` points to the shared vocabulary; a new
`m0.<instance>:` alias points to the instance itself.

```json
"@context": {
  "m0":            "https://.../ontology/M0_Common.jsonld#",
  "m0.fireTriangle": "https://.../instances/poclets/FireTriangle/M0_FireTriangle.jsonld#"
}
```

### 2. `owl:imports M0_Common.jsonld`

All instances must declare the import so OWL reasoners inherit the shared
property definitions:

```json
"owl:imports": [
  "M3_GenesisGrammar.jsonld",
  "M2_GenericConcepts.jsonld",
  "M1_CoreConcepts.jsonld",
  "M0_Common.jsonld"
]
```

### 3. Score values: bare numerics

**Before:**
```json
"A_score": {"@value": "0.85", "@type": "xsd:float"}
```

**After:**
```json
"m0:scoreA": 0.85
```

The `rdfs:range xsd:float` declaration in `M0_Common.jsonld` makes the
`@type` annotation redundant. Bare numerics are cleaner and avoid
pyshacl parsing issues.

### 4. Enum values: IRI objects (not strings)

**Before:**
```json
"m0:spectralClass": "Coherent"
```

**After:**
```json
"m0:spectralClass": {"@id": "m0:spectralClass.Coherent"}
```

Naming convention: `m0:<propertyName>.<ValuePascalCase>`

| Property | Example IRI value |
|---|---|
| `m0:spectralClass` | `m0:spectralClass.Coherent` / `m0:spectralClass.OnCriticalLine` |
| `m0:focalClass` | `m0:focalClass.Emmetropic` / `m0:focalClass.SlightlyHyperopic` |
| `m0:scoringStatus` | `m0:scoringStatus.Complete` / `m0:scoringStatus.Partial` |

### 5. M1 extension alias pattern

**Before (multiple inconsistent variants):**
```json
"m1bio":        "M1_extensions/biology/M1_Biology.jsonld#",
"m1.ext:biology": "...",
"m1core":       "https://.../M1_CoreConcepts.jsonld#"
```

**After (canonical dot-separated):**
```json
"m1.extensions.biology": "https://.../ontology/M1_extensions/biology/M1_Biology.jsonld#"
```

The `m1:` alias (→ `M1_CoreConcepts.jsonld#`) remains unchanged.

### 6. `m2:hasStructuralGrammarFormula` (replaces `hasTensorFormula`)

All occurrences of `m2:hasTensorFormula` anywhere in `@graph` must be
renamed to `m2:hasStructuralGrammarFormula`. This reflects the migration
from Hilbert-space tensor product notation to the Lambek calculus /
Structural Grammar formalism.

### 7. `m3:ontologyType` restricted to `@graph[0]`

`m3:ontologyType` is a metadata property of the ontology node only.
It must not appear in domain sub-nodes (`@graph[1+]`).

### 8. Obsolete aliases removed

The following `@context` aliases are **forbidden** in v1.5:

| Alias | Replaced by |
|---|---|
| `A_score` … `Im_score` | `m0:scoreA` … `m0:scoreIm` (from `M0_Common.jsonld`) |
| `m1core` | `m1:` |
| `sm` | removed (no replacement needed) |
| `m0bmc:`, `m0vsm:` | `m0.bmc:`, `m0.vsm:` (dot separator) |

---

## Canonical `@context` template

Copy this block into any v1.5-compliant M0 instance. Replace
`<instanceName>`, `<instanceType>`, `<InstanceName>`, and
`<domain>` with actual values.

```json
{
  "@context": {
    "@base":   "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
    "m0":      "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Common.jsonld#",
    "m0.<instanceName>": "https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/<instanceType>/<InstanceName>/M0_<InstanceName>.jsonld#",
    "m1":      "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m1.extensions.<domain>": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/<domain>/M1_<Domain>.jsonld#",
    "m2":      "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#",
    "m3":      "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#",
    "rdf":     "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs":    "http://www.w3.org/2000/01/rdf-schema#",
    "owl":     "http://www.w3.org/2002/07/owl#",
    "xsd":     "http://www.w3.org/2001/XMLSchema#",
    "dcterms": "http://purl.org/dc/terms/",
    "skos":    "http://www.w3.org/2004/02/skos/core#"
  }
}
```

---

## Migration workflow

### Step 0 — Verify the checker first (non-destructive)

```bash
cd cli_tools/check-M0

# Check all instances — summary table
python check_m0_instances_v1_5.py

# Check one instance only
python check_m0_instances_v1_5.py --instance FireTriangle

# Full detail with score values
python check_m0_instances_v1_5.py --verbose --scores

# Only show instances with failures
python check_m0_instances_v1_5.py --fails

# Save a JSON report
python check_m0_instances_v1_5.py --json check_report.json
```

### Step 1 — Dry-run the migration

```bash
# Simulate full corpus — no files modified
python migrate_m0_to_v1_5.py --dry-run

# Simulate one instance only
python migrate_m0_to_v1_5.py --dry-run --instance FireTriangle
```

Review the console output. Each instance shows the list of changes
that would be applied. Instances already compliant print `✅ already v1.5 compliant`.

### Step 2 — Apply migration

```bash
# Full corpus (prompts for confirmation)
python migrate_m0_to_v1_5.py

# One instance (no confirmation prompt)
python migrate_m0_to_v1_5.py --instance FireTriangle

# Continue past failures (useful when some instances need manual fixes)
python migrate_m0_to_v1_5.py --continue-on-error
```

Backups are created automatically in:
```
migration_backups/v1_5_<YYYYMMDD_HHMMSS>/<InstanceName>/M0_<Name>.jsonld
```

If SHACL validation fails after migration, the original file is **automatically
restored from backup** before the script stops.

### Step 3 — Validate

```bash
# Re-run checker after migration — should show all PASS
python check_m0_instances_v1_5.py

# Or run SHACL directly via pyshacl
pyshacl -s M0_Instances_Schema_shacl_v1.5.ttl -df json-ld \
  ../../../instances/poclets/FireTriangle/M0_FireTriangle.jsonld
```

### Step 4 — Manual fixes for complex instances

Some instances may need manual intervention before or after the automated
migration. See the `PENDING_SCORES_README.md` for the full inventory.

Known cases requiring manual work:

| Instance | Issue |
|---|---|
| `NakamotoConsensus` | References `M0_Poclets.jsonld` (wrong source file) |
| `BloodPressureControl` | 141 `tscg:` → `m0:` replacements (complex graph) |
| `ButterflyMetamorphosis` | Custom classes that conflict with v1.5 type system |
| `CellSignalingModes` | Inline component extraction needed |

---

## Checker reference (C01–C15)

| Code | Check | Severity |
|---|---|---|
| C01 | `@base` present and canonical | FAIL |
| C02 | `m0:` resolves to `M0_Common.jsonld#` | FAIL |
| C03 | `m0.<instance>:` local alias present | FAIL |
| C04 | `m1:` is an absolute URL | FAIL |
| C05 | `m2:` is an absolute URL | FAIL |
| C06 | `m3:` is an absolute URL | FAIL |
| C07 | No obsolete aliases (`A_score`…`Im_score`, `m1core`, `sm`) | FAIL |
| C08 | `m1.extensions.<domain>:` pattern (no old `m1bio:` etc.) | FAIL |
| C09 | `owl:imports` includes `M0_Common.jsonld` | FAIL |
| C10 | Score values are bare numerics | FAIL |
| C11 | Enum values are IRI objects | FAIL |
| C12 | `m2:hasTensorFormula` absent (all nodes) | FAIL |
| C13 | `m3:ontologyType` only in `@graph[0]` | FAIL |
| C14 | `m2:changelog` ≤ 3 entries | FAIL |
| C15 | SHACL v1.5 formal validation | FAIL |

WARN is used for borderline cases (e.g. `@base` present but non-standard,
`m2:changelog` absent). N/A is used when the check cannot run (e.g. SHACL
schema not found).

---

## Corpus state (as of 2026-06-19)

```
Total instances      : 33
PASS SHACL v1.5      :  1   (M0_AdaptativeImmuneResponse — reference migration)
PASS SHACL v1.4      :  8   (stubs without local properties)
FAIL namespace       : 23   (legacy m0:, m1core:, relative URLs)
Scores — Complete    :  6   (Vsm, Triz, Bmc + 3 TscgTools)
Scores — Partial     :  1   (AdaptativeImmuneResponse)
Scores — Pending     : 26
```

### Priority migration groups

**Group A — 8 instances (Pattern A scores, automated migration feasible):**
ComplexChemicalSynapse, Counterpoint, FourStrokeEngine, Kidneys,
NuclearReactorsTypology, Ptoe, Raas, Transistor

**Group B — 15 instances (missing or incorrect namespace, see `PENDING_SCORES_README.md`):**
BloodPressureControl, ButterflyMetamorphosis, CellSignalingModes,
ColorSynthesis, ExposureTriangle, FireTriangle, KindlebergerMinsky,
MtgColorWheel, NakamotoConsensus, PhaseTansition, PlateTectonics,
TrophicPyramid, TvTestPattern, Vco, Yggdrasil

---

## Reference: `M0_Common.jsonld` namespace table

| Alias | Resolves to | Usage |
|---|---|---|
| `m0:` | `M0_Common.jsonld#` | Shared scores, gap, focal, enum — **ALL instances** |
| `m0.<instance>:` | `instances/.../M0_<Name>.jsonld#` | Local properties — **ONE instance** |
| `m1:` | `M1_CoreConcepts.jsonld#` | CoreConcepts, `m1:domain`, `m1:simulationTitle` |
| `m1.extensions.<domain>:` | `M1_extensions/<d>/M1_<D>.jsonld#` | Domain concepts |
| `m2:` | `M2_GenericConcepts.jsonld#` | GenericConcepts, formulas |
| `m3:` | `M3_GenesisGrammar.jsonld#` | `m3:ontologyType`, M3 primitives |

**Forbidden patterns (SHACL will reject these):**

```
m1core:            → use m1:
m1bio:, m1chem:    → use m1.extensions.biology:, m1.extensions.chemistry:
m0bmc:, m0vsm:     → use m0.bmc:, m0.vsm:
tscg:              → forbidden in all M0 files
M0_Poclet#         → replaced by M0_Common.jsonld#
A_score … Im_score → replaced by m0:scoreA … m0:scoreIm
"Coherent"         → use {"@id": "m0:spectralClass.Coherent"}
{"@value":"0.85","@type":"xsd:float"} → use 0.85
```
