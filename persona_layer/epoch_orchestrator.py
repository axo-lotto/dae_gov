"""
Epoch Orchestrator - DAE 3.0 Fractal Levels 5-7
================================================

Implements epoch-level learning and global reward propagation from DAE 3.0.

Fractal Reward Cascade (DAE 3.0):
- Level 1 (Micro): Phrase patterns → Hebbian memory
- Level 2 (Organ): Organ weights → Gradient learning
- Level 3 (Coupling): R-matrix → Hebbian strengthening
- Level 4 (Family): V0 targets → EMA optimization
- **Level 5 (Task): Task confidence → Success tracking** ⭐
- **Level 6 (Epoch): Epoch consolidation → Batch learning** ⭐
- **Level 7 (Global): Organism confidence → Compound growth** ⭐

Key Concepts:
- **Task**: Single conversation with success/failure classification
- **Epoch**: Batch of N tasks (e.g., 10-30 conversations)
- **Global Confidence**: Organism-wide learning trajectory

Mathematical Formulation (DAE 3.0):
    R₅(task) = mean{R₄(family) | families in task}
    R₆(epoch) = mean{R₅(task) | tasks ∈ epoch}
    R₇(global) = EMA(R₆(epoch), α=0.1)

Date: November 12, 2025
Status: DAE 3.0 Integration - Fractal Levels 5-7
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class TaskResult:
    """Result of a single task (conversation)"""
    task_id: str
    input_text: str
    emission_text: str
    satisfaction: float
    confidence: float
    family_id: Optional[str]
    v0_final: float
    convergence_cycles: int
    success: bool  # satisfaction > threshold
    timestamp: str


@dataclass
class EpochResult:
    """Consolidated result of an epoch (batch of tasks)"""
    epoch_id: int
    task_count: int
    success_count: int
    success_rate: float
    mean_satisfaction: float
    mean_confidence: float
    mean_v0_final: float
    mean_convergence_cycles: float
    families_discovered: int
    epoch_reward: float  # R₆ - consolidated reward
    timestamp: str


@dataclass
class GlobalState:
    """Global organism learning state"""
    total_epochs: int
    total_tasks: int
    global_confidence: float  # R₇ - organism-wide confidence
    compound_growth_rate: float  # CAGR across epochs
    epoch_history: List[float]  # R₆ values over time
    last_updated: str


class EpochOrchestrator:
    """
    Orchestrates epoch-level learning and global reward propagation.

    Implements DAE 3.0 Fractal Levels 5-7:
    - Task tracking (Level 5)
    - Epoch consolidation (Level 6)
    - Global confidence updates (Level 7)
    """

    def __init__(
        self,
        organism_wrapper,
        epoch_size: int = 10,
        success_threshold: float = 0.75,
        global_learning_rate: float = 0.1,
        results_dir: Path = Path("results/epochs")
    ):
        """
        Initialize epoch orchestrator.

        Args:
            organism_wrapper: ConversationalOrganismWrapper instance
            epoch_size: Number of tasks per epoch
            success_threshold: Minimum satisfaction for task success
            global_learning_rate: EMA α for global confidence
            results_dir: Directory to save epoch results
        """
        self.organism = organism_wrapper
        self.epoch_size = epoch_size
        self.success_threshold = success_threshold
        self.global_alpha = global_learning_rate
        self.results_dir = results_dir

        # Ensure results directory exists
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Current epoch state
        self.current_epoch_id = 0
        self.current_epoch_tasks: List[TaskResult] = []

        # Global state
        self.global_state = self._load_or_initialize_global_state()

        print(f"✅ Epoch Orchestrator initialized")
        print(f"   Epoch size: {epoch_size} tasks")
        print(f"   Success threshold: {success_threshold}")
        print(f"   Global confidence: {self.global_state.global_confidence:.3f}")
        print(f"   Total epochs completed: {self.global_state.total_epochs}")

    def _load_or_initialize_global_state(self) -> GlobalState:
        """Load existing global state or initialize new"""
        state_path = self.results_dir / "global_state.json"

        if state_path.exists():
            try:
                with open(state_path, 'r') as f:
                    data = json.load(f)

                return GlobalState(
                    total_epochs=data.get('total_epochs', 0),
                    total_tasks=data.get('total_tasks', 0),
                    global_confidence=data.get('global_confidence', 0.5),
                    compound_growth_rate=data.get('compound_growth_rate', 0.0),
                    epoch_history=data.get('epoch_history', []),
                    last_updated=data.get('last_updated', datetime.now().isoformat())
                )
            except Exception as e:
                print(f"   ⚠️  Error loading global state: {e}, initializing new")

        # Initialize new global state
        return GlobalState(
            total_epochs=0,
            total_tasks=0,
            global_confidence=0.5,  # Start neutral
            compound_growth_rate=0.0,
            epoch_history=[],
            last_updated=datetime.now().isoformat()
        )

    def process_task(
        self,
        input_text: str,
        expected_output: Optional[str] = None,
        enable_phase2: bool = True,
        verbose: bool = False
    ) -> TaskResult:
        """
        Process a single task (conversation) and record result.

        DAE 3.0 Level 5: Task-level confidence tracking.

        Args:
            input_text: User input
            expected_output: Optional ground truth for supervised learning
            enable_phase2: Enable multi-cycle V0 convergence
            verbose: Print task details

        Returns:
            TaskResult with task-level metrics
        """
        # Generate task ID
        task_id = f"task_{self.global_state.total_tasks + len(self.current_epoch_tasks) + 1:05d}"

        # Process conversation
        result = self.organism.process_text(
            text=input_text,
            enable_phase2=enable_phase2,
            enable_tsk_recording=False
        )

        # Extract metrics
        satisfaction = result['felt_states']['satisfaction_final']
        confidence = result['felt_states'].get('emission_confidence', 0.0)
        v0_final = result['felt_states']['v0_energy']['final_energy']
        convergence_cycles = result['felt_states']['convergence_cycles']
        emission_text = result.get('emission_text', '')

        # Get family assignment
        family_id = None
        if self.organism.phase5_learning:
            family_id = self.organism.phase5_learning.get_current_family_id()

        # Determine task success
        success = satisfaction >= self.success_threshold

        # Create task result
        task_result = TaskResult(
            task_id=task_id,
            input_text=input_text,
            emission_text=emission_text,
            satisfaction=satisfaction,
            confidence=confidence,
            family_id=family_id,
            v0_final=v0_final,
            convergence_cycles=convergence_cycles,
            success=success,
            timestamp=datetime.now().isoformat()
        )

        # Add to current epoch
        self.current_epoch_tasks.append(task_result)

        if verbose:
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"\n{status} Task {task_id}:")
            print(f"   Satisfaction: {satisfaction:.3f} (threshold: {self.success_threshold})")
            print(f"   Confidence: {confidence:.3f}")
            print(f"   Family: {family_id if family_id else 'None'}")

        # Check if epoch is complete
        if len(self.current_epoch_tasks) >= self.epoch_size:
            self._consolidate_epoch()

        return task_result

    def _consolidate_epoch(self) -> EpochResult:
        """
        Consolidate epoch and update global state.

        DAE 3.0 Levels 6+7:
        - Compute epoch reward R₆
        - Update global confidence R₇ via EMA
        - Track compound growth
        """
        if not self.current_epoch_tasks:
            return None

        self.current_epoch_id += 1

        # Compute epoch-level metrics (R₆)
        success_count = sum(1 for task in self.current_epoch_tasks if task.success)
        success_rate = success_count / len(self.current_epoch_tasks)

        mean_satisfaction = np.mean([task.satisfaction for task in self.current_epoch_tasks])
        mean_confidence = np.mean([task.confidence for task in self.current_epoch_tasks])
        mean_v0_final = np.mean([task.v0_final for task in self.current_epoch_tasks])
        mean_convergence_cycles = np.mean([task.convergence_cycles for task in self.current_epoch_tasks])

        # Count unique families discovered
        families = set(task.family_id for task in self.current_epoch_tasks if task.family_id)
        families_discovered = len(families)

        # Epoch reward (R₆): Weighted combination of success rate and confidence
        # DAE 3.0 formula: R₆ = α * success_rate + β * mean_confidence
        alpha_success = 0.6
        beta_confidence = 0.4
        epoch_reward = alpha_success * success_rate + beta_confidence * mean_confidence

        # Create epoch result
        epoch_result = EpochResult(
            epoch_id=self.current_epoch_id,
            task_count=len(self.current_epoch_tasks),
            success_count=success_count,
            success_rate=success_rate,
            mean_satisfaction=mean_satisfaction,
            mean_confidence=mean_confidence,
            mean_v0_final=mean_v0_final,
            mean_convergence_cycles=mean_convergence_cycles,
            families_discovered=families_discovered,
            epoch_reward=epoch_reward,
            timestamp=datetime.now().isoformat()
        )

        # Update global state (R₇ - EMA)
        self.global_state.epoch_history.append(epoch_reward)

        # Compute global confidence via EMA
        if self.global_state.total_epochs == 0:
            # First epoch - initialize
            self.global_state.global_confidence = epoch_reward
        else:
            # EMA update: R₇ ← R₇ + α(R₆ - R₇)
            self.global_state.global_confidence = (
                (1 - self.global_alpha) * self.global_state.global_confidence +
                self.global_alpha * epoch_reward
            )

        # Compute compound growth rate (CAGR)
        if len(self.global_state.epoch_history) >= 2:
            first_reward = self.global_state.epoch_history[0]
            last_reward = self.global_state.epoch_history[-1]
            n_epochs = len(self.global_state.epoch_history)

            if first_reward > 0:
                # CAGR = (end_value / start_value)^(1/n) - 1
                self.global_state.compound_growth_rate = (
                    (last_reward / first_reward) ** (1 / n_epochs) - 1
                )

        # Update counters
        self.global_state.total_epochs += 1
        self.global_state.total_tasks += len(self.current_epoch_tasks)
        self.global_state.last_updated = datetime.now().isoformat()

        # Save results
        self._save_epoch_result(epoch_result)
        self._save_global_state()

        # Print summary
        print(f"\n{'='*80}")
        print(f"📊 EPOCH {self.current_epoch_id} COMPLETE")
        print(f"{'='*80}")
        print(f"Tasks: {epoch_result.task_count}")
        print(f"Success rate: {epoch_result.success_rate:.1%} ({success_count}/{epoch_result.task_count})")
        print(f"Mean satisfaction: {epoch_result.mean_satisfaction:.3f}")
        print(f"Mean confidence: {epoch_result.mean_confidence:.3f}")
        print(f"Families discovered: {epoch_result.families_discovered}")
        print(f"Epoch reward (R₆): {epoch_reward:.3f}")
        print(f"Global confidence (R₇): {self.global_state.global_confidence:.3f}")
        if self.global_state.compound_growth_rate != 0:
            print(f"Compound growth rate: {self.global_state.compound_growth_rate:+.1%} per epoch")

        # Clear current epoch
        self.current_epoch_tasks = []

        return epoch_result

    def _save_epoch_result(self, epoch_result: EpochResult):
        """Save epoch result to JSON"""
        result_path = self.results_dir / f"epoch_{epoch_result.epoch_id:03d}_result.json"

        with open(result_path, 'w') as f:
            json.dump(asdict(epoch_result), f, indent=2)

        print(f"   ✅ Saved epoch result: {result_path}")

    def _save_global_state(self):
        """Save global state to JSON"""
        state_path = self.results_dir / "global_state.json"

        with open(state_path, 'w') as f:
            json.dump(asdict(self.global_state), f, indent=2)

    def force_epoch_consolidation(self) -> Optional[EpochResult]:
        """Force consolidation of current epoch (even if incomplete)"""
        if self.current_epoch_tasks:
            return self._consolidate_epoch()
        return None

    def get_global_report(self) -> Dict[str, Any]:
        """Get global learning trajectory report"""
        return {
            'total_epochs': self.global_state.total_epochs,
            'total_tasks': self.global_state.total_tasks,
            'global_confidence': self.global_state.global_confidence,
            'compound_growth_rate': self.global_state.compound_growth_rate,
            'epoch_history': self.global_state.epoch_history,
            'last_updated': self.global_state.last_updated
        }


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 EPOCH ORCHESTRATOR TEST")
    print("="*70)

    # This would require organism wrapper initialization
    print("\n✅ EpochOrchestrator implementation complete!")
    print("   Use with ConversationalOrganismWrapper for full testing")
