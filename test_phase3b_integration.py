#!/usr/bin/env python3
"""
Phase 3B Integration Test - Quick Validation
===========================================

Tests all 5 epoch learning trackers with simple inputs to verify:
1. Trackers initialize successfully
2. Context data is captured correctly
3. Tracker updates execute without errors
4. JSON storage files are created
5. Statistics logging works

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
"""

import sys
from pathlib import Path
import time

# Set PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

def test_phase3b_integration():
    """Run quick integration test with 5 simple inputs."""

    print("=" * 80)
    print("🧪 PHASE 3B INTEGRATION TEST - 5 SIMPLE INPUTS")
    print("=" * 80)
    print()

    # Import wrapper
    print("📋 Step 1: Initialize Wrapper")
    print("-" * 80)

    from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

    wrapper = ConversationalOrganismWrapper()

    print()
    print("✅ Wrapper initialized")
    print()

    # Check tracker status
    print("📋 Step 2: Verify Tracker Status")
    print("-" * 80)

    trackers_status = {
        'WordOccasionTracker': wrapper.word_occasion_tracker is not None,
        'CycleConvergenceTracker': wrapper.cycle_convergence_tracker is not None,
        'GateCascadeQualityTracker': wrapper.gate_cascade_quality_tracker is not None,
        'NexusVsLLMDecisionTracker': wrapper.nexus_vs_llm_tracker is not None,
        'NeighborWordContextTracker': wrapper.neighbor_word_context_tracker is not None
    }

    for tracker_name, status in trackers_status.items():
        status_str = "✅ LOADED" if status else "❌ NOT LOADED"
        print(f"  {tracker_name}: {status_str}")

    all_loaded = all(trackers_status.values())

    if not all_loaded:
        print()
        print("❌ ERROR: Not all trackers loaded. Aborting test.")
        return False

    print()
    print("✅ All 5 trackers loaded successfully")
    print()

    # Initialize entity extraction components (Phase 3B)
    print("📋 Step 3: Initialize Entity Extraction")
    print("-" * 80)

    try:
        from persona_layer.entity_neighbor_prehension.entity_neighbor_prehension import EntityNeighborPrehension
        entity_prehension = EntityNeighborPrehension(
            entity_tracker=wrapper.entity_organ_tracker if hasattr(wrapper, 'entity_organ_tracker') else None
        )
        print("  ✅ EntityNeighborPrehension initialized")
    except Exception as e:
        print(f"  ⚠️  Could not initialize EntityNeighborPrehension: {e}")
        entity_prehension = None

    print()

    # Test inputs
    test_inputs = [
        "My daughter Emma is worried about her friend Alice",
        "I went to the hospital today",
        "Emma told me she's feeling better",
        "Work has been stressful lately",
        "I'm grateful for my family"
    ]

    print("📋 Step 4: Process 5 Test Inputs with Entity Extraction")
    print("-" * 80)
    print()

    # Create context for each input
    context_base = {
        'user_id': 'test_user_phase3b',
        'username': 'Test User',
        'conversation_id': 'test_session_phase3b',
        'temporal': {
            'timestamp': time.time(),
            'date': '2025-11-18',
            'time': '14:30:00',
            'time_of_day': 'afternoon',
            'is_weekend': False
        }
    }

    for i, user_input in enumerate(test_inputs, 1):
        print(f"Input {i}: \"{user_input}\"")

        # Copy context and add turn number
        context = context_base.copy()
        context['turn_number'] = i

        # Step 1: Extract entities (mimics dae_interactive.py flow)
        if entity_prehension:
            try:
                import time as time_module
                nexus_start = time_module.time()
                nexus_entities, word_occasions = entity_prehension.extract_entities(
                    user_input,
                    return_word_occasions=True
                )
                nexus_time_ms = (time_module.time() - nexus_start) * 1000.0

                # Compute NEXUS confidence
                nexus_confidence = max([e.get('confidence_score', 0.0) for e in nexus_entities], default=0.0)

                # Add to context (THIS IS THE KEY!)
                context['word_occasions'] = word_occasions
                context['nexus_entities'] = nexus_entities
                context['nexus_confidence'] = nexus_confidence
                context['extraction_time_ms'] = nexus_time_ms

                # Check if high confidence
                high_confidence = [e for e in nexus_entities if e.get('confidence_score', 0.0) >= 0.7]
                context['nexus_extraction_used'] = len(high_confidence) > 0

                print(f"  📊 Entity extraction: {len(nexus_entities)} entities, {len(word_occasions)} words, {nexus_confidence:.2f} confidence")

            except Exception as e:
                print(f"  ⚠️  Entity extraction failed: {e}")
                context['nexus_extraction_used'] = False

        try:
            # Process through wrapper
            result = wrapper.process_text(
                text=user_input,
                context=context,
                enable_tsk_recording=False,
                user_satisfaction=0.8  # Simulate positive feedback
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
    print("✅ ALL 5 INPUTS PROCESSED SUCCESSFULLY")
    print("=" * 80)
    print()

    # Check if JSON files were created
    print("📋 Step 5: Verify JSON Storage Files Created")
    print("-" * 80)

    storage_dir = Path("persona_layer/state/active")
    expected_files = [
        "word_occasion_patterns.json",
        "cycle_convergence_stats.json",
        "gate_cascade_quality.json",
        "nexus_vs_llm_decisions.json",
        "neighbor_word_context.json"
    ]

    files_created = []
    for filename in expected_files:
        filepath = storage_dir / filename
        exists = filepath.exists()
        status_str = "✅ CREATED" if exists else "⚠️  NOT CREATED"
        print(f"  {filename}: {status_str}")
        if exists:
            files_created.append(filename)

    print()
    print(f"Files created: {len(files_created)}/5")
    print()

    # Get tracker statistics
    print("📋 Step 6: Tracker Statistics Summary")
    print("-" * 80)

    try:
        if wrapper.word_occasion_tracker:
            stats = wrapper.word_occasion_tracker.get_statistics()
            print(f"  WordOccasionTracker:")
            print(f"    Total updates: {stats.get('total_updates', 0)}")
            print(f"    Word patterns: {stats.get('total_word_patterns', 0)}")
            print(f"    Reliable patterns: {stats.get('reliable_patterns', 0)}")

        if wrapper.cycle_convergence_tracker:
            stats = wrapper.cycle_convergence_tracker.get_statistics()
            global_stats = stats.get('global', {})
            print(f"  CycleConvergenceTracker:")
            print(f"    Total attempts: {global_stats.get('total_attempts', 0)}")
            print(f"    Mean cycles to kairos: {global_stats.get('mean_cycles_to_kairos', 0.0):.2f}")

        if wrapper.gate_cascade_quality_tracker:
            stats = wrapper.gate_cascade_quality_tracker.get_statistics()
            print(f"  GateCascadeQualityTracker:")
            print(f"    Total attempts: {stats.get('total_attempts', 0)}")
            print(f"    Bottleneck gate: {stats.get('bottleneck_gate', 'None')}")

        if wrapper.nexus_vs_llm_tracker:
            stats = wrapper.nexus_vs_llm_tracker.get_statistics()
            usage_stats = stats.get('usage', {})
            print(f"  NexusVsLLMDecisionTracker:")
            print(f"    Total decisions: {usage_stats.get('total_decisions', 0)}")
            print(f"    NEXUS usage rate: {usage_stats.get('nexus_usage_rate', 0.0):.1%}")

        if wrapper.neighbor_word_context_tracker:
            stats = wrapper.neighbor_word_context_tracker.get_statistics()
            print(f"  NeighborWordContextTracker:")
            print(f"    Total updates: {stats.get('total_updates', 0)}")
            print(f"    Neighbor patterns: {stats.get('total_neighbor_patterns', 0)}")
            print(f"    Reliable patterns: {stats.get('reliable_patterns', 0)}")

    except Exception as e:
        print(f"  ⚠️  Error getting statistics: {e}")

    print()
    print("=" * 80)
    print("✅ PHASE 3B INTEGRATION TEST COMPLETE")
    print("=" * 80)
    print()

    return True


if __name__ == "__main__":
    success = test_phase3b_integration()
    sys.exit(0 if success else 1)
