"""
Fix R-Matrix Saturation Issue
November 13, 2025

Critical Issue: R-matrix saturated at ~1.0 (mean=0.988, std=0.027)
Impact: Breaks discrimination, affects nexus weighting
Fix: Reset with lower learning rate and better initialization
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
import shutil

def backup_current_r_matrix():
    """Create backup of current saturated R-matrix."""
    r_matrix_path = Path("persona_layer/conversational_hebbian_memory.json")
    backup_path = Path(f"persona_layer/conversational_hebbian_memory_backup_saturated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    shutil.copy(r_matrix_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return backup_path

def analyze_current_saturation():
    """Analyze current R-matrix saturation."""
    r_matrix_path = Path("persona_layer/conversational_hebbian_memory.json")

    with open(r_matrix_path, 'r') as f:
        data = json.load(f)

    r_matrix = np.array(data['r_matrix'])

    # Compute statistics
    mean_val = np.mean(r_matrix)
    std_val = np.std(r_matrix)
    min_val = np.min(r_matrix)
    max_val = np.max(r_matrix)

    # Off-diagonal statistics (excluding diagonal = 1.0)
    off_diag = r_matrix[~np.eye(r_matrix.shape[0], dtype=bool)]
    off_diag_mean = np.mean(off_diag)
    off_diag_std = np.std(off_diag)

    print("\n📊 Current R-Matrix Analysis:")
    print(f"   Shape: {r_matrix.shape}")
    print(f"   Mean: {mean_val:.6f} (saturated, should be ~0.5-0.7)")
    print(f"   Std Dev: {std_val:.6f} (no discrimination, should be >0.1)")
    print(f"   Min: {min_val:.6f}")
    print(f"   Max: {max_val:.6f}")
    print(f"\n   Off-diagonal Mean: {off_diag_mean:.6f}")
    print(f"   Off-diagonal Std Dev: {off_diag_std:.6f}")
    print(f"\n   ⚠️  SATURATED: All couplings ~1.0, no discrimination")

    return r_matrix, data

def create_discriminative_r_matrix(size=11, approach='soft_reset'):
    """
    Create new R-matrix with good discrimination.

    Args:
        size: Matrix size (11 for 11 organs)
        approach: 'soft_reset' (preserve 30% of learned structure) or 'hard_reset' (start fresh)

    Returns:
        New R-matrix with restored discrimination
    """
    if approach == 'hard_reset':
        # Hard reset: Identity + structured noise
        print("\n🔄 Using HARD RESET approach (fresh start)...")

        # Base: Identity matrix (diagonal = 1.0, rest = 0.0)
        R_new = np.eye(size)

        # Add structured noise for initial couplings
        # Use organ semantics for initialization:
        # - Conversational organs (0-4): Higher coupling
        # - Trauma organs (5-10): Moderate coupling
        # - Cross-category: Lower coupling

        for i in range(size):
            for j in range(size):
                if i != j:
                    # Conversational-conversational (0-4)
                    if i < 5 and j < 5:
                        R_new[i,j] = 0.65 + np.random.randn() * 0.10
                    # Trauma-trauma (5-10)
                    elif i >= 5 and j >= 5:
                        R_new[i,j] = 0.60 + np.random.randn() * 0.10
                    # Cross-category
                    else:
                        R_new[i,j] = 0.50 + np.random.randn() * 0.12

                    # Clamp to reasonable range
                    R_new[i,j] = np.clip(R_new[i,j], 0.3, 0.85)

        # Make symmetric
        R_new = (R_new + R_new.T) / 2

        # Ensure diagonal = 1.0
        np.fill_diagonal(R_new, 1.0)

    else:  # soft_reset
        # Soft reset: Preserve some learned structure
        print("\n🔄 Using SOFT RESET approach (preserve 30% of learned structure)...")

        # Load current saturated matrix
        r_matrix_path = Path("persona_layer/conversational_hebbian_memory.json")
        with open(r_matrix_path, 'r') as f:
            data = json.load(f)
        R_old = np.array(data['r_matrix'])

        # Blend: 30% old structure + 70% discriminative base
        R_base = np.eye(size) * 0.6 + np.random.randn(size, size) * 0.15
        R_base = (R_base + R_base.T) / 2  # Symmetric
        R_base = np.clip(R_base, 0.3, 0.85)
        np.fill_diagonal(R_base, 1.0)

        R_new = 0.3 * R_old + 0.7 * R_base

        # Ensure diagonal = 1.0
        np.fill_diagonal(R_new, 1.0)

        # Clip to reasonable range
        R_new = np.clip(R_new, 0.0, 1.0)

    return R_new

def validate_discrimination(R_matrix):
    """Validate that new R-matrix has good discrimination."""
    mean_val = np.mean(R_matrix)
    std_val = np.std(R_matrix)

    # Off-diagonal statistics
    off_diag = R_matrix[~np.eye(R_matrix.shape[0], dtype=bool)]
    off_diag_mean = np.mean(off_diag)
    off_diag_std = np.std(off_diag)

    print("\n✅ New R-Matrix Validation:")
    print(f"   Mean: {mean_val:.6f} (target: 0.5-0.7)")
    print(f"   Std Dev: {std_val:.6f} (target: >0.1)")
    print(f"   Off-diagonal Mean: {off_diag_mean:.6f}")
    print(f"   Off-diagonal Std Dev: {off_diag_std:.6f}")

    # Check criteria
    good_mean = 0.5 <= mean_val <= 0.7
    good_std = std_val > 0.1
    good_off_diag_std = off_diag_std > 0.08

    if good_mean and good_std and good_off_diag_std:
        print(f"\n   ✅ DISCRIMINATION RESTORED: Matrix has good variance")
        return True
    else:
        print(f"\n   ⚠️  WARNING: Discrimination may still be weak")
        if not good_mean:
            print(f"      - Mean {mean_val:.3f} outside target range [0.5, 0.7]")
        if not good_std:
            print(f"      - Std dev {std_val:.3f} too low (need >0.1)")
        if not good_off_diag_std:
            print(f"      - Off-diagonal std dev {off_diag_std:.3f} too low (need >0.08)")
        return False

def save_new_r_matrix(R_new, old_data, approach):
    """Save new R-matrix to file."""
    r_matrix_path = Path("persona_layer/conversational_hebbian_memory.json")

    # Update data
    new_data = {
        "r_matrix": R_new.tolist(),
        "last_updated": datetime.now().isoformat(),
        "reset_reason": f"Fixed saturation issue ({approach} approach) - Nov 13, 2025",
        "previous_state": f"saturated (mean={old_data['r_matrix_metadata'].get('mean', 0.988):.3f})",
        "r_matrix_metadata": {
            "shape": list(R_new.shape),
            "learning_rate": 0.005,  # 🆕 Much lower learning rate (was 0.05)
            "total_updates": 0,  # Reset counter
            "mean": float(np.mean(R_new)),
            "std": float(np.std(R_new)),
            "approach": approach
        }
    }

    with open(r_matrix_path, 'w') as f:
        json.dump(new_data, f, indent=2)

    print(f"\n✅ New R-matrix saved: {r_matrix_path}")
    print(f"   New learning rate: 0.005 (was 0.05 - 10× slower)")
    print(f"   Update counter reset to: 0")

def main():
    print("="*70)
    print("🔧 R-Matrix Saturation Fix")
    print("="*70)

    # Step 1: Analyze current saturation
    print("\n📋 STEP 1: Analyzing current R-matrix...")
    R_old, old_data = analyze_current_saturation()

    # Step 2: Backup
    print("\n📋 STEP 2: Creating backup...")
    backup_path = backup_current_r_matrix()

    # Step 3: Choose approach
    print("\n📋 STEP 3: Selecting reset approach...")
    print("\n   Two options:")
    print("   1. SOFT RESET: Preserve 30% of learned structure")
    print("   2. HARD RESET: Fresh start with structured initialization")
    print("\n   Recommendation: SOFT RESET (safer, preserves some learning)")

    approach = 'hard_reset'  # Use hard reset for better discrimination
    print(f"\n   Selected: {approach.upper()}")

    # Step 4: Create new R-matrix
    print("\n📋 STEP 4: Creating new discriminative R-matrix...")
    R_new = create_discriminative_r_matrix(size=11, approach=approach)

    # Step 5: Validate discrimination
    print("\n📋 STEP 5: Validating discrimination...")
    discrimination_ok = validate_discrimination(R_new)

    if not discrimination_ok:
        print("\n⚠️  WARNING: Discrimination not ideal. Consider HARD RESET approach.")
        print("   To use hard reset, edit this script and set approach='hard_reset'")

    # Step 6: Save new R-matrix
    print("\n📋 STEP 6: Saving new R-matrix...")
    save_new_r_matrix(R_new, old_data, approach)

    # Step 7: Summary
    print("\n" + "="*70)
    print("✅ R-MATRIX SATURATION FIX COMPLETE")
    print("="*70)
    print(f"\n📊 Results:")
    print(f"   Backup created: {backup_path.name}")
    print(f"   Approach: {approach.upper()}")
    print(f"   New mean: {np.mean(R_new):.3f} (was 0.988)")
    print(f"   New std dev: {np.std(R_new):.3f} (was 0.027)")
    print(f"   Learning rate: 0.005 (was 0.05 - 10× slower)")

    print(f"\n🔄 Next Steps:")
    print(f"   1. Run quick validation: python3 dae_orchestrator.py validate --quick")
    print(f"   2. Run baseline training to test discrimination")
    print(f"   3. Monitor R-matrix evolution (should stay <0.85 mean)")

    print(f"\n⚠️  If discrimination degrades again:")
    print(f"   - Restore backup: mv {backup_path.name} conversational_hebbian_memory.json")
    print(f"   - Try HARD RESET approach instead")

    return discrimination_ok

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
