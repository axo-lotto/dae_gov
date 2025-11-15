#!/usr/bin/env python3
"""
🌀 Phase 1.8+: TSK Entity Enrichment Test (Nov 14, 2025)

Tests end-to-end entity extraction with transductive felt-state enrichment.
Validates that entities are differentiated by felt-state fingerprints.

Test Flow:
1. User introduces name in crisis context
2. Verify entity extracted with crisis felt-state
3. User mentions same name in healing context
4. Verify entity differentiated with healing felt-state
5. Check composite signatures show both crisis and healing
"""

import sys
import os
import json
from datetime import datetime

# Set PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from persona_layer.memory_intent_detector import MemoryIntentDetector
from persona_layer.entity_extractor import EntityExtractor
from persona_layer.superject_structures import EnhancedUserProfile

def create_mock_felt_state(crisis_mode=True):
    """Create mock felt-state for testing."""
    if crisis_mode:
        # Crisis context: high urgency, sympathetic state
        return {
            'polyvagal_state': 'sympathetic',
            'self_distance': 0.2,  # Exiled
            'urgency_level': 0.85,
            'nexuses': [
                {'name': 'Urgency', 'confidence': 0.9},
                {'name': 'Disruptive', 'confidence': 0.7}
            ],
            'v0_energy': 0.8,  # High unsatisfied energy
            'satisfaction': 0.3,
            'convergence_cycles': 3,
            'active_organs': ['NDAM', 'BOND', 'LISTENING', 'EMPATHY'],
            'transduction_mechanism': 'crisis_urgency',
            'transduction_pathway': 'protective_shutdown',
            'healing_trajectory': False
        }
    else:
        # Healing context: low urgency, ventral vagal state
        return {
            'polyvagal_state': 'ventral_vagal',
            'self_distance': 0.8,  # Self-led
            'urgency_level': 0.1,
            'nexuses': [
                {'name': 'Relational', 'confidence': 0.85},
                {'name': 'Innate', 'confidence': 0.75}
            ],
            'v0_energy': 0.2,  # Low unsatisfied energy
            'satisfaction': 0.9,
            'convergence_cycles': 2,
            'active_organs': ['PRESENCE', 'WISDOM', 'AUTHENTICITY', 'EMPATHY'],
            'transduction_mechanism': 'relational_depth',
            'transduction_pathway': 'mutual_resonance',
            'healing_trajectory': True
        }

