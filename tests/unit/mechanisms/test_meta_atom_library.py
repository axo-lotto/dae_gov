#!/usr/bin/env python3
"""
Test Meta-Atom Phrase Library Loading
======================================

Tests that the emission generator can:
1. Load the meta-atom phrase library
2. Generate phrases from meta-atoms with V0 modulation
3. Handle intensity selection correctly
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.emission_generator import EmissionGenerator
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MockNexus:
    """Mock nexus for testing meta-atom phrase generation."""
    atom: str
    participants: List[str]
    activations: Dict[str, float]
    emission_readiness: float
    coherence: float
    field_strength: float

def test_meta_atom_library_loading():
    """Test that meta-atom phrase library loads correctly."""
    print("="*80)
    print("🧪 TEST: Meta-Atom Phrase Library Loading")
    print("="*80)

    # Initialize emission generator
    try:
        generator = EmissionGenerator(
            semantic_atoms_path='persona_layer/semantic_atoms.json',
            hebbian_memory_path='persona_layer/conversational_hebbian_memory.json'
        )

        print(f"\n✅ EmissionGenerator initialized successfully")

        # Check if meta-atom phrases loaded
        if generator.meta_atom_phrases:
            print(f"✅ Meta-atom phrase library loaded: {len(generator.meta_atom_phrases)} meta-atoms")
            print(f"\nMeta-atoms available:")
            for atom_name in generator.meta_atom_phrases.keys():
                print(f"   - {atom_name}")
        else:
            print(f"❌ Meta-atom phrase library is empty!")
            return False

        # Check meta-atom names set
        print(f"\n✅ Meta-atom names set: {len(generator.meta_atom_names)} names")

        return True

    except Exception as e:
        print(f"\n❌ EmissionGenerator initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_meta_atom_phrase_generation():
    """Test generating phrases from meta-atoms with different V0 intensities."""
    print("\n" + "="*80)
    print("🧪 TEST: Meta-Atom Phrase Generation")
    print("="*80)

    # Initialize generator
    try:
        generator = EmissionGenerator(
            semantic_atoms_path='persona_layer/semantic_atoms.json',
            hebbian_memory_path='persona_layer/conversational_hebbian_memory.json'
        )
    except Exception as e:
        print(f"❌ Could not initialize generator: {e}")
        return False

    if not generator.meta_atom_phrases:
        print(f"❌ No meta-atom phrases loaded!")
        return False

    # Create mock meta-atom nexuses
    test_cases = [
        {
            'name': 'fierce_holding',
            'v0_energy': 0.8,  # High energy → high intensity
            'organs': ['EMPATHY', 'AUTHENTICITY', 'BOND'],
            'expected_intensity': 'high'
        },
        {
            'name': 'somatic_wisdom',
            'v0_energy': 0.5,  # Medium energy → medium intensity
            'organs': ['PRESENCE', 'BOND', 'EO'],
            'expected_intensity': 'medium'
        },
        {
            'name': 'trauma_aware',
            'v0_energy': 0.2,  # Low energy → low intensity
            'organs': ['BOND', 'EO', 'NDAM'],
            'expected_intensity': 'low'
        }
    ]

    all_passed = True

    for test_case in test_cases:
        print(f"\n📋 Test Case: {test_case['name']} (V0={test_case['v0_energy']})")
        print(f"   Expected intensity: {test_case['expected_intensity']}")

        # Create mock nexus
        mock_nexus = MockNexus(
            atom=test_case['name'],
            participants=test_case['organs'],
            activations={organ: 0.7 for organ in test_case['organs']},
            emission_readiness=0.65,  # High enough for direct emission
            coherence=0.80,
            field_strength=0.75
        )

        # Generate emissions
        try:
            emissions, path = generator.generate_v0_guided_emissions(
                nexuses=[mock_nexus],
                v0_energy=test_case['v0_energy'],
                kairos_detected=True,  # Test Kairos boost
                num_emissions=1
            )

            if emissions:
                emission = emissions[0]
                print(f"   ✅ Generated phrase: \"{emission.text}\"")
                print(f"   Strategy: {emission.strategy}")
                print(f"   Confidence: {emission.confidence:.3f}")
                print(f"   Path: {path}")

                # Verify it's using meta-atom strategy
                if emission.strategy == 'meta_atom':
                    print(f"   ✅ Using meta_atom strategy (correct!)")
                else:
                    print(f"   ⚠️  Using {emission.strategy} strategy (expected meta_atom)")
                    all_passed = False

            else:
                print(f"   ❌ No emissions generated!")
                all_passed = False

        except Exception as e:
            print(f"   ❌ Generation failed: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False

    return all_passed

def test_hebbian_fallback():
    """Test that Hebbian fallback still works when no nexuses."""
    print("\n" + "="*80)
    print("🧪 TEST: Hebbian Fallback (No Nexuses)")
    print("="*80)

    try:
        generator = EmissionGenerator(
            semantic_atoms_path='persona_layer/semantic_atoms.json',
            hebbian_memory_path='persona_layer/conversational_hebbian_memory.json'
        )

        # Generate with empty nexuses list
        emissions, path = generator.generate_v0_guided_emissions(
            nexuses=[],  # No nexuses → should use Hebbian fallback
            v0_energy=0.5,
            kairos_detected=False,
            num_emissions=2
        )

        if emissions:
            print(f"✅ Hebbian fallback generated {len(emissions)} phrases")
            print(f"   Path: {path}")
            for i, emission in enumerate(emissions, 1):
                print(f"   {i}. \"{emission.text}\" (strategy: {emission.strategy})")

            if path == 'hebbian':
                print(f"✅ Correct fallback path!")
                return True
            else:
                print(f"⚠️  Expected 'hebbian' path, got '{path}'")
                return False
        else:
            print(f"❌ No emissions generated!")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n🌀 TESTING META-ATOM PHRASE LIBRARY INTEGRATION 🌀\n")

    # Run tests
    test_results = []

    test_results.append(('Library Loading', test_meta_atom_library_loading()))
    test_results.append(('Phrase Generation', test_meta_atom_phrase_generation()))
    test_results.append(('Hebbian Fallback', test_hebbian_fallback()))

    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)

    for test_name, passed in test_results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")

    all_passed = all(result for _, result in test_results)

    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED! Meta-atom phrase library is operational.")
    else:
        print(f"\n⚠️  SOME TESTS FAILED. See details above.")

    print("\n" + "="*80)

    sys.exit(0 if all_passed else 1)
