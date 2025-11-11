#!/usr/bin/env python3
"""
ARC-AGI 2.0 Training - 1,000 Tasks with 99% Threshold
=====================================================

Scale to full ARC-AGI 2.0 training set (1,000 tasks)
With accumulated knowledge from ARC 1.0 (400 tasks)

Key Improvements:
- 93 perfect solutions from ARC 1.0
- 71 high-quality patterns (99%+ threshold)
- 34 mature organic families
- Global confidence: 1.00

Created: November 3, 2025
"""

import sys
import os

# Add to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from core.complete_organic_system import CompleteOrganicSystem
from core.tsk_log_memory import TSKLogMemory
import json
import numpy as np
from datetime import datetime


def main():
    """Run ARC-AGI 2.0 training on 1,000 tasks."""

    print("🚀 Starting ARC-AGI 2.0 Training (1,000 Tasks)")
    print("   Building on ARC 1.0 success: 93 perfect tasks")
    print("   99% threshold for near-perfect pattern storage")
    print("   Progressive difficulty + Organic discovery")
    print()

    # Initialize system with accumulated knowledge
    system = CompleteOrganicSystem()

    # Set 99% threshold
    system.tsk_memory = TSKLogMemory(
        log_dir=os.path.join(system.base_path, "data/logs"),
        min_recall_threshold=0.99
    )

    # ARC-AGI 2.0 path (JSON format)
    arc2_challenges_path = "/Users/daedalea/Desktop/DAE_HYPHAE_1/arc_data/arc2/arc-agi_training_challenges.json"
    arc2_solutions_path = "/Users/daedalea/Desktop/DAE_HYPHAE_1/arc_data/arc2/arc-agi_training_solutions.json"

    print(f"\n{'='*80}")
    print("ARC-AGI 2.0 FULL TRAINING - 99% THRESHOLD")
    print(f"{'='*80}")
    print("Strategy: Scale with accumulated knowledge from 400-task foundation")
    print("Quality: Only store transformations with 99%+ accuracy")
    print("Goal: Maximize pattern accumulation across 1,000 diverse tasks")
    print()

    # Run batch learning
    results = batch_learning_arc2(
        system,
        arc2_challenges_path,
        arc2_solutions_path,
        checkpoint_frequency=50
    )

    print("\n✅ ARC-AGI 2.0 training complete!")
    print(f"   Final success rate: {results['success_rate']:.1%}")
    print(f"   Near-perfect tasks: {results['near_perfect']} ({results['near_perfect_rate']:.1%})")
    print(f"   Total patterns stored: {results.get('total_patterns', 'N/A')}")
    print(f"   Organic families: {results.get('organic_families', 'N/A')}")


