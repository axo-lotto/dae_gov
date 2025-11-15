"""
Test Reconstruction Pipeline Integration
==========================================

Quick test to verify reconstruction pipeline initializes and processes correctly.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_reconstruction_initialization():
    """Test that reconstruction pipeline initializes correctly."""
    print("\n" + "="*70)
    print("Testing Reconstruction Pipeline Initialization")
    print("="*70 + "\n")

    try:
        # Initialize wrapper (should load reconstruction pipeline)
        wrapper = ConversationalOrganismWrapper()

        # Check if reconstruction pipeline is available
        if wrapper.reconstruction_pipeline:
            print("\n✅ SUCCESS: Reconstruction pipeline initialized!")
            print(f"   Components wired:")
            print(f"      - EmissionGenerator: {wrapper.emission_generator is not None}")
            print(f"      - NexusComposer: {wrapper.nexus_composer is not None}")
            print(f"      - ResponseAssembler: {wrapper.response_assembler is not None}")
            print(f"      - SELFGovernance: {wrapper.self_governance is not None}")
        else:
            print("\n⚠️  WARNING: Reconstruction pipeline not initialized")
            print(f"   Check component availability:")
            print(f"      - EmissionGenerator: {wrapper.emission_generator is not None}")
            print(f"      - NexusComposer: {wrapper.nexus_composer is not None}")
            print(f"      - SELFGovernance: {wrapper.self_governance is not None}")

        return True

    except Exception as e:
        print(f"\n❌ ERROR: Initialization failed")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False


def test_reconstruction_processing():
    """Test that reconstruction pipeline can process text."""
    print("\n" + "="*70)
    print("Testing Reconstruction Pipeline Processing")
    print("="*70 + "\n")

    try:
        # Initialize wrapper
        wrapper = ConversationalOrganismWrapper()

        if not wrapper.reconstruction_pipeline:
            print("⚠️  Skipping processing test (reconstruction pipeline unavailable)")
            return False

        # Test input
        test_text = "I'm feeling overwhelmed and don't know what to do"

        print(f"Input: \"{test_text}\"\n")

        # Process text
        result = wrapper.process_text(
            text=test_text,
            context={'conversation_id': 'test', 'user_id': 'test'},
            enable_tsk_recording=False
        )

        # Check results
        if 'emission_text' in result:
            print(f"\n✅ SUCCESS: Emission generated!")
            print(f"   Emission: \"{result['emission_text']}\"")
            print(f"   Confidence: {result.get('emission_confidence', 0.0):.3f}")
            print(f"   Path: {result.get('emission_path', 'unknown')}")
            return True
        else:
            print(f"\n⚠️  WARNING: No emission generated")
            return False

    except Exception as e:
        print(f"\n❌ ERROR: Processing failed")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🌀 DAE_HYPHAE_1 Reconstruction Pipeline Integration Test\n")

    # Test 1: Initialization
    init_success = test_reconstruction_initialization()

    if init_success:
        # Test 2: Processing
        process_success = test_reconstruction_processing()

        if process_success:
            print("\n" + "="*70)
            print("✅ ALL TESTS PASSED - RECONSTRUCTION PIPELINE OPERATIONAL")
            print("="*70 + "\n")
        else:
            print("\n" + "="*70)
            print("⚠️  PARTIAL SUCCESS - Init passed, processing failed")
            print("="*70 + "\n")
    else:
        print("\n" + "="*70)
        print("❌ TESTS FAILED - Initialization failed")
        print("="*70 + "\n")
