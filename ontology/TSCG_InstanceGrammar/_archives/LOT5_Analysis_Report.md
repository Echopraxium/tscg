# Analyse Comparative - Lot 5 (4 M0 Poclets)

**Fichiers analysés :**
1. `M0_RAAS.jsonld`
2. `M0_TPACK.jsonld`
3. `M0_Transistor.jsonld`
4. `M0_TrophicPyramid.jsonld`

**Total cumulé :** 21 M0 analysés (Lots 1-5)  
**Couverture corpus :** 21/24 = **88%** 🎯

---

## 🎊 GRAMMAIRE FINALE ATTEINTE ! (88% corpus)

Avec 21 M0, la grammaire commune est **définitive et statistiquement robuste**.

---

## ✅ CONVERGENCES STABLES (lots 1-5)

### Métadonnées universelles

| Propriété | Présence | Statut |
|-----------|----------|--------|
| `dcterms:creator` | 21/21 = **100%** | ✅ **OBLIGATOIRE** |
| `dcterms:created` | 21/21 = **100%** | ✅ **OBLIGATOIRE** |
| `owl:versionInfo` | 18/21 = **86%** | ✅ **OBLIGATOIRE** |
| `m2:changelog` | 16/21 = **76%** | ✅ **RECOMMANDÉ** |
| `owl:imports` | 16/21 = **76%** | ✅ **RECOMMANDÉ** |
| `m0:domain` | 18/21 = **86%** | ✅ **RECOMMANDÉ** |

### Propriété label/comment

| Propriété | Présence | Statut |
|-----------|----------|--------|
| `rdfs:label` | 15/21 = **71%** | ✅ **STANDARD** (seuil atteint !) |
| `dcterms:title` | 6/21 = **29%** | ⚠️ **MINORITAIRE** (interdire) |
| `rdfs:comment` | 17/21 = **81%** | ✅ **STANDARD** |
| `dcterms:description` | 4/21 = **19%** | ⚠️ **MINORITAIRE** (interdire) |

---

## ❌ DIVERGENCES CRITIQUES PERSISTANTES

### 1. @type au niveau ontologie

| Fichier LOT 5 | @type | Statut |
|---------------|-------|--------|
| RAAS | `["owl:NamedIndividual"]` | ❌ Erreur |
| TPACK | `"owl:NamedIndividual"` | ❌ Erreur |
| Transistor | `["owl:NamedIndividual"]` | ❌ Erreur |
| **TrophicPyramid** | `"owl:Ontology"` | ✅ **CONFORME** |

**Bilan Lot 5 :** 1/4 conformes (25%)  
**Bilan cumulé (21 M0) :** 11/21 = **52% conformes**

→ **RECUL** : de 59% (lot 4) à 52%

### 2. m3:ontologyType

| Fichier LOT 5 | Déclaration |
|---------------|-------------|
| **RAAS** | ✅ `m3:ontologyType: {"@id": "m3:Poclet"}` **CONFORME** |
| TPACK | ❌ Absent + `rdf:type: "m0:Poclet"` |
| **Transistor** | ✅ `m3:ontologyType: {"@id": "m3:Poclet"}` **CONFORME** |
| **TrophicPyramid** | ✅ `m3:ontologyType: {"@id": "m3:Poclet"}` **CONFORME** |

**Bilan Lot 5 :** 3/4 conformes (75%)  
**Bilan cumulé (21 M0) :** 8/21 = **38% conformes**

→ **AMÉLIORATION** : +9% (de 29% lot 4 à 38% lot 5)

### 3. Scores ASFID/REVOI

| Fichier LOT 5 | ASFID | REVOI |
|---------------|-------|-------|
| **RAAS** | ✅ Compact | ✅ Compact |
| TPACK | ❌ Absent | ❌ Absent |
| **Transistor** | ✅ Compact | ✅ Compact |
| **TrophicPyramid** | ✅ Dans territorySpace | ✅ Dans mapSpace |

**Bilan Lot 5 :** 3/4 ont des scores  
**Bilan cumulé (21 M0) :** 10/21 = **48% ont des scores**

---

## 🆕 Patterns identifiés (Lot 5)

### 1. @base URL incorrecte (RAAS)
```json
"@base": "https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/"
```
→ 2e occurrence (après NuclearReactorTypology)

