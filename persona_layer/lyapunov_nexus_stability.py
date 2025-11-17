"""
Lyapunov Nexus Stability Analysis
==================================

Stability gating for nexus-phrase patterns from FFITTSS legacy.
Predicts pattern stability using Lyapunov function to gate phrase learning.

Proven Impact (from FFITTSS):
- +5-8pp phrase quality improvement
- Prevents unstable pattern reinforcement
- Identifies stable attractor basins for learning
- Predicts convergence trajectories

Lyapunov Function:
    V(x) = α·(1-C) + β·ΔCn² + γ·∑(dissonances)

Where:
- C = field coherence (DAE 3.0: 1 - std([organs]))
- ΔCn = constraint delta squared (BOND, NDAM, SANS, EO changes)
- dissonances = organ-level conflicts

Regimes:
1. STABLE: V < 0.3 → BOOST quality (+0.08)
2. ATTRACTING: dV/dt < 0 (V decreasing) → BOOST quality (+0.12)
3. MARGINAL: 0.3 ≤ V < 0.7 → NEUTRAL (no adjustment)
4. UNSTABLE: V ≥ 0.7 → REJECT emission (-0.30)

Integration: Phase 1 Week 2, Day 4
North Star: Companion Intelligence (Affective Domain)

November 17, 2025
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class LyapunovStabilityAnalysis:
    """
    Lyapunov stability assessment for nexus pattern.

    Attributes:
        V: Lyapunov function value [0.0-1.0+]
        regime: One of STABLE/ATTRACTING/MARGINAL/UNSTABLE
        quality_adjustment: Phrase quality modifier [-0.30, +0.12]
        confidence: Analysis confidence [0.0-1.0]
        components: Breakdown of V function (coherence, constraint, dissonance)
        stability_summary: Human-readable summary
    """

    V: float
    regime: str
    quality_adjustment: float
    confidence: float
    components: Dict[str, float]
    stability_summary: str


class LyapunovNexusStabilityGate:
    """
    Lyapunov stability gating for nexus-phrase patterns.

    Predicts pattern stability from field coherence, constraint dynamics,
    and organ dissonances to gate phrase learning quality.

    Usage:
        gate = LyapunovNexusStabilityGate()

        # Compute stability for current nexus state
        analysis = gate.analyze_stability(
            coherence=0.72,
            constraint_deltas={'BOND': 0.05, 'NDAM': -0.02, 'SANS': 0.01, 'EO': 0.03},
            organ_dissonances={'EMPATHY': 0.1, 'NDAM': 0.3, 'RNX': 0.05}
        )

        # Apply stability-based quality gating
        adjusted_quality = base_quality + analysis.quality_adjustment
    """

    def __init__(
        self,
        alpha: float = 0.4,  # Coherence disorder weight
        beta: float = 0.3,   # Constraint delta weight
        gamma: float = 0.3,  # Organ dissonance weight
        stable_threshold: float = 0.3,
        unstable_threshold: float = 0.7
    ):
        """
        Initialize Lyapunov stability gate.

        Args:
            alpha: Weight for coherence disorder (1-C) term
            beta: Weight for constraint delta squared term
            gamma: Weight for organ dissonance term
            stable_threshold: V threshold for STABLE regime (default 0.3)
            unstable_threshold: V threshold for UNSTABLE regime (default 0.7)
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.stable_threshold = stable_threshold
        self.unstable_threshold = unstable_threshold

        # History for trajectory analysis (dV/dt)
        self.V_history: List[float] = []

    def compute_lyapunov_function(
        self,
        coherence: float,
        constraint_deltas: Dict[str, float],
        organ_dissonances: Dict[str, float]
    ) -> Tuple[float, Dict[str, float]]:
        """
        Compute Lyapunov function V(x).

        V(x) = α·(1-C) + β·ΔCn² + γ·∑(dissonances)

        Args:
            coherence: Field coherence [0.0-1.0] (from DAE 3.0: 1 - std([organs]))
            constraint_deltas: Per-constraint changes (BOND, NDAM, SANS, EO)
            organ_dissonances: Per-organ conflict magnitudes

        Returns:
            (V, components) tuple where components breakdown V contributions
        """
        # Component 1: Coherence disorder (penalty for low coherence)
        coherence_disorder = 1.0 - coherence
        coherence_term = self.alpha * coherence_disorder

        # Component 2: Constraint delta squared (penalty for large constraint changes)
        constraint_delta_sq = sum(d**2 for d in constraint_deltas.values())
        constraint_term = self.beta * constraint_delta_sq

        # Component 3: Organ dissonances (penalty for organ conflicts)
        dissonance_sum = sum(organ_dissonances.values())
        dissonance_term = self.gamma * dissonance_sum

        # Total Lyapunov function
        V = coherence_term + constraint_term + dissonance_term

        # Clip to [0.0, 1.0+] (can exceed 1.0 for highly unstable states)
        V = max(0.0, V)

        components = {
            'coherence_disorder': coherence_disorder,
            'coherence_term': coherence_term,
            'constraint_delta_sq': constraint_delta_sq,
            'constraint_term': constraint_term,
            'dissonance_sum': dissonance_sum,
            'dissonance_term': dissonance_term
        }

        return V, components

    def classify_regime(
        self,
        V: float,
        V_history: Optional[List[float]] = None
    ) -> Tuple[str, float]:
        """
        Classify stability regime from V and its trajectory.

        Args:
            V: Current Lyapunov function value
            V_history: Optional trajectory (for ATTRACTING detection)

        Returns:
            (regime, quality_adjustment) tuple
        """
        # Check for ATTRACTING (V decreasing rapidly)
        if V_history and len(V_history) >= 2:
            dV_dt = V_history[-1] - V_history[-2]
            if dV_dt < -0.1:  # Rapid decrease toward stability
                return 'ATTRACTING', +0.12

        # Static regime classification
        if V < self.stable_threshold:
            return 'STABLE', +0.08
        elif V >= self.unstable_threshold:
            return 'UNSTABLE', -0.30
        else:
            return 'MARGINAL', 0.0

    def analyze_stability(
        self,
        coherence: float,
        constraint_deltas: Optional[Dict[str, float]] = None,
        organ_dissonances: Optional[Dict[str, float]] = None,
        track_trajectory: bool = True
    ) -> LyapunovStabilityAnalysis:
        """
        Perform complete Lyapunov stability analysis.

        Args:
            coherence: Field coherence [0.0-1.0]
            constraint_deltas: Per-constraint changes (default: empty)
            organ_dissonances: Per-organ conflicts (default: empty)
            track_trajectory: Whether to track V history for ATTRACTING detection

        Returns:
            LyapunovStabilityAnalysis with regime and quality adjustment
        """
        # Default empty dicts
        constraint_deltas = constraint_deltas or {}
        organ_dissonances = organ_dissonances or {}

        # Compute Lyapunov function
        V, components = self.compute_lyapunov_function(
            coherence=coherence,
            constraint_deltas=constraint_deltas,
            organ_dissonances=organ_dissonances
        )

        # Track trajectory
        if track_trajectory:
            self.V_history.append(V)
            # Keep last 10 values only
            if len(self.V_history) > 10:
                self.V_history.pop(0)

        # Classify regime
        regime, quality_adjustment = self.classify_regime(
            V=V,
            V_history=self.V_history if track_trajectory else None
        )

        # Compute confidence (higher for extreme values, lower for marginal)
        if regime == 'MARGINAL':
            confidence = 1.0 - 2.0 * abs(V - 0.5)  # Low confidence near 0.5
        else:
            confidence = min(abs(V - 0.5) * 2.0, 1.0)  # High confidence at extremes

        # Create summary
        stability_summary = self._create_summary(regime, V, components)

        return LyapunovStabilityAnalysis(
            V=V,
            regime=regime,
            quality_adjustment=quality_adjustment,
            confidence=confidence,
            components=components,
            stability_summary=stability_summary
        )

    def _create_summary(
        self,
        regime: str,
        V: float,
        components: Dict[str, float]
    ) -> str:
        """Create human-readable stability summary."""
        summaries = {
            'STABLE': f'Stable attractor basin (V={V:.3f} < {self.stable_threshold})',
            'ATTRACTING': f'Converging toward stability (V↓={V:.3f}, rapid decrease)',
            'MARGINAL': f'Marginal stability (V={V:.3f} ∈ [{self.stable_threshold}, {self.unstable_threshold}])',
            'UNSTABLE': f'Unstable divergence (V={V:.3f} ≥ {self.unstable_threshold})'
        }

        base_summary = summaries.get(regime, f'Unknown regime (V={V:.3f})')

        # Add dominant component
        component_names = {
            'coherence_term': 'coherence disorder',
            'constraint_term': 'constraint dynamics',
            'dissonance_term': 'organ dissonance'
        }

        dominant_component = max(
            [('coherence_term', components['coherence_term']),
             ('constraint_term', components['constraint_term']),
             ('dissonance_term', components['dissonance_term'])],
            key=lambda x: x[1]
        )

        dominant_name = component_names[dominant_component[0]]
        dominant_value = dominant_component[1]

        return f'{base_summary}, dominated by {dominant_name} ({dominant_value:.3f})'

    def reset_trajectory(self) -> None:
        """Reset V history (for new conversation)."""
        self.V_history = []

    def get_adjusted_quality(
        self,
        base_quality: float,
        coherence: float,
        constraint_deltas: Optional[Dict[str, float]] = None,
        organ_dissonances: Optional[Dict[str, float]] = None
    ) -> Tuple[float, LyapunovStabilityAnalysis]:
        """
        Apply Lyapunov stability-based quality adjustment.

        Args:
            base_quality: Base phrase quality [0.0-1.0]
            coherence: Field coherence
            constraint_deltas: Constraint changes
            organ_dissonances: Organ conflicts

        Returns:
            (adjusted_quality, analysis) tuple
        """
        analysis = self.analyze_stability(
            coherence=coherence,
            constraint_deltas=constraint_deltas,
            organ_dissonances=organ_dissonances
        )

        adjusted_quality = base_quality + analysis.quality_adjustment
        adjusted_quality = np.clip(adjusted_quality, 0.0, 1.0)

        return adjusted_quality, analysis


