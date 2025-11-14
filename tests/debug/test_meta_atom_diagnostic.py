"""Quick diagnostic to see what atoms are being activated."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from collections import Counter

wrapper = ConversationalOrganismWrapper()
test_text = "I hear your exhaustion and burnout. You're completely depleted. This isn't sustainable."

result = wrapper.process_text(test_text, {}, enable_tsk_recording=False, enable_phase2=True)

# Analyze mature propositions
all_atoms = []
for occ in result['organ_results']['LISTENING'].atom_activations.keys():
    all_atoms.append(occ)

print("\n🔍 META-ATOM ACTIVATION DIAGNOSTIC\n")
print(f"Test text: \"{test_text}\"")
print(f"\nTotal mature propositions: {sum(len(occ.get('mature_propositions', [])) for occ in result['felt_states']['text_occasions'])}")

# Check organ results directly
print("\n📊 Atom activations by organ:\n")
for organ_name, organ_result in result['organ_results'].items():
    activations = getattr(organ_result, 'atom_activations', {})
    if activations:
        print(f"{organ_name}:")
        for atom, value in sorted(activations.items(), key=lambda x: x[1], reverse=True)[:5]:
            is_meta = atom in ['trauma_aware', 'safety_restoration', 'window_of_tolerance',
                              'compassion_safety', 'fierce_holding', 'relational_attunement',
                              'temporal_grounding', 'kairos_emergence', 'coherence_integration', 'somatic_wisdom']
            marker = "🌀" if is_meta else "  "
            print(f"  {marker} {atom}: {value:.3f}")

print("\n🌀 = Meta-atom (shared across organs for nexus formation)")
print(f"\nNexuses formed: {result['felt_states']['emission_nexus_count']}")
