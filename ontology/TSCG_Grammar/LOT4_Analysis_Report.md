# Analyse Comparative - Lot 4 (4 M0 Poclets)

**Fichiers analysés :**
1. `M0_Poclet_NakamotoConsensus.jsonld`
2. `M0_NuclearReactorTypology.jsonld`
3. `M0_PhaseTransition.jsonld`
4. `M0_PlateTectonics.jsonld`

**Total cumulé :** 17 M0 analysés (Lots 1-4)  
**Couverture corpus :** 17/24 = **71%** 🎯

---

## 🎉 MASSE CRITIQUE DÉPASSÉE ! (71% corpus)

Avec 17 M0, la grammaire commune est maintenant **statistiquement robuste**.

---

## ✅ CONVERGENCES STABLES (lots 1-4)

### Métadonnées universelles

| Propriété | Présence | Statut |
|-----------|----------|--------|
| `dcterms:creator` | 17/17 = **100%** | ✅ **OBLIGATOIRE** |
| `dcterms:created` | 17/17 = **100%** | ✅ **OBLIGATOIRE** |
| `owl:versionInfo` | 14/17 = **82%** | ✅ **OBLIGATOIRE** |
| `m2:changelog` | 13/17 = **76%** | ✅ **RECOMMANDÉ** |
| `owl:imports` | 13/17 = **76%** | ✅ **RECOMMANDÉ** |
| `m0:domain` | 14/17 = **82%** | ✅ **RECOMMANDÉ** |

### Propriété label/comment

| Propriété | Présence | Statut |
|-----------|----------|--------|
| `rdfs:label` | 11/17 = **65%** | ⚠️ **MAJORITAIRE** (imposer ?) |
| `dcterms:title` | 6/17 = **35%** | ⚠️ **MINORITAIRE** (interdire ?) |
| `rdfs:comment` | 13/17 = **76%** | ✅ **STANDARD** |
| `dcterms:description` | 4/17 = **24%** | ⚠️ **MINORITAIRE** |

---

## ❌ DIVERGENCES CRITIQUES PERSISTANTES

### 1. @type au niveau ontologie

| Fichier LOT 4 | @type | Statut |
|---------------|-------|--------|
| NakamotoConsensus | `"m0:Poclet"` | ❌ **Erreur majeure** (ni Ontology ni NamedIndividual) |
| **NuclearReactorTypology** | `["owl:Ontology"]` | ✅ **CONFORME** |
| **PhaseTransition** | `"owl:Ontology"` | ✅ **CONFORME** |
| **PlateTectonics** | `"owl:Ontology"` | ✅ **CONFORME** |

**Bilan Lot 4 :** 3/4 conformes (75%)  
**Bilan cumulé (17 M0) :** 10/17 = **59% conformes**

→ **TENDANCE POSITIVE** : progression de 54% (lot 3) à 59%

### 2. m3:ontologyType (AMÉLIORATION SIGNIFICATIVE !)

| Fichier LOT 4 | Déclaration |
|---------------|-------------|
| NakamotoConsensus | ❌ Absent |
| **NuclearReactorTypology** | ✅ `m3:ontologyType: {"@id": "m3:Poclet"}` **CONFORME** |
| **PhaseTransition** | ✅ `m3:ontologyType: {"@id": "m3:Poclet"}` **CONFORME** |
| **PlateTectonics** | ✅ `m3:ontologyType: {"@id": "m3:Poclet"}` **CONFORME** |

**Bilan Lot 4 :** 3/4 conformes (75%) 🎉  
**Bilan cumulé (17 M0) :** 5/17 = **29% conformes**

→ **AMÉLIORATION MAJEURE** : +15% (de 15% lot 3 à 29% lot 4) !

### 3. Scores ASFID/REVOI

| Fichier LOT 4 | ASFID | REVOI |
|---------------|-------|-------|
| NakamotoConsensus | ❌ Absent (mention "5/5 ASFID" mais pas de structure) | ❌ Absent (mention "ORIVE" obsolète) |
| **NuclearReactorTypology** | ✅ Compact | ✅ Compact |
| PhaseTransition | ❌ Absent | ❌ Absent |
| PlateTectonics | ❌ Absent | ❌ Absent |

**Bilan Lot 4 :** 1/4 ont des scores  
**Bilan cumulé (17 M0) :** 7/17 = **41% ont des scores**

---

## 🆕 Nouveaux patterns identifiés (Lot 4)

