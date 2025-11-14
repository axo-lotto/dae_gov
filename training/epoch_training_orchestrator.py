#!/usr/bin/env python3
"""
Epoch Training Orchestrator
============================

Automated training across epochs with checkpoint management.
Demonstrates learning over time with comprehensive metrics tracking.

Date: November 13, 2025
Phase: C (Epoch Training + Meta-Learning Validation)
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

import json
from pathlib import Path
from typing import List, Dict, Any
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from tests.intelligence.utils.checkpoint_manager import CheckpointManager
from tests.intelligence.utils.family_loader import FamilyLoader


class EpochTrainingOrchestrator:
    """Manages multi-epoch training with checkpoints and learning metrics."""

    def __init__(
        self,
        training_corpus_path: str,
        checkpoint_dir: str = None,
        save_every_n_epochs: int = 1
    ):
        """
        Initialize epoch training orchestrator.

        Args:
            training_corpus_path: Path to training pairs JSON
            checkpoint_dir: Where to save checkpoints (default: results/checkpoints)
            save_every_n_epochs: Checkpoint frequency
        """
        self.corpus_path = Path(training_corpus_path)
        self.checkpoint_mgr = CheckpointManager(checkpoint_dir)
        self.save_every_n_epochs = save_every_n_epochs
        self.organism = ConversationalOrganismWrapper()

    def load_training_pairs(self) -> List[Dict[str, str]]:
        """Load training pairs from JSON corpus."""
        with open(self.corpus_path, 'r') as f:
            data = json.load(f)

        # Check for 'training_pairs' key
        if 'training_pairs' in data:
            # New format: training_pairs is a flat list
            return data['training_pairs']
        else:
            # Old format: categories are top-level keys
            pairs = []
            for key, value in data.items():
                if isinstance(value, list):
                    pairs.extend(value)
            return pairs

    def train_epoch(
        self,
        epoch_num: int,
        training_pairs: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Train for one epoch and return metrics.

        Args:
            epoch_num: Current epoch number
            training_pairs: List of training pairs to process

        Returns:
            Dict of epoch metrics
        """
        print(f"\n{'='*80}")
        print(f"EPOCH {epoch_num} TRAINING")
        print('='*80)

        confidences = []
        nexus_counts = []
        processing_times = []
        v0_energies = []
        v0_cycles = []

        for i, pair in enumerate(training_pairs, 1):
            # Handle both 'input', 'INPUT', and 'input_text' keys
            input_text = pair.get('input') or pair.get('INPUT') or pair.get('input_text')
            if not input_text:
                print(f"   ⚠️  Skipping pair {i}: no input text found")
                continue

            result = self.organism.process_text(
                input_text,
                enable_phase2=True,
                enable_tsk_recording=True
            )

            # Collect metrics
            confidences.append(result.get('emission_confidence', 0.0))
            nexus_counts.append(result.get('emission_nexus_count', 0))

            felt_states = result.get('felt_states', {})
            processing_times.append(felt_states.get('processing_time_ms', 0))

            v0_energy = felt_states.get('v0_energy', {})
            if v0_energy:
                v0_energies.append(v0_energy.get('final_energy', 0.0))
                v0_cycles.append(v0_energy.get('cycles', 0))

            if i % 10 == 0:
                print(f"   Processed {i}/{len(training_pairs)} pairs...")

        # Compute epoch metrics
        metrics = {
            'epoch': epoch_num,
            'pairs_trained': len(training_pairs),
            'mean_confidence': sum(confidences) / len(confidences) if confidences else 0.0,
            'mean_nexus_count': sum(nexus_counts) / len(nexus_counts) if nexus_counts else 0.0,
            'mean_processing_time': sum(processing_times) / len(processing_times) if processing_times else 0.0,
            'mean_v0_energy': sum(v0_energies) / len(v0_energies) if v0_energies else 0.0,
            'mean_v0_cycles': sum(v0_cycles) / len(v0_cycles) if v0_cycles else 0.0,
        }

        print(f"\n📊 Epoch {epoch_num} Metrics:")
        print(f"   Mean confidence: {metrics['mean_confidence']:.3f}")
        print(f"   Mean nexuses: {metrics['mean_nexus_count']:.1f}")
        print(f"   Mean V0 energy: {metrics['mean_v0_energy']:.3f}")
        print(f"   Mean V0 cycles: {metrics['mean_v0_cycles']:.1f}")
        print(f"   Mean processing: {metrics['mean_processing_time']:.1f}ms")

        return metrics

    def save_checkpoint(self, epoch_num: int, metrics: Dict[str, Any]):
        """
        Save organism state checkpoint.

        Args:
            epoch_num: Current epoch
            metrics: Epoch metrics
        """
        # Get current organism state
        family_loader = FamilyLoader()
        family_loader.reload()  # Reload from disk

        organism_state = {
            'organic_families': family_loader.families,
            'family_count': len(family_loader.families),
            'epoch': epoch_num,
            'metrics': metrics
        }

        checkpoint_path = self.checkpoint_mgr.save_checkpoint(
            epoch=epoch_num,
            organism_state=organism_state,
            metadata=metrics
        )

        print(f"   ✅ Checkpoint saved: {Path(checkpoint_path).name}")

    def run_training(
        self,
        total_epochs: int,
        pairs_per_epoch: int = None
    ) -> List[Dict[str, Any]]:
        """
        Run full training sequence.

        Args:
            total_epochs: Number of epochs to train
            pairs_per_epoch: Limit pairs per epoch (None = use all)

        Returns:
            List of epoch metrics
        """
        print(f"\n{'='*80}")
        print(f"STARTING {total_epochs}-EPOCH TRAINING SEQUENCE")
        print('='*80)

        # Load training pairs
        all_pairs = self.load_training_pairs()
        print(f"Loaded {len(all_pairs)} training pairs")

        if pairs_per_epoch:
            all_pairs = all_pairs[:pairs_per_epoch]
            print(f"Using {len(all_pairs)} pairs per epoch")

        epoch_metrics = []

        for epoch in range(1, total_epochs + 1):
            # Train epoch
            metrics = self.train_epoch(epoch, all_pairs)
            epoch_metrics.append(metrics)

            # Save checkpoint
            if epoch % self.save_every_n_epochs == 0:
                self.save_checkpoint(epoch, metrics)

        # Final summary
        self._print_training_summary(epoch_metrics)

        return epoch_metrics

    def _print_training_summary(self, epoch_metrics: List[Dict[str, Any]]):
        """Print comprehensive training summary."""
        print(f"\n{'='*80}")
        print("TRAINING SEQUENCE COMPLETE")
        print('='*80)

        first = epoch_metrics[0]
        last = epoch_metrics[-1]

        # Confidence trajectory
        conf_change = last['mean_confidence'] - first['mean_confidence']
        print(f"\n📈 Confidence Trajectory:")
        print(f"   Epoch 1:  {first['mean_confidence']:.3f}")
        print(f"   Epoch {len(epoch_metrics)}: {last['mean_confidence']:.3f}")
        print(f"   Change:   {conf_change:+.3f}")

        # Nexus formation trajectory
        nexus_change = last['mean_nexus_count'] - first['mean_nexus_count']
        print(f"\n🔗 Nexus Formation Trajectory:")
        print(f"   Epoch 1:  {first['mean_nexus_count']:.1f}")
        print(f"   Epoch {len(epoch_metrics)}: {last['mean_nexus_count']:.1f}")
        print(f"   Change:   {nexus_change:+.1f}")

        # V0 convergence efficiency
        if 'mean_v0_energy' in first and 'mean_v0_energy' in last:
            energy_change = last['mean_v0_energy'] - first['mean_v0_energy']
            print(f"\n⚡ V0 Convergence Efficiency:")
            print(f"   Epoch 1 energy:  {first['mean_v0_energy']:.3f}")
            print(f"   Epoch {len(epoch_metrics)} energy: {last['mean_v0_energy']:.3f}")
            print(f"   Change:          {energy_change:+.3f}")
            if energy_change < 0:
                print(f"   ✅ Improved convergence (lower final energy)")

        # Learning assessment
        print(f"\n🧠 Learning Assessment:")
        if conf_change > 0.05:
            print(f"   ✅ LEARNING DETECTED: Confidence improved by {conf_change:.3f}")
        elif conf_change > 0.01:
            print(f"   ⚠️  MARGINAL LEARNING: Confidence improved by {conf_change:.3f}")
        else:
            print(f"   ⚠️  LIMITED LEARNING: Confidence change {conf_change:+.3f}")

        print('='*80)


def main():
    """Main entry point for epoch training."""
    import argparse

    parser = argparse.ArgumentParser(description="Epoch training orchestrator")
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs')
    parser.add_argument('--pairs', type=int, default=None, help='Pairs per epoch (None = all)')
    parser.add_argument('--corpus', type=str,
                       default='/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/conversational_training_pairs.json',
                       help='Training corpus path')

    args = parser.parse_args()

    orchestrator = EpochTrainingOrchestrator(
        training_corpus_path=args.corpus,
        save_every_n_epochs=1
    )

    epoch_metrics = orchestrator.run_training(
        total_epochs=args.epochs,
        pairs_per_epoch=args.pairs
    )

    # Save metrics to file
    metrics_path = Path('/Users/daedalea/Desktop/DAE_HYPHAE_1/results/epochs') / f"training_epochs_{args.epochs}.json"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    with open(metrics_path, 'w') as f:
        json.dump(epoch_metrics, f, indent=2)

    print(f"\n📊 Metrics saved: {metrics_path}")


if __name__ == '__main__':
    main()
