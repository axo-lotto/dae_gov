#!/usr/bin/env python3
"""
Phase 1 Task 1.1: Add atom_activations field to all 11 organ result dataclasses

This script adds two new fields to each organ result dataclass:
1. atom_activations: Dict[str, float] = field(default_factory=dict)
2. felt_vector: Optional[np.ndarray] = None

Modifies all 11 organs in place.
"""

import re
from pathlib import Path

def add_atom_activations_to_result_dataclass(file_path: Path):
    """Add atom_activations and felt_vector fields to organ result dataclass."""

    content = file_path.read_text()

    # Pattern to find the Result dataclass and its last field before the blank line
    # We want to insert the new fields right before the final blank line or next @dataclass

    organ_name = file_path.stem.replace('_text_core', '').upper()

    # Determine Result class name based on organ type
    # Trauma/context organs use UPPERCASE: BONDResult, SANSResult, etc.
    # Conversational organs use TitleCase: ListeningResult, EmpathyResult, etc.
    trauma_context_organs = {'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'}

    if organ_name in trauma_context_organs:
        result_class_name = f"{organ_name}Result"  # BONDResult
    else:
        result_class_name = f"{organ_name.title()}Result"  # ListeningResult

    # Find the dataclass
    dataclass_pattern = rf'(@dataclass\nclass {result_class_name}:.*?)((?:\n\n@dataclass)|(?:\n\n\nclass ))'

    def insert_fields(match):
        dataclass_body = match.group(1)
        next_section = match.group(2)

        # Check if atom_activations already exists
        if 'atom_activations' in dataclass_body:
            print(f"  ✓ {result_class_name} already has atom_activations field")
            return match.group(0)

        # Find the last field definition (line ending with a value or comment)
        # Insert before the final blank line
        lines = dataclass_body.split('\n')

        # Find where to insert (before closing blank lines)
        insert_idx = len(lines)
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            if line and not line.startswith('#') and ':' in line:
                # This is a field definition
                insert_idx = i + 1
                break

        # Create new fields
        new_fields = [
            "",
            "    # 🆕 PHASE 1: Entity-native emission support",
            "    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission",
            "    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native"
        ]

        # Insert fields
        lines[insert_idx:insert_idx] = new_fields

        new_dataclass = '\n'.join(lines)
        return new_dataclass + next_section

    # Apply the replacement
    new_content, num_subs = re.subn(dataclass_pattern, insert_fields, content, flags=re.DOTALL)

    if num_subs > 0:
        # Also add numpy import if not present
        if 'import numpy as np' not in new_content and 'np.ndarray' in new_content:
            # Find imports section and add numpy
            import_pattern = r'(from typing import [^\n]+\n)'
            new_content = re.sub(
                import_pattern,
                r'\1import numpy as np\n',
                new_content,
                count=1
            )

        file_path.write_text(new_content)
        print(f"  ✅ Modified {result_class_name} in {file_path.name}")
        return True
    else:
        print(f"  ⚠️  Could not find {result_class_name} dataclass in {file_path.name}")
        return False

def main():
    """Main execution."""
    print("=" * 70)
    print("🔧 PHASE 1 TASK 1.1: ADD atom_activations TO ALL 11 ORGANS")
    print("=" * 70)
    print()

    # Find all organ core files
    organs_dir = Path("/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular")

    organ_files = list(organs_dir.glob("*/core/*_text_core.py"))

    print(f"Found {len(organ_files)} organ files")
    print()

    modified = 0
    skipped = 0

    for file_path in sorted(organ_files):
        organ_name = file_path.parent.parent.name.upper()
        print(f"Processing {organ_name}...")

        if add_atom_activations_to_result_dataclass(file_path):
            modified += 1
        else:
            skipped += 1

    print()
    print("=" * 70)
    print(f"✅ TASK 1.1 COMPLETE")
    print(f"   Modified: {modified} organs")
    print(f"   Skipped:  {skipped} organs (already had field or couldn't find dataclass)")
    print("=" * 70)

if __name__ == '__main__':
    main()
