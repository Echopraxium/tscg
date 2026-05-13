# M0 Instances - Realignment Tracker
**Auteur:** Echopraxium with the collaboration of Claude AI  
**Date de création:** 2026-04-13  
**Dernière mise à jour:** 2026-04-13 (Lot 1 analysé)

---

## 📊 Statistiques globales

| Statut | Count | Pourcentage |
|--------|-------|-------------|
| ✅ Conforme | 1 | 4% |
| ⚠️ Réalignement mineur | 10 | 42% |
| 🔴 Réalignement majeur | 13 | 54% |
| **TOTAL POCLETS** | **24** | **100%** |

**+ 2 INSTANCES NON-POCLET à réaligner :**
- M0_VSM_Metaconcepts (SystemicFramework) → 🔴 Critique (ontologyCategory + ORIVE)
- M0_IChing (SymbolicSystemGrammar) → ⚠️ Mineur (@base + dcterms)

**Lots analysés :** 6/6 (Lot 1: 5 M0, Lot 2: 4 M0, Lot 3: 4 M0, Lot 4: 4 M0, Lot 5: 4 M0, Lot 6: 3 M0)  
**Couverture corpus :** 24/24 = **100%** 🎊 **CORPUS COMPLET** + 2 instances

**RÈGLE CRITIQUE :** Toutes les instances TSCG doivent utiliser `m3:ontologyType` avec valeurs : `m3:Poclet` (24), `m3:SystemicFramework` (1), `m3:SymbolicSystemGrammar` (1). `m2:ontologyCategory` est obsolète.

---

## 📋 Vue d'ensemble du réalignement

### Volume global de modifications (12 M0 à réaligner)

| Catégorie | Nb M0 | Nb modifications | Temps estimé |
|-----------|-------|------------------|--------------|
| ⚠️ **Mineur** | 4 | 12 (1-5 par M0) | ⏱️ 30-60 min |
| 🔴 **Majeur simple** | 6 | ~24 (3-4 par M0) | ⏱️ 2-3h |
| 🔴 **Majeur complexe** | 2 | 60+ (10-50+ par M0) | ⏱️ 2-3h |
| **TOTAL** | **12** | **~96** | **⏱️ 5-7h** |

### Répartition par type de modification

#### 🟢 Modifications SIMPLES (1 ligne à changer)
- `@type: owl:NamedIndividual` → `owl:Ontology` : **6 M0**
  - Kidneys, CellSignaling, Counterpoint, ExposureTriangle, FireTriangle, FourStrokeEngine
- `m0:version` → `owl:versionInfo` : **2 M0**
  - Counterpoint, FourStrokeEngine
- Supprimer `m2:ontologyCategory` : **5 M0**
  - ColorSynthesis, ComplexChemicalSynapse, KindlebergerMinsky, MtgColorWheel, FourStrokeEngine

#### 🟡 Modifications MOYENNES (2-5 lignes)
- `rdf:type: m3:Poclet` → `m3:ontologyType: {"@id": "m3:Poclet"}` : **5 M0**
  - CellSignaling, Counterpoint, ExposureTriangle, FireTriangle, FourStrokeEngine
- `dcterms:title/description` → `rdfs:label/comment` : **3 M0**
  - ColorSynthesis, ComplexChemicalSynapse, MtgColorWheel
- `m2:ontologyType` → `m3:ontologyType` : **1 M0**
  - ComplexChemicalSynapse

#### 🔴 Modifications COMPLEXES (restructuration)
- **BloodPressureControl** : 50+ propriétés `tscg:*` → `m0:*` (renommage massif)
- **ButterflyMetamorphosis** : 10+ classes custom `m0:*` à supprimer/reclasser
- **CellSignalingModes** : Restructuration components inline
- **KindlebergerMinsky** : Conversion `m2:changelog` objet → array

### 🎯 Stratégie de réalignement recommandée

#### **PHASE 1 - Quick wins** (4 M0, 1h)
1. M0_Kidneys (10 min)
2. M0_KindlebergerMinsky (15 min)
3. M0_ColorSynthesis_Federated (20 min)
4. M0_MtgColorWheel (20 min)

