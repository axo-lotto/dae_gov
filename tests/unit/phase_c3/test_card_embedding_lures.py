#!/usr/bin/env python3
"""
Test CARD Embedding-Based Lure Computation (Phase C3.5)
"""
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.card.core.card_text_core import CARDTextCore
from transductive.text_occasion import TextOccasion
import numpy as np

def test_embedding_lures():
    print("="*80)
    print("🌀 TESTING CARD EMBEDDING-BASED LURES (Phase C3.5)")
    print("="*80)

    organ = CARDTextCore()

    test_cases = [
        {
            'description': 'minimal_holding - brief presence',
            'text': "Just need brief holding, simple presence, minimal words, short response",
            'expected_top': 'minimal_holding'
        },
        {
            'description': 'moderate_presence - balanced engagement',
            'text': "Medium depth response, balanced engagement, moderate level of detail",
            'expected_top': 'moderate_presence'
        },
        {
            'description': 'comprehensive_depth - full exploration',
            'text': "Full deep exploration, comprehensive detail, complete thorough analysis",
            'expected_top': 'comprehensive_depth'
        },
        {
            'description': 'silence_appropriate - no words needed',
            'text': "No words needed, silence is enough, quiet holding, just presence",
            'expected_top': 'silence_appropriate'
        },
        {
            'description': 'crisis_brevity - short grounding',
            'text': "Short grounding for overwhelm, brief crisis support, quick stabilization",
            'expected_top': 'crisis_brevity'
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
        lure_field = result.scale_lure_field

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
