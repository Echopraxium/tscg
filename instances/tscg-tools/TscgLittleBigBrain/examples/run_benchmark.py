#!/usr/bin/env python3
import sys
from pathlib import Path

# Ajouter le répertoire racine (parent de 'examples') au PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Maintenant l'import fonctionne
from tests.test_benchmark import main

if __name__ == "__main__":
    main()