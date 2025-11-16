"""
Minimal Epoch Coordinator - Pragmatic Epoch Learning Infrastructure
===================================================================

Lightweight epoch coordination layer that leverages existing POST-EMISSION hooks
in the organism wrapper. No refactoring required - just adds epoch boundaries
and state persistence.

Key Design Principles:
- Thin wrapper around organism processing (< 250 lines)
- Leverages existing learning components (Phase 5, organ confidence, etc.)
- No changes to organism wrapper or learning components
- Clean state persistence (resume training anytime)
- Progressive learning across epochs

Created: November 15, 2025
Status: Pragmatic solution for epoch-structured training
"""

import os
import json
import time
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class MinimalEpochCoordinator:
    """
    Lightweight epoch coordination without regime complexity.

    Leverages existing POST-EMISSION hooks in organism wrapper:
    - Phase 5 transformation learning (line 2252-2302)
    - Organ confidence updates (line 774-815)
    - Entity-organ tracking (line 806-815)

    What This Adds:
    - Epoch boundary detection
    - Epoch-level state persistence
    - Progressive learning accumulation
    - Epoch statistics aggregation

    What This Doesn't Add:
    - Regime-based training (too complex)
    - Felt-difference learning (deferred)
    - Curriculum learning (Phase 2)
    - Epoch-end consolidation (Phase 2)
    """

    def __init__(
        self,
        organism_wrapper,
        state_dir: str = 'persona_layer/state/active',
        enable_auto_save: bool = True
    ):
        """
        Initialize epoch coordinator.

        Args:
            organism_wrapper: ConversationalOrganismWrapper instance
            state_dir: Directory for epoch state persistence
            enable_auto_save: Auto-save epoch state after each epoch
        """
        self.organism = organism_wrapper
        self.state_dir = Path(state_dir)
        self.enable_auto_save = enable_auto_save

        # Epoch state
        self.current_epoch = 0
        self.total_epochs = 0
        self.epoch_history = []

        # Ensure state directory exists
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # Load existing epoch state (resume training)
        self._load_epoch_state()

        print(f"✅ MinimalEpochCoordinator initialized")
        print(f"   State directory: {self.state_dir}")
        print(f"   Current epoch: {self.current_epoch}")
        print(f"   Epoch history: {len(self.epoch_history)} epochs")

    def run_epoch(
        self,
        training_pairs: List[Dict],
        epoch_id: int,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run single epoch with automatic learning.

        Existing POST-EMISSION hooks fire automatically:
        - Phase 5 transformation learning
        - Organ confidence updates
        - Entity-organ tracking

        Args:
            training_pairs: List of {id, input_text, expected_output} dicts
            epoch_id: Epoch number (1-indexed)
            verbose: Print progress messages

        Returns:
            Epoch statistics dict
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"EPOCH {epoch_id}/{self.total_epochs}")
            print(f"{'='*80}\n")

        epoch_start = time.time()
        results = []
        families_discovered = set()

        for i, pair in enumerate(training_pairs, 1):
            if verbose:
                print(f"[{i}/{len(training_pairs)}] {pair.get('id', f'pair_{i}')}", end="")

            # Process through organism (existing learning hooks fire)
            result = self.organism.process_text(
                pair['input_text'],
                context={
                    'epoch_id': epoch_id,
                    'pair_id': pair.get('id', f'pair_{i}'),
                    'conversation_id': f"epoch{epoch_id}_{pair.get('id', f'pair_{i}')}"
                }
            )
            results.append(result)

            # Track family assignments
            family_id = result.get('felt_states', {}).get('phase5_family_id')
            if family_id:
                families_discovered.add(family_id)
                if verbose:
                    family_sim = result.get('felt_states', {}).get('phase5_similarity', 0.0)
                    is_new = result.get('felt_states', {}).get('phase5_is_new', False)
                    action = "CREATED" if is_new else "JOINED"
                    print(f" → {action} {family_id} (sim: {family_sim:.3f})")
            else:
                if verbose:
                    print(f" → No family assigned")

        # Epoch-end: Aggregate stats
        epoch_stats = self._aggregate_epoch_stats(results, epoch_id)
        epoch_stats['duration'] = time.time() - epoch_start
        epoch_stats['families_discovered_this_epoch'] = len(families_discovered)

        # Update state
        self.current_epoch = epoch_id
        self.epoch_history.append(epoch_stats)

        # Auto-save
        if self.enable_auto_save:
            self._save_epoch_state()

        # Print summary
        if verbose:
            self._print_epoch_summary(epoch_stats)

        return epoch_stats

    def run_training(
        self,
        training_pairs: List[Dict],
        num_epochs: int,
        verbose: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Run multi-epoch training with progressive learning.

        Args:
            training_pairs: Training data
            num_epochs: Number of epochs to run
            verbose: Print progress

        Returns:
            List of epoch statistics (one per epoch)
        """
        self.total_epochs = num_epochs
        epoch_results = []

        for epoch_id in range(1, num_epochs + 1):
            epoch_stats = self.run_epoch(training_pairs, epoch_id, verbose)
            epoch_results.append(epoch_stats)

        if verbose:
            self._print_training_summary(epoch_results)

        return epoch_results

    def _aggregate_epoch_stats(
        self,
        results: List[Dict],
        epoch_id: int
    ) -> Dict[str, Any]:
        """
        Aggregate statistics from all conversations in epoch.

        Args:
            results: List of organism processing results
            epoch_id: Current epoch number

        Returns:
            Aggregated statistics dict
        """
        # Extract values with fallbacks
        confidences = [r.get('confidence', 0.0) for r in results]
        v0_finals = [r.get('felt_states', {}).get('v0_energy_final', 1.0) for r in results]
        satisfactions = [r.get('felt_states', {}).get('satisfaction_final', 0.5) for r in results]

        # Get unique families assigned in this epoch
        families_assigned = [
            r.get('felt_states', {}).get('phase5_family_id')
            for r in results
            if r.get('felt_states', {}).get('phase5_family_id')
        ]
        unique_families = set(families_assigned)

        return {
            'epoch_id': epoch_id,
            'total_conversations': len(results),
            'mean_confidence': float(np.mean(confidences)) if confidences else 0.0,
            'mean_v0_final': float(np.mean(v0_finals)) if v0_finals else 1.0,
            'mean_satisfaction': float(np.mean(satisfactions)) if satisfactions else 0.5,
            'families_assigned_count': len(families_assigned),
            'unique_families_this_epoch': len(unique_families),
            'timestamp': datetime.now().isoformat()
        }

    def _print_epoch_summary(self, stats: Dict[str, Any]):
        """Print epoch summary statistics."""
        print(f"\n{'─'*80}")
        print(f"📊 EPOCH {stats['epoch_id']} SUMMARY")
        print(f"{'─'*80}")
        print(f"   Total conversations: {stats['total_conversations']}")
        print(f"   Mean confidence: {stats['mean_confidence']:.3f}")
        print(f"   Mean V0 final: {stats['mean_v0_final']:.3f}")
        print(f"   Mean satisfaction: {stats['mean_satisfaction']:.3f}")
        print(f"   Families assigned: {stats['families_assigned_count']}/{stats['total_conversations']}")
        print(f"   Unique families: {stats['unique_families_this_epoch']}")
        print(f"   Duration: {stats['duration']:.1f}s")
        print(f"{'─'*80}\n")

    def _print_training_summary(self, epoch_results: List[Dict]):
        """Print overall training summary."""
        print(f"\n{'='*80}")
        print(f"🎯 TRAINING COMPLETE - {len(epoch_results)} EPOCHS")
        print(f"{'='*80}\n")

        print("Epoch Progress:")
        print(f"{'Epoch':<8} {'Confidence':<12} {'Satisfaction':<14} {'V0 Final':<10} {'Families':<10}")
        print(f"{'-'*8} {'-'*12} {'-'*14} {'-'*10} {'-'*10}")

        for stats in epoch_results:
            print(f"{stats['epoch_id']:<8} "
                  f"{stats['mean_confidence']:<12.3f} "
                  f"{stats['mean_satisfaction']:<14.3f} "
                  f"{stats['mean_v0_final']:<10.3f} "
                  f"{stats['unique_families_this_epoch']:<10}")

        print(f"\n{'='*80}\n")

    def _save_epoch_state(self):
        """Persist epoch state to JSON for resumable training."""
        state = {
            'current_epoch': self.current_epoch,
            'total_epochs': self.total_epochs,
            'epoch_history': self.epoch_history,
            'total_conversations': sum(e['total_conversations'] for e in self.epoch_history),
            'last_updated': datetime.now().isoformat()
        }

        state_path = self.state_dir / 'epoch_state.json'

        # Backup existing state
        if state_path.exists():
            backup_path = self.state_dir / f'epoch_state_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            state_path.rename(backup_path)

        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)

    def _load_epoch_state(self):
        """Load epoch state from JSON (resume training)."""
        state_path = self.state_dir / 'epoch_state.json'

        if not state_path.exists():
            return

        try:
            with open(state_path) as f:
                state = json.load(f)

            self.current_epoch = state.get('current_epoch', 0)
            self.total_epochs = state.get('total_epochs', 0)
            self.epoch_history = state.get('epoch_history', [])

            print(f"📂 Loaded existing epoch state:")
            print(f"   Current epoch: {self.current_epoch}")
            print(f"   Total conversations: {state.get('total_conversations', 0)}")

        except Exception as e:
            print(f"⚠️  Failed to load epoch state: {e}")
            print(f"   Starting fresh")

    def get_progress_summary(self) -> Dict[str, Any]:
        """
        Get summary of training progress across all epochs.

        Returns:
            Progress summary dict
        """
        if not self.epoch_history:
            return {
                'epochs_completed': 0,
                'total_conversations': 0,
                'mean_confidence_trend': [],
                'families_trend': []
            }

        return {
            'epochs_completed': len(self.epoch_history),
            'total_conversations': sum(e['total_conversations'] for e in self.epoch_history),
            'mean_confidence_trend': [e['mean_confidence'] for e in self.epoch_history],
            'mean_satisfaction_trend': [e['mean_satisfaction'] for e in self.epoch_history],
            'families_trend': [e['unique_families_this_epoch'] for e in self.epoch_history],
            'latest_epoch': self.epoch_history[-1] if self.epoch_history else None
        }

    def save_training_history(self, output_path: str):
        """
        Save complete training history to JSON.

        Args:
            output_path: Path to save training history JSON
        """
        history = {
            'coordinator_type': 'MinimalEpochCoordinator',
            'epochs_completed': len(self.epoch_history),
            'total_conversations': sum(e['total_conversations'] for e in self.epoch_history),
            'epoch_history': self.epoch_history,
            'progress_summary': self.get_progress_summary(),
            'saved_at': datetime.now().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(history, f, indent=2)

        print(f"💾 Training history saved to: {output_path}")
