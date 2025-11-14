#!/usr/bin/env python3
"""
Quick test: WISDOM pattern lure field

Tests that WISDOM generates continuous pattern lure fields
across 7 dimensions (systems, meta, temporal, paradox, embodied, relational, integrative).
"""

import sys
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.wisdom.core.wisdom_text_core import WisdomTextCore


@dataclass
class MockTextOccasion:
    text: str
    chunk_id: str = "test_0_0"


def test_wisdom_lure_field():
    """Test WISDOM pattern lure field generation."""

    wisdom = WisdomTextCore()

    test_inputs = [
        "Stepping back, I notice a pattern here.",
        "The paradox is that both things can be true.",
        "Looking at the bigger picture, there's a systemic issue.",
        "It just clicked for me - I suddenly realize what's happening.",
        "This keeps happening over time - there's a cycle."
    ]

    print("\n" + "="*70)
    print("🧠 WISDOM PATTERN LURE FIELD TEST")
    print("="*70)

    for i, text in enumerate(test_inputs, 1):
        occasion = MockTextOccasion(text=text)
        result = wisdom.process_text_occasions([occasion], cycle=0)

        print(f"\n{'='*70}")
        print(f"Test {i}: {text[:50]}...")
        print(f"{'='*70}")
        print(f"  Coherence: {result.coherence:.3f}")
        print(f"  Lure: {result.lure:.3f}")
        print(f"  Patterns: {len(result.patterns)}")

        print(f"\n  🆕 Pattern Lure Field:")
        if result.pattern_lure_field:
            for pattern, strength in sorted(result.pattern_lure_field.items(),
                                           key=lambda x: x[1], reverse=True):
                bar_length = int(strength * 40)
                bar = '█' * bar_length
                print(f"    {pattern:12s}: {strength:.3f} {bar}")
        else:
            print("    ❌ NO LURE FIELD GENERATED")

    print("\n" + "="*70)
    print("✅ WISDOM pattern lure field test complete")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_wisdom_lure_field()
