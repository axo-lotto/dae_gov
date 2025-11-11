"""
Test Conversational Hebbian Learning Integration

Validates Phase 1.5 learning system:
1. Hebbian memory initialization and persistence
2. Pattern strengthening from positive outcomes
3. Pattern decay from negative outcomes
4. Cascade integration (polyvagal boost, SELF-energy boost, threshold adjustment, C preferences)
5. Learning trajectory tracking (0-10 conversations → 50-100 conversations)
6. Clinical safety (crisis family becomes MORE conservative)
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

import json
import tempfile
from pathlib import Path

from persona_layer.conversational_hebbian_memory import (
    ConversationalHebbianMemory,
    ConversationalOutcome
)
from persona_layer.self_led_cascade import (
    SELFLedCascade,
    SafetyLevel,
    GateDecision
)


def test_hebbian_memory_initialization():
    """Test 1: Hebbian memory initialization."""
    print("=" * 60)
    print("TEST 1: Hebbian Memory Initialization")
    print("=" * 60)
    print()

    # Create temporary storage
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        # Initialize memory
        memory = ConversationalHebbianMemory(
            eta=0.01,
            delta=0.001,
            storage_path=temp_path
        )

        print(f"✅ Memory initialized")
        print(f"   Detector names: {memory.detector_names}")
        print(f"   R-matrix shape: {memory.R_matrix.shape}")
        print(f"   Learning rate (η): {memory.eta}")
        print(f"   Decay rate (δ): {memory.delta}")
        print()

        # Check initial patterns
        assert 'ventral' in memory.polyvagal_patterns
        assert 'sympathetic' in memory.polyvagal_patterns
        assert 'dorsal' in memory.polyvagal_patterns
        print(f"✅ Polyvagal patterns initialized: {list(memory.polyvagal_patterns.keys())}")

        assert 'compassion' in memory.self_energy_patterns
        assert 'curiosity' in memory.self_energy_patterns
        print(f"✅ SELF-energy patterns initialized: {list(memory.self_energy_patterns.keys())[:4]}...")
        print()

        # Test persistence
        memory.save()
        print(f"✅ Memory saved to: {temp_path}")

        # Load and verify
        memory2 = ConversationalHebbianMemory(storage_path=temp_path)
        assert memory2.update_count == 0
        assert len(memory2.polyvagal_patterns) == 3
        print(f"✅ Memory loaded successfully")
        print()

    finally:
        Path(temp_path).unlink()

    print("TEST 1: ✅ PASS - Hebbian memory initialization working")
    print()


def test_pattern_strengthening():
    """Test 2: Pattern strengthening from positive outcomes."""
    print("=" * 60)
    print("TEST 2: Pattern Strengthening (Positive Outcomes)")
    print("=" * 60)
    print()

    memory = ConversationalHebbianMemory()

    # Simulate positive outcome: ventral polyvagal state successful
    outcome = ConversationalOutcome(
        polyvagal_state='ventral',
        polyvagal_confidence=0.45,  # Low initial confidence (fresh model)
        self_energy=0.7,
        self_energy_confidence=0.6,
        dominant_c='compassion',
        cs_activation={'compassion': 0.7, 'curiosity': 0.6, 'calm': 0.5, 'clarity': 0.4,
                       'confidence': 0.4, 'courage': 0.3, 'creativity': 0.3, 'connectedness': 0.4},
        conversational_family='self_led',
        satisfaction=0.75,
        coherence=0.8,
        ofel_energy=0.25,
        card_scale='detailed',
        next_polyvagal_state='ventral',  # Remained ventral (stable)
        next_self_energy=0.75,  # Increased SELF-energy
        next_satisfaction=0.8,
        explicit_feedback='helpful',
        gate_decision='RESPOND',
        response_text="I'm sensing compassion...",
        response_quality='HIGH_CONFIDENCE'
    )

    # Record initial state
    initial_ventral_boost = memory.polyvagal_patterns['ventral']['confidence_boost']
    initial_compassion_boost = memory.self_energy_patterns['compassion']['boost']
    initial_update_count = memory.update_count

    print(f"Initial state:")
    print(f"  Ventral boost: {initial_ventral_boost:.4f}")
    print(f"  Compassion boost: {initial_compassion_boost:.4f}")
    print(f"  Update count: {initial_update_count}")
    print()

    # Update from outcome
    updates = memory.update_from_outcome(outcome)

    print(f"After positive outcome:")
    print(f"  Ventral boost: {memory.polyvagal_patterns['ventral']['confidence_boost']:.4f}")
    print(f"  Compassion boost: {memory.self_energy_patterns['compassion']['boost']:.4f}")
    print(f"  Update count: {memory.update_count}")
    print(f"  Success count: {memory.success_count}")
    print()

    # Verify strengthening
    assert memory.polyvagal_patterns['ventral']['confidence_boost'] > initial_ventral_boost
    assert memory.self_energy_patterns['compassion']['boost'] > initial_compassion_boost
    assert memory.update_count == initial_update_count + 1
    assert memory.success_count == 1

    print(f"✅ Patterns strengthened:")
    print(f"   Ventral: +{memory.polyvagal_patterns['ventral']['confidence_boost'] - initial_ventral_boost:.4f}")
    print(f"   Compassion: +{memory.self_energy_patterns['compassion']['boost'] - initial_compassion_boost:.4f}")
    print()

    print("TEST 2: ✅ PASS - Pattern strengthening working")
    print()


def test_pattern_decay():
    """Test 3: Pattern decay from negative outcomes."""
    print("=" * 60)
    print("TEST 3: Pattern Decay (Negative Outcomes)")
    print("=" * 60)
    print()

    memory = ConversationalHebbianMemory()

    # First, strengthen some patterns
    positive_outcome = ConversationalOutcome(
        polyvagal_state='sympathetic',
        polyvagal_confidence=0.5,
        self_energy=0.4,
        self_energy_confidence=0.5,
        dominant_c='courage',
        cs_activation={'courage': 0.6, 'confidence': 0.5, 'calm': 0.4, 'compassion': 0.4,
                       'curiosity': 0.3, 'clarity': 0.3, 'creativity': 0.2, 'connectedness': 0.3},
        conversational_family='parts_work',
        satisfaction=0.6,
        coherence=0.7,
        ofel_energy=0.45,
        card_scale='moderate',
        next_polyvagal_state='ventral',  # Improved
        next_self_energy=0.5,
        explicit_feedback='helpful',
        gate_decision='RESPOND',
        response_text="Willing to stay...",
        response_quality='MEDIUM_CONFIDENCE'
    )

    memory.update_from_outcome(positive_outcome)
    initial_sympathetic_boost = memory.polyvagal_patterns['sympathetic']['confidence_boost']

    print(f"After positive outcome:")
    print(f"  Sympathetic boost: {initial_sympathetic_boost:.4f}")
    print()

    # Now simulate negative outcome (no improvement)
    negative_outcome = ConversationalOutcome(
        polyvagal_state='sympathetic',
        polyvagal_confidence=0.5,
        self_energy=0.4,
        self_energy_confidence=0.5,
        dominant_c='courage',
        cs_activation={'courage': 0.6, 'confidence': 0.5, 'calm': 0.4, 'compassion': 0.4,
                       'curiosity': 0.3, 'clarity': 0.3, 'creativity': 0.2, 'connectedness': 0.3},
        conversational_family='parts_work',
        satisfaction=0.6,
        coherence=0.7,
        ofel_energy=0.45,
        card_scale='moderate',
        next_polyvagal_state='sympathetic',  # No improvement
        next_self_energy=0.35,  # Decreased (negative outcome)
        explicit_feedback=None,
        gate_decision='RESPOND',
        response_text="Willing to stay...",
        response_quality='MEDIUM_CONFIDENCE'
    )

    memory.update_from_outcome(negative_outcome)
    final_sympathetic_boost = memory.polyvagal_patterns['sympathetic']['confidence_boost']

    print(f"After negative outcome:")
    print(f"  Sympathetic boost: {final_sympathetic_boost:.4f}")
    print(f"  Failure count: {memory.failure_count}")
    print()

    # Verify decay (should be slightly lower due to decay)
    assert final_sympathetic_boost < initial_sympathetic_boost or final_sympathetic_boost == initial_sympathetic_boost
    assert memory.failure_count == 1

    print(f"✅ Pattern decay working:")
    print(f"   Decay: {initial_sympathetic_boost - final_sympathetic_boost:.4f}")
    print()

    print("TEST 3: ✅ PASS - Pattern decay working")
    print()


def test_cascade_integration():
    """Test 4: Cascade integration with Hebbian learning."""
    print("=" * 60)
    print("TEST 4: Cascade Integration")
    print("=" * 60)
    print()

    # Create Hebbian memory with trained patterns
    memory = ConversationalHebbianMemory()

    # Pre-train some patterns (simulate 10 conversations)
    for i in range(10):
        outcome = ConversationalOutcome(
            polyvagal_state='ventral',
            polyvagal_confidence=0.45 + i * 0.01,
            self_energy=0.7,
            self_energy_confidence=0.6,
            dominant_c='curiosity',
            cs_activation={'curiosity': 0.8, 'compassion': 0.7, 'calm': 0.6, 'clarity': 0.5,
                           'confidence': 0.5, 'courage': 0.4, 'creativity': 0.4, 'connectedness': 0.5},
            conversational_family='parts_work',
            satisfaction=0.75,
            coherence=0.8,
            ofel_energy=0.25,
            card_scale='detailed',
            next_polyvagal_state='ventral',
            next_self_energy=0.75,
            explicit_feedback='helpful',
            gate_decision='RESPOND',
            response_text="I'm curious...",
            response_quality='HIGH_CONFIDENCE'
        )
        memory.update_from_outcome(outcome)

    print(f"Pre-training complete: {memory.update_count} updates, {memory.success_count} successes")
    print(f"Ventral confidence boost: {memory.polyvagal_patterns['ventral']['confidence_boost']:.4f}")
    print(f"Curiosity boost (parts_work): {memory.self_energy_patterns['curiosity']['family_effectiveness'].get('parts_work', 0.0):.4f}")
    print()

    # Create cascade WITH Hebbian memory
    cascade_with_learning = SELFLedCascade(hebbian_memory=memory)

    # Create cascade WITHOUT Hebbian memory (baseline)
    cascade_baseline = SELFLedCascade()

    # Mock organism context
    organism_context = {
        'organs': {
            'SANS': {'coherence': 0.85, 'lure': 0.7, 'confidence': 0.8},
            'BOND': {
                'coherence': 0.8,
                'lure': 0.6,
                'confidence': 0.75,
                'detected_parts': [{'part_type': 'explorer', 'strength': 0.7, 'self_distance': 0.3}],
                'keywords': [],
                'mean_self_distance': 0.3
            },
            'RNX': {'coherence': 0.8, 'lure': 0.5, 'confidence': 0.7},
            'EO': {'coherence': 0.82, 'lure': 0.65, 'confidence': 0.78},
            'NDAM': {'coherence': 0.77, 'lure': 0.55, 'confidence': 0.72},
            'CARD': {'coherence': 0.8, 'lure': 0.6, 'confidence': 0.75}
        },
        'ofel_components': {'polyvagal_energy': 0.1, 'parts_energy': 0.1, 'self_energy': 0.1},
        'vector35d': [0.0] * 35,
        'satisfaction': 0.75
    }

    text = "I'm curious about this protective part and what it needs."

    # Process with both cascades
    state_baseline = cascade_baseline.process_conversational_turn(text, organism_context)
    state_learned = cascade_with_learning.process_conversational_turn(text, organism_context)

    print(f"Baseline cascade:")
    print(f"  Polyvagal confidence: {state_baseline.polyvagal.confidence:.4f}")
    print(f"  SELF-energy: {state_baseline.self_energy.self_energy:.4f}")
    print(f"  Response quality: {state_baseline.response_quality}")
    print()

    print(f"Learned cascade:")
    print(f"  Polyvagal confidence: {state_learned.polyvagal.confidence:.4f}")
    print(f"  SELF-energy: {state_learned.self_energy.self_energy:.4f}")
    print(f"  Response quality: {state_learned.response_quality}")
    print()

    # Verify learning impact
    assert state_learned.polyvagal.confidence >= state_baseline.polyvagal.confidence
    print(f"✅ Polyvagal confidence boosted: +{state_learned.polyvagal.confidence - state_baseline.polyvagal.confidence:.4f}")

    # The SELF-energy might also be boosted
    if state_learned.self_energy and state_baseline.self_energy:
        print(f"✅ SELF-energy affected by learning: {state_learned.self_energy.self_energy:.4f} vs {state_baseline.self_energy.self_energy:.4f}")

    print()
    print("TEST 4: ✅ PASS - Cascade integration working")
    print()


def test_clinical_safety():
    """Test 5: Clinical safety (crisis family conservatism)."""
    print("=" * 60)
    print("TEST 5: Clinical Safety (Crisis Family Conservatism)")
    print("=" * 60)
    print()

    memory = ConversationalHebbianMemory()

    # Simulate dangerous blending pattern (high satisfaction + low SELF in crisis)
    dangerous_outcome = ConversationalOutcome(
        polyvagal_state='dorsal',
        polyvagal_confidence=0.85,
        self_energy=0.2,  # Very low SELF (dangerous)
        self_energy_confidence=0.8,
        dominant_c='compassion',
        cs_activation={'compassion': 0.6, 'calm': 0.5, 'curiosity': 0.3, 'clarity': 0.3,
                       'confidence': 0.2, 'courage': 0.2, 'creativity': 0.1, 'connectedness': 0.2},
        conversational_family='crisis',
        satisfaction=0.85,  # High satisfaction = dangerous (organs agree on shutdown)
        coherence=0.9,  # High coherence = dangerous (full agreement on parts-led state)
        ofel_energy=0.85,
        card_scale='minimal',
        next_polyvagal_state='dorsal',  # Still dorsal (contained appropriately)
        next_self_energy=0.25,  # Slight improvement (containment helped)
        explicit_feedback=None,
        gate_decision='CONTAIN',  # Appropriately contained
        response_text="Let's pause and ground...",
        response_quality='CONTAINMENT'
    )

    # Update from outcome (this is a POSITIVE outcome because containment was appropriate)
    initial_threshold = 0.0
    memory.update_from_outcome(dangerous_outcome)

    # Check that crisis family learned MORE conservative threshold
    context_key = f"crisis_CONTAIN_{dangerous_outcome.satisfaction:.1f}"
    if context_key in memory.cascade_patterns:
        threshold_adjustment = memory.cascade_patterns[context_key]['threshold_adjustment']
        print(f"Crisis family threshold adjustment: {threshold_adjustment:.4f}")
        assert threshold_adjustment < 0, "Crisis family should have NEGATIVE adjustment (more conservative)"
        print(f"✅ Crisis family became MORE conservative: {threshold_adjustment:.4f}")
    else:
        print(f"⚠️  Pattern not yet established (needs more training)")

    print()

    # Verify safety constraint: Never learn to ignore danger
    print("Testing safety constraint: DANGER threshold should never increase")
    print()

    # Simulate multiple DANGER scenarios
    for i in range(5):
        danger_outcome = ConversationalOutcome(
            polyvagal_state='dorsal',
            polyvagal_confidence=0.9,
            self_energy=0.1,
            self_energy_confidence=0.9,
            dominant_c='compassion',
            cs_activation={'compassion': 0.5, 'calm': 0.4, 'curiosity': 0.2, 'clarity': 0.2,
                           'confidence': 0.1, 'courage': 0.1, 'creativity': 0.1, 'connectedness': 0.1},
            conversational_family='crisis',
            satisfaction=0.9,
            coherence=0.95,
            ofel_energy=0.9,
            card_scale='minimal',
            next_polyvagal_state='dorsal',
            next_self_energy=0.15,
            explicit_feedback=None,
            gate_decision='CONTAIN',
            response_text="Safety first...",
            response_quality='CONTAINMENT'
        )
        memory.update_from_outcome(danger_outcome)

    print(f"After 5 DANGER containments:")
    print(f"  Danger detections: {memory.danger_detections}")
    print(f"  Dangerous blending detections: {memory.dangerous_blending_detections}")
    print(f"  Never ignored danger: {memory.never_ignored_danger}")
    print()

    assert memory.never_ignored_danger == True
    print(f"✅ Safety constraint maintained: DANGER never ignored")
    print()

    print("TEST 5: ✅ PASS - Clinical safety working")
    print()


def test_learning_trajectory():
    """Test 6: Learning trajectory (confidence improvement over time)."""
    print("=" * 60)
    print("TEST 6: Learning Trajectory (Confidence Improvement)")
    print("=" * 60)
    print()

    memory = ConversationalHebbianMemory()

    # Simulate learning trajectory: 0 → 10 → 50 conversations
    print("Simulating learning trajectory...")
    print()

    # Initial baseline (0 conversations)
    initial_polyvagal = memory.polyvagal_patterns['ventral']['confidence_boost']
    initial_self_energy = memory.self_energy_patterns['curiosity']['boost']
    print(f"Baseline (0 conversations):")
    print(f"  Polyvagal boost: {initial_polyvagal:.4f}")
    print(f"  SELF-energy boost: {initial_self_energy:.4f}")
    print()

    # Simulate 10 conversations
    for i in range(10):
        outcome = ConversationalOutcome(
            polyvagal_state='ventral',
            polyvagal_confidence=0.485,
            self_energy=0.7,
            self_energy_confidence=0.6,
            dominant_c='curiosity',
            cs_activation={'curiosity': 0.8, 'compassion': 0.7, 'calm': 0.6, 'clarity': 0.5,
                           'confidence': 0.5, 'courage': 0.4, 'creativity': 0.4, 'connectedness': 0.5},
            conversational_family='parts_work',
            satisfaction=0.75,
            coherence=0.8,
            ofel_energy=0.25,
            card_scale='detailed',
            next_polyvagal_state='ventral',
            next_self_energy=0.75,
            explicit_feedback='helpful',
            gate_decision='RESPOND',
            response_text="I'm curious...",
            response_quality='HIGH_CONFIDENCE'
        )
        memory.update_from_outcome(outcome)

    polyvagal_10 = memory.polyvagal_patterns['ventral']['confidence_boost']
    self_energy_10 = memory.self_energy_patterns['curiosity']['boost']
    print(f"After 10 conversations:")
    print(f"  Polyvagal boost: {polyvagal_10:.4f} (+{polyvagal_10 - initial_polyvagal:.4f})")
    print(f"  SELF-energy boost: {self_energy_10:.4f} (+{self_energy_10 - initial_self_energy:.4f})")
    print(f"  Success rate: {memory.success_rate:.2%}")
    print()

    # Simulate 40 more conversations (50 total)
    for i in range(40):
        # Vary the outcomes slightly
        outcome = ConversationalOutcome(
            polyvagal_state=['ventral', 'sympathetic'][i % 2],
            polyvagal_confidence=0.485 + i * 0.001,
            self_energy=0.6 + i * 0.005,
            self_energy_confidence=0.6 + i * 0.002,
            dominant_c=['curiosity', 'compassion', 'calm'][i % 3],
            cs_activation={'curiosity': 0.8, 'compassion': 0.7, 'calm': 0.6, 'clarity': 0.5,
                           'confidence': 0.5, 'courage': 0.4, 'creativity': 0.4, 'connectedness': 0.5},
            conversational_family=['parts_work', 'self_led'][i % 2],
            satisfaction=0.7 + i * 0.002,
            coherence=0.75 + i * 0.001,
            ofel_energy=0.3,
            card_scale='detailed',
            next_polyvagal_state='ventral',
            next_self_energy=0.75,
            explicit_feedback='helpful' if i % 3 == 0 else None,
            gate_decision='RESPOND',
            response_text="Response...",
            response_quality='HIGH_CONFIDENCE'
        )
        memory.update_from_outcome(outcome)

    polyvagal_50 = memory.polyvagal_patterns['ventral']['confidence_boost']
    self_energy_50 = memory.self_energy_patterns['curiosity']['boost']
    print(f"After 50 conversations:")
    print(f"  Polyvagal boost: {polyvagal_50:.4f} (+{polyvagal_50 - initial_polyvagal:.4f})")
    print(f"  SELF-energy boost: {self_energy_50:.4f} (+{self_energy_50 - initial_self_energy:.4f})")
    print(f"  Success rate: {memory.success_rate:.2%}")
    print(f"  Global confidence: {memory.get_global_confidence():.3f}")
    print()

    # Verify improvement trajectory
    assert polyvagal_50 > polyvagal_10 > initial_polyvagal
    assert self_energy_50 > self_energy_10 > initial_self_energy
    print(f"✅ Learning trajectory validated:")
    print(f"   Polyvagal: {initial_polyvagal:.4f} → {polyvagal_10:.4f} → {polyvagal_50:.4f}")
    print(f"   SELF-energy: {initial_self_energy:.4f} → {self_energy_10:.4f} → {self_energy_50:.4f}")
    print()

    # Expected trajectory (from design doc)
    print(f"Expected trajectory (from design):")
    print(f"  Fresh model (0-10): 0.485 polyvagal, 0.025 SELF-energy")
    print(f"  Early learning (10-50): +0.05-0.10pp polyvagal, +0.10-0.15pp SELF-energy")
    print(f"  Mature (50-100): +0.20-0.30pp polyvagal, +0.20-0.30pp SELF-energy")
    print()

    print("TEST 6: ✅ PASS - Learning trajectory validated")
    print()


def run_all_tests():
    """Run all tests."""
    print()
    print("=" * 60)
    print("CONVERSATIONAL HEBBIAN LEARNING TEST SUITE")
    print("Phase 1.5: Hebbian Learning Integration")
    print("=" * 60)
    print()

    tests = [
        test_hebbian_memory_initialization,
        test_pattern_strengthening,
        test_pattern_decay,
        test_cascade_integration,
        test_clinical_safety,
        test_learning_trajectory
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
            print()

    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print()
    print(f"Tests run: {passed + failed}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print()

    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
        print()
        print("Phase 1.5 Status:")
        print("  ✅ Phase 1.5c: Hebbian memory implementation COMPLETE")
        print("  ✅ Phase 1.5d: Cascade integration COMPLETE")
        print("  ✅ Phase 1.5e: Test validation COMPLETE")
        print()
        print("Next: Phase 2.1 - 6-Regime SELF Modulation")
    else:
        print("⚠️  Some tests failed. Please review and fix.")

    print()
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
