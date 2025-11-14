"""
Epoch Training Orchestrator - Multi-Iteration + DAE 3.0 Integration
====================================================================

Combines multi-iteration training with DAE 3.0 fractal reward cascade for
complete epoch-based learning with intelligence, continuity, and superject
dynamic validation.

Integration:
- multi_iteration_trainer.py: 2-5 iterations per conversation
- epoch_orchestrator.py: Fractal Levels 5-7 (task/epoch/global)
- Regime-based adaptation: EXPLORING → CONVERGING → STABLE → COMMITTED
- Entropy: Phase 1 surface entropy for voice development

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: Epoch Training Integration
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime

try:
    from .multi_iteration_trainer import MultiIterationTrainer, TrainingPairResult
    from .satisfaction_regime import SatisfactionRegime
    from .entropy_config import EntropyConfig
except ImportError:
    from multi_iteration_trainer import MultiIterationTrainer, TrainingPairResult
    from satisfaction_regime import SatisfactionRegime
    from entropy_config import EntropyConfig


@dataclass
class RegimeConfig:
    """Configuration for a training regime."""
    name: str
    epochs: Tuple[int, int]  # (start_epoch, end_epoch) inclusive
    tau_threshold: float  # Emission confidence threshold
    exploration_factor: float  # Entropy exploration level
    max_iterations: int  # Multi-iteration training limit
    satisfaction_target: float  # Convergence target
    description: str


@dataclass
class EpochTrainingResult:
    """Complete result of an epoch (batch of training pairs)."""
    epoch_id: int
    regime: str

    # Training metrics
    total_pairs: int
    converged_count: int
    convergence_rate: float
    mean_iterations: float
    mean_satisfaction: float
    mean_confidence: float
    mean_tau: float

    # Learning metrics
    families_discovered: int
    mean_r_matrix_coupling: float
    mean_v0_final: float
    mean_convergence_cycles: float

    # Regime distribution
    regime_distribution: Dict[str, int]

    # DAE 3.0 Fractal Rewards
    task_rewards: List[float]  # R₅ per conversation
    epoch_reward: float  # R₆ mean of task rewards

    # Timing
    start_time: str
    end_time: str
    total_time_seconds: float

    # Per-pair results
    pair_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class GlobalTrainingState:
    """Global organism training state across all epochs."""
    total_epochs: int
    total_conversations: int
    total_families: int

    # Global confidence (R₇)
    global_confidence: float
    global_confidence_history: List[float]

    # Compound learning growth
    compound_growth_rate: float  # CAGR

    # Epoch history
    epoch_rewards: List[float]  # R₆ per epoch
    epoch_satisfaction: List[float]
    epoch_convergence_rates: List[float]

    # Current regime
    current_regime: str

    # R-matrix statistics
    r_matrix_coupling_history: List[float]

    last_updated: str


class EpochTrainingOrchestrator:
    """
    Orchestrates multi-epoch training with regime-based adaptation.

    Implements:
    - 10-15 epoch training structure
    - 4 training regimes (EXPLORING → CONVERGING → STABLE → COMMITTED)
    - Multi-iteration training (2-5 iterations per pair)
    - DAE 3.0 fractal reward cascade (Levels 5-7)
    - Regime-adaptive entropy (Phase 1 surface)
    """

    def __init__(
        self,
        organism_wrapper,
        results_dir: Path = Path("results/epoch_training"),
        global_learning_rate: float = 0.1,  # EMA alpha for R₇
        regime_configs: Optional[List[RegimeConfig]] = None
    ):
        """
        Initialize epoch training orchestrator.

        Args:
            organism_wrapper: ConversationalOrganismWrapper instance
            results_dir: Directory to save training results
            global_learning_rate: EMA alpha for global confidence (R₇)
            regime_configs: List of RegimeConfig for 4 regimes (or use defaults)
        """
        self.organism = organism_wrapper
        self.results_dir = results_dir
        self.global_learning_rate = global_learning_rate

        # Ensure results directory exists
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Load or create regime configurations
        if regime_configs is None:
            self.regime_configs = self._create_default_regimes()
        else:
            self.regime_configs = regime_configs

        # Initialize global state
        self.global_state = self._load_or_create_global_state()

        # Initialize multi-iteration trainer (will be updated per regime)
        self.trainer = None

        print(f"✅ Epoch Training Orchestrator initialized")
        print(f"   Results dir: {results_dir}")
        print(f"   Global learning rate (α): {global_learning_rate}")
        print(f"   Regimes: {len(self.regime_configs)}")

    def _create_default_regimes(self) -> List[RegimeConfig]:
        """Create default 4-regime configuration."""
        return [
            RegimeConfig(
                name="EXPLORING",
                epochs=(1, 3),
                tau_threshold=0.30,
                exploration_factor=0.30,
                max_iterations=3,
                satisfaction_target=0.55,
                description="Pattern discovery, family formation, high exploration"
            ),
            RegimeConfig(
                name="CONVERGING",
                epochs=(4, 7),
                tau_threshold=0.50,
                exploration_factor=0.15,
                max_iterations=4,
                satisfaction_target=0.65,
                description="Strengthen successful patterns, moderate exploration"
            ),
            RegimeConfig(
                name="STABLE",
                epochs=(8, 10),
                tau_threshold=0.65,
                exploration_factor=0.05,
                max_iterations=5,
                satisfaction_target=0.75,
                description="Optimize couplings, refine families, low exploration"
            ),
            RegimeConfig(
                name="COMMITTED",
                epochs=(11, 15),
                tau_threshold=0.75,
                exploration_factor=0.00,
                max_iterations=5,
                satisfaction_target=0.75,
                description="Transfer learning, generalization, no exploration"
            )
        ]

    def _load_or_create_global_state(self) -> GlobalTrainingState:
        """Load existing global state or create new."""
        global_state_path = self.results_dir / "global_training_state.json"

        if global_state_path.exists():
            try:
                with open(global_state_path, 'r') as f:
                    data = json.load(f)
                    print(f"✅ Loaded existing global state")
                    print(f"   Total epochs: {data['total_epochs']}")
                    print(f"   Global confidence (R₇): {data['global_confidence']:.3f}")
                    return GlobalTrainingState(**data)
            except Exception as e:
                print(f"⚠️  Error loading global state: {e}")

        # Create new global state
        return GlobalTrainingState(
            total_epochs=0,
            total_conversations=0,
            total_families=1,  # Assume 1 existing family
            global_confidence=0.50,  # Neutral baseline
            global_confidence_history=[0.50],
            compound_growth_rate=0.0,
            epoch_rewards=[],
            epoch_satisfaction=[],
            epoch_convergence_rates=[],
            current_regime="EXPLORING",
            r_matrix_coupling_history=[],
            last_updated=datetime.now().isoformat()
        )

    def _save_global_state(self):
        """Save global training state to JSON."""
        global_state_path = self.results_dir / "global_training_state.json"

        with open(global_state_path, 'w') as f:
            json.dump(asdict(self.global_state), f, indent=2)

        print(f"💾 Saved global training state")

    def _get_regime_for_epoch(self, epoch_id: int) -> RegimeConfig:
        """Get regime configuration for a given epoch."""
        for regime in self.regime_configs:
            if regime.epochs[0] <= epoch_id <= regime.epochs[1]:
                return regime

        # Default to last regime if epoch beyond range
        return self.regime_configs[-1]

    def train_epoch(
        self,
        epoch_id: int,
        training_pairs: List[Dict[str, str]],
        verbose: bool = True
    ) -> EpochTrainingResult:
        """
        Train a single epoch (batch of training pairs).

        Args:
            epoch_id: Epoch number (1-indexed)
            training_pairs: List of dicts with 'pair_id', 'input_text', 'expected_output'
            verbose: Print training progress

        Returns:
            EpochTrainingResult with complete epoch metrics
        """
        start_time = datetime.now()

        # Get regime for this epoch
        regime = self._get_regime_for_epoch(epoch_id)

        if verbose:
            print(f"\n{'='*70}")
            print(f"🎓 EPOCH {epoch_id} - {regime.name}")
            print(f"{'='*70}")
            print(f"   Tau threshold: {regime.tau_threshold:.2f}")
            print(f"   Exploration: {regime.exploration_factor:.2f}")
            print(f"   Max iterations: {regime.max_iterations}")
            print(f"   Satisfaction target: {regime.satisfaction_target:.2f}")
            print(f"   Training pairs: {len(training_pairs)}")

        # Initialize multi-iteration trainer with regime parameters
        self.trainer = MultiIterationTrainer(
            organism_wrapper=self.organism,
            results_dir=self.results_dir / f"epoch_{epoch_id:03d}",
            initial_tau=regime.tau_threshold,
            max_iterations=regime.max_iterations,
            satisfaction_target=regime.satisfaction_target
        )

        # Train all pairs
        pair_results = self.trainer.train_multiple_pairs(
            training_pairs=training_pairs,
            verbose=verbose
        )

        # Compute epoch-level metrics
        converged_count = sum(1 for r in pair_results if r.converged)
        convergence_rate = converged_count / len(pair_results) if pair_results else 0.0

        mean_iterations = np.mean([r.iterations for r in pair_results])
        mean_satisfaction = np.mean([r.final_satisfaction for r in pair_results])
        mean_confidence = np.mean([r.final_confidence for r in pair_results])
        mean_tau = np.mean([r.final_tau for r in pair_results])
        mean_v0 = np.mean([r.final_variance for r in pair_results])  # Proxy for V0

        # Regime distribution
        final_regimes = [r.final_regime for r in pair_results]
        regime_distribution = {}
        for reg in final_regimes:
            regime_distribution[reg] = regime_distribution.get(reg, 0) + 1

        # DAE 3.0 Fractal Rewards
        # R₅ (task): Use final_confidence as proxy for task reward
        task_rewards = [r.final_confidence for r in pair_results]

        # R₆ (epoch): Mean of task rewards
        epoch_reward = np.mean(task_rewards)

        # Families discovered (from organism)
        families_count = 1  # Default
        if self.organism.phase5_learning:
            # phase5_learning.families is OrganicConversationalFamilies object
            # phase5_learning.families.families is the actual Dict[str, ConversationalFamily]
            families_count = len(self.organism.phase5_learning.families.families)

        # R-matrix coupling (extract from organism)
        r_matrix_coupling = 0.02  # Default
        r_matrix_snapshot = None
        if self.organism.organ_coupling_learner and hasattr(self.organism.organ_coupling_learner, 'R_matrix'):
            r_matrix = self.organism.organ_coupling_learner.R_matrix
            if r_matrix is not None:
                r_matrix_coupling = float(np.mean(r_matrix))

                # Save R-matrix snapshot for stability testing
                r_matrix_snapshot = {
                    'matrix': r_matrix.tolist(),
                    'mean_coupling': float(np.mean(r_matrix)),
                    'std_coupling': float(np.std(r_matrix)),
                    'max_coupling': float(np.max(r_matrix)),
                    'min_coupling': float(np.min(r_matrix))
                }

        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        # Create epoch result
        epoch_result = EpochTrainingResult(
            epoch_id=epoch_id,
            regime=regime.name,
            total_pairs=len(pair_results),
            converged_count=converged_count,
            convergence_rate=convergence_rate,
            mean_iterations=mean_iterations,
            mean_satisfaction=mean_satisfaction,
            mean_confidence=mean_confidence,
            mean_tau=mean_tau,
            families_discovered=families_count,
            mean_r_matrix_coupling=r_matrix_coupling,
            mean_v0_final=mean_v0,
            mean_convergence_cycles=3.0,  # TODO: Extract from results
            regime_distribution=regime_distribution,
            task_rewards=task_rewards,
            epoch_reward=epoch_reward,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            total_time_seconds=total_time,
            pair_results=[asdict(r) for r in pair_results]
        )

        # Update global state (R₇)
        self._update_global_state(epoch_result)

        # Save epoch result (with R-matrix snapshot)
        self._save_epoch_result(epoch_result, r_matrix_snapshot=r_matrix_snapshot)

        if verbose:
            print(f"\n{'='*70}")
            print(f"📊 EPOCH {epoch_id} SUMMARY")
            print(f"{'='*70}")
            print(f"   Convergence rate: {convergence_rate:.1%}")
            print(f"   Mean iterations: {mean_iterations:.2f}")
            print(f"   Mean satisfaction: {mean_satisfaction:.3f}")
            print(f"   Mean confidence: {mean_confidence:.3f}")
            print(f"   Epoch reward (R₆): {epoch_reward:.3f}")
            print(f"   Global confidence (R₇): {self.global_state.global_confidence:.3f}")
            print(f"   Training time: {total_time:.1f}s")

        return epoch_result

    def _update_global_state(self, epoch_result: EpochTrainingResult):
        """Update global training state with epoch results (Level 7: R₇)."""
        # Update R₇ using EMA: R₇_new = α × R₆ + (1-α) × R₇_old
        alpha = self.global_learning_rate
        r7_old = self.global_state.global_confidence
        r6 = epoch_result.epoch_reward

        r7_new = alpha * r6 + (1 - alpha) * r7_old

        self.global_state.global_confidence = r7_new
        self.global_state.global_confidence_history.append(r7_new)

        # Update epoch histories
        self.global_state.total_epochs += 1
        self.global_state.total_conversations += epoch_result.total_pairs
        self.global_state.epoch_rewards.append(r6)
        self.global_state.epoch_satisfaction.append(epoch_result.mean_satisfaction)
        self.global_state.epoch_convergence_rates.append(epoch_result.convergence_rate)
        self.global_state.r_matrix_coupling_history.append(epoch_result.mean_r_matrix_coupling)
        self.global_state.current_regime = epoch_result.regime
        self.global_state.total_families = epoch_result.families_discovered

        # Compute CAGR (compound annual growth rate)
        if len(self.global_state.global_confidence_history) >= 2:
            initial = self.global_state.global_confidence_history[0]
            final = self.global_state.global_confidence_history[-1]
            n_epochs = len(self.global_state.global_confidence_history) - 1

            if initial > 0:
                self.global_state.compound_growth_rate = ((final / initial) ** (1 / n_epochs) - 1) * 100

        self.global_state.last_updated = datetime.now().isoformat()

        # Save updated state
        self._save_global_state()

    def _save_epoch_result(self, epoch_result: EpochTrainingResult, r_matrix_snapshot: Optional[Dict] = None):
        """Save epoch result to JSON with R-matrix snapshot."""
        epoch_path = self.results_dir / f"epoch_{epoch_result.epoch_id:03d}_result.json"

        result_dict = asdict(epoch_result)

        # Add R-matrix snapshot if available
        if r_matrix_snapshot:
            result_dict['r_matrix_snapshot'] = r_matrix_snapshot

        with open(epoch_path, 'w') as f:
            json.dump(result_dict, f, indent=2)

        print(f"💾 Saved epoch {epoch_result.epoch_id} result")

    def train_multiple_epochs(
        self,
        start_epoch: int,
        end_epoch: int,
        training_pairs_per_epoch: int,
        training_corpus: List[Dict[str, str]],
        verbose: bool = True
    ) -> List[EpochTrainingResult]:
        """
        Train multiple epochs sequentially.

        Args:
            start_epoch: Starting epoch number (1-indexed)
            end_epoch: Ending epoch number (inclusive)
            training_pairs_per_epoch: Number of pairs per epoch
            training_corpus: Full training corpus to sample from
            verbose: Print progress

        Returns:
            List of EpochTrainingResult for each epoch
        """
        results = []

        for epoch_id in range(start_epoch, end_epoch + 1):
            # Sample training pairs for this epoch
            # TODO: Implement stratified/difficulty-weighted sampling
            sampled_pairs = self._sample_training_pairs(
                training_corpus,
                training_pairs_per_epoch,
                epoch_id
            )

            # Train epoch
            epoch_result = self.train_epoch(
                epoch_id=epoch_id,
                training_pairs=sampled_pairs,
                verbose=verbose
            )

            results.append(epoch_result)

        # Print final summary
        if verbose:
            self._print_training_summary(results)

        return results

    def _sample_training_pairs(
        self,
        corpus: List[Dict[str, str]],
        n_pairs: int,
        epoch_id: int
    ) -> List[Dict[str, str]]:
        """
        Sample training pairs for an epoch.

        TODO: Implement stratified/difficulty-weighted sampling based on regime.
        For now, simple random sampling.
        """
        if len(corpus) <= n_pairs:
            return corpus

        indices = np.random.choice(len(corpus), size=n_pairs, replace=False)
        return [corpus[i] for i in indices]

    def _print_training_summary(self, results: List[EpochTrainingResult]):
        """Print summary of multi-epoch training."""
        print(f"\n{'='*70}")
        print(f"📊 MULTI-EPOCH TRAINING SUMMARY")
        print(f"{'='*70}")

        total_epochs = len(results)
        total_conversations = sum(r.total_pairs for r in results)

        print(f"\n🎯 Training Completed:")
        print(f"   Total epochs: {total_epochs}")
        print(f"   Total conversations: {total_conversations}")
        print(f"   Total families: {self.global_state.total_families}")

        print(f"\n📈 Global Metrics:")
        print(f"   Global confidence (R₇): {self.global_state.global_confidence:.3f}")
        print(f"   CAGR: {self.global_state.compound_growth_rate:.1f}%")

        print(f"\n🌀 Epoch Progression:")
        for result in results:
            print(f"   Epoch {result.epoch_id} ({result.regime:12s}): "
                  f"sat={result.mean_satisfaction:.3f}, "
                  f"conv={result.convergence_rate:.1%}, "
                  f"R₆={result.epoch_reward:.3f}")

        print(f"\n✅ Training complete! Results saved to {self.results_dir}")


# Quick test/demo
if __name__ == "__main__":
    print("="*70)
    print("🎓 EPOCH TRAINING ORCHESTRATOR")
    print("="*70)
    print("\n⚠️  This requires ConversationalOrganismWrapper to run.")
    print("   Use training runner script for full epoch training.")
    print("\n✅ EpochTrainingOrchestrator implementation complete!")
    print("\n📊 Key Features:")
    print("   - 10-15 epoch training structure")
    print("   - 4 training regimes (EXPLORING → COMMITTED)")
    print("   - Multi-iteration training (2-5 iterations/pair)")
    print("   - DAE 3.0 fractal rewards (R₅/R₆/R₇)")
    print("   - Regime-adaptive entropy")
    print("   - Global confidence tracking (CAGR)")
    print("\n🌀 Ready to orchestrate epoch-based learning!")
