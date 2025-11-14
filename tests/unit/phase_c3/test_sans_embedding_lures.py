#!/usr/bin/env python3
"""
Test SANS Embedding-Based Lure Computation (Phase C3.1)
"""
import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.sans.core.sans_text_core import SANSTextCore
from transductive.text_occasion import TextOccasion
import numpy as np

def test_embedding_lures():
    print("="*80)
    print("🌀 TESTING SANS EMBEDDING-BASED LURES (Phase C3.1)")
    print("="*80)

    organ = SANSTextCore()

    test_cases = [
        {
            'description': 'semantic_drift - words losing meaning',
            'text': "My words don't match my meaning anymore, everything feels disconnected",
            'expected_top': 'semantic_drift'
        },
        {
            'description': 'contradiction_detected - conflicting statements',
            'text': "I said yes but meant no, these statements conflict with each other",
            'expected_top': 'contradiction_detected'
        },
        {
            'description': 'alignment_strong - coherent meaning',
            'text': "Everything aligns perfectly, it all makes sense together, complete coherence",
            'expected_top': 'alignment_strong'
        },
        {
            'description': 'repair_needed - needs reconnection',
            'text': "These pieces need reconnection, repair the broken links between ideas",
            'expected_top': 'repair_needed'
        },
        {
            'description': 'fragmentation - scattered thoughts',
            'text': "Scattered thoughts everywhere, no connection between ideas, total fragmentation",
            'expected_top': 'fragmentation'
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
        lure_field = result.coherence_lure_field

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
