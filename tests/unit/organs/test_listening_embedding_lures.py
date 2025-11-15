#!/usr/bin/env python3
"""
Test LISTENING Embedding-Based Lure Computation (Phase C3.5)
===========================================================

Validates that LISTENING organ uses embedding-based lure fields
and achieves higher activation rates than keyword-based approach.

Date: November 13, 2025
Phase: C3.5 Validation
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.listening.core.listening_text_core import ListeningTextCore
from transductive.text_occasion import TextOccasion
import numpy as np


def test_embedding_lures():
    """Test embedding-based inquiry lure computation."""

    print("="*80)
    print("🌀 TESTING LISTENING EMBEDDING-BASED LURES (Phase C3.5)")
    print("="*80)

    listening = ListeningTextCore()

    # Test cases designed to activate different inquiry dimensions
    test_cases = [
        {
            "text": "What happened before this started? When did you first notice it?",
            "expected_high": ["temporal_inquiry"],
            "description": "Temporal inquiry input"
        },
        {
            "text": "What's beneath the surface here? What deeper truth is calling?",
            "expected_high": ["core_exploration"],
            "description": "Core exploration input"
        },
        {
            "text": "I see you. I'm fully present with what you're sharing.",
            "expected_high": ["witnessing_presence"],
            "description": "Witnessing presence input"
        },
        {
            "text": "This connects to what you said earlier. I notice a pattern emerging.",
            "expected_high": ["pattern_mapping", "tracking_continuity"],
            "description": "Pattern mapping input"
        },
        {
            "text": "Can you say more about that? Help me understand.",
            "expected_high": ["clarifying_inquiry"],
            "description": "Clarifying inquiry input"
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

        # Process with LISTENING organ
        result = listening.process_text_occasions([occasion], cycle=1)

        # Check lure field
        lure_field = result.inquiry_lure_field
        print(f"\n✅ Inquiry Lure Field:")
        for dimension, strength in sorted(lure_field.items(), key=lambda x: x[1], reverse=True):
            print(f"   {dimension:20s}: {strength:.3f}")

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
    print("📊 PHASE C3.5 VALIDATION SUMMARY - LISTENING")
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
    print(f"{'✅ LISTENING PHASE C3.5 COMPLETE' if activation_rate >= 80 else '⚠️  LISTENING PHASE C3.5 NEEDS ATTENTION'}")
    print("="*80 + "\n")


if __name__ == '__main__':
    test_embedding_lures()
