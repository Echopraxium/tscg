#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_tensor_formulas.py - Correction automatique des formules tensorielles TSCG
Ajoute triple représentation: Unicode (⊗), LaTeX (\\otimes), ASCII ((x))
"""

import json
import re
import sys
from pathlib import Path

# Symbole tensoriel correct
TENSOR_SYMBOL = '⊗'  # U+2297 CIRCLED TIMES

# Mapping exhaustif des formules TSCG connues
KNOWN_FORMULAS = {
    # ASFID Order-3
    'ASF': 'A⊗S⊗F',
    'AID': 'A⊗I⊗D',
    'IFD': 'I⊗F⊗D',
    'ISD': 'I⊗S⊗D',
    'ASD': 'A⊗S⊗D',
    'SFD': 'S⊗F⊗D',
    'AFD': 'A⊗F⊗D',
    
    # ASFID Order-2
    'AS': 'A⊗S',
    'SD': 'S⊗D',
    'IF': 'I⊗F',
    'IS': 'I⊗S',
    'SF': 'S⊗F',
    'AD': 'A⊗D',
    'FD': 'F⊗D',
    'AI': 'A⊗I',
    'AF': 'A⊗F',
    'ID': 'I⊗D',
    
    # ORIVE Order-5
    'ORIVE': 'O⊗R⊗I⊗V⊗E',
    
    # ORIVE Partial
    'ORI': 'O⊗R⊗I',
    'RVE': 'R⊗V⊗E',
    'OV': 'O⊗V',
    'VE': 'V⊗E',
    'OR': 'O⊗R',
    'RI': 'R⊗I',
    'IV': 'I⊗V',  # Attention: conflit potentiel avec I⊗V ASFID
    'OI': 'O⊗I',
    'OE': 'O⊗E',
    'RE': 'R⊗E',
}

def clean_mojibake(text):
    """Nettoie les caractères mojibake courants."""
    # Remplacements simples d'abord
    replacements = [
        ('Ã¢Å"Â¨', '⊗'),
        ('¢ ¢', '⊗'),
        ('¢¢', '⊗'),
    ]
    
    for old, new in replacements:
        text = text.replace(old, new)
    
    # Patterns regex ensuite
    text = re.sub(r'[ÃÂâ€¢£¬®°±²³´µ¶·¸¹º»¼½¾¿]+', '', text)
    
    return text.strip()

def detect_formula_pattern(text):
    """Détecte le pattern de formule dans un texte corrompu."""
    # Nettoyer d'abord
    clean = clean_mojibake(text)
    
    # Extraire les lettres majuscules
    letters = ''.join(c for c in clean if c.isupper() and c in 'ASFIDORIVE')
    
    # Chercher dans formules connues
    if letters in KNOWN_FORMULAS:
        return KNOWN_FORMULAS[letters]
    
    # Si pas trouvé, essayer de reconstruire
    if letters:
        # Vérifier cohérence ASFID vs ORIVE
        asfid_chars = set('ASFID')
        orive_chars = set('ORIVE')
        letter_set = set(letters)
        
        if letter_set.issubset(asfid_chars):
            # Formule ASFID
            return '⊗'.join(letters)
        elif letter_set.issubset(orive_chars):
            # Formule ORIVE
            return '⊗'.join(letters)
        else:
            # Formule hybride ou inconnue
            return '⊗'.join(letters)
    
    return None

def formula_to_tex(formula_unicode):
    """Convertit formule Unicode en LaTeX."""
    if not formula_unicode or TENSOR_SYMBOL not in formula_unicode:
        return formula_unicode
    return formula_unicode.replace(TENSOR_SYMBOL, ' \\otimes ')

def formula_to_ascii(formula_unicode):
    """Convertit formule Unicode en ASCII safe."""
    if not formula_unicode or TENSOR_SYMBOL not in formula_unicode:
        return formula_unicode
    return formula_unicode.replace(TENSOR_SYMBOL, ' (x) ')

def fix_formula_in_object(obj, key='formula'):
    """Corrige une formule et ajoute ses variantes."""
    if key not in obj:
        return False
    
    formula = obj[key]
    fixed = False
    
    # Si déjà correct (contient ⊗), juste ajouter variantes
    if TENSOR_SYMBOL in formula:
        obj[f'{key}TeX'] = formula_to_tex(formula)
        obj[f'{key}ASCII'] = formula_to_ascii(formula)
        return True
    
    # Sinon, détecter et corriger
    detected = detect_formula_pattern(formula)
    if detected:
        obj[key] = detected
        obj[f'{key}TeX'] = formula_to_tex(detected)
        obj[f'{key}ASCII'] = formula_to_ascii(detected)
        fixed = True
        print(f"  ✓ Corrigé: '{formula}' → '{detected}'")
    
    return fixed

def process_metaconcept(obj, stats):
    """Traite un métaconcept."""
    if not isinstance(obj, dict):
        return
    
    # Identifier le métaconcept
    concept_id = obj.get('@id', 'unknown')
    fixed_any = False
    
    # 1. Traiter m2:hasTensorFormula (niveau principal)
    if 'm2:hasTensorFormula' in obj:
        if fix_formula_in_object(obj, 'm2:hasTensorFormula'):
            stats['formulas_fixed'] += 1
            fixed_any = True
    
    # 2. Traiter eagleView
    if 'eagleView' in obj and isinstance(obj['eagleView'], dict):
        if fix_formula_in_object(obj['eagleView'], 'formula'):
            stats['eagle_formulas_fixed'] += 1
            fixed_any = True
    
    # 3. Traiter sphinxView.formulaPrimary
    if 'sphinxView' in obj and isinstance(obj['sphinxView'], dict):
        sphinx = obj['sphinxView']
        
        if 'formulaPrimary' in sphinx and isinstance(sphinx['formulaPrimary'], dict):
            if fix_formula_in_object(sphinx['formulaPrimary'], 'formula'):
                stats['sphinx_primary_fixed'] += 1
                fixed_any = True
        
        if 'formulaFallback' in sphinx and isinstance(sphinx['formulaFallback'], dict):
            if fix_formula_in_object(sphinx['formulaFallback'], 'formula'):
                stats['sphinx_fallback_fixed'] += 1
                fixed_any = True
    
    # 4. Traiter m2:dualView si présent
    if 'm2:dualView' in obj and isinstance(obj['m2:dualView'], dict):
        dual = obj['m2:dualView']
        if 'territoryFormula' in dual:
            if fix_formula_in_object(dual, 'territoryFormula'):
                stats['dual_territory_fixed'] += 1
                fixed_any = True
        if 'mapFormula' in dual:
            if fix_formula_in_object(dual, 'mapFormula'):
                stats['dual_map_fixed'] += 1
                fixed_any = True
    
    if fixed_any:
        stats['metaconcepts_modified'] += 1

def process_graph(graph, stats):
    """Traite le @graph d'une ontologie JSON-LD."""
    if not isinstance(graph, list):
        return
    
    for item in graph:
        if isinstance(item, dict):
            # Vérifier si c'est un métaconcept
            item_type = item.get('@type', [])
            if isinstance(item_type, str):
                item_type = [item_type]
            
            if 'm2:MetaConcept' in item_type or item.get('@id', '').startswith('m2:'):
                process_metaconcept(item, stats)

