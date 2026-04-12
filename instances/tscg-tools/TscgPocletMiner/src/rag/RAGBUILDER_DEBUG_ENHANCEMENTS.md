# RagBuilder.js - Debug Enhancements

**Date:** 2026-04-06  
**Changes:** Added depth tracking and root directory listing

## 🔧 Modifications apportées

### 1. **Paramètre depth dans _walkDir()**

```javascript
// AVANT
_walkDir(dir, result) {
  // ...
}

// APRÈS
_walkDir(dir, result, depth = 0) {
  // Warn about deep directories
  if (depth > 5) {
    console.log(`[WARN] Deep directory (depth ${depth}): ${path.relative(this._root, dir)}`);
  }
  // ...
  this._walkDir(full, result, depth + 1);  // Récursion avec depth+1
}
```

### 2. **Liste des dossiers racines dans _collectFiles()**

```javascript
_collectFiles() {
  const result = [];
  console.log('[DEBUG] Starting scan from:', this._root);
  
  // ← AJOUT: Liste les dossiers racines
  const rootDirs = fs.readdirSync(this._root, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);
  console.log('[DEBUG] Root directories:', rootDirs);
  
  this._walkDir(this._root, result, 0);  // ← Passe depth=0
  // ...
}
```

## 📊 Logs attendus

### Démarrage du scan
```
[DEBUG] Starting scan from: E:\_00_Michel\_00_Lab\_00_GitHub\tscg
[DEBUG] Root directories: [
  '.claude', '.git', 'api_key', 'cli_tools',
  'docs', 'instances', 'node_modules', 'ontology',
  'src', '_archives', '_protos'
]
```

### Si dossiers profonds (depth > 5)
```
[WARN] Deep directory (depth 6): src/some/very/deep/nested/path
[WARN] Deep directory (depth 7): src/some/very/deep/nested/path/more
```

### Fichiers .js skippés
```
[SKIP JS] cli_tools/generate_index-html/_archives/generate_index.js (matched: _archives/)
```

### Résumé final
```
[DEBUG] Total files collected: 472
[DEBUG] Files by extension: { md: 203, txt: 31, js: 48, jsonld: 89, html: 21, py: 80 }
```

## 🎯 But du debug

### Identifier pourquoi 90 fichiers manquent vs Python

**Python** : 562 fichiers  
**JavaScript** : 472 fichiers  
**Différence** : 90 fichiers

Hypothèses testées :
1. ✅ Dossiers racines manquants → Non (tous présents)
2. 🔍 Dossiers très profonds ignorés ? → À tester avec depth
3. 🔍 Permissions d'accès différentes ? → Silencieusement ignoré par try-catch
4. 🔍 Encodage de noms de fichiers ? → Caractères spéciaux/accents

## 🔬 Prochaines étapes

1. **Relancer l'app** et rebuilder le RAG
2. **Vérifier les logs** pour des `[WARN] Deep directory`
3. **Comparer manuellement** le nombre de fichiers `.md` :
   ```bash
   dir /s /b *.md | find /c /v ""
   ```
   Python dit 228, JS dit 203 → vérifier le chiffre réel

4. **Si aucun warning de profondeur**, le problème est ailleurs :
   - Permissions de dossiers
   - Encodage de noms
   - Symlinks

## ✅ Fichier livré

**RagBuilder.js** avec :
- Paramètre `depth` dans `_walkDir()`
- Warning pour dossiers profonds (depth > 5)
- Liste des dossiers racines au démarrage
- Appel initial avec `depth = 0`

Remplace le fichier dans `src/rag/RagBuilder.js` et relance l'application !
