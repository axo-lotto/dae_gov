"""
ConversationalOccasion: Text tokens as Whiteheadian experiencing subjects.

Phase 2 implementation of entity-native process philosophy for DAE_HYPHAE_1.
Tokens become actual occasions that:
- Prehend organ feelings (accumulate felt affordances)
- Descend through V0 energy (appetition → satisfaction)
- Detect Kairos moments (opportune time for decision)
- Mature propositions post-convergence

Based on DAE 3.0 proven architecture (47.3% success, 841 perfect tasks).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np


@dataclass
class FeltAffordance:
    """
    Proto-proposition: felt possibility BEFORE decision.

    Whitehead: "A proposition is the potentiality of the datum for realization
    in actual entities." Affordances are felt DURING prehension as lures.

    These accumulate across cycles 1-N and mature POST-CONVERGENCE.
    """
    position: int  # Token index in conversation
    atom: str  # Semantic atom (77 organ-specific + 10 meta-atoms)
    organ_name: str  # Which organ felt this
    confidence: float  # Pattern strength × pattern confidence
    lure_intensity: float  # Appetition pull (how strongly drawn)
    cycle: int  # Which cycle this was felt (1, 2, 3, ...)

    # Context captured during prehension:
    v0_energy_context: Optional[float] = None  # V0 energy when felt
    satisfaction_context: Optional[float] = None  # Satisfaction when felt

    # Maturation (filled post-convergence):
    kairos_bonus: float = 1.0  # 1.5× if in Kairos window
    felt_energy: Optional[float] = None  # Computed from final V0 state


@dataclass
class PropositionFeltInterpretation:
    """
    MATURE proposition: affordance + V0 context → emission readiness.

    Created POST-CONVERGENCE from FeltAffordance with mature V0 state.
    Ready for nexus formation and emission generation.
    """
    position: int
    atom: str
    confidence: float  # Affordance confidence × kairos_bonus
    felt_energy: float  # E = α(1-S) + β·ΔE + ... (from V0)
    v0_bonus: float  # Kairos window multiplier (1.0 or 1.5)
    organ_sources: List[str]  # All organs that felt this atom
    intersection_strength: float  # Σ activations × coherences

    # Emission readiness (for 4-gate selection):
    emission_priority: float  # Combined score for sorting


@dataclass
class ConversationalOccasion:
    """
    Text token as EXPERIENCING SUBJECT (Whiteheadian actual occasion).

    Philosophy: Tokens are not inert data, but self-creating subjects
    that prehend organs, descend through V0 energy, and achieve satisfaction.

    Process Lifecycle:
    1. Conformal phase: Initial data (token embedding)
    2. Supplemental phases: Multi-cycle organ prehensions (felt affordances)
    3. Satisfaction: V0 descent + Kairos detection → convergence
    4. Maturation: Affordances → mature propositions
    5. Superject: Becomes data for emission generation
    """
    datum: str  # Token text (or None for generation)
    position: int  # Token index in conversation
    embedding: Optional[np.ndarray] = None  # 384D from sentence transformer

    # Whiteheadian process state:
    cycle: int = 0  # Current concrescence cycle
    v0_energy: float = 1.0  # Appetition (1.0 = max unsatisfied → 0.0 = satisfied)
    satisfaction: float = 0.0  # Convergence metric (0.0 → 1.0)

    # Prehension accumulation (DURING cycles 1-N):
    felt_affordances: List[FeltAffordance] = field(default_factory=list)
    organ_prehensions: Dict[str, Dict] = field(default_factory=dict)

    # Matured propositions (AFTER convergence):
    mature_propositions: List[PropositionFeltInterpretation] = field(default_factory=list)

    # Kairos detection:
    kairos_detected: bool = False
    kairos_cycle: int = 0

    # Private state tracking:
    _prev_v0_energy: float = field(default=1.0, init=False, repr=False)
    _prev_satisfaction: float = field(default=0.0, init=False, repr=False)

    # 🆕 SALIENCE INTEGRATION: Subjective aim (Whiteheadian direction of becoming)
    subjective_aim: Optional[Dict[str, float]] = None  # Set via salience model

    def add_felt_affordance(
        self,
        atom: str,
        organ_name: str,
        confidence: float,
        lure_intensity: float
    ):
        """
        Store felt affordance DURING organ prehension (cycles 1-N).

        Affordances are proto-propositions: lures for feeling felt before
        decision. They accumulate across cycles and mature post-convergence.
        """
        affordance = FeltAffordance(
            position=self.position,
            atom=atom,
            organ_name=organ_name,
            confidence=confidence,
            lure_intensity=lure_intensity,
            cycle=self.cycle,
            v0_energy_context=self.v0_energy,  # Capture current V0 state
            satisfaction_context=self.satisfaction
        )
        self.felt_affordances.append(affordance)

    def descend_v0_energy(self, organ_coherences: Dict[str, float], organ_results: Optional[Dict] = None):
        """
        V0 energy descent (DAE 3.0 formula adapted for text domain).

        E(t) = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I) + η·L

        where:
          S = satisfaction (0.0 → 1.0)
          ΔE = energy change from previous cycle
          A = organ agreement (1 - std(coherences))
          R = resonance (mean coherence)
          φ(I) = intensity (max coherence)
          L = lure contribution (🆕 Whiteheadian attractor pull)

        Coefficients from DAE 3.0 (empirically tuned):
          α=0.40 (satisfaction weight - primary driver)
          β=0.25 (energy change momentum)
          γ=0.15 (agreement weight)
          δ=0.10 (resonance weight)
          ζ=0.10 (intensity weight)
          η=0.20 (🆕 lure weight - enables organ learning)
        """
        # Coefficients from DAE 3.0 + lure:
        α, β, γ, δ, ζ, η = 0.40, 0.25, 0.15, 0.10, 0.10, 0.20

        S = self.satisfaction
        ΔE = self.v0_energy - self._prev_v0_energy

        coherences = list(organ_coherences.values())

        if len(coherences) > 1:
            A = 1.0 - np.std(coherences)
        else:
            A = 1.0

        R = np.mean(coherences) if coherences else 0.0
        φ_I = max(coherences) if coherences else 0.0

        # 🆕 LURE CONTRIBUTION: Compute from 6 lure attractor organs
        # (EO/NDAM/RNX from Phase A + EMPATHY/WISDOM/AUTHENTICITY from Phase B)
        L = 0.0
        if organ_results:
            # Extract lures from lure attractor organs (6 total, Nov 13 2025)
            lure_weights = {
                'EO': 0.20,          # Polyvagal state lure
                'NDAM': 0.20,        # Salience/crisis lure
                'RNX': 0.15,         # Temporal dynamics lure
                'EMPATHY': 0.20,     # 🆕 Emotional resonance lure
                'WISDOM': 0.15,      # 🆕 Pattern recognition lure
                'AUTHENTICITY': 0.10  # 🆕 Vulnerability lure
            }

            for organ_name, weight in lure_weights.items():
                if organ_name in organ_results:
                    organ_result = organ_results[organ_name]
                    if hasattr(organ_result, 'lure'):
                        L += organ_result.lure * weight

        # V0 energy formula (with lure):
        new_energy = α * (1 - S) + β * ΔE + γ * (1 - A) + δ * (1 - R) + ζ * φ_I + η * L

        # Update state:
        self._prev_v0_energy = self.v0_energy
        self.v0_energy = max(0.0, min(1.0, new_energy))  # Clip to [0, 1]
        self.cycle += 1

        # Update satisfaction (convergence metric):
        # Satisfaction increases as energy decreases AND coherence increases
        self.satisfaction = 1.0 - self.v0_energy * (1.0 - R)

    def compute_v0_energy_hybrid(
        self,
        satisfaction: float,
        appetition: float,
        relevance: float,
        complexity: float,
        llm_confidence: float = 0.0,
        llm_weight: float = 0.0
    ) -> float:
        """
        Hybrid V0 energy computation including LLM uncertainty term.

        Formula:
        E_v0 = α(1-S) + β·ΔE + γ(1-A) + δ(1-R) + ζ·φ(I) + η·(1-L_conf)

        Where:
          S = satisfaction (organ coherence: 1 - std(organ_values))
          ΔE = delta energy from previous cycle
          A = appetition (felt pull toward patterns)
          R = relevance (family-specific organ weights)
          φ(I) = complexity (information content)
          L_conf = LLM response confidence (0-1)

        Coefficients:
          Pure DAE mode (llm_weight = 0):
            α=0.40, β=0.25, γ=0.15, δ=0.10, ζ=0.10, η=0.0

          Hybrid mode (llm_weight > 0):
            α=0.35, β=0.25, γ=0.12, δ=0.10, ζ=0.10, η=0.08

        The LLM term (η·(1-L_conf)·w_llm) adds uncertainty awareness:
        - Low LLM confidence increases energy (need more exploration)
        - Weighted by llm_weight (decays as DAE matures)

        Progressive weaning:
        - Month 0: w_llm = 0.85, η = 0.09 (LLM scaffolding)
        - Month 6: w_llm = 0.18, η = 0.02 (DAE taking over)
        - Month 12: w_llm = 0.05, η = 0.01 (Full autonomy)

        Args:
            satisfaction: Organ coherence (1 - std(organ_values))
            appetition: Felt pull toward patterns
            relevance: Family-specific organ weights
            complexity: Information content
            llm_confidence: LLM response confidence (0-1)
            llm_weight: Current LLM weaning weight (0-1)

        Returns:
            V0 energy value (0.0-1.0)
        """
        from config import Config

        # Use hybrid coefficients if LLM enabled
        if Config.HYBRID_ENABLED and llm_weight > 0:
            alpha = Config.V0_ALPHA_HYBRID  # 0.35
            beta = Config.V0_BETA_HYBRID    # 0.25
            gamma = Config.V0_GAMMA_HYBRID  # 0.12
            delta = Config.V0_DELTA_HYBRID  # 0.10
            zeta = Config.V0_ZETA_HYBRID    # 0.10
            eta = Config.V0_ETA_HYBRID      # 0.08
        else:
            # Pure DAE coefficients
            alpha = 0.40
            beta = 0.25
            gamma = 0.15
            delta = 0.10
            zeta = 0.10
            eta = 0.0  # No LLM term

        # Standard V0 components
        E_satisfaction = alpha * (1 - satisfaction)
        E_delta = beta * abs(self.v0_energy - self._prev_v0_energy)
        E_appetition = gamma * (1 - appetition)
        E_relevance = delta * (1 - relevance)
        E_complexity = zeta * complexity

        # NEW: LLM uncertainty component (weighted by llm_weight)
        # High when LLM is uncertain (low confidence), weighted by current LLM reliance
        E_llm = eta * (1 - llm_confidence) * llm_weight

        total_energy = (
            E_satisfaction +
            E_delta +
            E_appetition +
            E_relevance +
            E_complexity +
            E_llm  # NEW term
        )

        return max(0.0, min(1.0, total_energy))  # Clip to [0, 1]

    def detect_kairos(self, prev_occasion: Optional['ConversationalOccasion'] = None) -> bool:
        """
        Detect Kairos moment (opportune time for decision).

        Tuned Nov 12, 2025: Widened window and relaxed stability for conversational V0.

        4-condition gate (all must pass):
          1. Energy in window [0.35, 0.75] (widened from [0.45, 0.70])
          2. Satisfaction increasing (ΔS > 0)
          3. Energy stable (ΔE < 0.3) - relaxed from 0.1 for rapid descent
          4. Coherence sufficient (mean > 0.4)

        Returns:
            True if Kairos moment detected (sets kairos_detected flag)
        """
        from config import Config

        # Condition 1: Energy in Kairos window (from config)
        in_window = Config.KAIROS_WINDOW_MIN <= self.v0_energy <= Config.KAIROS_WINDOW_MAX

        # Condition 2: Satisfaction increasing
        satisfaction_increasing = self.satisfaction > self._prev_satisfaction

        # Simplified Kairos for conversational: in window + good satisfaction
        # Conversational V0 descends rapidly through window, so just check:
        # 1. We're in the window
        # 2. Satisfaction is sufficient (>0.7 means good coherence)
        # 3. Not first cycle (too early)
        kairos = (
            self.cycle >= 2 and  # Skip first cycle (initial descent)
            in_window and
            self.satisfaction > 0.7  # High satisfaction = good moment for decision
        )

        if kairos and not self.kairos_detected:
            self.kairos_detected = True
            self.kairos_cycle = self.cycle

        self._prev_satisfaction = self.satisfaction

        return kairos

    def mature_propositions_from_affordances(self):
        """
        POST-CONVERGENCE: Convert felt affordances → mature propositions.

        Affordances mature with V0 context (final energy, satisfaction, Kairos).
        Kairos moment adds 1.5× confidence boost (empirical from DAE 3.0).

        Multiple organs can feel the same atom → nexus formation via meta-atoms!
        """
        kairos_bonus = 1.5 if self.kairos_detected else 1.0

        # Group affordances by atom (for multi-organ nexuses):
        atom_groups: Dict[str, List[FeltAffordance]] = {}
        for aff in self.felt_affordances:
            if aff.atom not in atom_groups:
                atom_groups[aff.atom] = []
            atom_groups[aff.atom].append(aff)

        for atom, affordances in atom_groups.items():
            # Aggregate across organs that felt this atom:
            total_confidence = sum(aff.confidence for aff in affordances) / len(affordances)
            total_confidence *= kairos_bonus

            # Felt energy (from final V0 state):
            felt_energy = self.v0_energy

            # Organ sources (for nexus tracking):
            organ_sources = [aff.organ_name for aff in affordances]

            # Intersection strength (for nexus weighting):
            intersection_strength = sum(
                aff.confidence * aff.lure_intensity
                for aff in affordances
            )

            # Emission priority: high confidence + low energy = ready to emit
            emission_priority = total_confidence * (1.0 - felt_energy)

            prop = PropositionFeltInterpretation(
                position=self.position,
                atom=atom,
                confidence=total_confidence,
                felt_energy=felt_energy,
                v0_bonus=kairos_bonus,
                organ_sources=organ_sources,
                intersection_strength=intersection_strength,
                emission_priority=emission_priority
            )
            self.mature_propositions.append(prop)

    def set_subjective_aim(
        self,
        lure_direction: str,
        intensity: float,
        ethical_weight: float,
        morphogenetic_guidance: Optional[str] = None
    ):
        """
        🆕 SALIENCE INTEGRATION: Set subjective aim from salience model.

        Whitehead: "The subjective aim is the determinant of the definiteness of
        the actual occasion. It determines why this particular prehension is felt
        rather than another."

        Args:
            lure_direction: Guidance string from salience model (e.g., "crystallize_insight",
                           "trauma_detected_gentle", "ground_present", "establish_safety")
            intensity: How strongly to pursue this aim (0.0-1.0, from morphogenetic pressure)
            ethical_weight: Salience of what matters (from ethical_salience_field term)
            morphogenetic_guidance: Optional override (e.g., "reduce_inflammation")

        Example:
            occasion.set_subjective_aim(
                lure_direction="trauma_detected_gentle",
                intensity=0.45,
                ethical_weight=0.72,
                morphogenetic_guidance="establish_safety"
            )

        Effect on prehension:
        - Modulates emission intensity (high trauma → gentle phrases)
        - Guides nexus selection (safety → prefer safety_restoration meta-atoms)
        - Influences proposition maturation (ethical_weight scales confidence)
        """
        self.subjective_aim = {
            "lure_direction": lure_direction,
            "intensity": intensity,
            "ethical_weight": ethical_weight,
            "morphogenetic_guidance": morphogenetic_guidance or lure_direction,
            "set_at_cycle": self.cycle,
            "v0_context": self.v0_energy
        }

    def get_summary(self) -> Dict:
        """
        Get summary of occasion state for logging/debugging.

        Returns:
            Dictionary with key metrics
        """
        summary = {
            'datum': self.datum,
            'position': self.position,
            'cycle': self.cycle,
            'v0_energy': round(self.v0_energy, 3),
            'satisfaction': round(self.satisfaction, 3),
            'kairos_detected': self.kairos_detected,
            'kairos_cycle': self.kairos_cycle,
            'felt_affordances_count': len(self.felt_affordances),
            'mature_propositions_count': len(self.mature_propositions),
            'unique_atoms': len(set(aff.atom for aff in self.felt_affordances)),
            'unique_organs': len(set(aff.organ_name for aff in self.felt_affordances))
        }

        # 🆕 SALIENCE: Include subjective aim if set
        if self.subjective_aim:
            summary['subjective_aim'] = self.subjective_aim['lure_direction']
            summary['aim_intensity'] = self.subjective_aim['intensity']

        return summary
