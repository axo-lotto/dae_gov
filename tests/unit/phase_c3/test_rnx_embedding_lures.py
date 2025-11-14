#!/usr/bin/env python3
"""
Test RNX Embedding-Based Lure Computation (Phase C3.3)
"""
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.rnx.core.rnx_text_core import RNXTextCore
from transductive.text_occasion import TextOccasion
import numpy as np

def test_embedding_lures():
    print("="*80)
    print("🌀 TESTING RNX EMBEDDING-BASED LURES (Phase C3.3)")
    print("="*80)

    organ = RNXTextCore()

    test_cases = [
        {
            'description': 'chronic_pattern - long-term pattern',
            'text': "This has been happening for years, longstanding chronic pattern, ongoing for so long",
            'expected_top': 'chronic_pattern'
        },
        {
            'description': 'acute_event - brand new event',
            'text': "Just happened today, brand new, sudden acute event, first time ever",
            'expected_top': 'acute_event'
        },
        {
            'description': 'cyclical_rhythm - repeating cycle',
            'text': "Comes and goes in cycles, repeating pattern, rhythmic oscillation, cyclical",
            'expected_top': 'cyclical_rhythm'
        },
        {
            'description': 'developmental_phase - growth edge',
            'text': "Growing edge, transitional moment, developmental phase, evolving period",
            'expected_top': 'developmental_phase'
        },
        {
            'description': 'stuck_repetition - stuck loop',
            'text': "Same thing over and over, stuck in loop, endless repetition, can't break free",
            'expected_top': 'stuck_repetition'
        }
    ]

    activation_rates = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-'*80}")
        print(f"Test Case {i}: {test_case['description']}")
        print(f"Input: \"{test_case['text']}\"")

        occasion = TextOccasion(
            chunk_id=f"test_{i}",
            position=0,
            text=test_case['text'],
            embedding=np.zeros(384)  # Will be computed by organ
        )

        result = organ.process_text_occasions([occasion], cycle=1)
        lure_field = result.temporal_lure_field

        print(f"\n✅ Lure Field:")
        for dim, strength in sorted(lure_field.items(), key=lambda x: x[1], reverse=True):
            marker = "🎯" if dim == test_case['expected_top'] else "  "
            print(f"   {marker} {dim:25s}: {strength:.3f}")

        variance = max(lure_field.values()) - min(lure_field.values())
        is_activated = variance > 0.05
        activation_rates.append(1 if is_activated else 0)

        print(f"\n📊 Variance: {variance:.3f} - {'✅ ACTIVATED' if is_activated else '❌ NOT ACTIVATED'}")

    activation_rate = sum(activation_rates) / len(activation_rates) * 100
    print(f"\n{'='*80}")
    print(f"Activation Rate: {activation_rate:.1f}% ({sum(activation_rates)}/{len(activation_rates)})")
    print(f"{'✅ PASS (≥80%)' if activation_rate >= 80 else '❌ FAIL (<80%)'}")
    print("="*80)

if __name__ == '__main__':
    test_embedding_lures()