**→ Conformité : 38% (5/13)**

#### **PHASE 2 - Corrections standards** (6 M0, 2-3h)
5. M0_FireTriangle (25 min)
6. M0_ExposureTriangle (25 min)
7. M0_Counterpoint (25 min)
8. M0_FourStrokeEngine (25 min)
9. M0_CellSignalingModes (30 min)
10. M0_ComplexChemicalSynapse (30 min)

**→ Conformité : 85% (11/13)**

#### **PHASE 3 - Gros chantiers** (2 M0, 2-3h)
11. M0_ButterflyMetamorphosis (60-90 min)
12. M0_BloodPressureControl (60-90 min)

**→ Conformité : 100% (13/13)** ✅

---

## 🔴 Instances nécessitant un RÉALIGNEMENT MAJEUR

### 1. M0_BloodPressureControl.jsonld
**Priorité:** 🔥 CRITIQUE (violations namespace massives)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ Namespace `tscg:*` | Utilise `tscg:*` pour presque toutes les propriétés | Renommer en `m0:*` ou namespace standard |
| ❌ `tscg:dateCreated` | Au lieu de `dcterms:created` | → `dcterms:created` |
| ❌ `tscg:authors` | Au lieu de `dcterms:creator` | → `dcterms:creator` |
| ❌ `tscg:domain` | Au lieu de `m0:domain` | → `m0:domain` |
| ❌ `tscg:asfidScore` | Au lieu de `m0:asfidScores` | → `m0:asfidScores` (structure détaillée) |
| ❌ `tscg:oriveScore` | ORIVE obsolète + mauvais namespace | → `m0:revoiScores` |
| ❌ `tscg:epistemicGap` | Au lieu de `m0:epistemicGap` | → `m0:epistemicGap` |
| ❌ `tscg:EffectorSystem` | Type custom avec namespace tscg | → Utiliser GenericConcept M2 ou `m0:*` |
| ❌ Dizaines de propriétés `tscg:*` | feedbackType, mechanismType, etc. | → Renommer toutes en `m0:*` |

**Estimation effort:** 🔥🔥🔥 ÉLEVÉ (50+ propriétés à renommer)

---

### 2. M0_CellSignalingModes.jsonld
**Priorité:** 🔥 CRITIQUE (erreurs structurelles)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: "owl:NamedIndividual"` | Au niveau ontologie | → `@type: "owl:Ontology"` |
| ❌ `rdf:type: "m0:Poclet"` | Mauvaise déclaration type | → `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ⚠️ Components inline | Tous les components dans un array inline | → Séparer dans @graph (?) |
| ⚠️ Pas de scores ASFID/REVOI | Absents | → Ajouter `m0:asfidScores` et `m0:revoiScores` |

**Estimation effort:** 🔥🔥 MOYEN (restructuration architecture)

---

### 3. M0_ButterflyMetamorphosis.jsonld
**Priorité:** 🔥 ÉLEVÉ (violations multiples)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `m0:oriveMean` | ORIVE obsolète | → `m0:revoiScores/mean` |
| ❌ Définit `m0:Poclet` comme `owl:Class` | Classe custom interdite | → Supprimer, utiliser `m3:Poclet` |
| ❌ Définit `m0:DevelopmentalPole` comme `owl:Class` | Classe custom interdite | → Utiliser GenericConcept M2 |
| ❌ Définit 10+ classes custom `m0:*` | BicephalousPerspective, PocletValidation, etc. | → Supprimer ou reclasser |
| ⚠️ Marqueurs étranges | `m0:check_following_attributes:START/END` | → Clarifier usage ou supprimer |

**Estimation effort:** 🔥🔥 MOYEN-ÉLEVÉ (nettoyage classes custom)

---

### 4. M0_Counterpoint.jsonld (LOT 2)
**Priorité:** 🔥 ÉLEVÉ (erreurs type + ontologyType)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: "owl:NamedIndividual"` | Au niveau ontologie | → `@type: "owl:Ontology"` |
| ❌ `rdf:type: {"@id": "m3:Poclet"}` | Mauvaise déclaration | → `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ `m3:ontologyCategory` | Au lieu de `m3:ontologyType` | → `m3:ontologyType` |
| ❌ `m0:version` | Au lieu de `owl:versionInfo` | → `owl:versionInfo` |

