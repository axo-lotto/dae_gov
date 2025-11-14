#!/usr/bin/env python3
"""
Organism Checkpoint Manager
============================

Save and load organism state for epoch-based intelligence testing.

Enables:
- Snapshot organism state at specific epochs
- Load organism from checkpoint
- Compare states across epochs

Date: November 13, 2025
Phase: Intelligence Test Refactoring (Phase 1)
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class CheckpointManager:
    """Manages organism state checkpoints for intelligence testing."""

    def __init__(self, checkpoint_dir: str = None):
        """
        Initialize checkpoint manager.

        Args:
            checkpoint_dir: Directory to store checkpoints
                           (default: results/checkpoints/)
        """
        if checkpoint_dir is None:
            checkpoint_dir = '/Users/daedalea/Desktop/DAE_HYPHAE_1/results/checkpoints'

        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # Save Organism State
    # =========================================================================

    def save_checkpoint(
        self,
        epoch: int,
        organism_state: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save organism state to checkpoint.

        Args:
            epoch: Epoch number
            organism_state: Dictionary containing organism state:
                - 'organic_families': family clustering state
                - 'hebbian_memory': conversational memory
                - 'organ_weights': learned organ importance
                - 'meta_atom_activations': shared meta-atom state
                - Any other organism-specific state
            metadata: Optional metadata (training config, performance metrics)

        Returns:
            Path to saved checkpoint file

        Example:
            >>> manager = CheckpointManager()
            >>> state = {
            ...     'organic_families': {...},
            ...     'hebbian_memory': {...},
            ...     'epoch': 10,
            ...     'performance': {'confidence': 0.65}
            ... }
            >>> path = manager.save_checkpoint(10, state)
            >>> print(f"Saved to: {path}")
        """
        checkpoint = {
            'epoch': epoch,
            'timestamp': datetime.now().isoformat(),
            'organism_state': organism_state,
            'metadata': metadata or {}
        }

        # Filename: checkpoint_epoch_10_20251113_123045.json
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"checkpoint_epoch_{epoch}_{timestamp}.json"
        filepath = self.checkpoint_dir / filename

        # Save to file
        with open(filepath, 'w') as f:
            json.dump(checkpoint, f, indent=2)

        print(f"✅ Checkpoint saved: {filepath}")
        return str(filepath)

    # =========================================================================
    # Load Organism State
    # =========================================================================

    def load_checkpoint(
        self,
        epoch: int = None,
        checkpoint_path: str = None
    ) -> Dict[str, Any]:
        """
        Load organism state from checkpoint.

        Args:
            epoch: Epoch number to load (loads most recent checkpoint for that epoch)
            checkpoint_path: Explicit path to checkpoint file (overrides epoch)

        Returns:
            Dictionary with checkpoint data:
                - 'epoch': int
                - 'timestamp': str
                - 'organism_state': Dict
                - 'metadata': Dict

        Example:
            >>> manager = CheckpointManager()
            >>> checkpoint = manager.load_checkpoint(epoch=10)
            >>> state = checkpoint['organism_state']
            >>> families = state['organic_families']
        """
        if checkpoint_path is not None:
            # Load explicit checkpoint
            filepath = Path(checkpoint_path)
        elif epoch is not None:
            # Find most recent checkpoint for epoch
            filepath = self._find_latest_checkpoint(epoch)
        else:
            raise ValueError("Must provide either epoch or checkpoint_path")

        if not filepath.exists():
            raise FileNotFoundError(f"Checkpoint not found: {filepath}")

        # Load from file
        with open(filepath, 'r') as f:
            checkpoint = json.load(f)

        print(f"✅ Checkpoint loaded: {filepath}")
        return checkpoint

    def _find_latest_checkpoint(self, epoch: int) -> Path:
        """Find most recent checkpoint file for given epoch."""
        pattern = f"checkpoint_epoch_{epoch}_*.json"
        matching = sorted(self.checkpoint_dir.glob(pattern))

        if not matching:
            raise FileNotFoundError(
                f"No checkpoint found for epoch {epoch} in {self.checkpoint_dir}"
            )

        # Return most recent (last in sorted list)
        return matching[-1]

    # =========================================================================
    # List Available Checkpoints
    # =========================================================================

    def list_checkpoints(self) -> Dict[int, list]:
        """
        List all available checkpoints grouped by epoch.

        Returns:
            Dictionary mapping epoch → list of checkpoint paths

        Example:
            >>> manager = CheckpointManager()
            >>> checkpoints = manager.list_checkpoints()
            >>> print(checkpoints)
            {
                1: ['checkpoint_epoch_1_20251113_120000.json'],
                5: ['checkpoint_epoch_5_20251113_130000.json'],
                10: ['checkpoint_epoch_10_20251113_140000.json']
            }
        """
        checkpoints = {}

        for filepath in sorted(self.checkpoint_dir.glob("checkpoint_epoch_*.json")):
            # Extract epoch from filename
            parts = filepath.stem.split('_')
            epoch = int(parts[2])

            if epoch not in checkpoints:
                checkpoints[epoch] = []

            checkpoints[epoch].append(str(filepath))

        return checkpoints

    # =========================================================================
    # Epoch Comparison
    # =========================================================================

    def compare_epochs(
        self,
        epoch_1: int,
        epoch_2: int
    ) -> Dict[str, Any]:
        """
        Compare organism state between two epochs.

        Args:
            epoch_1: First epoch
            epoch_2: Second epoch

        Returns:
            Dictionary with comparison metrics:
                - 'epoch_1': int
                - 'epoch_2': int
                - 'family_count_change': int
                - 'confidence_change': float (if available in metadata)
                - 'state_1': Dict (organism state at epoch 1)
                - 'state_2': Dict (organism state at epoch 2)

        Example:
            >>> manager = CheckpointManager()
            >>> comparison = manager.compare_epochs(1, 10)
            >>> print(f"Family growth: {comparison['family_count_change']}")
            Family growth: +5 families
        """
        checkpoint_1 = self.load_checkpoint(epoch=epoch_1)
        checkpoint_2 = self.load_checkpoint(epoch=epoch_2)

        state_1 = checkpoint_1['organism_state']
        state_2 = checkpoint_2['organism_state']

        # Extract family counts (if available)
        families_1 = state_1.get('organic_families', {})
        families_2 = state_2.get('organic_families', {})

        # Count mature families (has 'centroid' key)
        mature_count_1 = sum(
            1 for family in families_1.values()
            if isinstance(family, dict) and 'centroid' in family
        )
        mature_count_2 = sum(
            1 for family in families_2.values()
            if isinstance(family, dict) and 'centroid' in family
        )

        family_count_change = mature_count_2 - mature_count_1

        # Extract confidence (if in metadata)
        conf_1 = checkpoint_1.get('metadata', {}).get('mean_confidence', None)
        conf_2 = checkpoint_2.get('metadata', {}).get('mean_confidence', None)

        confidence_change = None
        if conf_1 is not None and conf_2 is not None:
            confidence_change = conf_2 - conf_1

        comparison = {
            'epoch_1': epoch_1,
            'epoch_2': epoch_2,
            'family_count_1': mature_count_1,
            'family_count_2': mature_count_2,
            'family_count_change': family_count_change,
            'confidence_1': conf_1,
            'confidence_2': conf_2,
            'confidence_change': confidence_change,
            'state_1': state_1,
            'state_2': state_2
        }

        return comparison


