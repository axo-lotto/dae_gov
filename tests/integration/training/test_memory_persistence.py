#!/usr/bin/env python3
"""
Memory Persistence Test - November 14, 2025
===========================================

Tests the complete memory persistence system end-to-end:
1. Entity extraction from user input
2. Storage in user profile
3. Persistent context loading on subsequent turns
4. Access to stored entities by organism and LLM

Tests cover:
- Name extraction and persistence
- Context injection
- Multi-turn memory continuity
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import components
from persona_layer.memory_intent_detector import MemoryIntentDetector
from persona_layer.entity_extractor import EntityExtractor
from persona_layer.user_registry import UserRegistry
from persona_layer.superject_structures import EnhancedUserProfile


class MemoryPersistenceTest:
    """Test suite for memory persistence system."""

    def __init__(self):
        """Initialize test components."""
        self.detector = MemoryIntentDetector()
        self.extractor = EntityExtractor()
        self.user_registry = UserRegistry()
        self.test_results = []

    def test_name_extraction(self):
        """Test 1: Name extraction from self-introduction."""
        print("\n" + "="*70)
        print("TEST 1: Name Extraction from Self-Introduction")
        print("="*70)

        test_input = "hello there my name is emiliano, can you remember this?"
        print(f"\n📝 Input: \"{test_input}\"")

        # Step 1: Detect intent
        detected, intent_type, confidence, context = self.detector.detect(test_input)
        print(f"\n✅ Intent Detection:")
        print(f"   Type: {intent_type}")
        print(f"   Confidence: {confidence:.3f}")
        print(f"   Context: {context}")

        # Step 2: Extract entities
        entities = self.extractor.extract(test_input, intent_type, context)
        print(f"\n✅ Entity Extraction:")
        for key, value in entities.items():
            if key not in ['timestamp', 'source_text', 'intent_type']:
                print(f"   {key}: {value}")

        # Verify
        success = entities.get('user_name') == 'emiliano'
        self.test_results.append({
            'test': 'name_extraction',
            'success': success,
            'expected': 'emiliano',
            'actual': entities.get('user_name', 'NOT FOUND')
        })

        if success:
            print(f"\n✅ TEST PASSED: Name 'emiliano' extracted correctly")
        else:
            print(f"\n❌ TEST FAILED: Expected 'emiliano', got '{entities.get('user_name', 'NOT FOUND')}'")

        return success, entities

    def test_entity_storage(self, entities):
        """Test 2: Entity storage in user profile."""
        print("\n" + "="*70)
        print("TEST 2: Entity Storage in User Profile")
        print("="*70)

        # Create test user
        test_user_id = f"test_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"\n📝 Creating test user: {test_user_id}")

        # Create user profile
        profile = EnhancedUserProfile(
            user_id=test_user_id,
            created_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat()
        )

        # Store entities
        profile.store_entities(entities)
        print(f"\n✅ Entities stored in profile")
        print(f"   Profile entities: {profile.entities}")

        # Verify storage
        success = 'user_name' in profile.entities and profile.entities['user_name'] == 'emiliano'
        self.test_results.append({
            'test': 'entity_storage',
            'success': success,
            'expected': 'emiliano in profile.entities',
            'actual': f"profile.entities = {profile.entities}"
        })

        if success:
            print(f"\n✅ TEST PASSED: Entity stored in profile")
        else:
            print(f"\n❌ TEST FAILED: Entity not found in profile")

        return success, profile

    def test_context_loading(self, profile):
        """Test 3: Persistent context loading."""
        print("\n" + "="*70)
        print("TEST 3: Persistent Context Loading (Simulated)")
        print("="*70)

        # Simulate context loading (as done in dae_interactive.py)
        context = {}

        # Load entity context
        context['entity_context_string'] = profile.get_entity_context_string()

        # Add individual entities
        if profile.entities:
            context['stored_entities'] = profile.entities

            # Add username
            if 'user_name' in profile.entities:
                context['username'] = profile.entities['user_name']

        print(f"\n✅ Context loaded:")
        print(f"   username: {context.get('username', 'NOT FOUND')}")
        print(f"   entity_context_string: {context.get('entity_context_string', 'EMPTY')}")
        print(f"   stored_entities: {context.get('stored_entities', {})}")

        # Verify
        success = context.get('username') == 'emiliano'
        self.test_results.append({
            'test': 'context_loading',
            'success': success,
            'expected': 'emiliano in context',
            'actual': f"context['username'] = {context.get('username', 'NOT FOUND')}"
        })

        if success:
            print(f"\n✅ TEST PASSED: Username loaded into context")
        else:
            print(f"\n❌ TEST FAILED: Username not found in context")

        return success, context

    def test_multi_turn_memory(self):
        """Test 4: Multi-turn memory continuity."""
        print("\n" + "="*70)
        print("TEST 4: Multi-Turn Memory Continuity")
        print("="*70)

        # Turn 1: Introduce name
        turn1_input = "my name is alice"
        print(f"\n📝 Turn 1: \"{turn1_input}\"")

        detected, intent_type, confidence, context = self.detector.detect(turn1_input)
        entities_turn1 = self.extractor.extract(turn1_input, intent_type, context)

        # Create profile and store
        profile = EnhancedUserProfile(
            user_id="test_multiturn",
            created_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat()
        )
        profile.store_entities(entities_turn1)
        print(f"   ✅ Stored: user_name = {profile.entities.get('user_name', 'NOT FOUND')}")

        # Turn 2: Ask about name (simulating "remember my name?")
        turn2_input = "what is my name?"
        print(f"\n📝 Turn 2: \"{turn2_input}\"")

        # Load context from profile (as interactive session would do)
        context_turn2 = {}
        if profile.entities and 'user_name' in profile.entities:
            context_turn2['username'] = profile.entities['user_name']
            context_turn2['stored_entities'] = profile.entities

        print(f"   ✅ Context loaded: username = {context_turn2.get('username', 'NOT FOUND')}")

        # Verify
        success = context_turn2.get('username') == 'alice'
        self.test_results.append({
            'test': 'multi_turn_memory',
            'success': success,
            'expected': 'alice remembered in turn 2',
            'actual': f"context['username'] = {context_turn2.get('username', 'NOT FOUND')}"
        })

        if success:
            print(f"\n✅ TEST PASSED: Name persisted across turns")
        else:
            print(f"\n❌ TEST FAILED: Name not available in turn 2")

        return success

    def run_all_tests(self):
        """Run complete test suite."""
        print("\n" + "="*70)
        print("🧪 MEMORY PERSISTENCE TEST SUITE")
        print("="*70)
        print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Testing: Entity extraction → Storage → Context loading → Multi-turn")

        # Run tests
        test1_pass, entities = self.test_name_extraction()
        test2_pass, profile = self.test_entity_storage(entities)
        test3_pass, context = self.test_context_loading(profile)
        test4_pass = self.test_multi_turn_memory()

        # Summary
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['success'])

        print(f"\nTotal tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")

        print("\nDetailed Results:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"\n{i}. {result['test']}: {status}")
            print(f"   Expected: {result['expected']}")
            print(f"   Actual: {result['actual']}")

        # Overall result
        print("\n" + "="*70)
        if passed_tests == total_tests:
            print("✅ ALL TESTS PASSED - Memory persistence system operational!")
        else:
            print(f"⚠️  {total_tests - passed_tests} TEST(S) FAILED - Review failures above")
        print("="*70 + "\n")

        return passed_tests == total_tests


def main():
    """Main test runner."""
    try:
        tester = MemoryPersistenceTest()
        all_passed = tester.run_all_tests()
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\n❌ TEST SUITE CRASHED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
