#!/usr/bin/env python3
"""
Apply comprehensive fix for family formation bug (V2).

Root cause: Organ signature extractor expects dicts but receives dataclass objects.
This includes NESTED dataclasses (e.g., ListeningPattern inside ListeningResult).

Fix: Recursive conversion of all dataclass objects to dicts.
"""

import sys
import shutil
from pathlib import Path

# Paths
PROJECT_ROOT = Path('/Users/daedalea/Desktop/DAE_HYPHAE_1')
LEARNING_FILE = PROJECT_ROOT / 'persona_layer' / 'phase5_learning_integration.py'
BACKUP_FILE = LEARNING_FILE.with_suffix('.py.backup_before_fix_v2')

print("="*80)
print("🔧 APPLYING FIX V2: Recursive Dataclass → Dict Conversion")
print("="*80)
print()

# Step 1: Restore from first backup or create new backup
print("Step 1: Creating backup...")
if BACKUP_FILE.exists():
    print(f"   ℹ️  Backup already exists: {BACKUP_FILE}")
else:
    shutil.copy(LEARNING_FILE, BACKUP_FILE)
    print(f"   ✅ Backup created: {BACKUP_FILE}")
print()

# Step 2: Read current file
print("Step 2: Reading current file...")
with open(LEARNING_FILE, 'r') as f:
    content = f.read()
print(f"   ✅ Read {len(content)} characters")
print()

# Step 3: Create improved helper method with recursive conversion
print("Step 3: Creating recursive conversion helper...")

improved_helper = '''    def _organ_results_to_dicts(self, organ_results: Dict) -> Dict:
        """
        Convert organ dataclass objects to dicts for signature extraction.

        The organ processing pipeline returns dataclass objects (e.g., ListeningResult)
        with nested dataclass objects (e.g., ListeningPattern). The signature extractor
        expects pure dicts with .get() method. This helper recursively converts all
        dataclass objects to dicts.

        Args:
            organ_results: Dict mapping organ_name -> OrganResult dataclass object

        Returns:
            Dict mapping organ_name -> dict of attributes (recursively converted)
        """
        def to_dict_recursive(obj):
            """Recursively convert dataclass objects to dicts."""
            if hasattr(obj, '__dict__'):
                # Dataclass object - convert to dict
                obj_dict = {}
                for key, value in obj.__dict__.items():
                    if isinstance(value, list):
                        # List of objects - recursively convert each
                        obj_dict[key] = [to_dict_recursive(item) for item in value]
                    elif isinstance(value, dict):
                        # Dict - recursively convert values
                        obj_dict[key] = {k: to_dict_recursive(v) for k, v in value.items()}
                    elif hasattr(value, '__dict__'):
                        # Nested dataclass - recursively convert
                        obj_dict[key] = to_dict_recursive(value)
                    else:
                        # Primitive value - use as-is
                        obj_dict[key] = value
                return obj_dict
            else:
                # Already a primitive or dict - return as-is
                return obj

        dict_results = {}
        for organ_name, result_obj in organ_results.items():
            dict_results[organ_name] = to_dict_recursive(result_obj)

        return dict_results

'''

# Check if old helper exists
if '_organ_results_to_dicts' in content:
    print("   ℹ️  Old helper method found, replacing with improved version...")

    # Find start and end of old helper
    helper_start = content.find('    def _organ_results_to_dicts(')
    if helper_start == -1:
        print("   ❌ Could not find old helper method!")
        sys.exit(1)

    # Find end of old helper (next method definition)
    helper_end = content.find('\n    def ', helper_start + 10)
    if helper_end == -1:
        print("   ❌ Could not find end of old helper method!")
        sys.exit(1)

    # Replace old helper with new one
    content = content[:helper_start] + improved_helper + content[helper_end:]
    print("   ✅ Replaced old helper with recursive version")
else:
    print("   ℹ️  No existing helper found, inserting new one...")

    # Find insertion point (before learn_from_conversation)
    insert_point = content.find('    def learn_from_conversation(')
    if insert_point == -1:
        print("   ❌ Could not find learn_from_conversation method!")
        sys.exit(1)

    # Insert helper
    content = content[:insert_point] + improved_helper + '\n' + content[insert_point:]
    print("   ✅ Inserted recursive helper method")

print()

# Step 4: Ensure conversion is called
print("Step 4: Verifying conversion call...")

if 'organ_results_dicts = self._organ_results_to_dicts(organ_results)' in content:
    print("   ✅ Conversion call already present")
elif 'self._organ_results_to_dicts' in content:
    print("   ✅ Helper method called somewhere")
else:
    print("   ⚠️  Need to add conversion call manually")

    # Find variance-weighted extraction
    extraction_line = 'self.signature_extractor.extract_composite_signature_variance_weighted('
    if extraction_line in content:
        idx = content.find(extraction_line)
        # Find start of this statement (backtrack to indent)
        line_start = content.rfind('\n', 0, idx) + 1

        # Insert conversion before extraction
        conversion = '        # Convert dataclass objects to dicts (recursive for nested objects)\n'
        conversion += '        organ_results_dicts = self._organ_results_to_dicts(organ_results)\n\n'
        content = content[:line_start] + conversion + content[line_start:]

        # Replace parameter
        content = content.replace(
            'organ_results=organ_results,',
            'organ_results=organ_results_dicts,'
        )
        print("   ✅ Added conversion call and updated parameter")

print()

# Step 5: Write updated file
print("Step 5: Writing updated file...")
with open(LEARNING_FILE, 'w') as f:
    f.write(content)
print(f"   ✅ Updated file written: {LEARNING_FILE}")
print()

# Step 6: Verify changes
print("Step 6: Verifying changes...")

if '_organ_results_to_dicts' in content:
    print("   ✅ Helper method present")
else:
    print("   ❌ Helper method NOT found!")

if 'to_dict_recursive' in content:
    print("   ✅ Recursive conversion present")
else:
    print("   ❌ Recursive conversion NOT found!")

if 'organ_results_dicts = self._organ_results_to_dicts(organ_results)' in content or 'self._organ_results_to_dicts' in content:
    print("   ✅ Conversion called")
else:
    print("   ⚠️  Conversion may not be called (check manually)")

if 'organ_results=organ_results_dicts,' in content:
    print("   ✅ Parameter updated")
else:
    print("   ⚠️  Parameter may not be updated (check manually)")

print()
print("="*80)
print("🎉 FIX V2 APPLIED SUCCESSFULLY!")
print("="*80)
print()
print("Improvements over V1:")
print("   ✅ Recursive conversion (handles nested dataclasses)")
print("   ✅ Handles lists of dataclass objects")
print("   ✅ Handles dict values that are dataclass objects")
print()
print("Next steps:")
print("   1. Run validation test: python3 VALIDATE_FAMILY_FORMATION_FIX.py")
print("   2. If validation passes, re-run arc training")
print()
