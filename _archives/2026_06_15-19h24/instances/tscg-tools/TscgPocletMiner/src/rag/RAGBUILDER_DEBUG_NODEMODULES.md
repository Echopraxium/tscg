# RagBuilder.js - Debug node_modules Exclusion

**Date:** 2026-04-06  
**Purpose:** Track which files are being skipped due to node_modules pattern

## 🔧 Modification

Ajout d'un log dans `_walkDir()` pour tracer **tous** les chemins contenant `node_modules` :

```javascript
// Debug pour node_modules
if (rel.includes('node_modules')) {
  console.log(`[SKIP node_modules] ${rel.substring(0, 100)}`);
}
```

**Position** : Juste **avant** le test `if (IGNORED_PATH_FRAGMENTS.some(...))` 

## 📊 Logs attendus

### Si l'exclusion fonctionne correctement :

```
[SKIP node_modules] node_modules/@electron/get/README.md
[SKIP node_modules] node_modules/boolean/README.md
[SKIP node_modules] instances/tscg-tools/TscgPocletMiner/node_modules/@electron/get/README.md
[SKIP node_modules] instances/tscg-tools/TscgPocletMiner/node_modules/boolean/README.md
...
(89 lignes pour node_modules racine + 89 lignes pour instances)
```

### Ce qu'on veut vérifier :

1. **Tous les fichiers dans node_modules sont-ils détectés ?**
   - Devrait afficher ~178 lignes `[SKIP node_modules]`

2. **Sont-ils effectivement exclus ?**
   - Le comptage final devrait exclure ces fichiers
   - `[DEBUG] Total files collected:` devrait être ~231-240 (pas 475)

## 🎯 Test à faire

1. **Remplacer** `src/rag/RagBuilder.js`
2. **Relancer** l'application
3. **Build RAG**
4. **Vérifier** dans le terminal :
   - Nombre de lignes `[SKIP node_modules]`
   - Nombre final dans `[DEBUG] Total files collected:`

## 📊 Résultats attendus

### Si l'exclusion fonctionne (✅) :
```
[DEBUG] Starting scan from: ...
[SKIP node_modules] node_modules/...  (×178 lignes environ)
[DEBUG] Total files collected: ~231
[DEBUG] Files by extension: { md: ~228, ... }
```

### Si l'exclusion ne fonctionne PAS (❌) :
```
[DEBUG] Starting scan from: ...
[SKIP node_modules] node_modules/...  (×178 lignes environ)
[DEBUG] Total files collected: 475  ← Les node_modules sont quand même indexés !
[DEBUG] Files by extension: { md: 206, ... }
```

Dans ce cas, le pattern est détecté mais **pas appliqué correctement** → bug dans la logique du `continue`.

## 🔍 Diagnostic possible

Si les logs montrent `[SKIP node_modules]` MAIS que les fichiers sont quand même comptés :

→ Le `continue` se produit **après** que le fichier soit ajouté à `result[]`

→ Vérifier l'ordre des instructions dans `_walkDir()` :
1. Le test doit être fait AVANT `result.push(full)`
2. Le `continue` doit être exécuté pour empêcher l'ajout

## 📦 Fichier livré

**RagBuilder.js** avec debug node_modules tracking.

Remplace le fichier, relance, et envoie-moi les logs du terminal ! 🔍