### 1. @type: "m0:Poclet" (NakamotoConsensus)
**Nouvelle erreur détectée :** ni `owl:Ontology` ni `owl:NamedIndividual`, mais directement `m0:Poclet`

### 2. Instance avec double @type (PlateTectonics)
```json
"@type": ["owl:NamedIndividual", "owl:Class"]
```
→ Utilise à la fois NamedIndividual ET Class dans l'instance

### 3. Namespace tscg:* persistent (PhaseTransition)
```json
"tscg:domain": "Physical Chemistry / Thermodynamics",
"tscg:namespace": "m0:PhaseTransition",
"@type": "tscg:Poclet"  // dans instance
```
→ **VIOLATION** (2e occurrence après BloodPressureControl)

### 4. URL @base incorrecte (NuclearReactorTypology)
```json
"@base": "https://raw.githubusercontent.com/aladas-org/cryptocalc/master/ontology/"
```
→ Pointe vers `aladas-org/cryptocalc` au lieu de `Echopraxium/tscg`

### 5. Creator variations
- Majorité : "Echopraxium with the collaboration of Claude AI"
- NakamotoConsensus : "Echopraxium with Claude Sonnet 4.6"

### 6. m2:changelog format objet (PlateTectonics)
```json
"m2:changelog": {
  "v1_1_0": { "date": ..., "description": ... }
}
```
→ Format objet (comme KindlebergerMinsky) au lieu d'array

---

## 🚨 Violations Lot 4 à corriger

### M0_Poclet_NakamotoConsensus.jsonld
**Priorité :** 🔴 Majeur

| Violation | Correction |
|-----------|------------|
| ❌ `@type: "m0:Poclet"` | → `@type: "owl:Ontology"` |
| ❌ Pas de `m3:ontologyType` | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ `dcterms:title/description` | → `rdfs:label/comment` |
| ❌ `dcterms:creator: "Echopraxium with Claude Sonnet 4.6"` | → "Echopraxium with the collaboration of Claude AI" |
| ⚠️ Mention "ORIVE" obsolète | → Utiliser "REVOI" |

### M0_NuclearReactorTypology.jsonld
**Priorité :** ⚠️ Mineur (quasi-conforme !)

| Violation | Correction |
|-----------|------------|
| ❌ `@base: aladas-org/cryptocalc` | → `Echopraxium/tscg` |
| ❌ `dcterms:title/description` | → `rdfs:label/comment` |

### M0_PhaseTransition.jsonld
**Priorité :** 🔴 Majeur (namespace tscg)

| Violation | Correction |
|-----------|------------|
| ❌ Namespace `tscg:*` | → Renommer en `m0:*` |
| ❌ `tscg:domain`, `tscg:namespace`, etc. | → `m0:domain`, etc. |
| ❌ Instance `@type: "tscg:Poclet"` | → `m3:Poclet` ou supprimer |

### M0_PlateTectonics.jsonld
**Priorité :** ⚠️ Mineur

| Violation | Correction |
|-----------|------------|
| ❌ `dcterms:title/description` | → `rdfs:label/comment` |
| ❌ `m2:changelog` objet | → Convertir en array |
| ⚠️ Instance `@type: ["owl:NamedIndividual", "owl:Class"]` | → Valider pattern |

---

## 📊 Statistiques cumulées (17 M0)

### @type Ontology
- ✅ `owl:Ontology` : 10/17 = **59%**
- ❌ `owl:NamedIndividual` : 6/17 = **35%**
- ❌ `m0:Poclet` : 1/17 = **6%** (nouveau)

### m3:ontologyType
- ✅ Correct : 5/17 = **29%** (+15% vs lot 3 !)
- ❌ Incorrect/Absent : 12/17 = **71%**

### owl:versionInfo
- ✅ Présent : 14/17 = **82%**
- ❌ Absent/m0:version : 3/17 = **18%**

### rdfs:label vs dcterms:title
- ✅ `rdfs:label` : 11/17 = **65%**
- ❌ `dcterms:title` : 6/17 = **35%**

### rdfs:comment vs dcterms:description
- ✅ `rdfs:comment` : 13/17 = **76%**
- ❌ `dcterms:description` : 4/17 = **24%**

### Scores ASFID/REVOI
- ✅ Présents : 7/17 = **41%**
- ❌ Absents : 10/17 = **59%**

### Namespace tscg:
- ✅ Conformes (pas de tscg) : 15/17 = **88%**
- ❌ Violation : 2/17 = **12%** (BloodPressure + PhaseTransition)

