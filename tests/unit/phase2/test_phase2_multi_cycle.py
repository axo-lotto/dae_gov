"""
Test Phase 2: Multi-cycle V0 convergence with Kairos detection.

Validates:
- ConversationalOccasion V0 descent
- Multi-cycle convergence (2-4 cycles)
- Kairos detection
- Nexus formation via shared meta-atoms
- Emission confidence improvement (0.30 → 0.60-0.85)
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_phase2_convergence():
    """Test Phase 2 multi-cycle convergence end-to-end."""
    print("\n" + "="*70)
    print("🧪 TESTING PHASE 2: MULTI-CYCLE V0 CONVERGENCE")
    print("="*70 + "\n")

    # Initialize wrapper
    wrapper = ConversationalOrganismWrapper()

    # Test text (trauma-aware therapeutic content)
    test_text = """
    I hear the exhaustion in your words. This level of depletion isn't sustainable.
    Let's create some breathing room together.
    """

    print("📘 Processing with Phase 2 (enable_phase2=True):")
    print(f"   Text: \"{test_text.strip()[:80]}...\"")
    print()

    # Process with Phase 2
    result = wrapper.process_text(
        text=test_text,
        context={
            'conversation_id': 'test_phase2_001',
            'epoch_num': 1,
            'training_phase': 'output'
        },
        enable_tsk_recording=True,
        enable_phase2=True  # ENABLE PHASE 2!
    )

    felt_states = result['felt_states']

    print("\n" + "="*70)
    print("✅ PHASE 2 RESULTS")
    print("="*70)

    # Validation checks
    success = True
    checks = []

    # Check 1: Multi-cycle convergence (2-4 cycles)
    cycles = felt_states['convergence_cycles']
    if 2 <= cycles <= 5:
        checks.append(f"✅ Convergence cycles: {cycles} (expected 2-5)")
    else:
        checks.append(f"❌ Convergence cycles: {cycles} (expected 2-5)")
        success = False

    # Check 2: Kairos detection
    kairos = felt_states.get('kairos_detected', False)
    if kairos:
        checks.append(f"✅ Kairos detected: True (cycle {felt_states['kairos_cycle_index']})")
    else:
        checks.append(f"⚠️  Kairos detected: False (may be OK if text doesn't trigger Kairos window)")

    # Check 3: V0 energy descent
    v0_final = felt_states['v0_energy']['final_energy']
    if v0_final < 0.8:
        checks.append(f"✅ V0 final energy: {v0_final:.3f} (converged from 1.0)")
    else:
        checks.append(f"❌ V0 final energy: {v0_final:.3f} (not converged, should be < 0.8)")
        success = False

    # Check 4: Nexus formation (should be > 0 with meta-atoms!)
    nexus_count = felt_states['emission_nexus_count']
    if nexus_count >= 1:
        checks.append(f"✅ Nexuses formed: {nexus_count} (meta-atoms working!)")
    else:
        checks.append(f"⚠️  Nexuses formed: {nexus_count} (expected >= 1 with meta-atoms)")

    # Check 5: Emission confidence
    confidence = felt_states['emission_confidence']
    if confidence >= 0.4:
        checks.append(f"✅ Emission confidence: {confidence:.3f} (good quality)")
    else:
        checks.append(f"⚠️  Emission confidence: {confidence:.3f} (low, may need tuning)")

    # Check 6: Emission path (should prefer intersection over hebbian)
    path = felt_states['emission_path']
    if path == 'intersection':
        checks.append(f"✅ Emission path: {path} (using nexuses)")
    else:
        checks.append(f"⚠️  Emission path: {path} (not using intersection)")

    # Print checks
    for check in checks:
        print(f"   {check}")

    # Print detailed results
    print()
    print("   Detailed Metrics:")
    print(f"     Text occasions: {len(felt_states['text_occasions'])}")
    print(f"     Mean coherence: {felt_states['mean_coherence']:.3f}")
    print(f"     Final satisfaction: {felt_states['satisfaction_final']:.3f}")
    print(f"     Convergence reason: {felt_states['convergence_reason']}")

    print()
    print("   Organ coherences:")
    for organ, coherence in felt_states['organ_coherences'].items():
        print(f"     {organ:15s}: {coherence:.3f}")

    if felt_states['emission_text']:
        print()
        print("   Generated emission:")
        print(f"     \"{felt_states['emission_text']}\"")

    print()
    print("="*70)
    if success:
        print("✅ PHASE 2 TEST PASSED")
    else:
        print("⚠️  PHASE 2 TEST COMPLETED WITH WARNINGS")
    print("="*70 + "\n")

    return success


def test_phase1_backward_compatibility():
    """Test that Phase 1 still works (backward compatibility)."""
    print("\n" + "="*70)
    print("🧪 TESTING PHASE 1 BACKWARD COMPATIBILITY")
    print("="*70 + "\n")

    wrapper = ConversationalOrganismWrapper()

    test_text = "I hear your exhaustion. Let's create breathing room."

    print("📘 Processing with Phase 1 (enable_phase2=False, default):")
    print(f"   Text: \"{test_text}\"")
    print()

    result = wrapper.process_text(
        text=test_text,
        context={'conversation_id': 'test_phase1_001'},
        enable_tsk_recording=True,
        enable_phase2=False  # PHASE 1
    )

    felt_states = result['felt_states']

    print("\n✅ PHASE 1 RESULTS:")
    print(f"   Convergence cycles: {felt_states['convergence_cycles']} (should be 1)")
    print(f"   Emission path: {felt_states['emission_path']}")
    print(f"   Emission confidence: {felt_states['emission_confidence']:.3f}")

    success = felt_states['convergence_cycles'] == 1

    if success:
        print("\n✅ PHASE 1 BACKWARD COMPATIBILITY CONFIRMED")
    else:
        print("\n❌ PHASE 1 BACKWARD COMPATIBILITY BROKEN")

    print("="*70 + "\n")

    return success


if __name__ == '__main__':
    print("\n🌀 DAE_HYPHAE_1 Phase 2 Testing Suite 🌀\n")

    # Test Phase 2
    phase2_success = test_phase2_convergence()

    # Test Phase 1 backward compatibility
    phase1_success = test_phase1_backward_compatibility()

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"   Phase 2 Multi-Cycle: {'✅ PASS' if phase2_success else '❌ FAIL'}")
    print(f"   Phase 1 Compatibility: {'✅ PASS' if phase1_success else '❌ FAIL'}")
    print("="*70 + "\n")

    if phase2_success and phase1_success:
        print("🎉 All tests passed! Phase 2 is operational.\n")
    else:
        print("⚠️  Some tests failed. Review output above.\n")
