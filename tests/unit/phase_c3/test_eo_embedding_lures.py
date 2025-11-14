#!/usr/bin/env python3
"""
Test EO Embedding-Based Lure Computation (Phase C3.4)
"""
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.eo.core.eo_text_core import EOTextCore
from transductive.text_occasion import TextOccasion
import numpy as np

def test_embedding_lures():
    print("="*80)
    print("🌀 TESTING EO EMBEDDING-BASED LURES (Phase C3.4)")
    print("="*80)

    organ = EOTextCore()

    test_cases = [
        {
            'description': 'ventral_vagal_safe - safe and connected',
            'text': "I feel safe, connected, socially engaged, comfortable with others, regulated",
            'expected_top': 'ventral_vagal_safe'
        },
        {
            'description': 'sympathetic_fight - angry and activated',
            'text': "Angry, activated, fighting energy, aggressive stance, ready to attack",
            'expected_top': 'sympathetic_fight'
        },
        {
            'description': 'sympathetic_flight - anxious and panicked',
            'text': "Anxious, panicked, need to escape, running away, fleeing the situation",
            'expected_top': 'sympathetic_flight'
        },
        {
            'description': 'dorsal_freeze - shut down and numb',
            'text': "Shut down, numb, collapsed, can't move, frozen in place, immobilized",
            'expected_top': 'dorsal_freeze'
        },
        {
            'description': 'dorsal_dissociation - disconnected and floating',
            'text': "Disconnected, floating, not really here, spaced out, dissociated away",
            'expected_top': 'dorsal_dissociation'
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
        lure_field = result.polyvagal_lure_field

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
