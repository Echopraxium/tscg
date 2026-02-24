# 🔄 Outil de Conversion JSON-LD → OWL Turtle pour TSCG

**Version** : 1.0.0  
**Date** : 15 février 2026  
**Auteur** : Echopraxium avec la collaboration de Claude AI

---

## 📦 Contenu du Package

Le dossier `ontology_tools/` contient tous les fichiers nécessaires pour convertir vos ontologies :

```
ontology_tools/
├── jsonld_to_turtle.py          # Script Python principal
├── requirements.txt              # Dépendances Python
├── README.md                     # Documentation complète (EN)
├── CHANGELOG.md                  # Historique des versions
├── test_converter.py             # Script de test
├── _convert_to_turtle.bat        # Script Windows (double-clic)
├── convert_to_turtle.sh          # Script Unix/Linux/Mac
└── .gitignore                    # Fichiers à ignorer dans Git
```

---

## 🚀 Installation Rapide

### Structure du Projet TSCG

Votre projet doit avoir cette structure :

```
tscg/                         ← Racine du repository GitHub
├── ontology/                 ← Ontologies TSCG (M3, M2, M1)
│   ├── M3_EagleEye.jsonld
│   ├── M3_SphinxEye.jsonld
│   ├── M2_MetaConcepts.jsonld
│   └── M1_extensions/
├── system-models/            ← Modèles de systèmes (M0 poclets)
│   ├── poclets/
│   └── validation/
└── src/                      
    └── tscg/
        └── ontology_tools/   ← PLACER LES FICHIERS ICI
            ├── jsonld_to_turtle.py
            ├── requirements.txt
            ├── _convert_to_turtle.bat
            └── ...
```

### Étape 1 : Placer les fichiers

Copier **tout le dossier `ontology_tools/`** dans votre projet :

```
tscg/src/tscg/ontology_tools/    ← Destination
```

Si le dossier `src/tscg/` n'existe pas encore, créez-le d'abord :

```bash
mkdir -p src/tscg
```

Puis copiez le dossier `ontology_tools/` dedans.

### Étape 2 : Installer les dépendances

```bash
cd src/tscg/ontology_tools
pip install -r requirements.txt
```

**OU** (si pip install ne fonctionne pas) :

```bash
pip install rdflib
```

### Étape 3 : Tester l'installation

```bash
python test_converter.py
```

Vous devriez voir :
```
✓ PASS  Python Version
✓ PASS  RDFLib Library
✓ PASS  Converter Script
✓ PASS  Help Message
✓ PASS  Dry-Run Mode

Tests passed: 5/5
```

---

## 🎯 Utilisation Simple

### Détection Automatique de la Racine

Le script **détecte automatiquement** la racine du projet TSCG en cherchant les dossiers `ontology/` et `system-models/`.

Depuis le dossier `src/tscg/ontology_tools/`, le script remonte automatiquement de 3 niveaux pour trouver la racine :
```
src/tscg/ontology_tools/ → src/tscg/ → src/ → RACINE/
```

**Vous n'avez donc RIEN à configurer !** 🎉

### Windows (Double-clic)

1. Double-cliquer sur `_convert_to_turtle.bat`
2. Attendre la fin de la conversion
3. Les fichiers `.ttl` sont créés à côté des `.jsonld`

### Ligne de commande (Windows/Linux/Mac)

```bash
# Preview de ce qui sera converti (SANS conversion)
python jsonld_to_turtle.py --dry-run

# Conversion complète
python jsonld_to_turtle.py

# Conversion avec gestion d'erreurs
python jsonld_to_turtle.py --skip-errors
```

### Si la structure est différente

Si votre projet a une structure non-standard :

```bash
python jsonld_to_turtle.py --root-dir /chemin/vers/racine/tscg
```

---

## 📂 Ce qui est converti

**Tous les fichiers .jsonld dans** :

```
ontology/
├── M3_EagleEye.jsonld       → M3_EagleEye.ttl
├── M3_SphinxEye.jsonld      → M3_SphinxEye.ttl
├── M3_GenesisSpace.jsonld   → M3_GenesisSpace.ttl
├── M2_MetaConcepts.jsonld   → M2_MetaConcepts.ttl
├── M1_CoreConcepts.jsonld   → M1_CoreConcepts.ttl
└── M1_extensions/
    ├── biology/M1_Biology.jsonld         → .ttl
    ├── chemistry/M1_Chemistry.jsonld     → .ttl
    ├── mythology/M1_Mythology.jsonld     → .ttl
    ├── optics/M1_Optics.jsonld           → .ttl
    └── photography/M1_Photography.jsonld → .ttl

system-models/
├── poclets/
│   ├── M0_FireTriangle.jsonld → .ttl
│   ├── M0_RAAS.jsonld         → .ttl
│   └── [tous les autres poclets...]
└── validation/
    └── [tous les modèles de validation...]
```

---

## 📊 Rapport de Conversion

Après l'exécution, vous verrez :

```
======================================================================
TSCG JSON-LD to OWL Turtle Converter v1.0.0
======================================================================
Root directory: C:\Projects\tscg
Target directories: ontology, system-models

Scanning for .jsonld files...
Found 58 .jsonld files

Starting conversion...
----------------------------------------------------------------------
[1/58] Processing...
Converting: ontology/M3_EagleEye.jsonld
  ✓ Created: ontology/M3_EagleEye.ttl

[2/58] Processing...
Converting: ontology/M2_MetaConcepts.jsonld
  ✓ Created: ontology/M2_MetaConcepts.ttl

...

======================================================================
CONVERSION SUMMARY
======================================================================
Files found:     58
Files converted: 58
Files failed:    0
Files skipped:   0
======================================================================
✓ All files converted successfully!
```

