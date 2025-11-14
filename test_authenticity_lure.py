#!/usr/bin/env python3
"""
Quick test: AUTHENTICITY vulnerability lure field

Tests that AUTHENTICITY generates continuous vulnerability lure fields
across 7 dimensions (vulnerable, honest, guarded, performative, emergent, receptive, boundaried).
"""

import sys
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.authenticity.core.authenticity_text_core import AuthenticityTextCore


@dataclass
class MockTextOccasion:
    text: str
    chunk_id: str = "test_0_0"


def test_authenticity_lure_field():
    """Test AUTHENTICITY vulnerability lure field generation."""

    authenticity = AuthenticityTextCore()

    test_inputs = [
        "I'm being really honest with you right now.",
        "I feel vulnerable sharing this.",
        "To be completely transparent, I don't know the answer.",
        "I'm going to be real with you - this is hard for me.",
        "I need to share something personal with you."
    ]

    print("\n" + "="*70)
    print("🎨 AUTHENTICITY VULNERABILITY LURE FIELD TEST")
    print("="*70)

    for i, text in enumerate(test_inputs, 1):
        occasion = MockTextOccasion(text=text)
        result = authenticity.process_text_occasions([occasion], cycle=0)

        print(f"\n{'='*70}")
        print(f"Test {i}: {text[:50]}...")
        print(f"{'='*70}")
        print(f"  Coherence: {result.coherence:.3f}")
        print(f"  Lure: {result.lure:.3f}")
        print(f"  Patterns: {len(result.patterns)}")

        print(f"\n  🆕 Vulnerability Lure Field:")
        if result.vulnerability_lure_field:
            for stance, strength in sorted(result.vulnerability_lure_field.items(),
                                          key=lambda x: x[1], reverse=True):
                bar_length = int(strength * 40)
                bar = '█' * bar_length
                print(f"    {stance:12s}: {strength:.3f} {bar}")
        else:
            print("    ❌ NO LURE FIELD GENERATED")

    print("\n" + "="*70)
    print("✅ AUTHENTICITY vulnerability lure field test complete")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_authenticity_lure_field()
