"""
Quick Test: Verify Felt-Guided LLM Natural Language Output
===========================================================

Simple test to verify Phase 1 is working with natural language.
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("="*80)
print("QUICK TEST: Felt-Guided LLM Natural Language")
print("="*80)

# Initialize organism
organism = ConversationalOrganismWrapper(bundle_path="Bundle/quick_test")

# Test inputs
test_inputs = [
    "Hello there i am feeling good today!",
    "I'm feeling overwhelmed and anxious",
    "Tell me about your day"
]

for i, user_input in enumerate(test_inputs, 1):
    print(f"\n{'='*80}")
    print(f"Test {i}: '{user_input}'")
    print("="*80)

    result = organism.process_text(user_input)

    # Try different keys to find the emission
    possible_keys = ['emission', 'emission_text', 'llm_response', 'response', 'text']

    print(f"\nResult keys: {list(result.keys())}")

    emission = None
    for key in possible_keys:
        if key in result and result[key]:
            emission = result[key]
            print(f"\nFound emission at key '{key}':")
            print(f"   '{emission}'")
            break

    if not emission:
        print("\n⚠️  No emission found in result")
        print("Full result:")
        for k, v in result.items():
            if isinstance(v, str) and len(v) < 200:
                print(f"   {k}: {v}")

print(f"\n{'='*80}")
print("Test Complete!")
print("="*80)
