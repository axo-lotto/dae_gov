"""
Full System Epoch Training with Comprehensive Metrics
======================================================

Runs epoch training with all DAE 3.0 fractal levels enabled and tracks
comprehensive metrics for detailed organism behavior analysis.

This script:
1. Loads all 30 training pairs
2. Runs 5 epochs (10 tasks per epoch = 50 conversations total)
3. Tracks all 7 fractal levels
4. Records R-matrix evolution, family formation, organ specialization
5. Generates detailed organism behavior report

Date: November 12, 2025
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_orchestrator import EpochOrchestrator


class ComprehensiveMetricsTracker:
    """Tracks all metrics across fractal levels for behavior analysis"""

    def __init__(self):
        self.task_metrics = []
        self.epoch_metrics = []
        self.r_matrix_snapshots = []
        self.family_snapshots = []
        self.organ_coherence_history = []
        self.v0_trajectory_history = []
        self.transduction_pathway_counts = {}
        self.meta_atom_activation_counts = {}

    def record_task(self, task_result, felt_states, organism):
        """Record comprehensive task-level metrics"""

        # Core task metrics (Level 5)
        task_metrics = {
            'task_id': task_result.task_id,
            'timestamp': task_result.timestamp,
            'input_text': task_result.input_text[:100],  # First 100 chars
            'satisfaction': task_result.satisfaction,
            'confidence': task_result.confidence,
            'v0_final': task_result.v0_final,
            'convergence_cycles': task_result.convergence_cycles,
            'success': task_result.success,
            'family_id': task_result.family_id
        }

        # Organ coherences
        organ_coherences = felt_states.get('organ_coherences', {})
        task_metrics['organ_coherences'] = organ_coherences
        task_metrics['active_organs'] = sum(1 for coh in organ_coherences.values() if coh > 0.5)
        task_metrics['mean_coherence'] = np.mean(list(organ_coherences.values())) if organ_coherences else 0.0

        # V0 energy trajectory
        v0_energy = felt_states.get('v0_energy', {})
        task_metrics['v0_initial'] = v0_energy.get('initial_energy', 1.0)
        task_metrics['v0_descent'] = v0_energy.get('initial_energy', 1.0) - v0_energy.get('final_energy', 1.0)

        # Transduction pathway
        transduction = felt_states.get('transduction', {})
        if transduction:
            pathway = transduction.get('primary_pathway', 'unknown')
            task_metrics['transduction_pathway'] = pathway
            self.transduction_pathway_counts[pathway] = self.transduction_pathway_counts.get(pathway, 0) + 1

        # Meta-atom activations
        meta_atoms = felt_states.get('meta_atom_activations', {})
        if meta_atoms:
            active_meta_atoms = [atom for atom, act in meta_atoms.items() if act > 0.5]
            task_metrics['active_meta_atoms'] = active_meta_atoms
            for atom in active_meta_atoms:
                self.meta_atom_activation_counts[atom] = self.meta_atom_activation_counts.get(atom, 0) + 1

        # Nexus count
        task_metrics['nexus_count'] = felt_states.get('nexus_count', 0)

        self.task_metrics.append(task_metrics)
        self.organ_coherence_history.append(organ_coherences)
        self.v0_trajectory_history.append(v0_energy)

    def record_epoch(self, epoch_result, organism):
        """Record epoch-level metrics (Level 6)"""

        epoch_metrics = {
            'epoch_id': epoch_result.epoch_id,
            'timestamp': epoch_result.timestamp,
            'task_count': epoch_result.task_count,
            'success_count': epoch_result.success_count,
            'success_rate': epoch_result.success_rate,
            'mean_satisfaction': epoch_result.mean_satisfaction,
            'mean_confidence': epoch_result.mean_confidence,
            'mean_v0_final': epoch_result.mean_v0_final,
            'mean_convergence_cycles': epoch_result.mean_convergence_cycles,
            'families_discovered': epoch_result.families_discovered,
            'epoch_reward': epoch_result.epoch_reward
        }

        # R-matrix snapshot (Level 3)
        if organism.organ_coupling_learner:
            r_matrix = organism.organ_coupling_learner.R_matrix.copy()
            self.r_matrix_snapshots.append({
                'epoch_id': epoch_result.epoch_id,
                'r_matrix': r_matrix.tolist(),
                'mean_coupling': float(np.mean(r_matrix)),
                'max_coupling': float(np.max(r_matrix)),
                'total_updates': len(organism.organ_coupling_learner.update_history)
            })

        # Family learning snapshot (Level 4)
        if organism.family_v0_learner:
            family_states = {}
            for family_id, state in organism.family_v0_learner.family_states.items():
                mean_satisfaction = np.mean(state.satisfaction_history) if state.satisfaction_history else 0.0
                family_states[family_id] = {
                    'target_v0': state.target_v0,
                    'total_updates': state.total_updates,
                    'mean_satisfaction': float(mean_satisfaction),
                    'convergence_cycles_mean': state.convergence_cycles_mean,
                    'top_organs': sorted(state.organ_weights.items(), key=lambda x: x[1], reverse=True)[:5]
                }

            self.family_snapshots.append({
                'epoch_id': epoch_result.epoch_id,
                'families': family_states
            })

        self.epoch_metrics.append(epoch_metrics)

    def get_summary_report(self) -> Dict[str, Any]:
        """Generate comprehensive summary report"""

        if not self.task_metrics:
            return {'error': 'No task metrics recorded'}

        # Task-level aggregates
        satisfactions = [t['satisfaction'] for t in self.task_metrics]
        confidences = [t['confidence'] for t in self.task_metrics]
        v0_descents = [t['v0_descent'] for t in self.task_metrics]
        convergence_cycles = [t['convergence_cycles'] for t in self.task_metrics]
        active_organs = [t['active_organs'] for t in self.task_metrics]

        # Organ participation over time
        all_organs = set()
        for coh_dict in self.organ_coherence_history:
            all_organs.update(coh_dict.keys())

        organ_participation = {}
        for organ in all_organs:
            activations = [coh_dict.get(organ, 0.0) for coh_dict in self.organ_coherence_history]
            organ_participation[organ] = {
                'mean_coherence': float(np.mean(activations)),
                'activation_rate': sum(1 for a in activations if a > 0.5) / len(activations),
                'max_coherence': float(np.max(activations))
            }

        # R-matrix evolution
        r_matrix_evolution = []
        if self.r_matrix_snapshots:
            for snapshot in self.r_matrix_snapshots:
                r_matrix_evolution.append({
                    'epoch_id': snapshot['epoch_id'],
                    'mean_coupling': snapshot['mean_coupling'],
                    'max_coupling': snapshot['max_coupling'],
                    'total_updates': snapshot['total_updates']
                })

        # Family formation trajectory
        family_formation = []
        if self.family_snapshots:
            for snapshot in self.family_snapshots:
                family_count = len(snapshot['families'])
                family_formation.append({
                    'epoch_id': snapshot['epoch_id'],
                    'family_count': family_count,
                    'families': snapshot['families']
                })

        return {
            'training_summary': {
                'total_tasks': len(self.task_metrics),
                'total_epochs': len(self.epoch_metrics),
                'training_completed': datetime.now().isoformat()
            },
            'task_level_stats': {
                'mean_satisfaction': float(np.mean(satisfactions)),
                'std_satisfaction': float(np.std(satisfactions)),
                'mean_confidence': float(np.mean(confidences)),
                'std_confidence': float(np.std(confidences)),
                'mean_v0_descent': float(np.mean(v0_descents)),
                'mean_convergence_cycles': float(np.mean(convergence_cycles)),
                'mean_active_organs': float(np.mean(active_organs)),
                'success_rate': sum(1 for t in self.task_metrics if t['success']) / len(self.task_metrics)
            },
            'epoch_level_stats': {
                'epochs': self.epoch_metrics
            },
            'organ_participation': organ_participation,
            'r_matrix_evolution': r_matrix_evolution,
            'family_formation': family_formation,
            'transduction_pathways': self.transduction_pathway_counts,
            'meta_atom_activations': self.meta_atom_activation_counts,
            'raw_task_metrics': self.task_metrics
        }


def run_full_epoch_training(
    num_epochs: int = 5,
    tasks_per_epoch: int = 10,
    results_dir: Path = Path("results/epochs/full_system_training")
):
    """
    Run comprehensive epoch training with full metrics tracking.

    Args:
        num_epochs: Number of epochs to run
        tasks_per_epoch: Tasks per epoch
        results_dir: Directory to save results
    """

    print("=" * 80)
    print("🌀 FULL SYSTEM EPOCH TRAINING - DAE 3.0")
    print("=" * 80)
    print(f"\n📋 Configuration:")
    print(f"   Epochs: {num_epochs}")
    print(f"   Tasks per epoch: {tasks_per_epoch}")
    print(f"   Total tasks: {num_epochs * tasks_per_epoch}")
    print(f"   Results directory: {results_dir}")

    # Load training data
    training_pairs_path = Path("knowledge_base/conversational_training_pairs.json")
    print(f"\n📚 Loading training data from {training_pairs_path}...")

    with open(training_pairs_path, 'r') as f:
        training_data = json.load(f)

    training_pairs = training_data['training_pairs']
    print(f"   Loaded {len(training_pairs)} training pairs")

    # Initialize organism
    print(f"\n🧬 Initializing organism...")
    organism = ConversationalOrganismWrapper(bundle_path="Bundle")

    print(f"   11-organ system: ✅")
    print(f"   R-matrix coupling: {'✅' if organism.organ_coupling_learner else '❌'}")
    print(f"   Family V0 learning: {'✅' if organism.family_v0_learner else '❌'}")
    print(f"   Phase 5 organic learning: {'✅' if organism.phase5_learning else '❌'}")

    # Initialize epoch orchestrator
    print(f"\n📊 Initializing epoch orchestrator...")
    orchestrator = EpochOrchestrator(
        organism_wrapper=organism,
        epoch_size=tasks_per_epoch,
        success_threshold=0.75,
        global_learning_rate=0.1,
        results_dir=results_dir
    )

    # Initialize metrics tracker
    metrics_tracker = ComprehensiveMetricsTracker()

    # Get initial state
    initial_report = orchestrator.get_global_report()
    print(f"\n📈 Initial Global State:")
    print(f"   Total epochs: {initial_report['total_epochs']}")
    print(f"   Total tasks: {initial_report['total_tasks']}")
    print(f"   Global confidence (R₇): {initial_report['global_confidence']:.3f}")

    # Run training
    total_tasks = num_epochs * tasks_per_epoch

    # Cycle through training pairs (repeat if necessary)
    task_inputs = []
    for i in range(total_tasks):
        pair = training_pairs[i % len(training_pairs)]
        task_inputs.append(pair['input_text'])

    print(f"\n{'=' * 80}")
    print(f"🚀 STARTING EPOCH TRAINING")
    print(f"{'=' * 80}\n")

    for i, input_text in enumerate(task_inputs, 1):
        current_epoch = (i - 1) // tasks_per_epoch + 1
        task_in_epoch = ((i - 1) % tasks_per_epoch) + 1

        print(f"{'─' * 80}")
        print(f"📝 Task {i}/{total_tasks} (Epoch {current_epoch}, Task {task_in_epoch}/{tasks_per_epoch})")
        print(f"{'─' * 80}")
        print(f"Input: \"{input_text[:80]}...\"")

        # Process task through orchestrator
        task_result = orchestrator.process_task(
            input_text=input_text,
            enable_phase2=True,
            verbose=False
        )

        # Get full felt states for metrics
        # Re-process to get felt_states (orchestrator doesn't return them)
        full_result = organism.process_text(
            text=input_text,
            enable_phase2=True,
            enable_tsk_recording=False
        )

        # Record metrics
        metrics_tracker.record_task(task_result, full_result['felt_states'], organism)

        # Print quick summary
        status = "✅" if task_result.success else "❌"
        print(f"{status} Satisfaction: {task_result.satisfaction:.3f}, "
              f"Confidence: {task_result.confidence:.3f}, "
              f"V0: {task_result.v0_final:.3f}, "
              f"Cycles: {task_result.convergence_cycles}, "
              f"Family: {task_result.family_id if task_result.family_id else 'None'}")

        # Check if epoch completed
        if i % tasks_per_epoch == 0:
            # Epoch just consolidated by orchestrator
            epoch_id = i // tasks_per_epoch

            # Get epoch result from orchestrator's last consolidation
            # (already printed by orchestrator)

            # Record epoch metrics
            # Get the epoch result that was just created
            epoch_result_path = results_dir / f"epoch_{epoch_id:03d}_result.json"
            if epoch_result_path.exists():
                with open(epoch_result_path, 'r') as f:
                    epoch_data = json.load(f)

                # Convert to EpochResult-like object for metrics tracker
                from dataclasses import dataclass
                @dataclass
                class EpochResultProxy:
                    epoch_id: int
                    timestamp: str
                    task_count: int
                    success_count: int
                    success_rate: float
                    mean_satisfaction: float
                    mean_confidence: float
                    mean_v0_final: float
                    mean_convergence_cycles: float
                    families_discovered: int
                    epoch_reward: float

                epoch_result = EpochResultProxy(
                    epoch_id=epoch_data['epoch_id'],
                    timestamp=epoch_data['timestamp'],
                    task_count=epoch_data['task_count'],
                    success_count=epoch_data['success_count'],
                    success_rate=epoch_data['success_rate'],
                    mean_satisfaction=epoch_data['mean_satisfaction'],
                    mean_confidence=epoch_data['mean_confidence'],
                    mean_v0_final=epoch_data['mean_v0_final'],
                    mean_convergence_cycles=epoch_data['mean_convergence_cycles'],
                    families_discovered=epoch_data['families_discovered'],
                    epoch_reward=epoch_data['epoch_reward']
                )

                metrics_tracker.record_epoch(epoch_result, organism)

    # Final global report
    print(f"\n{'=' * 80}")
    print("📊 FINAL GLOBAL STATE")
    print(f"{'=' * 80}")

    final_report = orchestrator.get_global_report()
    print(f"\nTotal epochs completed: {final_report['total_epochs']}")
    print(f"Total tasks processed: {final_report['total_tasks']}")
    print(f"Global confidence (R₇): {final_report['global_confidence']:.3f}")

    if len(final_report['epoch_history']) > 1:
        print(f"\nEpoch History (R₆ values):")
        for i, reward in enumerate(final_report['epoch_history'], 1):
            print(f"   Epoch {i}: R₆ = {reward:.3f}")

    if final_report['compound_growth_rate'] != 0.0:
        print(f"\nCompound Growth Rate: {final_report['compound_growth_rate']:+.1%} per epoch")

    # Generate comprehensive metrics report
    print(f"\n{'=' * 80}")
    print("📈 GENERATING COMPREHENSIVE METRICS REPORT")
    print(f"{'=' * 80}")

    summary_report = metrics_tracker.get_summary_report()

    # Save comprehensive report
    comprehensive_report_path = results_dir / "comprehensive_training_report.json"
    with open(comprehensive_report_path, 'w') as f:
        json.dump(summary_report, f, indent=2)

    print(f"\n✅ Comprehensive report saved: {comprehensive_report_path}")

    # Print key findings
    print(f"\n{'=' * 80}")
    print("🔍 KEY FINDINGS")
    print(f"{'=' * 80}")

    stats = summary_report['task_level_stats']
    print(f"\n📊 Task-Level Performance:")
    print(f"   Mean satisfaction: {stats['mean_satisfaction']:.3f} ± {stats['std_satisfaction']:.3f}")
    print(f"   Mean confidence: {stats['mean_confidence']:.3f} ± {stats['std_confidence']:.3f}")
    print(f"   Mean V0 descent: {stats['mean_v0_descent']:.3f}")
    print(f"   Mean convergence cycles: {stats['mean_convergence_cycles']:.1f}")
    print(f"   Mean active organs: {stats['mean_active_organs']:.1f}/11")
    print(f"   Overall success rate: {stats['success_rate']:.1%}")

    if summary_report['r_matrix_evolution']:
        print(f"\n🔗 R-Matrix Evolution (Hebbian Coupling):")
        initial_coupling = summary_report['r_matrix_evolution'][0]['mean_coupling']
        final_coupling = summary_report['r_matrix_evolution'][-1]['mean_coupling']
        growth = ((final_coupling / initial_coupling) - 1) * 100 if initial_coupling > 0 else 0
        print(f"   Initial mean coupling: {initial_coupling:.4f}")
        print(f"   Final mean coupling: {final_coupling:.4f}")
        print(f"   Growth: {growth:+.1f}%")
        print(f"   Total updates: {summary_report['r_matrix_evolution'][-1]['total_updates']}")

    if summary_report['family_formation']:
        print(f"\n👨‍👩‍👧‍👦 Family Formation:")
        initial_families = len(summary_report['family_formation'][0]['families'])
        final_families = len(summary_report['family_formation'][-1]['families'])
        print(f"   Initial families: {initial_families}")
        print(f"   Final families: {final_families}")
        print(f"   New families discovered: {final_families - initial_families}")

    if summary_report['transduction_pathways']:
        print(f"\n🌀 Transduction Pathways (Top 5):")
        top_pathways = sorted(summary_report['transduction_pathways'].items(),
                            key=lambda x: x[1], reverse=True)[:5]
        for pathway, count in top_pathways:
            print(f"   {pathway}: {count} tasks")

    if summary_report['meta_atom_activations']:
        print(f"\n⚛️  Meta-Atom Activations (Top 5):")
        top_atoms = sorted(summary_report['meta_atom_activations'].items(),
                          key=lambda x: x[1], reverse=True)[:5]
        for atom, count in top_atoms:
            print(f"   {atom}: {count} tasks")

    print(f"\n{'=' * 80}")
    print("✅ FULL SYSTEM EPOCH TRAINING COMPLETE")
    print(f"{'=' * 80}")
    print(f"\n📁 All results saved to: {results_dir}")
    print(f"   - Global state: global_state.json")
    print(f"   - Epoch results: epoch_XXX_result.json")
    print(f"   - Comprehensive report: comprehensive_training_report.json")

    return summary_report, orchestrator, organism


if __name__ == '__main__':
    # Run 5 epochs with 10 tasks each (50 total conversations)
    summary_report, orchestrator, organism = run_full_epoch_training(
        num_epochs=5,
        tasks_per_epoch=10,
        results_dir=Path("results/epochs/full_system_training")
    )

    print(f"\n🎉 Training complete! Next: Generate detailed organism behavior report.")
