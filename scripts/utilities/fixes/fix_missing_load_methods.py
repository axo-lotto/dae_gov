"""Add _load_shared_meta_atoms method to organs missing it."""

METHOD = '''    def _load_shared_meta_atoms(self) -> Optional[Dict]:
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

organs = ['empathy', 'wisdom', 'authenticity', 'presence', 'rnx', 'card']

for organ in organs:
    file_path = f"organs/modular/{organ}/core/{organ}_text_core.py"

    with open(file_path, 'r') as f:
        content = f.read()

    # Find "def _compute_atom_activations" and insert method before it
    if 'def _load_shared_meta_atoms' not in content:
        content = content.replace(
            '    def _compute_atom_activations(',
            METHOD + '    def _compute_atom_activations('
        )

        with open(file_path, 'w') as f:
            f.write(content)

        print(f"✅ Added _load_shared_meta_atoms() to {organ.upper()}")
    else:
        print(f"⏭️  {organ.upper()} already has method")

print("\n✅ All organs now have _load_shared_meta_atoms() method!")
