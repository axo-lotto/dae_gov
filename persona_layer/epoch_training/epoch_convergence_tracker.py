"""
Epoch Convergence Tracker - Stability-Based HALT Logic
=======================================================

Implements multi-iteration convergence detection adapted from FFITTSS V0 Tier 6,
integrated with DAE 3.0 wave training and stable memory identity formation.

## FFITTSS V0 Multi-Iteration Convergence:
From FFITTSS README_TIERS.md:
- Average iterations per task: 2.75 (range 2-5)
- HALT logic: Stop when stability window shows no improvement
- Stability window: Last 5 iterations
- Convergence criteria: Variance < threshold for N consecutive iterations

## DAE Integration - Stable Memory Identity:
This is about the organism learning when it's reached a **stable memory identity**
for a particular conversational pattern. The system needs to know:
1. "I've converged on this pattern" (satisfaction stable)
2. "My understanding is coherent" (field coherence stable)
3. "I've stopped exploring variations" (spatial variance low + stable)
4. "I can reliably reproduce this response" (emission confidence stable)

**The Bet**: Multi-iteration training creates stable memory traces in:
- Hebbian R-matrix (organ coupling patterns)
- Organic families (conversation clustering)
- V0 targets (per-family energy descent goals)
- Transduction pathways (mechanism preferences)

**When to HALT**:
- Satisfaction reached target AND stable (last N iterations similar)
- Field coherence high AND stable (organs balanced consistently)
- Spatial variance low AND stable (not exploring new regions)
- OR Max iterations reached (safety limit)

## Mathematical Formulation:

Given iteration history for single training pair:
- satisfaction_history = [s₁, s₂, ..., sₙ]
- coherence_history = [c₁, c₂, ..., cₙ]
- variance_history = [v₁, v₂, ..., vₙ]

Stability window (last K iterations):
- window = history[-K:]
- window_variance = var(window)
- window_mean = mean(window)

Convergence decision:
    IF window_variance < threshold AND window_mean >= target:
        → HALT (converged)
    ELIF n >= max_iterations:
        → HALT (max reached)
    ELSE:
        → CONTINUE (need more iterations)

## Usage Example:

```python
from epoch_convergence_tracker import EpochConvergenceTracker, ConvergenceDecision

# Initialize tracker
tracker = EpochConvergenceTracker(
    stability_window=5,
    satisfaction_target=0.75,
    max_iterations=5
)

# Train single pair multiple times
for iteration in range(1, 10):
    # Process conversation
    result = organism.process_text(input_text)

    # Record iteration
    tracker.record_iteration(
        satisfaction=result['satisfaction'],
        field_coherence=result['coherence'],
        spatial_variance=result['spatial_variance'],
        emission_confidence=result['emission_confidence']
    )

    # Check convergence
    decision = tracker.evaluate_convergence()

    if decision == ConvergenceDecision.HALT:
        print(f"Converged at iteration {iteration}")
        break
    elif decision == ConvergenceDecision.MAX_ITERATIONS:
        print(f"Max iterations reached")
        break
```

Author: DAE_HYPHAE_1 Persona Layer
Date: November 13, 2025
"""

from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import numpy as np

# Import regime types for context
try:
    from .satisfaction_regime import SatisfactionRegime, RegimeClassification
except ImportError:
    from satisfaction_regime import SatisfactionRegime, RegimeClassification


class ConvergenceDecision(Enum):
    """Decision about whether to HALT or CONTINUE training."""
    CONTINUE = "CONTINUE"              # Keep training (not converged yet)
    HALT = "HALT"                      # Stop training (converged)
    MAX_ITERATIONS = "MAX_ITERATIONS"  # Stop training (max reached)


@dataclass
class IterationRecord:
    """Record of a single training iteration."""
    iteration: int
    satisfaction: float
    field_coherence: float
    spatial_variance: float
    emission_confidence: float
    v0_final: float
    convergence_cycles: int
    regime: Optional[SatisfactionRegime] = None
    tau: Optional[float] = None


