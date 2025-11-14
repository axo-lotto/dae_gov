"""
Monitor Training Progress and R-Matrix Health
November 13, 2025

Monitors:
- Baseline training progress (from log file)
- R-matrix evolution (mean, std, off-diag std)
- System health metrics
"""

import json
import numpy as np
from pathlib import Path
import time

def check_r_matrix_health():
    """Check current R-matrix health metrics."""
    r_matrix_path = Path("persona_layer/conversational_hebbian_memory.json")

    if not r_matrix_path.exists():
        print("⚠️  R-matrix file not found")
        return None

    with open(r_matrix_path) as f:
        data = json.load(f)

    R = np.array(data['r_matrix'])
    metadata = data.get('r_matrix_metadata', {})

    mean_val = np.mean(R)
    std_val = np.std(R)
    off_diag = R[~np.eye(R.shape[0], dtype=bool)]
    off_diag_mean = np.mean(off_diag)
    off_diag_std = np.std(off_diag)

    total_updates = metadata.get('total_updates', 0)
    learning_rate = metadata.get('learning_rate', 0.0)

    print("\n📊 R-Matrix Health Check")
    print("="*60)
    print(f"   Total updates: {total_updates}")
    print(f"   Learning rate: {learning_rate}")
    print(f"   Mean: {mean_val:.6f} (target: 0.5-0.85)")
    print(f"   Std Dev: {std_val:.6f} (target: >0.08)")
    print(f"   Off-diagonal Mean: {off_diag_mean:.6f}")
    print(f"   Off-diagonal Std Dev: {off_diag_std:.6f} (target: >0.06)")

    # Health checks
    health_ok = True

    if mean_val > 0.85:
        print(f"   ⚠️  WARNING: Mean {mean_val:.3f} approaching saturation (>0.85)")
        health_ok = False
    elif mean_val < 0.5:
        print(f"   ⚠️  WARNING: Mean {mean_val:.3f} below target (<0.5)")
        health_ok = False
    else:
        print(f"   ✅ Mean within target range")

    if std_val < 0.08:
        print(f"   ⚠️  WARNING: Std {std_val:.3f} too low (losing discrimination)")
        health_ok = False
    else:
        print(f"   ✅ Std Dev good (discrimination maintained)")

    if off_diag_std < 0.06:
        print(f"   ⚠️  WARNING: Off-diag std {off_diag_std:.3f} too low")
        health_ok = False
    else:
        print(f"   ✅ Off-diagonal variance good")

    if health_ok:
        print(f"\n   🟢 R-MATRIX HEALTHY")
    else:
        print(f"\n   🟡 R-MATRIX NEEDS ATTENTION")

    return {
        'mean': mean_val,
        'std': std_val,
        'off_diag_mean': off_diag_mean,
        'off_diag_std': off_diag_std,
        'total_updates': total_updates,
        'learning_rate': learning_rate,
        'healthy': health_ok
    }

def check_training_log():
    """Check baseline training log for progress."""
    log_path = Path("/tmp/baseline_training.log")

    if not log_path.exists():
        print("\n⚠️  Training log not found (training may not have started)")
        return None

    with open(log_path) as f:
        lines = f.readlines()

    # Count completed pairs
    completed_pairs = 0
    for line in lines:
        if "Training Pair" in line and "/" in line:
            try:
                parts = line.split("Training Pair")[1].split("/")
                completed_pairs = int(parts[0].strip())
            except:
                pass

    total_pairs = 30
    progress_pct = (completed_pairs / total_pairs) * 100 if total_pairs > 0 else 0

    print("\n📈 Training Progress")
    print("="*60)
    print(f"   Completed: {completed_pairs}/{total_pairs} pairs ({progress_pct:.1f}%)")

    # Check for errors
    error_count = sum(1 for line in lines if "❌ Error" in line)
    if error_count > 0:
        print(f"   ⚠️  Errors encountered: {error_count}")
    else:
        print(f"   ✅ No errors detected")

    # Check if complete
    if "BASELINE TRAINING COMPLETE" in ''.join(lines):
        print(f"   🎉 TRAINING COMPLETE!")
        return {'completed': True, 'pairs': completed_pairs, 'errors': error_count}
    elif completed_pairs == total_pairs:
        print(f"   ⏳ Training complete, finalizing results...")
        return {'completed': True, 'pairs': completed_pairs, 'errors': error_count}
    else:
        print(f"   ⏳ Training in progress...")
        return {'completed': False, 'pairs': completed_pairs, 'errors': error_count}

def check_results_file():
    """Check if baseline results file exists."""
    results_path = Path("baseline_training_results.json")

    if not results_path.exists():
        print("\n⏳ Results file not yet generated")
        return None

    with open(results_path) as f:
        data = json.load(f)

    results = data.get('results', [])
    summary = data.get('summary', {})

    print("\n📊 Training Results Summary")
    print("="*60)
    print(f"   Total pairs processed: {len(results)}")
    print(f"   Success rate: {summary.get('success_rate', 0):.1%}")
    print(f"   Mean confidence: {summary.get('mean_confidence', 0):.3f}")
    print(f"   Mean nexus count: {summary.get('mean_nexus_count', 0):.1f}")
    print(f"   Mean cycles: {summary.get('mean_cycles', 0):.1f}")
    print(f"   Mean V0 descent: {summary.get('mean_v0_descent', 0):.3f}")

    return summary

def main():
    """Main monitoring function."""
    print("\n" + "="*60)
    print("🔍 TRAINING PROGRESS & R-MATRIX HEALTH MONITOR")
    print("="*60)

    # Check training progress
    training_status = check_training_log()

    # Check R-matrix health
    r_matrix_health = check_r_matrix_health()

    # Check results if available
    if training_status and training_status.get('completed'):
        results_summary = check_results_file()

    print("\n" + "="*60)
    print("✅ MONITORING COMPLETE")
    print("="*60)

    # Summary
    if training_status:
        if training_status.get('completed'):
            print("\n🎉 Training complete! Check baseline_training_results.json for full results.")
        else:
            pairs_done = training_status.get('pairs', 0)
            print(f"\n⏳ Training in progress: {pairs_done}/30 pairs complete")
            print("   Run this script again to check progress.")

    if r_matrix_health:
        if r_matrix_health['healthy']:
            print(f"🟢 R-matrix healthy (mean={r_matrix_health['mean']:.3f}, std={r_matrix_health['std']:.3f})")
        else:
            print(f"🟡 R-matrix needs attention (check metrics above)")

    print()

if __name__ == "__main__":
    main()
