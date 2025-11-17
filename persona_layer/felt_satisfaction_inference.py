"""
Felt-Satisfaction Inference - Non-Invasive Mutual Satisfaction
===============================================================

Infers mutual satisfaction from organism's felt intelligence WITHOUT
requiring explicit user feedback. Uses existing scaffolding:
- Field coherence (organ harmony)
- V0 convergence (energy descent)
- Kairos detection (opportune moments)
- Emission quality (confidence, path)

Philosophy (Process):
- Satisfaction = quality of completion (not user rating)
- Inferred from organism's felt-state (not asked)
- Mutual = both organism AND user satisfied
- Non-invasive = no feedback prompts

Integration:
- Called POST-EMISSION by conversational_organism_wrapper
- Feeds into EntitySalienceTracker for urgency_context
- Replaces explicit user feedback (optional fallback)

Author: DAE_HYPHAE_1 + Claude Code
Date: November 17, 2025
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class FeltSatisfactionMetrics:
    """
    Inferred satisfaction from felt-state (non-invasive).

    Attributes:
        field_coherence: Organ harmony (1 - std([12 organs]))
        v0_descent: Energy reduction (1 - final_v0/initial_v0)
        kairos_detected: Opportune moment boolean
        emission_confidence: Emission quality (0.0-1.0)
        emission_path: "organic" / "felt_guided_llm" / "hebbian_fallback"

        # Computed
        inferred_satisfaction: Weighted composite (0.0-1.0)
        satisfaction_tier: "excellent" / "good" / "adequate" / "poor"
        confidence_level: How confident we are in inference
    """
    # Input metrics (from organism)
    field_coherence: float
    v0_descent: float
    kairos_detected: bool
    emission_confidence: float
    emission_path: str

    # Computed
    inferred_satisfaction: float = 0.0
    satisfaction_tier: str = "adequate"
    confidence_level: float = 0.0


class FeltSatisfactionInferencer:
    """
    Infer mutual satisfaction from organism's felt intelligence.

    Non-invasive alternative to explicit user feedback. Uses existing
    scaffolding from conversational_organism_wrapper:
    - Field coherence (already computed)
    - V0 convergence (already tracked)
    - Kairos detection (already detected)
    - Emission confidence (already known)

    Philosophy:
    - High field coherence → organs in harmony → good outcome
    - Low V0 (energy descent) → satisfactory completion
    - Kairos detected → opportune moment seized
    - Organic emission → authentic voice (not fallback)

    Integration Points:
    - POST-EMISSION: conversational_organism_wrapper
    - ENTITY SALIENCE: urgency_context for entity boosting
    - USER SUPERJECT: satisfaction trajectory learning
    """

    # Weights for composite satisfaction (tuned from DAE 3.0 empirical data)
    WEIGHT_FIELD_COHERENCE = 0.4  # Organ harmony (most important)
    WEIGHT_V0_DESCENT = 0.3        # Energy descent (second most)
    WEIGHT_KAIROS = 0.2            # Opportune moment (third)
    WEIGHT_EMISSION_CONF = 0.1     # Emission quality (least, already reflected in above)

    # Satisfaction tier thresholds
    TIER_EXCELLENT = 0.75  # Excellent conversation
    TIER_GOOD = 0.60       # Good conversation
    TIER_ADEQUATE = 0.45   # Adequate (baseline)
    # Below 0.45 = poor

    # Emission path quality modifiers
    PATH_QUALITY = {
        "organic": 1.2,              # Authentic voice (boost)
        "felt_guided_llm": 1.0,      # Baseline
        "hebbian_fallback": 0.7,     # Fallback (penalty)
        "direct_no_fusion": 0.8      # Direct without fusion
    }

    def __init__(self):
        """Initialize felt-satisfaction inferencer."""
        pass

    def infer_satisfaction(
        self,
        field_coherence: float,
        v0_initial: float,
        v0_final: float,
        kairos_detected: bool,
        emission_confidence: float,
        emission_path: str = "felt_guided_llm",
        active_organs: int = 12
    ) -> FeltSatisfactionMetrics:
        """
        Infer mutual satisfaction from felt-state metrics.

        Args:
            field_coherence: 1 - std([12 organs]) (0.0-1.0)
            v0_initial: Initial V0 appetition (typically 1.0)
            v0_final: Final V0 after convergence (0.0-1.0)
            kairos_detected: Was Kairos moment detected? (bool)
            emission_confidence: Emission generation confidence (0.0-1.0)
            emission_path: "organic" / "felt_guided_llm" / "hebbian_fallback"
            active_organs: Number of organs that participated (1-12)

        Returns:
            FeltSatisfactionMetrics with inferred_satisfaction
        """
        # Compute V0 descent (how much energy reduced)
        if v0_initial > 0:
            v0_descent = 1.0 - (v0_final / v0_initial)
        else:
            v0_descent = 0.0

        # Clamp to [0, 1]
        v0_descent = max(0.0, min(1.0, v0_descent))

        # Kairos as binary (0.0 or 1.0)
        kairos_score = 1.0 if kairos_detected else 0.0

        # Emission path quality modifier
        path_modifier = self.PATH_QUALITY.get(emission_path, 1.0)

        # Base satisfaction (weighted composite)
        base_satisfaction = (
            self.WEIGHT_FIELD_COHERENCE * field_coherence +
            self.WEIGHT_V0_DESCENT * v0_descent +
            self.WEIGHT_KAIROS * kairos_score +
            self.WEIGHT_EMISSION_CONF * emission_confidence
        )

        # Apply path quality modifier
        inferred_satisfaction = base_satisfaction * path_modifier

        # Clamp to [0, 1]
        inferred_satisfaction = max(0.0, min(1.0, inferred_satisfaction))

        # Determine satisfaction tier
        if inferred_satisfaction >= self.TIER_EXCELLENT:
            satisfaction_tier = "excellent"
        elif inferred_satisfaction >= self.TIER_GOOD:
            satisfaction_tier = "good"
        elif inferred_satisfaction >= self.TIER_ADEQUATE:
            satisfaction_tier = "adequate"
        else:
            satisfaction_tier = "poor"

        # Confidence in inference (based on organ participation)
        # More active organs → higher confidence in inference
        confidence_level = active_organs / 12.0

        # Build metrics
        metrics = FeltSatisfactionMetrics(
            field_coherence=field_coherence,
            v0_descent=v0_descent,
            kairos_detected=kairos_detected,
            emission_confidence=emission_confidence,
            emission_path=emission_path,
            inferred_satisfaction=inferred_satisfaction,
            satisfaction_tier=satisfaction_tier,
            confidence_level=confidence_level
        )

        return metrics

    def get_urgency_context(self, inferred_satisfaction: float) -> float:
        """
        Convert inferred satisfaction to urgency context for entity salience.

        Logic:
        - Low satisfaction → high urgency (something wrong)
        - High satisfaction → low urgency (all good)

        Args:
            inferred_satisfaction: 0.0-1.0

        Returns:
            Urgency context (0.0-1.0) for EntitySalienceTracker
        """
        # Inverse relationship: low satisfaction = high urgency
        urgency = 1.0 - inferred_satisfaction

        return urgency

    def blend_with_explicit_feedback(
        self,
        inferred_satisfaction: float,
        explicit_rating: Optional[float] = None,
        inferred_weight: float = 0.7
    ) -> float:
        """
        Blend inferred satisfaction with optional explicit user feedback.

        Args:
            inferred_satisfaction: Felt-based inference (0.0-1.0)
            explicit_rating: Optional user rating (0.0-1.0)
            inferred_weight: Weight for inferred (0.7 = 70% inferred, 30% explicit)

        Returns:
            Blended satisfaction (0.0-1.0)
        """
        if explicit_rating is None:
            # No explicit feedback → use inferred only
            return inferred_satisfaction

        # Blend inferred + explicit
        blended = (
            inferred_weight * inferred_satisfaction +
            (1 - inferred_weight) * explicit_rating
        )

        return blended


# Module-level singleton for convenience
_default_inferencer = None

def get_default_inferencer() -> FeltSatisfactionInferencer:
    """Get or create default FeltSatisfactionInferencer singleton."""
    global _default_inferencer
    if _default_inferencer is None:
        _default_inferencer = FeltSatisfactionInferencer()
    return _default_inferencer
