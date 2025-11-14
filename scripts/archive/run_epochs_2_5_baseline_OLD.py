#!/usr/bin/env python3
"""
Run Epochs 2-5 to Establish Pre-Governance Baseline
====================================================

Purpose: Run 4 additional training epochs (2-5) to establish baseline
learning trajectory BEFORE implementing SELF matrix governance layer.

This allows us to:
1. Establish pre-governance baseline performance
2. Measure learning trajectory without governance
3. Compare post-governance improvements quantitatively
4. Validate organic family formation patterns

Date: November 12, 2025
Status: Baseline establishment for governance comparison
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from run_baseline_training import run_baseline_training


def run_epochs_2_5():
    """Run Epochs 2-5 sequentially."""

    print("="*80)
    print("🌀 EPOCHS 2-5 BASELINE TRAINING (PRE-GOVERNANCE)")
    print("="*80)
    print()
    print("📋 Purpose: Establish baseline learning trajectory before SELF governance")
    print("   - Epoch 1: COMPLETE (baseline_training_results.json)")
    print("   - Epochs 2-5: Running now...")
    print()

    # Configuration
    training_pairs_path = "knowledge_base/conversational_training_pairs.json"
    num_pairs = 30
    enable_phase2 = True
    enable_salience = True

    # Store results for all epochs
    all_epoch_results = []

    # Load Epoch 1 results
    epoch1_path = Path("baseline_training_results.json")
    if epoch1_path.exists():
        with open(epoch1_path, 'r') as f:
            epoch1_results = json.load(f)
            all_epoch_results.append({
                "epoch": 1,
                "results": epoch1_results,
                "timestamp": epoch1_results["metadata"]["training_date"]
            })
            print(f"✅ Loaded Epoch 1 results:")
            print(f"   Success rate: {epoch1_results['aggregate_metrics']['success_rate']*100:.1f}%")
            print(f"   Mean confidence: {epoch1_results['aggregate_metrics']['mean_confidence']:.3f}")
            print(f"   Mean nexuses: {epoch1_results['aggregate_metrics']['mean_nexus_count']:.2f}")
            print()
    else:
        print("⚠️  Epoch 1 results not found at baseline_training_results.json")
        print("   Please run run_baseline_training.py first")
        return

    # Run Epochs 2-5
    for epoch_num in range(2, 6):
        print("="*80)
        print(f"📝 EPOCH {epoch_num}/5")
        print("="*80)
        print()

        # Output path for this epoch
        output_path = f"epoch_{epoch_num}_results.json"

        # Run training
        start_time = time.time()
        results = run_baseline_training(
            training_pairs_path=training_pairs_path,
            num_pairs=num_pairs,
            output_path=output_path,
            enable_phase2=enable_phase2,
            enable_salience=enable_salience
        )
        elapsed = time.time() - start_time

        # Store results
        all_epoch_results.append({
            "epoch": epoch_num,
            "results": results,
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": elapsed
        })

        # Print summary
        print()
        print(f"✅ Epoch {epoch_num} complete ({elapsed:.1f}s)")
        print(f"   Success rate: {results['aggregate_metrics']['success_rate']*100:.1f}%")
        print(f"   Mean confidence: {results['aggregate_metrics']['mean_confidence']:.3f}")
        print(f"   Mean nexuses: {results['aggregate_metrics']['mean_nexus_count']:.2f}")
        print(f"   Results saved: {output_path}")
        print()

        # Brief pause between epochs
        if epoch_num < 5:
            time.sleep(2)

    # Save consolidated results
    consolidated_path = "epochs_1_5_baseline_consolidated.json"
    consolidated = {
        "metadata": {
            "training_date": datetime.now().isoformat(),
            "num_epochs": 5,
            "purpose": "Pre-governance baseline establishment",
            "phase2_enabled": enable_phase2,
            "salience_enabled": enable_salience
        },
        "epochs": all_epoch_results
    }

    with open(consolidated_path, 'w') as f:
        json.dump(consolidated, f, indent=2)

    print("="*80)
    print("🎉 EPOCHS 1-5 BASELINE TRAINING COMPLETE")
    print("="*80)
    print()
    print(f"📊 Consolidated results saved: {consolidated_path}")
    print()

    # Print trajectory summary
    print("📈 LEARNING TRAJECTORY (Epochs 1-5):")
    print()
    print("Epoch | Success | Confidence | Nexuses | Cycles | V0 Final | Trauma Detect")
    print("------|---------|------------|---------|--------|----------|---------------")

    for epoch_data in all_epoch_results:
        epoch = epoch_data["epoch"]
        metrics = epoch_data["results"]["aggregate_metrics"]
        print(f"  {epoch}   | {metrics['success_rate']*100:5.1f}%  | "
              f"{metrics['mean_confidence']:10.3f} | "
              f"{metrics['mean_nexus_count']:7.2f} | "
              f"{metrics['mean_cycles']:6.2f} | "
              f"{metrics['mean_v0_final']:8.3f} | "
              f"{metrics.get('mean_trauma_detection', 0.0):13.3f}")

    print()
    print("📋 Next Steps:")
    print("   1. Analyze learning trajectory across epochs")
    print("   2. Identify patterns in organic family formation")
    print("   3. Establish baseline performance metrics")
    print("   4. Implement SELF matrix governance layer")
    print("   5. Run Epochs 6-10 with governance for comparison")
    print()
    print("🌀 Baseline established - ready for governance integration!")
    print()


if __name__ == '__main__':
    try:
        run_epochs_2_5()
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during epochs 2-5 training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