**Estimation effort:** 🔥 MOYEN (4 propriétés à corriger)

---

### 5. M0_ExposureTriangle.jsonld (LOT 2)
**Priorité:** 🔥 ÉLEVÉ (erreurs type + ontologyType)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: "owl:NamedIndividual"` | Au niveau ontologie | → `@type: "owl:Ontology"` |
| ❌ `rdf:type: "m0:Poclet"` | Namespace m0 au lieu de m3 | → `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ Pas de `m3:ontologyType` | Absent | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ⚠️ Pas de scores ASFID/REVOI | Absents | → Ajouter `m0:asfidScores` et `m0:revoiScores` (?) |

**Estimation effort:** 🔥 MOYEN (3-4 propriétés + scores optionnels)

---

### 6. M0_ComplexChemicalSynapse.jsonld (LOT 2)
**Priorité:** ⚠️ MOYEN (erreurs mineures multiples)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `m2:ontologyType` | Au lieu de `m3:ontologyType` | → `m3:ontologyType` |
| ❌ `m2:ontologyCategory` | Propriété invalide (probable) | → Supprimer si présent |
| ❌ `dcterms:title` | Au lieu de `rdfs:label` | → `rdfs:label` |
| ❌ `dcterms:description` | Au lieu de `rdfs:comment` | → `rdfs:comment` (ou garder les deux ?) |
| ⚠️ Instance double | owl:NamedIndividual + m1:core:Poclet séparé | → Valider pattern avec Michel |
| ⚠️ Namespace `tscg:` dans @context | Pointe vers README.md | → Supprimer ou corriger |

**Estimation effort:** 🔥 FAIBLE-MOYEN (5-6 corrections simples)

---

### 8. M0_FireTriangle.jsonld (LOT 3)
**Priorité:** 🔴 ÉLEVÉ (erreurs type + manque version/scores)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: "owl:NamedIndividual"` | Au niveau ontologie | → `@type: "owl:Ontology"` |
| ❌ `rdf:type: ["m1:chemistry:Combustion", "m1:core:Poclet"]` | Mauvaise déclaration | → `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ Pas de `owl:versionInfo` | Absent | → Ajouter version semver |
| ⚠️ Pas de scores ASFID/REVOI | Absents | → Recommandé (optionnel ?) |

**Estimation effort:** 🔥 MOYEN (3 propriétés obligatoires + scores optionnels)

---

### 13. M0_Poclet_NakamotoConsensus.jsonld (LOT 4)
**Priorité:** 🔴 ÉLEVÉ (erreurs type + creator + ORIVE obsolète)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: "m0:Poclet"` | Ni Ontology ni NamedIndividual | → `@type: "owl:Ontology"` |
| ❌ Pas de `m3:ontologyType` | Absent | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ `dcterms:title/description` | Au lieu de rdfs:label/comment | → `rdfs:label/comment` |
| ❌ `dcterms:creator` | "Echopraxium with Claude Sonnet 4.6" | → "Echopraxium with the collaboration of Claude AI" |
| ⚠️ Mention "ORIVE" | Obsolète | → Utiliser "REVOI" |

**Estimation effort:** 🔥 MOYEN (5 propriétés à corriger)

---

### 14. M0_PhaseTransition.jsonld (LOT 4)
**Priorité:** 🔴 CRITIQUE (namespace tscg massif - 2e occurrence)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ Namespace `tscg:*` | Utilisé partout | → Renommer en `m0:*` |
| ❌ `tscg:domain`, `tscg:namespace`, etc. | Multiple propriétés | → `m0:domain`, etc. |
| ❌ Instance `@type: "tscg:Poclet"` | Dans instance séparée | → `m3:Poclet` ou supprimer |

**Estimation effort:** 🔥🔥 MOYEN-ÉLEVÉ (renommages multiples comme BloodPressure)

---

### 17. M0_RAAS.jsonld (LOT 5)
**Priorité:** 🔴 MOYEN (@type + @base)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: ["owl:NamedIndividual"]` | Au niveau ontologie | → `@type: "owl:Ontology"` |
| ❌ `@base: aladas-org/cryptocalc` | Pointe vers ancien repo | → `Echopraxium/tscg` |

