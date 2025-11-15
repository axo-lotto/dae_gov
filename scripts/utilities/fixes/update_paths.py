#!/usr/bin/env python3
"""Update import paths for DAE_HYPHAE_1 migration."""
import os
import re
from pathlib import Path

def update_imports(file_path):
    """Update import statements in a Python file."""
    with open(file_path, 'r') as f:
        content = f.read()

    original = content

    # Update imports
    replacements = {
        'from unified_core.epoch_learning.core.': 'from core.',
        'from organs.modular.card.core.': 'from organs.card.',
        'from organs.modular.card.config.': 'from organs.card.',
        'from organs.modular.card.algorithms.': 'from organs.card.algorithms.',
        'from organs.modular.card': 'from organs.card',
        'from organs.shared.satisfaction.': 'from organs.shared.satisfaction.',
        'from organs.shared.spatial.': 'from organs.shared.spatial.',
        'from transductive_core.': 'from transductive.',
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    # Update hardcoded paths
    content = content.replace(
        '/Users/daedalea/Desktop/DAE 3.0 AXO ARC ',
        '/Users/daedalea/Desktop/DAE_HYPHAE_1'
    )

    # Update data paths
    content = content.replace('TSK/', 'data/')
    content = content.replace('"TSK', '"data')

    # Update ARC data paths
    content = content.replace(
        'ARC DATA/arg_agi_1/ARC-AGI-1.0.2/data/training',
        'arc_data/arc1/training'
    )
    content = content.replace(
        'ARC DATA/arc-agi_training_challenges.json',
        'arc_data/arc2/arc-agi_training_challenges.json'
    )
    content = content.replace(
        'ARC DATA/arc-agi_training_solutions.json',
        'arc_data/arc2/arc-agi_training_solutions.json'
    )

    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {file_path}")
        return True
    return False

# Process all Python files
print("🔄 Updating import paths...")
updated = 0
for py_file in Path('.').rglob('*.py'):
    if 'update_paths.py' not in str(py_file):  # Don't update self
        if update_imports(py_file):
            updated += 1

print(f"\n✅ Updated {updated} files")
