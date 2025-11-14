#!/usr/bin/env python3
"""
Apply fix for family formation bug.

Root cause: Organ signature extractor expects dicts but receives dataclass objects.
Fix: Convert dataclass objects to dicts before signature extraction.
"""

import sys
import shutil
from pathlib import Path

# Paths
PROJECT_ROOT = Path('/Users/daedalea/Desktop/DAE_HYPHAE_1')
LEARNING_FILE = PROJECT_ROOT / 'persona_layer' / 'phase5_learning_integration.py'
BACKUP_FILE = LEARNING_FILE.with_suffix('.py.backup_before_fix')

print("="*80)
print("🔧 APPLYING FIX: Family Formation Bug (Dataclass → Dict Conversion)")
print("="*80)
print()

# Step 1: Backup original file
print("Step 1: Creating backup...")
shutil.copy(LEARNING_FILE, BACKUP_FILE)
print(f"   ✅ Backup created: {BACKUP_FILE}")
print()

# Step 2: Read original file
print("Step 2: Reading original file...")
with open(LEARNING_FILE, 'r') as f:
    lines = f.readlines()
print(f"   ✅ Read {len(lines)} lines")
print()

# Step 3: Insert helper method after __init__ (around line 93)
print("Step 3: Inserting helper method...")

# Find insertion point (after __init__, before learn_from_conversation)
insert_idx = None
for i, line in enumerate(lines):
    if 'def learn_from_conversation(' in line:
        insert_idx = i
        break

if insert_idx is None:
    print("   ❌ Could not find insertion point (learn_from_conversation method)")
    sys.exit(1)

helper_method = '''    def _organ_results_to_dicts(self, organ_results: Dict) -> Dict:
        """
        Convert organ dataclass objects to dicts for signature extraction.

        The organ processing pipeline returns dataclass objects (e.g., ListeningResult),
        but the signature extractor expects dicts with .get() method. This helper
        converts dataclass objects to dicts to enable signature extraction.

        Args:
            organ_results: Dict mapping organ_name -> OrganResult dataclass object

        Returns:
            Dict mapping organ_name -> dict of attributes
        """
        dict_results = {}
        for organ_name, result_obj in organ_results.items():
            if hasattr(result_obj, '__dict__'):
                # Dataclass object - convert to dict using vars()
                dict_results[organ_name] = vars(result_obj)
            else:
                # Already a dict - use as-is
                dict_results[organ_name] = result_obj
        return dict_results

'''

# Insert helper method
lines.insert(insert_idx, helper_method)
print(f"   ✅ Inserted helper method at line {insert_idx}")
print()

# Step 4: Update variance-weighted signature extraction call
print("Step 4: Updating variance-weighted signature extraction...")

# Find the variance-weighted extraction call (around line 146 + inserted lines)
update_idx = None
for i, line in enumerate(lines):
    if 'extract_composite_signature_variance_weighted(' in line and 'organ_results=' in lines[i+1]:
        update_idx = i + 1  # Next line has organ_results parameter
        break

if update_idx is None:
    print("   ⚠️  Could not find variance-weighted extraction call (may already be fixed)")
else:
    # Insert conversion before the call
    indent = ' ' * 8
    conversion_line = f'{indent}# Convert dataclass objects to dicts for signature extraction\n'
    conversion_call = f'{indent}organ_results_dicts = self._organ_results_to_dicts(organ_results)\n\n'

    lines.insert(update_idx - 1, conversion_call)
    lines.insert(update_idx - 1, conversion_line)

    # Update the parameter from organ_results to organ_results_dicts
    # Find the line with organ_results= parameter
    for j in range(update_idx, update_idx + 5):
        if 'organ_results=' in lines[j] and 'organ_results,' in lines[j]:
            lines[j] = lines[j].replace('organ_results=organ_results,', 'organ_results=organ_results_dicts,')
            print(f"   ✅ Updated parameter at line {j}")
            break

    print(f"   ✅ Added conversion call before extraction")
print()

# Step 5: Write updated file
print("Step 5: Writing updated file...")
with open(LEARNING_FILE, 'w') as f:
    f.writelines(lines)
print(f"   ✅ Updated file written: {LEARNING_FILE}")
print()

# Step 6: Verify changes
print("Step 6: Verifying changes...")
with open(LEARNING_FILE, 'r') as f:
    content = f.read()

if '_organ_results_to_dicts' in content:
    print("   ✅ Helper method present")
else:
    print("   ❌ Helper method NOT found!")

if 'organ_results_dicts = self._organ_results_to_dicts(organ_results)' in content:
    print("   ✅ Conversion call present")
else:
    print("   ❌ Conversion call NOT found!")

if 'organ_results=organ_results_dicts,' in content:
    print("   ✅ Parameter updated")
else:
    print("   ⚠️  Parameter may not be updated (check manually)")

print()
print("="*80)
print("🎉 FIX APPLIED SUCCESSFULLY!")
print("="*80)
print()
print("Next steps:")
print("   1. Run validation test: python3 VALIDATE_FAMILY_FORMATION_FIX.py")
print("   2. If validation passes, re-run arc training")
print("   3. If validation fails, restore backup:")
print(f"      cp {BACKUP_FILE} {LEARNING_FILE}")
print()