**Estimation effort:** 🔥 FAIBLE (2 propriétés simples)

---

### 18. M0_TPACK.jsonld (LOT 5)
**Priorité:** 🔴 ÉLEVÉ (@type + ontologyType absent)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: "owl:NamedIndividual"` | Au niveau ontologie | → `@type: "owl:Ontology"` |
| ❌ `rdf:type: "m0:Poclet"` | Mauvaise déclaration | → Supprimer (remplacé par m3:ontologyType) |
| ❌ Pas de `m3:ontologyType` | Absent | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |

**Estimation effort:** 🔥 MOYEN (3 propriétés)

---

### 21. M0_VCO.jsonld (LOT 6)
**Priorité:** 🔴 ÉLEVÉ (ontologyType absent + changelog absent)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ Pas de `m3:ontologyType` | Omission complète | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ Pas de `m2:changelog` | Absent | → Ajouter (recommandé mais absence = 29%) |

**Estimation effort:** 🔥 FAIBLE (2 propriétés à ajouter)

---

### 22. M0_Yggdrasil.jsonld (LOT 6)
**Priorité:** 🔴 ÉLEVÉ (@base + ontologyType + dcterms + changelog)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ Pas de `m3:ontologyType` | Omission complète | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ `@base: aladas-org/cryptocalc` | Pointe vers ancien repo | → `Echopraxium/tscg` |
| ❌ `dcterms:title/description` | Au lieu de rdfs | → Supprimer (garder rdfs:label/comment) |
| ❌ `m0:changelog` objet | Format minoritaire | → Convertir en array |

**Estimation effort:** 🔥 MOYEN (4 propriétés)

---

### 9. M0_FourStrokeEngine.jsonld (LOT 3)
**Priorité:** 🔴 ÉLEVÉ (erreurs type + ontologyType)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: "owl:NamedIndividual"` | Au niveau ontologie | → `@type: "owl:Ontology"` |
| ❌ `rdf:type: {"@id": "m3:Poclet"}` | Mauvaise déclaration | → `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ `m3:ontologyCategory` | Propriété invalide | → Supprimer (seul `m3:ontologyType` valide) |
| ❌ `m0:version` | Au lieu de `owl:versionInfo` | → `owl:versionInfo` |

**Estimation effort:** 🔥 MOYEN (4 propriétés à corriger)

---

## ⚠️ Instances nécessitant un RÉALIGNEMENT MINEUR

### 4. M0_Kidneys.jsonld (LOT 1)
**Priorité:** ⚠️ MOYEN (erreur unique mais critique)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: ["owl:NamedIndividual"]` | Au niveau ontologie | → `@type: "owl:Ontology"` |

**Estimation effort:** 🔥 FAIBLE (1 ligne à changer)

**Note:** M0_Kidneys est utilisé comme référence pour la structure ASFID/REVOI, donc prioritaire à corriger.

---

### 7. M0_ColorSynthesis_Federated.jsonld (LOT 2)
**Priorité:** ⚠️ MOYEN (poclet Federated - cas spécial)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ Pas de `m3:ontologyType` | Absent | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ `m2:ontologyCategory: "Poclet"` | Propriété invalide | → Supprimer (seul `m3:ontologyType` valide) |
| ❌ `dcterms:title` | Au lieu de `rdfs:label` | → `rdfs:label` |
| ❌ `dcterms:description` | Au lieu de `rdfs:comment` | → `rdfs:comment` |
| ⚠️ Pas de scores ASFID/REVOI | Absents | → À clarifier avec Michel (Federated = exception ?) |

**Estimation effort:** 🔥 FAIBLE (4 propriétés + clarification Federated)

**Note spéciale:** Poclet de type "Federated" référençant 4 autres poclets (RGB, HSL, CMY, CMYK). Peut-être acceptable sans scores propres ?

---

