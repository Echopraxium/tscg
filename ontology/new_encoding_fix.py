#!/usr/bin/env python3
"""
Script de correction d'encodage pour fichiers JSON-LD TSCG
Usage: python script.py <fichier_source> [<fichier_cible>]
"""

import json
import re
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

# ==============================================================================
# FONCTIONS DE GESTION DES CORRESPONDANCES
# ==============================================================================

def load_correspondances_from_json(json_file='encoding_correspondances.json'):
    """Charge les correspondances d'encodage depuis un fichier JSON."""
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ Chargé {len(data.get('correspondances', {}))} correspondances depuis {json_file}")
                return data.get('correspondances', {})
        except Exception as e:
            print(f"⚠️  Erreur lors du chargement de {json_file}: {e}")
    
    print(f"⚠️  Fichier {json_file} introuvable, utilisation des correspondances par défaut")
    return get_default_correspondances()

def get_default_correspondances():
    """Retourne les correspondances par défaut."""
    return {
        # ==============================================================================
        # SYMBOLES MATHÉMATIQUES
        # ==============================================================================
        
        # Opérateurs de produit tensoriel
        'âŠ—': '⊗',
        'Ã¢Å â€"': '⊗',
        'Ã¢â€ â€™': '⊗',
        
        # Flèches simples
        'â†\'': '→',
        '←': '←',
        '↔': '↔',
        'â†': '→',
        
        # Flèches doubles
        'â‡': '⇒',
        'â‡”': '⇔',
        'â‡€': '⇐',
        
        # Flèches verticales
        'â‡‘': '↑',
        'â‡"': '↓',
        'â†‘': '↑',
        'â†"': '↓',
        
        # Double flèche horizontale
        'â‡”': '⇔',
        'â†”': '↔',
        
        # Flèche vers le bas
        '↓': '↓',
        
        # Théorie des ensembles
        'âˆˆ': '∈',
        'âˆ‰': '∉',
        'âŠ†': '⊆',
        'âŠ‚': '⊂',
        'âŠ•': '⊕',
        'âˆ©': '∩',
        'âˆª': '∪',
        'âˆ…': '∅',
        
        # Comparaisons et relations
        'â‰': '≈',
        'â‰ƒ': '≃',
        'â‰¤': '≤',
        'â‰¥': '≥',
        'â‰¡': '≡',
        'â‰': '≠',
        '≠ˆ': '≈',  # Corruption de ≈
        'â‰ˆ': '≈',
        '≠âˆ': '≈',
        
        # Quantificateurs logiques
        'âˆ€': '∀',
        'âˆƒ': '∃',
        'Â¬': '¬',
        'âˆ§': '∧',
        'âˆ¨': '∨',
        
        # Opérateurs mathématiques
        'âˆ\'': '∑',
        'âˆ«': '∫',
        'âˆ‚': '∂',
        'âˆ‡': '∇',
        'âˆž': '∞',
        'âˆ': '√',
        'Ã—': '×',
        'Ã·': '÷',
        'Â±': '±',
        'âˆ"': '∓',
        
        # Crochets et délimiteurs
        'âŸ¨': '⟨',
        'âŸ©': '⟩',
        'âŒˆ': '⌈',
        'âŒ‰': '⌉',
        'âŒŠ': '⌊',
        'âŒ‹': '⌋',
        
        # Divers mathématiques
        'âˆ¥': '∥',
        'âŠ¥': '⊥',
        'âˆ¼': '∼',
        'â‰…': '≅',
        'âˆ': '∝',
        
        # ==============================================================================
        # LETTRES GRECQUES (MINUSCULES)
        # ==============================================================================
        'Î±': 'α',
        'Î²': 'β',
        'Î³': 'γ',
        'Î´': 'δ',
        'Îµ': 'ε',
        'Î¶': 'ζ',
        'Î·': 'η',
        'Î¸': 'θ',
        'Î¹': 'ι',
        'Îº': 'κ',
        'Î»': 'λ',
        'Âµ': 'μ',
        'Î¼': 'μ',
        'Î½': 'ν',
        'Î¾': 'ξ',
        'Î¿': 'ο',
        'Ï€': 'π',
        'Ï': 'ρ',
        'Ïƒ': 'σ',
        'Ï„': 'τ',
        'Ï…': 'υ',
        'Ï†': 'φ',
        'Ï‡': 'χ',
        'Ïˆ': 'ψ',
        'Ï‰': 'ω',
        
        # ==============================================================================
        # LETTRES GRECQUES (MAJUSCULES)
        # ==============================================================================
        'Î\'': 'Α',
        'Î"': 'Δ',
        'Î‘': 'Α',
        'Î\'': 'Β',
        'Î"': 'Γ',
        'Î"': 'Δ',
        'Îµ': 'Ε',
        'Î–': 'Ζ',
        'Î—': 'Η',
        'Î˜': 'Θ',
        'Î™': 'Ι',
        'Îš': 'Κ',
        'Î›': 'Λ',
        'Îœ': 'Μ',
        'Î': 'Ν',
        'Îž': 'Ξ',
        'ÎŸ': 'Ο',
        'Î': 'Π',
        'Î¡': 'Ρ',
        'Î£': 'Σ',
        'Î¤': 'Τ',
        'Î¥': 'Υ',
        'Î¦': 'Φ',
        'Î§': 'Χ',
        'Îª': 'Ψ',
        'Î©': 'Ω',
        
        # ==============================================================================
        # EXPOSANTS ET INDICES
        # ==============================================================================
        'Â¹': '¹',
        'Â²': '²',
        'Â³': '³',
        'â�´': '⁴',
        'â�µ': '⁵',
        'â�¶': '⁶',
        'â�·': '⁷',
        'â�¸': '⁸',
        'â�¹': '⁹',
        'â�º': '⁰',
        'á´µ': 'ⁱ',
        'Ã‚Â¡': 'ⁱ',
        'âБ': 'ⁿ',
        'â‚€': '₀',
        'â‚': '₁',
        'â‚‚': '₂',
        'â‚ƒ': '₃',
        'â‚„': '₄',
        'â‚…': '₅',
        'â‚†': '₆',
        'â‚‡': '₇',
        'â‚ˆ': '₈',
        'â‚‰': '₉',
        
        # ==============================================================================
        # ARTEFACTS D'ENCODING À SUPPRIMER
        # ==============================================================================
        'Ã‚Â': '',  # Artefact UTF-8
        'Ãƒ': '',   # Artefact UTF-8
        'Â': '',    # Espace insécable corrompu
        'Â': '',   # Artefact spécifique
        'ÃŽ': '',   # Artefact spécifique
        'Ã': '',    # Artefact générique
        'â€': '',   # Artefact guillemets
        '‘': '',   # Artefact chimique
        '∂': '₂',  # Artefact → indice 2
        
        # ==============================================================================
        # CAS SPÉCIAL : REVOÎ vs REVOI
        # ==============================================================================
        'REVOÃŽ': 'REVOI',
        'REVOÃ': 'REVOI',
        'REVOÎ': 'REVOI',
        
        # ==============================================================================
        # CORRECTIONS SPÉCIFIQUES
        # ==============================================================================
        'Î"': 'δ',
        'âˆ\'': '∑',
        '⊗Â': '⊗',
        '⊗Â': '⊗',
        'âŠ—Â': '⊗',
        'â‡‘Â': '↑',
        'âˆ‚Î¼': '∂μ',
        'Â': '',
        '→Â': '→',
        '←Â': '←',
        '↑Â': '↑',
        '↓Â': '↓',
        '⇒Â': '⇒',
        '⇔Â': '⇔',
        
        # ==============================================================================
        # CORRECTIONS CHIMIQUES ET EXEMPLES
        # ==============================================================================
        'H⇒‘∂': 'H₂',
        'O⇒‘∂': 'O₂', 
        'H⇒‘∂O': 'H₂O',
        '⇒‘∂': '₂',
        
        '⊗construction': '→ construction',
        '⊗LEGO': '→ LEGO',
        '⊗molecule': '→ molecule', 
        '⊗atoms': '→ atoms',
        '⊗Flame': '→ Flame',
        '⊗Color': '→ Color',
        '⊗(R': '→ (R',
        
        'H⇒‘∂ + O ⊗H⇒‘∂O': '2H + O → H₂O',
        'H⇒‘∂O ⊗H⇒‘∂ + O': 'H₂O → 2H + O',
        'Fuel + O⇒‘∂ + Heat ⊗Flame': 'Fuel + O₂ + Heat → Flame',
        'Flame ⊗Fuel, O⇒‘∂, Heat': 'Flame → Fuel + O₂ + Heat',
        
        # Notation chimique propre
        'H₂O': 'H₂O',
        'O₂': 'O₂', 
        'H₂': 'H₂',
        '∂': '₂',  # Dans le contexte chimique
        
        # ==============================================================================
        # CORRECTIONS POUR FORMULES MATHÉMATIQUES
        # ==============================================================================
        'structure(level_n) ≠ˆ structure(level_0)': 'structure(level_n) ≈ structure(level_0)',
        '∀n, structure(level_n) ≠ˆ structure(level_0)': '∀n, structure(level_n) ≈ structure(level_0)',
    }

