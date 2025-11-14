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
import subprocess
import time
from pathlib import Path
from datetime import datetime

print("="*80)
print("🌀 EPOCHS 2-5 BASELINE TRAINING (PRE-GOVERNANCE)")
print("="*80)
print()
print("📋 Purpose: Establish baseline learning trajectory before SELF governance")
print("   - Epoch 1: COMPLETE (baseline_training_results.json)")
print("   - Epochs 2-5: Running now...")
print()

# Load Epoch 1 results
epoch1_path = Path("baseline_training_results.json")
if not epoch1_path.exists():
    print("⚠️  Epoch 1 results not found at baseline_training_results.json")
    print("   Please run run_baseline_training.py first")
    sys.exit(1)

with open(epoch1_path, 'r') as f:
    epoch1_results = json.load(f)
    print(f"✅ Loaded Epoch 1 results:")
    print(f"   Success rate: {epoch1_results['aggregate_metrics']['success_rate']*100:.1f}%")
    print(f"   Mean confidence: {epoch1_results['aggregate_metrics']['mean_confidence']:.3f}")
    print(f"   Mean nexuses: {epoch1_results['aggregate_metrics']['mean_nexus_count']:.2f}")
    print()

all_epoch_results = [{
    "epoch": 1,
    "results": epoch1_results,
    "timestamp": epoch1_results["metadata"]["training_date"]
}]

# Run Epochs 2-5 by calling run_baseline_training.py
for epoch_num in range(2, 6):
    print("="*80)
    print(f"📝 EPOCH {epoch_num}/5")
    print("="*80)
    print()

    # Output path for this epoch
    output_path = f"epoch_{epoch_num}_results.json"

    # Temporarily modify run_baseline_training.py to use different output path
    # Read the script
    with open("run_baseline_training.py", 'r') as f:
        script_content = f.read()

    # Replace OUTPUT_PATH
    modified_script = script_content.replace(
        'OUTPUT_PATH = "baseline_training_results.json"',
        f'OUTPUT_PATH = "{output_path}"'
    )

    # Write to temp file
    temp_script = f"_temp_epoch_{epoch_num}.py"
    with open(temp_script, 'w') as f:
        f.write(modified_script)

    # Run training
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, temp_script],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            env={'PYTHONPATH': str(Path.cwd())}
        )

        elapsed = time.time() - start_time

        # Check if successful
        if result.returncode != 0:
            print(f"❌ Epoch {epoch_num} failed with return code {result.returncode}")
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            sys.exit(1)

        # Load results
        if not Path(output_path).exists():
            print(f"❌ Results file not created: {output_path}")
            sys.exit(1)

        with open(output_path, 'r') as f:
            results = json.load(f)

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

    finally:
        # Clean up temp file
        if Path(temp_script).exists():
            Path(temp_script).unlink()

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
        "phase2_enabled": True,
        "salience_enabled": True
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
