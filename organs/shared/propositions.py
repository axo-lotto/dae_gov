"""
Proposition System for DAE 3.0 AXO ARC
========================================

Position-mapped propositions that bridge organ intelligence and entity values.

This module provides the core Proposition dataclass and utilities for creating,
managing, and aggregating propositions from multiple organs.

Created: October 24, 2025
Purpose: Enable organs to propose specific transformations for grid positions
Status: Phase 1 Implementation
"""

from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any, List
from enum import Enum


class PropositionType(Enum):
    """Type of proposition from organ analysis."""
    SPATIAL_TRANSFORMATION = "spatial"      # BOND: geometric/spatial changes
    COLOR_TRANSFORMATION = "color"          # EO: color/archetypal changes
    TEMPORAL_PREDICTION = "temporal"        # RNX: temporal pattern predictions
    SEMANTIC_ENHANCEMENT = "semantic"       # SANS: semantic meaning
    CONSTRAINT_SATISFACTION = "constraint"  # NDAM: constraint-based suggestions
    SCALING_PATTERN = "scaling"             # CARD: multi-scale patterns


@dataclass
class Proposition:
    """
    Position-mapped proposition from organ analysis.

    Represents a specific suggestion from an organ about what value
    a particular grid position should have in the output.

    Attributes:
        position: (row, col) grid position this proposition applies to
        organ_name: Which organ created this proposition (BOND, EO, RNX, etc.)
        proposition_type: Category of proposition
        proposed_value: The actual color/value being proposed (0-9 for ARC)
        confidence: How confident the organ is (0.0-1.0, from organ coherence)
        lure_intensity: How strongly this proposition "pulls" (0.0-1.0)

    Optional organ-specific metadata:
        spatial_score: BOND's geometric fit score
        semantic_intensity: SANS's semantic strength
        temporal_probability: RNX's prediction confidence
        archetypal_match: EO's archetypal resonance
        constraint_satisfaction: NDAM's constraint fulfillment

    Metadata for learning:
        source_pattern: What pattern triggered this proposition
        reasoning: Human-readable explanation of why this was proposed
    """

    # Core identification
    position: Tuple[int, int]
    organ_name: str
    proposition_type: PropositionType

    # Proposed transformation
    proposed_value: int  # 0-9 for ARC colors

    # Confidence metrics
    confidence: float  # From organ coherence (0.0-1.0)
    lure_intensity: float  # Strength of this proposition (0.0-1.0)

    # Organ-specific scores (optional)
    spatial_score: Optional[float] = None
    semantic_intensity: Optional[float] = None
    temporal_probability: Optional[float] = None
    archetypal_match: Optional[float] = None
    constraint_satisfaction: Optional[float] = None

    # Learning metadata
    source_pattern: Optional[str] = None
    reasoning: Optional[str] = None

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_combined_score(self) -> float:
        """
        Get combined score for proposition ranking.

        Uses confidence * lure_intensity as the base score,
        with optional organ-specific bonuses.
        """
        base_score = self.confidence * self.lure_intensity

        # Add organ-specific bonuses
        if self.spatial_score is not None:
            base_score *= (1.0 + 0.1 * self.spatial_score)
        if self.semantic_intensity is not None:
            base_score *= (1.0 + 0.1 * self.semantic_intensity)
        if self.temporal_probability is not None:
            base_score *= (1.0 + 0.15 * self.temporal_probability)  # Slightly higher weight
        if self.archetypal_match is not None:
            base_score *= (1.0 + 0.1 * self.archetypal_match)
        if self.constraint_satisfaction is not None:
            base_score *= (1.0 + 0.2 * self.constraint_satisfaction)  # Highest weight

        return base_score

    def to_dict(self) -> Dict[str, Any]:
        """Convert proposition to dictionary for serialization."""
        return {
            "position": self.position,
            "organ_name": self.organ_name,
            "proposition_type": self.proposition_type.value,
            "proposed_value": self.proposed_value,
            "confidence": self.confidence,
            "lure_intensity": self.lure_intensity,
            "spatial_score": self.spatial_score,
            "semantic_intensity": self.semantic_intensity,
            "temporal_probability": self.temporal_probability,
            "archetypal_match": self.archetypal_match,
            "constraint_satisfaction": self.constraint_satisfaction,
            "source_pattern": self.source_pattern,
            "reasoning": self.reasoning,
            "combined_score": self.get_combined_score(),
            "metadata": self.metadata
        }


