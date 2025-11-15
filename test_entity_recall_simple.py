#!/usr/bin/env python3
"""
Simple Entity Recall Test
November 14, 2025

Quick test to verify entity context is passed to LLM.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def main():
    print("=" * 80)
    print("🧪 SIMPLE ENTITY RECALL TEST")
    print("=" * 80)

    organism = ConversationalOrganismWrapper()

    # Test case: User asks to recall their name
    test_input = "do you remember my name?"

    # Build context with entity information (simulating dae_interactive behavior)
    context = {
        'user_id': 'test_user',
        'username': 'TestUser',
        'stored_entities': {
            'user_name': 'Emiliano'
        },
        'entity_context_string': "Known information:\n- User's name: Emiliano",
        'memory_intent': True
    }

    print(f"\n📝 Input: \"{test_input}\"")
    print(f"\n📦 Context:")
    print(f"   entity_context_string: \"{context['entity_context_string']}\"")
    print(f"   memory_intent: {context['memory_intent']}")

    print(f"\n🌀 Processing...")

    # Process
    try:
        response = organism.process_text(test_input, context=context)

        # Extract emission text from response (can be dict or string)
        if isinstance(response, dict):
            emission_text = response.get('emission_text', str(response))
        else:
            emission_text = str(response)

        print(f"\n💬 Response: \"{emission_text}\"")

        # Check if name is mentioned
        if 'emiliano' in emission_text.lower():
            print(f"\n✅ SUCCESS - Name 'Emiliano' found in response!")
            print(f"\n🎉 Entity recall is WORKING!")
            return True
        else:
            print(f"\n❌ FAIL - Name 'Emiliano' NOT found in response")
            print(f"\n⚠️  Entity recall still NOT working")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
