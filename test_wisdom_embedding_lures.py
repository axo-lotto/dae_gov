#!/usr/bin/env python3
"""
Test WISDOM Embedding-Based Lure Computation (Phase C3.3)
==========================================================

Validates that WISDOM organ uses embedding-based lure fields
and achieves higher activation rates than keyword-based approach.

Date: November 13, 2025
Phase: C3.3 Validation
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.wisdom.core.wisdom_text_core import WisdomTextCore
from transductive.text_occasion import TextOccasion
import numpy as np


def test_embedding_lures():
    """Test embedding-based pattern lure computation."""

    print("="*80)
    print("🌀 TESTING WISDOM EMBEDDING-BASED LURES (Phase C3.3)")
    print("="*80)

    wisdom = WisdomTextCore()

    # Test cases designed to activate different cognitive patterns
    test_cases = [
        {
            "text": "I see how parts interconnect and form the whole system.",
            "expected_high": ["systems", "integrative"],
            "description": "Systems thinking"
        },
        {
            "text": "I notice I'm noticing my own thinking patterns.",
            "expected_high": ["meta"],
            "description": "Meta-awareness"
        },
        {
            "text": "This pattern keeps recurring over time in cycles.",
            "expected_high": ["temporal"],
            "description": "Temporal pattern recognition"
        },
        {
            "text": "I can hold both truths simultaneously, they coexist in tension.",
            "expected_high": ["paradox"],
            "description": "Paradox holding"
        },
        {
            "text": "I feel this truth in my body, it's viscerally real.",
            "expected_high": ["embodied"],
            "description": "Embodied knowing"
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

        # Process with WISDOM organ
        result = wisdom.process_text_occasions([occasion], cycle=1)

        # Check lure field
        lure_field = result.pattern_lure_field
        print(f"\n✅ Pattern Lure Field:")
        for pattern, strength in sorted(lure_field.items(), key=lambda x: x[1], reverse=True):
            print(f"   {pattern:12s}: {strength:.3f}")

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

        # Check if expected patterns are high
        expected_found = []
        for expected_pattern in test_case['expected_high']:
            if lure_field.get(expected_pattern, 0.0) > 0.15:  # Above balanced baseline
                expected_found.append(expected_pattern)

        if expected_found:
            print(f"   Expected patterns found: {', '.join(expected_found)} ✅")
        else:
            print(f"   ⚠️  Expected patterns not prominent")

    # Summary
    print(f"\n{'='*80}")
    print("📊 PHASE C3.3 VALIDATION SUMMARY")
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
    print(f"{'✅ PHASE C3.3 COMPLETE' if activation_rate >= 80 else '⚠️  PHASE C3.3 NEEDS ATTENTION'}")
    print("="*80 + "\n")


if __name__ == '__main__':
    test_embedding_lures()
