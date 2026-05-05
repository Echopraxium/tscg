# Migration Guide: m1:simulationTitle

**Date:** 2026-04-28  
**Version:** M1_CoreConcepts v2.2.0

---

## Vue d'ensemble

Cette migration ajoute la propriété `m1core:simulationTitle` aux instances TSCG pour séparer :
- Le **titre formel** (`rdfs:label`) — nom complet de l'ontologie avec préfixes
- Le **titre d'affichage** (`m1core:simulationTitle`) — nom court pour la galerie

### Exemple
```json
{
  "@id": "",
  "@type": "owl:Ontology",
  "rdfs:label": "TSCG M0 Trophic Pyramid Poclet",
  "m1core:simulationTitle": "Trophic Pyramid"
}
```

---

## Fichiers modifiés

### 1. `M1_CoreConcepts.jsonld` (v2.1.0 → v2.2.0)

✅ **Nouvelle propriété OWL ajoutée** :
```json
{
  "@id": "m1core:simulationTitle",
  "@type": "owl:DatatypeProperty",
  "rdfs:label": "Simulation Title",
  "rdfs:domain": "owl:Ontology",
  "rdfs:range": "xsd:string"
}
```

### 2. `generate_index.js`

✅ **Fonction `parseJsonld()` mise à jour** :
```javascript
// Extract label from the main node (prefer m1core:simulationTitle, fallback to rdfs:label)
const label = (
  mainNode['m1core:simulationTitle'] || 
  (mainNode['rdfs:label'] || '').replace(/\s*\([^)]+\)\s*$/, '').trim()
) || '';
```

### 3. `migrate_simulation_titles.py` (nouveau)

✅ **Script de migration interactif** pour ajouter `m1core:simulationTitle` aux instances existantes

---

## Procédure de migration

### Étape 1 : Tester en mode dry-run

```bash
python migrate_simulation_titles.py --dry-run
```

Ceci va scanner toutes les instances et afficher ce qui serait modifié **sans toucher aux fichiers**.

### Étape 2 : Exécuter la migration interactive

```bash
python migrate_simulation_titles.py
```

Pour chaque instance avec simulation :
1. Le script affiche le `rdfs:label` actuel
2. Il suggère un titre nettoyé (sans préfixes "TSCG M0", etc.)
3. Tu peux :
   - **Appuyer sur Entrée** → utiliser la suggestion
   - **Taper un titre personnalisé** → utiliser ton titre
   - **Taper 's'** → sauter cette instance

### Étape 3 : Régénérer la galerie

```bash
node generate_index.js
```

Le script utilisera maintenant `m1core:simulationTitle` si présent, sinon il fallback sur `rdfs:label`.

---

## Options du script de migration

```
Options:
  --root <path>    Spécifier la racine du repo (auto-détecté par défaut)
  --dry-run        Prévisualiser sans modifier les fichiers
  --help           Afficher l'aide
```

---

## Exemples de titres à corriger

Selon ton retour initial :

| Instance | rdfs:label actuel | m1:simulationTitle souhaité |
|----------|-------------------|----------------------------|
| TrophicPyramid | "TSCG M0 Trophic Pyramid Poclet" | "Trophic Pyramid" |
| KindlebergerMinsky | "Kindleberger-Minsky Financial Crisis Cycle" | "Kindleberger-Minsky Financial Bubble" |
| NuclearReactorsTypology | "TSCG M0 Nuclear Reactor Typology Poclet" | "Nuclear Reactor Typology" |

Le script suggérera automatiquement ces titres nettoyés.

---

## Validation

Après migration, vérifie que :
1. ✅ Les fichiers JSON-LD sont toujours valides (pas de corruption UTF-8)
2. ✅ `node generate_index.js` produit les titres corrects
3. ✅ La galerie affiche les nouveaux titres courts

---

## Notes techniques

- **Encodage** : Le script Python utilise `ensure_ascii=False` pour préserver UTF-8
- **Backup** : Considère faire un `git commit` avant la migration
- **Rollback** : Si problème, `git checkout -- instances/` annule les changements
- **Compatibilité** : Si `m1core:simulationTitle` est absent, `generate_index.js` utilise `rdfs:label` (rétro-compatible)

---

## Architecture

```
M3_GenesisSpace
    ↓ (defines ontology types)
M1_CoreConcepts
    ↓ (defines m1core:simulationTitle property)
M0_*.jsonld
    ↓ (uses m1core:simulationTitle for display)
generate_index.js
    → reads m1core:simulationTitle
    → generates index.html
```

La propriété est définie au niveau M1 car elle décrit les instances M0 (cohérence architecturale).

---

## Contact

En cas de problème, contacte Michel (Echopraxium) ou consulte la documentation TSCG.
