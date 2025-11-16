#!/usr/bin/env python3
"""
Quick test for wave training modulation.

Validates:
1. Wave training methods exist and are callable
2. Satisfaction modulation works correctly
3. Phase detection logic is accurate
4. Config parameters are properly loaded
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_occasion import ConversationalOccasion
from config import Config

def test_wave_training():
    """Test wave training integration."""

    print("=" * 70)
    print("🌀 Wave Training Integration Test")
    print("=" * 70)

    # 1. Test config parameters
    print("\n1. Config Parameters:")
    print(f"   ENABLE_WAVE_TRAINING: {Config.ENABLE_WAVE_TRAINING}")
    print(f"   EXPANSIVE_MOD: {Config.WAVE_TRAINING_EXPANSIVE_MOD}")
    print(f"   NAVIGATION_MOD: {Config.WAVE_TRAINING_NAVIGATION_MOD}")
    print(f"   CONCRESCENCE_MOD: {Config.WAVE_TRAINING_CONCRESCENCE_MOD}")
    print(f"   V0_MIN_CYCLES: {Config.V0_MIN_CYCLES}")
    print(f"   V0_MAX_CYCLES: {Config.V0_MAX_CYCLES}")

    # 2. Create test occasion
    occasion = ConversationalOccasion(
        position=1,
        datum="Test input for wave training"
    )

    print("\n2. Phase Detection Tests:")

    # Test EXPANSIVE phase (low satisfaction, early cycle)
    phase = occasion._determine_appetitive_phase(
        satisfaction=0.50,
        cycle=1,
        min_cycles=2,
        max_cycles=5
    )
    print(f"   satisfaction=0.50, cycle=1: {phase} (expected: EXPANSIVE)")
    assert phase == 'EXPANSIVE', f"Expected EXPANSIVE, got {phase}"

    # Test NAVIGATION phase (mid satisfaction, mid cycle)
    phase = occasion._determine_appetitive_phase(
        satisfaction=0.60,
        cycle=2,
        min_cycles=2,
        max_cycles=5
    )
    print(f"   satisfaction=0.60, cycle=2: {phase} (expected: NAVIGATION)")
    assert phase == 'NAVIGATION', f"Expected NAVIGATION, got {phase}"

    # Test CONCRESCENCE phase (high satisfaction)
    phase = occasion._determine_appetitive_phase(
        satisfaction=0.75,
        cycle=2,
        min_cycles=2,
        max_cycles=5
    )
    print(f"   satisfaction=0.75, cycle=2: {phase} (expected: CONCRESCENCE)")
    assert phase == 'CONCRESCENCE', f"Expected CONCRESCENCE, got {phase}"

    # Test CONCRESCENCE phase (late cycle)
    phase = occasion._determine_appetitive_phase(
        satisfaction=0.60,
        cycle=4,
        min_cycles=2,
        max_cycles=5
    )
    print(f"   satisfaction=0.60, cycle=4: {phase} (expected: CONCRESCENCE)")
    assert phase == 'CONCRESCENCE', f"Expected CONCRESCENCE, got {phase}"

    print("\n3. Satisfaction Modulation Tests:")

    # Test EXPANSIVE modulation (-5%)
    modulated = occasion._apply_wave_training_modulation(
        satisfaction=0.50,  # Low enough to trigger EXPANSIVE
        cycle=1,
        min_cycles=2,
        max_cycles=5
    )
    expected = 0.50 * 0.95  # -5%
    print(f"   EXPANSIVE: 0.50 → {modulated:.4f} (expected: {expected:.4f})")
    assert abs(modulated - expected) < 0.001, f"Expected {expected}, got {modulated}"

    # Test NAVIGATION modulation (0%)
    modulated = occasion._apply_wave_training_modulation(
        satisfaction=0.60,
        cycle=2,
        min_cycles=2,
        max_cycles=5
    )
    expected = 0.60  # 0%
    print(f"   NAVIGATION: 0.60 → {modulated:.4f} (expected: {expected:.4f})")
    assert abs(modulated - expected) < 0.001, f"Expected {expected}, got {modulated}"

    # Test CONCRESCENCE modulation (+5%)
    modulated = occasion._apply_wave_training_modulation(
        satisfaction=0.60,
        cycle=4,
        min_cycles=2,
        max_cycles=5
    )
    expected = 0.60 * 1.05  # +5%
    print(f"   CONCRESCENCE: 0.60 → {modulated:.4f} (expected: {expected:.4f})")
    assert abs(modulated - expected) < 0.001, f"Expected {expected}, got {modulated}"

    print("\n4. Boundary Tests:")

    # Test clipping to [0, 1]
    modulated = occasion._apply_wave_training_modulation(
        satisfaction=0.98,
        cycle=4,  # CONCRESCENCE phase
        min_cycles=2,
        max_cycles=5
    )
    print(f"   High satisfaction: 0.98 → {modulated:.4f} (should clip to 1.0)")
    assert modulated <= 1.0, f"Should clip to 1.0, got {modulated}"

    modulated = occasion._apply_wave_training_modulation(
        satisfaction=0.05,
        cycle=1,  # EXPANSIVE phase
        min_cycles=2,
        max_cycles=5
    )
    print(f"   Low satisfaction: 0.05 → {modulated:.4f} (should not go negative)")
    assert modulated >= 0.0, f"Should not go negative, got {modulated}"

    print("\n" + "=" * 70)
    print("✅ All wave training tests PASSED!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Test with full organism in interactive mode")
    print("2. Monitor satisfaction variance over 10 conversations")
    print("3. Check for nexus formation (expected 10-20% rate)")
    print("4. Validate Kairos detection improvement")

if __name__ == "__main__":
    test_wave_training()
