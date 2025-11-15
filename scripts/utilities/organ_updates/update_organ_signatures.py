#!/usr/bin/env python3
"""
Batch update all 10 organ signatures to accept entity context parameter.
Follows CARD organ pattern for consistency.

November 14, 2025 - Entity-Organism Integration Phase 2.2
"""

import re
from pathlib import Path

# Organs to update (CARD already has context parameter)
ORGANS = [
    ('LISTENING', 'organs/modular/listening/core/listening_text_core.py'),
    ('EMPATHY', 'organs/modular/empathy/core/empathy_text_core.py'),
    ('WISDOM', 'organs/modular/wisdom/core/wisdom_text_core.py'),
    ('AUTHENTICITY', 'organs/modular/authenticity/core/authenticity_text_core.py'),
    ('PRESENCE', 'organs/modular/presence/core/presence_text_core.py'),
    ('BOND', 'organs/modular/bond/core/bond_text_core.py'),
    ('SANS', 'organs/modular/sans/core/sans_text_core.py'),
    ('NDAM', 'organs/modular/ndam/core/ndam_text_core.py'),
    ('RNX', 'organs/modular/rnx/core/rnx_text_core.py'),
    ('EO', 'organs/modular/eo/core/eo_text_core.py'),
]

BASE_DIR = Path('/Users/daedalea/Desktop/DAE_HYPHAE_1')


def update_organ_signature(organ_name: str, file_path: str):
    """Update process_text_occasions signature to accept context parameter."""
    full_path = BASE_DIR / file_path

    if not full_path.exists():
        print(f"❌ {organ_name}: File not found - {file_path}")
        return False

    with open(full_path, 'r') as f:
        content = f.read()

    # Pattern to match: def process_text_occasions(self, occasions: List, cycle: int) -> XResult:
    # Replace with: def process_text_occasions(self, occasions: List, cycle: int, context: Optional[Dict] = None) -> XResult:

    pattern = r'(def process_text_occasions\(\s*self,\s*occasions:\s*List.*?,\s*cycle:\s*int)\s*\)\s*->'
    replacement = r'\1, context: Optional[Dict] = None) ->'

    new_content, count = re.subn(pattern, replacement, content)

    if count == 0:
        print(f"⚠️  {organ_name}: No signature found to update")
        return False

    # Check if Optional and Dict are imported
    has_optional = 'from typing import' in content and 'Optional' in content
    has_dict = 'Dict' in content or 'from typing import' in content

    if not has_optional or not has_dict:
        # Add imports at top after existing typing imports
        import_pattern = r'(from typing import [^\n]+)'

        def add_imports(match):
            imports = match.group(1)
            if 'Optional' not in imports:
                imports = imports.replace('import ', 'import Optional, ')
            if 'Dict' not in imports:
                imports = imports.replace('import ', 'import Dict, ')
            return imports

        new_content = re.sub(import_pattern, add_imports, new_content, count=1)

    # Write updated content
    with open(full_path, 'w') as f:
        f.write(new_content)

    print(f"✅ {organ_name}: Signature updated ({count} occurrence)")
    return True


def main():
    """Update all organ signatures."""
    print("🌀 Updating organ signatures for entity context support\n")

    updated = 0
    failed = 0

    for organ_name, file_path in ORGANS:
        if update_organ_signature(organ_name, file_path):
            updated += 1
        else:
            failed += 1

    print(f"\n📊 Results: {updated} updated, {failed} failed/skipped")
    print("\n✅ Phase 2.2 signature updates complete!")
    print("Note: Organs will now accept context parameter but won't use it yet.")
    print("Entity awareness will emerge through Hebbian learning.")


if __name__ == '__main__':
    main()
