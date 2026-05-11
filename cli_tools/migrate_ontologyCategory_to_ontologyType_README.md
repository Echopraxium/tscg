# Migration Script: ontologyCategory → ontologyType

**Auteur**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-05-11

## Description

Ce script Python migre toutes les occurrences de `ontologyCategory` vers `ontologyType` dans les fichiers d'ontologie TSCG (couches M3, M2, M1, M0).

## Remplacements effectués

Le script détecte et remplace les patterns suivants :

1. `"m3:ontologyCategory"` → `"m3:ontologyType"`
2. `"m2:ontologyCategory"` → `"m3:ontologyType"` (correction de namespace)
3. `'m3:ontologyCategory'` → `'m3:ontologyType'` (guillemets simples)
4. `'m2:ontologyCategory'` → `'m3:ontologyType'` (guillemets simples)
5. `"ontologyCategory":` → `"ontologyType":` (dans les définitions @context)

## Résultats du test (dry-run)

Test effectué sur le répertoire `/mnt/project` :

```
Files processed:    6
Files modified:     3
Total replacements: 3

Fichiers nécessitant une modification :
  ✓ M2_GenericConcepts.jsonld  (1 occurrence)
  ✓ M3_EagleEye.jsonld         (1 occurrence)
  ✓ M3_SphinxEye.jsonld        (1 occurrence)
```

## Installation

Placez le script dans le dossier `cli-tools` de votre repo :
```
tscg/
├── cli-tools/
│   └── migrate_ontologyCategory_to_ontologyType.py
└── ontology/
    ├── instances/
    ├── M1-Extensions/
    └── ...
```

## Utilisation

### 1. Mode dry-run (recommandé en premier)

```bash
# Depuis le dossier cli-tools
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\cli-tools
python migrate_ontologyCategory_to_ontologyType.py --dir ../ontology --dry-run

# Ou avec chemin absolu
python E:\_00_Michel\_00_Lab\_00_GitHub\tscg\cli-tools\migrate_ontologyCategory_to_ontologyType.py --dir E:\_00_Michel\_00_Lab\_00_GitHub\tscg\ontology --dry-run
```

Ce mode affiche ce qui sera modifié **sans toucher aux fichiers**.

### 2. Migration réelle avec backup automatique

```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\cli-tools
python migrate_ontologyCategory_to_ontologyType.py --dir ../ontology
```

Crée automatiquement un dossier de backup avec timestamp avant modification.

### 3. Migration sans backup (si git est utilisé)

```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\cli-tools
python migrate_ontologyCategory_to_ontologyType.py --dir ../ontology --no-backup
```

## Options

- `--dir <directory>` : Répertoire racine contenant les fichiers d'ontologie (obligatoire)
- `--dry-run` : Mode simulation - affiche les changements sans modifier les fichiers
- `--no-backup` : Ne pas créer de backup (non recommandé sauf si git est utilisé)

## Sécurité

Le script :
- ✅ Valide que le JSON reste valide après modification
- ✅ Crée des backups automatiques (sauf en dry-run ou avec --no-backup)
- ✅ Produit un rapport détaillé des modifications
- ✅ Gère les erreurs sans corrompre les fichiers

## Fichiers concernés

Le script traite **récursivement** tous les fichiers `.jsonld` correspondant aux patterns :
- `M3_*.jsonld` (racine de l'ontologie)
- `M2_*.jsonld` (racine de l'ontologie)
- `M1_*.jsonld` (racine + **M1-Extensions/\*\*/\*.jsonld** - toutes les extensions de domaine)
- `M0_*.jsonld` (**instances/\*\*/\*.jsonld** - tous les poclets, systemic frameworks, etc.)

La recherche explore **tous les sous-dossiers** :
- ✅ Racine : `M3_GenesisSpace.jsonld`, `M2_GenericConcepts.jsonld`, `M1_CoreConcepts.jsonld`
- ✅ Extensions M1 : `M1-Extensions/biology/M1_Biology.jsonld`, `M1-Extensions/physics/M1_Physics.jsonld`, etc.
- ✅ Instances M0 : `instances/poclets/FireTriangle/M0_FireTriangle.jsonld`, etc.

## Rapport de migration

À la fin de l'exécution, le script affiche :
- Nombre de fichiers traités
- Nombre de fichiers modifiés
- Nombre total de remplacements effectués
- Liste détaillée des modifications par fichier
- Emplacement du dossier de backup (si créé)
- Liste des erreurs (si rencontrées)

## Exemple de sortie (dry-run)

```
================================================================================
TSCG Ontology Migration: ontologyCategory -> ontologyType
================================================================================
Root directory: E:\_00_Michel\_00_Lab\_00_GitHub\tscg\ontology
Mode: DRY-RUN (no files will be modified)
Backup: Disabled

Found 6 JSON-LD files to process:
  - M3_GenesisSpace.jsonld
  - M3_EagleEye.jsonld
  - M3_SphinxEye.jsonld
  - M2_GenericConcepts.jsonld
  - M1_CoreConcepts.jsonld
  - ...

Processing files...
--------------------------------------------------------------------------------

M2_GenericConcepts.jsonld:
  ⚠ DRY-RUN: Would modify file (1 replacements)
    - "m3:ontologyCategory" -> "m3:ontologyType" (1 times)

M3_EagleEye.jsonld:
  ⚠ DRY-RUN: Would modify file (1 replacements)
    - "m3:ontologyCategory" -> "m3:ontologyType" (1 times)

================================================================================
MIGRATION SUMMARY
================================================================================
Files processed:    6
Files modified:     3
Total replacements: 3
Errors:             0

⚠ DRY-RUN MODE: No files were actually modified.
   Run without --dry-run to apply changes.
================================================================================
```

## Recommandations

1. **Toujours commencer par un dry-run** pour voir ce qui sera modifié
2. **Vérifier le rapport** avant de lancer la migration réelle
3. **Garder les backups** jusqu'à validation complète
4. **Tester les fichiers modifiés** dans votre environnement après migration

## Support

En cas de problème, le script affiche des messages d'erreur détaillés et continue le traitement des autres fichiers sans interruption.