### 2. m2:changelog format objet (TrophicPyramid)
```json
"m2:changelog": {
  "v2.1.0": { "date": ..., "description": ... },
  "v2.0.0": { ... },
  "v1.0.0": { ... }
}
```
→ 3e occurrence (KindlebergerMinsky, PlateTectonics, TrophicPyramid)

### 3. Scores dans territorySpace/mapSpace (TrophicPyramid)
```json
"m0:territorySpace": {
  "m0:asfidState": { "A": 0.97, ... }
},
"m0:mapSpace": {
  "m0:reviState": { "R": 0.85, ... }
}
```
→ Format différent (pas compact au niveau ontologie)

### 4. Instance avec double @type (TrophicPyramid)
```json
"@type": ["owl:NamedIndividual", "owl:Class"]
```
→ 2e occurrence (après PlateTectonics)

---

## 🚨 Violations Lot 5 à corriger

### M0_RAAS.jsonld
**Priorité :** 🔴 Majeur

| Violation | Correction |
|-----------|------------|
| ❌ `@type: ["owl:NamedIndividual"]` | → `@type: "owl:Ontology"` |
| ❌ `@base: aladas-org/cryptocalc` | → `Echopraxium/tscg` |

### M0_TPACK.jsonld
**Priorité :** 🔴 Majeur

| Violation | Correction |
|-----------|------------|
| ❌ `@type: "owl:NamedIndividual"` | → `@type: "owl:Ontology"` |
| ❌ `rdf:type: "m0:Poclet"` | → Supprimer (remplacé par m3:ontologyType) |
| ❌ Pas de `m3:ontologyType` | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |

### M0_Transistor.jsonld
**Priorité :** ⚠️ Mineur (quasi-conforme)

| Violation | Correction |
|-----------|------------|
| ❌ `@type: ["owl:NamedIndividual"]` | → `@type: "owl:Ontology"` |

### M0_TrophicPyramid.jsonld
**Priorité :** ⚠️ Mineur

| Violation | Correction |
|-----------|------------|
| ❌ `dcterms:title/description` | → `rdfs:label/comment` |
| ❌ `m2:changelog` objet | → Convertir en array |
| ⚠️ Scores dans territorySpace/mapSpace | → Format valide mais différent |

---

## 📊 Statistiques cumulées (21 M0)

### @type Ontology
- ✅ `owl:Ontology` : 11/21 = **52%**
- ❌ `owl:NamedIndividual` : 9/21 = **43%**
- ❌ `m0:Poclet` : 1/21 = **5%**

### m3:ontologyType
- ✅ Correct : 8/21 = **38%** (+9% vs lot 4)
- ❌ Incorrect/Absent : 13/21 = **62%**

### owl:versionInfo
- ✅ Présent : 18/21 = **86%**
- ❌ Absent/m0:version : 3/21 = **14%**

### rdfs:label vs dcterms:title
- ✅ `rdfs:label` : 15/21 = **71%** (seuil atteint !)
- ❌ `dcterms:title` : 6/21 = **29%**

### rdfs:comment vs dcterms:description
- ✅ `rdfs:comment` : 17/21 = **81%**
- ❌ `dcterms:description` : 4/21 = **19%**

### Scores ASFID/REVOI
- ✅ Présents : 10/21 = **48%**
- ❌ Absents : 11/21 = **52%**

### Namespace tscg:
- ✅ Conformes (pas de tscg) : 19/21 = **90%**
- ❌ Violation : 2/21 = **10%** (BloodPressure + PhaseTransition)

### m2:ontologyCategory
- ✅ Conformes : 16/21 = **76%**
- ❌ Violation : 5/21 = **24%**

### @base URL
- ✅ Correct : 19/21 = **90%**
- ❌ Incorrect (aladas-org/cryptocalc) : 2/21 = **10%** (RAAS + NuclearReactorTypology)

---

## 🎯 GRAMMAIRE FINALE (21 M0, seuil ≥70%)

### ✅ CONSENSUS UNIVERSEL (≥90%)
1. `dcterms:creator` (21/21 = **100%**)
2. `dcterms:created` (21/21 = **100%**)
3. Interdiction `tscg:*` (19/21 = **90%**)
4. @base URL correct (19/21 = **90%**)

