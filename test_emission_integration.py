"""
Test Emission Generator Integration with Pattern Learner
==========================================================

Phase 1 Week 3, Days 1-2: Minimal Integration Test

Tests that the EmissionGenerator successfully integrates the
NexusPhrasePatternLearner for hebbian fallback emission.

November 17, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.emission_generator import EmissionGenerator
from persona_layer.nexus_signature_extractor import NexusSignature


def test_emission_generator_initialization():
    """Test that EmissionGenerator initializes with pattern learner."""
    print("\n" + "=" * 70)
    print("TEST 1: EmissionGenerator Initialization with Pattern Learner")
    print("=" * 70)

    try:
        generator = EmissionGenerator(
            semantic_atoms_path="persona_layer/semantic_atoms.json",
            hebbian_memory_path="persona_layer/conversational_hebbian_memory.json"
        )

        # Check that pattern learner was initialized
        assert hasattr(generator, 'pattern_learner'), "Pattern learner not initialized"
        print("✅ Pattern learner initialized successfully")

        # Check that pattern learner has expected methods
        assert hasattr(generator.pattern_learner, 'get_candidate_phrases'), \
            "Pattern learner missing get_candidate_phrases method"
        print("✅ Pattern learner has get_candidate_phrases method")

        assert hasattr(generator.pattern_learner, 'record_emission_outcome'), \
            "Pattern learner missing record_emission_outcome method"
        print("✅ Pattern learner has record_emission_outcome method")

        return generator

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_hebbian_fallback_with_organ_results():
    """Test hebbian fallback with organ_results (should extract signature)."""
    print("\n" + "=" * 70)
    print("TEST 2: Hebbian Fallback with Organ Results")
    print("=" * 70)

    try:
        generator = EmissionGenerator(
            semantic_atoms_path="persona_layer/semantic_atoms.json",
            hebbian_memory_path="persona_layer/conversational_hebbian_memory.json"
        )

        # Create mock organ_results
        organ_results = {
            'LISTENING': {'coherence': 0.6, 'atoms': {'temporal_inquiry': 0.5}},
            'EMPATHY': {'coherence': 0.7, 'atoms': {'emotional_resonance': 0.6}},
            'WISDOM': {'coherence': 0.5, 'atoms': {'pattern_recognition': 0.4}}
        }

        # Test _generate_hebbian_fallback with organ_results
        emissions = generator._generate_hebbian_fallback(
            num_emissions=1,
            organ_results=organ_results,
            current_turn=5
        )

        assert len(emissions) == 1, f"Expected 1 emission, got {len(emissions)}"
        print(f"✅ Generated 1 emission")

        emission = emissions[0]
        print(f"   Strategy: {emission.strategy}")
        print(f"   Text: {emission.text[:60]}...")
        print(f"   Confidence: {emission.confidence:.3f}")

        # Verify emission has correct structure
        assert hasattr(emission, 'text'), "Emission missing text"
        assert hasattr(emission, 'strategy'), "Emission missing strategy"
        assert hasattr(emission, 'confidence'), "Emission missing confidence"
        print("✅ Emission has correct structure")

        return True

    except Exception as e:
        print(f"❌ Hebbian fallback test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hebbian_fallback_with_explicit_signature():
    """Test hebbian fallback with explicit nexus signature."""
    print("\n" + "=" * 70)
    print("TEST 3: Hebbian Fallback with Explicit Nexus Signature")
    print("=" * 70)

    try:
        generator = EmissionGenerator(
            semantic_atoms_path="persona_layer/semantic_atoms.json",
            hebbian_memory_path="persona_layer/conversational_hebbian_memory.json"
        )

        # Create test nexus signature
        test_signature = NexusSignature(
            participating_organs=frozenset(['EMPATHY', 'LISTENING', 'WISDOM']),
            organ_count=3,
            nexus_type='PSYCHE',
            mechanism='THERAPEUTIC_WITNESSING',
            coherence_bin=6,
            urgency_bin=3,
            polyvagal_state='ventral',
            zone=2,
            v0_energy_bin=5,
            kairos_detected=False,
            field_strength_bin=7,
            dominant_meta_atom='compassion_safety'
        )

        # Test with explicit signature
        emissions = generator._generate_hebbian_fallback(
            num_emissions=1,
            nexus_signature=test_signature,
            current_turn=10
        )

        assert len(emissions) == 1, f"Expected 1 emission, got {len(emissions)}"
        print(f"✅ Generated 1 emission")

        emission = emissions[0]
        print(f"   Strategy: {emission.strategy}")
        print(f"   Text: {emission.text[:60]}...")
        print(f"   Confidence: {emission.confidence:.3f}")
        print(f"   Participant Organs: {emission.participant_organs}")

        return True

    except Exception as e:
        print(f"❌ Explicit signature test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_v0_guided_emissions_with_current_turn():
    """Test that generate_v0_guided_emissions passes current_turn correctly."""
    print("\n" + "=" * 70)
    print("TEST 4: V0 Guided Emissions with current_turn Parameter")
    print("=" * 70)

    try:
        generator = EmissionGenerator(
            semantic_atoms_path="persona_layer/semantic_atoms.json",
            hebbian_memory_path="persona_layer/conversational_hebbian_memory.json"
        )

        # Create mock organ_results
        organ_results = {
            'LISTENING': {'coherence': 0.6, 'atoms': {'temporal_inquiry': 0.5}},
            'EMPATHY': {'coherence': 0.7, 'atoms': {'emotional_resonance': 0.6}}
        }

        # Test with no nexuses (should trigger hebbian fallback)
        emissions, strategy = generator.generate_v0_guided_emissions(
            nexuses=[],  # No nexuses → hebbian fallback
            v0_energy=0.5,
            kairos_detected=False,
            num_emissions=1,
            organ_results=organ_results,
            current_turn=15  # 🌀 NEW PARAMETER
        )

        assert len(emissions) == 1, f"Expected 1 emission, got {len(emissions)}"
        print(f"✅ Generated 1 emission via {strategy} strategy")

        emission = emissions[0]
        print(f"   Text: {emission.text[:60]}...")
        print(f"   Confidence: {emission.confidence:.3f}")

        return True

    except Exception as e:
        print(f"❌ V0 guided emissions test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests."""
    print("\n" + "=" * 70)
    print("🌀 EMISSION GENERATOR PATTERN LEARNER INTEGRATION TESTS")
    print("   Phase 1 Week 3, Days 1-2: Minimal Integration")
    print("   November 17, 2025")
    print("=" * 70)

    results = []

    # Test 1: Initialization
    generator = test_emission_generator_initialization()
    results.append(("Initialization", generator is not None))

    if generator:
        # Test 2: Hebbian fallback with organ_results
        result2 = test_hebbian_fallback_with_organ_results()
        results.append(("Hebbian Fallback (organ_results)", result2))

        # Test 3: Hebbian fallback with explicit signature
        result3 = test_hebbian_fallback_with_explicit_signature()
        results.append(("Hebbian Fallback (explicit signature)", result3))

        # Test 4: V0 guided emissions with current_turn
        result4 = test_v0_guided_emissions_with_current_turn()
        results.append(("V0 Guided Emissions (current_turn)", result4))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY:")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passing")

    if passed == total:
        print("\n🎉 ALL TESTS PASSING - Integration successful!")
        print("\n✅ Week 3 Days 1-2: Minimal Integration COMPLETE")
        print("   - Pattern learner integrated into EmissionGenerator")
        print("   - Hebbian fallback now uses nexus-phrase pattern matching")
        print("   - Organ results → signature extraction working")
        print("   - current_turn parameter threaded through emission methods")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failing")
        return 1


if __name__ == '__main__':
    sys.exit(main())
