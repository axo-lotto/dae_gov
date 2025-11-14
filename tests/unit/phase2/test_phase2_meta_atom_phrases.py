"""Test Phase 2 with meta-atom phrase library integration."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\n" + "="*70)
print("🌀 PHASE 2: META-ATOM PHRASE LIBRARY TEST")
print("="*70 + "\n")

wrapper = ConversationalOrganismWrapper()

# Test cases with different emotional tones
test_cases = [
    {
        'name': 'Trauma Awareness',
        'text': "I hear your exhaustion and burnout. You're completely depleted. This isn't sustainable.",
        'expected_meta_atoms': ['trauma_aware', 'temporal_grounding']
    },
    {
        'name': 'Safety Restoration',
        'text': "Take a breath. Let's slow down together. There's space here for you.",
        'expected_meta_atoms': ['safety_restoration', 'relational_attunement', 'temporal_grounding']
    },
    {
        'name': 'Compassion & Presence',
        'text': "I'm with you. What you're feeling matters. Your experience is real and valid.",
        'expected_meta_atoms': ['compassion_safety', 'relational_attunement']
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'='*70}")
    print(f"TEST {i}: {test_case['name']}")
    print(f"{'='*70}")
    print(f"\n📝 Input: \"{test_case['text']}\"")

    result = wrapper.process_text(
        test_case['text'],
        {},
        enable_tsk_recording=False,
        enable_phase2=True
    )

    # Extract results
    nexus_count = result['felt_states'].get('emission_nexus_count', 0)
    emission_text = result['felt_states'].get('emission_text', '')
    emission_confidence = result['felt_states'].get('emission_confidence', 0.0)
    emission_path = result['felt_states'].get('emission_path', 'none')
    v0_energy = result['felt_states']['v0_energy']['final_energy']
    cycles = result['felt_states']['convergence_cycles']

    # Determine V0 intensity
    if v0_energy > 0.7:
        intensity = 'high'
    elif v0_energy < 0.3:
        intensity = 'low'
    else:
        intensity = 'medium'

    print(f"\n🌀 CONVERGENCE:")
    print(f"   Cycles: {cycles}")
    print(f"   V0 energy: {v0_energy:.3f} (intensity: {intensity})")
    print(f"   Nexuses: {nexus_count}")

    print(f"\n💬 EMISSION:")
    if emission_text:
        print(f"   Text: \"{emission_text}\"")
    else:
        print(f"   Text: [None generated]")
    print(f"   Confidence: {emission_confidence:.3f}")
    print(f"   Path: {emission_path}")

    # Check which meta-atoms activated
    print(f"\n🌀 META-ATOMS ACTIVATED:")
    meta_atom_names = {
        'trauma_aware', 'safety_restoration', 'window_of_tolerance',
        'compassion_safety', 'fierce_holding', 'relational_attunement',
        'temporal_grounding', 'kairos_emergence', 'coherence_integration',
        'somatic_wisdom'
    }

    activated_meta_atoms = []
    for organ_name, organ_result in result['organ_results'].items():
        activations = getattr(organ_result, 'atom_activations', {})
        for atom, value in activations.items():
            if atom in meta_atom_names and value > 0.05:
                activated_meta_atoms.append((atom, organ_name, value))

    if activated_meta_atoms:
        for atom, organ, value in sorted(activated_meta_atoms, key=lambda x: x[2], reverse=True):
            print(f"   ✓ {atom}: {value:.3f} ({organ})")
    else:
        print(f"   ⚠️ No meta-atoms activated")

    # Success criteria
    success = nexus_count >= 1 and emission_confidence > 0.40
    if success:
        print(f"\n✅ TEST PASSED: {nexus_count} nexuses, confidence {emission_confidence:.3f}")
    else:
        print(f"\n⚠️ TEST NEEDS TUNING: {nexus_count} nexuses, confidence {emission_confidence:.3f}")

print("\n" + "="*70)
print("🌀 ALL TESTS COMPLETE")
print("="*70 + "\n")
