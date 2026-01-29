#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import re
from pathlib import Path

# Table de remplacement COMPLÈTE pour les caractères grecs et mathématiques
REPLACEMENTS = {
    # Caractères grecs minuscules
    'ÃƒÂ¡': 'α', 'Î±': 'α', 'ÃŽÂ±': 'α',
    'ÃƒÂŸ': 'β', 'ÃƒÅ¸': 'β', 'Î²': 'β',
    'ÃƒÂ§': 'γ', 'Î³': 'γ',
    'ÃƒÂ´': 'δ', 'Î´': 'δ',
    'ÃƒÂ©': 'ε', 'Îµ': 'ε',
    'ÃƒÂ¶': 'ζ', 'Î¶': 'ζ',
    'ÃƒÂ·': 'η', 'Î·': 'η',
    'ÃƒÂ¸': 'θ', 'Î¸': 'θ',
    'ÃƒÂ¹': 'ι', 'Î¹': 'ι',
    'ÃƒÂº': 'κ', 'Îº': 'κ',
    'ÃƒÂ»': 'λ', 'Î»': 'λ',
    'ÃƒÂ¼': 'μ', 'Î¼': 'μ',
    'ÃƒÂ½': 'ν', 'Î½': 'ν',
    'ÃƒÂ¿': 'ξ', 'Î¾': 'ξ',
    'Ã„â‚¬': 'ο', 'Î¿': 'ο',
    'Ã„â€š': 'π', 'Ï€': 'π',
    'Ã„â€ž': 'ρ', 'Ï': 'ρ',
    'Ã„â€ ': 'σ', 'Ïƒ': 'σ',
    'Ã„â€¡': 'τ', 'Ï„': 'τ',
    'Ã„â€°': 'υ', 'Ï…': 'υ',
    'Ã„â€¹': 'φ', 'Ï†': 'φ',
    'Ã„â€º': 'χ', 'Ï‡': 'χ',
    'Ã„â€œ': 'ψ', 'Ïˆ': 'ψ',
    'Ã„â€': 'ω', 'Ï‰': 'ω',
    
    # Symboles mathématiques spécifiques
    'ÃƒÂ¢Ã…Â Ã¢â‚¬Â¢': '⊗',  # Produit tensoriel
    'Ã¢Å“Â¨': '⊗',
    'ÃƒÂ¢Ã…Â Ã¢â‚¬â€': '—',
    
    # Votre cas spécifique
    'ÃƒÂ¢Ã…Â Ã¢â‚¬Â¢': '⊗',
    'ÃƒÂ¢Ã…Â Ã¢â‚¬â€': '—',
    
    # Symboles généraux
    'Ã¢â‚¬Â¢': '•',
    'Ã¢â‚¬â€œ': '–',
    'Ã¢â‚¬â€': '—',
    'Ã¢Ë†Âˆ': '∈',
    'Ã¢Ë†Â‚': '∂',
    'Ã¢Ë†Â‡': '∇',
    'Ã¢Ë†Â‘': '∑',
    'Ã¢Ë†Â«': '∫',
    'Ã¢Ë†Â®': '∮',
    'Ã¢â€°Â¤': '≤',
    'Ã¢â€°Â¥': '≥',
    'Ã¢â€°Â': '≠',
    'Ã¢â€°Â¡': '≡',
    'Ã¢â€°Ë†': '≈',
    
    # Symboles ensemblistes et logiques
    'Ã¢Ë†Â€': '∀',
    'Ã¢Ë†Æ’': '∃',
    'Ã¢Ë†â€¦': '∅',
    'Ã¢Ë†Âˆ': '∈',
    'Ã¢Ë†Â': '∉',
    'Ã¢Å“â€š': '⊂',
    'Ã¢Å“Å’': '⊆',
    'Ã¢Ë†Â©': '∩',
    'Ã¢Ë†Âª': '∪',
    
    # Flèches
    'Ã¢â€ â€™': '⇒',
    'Ã¢â€ â€œ': '⇔',
    'Ã¢â€ Â': '→',
    'Ã¢â€ â€': '↔',
    
    # Opérateurs
    'Ã¢Ë†â€™': '−',
    'Ã¢Ë†Å½': '∫',
    'Ã¢Ë†Å“': '∮',
    'Ã¢Ë†ï¿½': '∞',
    'Ã¢Ë†Â±': '±',
    
    # Autres
    'Ã‚Â°': '°',
    'Ã‚Â±': '±',
    'Ã‚Â²': '²',
    'Ã‚Â³': '³',
    'Ã‚Â¼': '¼',
    'Ã‚Â½': '½',
    'Ã‚Â¾': '¾',
    
    # Patterns à nettoyer
    'ÃƒÂ¢': '',
    'Ã…Â': '',
    'Ã¢â‚¬': '',
}

