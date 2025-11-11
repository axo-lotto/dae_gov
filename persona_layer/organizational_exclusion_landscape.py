"""
Organizational Fractal Exclusion Landscape (OFEL)

Adapted from FFITTSS v0 T0 exclusion_landscape.py for trauma-informed organizational safety.

Key Differences from FFITTSS:
- FFITTSS: Palette boundaries, spatial boundaries, local variance
- DAE-GOV: Polyvagal safety, IFS part protection, SELF-distance guidance

Mathematical Framework:
    E_org(x) = α·E_polyvagal + β·E_parts + γ·E_SELF

Where:
    E_polyvagal: Distance to unsafe nervous system states (dorsal shutdown)
    E_parts: Risk of triggering exiles without SELF-energy
    E_SELF: Distance from core SELF orbit [0.0-0.15]

Tier Compliance:
- T0-equivalent: Pre-processing safety constraints (no semantic interpretation)
- Read-only: Computes penalty field, doesn't modify organism state
- TSK-compatible: Returns structured dict for genealogy logging

Source:
- FFITTSS v0 Phase 8B (exclusion_landscape.py)
- DAE 3.0 Felt Intelligence Foundations (transductive signaling space)
- DAE-GOV SELF Matrix Mathematical Addendum (d_SELF function)

Author: DAE-GOV Development Team
Date: November 10, 2025
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class OrganizationalExclusionLandscape:
    """
    Organizational exclusion penalty field for trauma-informed safety.

    Fields:
        field: Exclusion penalty E_org(x) ∈ [0,1]
        components: Breakdown {E_polyvagal, E_parts, E_SELF}
        stats: Field statistics for TSK logging
        safety_level: Categorical safety assessment
    """
    field: float  # Scalar [0,1] (not spatial, but conversational moment)
    components: Dict[str, float]
    stats: Dict[str, Any]
    safety_level: str  # "SAFE", "CAUTION", "DANGER"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to TSK-compatible dictionary."""
        return {
            'field_value': float(self.field),
            'safety_level': self.safety_level,
            'components': self.components,
            'stats': self.stats
        }


