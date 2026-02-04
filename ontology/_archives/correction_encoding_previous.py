# correct_encoding.py
"""
Script de correction d'encodage pour fichiers JSON-LD TSCG
Usage: python correct_encoding.py source_file.jsonld destination_file.jsonld
"""

import json
import sys
import os

def fix_encoding(content):
    """Corrige les problèmes d'encodage dans le contenu."""
    
    # Dictionnaire complet des corrections
    corrections = {
        # Produit tensoriel
        'âŠ—': '⊗',
        'Ã¢Å â€"': '⊗',
        'Ã¢â€ â€™': '⊗',
        
        # Symboles mathématiques
        'âˆˆ': '∈',
        'âˆ‰': '∉',
        'âŠ†': '⊆',
        'âŠ‚': '⊂',
        'âŠ•': '⊕',
        'âˆ©': '∩',
        'âˆª': '∪',
        'âˆ…': '∅',
        
        # Comparaisons
        'â‰': '≈',
        'â‰ƒ': '≃',
        'â‰¤': '≤',
        'â‰¥': '≥',
        'â‰ ': '≠',
        'â‰¡': '≡',
        
        # Quantificateurs
        'âˆ€': '∀',
        'âˆƒ': '∃',
        'Â¬': '¬',
        'âˆ§': '∧',
        'âˆ¨': '∨',
        
        # Opérateurs
        'âˆ\'': '∑',
        'âˆ«': '∫',
        'âˆ‚': '∂',
        'âˆ‡': '∇',
        'âˆž': '∞',
        'âˆ': '√',
        'Â±': '±',
        'âˆ"': '∓',
        
        # Crochets
        'âŸ¨': '⟨',
        'âŸ©': '⟩',
        
        # Divers
        'âˆ¥': '∥',
        'âŠ¥': '⊥',
        'âˆ ': '∝',
        'âˆ¼': '∼',
        'â‰…': '≅',
        
        # Lettres grecques minuscules
        'Î±': 'α',
        'Î²': 'β',
        'Î³': 'γ',
        'Î´': 'δ',
        'Î"': 'δ',
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
        
        # REVOI
        'REVOÃŽ': 'REVOI',
        'REVOÃ': 'REVOI',
        'REVOÎ': 'REVOI',
        
        # Artefacts
        'Ã‚Â': '',
        'Ãƒ': '',
        'Â': ' ',
        'Â': '',
        'â': '',
        'Ã¢â€šÂ': '',
        'Ã‚': '',
        
        # Exposants et indices
        'Â¹': '¹',
        'Â²': '²',
        'Â³': '³',
        'Ã‚Â¡': 'ⁱ',
        
        # Combinaisons courantes
        'âŠ—Â': '⊗',
        'âŠ—Â': '⊗',
        'âˆ‚Â': '∂',
        
        # Flèches
        'â†\'': '→',
        'â‡': '⇒',
    }
    
    # Appliquer toutes les corrections
    for wrong, right in corrections.items():
        if wrong in content:
            count = content.count(wrong)
            if count > 0:
                content = content.replace(wrong, right)
                print(f"  Corrigé {count:3d} × '{wrong}' → '{right}'")
    
    return content

def validate_json(filepath):
    """Valide qu'un fichier contient du JSON valide."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except json.JSONDecodeError as e:
        print(f"  ✗ Erreur JSON à la ligne {e.lineno}, colonne {e.colno}:")
        print(f"    {e.msg}")
        return False
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        return False

def main():
    """Fonction principale."""
    
    # Vérifier les arguments
    if len(sys.argv) != 3:
        print("Usage: python correct_encoding.py <fichier_source> <fichier_destination>")
        print("Exemple: python correct_encoding.py M2_MetaConcepts.jsonld M2_MetaConcepts_corrige.jsonld")
        sys.exit(1)
    
    source_file = sys.argv[1]
    dest_file = sys.argv[2]
    
    # Vérifier que le fichier source existe
    if not os.path.exists(source_file):
        print(f"Erreur: Le fichier source '{source_file}' n'existe pas.")
        sys.exit(1)
    
    print(f"Source:      {source_file}")
    print(f"Destination: {dest_file}")
    print("-" * 60)
    
    # Lire le fichier source
    print("Lecture du fichier source...")
    try:
        # Essayer différents encodages
        encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-8-sig']
        content = None
        
        for encoding in encodings:
            try:
                with open(source_file, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"  Lecture réussie avec l'encodage: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("  ✗ Impossible de lire le fichier avec les encodages supportés")
            sys.exit(1)
            
    except Exception as e:
        print(f"  ✗ Erreur de lecture: {e}")
        sys.exit(1)
    
    # Afficher des statistiques
    print(f"  Taille: {len(content)} caractères")
    print(f"  Lignes: {content.count(chr(10)) + 1}")
    
    # Valider le JSON source (avant correction)
    print("\nValidation du JSON source...")
    if not validate_json(source_file):
        print("  ⚠️  Le fichier source contient des erreurs JSON")
        print("  La correction sera tentée quand même...")
    
    # Appliquer les corrections
    print("\nApplication des corrections d'encodage...")
    corrected_content = fix_encoding(content)
    
    # Écrire le fichier destination
    print(f"\nÉcriture du fichier destination...")
    try:
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        print(f"  ✓ Fichier écrit: {dest_file}")
        print(f"  Taille: {len(corrected_content)} caractères")
    except Exception as e:
        print(f"  ✗ Erreur d'écriture: {e}")
        sys.exit(1)
    
    # Valider le JSON destination
    print("\nValidation du JSON destination...")
    if validate_json(dest_file):
        print("  ✓ JSON valide!")
    else:
        print("  ✗ Le fichier corrigé contient des erreurs JSON")
        print("  Vous devrez peut-être corriger manuellement les erreurs restantes.")
    
    # Afficher un rapport de vérification
    print("\n" + "=" * 60)
    print("RAPPORT DE VÉRIFICATION:")
    print("=" * 60)
    
    verification_items = [
        ("⊗ (produit tensoriel)", "⊗" in corrected_content),
        ("∈ (appartient à)", "∈" in corrected_content),
        ("∀ (pour tout)", "∀" in corrected_content),
        ("∂ (dérivée partielle)", "∂" in corrected_content),
        ("α, β, γ (lettres grecques)", all(c in corrected_content for c in ["α", "β", "γ"])),
        ("REVOI correct", "REVOI" in corrected_content and "REVOÃŽ" not in corrected_content),
        ("Pas d'artefacts Ã", "Ã‚" not in corrected_content and "Ãƒ" not in corrected_content[:1000]),
    ]
    
    for item, check in verification_items:
        status = "✓" if check else "✗"
        print(f"  {status} {item}")
    
    # Afficher un échantillon du résultat
    print("\n" + "=" * 60)
    print("ÉCHANTILLON DU RÉSULTAT (premières 500 caractères):")
    print("=" * 60)
    print(corrected_content[:500])
    print("..." if len(corrected_content) > 500 else "")
    
    print("\n" + "=" * 60)
    print("✓ Correction terminée!")
    print(f"  Fichier source conservé: {source_file}")
    print(f"  Fichier corrigé créé:    {dest_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()