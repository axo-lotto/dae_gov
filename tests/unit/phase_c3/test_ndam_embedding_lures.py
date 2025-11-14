#!/usr/bin/env python3
"""
Test NDAM Embedding-Based Lure Computation (Phase C3.2)
"""
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.ndam.core.ndam_text_core import NDAMTextCore
from transductive.text_occasion import TextOccasion
import numpy as np

def test_embedding_lures():
    print("="*80)
    print("🌀 TESTING NDAM EMBEDDING-BASED LURES (Phase C3.2)")
    print("="*80)

    organ = NDAMTextCore()

    test_cases = [
        {
            'description': 'crisis_imminent - immediate danger',
            'text': "Right now, immediate danger, can't wait, this is urgent crisis situation",
            'expected_top': 'crisis_imminent'
        },
        {
            'description': 'safety_concern - worried about safety',
            'text': "Worried about safety, could get hurt, someone might be in danger",
            'expected_top': 'safety_concern'
        },
        {
            'description': 'escalating_intensity - building crisis',
            'text': "Getting worse, building toward crisis, escalating rapidly, intensifying",
            'expected_top': 'escalating_intensity'
        },
        {
            'description': 'stability_present - feeling stable',
            'text': "Feeling stable, grounded, not in crisis, everything is calm and okay",
            'expected_top': 'stability_present'
        },
        {
            'description': 'harm_risk - risk of harm',
            'text': "Risk of harm to self or others, potential for serious injury or damage",
            'expected_top': 'harm_risk'
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
        lure_field = result.urgency_lure_field

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
