"""
Organ Confidence Tracker - Level 2 Fractal Reward Propagation
==============================================================

Implements DAE 3.0's proven Level 2 fractal reward mechanism:
Per-organ confidence tracking based on participation in successful emissions.

Philosophy (DAE 3.0):
- Organs that consistently contribute to successful outcomes gain higher weights
- Poor-performing organs are dampened (defensive degradation)
- Enables organic self-optimization over epochs
- Part of 7-level fractal reward propagation

Integration Point:
- Called POST-EMISSION by conversational_organism_wrapper
- Updates per-organ confidence based on:
  * Organ participated (was active)
  * Emission was successful (user satisfaction ≥ threshold)
- Confidence affects organ weight multipliers in future processing

Date: November 15, 2025
Status: Legacy Integration (DAE 3.0 → HYPHAE_1)
"""

import json
import numpy as np
from typing import Dict, Optional, List
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class OrganConfidenceMetrics:
    """Per-organ performance metrics over time"""
    organ_name: str
    confidence: float  # EMA confidence [0.0, 1.0]
    success_count: int  # Total successful participations
    failure_count: int  # Total failed participations
    total_participations: int  # success + failure
    success_rate: float  # success / total

    # Weight multiplier for future processing
    weight_multiplier: float  # Range: [0.8, 1.2]

    # Temporal tracking
    last_updated: str  # ISO timestamp
    first_seen: str  # ISO timestamp


