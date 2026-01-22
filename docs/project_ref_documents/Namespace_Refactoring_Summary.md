# TSCG Ontology Namespace Refactoring - Summary

**Date**: 2026-01-22  
**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: Namespace Refactoring v1.0

---

## 🎯 Objectif

Refactorisation complète des namespaces des ontologies TSCG pour améliorer la cohérence, la lisibilité et la maintenabilité du framework.

---

## ✅ Corrections Effectuées

### 1. **Namespaces M3** - Architecture Bicéphale

**Avant** :
```json
"m3genesis": "https://tscg.org/...",
"m3eagle": "https://tscg.org/...",
"m3sphinx": "https://tscg.org/..."
```

**Après** :
```json
"m3:genesis": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
"m3:eagle_eye": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#",
"m3:sphinx_eye": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#"
```

**Fichiers modifiés** :
- ✅ `M3_GenesisSpace.jsonld` (v2.0.0 → v2.0.1)
- ✅ `M3_EagleEye.jsonld` (v2.0.0 → v2.0.1)
- ✅ `M3_SphinxEye.jsonld` (v2.0.0 → v2.0.1)

**Avantages** :
- Format `snake_case` cohérent
- Séparation claire namespace:sous-namespace
- Lisibilité améliorée

---

### 2. **Namespaces M1** - Extensions de Domaine

**Avant** :
```json
"m1": "https://raw.githubusercontent.com/..."
```

**Après** :
```json
"m1:core": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
"m1:optics": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Optics.jsonld#",
"m1:chemistry": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Chemistry.jsonld#",
"m1:biology": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Biology.jsonld#",
"m1:photography": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Photography.jsonld#"
```

**Fichiers modifiés** :
- ✅ `M1_CoreConcepts.jsonld` → namespace `m1:core`
- ✅ `M1_Optics.jsonld` → namespace `m1:optics`

**Fichiers à créer** (recommandés) :
- ⏳ `M1_Chemistry.jsonld` → namespace `m1:chemistry`
- ⏳ `M1_Biology.jsonld` → namespace `m1:biology`
- ⏳ `M1_Photography.jsonld` → namespace `m1:photography`

**Principe** :
Le namespace M1 correspond au nom du dossier dans `/ontology/M1_extensions/{domain}/` en `snake_case`.

---

### 3. **Namespaces M0** - Poclets

**Avant** :
```json
"m0": "https://github.com/Echopraxium/tscg/blob/main/ontology/poclets/.../M0_*.jsonld#"
```

**Après** :
```json
"m0:fire_triangle": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/fire_triangle/M0_FireTriangle.jsonld#",
"m0:cell_signaling": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/cell_signaling/M0_CellSignalingModes.jsonld#",
"m0:color_synthesis": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/color_synthesis/M0_ColorSynthesis_Federated.jsonld#",
"m0:exposition_triangle": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/exposition_triangle/M0_ExposureTriangle.jsonld#",
...
```

**Fichiers modifiés** :
- ✅ `M0_FireTriangle.jsonld` → namespace `m0:fire_triangle`

**Fichiers à modifier** (recommandés) :
- ⏳ `M0_CellSignalingModes.jsonld` → `m0:cell_signaling`
- ⏳ `M0_ExposureTriangle.jsonld` → `m0:exposition_triangle`
- ⏳ `M0_RGB_Additive.jsonld` → `m0:color_synthesis`
- ⏳ `M0_HSL_Additive.jsonld` → `m0:color_synthesis`
- ⏳ `M0_CMY_Subtractive.jsonld` → `m0:color_synthesis`
- ⏳ `M0_CMYK_Subtractive.jsonld` → `m0:color_synthesis`
- ⏳ `M0_ColorSynthesis_Federated.jsonld` → `m0:color_synthesis`
- ⏳ `M0_ComplexChemicalSynapse.jsonld` → `m0:complex_chemical_synapse`
- ⏳ `M0_TPACK.jsonld` → `m0:tpack`
- ⏳ `M0_FourStrokeEngine.jsonld` → `m0:four_stroke_engine`
- ⏳ `M0_MTG_ColorWheel.jsonld` → `m0:mtg_color_wheel`

**Principe** :
Le namespace M0 correspond au nom du dossier dans `/ontology/poclets/{poclet_name}/` en `snake_case`.

---

### 4. **Import de M1_CoreConcepts**

**Ajout obligatoire** :
Tous les poclets (M0) doivent maintenant importer `M1_CoreConcepts.jsonld` :

```json
"owl:imports": [
  "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld",
  "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld"
]
```

**Status** :
- ✅ `M0_FireTriangle.jsonld` - Import ajouté
- ⏳ Autres poclets à mettre à jour

---

### 5. **Correction des URIs**

**Avant** :
```
https://github.com/Echopraxium/tscg/blob/main/ontology/...
https://tscg.org/...
```

**Après** :
```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/...
```

**Raison** :
- GitHub raw permet l'accès direct au contenu des fichiers
- Nécessaire pour le fonctionnement correct de `owl:imports`
- Standard pour les ontologies hébergées sur GitHub

---

## 📋 Checklist de Migration

### Fichiers Corrigés ✅

**M3 Layer** (3/3):
- [x] M3_GenesisSpace.jsonld
- [x] M3_EagleEye.jsonld
- [x] M3_SphinxEye.jsonld

**M2 Layer** (1/1):
- [x] M2_MetaConcepts.jsonld

