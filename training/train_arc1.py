#!/usr/bin/env python3
"""
Full 402-Task ARC-AGI Training with 99% Threshold
=================================================

Scale to complete ARC-AGI 1.0 training dataset.
Uses proven 99% threshold for near-perfect pattern storage.

Strategy:
- Progressive difficulty sorting (easiest first)
- 99% threshold for pattern storage
- Periodic checkpoints every 25 tasks
- Comprehensive statistics tracking
- Organic family maturation monitoring

Created: November 3, 2025
"""

import sys
import os

# Add to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from core.complete_organic_system import CompleteOrganicSystem
from core.tsk_log_memory import TSKLogMemory
from pathlib import Path
import json
import numpy as np
from datetime import datetime


def main():
    """Run full 402-task training with 99% threshold."""

    print("🚀 Starting Full 402-Task ARC-AGI Training")
    print("   99% threshold for near-perfect pattern storage")
    print("   Progressive difficulty + Organic discovery")
    print("   Checkpoint every 25 tasks")
    print()

    # Initialize system
    system = CompleteOrganicSystem()

    # Set 99% threshold for recall
    print("   📊 Setting recall threshold to 99% (near-perfect only)")
    system.tsk_memory = TSKLogMemory(
        log_dir=os.path.join(system.base_path, "data/logs"),
        min_recall_threshold=0.99
    )

    # Run batch learning on ALL 402 tasks
    arc_path = "/Users/daedalea/Desktop/DAE_HYPHAE_1/arc_data/arc1/training"

    print(f"\n{'='*80}")
    print("FULL 402-TASK TRAINING - 99% THRESHOLD")
    print(f"{'='*80}")
    print("Strategy: Progressive difficulty → Build pattern database → Scale")
    print("Quality: Only store transformations with 99%+ accuracy")
    print("Goal: Maximum quality accumulated knowledge for all 402 tasks")
    print()

    # Run full batch learning
    results = batch_learning_full_dataset(system, arc_path, checkpoint_frequency=25)

    print("\n✅ Full 402-task training complete!")
    print(f"   Final success rate: {results['success_rate']:.1%}")
    print(f"   Near-perfect tasks: {results['near_perfect']} ({results['near_perfect_rate']:.1%})")
    print(f"   Total patterns stored: {results.get('total_patterns', 'N/A')}")


