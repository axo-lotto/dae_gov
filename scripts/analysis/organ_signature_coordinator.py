#!/usr/bin/env python3
"""
Organ Signature Coordinator - Batch update all organ signatures for entity context.

Handles multi-line signatures intelligently by parsing the full method definition.
November 14, 2025 - Entity-Organism Integration Phase 2.2

Usage:
    python3 organ_signature_coordinator.py --dry-run  # Preview changes
    python3 organ_signature_coordinator.py            # Apply changes
"""

import re
import argparse
from pathlib import Path
from typing import Tuple, Optional

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


def find_signature_span(content: str, start_pos: int) -> Tuple[int, int]:
    """
    Find the full span of a multi-line function signature.

    Returns: (start_index, end_index) of the signature including the closing paren + return type
    """
    # Find the opening '(' after 'def process_text_occasions'
    paren_count = 0
    in_signature = False
    signature_start = start_pos

    i = start_pos
    while i < len(content):
        char = content[i]

        if char == '(':
            paren_count += 1
            in_signature = True
        elif char == ')':
            paren_count -= 1
            if paren_count == 0 and in_signature:
                # Found the closing paren, now find the return type
                # Look for ') -> XResult:' pattern
                rest = content[i:i+200]
                match = re.search(r'\)\s*->\s*\w+Result:', rest)
                if match:
                    signature_end = i + match.end()
                    return signature_start, signature_end
                else:
                    # No return type found, just close at ')'
                    return signature_start, i + 1

        i += 1

    return signature_start, i


def update_organ_signature(organ_name: str, file_path: str, dry_run: bool = False) -> bool:
    """Update process_text_occasions signature to accept context parameter."""
    full_path = BASE_DIR / file_path

    if not full_path.exists():
        print(f"❌ {organ_name}: File not found - {file_path}")
        return False

    with open(full_path, 'r') as f:
        content = f.read()

    # Find the method definition
    pattern = r'def process_text_occasions\('
    match = re.search(pattern, content)

    if not match:
        print(f"⚠️  {organ_name}: No process_text_occasions method found")
        return False

    # Find the full signature span
    sig_start, sig_end = find_signature_span(content, match.start())
    original_sig = content[sig_start:sig_end]

    # Check if already has context parameter
    if 'context:' in original_sig or 'context =' in original_sig:
        print(f"✓  {organ_name}: Already has context parameter")
        return True

    # Parse the signature
    # Pattern: def process_text_occasions(self, occasions: List, cycle: int) -> XResult:
    # We need to insert ", context: Optional[Dict] = None" before the closing paren

    # Find the position just before ') ->'
    close_paren_match = re.search(r'\)\s*->', original_sig)
    if not close_paren_match:
        print(f"⚠️  {organ_name}: Couldn't parse signature format")
        return False

    insert_pos = sig_start + close_paren_match.start()

    # Build the new signature by inserting the context parameter
    new_content = (
        content[:insert_pos] +
        ',\n        context: Optional[Dict] = None' +
        content[insert_pos:]
    )

    # Ensure imports are present
    has_optional = 'Optional' in content[:5000]  # Check first 5000 chars (imports section)
    has_dict = 'Dict' in content[:5000]

    if not has_optional or not has_dict:
        # Find the typing import line
        import_match = re.search(r'from typing import ([^\n]+)', new_content)
        if import_match:
            current_imports = import_match.group(1)
            imports_to_add = []

            if not has_optional and 'Optional' not in current_imports:
                imports_to_add.append('Optional')
            if not has_dict and 'Dict' not in current_imports:
                imports_to_add.append('Dict')

            if imports_to_add:
                # Add to existing imports
                new_imports = current_imports.rstrip() + ', ' + ', '.join(imports_to_add)
                new_content = new_content.replace(
                    f'from typing import {current_imports}',
                    f'from typing import {new_imports}'
                )

    # Show preview
    new_sig = new_content[sig_start:sig_end + 60]  # Include a bit more to show the change
    print(f"\n{'='*60}")
    print(f"📝 {organ_name}")
    print(f"{'='*60}")
    print(f"Before:\n{original_sig[:150]}...")
    print(f"\nAfter:\n{new_sig[:200]}...")

    if dry_run:
        print(f"🔍 DRY RUN - No changes written")
        return True

    # Write updated content
    with open(full_path, 'w') as f:
        f.write(new_content)

    print(f"✅ Updated!")
    return True


def main():
    """Coordinate organ signature updates."""
    parser = argparse.ArgumentParser(description='Update organ signatures for entity context support')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing')
    args = parser.parse_args()

    print("🌀 Organ Signature Coordinator")
    print("Entity-Organism Integration Phase 2.2")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'APPLY CHANGES'}\n")

    updated = 0
    failed = 0
    skipped = 0

    for organ_name, file_path in ORGANS:
        result = update_organ_signature(organ_name, file_path, dry_run=args.dry_run)
        if result:
            if "Already has" in str(result):
                skipped += 1
            else:
                updated += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"📊 Results: {updated} updated, {skipped} skipped, {failed} failed")

    if args.dry_run:
        print(f"\n🔍 This was a DRY RUN - no files were modified")
        print(f"Run without --dry-run to apply changes")
    else:
        print(f"\n✅ Organ signatures updated!")
        print(f"\nNext steps:")
        print(f"1. Test integration: python3 test_entity_integration_basic.py")
        print(f"2. Verify no errors in organism processing")
        print(f"3. Begin entity awareness testing")


if __name__ == '__main__':
    main()