@dataclass
class PropositionFeltInterpretation:
    """
    Pure felt interpretation of a proposition without prediction targets.

    This is the "clean" version of Proposition used for epoch learning,
    containing only felt intelligence (organ interpretations) without
    contamination from expected_output (proposed_value).

    Used in processing_only mode for:
    - Epoch learning from felt transformation patterns
    - Capturing organ agreement and confidence without prediction
    - Learning which positions need attention

    Identical to Proposition except excludes:
    - proposed_value (the only contaminated field)

    All felt intelligence is preserved:
    - Position attention signals (which cells need transformation)
    - Organ confidence and lure (how strongly organ believes)
    - Organ-specific felt scores (spatial, semantic, temporal, etc.)
    - Metadata and reasoning (why this position matters)
    """

    # Core identification (FELT)
    position: Tuple[int, int]
    organ_name: str
    proposition_type: PropositionType

    # Confidence metrics (FELT)
    confidence: float  # From organ coherence (0.0-1.0)
    lure_intensity: float  # Strength of attention (0.0-1.0)

    # Organ-specific felt scores (FELT)
    spatial_score: Optional[float] = None
    semantic_intensity: Optional[float] = None
    temporal_probability: Optional[float] = None
    archetypal_match: Optional[float] = None
    constraint_satisfaction: Optional[float] = None

    # Learning metadata (FELT)
    source_pattern: Optional[str] = None
    reasoning: Optional[str] = None

    # Additional metadata (FELT)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_felt_strength(self) -> float:
        """
        Get combined felt strength for ranking attention.

        Similar to Proposition.get_combined_score() but for felt-only context.
        Uses confidence * lure_intensity as base, with organ-specific bonuses.
        """
        base_strength = self.confidence * self.lure_intensity

        # Add organ-specific bonuses
        if self.spatial_score is not None:
            base_strength *= (1.0 + 0.1 * self.spatial_score)
        if self.semantic_intensity is not None:
            base_strength *= (1.0 + 0.1 * self.semantic_intensity)
        if self.temporal_probability is not None:
            base_strength *= (1.0 + 0.15 * self.temporal_probability)
        if self.archetypal_match is not None:
            base_strength *= (1.0 + 0.1 * self.archetypal_match)
        if self.constraint_satisfaction is not None:
            base_strength *= (1.0 + 0.2 * self.constraint_satisfaction)

        return base_strength

    def to_dict(self) -> Dict[str, Any]:
        """Convert felt interpretation to dictionary for serialization."""
        return {
            "position": self.position,
            "organ_name": self.organ_name,
            "proposition_type": self.proposition_type.value,
            # NOTE: No proposed_value (clean for epoch learning)
            "confidence": self.confidence,
            "lure_intensity": self.lure_intensity,
            "spatial_score": self.spatial_score,
            "semantic_intensity": self.semantic_intensity,
            "temporal_probability": self.temporal_probability,
            "archetypal_match": self.archetypal_match,
            "constraint_satisfaction": self.constraint_satisfaction,
            "source_pattern": self.source_pattern,
            "reasoning": self.reasoning,
            "felt_strength": self.get_felt_strength(),
            "metadata": self.metadata
        }


def extract_felt_interpretation(proposition) -> PropositionFeltInterpretation:
    """
    Extract pure felt interpretation from full proposition.

    Removes the contaminated field (proposed_value) while preserving
    all felt intelligence (position, confidence, scores, metadata).

    Args:
        proposition: Full proposition (Proposition object OR dict)

    Returns:
        PropositionFeltInterpretation with only felt component

    Example:
        >>> prop = create_spatial_proposition((2, 3), proposed_value=5,
        ...                                   confidence=0.8, lure_intensity=0.6)
        >>> felt = extract_felt_interpretation(prop)
        >>> # felt has position, confidence, lure, spatial_score
        >>> # felt does NOT have proposed_value
    """
    # Handle both Proposition objects and dicts
    if isinstance(proposition, dict):
        # Dict format (from aggregator)
        return PropositionFeltInterpretation(
            position=tuple(proposition.get('position', (0, 0))),
            organ_name=proposition.get('organ', proposition.get('organ_name', 'unknown')),
            proposition_type=PropositionType(proposition.get('type', 'spatial')) if isinstance(proposition.get('type'), str) else proposition.get('type', PropositionType.SPATIAL_TRANSFORMATION),
            confidence=proposition.get('confidence', 0.5),
            lure_intensity=proposition.get('lure', proposition.get('lure_intensity', 0.5)),
            spatial_score=proposition.get('spatial_score'),
            semantic_intensity=proposition.get('semantic_intensity'),
            temporal_probability=proposition.get('temporal_probability'),
            archetypal_match=proposition.get('archetypal_match'),
            constraint_satisfaction=proposition.get('constraint_satisfaction'),
            source_pattern=proposition.get('source_pattern'),
            reasoning=proposition.get('reasoning'),
            metadata=proposition.get('metadata', {}).copy() if proposition.get('metadata') else {}
        )
    else:
        # Proposition object
        return PropositionFeltInterpretation(
            position=proposition.position,
            organ_name=proposition.organ_name,
            proposition_type=proposition.proposition_type,
            confidence=proposition.confidence,
            lure_intensity=proposition.lure_intensity,
            spatial_score=proposition.spatial_score,
            semantic_intensity=proposition.semantic_intensity,
            temporal_probability=proposition.temporal_probability,
            archetypal_match=proposition.archetypal_match,
            constraint_satisfaction=proposition.constraint_satisfaction,
            source_pattern=proposition.source_pattern,
            reasoning=proposition.reasoning,
            metadata=proposition.metadata.copy() if proposition.metadata else {}
        )


