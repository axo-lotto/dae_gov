"""
Continuity Test: R-Matrix Growth (CONT-007)
============================================

Tests that the Hebbian R-matrix (11×11 organ coupling) grows appropriately
during epoch training, demonstrating Z→Y learning (emissions become data).

Theoretical Foundation (Whiteheadian):
- Z (Superject): Completed occasion objectifies for future
- Y (Objectified Past): Previous occasions as data
- Learning: Z becomes Y for next X (R-matrix accumulates prehensions)

Test Protocol:
1. Load R-matrix at epoch 0 (baseline)
2. Load R-matrix at epoch N (after training)
3. Compute growth metrics:
   - Mean coupling strength increase
   - Std coupling diversity
   - Specific organ pair growth
4. Validate growth is:
   - Positive (mean increases)
   - Diverse (std > 0.15, not all same)
   - Bounded (mean < 0.70, saturation term working)

Success Criteria:
- Mean coupling growth: +0.10 per 5 epochs (≥+0.02 per epoch)
- Std coupling: > 0.15 (diversity maintained)
- Mean coupling: < 0.70 (saturation prevents runaway)
- Growth stability: No sudden jumps/drops (±0.05 per epoch)

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Continuity Testing)
"""

import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import Config


@dataclass
class RMatrixSnapshot:
    """Snapshot of R-matrix at a specific epoch."""
    epoch: int
    r_matrix: np.ndarray  # 11×11
    mean_coupling: float
    std_coupling: float
    max_coupling: float
    min_coupling: float
    timestamp: str


@dataclass
class RMatrixGrowthResult:
    """Result of R-matrix growth test."""
    baseline_epoch: int
    final_epoch: int
    epochs_elapsed: int

    # Growth metrics
    mean_growth: float  # Final - baseline mean
    growth_per_epoch: float  # mean_growth / epochs_elapsed
    std_final: float

    # Stability metrics
    growth_trajectory: List[float]  # Mean coupling per epoch
    growth_stable: bool  # No jumps > ±0.05 per epoch

    # Saturation check
    mean_coupling_final: float
    saturation_healthy: bool  # < 0.70

    # Diversity check
    diversity_maintained: bool  # std > 0.15

    # Overall success
    success: bool
    reasoning: str


