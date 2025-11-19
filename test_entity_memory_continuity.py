"""
Test Entity Memory Continuity - Cross-Session Memory Availability
==================================================================

Validates that entity memory is ALWAYS available when users have stored entities,
ensuring cross-session continuity for companion intelligence.

Date: November 18, 2025
"""

import os
import sys
import json

# Ensure PYTHONPATH is set
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')
os.environ['PYTHONPATH'] = '/Users/daedalea/Desktop/DAE_HYPHAE_1'

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_entity_memory_continuity():
    """
    Test cross-session entity memory availability.

    Scenario:
    - Turn 1: User introduces themselves ("My name is Xeno")
    - Turn 2: User asks relational query ("remember me?")
    - Expected: entity_memory_available = True on BOTH turns
    """

    print("=" * 80)
    print("🧪 TESTING CROSS-SESSION ENTITY MEMORY CONTINUITY")
    print("=" * 80)

    # Initialize organism
    print("\n1️⃣  Initializing organism...")
    organism = ConversationalOrganismWrapper()

    user_id = "user_20251118_continuity_test"

    # Clean slate - remove any existing profile
    profile_path = f"persona_layer/users/{user_id}_superject.json"
    if os.path.exists(profile_path):
        os.remove(profile_path)
        print(f"   Removed existing profile for clean test")

    print(f"\n{'=' * 80}")
    print(f"TURN 1: User introduces themselves")
    print(f"{'=' * 80}\n")

    # TURN 1: User introduces name
    turn1_input = "My name is Xeno"
    print(f"   User: '{turn1_input}'\n")

    result1 = organism.process_text(
        text=turn1_input,
        user_id=user_id,
        user_satisfaction=None
    )

    # Check entity extraction happened
    entity_prehension1 = result1.get('entity_prehension', {})
    print(f"\n   ✅ Turn 1 Results:")
    print(f"      entity_memory_available: {entity_prehension1.get('entity_memory_available')}")
    print(f"      mentioned_entities count: {len(entity_prehension1.get('mentioned_entities', []))}")

    # Load profile to verify entity was stored
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            profile = json.load(f)
            print(f"      ✅ Profile created with entities: {list(profile.get('entities', {}).keys())}")
            if 'user_name' in profile.get('entities', {}):
                print(f"      ✅ User name stored: {profile['entities']['user_name']}")

    print(f"\n{'=' * 80}")
    print(f"TURN 2: User asks relational query (cross-session continuity test)")
    print(f"{'=' * 80}\n")

    # TURN 2: User asks "remember me?" (relational query, no new entities)
    turn2_input = "hello there! remember me?"
    print(f"   User: '{turn2_input}'\n")

    result2 = organism.process_text(
        text=turn2_input,
        user_id=user_id,
        user_satisfaction=None
    )

    # Check entity memory availability
    entity_prehension2 = result2.get('entity_prehension', {})
    print(f"\n   ✅ Turn 2 Results:")
    print(f"      entity_memory_available: {entity_prehension2.get('entity_memory_available')}")
    print(f"      mentioned_entities count: {len(entity_prehension2.get('mentioned_entities', []))}")

    print(f"\n{'=' * 80}")
    print(f"VALIDATION")
    print(f"{'=' * 80}\n")

    # Validate results
    turn1_memory_available = entity_prehension1.get('entity_memory_available', False)
    turn2_memory_available = entity_prehension2.get('entity_memory_available', False)

    print(f"   Turn 1 (entity introduction):")
    print(f"      entity_memory_available = {turn1_memory_available}")
    if turn1_memory_available:
        print(f"      ✅ PASS - Memory available after extraction")
    else:
        print(f"      ⚠️  WARN - Memory should be available after extraction")

    print(f"\n   Turn 2 (relational query):")
    print(f"      entity_memory_available = {turn2_memory_available}")
    if turn2_memory_available:
        print(f"      ✅ PASS - Cross-session continuity WORKING!")
        print(f"      🌀 Stored entities available as context without explicit mention")
    else:
        print(f"      ❌ FAIL - Cross-session continuity BROKEN!")
        print(f"      🚨 User has stored entities but memory not available")

    # Overall assessment
    print(f"\n{'=' * 80}")
    if turn1_memory_available and turn2_memory_available:
        print(f"✅ CROSS-SESSION CONTINUITY: COMPLETE")
        print(f"   Entity memory persists across turns as CONTEXT")
        print(f"   Companion intelligence can reference stored entities")
    else:
        print(f"❌ CROSS-SESSION CONTINUITY: INCOMPLETE")
        print(f"   Fix required in entity prehension logic")
    print(f"{'=' * 80}\n")

    # Cleanup
    if os.path.exists(profile_path):
        os.remove(profile_path)
        print(f"   Cleaned up test profile\n")


if __name__ == "__main__":
    test_entity_memory_continuity()
