"""
Satisfaction Regime Classification - Integrated with DAE 3.0 Wave Training
==========================================================================

Implements 6-regime satisfaction classification adapted from FFITTSS V0 Tier 6,
integrated with DAE 3.0's wave training architecture and DAE_GOV's satisfaction scaffolding.

## FFITTSS Regimes (from README_TIERS.md):
- INITIALIZING: First 3 iterations (warm-up)
- EXPLORING: Low satisfaction, high variance (search mode)
- CONVERGING: Rising satisfaction, decreasing variance (homing in)
- STABLE: High satisfaction, low variance (found optimum)
- COMMITTED: Sustained stability (confidence in solution)
- PLATEAUED: No improvement for many iterations (local minimum)

## DAE 3.0 Integration - Wave Training Phases:
From DAE 3.0's appetitive phase system (EXPANSIVE → NAVIGATION → CONCRESCENCE):
- Satisfaction is NOT uniform across iterations
- Each V0 cycle has appetitive phase modulation (wave training)
- Satisfaction variance per position (spatial felt, not scalar)
- Per-cycle satisfaction field from organ fusion (6-11 organs)

## DAE_GOV Integration - Satisfaction Scaffolding:
From DAE_GOV's satisfaction_calculator.py:
- Per-organ satisfaction with organ-specific formulas
- Field coherence from organ balance
- Spatial satisfaction variance (IQR >= 0.0005)
- No overconfidence amplification (removed in Oct 26 fix)

## Key Architectural Alignment:
1. **Respects Wave Training**: Regime classification considers appetitive phase progression
2. **Spatial Variance Aware**: Uses IQR of satisfaction field, not just mean
3. **Organ Coherence**: Considers field coherence from organ balance
4. **Multi-Cycle**: Tracks satisfaction across V0 convergence cycles
5. **Family Learning**: Per-family regime evolution (organic families)

## Regime Evolution Rates:
Evolution rates control how aggressively tau thresholds adjust per regime:
- INITIALIZING: 0.1 (very cautious - system warming up)
- EXPLORING: 0.3 (moderate - active search)
- CONVERGING: 0.5 (faster - homing in on target)
- STABLE: 0.2 (maintain - found good region)
- COMMITTED: 0.1 (very slow - sustained success)
- PLATEAUED: 1.0 (aggressive - escape local minimum)

## Mathematical Formulation:
Given satisfaction_history = [s₁, s₂, ..., sₙ] from N training iterations:
- Mean: μ = mean(satisfaction_history)
- Variance: σ² = var(satisfaction_history)
- Trend: β = slope of linear fit
- Regime: classify(μ, σ², β, N) → {INITIALIZING, EXPLORING, ...}
- Evolution rate: η ∈ [0.1, 1.0] based on regime

Tau threshold evolution (next file: convergence_evolver.py):
    τ_new = τ_old + η · direction · magnitude

Author: DAE_HYPHAE_1 Persona Layer
Date: November 13, 2025 (Updated for DAE 3.0 integration)
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Any
import numpy as np


class SatisfactionRegime(Enum):
    """
    6 regimes of satisfaction evolution during epoch training.

    Each regime has different characteristics and evolution rates:
    - INITIALIZING: Warm-up phase, cautious evolution
    - EXPLORING: Active search, moderate evolution
    - CONVERGING: Approaching target, faster evolution
    - STABLE: At target, maintain position
    - COMMITTED: Sustained stability, very slow evolution
    - PLATEAUED: Stuck, aggressive evolution to escape
    """
    INITIALIZING = "INITIALIZING"  # First 3 iterations
    EXPLORING = "EXPLORING"        # Low sat, high variance
    CONVERGING = "CONVERGING"      # Rising sat, decreasing variance
    STABLE = "STABLE"              # High sat, low variance
    COMMITTED = "COMMITTED"        # Sustained stability
    PLATEAUED = "PLATEAUED"        # No improvement


@dataclass
class RegimeClassification:
    """Result of regime classification."""
    regime: SatisfactionRegime
    evolution_rate: float  # Tau adjustment multiplier
    confidence: float      # Classification confidence
    reasoning: str         # Human-readable explanation

    # Regime statistics
    mean_satisfaction: float
    satisfaction_variance: float
    satisfaction_trend: float  # Slope of recent window
    iterations_in_regime: int


class RegimeConfig:
    """
    Configuration for regime classification thresholds.

    These thresholds are adapted from FFITTSS V0's observed distributions:
    - FFITTSS had 86.2% COMMITTED, 12.2% STABLE (very healthy)
    - DAE targets similar distribution for conversational training
    """

    # Iteration count thresholds
    INITIALIZING_WINDOW = 3  # First 3 iterations always INITIALIZING
    COMMITTED_MIN_ITERATIONS = 10  # Minimum for COMMITTED regime
    PLATEAUED_MIN_ITERATIONS = 15  # Minimum for PLATEAUED regime

    # Satisfaction thresholds (0.0-1.0)
    HIGH_SATISFACTION_THRESHOLD = 0.65  # Above this = high satisfaction
    LOW_SATISFACTION_THRESHOLD = 0.40   # Below this = low satisfaction

    # Variance thresholds (std dev of satisfaction)
    LOW_VARIANCE_THRESHOLD = 0.05   # Below this = low variance (stable)
    HIGH_VARIANCE_THRESHOLD = 0.15  # Above this = high variance (exploring)

    # Trend thresholds (slope per iteration)
    POSITIVE_TREND_THRESHOLD = 0.02   # Rising satisfaction
    NEGATIVE_TREND_THRESHOLD = -0.02  # Falling satisfaction
    PLATEAU_THRESHOLD = 0.005         # No significant change

    # Stability window (for COMMITTED/PLATEAUED detection)
    STABILITY_WINDOW_SIZE = 5  # Look at last 5 iterations

    # Evolution rates per regime (tau adjustment multiplier)
    EVOLUTION_RATES = {
        SatisfactionRegime.INITIALIZING: 0.1,   # Very cautious
        SatisfactionRegime.EXPLORING: 0.3,      # Moderate exploration
        SatisfactionRegime.CONVERGING: 0.5,     # Faster convergence
        SatisfactionRegime.STABLE: 0.2,         # Maintain stability
        SatisfactionRegime.COMMITTED: 0.1,      # Very slow evolution
        SatisfactionRegime.PLATEAUED: 1.0       # Aggressive escape
    }


def classify_satisfaction_regime(
    satisfaction_history: List[float],
    iteration_count: int,
    config: Optional[RegimeConfig] = None
) -> RegimeClassification:
    """
    Classify current satisfaction regime based on history.

    Adapted from FFITTSS V0 Tier 6 regime classification logic.

    Args:
        satisfaction_history: List of satisfaction scores (most recent last)
        iteration_count: Total iterations so far (for INITIALIZING gate)
        config: Optional custom configuration

    Returns:
        RegimeClassification with regime, evolution_rate, and statistics

    Example:
        >>> history = [0.45, 0.52, 0.58, 0.64, 0.68, 0.70, 0.71, 0.71]
        >>> result = classify_satisfaction_regime(history, iteration_count=8)
        >>> result.regime
        SatisfactionRegime.STABLE
        >>> result.evolution_rate
        0.2
    """
    if config is None:
        config = RegimeConfig()

    # Edge case: No history
    if len(satisfaction_history) == 0:
        return RegimeClassification(
            regime=SatisfactionRegime.INITIALIZING,
            evolution_rate=config.EVOLUTION_RATES[SatisfactionRegime.INITIALIZING],
            confidence=1.0,
            reasoning="No satisfaction history yet",
            mean_satisfaction=0.0,
            satisfaction_variance=0.0,
            satisfaction_trend=0.0,
            iterations_in_regime=0
        )

    # Compute statistics
    mean_sat = float(np.mean(satisfaction_history))
    variance_sat = float(np.var(satisfaction_history))
    std_sat = float(np.std(satisfaction_history))

    # Compute trend (linear regression slope)
    if len(satisfaction_history) >= 2:
        x = np.arange(len(satisfaction_history))
        trend = float(np.polyfit(x, satisfaction_history, 1)[0])
    else:
        trend = 0.0

    # Rule 1: INITIALIZING (first 3 iterations)
    if iteration_count < config.INITIALIZING_WINDOW:
        return RegimeClassification(
            regime=SatisfactionRegime.INITIALIZING,
            evolution_rate=config.EVOLUTION_RATES[SatisfactionRegime.INITIALIZING],
            confidence=1.0,
            reasoning=f"First {config.INITIALIZING_WINDOW} iterations (warm-up phase)",
            mean_satisfaction=mean_sat,
            satisfaction_variance=variance_sat,
            satisfaction_trend=trend,
            iterations_in_regime=iteration_count
        )

    # Get stability window (last N iterations)
    window_size = min(config.STABILITY_WINDOW_SIZE, len(satisfaction_history))
    recent_window = satisfaction_history[-window_size:]
    recent_variance = float(np.var(recent_window))
    recent_mean = float(np.mean(recent_window))
    recent_std = float(np.std(recent_window))

    # Rule 2: COMMITTED (sustained high satisfaction + low variance)
    if (iteration_count >= config.COMMITTED_MIN_ITERATIONS and
        recent_mean >= config.HIGH_SATISFACTION_THRESHOLD and
        recent_std <= config.LOW_VARIANCE_THRESHOLD and
        abs(trend) <= config.PLATEAU_THRESHOLD):
        return RegimeClassification(
            regime=SatisfactionRegime.COMMITTED,
            evolution_rate=config.EVOLUTION_RATES[SatisfactionRegime.COMMITTED],
            confidence=0.95,
            reasoning=f"Sustained high satisfaction ({recent_mean:.3f}) with low variance ({recent_std:.3f}) for {window_size} iterations",
            mean_satisfaction=mean_sat,
            satisfaction_variance=variance_sat,
            satisfaction_trend=trend,
            iterations_in_regime=iteration_count - config.COMMITTED_MIN_ITERATIONS
        )

    # Rule 3: PLATEAUED (no improvement for many iterations)
    if (iteration_count >= config.PLATEAUED_MIN_ITERATIONS and
        abs(trend) <= config.PLATEAU_THRESHOLD and
        recent_mean < config.HIGH_SATISFACTION_THRESHOLD):
        return RegimeClassification(
            regime=SatisfactionRegime.PLATEAUED,
            evolution_rate=config.EVOLUTION_RATES[SatisfactionRegime.PLATEAUED],
            confidence=0.85,
            reasoning=f"No improvement for {window_size} iterations (mean={recent_mean:.3f}, trend={trend:.4f})",
            mean_satisfaction=mean_sat,
            satisfaction_variance=variance_sat,
            satisfaction_trend=trend,
            iterations_in_regime=iteration_count - config.PLATEAUED_MIN_ITERATIONS
        )

    # Rule 4: STABLE (high satisfaction + low variance, but not sustained)
    if (recent_mean >= config.HIGH_SATISFACTION_THRESHOLD and
        recent_std <= config.LOW_VARIANCE_THRESHOLD):
        return RegimeClassification(
            regime=SatisfactionRegime.STABLE,
            evolution_rate=config.EVOLUTION_RATES[SatisfactionRegime.STABLE],
            confidence=0.80,
            reasoning=f"High satisfaction ({recent_mean:.3f}) with low variance ({recent_std:.3f})",
            mean_satisfaction=mean_sat,
            satisfaction_variance=variance_sat,
            satisfaction_trend=trend,
            iterations_in_regime=1  # Just entered
        )

    # Rule 5: CONVERGING (rising satisfaction, decreasing variance)
    if (trend >= config.POSITIVE_TREND_THRESHOLD and
        recent_std < std_sat):  # Variance decreasing
        return RegimeClassification(
            regime=SatisfactionRegime.CONVERGING,
            evolution_rate=config.EVOLUTION_RATES[SatisfactionRegime.CONVERGING],
            confidence=0.75,
            reasoning=f"Rising satisfaction (trend={trend:.4f}) with decreasing variance",
            mean_satisfaction=mean_sat,
            satisfaction_variance=variance_sat,
            satisfaction_trend=trend,
            iterations_in_regime=1
        )

    # Rule 6: EXPLORING (fallback - active search mode)
    return RegimeClassification(
        regime=SatisfactionRegime.EXPLORING,
        evolution_rate=config.EVOLUTION_RATES[SatisfactionRegime.EXPLORING],
        confidence=0.70,
        reasoning=f"Active exploration (mean={mean_sat:.3f}, variance={variance_sat:.4f}, trend={trend:.4f})",
        mean_satisfaction=mean_sat,
        satisfaction_variance=variance_sat,
        satisfaction_trend=trend,
        iterations_in_regime=1
    )


def compute_regime_statistics(
    satisfaction_history: List[float],
    regime_history: List[SatisfactionRegime]
) -> dict:
    """
    Compute aggregate statistics across regimes.

    Useful for analyzing training behavior and comparing to FFITTSS benchmarks.

    Args:
        satisfaction_history: All satisfaction scores
        regime_history: Corresponding regime classifications

    Returns:
        Dict with regime distribution, mean satisfaction per regime, etc.

    Example:
        >>> stats = compute_regime_statistics(sat_history, regime_history)
        >>> stats['regime_distribution']
        {SatisfactionRegime.COMMITTED: 0.862, SatisfactionRegime.STABLE: 0.122, ...}
    """
    if len(satisfaction_history) == 0 or len(regime_history) == 0:
        return {
            'regime_distribution': {},
            'mean_satisfaction_per_regime': {},
            'total_iterations': 0
        }

    # Regime distribution
    total = len(regime_history)
    regime_counts = {}
    for regime in regime_history:
        regime_counts[regime] = regime_counts.get(regime, 0) + 1

    regime_distribution = {
        regime: count / total
        for regime, count in regime_counts.items()
    }

    # Mean satisfaction per regime
    regime_satisfactions = {regime: [] for regime in SatisfactionRegime}
    for sat, regime in zip(satisfaction_history, regime_history):
        regime_satisfactions[regime].append(sat)

    mean_sat_per_regime = {
        regime: float(np.mean(sats)) if len(sats) > 0 else 0.0
        for regime, sats in regime_satisfactions.items()
    }

    # Overall statistics
    return {
        'regime_distribution': regime_distribution,
        'mean_satisfaction_per_regime': mean_sat_per_regime,
        'total_iterations': total,
        'overall_mean_satisfaction': float(np.mean(satisfaction_history)),
        'overall_std_satisfaction': float(np.std(satisfaction_history)),

        # FFITTSS benchmarks for comparison
        'ffittss_target_distribution': {
            'COMMITTED': 0.862,
            'STABLE': 0.122,
            'OTHER': 0.016
        }
    }


# ============================================================================
# DAE 3.0 Integration - Wave Training & Spatial Variance
# ============================================================================

def classify_regime_with_wave_context(
    satisfaction_history: List[float],
    iteration_count: int,
    appetitive_phases: Optional[List[str]] = None,
    satisfaction_variances: Optional[List[float]] = None,
    field_coherences: Optional[List[float]] = None,
    config: Optional[RegimeConfig] = None
) -> RegimeClassification:
    """
    Enhanced regime classification with DAE 3.0 wave training context.

    Integrates:
    - Appetitive phase progression (EXPANSIVE → NAVIGATION → CONCRESCENCE)
    - Spatial satisfaction variance (IQR from per-position organ fusion)
    - Field coherence (organ balance from satisfaction_calculator.py)

    This respects DAE 3.0's insight that satisfaction is NOT uniform:
    - Each V0 cycle has wave training phase modulation
    - Satisfaction varies spatially across positions
    - Regime classification must account for this natural variance

    Args:
        satisfaction_history: Mean satisfaction per iteration
        iteration_count: Total iterations so far
        appetitive_phases: Optional list of phases per iteration
                          ["EXPANSIVE", "NAVIGATION", "CONCRESCENCE", ...]
        satisfaction_variances: Optional IQR or std dev per iteration
                               (spatial variance from position satisfaction)
        field_coherences: Optional organ balance per iteration
                         (from satisfaction_calculator.calculate_field_coherence)
        config: Optional custom configuration

    Returns:
        RegimeClassification with wave-aware reasoning

    Example:
        >>> # Standard regime classification
        >>> basic = classify_satisfaction_regime(sat_history, N)
        >>>
        >>> # Wave-aware regime classification (DAE 3.0 style)
        >>> enhanced = classify_regime_with_wave_context(
        ...     sat_history,
        ...     N,
        ...     appetitive_phases=["EXPANSIVE", "NAVIGATION", "CONCRESCENCE"],
        ...     satisfaction_variances=[0.002, 0.001, 0.0005],  # IQR decreasing
        ...     field_coherences=[0.65, 0.72, 0.81]  # Coherence increasing
        ... )
    """
    # Get base classification
    base_classification = classify_satisfaction_regime(
        satisfaction_history,
        iteration_count,
        config
    )

    # If no wave context provided, return base classification
    if not (appetitive_phases or satisfaction_variances or field_coherences):
        return base_classification

    config = config or RegimeConfig()

    # Analyze wave training patterns
    wave_analysis = _analyze_wave_training_patterns(
        appetitive_phases,
        satisfaction_variances,
        field_coherences
    )

    # Adjust regime classification based on wave patterns
    adjusted_regime = base_classification.regime
    adjusted_reasoning = base_classification.reasoning

    # Rule: If wave training shows healthy phase progression (EXPANSIVE→NAVIGATION→CONCRESCENCE)
    # with decreasing variance and increasing coherence, favor CONVERGING/STABLE
    if wave_analysis['healthy_phase_progression'] and wave_analysis['variance_decreasing']:
        if base_classification.regime == SatisfactionRegime.EXPLORING:
            adjusted_regime = SatisfactionRegime.CONVERGING
            adjusted_reasoning += f" | Wave training shows healthy progression (variance↓: {wave_analysis['variance_trend']:.4f})"

        elif base_classification.regime == SatisfactionRegime.CONVERGING:
            # Check if ready for STABLE
            if wave_analysis['recent_coherence'] >= 0.70 and wave_analysis['recent_variance'] <= 0.002:
                adjusted_regime = SatisfactionRegime.STABLE
                adjusted_reasoning += f" | Wave training indicates stability (coherence={wave_analysis['recent_coherence']:.3f}, variance={wave_analysis['recent_variance']:.4f})"

    # Rule: If variance is HIGH despite high mean satisfaction, stay in EXPLORING
    # (This respects DAE 3.0's spatial variance - high IQR means organism is still exploring)
    if wave_analysis['high_spatial_variance'] and base_classification.regime in [SatisfactionRegime.STABLE, SatisfactionRegime.COMMITTED]:
        adjusted_regime = SatisfactionRegime.EXPLORING
        adjusted_reasoning = f"High spatial variance ({wave_analysis['recent_variance']:.4f}) despite high satisfaction - organism still exploring"

    # Rule: If coherence is LOW, prevent COMMITTED classification
    if wave_analysis['low_coherence'] and base_classification.regime == SatisfactionRegime.COMMITTED:
        adjusted_regime = SatisfactionRegime.STABLE
        adjusted_reasoning += f" | Low field coherence ({wave_analysis['recent_coherence']:.3f}) prevents COMMITTED"

    # Create adjusted classification
    return RegimeClassification(
        regime=adjusted_regime,
        evolution_rate=config.EVOLUTION_RATES[adjusted_regime],
        confidence=base_classification.confidence * 0.95,  # Slightly lower confidence (wave context adds uncertainty)
        reasoning=adjusted_reasoning,
        mean_satisfaction=base_classification.mean_satisfaction,
        satisfaction_variance=wave_analysis['overall_variance'],
        satisfaction_trend=base_classification.satisfaction_trend,
        iterations_in_regime=base_classification.iterations_in_regime
    )


def _analyze_wave_training_patterns(
    appetitive_phases: Optional[List[str]],
    satisfaction_variances: Optional[List[float]],
    field_coherences: Optional[List[float]]
) -> Dict[str, Any]:
    """
    Analyze wave training patterns from DAE 3.0 appetitive phase data.

    Returns:
        Dict with wave training analysis:
        - healthy_phase_progression: True if seeing EXPANSIVE→NAVIGATION→CONCRESCENCE
        - variance_decreasing: True if satisfaction variance trending down
        - variance_trend: Linear slope of variance over time
        - recent_variance: Mean variance of last 3 iterations
        - recent_coherence: Mean field coherence of last 3 iterations
        - high_spatial_variance: True if recent variance > 0.005 (organism exploring)
        - low_coherence: True if recent coherence < 0.60 (organs unbalanced)
        - overall_variance: Overall variance of satisfaction
    """
    analysis = {
        'healthy_phase_progression': False,
        'variance_decreasing': False,
        'variance_trend': 0.0,
        'recent_variance': 0.0,
        'recent_coherence': 0.0,
        'high_spatial_variance': False,
        'low_coherence': False,
        'overall_variance': 0.0
    }

    # Analyze appetitive phase progression
    if appetitive_phases and len(appetitive_phases) >= 3:
        # Look for EXPANSIVE → NAVIGATION → CONCRESCENCE pattern
        phases_seen = set(appetitive_phases[-5:])  # Last 5 phases
        expected_progression = {'EXPANSIVE', 'NAVIGATION', 'CONCRESCENCE'}

        # Healthy if we've seen all 3 phases recently
        analysis['healthy_phase_progression'] = expected_progression.issubset(phases_seen)

    # Analyze satisfaction variance trend (spatial IQR from position satisfaction)
    if satisfaction_variances and len(satisfaction_variances) >= 2:
        # Compute trend (variance decreasing = good, organism settling)
        x = np.arange(len(satisfaction_variances))
        variance_slope = float(np.polyfit(x, satisfaction_variances, 1)[0])
        analysis['variance_trend'] = variance_slope
        analysis['variance_decreasing'] = variance_slope < -0.0001  # Decreasing

        # Recent variance (last 3 iterations)
        recent_window = satisfaction_variances[-3:]
        analysis['recent_variance'] = float(np.mean(recent_window))

        # High spatial variance = organism still exploring (respects DAE 3.0 spatial felt)
        analysis['high_spatial_variance'] = analysis['recent_variance'] > 0.005

        # Overall variance
        analysis['overall_variance'] = float(np.var(satisfaction_variances))

    # Analyze field coherence (organ balance from satisfaction_calculator.py)
    if field_coherences and len(field_coherences) >= 1:
        recent_coherences = field_coherences[-3:]
        analysis['recent_coherence'] = float(np.mean(recent_coherences))

        # Low coherence = organs unbalanced (prevent premature COMMITTED)
        analysis['low_coherence'] = analysis['recent_coherence'] < 0.60

    return analysis


# ============================================================================
# Unit Tests
# ============================================================================

def test_initializing_regime():
    """Test INITIALIZING regime (first 3 iterations)."""
    history = [0.30, 0.35]
    result = classify_satisfaction_regime(history, iteration_count=2)
    assert result.regime == SatisfactionRegime.INITIALIZING
    assert result.evolution_rate == 0.1
    assert result.confidence == 1.0
    print("✅ test_initializing_regime passed")


def test_committed_regime():
    """Test COMMITTED regime (sustained high satisfaction)."""
    # 12 iterations with high, stable satisfaction
    history = [0.68, 0.70, 0.71, 0.71, 0.70, 0.72, 0.71, 0.70, 0.71, 0.72, 0.71, 0.71]
    result = classify_satisfaction_regime(history, iteration_count=12)
    assert result.regime == SatisfactionRegime.COMMITTED
    assert result.evolution_rate == 0.1
    assert result.mean_satisfaction >= 0.65
    print("✅ test_committed_regime passed")


def test_exploring_regime():
    """Test EXPLORING regime (low satisfaction, high variance)."""
    history = [0.30, 0.45, 0.35, 0.50, 0.40, 0.38]
    result = classify_satisfaction_regime(history, iteration_count=6)
    assert result.regime == SatisfactionRegime.EXPLORING
    assert result.evolution_rate == 0.3
    print("✅ test_exploring_regime passed")


def test_converging_regime():
    """Test CONVERGING regime (rising satisfaction)."""
    history = [0.30, 0.35, 0.42, 0.50, 0.58, 0.62]
    result = classify_satisfaction_regime(history, iteration_count=6)
    # After INITIALIZING (first 3), should detect CONVERGING if trending up
    assert result.regime in [SatisfactionRegime.CONVERGING, SatisfactionRegime.EXPLORING]
    assert result.evolution_rate in [0.3, 0.5]  # EXPLORING or CONVERGING
    assert result.satisfaction_trend > 0.02
    print("✅ test_converging_regime passed")


def test_plateaued_regime():
    """Test PLATEAUED regime (no improvement)."""
    # 20 iterations stuck at low satisfaction
    history = [0.45] * 20
    result = classify_satisfaction_regime(history, iteration_count=20)
    assert result.regime == SatisfactionRegime.PLATEAUED
    assert result.evolution_rate == 1.0  # Aggressive escape
    print("✅ test_plateaued_regime passed")


def test_regime_statistics():
    """Test aggregate regime statistics computation."""
    sat_history = [0.30, 0.35, 0.40, 0.50, 0.60, 0.68, 0.70, 0.71, 0.71, 0.72]
    regime_history = [
        SatisfactionRegime.INITIALIZING,
        SatisfactionRegime.INITIALIZING,
        SatisfactionRegime.INITIALIZING,
        SatisfactionRegime.EXPLORING,
        SatisfactionRegime.CONVERGING,
        SatisfactionRegime.CONVERGING,
        SatisfactionRegime.STABLE,
        SatisfactionRegime.COMMITTED,
        SatisfactionRegime.COMMITTED,
        SatisfactionRegime.COMMITTED
    ]

    stats = compute_regime_statistics(sat_history, regime_history)
    assert stats['total_iterations'] == 10
    assert SatisfactionRegime.COMMITTED in stats['regime_distribution']
    assert stats['regime_distribution'][SatisfactionRegime.COMMITTED] == 0.3
    print("✅ test_regime_statistics passed")


def test_wave_training_integration():
    """Test wave training integration (DAE 3.0 style)."""
    # Simulated wave training scenario:
    # - Satisfaction rising (0.50 → 0.75)
    # - Appetitive phases progressing (EXPANSIVE → NAVIGATION → CONCRESCENCE)
    # - Variance decreasing (spatial felt settling: 0.010 → 0.001)
    # - Coherence increasing (organs balancing: 0.60 → 0.80)

    sat_history = [0.50, 0.58, 0.65, 0.70, 0.73, 0.75]
    iteration_count = 6

    appetitive_phases = [
        "EXPANSIVE",
        "EXPANSIVE",
        "NAVIGATION",
        "NAVIGATION",
        "CONCRESCENCE",
        "CONCRESCENCE"
    ]

    # Spatial satisfaction variance (IQR from per-position organ fusion)
    satisfaction_variances = [0.010, 0.008, 0.005, 0.003, 0.002, 0.001]

    # Field coherence (organ balance from satisfaction_calculator.py)
    field_coherences = [0.60, 0.64, 0.68, 0.72, 0.76, 0.80]

    # Basic classification (without wave context)
    basic = classify_satisfaction_regime(sat_history, iteration_count)
    print(f"   Basic regime: {basic.regime.value}")

    # Wave-aware classification
    wave_aware = classify_regime_with_wave_context(
        sat_history,
        iteration_count,
        appetitive_phases=appetitive_phases,
        satisfaction_variances=satisfaction_variances,
        field_coherences=field_coherences
    )

    print(f"   Wave-aware regime: {wave_aware.regime.value}")
    print(f"   Reasoning: {wave_aware.reasoning}")

    # Expect wave-aware to be CONVERGING or STABLE (healthy progression)
    assert wave_aware.regime in [SatisfactionRegime.CONVERGING, SatisfactionRegime.STABLE]
    print("✅ test_wave_training_integration passed")


def test_high_spatial_variance_prevents_committed():
    """Test that high spatial variance prevents premature COMMITTED classification."""
    # Scenario: High mean satisfaction BUT high spatial variance
    # (Organism has high average satisfaction but still exploring spatially)

    sat_history = [0.68, 0.70, 0.71, 0.72, 0.71, 0.72, 0.71, 0.72, 0.71, 0.72, 0.71, 0.72]
    iteration_count = 12

    # High spatial variance (IQR > 0.005) - organism still exploring
    satisfaction_variances = [0.008, 0.009, 0.007, 0.008, 0.009, 0.007, 0.008, 0.009, 0.007, 0.008, 0.009, 0.007]

    # Basic classification would be COMMITTED (high, stable satisfaction)
    basic = classify_satisfaction_regime(sat_history, iteration_count)
    print(f"   Basic regime: {basic.regime.value}")

    # Wave-aware should prevent COMMITTED due to high spatial variance
    wave_aware = classify_regime_with_wave_context(
        sat_history,
        iteration_count,
        satisfaction_variances=satisfaction_variances
    )

    print(f"   Wave-aware regime: {wave_aware.regime.value}")
    print(f"   Reasoning: {wave_aware.reasoning}")

    # Should be EXPLORING, not COMMITTED (respects spatial variance)
    assert wave_aware.regime == SatisfactionRegime.EXPLORING
    assert "spatial variance" in wave_aware.reasoning.lower()
    print("✅ test_high_spatial_variance_prevents_committed passed")


def test_low_coherence_prevents_committed():
    """Test that low field coherence prevents premature COMMITTED classification."""
    # Scenario: High satisfaction BUT low organ coherence
    # (Organs unbalanced - prevent premature commitment)

    sat_history = [0.68, 0.70, 0.71, 0.72, 0.71, 0.72, 0.71, 0.72, 0.71, 0.72, 0.71, 0.72]
    iteration_count = 12

    # Low field coherence (organs unbalanced)
    field_coherences = [0.55, 0.54, 0.56, 0.55, 0.54, 0.56, 0.55, 0.54, 0.56, 0.55, 0.54, 0.56]

    # Basic classification would be COMMITTED
    basic = classify_satisfaction_regime(sat_history, iteration_count)
    print(f"   Basic regime: {basic.regime.value}")

    # Wave-aware should downgrade to STABLE due to low coherence
    wave_aware = classify_regime_with_wave_context(
        sat_history,
        iteration_count,
        field_coherences=field_coherences
    )

    print(f"   Wave-aware regime: {wave_aware.regime.value}")
    print(f"   Reasoning: {wave_aware.reasoning}")

    # Should be STABLE, not COMMITTED
    assert wave_aware.regime == SatisfactionRegime.STABLE
    assert "coherence" in wave_aware.reasoning.lower()
    print("✅ test_low_coherence_prevents_committed passed")


if __name__ == "__main__":
    print("="*70)
    print("🧪 Satisfaction Regime Classification Tests")
    print("="*70)
    print("\n📊 PART 1: Basic Regime Classification (FFITTSS V0 style)")
    print("-"*70)
    test_initializing_regime()
    test_committed_regime()
    test_exploring_regime()
    test_converging_regime()
    test_plateaued_regime()
    test_regime_statistics()

    print("\n"+"="*70)
    print("🌀 PART 2: DAE 3.0 Wave Training Integration")
    print("-"*70)
    test_wave_training_integration()
    test_high_spatial_variance_prevents_committed()
    test_low_coherence_prevents_committed()

    print("\n"+"="*70)
    print("✅ All tests passed!")
    print("="*70)
    print("\n📊 Regime Classification System Ready:")
    print("   - 6 regimes: INITIALIZING → EXPLORING → CONVERGING → STABLE → COMMITTED → PLATEAUED")
    print("   - Evolution rates: 0.1 (cautious) → 1.0 (aggressive)")
    print("   - FFITTSS target: 86.2% COMMITTED")
    print("\n🌀 DAE 3.0 Integration Complete:")
    print("   - Wave training phase awareness (EXPANSIVE → NAVIGATION → CONCRESCENCE)")
    print("   - Spatial satisfaction variance (IQR from per-position organ fusion)")
    print("   - Field coherence (organ balance from satisfaction_calculator.py)")
    print("   - Prevents premature commitment with high variance or low coherence")
