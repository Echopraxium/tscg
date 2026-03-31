---
name: tscg-article-pipeline
description: >
  Pipeline de rédaction ou mise à jour d'un article de recherche TSCG en 5 étapes séquentielles :
  Audit, Planification, Rédaction section par section, Révision globale, Finalisation.
  Utilise ce skill dès que Michel mentionne l'article de recherche, demande de rédiger ou mettre
  à jour un article sur TSCG, veut préparer une soumission HAL ou Zenodo, mentionne "matières
  premières pour l'article", ou dit des choses comme "on met à jour l'article", "nouvelle version
  de l'article", "soumission HAL", "il faut écrire la section X", "l'article est obsolète",
  "version 4 de l'article". Applicable aussi quand Michel fournit un article existant à réviser
  ou demande d'exploiter les fichiers dans docs/papers/inputs/ ou ontology/docs/.
---

# TSCG Research Article Pipeline

Pipeline en 5 étapes pour rédiger ou mettre à jour un article de recherche TSCG :
**Audit → Planification → Rédaction → Révision globale → Finalisation**

Chaque étape contient des **points de synchronisation humain** (⏸) qui suspendent le pipeline
jusqu'à décision explicite de Michel de continuer.

La conversation est en **Français** ; tous les fichiers générés sont en **Anglais**.

---

## Localisation des ressources

### Article en cours
```
docs/papers/preprints/TSCG_Research_Paper_Draft_v3.md   ← version actuelle (v3.0, TSCG v15.1.0)
docs/papers/preprints/new draft specification.txt        ← spécifications d'une future version
docs/papers/preprints/HAL Guidelines.md                 ← contraintes de soumission HAL
docs/papers/preprints/TSCG_HAL_Additions_v1.md          ← sections déjà préparées pour HAL
```

### Matières premières (sources à exploiter)
```
docs/papers/inputs/
  00_M3_Cyclops_Correction_Summary.md
  00_M3_Philosophical_Basis_Sketch.jsonld
  00_Map_Territory_v1.2_Update_Summary.md
  00_TSCG_M3_Bicephalous_Architecture.md
  00_TSCG_Map_Territory_Theoretical_Foundation.md
  M2_v7.2.0_Summary.md
  M2_v8.0.0_Update_Guide.md
  TSCG-M3_Ontology_Documentation.md
  TSCG_Session_Complete_Summary_Claude_2025_01_14.md
  Network_Decomposition_Report.md

ontology/docs/              ← inventorier en début de session (contenu à confirmer)
```

### Contexte framework (source de vérité)
```
docs/reboot-kit/TSCG_Smart_Prompt_v15_10_1.md     ← version courante du framework
TSCG_Session_README_2026-03-23.md                 ← dernières découvertes (M2 v15.11.0 candidats)
ontology/M2_GenericConcepts.jsonld                 ← 75 GenericConcepts atomiques v15.10.1
ontology/M1_CoreConcepts.jsonld                    ← combos + KnowledgeFieldConceptCombo
```

---

## Watchdog terminologique — OBLIGATOIRE à chaque section

Avant toute génération de contenu, vérifier systématiquement :

