#!/usr/bin/env python3
"""
Debug Entity Flow for User "Emi"
November 14, 2025

Check every step of the entity persistence flow.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.user_registry import UserRegistry
from persona_layer.superject_structures import EnhancedUserProfile
from persona_layer.entity_extractor import EntityExtractor

def main():
    print("=" * 80)
    print("🔍 ENTITY FLOW DEBUG - User 'Emi'")
    print("=" * 80)

    user_registry = UserRegistry()
    user_id = 'user_20251113_143117'  # User "Emi"

    print(f"\n1. Loading user state...")
    user_state = user_registry.load_user_state(user_id)
    print(f"   ✅ User state loaded")

    print(f"\n2. Loading user profile...")
    if 'user_profile' in user_state:
        profile = EnhancedUserProfile.from_dict(user_state['user_profile'])
        print(f"   ✅ Profile loaded")
        print(f"   Profile entities: {profile.entities}")
    else:
        print(f"   ❌ NO user_profile in user_state!")
        profile = None

    print(f"\n3. Generate entity context string...")
    if profile:
        entity_context_string = profile.get_entity_context_string()
        print(f"   Entity context string:")
        print(f"   '{entity_context_string}'")
    else:
        entity_context_string = ""

    print(f"\n4. Test entity extraction on sample input...")
    entity_extractor = EntityExtractor()

    test_inputs = [
        "Hello there! my name is emiliano, it is very nice to meet you",
        "my name is Emiliano",
        "Hello! My name is Emiliano.",
    ]

    for test_input in test_inputs:
        print(f"\n   Input: '{test_input}'")
        context = {
            'stored_entities': profile.entities if profile else {}
        }
        extracted = entity_extractor.extract(test_input, 'explicit_request', context)
        print(f"   Extracted: {extracted}")

        # Check if user_name found
        if 'user_name' in extracted and extracted['user_name']:
            print(f"   ✅ Name extracted: '{extracted['user_name']}'")
        else:
            print(f"   ❌ NO name extracted!")

    print(f"\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if profile and profile.entities.get('user_name'):
        print(f"✅ Name stored in profile: '{profile.entities['user_name']}'")
    else:
        print(f"❌ Name NOT stored in profile")

    if entity_context_string:
        print(f"✅ Entity context string generated: '{entity_context_string}'")
    else:
        print(f"❌ Entity context string EMPTY")

if __name__ == '__main__':
    main()