def process_jsonld_file(input_path, output_path=None):
    """Traite un fichier JSON-LD."""
    print(f"\n📄 Traitement: {input_path}")
    
    # Lire le fichier
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture: {e}")
        return False
    
    # Statistiques
    stats = {
        'metaconcepts_modified': 0,
        'formulas_fixed': 0,
        'eagle_formulas_fixed': 0,
        'sphinx_primary_fixed': 0,
        'sphinx_fallback_fixed': 0,
        'dual_territory_fixed': 0,
        'dual_map_fixed': 0,
    }
    
    # Traiter @graph
    if '@graph' in data:
        process_graph(data['@graph'], stats)
    else:
        # Traiter l'objet racine
        process_metaconcept(data, stats)
    
    # Déterminer chemin de sortie
    if output_path is None:
        input_pathobj = Path(input_path)
        output_path = input_pathobj.parent / f"{input_pathobj.stem}_fixed{input_pathobj.suffix}"
    
    # Écrire le fichier
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Fichier écrit: {output_path}")
    except Exception as e:
        print(f"❌ Erreur écriture: {e}")
        return False
    
    # Afficher statistiques
    print("\n📊 Statistiques:")
    print(f"  Métaconcepts modifiés: {stats['metaconcepts_modified']}")
    print(f"  Formules principales: {stats['formulas_fixed']}")
    print(f"  Eagle formulas: {stats['eagle_formulas_fixed']}")
    print(f"  Sphinx primary: {stats['sphinx_primary_fixed']}")
    print(f"  Sphinx fallback: {stats['sphinx_fallback_fixed']}")
    print(f"  Dual territory: {stats['dual_territory_fixed']}")
    print(f"  Dual map: {stats['dual_map_fixed']}")
    total = sum(stats.values()) - stats['metaconcepts_modified']
    print(f"  Total formules corrigées: {total}")
    
    return True

def main():
    """Point d'entrée principal."""
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   TSCG Tensor Formula Fixer                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Corrige automatiquement les formules tensorielles dans les ontologies TSCG.
Ajoute triple représentation: Unicode (⊗), LaTeX (\\otimes), ASCII ((x))

Usage:
  python fix_tensor_formulas.py <input.jsonld> [output.jsonld]

Exemples:
  python fix_tensor_formulas.py M2_MetaConcepts.jsonld
  python fix_tensor_formulas.py M2_MetaConcepts.jsonld M2_MetaConcepts_fixed.jsonld
  python fix_tensor_formulas.py M0_VSM.jsonld

Le script:
  ✓ Détecte les formules corrompues (mojibake)
  ✓ Corrige vers Unicode UTF-8 pur (⊗)
  ✓ Ajoute variante LaTeX (\\otimes)
  ✓ Ajoute variante ASCII ((x))
  ✓ Traite m2:hasTensorFormula, eagleView, sphinxView
  ✓ Préserve la structure JSON-LD

Formules supportées:
  ASFID: A⊗S⊗F, A⊗S, S⊗D, I⊗F, etc.
  ORIVE: O⊗R⊗I⊗V⊗E, O⊗R⊗I, R⊗V⊗E, etc.
""")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(input_file).exists():
        print(f"❌ Erreur: Fichier '{input_file}' introuvable.")
        sys.exit(1)
    
    success = process_jsonld_file(input_file, output_file)
    
    if success:
        print("\n✅ Traitement terminé avec succès!")
    else:
        print("\n❌ Échec du traitement.")
        sys.exit(1)

if __name__ == '__main__':
    main()