Un fichier log détaillé est créé : `conversion_YYYYMMDD_HHMMSS.log`

---

## 🔍 Vérification avec Protégé

### Étape 1 : Ouvrir un fichier .ttl

1. Lancer Protégé
2. **File → Open...**
3. Sélectionner `ontology/M2_MetaConcepts.ttl`
4. Cliquer **Open**

### Étape 2 : Activer un raisonneur

1. **Reasoner → Pellet** (ou HermiT, ELK)
2. **Reasoner → Start Reasoner**
3. Attendre la classification (quelques secondes)
4. Voir la hiérarchie inférée : **Entities → Classes**

### Étape 3 : Vérifier les résultats

✅ **Signes de succès** :
- La hiérarchie des classes s'affiche
- Les propriétés sont visibles
- Pas d'erreur "Inconsistent Ontology"
- Les annotations sont préservées

❌ **Problèmes possibles** :
- Erreur "Parse Error" → Le fichier JSON-LD source est invalide
- "Inconsistent Ontology" → Il y a une contradiction logique (utile à savoir !)
- Imports non résolus → Vérifier les URIs

---

## 🔧 Options Avancées

### Convertir vers un dossier séparé

```bash
python jsonld_to_turtle.py --output-dir ../turtle-ontologies
```

Résultat :
```
turtle-ontologies/
├── ontology/
│   ├── M3_EagleEye.ttl
│   ├── M2_MetaConcepts.ttl
│   └── ...
└── system-models/
    └── ...
```

### Mode verbeux (debug)

```bash
python jsonld_to_turtle.py --verbose > conversion.log 2>&1
```

### Continuer malgré les erreurs

```bash
python jsonld_to_turtle.py --skip-errors
```

---

## ⚠️ Résolution de Problèmes

### Erreur : "rdflib not found"

**Solution** :
```bash
pip install rdflib
```

### Erreur : "Python not found"

**Solution** :
- Installer Python 3.8+ depuis https://www.python.org/
- Sur Windows, cocher "Add Python to PATH" pendant l'installation

### Erreur : UTF-8 encoding

Le script gère automatiquement l'UTF-8. Si vous voyez des erreurs :
1. Vérifier que vos fichiers `.jsonld` sont en UTF-8
2. Utiliser `--skip-errors` pour continuer
3. Consulter le log pour identifier les fichiers problématiques

### Fichiers manquants

Le script attend cette structure :
```
tscg/                          ← Racine du repository
├── ontology/                  ← Doit exister
├── system-models/             ← Doit exister
└── src/tscg/ontology_tools/   ← Vous êtes ici
```

**Le script détecte automatiquement la racine** en cherchant les dossiers `ontology/` et `system-models/`.

Si vous avez une structure différente :
```bash
python jsonld_to_turtle.py --root-dir /chemin/vers/tscg
```

---

## 🎯 Prochaines Étapes Après Conversion

1. **Ouvrir dans Protégé** pour visualiser la structure
2. **Lancer un raisonneur OWL** pour détecter :
   - Incohérences logiques
   - Subsomptions implicites
   - Classes insatisfiables
3. **Exécuter des requêtes SPARQL** pour analyse
4. **Valider avec SHACL** (si vous avez des shapes)

---

## 📝 Notes Importantes

### ✅ Avantages de Turtle pour TSCG

1. **Protégé** : Support natif complet
2. **Raisonneurs** : Pellet, HermiT, ELK fonctionnent mieux
3. **Lisibilité** : Format plus compact et lisible
4. **Standard** : Format de facto pour OWL 2

### ⚙️ Conservation des données

- ✅ Tous les triples RDF préservés
- ✅ Tous les axiomes OWL préservés
- ✅ Toutes les annotations préservées
- ✅ Conversion bidirectionnelle sans perte

### 🔄 Workflow suggéré

1. **Développement** : Garder JSON-LD comme source
2. **Conversion** : Générer .ttl pour Protégé/raisonneurs
3. **Validation** : Utiliser Protégé + raisonneur
4. **Mise à jour** : Modifier JSON-LD, re-générer .ttl

---

## 📚 Documentation Complète

Consulter `README.md` (en anglais) pour :
- Guide détaillé de toutes les options
- Exemples d'utilisation avancés
- Intégration avec Apache Jena
- Requêtes SPARQL
- Et plus encore...

---

## 🐛 Bugs ou Questions ?

- Créer une issue sur le repo TSCG GitHub
- Consulter le fichier `CHANGELOG.md` pour les versions
- Vérifier le fichier log de conversion

---

## ✅ Checklist Post-Conversion

- [ ] Tous les fichiers .ttl créés
- [ ] Ouvert M2_MetaConcepts.ttl dans Protégé
- [ ] Raisonneur exécuté sans erreurs
- [ ] Hiérarchie des classes visible
- [ ] Imports fonctionnent correctement
- [ ] Pas de warnings UTF-8

---

**Bon travail avec le raisonneur OWL !** 🎉

Pour rappel, **REVOI** = **R**epresentability, **E**volvability, **V**erifiability, **O**bservability, **I**nteroperability  
(R n'est jamais "Reproducibility" !)
