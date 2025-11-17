"""
Test Entity Salience Tracker - 3-Tier Temporal Decay
=====================================================

Validates EntitySalienceTracker with FFITTSS-inspired multi-scale decay.

Expected Results:
- Local salience: Fast adaptation (α=0.05, half-life ≈ 13 turns)
- Family salience: Medium adaptation (α=0.1, half-life ≈ 7 turns)
- Global salience: Slow adaptation (α=0.05, half-life ≈ 14 turns)
- Staleness pruning: 300+ turns → stale
- L2 regularization: Prevents explosion

Author: DAE_HYPHAE_1 + Claude Code
Date: November 17, 2025
"""

import os
import tempfile
from persona_layer.entity_salience_tracker import EntitySalienceTracker


def test_initialization():
    """Test basic initialization."""
    print("="*80)
    print("TEST 1: Initialization")
    print("="*80)

    tracker = EntitySalienceTracker(
        storage_path=tempfile.mktemp(suffix=".json"),
        staleness_threshold=300
    )

    assert len(tracker.entity_metrics) == 0
    assert tracker.current_turn == 0
    assert tracker.global_salience == 0.0

    print("  ✅ Tracker initialized successfully")
    print(f"  ✅ Decay rates: local={tracker.LOCAL_ALPHA}, family={tracker.FAMILY_ALPHA}, global={tracker.GLOBAL_ALPHA}")
    print(f"  ✅ Staleness threshold: {tracker.staleness_threshold}")
    print()
    return True


def test_single_entity_salience():
    """Test salience for single entity over time."""
    print("="*80)
    print("TEST 2: Single Entity Salience Evolution")
    print("="*80)

    tracker = EntitySalienceTracker(storage_path=tempfile.mktemp(suffix=".json"))

    # Mention Emma on turns 1, 2, 3
    for turn in [1, 2, 3]:
        tracker.update_salience(
            extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
            current_turn=turn,
            urgency_context=0.0
        )

    metrics = tracker.entity_metrics['Emma']

    print(f"  After 3 mentions:")
    print(f"    Local salience: {metrics.local_salience:.3f}")
    print(f"    Family salience: {metrics.family_salience:.3f}")
    print(f"    Global salience: {metrics.global_salience:.3f}")
    print(f"    Composite: {metrics.composite_salience:.3f}")
    print(f"    Mention count: {metrics.mention_count}")
    print(f"    Turn since mention: {metrics.turn_since_mention}")

    # Verify salience increased
    assert metrics.local_salience > 0
    assert metrics.composite_salience > 0
    assert metrics.mention_count == 3

    print(f"\n  ✅ Salience increases with mentions\n")
    return True


def test_temporal_decay():
    """Test salience decay over time."""
    print("="*80)
    print("TEST 3: Temporal Decay")
    print("="*80)

    tracker = EntitySalienceTracker(storage_path=tempfile.mktemp(suffix=".json"))

    # Mention Emma at turn 1
    tracker.update_salience(
        extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
        current_turn=1,
        urgency_context=0.0
    )

    initial_salience = tracker.entity_metrics['Emma'].composite_salience
    print(f"  Turn 1 (mentioned): composite salience = {initial_salience:.3f}")

    # Let time pass (turns 2-10 without mention)
    for turn in range(2, 11):
        tracker.update_salience(
            extracted_entities=[],  # No mentions
            current_turn=turn,
            urgency_context=0.0
        )

    decayed_salience = tracker.entity_metrics['Emma'].composite_salience
    print(f"  Turn 10 (not mentioned): composite salience = {decayed_salience:.3f}")

    # Verify decay occurred
    assert decayed_salience < initial_salience
    print(f"  ✅ Salience decayed by {(1 - decayed_salience/initial_salience)*100:.1f}%\n")
    return True


def test_urgency_boost():
    """Test urgency context boosts salience."""
    print("="*80)
    print("TEST 4: Urgency Boost")
    print("="*80)

    tracker = EntitySalienceTracker(storage_path=tempfile.mktemp(suffix=".json"))

    # Mention Emma with low urgency
    tracker.update_salience(
        extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
        current_turn=1,
        urgency_context=0.0  # Low urgency
    )
    low_urgency_salience = tracker.entity_metrics['Emma'].composite_salience

    # Mention Lily with high urgency
    tracker.update_salience(
        extracted_entities=[{'entity_value': 'Lily', 'entity_type': 'Person'}],
        current_turn=2,
        urgency_context=0.8  # High urgency
    )
    high_urgency_salience = tracker.entity_metrics['Lily'].composite_salience

    print(f"  Emma (urgency 0.0): {low_urgency_salience:.3f}")
    print(f"  Lily (urgency 0.8): {high_urgency_salience:.3f}")

    # Verify urgency boost
    assert high_urgency_salience > low_urgency_salience
    print(f"  ✅ High urgency → {(high_urgency_salience/low_urgency_salience):.2f}× higher salience\n")
    return True