class OrganizationalFELComputer:
    """
    Compute organizational exclusion landscape for conversational safety.

    Adapted from FFITTSS FEL but operates on:
    - Text embeddings (384-dim) instead of grids
    - Polyvagal states instead of palette boundaries
    - IFS parts instead of spatial boundaries
    - SELF-distance instead of local variance
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize OFEL computer with trauma-informed configuration.

        Args:
            config: Optional configuration with keys:
                - alpha: Polyvagal weight (default 0.4)
                - beta: IFS part weight (default 0.3)
                - gamma: SELF-distance weight (default 0.3)
                - danger_threshold: E_org > threshold → DANGER (default 0.7)
                - caution_threshold: E_org > threshold → CAUTION (default 0.3)
        """
        self.config = config or {}
        self.alpha = self.config.get('alpha', 0.4)
        self.beta = self.config.get('beta', 0.3)
        self.gamma = self.config.get('gamma', 0.3)

        self.danger_threshold = self.config.get('danger_threshold', 0.7)
        self.caution_threshold = self.config.get('caution_threshold', 0.3)

        # Polyvagal state mappings (from EO organ)
        self.polyvagal_penalties = {
            'ventral': 0.0,      # Safe, connected, curious
            'sympathetic': 0.3,  # Fight/flight, mobilized
            'dorsal': 0.8,       # Shutdown, freeze, dissociation
            'mixed': 0.5,        # Mixed states (e.g., freeze + rage)
            'unknown': 0.4       # Default if unclear
        }

        # IFS part risk mappings (from BOND organ)
        self.part_risk_profiles = {
            'SELF': 0.0,          # Core SELF = maximum safety
            'manager': 0.2,       # Protective parts, mild caution
            'firefighter': 0.4,   # Reactive protectors, moderate caution
            'exile': 0.9,         # Wounded parts WITHOUT SELF = high risk
            'exile_with_SELF': 0.1,  # Exile WITH SELF = safe to witness
            'unknown': 0.3        # Default if unclear
        }

    def compute_polyvagal_exclusion(
        self,
        polyvagal_state: str,
        coherence: float
    ) -> float:
        """
        Compute polyvagal exclusion penalty E_polyvagal.

        Principle: Avoid responses that push toward dorsal shutdown.

        Args:
            polyvagal_state: "ventral", "sympathetic", "dorsal", "mixed", "unknown"
            coherence: Confidence in state classification [0,1]

        Returns:
            E_polyvagal ∈ [0,1]

        Formula:
            E_polyvagal = base_penalty × coherence_adjustment

            where coherence_adjustment = 1.0 if coherence ≥ 0.7
                                       = 0.5 if coherence < 0.7 (uncertain state)

        Example:
            >>> compute_polyvagal_exclusion("dorsal", coherence=0.8)
            0.8  # High penalty, high confidence

            >>> compute_polyvagal_exclusion("dorsal", coherence=0.4)
            0.4  # High penalty, low confidence → reduced
        """
        base_penalty = self.polyvagal_penalties.get(
            polyvagal_state.lower(),
            self.polyvagal_penalties['unknown']
        )

        # Coherence adjustment: Only apply full penalty if confident
        if coherence >= 0.7:
            adjustment = 1.0
        elif coherence >= 0.4:
            adjustment = 0.7
        else:
            adjustment = 0.5  # Low confidence → reduce penalty

        return base_penalty * adjustment

    def compute_ifs_part_exclusion(
        self,
        active_parts: List[str],
        self_energy: float
    ) -> float:
        """
        Compute IFS part protection penalty E_parts.

        Principle: Avoid triggering exiles without SELF-energy present.

        Args:
            active_parts: List of detected parts ["manager", "exile", etc.]
            self_energy: SELF-energy level [0,1] (= 1 - d_SELF)

        Returns:
            E_parts ∈ [0,1]

        Formula:
            If 'exile' in parts AND self_energy < 0.6:
                E_parts = 0.9  # DANGER: Exile without SELF
            Elif 'exile' in parts AND self_energy ≥ 0.6:
                E_parts = 0.1  # SAFE: SELF present to witness
            Elif 'SELF' in parts:
                E_parts = 0.0  # SAFE: SELF-led
            Else:
                E_parts = max(part_penalties)  # Manager/firefighter

        Example:
            >>> compute_ifs_part_exclusion(["exile"], self_energy=0.4)
            0.9  # DANGER: Exile without SELF

            >>> compute_ifs_part_exclusion(["exile", "SELF"], self_energy=0.75)
            0.1  # SAFE: SELF present to witness exile
        """
        if not active_parts:
            return self.part_risk_profiles['unknown']

        # Convert to lowercase for matching
        parts_lower = [p.lower() for p in active_parts]

        # Check for exile without SELF
        if 'exile' in parts_lower:
            if self_energy >= 0.6:
                # SAFE: SELF-energy present to witness exile
                return self.part_risk_profiles['exile_with_SELF']
            else:
                # DANGER: Exile without SELF = trauma risk
                return self.part_risk_profiles['exile']

        # Check for SELF-led state
        if 'self' in parts_lower:
            return self.part_risk_profiles['SELF']

        # Manager/firefighter protection
        penalties = []
        for part in parts_lower:
            if part in self.part_risk_profiles:
                penalties.append(self.part_risk_profiles[part])

        if penalties:
            return max(penalties)  # Take highest risk
        else:
            return self.part_risk_profiles['unknown']

    def compute_self_distance_exclusion(
        self,
        self_distance: float
    ) -> float:
        """
        Compute SELF-distance exclusion penalty E_SELF.

        Principle: Guide responses toward core SELF orbit [0.0-0.15].

        Args:
            self_distance: Distance from core SELF [0,1]
                From SELF Matrix: d_SELF = clip(base + modifier, 0, 1)

        Returns:
            E_SELF ∈ [0,1]

        Formula (piecewise linear):
            d_SELF ∈ [0.00, 0.15]: E_SELF = 0.0  (Core SELF Orbit)
            d_SELF ∈ (0.15, 0.35]: E_SELF = 0.2  (Sustainable Orbit)
            d_SELF ∈ (0.35, 0.60]: E_SELF = 0.6  (Shadow/Compost Edge)
            d_SELF ∈ (0.60, 1.00]: E_SELF = 0.9  (Deep Exile)

        From SELF Matrix zones:
            Core SELF:       0.00-0.15 (clarity, compassion, curiosity)
            Sustainable:     0.15-0.35 (working SELF, engaged)
            Shadow/Compost:  0.35-0.60 (unintegrated, needs witnessing)
            Deep Exile:      0.60+     (severe wounding, high protection)

        Example:
            >>> compute_self_distance_exclusion(0.10)
            0.0  # Core SELF - no exclusion

            >>> compute_self_distance_exclusion(0.50)
            0.6  # Shadow zone - moderate exclusion
        """
        if self_distance <= 0.15:
            return 0.0  # Core SELF Orbit
        elif self_distance <= 0.35:
            return 0.2  # Sustainable Orbit
        elif self_distance <= 0.60:
            return 0.6  # Shadow/Compost Edge
        else:
            return 0.9  # Deep Exile

    def compute_organizational_fel(
        self,
        polyvagal_state: str,
        active_parts: List[str],
        self_distance: float,
        coherence: float
    ) -> OrganizationalExclusionLandscape:
        """
        Compute complete organizational FEL (main entry point).

        Args:
            polyvagal_state: "ventral", "sympathetic", "dorsal", etc.
            active_parts: List of IFS parts ["manager", "exile", etc.]
            self_distance: Distance from core SELF [0,1]
            coherence: Organ agreement on polyvagal state [0,1]

        Returns:
            OrganizationalExclusionLandscape with field, components, stats

        Formula:
            E_org(x) = α·E_polyvagal + β·E_parts + γ·E_SELF

        Coefficients (trauma-informed weighting):
            α = 0.4  (polyvagal safety primary)
            β = 0.3  (part protection secondary)
            γ = 0.3  (SELF-energy guidance tertiary)

        Safety Levels:
            E_org < 0.3: SAFE (proceed with full 8 C's)
            0.3 ≤ E_org < 0.7: CAUTION (gentle, validating)
            E_org ≥ 0.7: DANGER (containment only)

        Example:
            >>> compute_organizational_fel(
            ...     polyvagal_state="dorsal",
            ...     active_parts=["exile"],
            ...     self_distance=0.65,
            ...     coherence=0.8
            ... )
            OrganizationalExclusionLandscape(
                field=0.84,  # High exclusion
                safety_level="DANGER",
                ...
            )
        """
        # Compute component exclusions
        self_energy = 1.0 - self_distance

        E_polyvagal = self.compute_polyvagal_exclusion(
            polyvagal_state, coherence
        )
        E_parts = self.compute_ifs_part_exclusion(
            active_parts, self_energy
        )
        E_SELF = self.compute_self_distance_exclusion(self_distance)

        # Combine with weights
        E_field = (
            self.alpha * E_polyvagal +
            self.beta * E_parts +
            self.gamma * E_SELF
        )

        # Clamp to [0, 1]
        E_field = np.clip(E_field, 0.0, 1.0)

        # Determine safety level
        if E_field >= self.danger_threshold:
            safety_level = "DANGER"
        elif E_field >= self.caution_threshold:
            safety_level = "CAUTION"
        else:
            safety_level = "SAFE"

        # Build components dict
        components = {
            'E_polyvagal': float(E_polyvagal),
            'E_parts': float(E_parts),
            'E_SELF': float(E_SELF),
            'E_combined': float(E_field)
        }

        # Build stats dict
        stats = {
            'polyvagal_state': polyvagal_state,
            'active_parts': active_parts,
            'self_distance': float(self_distance),
            'self_energy': float(self_energy),
            'coherence': float(coherence),
            'alpha': self.alpha,
            'beta': self.beta,
            'gamma': self.gamma
        }

        return OrganizationalExclusionLandscape(
            field=E_field,
            components=components,
            stats=stats,
            safety_level=safety_level
        )


