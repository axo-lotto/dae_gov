#!/usr/bin/env python3
"""
Unit Tests for Nexus Signature Extractor

Tests 18D signature extraction, quantization, hashing, and fuzzy matching.

From REFINED_FOUNDATIONAL_INTELLIGENCE_SYNTHESIS_NOV17_2025.md Phase 1 Week 1
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from persona_layer.nexus_signature_extractor import (
    NexusSignature,
    NexusSignatureExtractor,
    get_default_extractor
)


def test_1_basic_extraction():
    """Test 1: Basic signature extraction from nexus + felt-state."""
    print("\n" + "="*80)
    print("🧪 TEST 1: Basic Signature Extraction")
    print("="*80)

    extractor = get_default_extractor()

    # Simulate nexus
    nexus = {
        'participating_organs': ['BOND', 'NDAM', 'EMPATHY'],
        'nexus_type': 'GUT_BOND_NDAM',
        'mechanism': 'protective_stasis'
    }

    # Simulate organ results
    organ_results = {
        'BOND': {'coherence': 0.85},
        'NDAM': {'coherence': 0.78},
        'EMPATHY': {'coherence': 0.82}
    }

    # Simulate felt-state
    felt_state = {
        'field_coherence': 0.81,
        'urgency': 0.75,
        'polyvagal_state': 'sympathetic',
        'zone': 4,
        'v0_final': 0.32,
        'kairos_detected': True,
        'dominant_meta_atom': 'fierce_holding'
    }

    sig = extractor.extract(nexus, organ_results, felt_state)

    print(f"\n✅ Extracted Signature:")
    print(f"   Organs: {sig.participating_organs}")
    print(f"   Organ Count: {sig.organ_count}")
    print(f"   Nexus Type: {sig.nexus_type}")
    print(f"   Mechanism: {sig.mechanism}")
    print(f"   Coherence Bin: {sig.coherence_bin} (from {felt_state['field_coherence']})")
    print(f"   Urgency Bin: {sig.urgency_bin} (from {felt_state['urgency']})")
    print(f"   Polyvagal: {sig.polyvagal_state}")
    print(f"   Zone: {sig.zone}")
    print(f"   V0 Bin: {sig.v0_energy_bin} (from {felt_state['v0_final']})")
    print(f"   Kairos: {sig.kairos_detected}")
    print(f"   Meta-Atom: {sig.dominant_meta_atom}")

    # Assertions
    assert sig.organ_count == 3
    assert sig.nexus_type == 'GUT_BOND_NDAM'
    assert sig.coherence_bin == 8  # 0.81 → bin 8
    assert sig.urgency_bin == 7  # 0.75 → bin 7
    assert sig.polyvagal_state == 'sympathetic'
    assert sig.zone == 4
    assert sig.kairos_detected == True

    print(f"\n✅ TEST 1 PASSED")
    return sig


def test_2_quantization():
    """Test 2: Quantization bin boundaries."""
    print("\n" + "="*80)
    print("🧪 TEST 2: Quantization Bin Boundaries")
    print("="*80)

    extractor = get_default_extractor()

    test_cases = [
        (0.0, 10, 0.0, 1.0, 0),  # Min boundary
        (0.05, 10, 0.0, 1.0, 0),  # Within first bin
        (0.10, 10, 0.0, 1.0, 1),  # Bin boundary
        (0.55, 10, 0.0, 1.0, 5),  # Mid-value
        (0.95, 10, 0.0, 1.0, 9),  # Within last bin
        (1.0, 10, 0.0, 1.0, 9),  # Max boundary
        (1.5, 10, 0.0, 1.0, 9),  # Overflow (clamped)
        (-0.5, 10, 0.0, 1.0, 0),  # Underflow (clamped)
    ]

    print(f"\n📊 Quantization Results:")
    for value, num_bins, min_val, max_val, expected_bin in test_cases:
        actual_bin = extractor._quantize(value, num_bins, min_val, max_val)
        status = "✅" if actual_bin == expected_bin else "❌"
        print(f"   {status} Value {value:.2f} → Bin {actual_bin} (expected {expected_bin})")
        assert actual_bin == expected_bin, f"Quantization failed: {value} → {actual_bin} (expected {expected_bin})"

    print(f"\n✅ TEST 2 PASSED")


def test_3_hashable_precision():
    """Test 3: Hashable tuple at different precisions."""
    print("\n" + "="*80)
    print("🧪 TEST 3: Hashable Tuple Precision Levels")
    print("="*80)

    sig = NexusSignature(
        participating_organs=frozenset({'BOND', 'NDAM'}),
        organ_count=2,
        nexus_type='GUT_BOND_NDAM',
        mechanism='protective_stasis',
        coherence_bin=8,
        urgency_bin=7,
        polyvagal_state='sympathetic',
        zone=4,
        v0_energy_bin=1,
        kairos_detected=True,
        field_strength_bin=3,
        dominant_meta_atom='fierce_holding',
        constraint_pattern='BOND_high_NDAM_high',
        transductive_vocabulary=frozenset({'signal_inflation'}),
        satisfaction_tier='medium',
        emission_path='organic',
        convergence_cycles=3,
        entity_context=frozenset({'Emma'})
    )

    # Low precision (4D)
    low_key = sig.to_hashable(precision='low')
    print(f"\n📊 Low Precision (4D): {len(low_key)} elements")
    print(f"   {low_key[:2]}")
    assert len(low_key) == 4

    # Medium precision (12D) - RECOMMENDED
    medium_key = sig.to_hashable(precision='medium')
    print(f"\n📊 Medium Precision (12D): {len(medium_key)} elements")
    print(f"   {medium_key[:4]}")
    assert len(medium_key) == 12

    # High precision (18D)
    high_key = sig.to_hashable(precision='high')
    print(f"\n📊 High Precision (18D): {len(high_key)} elements")
    print(f"   {high_key[:4]}")
    assert len(high_key) == 18

    # Verify hashable (can be used as dict key)
    test_dict = {
        low_key: 'low',
        medium_key: 'medium',
        high_key: 'high'
    }
    assert test_dict[low_key] == 'low'
    assert test_dict[medium_key] == 'medium'
    assert test_dict[high_key] == 'high'

    print(f"\n✅ TEST 3 PASSED")


def test_4_fuzzy_matching():
    """Test 4: Fuzzy match key generation."""
    print("\n" + "="*80)
    print("🧪 TEST 4: Fuzzy Match Key Generation")
    print("="*80)

    sig = NexusSignature(
        participating_organs=frozenset({'BOND', 'NDAM'}),
        organ_count=2,
        nexus_type='GUT_BOND_NDAM',
        mechanism='protective_stasis',
        coherence_bin=7,  # Will fuzz to [6,7,8]
        urgency_bin=3,    # Will fuzz to [2,3,4]
        polyvagal_state='sympathetic',
        zone=4,
        v0_energy_bin=1,
        kairos_detected=True,
        field_strength_bin=3,
        dominant_meta_atom='fierce_holding'
    )

    # Generate fuzzy keys (tolerance=1, only fuzz coherence + urgency)
    fuzzy_keys = sig.fuzzy_match_keys(tolerance=1, precision='medium')

    print(f"\n📊 Fuzzy Matching:")
    print(f"   Exact signature: coherence_bin={sig.coherence_bin}, urgency_bin={sig.urgency_bin}")
    print(f"   Generated {len(fuzzy_keys)} fuzzy keys")
    print(f"   Expected: 3 (coherence) × 3 (urgency) = 9 keys")

    # Should generate 3×3 = 9 fuzzy keys
    assert len(fuzzy_keys) == 9, f"Expected 9 fuzzy keys, got {len(fuzzy_keys)}"

    # Verify exact key is included
    exact_key = sig.to_hashable(precision='medium')
    assert exact_key in fuzzy_keys, "Exact key should be in fuzzy keys"

    # Verify bin variations
    coherence_bins = {key[4] for key in fuzzy_keys}  # Index 4 = coherence_bin
    urgency_bins = {key[5] for key in fuzzy_keys}     # Index 5 = urgency_bin

    print(f"   Coherence bins: {sorted(coherence_bins)} (expected [6,7,8])")
    print(f"   Urgency bins: {sorted(urgency_bins)} (expected [2,3,4])")

    assert coherence_bins == {6, 7, 8}
    assert urgency_bins == {2, 3, 4}

    print(f"\n✅ TEST 4 PASSED")


def test_5_fuzzy_clamping():
    """Test 5: Fuzzy matching with bin boundary clamping."""
    print("\n" + "="*80)
    print("🧪 TEST 5: Fuzzy Matching Boundary Clamping")
    print("="*80)

    # Edge case: coherence_bin=0 (at lower boundary)
    sig_low = NexusSignature(
        participating_organs=frozenset({'BOND'}),
        organ_count=1,
        nexus_type='GUT_BOND',
        mechanism='protective_stasis',
        coherence_bin=0,  # Will fuzz to [0,1] (clamped at 0)
        urgency_bin=5,
        polyvagal_state='dorsal',
        zone=5,
        v0_energy_bin=0,
        kairos_detected=False,
        field_strength_bin=0,
        dominant_meta_atom='none'
    )

    fuzzy_keys_low = sig_low.fuzzy_match_keys(tolerance=1, precision='medium')
    coherence_bins_low = {key[4] for key in fuzzy_keys_low}

    print(f"\n📊 Lower Boundary:")
    print(f"   Exact coherence_bin: {sig_low.coherence_bin}")
    print(f"   Fuzzy coherence_bins: {sorted(coherence_bins_low)} (expected [0,1])")
    assert coherence_bins_low == {0, 1}, "Lower boundary should clamp at 0"

    # Edge case: coherence_bin=9 (at upper boundary)
    sig_high = NexusSignature(
        participating_organs=frozenset({'EMPATHY'}),
        organ_count=1,
        nexus_type='SOCIAL_EMPATHY',
        mechanism='relational_attunement',
        coherence_bin=9,  # Will fuzz to [8,9] (clamped at 9)
        urgency_bin=5,
        polyvagal_state='ventral',
        zone=1,
        v0_energy_bin=4,
        kairos_detected=True,
        field_strength_bin=4,
        dominant_meta_atom='somatic_wisdom'
    )

    fuzzy_keys_high = sig_high.fuzzy_match_keys(tolerance=1, precision='medium')
    coherence_bins_high = {key[4] for key in fuzzy_keys_high}

    print(f"\n📊 Upper Boundary:")
    print(f"   Exact coherence_bin: {sig_high.coherence_bin}")
    print(f"   Fuzzy coherence_bins: {sorted(coherence_bins_high)} (expected [8,9])")
    assert coherence_bins_high == {8, 9}, "Upper boundary should clamp at 9"

    print(f"\n✅ TEST 5 PASSED")


def test_6_field_strength():
    """Test 6: Field strength computation from organ coherences."""
    print("\n" + "="*80)
    print("🧪 TEST 6: Field Strength Computation")
    print("="*80)

    extractor = get_default_extractor()

    # Test case 1: Uniform coherences
    organ_results_uniform = {
        'BOND': {'coherence': 0.8},
        'NDAM': {'coherence': 0.8},
        'EMPATHY': {'coherence': 0.8}
    }
    field_strength_uniform = extractor._compute_field_strength(organ_results_uniform)
    print(f"\n📊 Uniform Coherences (0.8):")
    print(f"   Field Strength: {field_strength_uniform:.3f} (expected 0.800)")
    assert abs(field_strength_uniform - 0.8) < 0.001

    # Test case 2: Mixed coherences
    organ_results_mixed = {
        'BOND': {'coherence': 0.9},
        'NDAM': {'coherence': 0.5},
        'EMPATHY': {'coherence': 0.7}
    }
    field_strength_mixed = extractor._compute_field_strength(organ_results_mixed)
    expected_mixed = (0.9 + 0.5 + 0.7) / 3
    print(f"\n📊 Mixed Coherences (0.9, 0.5, 0.7):")
    print(f"   Field Strength: {field_strength_mixed:.3f} (expected {expected_mixed:.3f})")
    assert abs(field_strength_mixed - expected_mixed) < 0.001

    # Test case 3: Empty organs (edge case)
    organ_results_empty = {}
    field_strength_empty = extractor._compute_field_strength(organ_results_empty)
    print(f"\n📊 Empty Organs:")
    print(f"   Field Strength: {field_strength_empty:.3f} (expected 0.500 default)")
    assert field_strength_empty == 0.5

    print(f"\n✅ TEST 6 PASSED")


def test_7_tsk_enhancement():
    """Test 7: Optional TSK enhancement fields."""
    print("\n" + "="*80)
    print("🧪 TEST 7: TSK Enhancement Fields (Optional)")
    print("="*80)

    extractor = get_default_extractor()

    nexus = {
        'participating_organs': ['SANS', 'RNX'],
        'nexus_type': 'PSYCHE_SANS',
        'mechanism': 'coherence_repair'
    }

    organ_results = {
        'SANS': {'coherence': 0.65},
        'RNX': {'coherence': 0.70}
    }

    # With TSK enhancement
    felt_state_tsk = {
        'field_coherence': 0.68,
        'urgency': 0.25,
        'polyvagal_state': 'ventral',
        'zone': 2,
        'v0_final': 0.45,
        'kairos_detected': False,
        'dominant_meta_atom': 'somatic_wisdom',
        # TSK fields
        'constraint_pattern': 'SANS_medium_RNX_medium',
        'transductive_vocabulary': ['coherence_leakage'],
        'satisfaction_tier': 'high',
        'emission_path': 'organic',
        'convergence_cycles': 2,
        'entity_context': ['Emma', 'work']
    }

    sig_tsk = extractor.extract(nexus, organ_results, felt_state_tsk)

    print(f"\n✅ TSK-Enhanced Signature:")
    print(f"   Constraint Pattern: {sig_tsk.constraint_pattern}")
    print(f"   Transductive Vocab: {sig_tsk.transductive_vocabulary}")
    print(f"   Satisfaction Tier: {sig_tsk.satisfaction_tier}")
    print(f"   Emission Path: {sig_tsk.emission_path}")
    print(f"   Convergence Cycles: {sig_tsk.convergence_cycles}")
    print(f"   Entity Context: {sig_tsk.entity_context}")

    # Assertions
    assert sig_tsk.constraint_pattern == 'SANS_medium_RNX_medium'
    assert 'coherence_leakage' in sig_tsk.transductive_vocabulary
    assert sig_tsk.satisfaction_tier == 'high'
    assert sig_tsk.emission_path == 'organic'
    assert sig_tsk.convergence_cycles == 2
    assert 'Emma' in sig_tsk.entity_context
    assert 'work' in sig_tsk.entity_context

    # Without TSK enhancement (should be None)
    felt_state_basic = {
        'field_coherence': 0.68,
        'urgency': 0.25,
        'polyvagal_state': 'ventral',
        'zone': 2,
        'v0_final': 0.45,
        'kairos_detected': False,
        'dominant_meta_atom': 'somatic_wisdom'
    }

    sig_basic = extractor.extract(nexus, organ_results, felt_state_basic)

    print(f"\n✅ Basic Signature (No TSK):")
    print(f"   Constraint Pattern: {sig_basic.constraint_pattern} (expected None)")
    assert sig_basic.constraint_pattern is None
    assert sig_basic.transductive_vocabulary is None
    assert sig_basic.satisfaction_tier is None

    print(f"\n✅ TEST 7 PASSED")


def test_8_frozenset_organs():
    """Test 8: Organ order independence via frozenset."""
    print("\n" + "="*80)
    print("🧪 TEST 8: Organ Order Independence (Frozenset)")
    print("="*80)

    extractor = get_default_extractor()

    # Same organs, different order
    nexus_1 = {
        'participating_organs': ['BOND', 'NDAM', 'EMPATHY'],
        'nexus_type': 'GUT_BOND_NDAM',
        'mechanism': 'protective_stasis'
    }

    nexus_2 = {
        'participating_organs': ['EMPATHY', 'BOND', 'NDAM'],  # Different order!
        'nexus_type': 'GUT_BOND_NDAM',
        'mechanism': 'protective_stasis'
    }

    felt_state = {
        'field_coherence': 0.75,
        'urgency': 0.60,
        'polyvagal_state': 'sympathetic',
        'zone': 4,
        'v0_final': 0.30,
        'kairos_detected': True,
        'dominant_meta_atom': 'fierce_holding'
    }

    organ_results = {
        'BOND': {'coherence': 0.8},
        'NDAM': {'coherence': 0.7},
        'EMPATHY': {'coherence': 0.75}
    }

    sig_1 = extractor.extract(nexus_1, organ_results, felt_state)
    sig_2 = extractor.extract(nexus_2, organ_results, felt_state)

    print(f"\n📊 Organ Sets:")
    print(f"   Nexus 1: {nexus_1['participating_organs']}")
    print(f"   Nexus 2: {nexus_2['participating_organs']}")
    print(f"   Frozenset 1: {sig_1.participating_organs}")
    print(f"   Frozenset 2: {sig_2.participating_organs}")

    # Should be identical (frozensets are order-independent)
    assert sig_1.participating_organs == sig_2.participating_organs

    # Hashable keys should be identical
    key_1 = sig_1.to_hashable(precision='medium')
    key_2 = sig_2.to_hashable(precision='medium')
    assert key_1 == key_2, "Keys should be identical despite different organ order"

    print(f"\n✅ Frozensets are identical (order-independent)")
    print(f"\n✅ TEST 8 PASSED")


def test_9_extreme_values():
    """Test 9: Extreme felt-state values."""
    print("\n" + "="*80)
    print("🧪 TEST 9: Extreme Felt-State Values")
    print("="*80)

    extractor = get_default_extractor()

    nexus = {
        'participating_organs': ['NDAM'],
        'nexus_type': 'GUT_NDAM',
        'mechanism': 'crisis_amplification'
    }

    organ_results = {
        'NDAM': {'coherence': 1.0}  # Maximum coherence
    }

    # Extreme crisis state
    felt_state_crisis = {
        'field_coherence': 0.05,  # Near chaos
        'urgency': 0.98,           # Near emergency
        'polyvagal_state': 'dorsal',
        'zone': 5,
        'v0_final': 0.95,          # High energy (not converged)
        'kairos_detected': False,
        'dominant_meta_atom': 'protective_withdrawal'
    }

    sig_crisis = extractor.extract(nexus, organ_results, felt_state_crisis)

    print(f"\n📊 Extreme Crisis State:")
    print(f"   Coherence: {felt_state_crisis['field_coherence']} → Bin {sig_crisis.coherence_bin}")
    print(f"   Urgency: {felt_state_crisis['urgency']} → Bin {sig_crisis.urgency_bin}")
    print(f"   V0 Energy: {felt_state_crisis['v0_final']} → Bin {sig_crisis.v0_energy_bin}")

    assert sig_crisis.coherence_bin == 0  # 0.05 → bin 0
    assert sig_crisis.urgency_bin == 9    # 0.98 → bin 9
    assert sig_crisis.v0_energy_bin == 4  # 0.95 → bin 4 (out of 5 bins [0-4], bin_width=0.2)

    # Extreme peace state
    felt_state_peace = {
        'field_coherence': 0.95,   # Near harmony
        'urgency': 0.02,            # Near calm
        'polyvagal_state': 'ventral',
        'zone': 1,
        'v0_final': 0.05,           # Low energy (converged)
        'kairos_detected': True,
        'dominant_meta_atom': 'embodied_awareness'
    }

    sig_peace = extractor.extract(nexus, organ_results, felt_state_peace)

    print(f"\n📊 Extreme Peace State:")
    print(f"   Coherence: {felt_state_peace['field_coherence']} → Bin {sig_peace.coherence_bin}")
    print(f"   Urgency: {felt_state_peace['urgency']} → Bin {sig_peace.urgency_bin}")
    print(f"   V0 Energy: {felt_state_peace['v0_final']} → Bin {sig_peace.v0_energy_bin}")

    assert sig_peace.coherence_bin == 9  # 0.95 → bin 9
    assert sig_peace.urgency_bin == 0    # 0.02 → bin 0
    assert sig_peace.v0_energy_bin == 0  # 0.05 → bin 0

    print(f"\n✅ TEST 9 PASSED")


def test_10_signature_immutability():
    """Test 10: Signature immutability (frozen dataclass)."""
    print("\n" + "="*80)
    print("🧪 TEST 10: Signature Immutability (Frozen Dataclass)")
    print("="*80)

    sig = NexusSignature(
        participating_organs=frozenset({'BOND'}),
        organ_count=1,
        nexus_type='GUT_BOND',
        mechanism='protective_stasis',
        coherence_bin=5,
        urgency_bin=5,
        polyvagal_state='sympathetic',
        zone=3,
        v0_energy_bin=2,
        kairos_detected=False,
        field_strength_bin=2,
        dominant_meta_atom='fierce_holding'
    )

    print(f"\n📊 Original Signature:")
    print(f"   Coherence Bin: {sig.coherence_bin}")

    # Attempt to modify (should raise FrozenInstanceError)
    try:
        sig.coherence_bin = 7
        assert False, "Should not be able to modify frozen dataclass"
    except (AttributeError, TypeError) as e:
        print(f"\n✅ Modification blocked (as expected): {type(e).__name__}")

    # Verify original unchanged
    assert sig.coherence_bin == 5, "Original value should be unchanged"

    print(f"\n✅ TEST 10 PASSED")


def main():
    """Run all 10 unit tests for nexus signature extractor."""
    print("\n" + "="*80)
    print("🌀 NEXUS SIGNATURE EXTRACTOR - UNIT TEST SUITE")
    print("="*80)
    print("\nTesting 18D signature extraction, quantization, hashing, fuzzy matching")

    try:
        test_1_basic_extraction()
        test_2_quantization()
        test_3_hashable_precision()
        test_4_fuzzy_matching()
        test_5_fuzzy_clamping()
        test_6_field_strength()
        test_7_tsk_enhancement()
        test_8_frozenset_organs()
        test_9_extreme_values()
        test_10_signature_immutability()

        print("\n" + "="*80)
        print("🎉 ALL 10 TESTS PASSED - NEXUS SIGNATURE EXTRACTOR VALIDATED!")
        print("="*80)
        print("\n✅ Phase 1 Week 1 Complete:")
        print("   • 18D signature extraction operational")
        print("   • Quantization with boundary clamping")
        print("   • Hashable tuple generation (3 precision levels)")
        print("   • Fuzzy matching with tolerance")
        print("   • Order-independent organ sets (frozenset)")
        print("   • TSK enhancement support")
        print("   • Immutable signatures (frozen dataclass)")
        print("\n🌀 Ready for Week 2: Nexus-Phrase Pattern Learner")

        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
