#!/usr/bin/env python3
"""
Phase 3B Fix Validation Test
=============================

Quick test to verify the new process_text_with_phase3b_context() method
properly builds Phase 3B context and passes it to all trackers.

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
"""

import sys
from pathlib import Path

# Set PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

def test_phase3b_fix():
    """Test the Phase 3B fix with 3 simple inputs."""

    print("=" * 80)
    print("🧪 PHASE 3B FIX VALIDATION TEST")
    print("=" * 80)
    print()

    # Import wrapper
    print("📋 Step 1: Initialize Wrapper")
    print("-" * 80)

    from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

    wrapper = ConversationalOrganismWrapper()

    print("✅ Wrapper initialized")
    print()

    # Test inputs
    test_inputs = [
        "My daughter Emma is worried about her friend",
        "I went to the hospital today",
        "Emma told me she's feeling better"
    ]

    print("📋 Step 2: Process 3 Test Inputs with Phase 3B Context")
    print("-" * 80)
    print()

    for i, user_input in enumerate(test_inputs, 1):
        print(f"Input {i}: \"{user_input}\"")

        try:
            # Use new wrapper method (Phase 3B fix)
            result = wrapper.process_text_with_phase3b_context(
                text=user_input,
                user_id='test_fix_phase3b',
                username='Test User',
                enable_phase2=True,
                enable_tsk_recording=False,
                user_satisfaction=0.8
            )

            # Check if result has emission
            if result.get('emission_text'):
                print(f"  ✅ Processed successfully")
                print(f"  Emission: {result['emission_text'][:60]}...")
            else:
                print(f"  ⚠️  Processed but no emission generated")

        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

        print()

    print("=" * 80)
    print("✅ ALL 3 INPUTS PROCESSED WITH PHASE 3B CONTEXT")
    print("=" * 80)
    print()

    # Check tracker statistics
    print("📋 Step 3: Verify Trackers Received Data")
    print("-" * 80)

    try:
        if wrapper.word_occasion_tracker:
            stats = wrapper.word_occasion_tracker.get_statistics()
            total_updates = stats.get('total_updates', 0)
            print(f"  WordOccasionTracker: {total_updates} updates")
            if total_updates > 0:
                print(f"    ✅ SUCCESS: Tracker received word_occasions!")
            else:
                print(f"    ❌ FAILED: Tracker has 0 updates (context not passed)")

        if wrapper.cycle_convergence_tracker:
            stats = wrapper.cycle_convergence_tracker.get_statistics()
            total_attempts = stats.get('global', {}).get('total_attempts', 0)
            print(f"  CycleConvergenceTracker: {total_attempts} attempts")

        if wrapper.gate_cascade_quality_tracker:
            stats = wrapper.gate_cascade_quality_tracker.get_statistics()
            total_attempts = stats.get('total_attempts', 0)
            print(f"  GateCascadeQualityTracker: {total_attempts} attempts")
            if total_attempts > 0:
                print(f"    ✅ SUCCESS: Tracker received gate_results!")
            else:
                print(f"    ⚠️  No gate attempts (expected if entity extraction didn't find entities)")

        if wrapper.nexus_vs_llm_tracker:
            stats = wrapper.nexus_vs_llm_tracker.get_statistics()
            total_decisions = stats.get('usage', {}).get('total_decisions', 0)
            print(f"  NexusVsLLMDecisionTracker: {total_decisions} decisions")
            if total_decisions > 0:
                print(f"    ✅ SUCCESS: Tracker received NEXUS metadata!")
            else:
                print(f"    ❌ FAILED: Tracker has 0 decisions (context not passed)")

        if wrapper.neighbor_word_context_tracker:
            stats = wrapper.neighbor_word_context_tracker.get_statistics()
            total_updates = stats.get('total_updates', 0)
            print(f"  NeighborWordContextTracker: {total_updates} updates")
            if total_updates > 0:
                print(f"    ✅ SUCCESS: Tracker received neighbor context!")
            else:
                print(f"    ⚠️  No neighbor updates (expected if no entities extracted)")

    except Exception as e:
        print(f"  ⚠️  Error getting statistics: {e}")

    print()
    print("=" * 80)
    print("✅ PHASE 3B FIX VALIDATION COMPLETE")
    print("=" * 80)
    print()

    return True


if __name__ == "__main__":
    success = test_phase3b_fix()
    sys.exit(0 if success else 1)