def batch_learning_arc2(
    system: CompleteOrganicSystem,
    challenges_path: str,
    solutions_path: str,
    checkpoint_frequency: int = 50
):
    """
    Batch learning on ARC-AGI 2.0 (1,000 tasks) with 99% threshold.

    ARC-AGI 2.0 format:
    - challenges.json: {task_id: {'train': [...], 'test': [...]}}
    - solutions.json: {task_id: [[solution_grid]]}
    """

    print(f"\n📊 Loading ARC-AGI 2.0 dataset...")

    # Load challenges
    with open(challenges_path, 'r') as f:
        challenges = json.load(f)

    # Load solutions
    with open(solutions_path, 'r') as f:
        solutions = json.load(f)

    print(f"   ✅ Loaded {len(challenges)} training tasks")
    print(f"   ✅ Loaded {len(solutions)} solutions")

    # Sort by difficulty
    print(f"   Sorting by difficulty (easiest → hardest)...")
    sorted_task_ids = sort_arc2_by_difficulty(challenges)
    print(f"   ✅ Sorted {len(sorted_task_ids)} tasks")

    results = []
    successful = 0  # ≥90% accuracy
    near_perfect = 0  # ≥99% accuracy
    total = 0

    checkpoint_stats = []
    start_time = datetime.now()

    for i, task_id in enumerate(sorted_task_ids):
        print(f"\n[{i+1}/{len(sorted_task_ids)}] {task_id}")

        try:
            task_data = challenges[task_id]
            solution_grids = solutions[task_id]

            # Convert to numpy
            training_examples = [
                (np.array(pair['input']), np.array(pair['output']))
                for pair in task_data['train']
            ]

            # Use first test input/output
            test_input = np.array(task_data['test'][0]['input'])
            test_output = np.array(solution_grids[0])

            # Learn organically
            result = system.learn_task_organically(
                task_id=task_id,
                training_examples=training_examples,
                test_input=test_input,
                test_output=test_output,
                max_iterations=15
            )

            results.append(result)
            total += 1

            # Track successes
            if result['test_accuracy'] >= 0.9:
                successful += 1
                print(f"   ✅ Success: {result['test_accuracy']:.1%}")
            else:
                print(f"   ❌ Below threshold: {result['test_accuracy']:.1%}")

            if result['test_accuracy'] >= 0.99:
                near_perfect += 1
                print(f"   ✨ NEAR-PERFECT! {result['test_accuracy']:.1%}")

            # Checkpoint
            if (i + 1) % checkpoint_frequency == 0:
                elapsed = (datetime.now() - start_time).total_seconds()

                tsk_stats = system.tsk_memory.get_statistics()
                family_stats = system.organic_learner.get_transformation_statistics()
                trajectory = system.persistent_state.get_learning_trajectory()

                checkpoint_data = {
                    'task_index': i + 1,
                    'successful': successful,
                    'near_perfect': near_perfect,
                    'success_rate': successful / max(total, 1),
                    'near_perfect_rate': near_perfect / max(total, 1),
                    'global_confidence': trajectory['global_confidence'],
                    'organic_families': family_stats['organic_families'],
                    'high_conf_patterns': tsk_stats['high_conf_mappings']
                }

                checkpoint_stats.append(checkpoint_data)
                system.persistent_state.save_state()

                print(f"\n{'='*80}")
                print(f"CHECKPOINT {i+1}/{len(sorted_task_ids)}")
                print(f"{'='*80}")
                print(f"   Success rate: {successful/total:.1%} ({successful}/{total})")
                print(f"   Near-perfect rate: {near_perfect/total:.1%} ({near_perfect}/{total})")
                print(f"   Global confidence: {trajectory['global_confidence']:.2f}")
                print(f"   Organic families: {family_stats['organic_families']}")
                print(f"   High-quality patterns: {tsk_stats['high_conf_mappings']}")
                print(f"   Elapsed: {elapsed/60:.1f} min")
                print(f"{'='*80}\n")

        except Exception as e:
            print(f"   ⚠️ Error: {e}")
            import traceback
            traceback.print_exc()
            total += 1

    # Final summary
    print("\n" + "="*80)
    print("ARC-AGI 2.0 TRAINING SUMMARY (1,000 TASKS)")
    print("="*80)

    print(f"\n📊 Overall Performance:")
    print(f"   Total tasks: {total}")
    print(f"   Successful (≥90%): {successful} ({successful/max(total,1):.1%})")
    print(f"   Near-perfect (≥99%): {near_perfect} ({near_perfect/max(total,1):.1%})")

    if results:
        accuracies = [r['test_accuracy'] for r in results]
        print(f"\n   Accuracy distribution:")
        print(f"      Mean: {np.mean(accuracies):.1%}")
        print(f"      Median: {np.median(accuracies):.1%}")
        print(f"      Best: {max(accuracies):.1%}")
        print(f"      Std dev: {np.std(accuracies):.1%}")

    # Organic families
    family_stats = system.organic_learner.get_transformation_statistics()
    print(f"\n🌱 Organic Discovery:")
    print(f"   Total transformations: {family_stats['total_discoveries']}")
    print(f"   Organic families: {family_stats['organic_families']}")

    # Persistent state
    trajectory = system.persistent_state.get_learning_trajectory()
    print(f"\n📈 Learning Trajectory:")
    print(f"   Global confidence: {trajectory['global_confidence']:.2f}")
    print(f"   Overall success rate: {trajectory['current_success_rate']:.1%}")

    # TSK memory
    tsk_stats = system.tsk_memory.get_statistics()
    print(f"\n💾 High-Quality Memory (99% threshold):")
    print(f"   Near-perfect patterns: {tsk_stats['high_conf_mappings']}")
    print(f"   Total patterns: {tsk_stats['total_patterns']}")

    # Time analysis
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n⏱️ Performance:")
    print(f"   Total time: {elapsed/3600:.2f} hours")
    print(f"   Average per task: {elapsed/max(total, 1):.1f} seconds")

    # Checkpoint progression
    if checkpoint_stats:
        print(f"\n📊 Checkpoint Progression:")
        for cp in checkpoint_stats[-10:]:  # Last 10 checkpoints
            print(f"   [{cp['task_index']:4d}] Success: {cp['success_rate']:.1%}, "
                  f"Near-perfect: {cp['near_perfect_rate']:.1%}, "
                  f"Families: {cp['organic_families']}")

    system.persistent_state.end_session()

    return {
        'results': results,
        'successful': successful,
        'near_perfect': near_perfect,
        'total': total,
        'success_rate': successful / max(total, 1),
        'near_perfect_rate': near_perfect / max(total, 1),
        'checkpoint_stats': checkpoint_stats,
        'total_patterns': tsk_stats['total_patterns'],
        'organic_families': family_stats['organic_families'],
        'elapsed_hours': elapsed / 3600
    }


def sort_arc2_by_difficulty(challenges: dict) -> list:
    """Sort ARC-AGI 2.0 tasks by estimated difficulty."""

    difficulties = []

    for task_id, task_data in challenges.items():
        try:
            # Get first training pair
            inp = np.array(task_data['train'][0]['input'])
            out = np.array(task_data['train'][0]['output'])

            # Difficulty factors
            shape_diff = abs(np.prod(out.shape) - np.prod(inp.shape))
            color_count = len(np.unique(inp)) + len(np.unique(out))
            training_pairs = len(task_data['train'])

            # Combined difficulty
            difficulty = (shape_diff * color_count) / max(training_pairs, 1)

            difficulties.append((task_id, difficulty))

        except:
            difficulties.append((task_id, 999999))

    # Sort by difficulty (easiest first)
    difficulties.sort(key=lambda x: x[1])

    return [task_id for task_id, _ in difficulties]


if __name__ == "__main__":
    main()