def format_ofel_summary(ofel: OrganizationalExclusionLandscape) -> str:
    """
    Format OFEL for human-readable display.

    Args:
        ofel: OrganizationalExclusionLandscape object

    Returns:
        Formatted string summary

    Example:
        >>> print(format_ofel_summary(ofel))
        === Organizational Exclusion Landscape ===

        Safety Level: CAUTION
        Field Value: 0.45

        Component Breakdown:
          E_polyvagal: 0.30 (sympathetic activation)
          E_parts:     0.40 (firefighter protective)
          E_SELF:      0.60 (shadow zone)
        ...
    """
    lines = []
    lines.append("=== Organizational Exclusion Landscape ===")
    lines.append("")

    # Safety assessment
    safety_emoji = {
        'SAFE': '✅',
        'CAUTION': '⚠️',
        'DANGER': '🚨'
    }
    emoji = safety_emoji.get(ofel.safety_level, '❓')
    lines.append(f"Safety Level: {emoji} {ofel.safety_level}")
    lines.append(f"Field Value: {ofel.field:.2f}")
    lines.append("")

    # Component breakdown
    lines.append("Component Breakdown:")
    lines.append(f"  E_polyvagal: {ofel.components['E_polyvagal']:.2f} ({ofel.stats['polyvagal_state']})")
    lines.append(f"  E_parts:     {ofel.components['E_parts']:.2f} ({', '.join(ofel.stats['active_parts'])})")
    lines.append(f"  E_SELF:      {ofel.components['E_SELF']:.2f} (d_SELF={ofel.stats['self_distance']:.2f})")
    lines.append("")

    # Weights
    lines.append("Component Weights:")
    lines.append(f"  α (polyvagal): {ofel.stats['alpha']:.2f}")
    lines.append(f"  β (parts):     {ofel.stats['beta']:.2f}")
    lines.append(f"  γ (SELF):      {ofel.stats['gamma']:.2f}")
    lines.append("")

    # Guidance
    lines.append("Guidance:")
    if ofel.safety_level == "SAFE":
        lines.append("  ✅ Proceed with full 8 C's engagement")
        lines.append("  ✅ Can explore, challenge gently, go deeper")
    elif ofel.safety_level == "CAUTION":
        lines.append("  ⚠️ Gentle, validating responses only")
        lines.append("  ⚠️ Avoid challenging or going deeper")
        lines.append("  ⚠️ Use Compassion + Courage")
    else:  # DANGER
        lines.append("  🚨 CONTAINMENT ONLY")
        lines.append("  🚨 Acknowledge what's here without exploration")
        lines.append("  🚨 Suggest external support if needed")

    return "\n".join(lines)


# Quick utility functions for common use cases
def quick_safety_check(
    polyvagal_state: str,
    ifs_part: str,
    self_energy: float,
    coherence: float = 0.8
) -> str:
    """
    Quick safety check returning just the safety level.

    Convenience function for rapid assessment.

    Args:
        polyvagal_state: "ventral", "sympathetic", "dorsal"
        ifs_part: "SELF", "manager", "firefighter", "exile"
        self_energy: SELF-energy [0,1] (= 1 - d_SELF)
        coherence: Confidence [0,1] (default 0.8)

    Returns:
        "SAFE", "CAUTION", or "DANGER"

    Example:
        >>> quick_safety_check("dorsal", "exile", self_energy=0.3)
        "DANGER"
    """
    computer = OrganizationalFELComputer()
    self_distance = 1.0 - self_energy

    ofel = computer.compute_organizational_fel(
        polyvagal_state=polyvagal_state,
        active_parts=[ifs_part] if ifs_part else [],
        self_distance=self_distance,
        coherence=coherence
    )

    return ofel.safety_level
