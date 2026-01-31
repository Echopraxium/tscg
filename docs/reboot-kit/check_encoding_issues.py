#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de détection d'encodages suspects dans fichiers JSON-LD TSCG
Auteur: Echopraxium with the collaboration of Claude AI
Date: 2026-01-31
"""

import sys
import json
from pathlib import Path
from collections import defaultdict

# Caractères suspects indicateurs de corruption UTF-8
SUSPECT_CHARS = {
    'Ã': 'Corruption UTF-8 (début séquence)',
    'Â': 'Artefact UTF-8',
    'â€': 'Symbole corrompu (flèche/quote)',
    'Å': 'Latin étendu corrompu',
    '¢': 'Cent sign (souvent corruption)',
    '€': 'Euro sign (souvent corruption symboles math)',
    '‚': 'Single low quote (corruption)',
    'ƒ': 'Latin f hook (corruption)',
    '„': 'Double low quote (corruption)',
    '…': 'Ellipsis (parfois corruption)',
}

# Patterns spécifiques TSCG
TSCG_CORRUPT_PATTERNS = [
    'Ã¢Å â€"',      # ⊗ corrompu
    'ÃƒÂ¢Ã…Â Ã¢â‚¬â€',  # ⊗ double-encodé
    'Ã¢â€ â€™',     # → corrompu
    'Ã¢â€°Â¥',      # ≥ corrompu
    'Ã¢Ë†Ë†',       # ∈ corrompu
    'Ã¢Ë†Â«',       # ∫ corrompu
    'ÃŽâ€',         # δ corrompu
    'Ãâ€ž',         # τ corrompu
    'REVOÃŽ',        # REVOI avec circonflexe
    'Â¡Â·',         # ∇· corrompu
]

def check_file_encoding(filepath):
    """
    Analyse un fichier JSON-LD pour détecter les encodages suspects.
    
    Args:
        filepath: Chemin vers le fichier à analyser
        
    Returns:
        dict: Résultats de l'analyse
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        return {'error': f'Fichier non trouvé: {filepath}'}
    
    # Lire le fichier
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError as e:
        return {'error': f'Erreur de décodage UTF-8: {e}'}
    
    # Structures de résultats
    results = {
        'filename': filepath.name,
        'total_lines': len(lines),
        'suspect_lines': [],
        'suspect_chars_count': defaultdict(int),
        'corrupt_patterns_count': defaultdict(int),
        'json_valid': False,
    }
    
    # Analyser ligne par ligne
    for line_num, line in enumerate(lines, start=1):
        line_issues = []
        
        # Détecter caractères suspects
        for char, description in SUSPECT_CHARS.items():
            if char in line:
                count = line.count(char)
                results['suspect_chars_count'][char] += count
                line_issues.append(f"{char} ({description}): {count}x")
        
        # Détecter patterns corrompus TSCG
        for pattern in TSCG_CORRUPT_PATTERNS:
            if pattern in line:
                count = line.count(pattern)
                results['corrupt_patterns_count'][pattern] += count
                line_issues.append(f"Pattern '{pattern}': {count}x")
        
        # Si la ligne a des problèmes, l'enregistrer
        if line_issues:
            results['suspect_lines'].append({
                'line_num': line_num,
                'content': line.rstrip(),
                'issues': line_issues
            })
    
    # Valider JSON
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        results['json_valid'] = True
    except json.JSONDecodeError as e:
        results['json_error'] = str(e)
    
    return results

