#!/usr/bin/env python3
"""
Migrate FireTriangle README and HTML to It/Im nomenclature
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-18
"""

import re
from pathlib import Path

# Paths
README_PATH = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg/instances/poclets/FireTriangle/M0_FireTriangle_README.md")
HTML_PATH = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg/instances/poclets/FireTriangle/static/M0_FireTriangle.html")

def migrate_readme(content):
    """Migrate README markdown: |I⟩ → |It⟩ (ASFID) or |Im⟩ (REVOI)"""
    modifications = []
    
    # Pattern 1: ASFID state vectors with order A, S, F, I, D
    # Example: |Ω_fire⟩ = 0.85|A⟩ + 0.70|S⟩ + 0.90|F⟩ + 0.65|I⟩ + 0.75|D⟩
    pattern_asfid = r'(\|[A-Z_]+⟩\s*=\s*[\d.]+\|A⟩\s*\+\s*[\d.]+\|S⟩\s*\+\s*[\d.]+\|F⟩\s*\+\s*[\d.]+)\|I⟩(\s*\+\s*[\d.]+\|D⟩)'
    
    def replace_asfid(match):
        modifications.append(f"ASFID vector: |I⟩ → |It⟩")
        return match.group(1) + '|It⟩' + match.group(2)
    
    content = re.sub(pattern_asfid, replace_asfid, content)
    
    # Pattern 2: REVOI state vectors (contains O, R, I, V, E but not all of A,S,F,D)
    # Example: |M_triangle⟩_REVOI = 0.80|O⟩ + 0.90|R⟩ + 0.90|I⟩ + 0.95|V⟩ + 0.70|E⟩
    pattern_revoi = r'(\|[A-Z_]+⟩_REVOI\s*=\s*(?:[\d.]+\|[ORVE]⟩\s*\+\s*)+[\d.]+)\|I⟩'
    
    def replace_revoi(match):
        modifications.append(f"REVOI vector: |I⟩ → |Im⟩")
        return match.group(1) + '|Im⟩'
    
    content = re.sub(pattern_revoi, replace_revoi, content)
    
    # Pattern 3: Standalone mentions in tables/lists with ASFID context
    # Lines containing "| **I**" or "I:" in ASFID sections
    lines = content.split('\n')
    in_asfid_section = False
    in_revoi_section = False
    
    for i, line in enumerate(lines):
        # Detect section boundaries
        if 'ASFID Analysis' in line or 'Eagle Eye' in line:
            in_asfid_section = True
            in_revoi_section = False
        elif 'REVOI Analysis' in line or 'Sphinx Eye' in line:
            in_revoi_section = True
            in_asfid_section = False
        elif line.startswith('##'):  # New section
            in_asfid_section = False
            in_revoi_section = False
        
        # Replace in appropriate sections
        if in_asfid_section and '**I**' in line:
            lines[i] = line.replace('**I**', '**It**')
            modifications.append(f"Line {i+1}: **I** → **It** (ASFID section)")
        elif in_revoi_section and '**I**' in line:
            lines[i] = line.replace('**I**', '**Im**')
            modifications.append(f"Line {i+1}: **I** → **Im** (REVOI section)")
    
    content = '\n'.join(lines)
    
    # Pattern 4: ASFID/REVOI in parentheses like (A, S, F, I, D)
    content = re.sub(r'\(A,\s*S,\s*F,\s*I,\s*D\)', '(A, S, F, It, D)', content)
    modifications.append("Dimension list: (A, S, F, I, D) → (A, S, F, It, D)")
    
    return content, modifications