class OrganConfidenceTracker:
    """
    Track per-organ confidence evolution (DAE 3.0 Level 2).

    Strategy:
    1. Each organ starts with neutral confidence (0.5)
    2. After each emission:
       - IF organ participated AND emission successful → boost confidence
       - IF organ participated AND emission failed → lower confidence
       - IF organ did NOT participate → no change
    3. Confidence affects weight multiplier:
       - High confidence (0.8-1.0) → multiplier 1.08-1.2 (boost)
       - Medium confidence (0.4-0.7) → multiplier 0.96-1.08 (neutral)
       - Low confidence (0.0-0.3) → multiplier 0.8-0.96 (dampen)

    Expected Benefits (from DAE 3.0):
    - Organs self-optimize over 50-100 epochs
    - Poor organs dampened (not eliminated - defensive)
    - System learns which organs work best for different contexts
    - Improves family formation (different organ patterns → different families)
    """

    def __init__(
        self,
        storage_path: str = "persona_layer/state/active/organ_confidence.json",
        ema_alpha: float = 0.1,  # DAE 3.0 validated
        initial_confidence: float = 0.5,
        success_threshold: float = 0.5  # Min user satisfaction for "success"
    ):
        """
        Initialize organ confidence tracking.

        Args:
            storage_path: Path to persistent confidence storage (JSON)
            ema_alpha: EMA smoothing factor (0.1 = slow adaptation, DAE 3.0)
            initial_confidence: Starting confidence for new organs (0.5 = neutral)
            success_threshold: Min satisfaction to count as success (0.5 = "Helpful")
        """
        self.storage_path = Path(storage_path)
        self.ema_alpha = ema_alpha
        self.initial_confidence = initial_confidence
        self.success_threshold = success_threshold

        # Per-organ metrics
        self.organ_metrics: Dict[str, OrganConfidenceMetrics] = {}

        # Load existing state
        self._load()

        print(f"✅ Organ Confidence Tracker initialized (Level 2 Fractal Rewards)")
        print(f"   Storage: {self.storage_path}")
        print(f"   EMA alpha: {self.ema_alpha}")
        print(f"   Tracked organs: {len(self.organ_metrics)}")

    def update(
        self,
        organ_results: Dict,
        emission_confidence: float,
        user_satisfaction: Optional[float] = None
    ):
        """
        Update organ confidences based on emission outcome.

        Args:
            organ_results: Dict of organ_name → organ result (from wrapper)
            emission_confidence: Final emission confidence [0.0, 1.0]
            user_satisfaction: Optional user rating [0.0, 1.0]
        """
        # Determine if emission was successful
        # Use user satisfaction if available, else emission confidence
        satisfaction = user_satisfaction if user_satisfaction is not None else emission_confidence
        task_success = satisfaction >= self.success_threshold

        # Update each organ
        for organ_name, organ_result in organ_results.items():
            # Check if organ participated (was active)
            participated = self._organ_participated(organ_result)

            # Get or create metrics
            if organ_name not in self.organ_metrics:
                self._initialize_organ(organ_name)

            metrics = self.organ_metrics[organ_name]

            # Update based on participation + success
            if participated:
                if task_success:
                    # Success → boost confidence
                    metrics.confidence = (
                        (1 - self.ema_alpha) * metrics.confidence +
                        self.ema_alpha * 1.0
                    )
                    metrics.success_count += 1
                else:
                    # Failure → lower confidence
                    metrics.confidence = (
                        (1 - self.ema_alpha) * metrics.confidence +
                        self.ema_alpha * 0.0
                    )
                    metrics.failure_count += 1

                # Update derived metrics
                metrics.total_participations = metrics.success_count + metrics.failure_count
                if metrics.total_participations > 0:
                    metrics.success_rate = metrics.success_count / metrics.total_participations

                # Update weight multiplier
                metrics.weight_multiplier = self._compute_weight_multiplier(metrics.confidence)
                metrics.last_updated = datetime.now().isoformat()

        # Save updated state
        self._save()

    def get_weight_multiplier(self, organ_name: str) -> float:
        """
        Get weight multiplier for organ during processing.

        Args:
            organ_name: Name of organ (e.g., 'BOND', 'WISDOM')

        Returns:
            Weight multiplier [0.8, 1.2]
            - 1.0 = neutral (initial state)
            - >1.0 = boost (high confidence)
            - <1.0 = dampen (low confidence)
        """
        if organ_name not in self.organ_metrics:
            return 1.0  # Neutral for new organs

        return self.organ_metrics[organ_name].weight_multiplier

    def get_all_multipliers(self) -> Dict[str, float]:
        """Get weight multipliers for all tracked organs"""
        return {
            organ_name: metrics.weight_multiplier
            for organ_name, metrics in self.organ_metrics.items()
        }

    def get_metrics(self, organ_name: str) -> Optional[OrganConfidenceMetrics]:
        """Get full metrics for specific organ"""
        return self.organ_metrics.get(organ_name)

    def get_summary(self) -> Dict:
        """Get summary statistics across all organs"""
        if not self.organ_metrics:
            return {}

        confidences = [m.confidence for m in self.organ_metrics.values()]
        multipliers = [m.weight_multiplier for m in self.organ_metrics.values()]
        success_rates = [m.success_rate for m in self.organ_metrics.values() if m.total_participations > 0]

        return {
            'total_organs': len(self.organ_metrics),
            'mean_confidence': np.mean(confidences),
            'std_confidence': np.std(confidences),
            'min_confidence': np.min(confidences),
            'max_confidence': np.max(confidences),
            'mean_multiplier': np.mean(multipliers),
            'mean_success_rate': np.mean(success_rates) if success_rates else 0.0,
            'organs_above_neutral': sum(1 for c in confidences if c > 0.55),
            'organs_below_neutral': sum(1 for c in confidences if c < 0.45),
        }

    # ===== Private Methods =====

    def _organ_participated(self, organ_result) -> bool:
        """
        Check if organ actively participated in emission.

        Heuristic: Organ participated if it has above-threshold coherence.
        This creates natural differentiation - only organs that were truly
        active get credit/blame.
        """
        if organ_result is None:
            return False

        # If result is a simple dict with coherence
        if isinstance(organ_result, dict):
            coherence = organ_result.get('coherence', 0.0)
            # Only count as participated if coherence > 0.3 (above minimal threshold)
            # This ensures organs that were barely active don't get equal credit
            return coherence > 0.3

        # Check for various indicators of participation
        if hasattr(organ_result, 'atom_activations'):
            activations = getattr(organ_result, 'atom_activations', {})
            if activations and len(activations) > 0:
                # Check if any activation is significant
                if any(v > 0.3 for v in activations.values()):
                    return True
                return False

        if hasattr(organ_result, 'pattern'):
            pattern = getattr(organ_result, 'pattern', None)
            if pattern is not None:
                return True

        if hasattr(organ_result, 'coherence'):
            coherence = getattr(organ_result, 'coherence', 0.0)
            return coherence > 0.3

        # Default: NOT participated unless proven otherwise
        # This is the key fix - was returning True, causing all organs to get 1.0 confidence
        return False

    def _initialize_organ(self, organ_name: str):
        """Initialize new organ with neutral confidence"""
        now = datetime.now().isoformat()
        self.organ_metrics[organ_name] = OrganConfidenceMetrics(
            organ_name=organ_name,
            confidence=self.initial_confidence,
            success_count=0,
            failure_count=0,
            total_participations=0,
            success_rate=0.0,
            weight_multiplier=1.0,  # Neutral initially
            last_updated=now,
            first_seen=now
        )

    def _compute_weight_multiplier(self, confidence: float) -> float:
        """
        Compute organ weight multiplier from confidence.

        Formula: multiplier = 0.8 + (0.4 * confidence)

        Range:
        - confidence=0.0 → multiplier=0.8 (dampen by 20%)
        - confidence=0.5 → multiplier=1.0 (neutral)
        - confidence=1.0 → multiplier=1.2 (boost by 20%)
        """
        return 0.8 + (0.4 * confidence)

    def _load(self):
        """Load organ metrics from disk"""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Deserialize metrics
            for organ_name, metrics_dict in data.get('organ_metrics', {}).items():
                self.organ_metrics[organ_name] = OrganConfidenceMetrics(**metrics_dict)

        except Exception as e:
            print(f"⚠️  Could not load organ confidence state: {e}")

    def _save(self):
        """Save organ metrics to disk"""
        try:
            # Serialize metrics
            data = {
                'organ_metrics': {
                    organ_name: asdict(metrics)
                    for organ_name, metrics in self.organ_metrics.items()
                },
                'last_updated': datetime.now().isoformat(),
                'total_organs': len(self.organ_metrics),
            }

            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Could not save organ confidence state: {e}")
