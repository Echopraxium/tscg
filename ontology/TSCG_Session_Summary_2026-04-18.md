# TSCG - Résumé de session : Migration m1:domain + Plan A-B-C
**Date :** 2026-04-18  
**Objectif :** Réaligner la grammaire TSCG pour corriger l'incohérence des domaines  
**Statut :** Phase 1 terminée (SHACL mis à jour) → Transition vers Claude Code pour phases 2-3

---

## 🎯 Problématique initiale

### Incohérences identifiées dans le corpus
1. **Propriété domain au mauvais niveau** : `m0:domain` utilisé alors que c'est un concept M1 (extension disciplinaire)
2. **Formats multiples non standardisés** :
   - Certains poclets : `"m0:domain": "Chemistry"` (string simple)
   - D'autres : `"m0:domain": "Ecology / Biology"` (multi-domaine avec slash)
   - Pas de vocabulaire contrôlé
3. **Subdomains dispersés** : `m0:subdomains` dans chaque poclet au lieu d'un registre centralisé
4. **Violations SHACL** : 24 poclets avec incohérences grammaticales (voir M0_Realignment_Tracker.md)

---

## ✅ Décisions architecturales prises

### 1. Migration m0:domain → m1:domain
**Rationale :** Le domaine est un concept M1 (extension disciplinaire), pas M0 (instance).

