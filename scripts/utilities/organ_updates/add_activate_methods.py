"""Add _activate_meta_atoms method to all organs that need it."""

METHOD = '''
    def _activate_meta_atoms(self, patterns, coherence, lure) -> Dict[str, float]:
        """🆕 PHASE 2: Activate shared meta-atoms (simple coherence-based)."""
        if not self.meta_atoms_config or not patterns:
            return {}
        meta_activations = {}
        # Simple activation: If patterns detected and coherence > 0.5, activate all meta-atoms
        if coherence > 0.5:
            for meta_atom in self.meta_atoms_config['meta_atoms']:
                activation = coherence * (0.5 + 0.5 * lure)
                meta_activations[meta_atom['atom']] = min(1.0, activation)
        return meta_activations
'''

organs = ['empathy', 'listening', 'wisdom', 'authenticity', 'presence', 'rnx', 'card']

for organ in organs:
    file_path = f"organs/modular/{organ}/core/{organ}_text_core.py"

    with open(file_path, 'r') as f:
        content = f.read()

    # Add method after _compute_atom_activations if not already present
    if 'def _activate_meta_atoms' not in content:
        # Find the end of _compute_atom_activations (look for "return atom_activations" followed by next method or class end)
        import re
        # Insert after the method that contains "return atom_activations"
        pattern = r'(def _compute_atom_activations.*?return atom_activations\n)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + METHOD + content[insert_pos:]

            with open(file_path, 'w') as f:
                f.write(content)

            print(f"✅ Added _activate_meta_atoms() to {organ.upper()}")
        else:
            print(f"❌ Could not find insertion point in {organ.upper()}")
    else:
        print(f"⏭️  {organ.upper()} already has method")

print("\n✅ All organs now have _activate_meta_atoms() method!")