def save_correspondances_to_json(correspondances, json_file='encoding_correspondances.json', metadata=None):
    """Sauvegarde les correspondances dans un fichier JSON."""
    if metadata is None:
        metadata = {}
    
    data = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "1.2.0",
            "description": "Correspondances de correction d'encodage pour fichiers JSON-LD TSCG",
            "author": "Script de correction d'encodage",
            **metadata
        },
        "statistics": {
            "total_correspondances": len(correspondances),
            "categories": categorize_correspondances(correspondances)
        },
        "correspondances": correspondances
    }
    
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Correspondances sauvegardées dans {json_file}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def categorize_correspondances(correspondances):
    """Catégorise les correspondances pour les statistiques."""
    categories = {
        "flèches": [],
        "symboles_mathématiques": [],
        "lettres_grecques": [],
        "artefacts": [],
        "exposants_indices": [],
        "revoi": [],
        "corrections_chimiques": [],
        "formules_spécifiques": []
    }
    
    for wrong, right in correspondances.items():
        # Catégoriser
        if any(arrow_char in right for arrow_char in ['→', '←', '↑', '↓', '⇒', '⇔', '↔']):
            categories["flèches"].append(wrong)
        elif any(math_char in right for math_char in ['⊗', '∈', '∀', '∃', '∑', '∫', '∂', '∇', '∞', '√', '×', '÷', '±']):
            categories["symboles_mathématiques"].append(wrong)
        elif any(greek_char in right for greek_char in ['α', 'β', 'γ', 'δ', 'ε', 'μ', 'π', 'σ', 'τ', 'φ', 'ψ', 'ω']):
            categories["lettres_grecques"].append(wrong)
        elif right == '':
            categories["artefacts"].append(wrong)
        elif any(sup_char in right for sup_char in ['¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', '⁰', 'ⁱ', 'ⁿ']):
            categories["exposants_indices"].append(wrong)
        elif 'REVO' in wrong.upper():
            categories["revoi"].append(wrong)
        elif any(chem in wrong for chem in ['H₂', 'O₂', 'H₂O', 'Fuel', 'Flame']):
            categories["corrections_chimiques"].append(wrong)
        elif 'structure(' in wrong or 'level_' in wrong:
            categories["formules_spécifiques"].append(wrong)
        else:
            categories["formules_spécifiques"].append(wrong)
    
    # Convertir en comptages
    return {category: len(items) for category, items in categories.items()}