**Cohérence TSCG :**
- **M3** : Méta-ontologie (types d'ontologies : Poclet, SystemicFramework, etc.)
- **M2** : GenericConcepts transdisciplinaires (Synergy, Balance, Flow, etc.)
- **M1** : Extensions disciplinaires → **m1:domain appartient ici** ✅
- **M0** : Instances concrètes (poclets)

### 2. Support multi-domaines via array JSON
**Format retenu :**
```json
// Domaine unique
"m1:domain": "Chemistry"

// Multi-domaines
"m1:domain": ["Chemistry", "Physics"]
```

**Rejeté :** Séparateur slash `"Chemistry / Physics"` (parsing complexe, ambiguïté)

### 3. Création de M1_Domains.jsonld
**Registre centralisé évolutif** des domaines TSCG avec :
- Entrée par domaine : `m1domain:DomainName`
- Propriétés : `rdfs:label`, `rdfs:comment`, `m1:subdomains`, `m1:relatedDomains`, `m1:pocletExamples`, `m1:pocletCount`
- Subdomains déplacés de M0 vers M1_Domains.jsonld
- Référencé par la grammaire SHACL

### 4. Migration des subdomains
**AVANT (dispersé dans chaque M0) :**
```json
// M0_Transistor.jsonld
{
  "m0:domain": "Electronics",
  "m0:subdomains": ["Semiconductor Physics", "Digital Logic"]
}
```

**APRÈS (centralisé dans M1_Domains.jsonld) :**
```json
// M1_Domains.jsonld
{
  "@id": "m1domain:Electronics",
  "m1:subdomains": ["Semiconductor Physics", "Digital Logic", "Analog Circuits"]
}

// M0_Transistor.jsonld
{
  "m1:domain": {"@id": "m1domain:Electronics"}
}
```

---

## 📝 Fichiers modifiés/créés

### ✅ TERMINÉ : M0_Instances_Schema_shacl.ttl v1.1

**Modifications :**
1. Ajout préfixe `@prefix m1:`
2. Migration contrainte `m0:domain` → `m1:domain`
3. Support multi-domaines (string OU array)
4. Message validation référençant M1_Domains.jsonld
5. Changelog v1.1 documentant la migration

**Fichier disponible :** `/mnt/user-data/outputs/M0_Instances_Schema_shacl.ttl`

**Extraits clés :**
```turtle
# Préfixe ajouté (ligne 8)
@prefix m1: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#> .

# Contrainte domain (lignes 126-135)
sh:property [
  sh:path m1:domain ;
  sh:or (
    [ sh:datatype xsd:string ]           # Single domain
    [ sh:nodeKind sh:Literal ]           # Array of domains
  ) ;
  sh:minCount 1 ;
  sh:message "m1:domain is MANDATORY (M1-level property, not m0:domain). 
              Accepts single string ('Chemistry') or array (['Chemistry', 'Physics']). 
              Domain values are registered in M1_Domains.jsonld (evolving registry)."
] ;
```

---

## 🚧 À FAIRE : Plan A-B-C

### **A) Créer M1_Domains.jsonld** (30-45 min)

**Objectif :** Registre centralisé de tous les domaines TSCG

**Inputs nécessaires :**
- Corpus complet : `instances/poclets/*/M0_*.jsonld` (24 poclets)
- Instances non-poclet : `M0_VSM_Metaconcepts.jsonld`, `M0_IChing.jsonld`

**Structure attendue :**
```json
{
  "@context": { ... },
  "@graph": [
    {
      "@id": "M1_Domains.jsonld",
      "@type": "owl:Ontology",
      "rdfs:label": "TSCG Knowledge Domains Registry",
      "m1:domainCount": 15,
      "m1:totalPoclets": 24
    },
    {
      "@id": "m1domain:Chemistry",
      "@type": "m1:Domain",
      "rdfs:label": "Chemistry",
      "rdfs:comment": "Science of matter, composition, and transformations",
      "m1:subdomains": [
        "Combustion Chemistry",
        "Thermodynamics",
        "Chemical Kinetics"
      ],
      "m1:relatedDomains": [
        {"@id": "m1domain:Physics"},
        {"@id": "m1domain:Biology"}
      ],
      "m1:pocletExamples": [
        "M0_FireTriangle",
        "M0_PhaseTransition"
      ],
      "m1:pocletCount": 2
    },
    // ... autres domaines
  ]
}
```

**Domaines identifiés (extraction partielle - 10 fichiers disponibles) :**
- Biology (subdomains: Developmental Biology, Endocrinology, Renal Physiology, etc.)
- Electronics (subdomains: Semiconductor Physics, Analog/Digital Electronics)
- Ecology
- Chemistry
- Physics
- Computer Science
- Economics
- Engineering
- Mythology
- Nuclear Engineering

**Action Claude Code :**
1. Scanner `instances/poclets/*/M0_*.jsonld`
2. Extraire tous les `m0:domain` et `m0:subdomains`
3. Consolider dans M1_Domains.jsonld
4. Sauvegarder dans `ontology/M1_Domains.jsonld`

---

### **B) Réaligner M0_FireTriangle.jsonld** (15-20 min)

**Fichier :** `instances/poclets/FireTriangle/M0_FireTriangle.jsonld`

**Violations identifiées (M0_Realignment_Tracker.md) :**

| Violation | État actuel | Correction requise |
|-----------|-------------|-------------------|
| ❌ `@type` au niveau ontologie | `"owl:NamedIndividual"` (ligne 18) | → `"owl:Ontology"` |
| ❌ Type de poclet | `rdf:type: ["m1:chemistry:Combustion", "m1:core:Poclet"]` (lignes 22-24) | → `m3:ontologyType: {"@id": "m3:Poclet"}` |
| ❌ Domain au mauvais niveau/namespace | `"m0:FireTriangle:domain": "Chemistry"` (ligne 36) | → `"m1:domain": "Chemistry"` au niveau ontologie |
| ⚠️ Version manquante | Absent | → Ajouter `"owl:versionInfo": "1.2.0"` |
| ⚠️ Scores optionnels | Absents au niveau ontologie | → Ajouter `m0:asfidScores` et `m0:revoiScores` (format compact) |

**Corrections détaillées :**

#### 1. Correction @type (ligne 18)
```json
// AVANT
{
  "@id": "m0:FireTriangle:FireTrianglePoclet",
  "@type": "owl:NamedIndividual",
  ...
}

// APRÈS
{
  "@id": "M0_FireTriangle.jsonld",
  "@type": "owl:Ontology",
  ...
}
```

#### 2. Correction m3:ontologyType (lignes 22-24)
```json
// AVANT
"rdf:type": [
  "m1:chemistry:Combustion",
  "m1:core:Poclet"
],

// APRÈS
"m3:ontologyType": {"@id": "m3:Poclet"},
```

#### 3. Correction m1:domain (ligne 36)
```json
// AVANT
"m0:FireTriangle:domain": "Chemistry",

// APRÈS (au niveau ontologie, pas dans composant)
"m1:domain": "Chemistry",
// OU avec IRI reference
"m1:domain": {"@id": "m1domain:Chemistry"},
```

#### 4. Ajout owl:versionInfo (après ligne 29)
```json
"owl:versionInfo": "1.2.0",
```

#### 5. Ajout scores compacts (optionnel - après owl:versionInfo)
```json
"m0:asfidScores": {
  "A": 0.75,
  "S": 0.90,
  "F": 0.60,
  "I": 0.80,
  "D": 0.50,
  "mean": 0.71
},
"m0:revoiScores": {
  "R": 0.85,
  "E": 0.70,
  "V": 0.90,
  "O": 0.75,
  "I": 0.65,
  "mean": 0.77
}
```

**Template réutilisable :**
Ce pattern s'applique à **6 poclets** avec les mêmes violations :
- M0_ExposureTriangle.jsonld
- M0_Counterpoint.jsonld
- M0_FourStrokeEngine.jsonld
- M0_CellSignalingModes.jsonld
- M0_Kidneys.jsonld

**Validation :**
```bash
pyshacl -s ontology/M0_Instances_Schema_shacl.ttl \
        -df json-ld \
        instances/poclets/FireTriangle/M0_FireTriangle.jsonld
```

---

### **C) App ElectronJS : TscgGrammarValidator** (2-3h)

**Emplacement :** `instances/tscg-tools/TscgGrammarValidator/`

**Fonctionnalités :**

#### 1. **Scanner de corpus**
- Parcourir `instances/poclets/*/M0_*.jsonld`
- Détecter violations SHACL
- Afficher rapport par fichier

#### 2. **Migration automatique m0:domain → m1:domain**
- Détecter toutes occurrences de `"m0:domain"`
- Remplacer par `"m1:domain"`
- Déplacer au bon niveau (ontologie, pas composant)
- Backup avant modification

#### 3. **Validation SHACL**
- Charger `M0_Instances_Schema_shacl.ttl`
- Valider chaque M0 contre la grammaire
- Rapport conformité avec détails violations

#### 4. **Tableau de bord**
- Statistiques corpus (24 poclets + 2 autres)
- Conformité globale (% validé)
- Top violations
- Progression migration

**Architecture Electron :**

```
TscgGrammarValidator/
├── package.json
├── main.js                    # Electron main process
├── preload.js                 # Context bridge
├── renderer/
│   ├── index.html            # UI principale
│   ├── styles.css            # Dark theme GitHub-inspired
│   └── renderer.js           # UI logic
├── validators/
│   ├── ShaclValidator.js     # pyshacl wrapper
│   ├── DomainMigrator.js     # m0→m1 migration
│   └── CorpusScanner.js      # Parcours instances/
├── utils/
│   ├── FileManager.js        # I/O + backup
│   └── ReportGenerator.js    # Markdown reports
└── config/
    └── paths.json            # Chemins repo TSCG
```

**UI inspirée de TscgPocletMiner :**
- Sidebar : Navigation (Scanner, Migrator, Validator, Reports)
- Main panel : Tableau de bord ou outil actif
- Dark theme cohérent avec les autres outils TSCG
- Logs en temps réel

**Technologies :**
- **ElectronJS** (pas de React, vanilla JS/CSS)
- **pyshacl** via child_process (Python subprocess)
- **JSON-LD parsing** : `jsonld` npm package
- **File watching** : `chokidar` pour détection changements

**Dépendances package.json :**
```json
{
  "name": "tscg-grammar-validator",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder"
  },
  "dependencies": {
    "jsonld": "^8.3.0",
    "chokidar": "^3.5.3"
  },
  "devDependencies": {
    "electron": "^28.0.0",
    "electron-builder": "^24.9.0"
  }
}
```

**Python requirement :**
```bash
pip install pyshacl --break-system-packages
```

---

## 📂 Fichiers de référence importants

### Dans le projet Claude.ai (accessibles via /mnt/project)
- `M0_Realignment_Tracker.md` - Liste des 24 poclets à réaligner avec détails violations
- `LOT6_FINAL_Analysis_Report.md` - Analyse complète corpus (statistiques, patterns)
- `M0_Instances_Schema_shacl.ttl` - Grammaire SHACL v1.0 (ANCIEN - remplacé par v1.1)
- `TSCG_Smart_Prompt_v15_10_1.md` - Contexte framework TSCG

### Fichiers uploadés disponibles
- `M0_FireTriangle.jsonld` - Exemple poclet à réaligner
- `M0_FireTriangle_README.md` - Documentation poclet
- `M0_FireTriangle.html` - Simulation (autonome, pas impacté)
- `M0_Instances_Schema_shacl.ttl` - Grammaire v1.0 (uploadée avant mise à jour)

### Fichiers créés pendant la session
- `/mnt/user-data/outputs/M0_Instances_Schema_shacl.ttl` - **Grammaire v1.1 MISE À JOUR** ✅

---

## 🗺️ Contexte architectural TSCG (rappel)

### Architecture M3 → M2 → M1 → M0

**M3_GenesisSpace.jsonld :**
- Définit 11 `m3:ontologyType` dont :
  - `m3:Poclet` (24 instances)
  - `m3:SystemicFramework` (1 instance: VSM)
  - `m3:SymbolicSystemGrammar` (1 instance: IChing)
- Bicephalous architecture : Eagle Eye (ASFID) + Sphinx Eye (REVOI)

**M2_GenericConcepts.jsonld v15.10.1 :**
- 75 GenericConcepts atomiques transdisciplinaires
- 9 familles : Spatial, Temporal, Energetic, Informational, Dynamical, Ontological, Teleonomic, Relational, Emergent
- Combo family migrée vers M1_CoreConcepts.jsonld

**M1 Extensions :**
- `M1_CoreConcepts.jsonld` v2.1.0 : GenericConceptCombos + KnowledgeFieldCombos
- Extensions disciplinaires : `M1_Biology.jsonld`, `M1_Chemistry.jsonld`, `M1_Optics.jsonld`, etc.
- **NOUVEAU** : `M1_Domains.jsonld` (à créer) - Registre des domaines

**M0 Instances :**
- 24 Poclets validés
- 2 autres instances (VSM, IChing)
- Stockés dans `instances/poclets/[PocletName]/M0_PocletName.jsonld`

### Epistemic scoring (δ formulas)
- δ₀ : scalar gap
- δ₁ : normalized vectorial gap (recommandé)
- δ₂ : Riemannian (future)
- SpectralClasses : Coherent [0,0.05), OnCriticalLine [0.05,0.15), Liminal [0.15,0.30), Enigmatic [0.30,1.0]

---

## 🔧 Pour Claude Code : Instructions de démarrage

### Étape 0 : Vérifier l'environnement
```bash
# Naviguer vers le repo local
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\

# Vérifier structure
ls instances/poclets/
ls ontology/

# Vérifier Python + pyshacl
python --version
pip list | grep pyshacl
```

### Étape A : Créer M1_Domains.jsonld
```bash
# Scanner le corpus
find instances/poclets -name "M0_*.jsonld" -type f

# Créer le fichier
# [Claude Code génère M1_Domains.jsonld avec analyse complète]

# Placer dans ontology/
cp M1_Domains.jsonld ontology/M1_Domains.jsonld
```

### Étape B : Réaligner FireTriangle
```bash
# Backup
cp instances/poclets/FireTriangle/M0_FireTriangle.jsonld \
   instances/poclets/FireTriangle/M0_FireTriangle.jsonld.bak

# Éditer avec corrections SHACL
# [Claude Code applique les 5 corrections listées]

# Valider
pyshacl -s ontology/M0_Instances_Schema_shacl.ttl \
        -df json-ld \
        instances/poclets/FireTriangle/M0_FireTriangle.jsonld
```

### Étape C : Créer TscgGrammarValidator
```bash
# Créer structure
mkdir -p instances/tscg-tools/TscgGrammarValidator
cd instances/tscg-tools/TscgGrammarValidator

# Initialiser npm
npm init -y

# Installer dépendances
npm install electron jsonld chokidar

# [Claude Code génère main.js, renderer/, validators/, etc.]

# Tester
npm start
```

---

## 📊 État du corpus (conformité SHACL)

### Statistiques globales (M0_Realignment_Tracker.md)
- **Total instances** : 26 (24 Poclets + 2 autres)
- **Conformité actuelle** : 4% (1 seul conforme : M0_AdaptiveImmuneResponse)
- **Réalignement mineur** : 42% (10 poclets)
- **Réalignement majeur** : 54% (13 poclets)

### Top violations
1. **@type: owl:NamedIndividual** → 38% (9 poclets) — doit être `owl:Ontology`
2. **m3:ontologyType manquant/incorrect** → 62% (15 instances)
3. **m0:domain** au lieu de **m1:domain** → 85% (22 instances) — **BREAKING CHANGE**
4. **dcterms:title/description** au lieu de **rdfs:label/comment** → 42% (11 instances)
5. **Namespace tscg:*** interdit → 8% (2 poclets : BloodPressureControl, PhaseTransition)

### Stratégie de migration par vagues
**VAGUE 1 — Quick wins** (4 poclets, 1h) :
- M0_Kidneys, M0_KindlebergerMinsky, M0_ColorSynthesis, M0_MtgColorWheel

**VAGUE 2 — Batch standard** (6 poclets, 2-3h) :
- M0_FireTriangle, M0_ExposureTriangle, M0_Counterpoint, M0_FourStrokeEngine, M0_CellSignalingModes, M0_ComplexChemicalSynapse

**VAGUE 3 — Gros chantiers** (2 poclets, 2-3h) :
- M0_ButterflyMetamorphosis (10+ classes custom à supprimer)
- M0_BloodPressureControl (50+ propriétés `tscg:*` à renommer)

---

## ⚠️ Points critiques à retenir

### 1. BREAKING CHANGE : m0:domain → m1:domain
**Tous les M0 doivent être migrés.** Aucune rétrocompatibilité.

**Pattern de migration :**
```bash
# Recherche globale
grep -r "m0:domain" instances/poclets/

# Remplacement (avec backup)
# [Sera géré par TscgGrammarValidator app]
```

### 2. Formats domain acceptés
```json
// ✅ String simple
"m1:domain": "Chemistry"

// ✅ Array multi-domaines
"m1:domain": ["Chemistry", "Physics"]

// ✅ IRI reference (futur)
"m1:domain": {"@id": "m1domain:Chemistry"}

// ❌ INTERDIT : slash separator
"m1:domain": "Chemistry / Physics"
```

### 3. Subdomains migrés vers M1_Domains.jsonld
**Ne plus mettre dans M0** :
```json
// ❌ ANCIEN pattern (à supprimer des M0)
"m0:subdomains": ["Combustion Chemistry", "Thermodynamics"]

// ✅ NOUVEAU pattern (dans M1_Domains.jsonld uniquement)
{
  "@id": "m1domain:Chemistry",
  "m1:subdomains": ["Combustion Chemistry", "Thermodynamics", ...]
}
```

### 4. Impact HTML simulations
**Aucun impact** — Les simulations HTML (FireTriangle.html, etc.) sont **autonomes** et ne chargent pas les fichiers .jsonld dynamiquement. Elles restent fonctionnelles sans modification.

### 5. Changelog SHACL
Toujours **maximum 3 entrées** (most recent first). Lors de futurs changements, supprimer la plus ancienne.

---

## 🎯 Objectifs de succès

### Phase A — M1_Domains.jsonld
- ✅ Fichier créé dans `ontology/M1_Domains.jsonld`
- ✅ 15+ domaines extraits du corpus
- ✅ Subdomains complets pour chaque domaine
- ✅ pocletCount exact
- ✅ Format JSON-LD valide avec @context

### Phase B — FireTriangle réaligné
- ✅ Passe validation SHACL sans erreurs
- ✅ `m1:domain: "Chemistry"` au niveau ontologie
- ✅ `m3:ontologyType: {"@id": "m3:Poclet"}`
- ✅ `@type: "owl:Ontology"`
- ✅ `owl:versionInfo` présent
- ✅ Template réutilisable documenté

### Phase C — TscgGrammarValidator
- ✅ App Electron fonctionnelle
- ✅ Scanner corpus complet
- ✅ Migration m0→m1 automatique avec backup
- ✅ Validation SHACL intégrée
- ✅ Rapports conformité exportables (MD)
- ✅ UI dark theme cohérente
- ✅ Documentation README.md

---

## 📚 Ressources complémentaires

### Grammaires et schémas
- `M0_Instances_Schema_shacl.ttl` v1.1 (fourni)
- `M3_GenesisSpace.jsonld` (définit m3:ontologyType)
- `M2_GenericConcepts.jsonld` v15.10.1

### Documentation
- `TSCG_Smart_Prompt_v15_10_1.md` - Contexte framework complet
- `Poclet_Analysis_Methodology.md` - Méthodologie analyse poclets
- `M1_Extensions_Summary.md` - Vue d'ensemble extensions M1
- `M2_FormulasReference_v15_10_0.md` - Formules GenericConcepts

### Trackers
- `M0_Realignment_Tracker.md` - État réalignement par poclet
- `LOT6_FINAL_Analysis_Report.md` - Analyse corpus complète
- `TSCG_v15_1_0_Integration_Report.md` - Rapport migration v15

### Exemples de référence
- `M0_FireTriangle.jsonld` - Poclet canonique (à réaligner)
- `M0_Transistor.jsonld` - Exemple avec scores compacts ✅
- `M0_TrophicPyramid.jsonld` - Exemple avec multi-domaines

---

## 🚀 Commandes rapides pour Claude Code

```bash
# Validation SHACL d'un fichier
pyshacl -s ontology/M0_Instances_Schema_shacl.ttl \
        -df json-ld \
        instances/poclets/FireTriangle/M0_FireTriangle.jsonld

# Scanner tous les M0
find instances/poclets -name "M0_*.jsonld" -type f

# Extraire tous les domaines du corpus
grep -rh "\"m0:domain\"\|\"m1:domain\"" instances/poclets/ | sort | uniq

# Compter les violations d'un type
grep -r "owl:NamedIndividual" instances/poclets/ | wc -l

# Backup avant modification massive
cp -r instances/poclets instances/poclets.backup.$(date +%Y%m%d)

# Lancer TscgGrammarValidator (après création)
cd instances/tscg-tools/TscgGrammarValidator
npm start
```

---

## 💡 Conseils pour Claude Code

1. **Analyser avant de modifier** : Toujours scanner le corpus complet avant toute migration massive
2. **Backups systématiques** : Créer `.bak` avant chaque modification de M0
3. **Validation incrémentale** : Valider chaque M0 après correction (pas tout d'un coup)
4. **UTF-8 strict** : Utiliser `encoding='utf-8'` et `ensure_ascii=False` pour JSON-LD
5. **Git tracking** : Commit après chaque vague de migration réussie
6. **Logs détaillés** : TscgGrammarValidator doit logger toutes les modifications

---

## 📞 Contact/Questions

**Auteur :** Echopraxium (Michel) with the collaboration of Claude AI  
**Session date :** 2026-04-18  
**Framework version :** TSCG v15.11.0  
**Repo local :** `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\`

**Points de clarification potentiels pour Claude Code :**
- Confirmez structure exacte de `instances/poclets/` avant scan
- Vérifiez présence de `pyshacl` dans environnement Python
- Validez chemins absolus pour TscgGrammarValidator config

---

**FIN DU RÉSUMÉ** — Prêt pour transition vers Claude Code ! 🚀
