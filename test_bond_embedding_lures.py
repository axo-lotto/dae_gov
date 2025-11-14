#!/usr/bin/env python3
"""
Test BOND Embedding-Based Lure Computation (Phase C3.1)
"""
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.bond.core.bond_text_core import BONDTextCore
from transductive.text_occasion import TextOccasion
import numpy as np

def test_embedding_lures():
    print("="*80)
    print(f"🌀 TESTING BOND EMBEDDING-BASED LURES (Phase C3.1)")
    print("="*80)

    organ = BONDTextCore()

    test_cases = [
        {
            "text": "I need to control everything and organize it properly.",
            "expected_high": ["manager_control"],
            "description": "Manager control language"
        },
        {
            "text": "I can't take this anymore, I'm shutting down and numbing out.",
            "expected_high": ["firefighter_numbing"],
            "description": "Firefighter numbing"
        },
        {
            "text": "I feel worthless and hurt, everyone will abandon me.",
            "expected_high": ["exile_pain"],
            "description": "Exile pain language"
        },
        {
            "text": "I'm calm, curious, and connected to my compassionate self.",
            "expected_high": ["self_energy"],
            "description": "SELF energy presence"
        },
        {
            "text": "I can feel myself letting go of these old burdens.",
            "expected_high": ["unburdening_release"],
            "description": "Unburdening process"
        }
    ]

    activation_rates = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-'*80}")
        print(f"Test Case {i}: {test_case['description']}")
        print(f"{'-'*80}")
        print(f"Input: \"{test_case['text']}\"")

        occasion = TextOccasion(
            chunk_id=f"test_{i}",
            position=0,
            text=test_case['text'],
            embedding=np.zeros(384)
        )

        result = organ.process_text_occasions([occasion], cycle=1)
        lure_field = result.parts_lure_field

        print(f"\n✅ IFS Parts Lure Field:")
        for dim, strength in sorted(lure_field.items(), key=lambda x: x[1], reverse=True):
            print(f"   {dim:25s}: {strength:.3f}")

        # Check activation
        lure_values = list(lure_field.values())
        variance = max(lure_values) - min(lure_values)
        is_activated = variance > 0.05
        activation_rates.append(1 if is_activated else 0)

        print(f"\n📊 Activation Status:")
        print(f"   Variance: {variance:.3f}")
        print(f"   Activated: {'✅ YES' if is_activated else '❌ NO'}")

    # Summary
    activation_rate = sum(activation_rates) / len(activation_rates) * 100
    print(f"\n{'='*80}")
    print(f"Activation Rate: {activation_rate:.1f}% ({sum(activation_rates)}/{len(activation_rates)} tests)")

    if activation_rate >= 80:
        print(f"✅ TARGET ACHIEVED: ≥80% activation rate")
    else:
        print(f"⚠️ BELOW TARGET: {activation_rate:.1f}% (target: 80%)")

    print("="*80 + "\n")

if __name__ == '__main__':
    test_embedding_lures()
