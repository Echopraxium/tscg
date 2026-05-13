# Templates M0 TSCG - Récapitulatif Complet

**Auteur:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-04-18  
**Version:** 1.0.0

## 📋 Vue d'Ensemble

Suite aux erreurs de validation SHACL sur `M0_FireTriangle.jsonld`, j'ai créé un ensemble complet de templates et d'outils pour faciliter la création et la maintenance des poclets M0 TSCG.

## 📦 Fichiers Créés

### 1. Correction de FireTriangle (Problème Immédiat)

#### `fix_firetriangle_float.py`
**Type:** Script Python  
**Objectif:** Corriger automatiquement le typage xsd:float dans M0_FireTriangle.jsonld  
**Utilisation:**
```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg
python fix_firetriangle_float.py
```
**Effet:** Ajoute `"@type": "xsd:float"` à toutes les propriétés de scores dans le @context

#### `M0_FireTriangle_CONTEXT_CORRECTED.json`
**Type:** Référence JSON  
**Objectif:** Exemple de @context complet et correct pour FireTriangle  
**Utilisation:** Référence pour copier-coller le @context manuellement

#### `GUIDE_FIX_FIRETRIANGLE.md`
**Type:** Documentation  
**Objectif:** Guide complet pour corriger M0_FireTriangle.jsonld  
**Contenu:** 
- Explication du problème
- Deux options de correction (manuelle vs automatique)
- Instructions de validation SHACL

---

### 2. Templates pour Futurs Poclets

#### `M0_CONTEXT_TEMPLATE.json`
**Type:** Template JSON  
**Objectif:** Template de @context standard TSCG avec tous les namespaces et typages float  
**Caractéristiques:**
- Tous les namespaces RDF/OWL standards
- Namespaces TSCG (m0, m1, m2, m3, eagle_eye, sphinx_eye)
- Exemples de namespaces M1 extensions commentés
- **12 propriétés float-typées explicitement** (solution au problème xsd:double)
- Commentaires inline pour documentation

**Utilisation:** Copier ce @context dans chaque nouveau poclet M0

#### `M0_POCLET_TEMPLATE.jsonld`
**Type:** Template JSON-LD complet  
**Objectif:** Point de départ complet pour créer un nouveau poclet  
**Contient:**
- @context complet avec tous les typages float
- Métadonnées obligatoires (rdfs:label, rdfs:comment, owl:versionInfo, etc.)
- Structure de scores ASFID/REVOI pré-remplie avec justifications
- Exemples de components et interactions
- Tous les champs conformes au schéma SHACL M0_Instances_Schema.shacl.ttl

**Utilisation:** Base pour créer un nouveau poclet (voir guide ci-dessous)

---

### 3. Documentation et Guides

#### `M0_TEMPLATES_USAGE_GUIDE.md`
**Type:** Guide d'utilisation complet  
**Objectif:** Documentation détaillée sur l'utilisation des templates  
**Sections:**
1. Utilisation pour créer un nouveau poclet (6 étapes)
2. Personnalisation des métadonnées
3. Ajout d'extensions M1 si nécessaire
4. Calcul et remplissage des scores ASFID/REVOI
5. Modélisation des composants et interactions
6. Validation SHACL
7. Checklist de validation (15 points)
8. Dépannage des erreurs courantes
9. Bonnes pratiques de nommage et structure

**Utilisation:** Consulter ce guide chaque fois que tu crées un nouveau poclet

---

### 4. Outils d'Automatisation

#### `create_new_poclet.ps1`
**Type:** Script PowerShell  
**Objectif:** Créer automatiquement un nouveau poclet à partir du template  
**Utilisation:**
```powershell
.\create_new_poclet.ps1 -Name "NewPocletName" -Domain "Physics"
```

**Options:**
- `-Name` (obligatoire) : Nom du poclet en PascalCase
- `-Domain` (obligatoire) : Domaine du poclet
- `-Label` (optionnel) : Titre court custom
- `-Description` (optionnel) : Description custom

**Actions automatiques:**
1. Crée le répertoire `instances/poclets/NewPocletName/`
2. Copie le template vers `M0_NewPocletName.jsonld`
3. Remplace automatiquement :
   - POCLET_NAME → NewPocletName
   - DOMAIN_NAME → Physics
   - Date → aujourd'hui
   - Labels/descriptions selon paramètres
4. Propose d'ouvrir le fichier dans l'éditeur

**Validation:** Vérifie que le nom est en PascalCase (warning sinon)

#### `fix_float_typing.py`
**Type:** Script Python générique  
**Objectif:** Corriger le typage float dans n'importe quel fichier JSON-LD  
**Utilisation:**
```bash
python fix_float_typing.py file1.jsonld file2.jsonld ...
python fix_float_typing.py --dry-run file.jsonld  # Test sans modification
```

**Utilisation avancée:** Traiter tous les M0 en batch
```bash
python fix_float_typing.py instances/poclets/*/M0_*.jsonld
```

#### `fix_m0_float_typing.bat`
**Type:** Script batch Windows  
**Objectif:** Wrapper Windows pour traiter tous les M0 automatiquement  
**Utilisation:**
```cmd
fix_m0_float_typing.bat
```
**Actions:** Trouve tous les `M0_*.jsonld` dans `instances/poclets/` et applique le fix

---

## 🎯 Flux de Travail Recommandé

### Pour Corriger FireTriangle (Maintenant)

