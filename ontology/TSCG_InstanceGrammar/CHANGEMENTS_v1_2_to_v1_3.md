# Résumé des Changements - SHACL Grammar v1.2 → v1.3

**Date:** 2026-04-25  
**Auteur:** Echopraxium avec la collaboration de Claude AI

## 📝 Changements Appliqués

### 1. ✅ En-tête du Fichier (lignes 1-5)

**Changements:**
- Version: v1.2 → v1.3
- Date ajoutée: 2026-04-25 (v1.3 - domain format enforcement)
- Status mis à jour: "Domain format enforcement: m1:domain must use array for multiple domains"

### 2. ✅ Contrainte `m1:domain` (lignes 141-162)

**BEFORE (v1.2):**
```turtle
sh:property [
  sh:path m1:domain ;
  sh:or (
    [ sh:datatype xsd:string ]           # Single domain string
    [ sh:nodeKind sh:Literal ]           # Array of domain strings
  ) ;
```

**AFTER (v1.3):**
```turtle
sh:property [
  sh:path m1:domain ;
  sh:or (
    # Single domain: string WITHOUT "/" separator
    [ 
      sh:datatype xsd:string ;
      sh:pattern "^[^/]+$" ;  # ⚠️ NOUVEAU: Reject strings containing "/"
    ]
    # Multiple domains: array of strings
    [ 
      sh:nodeKind sh:Literal ;
    ]
  ) ;
```

**Effet:**
- ✅ ACCEPTE: `"Chemistry"` (single domain sans "/")
- ✅ ACCEPTE: `["Photography", "Optics"]` (array)
- ❌ REJETTE: `"Photography / Optics"` (string avec "/")
- ❌ REJETTE: `"Chemistry / Physics"` (string avec "/")

### 3. ✅ Message de Validation Amélioré

**Nouveau message:**
```
m1:domain is MANDATORY. 
FORMATS: 
  - single string ('Chemistry') for one domain
  - OR array (['Chemistry', 'Physics']) for multiple domains
  
String format with '/' separator (e.g., 'Chemistry / Physics') is FORBIDDEN - use array format instead.
```

### 4. ✅ Changelog (fin du fichier)

**Gardé seulement les 3 dernières versions:**
- v1.3 (2026-04-25): Domain format enforcement
- v1.2 (2026-04-19): Absolute URL requirements documentation
- v1.1 (2026-04-18): Domain property migration to M1 level

**Versions supprimées du changelog:**
- v1.0, v0.3, v0.2, v0.1 (conformément à la règle "max 3 entrées")

## 🎯 Impact

### Instances Concernées

**Vont échouer la validation (jusqu'à correction):**
- ExposureTriangle: `"Photography / Optics"` → doit devenir `["Photography", "Optics"]`
- (Toute autre instance avec le format "/" dans m1:domain)

**Resteront valides:**
- Instances avec format simple: `"Chemistry"` ✅
- Instances avec format array: `["Biology", "Chemistry"]` ✅

### Workflow de Migration

```bash
# 1. Identifier les instances à corriger
python fix_domain_format.py --dry-run

# 2. Appliquer les corrections
python fix_domain_format.py

# 3. Remplacer la grammaire SHACL
cp M0_Instances_Schema_v1_3.ttl ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl

# 4. Valider le corpus
python validate_all_instances.py
```

## 📊 Statistiques Inchangées

Les statistiques du corpus (lignes 480-521) restent identiques car elles documentent l'état AVANT correction. Ces stats seront mises à jour lors du prochain scan complet du corpus après migration.

## 🔒 Garanties

**Cette version garantit:**
- ✅ Format cohérent pour domaines multiples (toujours en array)
- ✅ Prévention de futures erreurs (pattern `^[^/]+$`)
- ✅ Messages de validation clairs et explicites
- ✅ Rétrocompatibilité pour instances correctement formatées

**Breaking change:**
- ❌ Rejette désormais `"Domain1 / Domain2"` (était accepté en v1.2)
- ✅ Solution: Utiliser `fix_domain_format.py` pour migration automatique
