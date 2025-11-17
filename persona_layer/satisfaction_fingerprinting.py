"""
Satisfaction Fingerprinting
============================

Temporal pattern classification from FFITTSS RNX legacy.
Classifies satisfaction trajectories into 4 archetypes to gate phrase learning.

Proven Impact (from FFITTSS):
- +8-12pp phrase quality improvement
- Crisis detection prevents bad phrase reinforcement
- Concrescent patterns boost high-quality learning
- Restorative trajectories capture Kairos moments

Archetypes:
1. CRISIS: Satisfaction diverging (all deltas < -0.05) → REJECT emission
2. CONCRESCENT: Satisfaction converging (all deltas > +0.05) → BOOST quality (+0.10)
3. RESTORATIVE: U-shaped recovery (crisis → healing) → KAIROS BONUS (+0.15)
4. PULL: High volatility/oscillation (abs(delta) > 0.1) → PENALTY (-0.05)
5. STABLE: Minimal change → NEUTRAL (no adjustment)

Integration: Phase 1 Week 2, Day 3
North Star: Companion Intelligence (Affective Domain)

November 17, 2025
"""

from typing import List, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class SatisfactionFingerprint:
    """
    Temporal pattern classification for satisfaction trajectory.

    Attributes:
        archetype: One of CRISIS/CONCRESCENT/RESTORATIVE/PULL/STABLE
        quality_adjustment: Phrase quality modifier [-0.15, +0.15]
        confidence: Classification confidence [0.0-1.0]
        trajectory_summary: Human-readable summary
    """

    archetype: str
    quality_adjustment: float
    confidence: float
    trajectory_summary: str