### 10. M0_MtgColorWheel.jsonld (LOT 3)
**Priorité:** ⚠️ MOYEN (proche conformité - dcterms + ontologyType manquant)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `dcterms:title` | Au lieu de `rdfs:label` | → `rdfs:label` |
| ❌ `dcterms:description` | Au lieu de `rdfs:comment` | → `rdfs:comment` |
| ❌ Pas de `m3:ontologyType` | Absent au niveau ontologie | → Ajouter `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ `m2:ontologyCategory` | Erreur - propriété invalide | → Supprimer (seul `m3:ontologyType` valide) |
| ⚠️ Instance avec `rdf:type: "m0:Poclet"` | Namespace m0 au lieu de m3 | → `m3:Poclet` dans instance séparée |

**Estimation effort:** 🔥 FAIBLE (5 propriétés simples)

---

### 11. M0_KindlebergerMinsky.jsonld (LOT 3)
**Priorité:** ⚠️ FAIBLE (quasi-conforme - architecture exemplaire)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `m2:ontologyCategory: "Poclet"` | Propriété invalide (doublon) | → Supprimer (seul `m3:ontologyType` valide) |
| ⚠️ `m2:changelog` objet | Format minoritaire (1/13) | → Convertir en array (cohérence) |

**Estimation effort:** 🔥 TRÈS FAIBLE (2 ajustements mineurs)

**Note:** Architecture quasi-exemplaire ! Toutes les propriétés obligatoires correctes sauf ce doublon `m2:ontologyCategory`.

---

### 15. M0_NuclearReactorTypology.jsonld (LOT 4) 🥈
**Priorité:** ⚠️ FAIBLE (quasi-conforme - architecture exemplaire)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@base` URL | Pointe vers `aladas-org/cryptocalc` | → `Echopraxium/tscg` |
| ❌ `dcterms:title/description` | Au lieu de `rdfs:label/comment` | → `rdfs:label/comment` |

**Estimation effort:** 🔥 TRÈS FAIBLE (2 ajustements simples)

**Note:** 🥈 **Médaille d'argent !** Architecture quasi-parfaite avec m3:ontologyType correct, scores ASFID/REVOI compacts, @type owl:Ontology.

---

### 16. M0_PlateTectonics.jsonld (LOT 4)
**Priorité:** ⚠️ MOYEN (proche conformité)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `dcterms:title/description` | Au lieu de `rdfs:label/comment` | → `rdfs:label/comment` |
| ❌ `m2:changelog` objet | Format minoritaire | → Convertir en array |
| ⚠️ Instance `@type: ["owl:NamedIndividual", "owl:Class"]` | Double type | → Valider pattern avec Michel |

**Estimation effort:** 🔥 FAIBLE (3 ajustements)

---

### 19. M0_Transistor.jsonld (LOT 5) 🥈
**Priorité:** ⚠️ TRÈS FAIBLE (quasi-conforme - architecture exemplaire)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@type: ["owl:NamedIndividual"]` | Au niveau ontologie | → `@type: "owl:Ontology"` |

**Estimation effort:** 🔥 TRÈS FAIBLE (1 ligne seulement)

**Note:** 🥈 **Médaille d'argent !** Architecture quasi-parfaite avec m3:ontologyType correct, scores ASFID/REVOI compacts, m2:changelog array. Un seul @type à corriger.

---

### 20. M0_TrophicPyramid.jsonld (LOT 5) 🥉
**Priorité:** ⚠️ FAIBLE (proche conformité)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `dcterms:title/description` | Au lieu de `rdfs:label/comment` | → `rdfs:label/comment` |
| ❌ `m2:changelog` objet | Format minoritaire (3/21 = 14%) | → Convertir en array |
| ⚠️ Instance `@type: ["owl:NamedIndividual", "owl:Class"]` | Double type | → Valider pattern avec Michel |
| ⚠️ Scores dans territorySpace/mapSpace | Format valide mais différent | → Format acceptable |

**Estimation effort:** 🔥 FAIBLE (2-3 ajustements)

**Note:** 🥉 **Médaille de bronze !** @type owl:Ontology correct, m3:ontologyType correct, scores présents (format différent mais valide).

---

### 21. M0_TVTestPattern.jsonld (LOT 6)
**Priorité:** ⚠️ FAIBLE (proche conformité)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `dcterms:title/description` | Doublon avec rdfs:label/comment | → Supprimer dcterms (garder rdfs) |
| ❌ `m2:changelog` objet | Format minoritaire | → Convertir en array |

**Estimation effort:** 🔥 TRÈS FAIBLE (2 ajustements)

---

### 22. M0_IChing.jsonld (SymbolicSystemGrammar - instance non-Poclet)
**Priorité:** ⚠️ FAIBLE (quasi-conforme)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@base: aladas-org/cryptocalc` | Pointe vers ancien repo | → `Echopraxium/tscg` |
| ❌ `dcterms:title/description` | Doublon avec rdfs | → Supprimer dcterms |
| ❌ `m0:changelog` objet | Format minoritaire | → Convertir en array |