def batch_learning_full_dataset(
    system: CompleteOrganicSystem,
    arc_data_path: str,
    checkpoint_frequency: int = 25
):
    """
    Full 402-task batch learning with 99% threshold.

    Features:
    - Progressive difficulty sorting
    - Periodic checkpoints
    - Comprehensive statistics
    - Organic family tracking
    """

    print(f"\n📊 Loading all ARC-AGI training tasks...")

    # Load ALL tasks (no limit)
    all_task_files = sorted(Path(arc_data_path).glob("*.json"))
    print(f"   Found {len(all_task_files)} total tasks")

    # Sort by difficulty (easiest first)
    print(f"   Sorting by difficulty (easiest → hardest)...")
    sorted_tasks = system._sort_by_difficulty([str(f) for f in all_task_files])
    print(f"   ✅ Sorted {len(sorted_tasks)} tasks")

    results = []
    successful = 0  # ≥90% accuracy
    near_perfect = 0  # ≥99% accuracy
    total = 0

    # Track statistics over time
    checkpoint_stats = []

    start_time = datetime.now()

    for i, task_file in enumerate(sorted_tasks):
        task_name = os.path.basename(task_file)
        print(f"\n[{i+1}/{len(sorted_tasks)}] {task_name}")

        try:
            # Load task
            with open(task_file, 'r') as f:
                task_data = json.load(f)

            task_id = task_name.replace('.json', '')

            # Convert to numpy
            training_examples = [
                (np.array(pair['input']), np.array(pair['output']))
                for pair in task_data['train']
            ]
            test_input = np.array(task_data['test'][0]['input'])
            test_output = np.array(task_data['test'][0]['output'])

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

            # Checkpoint every N tasks
            if (i + 1) % checkpoint_frequency == 0:
                elapsed = (datetime.now() - start_time).total_seconds()

                # Get current statistics
                tsk_stats = system.tsk_memory.get_statistics()
                family_stats = system.organic_learner.get_transformation_statistics()
                trajectory = system.persistent_state.get_learning_trajectory()

                checkpoint_data = {
                    'task_index': i + 1,
                    'tasks_processed': total,
                    'successful': successful,
                    'near_perfect': near_perfect,
                    'success_rate': successful / max(total, 1),
                    'near_perfect_rate': near_perfect / max(total, 1),
                    'elapsed_seconds': elapsed,
                    'tasks_per_second': total / max(elapsed, 1),
                    'global_confidence': trajectory['global_confidence'],
                    'organic_families': family_stats['organic_families'],
                    'high_conf_patterns': tsk_stats['high_conf_mappings'],
                    'total_patterns': tsk_stats['total_patterns']
                }

                checkpoint_stats.append(checkpoint_data)

                # Save state
                system.persistent_state.save_state()

                print(f"\n{'='*80}")
                print(f"CHECKPOINT {i+1}/{len(sorted_tasks)}")
                print(f"{'='*80}")
                print(f"   Tasks processed: {total}")
                print(f"   Success rate: {successful/total:.1%} ({successful}/{total})")
                print(f"   Near-perfect rate: {near_perfect/total:.1%} ({near_perfect}/{total})")
                print(f"   Global confidence: {trajectory['global_confidence']:.2f}")
                print(f"   Organic families: {family_stats['organic_families']}")
                print(f"   High-quality patterns: {tsk_stats['high_conf_mappings']}")
                print(f"   Elapsed time: {elapsed/60:.1f} minutes")
                print(f"   Speed: {total/max(elapsed, 1)*60:.1f} tasks/minute")
                print(f"   Estimated remaining: {(len(sorted_tasks) - (i+1)) / max(total/max(elapsed, 1), 0.01) / 60:.1f} minutes")
                print(f"{'='*80}\n")

        except Exception as e:
            print(f"   ⚠️ Error: {e}")
            import traceback
            traceback.print_exc()
            total += 1

    # Final summary
    print("\n" + "="*80)
    print("FULL 402-TASK TRAINING SUMMARY (99% THRESHOLD)")
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
        print(f"      Worst: {min(accuracies):.1%}")
        print(f"      Std dev: {np.std(accuracies):.1%}")

    # Near-perfect tasks
    near_perfect_tasks = [r for r in results if r['test_accuracy'] >= 0.99]
    if near_perfect_tasks:
        print(f"\n✨ Near-Perfect Tasks ({len(near_perfect_tasks)}):")
        for r in near_perfect_tasks[:20]:  # Show first 20
            print(f"      {r['task_id']}: {r['test_accuracy']:.1%}")
        if len(near_perfect_tasks) > 20:
            print(f"      ... and {len(near_perfect_tasks) - 20} more")

    # Organic families
    family_stats = system.organic_learner.get_transformation_statistics()
    print(f"\n🌱 Organic Discovery:")
    print(f"   Total transformations: {family_stats['total_discoveries']}")
    print(f"   Organic families: {family_stats['organic_families']}")
    print(f"   Mature families (≥3 samples): {family_stats.get('mature_families', 'N/A')}")

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
    print(f"   Total tasks logged: {tsk_stats['total_tasks']}")

    # Time analysis
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n⏱️ Performance:")
    print(f"   Total time: {elapsed/3600:.2f} hours ({elapsed/60:.1f} minutes)")
    print(f"   Average time per task: {elapsed/max(total, 1):.1f} seconds")
    print(f"   Tasks per minute: {total/max(elapsed, 1)*60:.1f}")

    # Checkpoint progression
    if checkpoint_stats:
        print(f"\n📊 Checkpoint Progression:")
        for i, cp in enumerate(checkpoint_stats):
            print(f"   [{cp['task_index']:3d}] Success: {cp['success_rate']:.1%}, "
                  f"Near-perfect: {cp['near_perfect_rate']:.1%}, "
                  f"Families: {cp['organic_families']}, "
                  f"Confidence: {cp['global_confidence']:.2f}")

    # End session
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


if __name__ == "__main__":
    main()