# ==============================================================================
# FONCTIONS DE CORRECTION
# ==============================================================================

def fix_encoding_file(source_file, target_file=None, correspondances_file='encoding_correspondances.json'):
    """Corrige les problèmes d'encodage dans un fichier."""
    if not os.path.exists(source_file):
        return False, 0, f"Fichier source introuvable: {source_file}"
    
    # Charger les correspondances
    correspondances = load_correspondances_from_json(correspondances_file)
    
    # Si pas de fichier cible, on remplace le source
    if target_file is None:
        target_file = source_file
        backup_file = source_file + '.bak'
        
        try:
            shutil.copy2(source_file, backup_file)
            print(f"✅ Backup créé: {backup_file}")
        except Exception as e:
            print(f"⚠️  Impossible de créer le backup: {e}")
    
    try:
        # Lire le fichier source
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        total_corrections = 0
        corrections_applied = {}
        
        # Étape 1: Corrections de base
        for wrong, right in correspondances.items():
            if wrong in content:
                count = content.count(wrong)
                content = content.replace(wrong, right)
                total_corrections += count
                corrections_applied[wrong] = (count, right)
        
        # Étape 2: Corrections regex
        content, regex_count = apply_regex_corrections(content)
        total_corrections += regex_count
        
        # Étape 3: Corrections spécifiques
        content, specific_count = fix_specific_examples(content)
        total_corrections += specific_count
        
        # Étape 4: Corrections chimiques
        content, chem_count = fix_chemical_notation(content)
        total_corrections += chem_count
        
        # Étape 5: Corrections mathématiques
        content, math_count = fix_mathematical_formulas(content)
        total_corrections += math_count
        
        # Écrire le fichier cible
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Afficher le résumé
        if total_corrections > 0:
            print_summary(corrections_applied, total_corrections)
        
        # Valider JSON
        validate_json(target_file)
        
        return True, total_corrections, ""
    
    except Exception as e:
        return False, 0, f"Erreur: {str(e)}"