@dataclass
class ConvergenceResult:
    """Result of convergence evaluation."""
    decision: ConvergenceDecision
    iteration_count: int
    converged_at: Optional[int]  # Which iteration converged (if HALT)
    reasoning: str

    # Stability metrics
    satisfaction_stable: bool
    coherence_stable: bool
    variance_stable: bool

    # Window statistics
    window_satisfaction_mean: float
    window_satisfaction_variance: float
    window_coherence_mean: float
    window_variance_mean: float

    # Final metrics
    final_satisfaction: float
    final_coherence: float
    final_variance: float
    final_confidence: float


class ConvergenceConfig:
    """Configuration for convergence tracking."""

    # Stability window
    STABILITY_WINDOW_SIZE = 5  # Last N iterations to check for stability
    MIN_ITERATIONS_FOR_STABILITY = 3  # Minimum iterations before checking stability

    # Convergence thresholds
    SATISFACTION_TARGET = 0.75  # Target satisfaction
    SATISFACTION_VARIANCE_THRESHOLD = 0.01  # Max variance in stability window

    COHERENCE_TARGET = 0.70  # Target field coherence
    COHERENCE_VARIANCE_THRESHOLD = 0.015  # Max coherence variance

    VARIANCE_STABLE_THRESHOLD = 0.0005  # Max spatial variance variance (yes, variance of variance)
    VARIANCE_LOW_THRESHOLD = 0.005  # Spatial variance should be below this

    # Safety limits
    MAX_ITERATIONS = 5  # FFITTSS had 2.75 avg, we allow up to 5
    MIN_ITERATIONS = 2  # Always do at least 2 iterations

    # Regime considerations
    HALT_REGIMES = [SatisfactionRegime.STABLE, SatisfactionRegime.COMMITTED]  # Can halt in these regimes
    CONTINUE_REGIMES = [SatisfactionRegime.INITIALIZING, SatisfactionRegime.EXPLORING]  # Force continue


