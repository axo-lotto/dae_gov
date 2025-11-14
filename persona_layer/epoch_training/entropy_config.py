"""
Entropy Configuration - Regime-Adaptive Exploration
====================================================

Centralized configuration for adding controlled non-determinism to enable
authentic voice development and per-user language learning.

## Phase 1: Surface Entropy (SAFE)
- Phrase selection: Softmax sampling instead of random.choice
- Strategy selection: Probabilistic weighting instead of MAX
- Regime-adaptive: More exploration early, less when committed

## Design Principles:
1. **Regime-Adaptive**: Exploration inversely proportional to commitment
2. **Safety-Gated**: No exploration during crisis (NDAM urgency > 0.7)
3. **Organic**: Respects Hebbian strengths (doesn't override learning)
4. **Gradual**: EXPLORING → CONVERGING → COMMITTED (0.30 → 0.12 → 0.01)

## Integration with Multi-Iteration Training:
- Early iterations: High exploration (discover voice)
- Middle iterations: Moderate exploration (refine patterns)
- Late iterations: Low exploration (stabilize identity)

Author: DAE_HYPHAE_1 Persona Layer
Date: November 13, 2025
Phase: 1 (Surface Entropy)
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum

try:
    from .satisfaction_regime import SatisfactionRegime
except ImportError:
    # Fallback if running as script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from satisfaction_regime import SatisfactionRegime


@dataclass
class EntropyConfig:
    """Configuration for regime-adaptive entropy."""

    # Phase 1: Surface Entropy (phrase/strategy selection)
    enable_phrase_exploration: bool = True
    enable_strategy_exploration: bool = True

    # Regime-to-exploration mapping
    # Higher = more random exploration, Lower = more Hebbian/deterministic
    exploration_by_regime: Dict[str, float] = None

    # Softmax temperature for phrase selection
    # Higher = more uniform, Lower = more peaked
    softmax_temperature_base: float = 1.0

    # Strategy selection weights (baseline before exploration)
    strategy_weights_baseline: Dict[str, float] = None

    # Safety gates
    crisis_urgency_threshold: float = 0.7  # NDAM urgency above this = no exploration
    crisis_zone_threshold: int = 5  # Crisis zone 5+ = no exploration

    # Phase 2/3 (Future - disabled by default)
    enable_core_semantic_exploration: bool = False  # Nexus threshold noise
    enable_deep_coupling_exploration: bool = False  # R-matrix perturbation

    def __post_init__(self):
        """Set default mappings if not provided."""
        if self.exploration_by_regime is None:
            self.exploration_by_regime = {
                'INITIALIZING': 0.20,  # Moderate exploration (warming up)
                'EXPLORING': 0.30,     # High exploration (active discovery)
                'CONVERGING': 0.12,    # Low exploration (homing in)
                'STABLE': 0.05,        # Very low exploration (found optimum)
                'COMMITTED': 0.01,     # Minimal exploration (sustained success)
                'PLATEAUED': 0.25,     # High exploration (escape local minimum)
            }

        if self.strategy_weights_baseline is None:
            # Default strategy preferences (before exploration noise)
            self.strategy_weights_baseline = {
                'intersection': 0.60,  # Prefer nexus intersection (most coherent)
                'direct': 0.30,        # Allow direct reconstruction (backup)
                'fusion': 0.10,        # Rare fusion (experimental)
            }

    def get_exploration_factor(
        self,
        regime: Optional[SatisfactionRegime] = None,
        regime_str: Optional[str] = None,
        ndam_urgency: float = 0.0,
        crisis_zone: int = 0
    ) -> float:
        """
        Get exploration factor for current regime with safety gates.

        Args:
            regime: SatisfactionRegime enum
            regime_str: Regime as string (alternative)
            ndam_urgency: NDAM urgency level (0-1)
            crisis_zone: Crisis zone (1-5)

        Returns:
            Exploration factor (0.0 = deterministic, 0.3 = high exploration)
        """
        # Safety gates
        if ndam_urgency > self.crisis_urgency_threshold:
            return 0.0  # No exploration during crisis

        if crisis_zone >= self.crisis_zone_threshold:
            return 0.0  # No exploration in crisis zones

        # Get regime key
        if regime is not None:
            regime_key = regime.value
        elif regime_str is not None:
            regime_key = regime_str
        else:
            regime_key = 'EXPLORING'  # Default

        return self.exploration_by_regime.get(regime_key, 0.15)

    def get_softmax_temperature(
        self,
        exploration_factor: float
    ) -> float:
        """
        Convert exploration factor to softmax temperature.

        Higher exploration → higher temperature → more uniform sampling
        Lower exploration → lower temperature → more peaked (Hebbian-biased)

        Args:
            exploration_factor: 0.0-0.3 (from get_exploration_factor)

        Returns:
            Temperature for softmax (0.1 = very peaked, 2.0 = very uniform)
        """
        # Map exploration_factor to temperature
        # 0.0 → 0.1 (deterministic, use strongest Hebbian)
        # 0.3 → 2.0 (uniform, explore all phrases equally)
        min_temp = 0.1
        max_temp = 2.0

        # Linear scaling
        temperature = min_temp + (exploration_factor / 0.3) * (max_temp - min_temp)

        return temperature

    def get_strategy_weights(
        self,
        exploration_factor: float
    ) -> Dict[str, float]:
        """
        Get strategy weights with exploration noise.

        Args:
            exploration_factor: 0.0-0.3

        Returns:
            Dict with strategy weights (sum to 1.0)
        """
        import numpy as np

        if not self.enable_strategy_exploration or exploration_factor < 0.01:
            # No exploration, return baseline
            return self.strategy_weights_baseline.copy()

        # Add uniform noise proportional to exploration_factor
        weights = {}
        noise_scale = exploration_factor

        for strategy, baseline_weight in self.strategy_weights_baseline.items():
            # Add Gaussian noise
            noise = np.random.randn() * noise_scale * 0.2  # Scale noise
            noisy_weight = baseline_weight + noise
            weights[strategy] = max(0.05, noisy_weight)  # Keep positive

        # Normalize to sum to 1.0
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}

        return weights


# Default configuration
DEFAULT_ENTROPY_CONFIG = EntropyConfig()


# Quick test
if __name__ == "__main__":
    print("="*70)
    print("🎲 ENTROPY CONFIGURATION TEST")
    print("="*70)

    config = EntropyConfig()

    print("\n📊 Exploration Factors by Regime:")
    for regime in ['INITIALIZING', 'EXPLORING', 'CONVERGING', 'STABLE', 'COMMITTED', 'PLATEAUED']:
        factor = config.get_exploration_factor(regime_str=regime)
        temp = config.get_softmax_temperature(factor)
        print(f"   {regime:15s}: exploration={factor:.2f}, temperature={temp:.2f}")

    print("\n🚨 Safety Gates:")
    print(f"   Crisis (urgency=0.8): exploration={config.get_exploration_factor(regime_str='EXPLORING', ndam_urgency=0.8):.2f}")
    print(f"   Crisis (zone=5): exploration={config.get_exploration_factor(regime_str='EXPLORING', crisis_zone=5):.2f}")
    print(f"   Safe (urgency=0.3, zone=2): exploration={config.get_exploration_factor(regime_str='EXPLORING', ndam_urgency=0.3, crisis_zone=2):.2f}")

    print("\n🎯 Strategy Weights (EXPLORING regime):")
    factor = config.get_exploration_factor(regime_str='EXPLORING')
    weights = config.get_strategy_weights(factor)
    for strategy, weight in weights.items():
        print(f"   {strategy:15s}: {weight:.3f}")

    print("\n✅ Entropy configuration ready!")
    print("\n🌀 Phase 1 Surface Entropy:")
    print("   - Regime-adaptive exploration schedule")
    print("   - Safety gates for crisis contexts")
    print("   - Softmax phrase sampling (temperature-controlled)")
    print("   - Probabilistic strategy selection")
    print("   - Organic (respects Hebbian strengths)")