def migrate_html(content):
    """Migrate HTML: I: → It: (asfid) or Im: (revoi)"""
    modifications = []
    
    # Pattern 1: asfid objects
    # asfid: { A: 0.90, S: 0.85, F: 0.85, I: 0.80, D: 0.90 }
    pattern_asfid = r'(asfid:\s*\{[^}]*?)\bI:(\s*[\d.]+)'
    
    def replace_asfid(match):
        modifications.append(f"asfid object: I: → It:")
        return match.group(1) + 'It:' + match.group(2)
    
    content = re.sub(pattern_asfid, replace_asfid, content)
    
    # Pattern 2: revoi objects
    # revoi: { R: 0.90, E: 0.70, V: 0.95, O: 0.85, I: 0.85 }
    pattern_revoi = r'(revoi:\s*\{[^}]*?)\bI:(\s*[\d.]+)'
    
    def replace_revoi(match):
        modifications.append(f"revoi object: I: → Im:")
        return match.group(1) + 'Im:' + match.group(2)
    
    content = re.sub(pattern_revoi, replace_revoi, content)
    
    # Pattern 3: Template strings referencing .asfid.I
    # ASFID: A=${pole.asfid.A} ... I=${pole.asfid.I} ...
    pattern_asfid_ref = r'(\$\{pole\.asfid\.)I(\})'
    content = re.sub(pattern_asfid_ref, r'\1It\2', content)
    modifications.append("Template reference: pole.asfid.I → pole.asfid.It")
    
    # Pattern 4: Template strings referencing .revoi.I
    pattern_revoi_ref = r'(\$\{pole\.revoi\.)I(\})'
    if re.search(pattern_revoi_ref, content):
        content = re.sub(pattern_revoi_ref, r'\1Im\2', content)
        modifications.append("Template reference: pole.revoi.I → pole.revoi.Im")
    
    # Pattern 5: CSS variables --col-I should become --col-It (if exists)
    # Already done: --col-Im exists, but check for --col-I
    if '--col-I:' in content and '--col-It:' not in content:
        # This is tricky - we need to know if it's for ASFID or REVOI
        # In FireTriangle, there's likely one for each
        # For now, let's flag it for manual review
        modifications.append("WARNING: Check CSS variable --col-I manually")
    
    return content, modifications

def main():
    """Main entry point."""
    print("="*70)
    print("Migrating FireTriangle README and HTML to It/Im")
    print("="*70)
    
    all_modifications = []
    
    # ===== Migrate README =====
    print("\n📄 Processing README...")
    if README_PATH.exists():
        with open(README_PATH, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        new_readme, readme_mods = migrate_readme(readme_content)
        
        if readme_mods:
            with open(README_PATH, 'w', encoding='utf-8') as f:
                f.write(new_readme)
            
            print(f"  ✓ {len(readme_mods)} modifications:")
            for mod in readme_mods[:5]:
                print(f"    • {mod}")
            if len(readme_mods) > 5:
                print(f"    ... and {len(readme_mods) - 5} more")
            all_modifications.extend(readme_mods)
        else:
            print("  ℹ No changes needed")
    else:
        print(f"  ⚠ File not found: {README_PATH}")
    
    # ===== Migrate HTML =====
    print("\n🌐 Processing HTML...")
    if HTML_PATH.exists():
        with open(HTML_PATH, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        new_html, html_mods = migrate_html(html_content)
        
        if html_mods:
            with open(HTML_PATH, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print(f"  ✓ {len(html_mods)} modifications:")
            for mod in html_mods[:5]:
                print(f"    • {mod}")
            if len(html_mods) > 5:
                print(f"    ... and {len(html_mods) - 5} more")
            all_modifications.extend(html_mods)
        else:
            print("  ℹ No changes needed")
    else:
        print(f"  ⚠ File not found: {HTML_PATH}")
    
    # ===== Summary =====
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if all_modifications:
        print(f"\n✅ Migration complete! {len(all_modifications)} total modifications")
        print("\nFiles updated:")
        if README_PATH.exists():
            print(f"  • {README_PATH}")
        if HTML_PATH.exists():
            print(f"  • {HTML_PATH}")
        
        print("\n" + "="*70)
        print("Next steps:")
        print("="*70)
        print("1. Review the changes (especially CSS variables if flagged)")
        print("2. Test the HTML simulation in a browser")
        print("3. Verify the README renders correctly")
        return 0
    else:
        print("\n✅ All files already use It/Im nomenclature")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
