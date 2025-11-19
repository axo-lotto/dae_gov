"""
Test Entity Extraction Debug - Reproduce Real Session Flow
===========================================================

Reproduces the exact scenario from user's interactive session log:
- User "Xeno" with 7 sessions, 37 turns
- Says "hello there! remember me?"
- Entity extraction should run but doesn't

Date: November 18, 2025
"""

import os
import sys

# Ensure PYTHONPATH is set
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')
os.environ['PYTHONPATH'] = '/Users/daedalea/Desktop/DAE_HYPHAE_1'

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_entity_extraction_flow():
    """Test the exact flow from user's session log."""

    print("=" * 80)
    print("🧪 TESTING ENTITY EXTRACTION DEBUG FLOW")
    print("=" * 80)

    # Initialize organism (same as interactive mode)
    print("\n1️⃣  Initializing organism...")
    organism = ConversationalOrganismWrapper()

    # Simulate user "Xeno" (using a test user_id)
    user_id = "user_20251118_test_xeno"
    user_input = "hello there! remember me?"

    print(f"\n2️⃣  Processing input from user '{user_id}':")
    print(f"   Input: '{user_input}'")
    print(f"\n" + "=" * 80)

    # Process the input (this should trigger entity extraction)
    result = organism.process_text(
        text=user_input,
        user_id=user_id,
        user_satisfaction=None  # Not providing satisfaction (like first turn)
    )

    print("\n" + "=" * 80)
    print(f"3️⃣  RESULT:")
    print(f"   Emission: {result.get('emission', 'NO EMISSION')}")
    print(f"   Confidence: {result.get('confidence', 'NO CONFIDENCE')}")

    # Check if entity extraction ran
    print(f"\n4️⃣  VALIDATION:")
    entity_prehension = result.get('entity_prehension')
    if entity_prehension:
        print(f"   ✅ Entity prehension result exists")
        print(f"   entity_memory_available: {entity_prehension.get('entity_memory_available')}")
        print(f"   mentioned_entities: {len(entity_prehension.get('mentioned_entities', []))}")
    else:
        print(f"   ❌ No entity prehension result")

    print("\n" + "=" * 80)
    print("✅ Test complete - check debug output above")
    print("=" * 80)


if __name__ == "__main__":
    test_entity_extraction_flow()
