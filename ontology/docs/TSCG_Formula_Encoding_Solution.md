# 🔧 Solution Encodage Formules TSCG

## 📋 Problème Identifié

### Encodages actuels problématiques:

**Version originale (corrupted):**
```json
"m2:hasTensorFormula": "AÃƒÆ'Ã‚Â¢Ãƒâ€¦Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬ÂSÃƒÆ'Ã‚Â¢Ãƒâ€¦Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬ÂF"
```

**Version transcode.py (partiellement corrigée):**
```json
"m2:hasTensorFormula": "A¢ ¢S¢ ¢F"
```

**Attendu:**
```
A⊗S⊗F  (avec le vrai symbole ⊗ = produit tensoriel Unicode U+2297)
```

---

## ✅ Solution Proposée: Triple Représentation

Ajouter **3 attributs complémentaires** pour chaque formule:

### 1. `m2:hasTensorFormula` (Human-readable Unicode)
```json
"m2:hasTensorFormula": "A⊗S⊗F"
```
- **Encodage:** UTF-8 pur
- **Symbole:** ⊗ (U+2297 CIRCLED TIMES)
- **Usage:** Affichage direct, lecture humaine

### 2. `m2:tensorFormulaTeX` (LaTeX notation) ✨ **NOUVEAU**
```json
"m2:tensorFormulaTeX": "A \\otimes S \\otimes F"
```
- **Encodage:** ASCII pur (garantie zéro problème)
- **Symbole:** `\\otimes` (commande LaTeX standard)
- **Usage:** Documentation, publications, export LaTeX/PDF

### 3. `m2:tensorFormulaASCII` (Fallback ASCII) ✨ **NOUVEAU**
```json
"m2:tensorFormulaASCII": "A (x) S (x) F"
```
- **Encodage:** ASCII 7-bit (ultra-safe)
- **Symbole:** `(x)` représente ⊗
- **Usage:** Logs, systèmes legacy, débogage

---

## 📝 Exemple Complet: m2:Homeostasis

### Ancienne version (problématique):
```json
{
  "@id": "m2:Homeostasis",
  "m2:hasTensorFormula": "AÃƒÂ¢Ã…Â Ã¢â‚¬â€SÃƒÂ¢Ã…Â Ã¢â‚¬â€F",
  "m2:hasDominantM3": ["m3:eagle_eye:Attractor", "m3:eagle_eye:Structure", "m3:eagle_eye:Flow"]
}
```

### Nouvelle version (solution complète):
```json
{
  "@id": "m2:Homeostasis",
  "@type": ["owl:NamedIndividual", "m2:MetaConcept"],
  "rdfs:label": "Homeostasis",
  "rdfs:comment": "Self-regulation maintaining stable internal state despite external perturbations.",
  "m2:hasCategory": "m2:Regulatory",
  
  "m2:hasTensorFormula": "A⊗S⊗F",
  "m2:tensorFormulaTeX": "A \\otimes S \\otimes F",
  "m2:tensorFormulaASCII": "A (x) S (x) F",
  
  "m2:hasDominantM3": [
    "m3:eagle_eye:Attractor",
    "m3:eagle_eye:Structure",
    "m3:eagle_eye:Flow"
  ],
  "m2:hasEpistemicGap": 0.2,
  "m2:hasPolarity": "neutral",
  "m2:perspective": "territory"
}
```

---

## 🎯 Exemple: m2:ValueSpace (ORIVE)

```json
{
  "@id": "m2:ValueSpace",
  "@type": ["owl:NamedIndividual", "m2:MetaConcept"],
  "rdfs:label": "Value Space",
  "m2:hasCategory": "m2:Informational",
  
  "m2:hasTensorFormula": "O⊗R⊗I⊗V⊗E",
  "m2:tensorFormulaTeX": "O \\otimes R \\otimes I \\otimes V \\otimes E",
  "m2:tensorFormulaASCII": "O (x) R (x) I (x) V (x) E",
  
  "m2:perspective": "map",
  "m2:sphinxView": {
    "formulaPrimary": {
      "basis": "ORIVE",
      "formula": "O⊗R⊗I⊗V⊗E",
      "formulaTeX": "O \\otimes R \\otimes I \\otimes V \\otimes E",
      "formulaASCII": "O (x) R (x) I (x) V (x) E"
    },
    "formulaFallback": {
      "basis": "ASFID",
      "formula": "S⊗I",
      "formulaTeX": "S \\otimes I",
      "formulaASCII": "S (x) I"
    }
  }
}
```