**Estimation effort:** 🔥 FAIBLE (3 ajustements)

**Note:** ✅ Utilise correctement `m3:ontologyType: {"@id": "m3:SymbolicSystemGrammar"}`

---

## ✅ Instances CONFORMES

### 5. M0_AdaptiveImmuneResponse.jsonld (LOT 1)
**Statut:** ✅ Conforme (seul M0 100% validé à ce jour)

**Checklist complète :**
- ✅ `@type: ["owl:Ontology", "m1:core:Poclet"]` → À clarifier si m1:core:Poclet acceptable
- ✅ Utilise `dcterms:created`, `dcterms:creator`
- ✅ Structure @graph propre avec GenericConcepts M2
- ✅ Pas de namespace `tscg:`
- ✅ Pas de `m2:ontologyCategory` (pas de doublon)

**Note:** Utilise `m1:core:Poclet` dans @type mais Michel a dit que c'est `m3:Poclet` qui est la référence. À clarifier si `m1:core:Poclet` est acceptable ou si c'est une erreur.

---

## 📋 TODO - Prochains lots

### Lot 2 (4 M0 à analyser)
- [ ] M0_???
- [ ] M0_???
- [ ] M0_???
- [ ] M0_???

### Lot 3 (4 M0)
- [ ] À définir

### Lot 4 (4 M0)
- [ ] À définir

### Lot 5 (4 M0)
- [ ] À définir

### Lot 6 (4 M0)
- [ ] À définir

---

## 🎯 Actions immédiates recommandées

### Haute priorité (blocantes)
1. **M0_BloodPressureControl.jsonld** → Renommage massif `tscg:*` → `m0:*`
2. **M0_Kidneys.jsonld** → Fix `@type` (référence utilisée par SHACL)

### Priorité moyenne
3. **M0_ButterflyMetamorphosis.jsonld** → Nettoyage classes custom
4. **M0_CellSignalingModes.jsonld** → Fix `@type` + structure

### À clarifier avec Michel
- [ ] `m1:core:Poclet` dans @type de AdaptiveImmune : acceptable ou erreur ?
- [ ] Components inline (CellSignaling) : autoriser ou imposer @graph ?
- [ ] Marqueurs `m0:check_following_attributes:START/END` : usage légitime ?

---

## 🔴 INSTANCES NON-POCLET (Lot 6 - 2 instances)

### M0_VSM_Metaconcepts.jsonld (SystemicFramework)
**Priorité:** 🔴 CRITIQUE (propriété obsolète + terminologie obsolète)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `m3:ontologyCategory` | Propriété obsolète | → `m3:ontologyType: {"@id": "m3:SystemicFramework"}` |
| ❌ `dcterms:title/description` | Au lieu de rdfs | → `rdfs:label/comment` |
| ❌ Terminologie **ORIVE** | Obsolète dans tout le fichier | → Remplacer par **REVOI** partout |
| ⚠️ `sphinxEye_ORIVE`, `ORIVE_Global` | Propriétés obsolètes | → `sphinxEye_REVOI`, `REVOI_Global` |

**Estimation effort:** 🔥🔥 MOYEN-ÉLEVÉ (renommages multiples ORIVE→REVOI + ontologyCategory→ontologyType)

**CRITIQUE :** VSM est la seule instance utilisant encore `m3:ontologyCategory` (doit être `m3:ontologyType`) ET la terminologie obsolète ORIVE (doit être REVOI).

