#!/usr/bin/env python3
"""
Quick test: EMPATHY emotional lure field

Tests that EMPATHY generates continuous emotional lure fields
across 7 dimensions (joy, grief, fear, anger, compassion, shame, neutral).
"""

import sys
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.empathy.core.empathy_text_core import EmpathyTextCore


@dataclass
class MockTextOccasion:
    text: str
    chunk_id: str = "test_0_0"


def test_empathy_lure_field():
    """Test EMPATHY emotional lure field generation."""

    empathy = EmpathyTextCore()

    test_inputs = [
        "I'm feeling overwhelmed right now.",
        "This conversation feels really safe and connected.",
        "I notice I'm getting defensive here.",
        "There's so much grief in this moment.",
        "I just need someone to validate that I'm not crazy."
    ]

    print("\n" + "="*70)
    print("🎭 EMPATHY EMOTIONAL LURE FIELD TEST")
    print("="*70)

    for i, text in enumerate(test_inputs, 1):
        occasion = MockTextOccasion(text=text)
        result = empathy.process_text_occasions([occasion], cycle=0)

        print(f"\n{'='*70}")
        print(f"Test {i}: {text[:50]}...")
        print(f"{'='*70}")
        print(f"  Coherence: {result.coherence:.3f}")
        print(f"  Lure: {result.lure:.3f}")
        print(f"  Patterns: {len(result.patterns)}")

        print(f"\n  🆕 Emotional Lure Field:")
        if result.emotional_lure_field:
            for emotion, strength in sorted(result.emotional_lure_field.items(),
                                           key=lambda x: x[1], reverse=True):
                bar_length = int(strength * 40)
                bar = '█' * bar_length
                print(f"    {emotion:12s}: {strength:.3f} {bar}")
        else:
            print("    ❌ NO LURE FIELD GENERATED")

    print("\n" + "="*70)
    print("✅ EMPATHY emotional lure field test complete")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_empathy_lure_field()