---

## 🔧 Script de Correction Automatique

```python
#!/usr/bin/env python3
# fix_tensor_formulas.py

import json
import re
from pathlib import Path

# Mapping des formules corrompues vers UTF-8 correct
FORMULA_FIXES = {
    # ASFID formulas (Territory)
    r'A.*?S.*?F': 'A⊗S⊗F',
    r'A.*?S': 'A⊗S',
    r'A.*?I.*?D': 'A⊗I⊗D',
    r'I.*?F.*?D': 'I⊗F⊗D',
    r'I.*?S.*?D': 'I⊗S⊗D',
    r'S.*?D': 'S⊗D',
    r'I.*?F': 'I⊗F',
    r'I.*?S': 'I⊗S',
    r'S.*?F': 'S⊗F',
    r'A.*?D': 'A⊗D',
    r'F.*?D': 'F⊗D',
    
    # ORIVE formulas (Map)
    r'O.*?R.*?I': 'O⊗R⊗I',
    r'O.*?R.*?I.*?V.*?E': 'O⊗R⊗I⊗V⊗E',
    r'R.*?V.*?E': 'R⊗V⊗E',
    r'O.*?V': 'O⊗V',
    r'V.*?E': 'V⊗E',
}

def formula_to_tex(formula_unicode):
    """Convertit formule Unicode en LaTeX."""
    return formula_unicode.replace('⊗', ' \\otimes ')

def formula_to_ascii(formula_unicode):
    """Convertit formule Unicode en ASCII safe."""
    return formula_unicode.replace('⊗', ' (x) ')

def detect_and_fix_formula(corrupted_text):
    """Détecte et corrige une formule corrompue."""
    # Nettoyer les caractères mojibake
    clean = re.sub(r'[ÃÂâ€¢£¬]', '', corrupted_text)
    
    # Essayer de matcher avec patterns connus
    for pattern, correct in FORMULA_FIXES.items():
        if re.search(pattern, clean):
            return correct
    
    # Si pas de match, retourner None
    return None

def add_formula_variants(obj):
    """Ajoute les variantes TeX et ASCII aux formules."""
    if isinstance(obj, dict):
        # Traiter hasTensorFormula
        if 'm2:hasTensorFormula' in obj:
            formula = obj['m2:hasTensorFormula']
            
            # Si formule corrompue, la corriger
            if '⊗' not in formula:
                fixed = detect_and_fix_formula(formula)
                if fixed:
                    obj['m2:hasTensorFormula'] = fixed
                    formula = fixed
            
            # Ajouter variantes
            if '⊗' in formula:
                obj['m2:tensorFormulaTeX'] = formula_to_tex(formula)
                obj['m2:tensorFormulaASCII'] = formula_to_ascii(formula)
        
        # Traiter sphinxView.formulaPrimary
        if 'sphinxView' in obj and isinstance(obj['sphinxView'], dict):
            if 'formulaPrimary' in obj['sphinxView']:
                primary = obj['sphinxView']['formulaPrimary']
                if 'formula' in primary:
                    formula = primary['formula']
                    if '⊗' not in formula:
                        fixed = detect_and_fix_formula(formula)
                        if fixed:
                            primary['formula'] = fixed
                            formula = fixed
                    if '⊗' in formula:
                        primary['formulaTeX'] = formula_to_tex(formula)
                        primary['formulaASCII'] = formula_to_ascii(formula)
            
            # Traiter formulaFallback
            if 'formulaFallback' in obj['sphinxView']:
                fallback = obj['sphinxView']['formulaFallback']
                if 'formula' in fallback:
                    formula = fallback['formula']
                    if '⊗' not in formula:
                        fixed = detect_and_fix_formula(formula)
                        if fixed:
                            fallback['formula'] = fixed
                            formula = fixed
                    if '⊗' in formula:
                        fallback['formulaTeX'] = formula_to_tex(formula)
                        fallback['formulaASCII'] = formula_to_ascii(formula)
        
        # Traiter eagleView
        if 'eagleView' in obj and isinstance(obj['eagleView'], dict):
            if 'formula' in obj['eagleView']:
                formula = obj['eagleView']['formula']
                if '⊗' not in formula:
                    fixed = detect_and_fix_formula(formula)
                    if fixed:
                        obj['eagleView']['formula'] = fixed
                        formula = fixed
                if '⊗' in formula:
                    obj['eagleView']['formulaTeX'] = formula_to_tex(formula)
                    obj['eagleView']['formulaASCII'] = formula_to_ascii(formula)
        
        # Recursion
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                add_formula_variants(value)
    
    elif isinstance(obj, list):
        for item in obj:
            add_formula_variants(item)

def process_jsonld(input_file, output_file):
    """Traite un fichier JSON-LD."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Ajouter variantes
    add_formula_variants(data)
    
    # Écrire résultat
    with open(output_file, 'w', encoding='utf-8', ensure_ascii=False) as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Fichier corrigé: {output_file}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python fix_tensor_formulas.py input.jsonld [output.jsonld]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.jsonld', '_fixed.jsonld')
    
    process_jsonld(input_file, output_file)
```