# Example usage and validation
if __name__ == '__main__':
    gate = LyapunovNexusStabilityGate()

    print("Lyapunov Nexus Stability Validation")
    print("=" * 60)

    # Test cases
    test_cases = [
        {
            'name': 'STABLE: High coherence, low dynamics',
            'coherence': 0.85,
            'constraint_deltas': {'BOND': 0.01, 'NDAM': 0.02, 'SANS': 0.01, 'EO': 0.00},
            'organ_dissonances': {'EMPATHY': 0.05, 'NDAM': 0.03},
            'expected_regime': 'STABLE'
        },
        {
            'name': 'UNSTABLE: Low coherence, high dissonance',
            'coherence': 0.30,
            'constraint_deltas': {'BOND': 0.3, 'NDAM': 0.4, 'SANS': 0.2, 'EO': 0.5},
            'organ_dissonances': {'EMPATHY': 0.4, 'NDAM': 0.6, 'RNX': 0.5},
            'expected_regime': 'UNSTABLE'
        },
        {
            'name': 'MARGINAL: Medium coherence, moderate dynamics',
            'coherence': 0.60,
            'constraint_deltas': {'BOND': 0.05, 'NDAM': 0.08, 'SANS': 0.03, 'EO': 0.04},
            'organ_dissonances': {'EMPATHY': 0.15, 'NDAM': 0.20},
            'expected_regime': 'MARGINAL'
        },
        {
            'name': 'ATTRACTING: Improving coherence (trajectory test)',
            'coherence': 0.65,
            'constraint_deltas': {'BOND': 0.02, 'NDAM': 0.01, 'SANS': 0.01, 'EO': 0.02},
            'organ_dissonances': {'EMPATHY': 0.10, 'NDAM': 0.08},
            'expected_regime': 'ATTRACTING'  # Will be detected after trajectory buildup
        }
    ]

    for i, test in enumerate(test_cases):
        print(f"\nTest {i+1}: {test['name']}")
        print("-" * 60)

        # For ATTRACTING test, simulate improving trajectory
        if test['expected_regime'] == 'ATTRACTING':
            gate.reset_trajectory()
            # Simulate 3 turns with improving V
            for coherence in [0.50, 0.58, test['coherence']]:
                analysis = gate.analyze_stability(
                    coherence=coherence,
                    constraint_deltas=test['constraint_deltas'],
                    organ_dissonances=test['organ_dissonances']
                )
        else:
            gate.reset_trajectory()
            analysis = gate.analyze_stability(
                coherence=test['coherence'],
                constraint_deltas=test['constraint_deltas'],
                organ_dissonances=test['organ_dissonances']
            )

        match = '✅' if analysis.regime == test['expected_regime'] else '❌'

        print(f"   {match} Regime: {analysis.regime} (expected: {test['expected_regime']})")
        print(f"   V(x): {analysis.V:.3f}")
        print(f"   Quality Δ: {analysis.quality_adjustment:+.2f}")
        print(f"   Confidence: {analysis.confidence:.2f}")
        print(f"   Components:")
        print(f"     • Coherence disorder: {analysis.components['coherence_disorder']:.3f} → {analysis.components['coherence_term']:.3f}")
        print(f"     • Constraint Δ²: {analysis.components['constraint_delta_sq']:.3f} → {analysis.components['constraint_term']:.3f}")
        print(f"     • Dissonance Σ: {analysis.components['dissonance_sum']:.3f} → {analysis.components['dissonance_term']:.3f}")
        print(f"   Summary: {analysis.stability_summary}")

    # Test quality adjustment
    print("\n" + "=" * 60)
    print("Quality Adjustment Example:")
    print("=" * 60)

    base_quality = 0.70
    stable_coherence = 0.85
    unstable_coherence = 0.30

    gate.reset_trajectory()
    stable_adjusted, stable_analysis = gate.get_adjusted_quality(
        base_quality=base_quality,
        coherence=stable_coherence,
        constraint_deltas={'BOND': 0.01, 'NDAM': 0.02},
        organ_dissonances={'EMPATHY': 0.05}
    )

    gate.reset_trajectory()
    unstable_adjusted, unstable_analysis = gate.get_adjusted_quality(
        base_quality=base_quality,
        coherence=unstable_coherence,
        constraint_deltas={'BOND': 0.3, 'NDAM': 0.4},
        organ_dissonances={'EMPATHY': 0.5, 'NDAM': 0.6}
    )

    print(f"\nBase Quality: {base_quality:.2f}")
    print(f"\nSTABLE State (coherence={stable_coherence:.2f}):")
    print(f"  → Adjusted Quality: {stable_adjusted:.2f} (Δ={stable_analysis.quality_adjustment:+.2f})")
    print(f"  → V(x): {stable_analysis.V:.3f}")

    print(f"\nUNSTABLE State (coherence={unstable_coherence:.2f}):")
    print(f"  → Adjusted Quality: {unstable_adjusted:.2f} (Δ={unstable_analysis.quality_adjustment:+.2f})")
    print(f"  → V(x): {unstable_analysis.V:.3f}")
