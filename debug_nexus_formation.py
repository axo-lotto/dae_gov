"""
Debug: Why aren't nexuses forming?
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("="*80)
print("DEBUG: Nexus Formation Issue")
print("="*80)

organism = ConversationalOrganismWrapper(bundle_path="Bundle/debug_nexus")

test_inputs = [
    "Hello there today is a beautiful day!",
    "Hello there i am feeling good today!",
    "I'm feeling overwhelmed and anxious"
]

for user_input in test_inputs:
    print(f"\n{'='*80}")
    print(f"Input: '{user_input}'")
    print("="*80)

    result = organism.process_text(user_input)

    nexus_count = result.get('emission_nexus_count', 0)
    confidence = result.get('emission_confidence', 0.0)
    path = result.get('emission_path', 'unknown')

    print(f"\n📊 Results:")
    print(f"   Nexuses formed: {nexus_count}")
    print(f"   Confidence: {confidence:.3f}")
    print(f"   Path: {path}")

    # Check organ results
    organ_results = result.get('organ_results', {})
    print(f"\n🧬 Organ Activations:")
    for organ_name, organ_result in organ_results.items():
        if hasattr(organ_result, 'coherence'):
            coherence = organ_result.coherence
            print(f"   {organ_name}: coherence={coherence:.3f}")

    # Check semantic fields
    if nexus_count == 0:
        print(f"\n⚠️  NO NEXUSES - Why?")
        print(f"   Check: Are semantic fields being created?")
        print(f"   Check: Are atoms shared between organs?")
        print(f"   Check: Is intersection threshold too high?")