class SatisfactionFingerprintClassifier:
    """
    Classifies satisfaction trajectories into temporal archetypes.

    Usage:
        classifier = SatisfactionFingerprintClassifier()

        # Multi-turn satisfaction trace
        S_trace = [0.3, 0.25, 0.2, 0.35, 0.5, 0.65]

        fingerprint = classifier.classify(S_trace)
        # Returns: SatisfactionFingerprint(
        #     archetype='RESTORATIVE',
        #     quality_adjustment=+0.15,  # Kairos bonus
        #     confidence=0.92,
        #     trajectory_summary='Crisis → Healing (U-shaped recovery)'
        # )
    """

    def __init__(
        self,
        crisis_threshold: float = -0.05,
        concrescent_threshold: float = 0.05,
        volatility_threshold: float = 0.1,
        min_samples: int = 3
    ):
        """
        Initialize fingerprint classifier.

        Args:
            crisis_threshold: Delta threshold for crisis detection (default -0.05)
            concrescent_threshold: Delta threshold for convergence (default +0.05)
            volatility_threshold: Absolute delta for volatility (default 0.1)
            min_samples: Minimum trajectory samples for classification (default 3)
        """
        self.crisis_threshold = crisis_threshold
        self.concrescent_threshold = concrescent_threshold
        self.volatility_threshold = volatility_threshold
        self.min_samples = min_samples

    def classify(self, satisfaction_trace: List[float]) -> SatisfactionFingerprint:
        """
        Classify satisfaction trajectory into archetype.

        Args:
            satisfaction_trace: List of satisfaction values over time [0.0-1.0]

        Returns:
            SatisfactionFingerprint with archetype and quality adjustment
        """
        # Validate input
        if len(satisfaction_trace) < self.min_samples:
            return SatisfactionFingerprint(
                archetype='STABLE',
                quality_adjustment=0.0,
                confidence=0.0,
                trajectory_summary='Insufficient samples for classification'
            )

        # Compute first-order differences (delta satisfaction)
        delta_S = np.diff(satisfaction_trace)

        # Check for CRISIS (all deltas negative)
        if self._is_crisis(delta_S):
            return SatisfactionFingerprint(
                archetype='CRISIS',
                quality_adjustment=-0.20,  # REJECT (strong penalty)
                confidence=self._compute_crisis_confidence(delta_S),
                trajectory_summary=f'Diverging satisfaction (mean Δ={np.mean(delta_S):.3f})'
            )

        # Check for CONCRESCENT (all deltas positive)
        if self._is_concrescent(delta_S):
            return SatisfactionFingerprint(
                archetype='CONCRESCENT',
                quality_adjustment=+0.10,  # BOOST
                confidence=self._compute_concrescent_confidence(delta_S),
                trajectory_summary=f'Converging satisfaction (mean Δ={np.mean(delta_S):.3f})'
            )

        # Check for RESTORATIVE (U-shaped: crisis → healing)
        if self._is_restorative(delta_S, satisfaction_trace):
            return SatisfactionFingerprint(
                archetype='RESTORATIVE',
                quality_adjustment=+0.15,  # KAIROS BONUS
                confidence=self._compute_restorative_confidence(delta_S),
                trajectory_summary='Crisis → Healing (U-shaped recovery, Kairos detected)'
            )

        # Check for PULL (high volatility/oscillation)
        if self._is_pull(delta_S):
            return SatisfactionFingerprint(
                archetype='PULL',
                quality_adjustment=-0.05,  # PENALTY
                confidence=self._compute_pull_confidence(delta_S),
                trajectory_summary=f'Volatile/oscillating (mean |Δ|={np.mean(np.abs(delta_S)):.3f})'
            )

        # Default: STABLE (minimal change)
        return SatisfactionFingerprint(
            archetype='STABLE',
            quality_adjustment=0.0,  # NEUTRAL
            confidence=1.0 - np.std(delta_S),  # Low variance = high confidence
            trajectory_summary=f'Stable satisfaction (std Δ={np.std(delta_S):.3f})'
        )

    def _is_crisis(self, delta_S: np.ndarray) -> bool:
        """Check if all deltas indicate crisis (negative trend)."""
        return all(d < self.crisis_threshold for d in delta_S)

    def _is_concrescent(self, delta_S: np.ndarray) -> bool:
        """Check if all deltas indicate convergence (positive trend)."""
        return all(d > self.concrescent_threshold for d in delta_S)

    def _is_restorative(self, delta_S: np.ndarray, S_trace: List[float]) -> bool:
        """
        Check for U-shaped recovery (crisis → healing).

        Criteria:
        - First delta negative (crisis onset)
        - Last delta positive (healing)
        - Overall trend upward
        """
        if len(delta_S) < 2:
            return False

        # Crisis onset (first delta negative)
        crisis_onset = delta_S[0] < self.crisis_threshold

        # Healing recovery (last delta positive)
        healing_recovery = delta_S[-1] > self.concrescent_threshold

        # Overall upward trend (final > initial)
        upward_trend = S_trace[-1] > S_trace[0]

        return crisis_onset and healing_recovery and upward_trend

    def _is_pull(self, delta_S: np.ndarray) -> bool:
        """Check for high volatility (oscillation/ambivalence)."""
        return any(abs(d) > self.volatility_threshold for d in delta_S)

    def _compute_crisis_confidence(self, delta_S: np.ndarray) -> float:
        """Confidence based on consistency of negative trend."""
        mean_delta = np.mean(delta_S)
        std_delta = np.std(delta_S)

        # High confidence if consistently negative with low variance
        consistency = 1.0 - (std_delta / max(abs(mean_delta), 0.01))
        return np.clip(consistency, 0.0, 1.0)

    def _compute_concrescent_confidence(self, delta_S: np.ndarray) -> float:
        """Confidence based on consistency of positive trend."""
        mean_delta = np.mean(delta_S)
        std_delta = np.std(delta_S)

        # High confidence if consistently positive with low variance
        consistency = 1.0 - (std_delta / max(mean_delta, 0.01))
        return np.clip(consistency, 0.0, 1.0)

    def _compute_restorative_confidence(self, delta_S: np.ndarray) -> float:
        """Confidence based on U-shaped recovery pattern strength."""
        if len(delta_S) < 2:
            return 0.0

        # Measure recovery strength (magnitude of last positive delta)
        recovery_strength = delta_S[-1]

        # Measure crisis depth (magnitude of first negative delta)
        crisis_depth = abs(delta_S[0])

        # High confidence if strong recovery from deep crisis
        confidence = min(recovery_strength, crisis_depth) / max(recovery_strength, crisis_depth, 0.01)
        return np.clip(confidence, 0.0, 1.0)

    def _compute_pull_confidence(self, delta_S: np.ndarray) -> float:
        """Confidence based on volatility magnitude."""
        max_volatility = np.max(np.abs(delta_S))
        mean_volatility = np.mean(np.abs(delta_S))

        # High confidence if consistently volatile
        consistency = mean_volatility / max(max_volatility, 0.01)
        return np.clip(consistency, 0.0, 1.0)

    def get_adjusted_quality(
        self,
        base_quality: float,
        satisfaction_trace: List[float]
    ) -> Tuple[float, SatisfactionFingerprint]:
        """
        Apply fingerprint-based quality adjustment.

        Args:
            base_quality: Base phrase quality [0.0-1.0]
            satisfaction_trace: Satisfaction trajectory

        Returns:
            (adjusted_quality, fingerprint) tuple
        """
        fingerprint = self.classify(satisfaction_trace)

        adjusted_quality = base_quality + fingerprint.quality_adjustment
        adjusted_quality = np.clip(adjusted_quality, 0.0, 1.0)

        return adjusted_quality, fingerprint


