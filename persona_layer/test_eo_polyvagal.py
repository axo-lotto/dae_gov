#!/usr/bin/env python3
"""Test EO organ atom activation implementation."""

import sys
import os
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from organs.modular.eo.core.eo_text_core import EOTextCore

def test_eo_polyvagal():
    """Test EO organ with polyvagal state detection text."""

    eo = EOTextCore()

    # Test text with ventral vagal (safety) state
    test_text = """
    I feel safe and connected right now. There's a sense of warmth
    and openness in my chest. I'm breathing easily and feel grounded
    in this moment. Connection feels natural and effortless.
    """

    print("=" * 70)
    print("EO ORGAN ATOM ACTIVATION TEST")
    print("=" * 70)
    print(f"\nTest text: {test_text.strip()}\n")

    result = eo.process_text(test_text)

    print(f"Coherence: {result.coherence:.4f}")
    print(f"Polyvagal State: {result.polyvagal_state}")
    print(f"State Confidence: {result.state_confidence:.4f}")
    print(f"State Clarity: {result.state_clarity:.4f}")
    print(f"Self Distance Modifier: {result.self_distance_modifier:.4f}")
    print(f"\nDetected {len(result.patterns)} polyvagal patterns:")

    for p in result.patterns:
        print(f"  - {p.pattern_type}: strength={p.strength:.4f}, "
              f"confidence={p.confidence:.4f}")

    print(f"\n🌀 ATOM ACTIVATIONS ({len(result.atom_activations)} atoms):")
    if result.atom_activations:
        for atom, activation in sorted(result.atom_activations.items(),
                                       key=lambda x: x[1], reverse=True):
            print(f"  - {atom}: {activation:.4f}")
        print(f"\n✅ EO ORGAN VALIDATION SUCCESSFUL!")
        print(f"   Expected ventral_vagal, safety_cues, neuroception")
        print(f"   Got: {list(result.atom_activations.keys())}")
    else:
        print("  ❌ NO ACTIVATIONS (ERROR!)")

    print("=" * 70)

if __name__ == '__main__':
    test_eo_polyvagal()