---

### M0_IChing.jsonld (SymbolicSystemGrammar)
**Priorité:** ⚠️ FAIBLE (quasi-conforme)

| Violation | Détail | Correction requise |
|-----------|--------|-------------------|
| ❌ `@base: aladas-org/cryptocalc` | Pointe vers ancien repo | → `Echopraxium/tscg` |
| ❌ `dcterms:title/description` | Doublon avec rdfs | → Supprimer dcterms |
| ❌ `m0:changelog` objet | Format minoritaire | → Convertir en array |

**Estimation effort:** 🔥 FAIBLE (3 ajustements)

**Note:** ✅ Utilise correctement `m3:ontologyType: {"@id": "m3:SymbolicSystemGrammar"}`

---

## 📝 Historique des mises à jour

**2026-04-13 - Lot 6 + Instances analysés** 🎊 **100% CORPUS COMPLET** + 2 instances
- M0_TVTestPattern.jsonld → ⚠️ Réalignement mineur (proche conformité)
- M0_VCO.jsonld → 🔴 Réalignement majeur (ontologyType absent)
- M0_Yggdrasil.jsonld → 🔴 Réalignement majeur (@base + ontologyType)
- M0_VSM_Metaconcepts.jsonld (SystemicFramework) → 🔴 CRITIQUE (ontologyCategory + ORIVE)
- M0_IChing.jsonld (SymbolicSystemGrammar) → ⚠️ Mineur (@base + dcterms)

**2026-04-13 - Lot 5 analysé** 🎊 **GRAMMAIRE FINALE (88% corpus)**
- M0_Transistor.jsonld → ⚠️ Réalignement mineur (quasi-conforme 🥈)
- M0_TrophicPyramid.jsonld → ⚠️ Réalignement mineur (proche conformité 🥉)
- M0_RAAS.jsonld → 🔴 Réalignement majeur (@type + @base)
- M0_TPACK.jsonld → 🔴 Réalignement majeur (@type + ontologyType absent)

**2026-04-13 - Lot 4 analysé** 🎯 **MASSE CRITIQUE ATTEINTE (71% corpus)**
- M0_NuclearReactorTypology.jsonld → ⚠️ Réalignement mineur (quasi-conforme 🥈)
- M0_PlateTectonics.jsonld → ⚠️ Réalignement mineur (proche conformité)
- M0_Poclet_NakamotoConsensus.jsonld → 🔴 Réalignement majeur (@type: m0:Poclet)
- M0_PhaseTransition.jsonld → 🔴 Réalignement majeur (namespace tscg)

**2026-04-13 - Lot 3 analysé**
- M0_KindlebergerMinsky.jsonld → ⚠️ Réalignement mineur (m2:ontologyCategory)
- M0_FireTriangle.jsonld → 🔴 Réalignement majeur (@type + ontologyType + version)
- M0_FourStrokeEngine.jsonld → 🔴 Réalignement majeur (@type + ontologyType)
- M0_MtgColorWheel.jsonld → ⚠️ Réalignement mineur (dcterms:title + ontologyType)

**2026-04-13 - Lot 2 analysé**
- M0_Counterpoint.jsonld → 🔴 Réalignement majeur (@type + ontologyType)
- M0_ExposureTriangle.jsonld → 🔴 Réalignement majeur (@type + ontologyType)
- M0_ComplexChemicalSynapse.jsonld → 🔴 Réalignement majeur (m2:ontologyType, dcterms:title)
- M0_ColorSynthesis_Federated.jsonld → ⚠️ Réalignement mineur (ontologyType, dcterms:title)

**2026-04-13 - Lot 1 analysé**
- M0_BloodPressureControl.jsonld → 🔴 Réalignement majeur (namespace tscg)
- M0_CellSignalingModes.jsonld → 🔴 Réalignement majeur (type + structure)
- M0_ButterflyMetamorphosis.jsonld → 🔴 Réalignement majeur (classes custom)
- M0_Kidneys.jsonld → ⚠️ Réalignement mineur (@type)
- M0_AdaptiveImmuneResponse.jsonld → ✅ Conforme (sous réserve)
