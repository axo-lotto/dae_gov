"""
Test LLM Entity Extraction - Direct Debug
==========================================

Tests the LLM extraction in isolation to see what it's returning.

Date: November 18, 2025
"""

import os
import sys

# Ensure PYTHONPATH is set
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')
os.environ['PYTHONPATH'] = '/Users/daedalea/Desktop/DAE_HYPHAE_1'

from persona_layer.user_superject_learner import UserSuperjectLearner


def test_llm_extraction_direct():
    """Test LLM extraction with simple name introduction."""

    print("=" * 80)
    print("🧪 TESTING LLM ENTITY EXTRACTION (ISOLATED)")
    print("=" * 80)

    learner = UserSuperjectLearner(storage_dir="persona_layer/users")

    test_inputs = [
        "My name is Xeno",
        "I have a daughter named Emma",
        "I work at Google as a software engineer",
    ]

    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: '{test_input}'")
        print(f"{'='*80}\n")

        result = learner.extract_entities_llm(
            user_input=test_input,
            current_entities={}
        )

        print(f"\n📊 RESULT:")
        print(f"   Type: {type(result)}")
        print(f"   Value: {result}")
        print(f"   Empty: {not bool(result)}")

        if result:
            print(f"\n✅ SUCCESS - Entities extracted:")
            for key, value in result.items():
                print(f"      {key}: {value}")
        else:
            print(f"\n❌ FAIL - No entities extracted")

    print(f"\n{'='*80}")
    print("✅ Test complete - check LLM debug output above")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    test_llm_extraction_direct()