def apply_regex_corrections(content):
    """Applique les corrections regex."""
    regex_corrections = [
        (r'\\otimes\s*Â', '⊗'),
        (r'\\otimes\s*Â', '⊗'),
        (r'\\to\s*Â', '→'),
        (r'\\mapsto\s*Â', '↦'),
        (r'\\rightarrow\s*Â', '→'),
        (r'\\leftarrow\s*Â', '←'),
        (r'\\uparrow\s*Â', '↑'),
        (r'\\downarrow\s*Â', '↓'),
        (r'\\Rightarrow\s*Â', '⇒'),
        (r'\\Leftrightarrow\s*Â', '⇔'),
        
        # Lettres grecques
        (r'Î¼', 'μ'),
        (r'Ï„', 'τ'),
        (r'Ï€', 'π'),
        (r'Ïƒ', 'σ'),
        (r'Ï†', 'φ'),
        (r'Ïˆ', 'ψ'),
        (r'Ï‰', 'ω'),
        (r'Î±', 'α'),
        (r'Î²', 'β'),
        (r'Î³', 'γ'),
        (r'Î´', 'δ'),
        (r'Î¸', 'θ'),
        (r'Î»', 'λ'),
        (r'Î¾', 'ξ'),
        
        # Formules de similarité
        (r'structure\(level_n\)\s*[≠â‰ˆ]\s*structure\(level_0\)', 
         'structure(level_n) ≈ structure(level_0)'),
        
        (r'∀n,\s*structure\(level_n\)\s*[≠â‰ˆ]\s*structure\(level_0\)', 
         '∀n, structure(level_n) ≈ structure(level_0)'),
    ]
    
    corrections_count = 0
    for pattern, replacement in regex_corrections:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            corrections_count += count
    
    return content, corrections_count

def fix_specific_examples(content):
    """Corrige les exemples spécifiques de composition/décomposition."""
    example_corrections = [
        (r'Composition: Atoms ⊗molecule \(H⇒‘∂ \+ O ⊗H⇒‘∂O\)', 
         'Composition: Atoms → molecule (2H + O → H₂O)'),
        
        (r'Decomposition: Molecule ⊗atoms \(H⇒‘∂O ⊗H⇒‘∂ \+ O\)', 
         'Decomposition: Molecule → atoms (H₂O → 2H + O)'),
        
        (r'Composition: Fuel \+ O⇒‘∂ \+ Heat ⊗Flame', 
         'Composition: Fuel + O₂ + Heat → Flame'),
        
        (r'Decomposition: Flame ⊗Fuel, O⇒‘∂, Heat \(forensics\)', 
         'Decomposition: Flame → Fuel + O₂ + Heat (forensics)'),
        
        (r'Composition: LEGO bricks ⊗construction', 
         'Composition: LEGO bricks → construction'),
        
        (r'Decomposition: Construction ⊗LEGO bricks', 
         'Decomposition: Construction → LEGO bricks'),
        
        (r'Composition: R \+ G \+ B ⊗Color', 
         'Composition: R + G + B → Color'),
        
        (r'Decomposition: Color ⊗\(R, G, B\) triplet', 
         'Decomposition: Color → (R, G, B) triplet'),
    ]
    
    corrections_count = 0
    for pattern, replacement in example_corrections:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            corrections_count += count
    
    return content, corrections_count

def fix_chemical_notation(content):
    """Corrige la notation chimique spécifique."""
    chemical_corrections = [
        (r'H([⇒‘∂]+)', r'H₂'),
        (r'O([⇒‘∂]+)', r'O₂'),
        (r'H([⇒‘∂]+)O', r'H₂O'),
        (r'([A-Za-z])([⇒‘∂]+)', r'\1₂'),
        (r'([A-Za-z0-9]+)[⇒‘∂]*\s*[⊗âŠ—]\s*([A-Za-z0-9]+)', r'\1 → \2'),
        (r'([A-Za-z0-9]+)\s*[⊗âŠ—]\s*([A-Za-z0-9,]+)', r'\1 → \2'),
    ]
    
    corrections_count = 0
    for pattern, replacement in chemical_corrections:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            corrections_count += count
    
    return content, corrections_count

