"""
Batch add meta-atom template methods to remaining 7 organs.
This adds the structural code, but activation logic will be simple (coherence-based).
"""

import re
from pathlib import Path

ORGANS = {
    'EMPATHY': {
        'path': 'organs/modular/empathy/core/empathy_text_core.py',
        'meta_atoms': ['compassion_safety', 'fierce_holding', 'relational_attunement']
    },
    'LISTENING': {
        'path': 'organs/modular/listening/core/listening_text_core.py',
        'meta_atoms': ['relational_attunement', 'temporal_grounding', 'coherence_integration']
    },
    'WISDOM': {
        'path': 'organs/modular/wisdom/core/wisdom_text_core.py',
        'meta_atoms': ['kairos_emergence', 'coherence_integration']
    },
    'AUTHENTICITY': {
        'path': 'organs/modular/authenticity/core/authenticity_text_core.py',
        'meta_atoms': ['fierce_holding', 'kairos_emergence', 'somatic_wisdom']
    },
    'PRESENCE': {
        'path': 'organs/modular/presence/core/presence_text_core.py',
        'meta_atoms': ['temporal_grounding', 'kairos_emergence', 'somatic_wisdom']
    },
    'RNX': {
        'path': 'organs/modular/rnx/core/rnx_text_core.py',
        'meta_atoms': ['window_of_tolerance', 'temporal_grounding', 'kairos_emergence']
    },
    'CARD': {
        'path': 'organs/modular/card/core/card_text_core.py',
        'meta_atoms': ['window_of_tolerance']
    },
}

LOAD_METHOD_TEMPLATE = '''
    def _load_shared_meta_atoms(self) -> Optional[Dict]:
        """🆕 PHASE 2: Load shared meta-atoms for nexus formation."""
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
            return {'meta_atoms': relevant_meta_atoms, 'count': len(relevant_meta_atoms)}
        except Exception as e:
            return None
'''

ACTIVATE_METHOD_TEMPLATE = '''
    def _activate_meta_atoms(self, patterns, coherence, lure) -> Dict[str, float]:
        """🆕 PHASE 2: Activate shared meta-atoms (simple coherence-based)."""
        if not self.meta_atoms_config or not patterns:
            return {}
        meta_activations = {}
        import numpy as np
        # Simple activation: If patterns detected and coherence > 0.5, activate all meta-atoms
        if coherence > 0.5:
            for meta_atom in self.meta_atoms_config['meta_atoms']:
                activation = coherence * (0.5 + 0.5 * lure)
                meta_activations[meta_atom['atom']] = min(1.0, activation)
        return meta_activations
'''

def add_meta_atoms_to_organ(organ_name, organ_info):
    """Add meta-atom support to a single organ."""
    file_path = Path(organ_info['path'])

    if not file_path.exists():
        print(f"  ❌ {organ_name}: File not found")
        return False

    with open(file_path, 'r') as f:
        content = f.read()

    # Step 1: Add meta_atoms_config loading after self.organ_name
    if 'self.meta_atoms_config' not in content:
        pattern = rf'(self\.organ_name = ["\']' + organ_name + r'["\'])'
        if re.search(pattern, content):
            replacement = r'\1\n\n        # 🆕 PHASE 2: Load shared meta-atoms\n        self.meta_atoms_config = self._load_shared_meta_atoms()'
            content = re.sub(pattern, replacement, content, count=1)
            print(f"  ✅ {organ_name}: Added config loading")
        else:
            print(f"  ⚠️  {organ_name}: Could not find organ_name assignment")
            return False

    # Step 2: Add _load_shared_meta_atoms() method before _compute_atom_activations
    if '_load_shared_meta_atoms' not in content:
        pattern = r'(\n    def _compute_atom_activations)'
        content = re.sub(pattern, LOAD_METHOD_TEMPLATE + r'\1', content, count=1)
        print(f"  ✅ {organ_name}: Added _load_shared_meta_atoms() method")

    # Step 3: Add _activate_meta_atoms() call in _compute_atom_activations before return
    if 'self._activate_meta_atoms' not in content:
        # Find return atom_activations and add meta-atom call before it
        pattern = r'(\n        return atom_activations)'
        replacement = r'\n        # 🆕 PHASE 2: Add meta-atom activations\n        if self.meta_atoms_config:\n            meta_activations = self._activate_meta_atoms(patterns, coherence, lure)\n            atom_activations.update(meta_activations)\1'
        content = re.sub(pattern, replacement, content, count=1)
        print(f"  ✅ {organ_name}: Added meta-atom call")

    # Step 4: Add _activate_meta_atoms() method after _compute_atom_activations
    if 'def _activate_meta_atoms' not in content:
        # Find the end of _compute_atom_activations and add method after
        pattern = r'(def _compute_atom_activations.*?return atom_activations\n)'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, r'\1' + ACTIVATE_METHOD_TEMPLATE, content, count=1)
            print(f"  ✅ {organ_name}: Added _activate_meta_atoms() method")

    # Write back
    with open(file_path, 'w') as f:
        f.write(content)

    return True

print("🔧 Batch adding meta-atom support to 7 remaining organs...")
print("="*70)

success_count = 0
for organ_name, organ_info in ORGANS.items():
    print(f"\n{organ_name} ({len(organ_info['meta_atoms'])} meta-atoms):")
    if add_meta_atoms_to_organ(organ_name, organ_info):
        success_count += 1

print("\n" + "="*70)
print(f"✅ Successfully added meta-atoms to {success_count}/{len(ORGANS)} organs")
print("\n📋 Next: Run test to validate all 11 organs!")
