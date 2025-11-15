#!/usr/bin/env python3
"""
Complete Entity Recall Test - Both Emission Paths
November 14, 2025

Tests entity recall through:
1. Direct emission generator path
2. Reconstruction pipeline path

Verifies the fix is working end-to-end.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.user_registry import UserRegistry
from persona_layer.superject_structures import EnhancedUserProfile
import json

def test_entity_recall_both_paths():
    """Test entity recall through both emission paths"""

    print("=" * 80)
    print("🧪 COMPLETE ENTITY RECALL TEST - BOTH EMISSION PATHS")
    print("=" * 80)

    # Initialize system
    organism = ConversationalOrganismWrapper()
    user_registry = UserRegistry()

    # Create test user profile with name stored
    test_user_id = "test_entity_recall_user"
    test_profile = EnhancedUserProfile(
        user_id=test_user_id,
        created_at="2025-11-14T00:00:00",
        last_active="2025-11-14T00:00:00"
    )
    # Add entities manually (following correct structure)
    test_profile.entities = {
        'user_name': 'Emiliano',
        'family_members': [
            {'name': 'Charlie', 'relation': 'brother'}
        ],
        'preferences': {'favorite_color': 'blue'}
    }

    # Build entity context string (simulating dae_interactive.py behavior)
    entity_context_string = test_profile.get_entity_context_string()

    print(f"\n1. TEST SETUP")
    print(f"   User ID: {test_user_id}")
    print(f"   Stored entities: {test_profile.entities}")
    print(f"   Entity context string:")
    print(f"   '{entity_context_string}'")

    # Test inputs that should trigger entity recall
    test_cases = [
        {
            'input': "do you remember my name?",
            'expected_contains': ['emiliano', 'Emiliano'],
            'description': "Name recall test"
        },
        {
            'input': "what is my name?",
            'expected_contains': ['emiliano', 'Emiliano'],
            'description': "Direct name query"
        },
        {
            'input': "who is Charlie?",
            'expected_contains': ['brother', 'Charlie'],
            'description': "Family member recall"
        },
        {
            'input': "what's my favorite color?",
            'expected_contains': ['blue'],
            'description': "Preference recall"
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"TEST CASE {i}/{len(test_cases)}: {test_case['description']}")
        print(f"{'=' * 80}")
        print(f"Input: \"{test_case['input']}\"")

        # Build context with entity information
        context = {
            'user_id': test_user_id,
            'username': 'TestUser',
            'stored_entities': test_profile.entities,
            'entity_context_string': entity_context_string,
            'memory_intent': True  # Explicitly signal memory query
        }

        # Process through organism
        try:
            response = organism.process_text(test_case['input'], context=context)

            print(f"\n✅ Response generated:")
            print(f"   \"{response}\"")

            # Check if expected content is present
            response_lower = response.lower()
            found_matches = []
            for expected in test_case['expected_contains']:
                if expected.lower() in response_lower:
                    found_matches.append(expected)

            if found_matches:
                print(f"\n✅ PASS - Found expected content: {found_matches}")
                results.append({
                    'test': test_case['description'],
                    'status': 'PASS',
                    'response': response,
                    'matched': found_matches
                })
            else:
                print(f"\n❌ FAIL - Expected to find one of: {test_case['expected_contains']}")
                print(f"   But response was: \"{response}\"")
                results.append({
                    'test': test_case['description'],
                    'status': 'FAIL',
                    'response': response,
                    'expected': test_case['expected_contains']
                })

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append({
                'test': test_case['description'],
                'status': 'ERROR',
                'error': str(e)
            })

    # Summary
    print(f"\n{'=' * 80}")
    print("📊 TEST SUMMARY")
    print(f"{'=' * 80}")

    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] == 'ERROR')

    print(f"\nTotal Tests: {len(results)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"💥 Errors: {errors}")

    if passed == len(results):
        print(f"\n🎉 ALL TESTS PASSED - Entity recall working!")
    else:
        print(f"\n⚠️  SOME TESTS FAILED - Entity recall needs debugging")

    # Save detailed results
    results_file = Path('/tmp/entity_recall_test_results.json')
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': '2025-11-14',
            'summary': {
                'total': len(results),
                'passed': passed,
                'failed': failed,
                'errors': errors
            },
            'test_cases': results
        }, f, indent=2)

    print(f"\n📄 Detailed results saved to: {results_file}")

    return passed == len(results)

if __name__ == '__main__':
    success = test_entity_recall_both_paths()
    sys.exit(0 if success else 1)
