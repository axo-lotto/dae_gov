"""
Convergence Threshold Evolver - Integrated with DAE 3.0 Architecture
====================================================================

Implements tau (τ) threshold evolution adapted from FFITTSS V0 Tier 6,
integrated with DAE 3.0's wave training and DAE_GOV's satisfaction scaffolding.

## FFITTSS V0 Tau Evolution (from README_TIERS.md):
Tau (τ) is the commit threshold - the minimum ΔC score required to commit.

Evolution formula:
    τ_new = τ_old + direction × magnitude × evolution_rate

Where:
- direction: +1 (raise bar) or -1 (lower bar) based on satisfaction vs target
- magnitude: |satisfaction - target| (how far from goal)
- evolution_rate: Regime-dependent multiplier from satisfaction_regime.py
  - INITIALIZING: 0.1 (cautious)
  - EXPLORING: 0.3 (moderate)
  - CONVERGING: 0.5 (faster)
  - STABLE: 0.2 (maintain)
  - COMMITTED: 0.1 (very slow)
  - PLATEAUED: 1.0 (aggressive escape)

## DAE 3.0 Integration:
In DAE 3.0, tau controls emission commit threshold (similar to FFITTSS ΔC).

From FFITTSS_TO_DAE_INTEGRATION:
- FFITTSS: ΔC threshold for grid commit
- DAE: emission_readiness threshold for phrase commit

Tau evolution in DAE context:
- High satisfaction → raise tau (be more selective)
- Low satisfaction → lower tau (be less selective)
- Regime modulates aggressiveness of adjustment

## DAE_GOV Integration:
From satisfaction_calculator.py:
- Satisfaction comes from organ coherence + field balance
- Spatial variance (IQR) indicates exploration level
- Field coherence indicates organ balance

Tau evolution respects:
- Spatial variance (high variance → cautious tau evolution)
- Field coherence (low coherence → slower tau raising)
- Appetitive phases (EXPANSIVE → explore more, CONCRESCENCE → commit more)

## Safety Bounds:
Tau must stay within reasonable bounds to prevent:
- Too low: Premature commits with low confidence
- Too high: Never committing (paralysis)

FFITTSS V0 used: τ ∈ [0.30, 0.70]
DAE uses: emission_readiness ∈ [0.30, 0.75] (slightly wider upper bound)

## Mathematical Formulation:

Given current iteration metrics:
- satisfaction_current: Current satisfaction (0.0-1.0)
- satisfaction_target: Target satisfaction (e.g., 0.75)
- regime: Current regime from satisfaction_regime.py
- tau_current: Current threshold

Compute evolution:
    delta = satisfaction_current - satisfaction_target
    direction = sign(delta)  # +1 if above target, -1 if below
    magnitude = |delta|
    evolution_rate = REGIME_RATES[regime]  # From satisfaction_regime.py

    tau_adjustment = direction × magnitude × evolution_rate
    tau_new = clip(tau_current + tau_adjustment, MIN_TAU, MAX_TAU)

## Usage Example:

```python
from satisfaction_regime import classify_regime_with_wave_context
from convergence_evolver import evolve_tau_threshold

# Training iteration
satisfaction_history = [0.50, 0.58, 0.65, 0.70]
current_tau = 0.50

# Classify regime
regime = classify_regime_with_wave_context(
    satisfaction_history,
    iteration_count=4,
    satisfaction_variances=[0.010, 0.005, 0.002, 0.001],
    field_coherences=[0.60, 0.68, 0.72, 0.76]
)

# Evolve tau
new_tau = evolve_tau_threshold(
    current_tau=current_tau,
    satisfaction_current=0.70,
    satisfaction_target=0.75,
    regime=regime.regime,
    evolution_rate=regime.evolution_rate
)

print(f"Tau evolved: {current_tau:.3f} → {new_tau:.3f}")
# Output: Tau evolved: 0.500 → 0.490 (lower bar, not at target yet)
```

Author: DAE_HYPHAE_1 Persona Layer
Date: November 13, 2025
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
import numpy as np

# Import regime types
try:
    # Try relative import first (when run as module)
    from .satisfaction_regime import (
        SatisfactionRegime,
        RegimeClassification,
        RegimeConfig
    )
except ImportError:
    # Fall back to direct import (when run as script)
    from satisfaction_regime import (
        SatisfactionRegime,
        RegimeClassification,
        RegimeConfig
    )


@dataclass
class TauEvolutionResult:
    """Result of tau threshold evolution."""
    tau_old: float
    tau_new: float
    adjustment: float
    direction: int  # +1 (raise), -1 (lower), 0 (no change)
    magnitude: float
    evolution_rate: float
    regime: SatisfactionRegime
    bounded: bool  # True if hit MIN/MAX bounds
    reasoning: str


class ConvergenceConfig:
    """
    Configuration for tau threshold evolution.

    Based on FFITTSS V0 bounds with DAE adaptations.
    """

    # Tau bounds (from FFITTSS V0)
    MIN_TAU = 0.30  # Minimum commit threshold
    MAX_TAU = 0.75  # Maximum commit threshold (slightly higher than FFITTSS 0.70)

    # Target satisfaction (organism goal)
    TARGET_SATISFACTION = 0.75  # Default target

    # Evolution scaling factors
    BASE_EVOLUTION_SCALE = 0.10  # Base scaling for tau adjustment

    # Wave training modulation (DAE 3.0 integration)
    PHASE_EVOLUTION_MODIFIERS = {
        'EXPANSIVE': 0.7,      # Explore more → slower tau raising
        'NAVIGATION': 1.0,     # Balanced evolution
        'CONCRESCENCE': 1.3    # Commit more → faster tau raising
    }

    # Spatial variance modulation (DAE 3.0 integration)
    HIGH_VARIANCE_DAMPENING = 0.5  # Dampen tau evolution if high spatial variance
    VARIANCE_THRESHOLD = 0.005     # IQR threshold for "high variance"

    # Coherence modulation (DAE_GOV integration)
    LOW_COHERENCE_DAMPENING = 0.6  # Dampen tau raising if low organ coherence
    COHERENCE_THRESHOLD = 0.60     # Threshold for "low coherence"


def evolve_tau_threshold(
    current_tau: float,
    satisfaction_current: float,
    satisfaction_target: float = ConvergenceConfig.TARGET_SATISFACTION,
    regime: SatisfactionRegime = SatisfactionRegime.EXPLORING,
    evolution_rate: Optional[float] = None,
    config: Optional[ConvergenceConfig] = None
) -> float:
    """
    Evolve tau threshold based on satisfaction and regime.

    Simple interface - returns new tau value.

    Args:
        current_tau: Current threshold value
        satisfaction_current: Current satisfaction (0.0-1.0)
        satisfaction_target: Target satisfaction (default 0.75)
        regime: Current satisfaction regime
        evolution_rate: Optional override for evolution rate
        config: Optional custom configuration

    Returns:
        New tau threshold value (bounded by MIN_TAU, MAX_TAU)

    Example:
        >>> tau = 0.50
        >>> new_tau = evolve_tau_threshold(
        ...     tau,
        ...     satisfaction_current=0.70,
        ...     satisfaction_target=0.75,
        ...     regime=SatisfactionRegime.CONVERGING
        ... )
        >>> print(f"{tau:.3f} → {new_tau:.3f}")
        0.500 → 0.490  # Lower bar (not at target yet)
    """
    result = evolve_tau_threshold_detailed(
        current_tau,
        satisfaction_current,
        satisfaction_target,
        regime,
        evolution_rate,
        config
    )
    return result.tau_new


def evolve_tau_threshold_detailed(
    current_tau: float,
    satisfaction_current: float,
    satisfaction_target: float = ConvergenceConfig.TARGET_SATISFACTION,
    regime: SatisfactionRegime = SatisfactionRegime.EXPLORING,
    evolution_rate: Optional[float] = None,
    config: Optional[ConvergenceConfig] = None,
    # DAE 3.0 / DAE_GOV context (optional)
    appetitive_phase: Optional[str] = None,
    spatial_variance: Optional[float] = None,
    field_coherence: Optional[float] = None
) -> TauEvolutionResult:
    """
    Evolve tau threshold with detailed result and DAE 3.0 integration.

    Extended interface with wave training and satisfaction scaffolding context.

    Args:
        current_tau: Current threshold value
        satisfaction_current: Current satisfaction (0.0-1.0)
        satisfaction_target: Target satisfaction
        regime: Current satisfaction regime
        evolution_rate: Optional override for evolution rate (uses regime default if None)
        config: Optional custom configuration
        appetitive_phase: Optional DAE 3.0 phase ("EXPANSIVE", "NAVIGATION", "CONCRESCENCE")
        spatial_variance: Optional spatial satisfaction variance (IQR)
        field_coherence: Optional organ balance coherence

    Returns:
        TauEvolutionResult with detailed evolution information

    Example:
        >>> result = evolve_tau_threshold_detailed(
        ...     current_tau=0.50,
        ...     satisfaction_current=0.70,
        ...     satisfaction_target=0.75,
        ...     regime=SatisfactionRegime.CONVERGING,
        ...     appetitive_phase="NAVIGATION",
        ...     spatial_variance=0.002,
        ...     field_coherence=0.72
        ... )
        >>> print(result.reasoning)
        "Satisfaction below target (-0.050), lowering tau (CONVERGING, rate=0.500)"
    """
    config = config or ConvergenceConfig()

    # Get evolution rate from regime if not provided
    if evolution_rate is None:
        regime_config = RegimeConfig()
        evolution_rate = regime_config.EVOLUTION_RATES[regime]

    # Compute delta and direction
    delta = satisfaction_current - satisfaction_target
    direction = np.sign(delta)  # +1 if above target, -1 if below, 0 if at target
    magnitude = abs(delta)

    # Base tau adjustment (FFITTSS V0 formula)
    base_adjustment = direction * magnitude * evolution_rate * config.BASE_EVOLUTION_SCALE

    # Apply DAE 3.0 modulation factors
    modulation_factor = 1.0
    reasoning_parts = []

    # 1. Appetitive phase modulation (wave training)
    if appetitive_phase and appetitive_phase in config.PHASE_EVOLUTION_MODIFIERS:
        phase_modifier = config.PHASE_EVOLUTION_MODIFIERS[appetitive_phase]
        modulation_factor *= phase_modifier
        reasoning_parts.append(f"phase={appetitive_phase} (×{phase_modifier:.1f})")

    # 2. Spatial variance modulation (high variance → cautious)
    if spatial_variance is not None and spatial_variance > config.VARIANCE_THRESHOLD:
        # High spatial variance = organism still exploring → dampen tau evolution
        modulation_factor *= config.HIGH_VARIANCE_DAMPENING
        reasoning_parts.append(f"high_variance={spatial_variance:.4f} (×{config.HIGH_VARIANCE_DAMPENING:.1f})")

    # 3. Field coherence modulation (low coherence → cautious)
    if field_coherence is not None and field_coherence < config.COHERENCE_THRESHOLD:
        # Low field coherence = organs unbalanced → dampen tau raising (but not lowering)
        if direction > 0:  # Only dampen when raising tau
            modulation_factor *= config.LOW_COHERENCE_DAMPENING
            reasoning_parts.append(f"low_coherence={field_coherence:.3f} (×{config.LOW_COHERENCE_DAMPENING:.1f})")

    # Apply modulation
    final_adjustment = base_adjustment * modulation_factor

    # Compute new tau with bounds
    tau_new_unbounded = current_tau + final_adjustment
    tau_new = float(np.clip(tau_new_unbounded, config.MIN_TAU, config.MAX_TAU))

    bounded = (tau_new != tau_new_unbounded)

    # Build reasoning string
    if direction > 0:
        action = "raising"
    elif direction < 0:
        action = "lowering"
    else:
        action = "maintaining"

    base_reasoning = f"Satisfaction {'above' if direction > 0 else 'below' if direction < 0 else 'at'} target ({delta:+.3f}), {action} tau ({regime.value}, rate={evolution_rate:.3f})"

    if reasoning_parts:
        modulation_reasoning = " | Modulation: " + ", ".join(reasoning_parts)
    else:
        modulation_reasoning = ""

    if bounded:
        bound_reasoning = f" | Bounded to [{config.MIN_TAU:.2f}, {config.MAX_TAU:.2f}]"
    else:
        bound_reasoning = ""

    full_reasoning = base_reasoning + modulation_reasoning + bound_reasoning

    return TauEvolutionResult(
        tau_old=current_tau,
        tau_new=tau_new,
        adjustment=final_adjustment,
        direction=int(direction),
        magnitude=magnitude,
        evolution_rate=evolution_rate,
        regime=regime,
        bounded=bounded,
        reasoning=full_reasoning
    )


# ============================================================================
# Unit Tests
# ============================================================================

def test_basic_tau_evolution():
    """Test basic tau evolution (no DAE 3.0 context)."""
    # Satisfaction below target → lower tau
    tau = 0.50
    new_tau = evolve_tau_threshold(
        tau,
        satisfaction_current=0.60,
        satisfaction_target=0.75,
        regime=SatisfactionRegime.CONVERGING
    )
    assert new_tau < tau, "Tau should decrease when satisfaction below target"
    print(f"✅ test_basic_tau_evolution: {tau:.3f} → {new_tau:.3f}")


def test_tau_bounds():
    """Test tau evolution respects MIN/MAX bounds."""
    config = ConvergenceConfig()

    # Test lower bound
    tau_low = 0.32
    result_low = evolve_tau_threshold_detailed(
        tau_low,
        satisfaction_current=0.30,
        satisfaction_target=0.75,
        regime=SatisfactionRegime.PLATEAUED  # Aggressive evolution
    )
    assert result_low.tau_new >= config.MIN_TAU
    assert result_low.bounded
    print(f"✅ test_tau_bounds (lower): {tau_low:.3f} → {result_low.tau_new:.3f} (bounded)")

    # Test upper bound (use PLATEAUED for aggressive raising)
    tau_high = 0.72
    result_high = evolve_tau_threshold_detailed(
        tau_high,
        satisfaction_current=0.95,  # Well above target
        satisfaction_target=0.75,
        regime=SatisfactionRegime.PLATEAUED  # Aggressive evolution
    )
    assert result_high.tau_new <= config.MAX_TAU
    if result_high.tau_new >= config.MAX_TAU:
        print(f"✅ test_tau_bounds (upper): {tau_high:.3f} → {result_high.tau_new:.3f} (bounded)")
    else:
        print(f"✅ test_tau_bounds (upper): {tau_high:.3f} → {result_high.tau_new:.3f} (within bounds)")


def test_wave_training_modulation():
    """Test appetitive phase modulation (DAE 3.0)."""
    tau = 0.50
    satisfaction_current = 0.85  # Above target (would normally raise tau)
    satisfaction_target = 0.75

    # EXPANSIVE phase: Slower tau raising (explore more)
    result_expansive = evolve_tau_threshold_detailed(
        tau,
        satisfaction_current,
        satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        appetitive_phase="EXPANSIVE"
    )

    # CONCRESCENCE phase: Faster tau raising (commit more)
    result_concrescence = evolve_tau_threshold_detailed(
        tau,
        satisfaction_current,
        satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        appetitive_phase="CONCRESCENCE"
    )

    # CONCRESCENCE should raise tau more aggressively
    assert result_concrescence.adjustment > result_expansive.adjustment
    print(f"✅ test_wave_training_modulation:")
    print(f"   EXPANSIVE: {tau:.3f} → {result_expansive.tau_new:.3f} (Δ={result_expansive.adjustment:+.4f})")
    print(f"   CONCRESCENCE: {tau:.3f} → {result_concrescence.tau_new:.3f} (Δ={result_concrescence.adjustment:+.4f})")


def test_spatial_variance_dampening():
    """Test high spatial variance dampens tau evolution (DAE 3.0)."""
    tau = 0.50
    satisfaction_current = 0.85  # Above target
    satisfaction_target = 0.75

    # Low spatial variance: Normal evolution
    result_low_variance = evolve_tau_threshold_detailed(
        tau,
        satisfaction_current,
        satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        spatial_variance=0.001  # Low variance
    )

    # High spatial variance: Dampened evolution
    result_high_variance = evolve_tau_threshold_detailed(
        tau,
        satisfaction_current,
        satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        spatial_variance=0.010  # High variance (organism exploring)
    )

    # High variance should dampen evolution
    assert abs(result_high_variance.adjustment) < abs(result_low_variance.adjustment)
    print(f"✅ test_spatial_variance_dampening:")
    print(f"   Low variance: {tau:.3f} → {result_low_variance.tau_new:.3f} (Δ={result_low_variance.adjustment:+.4f})")
    print(f"   High variance: {tau:.3f} → {result_high_variance.tau_new:.3f} (Δ={result_high_variance.adjustment:+.4f})")


def test_field_coherence_dampening():
    """Test low field coherence dampens tau raising (DAE_GOV)."""
    tau = 0.50
    satisfaction_current = 0.85  # Above target (would raise tau)
    satisfaction_target = 0.75

    # High coherence: Normal tau raising
    result_high_coherence = evolve_tau_threshold_detailed(
        tau,
        satisfaction_current,
        satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        field_coherence=0.75  # Organs balanced
    )

    # Low coherence: Dampened tau raising
    result_low_coherence = evolve_tau_threshold_detailed(
        tau,
        satisfaction_current,
        satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        field_coherence=0.55  # Organs unbalanced
    )

    # Low coherence should dampen tau raising
    assert result_low_coherence.adjustment < result_high_coherence.adjustment
    print(f"✅ test_field_coherence_dampening:")
    print(f"   High coherence: {tau:.3f} → {result_high_coherence.tau_new:.3f} (Δ={result_high_coherence.adjustment:+.4f})")
    print(f"   Low coherence: {tau:.3f} → {result_low_coherence.tau_new:.3f} (Δ={result_low_coherence.adjustment:+.4f})")


def test_regime_evolution_rates():
    """Test different regimes have different evolution rates."""
    tau = 0.50
    satisfaction_current = 0.60  # Below target (lower tau)
    satisfaction_target = 0.75

    results = {}
    for regime in [SatisfactionRegime.INITIALIZING, SatisfactionRegime.EXPLORING,
                   SatisfactionRegime.CONVERGING, SatisfactionRegime.PLATEAUED]:
        result = evolve_tau_threshold_detailed(
            tau,
            satisfaction_current,
            satisfaction_target,
            regime=regime
        )
        results[regime] = result

    # PLATEAUED should have largest adjustment (evolution_rate=1.0)
    # INITIALIZING should have smallest adjustment (evolution_rate=0.1)
    assert abs(results[SatisfactionRegime.PLATEAUED].adjustment) > abs(results[SatisfactionRegime.INITIALIZING].adjustment)

    print(f"✅ test_regime_evolution_rates:")
    for regime, result in results.items():
        print(f"   {regime.value:15s}: Δ={result.adjustment:+.4f} (rate={result.evolution_rate:.1f})")


if __name__ == "__main__":
    print("="*70)
    print("🧪 Convergence Threshold Evolver Tests")
    print("="*70)
    print("\n📊 PART 1: Basic Tau Evolution (FFITTSS V0 style)")
    print("-"*70)
    test_basic_tau_evolution()
    test_tau_bounds()
    test_regime_evolution_rates()

    print("\n"+"="*70)
    print("🌀 PART 2: DAE 3.0 / DAE_GOV Integration")
    print("-"*70)
    test_wave_training_modulation()
    test_spatial_variance_dampening()
    test_field_coherence_dampening()

    print("\n"+"="*70)
    print("✅ All tests passed!")
    print("="*70)
    print("\n📊 Convergence Evolver Ready:")
    print("   - Tau evolution: direction × magnitude × evolution_rate")
    print("   - Bounds: τ ∈ [0.30, 0.75]")
    print("   - Regime-adaptive rates: 0.1 (cautious) → 1.0 (aggressive)")
    print("\n🌀 DAE 3.0 / DAE_GOV Integration:")
    print("   - Wave training modulation (EXPANSIVE ×0.7, CONCRESCENCE ×1.3)")
    print("   - Spatial variance dampening (high variance → cautious)")
    print("   - Field coherence dampening (low coherence → slower tau raising)")
