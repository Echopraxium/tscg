# Guide de Correction du Format `m1:domain`

**Date:** 2026-04-25  
**Auteur:** Echopraxium avec la collaboration de Claude AI  
**Problème:** Format incorrect `"Photography / Optics"` au lieu de `["Photography", "Optics"]`

## 🔍 Diagnostic

### Où se situe le problème ?

**✅ Script de validation:** Fonctionne correctement selon la grammaire actuelle  
**✅ Script de migration:** Fonctionne correctement - copie la valeur telle quelle  
**❌ Grammaire SHACL:** Trop permissive - accepte les deux formats  
**❌ Données sources:** Certaines instances avaient déjà le format incorrect

### Cause Racine

**Double problème identifié:**

1. **Grammaire SHACL trop permissive**
   - Accepte `"Photography / Optics"` (chaîne avec "/")
   - Accepte `["Photography", "Optics"]` (array)
   - Ne distingue pas entre les deux formats

2. **Données historiques incorrectes**
   - Certaines instances avaient `"m0:domain": "Photography / Optics"` dès le départ
   - Le script de migration a simplement copié: `"m0:domain"` → `"m1:domain"`
   - Aucune transformation du format n'a été appliquée

## 📋 Solution en 3 Étapes

### Étape 1: Scanner les instances problématiques (DRY RUN)

```bash
python fix_domain_format.py --dry-run
```

**Résultat attendu:**
- Liste des instances à corriger
- Aperçu des transformations (old → new)
- Aucune modification appliquée

**Exemple de sortie:**
```
🔍 DRY RUN MODE - No changes applied

📊 Would fix: 3
⏭️  Skip (already correct): 23
❌ Errors: 0

INSTANCES THAT WOULD BE FIXED:
📄 ExposureTriangle
   Old:  'Photography / Optics'
   New:  ['Photography', 'Optics']
```

### Étape 2: Appliquer les corrections

```bash
python fix_domain_format.py
```

**Ce que fait le script:**
1. ✅ Crée des backups dans `domain_format_fix_backups/YYYYMMDD_HHMMSS/`
2. ✅ Détecte les chaînes avec "/" dans `m1:domain`
3. ✅ Split sur "/" et nettoie les espaces
4. ✅ Convertit en format array
5. ✅ Sauvegarde les fichiers corrigés

**Exemple de transformation:**
```json
// AVANT
"m1:domain": "Photography / Optics"

// APRÈS
"m1:domain": ["Photography", "Optics"]
```

### Étape 3: Durcir la grammaire SHACL (optionnel mais recommandé)

**Fichier à modifier:** `ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl`

**Lignes 141-150 à remplacer par:**

```turtle
  # Domain (83% consensus on poclets - MIGRATED to M1 level)
  # v1.3 CHANGE: Added pattern to reject "/" separator in single string format
  sh:property [
    sh:path m1:domain ;
    sh:or (
      # Single domain: string WITHOUT "/" separator
      [ 
        sh:datatype xsd:string ;
        sh:pattern "^[^/]+$" ;  # Reject strings containing "/"
      ]
      # Multiple domains: array of strings
      [ 
        sh:nodeKind sh:Literal ;
      ]
    ) ;
    sh:minCount 1 ;
    sh:message "m1:domain is MANDATORY. FORMATS: single string ('Chemistry') for one domain, OR array (['Chemistry', 'Physics']) for multiple domains. String format with '/' separator is FORBIDDEN." ;
  ] ;
```

**Changelog à ajouter (fin du fichier):**
```turtle
# v1.3 (2026-04-25): Domain format enforcement
#   - BREAKING CHANGE: Reject m1:domain strings containing "/" separator
#   - Added pattern constraint "^[^/]+$" to enforce format
#   - Multiple domains MUST use array format: ["Domain1", "Domain2"]
```

## 🧪 Validation Post-Correction

```bash
# Valider une instance spécifique
python validate_m0_instance.py instances/poclets/ExposureTriangle/M0_ExposureTriangle.jsonld

# Valider toutes les instances (si tu as un script pour ça)
python validate_all_instances.py
```

## 📊 Résultats Attendus

**Avant correction:**
- ❌ `ExposureTriangle`: `"Photography / Optics"` (validation passe mais format incorrect)
- ❌ Autres instances potentielles avec le même problème

**Après correction:**
- ✅ `ExposureTriangle`: `["Photography", "Optics"]` (validation passe, format correct)
- ✅ Grammaire SHACL v1.3 rejette désormais le format avec "/"

## 🔄 Workflow Complet

```bash
# 1. Scanner le problème
python fix_domain_format.py --dry-run

# 2. Appliquer les corrections
python fix_domain_format.py

# 3. (Optionnel) Corriger une instance spécifique seulement
python fix_domain_format.py --instance ExposureTriangle

# 4. Valider les corrections
python validate_m0_instance.py instances/poclets/ExposureTriangle/M0_ExposureTriangle.jsonld

# 5. Mettre à jour la grammaire SHACL
# → Éditer manuellement M0_Instances_Schema.shacl.ttl avec la nouvelle contrainte
```

## 📁 Fichiers Générés

1. **`fix_domain_format.py`**
   - Script de correction automatique
   - Support dry-run et instance spécifique
   - Création automatique de backups

2. **`M0_Instances_Schema_domain_fix_v1_3.ttl`**
   - Contrainte SHACL corrigée
   - Pattern pour rejeter les "/"
   - Instructions de migration

3. **`domain_format_analysis.md`**
   - Analyse détaillée du problème
   - Diagnostic complet
   - Recommandations

## ⚠️ Points d'Attention

**Ce qui NE change PAS:**
- ✅ Format array déjà correct: `["Chemistry", "Physics"]` → inchangé
- ✅ Format string simple: `"Chemistry"` → inchangé

**Ce qui CHANGE:**
- ❌ Format string avec "/": `"Photography / Optics"` → `["Photography", "Optics"]`

**Backups:**
- 💾 Tous les fichiers modifiés sont sauvegardés avant correction
- 📁 Localisation: `domain_format_fix_backups/YYYYMMDD_HHMMSS/<instance_name>/`

## 🎯 Prochaines Étapes

1. ✅ **Exécuter le dry-run** pour voir l'étendue du problème
2. ✅ **Appliquer les corrections** avec le script
3. ✅ **Valider** les instances corrigées
4. ⚡ **Optionnel:** Mettre à jour la grammaire SHACL pour prévenir futures erreurs

## 💡 Conclusion

**Ce n'était pas un bug**, mais une **grammaire trop permissive** combinée à des **données historiques incorrectes**.

**Solutions fournies:**
- ✅ Script de correction automatique (`fix_domain_format.py`)
- ✅ Grammaire SHACL durcie (v1.3 avec pattern `^[^/]+$`)
- ✅ Prévention de futures erreurs
