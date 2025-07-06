#!/usr/bin/env python3
"""Einfache WWAQ-Prüfung"""

import os
from pathlib import Path

transformations = {
    'zerbrechen': 'bersten',
    'zerstören': 'wandeln',
    'verschwinden': 'schwinden',
    'Kabbala': 'Qabbala',
    'Kawana': 'Qawana',
    'WWAK': 'WWAQ'
}

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    violations = []
    for old, new in transformations.items():
        if old in content:
            count = content.count(old)
            violations.append(f"{old} ({count}x) → {new}")
    
    return violations

# Prüfe alle Python-Dateien
base_path = Path.home() / "ez-chajim-wwaq"
for py_file in base_path.rglob("*.py"):
    violations = check_file(py_file)
    if violations:
        print(f"\n📄 {py_file.name}:")
        for v in violations:
            print(f"   ⚠️  {v}")

print("\nQ!")
