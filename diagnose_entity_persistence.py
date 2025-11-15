#!/usr/bin/env python3
"""
Comprehensive Entity Persistence Diagnostic
Traces entity flow through extraction, storage, and retrieval.

November 14, 2025 - Entity Persistence Debugging
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.user_registry import UserRegistry
from persona_layer.superject_structures import EnhancedUserProfile
from datetime import datetime
import json


def test_profile_initialization():
    """Test that EnhancedUserProfile correctly initializes entities field."""
    print("=" * 80)
    print("TEST 1: Profile Initialization")
    print("=" * 80)

    profile = EnhancedUserProfile(
        user_id="test_user_123",
        created_at=datetime.now().isoformat(),
        last_active=datetime.now().isoformat()
    )

    print(f"\n✓ Created profile")
    print(f"  user_id: {profile.user_id}")

    # Check if entities attribute exists
    if hasattr(profile, 'entities'):
        print(f"  ✅ profile.entities exists")
        print(f"  Type: {type(profile.entities)}")
        print(f"  Value: {profile.entities}")

        if isinstance(profile.entities, dict):
            print(f"  ✅ profile.entities is a dict")
            return True
        else:
            print(f"  ❌ profile.entities is NOT a dict (type: {type(profile.entities)})")
            return False
    else:
        print(f"  ❌ profile.entities does NOT exist")
        print(f"  Available attributes: {dir(profile)}")
        return False


def test_entity_storage():
    """Test that store_entities() correctly updates profile.entities."""
    print("\n\n" + "=" * 80)
    print("TEST 2: Entity Storage")
    print("=" * 80)

    profile = EnhancedUserProfile(
        user_id="test_user_123",
        created_at=datetime.now().isoformat(),
        last_active=datetime.now().isoformat()
    )

    # Test entities
    test_entities = {
        'user_name': 'Emiliano',
        'family_members': [{'name': 'Bob', 'relation': 'brother'}],
        'friends': [{'name': 'Charlie'}],
        'preferences': {'color': 'blue', 'hobby': 'coding'}
    }

    print(f"\n📝 Storing entities:")
    for key, value in test_entities.items():
        print(f"  {key}: {value}")

    # Store entities
    profile.store_entities(test_entities)

    print(f"\n✓ store_entities() called")

    # Check if entities were stored
    if hasattr(profile, 'entities'):
        print(f"\n📦 profile.entities after storage:")
        for key, value in profile.entities.items():
            print(f"  {key}: {value}")

        # Verify each entity
        success = True

        if profile.entities.get('user_name') == 'Emiliano':
            print(f"\n  ✅ user_name stored correctly")
        else:
            print(f"\n  ❌ user_name NOT stored (got: {profile.entities.get('user_name')})")
            success = False

        expected_family = [{'name': 'Bob', 'relation': 'brother'}]
        if profile.entities.get('family_members') == expected_family:
            print(f"  ✅ family_members stored correctly")
        else:
            print(f"  ❌ family_members NOT stored correctly")
            print(f"     Expected: {expected_family}")
            print(f"     Got: {profile.entities.get('family_members')}")
            success = False

        if profile.entities.get('preferences') == {'color': 'blue', 'hobby': 'coding'}:
            print(f"  ✅ preferences stored correctly")
        else:
            print(f"  ❌ preferences NOT stored correctly")
            success = False

        return success
    else:
        print(f"\n  ❌ profile.entities does NOT exist after storage")
        return False


def test_serialization():
    """Test that to_dict() and from_dict() correctly serialize entities."""
    print("\n\n" + "=" * 80)
    print("TEST 3: Serialization (to_dict/from_dict)")
    print("=" * 80)

    # Create profile with entities
    profile1 = EnhancedUserProfile(
        user_id="test_user_123",
        created_at=datetime.now().isoformat(),
        last_active=datetime.now().isoformat()
    )

    test_entities = {
        'user_name': 'Emiliano',
        'family_members': [{'name': 'Bob', 'relation': 'brother'}],
        'friends': [],
        'preferences': {'color': 'blue'}
    }

    profile1.store_entities(test_entities)

    print(f"\n📝 Original profile.entities:")
    print(f"  {profile1.entities}")

    # Serialize
    profile_dict = profile1.to_dict()

    print(f"\n📦 Serialized to dict:")
    print(f"  Keys: {profile_dict.keys()}")

    if 'entities' in profile_dict:
        print(f"  ✅ 'entities' in serialized dict")
        print(f"  entities value: {profile_dict['entities']}")
    else:
        print(f"  ❌ 'entities' NOT in serialized dict")
        print(f"  Available keys: {list(profile_dict.keys())}")
        return False

    # Deserialize
    profile2 = EnhancedUserProfile.from_dict(profile_dict)

    print(f"\n📥 Deserialized profile.entities:")
    if hasattr(profile2, 'entities'):
        print(f"  {profile2.entities}")

        if profile2.entities.get('user_name') == 'Emiliano':
            print(f"\n  ✅ user_name survived serialization")
            return True
        else:
            print(f"\n  ❌ user_name LOST in serialization")
            print(f"     Expected: 'Emiliano'")
            print(f"     Got: {profile2.entities.get('user_name')}")
            return False
    else:
        print(f"  ❌ profile.entities does NOT exist after deserialization")
        return False


def test_user_state_persistence():
    """Test full user state save/load cycle."""
    print("\n\n" + "=" * 80)
    print("TEST 4: User State Persistence (Full Cycle)")
    print("=" * 80)

    user_registry = UserRegistry()

    # Create test user
    user_id = user_registry.create_user("test_entity_persist")
    print(f"\n✅ Created user: {user_id}")

    # === TURN 1: Store entities ===
    print(f"\n{'='*80}")
    print(f"TURN 1: Storing Entities")
    print(f"{'='*80}")

    # Load user state
    user_state = user_registry.load_user_state(user_id)
    print(f"\n📦 Loaded user_state (Turn 1)")
    print(f"  Keys: {user_state.keys()}")

    # Create or load profile
    if 'user_profile' not in user_state:
        print(f"  ℹ️  No profile exists yet - creating new")
        profile = EnhancedUserProfile(
            user_id=user_id,
            created_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat()
        )
    else:
        profile = EnhancedUserProfile.from_dict(user_state['user_profile'])

    # Store test entities
    test_entities = {
        'user_name': 'Emiliano',
        'family_members': [{'name': 'Bob', 'relation': 'brother'}],
        'friends': [],
        'preferences': {'color': 'blue'}
    }

    print(f"\n📝 Storing entities:")
    for key, value in test_entities.items():
        print(f"  {key}: {value}")

    profile.store_entities(test_entities)

    # Save to user_state
    user_state['user_profile'] = profile.to_dict()

    # Save to disk
    user_registry.save_user_state(user_id, user_state)
    print(f"\n✅ Saved user_state to disk")

    # Verify what was saved
    print(f"\n🔍 Verifying saved data:")
    if 'entities' in user_state['user_profile']:
        print(f"  ✅ 'entities' in user_profile")
        print(f"  entities: {user_state['user_profile']['entities']}")
    else:
        print(f"  ❌ 'entities' NOT in user_profile")
        print(f"  Keys: {user_state['user_profile'].keys()}")

    # === TURN 2: Load entities ===
    print(f"\n{'='*80}")
    print(f"TURN 2: Loading Entities (Simulating New Turn)")
    print(f"{'='*80}")

    # Reload user state (simulate new turn)
    user_state = user_registry.load_user_state(user_id)
    print(f"\n📦 Loaded user_state (Turn 2)")

    if 'user_profile' in user_state:
        print(f"  ✅ user_profile exists in user_state")

        profile = EnhancedUserProfile.from_dict(user_state['user_profile'])
        print(f"  ✅ Profile deserialized")

        # Check entities
        if hasattr(profile, 'entities'):
            print(f"\n📦 profile.entities (Turn 2):")
            print(f"  {profile.entities}")

            # Build stored_entities (like dae_interactive.py does)
            stored_entities = {}
            if isinstance(profile.entities, dict):
                stored_entities = profile.entities
                print(f"\n✅ Entities loaded into stored_entities:")
                for key, value in stored_entities.items():
                    print(f"  {key}: {value}")

                # Final verification
                if stored_entities.get('user_name') == 'Emiliano':
                    print(f"\n✅ SUCCESS: Entity persistence works!")
                    print(f"   user_name persisted across turns")
                    return True
                else:
                    print(f"\n❌ FAIL: user_name not correct")
                    print(f"   Expected: 'Emiliano'")
                    print(f"   Got: {stored_entities.get('user_name')}")
                    return False
            else:
                print(f"\n❌ FAIL: profile.entities is not a dict")
                print(f"   Type: {type(profile.entities)}")
                return False
        else:
            print(f"\n❌ FAIL: profile.entities does NOT exist")
            return False
    else:
        print(f"\n❌ FAIL: user_profile not in user_state")
        return False


def test_entity_context_string():
    """Test that entity context string is correctly generated."""
    print("\n\n" + "=" * 80)
    print("TEST 5: Entity Context String Generation")
    print("=" * 80)

    profile = EnhancedUserProfile(
        user_id="test_user_123",
        created_at=datetime.now().isoformat(),
        last_active=datetime.now().isoformat()
    )

    # Store entities
    test_entities = {
        'user_name': 'Emiliano',
        'family_members': [{'name': 'Bob', 'relation': 'brother'}],
        'friends': [{'name': 'Charlie'}],
        'preferences': {}
    }

    profile.store_entities(test_entities)

    # Get entity context string
    if hasattr(profile, 'get_entity_context_string'):
        context_string = profile.get_entity_context_string()
        print(f"\n📝 Entity context string:")
        print(f'  "{context_string}"')

        if 'Emiliano' in context_string:
            print(f"\n  ✅ Contains user_name (Emiliano)")
            return True
        else:
            print(f"\n  ❌ Does NOT contain user_name")
            return False
    else:
        print(f"\n  ⚠️  get_entity_context_string() method not found")
        return False


def main():
    """Run all diagnostics."""
    print("\n🔍 COMPREHENSIVE ENTITY PERSISTENCE DIAGNOSTIC")
    print("November 14, 2025")
    print("\n")

    results = {}

    # Test 1: Profile initialization
    results['initialization'] = test_profile_initialization()

    # Test 2: Entity storage
    results['storage'] = test_entity_storage()

    # Test 3: Serialization
    results['serialization'] = test_serialization()

    # Test 4: Full persistence cycle
    results['persistence'] = test_user_state_persistence()

    # Test 5: Context string
    results['context_string'] = test_entity_context_string()

    # Summary
    print("\n\n" + "=" * 80)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 80)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    total_passed = sum(1 for p in results.values() if p)
    total_tests = len(results)

    print(f"\nTotal: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print("\n🎉 All tests passed! Entity persistence is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Entity persistence has issues.")

        # Diagnosis
        print("\n" + "=" * 80)
        print("DIAGNOSIS")
        print("=" * 80)

        if not results['initialization']:
            print("\n❌ ISSUE: profile.entities field not initialized")
            print("   FIX: Add 'self.entities = {}' to EnhancedUserProfile.__init__()")

        if results['initialization'] and not results['storage']:
            print("\n❌ ISSUE: store_entities() not working")
            print("   FIX: Check EnhancedUserProfile.store_entities() implementation")

        if results['storage'] and not results['serialization']:
            print("\n❌ ISSUE: to_dict() or from_dict() not preserving entities")
            print("   FIX: Ensure to_dict() includes 'entities' field")
            print("        Ensure from_dict() restores 'entities' field")

        if results['serialization'] and not results['persistence']:
            print("\n❌ ISSUE: User state save/load not working")
            print("   FIX: Check user_registry.save_user_state() and load_user_state()")

    return total_passed == total_tests


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
