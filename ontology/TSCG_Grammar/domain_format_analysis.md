# Analyse du Problème de Format `m1:domain`

## Problème Identifié

**Symptôme:** Certaines instances ont `"m1:domain": "Photography / Optics"` au lieu de `"m1:domain": ["Photography", "Optics"]`

**Exemple problématique:**
```json
"m1:domain": "Photography / Optics"
```

**Format correct attendu:**
```json
"m1:domain": ["Photography", "Optics"]
```

## Diagnostic: Où se situe le problème?

### 1. ✅ Script de Validation (`validate_m0_instance.py`)
**Verdict:** Fonctionne correctement selon la grammaire SHACL actuelle

Le script de validation exécute simplement pyshacl contre la grammaire - il ne fait aucune transformation des données. Il valide ce que la grammaire SHACL définit comme acceptable.

### 2. ✅ Script de Migration (`automated_migration_easy_instances.py`)
**Verdict:** Fonctionne correctement - copie la valeur telle quelle

**Fonction concernée:** `migrate_domain_from_graph_objects()` (lignes 91-132)

```python
# Le script copie simplement la valeur sans transformation:
ontology["m1:domain"] = domain_value  # ligne 127
```

Le script:
1. Cherche `m0:domain` dans @graph[1], @graph[2], etc.
2. Extrait sa valeur **telle quelle**
3. L'ajoute à @graph[0] comme `m1:domain`
4. Supprime `m0:domain` de la source

**Important:** Le script NE transforme PAS le format - il copie la valeur originale.

### 3. ❌ Grammaire SHACL (`M0_Instances_Schema_shacl.ttl`)
**Verdict:** TROP PERMISSIVE - accepte les deux formats

**Lignes 141-150:**
```turtle
sh:property [
  sh:path m1:domain ;
  sh:or (
    [ sh:datatype xsd:string ]           # ❌ Accepte "Photography / Optics"
    [ sh:nodeKind sh:Literal ]           # ✅ Accepte ["Photography", "Optics"]
  ) ;
  sh:minCount 1 ;
```

**Problème:** La contrainte `sh:datatype xsd:string` accepte N'IMPORTE QUELLE chaîne, y compris `"Photography / Optics"`.

### 4. ❌ Données Sources (instances originales)
**Verdict:** Contenaient déjà le format incorrect

Les instances originales (avant migration) avaient probablement déjà `"m0:domain": "Photography / Optics"`, et le script de migration a simplement copié cette valeur incorrecte vers `m1:domain`.

## Cause Racine

**Double problème:**
1. **Grammaire trop permissive:** SHACL accepte à la fois le format string avec "/" ET le format array
2. **Données historiques incorrectes:** Certaines instances avaient le format avec "/" dès le départ

## Solutions Recommandées

### Solution 1: Corriger la Grammaire SHACL (Recommandé)

**Modifier la contrainte pour:**
- ✅ Accepter une chaîne simple pour un domaine unique: `"Chemistry"`
- ✅ Accepter un array pour des domaines multiples: `["Photography", "Optics"]`
- ❌ REJETER les chaînes avec "/" pour domaines multiples: `"Photography / Optics"`

**Nouvelle contrainte suggérée:**
```turtle
sh:property [
  sh:path m1:domain ;
  sh:or (
    # Single domain: string without "/" separator
    [ 
      sh:datatype xsd:string ;
      sh:pattern "^[^/]+$" ;  # Reject strings containing "/"
    ]
    # Multiple domains: array of strings
    [ 
      sh:nodeKind sh:Literal ;
      # Could add sh:minCount 2 to enforce array for multiple domains
    ]
  ) ;
  sh:minCount 1 ;
  sh:message "m1:domain MUST use: single string ('Chemistry') for one domain, or array (['Chemistry', 'Physics']) for multiple domains. String format with '/' separator is NOT allowed." ;
] ;
```

### Solution 2: Script de Correction des Instances

Créer un script Python pour convertir automatiquement:
- `"Photography / Optics"` → `["Photography", "Optics"]`
- `"Chemistry / Physics"` → `["Chemistry", "Physics"]`

**Pattern de détection:**
```python
if isinstance(domain_value, str) and "/" in domain_value:
    # Split and clean
    domains = [d.strip() for d in domain_value.split("/")]
    ontology["m1:domain"] = domains
```

## Impact

**Instances affectées:** À déterminer par scan du corpus

**Exemples connus:**
- ExposureTriangle: `"Photography / Optics"` → `["Photography", "Optics"]`
- (Autres instances à identifier)

## Recommandation Finale

**Approche en 2 étapes:**

1. **Étape 1 - Correction des données:**
   - Créer un script de conversion `fix_domain_format.py`
   - Scanner toutes les instances pour détecter le format avec "/"
   - Convertir automatiquement vers le format array

2. **Étape 2 - Durcissement de la grammaire:**
   - Mettre à jour `M0_Instances_Schema_shacl.ttl`
   - Ajouter une contrainte pour rejeter les "/" dans les strings
   - Documenter le format standard dans les messages de validation

Cette approche garantit:
- ✅ Correction des données existantes
- ✅ Prévention de futures erreurs via SHACL
- ✅ Cohérence du corpus
