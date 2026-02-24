#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for TSCG JSON-LD to Turtle Converter
=================================================

Quick validation that the converter is properly installed and working.

Author: Echopraxium with the collaboration of Claude AI
Date: 2026-02-15
Version: 1.0.0
"""

import sys
import subprocess
from pathlib import Path

def test_python_version():
    """Test if Python version is adequate"""
    print("Testing Python version...", end=" ")
    if sys.version_info < (3, 8):
        print("❌ FAILED")
        print(f"  Python 3.8+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✓ OK ({sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})")
    return True

def test_rdflib_import():
    """Test if rdflib can be imported"""
    print("Testing rdflib import...", end=" ")
    try:
        import rdflib
        print(f"✓ OK (version {rdflib.__version__})")
        return True
    except ImportError:
        print("❌ FAILED")
        print("  Run: pip install rdflib")
        return False

def test_converter_script():
    """Test if converter script exists"""
    print("Testing converter script...", end=" ")
    script_path = Path(__file__).parent / "jsonld_to_turtle.py"
    if script_path.exists():
        print("✓ OK")
        return True
    else:
        print("❌ FAILED")
        print(f"  Script not found: {script_path}")
        return False

def test_help_message():
    """Test if converter script can show help"""
    print("Testing converter help...", end=" ")
    try:
        result = subprocess.run(
            [sys.executable, "jsonld_to_turtle.py", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and "TSCG JSON-LD" in result.stdout:
            print("✓ OK")
            return True
        else:
            print("❌ FAILED")
            return False
    except Exception as e:
        print(f"❌ FAILED ({str(e)})")
        return False

def test_dry_run():
    """Test dry-run mode"""
    print("Testing dry-run mode...", end=" ")
    try:
        result = subprocess.run(
            [sys.executable, "jsonld_to_turtle.py", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=30
        )
        # Dry-run should succeed even if no files found
        if result.returncode in [0, 1]:  # 1 is OK if no files found
            print("✓ OK")
            return True
        else:
            print("❌ FAILED")
            print(f"  Return code: {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ FAILED ({str(e)})")
        return False

def main():
    """Run all tests"""
    print("="*70)
    print("TSCG Converter - Installation Test")
    print("="*70)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("RDFLib Library", test_rdflib_import),
        ("Converter Script", test_converter_script),
        ("Help Message", test_help_message),
        ("Dry-Run Mode", test_dry_run)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            results.append(test_func())
        except Exception as e:
            print(f"❌ FAILED ({str(e)})")
            results.append(False)
        print()
    
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    
    for (name, _), result in zip(tests, results):
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}  {name}")
    
    print()
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print()
        print("✓ All tests passed! Converter is ready to use.")
        print()
        print("Next steps:")
        print("  1. Run: python jsonld_to_turtle.py --dry-run")
        print("  2. Run: python jsonld_to_turtle.py")
        print("  3. Open generated .ttl files in Protégé")
        return 0
    else:
        print()
        print("⚠ Some tests failed. Please fix issues before using converter.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
