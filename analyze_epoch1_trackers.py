#!/usr/bin/env python3
"""
Epoch 1 Phase 3B Tracker Analysis
==================================

Analyzes the statistics from all 5 Phase 3B trackers after Epoch 1 training.

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
"""

import sys
from pathlib import Path
import json

# Set PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

def analyze_epoch1_trackers():
    """Analyze Phase 3B tracker outputs after Epoch 1."""

    print("=" * 80)
    print("📊 EPOCH 1 PHASE 3B TRACKER ANALYSIS")
    print("=" * 80)
    print()

    # Import wrapper
    print("📋 Step 1: Load Wrapper with All Trackers")
    print("-" * 80)

    from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

    wrapper = ConversationalOrganismWrapper()

    print("✅ Wrapper loaded")
    print()

    # Check JSON files
    print("📋 Step 2: Check JSON Storage Files")
    print("-" * 80)

    storage_dir = Path("persona_layer/state/active")
    expected_files = {
        "word_occasion_patterns.json": "WordOccasionTracker",
        "cycle_convergence_stats.json": "CycleConvergenceTracker",
        "gate_cascade_quality.json": "GateCascadeQualityTracker",
        "nexus_vs_llm_decisions.json": "NexusVsLLMDecisionTracker",
        "neighbor_word_context.json": "NeighborWordContextTracker"
    }

    files_status = {}
    for filename, tracker_name in expected_files.items():
        filepath = storage_dir / filename
        exists = filepath.exists()
        status_str = "✅ EXISTS" if exists else "❌ NOT FOUND"
        print(f"  {filename}: {status_str}")
        files_status[tracker_name] = exists

        if exists:
            # Show file size
            size_kb = filepath.stat().st_size / 1024
            print(f"     Size: {size_kb:.2f} KB")

    print()
    print(f"Files created: {sum(files_status.values())}/5")
    print()

    # Analyze each tracker
    print("📋 Step 3: Tracker Statistics Breakdown")
    print("-" * 80)
    print()

    # Tracker 1: WordOccasionTracker
    print("🔹 Tracker 1: WordOccasionTracker")
    print("-" * 80)
    if wrapper.word_occasion_tracker:
        try:
            stats = wrapper.word_occasion_tracker.get_statistics()
            print(f"  Total updates: {stats.get('total_updates', 0)}")
            print(f"  Unique words tracked: {stats.get('total_word_patterns', 0)}")
            print(f"  Reliable patterns (≥3 mentions): {stats.get('reliable_patterns', 0)}")

            # Show top 5 most mentioned words
            word_stats = stats.get('word_stats', {})
            if word_stats:
                sorted_words = sorted(
                    word_stats.items(),
                    key=lambda x: x[1].get('mention_count', 0),
                    reverse=True
                )[:5]
                print(f"  Top 5 words:")
                for word, word_data in sorted_words:
                    mentions = word_data.get('mention_count', 0)
                    avg_activation = word_data.get('avg_organ_activation', 0.0)
                    print(f"    - {word}: {mentions} mentions, {avg_activation:.3f} avg activation")
            else:
                print(f"  ⚠️  No word patterns learned")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
    else:
        print(f"  ❌ Tracker not initialized")
    print()

    # Tracker 2: CycleConvergenceTracker
    print("🔹 Tracker 2: CycleConvergenceTracker")
    print("-" * 80)
    if wrapper.cycle_convergence_tracker:
        try:
            stats = wrapper.cycle_convergence_tracker.get_statistics()
            global_stats = stats.get('global', {})
            print(f"  Total convergence attempts: {global_stats.get('total_attempts', 0)}")
            print(f"  Mean cycles to kairos: {global_stats.get('mean_cycles_to_kairos', 0.0):.2f}")
            print(f"  Kairos success rate: {global_stats.get('kairos_success_rate', 0.0):.1%}")

            # Context breakdown
            context_stats = stats.get('context_stats', {})
            if context_stats:
                print(f"  Context patterns learned:")
                for context_key, context_data in context_stats.items():
                    attempts = context_data.get('attempts', 0)
                    mean_cycles = context_data.get('mean_cycles_to_kairos', 0.0)
                    print(f"    - {context_key}: {attempts} attempts, {mean_cycles:.2f} avg cycles")
            else:
                print(f"  ⚠️  No context patterns learned")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
    else:
        print(f"  ❌ Tracker not initialized")
    print()

    # Tracker 3: GateCascadeQualityTracker
    print("🔹 Tracker 3: GateCascadeQualityTracker")
    print("-" * 80)
    if wrapper.gate_cascade_quality_tracker:
        try:
            stats = wrapper.gate_cascade_quality_tracker.get_statistics()
            print(f"  Total attempts: {stats.get('total_attempts', 0)}")
            print(f"  Bottleneck gate: {stats.get('bottleneck_gate', 'None')}")

            # Per-gate statistics
            gate_stats = stats.get('gate_stats', {})
            if gate_stats:
                print(f"  Gate pass rates:")
                for gate_name, gate_data in sorted(gate_stats.items()):
                    pass_rate = gate_data.get('pass_rate', 0.0)
                    attempts = gate_data.get('attempts', 0)
                    avg_score = gate_data.get('avg_score', 0.0)
                    print(f"    - {gate_name}: {pass_rate:.1%} pass rate ({attempts} attempts), {avg_score:.3f} avg score")
            else:
                print(f"  ⚠️  No gate statistics available")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
    else:
        print(f"  ❌ Tracker not initialized")
    print()

    # Tracker 4: NexusVsLLMDecisionTracker
    print("🔹 Tracker 4: NexusVsLLMDecisionTracker")
    print("-" * 80)
    if wrapper.nexus_vs_llm_tracker:
        try:
            stats = wrapper.nexus_vs_llm_tracker.get_statistics()
            usage_stats = stats.get('usage', {})
            performance_stats = stats.get('performance', {})

            print(f"  Total decisions: {usage_stats.get('total_decisions', 0)}")
            print(f"  NEXUS usage rate: {usage_stats.get('nexus_usage_rate', 0.0):.1%}")
            print(f"  LLM fallback rate: {usage_stats.get('llm_fallback_rate', 0.0):.1%}")

            # Performance comparison
            if performance_stats:
                nexus_time = performance_stats.get('avg_nexus_time_ms', 0.0)
                llm_time = performance_stats.get('avg_llm_time_ms', 0.0)
                speedup = performance_stats.get('speedup_factor', 0.0)
                print(f"  Avg NEXUS time: {nexus_time:.2f}ms")
                print(f"  Avg LLM time: {llm_time:.2f}ms")
                print(f"  Speedup factor: {speedup:.1f}×")
            else:
                print(f"  ⚠️  No performance data available")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
    else:
        print(f"  ❌ Tracker not initialized")
    print()

    # Tracker 5: NeighborWordContextTracker
    print("🔹 Tracker 5: NeighborWordContextTracker")
    print("-" * 80)
    if wrapper.neighbor_word_context_tracker:
        try:
            stats = wrapper.neighbor_word_context_tracker.get_statistics()
            print(f"  Total updates: {stats.get('total_updates', 0)}")
            print(f"  Unique neighbor patterns: {stats.get('total_neighbor_patterns', 0)}")
            print(f"  Reliable patterns (≥5 co-occurrences): {stats.get('reliable_patterns', 0)}")

            # Show top 5 neighbor pairs
            neighbor_stats = stats.get('neighbor_stats', {})
            if neighbor_stats:
                sorted_neighbors = sorted(
                    neighbor_stats.items(),
                    key=lambda x: x[1].get('co_occurrence_count', 0),
                    reverse=True
                )[:5]
                print(f"  Top 5 neighbor pairs:")
                for neighbor_key, neighbor_data in sorted_neighbors:
                    count = neighbor_data.get('co_occurrence_count', 0)
                    avg_boost = neighbor_data.get('avg_boost', 0.0)
                    print(f"    - {neighbor_key}: {count} co-occurrences, {avg_boost:.3f} avg boost")
            else:
                print(f"  ⚠️  No neighbor patterns learned")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
    else:
        print(f"  ❌ Tracker not initialized")
    print()

    # Summary and diagnosis
    print("=" * 80)
    print("📋 DIAGNOSIS & NEXT STEPS")
    print("=" * 80)
    print()

    # Check minimum success criteria
    min_criteria = {
        "JSON files created": sum(files_status.values()) == 5,
        "CycleConvergenceTracker has data": (
            wrapper.cycle_convergence_tracker and
            wrapper.cycle_convergence_tracker.get_statistics().get('global', {}).get('total_attempts', 0) > 0
        ),
        "NexusVsLLMDecisionTracker has data": (
            wrapper.nexus_vs_llm_tracker and
            wrapper.nexus_vs_llm_tracker.get_statistics().get('usage', {}).get('total_decisions', 0) > 0
        )
    }

    print("🎯 Minimum Success Criteria:")
    for criterion, met in min_criteria.items():
        status = "✅ MET" if met else "❌ NOT MET"
        print(f"  {criterion}: {status}")
    print()

    # Identify issues
    print("🔍 Issues Identified:")
    issues = []

    if not files_status.get("WordOccasionTracker", False):
        issues.append("WordOccasionTracker JSON not created - no word_occasions in context")

    if not files_status.get("GateCascadeQualityTracker", False):
        issues.append("GateCascadeQualityTracker JSON not created - no gate_results in context")

    if not files_status.get("NeighborWordContextTracker", False):
        issues.append("NeighborWordContextTracker JSON not created - no neighbor data in context")

    # Check if trackers have 0 data
    if wrapper.word_occasion_tracker:
        total_updates = wrapper.word_occasion_tracker.get_statistics().get('total_updates', 0)
        if total_updates == 0:
            issues.append("WordOccasionTracker has 0 updates - context not passed correctly")

    if not issues:
        print("  ✅ No issues found!")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    print()

    # Recommendations
    print("💡 Recommendations:")
    if issues:
        print("  1. Modify epoch training script to call entity extraction with return_word_occasions=True")
        print("  2. Add word_occasions, nexus_entities, and gate_results to context before process_text()")
        print("  3. Re-run Epoch 1 training with proper context extensions")
    else:
        print("  ✅ System working as expected! Proceed with Epoch 2 training.")
    print()

    print("=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    print()

    return True


if __name__ == "__main__":
    success = analyze_epoch1_trackers()
    sys.exit(0 if success else 1)