**Option Rapide (Recommandée):**
```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg
python fix_firetriangle_float.py
pyshacl -s ontology/M0_Instances_Schema.shacl.ttl -df json-ld instances/poclets/FireTriangle/M0_FireTriangle.jsonld
```

**Option Manuelle:**
1. Ouvrir `M0_FireTriangle_CONTEXT_CORRECTED.json`
2. Copier le @context complet
3. Remplacer le @context dans `M0_FireTriangle.jsonld`
4. Valider avec pyshacl

---

### Pour Créer un Nouveau Poclet

**Option Automatique (Recommandée):**
```powershell
.\create_new_poclet.ps1 -Name "Crystallization" -Domain "Chemistry" -Label "Crystal Formation Process"
# Puis éditer le fichier généré
```

**Option Manuelle:**
1. Créer `instances/poclets/NewPoclet/`
2. Copier `M0_POCLET_TEMPLATE.jsonld` → `M0_NewPoclet.jsonld`
3. Éditer selon `M0_TEMPLATES_USAGE_GUIDE.md`
4. Valider avec SHACL

---

### Pour Mettre à Jour des Poclets Existants

Si d'autres poclets ont le problème xsd:double :

```bash
# Tous les poclets d'un coup
python fix_float_typing.py instances/poclets/*/M0_*.jsonld

# Ou via le batch Windows
fix_m0_float_typing.bat
```

---

## ✅ Checklist d'Installation

Copier ces fichiers dans ton dépôt TSCG :

```
E:\_00_Michel\_00_Lab\_00_GitHub\tscg\
├── fix_firetriangle_float.py          ← Script correction FireTriangle
├── fix_float_typing.py                ← Script correction générique
├── fix_m0_float_typing.bat            ← Batch Windows
├── M0_CONTEXT_TEMPLATE.json           ← Template @context
├── M0_POCLET_TEMPLATE.jsonld          ← Template poclet complet
├── M0_FireTriangle_CONTEXT_CORRECTED.json  ← Référence
├── create_new_poclet.ps1              ← Script création poclet
├── M0_TEMPLATES_USAGE_GUIDE.md        ← Guide d'utilisation
└── GUIDE_FIX_FIRETRIANGLE.md          ← Guide correction FireTriangle
```

---

## 🔧 Commandes Utiles

### Validation SHACL

```bash
# Valider un poclet spécifique
pyshacl -s ontology/M0_Instances_Schema.shacl.ttl ^
        -df json-ld ^
        instances/poclets/PocletName/M0_PocletName.jsonld

# Valider tous les poclets (bash)
for file in instances/poclets/*/M0_*.jsonld; do
    echo "Validating $file..."
    pyshacl -s ontology/M0_Instances_Schema.shacl.ttl -df json-ld "$file"
done
```

### Correction en Batch

```bash
# Dry run (voir ce qui serait fait)
python fix_float_typing.py --dry-run instances/poclets/*/M0_*.jsonld

# Réelle correction
python fix_float_typing.py instances/poclets/*/M0_*.jsonld
```

---

## 📚 Documentation de Référence

- **M0_Instances_Schema.shacl.ttl** - Schéma de validation (contraintes)
- **M2_GenericConcepts.jsonld** - 75 concepts génériques TSCG
- **M3_GenesisSpace.jsonld** - Définitions ASFID/REVOI
- **M0_FireTriangle.jsonld** - Poclet de référence canonique

---

## 🐛 Problèmes Connus et Solutions

### "Literal(..., datatype=xsd:double)"
**Cause:** @context manque les définitions `@type: xsd:float`  
**Solution:** Utiliser `M0_CONTEXT_TEMPLATE.json` ou `fix_float_typing.py`

### "FORBIDDEN: Use rdfs:label instead of dcterms:title"
**Cause:** Utilisation de propriétés dcterms au lieu de rdfs  
**Solution:** Utiliser `rdfs:label` et `rdfs:comment` (voir template)

### "m3:ontologyType MUST be one of..."
**Cause:** Utilisation de `m2:ontologyCategory` obsolète  
**Solution:** Utiliser `"m3:ontologyType": {"@id": "m3:Poclet"}` (voir template)

---

## 🎓 Pourquoi ce Problème Existe

**Contexte technique :**

JSON n'a qu'un seul type numérique décimal (`number`). Quand JSON-LD sérialise en RDF, il doit choisir un type XSD. Par défaut, il utilise `xsd:double` (64-bit floating point).

TSCG utilise `xsd:float` (32-bit) pour les scores car :
- Précision suffisante pour [0.0, 1.0]
- Plus compact en RDF/Turtle
- Convention établie dans le schéma SHACL

**Solution :**

JSON-LD permet de forcer le type via `@context` :
```json
"propertyName": {
  "@id": "namespace:propertyName",
  "@type": "xsd:float"  ← Force xsd:float au lieu de xsd:double
}
```

Tous les templates intègrent maintenant cette solution.

---

## 📞 Support

Questions ? Consulte dans l'ordre :
1. `M0_TEMPLATES_USAGE_GUIDE.md` - Guide complet
2. `GUIDE_FIX_FIRETRIANGLE.md` - Problème spécifique FireTriangle
3. Template files - Exemples concrets

---

**Dernière mise à jour :** 2026-04-18  
**Testé avec :** pyshacl 0.28.2, Python 3.11, Windows 11