# Expressions régulières pour préserver la mise en forme
INDENT_PATTERN = re.compile(r'^(\s*)')  # Pour capturer l'indentation au début de la ligne

def preserve_indentation_and_tabs(fix_func):
    """Décorateur pour préserver l'indentation et les tabulations."""
    def wrapper(text):
        # Capturer l'indentation initiale (espaces et tabulations)
        indent_match = INDENT_PATTERN.match(text)
        original_indent = indent_match.group(1) if indent_match else ''
        
        # Appliquer la correction seulement sur le contenu (sans l'indentation)
        content = text[len(original_indent):] if original_indent else text
        
        # Corriger le contenu
        fixed_content = fix_func(content)
        
        # Restaurer l'indentation originale
        result = original_indent + fixed_content
        
        return result
    return wrapper

@preserve_indentation_and_tabs
def fix_string_aggressive(text):
    """Correction agressive avec remplacements multiples."""
    original = text
    
    # Étape 1: Décodage en chaîne
    text = decode_mojibake_chain(text)
    
    # Étape 2: Remplacements directs
    for pattern, replacement in REPLACEMENTS.items():
        if pattern in text:
            text = text.replace(pattern, replacement)
    
    # Étape 3: Nettoyage des résidus (sans affecter les tabulations)
    # Nettoyer seulement les séquences problématiques spécifiques
    cleanup_patterns = [
        (r'Ã[^a-zA-Z0-9\t\n\r]?', ''),  # Résidus de 'Ã' mais pas les tabulations
        (r'â[^a-zA-Z0-9\t\n\r]?', ''),  # Résidus de 'â'
        (r'Â[^a-zA-Z0-9\t\n\r]?', ''),  # Résidus de 'Â'
        (r'€[^a-zA-Z0-9\t\n\r]?', ''),  # Résidus de '€'
    ]
    
    for pattern, replacement in cleanup_patterns:
        text = re.sub(pattern, replacement, text)
    
    # Étape 4: Corriger les espaces insécables mais garder les tabulations
    text = text.replace('\xc2\xa0', ' ')  # Espace insécable UTF-8
    text = text.replace('\xa0', ' ')      # Espace insécable
    
    # Étape 5: Vérification spécifique pour les patterns complexes
    complex_patterns = {
        r'ÃƒÂ¢Ã…Â\s*Ã¢â‚¬Â¢': '⊗',
        r'ÃƒÂ¢Ã…Â\s*Ã¢â‚¬â€': '—',
    }
    
    for pattern, replacement in complex_patterns.items():
        text = re.sub(pattern, replacement, text)
    
    return text

def decode_mojibake_chain(text):
    """Tente de décoder les chaînes de mojibake successives."""
    chains = [
        # UTF-8 → latin-1 → UTF-8
        lambda t: t.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore'),
        # UTF-8 → cp1252 → UTF-8
        lambda t: t.encode('cp1252', errors='ignore').decode('utf-8', errors='ignore'),
    ]
    
    for decode_func in chains:
        try:
            result = decode_func(text)
            if has_improved(text, result):
                text = result
                break
        except:
            continue
    
    return text

def has_improved(original, new):
    """Vérifie si le nouveau texte est mieux décodé."""
    # Compter les caractères mojibake
    mojibake_chars = ['Ã', 'Â', 'â', '€', '¢', '£']
    orig_count = sum(1 for c in original if any(m in c for m in mojibake_chars))
    new_count = sum(1 for c in new if any(m in c for m in mojibake_chars))
    
    return new_count < orig_count

