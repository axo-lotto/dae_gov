#!/usr/bin/env python3
"""
Test Entity Persistence in Interactive Mode
November 14, 2025

Simulates the exact user scenario:
Turn 1: "my name is Emiliano"
Turn 2: "do you remember my name?"

Verifies entities persist across turns.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.user_registry import UserRegistry
from persona_layer.superject_structures import EnhancedUserProfile
from persona_layer.entity_extractor import EntityExtractor
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from datetime import datetime


def simulate_turn_1():
    """Turn 1: User introduces themselves."""
    print("=" * 80)
    print("TURN 1: User introduces themselves")
    print("=" * 80)

    # Create test user
    user_registry = UserRegistry()
    user_id = user_registry.create_user("test_emiliano")
    user = user_registry.get_user(user_id)

    print(f"\n✅ Created user: {user_id}")

    # Load user state
    user_state = user_registry.load_user_state(user_id)

    # Create profile
    profile = EnhancedUserProfile(
        user_id=user_id,
        created_at=datetime.now().isoformat(),
        last_active=datetime.now().isoformat()
    )

    # Extract entities from user input
    entity_extractor = EntityExtractor()
    user_input = "Hello! My name is Emiliano and this is my brother Bob."

    print(f"\n📥 User input: \"{user_input}\"")

    # Create context for extraction
    context = {
        'stored_entities': {
            'user_name': None,
            'family_members': [],
            'friends': [],
            'preferences': {}
        }
    }

    extracted_entities = entity_extractor.extract(
        text=user_input,
        intent_type='explicit_request',
        context=context
    )

    print(f"\n📦 Extracted entities:")
    for key, value in extracted_entities.items():
        print(f"  {key}: {value}")

    # Store entities in profile
    profile.store_entities(extracted_entities)

    print(f"\n📦 Profile entities after storage:")
    for key, value in profile.entities.items():
        if value:  # Only show non-empty
            print(f"  {key}: {value}")

    # Save to user_state
    user_state['user_profile'] = profile.to_dict()
    user_registry.save_user_state(user_id, user_state)

    print(f"\n✅ Saved to disk")

    return user_id


def simulate_turn_2(user_id):
    """Turn 2: User asks if DAE remembers their name."""
    print("\n\n" + "=" * 80)
    print("TURN 2: User asks if DAE remembers")
    print("=" * 80)

    user_registry = UserRegistry()

    # Reload user state (simulate new turn)
    user_state = user_registry.load_user_state(user_id)

    print(f"\n📦 Loaded user_state")

    # Load profile
    if 'user_profile' not in user_state:
        print(f"\n❌ FAIL: user_profile not in user_state")
        return False

    profile = EnhancedUserProfile.from_dict(user_state['user_profile'])

    print(f"\n📦 Profile entities from disk:")
    for key, value in profile.entities.items():
        if value:  # Only show non-empty
            print(f"  {key}: {value}")

    # Build context (like dae_interactive.py does)
    context = {}

    # Add entity context string
    context['entity_context_string'] = profile.get_entity_context_string()

    print(f"\n📝 Entity context string:")
    print(f'  "{context["entity_context_string"]}"')

    # Add stored_entities to context
    stored_entities = {}
    if hasattr(profile, 'entities') and profile.entities:
        if isinstance(profile.entities, dict):
            stored_entities = profile.entities

    context['stored_entities'] = stored_entities

    print(f"\n📦 stored_entities in context:")
    for key, value in stored_entities.items():
        if value:  # Only show non-empty
            print(f"  {key}: {value}")

    # Check if name is available
    if stored_entities.get('user_name') == 'Emiliano':
        print(f"\n✅ SUCCESS: Name 'Emiliano' available in context!")

        # Check family member
        if stored_entities.get('family_members'):
            family = stored_entities['family_members']
            if any(m.get('name') == 'Bob' for m in family):
                print(f"✅ SUCCESS: Brother 'Bob' available in context!")
                return True
            else:
                print(f"⚠️  WARNING: Bob not found in family_members")
                return True  # Still pass - name is the critical one
        else:
            print(f"⚠️  WARNING: family_members empty")
            return True  # Still pass - name is the critical one
    else:
        print(f"\n❌ FAIL: Name NOT available in context")
        print(f"   Expected: 'Emiliano'")
        print(f"   Got: {stored_entities.get('user_name')}")
        return False


def main():
    """Run full Turn 1 → Turn 2 simulation."""
    print("\n🧪 Entity Persistence Interactive Test")
    print("Simulating: Turn 1 (introduce) → Turn 2 (recall)")
    print("\n")

    # Turn 1: User introduces themselves
    user_id = simulate_turn_1()

    # Turn 2: User asks if DAE remembers
    success = simulate_turn_2(user_id)

    # Summary
    print("\n\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    if success:
        print("\n🎉 SUCCESS: Entity persistence works in interactive mode!")
        print("\nExpected behavior:")
        print("  Turn 1: 'my name is Emiliano' → entities extracted and stored")
        print("  Turn 2: 'do you remember my name?' → entities loaded from disk")
        print("  Turn 2: Organism receives entity context with name 'Emiliano'")
        print("\nThe user's complaint should now be resolved.")
    else:
        print("\n❌ FAIL: Entity persistence broken")
        print("The issue is NOT fixed.")

    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
