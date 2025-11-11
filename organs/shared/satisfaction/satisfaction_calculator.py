"""
Shared Satisfaction Calculator
============================

Centralized satisfaction calculation for all modular organs.
Replaces duplicated satisfaction logic across legacy organs.

Implements:
- Organ-specific satisfaction calculation
- Vector35D integration
- Dynamic satisfaction calibration
- Pattern learning integration

Per 35D_IMPLEMENTATION_OCCASIONS.md: Shared utilities eliminate duplication
"""

from typing import Dict, Any, Optional, List
import numpy as np
from dataclasses import dataclass


@dataclass
class SatisfactionComponents:
    """Components used in satisfaction calculation"""
    intensity: float
    stability: float
    coherence: float
    enhancement_factor: float = 1.0
    vector35d_boost: float = 0.0


class SatisfactionCalculator:
    """
    Centralized satisfaction calculation for modular organ architecture
    """

    def __init__(self):
        # Organ-specific satisfaction formulas
        self.organ_formulas = {
            'semantic': self._calculate_semantic_satisfaction,
            'spatial': self._calculate_spatial_satisfaction,
            'archetypal': self._calculate_archetypal_satisfaction,
            'temporal': self._calculate_temporal_satisfaction,
            'constraint': self._calculate_constraint_satisfaction
        }

        # Base satisfaction parameters
        self.base_satisfaction_threshold = 0.5
        self.vector35d_enhancement_factor = 0.2
        self.stability_weight = 0.3

    def calculate_organ_coherence(self, intensity: float, stability: float,
                                organ_type: str, enhancement: Optional[Dict] = None) -> float:
        """
        Calculate coherence for an organ based on intensity, stability, and type

        Args:
            intensity: Primary processing intensity (0.0-1.0)
            stability: Pattern stability measure (0.0-1.0)
            organ_type: Type of organ ('semantic', 'spatial', etc.)
            enhancement: Optional Vector35D enhancement data

        Returns:
            Coherence value (0.0-1.0+)
        """

        # Get base satisfaction using organ-specific formula
        if organ_type in self.organ_formulas:
            base_satisfaction = self.organ_formulas[organ_type](intensity, stability)
        else:
            base_satisfaction = self._calculate_default_satisfaction(intensity, stability)

        # Apply enhancement if available
        enhancement_boost = 0.0
        if enhancement and enhancement.get('vector35d_enhancement'):
            enhancement_boost = self._calculate_vector35d_boost(enhancement, organ_type)

        # Calculate final coherence
        coherence = base_satisfaction + enhancement_boost

        # REMOVED: Coherence amplification for strong patterns
        # CRITICAL FIX #3 (Oct 26, 2025): REMOVE OVERCONFIDENCE REWARD
        #
        # BEFORE (BROKEN): if coherence > 0.8: coherence = coherence * 1.1
        # AFTER (FIXED): No amplification - high coherence should not be rewarded
        #
        # **Why This Was Breaking Metacognitive Calibration:**
        # - High coherence = organ overconfidence = likely wrong
        # - Amplifying it by 1.1x made the problem worse
        # - This fought against Fix #1 and Fix #2's inverse correlation
        #
        # **Impact of Removal:**
        # - High coherence tasks no longer get artificial boost
        # - Metacognitive compass can now properly detect overconfidence
        # - Expected: Better correlation with Fix #1 + Fix #2

        return min(coherence, 2.0)  # Cap at 2.0 for extreme cases

    def calculate_field_coherence(self, organ_coherences: Dict[str, float]) -> float:
        """
        Calculate overall field coherence from individual organ coherences

        Args:
            organ_coherences: Dictionary of organ_name -> coherence

        Returns:
            Overall field coherence
        """

        if not organ_coherences:
            return 0.0

        # Weighted average with emphasis on balanced activation
        coherences = list(organ_coherences.values())

        # Base field coherence
        field_coherence = sum(coherences) / len(coherences)

        # Bonus for balanced activation (all organs contributing)
        activation_balance = min(coherences) / max(coherences) if max(coherences) > 0 else 0
        balance_bonus = activation_balance * 0.1

        return field_coherence + balance_bonus

    def _calculate_semantic_satisfaction(self, intensity: float, stability: float) -> float:
        """SANS-specific satisfaction calculation"""

        # SANS prefers high intensity with moderate stability
        semantic_satisfaction = (
            intensity * 0.7 +           # Primary focus on semantic intensity
            stability * 0.3             # Secondary focus on stability
        )

        # SANS boost for consistent positive salience
        if intensity > 0.6 and stability > 0.5:
            semantic_satisfaction *= 1.15

        return semantic_satisfaction

    def _calculate_spatial_satisfaction(self, intensity: float, stability: float) -> float:
        """BOND-specific satisfaction calculation"""

        # BOND balances intensity and stability for spatial patterns
        spatial_satisfaction = (
            intensity * 0.6 +           # Spatial pattern strength
            stability * 0.4             # Spatial consistency
        )

        # BOND boost for strong spatial coherence
        if intensity > 0.7 and stability > 0.6:
            spatial_satisfaction *= 1.2

        return spatial_satisfaction

    def _calculate_archetypal_satisfaction(self, intensity: float, stability: float) -> float:
        """EO-specific satisfaction calculation"""

        # EO emphasizes intensity (archetypal recognition) over stability
        archetypal_satisfaction = (
            intensity * 0.8 +           # Strong archetypal lure intensity
            stability * 0.2             # Minimal stability requirement
        )

        # EO boost for strong archetypal patterns
        if intensity > 0.75:
            archetypal_satisfaction *= 1.25

        return archetypal_satisfaction

    def _calculate_temporal_satisfaction(self, intensity: float, stability: float) -> float:
        """RNX-specific satisfaction calculation"""

        # RNX balances pattern recognition with memory consistency
        temporal_satisfaction = (
            intensity * 0.5 +           # Pattern recognition intensity
            stability * 0.5             # Memory consistency
        )

        # RNX boost for stable temporal patterns
        if stability > 0.7:
            temporal_satisfaction *= 1.1

        return temporal_satisfaction

    def _calculate_constraint_satisfaction(self, intensity: float, stability: float) -> float:
        """NDAM-specific satisfaction calculation"""

        # NDAM prioritizes stability (constraint consistency)
        constraint_satisfaction = (
            intensity * 0.4 +           # Constraint detection intensity
            stability * 0.6             # Constraint stability
        )

        # NDAM boost for stable constraint patterns
        if stability > 0.8:
            constraint_satisfaction *= 1.1

        return constraint_satisfaction

    def _calculate_default_satisfaction(self, intensity: float, stability: float) -> float:
        """Default satisfaction for unknown organ types"""

        return (intensity + stability) / 2.0

    def _calculate_vector35d_boost(self, enhancement: Dict, organ_type: str) -> float:
        """Calculate Vector35D enhancement boost"""

        vector35d_data = enhancement.get('vector35d_enhancement', {})

        if not vector35d_data:
            return 0.0

        # Base boost from Vector35D presence
        base_boost = 0.05

        # Organ-specific Vector35D boost
        if organ_type == 'semantic' and vector35d_data.get('semantic_bundle_active'):
            bundle_boost = vector35d_data.get('enhancement_level', 0) * 0.15
            return base_boost + bundle_boost

        elif organ_type == 'spatial' and vector35d_data.get('spatial_bundle_active'):
            bundle_boost = vector35d_data.get('enhancement_level', 0) * 0.12
            return base_boost + bundle_boost

        elif organ_type == 'archetypal' and vector35d_data.get('creative_bundle_active'):
            bundle_boost = vector35d_data.get('enhancement_level', 0) * 0.18
            return base_boost + bundle_boost

        # General Vector35D boost for dimensional enhancement
        general_boost = vector35d_data.get('dimensional_enhancement', 0) * 0.08
        return base_boost + general_boost

    def get_satisfaction_diagnostics(self, organ_coherences: Dict[str, float]) -> Dict[str, Any]:
        """Get diagnostic information about satisfaction calculations"""

        if not organ_coherences:
            return {'error': 'No organ coherences provided'}

        field_coherence = self.calculate_field_coherence(organ_coherences)

        return {
            'field_coherence': field_coherence,
            'organ_coherences': organ_coherences,
            'highest_coherence_organ': max(organ_coherences.keys(), key=lambda k: organ_coherences[k]),
            'lowest_coherence_organ': min(organ_coherences.keys(), key=lambda k: organ_coherences[k]),
            'coherence_variance': np.var(list(organ_coherences.values())),
            'activation_balance': (min(organ_coherences.values()) / max(organ_coherences.values())
                                 if max(organ_coherences.values()) > 0 else 0),
            'organs_above_threshold': sum(1 for c in organ_coherences.values() if c > self.base_satisfaction_threshold)
        }