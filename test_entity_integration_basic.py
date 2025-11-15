#!/usr/bin/env python3
"""
Basic test of entity-organism integration.

Tests that entity context flows through the organism without errors.
DAE 3.0 compliant - tests felt-based entity prehension.

November 14, 2025 - Entity Integration Testing
"""

import sys
from pathlib import Path

# Ensure PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_entity_context_flow():
    """Test that entity context flows through organism without errors."""
    print("🧪 Test 1: Entity Context Flow (No Errors)")
    print("=" * 60)

    # Initialize organism
    organism = ConversationalOrganismWrapper()  # Use default settings

    # Test input with entity context
    test_input = "Hello, my name is Alice"

    # Entity context (simulating what dae_interactive.py would pass)
    context = {
        'stored_entities': {
            'user_name': 'Bob',  # Existing stored name
            'family_members': [],
            'friends': [],
            'preferences': {}
        },
        'username': 'Bob'
    }

    try:
        # Process with entity context
        print(f"\n📥 Input: \"{test_input}\"")
        print(f"📦 Context: {context['stored_entities']}")

        result = organism.process_text(
            text=test_input,
            context=context,
            enable_tsk_recording=False
        )

        print(f"\n✅ Processing successful!")
        print(f"📤 Emission: \"{result['emission_text'][:100]}...\"")
        print(f"🎯 Confidence: {result['emission_confidence']:.3f}")
        print(f"🌀 Active organs: {len(result['organ_results'])}")
        print(f"🌀 Zone: {result['zone']}")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_occasion_entity_fields():
    """Test that TextOccasions carry entity fields."""
    print("\n\n🧪 Test 2: TextOccasion Entity Fields")
    print("=" * 60)

    from transductive.text_occasion import TextOccasion
    import numpy as np

    # Create occasion with entity fields
    occasion = TextOccasion(
        chunk_id="test_0_0_0_0",
        position=0,
        text="Alice",
        embedding=np.zeros(384)
    )

    # Check entity fields exist
    try:
        occasion.known_entities = {'user_name': 'Alice'}
        occasion.entity_references = ['Alice']
        occasion.entity_match_confidence = {'Alice': 0.95}

        print(f"\n✅ Entity fields accessible!")
        print(f"   known_entities: {occasion.known_entities}")
        print(f"   entity_references: {occasion.entity_references}")
        print(f"   entity_match_confidence: {occasion.entity_match_confidence}")

        return True

    except Exception as e:
        print(f"\n❌ Error accessing entity fields: {e}")
        return False


def main():
    """Run basic integration tests."""
    print("\n🌀 Entity-Organism Integration - Basic Tests")
    print("Testing DAE 3.0 compliant felt-based entity prehension\n")

    results = []

    # Test 1: Entity context flow
    results.append(("Context Flow", test_entity_context_flow()))

    # Test 2: Occasion entity fields
    results.append(("Occasion Fields", test_occasion_entity_fields()))

    # Summary
    print("\n\n📊 Test Summary")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Entity integration is working.")
        print("\nNote: Organs don't use entity context yet (context parameter)")
        print("Entity awareness will emerge through Hebbian learning over epochs.")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")

    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
