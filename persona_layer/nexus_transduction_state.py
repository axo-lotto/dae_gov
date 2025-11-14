"""
Nexus Transduction State
=========================

Represents nexuses as dynamic transductive processes (not static categories).

Based on 14_NEXUS_DESIGN.md which reveals nexuses are living flows governed by:
- V0 energy descent (appetition satisfaction)
- Mutual satisfaction (co-regulation across parts)
- Rhythmic coherence (vibrational entrainment)

Date: November 12, 2025
Purpose: Implement transductive nexus dynamics for DAE_HYPHAE_1
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import numpy as np


@dataclass
class NexusTransductionState:
    """
    Nexus as dynamic transductive process (not static category).

    Represents current nexus attractor state and available pathways
    based on V0 energy, satisfaction, and rhythmic coherence.

    Key Insight: Nexuses are not fixed classifications but dynamic flows
    that transduce between types as V0 energy descends.
    """

    # Current state
    current_type: str  # e.g., "Urgency", "Recursive", "Relational", "Innate"
    current_category: str  # "GUT", "PSYCHE", "SOCIAL_CONTEXT"
    cycle_num: int  # Which cycle this state represents

    # V0 energy context (appetition)
    v0_energy: float  # 0-1 (1 = high unsatisfied appetition)
    satisfaction: float  # 0-1 (1 = fully satisfied)
    mutual_satisfaction: float  # 0-1 (co-satisfaction across parts)

    # Rhythmic/vibrational state
    rhythm_coherence: float  # 0-1 (parts in sync?)
    field_resonance: float  # 0-1 (coherent field?)

    # Transductive vocabulary (felt states)
    signal_inflation: float  # From salience (urgency amplification)
    salience_drift: float  # Losing coherence in feedback loop
    prehensive_overload: float  # Too many dissonant prehensions
    coherence_leakage: float  # Energy fracturing across parts

    # Available transduction pathways
    available_paths: List[Dict[str, Any]] = field(default_factory=list)
    # Each path: {type, mechanism, probability, description}

    next_type: Optional[str] = None  # Selected next type
    transition_mechanism: Optional[str] = None  # How transduction occurs
    transition_probability: float = 0.0  # Likelihood of transition

    # Relational context (affects pathway availability)
    relational_field_available: bool = False  # Can attunement occur?
    protective_field_active: bool = False  # Are protectors engaged?

    # Organ insights (for pathway evaluation)
    bond_self_distance: float = 0.5  # BOND SELF-distance
    ndam_urgency_level: float = 0.0  # NDAM urgency
    eo_polyvagal_state: str = "mixed"  # EO state
    rnx_temporal_coherence: float = 0.5  # RNX coherence

    def select_highest_probability_path(self):
        """Select the transduction path with highest probability."""
        if not self.available_paths:
            # No paths available - maintain current type
            self.next_type = self.current_type
            self.transition_mechanism = "maintain"
            self.transition_probability = 1.0
            return

        # Sort by probability
        sorted_paths = sorted(
            self.available_paths,
            key=lambda p: p['probability'],
            reverse=True
        )

        best_path = sorted_paths[0]
        self.next_type = best_path['type']
        self.transition_mechanism = best_path['mechanism']
        self.transition_probability = best_path['probability']

    def get_nexus_domain(self) -> str:
        """
        Get the domain (GUT/PSYCHE/SOCIAL_CONTEXT) for current nexus type.

        Based on 14_NEXUS_DESIGN.md mapping.
        """
        # GUT domain (somatic, pre-verbal)
        if self.current_type in ["Urgency", "Disruptive", "Looped"]:
            return "GUT"

        # PSYCHE domain (relational, intersubjective)
        elif self.current_type in ["Relational", "Innate", "Protective",
                                    "Recursive", "Dissociative"]:
            return "PSYCHE"

        # SOCIAL_CONTEXT domain (systemic, external)
        elif self.current_type in ["Contrast", "Fragmented", "Absorbed",
                                    "Isolated", "Paradox"]:
            return "SOCIAL_CONTEXT"

        else:
            return "UNKNOWN"

    def is_crisis_oriented(self) -> bool:
        """
        Check if current nexus is Crisis-Oriented (NDAM) vs Constitutional (SANS).

        Crisis-Oriented: Paradox, Dissociative, Disruptive, Recursive, Looped, Urgency
        Constitutional: Pre-Existing, Innate, Contrast, Relational, Fragmented,
                        Protective, Absorbed, Isolated
        """
        crisis_types = {
            "Paradox", "Dissociative", "Disruptive",
            "Recursive", "Looped", "Urgency"
        }
        return self.current_type in crisis_types

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'current_type': self.current_type,
            'current_category': self.current_category,
            'cycle_num': self.cycle_num,
            'v0_energy': float(self.v0_energy),
            'satisfaction': float(self.satisfaction),
            'mutual_satisfaction': float(self.mutual_satisfaction),
            'rhythm_coherence': float(self.rhythm_coherence),
            'field_resonance': float(self.field_resonance),
            'signal_inflation': float(self.signal_inflation),
            'salience_drift': float(self.salience_drift),
            'prehensive_overload': float(self.prehensive_overload),
            'coherence_leakage': float(self.coherence_leakage),
            'next_type': self.next_type,
            'transition_mechanism': self.transition_mechanism,
            'transition_probability': float(self.transition_probability),
            'relational_field_available': self.relational_field_available,
            'protective_field_active': self.protective_field_active,
            'domain': self.get_nexus_domain(),
            'is_crisis': self.is_crisis_oriented()
        }


def classify_nexus_type_from_v0(
    v0_energy: float,
    satisfaction: float,
    bond_self_distance: float,
    ndam_urgency_level: float,
    eo_polyvagal_state: str
) -> tuple[str, str]:
    """
    Classify nexus type based on V0 energy and organ insights.

    V0 Energy Mapping:
    - V0 > 0.7 → Crisis-Oriented attractors (Urgency, Disruptive)
    - V0 0.5-0.7 → Recursive/Protective states
    - V0 0.3-0.5 → Relational/Contrast states
    - V0 < 0.3 → Constitutional attractors (Innate, Pre-Existing)

    Returns:
        (nexus_type, category) tuple
    """

    # High V0 → Crisis-Oriented
    if v0_energy > 0.7:
        if ndam_urgency_level > 0.7:
            return "Urgency", "GUT"
        elif bond_self_distance > 0.6:
            return "Disruptive", "GUT"
        else:
            return "Recursive", "PSYCHE"

    # Medium-high V0 → Protective/Recursive
    elif v0_energy > 0.5:
        if bond_self_distance > 0.5:
            return "Protective", "PSYCHE"
        else:
            return "Recursive", "PSYCHE"

    # Medium V0 → Relational/Contrast
    elif v0_energy > 0.3:
        if bond_self_distance < 0.25:
            return "Relational", "PSYCHE"
        elif eo_polyvagal_state == "ventral_vagal":
            return "Relational", "PSYCHE"
        else:
            return "Contrast", "SOCIAL_CONTEXT"

    # Low V0 → Constitutional attractors
    else:
        if bond_self_distance < 0.15:
            return "Innate", "PSYCHE"
        elif satisfaction > 0.9:
            return "Innate", "PSYCHE"
        else:
            return "Relational", "PSYCHE"


def compute_rhythm_coherence(
    organ_results: Dict,
    rnx_temporal_coherence: float
) -> float:
    """
    Compute rhythm coherence: Are parts in sync?

    Rhythm coherence measures vibrational entrainment across organs.
    High coherence = parts oscillating in sync (co-regulated).
    Low coherence = parts out of phase (dysregulated).

    Args:
        organ_results: Dictionary of organ processing results
        rnx_temporal_coherence: RNX organ's temporal coherence metric

    Returns:
        rhythm_coherence (0-1)
    """

    # Extract organ coherences
    coherences = []
    for organ_name, result in organ_results.items():
        if hasattr(result, 'coherence'):
            coherences.append(result.coherence)

    if not coherences:
        return 0.5  # Neutral default

    # Rhythm coherence = temporal coherence × agreement (1 - variance)
    mean_coherence = np.mean(coherences)
    std_coherence = np.std(coherences)
    agreement = 1.0 - min(std_coherence, 1.0)

    rhythm_coherence = (
        0.5 * rnx_temporal_coherence +  # Temporal dimension
        0.3 * agreement +                # Inter-organ sync
        0.2 * mean_coherence             # Overall coherence
    )

    return max(0.0, min(1.0, rhythm_coherence))


def compute_mutual_satisfaction(
    organ_results: Dict,
    nexus_coherence: float,
    rhythm_coherence: float
) -> float:
    """
    Compute mutual satisfaction: Co-satisfaction of multiple parts.

    Mutual satisfaction = individual satisfactions + agreement + rhythm

    This is the organizing force in transduction. High mutual satisfaction
    enables healing pathways. Low mutual satisfaction leads to crisis pathways.

    Args:
        organ_results: Dictionary of organ processing results
        nexus_coherence: Coherence of dominant nexus
        rhythm_coherence: Rhythmic entrainment across parts

    Returns:
        mutual_satisfaction (0-1)
    """

    # Extract organ satisfactions (coherence as proxy for satisfaction)
    organ_satisfactions = []
    for organ_name, result in organ_results.items():
        if hasattr(result, 'coherence'):
            organ_satisfactions.append(result.coherence)

    if not organ_satisfactions:
        return 0.5  # Neutral default

    mean_organ_satisfaction = np.mean(organ_satisfactions)

    # Mutual satisfaction formula from document
    mutual_satisfaction = (
        0.4 * mean_organ_satisfaction +  # Individual satisfactions
        0.3 * nexus_coherence +           # Agreement (coherence)
        0.3 * rhythm_coherence            # Shared rhythm
    )

    return max(0.0, min(1.0, mutual_satisfaction))


def check_relational_field_available(
    bond_self_distance: float,
    eo_polyvagal_state: str,
    empathy_coherence: float
) -> bool:
    """
    Check if relational field is available for attunement.

    Relational field requires:
    - BOND SELF-distance not too high (< 0.6)
    - EO polyvagal state not dorsal vagal shutdown
    - EMPATHY organ activated (coherence > 0.4)

    Args:
        bond_self_distance: BOND organ SELF-distance metric
        eo_polyvagal_state: EO organ polyvagal state
        empathy_coherence: EMPATHY organ coherence

    Returns:
        bool: True if relational field available
    """

    return (
        bond_self_distance < 0.6 and
        eo_polyvagal_state != "dorsal_vagal" and
        empathy_coherence > 0.4
    )


def compute_transductive_vocabulary(
    salience_metrics: Dict,
    organ_activations: Dict,
    satisfaction: float,
    v0_energy: float
) -> Dict[str, float]:
    """
    Compute transductive vocabulary metrics (felt states).

    Maps DAE_HYPHAE_1 metrics to transductive vocabulary from 14_NEXUS_DESIGN.md:
    - signal_inflation: Urgency amplification (from salience)
    - salience_drift: Losing coherence in feedback loop
    - prehensive_overload: Too many dissonant prehensions
    - coherence_leakage: Energy fracturing across parts

    Args:
        salience_metrics: Salience model output (trauma markers)
        organ_activations: Activation levels across organs
        satisfaction: Current satisfaction level
        v0_energy: Current V0 appetition energy

    Returns:
        Dictionary of transductive vocabulary metrics
    """

    # Signal inflation = salience signal_inflation metric
    signal_inflation = salience_metrics.get('signal_inflation', 0.0)

    # Salience drift = low satisfaction + high V0 (unsatisfied appetition loops)
    salience_drift = (1.0 - satisfaction) * v0_energy

    # Prehensive overload = high activations + low agreement
    if organ_activations:
        activations = list(organ_activations.values())
        mean_activation = np.mean(activations)
        std_activation = np.std(activations)
        prehensive_overload = mean_activation * std_activation
    else:
        prehensive_overload = 0.0

    # Coherence leakage = 1 - safety_gradient (from salience)
    safety_gradient = salience_metrics.get('safety_gradient', 1.0)
    coherence_leakage = 1.0 - safety_gradient

    return {
        'signal_inflation': float(signal_inflation),
        'salience_drift': float(salience_drift),
        'prehensive_overload': float(prehensive_overload),
        'coherence_leakage': float(coherence_leakage)
    }
