"""
Test Regime-Based Confidence Modulation (Enhancement #1)
November 13, 2025

Quick test to validate that regime-based confidence modulation is working correctly.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.epoch_training.satisfaction_regime import SatisfactionRegime
from persona_layer.emission_generator import EmissionGenerator
from config import Config


def test_regime_confidence_modulation():
    """Test that regime modulation correctly adjusts confidence."""
    print("="*70)
    print("🧪 Testing Regime-Based Confidence Modulation (Enhancement #1)")
    print("="*70)

    # Initialize emission generator
    print("\n1. Initializing emission generator...")
    emission_gen = EmissionGenerator(
        semantic_atoms_path="persona_layer/semantic_atoms.json",
        hebbian_memory_path="persona_layer/conversational_hebbian_memory.json"
    )

    # Test base confidence value
    base_confidence = 0.60
    print(f"\n2. Base confidence: {base_confidence:.3f}")

    # Test each regime
    print("\n3. Testing confidence modulation per regime:")
    print("-"*70)

    test_cases = [
        (SatisfactionRegime.INITIALIZING, 0.80, "Conservative - system warming up"),
        (SatisfactionRegime.EXPLORING, 0.90, "Slight caution - active search"),
        (SatisfactionRegime.CONVERGING, 1.00, "Neutral - approaching target"),
        (SatisfactionRegime.STABLE, 1.15, "Boost - sweet spot ⭐"),
        (SatisfactionRegime.COMMITTED, 1.10, "Slight boost - sustained success"),
        (SatisfactionRegime.PLATEAUED, 0.85, "Pull back - escape local minimum")
    ]

    results = []
    for regime, expected_factor, description in test_cases:
        # Set regime
        emission_gen.set_exploration_context(regime=regime.value)

        # Apply modulation
        modulated = emission_gen._apply_regime_confidence_modulation(base_confidence)

        # Expected result
        expected = base_confidence * expected_factor
        expected = max(0.0, min(1.0, expected))

        # Validate
        match = abs(modulated - expected) < 0.001
        status = "✅" if match else "❌"

        results.append({
            'regime': regime.value,
            'modulated': modulated,
            'expected': expected,
            'match': match
        })

        print(f"{status} {regime.value:15s}: {base_confidence:.3f} → {modulated:.3f} "
              f"(expected: {expected:.3f}) | {description}")

    # Summary
    print("\n" + "="*70)
    passed = sum(1 for r in results if r['match'])
    total = len(results)

    if passed == total:
        print(f"✅ All {total}/{total} regime modulation tests PASSED!")
        print("\n📊 Regime modulation working correctly:")
        print(f"   - STABLE regime boosts confidence by 15% (sweet spot)")
        print(f"   - EXPLORING regime reduces by 10% (caution)")
        print(f"   - PLATEAUED regime reduces by 15% (escape)")
        return True
    else:
        print(f"❌ {passed}/{total} tests passed, {total-passed} FAILED")
        print("\nFailed tests:")
        for r in results:
            if not r['match']:
                print(f"   - {r['regime']}: got {r['modulated']:.3f}, expected {r['expected']:.3f}")
        return False


def test_no_regime_fallback():
    """Test that system works when no regime is set."""
    print("\n" + "="*70)
    print("🧪 Testing No-Regime Fallback (default behavior)")
    print("="*70)

    emission_gen = EmissionGenerator(
        semantic_atoms_path="persona_layer/semantic_atoms.json",
        hebbian_memory_path="persona_layer/conversational_hebbian_memory.json"
    )

    # Don't set any regime (current_regime = None)
    base_confidence = 0.75
    modulated = emission_gen._apply_regime_confidence_modulation(base_confidence)

    if modulated == base_confidence:
        print(f"✅ No-regime fallback working: {base_confidence:.3f} → {modulated:.3f} (no change)")
        return True
    else:
        print(f"❌ No-regime fallback FAILED: {base_confidence:.3f} → {modulated:.3f} (should be unchanged)")
        return False


def test_config_mappings():
    """Test that config mappings are correct."""
    print("\n" + "="*70)
    print("🧪 Testing Config Regime Mappings")
    print("="*70)

    print("\n1. Confidence modulation mappings:")
    for regime, factor in Config.CONFIDENCE_MODULATION_BY_REGIME.items():
        print(f"   {regime:15s}: {factor:.2f}×")

    print("\n2. Learning rate modulation mappings:")
    for regime, rate in Config.LEARNING_RATE_BY_REGIME.items():
        print(f"   {regime:15s}: {rate:.2f}")

    # Validate all regimes present
    expected_regimes = {'INITIALIZING', 'EXPLORING', 'CONVERGING', 'STABLE', 'COMMITTED', 'PLATEAUED'}

    conf_regimes = set(Config.CONFIDENCE_MODULATION_BY_REGIME.keys())
    learning_regimes = set(Config.LEARNING_RATE_BY_REGIME.keys())

    if conf_regimes == expected_regimes and learning_regimes == expected_regimes:
        print(f"\n✅ All 6 regimes mapped correctly in config")
        return True
    else:
        missing_conf = expected_regimes - conf_regimes
        missing_learning = expected_regimes - learning_regimes
        print(f"\n❌ Missing regime mappings:")
        if missing_conf:
            print(f"   Confidence: {missing_conf}")
        if missing_learning:
            print(f"   Learning rate: {missing_learning}")
        return False


if __name__ == "__main__":
    print("\n🌀 DAE_HYPHAE_1 Enhancement #1: Regime-Based Confidence Modulation")
    print("   Test Suite - November 13, 2025\n")

    results = []

    # Run tests
    results.append(("Regime Confidence Modulation", test_regime_confidence_modulation()))
    results.append(("No-Regime Fallback", test_no_regime_fallback()))
    results.append(("Config Mappings", test_config_mappings()))

    # Final summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")

    print("\n" + "="*70)
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({total}/{total})")
        print("\n🎉 Enhancement #1 implementation validated!")
        print("   Regime-based confidence modulation ready for baseline training.")
        sys.exit(0)
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total} passed)")
        print(f"\n   Please fix {total-passed} failing test(s) before proceeding.")
        sys.exit(1)