### m2:ontologyCategory
- ✅ Conformes (pas de m2:ontologyCategory) : 12/17 = **71%**
- ❌ Violation : 5/17 = **29%**

---

## 🎯 GRAMMAIRE FINALE ÉMERGENTE (seuil ≥70%)

### ✅ CONSENSUS UNIVERSEL (≥90%)
1. `dcterms:creator` (17/17 = 100%)
2. `dcterms:created` (17/17 = 100%)

### ✅ CONSENSUS FORT (70-89%)
3. `owl:versionInfo` (14/17 = 82%)
4. `m0:domain` (14/17 = 82%)
5. `m2:changelog` (13/17 = 76%)
6. `owl:imports` (13/17 = 76%)
7. `rdfs:comment` (13/17 = 76%)

### ⚠️ MAJORITAIRE (60-69%)
8. `rdfs:label` (11/17 = 65%) → **Imposer malgré 65%** (vs dcterms:title 35%)

### ⚠️ À NORMALISER (< 60%)
- `@type: owl:Ontology` (59%) → **À IMPOSER**
- `m3:ontologyType` (29%) → **À IMPOSER** (amélioration +15% mais encore faible)
- Scores ASFID/REVOI (41%) → **RECOMMANDÉ** (non obligatoire)

---

## 💡 Recommandations pour SHACL v0.3

### Contraintes confirmées (Lot 4)

1. **rdfs:label obligatoire** (65% vs 35% dcterms:title)
   - Seuil pas atteint (70%) mais majorité claire

2. **Interdire @type: "m0:Poclet"** (nouveau cas)
   - Seule valeur valide : `owl:Ontology`

3. **Interdire namespace tscg:* partout** (2/17 violations)
   - PhaseTransition utilise massivement `tscg:*`

4. **@base URL** : Imposer `Echopraxium/tscg`
   - NuclearReactorTypology pointe vers `aladas-org/cryptocalc`

5. **dcterms:creator** : Format canonique strict
   - "Echopraxium with the collaboration of Claude AI"
   - Rejeter variantes ("Claude Sonnet 4.6", etc.)

### Nouvelles découvertes

1. **Amélioration m3:ontologyType** : +15% (de 15% à 29%)
   - Lot 4 montre 75% conformité (3/4)
   - Tendance très positive !

2. **Namespace tscg:** limité à 2 M0 (12% violation)
   - BloodPressureControl + PhaseTransition
   - Problème contenu, pas généralisé

3. **m2:changelog objet** : 2 occurrences
   - KindlebergerMinsky + PlateTectonics
   - Minoritaire (2/13 = 15%), imposer array

---

## 🏆 M0 quasi-conformes identifiés (Lot 4)

### NuclearReactorTypology 🥈
**Presque parfait !** Seulement 2 ajustements :
- ✏️ Corriger @base URL
- ✏️ dcterms:title → rdfs:label

### PhaseTransition
**Structure correcte MAIS namespace tscg:*** :
- ✅ `@type: owl:Ontology`
- ✅ `m3:ontologyType` correct
- ❌ Utilise `tscg:*` partout

---

## 📈 Progression conformité (lots 1-4)

| Lot | M0 analysés | % m3:ontologyType conforme |
|-----|-------------|----------------------------|
| Lot 1 | 5 | 20% (1/5) |
| Lot 2 | 4 | 0% (0/4) |
| Lot 3 | 4 | 25% (1/4) |
| **Lot 4** | **4** | **75% (3/4)** 🎉 |

**TENDANCE TRÈS POSITIVE** : Les M0 récents sont mieux alignés !

---

## ❓ Questions pour Michel

1. **@base URL** : NuclearReactorTypology pointe vers `aladas-org/cryptocalc`. Erreur ou ancien repo ?

2. **Instance @type mixte** : PlateTectonics utilise `["owl:NamedIndividual", "owl:Class"]`. Pattern valide ?

3. **m2:changelog objet vs array** : 2 M0 utilisent format objet (KindlebergerMinsky, PlateTectonics). Acceptable ou imposer array ?

4. **Scores ASFID/REVOI** : Seulement 41% ont des scores. Obligatoires ou optionnels ?

---

**MASSE CRITIQUE ATTEINTE** : Avec 71% du corpus, la grammaire est statistiquement robuste ! Les patterns stables (≥70%) sont maintenant clairs.

**Prêt pour Lot 5 ?** Ou on finalise SHACL v0.3 maintenant ?
