# M1_Domains v1.2.0 — Ptoe Registration

**File**: M1_Domains_v1.2.0.jsonld  
**Version**: 1.1.0 → **1.2.0**  
**Date**: 2026-04-26  
**Status**: ✅ Complete — Ptoe registered in Chemistry domain

---

## Changes Made

### 1. Ontology Metadata Updated

**Version**:
- **Before**: `1.1.0`
- **After**: `1.2.0`

**Total Poclets**:
- **Before**: 24
- **After**: **25** (+1 for Ptoe)

**Domain Count**:
- **Unchanged**: 19 (Chemistry already existed)

---

### 2. Changelog Updated (Rolling Window — 3 entries max)

**New Entry**:
```json
{
  "version": "1.2.0",
  "date": "2026-04-26",
  "changes": "Added Ptoe (Periodic Table of Elements) to Chemistry domain. Updated Chemistry subdomains: added 'Atomic Structure' and 'Periodic Properties'. Chemistry pocletCount: 3→4. M1_Chemistry extension enriched to v1.1.0 with 8 atomic structure concepts."
}
```

**Kept** (from previous versions):
- v1.1.0 (2026-04-19): Blockchain domain addition
- v1.0.0 (2026-04-18): Initial registry

---

### 3. Chemistry Domain Updated

#### Subdomains (6 → 8)
**Added**:
- `"Atomic Structure"`
- `"Periodic Properties"`

**Full list now**:
```json
"m1:subdomains": [
  "Combustion Chemistry",
  "Physical Chemistry",
  "Thermodynamics",
  "Chemical Kinetics",
  "Organic Chemistry",
  "Inorganic Chemistry",
  "Atomic Structure",        ← NEW
  "Periodic Properties"       ← NEW
]
```

#### Poclet Examples (3 → 4)
**Added**:
- `"M0_Ptoe"`

**Full list now**:
```json
"m1:pocletExamples": [
  "M0_FireTriangle",
  "M0_PhaseTransition",
  "M0_ComplexChemicalSynapse",
  "M0_Ptoe"                   ← NEW
]
```

#### Poclet Count
- **Before**: 3
- **After**: **4**

#### Note Updated
**Before**:
> "PhaseTransition spans Physical Chemistry and Physics. ComplexChemicalSynapse spans Chemistry and Neurobiology."

**After**:
> "PhaseTransition spans Physical Chemistry and Physics. ComplexChemicalSynapse spans Chemistry and Neurobiology. **Ptoe (Periodic Table) demonstrates atomic structure and periodic properties.**"

---

## Validation

### Pre-Check ✅
- ✅ Ontology version bumped: 1.1.0 → 1.2.0
- ✅ Total poclets incremented: 24 → 25
- ✅ Changelog entry added (rolling window maintained)
- ✅ Chemistry domain found and updated
- ✅ Subdomains added (Atomic Structure, Periodic Properties)
- ✅ Ptoe added to pocletExamples
- ✅ Poclet count incremented: 3 → 4
- ✅ Note updated with Ptoe reference
- ✅ UTF-8 encoding preserved

---

## Installation

### Replace in Repo

```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\

# Backup original
cp ontology/M1_Domains.jsonld \
   ontology/M1_Domains_v1.1.0.backup.jsonld

# Install new version
cp ~/Downloads/M1_Domains_v1.2.0.jsonld \
   ontology/M1_Domains.jsonld
```

---

## Summary — Complete File Set for Ptoe

### Files to Install

| File | Version | Destination | Status |
|------|---------|-------------|--------|
| **M1_Chemistry.jsonld** | v1.1.0 | `ontology/M1_extensions/chemistry/` | ✅ Enriched (+8 concepts) |
| **M1_Domains.jsonld** | v1.2.0 | `ontology/` | ✅ Updated (Ptoe registered) |
| **M0_Ptoe.jsonld** | v1.0.1 | `instances/poclets/Ptoe/` | ✅ Namespace fixed |
| **M0_Ptoe_README.md** | v1.0.0 | `instances/poclets/Ptoe/` | ✅ Complete |
| **M0_Ptoe_analysis.md** | v1.0.0 | `instances/poclets/Ptoe/` | ✅ Complete |

---

## Next Step — SHACL Validation

Once all files are copied to the repo, run:

```bash
python ontology/TSCG_Grammar/validate_m0_instance.py \
       instances/poclets/Ptoe/M0_Ptoe.jsonld
```

**Expected**: ✅ VALIDATION PASSED

---

**Status**: ✅ M1_Domains v1.2.0 ready for installation
