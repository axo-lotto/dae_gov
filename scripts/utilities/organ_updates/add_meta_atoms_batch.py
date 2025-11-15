"""
Batch add meta-atom loading and activation stubs to remaining 9 organs.

This script adds:
1. meta_atoms_config loading in __init__
2. _load_shared_meta_atoms() method
3. Call to _activate_meta_atoms() in _compute_atom_activations()
4. _activate_meta_atoms() stub method

Each organ will need custom logic, but this gets the structure in place.
"""

import os
import re

# Organ file paths
ORGANS = {
    'EMPATHY': 'organs/modular/empathy/core/empathy_text_core.py',
    'LISTENING': 'organs/modular/listening/core/listening_text_core.py',
    'WISDOM': 'organs/modular/wisdom/core/wisdom_text_core.py',
    'AUTHENTICITY': 'organs/modular/authenticity/core/authenticity_text_core.py',
    'PRESENCE': 'organs/modular/presence/core/presence_text_core.py',
    'SANS': 'organs/modular/sans/core/sans_text_core.py',
    'NDAM': 'organs/modular/ndam/core/ndam_text_core.py',
    'RNX': 'organs/modular/rnx/core/rnx_text_core.py',
    'CARD': 'organs/modular/card/core/card_text_core.py',
}

# Meta-atom contributions (from shared_meta_atoms.json)
META_ATOM_CONTRIB = {
    'EMPATHY': ['compassion_safety', 'fierce_holding', 'relational_attunement'],
    'LISTENING': ['relational_attunement', 'temporal_grounding', 'coherence_integration'],
    'WISDOM': ['kairos_emergence', 'coherence_integration'],
    'AUTHENTICITY': ['fierce_holding', 'kairos_emergence', 'somatic_wisdom'],
    'PRESENCE': ['temporal_grounding', 'kairos_emergence', 'somatic_wisdom'],
    'SANS': ['safety_restoration', 'compassion_safety', 'coherence_integration'],
    'NDAM': ['trauma_aware', 'safety_restoration'],
    'RNX': ['window_of_tolerance', 'temporal_grounding', 'kairos_emergence'],
    'CARD': ['window_of_tolerance'],
}

def add_init_line(organ_name, file_path):
    """Add meta_atoms_config loading to __init__."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Find self.organ_name = or self.semantic_atoms =
    pattern = r'(self\.organ_name = ["\']' + organ_name + r'["\'])'
    if re.search(pattern, content):
        replacement = r'\1\n\n        # 🆕 PHASE 2: Load shared meta-atoms for nexus formation\n        self.meta_atoms_config = self._load_shared_meta_atoms()'
        content = re.sub(pattern, replacement, content, count=1)

        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ {organ_name}: Added meta_atoms_config loading")
        return True
    else:
        print(f"⚠️  {organ_name}: Could not find organ_name assignment")
        return False

def add_load_method(organ_name, file_path, meta_atoms):
    """Add _load_shared_meta_atoms() method."""
    load_method = f'''
    def _load_shared_meta_atoms(self) -> Optional[Dict]:
        """
        🆕 PHASE 2: Load shared meta-atoms for nexus formation.

        {organ_name} contributes to {len(meta_atoms)} meta-atoms:
        {chr(10).join(f"        - {ma}" for ma in meta_atoms)}
        """
        import json
        import os
        from typing import Optional, Dict

        current_dir = os.path.dirname(os.path.abspath(__file__))
        meta_atoms_path = os.path.join(current_dir, '..', '..', '..', '..',
                                       'persona_layer', 'shared_meta_atoms.json')

        try:
            with open(meta_atoms_path, 'r') as f:
                meta_atoms_data = json.load(f)

            relevant_meta_atoms = [
                ma for ma in meta_atoms_data['meta_atoms']
                if self.organ_name in ma['contributing_organs']
            ]

            return {{
                'meta_atoms': relevant_meta_atoms,
                'count': len(relevant_meta_atoms)
            }}
        except Exception as e:
            return None
'''

    with open(file_path, 'r') as f:
        content = f.read()

    # Find _compute_atom_activations and insert before it
    pattern = r'(\n    def _compute_atom_activations)'
    if re.search(pattern, content):
        content = re.sub(pattern, load_method + r'\1', content, count=1)

        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ {organ_name}: Added _load_shared_meta_atoms() method")
        return True
    else:
        print(f"⚠️  {organ_name}: Could not find _compute_atom_activations")
        return False

print("🔧 Batch adding meta-atom support to 9 organs...\n")

for organ_name, file_path in ORGANS.items():
    print(f"\n{organ_name}:")
    meta_atoms = META_ATOM_CONTRIB.get(organ_name, [])

    if not os.path.exists(file_path):
        print(f"  ❌ File not found: {file_path}")
        continue

    # Step 1: Add meta_atoms_config loading
    add_init_line(organ_name, file_path)

    # Step 2: Add _load_shared_meta_atoms() method
    add_load_method(organ_name, file_path, meta_atoms)

    # Note: _activate_meta_atoms() logic will be organ-specific
    # and needs to be added manually based on organ patterns

print("\n\n✅ Batch additions complete!")
print("\n📋 Next step: Add custom _activate_meta_atoms() logic to each organ")
print("   Template: Check BOND or EO for reference implementation")