### ✅ CONSENSUS FORT (70-89%)
5. `owl:versionInfo` (18/21 = **86%**)
6. `m0:domain` (18/21 = **86%**)
7. `rdfs:comment` (17/21 = **81%**)
8. `m2:changelog` (16/21 = **76%**)
9. `owl:imports` (16/21 = **76%**)
10. `m2:ontologyCategory` absent (16/21 = **76%**)
11. **`rdfs:label` (15/21 = 71%)** ← **SEUIL ATTEINT !**

### ⚠️ MAJORITAIRE (50-69%)
12. `@type: owl:Ontology` (11/21 = **52%**) → **À IMPOSER** (tendance négative)

### ⚠️ À NORMALISER (< 50%)
- `m3:ontologyType` (38%) → **À IMPOSER** (amélioration +9% mais encore faible)
- Scores ASFID/REVOI (48%) → **RECOMMANDÉ** (non obligatoire)

---

## 💡 Recommandations pour SHACL v0.3

### Contraintes confirmées DÉFINITIVES (≥70%)

1. **dcterms:creator** = "Echopraxium with the collaboration of Claude AI" (100%)
2. **dcterms:created** format YYYY-MM-DD (100%)
3. **Interdire tscg:*** (90%)
4. **@base** = `Echopraxium/tscg` (90%)
5. **owl:versionInfo** semver obligatoire (86%)
6. **m0:domain** obligatoire (86%)
7. **rdfs:comment** obligatoire (81%)
8. **m2:changelog** recommandé (76%)
9. **owl:imports** recommandé (76%)
10. **Interdire m2:ontologyCategory** (76%)
11. **rdfs:label obligatoire** (71%) ← **NOUVEAU : SEUIL ATTEINT !**

### Contraintes à imposer malgré < 70%

12. **@type: owl:Ontology** (52%) → Imposer car confusion @type massive (43% NamedIndividual)
13. **m3:ontologyType** (38%) → Imposer car propriété architecturale critique (amélioration +9%)

### Format m2:changelog

**Variantes détectées :**
- Array (18/21 = 86%) ← **MAJORITAIRE**
- Objet (3/21 = 14%) : KindlebergerMinsky, PlateTectonics, TrophicPyramid

→ **Imposer format array**

---

## 📈 Évolution m3:ontologyType (lots 1-5)

| Lot | M0 analysés | % conforme m3:ontologyType |
|-----|-------------|----------------------------|
| Lot 1 | 5 | 20% (1/5) |
| Lot 2 | 4 | 0% (0/4) |
| Lot 3 | 4 | 25% (1/4) |
| Lot 4 | 4 | 75% (3/4) 🎉 |
| **Lot 5** | **4** | **75% (3/4)** ✅ |

**Tendance stable à 75%** pour les M0 récents !

---

## 🏆 M0 quasi-conformes (Lot 5)

### Transistor 🥈
**Presque parfait !** Seulement 1 ajustement :
- ✏️ `@type: NamedIndividual` → `owl:Ontology`
- ✅ m3:ontologyType correct
- ✅ Scores ASFID/REVOI compacts
- ✅ m2:changelog array

### TrophicPyramid 🥉
**Très proche !** 2-3 ajustements mineurs :
- ✅ @type: owl:Ontology
- ✅ m3:ontologyType correct
- ✏️ dcterms:title → rdfs:label
- ✏️ m2:changelog objet → array

---

## 🎉 CONCLUSION : Grammaire robuste et définitive

**Avec 88% du corpus (21/24 M0) :**

### ✅ Patterns stables identifiés (≥70%)
- 11 contraintes obligatoires ou fortement recommandées
- rdfs:label franchit le seuil à 71% !
- @base URL et tscg:* violations limitées à 10%

### ⚠️ Points de confusion à normaliser
- `@type: owl:Ontology` (52%) → Imposer malgré <70% (confusion massive NamedIndividual 43%)
- `m3:ontologyType` (38%) → Imposer malgré <70% (tendance positive, critique architectural)

### 📊 Tendances encourageantes
- M0 récents (lots 4-5) montrent 75% conformité m3:ontologyType
- namespace tscg:* quasi-éliminé (90% propres)
- @base URL généralisé (90% correct)

**GRAMMAIRE PRÊTE POUR SHACL v0.3 FINAL !** 🚀
