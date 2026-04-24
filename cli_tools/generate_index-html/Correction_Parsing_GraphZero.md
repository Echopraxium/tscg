# Correction Parsing JSON-LD : Règle @graph[0]

## 🎯 Principe Simplifié

**Règle TSCG** : Le premier objet dans `@graph` (`@graph[0]`) est **TOUJOURS** la référence principale.

## ✅ Nouvelle Logique (Simplifiée)

```javascript
function parseJsonld(filePath) {
  const graph = raw['@graph'] || [raw];
  
  // @graph[0] = Nœud de référence (owl:Ontology avec métadonnées)
  const mainNode = graph[0];
  
  // Extraire depuis @graph[0]:
  const label   = mainNode['rdfs:label']
  const domain  = mainNode['m1:domain']  // Tableau
  const version = mainNode['owl:versionInfo']
  
  // Scores peuvent être dans d'autres nœuds (@graph[1], @graph[2]...)
  // → Parcourir tous les nœuds pour les trouver
  for (const node of graph) {
    if (node['m0:asfidScores']) asfid = ...
    if (node['m0:revoiScores']) revoi = ...
    if (node['m0:epistemicGap']) gap = ...
  }
}
```

## 📊 Exemple : M0_Triz.jsonld

```json
{
  "@graph": [
    {
      "@id": "m0triz:Triz_SystemicFramework",     // ← @graph[0]
      "@type": "owl:Ontology",
      "rdfs:label": "TRIZ — Theory of Inventive Problem Solving",
      "m1:domain": ["Systems Theory", "Systems Thinking"],
      "owl:versionInfo": "1.1.0"
    },
    {
      "@id": "m0triz:TRIZ_ASFID_Scores",          // ← @graph[1]
      "@type": "m3:eagle_eye:TerritorySpace",
      "rdfs:label": "TRIZ ASFID Scores (Eagle Eye — Territory)",
      "m3:eagle_eye:Attractor": 5.0,
      "m3:eagle_eye:Structure": 5.0,
      ...
    }
  ]
}
```

**Résultat avec la nouvelle logique** :
- **Label** : `"TRIZ — Theory of Inventive Problem Solving"` ← depuis `@graph[0]`
- **Domaine** : `"Systems Theory/Systems Thinking"` ← depuis `@graph[0]`
- **Version** : `"1.1.0"` ← depuis `@graph[0]`
- **Scores ASFID** : Trouvés dans `@graph[1]` via la boucle

## ❌ Ancienne Logique (Complexe)

L'ancienne logique cherchait :
1. Le nœud `owl:Ontology` pour le domaine
2. Un nœud non-Ontology pour les autres métadonnées
3. Préférait les nœuds avec `_Summary` dans leur `@id`
4. Multiples fallbacks et conditions

**Problème** : Pour Triz, ça prenait le label de `TRIZ_ASFID_Scores` au lieu de `Triz_SystemicFramework`.

## ✅ Avantages de la Nouvelle Logique

1. **Simple** : `@graph[0]` pour tout (sauf scores)
2. **Prévisible** : Toujours le même nœud
3. **Conforme** : Respecte la convention TSCG
4. **Robuste** : Pas de recherche complexe, pas de fallbacks multiples
5. **Correct** : Triz affiche maintenant "TRIZ — Theory of Inventive Problem Solving" ✓

## 📝 Résultats Attendus

Avant (incorrect) :
```
[Systems Theory/Systems Thinking] TRIZ ASFID Scores
```

Après (correct) :
```
[Systems Theory/Systems Thinking] TRIZ — Theory of Inventive Problem Solving
```

---

**Date** : 2026-04-24  
**Correction** : Parsing simplifié selon règle `@graph[0]`