def test_family_salience():
    """Test family-level (relationship type) salience."""
    print("="*80)
    print("TEST 5: Family-Level Salience")
    print("="*80)

    tracker = EntitySalienceTracker(storage_path=tempfile.mktemp(suffix=".json"))

    # Mention multiple people
    people = [{'entity_value': f'Person{i}', 'entity_type': 'Person'} for i in range(3)]
    tracker.update_salience(extracted_entities=people, current_turn=1)

    # Mention multiple places
    places = [{'entity_value': f'Place{i}', 'entity_type': 'Place'} for i in range(3)]
    tracker.update_salience(extracted_entities=places, current_turn=2)

    # Check family salience
    person_family = tracker.family_salience['Person']
    place_family = tracker.family_salience['Place']

    print(f"  Person family salience: {person_family:.3f}")
    print(f"  Place family salience: {place_family:.3f}")

    assert person_family > 0
    assert place_family > 0

    print(f"  ✅ Family-level salience tracking operational\n")
    return True


def test_staleness_detection():
    """Test staleness detection after 300+ turns."""
    print("="*80)
    print("TEST 6: Staleness Detection")
    print("="*80)

    tracker = EntitySalienceTracker(
        storage_path=tempfile.mktemp(suffix=".json"),
        staleness_threshold=10  # Lower threshold for testing
    )

    # Mention Emma at turn 1
    tracker.update_salience(
        extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
        current_turn=1
    )

    # Let 15 turns pass without mention
    tracker.update_salience(extracted_entities=[], current_turn=16)

    metrics = tracker.entity_metrics['Emma']

    print(f"  Turn 1: mentioned")
    print(f"  Turn 16: not mentioned (15 turns elapsed)")
    print(f"  Staleness threshold: {tracker.staleness_threshold} turns")
    print(f"  Is stale: {metrics.is_stale}")
    print(f"  Turn since mention: {metrics.turn_since_mention}")

    assert metrics.is_stale == True
    print(f"  ✅ Staleness detected after threshold\n")
    return True


def test_salience_filtering():
    """Test top-K salience filtering."""
    print("="*80)
    print("TEST 7: Salience Filtering (Top-K)")
    print("="*80)

    tracker = EntitySalienceTracker(storage_path=tempfile.mktemp(suffix=".json"))

    # Create entities with different salience
    entities_with_salience = []

    # Emma: mentioned 3 times
    for turn in [1, 2, 3]:
        tracker.update_salience(
            extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
            current_turn=turn
        )
    entities_with_salience.append({'entity_value': 'Emma', 'entity_type': 'Person'})

    # Lily: mentioned 1 time
    tracker.update_salience(
        extracted_entities=[{'entity_value': 'Lily', 'entity_type': 'Person'}],
        current_turn=4
    )
    entities_with_salience.append({'entity_value': 'Lily', 'entity_type': 'Person'})

    # Work: mentioned 5 times
    for turn in [5, 6, 7, 8, 9]:
        tracker.update_salience(
            extracted_entities=[{'entity_value': 'Work', 'entity_type': 'Place'}],
            current_turn=turn
        )
    entities_with_salience.append({'entity_value': 'Work', 'entity_type': 'Place'})

    # Filter top-2
    top2 = tracker.filter_by_salience(entities_with_salience, top_k=2)

    print(f"  Entities (mention counts): Emma=3, Lily=1, Work=5")
    print(f"  Top-2 by salience:")
    for i, entity in enumerate(top2, 1):
        print(f"    {i}. {entity['entity_value']} (salience={entity['composite_salience']:.3f})")

    # Verify ordering (Work > Emma > Lily)
    assert len(top2) == 2
    assert top2[0]['entity_value'] == 'Work'  # Most mentioned
    assert top2[1]['entity_value'] == 'Emma'  # Second most

    print(f"  ✅ Top-K filtering working correctly\n")
    return True


def test_salience_persistence():
    """Test salience persistence to JSON."""
    print("="*80)
    print("TEST 8: Salience Persistence")
    print("="*80)

    temp_path = tempfile.mktemp(suffix=".json")

    # Create tracker and add entities
    tracker1 = EntitySalienceTracker(storage_path=temp_path)
    tracker1.update_salience(
        extracted_entities=[{'entity_value': 'Emma', 'entity_type': 'Person'}],
        current_turn=1
    )
    tracker1.save()

    salience_before = tracker1.entity_metrics['Emma'].composite_salience

    # Load in new tracker
    tracker2 = EntitySalienceTracker(storage_path=temp_path)
    salience_after = tracker2.entity_metrics['Emma'].composite_salience

    print(f"  Salience before save: {salience_before:.3f}")
    print(f"  Salience after load: {salience_after:.3f}")

    assert abs(salience_before - salience_after) < 0.001

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)

    print(f"  ✅ Salience persisted and loaded correctly\n")
    return True


def main():
    """Run all entity salience tests."""
    print("\n" + "="*80)
    print("🌀 ENTITY SALIENCE TRACKER VALIDATION")
    print("="*80)
    print("Testing 3-tier temporal decay (FFITTSS-inspired)")
    print("="*80 + "\n")

    tests = [
        ("Initialization", test_initialization),
        ("Single Entity Salience", test_single_entity_salience),
        ("Temporal Decay", test_temporal_decay),
        ("Urgency Boost", test_urgency_boost),
        ("Family Salience", test_family_salience),
        ("Staleness Detection", test_staleness_detection),
        ("Salience Filtering", test_salience_filtering),
        ("Salience Persistence", test_salience_persistence),
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}\n")

    # Summary
    print("="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"  Tests passed: {passed}/{total}")
    print(f"  Success rate: {passed/total*100:.1f}%")

    if passed == total:
        print(f"\n  ✅ All tests PASSED - EntitySalienceTracker validated!\n")
    else:
        print(f"\n  ⚠️  Some tests failed - review output above\n")

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