# =============================================================================
# Self-Test
# =============================================================================

def self_test():
    """Self-test for checkpoint manager."""
    print("=" * 80)
    print("💾 TESTING CHECKPOINT MANAGER")
    print("=" * 80)

    # Use temporary test directory
    test_dir = '/Users/daedalea/Desktop/DAE_HYPHAE_1/results/checkpoints_test'
    manager = CheckpointManager(checkpoint_dir=test_dir)

    # Test 1: Save checkpoint
    print("\n" + "-" * 80)
    print("Test 1: Save Checkpoint")
    print("-" * 80)

    state_epoch_1 = {
        'organic_families': {
            'family_0': {
                'centroid': [0.1] * 57,
                'members': ['conv_1', 'conv_2']
            }
        },
        'hebbian_memory': {'some': 'data'},
        'performance': {'confidence': 0.45}
    }

    metadata_1 = {
        'training_pairs': 10,
        'mean_confidence': 0.45
    }

    path_1 = manager.save_checkpoint(1, state_epoch_1, metadata_1)
    assert os.path.exists(path_1), "Checkpoint file should exist"
    print(f"✅ Checkpoint saved successfully")

    # Test 2: Save another checkpoint (epoch 5)
    print("\n" + "-" * 80)
    print("Test 2: Save Second Checkpoint (Epoch 5)")
    print("-" * 80)

    state_epoch_5 = {
        'organic_families': {
            'family_0': {
                'centroid': [0.1] * 57,
                'members': ['conv_1', 'conv_2', 'conv_3']
            },
            'family_1': {
                'centroid': [0.2] * 57,
                'members': ['conv_4', 'conv_5']
            }
        },
        'hebbian_memory': {'more': 'data'},
        'performance': {'confidence': 0.62}
    }

    metadata_5 = {
        'training_pairs': 50,
        'mean_confidence': 0.62
    }

    path_5 = manager.save_checkpoint(5, state_epoch_5, metadata_5)
    assert os.path.exists(path_5), "Second checkpoint file should exist"
    print(f"✅ Second checkpoint saved successfully")

    # Test 3: Load checkpoint
    print("\n" + "-" * 80)
    print("Test 3: Load Checkpoint")
    print("-" * 80)

    loaded = manager.load_checkpoint(epoch=1)
    assert loaded['epoch'] == 1, "Epoch should be 1"
    assert 'organic_families' in loaded['organism_state'], "State should contain families"
    print(f"✅ Checkpoint loaded successfully")
    print(f"   Epoch: {loaded['epoch']}")
    print(f"   Timestamp: {loaded['timestamp']}")
    print(f"   Families: {len(loaded['organism_state']['organic_families'])}")

    # Test 4: List checkpoints
    print("\n" + "-" * 80)
    print("Test 4: List Checkpoints")
    print("-" * 80)

    checkpoints = manager.list_checkpoints()
    print(f"Available checkpoints: {list(checkpoints.keys())}")
    assert 1 in checkpoints, "Epoch 1 should be in list"
    assert 5 in checkpoints, "Epoch 5 should be in list"
    print(f"✅ Checkpoint listing working correctly")

    # Test 5: Compare epochs
    print("\n" + "-" * 80)
    print("Test 5: Compare Epochs")
    print("-" * 80)

    comparison = manager.compare_epochs(1, 5)
    print(f"Epoch 1 → Epoch 5:")
    print(f"   Families: {comparison['family_count_1']} → {comparison['family_count_2']}")
    print(f"   Family growth: {comparison['family_count_change']}")
    print(f"   Confidence: {comparison['confidence_1']:.3f} → {comparison['confidence_2']:.3f}")
    print(f"   Confidence change: {comparison['confidence_change']:.3f}")

    assert comparison['family_count_change'] == 1, "Should have 1 new family"
    assert comparison['confidence_change'] > 0.1, "Confidence should improve"
    print(f"✅ Epoch comparison working correctly")

    # Cleanup
    print("\n" + "-" * 80)
    print("Cleanup: Removing test checkpoints")
    print("-" * 80)
    import shutil
    shutil.rmtree(test_dir)
    print("✅ Test directory removed")

    # Summary
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED - Checkpoint Manager Ready")
    print("=" * 80)


if __name__ == '__main__':
    self_test()
