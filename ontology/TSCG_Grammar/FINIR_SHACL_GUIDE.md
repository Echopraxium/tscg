# Mini-Guide : Terminer les corrections SHACL (5 minutes)

## 📍 Statut actuel

**Fichier :** `M0_Instances_Schema.shacl.ttl`  
**État :** PARTIELLEMENT corrigé (7/10 dimensions mises à jour vers M3)

### ✅ Déjà fait (ASFID + 3 REVOI)
- `m0:A` → `m3:eagle_eye:Attractor` ✅
- `m0:S` → `m3:eagle_eye:Structure` ✅
- `m0:F` → `m3:eagle_eye:Flow` ✅
- `m0:I` (ASFID) → `m3:eagle_eye:Information` ✅
- `m0:D` → `m3:eagle_eye:Dynamics` ✅
- `m0:R` → `m3:sphinx_eye:Representable` ✅
- `m0:E` → `m3:sphinx_eye:Evolvable` ✅
- `m0:V` → `m3:sphinx_eye:Verifiable` ✅

### ⏳ Reste à faire (2 REVOI)
- `m0:O` → `m3:sphinx_eye:Observable` ❌
- `m3:eagle_eye:Information` (REVOI) → `m3:sphinx_eye:Interoperable` ❌

---

## 🔧 Instructions (2 modifications)

### 1. Ouvrir le fichier
```cmd
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg\ontology
notepad M0_Instances_Schema.shacl.ttl
```

### 2. Chercher et remplacer (Ctrl+H dans Notepad)

#### **Modification 1 : Observable**
**Chercher :** (ligne ~284)
```turtle
  sh:property [
    sh:path m3:sphinx_eye:Observable ;
```

**Remplacer par :**
```turtle
  sh:property [
    sh:path m3:sphinx_eye:Observable ;
```

#### **Modification 2 : Interoperable**
**Chercher :** (ligne ~293)
```turtle
  sh:property [
    sh:path m3:eagle_eye:Information ;
    sh:datatype xsd:float ;
    sh:minInclusive 0.0 ;
    sh:maxInclusive 1.0 ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "REVOI I (Interoperability) score is mandatory (0.0-1.0)"
```

**Remplacer par :**
```turtle
  sh:property [
    sh:path m3:sphinx_eye:Interoperable ;
    sh:datatype xsd:float ;
    sh:minInclusive 0.0 ;
    sh:maxInclusive 1.0 ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:message "REVOI I (Interoperable) score is mandatory (0.0-1.0)"
```

### 3. Mettre à jour la version et le changelog

**Chercher :** (ligne ~4)
```turtle
# Date: 2026-04-13 (initial), 2026-04-18 (v1.1 - domain migration)
# Status: UPDATED - Domain property migrated to M1 level
```

**Remplacer par :**
```turtle
# Date: 2026-04-13 (initial), 2026-04-18 (v1.1 - domain migration, v1.2 - M3 dimensions)
# Status: UPDATED - Domain migrated to M1, ASFID/REVOI dimensions migrated to M3
```

### 4. Sauvegarder et fermer

---

## ✅ Validation finale

```cmd
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg
pyshacl -s ontology/M0_Instances_Schema.shacl.ttl -df json-ld instances/poclets/FireTriangle/M0_FireTriangle.jsonld
```

**Résultat attendu :**
```
Conforms: True
```

Ou 