def extract_felt_interpretations(propositions: List[Proposition]) -> List[PropositionFeltInterpretation]:
    """
    Extract felt interpretations from list of propositions.

    Batch version of extract_felt_interpretation() for convenience.

    Args:
        propositions: List of full propositions

    Returns:
        List of felt interpretations (same order)

    Example:
        >>> props = [create_spatial_proposition(...), create_color_proposition(...)]
        >>> felts = extract_felt_interpretations(props)
        >>> len(felts) == len(props)  # Same count, but no proposed_values
    """
    return [extract_felt_interpretation(prop) for prop in propositions]


class PropositionAggregator:
    """
    Aggregates propositions from multiple organs for each position.

    Handles conflicts when multiple organs propose different values
    for the same position.
    """

    def __init__(self):
        self.propositions_by_position: Dict[Tuple[int, int], List[Proposition]] = {}

    def add_proposition(self, proposition: Proposition):
        """Add a proposition to the aggregator."""
        pos = proposition.position
        if pos not in self.propositions_by_position:
            self.propositions_by_position[pos] = []
        self.propositions_by_position[pos].append(proposition)

    def add_propositions(self, propositions: List[Proposition]):
        """Add multiple propositions."""
        for prop in propositions:
            self.add_proposition(prop)

    def get_propositions_for_position(self, position: Tuple[int, int]) -> List[Proposition]:
        """Get all propositions for a specific position."""
        return self.propositions_by_position.get(position, [])

    def get_best_proposition(self, position: Tuple[int, int]) -> Optional[Proposition]:
        """
        Get the best (highest scoring) proposition for a position.

        Returns None if no propositions exist for this position.
        """
        propositions = self.get_propositions_for_position(position)
        if not propositions:
            return None

        return max(propositions, key=lambda p: p.get_combined_score())

    def get_consensus_proposition(self, position: Tuple[int, int],
                                 min_agreement: int = 2) -> Optional[Proposition]:
        """
        Get proposition if multiple organs agree on the same value.

        Args:
            position: Grid position
            min_agreement: Minimum number of organs that must agree

        Returns:
            Best proposition if consensus exists, None otherwise
        """
        propositions = self.get_propositions_for_position(position)
        if len(propositions) < min_agreement:
            return None

        # Group by proposed value
        by_value: Dict[int, List[Proposition]] = {}
        for prop in propositions:
            if prop.proposed_value not in by_value:
                by_value[prop.proposed_value] = []
            by_value[prop.proposed_value].append(prop)

        # Find values with enough agreement
        for value, props in by_value.items():
            if len(props) >= min_agreement:
                # Return highest scoring proposition for this value
                return max(props, key=lambda p: p.get_combined_score())

        return None

    def get_all_positions(self) -> List[Tuple[int, int]]:
        """Get all positions that have propositions."""
        return list(self.propositions_by_position.keys())

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about propositions."""
        total_propositions = sum(len(props) for props in self.propositions_by_position.values())
        positions_with_propositions = len(self.propositions_by_position)

        # Count by organ
        by_organ: Dict[str, int] = {}
        for props in self.propositions_by_position.values():
            for prop in props:
                by_organ[prop.organ_name] = by_organ.get(prop.organ_name, 0) + 1

        # Count positions with multiple propositions (conflicts)
        conflicts = sum(1 for props in self.propositions_by_position.values() if len(props) > 1)

        return {
            "total_propositions": total_propositions,
            "positions_with_propositions": positions_with_propositions,
            "propositions_by_organ": by_organ,
            "positions_with_conflicts": conflicts,
            "avg_propositions_per_position": total_propositions / max(1, positions_with_propositions)
        }


def create_spatial_proposition(position: Tuple[int, int],
                               proposed_value: int,
                               confidence: float,
                               lure_intensity: float,
                               spatial_score: float = 0.5,
                               source_pattern: Optional[str] = None) -> Proposition:
    """Factory function for BOND spatial propositions."""
    return Proposition(
        position=position,
        organ_name="BOND",
        proposition_type=PropositionType.SPATIAL_TRANSFORMATION,
        proposed_value=proposed_value,
        confidence=confidence,
        lure_intensity=lure_intensity,
        spatial_score=spatial_score,
        source_pattern=source_pattern,
        reasoning=f"BOND spatial analysis suggests {proposed_value} at {position}"
    )


def create_color_proposition(position: Tuple[int, int],
                            proposed_value: int,
                            confidence: float,
                            lure_intensity: float,
                            archetypal_match: float = 0.5,
                            source_pattern: Optional[str] = None) -> Proposition:
    """Factory function for EO color/archetypal propositions."""
    return Proposition(
        position=position,
        organ_name="EO",
        proposition_type=PropositionType.COLOR_TRANSFORMATION,
        proposed_value=proposed_value,
        confidence=confidence,
        lure_intensity=lure_intensity,
        archetypal_match=archetypal_match,
        source_pattern=source_pattern,
        reasoning=f"EO archetypal analysis suggests {proposed_value} at {position}"
    )


def create_temporal_proposition(position: Tuple[int, int],
                               proposed_value: int,
                               confidence: float,
                               lure_intensity: float,
                               temporal_probability: float = 0.5,
                               source_pattern: Optional[str] = None) -> Proposition:
    """Factory function for RNX temporal propositions."""
    return Proposition(
        position=position,
        organ_name="RNX",
        proposition_type=PropositionType.TEMPORAL_PREDICTION,
        proposed_value=proposed_value,
        confidence=confidence,
        lure_intensity=lure_intensity,
        temporal_probability=temporal_probability,
        source_pattern=source_pattern,
        reasoning=f"RNX temporal prediction suggests {proposed_value} at {position}"
    )


def create_semantic_proposition(position: Tuple[int, int],
                                proposed_value: int,
                                confidence: float,
                                lure_intensity: float,
                                semantic_intensity: float = 0.5,
                                source_pattern: Optional[str] = None) -> Proposition:
    """Factory function for SANS semantic propositions."""
    return Proposition(
        position=position,
        organ_name="SANS",
        proposition_type=PropositionType.SEMANTIC_ENHANCEMENT,
        proposed_value=proposed_value,
        confidence=confidence,
        lure_intensity=lure_intensity,
        semantic_intensity=semantic_intensity,
        source_pattern=source_pattern,
        reasoning=f"SANS semantic analysis suggests {proposed_value} at {position}"
    )


def create_constraint_proposition(position: Tuple[int, int],
                                  proposed_value: int,
                                  confidence: float,
                                  lure_intensity: float,
                                  constraint_satisfaction: float = 0.5,
                                  source_pattern: Optional[str] = None) -> Proposition:
    """Factory function for NDAM constraint propositions."""
    return Proposition(
        position=position,
        organ_name="NDAM",
        proposition_type=PropositionType.CONSTRAINT_SATISFACTION,
        proposed_value=proposed_value,
        confidence=confidence,
        lure_intensity=lure_intensity,
        constraint_satisfaction=constraint_satisfaction,
        source_pattern=source_pattern,
        reasoning=f"NDAM constraint analysis suggests {proposed_value} at {position}"
    )


def create_scaling_proposition(position: Tuple[int, int],
                               proposed_value: int,
                               confidence: float,
                               lure_intensity: float,
                               source_pattern: Optional[str] = None) -> Proposition:
    """Factory function for CARD multi-scale propositions."""
    return Proposition(
        position=position,
        organ_name="CARD",
        proposition_type=PropositionType.SCALING_PATTERN,
        proposed_value=proposed_value,
        confidence=confidence,
        lure_intensity=lure_intensity,
        source_pattern=source_pattern,
        reasoning=f"CARD multi-scale analysis suggests {proposed_value} at {position}"
    )