---

## 📊 Table de Correspondance Complète

| Formule | Unicode (UTF-8) | LaTeX | ASCII Safe |
|---------|----------------|-------|------------|
| **ASFID Order-3** |
| A⊗S⊗F | A⊗S⊗F | A \\otimes S \\otimes F | A (x) S (x) F |
| A⊗I⊗D | A⊗I⊗D | A \\otimes I \\otimes D | A (x) I (x) D |
| I⊗F⊗D | I⊗F⊗D | I \\otimes F \\otimes D | I (x) F (x) D |
| I⊗S⊗D | I⊗S⊗D | I \\otimes S \\otimes D | I (x) S (x) D |
| **ASFID Order-2** |
| A⊗S | A⊗S | A \\otimes S | A (x) S |
| S⊗D | S⊗D | S \\otimes D | S (x) D |
| I⊗F | I⊗F | I \\otimes F | I (x) F |
| I⊗S | I⊗S | I \\otimes S | I (x) S |
| S⊗F | S⊗F | S \\otimes F | S (x) F |
| A⊗D | A⊗D | A \\otimes D | A (x) D |
| F⊗D | F⊗D | F \\otimes D | F (x) D |
| **ORIVE Order-5** |
| O⊗R⊗I⊗V⊗E | O⊗R⊗I⊗V⊗E | O \\otimes R \\otimes I \\otimes V \\otimes E | O (x) R (x) I (x) V (x) E |
| **ORIVE Partial** |
| O⊗R⊗I | O⊗R⊗I | O \\otimes R \\otimes I | O (x) R (x) I |
| R⊗V⊗E | R⊗V⊗E | R \\otimes V \\otimes E | R (x) V (x) E |
| O⊗V | O⊗V | O \\otimes V | O (x) V |
| V⊗E | V⊗E | V \\otimes E | V (x) E |
| **Hybrid (Domain)** |
| (A⊗S⊗F⊗I⊗D)⊗(O⊗R⊗I⊗V⊗E) | (ASFID)⊗(ORIVE) | (A \\otimes S \\otimes F \\otimes I \\otimes D) \\otimes (O \\otimes R \\otimes I \\otimes V \\otimes E) | (ASFID) (x) (ORIVE) |

---

## 🎯 Avantages de la Solution

### 1. **Robustesse**
- ✅ UTF-8 pur pour Unicode (⊗)
- ✅ LaTeX pour publications scientifiques
- ✅ ASCII pour compatibilité universelle

### 2. **Interopérabilité**
- ✅ Export direct vers LaTeX/PDF
- ✅ Affichage garanti dans tous systèmes
- ✅ Logs lisibles en ASCII

### 3. **Maintenabilité**
- ✅ Triple vérification croisée
- ✅ Conversion automatique garantie
- ✅ Zéro ambiguïté

### 4. **Documentation**
- ✅ LaTeX dans papers académiques
- ✅ Unicode dans interfaces web
- ✅ ASCII dans READMEs

---

## 📋 Action Items

1. ✅ **Ajouter propriétés OWL:**
   ```turtle
   m2:tensorFormulaTeX rdf:type owl:DatatypeProperty ;
       rdfs:domain m2:MetaConcept ;
       rdfs:range xsd:string .
   
   m2:tensorFormulaASCII rdf:type owl:DatatypeProperty ;
       rdfs:domain m2:MetaConcept ;
       rdfs:range xsd:string .
   ```

2. ✅ **Corriger M2_MetaConcepts.jsonld:**
   - Remplacer formules corrompues par UTF-8 pur
   - Ajouter tensorFormulaTeX
   - Ajouter tensorFormulaASCII

3. ✅ **Mettre à jour M0 poclets:**
   - Propager triple représentation
   - Cohérence dans tous fichiers

4. ✅ **Documentation:**
   - README expliquant convention
   - Exemples d'usage

---

**Fin de la proposition**