| Terme | Correct | Interdit |
|-------|---------|----------|
| R dans REVOI | **Representability** | ~~Reproducibility~~ |
| Acronyme Map | **REVOI** | ~~ORIVE~~ |
| Acronyme Territory | **ASFID** | ~~FASID~~, ~~FASDI~~ |
| Auteur | **Echopraxium with the collaboration of Claude AI** | tout autre ordre |
| Combo M1 | **KnowledgeFieldConceptCombo** | ~~KnowledgeFieldGenericCombo~~ |
| Dossier instances | **instances/** | ~~system-models/~~ |
| Simulations | **standalone HTML** | ~~Pygame~~ (pour les nouvelles) |

> Ces erreurs sont des hallucinations récurrentes documentées dans l'Appendix B de l'article.
> Ce watchdog s'applique en priorité absolue sur tout contenu généré.

---

## Étape 1 — AUDIT

### Objectif
Identifier précisément les écarts entre l'article existant et l'état actuel du framework.

### Actions

**1.1** Lire l'article existant (fourni par Michel ou dans `docs/papers/preprints/`)

**1.2** Inventorier les matières premières disponibles
- Lire `docs/papers/inputs/` et `ontology/docs/`
- Pour chaque fichier : sujet, date estimée, valeur pour la mise à jour

**1.3** Produire la table des écarts

Format obligatoire :
```
# Audit TSCG Article — [version article] → [version framework cible]

## Métadonnées
- Version article : vX.Y (TSCG vA.B.C)
- Version framework cible : TSCG v15.10.1
- Date audit : [date]

## Écarts identifiés

| # | Section article | Problème | Matière première disponible | Priorité |
|---|----------------|----------|----------------------------|----------|
| 1 | Abstract | Poclets 14→21+, KnowledgeFieldConceptCombo absent | Smart Prompt | Haute |
| 2 | §2 Architecture | system-models/→instances/, TransDisclet/Enigma absents | File Tree | Haute |
| 3 | §3 M2 | 75 GenericConcepts (vs ~58 cités), 5 nouveaux atomiques | Session README | Haute |
| ... | ... | ... | ... | ... |

## Matières premières non encore exploitées
[liste des fichiers inputs/ avec leur potentiel]

## Décision recommandée
[ ] Mise à jour ciblée (sections X, Y, Z uniquement)
[ ] Réécriture complète (v4.0)
[ ] Nouveau papier complémentaire
```

⏸ **Point de sync** — Michel décide du périmètre et de la stratégie avant de continuer.

---

## Étape 2 — PLANIFICATION

### Objectif
Définir le plan de travail section par section avec les sources à exploiter pour chacune.

### Actions

**2.1** Lire `new draft specification.txt` si présent

**2.2** Lire `HAL Guidelines.md` si la cible est une soumission HAL

**2.3** Produire le plan de travail

```
# Plan de mise à jour — Article TSCG v[X]

## Stratégie : [Mise à jour ciblée | Réécriture | Nouveau papier]
## Version cible : v[X.Y] (TSCG v15.10.1)
## Cible de soumission : [HAL | Zenodo | Autre]

## Sections à produire (ordre de rédaction)

| # | Section | Statut | Sources principales | Effort |
|---|---------|--------|---------------------|--------|
| 0 | Abstract | À réécrire | Smart Prompt, Session README | Moyen |
| 1 | Introduction | À mettre à jour | Map_Territory_Foundation.md | Faible |
| 2 | Architecture bicéphale M3 | À enrichir | M3_Bicephalous_Architecture.md | Moyen |
| 3 | GenericConcepts M2 | À réécrire | Session README, M2_GenericConcepts.jsonld | Élevé |
| 4 | Corpus poclets M0 | À étendre | Smart Prompt, File Tree | Moyen |
| 5 | Noise reduction (Combo) | À corriger | M1_CoreConcepts.jsonld | Faible |
| 6 | Validation + scores | À enrichir | Session README (δ, SpectralClasses) | Moyen |
| 7 | Discussion / Limitations | Nouveau | Session README, HAL Additions | Moyen |
| 8 | References | À compléter | Ranaora & Yii 2026 | Faible |
| A | Appendix A (Poclet catalog) | À étendre 14→21+ | File Tree, Smart Prompt | Moyen |
| B | Appendix B (Human-AI) | À mettre à jour | Smart Prompt v15.10.1 | Faible |

## Ordre de génération suggéré
[liste ordonnée selon dépendances logiques]
```

⏸ **Point de sync** — Michel valide le plan et priorise les sections.

---

## Étape 3 — RÉDACTION (section par section)

### Règle absolue
Une section à la fois. Jamais de génération en bloc de l'article entier (risque de troncature).

### Pour chaque section

**3.1** Annoncer la section :
```
## Rédaction : Section [N] — [Titre]
Sources utilisées : [liste]
Watchdog terminologique : actif
```

**3.2** Lire les matières premières pertinentes avant de rédiger

**3.3** Générer le contenu en Anglais

**3.4** Vérifier le watchdog terminologique avant soumission

**3.5** Afficher le contenu avec longueur estimée (mots / paragraphes)

⏸ **Point de sync après chaque section** — Michel valide, corrige ou demande une variante.

### Sections à traitement spécial

#### Abstract
- Mettre à jour : 14 poclets → 21+, ~58 GenericConcepts → 75 atomiques
- Ajouter KnowledgeFieldConceptCombo (absent en v3.0)
- Vérifier que les chiffres de réduction restent cohérents (~31% GenericConceptCombo)

#### Section Architecture M3
- Intégrer la relaxation de l'axiome F : `F ≥ 0` (vs `F ≠ 0` en v3.0)
- Spectre de F : F=0 (Stase) → F_potential → F_crit → F_active → ∞
- F comme dimension morphique : F ∈ Mor(Cat_M3) ∩ Ob(Cat_M3)
- Ajouter nouveaux types ontologiques : `m3:TransDisclet`, `m3:Enigma`
- Exploiter `00_TSCG_M3_Bicephalous_Architecture.md` et `00_Map_Territory_v1.2_Update_Summary.md`

#### Section GenericConcepts M2
- Mentionner les 75 concepts atomiques (9 familles) en v15.10.1
- Intégrer les candidats validés de la session 2026-03-23 si applicable :
  Entropy (F⊗I⊗D), Stase (S⊗A), Processor (S⊗I⊗F⊗D), Transducer (F⊗S⊗I),
  Coherence (A⊗S⊗I⊗R⊗O)
- Mentionner la révision de Dissipation (note Feynman, subClassOf Transducer)
- Présenter la chaîne causale :
  F_active → Dissipation → Entropy → Inertia → Absorbing State
- Exploiter `M2_v7.2.0_Summary.md`, `M2_v8.0.0_Update_Guide.md`, `Network_Decomposition_Report.md`

#### Appendix A (Poclet catalog)
- Étendre de 14 → 21+ poclets
- Corriger les noms de GenericConcepts (utiliser noms v15.10.1)
- Mettre à jour "accompanying simulation" : Python/Pygame → HTML standalone
- Nouveaux poclets à inclure (vérifier dans File Tree + Smart Prompt) :
  TrophicPyramid, TvTestPattern, KindlebergerMinsky, CounterPoint,
  NakamotoConsensus, MtgColorWheel, VCO, PhaseTransition, ExposureTriangle

#### Appendix B (Human-AI Collaboration)
- B.2 : Smart Prompt → `TSCG_Smart_Prompt_v15_10_1.md`
- B.5 : simulations → mentionner HTML standalone (Electron + navigateur)
- Envisager B.8 : Skills system (si pertinent pour le public cible)

---

## Étape 4 — RÉVISION GLOBALE

### Checklist de révision

```
### Terminologie
[ ] REVOI partout (jamais ORIVE)
[ ] R = Representability (jamais Reproducibility)
[ ] ASFID correct (jamais FASID)
[ ] KnowledgeFieldConceptCombo (jamais KnowledgeFieldGenericCombo)
[ ] instances/ (jamais system-models/)
[ ] Auteur : "Echopraxium with the collaboration of Claude AI"

### Cohérence des chiffres
[ ] Nombre de poclets cohérent (Abstract = §corpus = Appendix A)
[ ] Nombre de GenericConcepts cohérent (75 atomiques en v15.10.1)
[ ] Version framework cohérente partout
[ ] DOI Zenodo à jour

### Références croisées
[ ] Chaque section référence correctement les autres
[ ] Appendix A cohérent avec §corpus poclets
[ ] Abstract cohérent avec conclusions

### HAL / Zenodo (si soumission)
[ ] Respect des guidelines HAL (lire HAL Guidelines.md)
[ ] Métadonnées complètes (titre, auteurs, mots-clés, résumé)

### Nouvelles références bibliographiques
[ ] Ranaora & Yii 2026 (DOI: 10.5281/zenodo.19160047) si NakamotoConsensus inclus
[ ] Feynman (irréversibilité) si section M2 révisée
[ ] Prigogine si structures dissipatives mentionnées
```

⏸ **Point de sync** — Michel valide la révision globale ou demande des corrections.

---

## Étape 5 — FINALISATION

### Actions

**5.1** Assemblage de toutes les sections dans l'ordre canonique

**5.2** Mise à jour des métadonnées
```
Authors: Echopraxium with the collaboration of Claude AI
Date: [mois] [année]
Version: [X.Y]
Framework Version: TSCG v15.10.1
DOI (Prior Work): [mettre à jour si nouvelle version Zenodo]
```

**5.3** Changelog de l'article
```markdown
## Changelog

### v[X.Y] — [date]
- Updated to TSCG framework v15.10.1
- Extended poclet catalog: 14 → [N] poclets
- M2: 75 atomic GenericConcepts (9 families)
- M3: F axiom relaxed (F ≥ 0), F_morphic annotation
- New ontology types: m3:TransDisclet, m3:Enigma
- Simulations: Python/Pygame → standalone HTML
```

**5.4** Fichier de sortie : `docs/papers/preprints/TSCG_Research_Paper_Draft_v[X].md`

> La conversion vers PDF/DOCX pour HAL se fait en post-traitement (Pandoc) — hors portée de ce pipeline.

⏸ **Point de sync final** — Michel valide avant archivage / soumission.

---

## Résumé du pipeline

```
AUDIT
  └─ Table des écarts (article vs framework)
  └─ Inventaire inputs/ + ontology/docs/
  ⏸ Périmètre et stratégie → Michel

PLANIFICATION
  └─ Plan section par section (sources + effort)
  └─ Contraintes HAL/Zenodo si applicable
  ⏸ Validation du plan → Michel

RÉDACTION (section par section)
  └─ Watchdog terminologique actif en permanence
  └─ Lecture matières premières avant chaque section
  └─ Génération en Anglais, une section à la fois
  ⏸ Validation après chaque section → Michel

RÉVISION GLOBALE
  └─ Checklist cohérence transversale
  └─ Cohérence chiffres + terminologie + références
  ⏸ Validation révision → Michel

FINALISATION
  └─ Assemblage + métadonnées + changelog
  └─ Output Markdown dans docs/papers/preprints/
  ⏸ Validation finale → Michel → soumission
```

---

## Matières premières connues — table de correspondance

| Fichier | Contenu probable | Section(s) cible(s) |
|---------|-----------------|---------------------|
| `00_TSCG_M3_Bicephalous_Architecture.md` | Architecture Eagle Eye / Sphinx Eye | §2, §3 M3 |
| `00_TSCG_Map_Territory_Theoretical_Foundation.md` | Fondements philosophiques Korzybski | §1 Introduction |
| `00_Map_Territory_v1.2_Update_Summary.md` | Feedback loop Σ, Φ, Ψ | §2 Architecture |
| `00_M3_Cyclops_Correction_Summary.md` | Corrections "Bicephalous Cyclops" | §1.3 |
| `00_M3_Philosophical_Basis_Sketch.jsonld` | Base philosophique M3 formalisée | §3 M3 technique |
| `M2_v7.2.0_Summary.md` | État M2 à v7.2.0 | Historique évolution M2 |
| `M2_v8.0.0_Update_Guide.md` | Mise à jour M2 v8.0.0 | Historique évolution M2 |
| `TSCG-M3_Ontology_Documentation.md` | Documentation ontologie M3 | §3 M3 |
| `TSCG_Session_Complete_Summary_Claude_2025_01_14.md` | Résumé session Jan 2025 | §3, §4 |
| `Network_Decomposition_Report.md` | Décomposition réseau | §3 M2 |
| `ontology/docs/` | À inventorier en début de session | TBD |
