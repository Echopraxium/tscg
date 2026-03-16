# ⚡ Installation Express - TSCG JSON-LD → Turtle Converter

## 📁 Structure Exacte du Projet

```
tscg/                                    ← RACINE du repository GitHub
│
├── ontology/                            ← Ontologies TSCG
│   ├── M3_EagleEye.jsonld              → sera converti en .ttl
│   ├── M3_SphinxEye.jsonld             → sera converti en .ttl
│   ├── M3_GenesisSpace.jsonld          → sera converti en .ttl
│   ├── M2_MetaConcepts.jsonld          → sera converti en .ttl
│   ├── M1_CoreConcepts.jsonld          → sera converti en .ttl
│   └── M1_extensions/
│       ├── biology/M1_Biology.jsonld   → sera converti en .ttl
│       ├── chemistry/M1_Chemistry.jsonld
│       ├── mythology/M1_Mythology.jsonld
│       ├── optics/M1_Optics.jsonld
│       └── photography/M1_Photography.jsonld
│
├── instances/                       ← Modèles de systèmes
│   ├── poclets/
│   │   ├── M0_FireTriangle.jsonld      → sera converti en .ttl
│   │   ├── M0_RAAS.jsonld              → sera converti en .ttl
│   │   └── [tous les autres poclets...]
│   └── validation/
│       └── [modèles de validation...]
│
└── src/
    └── tscg/
        └── ontology_tools/              ← COPIER LES FICHIERS ICI
            ├── jsonld_to_turtle.py      ← Script principal
            ├── requirements.txt          ← Dépendances
            ├── _convert_to_turtle.bat   ← Windows (double-clic)
            ├── convert_to_turtle.sh     ← Linux/Mac
            ├── test_converter.py        ← Test installation
            ├── README.md                ← Doc complète (EN)
            ├── GUIDE_FR.md              ← Guide français
            ├── CHANGELOG.md             ← Versions
            └── .gitignore               ← Fichiers à ignorer
```

---

## 🚀 Installation en 3 Étapes

### Étape 1 : Copier les fichiers

**Si `src/tscg/` n'existe pas encore :**
```bash
cd tscg  # Aller à la racine du repo
mkdir -p src/tscg
```

**Copier le dossier `ontology_tools/` :**
```bash
cp -r ontology_tools/ src/tscg/
```

**Résultat :**
```
tscg/src/tscg/ontology_tools/  ✓ Tous les fichiers copiés
```

---

### Étape 2 : Installer rdflib

```bash
cd src/tscg/ontology_tools
pip install rdflib
```

**OU** (méthode complète) :
```bash
pip install -r requirements.txt
```

---

### Étape 3 : Tester

```bash
python test_converter.py
```

**Résultat attendu :**
```
✓ PASS  Python Version
✓ PASS  RDFLib Library
✓ PASS  Converter Script
✓ PASS  Help Message
✓ PASS  Dry-Run Mode

Tests passed: 5/5
✓ All tests passed! Converter is ready to use.
```

---

## ⚡ Utilisation Immédiate

### Windows (Double-clic)
```
Double-cliquer sur : _convert_to_turtle.bat
```

### Ligne de commande
```bash
# Preview (sans conversion)
python jsonld_to_turtle.py --dry-run

# Conversion complète
python jsonld_to_turtle.py

# Continuer sur erreurs
python jsonld_to_turtle.py --skip-errors
```

---

## 🎯 Fonctionnement Automatique

### Détection de la Racine

Le script **détecte automatiquement** la racine du projet :

```
Depuis: src/tscg/ontology_tools/
    ↑
    ├─ Remonte à: src/tscg/
    ↑
    ├─ Remonte à: src/
    ↑
    └─ Remonte à: tscg/  ← RACINE DÉTECTÉE ✓
        ├── ontology/       ← Trouvé !
        └── instances/  ← Trouvé !
```

**Vous n'avez RIEN à configurer !** 🎉

---

## 📊 Ce Qui Est Converti

**Scan récursif de :**
- ✅ `ontology/` et tous ses sous-dossiers
- ✅ `instances/` et tous ses sous-dossiers

**Pour chaque fichier `.jsonld` trouvé :**
```
M3_EagleEye.jsonld  →  M3_EagleEye.ttl  (même dossier)
```

**Estimation pour TSCG :**
- ~58 fichiers `.jsonld`
- ~10 secondes de conversion
- ~2-3 MB de fichiers `.ttl` générés

---

## ✅ Vérification avec Protégé

1. **Ouvrir Protégé**
2. **File → Open...** 
3. Sélectionner `ontology/M2_MetaConcepts.ttl`
4. **Reasoner → Pellet → Start Reasoner**
5. Attendre la classification (quelques secondes)
6. **Entities → Classes** pour voir la hiérarchie

**Signes de succès :**
- ✓ Classes s'affichent correctement
- ✓ Propriétés visibles
- ✓ Pas d'erreur "Inconsistent Ontology"
- ✓ Annotations préservées

---

## 🐛 Dépannage Express

### rdflib not found
```bash
pip install rdflib
```

### Python not found
Installer Python 3.8+ : https://www.python.org/

### Structure différente
```bash
python jsonld_to_turtle.py --root-dir /chemin/vers/tscg
```

### Voir les erreurs détaillées
```bash
python jsonld_to_turtle.py --verbose
```

---

## 📚 Documentation Complète

- **GUIDE_FR.md** : Guide complet en français
- **README.md** : Complete guide in English
- **CHANGELOG.md** : Version history

---

## 🎓 Rappel Important

**REVOI** signifie :
- **R**epresentability (jamais Reproducibility !)
- **E**volvability
- **V**erifiability
- **O**bservability
- **I**nteroperability

---

**Prêt à convertir !** 🚀

Commencez par un dry-run pour voir ce qui sera converti :
```bash
python jsonld_to_turtle.py --dry-run
```