class EpochConvergenceTracker:
    """
    Tracks multi-iteration training for a single conversation pair.

    Determines when the organism has formed a stable memory identity
    for this conversational pattern and can halt training.
    """

    def __init__(
        self,
        pair_id: str,
        stability_window: int = ConvergenceConfig.STABILITY_WINDOW_SIZE,
        satisfaction_target: float = ConvergenceConfig.SATISFACTION_TARGET,
        max_iterations: int = ConvergenceConfig.MAX_ITERATIONS,
        config: Optional[ConvergenceConfig] = None
    ):
        """
        Initialize convergence tracker for a training pair.

        Args:
            pair_id: Identifier for this training pair
            stability_window: Number of iterations to check for stability
            satisfaction_target: Target satisfaction for convergence
            max_iterations: Maximum iterations before forced halt
            config: Optional custom configuration
        """
        self.pair_id = pair_id
        self.stability_window = stability_window
        self.satisfaction_target = satisfaction_target
        self.max_iterations = max_iterations
        self.config = config or ConvergenceConfig()

        # Iteration history
        self.iterations: List[IterationRecord] = []

        # Convergence state
        self.converged = False
        self.converged_at: Optional[int] = None
        self.convergence_result: Optional[ConvergenceResult] = None

    def record_iteration(
        self,
        satisfaction: float,
        field_coherence: float,
        spatial_variance: float,
        emission_confidence: float,
        v0_final: float,
        convergence_cycles: int,
        regime: Optional[SatisfactionRegime] = None,
        tau: Optional[float] = None
    ) -> IterationRecord:
        """
        Record a single training iteration.

        Args:
            satisfaction: Final satisfaction for this iteration
            field_coherence: Organ balance coherence
            spatial_variance: Spatial satisfaction variance (IQR)
            emission_confidence: Emission generation confidence
            v0_final: Final V0 energy
            convergence_cycles: Number of V0 cycles
            regime: Optional satisfaction regime classification
            tau: Optional current tau threshold

        Returns:
            IterationRecord for this iteration
        """
        iteration_num = len(self.iterations) + 1

        record = IterationRecord(
            iteration=iteration_num,
            satisfaction=satisfaction,
            field_coherence=field_coherence,
            spatial_variance=spatial_variance,
            emission_confidence=emission_confidence,
            v0_final=v0_final,
            convergence_cycles=convergence_cycles,
            regime=regime,
            tau=tau
        )

        self.iterations.append(record)
        return record

    def evaluate_convergence(self) -> ConvergenceResult:
        """
        Evaluate whether training should HALT or CONTINUE.

        Checks:
        1. Max iterations reached → HALT
        2. Minimum iterations not met → CONTINUE
        3. Stability window analysis → HALT if stable, CONTINUE otherwise

        Returns:
            ConvergenceResult with decision and detailed metrics
        """
        iteration_count = len(self.iterations)

        # Safety: Must have at least MIN_ITERATIONS
        if iteration_count < self.config.MIN_ITERATIONS:
            return self._create_result(
                decision=ConvergenceDecision.CONTINUE,
                reasoning=f"Minimum iterations not met ({iteration_count}/{self.config.MIN_ITERATIONS})"
            )

        # Safety: Max iterations reached
        if iteration_count >= self.max_iterations:
            self.converged = True
            self.converged_at = iteration_count
            return self._create_result(
                decision=ConvergenceDecision.MAX_ITERATIONS,
                reasoning=f"Maximum iterations reached ({self.max_iterations})"
            )

        # Need enough iterations for stability window
        if iteration_count < self.config.MIN_ITERATIONS_FOR_STABILITY:
            return self._create_result(
                decision=ConvergenceDecision.CONTINUE,
                reasoning=f"Not enough iterations for stability check ({iteration_count}/{self.config.MIN_ITERATIONS_FOR_STABILITY})"
            )

        # Get stability window (last N iterations)
        window_size = min(self.stability_window, iteration_count)
        window = self.iterations[-window_size:]

        # Extract metrics from window
        window_satisfactions = [r.satisfaction for r in window]
        window_coherences = [r.field_coherence for r in window]
        window_variances = [r.spatial_variance for r in window]

        # Compute window statistics
        sat_mean = float(np.mean(window_satisfactions))
        sat_variance = float(np.var(window_satisfactions))

        coh_mean = float(np.mean(window_coherences))
        coh_variance = float(np.var(window_coherences))

        var_mean = float(np.mean(window_variances))
        var_variance = float(np.var(window_variances))  # Variance of spatial variance

        # Check stability criteria
        satisfaction_stable = (
            sat_variance < self.config.SATISFACTION_VARIANCE_THRESHOLD and
            sat_mean >= self.satisfaction_target
        )

        coherence_stable = (
            coh_variance < self.config.COHERENCE_VARIANCE_THRESHOLD and
            coh_mean >= self.config.COHERENCE_TARGET
        )

        # Spatial variance should be LOW and STABLE (not changing much)
        variance_stable = (
            var_mean < self.config.VARIANCE_LOW_THRESHOLD and
            var_variance < self.config.VARIANCE_STABLE_THRESHOLD
        )

        # Check regime (if available)
        latest_regime = window[-1].regime if window[-1].regime else None
        regime_allows_halt = (
            latest_regime is None or
            latest_regime in self.config.HALT_REGIMES
        )
        regime_forces_continue = (
            latest_regime is not None and
            latest_regime in self.config.CONTINUE_REGIMES
        )

        # Convergence decision logic
        reasoning_parts = []

        if regime_forces_continue:
            reasoning_parts.append(f"Regime {latest_regime.value} requires more exploration")
            decision = ConvergenceDecision.CONTINUE

        elif satisfaction_stable and coherence_stable and variance_stable:
            # All three metrics stable → CONVERGED
            reasoning_parts.append(f"Satisfaction stable ({sat_mean:.3f}±{np.sqrt(sat_variance):.3f})")
            reasoning_parts.append(f"Coherence stable ({coh_mean:.3f}±{np.sqrt(coh_variance):.3f})")
            reasoning_parts.append(f"Spatial variance stable ({var_mean:.4f}±{np.sqrt(var_variance):.4f})")

            if latest_regime:
                reasoning_parts.append(f"Regime: {latest_regime.value}")

            self.converged = True
            self.converged_at = iteration_count
            decision = ConvergenceDecision.HALT

        elif satisfaction_stable and coherence_stable:
            # 2/3 stable, but spatial variance still exploring
            reasoning_parts.append(f"Satisfaction + coherence stable, but spatial variance high ({var_mean:.4f})")
            reasoning_parts.append("Organism still exploring spatial regions")
            decision = ConvergenceDecision.CONTINUE

        elif satisfaction_stable:
            # Only satisfaction stable
            reasoning_parts.append(f"Satisfaction stable ({sat_mean:.3f}), but coherence/variance not settled")
            decision = ConvergenceDecision.CONTINUE

        else:
            # Not stable yet
            reasoning_parts.append(f"Satisfaction not stable (variance={sat_variance:.4f}, target={self.config.SATISFACTION_VARIANCE_THRESHOLD})")
            decision = ConvergenceDecision.CONTINUE

        reasoning = " | ".join(reasoning_parts)

        result = ConvergenceResult(
            decision=decision,
            iteration_count=iteration_count,
            converged_at=self.converged_at,
            reasoning=reasoning,
            satisfaction_stable=satisfaction_stable,
            coherence_stable=coherence_stable,
            variance_stable=variance_stable,
            window_satisfaction_mean=sat_mean,
            window_satisfaction_variance=sat_variance,
            window_coherence_mean=coh_mean,
            window_variance_mean=var_mean,
            final_satisfaction=self.iterations[-1].satisfaction,
            final_coherence=self.iterations[-1].field_coherence,
            final_variance=self.iterations[-1].spatial_variance,
            final_confidence=self.iterations[-1].emission_confidence
        )

        self.convergence_result = result
        return result

    def _create_result(self, decision: ConvergenceDecision, reasoning: str) -> ConvergenceResult:
        """Helper to create ConvergenceResult with current state."""
        if len(self.iterations) == 0:
            # No iterations yet
            return ConvergenceResult(
                decision=decision,
                iteration_count=0,
                converged_at=None,
                reasoning=reasoning,
                satisfaction_stable=False,
                coherence_stable=False,
                variance_stable=False,
                window_satisfaction_mean=0.0,
                window_satisfaction_variance=0.0,
                window_coherence_mean=0.0,
                window_variance_mean=0.0,
                final_satisfaction=0.0,
                final_coherence=0.0,
                final_variance=0.0,
                final_confidence=0.0
            )

        latest = self.iterations[-1]
        return ConvergenceResult(
            decision=decision,
            iteration_count=len(self.iterations),
            converged_at=self.converged_at,
            reasoning=reasoning,
            satisfaction_stable=False,
            coherence_stable=False,
            variance_stable=False,
            window_satisfaction_mean=latest.satisfaction,
            window_satisfaction_variance=0.0,
            window_coherence_mean=latest.field_coherence,
            window_variance_mean=latest.spatial_variance,
            final_satisfaction=latest.satisfaction,
            final_coherence=latest.field_coherence,
            final_variance=latest.spatial_variance,
            final_confidence=latest.emission_confidence
        )

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of convergence tracking."""
        if not self.iterations:
            return {
                'pair_id': self.pair_id,
                'iterations': 0,
                'converged': False,
                'status': 'not_started'
            }

        satisfaction_history = [r.satisfaction for r in self.iterations]
        coherence_history = [r.field_coherence for r in self.iterations]

        return {
            'pair_id': self.pair_id,
            'iterations': len(self.iterations),
            'converged': self.converged,
            'converged_at': self.converged_at,
            'satisfaction_mean': float(np.mean(satisfaction_history)),
            'satisfaction_final': self.iterations[-1].satisfaction,
            'satisfaction_trend': float(np.polyfit(range(len(satisfaction_history)), satisfaction_history, 1)[0]) if len(satisfaction_history) >= 2 else 0.0,
            'coherence_mean': float(np.mean(coherence_history)),
            'coherence_final': self.iterations[-1].field_coherence,
            'final_confidence': self.iterations[-1].emission_confidence,
            'convergence_result': asdict(self.convergence_result) if self.convergence_result else None
        }


# ============================================================================
# Unit Tests
# ============================================================================

def test_basic_convergence():
    """Test basic convergence detection."""
    print("\n" + "="*70)
    print("TEST 1: Basic Convergence Detection")
    print("="*70)

    tracker = EpochConvergenceTracker(
        pair_id="test_pair_1",
        stability_window=3,
        satisfaction_target=0.75,
        max_iterations=5
    )

    # Iteration 1: Low satisfaction
    tracker.record_iteration(
        satisfaction=0.60,
        field_coherence=0.65,
        spatial_variance=0.010,
        emission_confidence=0.50,
        v0_final=0.40,
        convergence_cycles=2
    )

    result = tracker.evaluate_convergence()
    print(f"After iteration 1: {result.decision.value}")
    print(f"   Reasoning: {result.reasoning}")
    assert result.decision == ConvergenceDecision.CONTINUE

    # Iteration 2: Better
    tracker.record_iteration(
        satisfaction=0.76,
        field_coherence=0.72,
        spatial_variance=0.004,
        emission_confidence=0.65,
        v0_final=0.30,
        convergence_cycles=2
    )

    result = tracker.evaluate_convergence()
    print(f"After iteration 2: {result.decision.value}")
    print(f"   Reasoning: {result.reasoning}")
    assert result.decision == ConvergenceDecision.CONTINUE  # Need stability

    # Iteration 3: Stable (very similar to iteration 2)
    tracker.record_iteration(
        satisfaction=0.76,
        field_coherence=0.72,
        spatial_variance=0.004,
        emission_confidence=0.70,
        v0_final=0.28,
        convergence_cycles=2
    )

    result = tracker.evaluate_convergence()
    print(f"After iteration 3: {result.decision.value}")
    print(f"   Reasoning: {result.reasoning}")

    # If still not stable, add iteration 4
    if result.decision != ConvergenceDecision.HALT:
        tracker.record_iteration(
            satisfaction=0.76,
            field_coherence=0.73,
            spatial_variance=0.004,
            emission_confidence=0.71,
            v0_final=0.27,
            convergence_cycles=2
        )

    result = tracker.evaluate_convergence()
    print(f"After final iteration: {result.decision.value}")
    print(f"   Reasoning: {result.reasoning}")
    print(f"   Satisfaction stable: {result.satisfaction_stable}")
    print(f"   Coherence stable: {result.coherence_stable}")
    print(f"   Variance stable: {result.variance_stable}")

    # Should HALT (all stable)
    assert result.decision == ConvergenceDecision.HALT, f"Expected HALT, got {result.decision.value}"
    assert result.satisfaction_stable, "Satisfaction should be stable"
    assert result.coherence_stable, "Coherence should be stable"
    assert result.variance_stable, "Variance should be stable"

    print("\n✅ TEST 1 PASSED - Basic convergence working")


def test_max_iterations():
    """Test max iterations safety limit."""
    print("\n" + "="*70)
    print("TEST 2: Max Iterations Safety")
    print("="*70)

    tracker = EpochConvergenceTracker(
        pair_id="test_pair_2",
        max_iterations=3
    )

    # 3 iterations, never stabilizes
    for i in range(3):
        tracker.record_iteration(
            satisfaction=0.60 + i * 0.05,  # Slowly improving
            field_coherence=0.60 + i * 0.03,
            spatial_variance=0.010 - i * 0.001,
            emission_confidence=0.50 + i * 0.10,
            v0_final=0.40,
            convergence_cycles=2
        )

        result = tracker.evaluate_convergence()
        print(f"After iteration {i+1}: {result.decision.value}")

    # Should hit MAX_ITERATIONS
    assert result.decision == ConvergenceDecision.MAX_ITERATIONS
    print(f"   Reasoning: {result.reasoning}")
    print("\n✅ TEST 2 PASSED - Max iterations safety working")


def test_high_spatial_variance_prevents_halt():
    """Test that high spatial variance prevents convergence."""
    print("\n" + "="*70)
    print("TEST 3: High Spatial Variance Prevents HALT")
    print("="*70)

    tracker = EpochConvergenceTracker(
        pair_id="test_pair_3",
        stability_window=3
    )

    # High satisfaction + coherence, BUT high spatial variance (organism exploring)
    for i in range(4):
        tracker.record_iteration(
            satisfaction=0.80,  # High and stable
            field_coherence=0.75,  # High and stable
            spatial_variance=0.012,  # HIGH variance (still exploring)
            emission_confidence=0.70,
            v0_final=0.25,
            convergence_cycles=2
        )

    result = tracker.evaluate_convergence()
    print(f"After 4 iterations: {result.decision.value}")
    print(f"   Reasoning: {result.reasoning}")

    # Should CONTINUE (spatial variance not stable)
    assert result.decision == ConvergenceDecision.CONTINUE
    assert result.satisfaction_stable
    assert result.coherence_stable
    assert not result.variance_stable  # Variance NOT stable

    print("\n✅ TEST 3 PASSED - Spatial variance prevents premature halt")


def test_regime_forced_continue():
    """Test that EXPLORING regime forces continue."""
    print("\n" + "="*70)
    print("TEST 4: Regime Forces CONTINUE")
    print("="*70)

    tracker = EpochConvergenceTracker(
        pair_id="test_pair_4",
        stability_window=3
    )

    # All metrics stable, BUT regime is EXPLORING
    for i in range(4):
        tracker.record_iteration(
            satisfaction=0.78,
            field_coherence=0.74,
            spatial_variance=0.003,
            emission_confidence=0.72,
            v0_final=0.26,
            convergence_cycles=2,
            regime=SatisfactionRegime.EXPLORING  # Forces continue
        )

    result = tracker.evaluate_convergence()
    print(f"After 4 iterations: {result.decision.value}")
    print(f"   Reasoning: {result.reasoning}")

    # Should CONTINUE (regime forces it)
    assert result.decision == ConvergenceDecision.CONTINUE
    assert "EXPLORING" in result.reasoning

    print("\n✅ TEST 4 PASSED - Regime-based CONTINUE working")


def run_all_tests():
    """Run all convergence tracker tests."""
    print("\n" + "="*70)
    print("🧪 EPOCH CONVERGENCE TRACKER TESTS")
    print("="*70)

    try:
        test_basic_convergence()
        test_max_iterations()
        test_high_spatial_variance_prevents_halt()
        test_regime_forced_continue()

        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED")
        print("="*70)
        print("\n📊 Convergence Tracker Ready:")
        print("   ✅ Stability-based HALT detection")
        print("   ✅ Max iterations safety")
        print("   ✅ Spatial variance awareness")
        print("   ✅ Regime-based gating")
        print("   ✅ Multi-metric stability (satisfaction + coherence + variance)")
        print("\n🌀 Ready for multi-iteration training with stable memory formation!")

        return True
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
