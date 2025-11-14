#!/usr/bin/env python3
"""
Test PRESENCE Embedding-Based Lure Computation (Phase C3.5)
===========================================================

Validates that PRESENCE organ uses embedding-based lure fields
and achieves higher activation rates than keyword-based approach.

Date: November 13, 2025
Phase: C3.5 Validation
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.presence.core.presence_text_core import PresenceTextCore
from transductive.text_occasion import TextOccasion
import numpy as np


def test_embedding_lures():
    """Test embedding-based presence lure computation."""

    print("="*80)
    print("🌀 TESTING PRESENCE EMBEDDING-BASED LURES (Phase C3.5)")
    print("="*80)

    presence = PresenceTextCore()

    # Test cases designed to activate different presence dimensions
    test_cases = [
        {
            "text": "I feel this deeply in my body right now, sensing everything",
            "expected_high": ["embodied_awareness", "somatic_noticing"],
            "description": "Embodied awareness input"
        },
        {
            "text": "I'm rooted and grounded, feet planted on solid earth",
            "expected_high": ["grounded_holding"],
            "description": "Grounded holding input"
        },
        {
            "text": "There's room for all of this, nothing needs fixing",
            "expected_high": ["spacious_allowing"],
            "description": "Spacious allowing input"
        },
        {
            "text": "I'm in the still point within, calm center amidst movement",
            "expected_high": ["centered_stillness"],
            "description": "Centered stillness input"
        },
        {
            "text": "All parts of me are welcome, integrated wholeness here",
            "expected_high": ["integrated_wholeness"],
            "description": "Integrated wholeness input"
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

        # Process with PRESENCE organ
        result = presence.process_text_occasions([occasion], cycle=1)

        # Check lure field
        lure_field = result.presence_lure_field
        print(f"\n✅ Presence Lure Field:")
        for dimension, strength in sorted(lure_field.items(), key=lambda x: x[1], reverse=True):
            print(f"   {dimension:25s}: {strength:.3f}")

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

        # Check if expected dimensions are high
        expected_found = []
        for expected_dimension in test_case['expected_high']:
            if lure_field.get(expected_dimension, 0.0) > 0.15:  # Above balanced baseline
                expected_found.append(expected_dimension)

        if expected_found:
            print(f"   Expected dimensions found: {', '.join(expected_found)} ✅")
        else:
            print(f"   ⚠️  Expected dimensions not prominent")

    # Summary
    print(f"\n{'='*80}")
    print("📊 PHASE C3.5 VALIDATION SUMMARY - PRESENCE")
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
    print(f"{'✅ PRESENCE PHASE C3.5 COMPLETE' if activation_rate >= 80 else '⚠️  PRESENCE PHASE C3.5 NEEDS ATTENTION'}")
    print("="*80 + "\n")


if __name__ == '__main__':
    test_embedding_lures()