def fix_mathematical_formulas(content):
    """Corrige les formules mathématiques spécifiques."""
    math_corrections = [
        (r'selfSimilarity":\s*"∀n,\s*structure\(level_n\)\s*≠ˆ\s*structure\(level_0\)"', 
         'selfSimilarity": "∀n, structure(level_n) ≈ structure(level_0)"'),
        
        (r'"∀n,\s*structure\(level_n\)\s*≠ˆ\s*structure\(level_0\)"', 
         '"∀n, structure(level_n) ≈ structure(level_0)"'),
        
        (r'â‰ˆ', '≈'),
        (r'≠ˆ', '≈'),
        (r'≠âˆ', '≈'),
    ]
    
    corrections_count = 0
    for pattern, replacement in math_corrections:
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            corrections_count += count
    
    return content, corrections_count

def print_summary(corrections_applied, total_corrections):
    """Affiche le résumé des corrections."""
    print("\n📊 RÉSUMÉ DES CORRECTIONS :")
    print("-" * 60)
    
    categories = {
        'Flèches': [],
        'Symboles mathématiques': [],
        'Lettres grecques': [],
        'Artefacts': [],
        'REVOI': [],
        'Chimie': [],
        'Formules': [],
        'Autres': []
    }
    
    for wrong, (count, right) in corrections_applied.items():
        if any(arrow_char in str(right) for arrow_char in ['→', '←', '↑', '↓', '⇒', '⇔', '↔']):
            categories['Flèches'].append((wrong, count, right))
        elif any(math_char in str(right) for math_char in ['⊗', '∈', '∀', '∃', '∑', '∫', '∂', '∇', '∞', '√']):
            categories['Symboles mathématiques'].append((wrong, count, right))
        elif any(greek_char in str(right) for greek_char in ['α', 'β', 'γ', 'δ', 'ε', 'μ', 'π', 'σ', 'τ', 'φ', 'ψ', 'ω']):
            categories['Lettres grecques'].append((wrong, count, right))
        elif 'REVO' in str(wrong).upper():
            categories['REVOI'].append((wrong, count, right))
        elif right == '':
            categories['Artefacts'].append((wrong, count, right))
        elif any(chem in str(wrong) for chem in ['H₂', 'O₂', 'H₂O', 'Fuel', 'Flame']):
            categories['Chimie'].append((wrong, count, right))
        elif 'structure(' in str(wrong) or 'level_' in str(wrong):
            categories['Formules'].append((wrong, count, right))
        else:
            categories['Autres'].append((wrong, count, right))
    
    for category, items in categories.items():
        if items:
            print(f"\n{category}:")
            for wrong, count, right in sorted(items, key=lambda x: x[1], reverse=True):
                right_display = right if right else '(supprimé)'
                print(f"  {repr(wrong):30} → {repr(right_display):20} : {count:4d}")
    
    print("-" * 60)
    print(f"  TOTAL : {total_corrections} corrections appliquées")

def validate_json(file_path):
    """Valide un fichier JSON."""
    if file_path.endswith(('.json', '.jsonld')):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"\n✅ Validation JSON: SUCCÈS")
        except json.JSONDecodeError as e:
            print(f"\n⚠️  Validation JSON: ÉCHEC - {e}")
            print("   Le fichier a été corrigé mais contient des erreurs JSON.")

# ==============================================================================
# FONCTIONS DE SCAN ET MISE À JOUR
# ==============================================================================

def scan_for_corruptions(file_path, correspondances_file='encoding_correspondances.json'):
    """Scanne un fichier pour détecter les corruptions courantes."""
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    correspondances = load_correspondances_from_json(correspondances_file)
    corruption_patterns = list(correspondances.keys())
    
    # Patterns supplémentaires
    additional_patterns = [
        'Ã¢', 'â€', 'â€"', 'â€™', 'â€˜', 'â€¦',
        'Â ', 'Â°', 'Â«', 'Â»', 'Â¿', 'Â¡'
    ]
    
    corruption_patterns.extend(additional_patterns)
    
    found = {}
    for pattern in corruption_patterns:
        if pattern:
            count = content.count(pattern)
            if count > 0:
                found[pattern] = count
    
    return found

def update_correspondances_json(correspondances_file, new_correspondances, source_file=None):
    """Met à jour le fichier JSON des correspondances."""
    if os.path.exists(correspondances_file):
        try:
            with open(correspondances_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                existing_correspondances = data.get('correspondances', {})
        except:
            existing_correspondances = {}
            data = {
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.2.0",
                    "description": "Correspondances de correction d'encodage"
                },
                "statistics": {},
                "correspondances": {}
            }
    else:
        existing_correspondances = {}
        data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.2.0",
                "description": "Correspondances de correction d'encodage"
            },
            "statistics": {},
            "correspondances": {}
        }
    
    updated = False
    for wrong, right in new_correspondances.items():
        if wrong not in existing_correspondances:
            existing_correspondances[wrong] = right
            updated = True
            print(f"  + Ajouté: {repr(wrong)} → {repr(right)}")
    
    if updated:
        metadata = data.get('metadata', {})
        metadata['last_updated'] = datetime.now().isoformat()
        if source_file:
            metadata['last_source_file'] = source_file
        
        save_correspondances_to_json(
            existing_correspondances,
            correspondances_file,
            metadata
        )
        print(f"✅ Fichier {correspondances_file} mis à jour")
    else:
        print("✅ Toutes les corruptions sont déjà dans les correspondances")

