#!/usr/bin/env python3
"""
Adaptive Threshold Manager - Prevent Learning Plateaus
======================================================

Dynamically adjusts thresholds to prevent plateaus and enable continuous learning.
Based on signal collection emission strategy.

Created: November 3, 2025
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any


class AdaptiveThresholdManager:
    """
    Manage thresholds adaptively to prevent plateaus.

    Key insight: When accuracy plateaus, we need to:
    1. Lower confidence thresholds to accept more patterns
    2. Increase learning rates to escape local minima
    3. Adjust reconstruction thresholds based on task family
    """

    def __init__(self):
        """Initialize adaptive threshold manager."""

        # Base thresholds (will be adapted)
        self.thresholds = {
            # Learning thresholds
            'convergence_threshold': 0.01,  # For detecting plateaus
            'hebbian_confidence': 0.3,      # For pattern storage
            'pattern_confidence': 0.5,       # For pattern recall

            # Reconstruction thresholds
            'intersection_threshold': 0.5,   # For nexus formation
            'coherence_threshold': 0.3,      # For organ agreement
            'min_confidence': 0.3,           # For value emission

            # Task-specific multipliers
            'value_task_multiplier': 1.0,
            'spatial_task_multiplier': 0.8,  # More lenient for spatial
            'pattern_task_multiplier': 0.6   # Most lenient for patterns
        }

        # Adaptation parameters
        self.plateau_history = []
        self.accuracy_history = []
        self.adaptation_rate = 0.1  # How much to adjust per plateau

        print("🎯 AdaptiveThresholdManager initialized")
        print(f"   Base thresholds: {len(self.thresholds)} parameters")

    def detect_plateau(self, accuracies: List[float], window: int = 3) -> bool:
        """
        Detect if learning has plateaued.

        Plateau = no improvement over last N iterations.
        """
        if len(accuracies) < window:
            return False

        recent = accuracies[-window:]
        variance = np.var(recent)

        # Plateau if variance is very low
        is_plateau = variance < 0.0001

        if is_plateau:
            self.plateau_history.append(len(accuracies))

        return is_plateau

    def adapt_thresholds(self,
                         current_accuracy: float,
                         task_type: str,
                         iteration: int) -> Dict[str, float]:
        """
        Adapt thresholds based on current performance.

        Lower thresholds when:
        - Accuracy is plateaued
        - Task type is difficult (pattern/spatial)
        - Many iterations without improvement
        """

        adapted = self.thresholds.copy()

        # Task-specific adaptation
        if task_type == 'pattern':
            multiplier = self.thresholds['pattern_task_multiplier']
        elif task_type == 'spatial':
            multiplier = self.thresholds['spatial_task_multiplier']
        else:  # value
            multiplier = self.thresholds['value_task_multiplier']

        # Apply task multiplier
        adapted['hebbian_confidence'] *= multiplier
        adapted['pattern_confidence'] *= multiplier
        adapted['min_confidence'] *= multiplier
        adapted['coherence_threshold'] *= multiplier

        # Plateau adaptation
        if len(self.plateau_history) > 0:
            plateau_count = len(self.plateau_history)

            # Progressive relaxation based on plateau count
            relaxation = 1.0 - (self.adaptation_rate * plateau_count)
            relaxation = max(0.1, relaxation)  # Don't go below 0.1

            # Relax thresholds
            adapted['hebbian_confidence'] *= relaxation
            adapted['pattern_confidence'] *= relaxation
            adapted['intersection_threshold'] *= relaxation
            adapted['coherence_threshold'] *= relaxation

            # Increase convergence threshold to detect smaller changes
            adapted['convergence_threshold'] *= (1 + plateau_count * 0.5)

            print(f"   🔧 Adapted thresholds (plateau #{plateau_count}):")
            print(f"      Hebbian confidence: {adapted['hebbian_confidence']:.3f}")
            print(f"      Pattern confidence: {adapted['pattern_confidence']:.3f}")
            print(f"      Convergence threshold: {adapted['convergence_threshold']:.3f}")

        # Performance-based adaptation
        if current_accuracy < 0.5:
            # Poor performance - be more permissive
            adapted['hebbian_confidence'] *= 0.5
            adapted['min_confidence'] *= 0.5
            print(f"   📉 Low accuracy - relaxing thresholds by 50%")
        elif current_accuracy > 0.9:
            # Good performance - can be more selective
            adapted['hebbian_confidence'] = min(0.8, adapted['hebbian_confidence'] * 1.2)
            adapted['min_confidence'] = min(0.8, adapted['min_confidence'] * 1.2)
            print(f"   📈 High accuracy - tightening thresholds slightly")

        # Iteration-based adaptation
        if iteration > 10 and current_accuracy < 0.7:
            # Many iterations without good accuracy - be aggressive
            adapted['hebbian_confidence'] *= 0.3
            adapted['pattern_confidence'] *= 0.3
            adapted['convergence_threshold'] *= 2.0
            print(f"   ⚡ Aggressive mode - very low thresholds")

        return adapted

    def get_family_thresholds(self, family_id: str) -> Dict[str, float]:
        """
        Get family-specific thresholds.

        Different families need different thresholds.
        """

        # Map family to task type (simplified)
        if 'value' in family_id.lower() or 'color' in family_id.lower():
            task_type = 'value'
        elif 'pattern' in family_id.lower() or 'extract' in family_id.lower():
            task_type = 'pattern'
        else:
            task_type = 'spatial'

        return self.adapt_thresholds(
            current_accuracy=0.5,  # Default
            task_type=task_type,
            iteration=0
        )

    def update_history(self, accuracy: float):
        """Update accuracy history for plateau detection."""
        self.accuracy_history.append(accuracy)

        # Keep only recent history
        if len(self.accuracy_history) > 20:
            self.accuracy_history = self.accuracy_history[-20:]

    def reset_for_task(self):
        """Reset adaptation for new task."""
        self.plateau_history = []
        self.accuracy_history = []

    def get_learning_rate(self, base_rate: float, iteration: int) -> float:
        """
        Get adaptive learning rate.

        Increase rate when plateaued, decrease when improving.
        """

        # Base adaptation
        rate = base_rate

        # Plateau boost
        if len(self.plateau_history) > 0:
            plateau_boost = 1.5 ** len(self.plateau_history)
            rate *= plateau_boost

        # Iteration decay (but not too much)
        decay = 1.0 / (1.0 + iteration * 0.01)
        rate *= decay

        # Keep in reasonable range
        rate = max(0.01, min(1.0, rate))

        return rate

    def get_status(self) -> Dict:
        """Get current adaptation status."""
        return {
            'plateau_count': len(self.plateau_history),
            'accuracy_history': self.accuracy_history[-5:] if self.accuracy_history else [],
            'current_thresholds': self.thresholds,
            'is_adapted': len(self.plateau_history) > 0
        }