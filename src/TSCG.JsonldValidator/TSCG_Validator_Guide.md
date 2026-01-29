# 🔍 TSCG Ontology Validator - Guide d'Utilisation

**Version:** 1.0.0  
**Date:** January 25, 2026  
**Author:** Echopraxium with the collaboration of Claude AI

---

## 📋 Table des Matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Validations Effectuées](#validations-effectuées)
4. [Utilisation](#utilisation)
5. [Exemples](#exemples)
6. [Codes de Sortie](#codes-de-sortie)
7. [Interprétation des Résultats](#interprétation-des-résultats)

---

## 🎯 Introduction

Le **TSCG Ontology Validator** est un outil Python qui valide automatiquement vos fichiers d'ontologie JSON-LD pour s'assurer qu'ils respectent les standards TSCG et les spécifications JSON-LD.

### Ce qu'il détecte :

- ❌ **Erreurs critiques** qui empêchent le parsing ou violent les standards
- ⚠️ **Avertissements** pour les pratiques non optimales

---

## 📦 Installation

### Prérequis

- Python 3.7+
- Aucune dépendance externe (utilise uniquement la bibliothèque standard)

### Installation

```bash
# 1. Télécharger le validateur
curl -O https://raw.githubusercontent.com/Echopraxium/tscg/main/tools/tscg_ontology_validator.py

# 2. Rendre exécutable (Linux/Mac)
chmod +x tscg_ontology_validator.py

# 3. Tester
python tscg_ontology_validator.py --help
```

---

## ✅ Validations Effectuées

### 1. Structure JSON-LD

- ✓ JSON valide et parsable
- ✓ Présence de `@context`
- ✓ Présence de `@graph` ou `@id`

### 2. Namespaces (@context)

| Validation | Description |
|------------|-------------|
| **Formats valides** | Vérifie les patterns TSCG (m3:eagle_eye, m1:biology, etc.) |
| **Séparateurs** | Détecte les POINTS (.) au lieu des DEUX-POINTS (:) |
| **Namespaces requis** | Vérifie présence de dcterms, owl, rdf, rdfs, xsd |
| **Ordre** | W3C alphabétique puis TSCG hiérarchique (M3→M2→M1→M0) |
| **Collisions** | Détecte les préfixes en double |

### 3. URIs

| Validation | Description |
|------------|-------------|
| **Format** | Vérifie https:// et structure correcte |
| **Domaine GitHub** | Détecte github.com au lieu de raw.githubusercontent.com |
| **Base URI** | Vérifie présence du base TSCG attendu |
| **Fragment #** | Avertit si absent en fin d'URI |
| **Chemins** | Valide structure /M3_*, /M1_extensions/, /poclets/ |

### 4. owl:imports

- ✓ Format des URIs importées
- ✓ Extension .jsonld
- ✓ Utilisation de raw.githubusercontent.com

### 5. Préfixes et Identifiants

| Validation | Description |
|------------|-------------|
| **Préfixes utilisés** | Tous les préfixes utilisés sont déclarés |
| **Préfixes inutilisés** | Avertit des déclarations non utilisées |
| **Format @id** | Valide les compact IRIs |
| **Références** | Détecte les références à des préfixes non définis |

---

## 🚀 Utilisation

### Mode 1 : Validation d'un fichier unique

```bash
python tscg_ontology_validator.py M0_TPACK.jsonld
```

### Mode 2 : Validation d'un répertoire

```bash
# Tous les fichiers .jsonld
python tscg_ontology_validator.py --dir ./ontology

# Pattern spécifique
python tscg_ontology_validator.py --dir ./ontology --pattern "M1_*.jsonld"
```

### Options

| Option | Description | Exemple |
|--------|-------------|---------|
| `file` | Fichier à valider | `M0_TPACK.jsonld` |
| `--dir`, `-d` | Répertoire à valider | `--dir ./ontology` |
| `--pattern`, `-p` | Pattern de fichiers | `--pattern "M2_*.jsonld"` |
| `--help`, `-h` | Affiche l'aide | `--help` |

---

## 📚 Exemples

### Exemple 1 : Valider M0_TPACK.jsonld

```bash
python tscg_ontology_validator.py M0_TPACK.jsonld
```

**Sortie (exemple avec erreurs) :**

```
================================================================================
🔍 Validating: M0_TPACK.jsonld
================================================================================

================================================================================
📊 VALIDATION REPORT - M0_TPACK.jsonld
================================================================================

Issues found: 3 errors, 2 warnings

────────────────────────────────────────────────────────────────────────────────
❌ ERRORS (must fix)
────────────────────────────────────────────────────────────────────────────────
 1. ❌ Invalid namespace 'm3.eagle_eye': contains POINT (.) - must use COLON (:)
 2. ❌ URI for 'm1:biology' uses github.com instead of raw.githubusercontent.com
 3. ❌ Prefix 'm4' used but not defined in @context

────────────────────────────────────────────────────────────────────────────────
⚠️  WARNINGS (should fix)
────────────────────────────────────────────────────────────────────────────────
 1. ⚠️  W3C namespaces not alphabetical: ['owl', 'dcterms', 'rdf'] (expected: ['dcterms', 'owl', 'rdf'])
 2. ⚠️  Prefix 'm1:chemistry' declared but never used

────────────────────────────────────────────────────────────────────────────────
📈 STATISTICS
────────────────────────────────────────────────────────────────────────────────
Namespaces defined: 8
Prefixes used: 6
IDs defined: 15
IDs referenced: 23
```

### Exemple 2 : Validation par lot

```bash
python tscg_ontology_validator.py --dir ./ontology/poclets --pattern "M0_*.jsonld"
```

**Sortie :**

```
================================================================================
🔍 BATCH VALIDATION - 11 files in ./ontology/poclets
================================================================================

[... rapport pour chaque fichier ...]

================================================================================
📊 BATCH SUMMARY
================================================================================
✅ Passed: 9/11
❌ Failed: 2/11
================================================================================
```

### Exemple 3 : Fichier sans erreur

```bash
python tscg_ontology_validator.py M3_GenesisSpace.jsonld
```

**Sortie :**

```
================================================================================
🔍 Validating: M3_GenesisSpace.jsonld
================================================================================

================================================================================
📊 VALIDATION REPORT - M3_GenesisSpace.jsonld
================================================================================

✅ VALIDATION PASSED - No issues found!

────────────────────────────────────────────────────────────────────────────────
📈 STATISTICS
────────────────────────────────────────────────────────────────────────────────
Namespaces defined: 8
Prefixes used: 5
IDs defined: 12
IDs referenced: 8
```

---

## 🔢 Codes de Sortie

| Code | Signification |
|------|---------------|
| `0` | ✅ Validation réussie (aucune erreur) |
| `1` | ❌ Validation échouée (erreurs détectées) |

**Usage dans scripts :**

```bash
#!/bin/bash
python tscg_ontology_validator.py M0_TPACK.jsonld
if [ $? -eq 0 ]; then
    echo "✅ Validation OK, procéder au commit"
    git add M0_TPACK.jsonld
    git commit -m "Add validated M0_TPACK ontology"
else
    echo "❌ Validation failed, corriger les erreurs"
    exit 1
fi
```

---

## 📖 Interprétation des Résultats

### Types de Messages

#### ❌ ERREURS (Critiques - MUST FIX)

**Doivent être corrigées** avant d'utiliser l'ontologie.

Exemples :
```
❌ Invalid namespace 'm3.eagle_eye': contains POINT (.) - must use COLON (:)
❌ Missing required W3C namespaces: owl, rdf
❌ Prefix 'm2' used but not defined in @context
```

**Action :** Corriger immédiatement

---

#### ⚠️ AVERTISSEMENTS (SHOULD FIX)

**Recommandé** de corriger pour respecter les bonnes pratiques.

Exemples :
```
⚠️  W3C namespaces not alphabetical
⚠️  URI doesn't end with # (fragment identifier)
⚠️  Prefix 'm1:chemistry' declared but never used
```

**Action :** Corriger si possible, mais non bloquant

---

### Messages Communs et Solutions

| Message | Cause | Solution |
|---------|-------|----------|
| `contains POINT (.)` | Namespace avec `.` au lieu de `:` | Remplacer `m3.eagle_eye` par `m3:eagle_eye` |
| `github.com instead of raw.githubusercontent.com` | Mauvais domaine GitHub | Utiliser `raw.githubusercontent.com` |
| `used but not defined` | Préfixe manquant dans @context | Ajouter le namespace dans @context |
| `not alphabetical` | Ordre incorrect | Réorganiser : W3C (alpha) puis TSCG (M3→M2→M1→M0) |
| `declared but never used` | Namespace inutile | Retirer ou commencer à l'utiliser |

---

## 🛠️ Intégration CI/CD

### GitHub Actions

```yaml
name: Validate Ontologies

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Validate ontologies
        run: |
          python tools/tscg_ontology_validator.py --dir ontology
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Validating changed JSON-LD files..."

# Get changed .jsonld files
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.jsonld$')

if [ -z "$changed_files" ]; then
    echo "✅ No JSON-LD files to validate"
    exit 0
fi

# Validate each file
for file in $changed_files; do
    python tools/tscg_ontology_validator.py "$file"
    if [ $? -ne 0 ]; then
        echo "❌ Validation failed for $file"
        exit 1
    fi
done

echo "✅ All JSON-LD files validated successfully"
exit 0
```

---

## 📝 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-25 | Initial release |

---

## 🤝 Support

Pour signaler des bugs ou proposer des améliorations :
- GitHub Issues : https://github.com/Echopraxium/tscg/issues
- Email : [votre email]

---

**Maintenu par :** Echopraxium with the collaboration of Claude AI  
**Dernière mise à jour :** January 25, 2026