def print_section(title):
    """Print section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_tsk_entity_enrichment():
    """Test full TSK entity enrichment flow."""

    print_section("🌀 TSK Entity Enrichment Test")

    # Initialize components
    detector = MemoryIntentDetector()
    extractor = EntityExtractor()
    profile = EnhancedUserProfile(
        user_id="test_user_tsk_001",
        created_at=datetime.now().isoformat(),
        last_active=datetime.now().isoformat()
    )

    # Test 1: Crisis mention
    print_section("Test 1: Entity Mention in Crisis Context")

    crisis_input = "Please remember these names: Alice is in the hospital right now"

    # Detect intent
    detected, intent_type, confidence, context = detector.detect(crisis_input)
    print(f"✓ Intent detected: {intent_type} (confidence: {confidence:.2f})")

    # Extract with crisis felt-state
    crisis_felt_state = create_mock_felt_state(crisis_mode=True)
    entities_crisis = extractor.extract(
        crisis_input,
        intent_type,
        context,
        felt_state=crisis_felt_state
    )

    print(f"✓ Entities extracted: {list(entities_crisis.keys())}")

    # Check transductive context
    if 'transductive_context' in entities_crisis:
        tc = entities_crisis['transductive_context']
        print(f"\n🌀 Transductive Context (Crisis):")
        print(f"   Polyvagal: {tc['polyvagal_state']}")
        print(f"   Self-distance: {tc['self_distance']:.2f}")
        print(f"   Urgency: {tc['urgency_level']:.2f}")
        print(f"   Dominant nexuses: {', '.join(tc['dominant_nexuses'])}")
        print(f"   Nexus category: {tc['nexus_category']}")
        print(f"   Crisis moment: {tc['is_crisis_moment']}")
        print(f"   V0 energy: {tc['v0_energy']:.2f}")
        print(f"   Satisfaction: {tc['satisfaction']:.2f}")
    else:
        print("⚠️  No transductive context extracted")
        return False

    # Store in profile
    profile.store_entities(entities_crisis)
    print(f"\n✓ Entities stored in profile")
    print(f"   Total entities: {len(profile.entities)}")

    # Test 2: Healing mention
    print_section("Test 2: Same Entity Mention in Healing Context")

    healing_input = "Can you remember - Alice came home from the hospital today!"

    # Detect intent
    detected2, intent_type2, confidence2, context2 = detector.detect(healing_input)
    print(f"✓ Intent detected: {intent_type2} (confidence: {confidence2:.2f})")

    # Extract with healing felt-state
    healing_felt_state = create_mock_felt_state(crisis_mode=False)
    entities_healing = extractor.extract(
        healing_input,
        intent_type2,
        context2,
        felt_state=healing_felt_state
    )

    print(f"✓ Entities extracted: {list(entities_healing.keys())}")

    # Check transductive context
    if 'transductive_context' in entities_healing:
        tc = entities_healing['transductive_context']
        print(f"\n🌀 Transductive Context (Healing):")
        print(f"   Polyvagal: {tc['polyvagal_state']}")
        print(f"   Self-distance: {tc['self_distance']:.2f}")
        print(f"   Urgency: {tc['urgency_level']:.2f}")
        print(f"   Dominant nexuses: {', '.join(tc['dominant_nexuses'])}")
        print(f"   Nexus category: {tc['nexus_category']}")
        print(f"   Healing trajectory: {tc['healing_trajectory']}")
        print(f"   V0 energy: {tc['v0_energy']:.2f}")
        print(f"   Satisfaction: {tc['satisfaction']:.2f}")

    # Store in profile (merge with existing)
    profile.store_entities(entities_healing)
    print(f"\n✓ Entities updated in profile")
    print(f"   Total entities: {len(profile.entities)}")

    # Test 3: Verify differentiation
    print_section("Test 3: Verify Entity Differentiation")

    # Get entity context string
    entity_context = profile.get_entity_context_string()
    print(f"Entity Context String:\n{entity_context}")

    # Show entity history
    if 'entity_history' in profile.entity_history and len(profile.entity_history) > 0:
        print(f"\n✓ Entity history tracked ({len(profile.entity_history)} entries)")
        for i, entry in enumerate(profile.entity_history, 1):
            print(f"   Entry {i}: {entry['timestamp'][:19]}")
            if 'entities' in entry:
                ent = entry['entities']
                if 'transductive_context' in ent:
                    tc = ent['transductive_context']
                    print(f"      → Polyvagal: {tc['polyvagal_state']}, Urgency: {tc['urgency_level']:.2f}")

    # Test 4: Validate differentiation capability
    print_section("Test 4: Validate Differentiation Capability")

    # Debug: Print entity_history length
    print(f"Entity history entries: {len(profile.entity_history)}")

    # Check if we can differentiate Alice mentions
    alice_entities = [e for e in profile.entity_history if 'transductive_context' in e.get('entities', {})]

    if len(alice_entities) >= 2:
        crisis_entry = alice_entities[0]['entities']['transductive_context']
        healing_entry = alice_entities[1]['entities']['transductive_context']

        print(f"✓ Alice mentioned in 2 different contexts:")
        print(f"\n  Crisis Context:")
        print(f"    Polyvagal: {crisis_entry['polyvagal_state']}")
        print(f"    Urgency: {crisis_entry['urgency_level']:.2f}")
        print(f"    Nexuses: {', '.join(crisis_entry['dominant_nexuses'])}")

        print(f"\n  Healing Context:")
        print(f"    Polyvagal: {healing_entry['polyvagal_state']}")
        print(f"    Urgency: {healing_entry['urgency_level']:.2f}")
        print(f"    Nexuses: {', '.join(healing_entry['dominant_nexuses'])}")

        # Verify differentiation
        urgency_diff = abs(crisis_entry['urgency_level'] - healing_entry['urgency_level'])
        polyvagal_diff = crisis_entry['polyvagal_state'] != healing_entry['polyvagal_state']

        print(f"\n✓ Differentiation Metrics:")
        print(f"   Urgency difference: {urgency_diff:.2f} (should be > 0.5)")
        print(f"   Polyvagal state differs: {polyvagal_diff}")

        if urgency_diff > 0.5 and polyvagal_diff:
            print(f"\n✅ SUCCESS: Entity differentiation working!")
            print(f"   Same entity ('Alice') successfully differentiated by felt-state context")
            return True
        else:
            print(f"\n⚠️  Warning: Differentiation metrics below threshold")
            return False
    else:
        print(f"⚠️  Warning: Expected 2 entity entries, found {len(alice_entities)}")
        return False

def test_without_tsk():
    """Test backward compatibility without TSK."""
    print_section("Test 5: Backward Compatibility (No TSK)")

    detector = MemoryIntentDetector()
    extractor = EntityExtractor()

    test_input = "My name is Bob"

    detected, intent_type, confidence, context = detector.detect(test_input)
    print(f"✓ Intent detected: {intent_type} (confidence: {confidence:.2f})")

    # Extract WITHOUT felt_state
    entities = extractor.extract(test_input, intent_type, context)

    print(f"✓ Entities extracted: {list(entities.keys())}")
    print(f"✓ Transductive context present: {'transductive_context' in entities}")

    if 'user_name' in entities:
        print(f"✓ User name extracted: {entities['user_name']}")
        print(f"\n✅ Backward compatibility verified - works without TSK")
        return True
    else:
        print(f"⚠️  User name not extracted")
        return False

if __name__ == '__main__':
    try:
        # Run main test
        result1 = test_tsk_entity_enrichment()

        # Run backward compatibility test
        result2 = test_without_tsk()

        # Summary
        print_section("Test Summary")
        print(f"TSK Entity Enrichment: {'✅ PASSED' if result1 else '❌ FAILED'}")
        print(f"Backward Compatibility: {'✅ PASSED' if result2 else '❌ FAILED'}")

        if result1 and result2:
            print(f"\n🌀 All tests passed! TSK entity enrichment operational.")
            sys.exit(0)
        else:
            print(f"\n⚠️  Some tests failed. Review output above.")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
