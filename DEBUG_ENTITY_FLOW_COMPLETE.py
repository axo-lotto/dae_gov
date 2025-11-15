#!/usr/bin/env python3
"""
DEBUG Entity Flow - Complete Trace
November 14, 2025

Traces entity flow from storage → organism → reconstruction → LLM → response
with FULL DEBUG output at every step.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.user_registry import UserRegistry
from persona_layer.superject_structures import EnhancedUserProfile
import json

def main():
    print("\n" + "=" * 80)
    print("🔍 DEBUG ENTITY FLOW - COMPLETE TRACE")
    print("=" * 80)

    # Initialize system
    print("\n1️⃣ INITIALIZING ORGANISM...")
    organism = ConversationalOrganismWrapper()
    print("   ✅ Organism initialized")

    # Load user "Emi" state
    print("\n2️⃣ LOADING USER 'Emi' STATE...")
    user_registry = UserRegistry()
    user_id = 'user_20251113_143117'  # User "Emi"
    user_state = user_registry.load_user_state(user_id)
    print(f"   ✅ User state loaded")
    print(f"   User ID: {user_id}")

    # Load profile
    print("\n3️⃣ LOADING USER PROFILE...")
    if 'user_profile' in user_state:
        profile = EnhancedUserProfile.from_dict(user_state['user_profile'])
        print(f"   ✅ Profile loaded")
        print(f"   Profile entities: {json.dumps(profile.entities, indent=2)}")
    else:
        print(f"   ❌ NO PROFILE FOUND!")
        return False

    # Build entity context string (simulating dae_interactive.py)
    print("\n4️⃣ BUILDING ENTITY CONTEXT STRING...")
    entity_context_string = profile.get_entity_context_string()
    print(f"   Entity context string:")
    print(f"   '{entity_context_string}'")

    if not entity_context_string:
        print(f"   ⚠️  WARNING: Entity context string is EMPTY!")

    # Build context dict (exactly as dae_interactive.py does)
    print("\n5️⃣ BUILDING CONTEXT DICT...")
    context = {
        'user_id': user_id,
        'username': profile.entities.get('user_name', 'Unknown'),
        'stored_entities': profile.entities,
        'entity_context_string': entity_context_string,
        'memory_intent': True  # Explicitly set for memory query
    }
    print(f"   Context built:")
    print(f"   {json.dumps({k: v for k, v in context.items() if k != 'stored_entities'}, indent=2)}")
    print(f"   stored_entities: {context['stored_entities']}")

    # Test memory query
    print("\n6️⃣ PROCESSING MEMORY QUERY...")
    test_input = "do you remember my name?"
    print(f"   Input: \"{test_input}\"")

    print("\n7️⃣ CALLING ORGANISM.PROCESS_TEXT()...")
    print(f"   Passing context with:")
    print(f"   - user_id: {context['user_id']}")
    print(f"   - username: {context['username']}")
    print(f"   - entity_context_string: '{context['entity_context_string'][:50]}...'")
    print(f"   - memory_intent: {context['memory_intent']}")

    try:
        result = organism.process_text(test_input, context=context)

        print("\n8️⃣ ORGANISM PROCESSING COMPLETE")

        # Check if result is dict or string
        if isinstance(result, dict):
            emission_text = result.get('emission_text', str(result))
            felt_states = result.get('felt_states', {})

            print(f"   Result type: dict")
            print(f"   Emission text: \"{emission_text}\"")

            # Check felt_states for entity context
            if 'context' in felt_states:
                fs_context = felt_states['context']
                print(f"\n9️⃣ CHECKING FELT_STATES CONTEXT...")
                print(f"   Has entity_context_string: {'entity_context_string' in fs_context}")
                if 'entity_context_string' in fs_context:
                    print(f"   Value: '{fs_context['entity_context_string']}'")
                else:
                    print(f"   ❌ MISSING entity_context_string in felt_states!")
            else:
                print(f"\n❌ NO 'context' IN FELT_STATES!")
                print(f"   felt_states keys: {list(felt_states.keys())}")
        else:
            emission_text = str(result)
            print(f"   Result type: {type(result)}")
            print(f"   Emission: \"{emission_text}\"")

        # Final check
        print(f"\n🔟 FINAL VERIFICATION...")
        if 'emiliano' in emission_text.lower():
            print(f"   ✅ SUCCESS - Name 'Emiliano' found in response!")
            print(f"\n🎉 ENTITY RECALL IS WORKING!")
            return True
        else:
            print(f"   ❌ FAIL - Name 'Emiliano' NOT in response")
            print(f"   Response: \"{emission_text}\"")
            print(f"\n⚠️  ENTITY RECALL STILL NOT WORKING")

            # Debug info
            print(f"\n🔍 DEBUG INFO:")
            print(f"   Was entity_context_string passed to organism? YES")
            print(f"   Value: '{context['entity_context_string']}'")
            print(f"   Was it received by LLM? CHECKING...")

            return False

    except Exception as e:
        print(f"\n❌ ERROR during processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()

    print(f"\n" + "=" * 80)
    print(f"RESULT: {'✅ SUCCESS' if success else '❌ FAILURE'}")
    print(f"=" * 80 + "\n")

    sys.exit(0 if success else 1)
