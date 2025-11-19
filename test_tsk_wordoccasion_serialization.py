"""
Test TSK WordOccasion Serialization Fix
=========================================

Validates that WordOccasion objects can be serialized by TSK recorder.

Date: November 19, 2025
"""

import sys
from pathlib import Path
import json

# Add parent to path
sys.path.append(str(Path(__file__).parent))

from persona_layer.tsk_serialization_helper import tsk_to_dict_recursive, validate_json_serializable
from transductive.word_occasion import WordOccasion, create_word_occasions_from_text


def test_wordoccasion_serialization():
    """Test that WordOccasion objects can be serialized."""
    print("\n" + "="*80)
    print("🧪 TSK WORDOCCASION SERIALIZATION TEST")
    print("="*80)

    # Create some WordOccasions
    print("\n1. Creating WordOccasions from text...")
    test_text = "Today Emma went to work"
    word_occasions = create_word_occasions_from_text(test_text, neighbor_window_size=3)
    print(f"   Created {len(word_occasions)} WordOccasions")

    # Create a mock result dict (simulating process_text return)
    print("\n2. Creating mock result dict with WordOccasions...")
    result = {
        'felt_states': {
            'emission_text': 'Test response',
            'emission_confidence': 0.7
        },
        'context': {
            'word_occasions': word_occasions,  # This is what causes the error
            'nexus_entities': [
                {'entity_value': 'Emma', 'entity_type': 'Person'}
            ]
        }
    }
    print(f"   Result dict contains {len(word_occasions)} WordOccasions in context")

    # Test validation BEFORE conversion (should find WordOccasions)
    print("\n3. Validating BEFORE conversion...")
    errors_before = validate_json_serializable(result)
    if errors_before:
        print(f"   ⚠️  Found {len(errors_before)} non-serializable objects:")
        for error in errors_before[:5]:  # Show first 5
            print(f"      - {error}")
    else:
        print(f"   ❌ Expected to find WordOccasion errors, but found none!")

    # Convert using tsk_to_dict_recursive
    print("\n4. Converting with tsk_to_dict_recursive...")
    result_converted = tsk_to_dict_recursive(result)
    print(f"   Conversion complete")

    # Test validation AFTER conversion (should be clean)
    print("\n5. Validating AFTER conversion...")
    errors_after = validate_json_serializable(result_converted)
    if errors_after:
        print(f"   ❌ Still found {len(errors_after)} non-serializable objects:")
        for error in errors_after[:5]:
            print(f"      - {error}")
        return False
    else:
        print(f"   ✅ All objects are JSON-serializable!")

    # Test actual JSON serialization
    print("\n6. Testing actual JSON serialization...")
    try:
        json_str = json.dumps(result_converted, indent=2)
        print(f"   ✅ JSON serialization successful ({len(json_str)} chars)")

        # Show sample of serialized WordOccasion
        word_occasions_serialized = result_converted['context']['word_occasions']
        if word_occasions_serialized:
            print(f"\n   Sample serialized WordOccasion:")
            sample = word_occasions_serialized[1]  # "Emma"
            print(f"      word: {sample.get('word')}")
            print(f"      position: {sample.get('position')}")
            print(f"      entity_type: {sample.get('entity_type')}")
            print(f"      entity_confidence: {sample.get('entity_confidence')}")

    except Exception as e:
        print(f"   ❌ JSON serialization failed: {e}")
        return False

    print("\n" + "="*80)
    print("✅ TSK WORDOCCASION SERIALIZATION TEST PASSED")
    print("="*80)

    return True


if __name__ == "__main__":
    success = test_wordoccasion_serialization()
    sys.exit(0 if success else 1)