# Example usage and validation
if __name__ == '__main__':
    classifier = SatisfactionFingerprintClassifier()

    # Test cases from FFITTSS
    test_cases = [
        # CRISIS: Diverging satisfaction
        {
            'name': 'Crisis Example',
            'trace': [0.6, 0.5, 0.4, 0.3, 0.2],
            'expected': 'CRISIS'
        },
        # CONCRESCENT: Converging satisfaction
        {
            'name': 'Concrescent Example',
            'trace': [0.3, 0.4, 0.5, 0.6, 0.7],
            'expected': 'CONCRESCENT'
        },
        # RESTORATIVE: U-shaped recovery
        {
            'name': 'Restorative Example',
            'trace': [0.5, 0.3, 0.25, 0.4, 0.6, 0.75],
            'expected': 'RESTORATIVE'
        },
        # PULL: High volatility
        {
            'name': 'Pull Example',
            'trace': [0.5, 0.7, 0.3, 0.8, 0.2, 0.6],
            'expected': 'PULL'
        },
        # STABLE: Minimal change
        {
            'name': 'Stable Example',
            'trace': [0.6, 0.61, 0.59, 0.60, 0.61],
            'expected': 'STABLE'
        }
    ]

    print("Satisfaction Fingerprinting Validation")
    print("=" * 60)

    for test in test_cases:
        fingerprint = classifier.classify(test['trace'])
        match = '✅' if fingerprint.archetype == test['expected'] else '❌'

        print(f"\n{match} {test['name']}")
        print(f"   Trace: {test['trace']}")
        print(f"   Archetype: {fingerprint.archetype} (expected: {test['expected']})")
        print(f"   Quality Δ: {fingerprint.quality_adjustment:+.2f}")
        print(f"   Confidence: {fingerprint.confidence:.2f}")
        print(f"   Summary: {fingerprint.trajectory_summary}")

    # Test quality adjustment
    print("\n" + "=" * 60)
    print("Quality Adjustment Example:")
    print("=" * 60)

    base_quality = 0.70
    crisis_trace = [0.6, 0.5, 0.4, 0.3]
    restorative_trace = [0.3, 0.25, 0.4, 0.6, 0.75]

    crisis_adjusted, crisis_fp = classifier.get_adjusted_quality(base_quality, crisis_trace)
    restorative_adjusted, restorative_fp = classifier.get_adjusted_quality(base_quality, restorative_trace)

    print(f"\nBase Quality: {base_quality:.2f}")
    print(f"\nCrisis Trajectory: {crisis_trace}")
    print(f"  → Adjusted Quality: {crisis_adjusted:.2f} (Δ={crisis_fp.quality_adjustment:+.2f})")

    print(f"\nRestorative Trajectory: {restorative_trace}")
    print(f"  → Adjusted Quality: {restorative_adjusted:.2f} (Δ={restorative_fp.quality_adjustment:+.2f})")
