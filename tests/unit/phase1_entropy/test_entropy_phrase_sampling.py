"""
Unit Test: Phase 1 Surface Entropy - Phrase Sampling
=====================================================

Tests regime-adaptive phrase sampling in emission generator.

Verifies:
- Softmax sampling with temperature control
- Regime-adaptive exploration factors
- Safety gates (crisis contexts)
- Hebbian weight integration

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: 1 (Surface Entropy)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
from collections import Counter

# Import entropy config
from persona_layer.epoch_training.entropy_config import EntropyConfig

# Import emission generator (will test _softmax_sample_phrase)
from persona_layer.emission_generator import EmissionGenerator
from config import Config


def test_entropy_config():
    """Test 1: EntropyConfig regime mapping."""
    print("\n" + "="*70)
    print("TEST 1: Entropy Config Regime Mapping")
    print("="*70)

    config = EntropyConfig()

    # Test regime exploration factors
    regimes_expected = {
        'INITIALIZING': 0.20,
        'EXPLORING': 0.30,
        'CONVERGING': 0.12,
        'STABLE': 0.05,
        'COMMITTED': 0.01,
        'PLATEAUED': 0.25,
    }

    for regime, expected_factor in regimes_expected.items():
        actual_factor = config.get_exploration_factor(regime_str=regime)
        assert actual_factor == expected_factor, f"{regime}: expected {expected_factor}, got {actual_factor}"
        print(f"   ✅ {regime:15s}: exploration={actual_factor:.2f}")

    print("\n✅ TEST 1 PASSED - Regime mapping correct")


def test_safety_gates():
    """Test 2: Crisis safety gates."""
    print("\n" + "="*70)
    print("TEST 2: Crisis Safety Gates")
    print("="*70)

    config = EntropyConfig()

    # Test crisis urgency gate
    factor_crisis_urgency = config.get_exploration_factor(
        regime_str='EXPLORING',
        ndam_urgency=0.8,  # Above threshold (0.7)
        crisis_zone=0
    )
    assert factor_crisis_urgency == 0.0, "Should disable exploration during crisis urgency"
    print(f"   ✅ Crisis urgency (0.8): exploration={factor_crisis_urgency:.2f} (DISABLED)")

    # Test crisis zone gate
    factor_crisis_zone = config.get_exploration_factor(
        regime_str='EXPLORING',
        ndam_urgency=0.3,
        crisis_zone=5  # At threshold (5)
    )
    assert factor_crisis_zone == 0.0, "Should disable exploration in crisis zone"
    print(f"   ✅ Crisis zone (5): exploration={factor_crisis_zone:.2f} (DISABLED)")

    # Test safe context
    factor_safe = config.get_exploration_factor(
        regime_str='EXPLORING',
        ndam_urgency=0.3,
        crisis_zone=2
    )
    assert factor_safe == 0.30, "Should enable exploration in safe context"
    print(f"   ✅ Safe context: exploration={factor_safe:.2f} (ENABLED)")

    print("\n✅ TEST 2 PASSED - Safety gates working")


def test_softmax_temperature():
    """Test 3: Temperature mapping."""
    print("\n" + "="*70)
    print("TEST 3: Softmax Temperature Mapping")
    print("="*70)

    config = EntropyConfig()

    # Test temperature extremes
    temp_high = config.get_softmax_temperature(exploration_factor=0.30)  # EXPLORING
    temp_low = config.get_softmax_temperature(exploration_factor=0.01)  # COMMITTED

    print(f"   High exploration (0.30): temperature={temp_high:.2f}")
    print(f"   Low exploration (0.01): temperature={temp_low:.2f}")

    assert temp_high > temp_low, "High exploration should have higher temperature"
    assert 1.8 <= temp_high <= 2.1, "High temperature should be ~2.0"
    assert 0.1 <= temp_low <= 0.3, "Low temperature should be ~0.1-0.3"

    print("\n✅ TEST 3 PASSED - Temperature mapping correct")


def test_softmax_phrase_sampling():
    """Test 4: Softmax phrase sampling with weights."""
    print("\n" + "="*70)
    print("TEST 4: Softmax Phrase Sampling")
    print("="*70)

    # Initialize emission generator
    generator = EmissionGenerator(
        semantic_atoms_path=Config.SEMANTIC_ATOMS_PATH,
        hebbian_memory_path=Config.HEBBIAN_MEMORY_PATH,
        entropy_config=EntropyConfig()  # Enable entropy
    )

    # Test phrases with Hebbian weights
    phrases = ["Tell me more", "I'm listening", "What's present?", "Say more", "I'm with you"]
    weights = [5.0, 3.0, 2.0, 1.5, 1.0]  # Hebbian frequencies (Tell me more most common)

    # Test HIGH exploration (EXPLORING regime)
    generator.set_exploration_context(regime='EXPLORING')
    samples_high = [generator._softmax_sample_phrase(phrases, weights=weights) for _ in range(100)]
    counts_high = Counter(samples_high)

    print(f"\n   HIGH exploration (EXPLORING, temp≈2.0):")
    for phrase in phrases:
        count = counts_high.get(phrase, 0)
        print(f"      '{phrase[:20]}': {count}/100 ({count}%)")

    # Should be more uniform (all phrases have reasonable chance)
    assert len(counts_high) >= 4, "High exploration should sample from multiple phrases"

    # Test LOW exploration (COMMITTED regime)
    generator.set_exploration_context(regime='COMMITTED')
    samples_low = [generator._softmax_sample_phrase(phrases, weights=weights) for _ in range(100)]
    counts_low = Counter(samples_low)

    print(f"\n   LOW exploration (COMMITTED, temp≈0.1-0.2):")
    for phrase in phrases:
        count = counts_low.get(phrase, 0)
        print(f"      '{phrase[:20]}': {count}/100 ({count}%)")

    # Should be more peaked (highest weight phrase dominates)
    top_phrase = counts_low.most_common(1)[0][0]
    assert top_phrase == "Tell me more", "Low exploration should favor highest Hebbian weight"
    assert counts_low["Tell me more"] >= 60, "Low exploration should strongly bias highest weight"

    print("\n✅ TEST 4 PASSED - Softmax sampling respects regime + weights")


def test_crisis_disables_exploration():
    """Test 5: Crisis contexts disable exploration."""
    print("\n" + "="*70)
    print("TEST 5: Crisis Contexts Disable Exploration")
    print("="*70)

    generator = EmissionGenerator(
        semantic_atoms_path=Config.SEMANTIC_ATOMS_PATH,
        hebbian_memory_path=Config.HEBBIAN_MEMORY_PATH,
        entropy_config=EntropyConfig()
    )

    phrases = ["Tell me more", "I'm listening", "What's present?"]
    weights = [5.0, 3.0, 1.0]

    # Set crisis context
    generator.set_exploration_context(
        regime='EXPLORING',  # Would normally have high exploration
        ndam_urgency=0.8,  # Crisis!
        crisis_zone=0
    )

    samples = [generator._softmax_sample_phrase(phrases, weights=weights) for _ in range(100)]
    counts = Counter(samples)

    print(f"\n   Crisis (urgency=0.8, regime=EXPLORING):")
    for phrase in phrases:
        count = counts.get(phrase, 0)
        print(f"      '{phrase[:20]}': {count}/100")

    # Should behave like COMMITTED (very low exploration)
    assert counts["Tell me more"] >= 60, "Crisis should disable exploration, favor Hebbian strongest"

    print("\n✅ TEST 5 PASSED - Crisis contexts disable exploration")


def run_all_tests():
    """Run all Phase 1 entropy tests."""
    print("\n" + "="*70)
    print("🎲 PHASE 1 SURFACE ENTROPY: UNIT TESTS")
    print("="*70)
    print("\nTesting: Regime-Adaptive Phrase Sampling")
    print("Component: EntropyConfig + EmissionGenerator._softmax_sample_phrase")

    try:
        # Test 1: Config
        test_entropy_config()

        # Test 2: Safety gates
        test_safety_gates()

        # Test 3: Temperature
        test_softmax_temperature()

        # Test 4: Phrase sampling
        test_softmax_phrase_sampling()

        # Test 5: Crisis disables exploration
        test_crisis_disables_exploration()

        # Final summary
        print("\n" + "="*70)
        print("✅ ALL PHASE 1 ENTROPY TESTS PASSED")
        print("="*70)
        print("\n📊 Verified:")
        print("   ✅ Regime-to-exploration mapping (6 regimes)")
        print("   ✅ Safety gates (crisis urgency + zone)")
        print("   ✅ Temperature scaling (exploration → temperature)")
        print("   ✅ Softmax phrase sampling (HIGH vs LOW exploration)")
        print("   ✅ Hebbian weight integration")
        print("   ✅ Crisis contexts disable exploration")

        print("\n🌀 Phase 1 Surface Entropy:")
        print("   • EXPLORING → HIGH exploration (temp≈2.0)")
        print("   • COMMITTED → LOW exploration (temp≈0.1-0.2)")
        print("   • Crisis contexts → NO exploration (safety gate)")
        print("   • Hebbian weights respected (organic learning)")
        print("   • Voice development enabled ✓")

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
