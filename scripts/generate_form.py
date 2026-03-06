#!/usr/bin/env python3
"""Pet Sitter Client Intake Form Generator.

This is a thin wrapper for backward compatibility.
All logic lives in the pet_sitter_intake package.

Usage:
    python scripts/generate_form.py --business-name "Happy Paws" --theme ocean
    python scripts/generate_form.py --config my_business.yaml
    python scripts/generate_form.py --list-themes
"""

import sys
from pathlib import Path

# Add parent dir to path so package is importable without installation
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pet_sitter_intake.cli import main

if __name__ == "__main__":
    exit(main())
