"""
Test Polyvagal Detector (Embedding-Based)

Validates polyvagal state detection with trauma-informed scenarios.
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.polyvagal_detector import (
    PolyvagalDetector,
    quick_polyvagal_check,
    is_safe_to_engage
)


def test_polyvagal_scenarios():
    """Test polyvagal detector on trauma-informed scenarios."""

    print("=" * 60)
    print("POLYVAGAL DETECTOR VALIDATION TEST")
    print("=" * 60)
    print()

    detector = PolyvagalDetector()

    # Scenario 1: VENTRAL (safe, connected, curious)
    print("Scenario 1: VENTRAL - Safe and connected")
    print("-" * 60)
    text1 = "I'm feeling curious and open to exploring this further. There's a sense of ease and I feel grounded."
    detection1 = detector.detect_polyvagal_state(text1)
    print(f"Text: {text1}")
    print(f"Dominant State: {detection1.dominant_state}")
    print(f"Confidence: {detection1.confidence:.3f}")
    print(f"Coherence: {detection1.coherence:.3f}")
    print(f"Mixed Activation:")
    for state, prob in detection1.mixed_activation.items():
        print(f"  {state}: {prob:.3f}")

    assert detection1.dominant_state == "ventral", f"Expected 'ventral', got '{detection1.dominant_state}'"
    assert detection1.confidence > 0.45, f"Expected confidence > 0.45 (fresh model), got {detection1.confidence:.3f}"
    print("✅ PASS: Ventral state detected correctly")
    print()

    # Scenario 2: SYMPATHETIC (mobilized, anxious, fight/flight)
    print("Scenario 2: SYMPATHETIC - Mobilized and anxious")
    print("-" * 60)
    text2 = "I feel overwhelmed by the deadline pressure. There's so much to do and I'm anxious about getting it all done in time."
    detection2 = detector.detect_polyvagal_state(text2)
    print(f"Text: {text2}")
    print(f"Dominant State: {detection2.dominant_state}")
    print(f"Confidence: {detection2.confidence:.3f}")
    print(f"Coherence: {detection2.coherence:.3f}")
    print(f"Mixed Activation:")
    for state, prob in detection2.mixed_activation.items():
        print(f"  {state}: {prob:.3f}")

    assert detection2.dominant_state == "sympathetic", f"Expected 'sympathetic', got '{detection2.dominant_state}'"
    assert detection2.confidence > 0.4, f"Expected confidence > 0.4 (fresh model), got {detection2.confidence:.3f}"
    print("✅ PASS: Sympathetic state detected correctly")
    print()

    # Scenario 3: DORSAL (shutdown, freeze, dissociation)
    print("Scenario 3: DORSAL - Shutdown and numb")
    print("-" * 60)
    text3 = "I feel completely numb and shut down. Everything feels heavy and I just want to disappear. There's nothing left."
    detection3 = detector.detect_polyvagal_state(text3)
    print(f"Text: {text3}")
    print(f"Dominant State: {detection3.dominant_state}")
    print(f"Confidence: {detection3.confidence:.3f}")
    print(f"Coherence: {detection3.coherence:.3f}")
    print(f"Mixed Activation:")
    for state, prob in detection3.mixed_activation.items():
        print(f"  {state}: {prob:.3f}")

    assert detection3.dominant_state == "dorsal", f"Expected 'dorsal', got '{detection3.dominant_state}'"
    assert detection3.confidence > 0.4, f"Expected confidence > 0.4 (fresh model), got {detection3.confidence:.3f}"
    print("✅ PASS: Dorsal state detected correctly")
    print()

    # Scenario 4: MIXED (sympathetic + dorsal - "frozen rage")
    print("Scenario 4: MIXED - Frozen rage (sympathetic + dorsal)")
    print("-" * 60)
    text4 = "I'm simultaneously frozen and furious. My body feels stuck but my mind is racing with angry thoughts."
    detection4 = detector.detect_polyvagal_state(text4)
    print(f"Text: {text4}")
    print(f"Dominant State: {detection4.dominant_state}")
    print(f"Confidence: {detection4.confidence:.3f}")
    print(f"Coherence: {detection4.coherence:.3f}")
    print(f"Mixed Activation:")
    for state, prob in detection4.mixed_activation.items():
        print(f"  {state}: {prob:.3f}")

    # For mixed states, coherence should be lower (higher entropy)
    assert detection4.coherence < 0.8, f"Expected coherence < 0.8 for mixed state, got {detection4.coherence:.3f}"
    print("✅ PASS: Mixed state shows lower coherence")
    print()

    # Scenario 5: BAGUA modulation (high Lake Joy = lateral blending)
    print("Scenario 5: BAGUA MODULATION - Lake Joy lateral blending")
    print("-" * 60)
    text5 = "I'm feeling a bit anxious, but also curious and open."
    bagua_context = {
        'lake_joy': 0.718,  # High Lake Joy (from BAGUA addendum)
        'creative_force': 0.250
    }
    detection5_no_bagua = detector.detect_polyvagal_state(text5)
    detection5_with_bagua = detector.detect_polyvagal_state(text5, bagua_context)

    print(f"Text: {text5}")
    print(f"\nWithout BAGUA modulation:")
    print(f"  Dominant: {detection5_no_bagua.dominant_state} ({detection5_no_bagua.confidence:.3f})")
    print(f"  Mixed: {detection5_no_bagua.mixed_activation}")

    print(f"\nWith BAGUA modulation (Lake Joy = 0.718):")
    print(f"  Dominant: {detection5_with_bagua.dominant_state} ({detection5_with_bagua.confidence:.3f})")
    print(f"  Mixed: {detection5_with_bagua.mixed_activation}")

    # Lake Joy should flatten distribution (reduce peak confidence)
    assert detection5_with_bagua.confidence <= detection5_no_bagua.confidence + 0.01, \
        f"Expected BAGUA to flatten or maintain distribution"
    print("✅ PASS: BAGUA modulation flattens distribution")
    print()

    # Test quick utility functions
    print("=" * 60)
    print("QUICK UTILITY FUNCTIONS")
    print("=" * 60)
    print()

    # Test quick_polyvagal_check
    state, confidence = quick_polyvagal_check("I feel safe and grounded.")
    print(f"quick_polyvagal_check('I feel safe and grounded.')")
    print(f"  → State: {state}, Confidence: {confidence:.3f}")
    assert state == "ventral", f"Expected 'ventral', got '{state}'"
    print("✅ PASS: quick_polyvagal_check works")
    print()

    # Test is_safe_to_engage (with fresh model threshold)
    safe1 = is_safe_to_engage("I feel curious and open.", threshold=0.4)
    safe2 = is_safe_to_engage("I'm shutting down and numb.", threshold=0.4)
    print(f"is_safe_to_engage('I feel curious and open.', threshold=0.4)")
    print(f"  → {safe1}")
    print(f"is_safe_to_engage('I'm shutting down and numb.', threshold=0.4)")
    print(f"  → {safe2}")
    assert safe1 == True, "Expected True for ventral state"
    assert safe2 == False, "Expected False for dorsal state"
    print("✅ PASS: is_safe_to_engage safety checks work (fresh model threshold)")
    print()

    # Test OFEL integration (prehend_text interface)
    print("=" * 60)
    print("OFEL INTEGRATION (prehend_text interface)")
    print("=" * 60)
    print()

    output = detector.prehend_text("I feel overwhelmed and anxious.")
    print(f"prehend_text('I feel overwhelmed and anxious.')")
    print(f"  polyvagal_state: {output['polyvagal_state']}")
    print(f"  confidence: {output['confidence']:.3f}")
    print(f"  coherence: {output['coherence']:.3f}")
    print(f"  energy_cost: {output['energy_cost']:.3f} (for E_polyvagal)")
    print(f"  lure: {output['lure']:.3f}")
    print(f"  organ_name: {output['organ_name']}")

    assert output['organ_name'] == 'EO_POLYVAGAL', f"Expected 'EO_POLYVAGAL', got '{output['organ_name']}'"
    assert 'energy_cost' in output, "Missing energy_cost for OFEL integration"
    print("✅ PASS: OFEL integration interface works")
    print()

    print("=" * 60)
    print("POLYVAGAL DETECTOR VALIDATION COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print("  ✅ Ventral state detection")
    print("  ✅ Sympathetic state detection")
    print("  ✅ Dorsal state detection")
    print("  ✅ Mixed state coherence")
    print("  ✅ BAGUA modulation (Lake Joy)")
    print("  ✅ Quick utility functions")
    print("  ✅ OFEL integration interface")
    print()
    print("Status: ALL TESTS PASSED ✨")


if __name__ == "__main__":
    test_polyvagal_scenarios()