**M1 Layer** (5/5):
- [x] M1_CoreConcepts.jsonld
- [x] M1_Optics.jsonld
- [x] M1_Photography.jsonld ✨ NEW
- [x] M1_Chemistry.jsonld ✨ NEW
- [x] M1_Biology.jsonld ✨ NEW

**M0 Layer** (1/11):
- [x] M0_FireTriangle.jsonld

### Fichiers à Corriger ⏳
- [ ] M0_CellSignalingModes.jsonld
- [ ] M0_ExposureTriangle.jsonld
- [ ] M0_RGB_Additive.jsonld
- [ ] M0_HSL_Additive.jsonld
- [ ] M0_CMY_Subtractive.jsonld
- [ ] M0_CMYK_Subtractive.jsonld
- [ ] M0_ColorSynthesis_Federated.jsonld
- [ ] M0_ComplexChemicalSynapse.jsonld
- [ ] M0_TPACK.jsonld
- [ ] M0_FourStrokeEngine.jsonld
- [ ] M0_MTG_ColorWheel.jsonld

### Extensions M1 Complétées ✅

Les 4 extensions de domaine M1 ont été créées et corrigées :

**M1_Chemistry.jsonld** (namespace `m1:chemistry`):
- Patterns pour réactions chimiques, équilibres, combustion
- Concepts: Reactant, Product, Catalyst, Activation Energy
- Import correct de M1_CoreConcepts
- Références M3 corrigées (m3:eagle_eye, m3:sphinx_eye)

**M1_Biology.jsonld** (namespace `m1:biology`):
- Patterns pour communication cellulaire, signalisation
- Concepts: Autocrine, Paracrine, Endocrine, Juxtacrine
- Conversion m1bio: → m1:biology: pour cohérence
- Import M3 ajouté

**M1_Photography.jsonld** (namespace `m1:photography`):
- 10 patterns photographiques
- Concepts: Compensatory Triplet, Logarithmic Scaling, Side Effect Coupling
- Namespace corrigé m1: → m1:photography:
- Références M3 mises à jour

**M1_Optics.jsonld** (namespace `m1:optics`):
- 8 patterns optiques (v2 corrigée)
- Additive/Subtractive Color Synthesis, Channel Multiplexing
- URLs GitHub corrigées (blob → raw)
- Chemins de fichiers normalisés

### Extensions M1 à Créer ⏳
- [ ] M1_Chemistry.jsonld (namespace `m1:chemistry`)
- [ ] M1_Biology.jsonld (namespace `m1:biology`)
- [ ] M1_Photography.jsonld (namespace `m1:photography`)

---

## 🔧 Convention de Nommage

### Format Général
```
{layer}:{domain}:{entity}
```

### Exemples
```json
// M3 Layer
"m3:genesis:M3_GenesisSpace"
"m3:eagle_eye:Attractor"
"m3:sphinx_eye:Observer"

// M2 Layer
"m2:Homeostasis"
"m2:Balance"

// M1 Layer
"m1:core:Poclet"
"m1:optics:AdditiveColorSynthesis"
"m1:chemistry:Combustion"

// M0 Layer
"m0:fire_triangle:FireTrianglePoclet"
"m0:color_synthesis:RGB_Additive"
```

### Règles snake_case
- Dossiers : `fire_triangle`, `cell_signaling`, `color_synthesis`
- Namespaces : `m3:eagle_eye`, `m1:optics`, `m0:fire_triangle`
- Si multi-mots : toujours `snake_case`

---

## 📊 Impact de la Refactorisation

### Bénéfices
1. **Cohérence** : Convention de nommage uniforme sur tous les layers
2. **Lisibilité** : Namespaces explicites et auto-documentés
3. **Maintenabilité** : Ajout de nouveaux domaines facilité
4. **Interopérabilité** : URIs GitHub raw fonctionnels pour owl:imports
5. **Scalabilité** : Structure extensible pour futurs domaines

### Changements Breaking
⚠️ **Attention** : Ces modifications sont des changements majeurs (breaking changes)

- Toutes les références `m3eagle:` doivent devenir `m3:eagle_eye:`
- Toutes les références `m3sphinx:` doivent devenir `m3:sphinx_eye:`
- Toutes les références `m1:` doivent préciser le domaine (`m1:core:`, `m1:optics:`, etc.)
- Tous les poclets doivent importer `M1_CoreConcepts.jsonld`

### Rétrocompatibilité
❌ Non rétrocompatible avec les versions précédentes des ontologies

---

## 🚀 Prochaines Étapes

### Court Terme
1. Appliquer le même script de correction aux poclets restants
2. Créer les extensions M1 manquantes (Chemistry, Biology, Photography)
3. Valider toutes les ontologies avec un validateur OWL

### Moyen Terme
1. Mettre à jour la documentation (README, guides)
2. Créer des exemples d'utilisation avec nouveaux namespaces
3. Tests d'intégration complets

### Long Terme
1. Migration des outils et scripts vers nouveaux namespaces
2. Mise à jour des visualisations et diagrammes
3. Publication de la version stable du framework

---

## 📚 Références

### Documents Concernés
- `ontology_analysis.md` - Analyse initiale des problèmes
- `TSCG_File_Tree.md` - Structure complète du projet
- `Bicephalous_Integration_Guide.md` - Guide d'intégration M3

### Standards
- W3C OWL 2 Web Ontology Language
- JSON-LD 1.1 Specification
- GitHub raw content URLs

---

**FIN DU DOCUMENT**

**Status** : ✅ Phase 1 complétée (M3, M2, M1 core, M1 optics, M0 fire_triangle)  
**Date** : 2026-01-22  
**Next** : Application aux poclets restants