class RMatrixGrowthTester:
    """
    Tests R-matrix growth stability during epoch training.

    Validates that Hebbian learning:
    - Increases coupling strength (learning occurs)
    - Maintains diversity (not uniform)
    - Prevents saturation (bounded growth)
    - Grows stably (no sudden changes)
    """

    def __init__(
        self,
        r_matrix_path: Path = None,
        results_dir: Path = None
    ):
        """
        Initialize R-matrix growth tester.

        Args:
            r_matrix_path: Path to conversational_hebbian_memory.json
            results_dir: Path to epoch training results
        """
        if r_matrix_path is None:
            r_matrix_path = Path(Config.HEBBIAN_MEMORY_PATH)
        if results_dir is None:
            results_dir = Path("results/epoch_training")

        self.r_matrix_path = r_matrix_path
        self.results_dir = results_dir

    def load_r_matrix_snapshot(
        self,
        epoch: int,
        from_results: bool = True
    ) -> Optional[RMatrixSnapshot]:
        """
        Load R-matrix snapshot from a specific epoch.

        Args:
            epoch: Epoch number (0 = baseline)
            from_results: Load from epoch results vs current file

        Returns:
            RMatrixSnapshot or None if not found
        """
        if epoch == 0 and not from_results:
            # Load current R-matrix as baseline
            return self._load_current_r_matrix()

        # Try to load from epoch results
        epoch_result_path = self.results_dir / f"epoch_{epoch:03d}_result.json"

        if not epoch_result_path.exists():
            print(f"⚠️  Epoch {epoch} results not found at {epoch_result_path}")
            return None

        try:
            with open(epoch_result_path, 'r') as f:
                epoch_data = json.load(f)

            # Check if R-matrix snapshot saved
            if 'r_matrix_snapshot' in epoch_data:
                r_matrix_data = epoch_data['r_matrix_snapshot']
                r_matrix = np.array(r_matrix_data['matrix'])

                return RMatrixSnapshot(
                    epoch=epoch,
                    r_matrix=r_matrix,
                    mean_coupling=r_matrix_data['mean_coupling'],
                    std_coupling=r_matrix_data['std_coupling'],
                    max_coupling=r_matrix_data['max_coupling'],
                    min_coupling=r_matrix_data['min_coupling'],
                    timestamp=epoch_data.get('end_time', '')
                )
            else:
                print(f"⚠️  No R-matrix snapshot in epoch {epoch} results")
                return None

        except Exception as e:
            print(f"⚠️  Error loading epoch {epoch} results: {e}")
            return None

    def _load_current_r_matrix(self) -> Optional[RMatrixSnapshot]:
        """Load current R-matrix from file."""
        if not self.r_matrix_path.exists():
            print(f"⚠️  R-matrix file not found: {self.r_matrix_path}")
            return None

        try:
            with open(self.r_matrix_path, 'r') as f:
                data = json.load(f)

            if 'r_matrix' in data:
                r_matrix = np.array(data['r_matrix'])
            elif 'coupling_matrix' in data:
                r_matrix = np.array(data['coupling_matrix'])
            else:
                print(f"⚠️  No R-matrix found in {self.r_matrix_path}")
                return None

            # Compute statistics
            mean_coupling = float(np.mean(r_matrix))
            std_coupling = float(np.std(r_matrix))
            max_coupling = float(np.max(r_matrix))
            min_coupling = float(np.min(r_matrix))

            return RMatrixSnapshot(
                epoch=0,
                r_matrix=r_matrix,
                mean_coupling=mean_coupling,
                std_coupling=std_coupling,
                max_coupling=max_coupling,
                min_coupling=min_coupling,
                timestamp=data.get('last_updated', '')
            )

        except Exception as e:
            print(f"⚠️  Error loading R-matrix: {e}")
            return None

    def test_r_matrix_growth(
        self,
        baseline_epoch: int = 0,
        final_epoch: int = 5,
        verbose: bool = True
    ) -> RMatrixGrowthResult:
        """
        Test R-matrix growth between two epochs.

        Args:
            baseline_epoch: Starting epoch (usually 0)
            final_epoch: Ending epoch (e.g., 5, 10, 15)
            verbose: Print detailed results

        Returns:
            RMatrixGrowthResult with growth metrics and success status
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"🧬 R-MATRIX GROWTH TEST (CONT-007)")
            print(f"{'='*70}")
            print(f"\nTesting: Z→Y learning (emissions become data)")
            print(f"Epochs: {baseline_epoch} → {final_epoch}")

        # Load baseline
        baseline = self.load_r_matrix_snapshot(baseline_epoch, from_results=(baseline_epoch > 0))
        if baseline is None:
            if verbose:
                print(f"\n❌ FAILED: Could not load baseline (epoch {baseline_epoch})")
            return RMatrixGrowthResult(
                baseline_epoch=baseline_epoch,
                final_epoch=final_epoch,
                epochs_elapsed=0,
                mean_growth=0.0,
                growth_per_epoch=0.0,
                std_final=0.0,
                growth_trajectory=[],
                growth_stable=False,
                mean_coupling_final=0.0,
                saturation_healthy=False,
                diversity_maintained=False,
                success=False,
                reasoning="Could not load baseline R-matrix"
            )

        # Load final
        final = self.load_r_matrix_snapshot(final_epoch, from_results=True)
        if final is None:
            if verbose:
                print(f"\n❌ FAILED: Could not load final (epoch {final_epoch})")
            return RMatrixGrowthResult(
                baseline_epoch=baseline_epoch,
                final_epoch=final_epoch,
                epochs_elapsed=0,
                mean_growth=0.0,
                growth_per_epoch=0.0,
                std_final=0.0,
                growth_trajectory=[],
                growth_stable=False,
                mean_coupling_final=0.0,
                saturation_healthy=False,
                diversity_maintained=False,
                success=False,
                reasoning=f"Could not load final R-matrix (epoch {final_epoch})"
            )

        # Compute growth metrics
        epochs_elapsed = final_epoch - baseline_epoch
        mean_growth = final.mean_coupling - baseline.mean_coupling
        growth_per_epoch = mean_growth / epochs_elapsed if epochs_elapsed > 0 else 0.0

        # Load intermediate epochs for trajectory
        growth_trajectory = [baseline.mean_coupling]
        for epoch in range(baseline_epoch + 1, final_epoch + 1):
            snapshot = self.load_r_matrix_snapshot(epoch, from_results=True)
            if snapshot:
                growth_trajectory.append(snapshot.mean_coupling)

        # Check stability (no jumps > ±0.05 per epoch)
        growth_stable = True
        if len(growth_trajectory) >= 2:
            for i in range(1, len(growth_trajectory)):
                delta = abs(growth_trajectory[i] - growth_trajectory[i-1])
                if delta > 0.05:
                    growth_stable = False
                    break

        # Check saturation (mean < 0.70)
        saturation_healthy = final.mean_coupling < 0.70

        # Check diversity (std > 0.15)
        diversity_maintained = final.std_coupling > 0.15

        # Overall success criteria
        # Target: +0.10 per 5 epochs = +0.02 per epoch
        target_growth_per_epoch = 0.02

        success = (
            growth_per_epoch >= target_growth_per_epoch and
            saturation_healthy and
            diversity_maintained and
            growth_stable
        )

        # Reasoning
        if success:
            reasoning = f"Healthy growth: +{mean_growth:.3f} over {epochs_elapsed} epochs (+{growth_per_epoch:.3f}/epoch)"
        else:
            reasons = []
            if growth_per_epoch < target_growth_per_epoch:
                reasons.append(f"Growth too slow: {growth_per_epoch:.3f} < {target_growth_per_epoch:.3f}/epoch")
            if not saturation_healthy:
                reasons.append(f"Saturation risk: mean={final.mean_coupling:.3f} >= 0.70")
            if not diversity_maintained:
                reasons.append(f"Diversity lost: std={final.std_coupling:.3f} <= 0.15")
            if not growth_stable:
                reasons.append("Unstable growth: jumps > ±0.05 per epoch")
            reasoning = "; ".join(reasons)

        result = RMatrixGrowthResult(
            baseline_epoch=baseline_epoch,
            final_epoch=final_epoch,
            epochs_elapsed=epochs_elapsed,
            mean_growth=mean_growth,
            growth_per_epoch=growth_per_epoch,
            std_final=final.std_coupling,
            growth_trajectory=growth_trajectory,
            growth_stable=growth_stable,
            mean_coupling_final=final.mean_coupling,
            saturation_healthy=saturation_healthy,
            diversity_maintained=diversity_maintained,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result, baseline, final)

        return result

    def _print_results(
        self,
        result: RMatrixGrowthResult,
        baseline: RMatrixSnapshot,
        final: RMatrixSnapshot
    ):
        """Print detailed test results."""
        print(f"\n📊 Growth Metrics:")
        print(f"   Baseline (epoch {baseline.epoch}):")
        print(f"      Mean coupling: {baseline.mean_coupling:.3f}")
        print(f"      Std coupling: {baseline.std_coupling:.3f}")

        print(f"\n   Final (epoch {final.epoch}):")
        print(f"      Mean coupling: {final.mean_coupling:.3f}")
        print(f"      Std coupling: {final.std_coupling:.3f}")

        print(f"\n   Growth:")
        print(f"      Total: {result.mean_growth:+.3f} over {result.epochs_elapsed} epochs")
        print(f"      Per epoch: {result.growth_per_epoch:+.4f}")
        print(f"      Target: ≥0.0200/epoch")
        print(f"      Status: {'✅' if result.growth_per_epoch >= 0.02 else '❌'}")

        print(f"\n📈 Stability Checks:")
        print(f"   Growth stable: {'✅' if result.growth_stable else '❌'} (no jumps > ±0.05)")
        print(f"   Saturation healthy: {'✅' if result.saturation_healthy else '❌'} (mean < 0.70)")
        print(f"   Diversity maintained: {'✅' if result.diversity_maintained else '❌'} (std > 0.15)")

        if len(result.growth_trajectory) > 2:
            print(f"\n🌀 Growth Trajectory:")
            for i, coupling in enumerate(result.growth_trajectory):
                epoch_num = result.baseline_epoch + i
                marker = "📍" if i == 0 else ("🎯" if i == len(result.growth_trajectory) - 1 else "  ")
                print(f"   {marker} Epoch {epoch_num:2d}: {coupling:.3f}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: R-matrix growth healthy")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_r_matrix_growth_test(
    baseline_epoch: int = 0,
    final_epoch: int = 5
) -> bool:
    """
    Run R-matrix growth test.

    Args:
        baseline_epoch: Starting epoch
        final_epoch: Ending epoch

    Returns:
        True if test passed
    """
    tester = RMatrixGrowthTester()
    result = tester.test_r_matrix_growth(
        baseline_epoch=baseline_epoch,
        final_epoch=final_epoch,
        verbose=True
    )

    return result.success


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test R-matrix growth stability")
    parser.add_argument('--baseline', type=int, default=0, help='Baseline epoch')
    parser.add_argument('--final', type=int, default=5, help='Final epoch')

    args = parser.parse_args()

    success = run_r_matrix_growth_test(
        baseline_epoch=args.baseline,
        final_epoch=args.final
    )

    sys.exit(0 if success else 1)