def process_file_preserving_format(input_file, output_file=None):
    """Traite un fichier en préservant la mise en forme."""
    input_path = Path(input_file)
    
    # Détecter l'encodage et lire le fichier
    content, encoding = read_file_with_encoding(input_path)
    if content is None:
        return False
    
    print(f"Fichier lu avec l'encodage: {encoding}")
    
    # Traiter ligne par ligne en préservant la mise en forme
    lines = content.splitlines(keepends=True)  # Garder les sauts de ligne
    fixed_lines = []
    changes_count = 0
    
    for i, line in enumerate(lines, 1):
        # Préserver le saut de ligne à la fin
        line_ending = ''
        if line.endswith('\n'):
            line_ending = '\n'
            line_content = line.rstrip('\n')
        else:
            line_content = line
        
        # Corriger le contenu de la ligne
        fixed_content = fix_string_aggressive(line_content)
        
        # Reconstruire la ligne avec son saut de ligne
        fixed_line = fixed_content + line_ending
        
        if line_content != fixed_content:
            changes_count += 1
            # Afficher les différences (limité aux premières lignes)
            if changes_count <= 10:  # Afficher seulement les 10 premières corrections
                print(f"\nLigne {i} corrigée:")
                # Montrer l'indentation
                indent_match = INDENT_PATTERN.match(line_content)
                indent = indent_match.group(1) if indent_match else ''
                # Remplacer tabulation par une représentation visible
                indent_display = indent.replace('\t', '\\t').replace(' ', '·')
                
                print(f"  Indentation: '{indent_display}'")
                # Utiliser des variables pour éviter le backslash dans f-string
                tabs_before = line_content.count('\t')
                tabs_after = fixed_content.count('\t')
                print(f"  Tabulations avant: {tabs_before}, après: {tabs_after}")
                
                # Limiter la longueur de l'affichage
                before_preview = line_content[:60] + ('...' if len(line_content) > 60 else '')
                after_preview = fixed_content[:60] + ('...' if len(fixed_content) > 60 else '')
                print(f"  Avant: {before_preview}")
                print(f"  Après: {after_preview}")
        
        fixed_lines.append(fixed_line)
    
    # Écrire le fichier de sortie
    if output_file:
        output_path = Path(output_file)
    else:
        output_path = input_path.with_stem(input_path.stem + '_fixed')
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        f.writelines(fixed_lines)
    
    print(f"\n✓ Fichier corrigé écrit dans: {output_path}")
    print(f"✓ Nombre total de lignes modifiées: {changes_count}")
    
    # Afficher les statistiques
    print_statistics(content, ''.join(fixed_lines))
    
    return True

def read_file_with_encoding(file_path):
    """Lire un fichier en essayant différents encodages."""
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-8-sig']
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except UnicodeDecodeError:
            continue
    
    # Dernier recours: lire en binaire et décoder avec erreurs ignorées
    try:
        with open(file_path, 'rb') as f:
            content_bytes = f.read()
        content = content_bytes.decode('utf-8', errors='ignore')
        return content, 'utf-8 (avec erreurs ignorées)'
    except:
        return None, None

def print_statistics(original, fixed):
    """Afficher les statistiques de correction."""
    print("\n=== STATISTIQUES ===")
    
    # Compter les lignes
    orig_lines = original.count('\n') + (1 if original else 0)
    fixed_lines = fixed.count('\n') + (1 if fixed else 0)
    print(f"Lignes: {orig_lines} (identique)")
    
    # Compter les tabulations
    orig_tabs = original.count('\t')
    fixed_tabs = fixed.count('\t')
    print(f"Tabulations: {orig_tabs} → {fixed_tabs} ", end='')
    if orig_tabs == fixed_tabs:
        print("✓ préservées")
    else:
        print(f"⚠ différence de {fixed_tabs - orig_tabs}")
    
    # Compter les caractères problématiques
    mojibake_patterns = ['Ã', 'Â', 'â', '€']
    orig_problems = sum(original.count(p) for p in mojibake_patterns)
    fixed_problems = sum(fixed.count(p) for p in mojibake_patterns)
    print(f"Caractères problématiques: {orig_problems} → {fixed_problems}")
    
    # Compter les caractères grecs/mathématiques
    greek_math = 'αβγδεζηθικλμνξοπρστυφχψω⊗∑∂∇∈∉⊆⊂∩∪→⇒⟨⟩≤≥≠≡≈'
    orig_good = sum(1 for c in original if c in greek_math)
    fixed_good = sum(1 for c in fixed if c in greek_math)
    print(f"Caractères grecs/mathématiques: {orig_good} → {fixed_good}")
    
    # Aperçu des corrections
    print("\n=== APERÇU DES CORRECTIONS ===")
    orig_lines_list = original.split('\n')
    fixed_lines_list = fixed.split('\n')
    
    preview_count = 0
    for i in range(min(10, len(orig_lines_list))):
        if orig_lines_list[i] != fixed_lines_list[i]:
            preview_count += 1
            if preview_count <= 5:  # Limiter à 5 exemples
                print(f"\nLigne {i+1}:")
                before = orig_lines_list[i][:80]
                after = fixed_lines_list[i][:80]
                print(f"  Avant: {before}")
                print(f"  Après: {after}")

def main():
    """Fonction principale."""
    if len(sys.argv) < 2:
        print("""
Correcteur d'encodage avec préservation de la mise en forme
        
Usage: python transcode.py <fichier_entrée> [<fichier_sortie>]
        
Exemples:
  python transcode.py input.json
  python transcode.py input.json output_fixed.json
  python transcode.py input.txt output_fixed.txt
        """)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(input_file).exists():
        print(f"Erreur: Le fichier '{input_file}' n'existe pas.")
        sys.exit(1)
    
    success = process_file_preserving_format(input_file, output_file)
    
    if success:
        print("\n✓ Correction terminée avec succès!")
    else:
        print("\n✗ Échec de la correction.")

if __name__ == '__main__':
    main()