def print_results(results):
    """Affiche les résultats de l'analyse de manière formatée."""
    
    if 'error' in results:
        print(f"❌ ERREUR: {results['error']}")
        return
    
    print("="*80)
    print(f"📄 Fichier: {results['filename']}")
    print(f"📊 Total lignes: {results['total_lines']}")
    print(f"⚠️  Lignes suspectes: {len(results['suspect_lines'])}")
    print(f"✅ JSON valide: {'OUI' if results['json_valid'] else 'NON'}")
    
    if 'json_error' in results:
        print(f"   Erreur JSON: {results['json_error']}")
    
    print("="*80)
    
    # Résumé des caractères suspects
    if results['suspect_chars_count']:
        print("\n🔍 CARACTÈRES SUSPECTS DÉTECTÉS:")
        print("-"*80)
        for char, count in sorted(results['suspect_chars_count'].items(), 
                                   key=lambda x: x[1], reverse=True):
            description = SUSPECT_CHARS.get(char, 'Inconnu')
            print(f"  '{char}' ({description}): {count} occurrences")
    
    # Résumé des patterns corrompus
    if results['corrupt_patterns_count']:
        print("\n🚨 PATTERNS CORROMPUS TSCG:")
        print("-"*80)
        for pattern, count in sorted(results['corrupt_patterns_count'].items(), 
                                      key=lambda x: x[1], reverse=True):
            print(f"  '{pattern}': {count} occurrences")
    
    # Liste des lignes suspectes
    if results['suspect_lines']:
        print(f"\n📋 LISTE DES LIGNES SUSPECTES ({len(results['suspect_lines'])}):")
        print("-"*80)
        
        for item in results['suspect_lines']:
            print(f"\n  Ligne {item['line_num']}:")
            print(f"    Contenu: {item['content'][:100]}")
            if len(item['content']) > 100:
                print(f"             ... (tronqué)")
            print(f"    Problèmes:")
            for issue in item['issues']:
                print(f"      - {issue}")
    else:
        print("\n✅ Aucun problème d'encodage détecté !")
    
    print("\n" + "="*80)

def save_report(results, output_file):
    """Sauvegarde le rapport dans un fichier texte."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT D'ANALYSE D'ENCODAGE - {results['filename']}\n")
        f.write(f"{'='*80}\n\n")
        
        f.write(f"Total lignes: {results['total_lines']}\n")
        f.write(f"Lignes suspectes: {len(results['suspect_lines'])}\n")
        f.write(f"JSON valide: {'OUI' if results['json_valid'] else 'NON'}\n\n")
        
        if results['suspect_chars_count']:
            f.write("CARACTÈRES SUSPECTS:\n")
            f.write("-"*80 + "\n")
            for char, count in sorted(results['suspect_chars_count'].items(), 
                                       key=lambda x: x[1], reverse=True):
                description = SUSPECT_CHARS.get(char, 'Inconnu')
                f.write(f"  '{char}' ({description}): {count} occurrences\n")
            f.write("\n")
        
        if results['corrupt_patterns_count']:
            f.write("PATTERNS CORROMPUS TSCG:\n")
            f.write("-"*80 + "\n")
            for pattern, count in sorted(results['corrupt_patterns_count'].items(), 
                                          key=lambda x: x[1], reverse=True):
                f.write(f"  '{pattern}': {count} occurrences\n")
            f.write("\n")
        
        if results['suspect_lines']:
            f.write(f"LIGNES SUSPECTES ({len(results['suspect_lines'])}):\n")
            f.write("-"*80 + "\n\n")
            
            for item in results['suspect_lines']:
                f.write(f"Ligne {item['line_num']}:\n")
                f.write(f"  {item['content']}\n")
                f.write(f"  Problèmes:\n")
                for issue in item['issues']:
                    f.write(f"    - {issue}\n")
                f.write("\n")
    
    print(f"\n💾 Rapport sauvegardé dans: {output_file}")

def main():
    """Point d'entrée principal du script."""
    
    if len(sys.argv) < 2:
        print("Usage: python check_encoding_issues.py <fichier.jsonld> [--save-report]")
        print("\nExemples:")
        print("  python check_encoding_issues.py M2_MetaConcepts.jsonld")
        print("  python check_encoding_issues.py M2_MetaConcepts.jsonld --save-report")
        sys.exit(1)
    
    filepath = sys.argv[1]
    save_report_flag = '--save-report' in sys.argv
    
    # Analyser le fichier
    results = check_file_encoding(filepath)
    
    # Afficher les résultats
    print_results(results)
    
    # Sauvegarder le rapport si demandé
    if save_report_flag and 'error' not in results:
        output_file = Path(filepath).stem + '_encoding_report.txt'
        save_report(results, output_file)
    
    # Code de sortie
    if 'error' in results:
        sys.exit(1)
    elif results['suspect_lines']:
        sys.exit(2)  # Code 2 = problèmes détectés mais pas fatal
    else:
        sys.exit(0)  # Code 0 = tout OK

if __name__ == '__main__':
    main()
