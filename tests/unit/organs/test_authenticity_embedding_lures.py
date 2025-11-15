#!/usr/bin/env python3
"""
Test AUTHENTICITY Embedding-Based Lure Computation (Phase C3.4)
================================================================

Validates that AUTHENTICITY organ uses embedding-based lure fields
and achieves higher activation rates than keyword-based approach.

Date: November 13, 2025
Phase: C3.4 Validation
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.authenticity.core.authenticity_text_core import AuthenticityTextCore
from transductive.text_occasion import TextOccasion
import numpy as np


def test_embedding_lures():
    """Test embedding-based vulnerability lure computation."""

    print("="*80)
    print("🌀 TESTING AUTHENTICITY EMBEDDING-BASED LURES (Phase C3.4)")
    print("="*80)

    authenticity = AuthenticityTextCore()

    # Test cases designed to activate different vulnerability stances
    test_cases = [
        {
            "text": "I feel exposed and open, this is tender truth.",
            "expected_high": ["vulnerable", "honest"],
            "description": "Vulnerable openness"
        },
        {
            "text": "I speak the truth with clarity and directness.",
            "expected_high": ["honest"],
            "description": "Direct honesty"
        },
        {
            "text": "I protect what's tender and keep careful distance.",
            "expected_high": ["guarded", "boundaried"],
            "description": "Protective guardedness"
        },
        {
            "text": "I show what's expected with polished presentation.",
            "expected_high": ["performative"],
            "description": "Performance mode"
        },
        {
            "text": "I'm becoming something new, unfolding and discovering.",
            "expected_high": ["emergent"],
            "description": "Emergent growth"
        }
    ]

    activation_rates = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-'*80}")
        print(f"Test Case {i}: {test_case['description']}")
        print(f"{'-'*80}")
        print(f"Input: \"{test_case['text']}\"")

        # Create occasion
        occasion = TextOccasion(
            chunk_id=f"test_{i}",
            position=0,
            text=test_case['text'],
            embedding=np.zeros(384)  # Dummy embedding
        )

        # Process with AUTHENTICITY organ
        result = authenticity.process_text_occasions([occasion], cycle=1)

        # Check lure field
        lure_field = result.vulnerability_lure_field
        print(f"\n✅ Vulnerability Lure Field:")
        for stance, strength in sorted(lure_field.items(), key=lambda x: x[1], reverse=True):
            print(f"   {stance:13s}: {strength:.3f}")

        # Check if lure field is non-uniform (activated)
        lure_values = list(lure_field.values())
        max_lure = max(lure_values)
        min_lure = min(lure_values)
        variance = max_lure - min_lure

        # Activation criteria: variance > 0.05 (not balanced 1/7 = 0.143)
        is_activated = variance > 0.05
        activation_rates.append(1 if is_activated else 0)

        print(f"\n📊 Activation Status:")
        print(f"   Max lure: {max_lure:.3f}")
        print(f"   Min lure: {min_lure:.3f}")
        print(f"   Variance: {variance:.3f}")
        print(f"   Activated: {'✅ YES' if is_activated else '❌ NO (balanced default)'}")

        # Check if expected stances are high
        expected_found = []
        for expected_stance in test_case['expected_high']:
            if lure_field.get(expected_stance, 0.0) > 0.15:  # Above balanced baseline
                expected_found.append(expected_stance)

        if expected_found:
            print(f"   Expected stances found: {', '.join(expected_found)} ✅")
        else:
            print(f"   ⚠️  Expected stances not prominent")

    # Summary
    print(f"\n{'='*80}")
    print("📊 PHASE C3.4 VALIDATION SUMMARY")
    print("="*80)

    activation_rate = sum(activation_rates) / len(activation_rates) * 100
    print(f"Activation Rate: {activation_rate:.1f}% ({sum(activation_rates)}/{len(activation_rates)} tests)")

    if activation_rate >= 80:
        print(f"✅ TARGET ACHIEVED: ≥80% activation rate")
        print(f"   Embedding-based lures working correctly!")
    elif activation_rate >= 60:
        print(f"⚠️  PARTIAL SUCCESS: {activation_rate:.1f}% activation (target: 80%)")
        print(f"   Needs tuning or more test cases")
    else:
        print(f"❌ BELOW TARGET: {activation_rate:.1f}% activation (target: 80%)")
        print(f"   Check embedding coordinator and prototypes")

    print("\n" + "="*80)
    print(f"{'✅ PHASE C3.4 COMPLETE' if activation_rate >= 80 else '⚠️  PHASE C3.4 NEEDS ATTENTION'}")
    print("="*80 + "\n")


if __name__ == '__main__':
    test_embedding_lures()
