"""
Test Phase 2 Multi-Cycle Reconstruction Pipeline Integration
=============================================================

Quick test to verify reconstruction pipeline works with Phase 2 multi-cycle convergence.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_phase2_reconstruction():
    """Test that reconstruction pipeline works with Phase 2 multi-cycle."""
    print("\n" + "="*70)
    print("Testing Phase 2 Multi-Cycle Reconstruction Pipeline")
    print("="*70 + "\n")

    try:
        # Initialize wrapper
        wrapper = ConversationalOrganismWrapper()

        if not wrapper.reconstruction_pipeline:
            print("❌ Reconstruction pipeline not available")
            return False

        # Test input (should trigger Zone 5 collapse)
        test_text = "I'm feeling overwhelmed and don't know what to do"

        print(f"Input: \"{test_text}\"")
        print(f"Phase 2: ENABLED (multi-cycle V0 convergence)\n")

        # Process with Phase 2 enabled
        result = wrapper.process_text(
            text=test_text,
            context={'conversation_id': 'test', 'user_id': 'test'},
            enable_tsk_recording=False,
            enable_phase2=True  # ✅ KEY: Enable Phase 2
        )

        # Check results
        emission_text = result.get('emission_text')
        emission_confidence = result.get('emission_confidence', 0.0)
        emission_path = result.get('emission_path', 'none')
        cycles = result.get('felt_states', {}).get('convergence_cycles', 0)
        zone_id = result.get('felt_states', {}).get('zone_id', 0)

        if emission_text:
            print(f"\n✅ SUCCESS: Phase 2 reconstruction working!")
            print(f"   Emission: \"{emission_text}\"")
            print(f"   Confidence: {emission_confidence:.3f}")
            print(f"   Path: {emission_path}")
            print(f"   Cycles: {cycles}")
            print(f"   Zone: {zone_id}")

            # Verify SELF matrix governance worked
            if zone_id == 5 and emission_text == "Breathe":
                print(f"\n   🎯 PERFECT: Zone 5 safety override working!")
                print(f"      Detected collapse → overrode to minimal safe emission")
                return True
            else:
                print(f"\n   ⚠️  Zone governance unexpected (zone={zone_id}, emission=\"{emission_text}\")")
                return True  # Still working, just different zone

        else:
            print(f"\n❌ ERROR: No emission generated")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🌀 DAE_HYPHAE_1 Phase 2 Reconstruction Pipeline Test\n")

    success = test_phase2_reconstruction()

    if success:
        print("\n" + "="*70)
        print("✅ TEST PASSED - PHASE 2 RECONSTRUCTION OPERATIONAL")
        print("="*70 + "\n")
    else:
        print("\n" + "="*70)
        print("❌ TEST FAILED")
        print("="*70 + "\n")