def export_correspondances_to_text(json_file, text_file):
    """Exporte les correspondances du format JSON vers le format texte."""
    if not os.path.exists(json_file):
        print(f"❌ Fichier {json_file} introuvable")
        return False
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        correspondances = data.get('correspondances', {})
        
        lines = [
            "# Correspondances de correction d'encodage",
            "# Exporté depuis: " + json_file,
            "# Date: " + datetime.now().isoformat(),
            "#",
            ""
        ]
        
        # Organiser par catégorie
        categories = categorize_correspondances(correspondances)
        
        # Ajouter les sections
        sections = [
            ("FLÈCHES", [(k, v) for k, v in correspondances.items() 
                        if any(c in v for c in ['→', '←', '↑', '↓', '⇒', '⇔', '↔'])]),
            ("SYMBOLES MATHÉMATIQUES", [(k, v) for k, v in correspondances.items() 
                                       if any(c in v for c in ['⊗', '∈', '∀', '∃', '∑', '∫', '∂', '∇', '∞', '√'])]),
            ("LETTRES GRECQUES", [(k, v) for k, v in correspondances.items() 
                                 if any(c in v for c in ['α', 'β', 'γ', 'δ', 'ε', 'μ', 'π', 'σ', 'τ', 'φ', 'ψ', 'ω'])]),
            ("EXPOSANTS ET INDICES", [(k, v) for k, v in correspondances.items() 
                                     if any(c in v for c in ['¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', '⁰', 'ⁱ', 'ⁿ'])]),
            ("ARTEFACTS D'ENCODING", [(k, v) for k, v in correspondances.items() if v == '']),
            ("CORRECTIONS CHIMIQUES", [(k, v) for k, v in correspondances.items() 
                                      if any(chem in k for chem in ['H₂', 'O₂', 'H₂O', 'Fuel', 'Flame'])]),
            ("FORMULES SPÉCIFIQUES", [(k, v) for k, v in correspondances.items() 
                                     if 'structure(' in k or 'level_' in k]),
            ("AUTRES CORRECTIONS", [(k, v) for k, v in correspondances.items() 
                                   if not any(c in v for c in ['→', '←', '↑', '↓', '⇒', '⇔', '↔', '⊗', '∈', '∀', '∃', '∑', '∫', '∂', '∇', '∞', '√', '×', '÷', '±', 'α', 'β', 'γ', 'δ', 'ε', 'μ', 'π', 'σ', 'τ', 'φ', 'ψ', 'ω', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', '⁰', 'ⁱ', 'ⁿ']) and v != '']),
        ]
        
        for title, items in sections:
            if items:
                lines.append("# " + "=" * 75)
                lines.append(f"# {title}")
                lines.append("# " + "=" * 75)
                lines.append("")
                for wrong, right in sorted(items):
                    wrong_formatted = wrong.ljust(25)
                    right_formatted = right if right else '(vide)'
                    unicode_code = f"U+{ord(right):04X}" if right and len(right) == 1 else ""
                    comment = f"  # {unicode_code}" if unicode_code else f"  # {wrong} → {right_formatted}"
                    lines.append(f"{wrong_formatted} → {right_formatted:15}{comment}")
                lines.append("")
        
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Correspondances exportées vers {text_file}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        return False

# ==============================================================================
# FONCTION PRINCIPALE
# ==============================================================================

def main():
    """Fonction principale."""
    
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_help()
        sys.exit(0)
    
    if sys.argv[1] == '--init-json':
        handle_init_json()
    elif sys.argv[1] == '--export':
        handle_export()
    elif sys.argv[1] == '--scan':
        handle_scan()
    elif sys.argv[1] == '--update':
        handle_update()
    else:
        handle_correction()

def print_help():
    """Affiche l'aide."""
    print("""
Script de correction d'encodage pour fichiers JSON-LD TSCG

Usage:
  python script.py <fichier_source> [<fichier_cible>]
  python script.py --scan <fichier>
  python script.py --update <fichier_source>
  python script.py --export <fichier_json> <fichier_texte>
  python script.py --init-json [<fichier_json>]

Options:
  --scan          : Scanner un fichier pour détecter les corruptions
  --update        : Mettre à jour le fichier JSON des correspondances
  --export        : Exporter les correspondances JSON vers format texte
  --init-json     : Initialiser le fichier JSON des correspondances
  -h, --help      : Afficher cette aide

Exemples:
  python script.py M2_MetaConcepts.jsonld
  python script.py M2_MetaConcepts.jsonld M2_MetaConcepts_corrigé.jsonld
  python script.py --scan M2_MetaConcepts.jsonld
  python script.py --update M2_MetaConcepts.jsonld
  python script.py --export encoding_correspondances.json correspondances.txt
  python script.py --init-json

Fonctionnalités:
  • Correction des flèches (→, ←, ↑, ↓, ⇒, ⇔)
  • Correction des symboles mathématiques (⊗, ∈, ∀, ∑, ∂, ≈)
  • Correction des lettres grecques (α, β, γ, δ, μ, π)
  • Correction des formules chimiques (H₂O, O₂)
  • Correction des formules mathématiques (structure ≈ structure)
  • Suppression des artefacts UTF-8
  • Correction de REVOÎ → REVOI
  • Backup automatique
  • Validation JSON
  • Rapport détaillé des corrections
""")

def handle_init_json():
    """Gère l'initialisation du JSON."""
    json_file = sys.argv[2] if len(sys.argv) > 2 else 'encoding_correspondances.json'
    correspondances = get_default_correspondances()
    if save_correspondances_to_json(correspondances, json_file):
        print(f"✅ Fichier JSON initialisé: {json_file}")
        print(f"   Contient {len(correspondances)} correspondances")
    sys.exit(0)

def handle_export():
    """Gère l'export."""
    if len(sys.argv) < 4:
        print("Erreur: Spécifiez le fichier JSON source et le fichier texte cible")
        sys.exit(1)
    json_file = sys.argv[2]
    text_file = sys.argv[3]
    export_correspondances_to_text(json_file, text_file)
    sys.exit(0)

def handle_scan():
    """Gère le scan."""
    if len(sys.argv) < 3:
        print("Erreur: Spécifiez un fichier à scanner")
        sys.exit(1)
    
    file_to_scan = sys.argv[2]
    print(f"🔍 Scan des corruptions dans: {file_to_scan}")
    print("-" * 60)
    
    corruptions = scan_for_corruptions(file_to_scan)
    
    if corruptions:
        print_corruption_summary(corruptions)
    else:
        print("✅ Aucune corruption détectée")
    
    sys.exit(0)

def print_corruption_summary(corruptions):
    """Affiche le résumé des corruptions."""
    print("Corruptions détectées:")
    
    categories = {
        'Flèches': [],
        'Symboles mathématiques': [],
        'Lettres grecques': [],
        'Artefacts': [],
        'REVOI': [],
        'Chimie': [],
        'Formules': [],
        'Autres': []
    }
    
    for pattern, count in corruptions.items():
        if any(arrow in pattern for arrow in ['â†', 'â‡', '→', '←', '↑', '↓']):
            categories['Flèches'].append((pattern, count))
        elif any(math in pattern for math in ['âˆ', 'âŠ', 'â‰', 'Ã']):
            categories['Symboles mathématiques'].append((pattern, count))
        elif any(greek in pattern for greek in ['Î', 'Ï']):
            categories['Lettres grecques'].append((pattern, count))
        elif 'REVO' in pattern.upper():
            categories['REVOI'].append((pattern, count))
        elif any(chem in pattern for chem in ['H⇒', 'O⇒', 'Fuel', 'Flame']):
            categories['Chimie'].append((pattern, count))
        elif 'structure(' in pattern or 'level_' in pattern:
            categories['Formules'].append((pattern, count))
        elif 'Â' in pattern or 'Ã' in pattern:
            categories['Artefacts'].append((pattern, count))
        else:
            categories['Autres'].append((pattern, count))
    
    total_count = 0
    for category, items in categories.items():
        if items:
            print(f"\n{category}:")
            for pattern, count in sorted(items, key=lambda x: x[1], reverse=True):
                print(f"  {repr(pattern):30} : {count:4d}")
                total_count += count
    
    print("-" * 60)
    print(f"Total: {len(corruptions)} types de corruptions, {total_count} occurences")

def handle_update():
    """Gère la mise à jour des correspondances."""
    if len(sys.argv) < 3:
        print("Erreur: Spécifiez le fichier source")
        sys.exit(1)
    
    source_file = sys.argv[2]
    correspondances_file = 'encoding_correspondances.json'
    
    print(f"🔍 Recherche de nouvelles corruptions dans: {source_file}")
    corruptions = scan_for_corruptions(source_file, correspondances_file)
    
    if corruptions:
        existing_correspondances = load_correspondances_from_json(correspondances_file)
        new_corruptions = {}
        
        for corruption, count in corruptions.items():
            if corruption not in existing_correspondances:
                new_corruptions[corruption] = count
        
        if new_corruptions:
            print(f"\nNouvelles corruptions trouvées ({len(new_corruptions)}):")
            for corruption, count in sorted(new_corruptions.items()):
                print(f"  {repr(corruption):30} : {count:4d} occurences")
            
            print("\nPour chaque nouvelle corruption, entrez la correction:")
            print("  - Entrez le caractère correct")
            print("  - Entrez 'vide' ou laissez vide pour supprimer")
            print("  - Entrez 'skip' pour ignorer")
            print()
            
            new_correspondances = {}
            for corruption in new_corruptions:
                print(f"Corruption: {repr(corruption)}")
                print(f"Occurences: {new_corruptions[corruption]}")
                
                try:
                    with open(source_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        pos = content.find(corruption)
                        if pos != -1:
                            start = max(0, pos - 30)
                            end = min(len(content), pos + len(corruption) + 30)
                            context = content[start:end].replace('\n', ' ')
                            print(f"Contexte: ...{context}...")
                except:
                    pass
                
                correction = input("Correction: ").strip()
                
                if correction.lower() == 'skip':
                    print("  Ignoré\n")
                    continue
                elif correction.lower() == 'vide' or correction == '':
                    new_correspondances[corruption] = ''
                    print(f"  → Supprimé\n")
                else:
                    new_correspondances[corruption] = correction
                    print(f"  → {repr(correction)}\n")
            
            if new_correspondances:
                update_correspondances_json(correspondances_file, new_correspondances, source_file)
            else:
                print("✅ Aucune nouvelle correspondance ajoutée")
        else:
            print("✅ Toutes les corruptions sont déjà dans les correspondances")
    else:
        print("✅ Aucune nouvelle corruption trouvée")
    
    sys.exit(0)

def handle_correction():
    """Gère la correction normale."""
    source_file = sys.argv[1]
    target_file = sys.argv[2] if len(sys.argv) > 2 else None
    correspondances_file = 'encoding_correspondances.json'
    
    print(f"🔄 Correction d'encodage")
    print(f"   Source: {source_file}")
    print(f"   Cible:  {target_file if target_file else source_file + ' (remplacement)'}")
    print(f"   Correspondances: {correspondances_file}")
    print("-" * 60)
    
    print("🔍 Scan initial...")
    corruptions_before = scan_for_corruptions(source_file, correspondances_file)
    
    if corruptions_before:
        print_corruption_summary(corruptions_before)
    else:
        print("✅ Aucune corruption détectée avant correction")
    
    print("-" * 60)
    
    if target_file is None or target_file == source_file:
        response = input("⚠️  Le fichier source sera remplacé. Continuer? (o/N): ")
        if response.lower() != 'o':
            print("Opération annulée")
            sys.exit(0)
    
    success, corrections_count, error = fix_encoding_file(
        source_file, 
        target_file, 
        correspondances_file
    )
    
    if success:
        print(f"\n✅ Correction terminée avec succès!")
        print(f"   {corrections_count} corrections appliquées")
        
        final_file = target_file if target_file else source_file
        corruptions_after = scan_for_corruptions(final_file, correspondances_file)
        
        if corruptions_after:
            print(f"\n⚠️  Corruptions résiduelles détectées:")
            residual_count = sum(corruptions_after.values())
            for pattern, count in sorted(corruptions_after.items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    print(f"  {repr(pattern):30} : {count:4d}")
            print(f"Total résiduel: {residual_count} occurences")
            
            if residual_count > 0:
                print(f"\n💡 Conseil: Utilisez 'python script.py --update {source_file}'")
                print("   pour ajouter ces corruptions aux correspondances.")
        else:
            print(f"\n✅ Aucune corruption résiduelle détectée")
        
        if os.path.exists(source_file) and os.path.exists(final_file):
            size_before = os.path.getsize(source_file)
            size_after = os.path.getsize(final_file)
            print(f"\n📊 Taille: {size_before:,} → {size_after:,} octets")
    
    else:
        print(f"\n❌ Échec de la correction: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()