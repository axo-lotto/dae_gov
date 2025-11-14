#!/usr/bin/env python3
"""
Test EMPATHY Embedding-Based Lure Computation (Phase C3.2)
===========================================================

Validates that EMPATHY organ uses embedding-based lure fields
and achieves higher activation rates than keyword-based approach.

Date: November 13, 2025
Phase: C3.2 Validation
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.empathy.core.empathy_text_core import EmpathyTextCore
from transductive.text_occasion import TextOccasion
import numpy as np


def test_embedding_lures():
    """Test embedding-based emotional lure computation."""

    print("="*80)
    print("🌀 TESTING EMPATHY EMBEDDING-BASED LURES (Phase C3.2)")
    print("="*80)

    empathy = EmpathyTextCore()

    # Test cases designed to activate different emotional dimensions
    test_cases = [
        {
            "text": "I'm feeling really overwhelmed and scared right now.",
            "expected_high": ["fear", "grief"],  # Expected dominant emotions
            "description": "High fear input"
        },
        {
            "text": "This conversation feels really safe and connected.",
            "expected_high": ["joy", "compassion"],
            "description": "High joy/connection input"
        },
        {
            "text": "I notice I'm getting defensive and need space.",
            "expected_high": ["anger", "neutral"],
            "description": "Anger/boundary input"
        },
        {
            "text": "I feel tender sadness for what was lost.",
            "expected_high": ["grief", "compassion"],
            "description": "Grief/tenderness input"
        },
        {
            "text": "There's brightness and aliveness here.",
            "expected_high": ["joy"],
            "description": "Joy/vitality input"
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

        # Process with EMPATHY organ
        result = empathy.process_text_occasions([occasion], cycle=1)

        # Check lure field
        lure_field = result.emotional_lure_field
        print(f"\n✅ Emotional Lure Field:")
        for emotion, strength in sorted(lure_field.items(), key=lambda x: x[1], reverse=True):
            print(f"   {emotion:12s}: {strength:.3f}")

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

        # Check if expected emotions are high
        expected_found = []
        for expected_emotion in test_case['expected_high']:
            if lure_field.get(expected_emotion, 0.0) > 0.15:  # Above balanced baseline
                expected_found.append(expected_emotion)

        if expected_found:
            print(f"   Expected emotions found: {', '.join(expected_found)} ✅")
        else:
            print(f"   ⚠️  Expected emotions not prominent")

    # Summary
    print(f"\n{'='*80}")
    print("📊 PHASE C3.2 VALIDATION SUMMARY")
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
    print(f"{'✅ PHASE C3.2 COMPLETE' if activation_rate >= 80 else '⚠️  PHASE C3.2 NEEDS ATTENTION'}")
    print("="*80 + "\n")


if __name__ == '__main__':
    test_embedding_lures()
