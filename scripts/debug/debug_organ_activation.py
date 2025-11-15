#!/usr/bin/env python3
"""Debug organ activation and nexus formation."""
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

organism = ConversationalOrganismWrapper()

test_inputs = [
    "I'm feeling overwhelmed and scared",  # Emotional
    "The time complexity is O(n log n)",   # Technical
    "I need some space right now",          # Moderate
]

for text in test_inputs:
    print(f"\n{'='*80}")
    print(f"Input: {text}")
    print('='*80)

    result = organism.process_text(text, enable_phase2=True, enable_tsk_recording=False)
    organ_results = result.get('organ_results', {})

    print("\n🧬 Organ Activations:")
    for organ_name, organ_result in organ_results.items():
        coherence = getattr(organ_result, 'coherence', 0.0)
        attention = getattr(organ_result, 'attention_score', 0.0)
        print(f"   {organ_name:15s}: coherence={coherence:.3f}, attention={attention:.3f}")

    felt_states = result.get('felt_states', {})
    v0_energy = felt_states.get('v0_energy', {})
    print(f"\n📊 System State:")
    print(f"   Nexuses formed: {result.get('emission_nexus_count', 0)}")
    print(f"   V0 final energy: {v0_energy.get('final_energy', 'N/A')}")
    print(f"   Emission confidence: {result.get('emission_confidence', 0.0):.3f}")
    print(f"   Emission path: {result.get('emission_path', 'unknown')}")
