#!/usr/bin/env python3
"""
Test Pre-Emission Entity Prehension Integration
=================================================

Tests the critical fix for entity memory retrieval BEFORE organ activation.

This test simulates the exact scenario where the system failed:
- User: "do you remember my name and the nature of our relationship?"
- System: Zero nexuses formed, called user "an"

Expected behavior after fix:
- Entity memory retrieved BEFORE organ activation
- Relational query detected
- User name retrieved from profile
- Entity context enriches organ processing
- Entity Memory Nexus (EMN) can form

Date: November 16, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.pre_emission_entity_prehension import PreEmissionEntityPrehension
from persona_layer.user_superject_learner import UserSuperjectLearner
from persona_layer.superject_structures import create_default_profile


def main():
    print("\n" + "="*70)
    print("PRE-EMISSION ENTITY PREHENSION - INTEGRATION TEST")
    print("="*70 + "\n")

    # Test 1: Create a test user with entity memory
    print("TEST 1: Create test user with entity memory")
    print("-" * 50)

    learner = UserSuperjectLearner(storage_dir="persona_layer/users")
    test_user_id = "test_pre_emission_emiliano"

    # Create profile with entities (simulating Emiliano's profile)
    profile = learner.get_or_create_profile(test_user_id)

    # Add entity data
    test_entities = {
        'user_name': 'Emiliano',
        'user_role': 'researcher',
        'relationships': [
            {
                'name': 'Emma',
                'type': 'person',
                'relationship': 'daughter',
                'polyvagal_state': 'ventral_vagal',
                'safety_score': 0.95,
            },
            {
                'name': 'Lily',
                'type': 'person',
                'relationship': 'daughter',
                'polyvagal_state': 'ventral_vagal',
                'safety_score': 0.92,
            },
        ],
        'mentioned_names': ['Sarah', 'Michael', 'Dr. Chen'],
        'facts': ['Works on AI research', 'Interested in Whitehead'],
        'preferences': ['prefers morning meetings', 'likes detailed explanations'],
    }

    profile.store_entities(test_entities)
    learner.save_profile(profile)

    print(f"  ✅ Created user profile for: {test_user_id}")
    print(f"     User name: {profile.entities.get('user_name')}")
    print(f"     Relationships: {len(profile.entities.get('relationships', []))}")
    print(f"     Mentioned names: {len(profile.entities.get('mentioned_names', []))}")

    # Test 2: Pre-emission retrieval on relational query
    print("\nTEST 2: Pre-emission retrieval on relational query")
    print("-" * 50)

    prehension = PreEmissionEntityPrehension(storage_dir="persona_layer/users")

    # The EXACT query that failed
    failed_query = "do you remember my name and the nature of our relationship?"

    result = prehension.retrieve_relevant_entities(
        user_input=failed_query,
        user_id=test_user_id
    )

    print(f"  Query: '{failed_query}'")
    print(f"\n  Results:")
    print(f"    Entity memory available: {result['entity_memory_available']}")
    print(f"    Relational query detected: {result['relational_query_detected']}")
    print(f"    User name retrieved: {result['user_name']}")
    print(f"    Mentioned entities: {len(result['mentioned_entities'])}")
    print(f"    Implicit references: {len(result['implicit_references'])}")
    print(f"    Memory richness: {result['historical_context'].get('memory_richness', 0):.2f}")

    # Verify fix
    if result['relational_query_detected'] and result['user_name'] == 'Emiliano':
        print("\n  ✅ CRITICAL FIX VERIFIED: Entity memory available BEFORE organ activation!")
    else:
        print("\n  ❌ Fix incomplete: Entity memory not properly retrieved")

    # Test 3: Organ context enrichment
    print("\nTEST 3: Organ context enrichment")
    print("-" * 50)

    enrichment = prehension.inject_into_organ_context(result)

    print("  Organ boosts from entity context:")
    print(f"    LISTENING.relational_inquiry_boost: {enrichment['LISTENING']['relational_inquiry_boost']}")
    print(f"    EMPATHY.relational_attunement_boost: {enrichment['EMPATHY']['relational_attunement_boost']}")
    print(f"    BOND.entity_parts_available: {enrichment['BOND']['entity_parts_available']}")
    print(f"    EO.historical_safety_scores: {enrichment['EO']['historical_safety_scores']}")

    # Test 4: Entity Memory Nexus formation check
    print("\nTEST 4: Entity Memory Nexus (EMN) formation potential")
    print("-" * 50)

    # Simulate organ results with good activation
    mock_organ_results = {
        'LISTENING': {
            'top_atoms': [('relational_inquiry', 0.85), ('temporal_inquiry', 0.60)]
        },
        'EMPATHY': {
            'top_atoms': [('relational_attunement', 0.78), ('compassionate_presence', 0.65)]
        },
        'BOND': {
            'top_atoms': [('SELF_energy', 0.55), ('manager_parts', 0.45)]
        },
        'EO': {
            'top_atoms': [('ventral_vagal', 0.92), ('sympathetic_activation', 0.25)]
        },
    }

    emn_data = prehension.create_entity_memory_nexus_data(result, mock_organ_results)

    print(f"  Can form Entity Memory Nexus: {emn_data['can_form_emn']}")
    print(f"  EMN strength: {emn_data['emn_strength']:.2f}")
    print(f"  Participating organs: {emn_data['participating_organs']}")
    print(f"  Entity context:")
    print(f"    User name: {emn_data['entity_context'].get('user_name')}")
    print(f"    Memory richness: {emn_data['entity_context'].get('memory_richness'):.2f}")

    if emn_data['can_form_emn']:
        print("\n  ✅ Entity Memory Nexus CAN form (was impossible before!)")
    else:
        print("\n  ⚠️  EMN cannot form (organ activation too low)")

    # Test 5: Test with entity mention (daughter)
    print("\nTEST 5: Entity mention detection (Emma)")
    print("-" * 50)

    emma_query = "How is Emma doing with school?"

    emma_result = prehension.retrieve_relevant_entities(
        user_input=emma_query,
        user_id=test_user_id
    )

    print(f"  Query: '{emma_query}'")
    print(f"  Entities mentioned: {len(emma_result['mentioned_entities'])}")

    for entity in emma_result['mentioned_entities']:
        print(f"    - {entity['name']} ({entity.get('relationship', entity.get('type', 'entity'))})")
        if 'historical_polyvagal' in entity:
            print(f"      Historical polyvagal: {entity['historical_polyvagal']}")
            print(f"      Historical safety: {entity.get('historical_safety', 0):.2f}")

    # Test 6: Implicit reference detection
    print("\nTEST 6: Implicit reference detection (my daughter)")
    print("-" * 50)

    implicit_query = "My daughter has been struggling lately"

    implicit_result = prehension.retrieve_relevant_entities(
        user_input=implicit_query,
        user_id=test_user_id
    )

    print(f"  Query: '{implicit_query}'")
    print(f"  Implicit references detected: {len(implicit_result['implicit_references'])}")

    for ref in implicit_result['implicit_references']:
        print(f"    - '{ref['keyword']}' → {ref['resolved_to']} (confidence: {ref['confidence']:.2f})")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    checks_passed = 0
    total_checks = 5

    # Check 1: Relational query detection
    if result['relational_query_detected']:
        print("✅ Check 1: Relational query detection PASSED")
        checks_passed += 1
    else:
        print("❌ Check 1: Relational query detection FAILED")

    # Check 2: User name retrieval
    if result['user_name'] == 'Emiliano':
        print("✅ Check 2: User name retrieval PASSED")
        checks_passed += 1
    else:
        print("❌ Check 2: User name retrieval FAILED")

    # Check 3: Organ context enrichment
    if enrichment['LISTENING']['relational_inquiry_boost'] > 0:
        print("✅ Check 3: Organ context enrichment PASSED")
        checks_passed += 1
    else:
        print("❌ Check 3: Organ context enrichment FAILED")

    # Check 4: EMN formation potential
    if emn_data['can_form_emn']:
        print("✅ Check 4: Entity Memory Nexus formation PASSED")
        checks_passed += 1
    else:
        print("❌ Check 4: Entity Memory Nexus formation FAILED")

    # Check 5: Entity mention detection
    if len(emma_result['mentioned_entities']) > 0:
        print("✅ Check 5: Entity mention detection PASSED")
        checks_passed += 1
    else:
        print("❌ Check 5: Entity mention detection FAILED")

    print(f"\nResult: {checks_passed}/{total_checks} checks passed")

    if checks_passed == total_checks:
        print("\n🌀 PRE-EMISSION ENTITY PREHENSION FULLY OPERATIONAL!")
        print("   Entity memory now retrieved BEFORE organ activation.")
        print("   Entity Memory Nexus formation enabled.")
        print("   No more 'Nexuses formed: 0' on relational queries!")
    else:
        print(f"\n⚠️  {total_checks - checks_passed} checks need attention")

    print("\n" + "="*70)

    # Clean up test profile (optional)
    # import os
    # profile_path = f"persona_layer/users/{test_user_id}_superject.json"
    # if os.path.exists(profile_path):
    #     os.remove(profile_path)


if __name__ == "__main__":
    main()
