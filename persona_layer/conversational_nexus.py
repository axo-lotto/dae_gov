"""
Conversational Nexus - 4-Gate Intersection Architecture

Organ coalition formation with curiosity-driven question generation.
Based on DAE 3.0's validated 4-gate intersection design.

Philosophy:
- Gate 1: INTERSECTION (τ_I = 1.5) - requires ≥2 organs with high lure
- Gate 2: COHERENCE (τ_C = 0.4) - measures organ agreement
- Gate 3: SATISFACTION (Kairos window [0.45, 0.70]) - 1.5× confidence boost
- Gate 4: FELT ENERGY (argmin) - selects response minimizing energy

Curiosity Triggering:
- When coherence < 0.4: System doesn't understand → ask clarifying question
- When intersection < 1.5: Organs disagree → ask exploration question
- Question templates specific to each organ's domain

Architecture:
- Takes 5 organ results + R-matrix coupling
- Computes 4 gates
- Decides: curiosity_question, reflection, insight, or silence
- Returns NexusDecision with suggested action

Author: DAE-GOV Development Team
Created: November 10, 2025
Version: 1.0 (Curiosity-Driven Foundation)
"""

import numpy as np
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class NexusDecision:
    """
    Result of nexus formation (organ coalition decision).

    The organism has spoken. This is what it wants to do next.
    """
    decision_type: str  # 'curiosity_question', 'reflection', 'insight', 'compassion', 'silence'
    confidence: float  # Nexus agreement strength (0.0-1.0)
    contributing_organs: List[str]  # Which organs agreed
    suggested_action: str  # What to do/say next
    felt_energy: float  # Energy of decision (0.0-1.0, lower is better)
    kairos_moment: bool  # Is this a convergence moment?

    # Gate outputs (for debugging/logging)
    intersection_count: float  # How many organs agree (0-5)
    coherence_score: float  # Organ agreement (0.0-1.0)
    in_kairos_window: bool  # Satisfaction in sweet spot

    # Question metadata (if decision_type == 'curiosity_question')
    question_organ: Optional[str] = None  # Which organ generated the question
    question_type: Optional[str] = None  # 'clarification', 'exploration', 'deepening'


class ConversationalNexus:
    """
    4-Gate Intersection Architecture for conversational decisions.

    Based on DAE 3.0 validated design with curiosity triggering.

    Gate 1: INTERSECTION (τ_I = 1.5)
      - Count organs with lure > 0.6
      - Need ≥2 organs to proceed with response
      - <2 organs → trigger curiosity question

    Gate 2: COHERENCE (τ_C = 0.4)
      - Coherence = 1 - std(organ_coherences)
      - Coherence < 0.4 → organs disagree, trigger curiosity
      - Coherence ≥ 0.4 → organs agree, proceed with decision

    Gate 3: SATISFACTION (Kairos window [0.45, 0.70])
      - Mean organ coherence in sweet spot
      - In window → 1.5× confidence boost (transformative moment)
      - Outside window → normal confidence

    Gate 4: FELT ENERGY (argmin)
      - Compute felt energy for each decision type
      - Select decision minimizing energy
      - Lower energy = more organismically satisfying
    """

    def __init__(self, r_matrix: 'ConversationalHebbianMemory'):
        """
        Initialize Conversational Nexus.

        Args:
            r_matrix: Hebbian R-matrix for organ coupling
        """
        self.r_matrix = r_matrix

        # Thresholds (DAE 3.0 validated)
        self.tau_intersection = 1.5  # At least 2 organs
        self.tau_coherence = 0.4  # Minimum agreement
        self.kairos_window = (0.45, 0.70)  # Satisfaction sweet spot
        self.kairos_boost = 1.5  # Confidence multiplier in Kairos

        # Curiosity question templates
        self._init_question_templates()

    def _init_question_templates(self):
        """Initialize curiosity question templates for each organ."""
        self.question_templates = {
            'LISTENING': [
                "Can you say more about that?",
                "What else comes up when you think about this?",
                "I'm curious - what's that like for you?",
                "Help me understand what you mean by that.",
                "What's important about that for you?"
            ],
            'EMPATHY': [
                "How does that feel for you?",
                "What emotions are present as you share this?",
                "What's the felt sense of that?",
                "I'm sensing something here - what's alive for you right now?",
                "What does your heart say about this?"
            ],
            'WISDOM': [
                "What sense are you making of this?",
                "What patterns do you notice here?",
                "How does this fit with your larger understanding?",
                "What's the bigger picture you're seeing?",
                "What does this tell you about yourself/the situation?"
            ],
            'AUTHENTICITY': [
                "What's really true for you here?",
                "What are you not saying that wants to be said?",
                "What would it be like to be completely honest about this?",
                "What's underneath that?",
                "If you could speak from your deepest truth, what would you say?"
            ],
            'PRESENCE': [
                "What are you noticing right now, in this moment?",
                "Can we pause and feel into this together?",
                "What's happening in your body as we talk about this?",
                "Let's stay with this - what's present right here?",
                "What do you sense when you bring your awareness to this?"
            ]
        }

    def form_nexus(
        self,
        organ_results: Dict[str, any],
        coherence_gap_threshold: float = 0.4
    ) -> NexusDecision:
        """
        Form nexus from organ outputs using 4-gate architecture.

        Args:
            organ_results: Dict of organ Result objects
                {
                    'LISTENING': ListeningResult,
                    'EMPATHY': EmpathyResult,
                    'WISDOM': WisdomResult,
                    'AUTHENTICITY': AuthenticityResult,
                    'PRESENCE': PresenceResult
                }
            coherence_gap_threshold: If coherence < this, trigger curiosity

        Returns:
            NexusDecision with action recommendation
        """
        organs = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE']

        # Extract organ values
        coherences = np.array([organ_results[o].coherence for o in organs])
        lures = np.array([organ_results[o].lure for o in organs])

        # GATE 1: INTERSECTION
        # Count organs with high lure (> 0.6)
        high_lure_mask = lures > 0.6
        intersection_count = float(np.sum(high_lure_mask))

        # GATE 2: COHERENCE
        # Measure organ agreement: 1 - std(coherences)
        coherence_score = 1.0 - float(np.std(coherences))

        # GATE 3: SATISFACTION (Kairos)
        # Check if mean coherence in Kairos window
        mean_coherence = float(np.mean(coherences))
        in_kairos_window = self.kairos_window[0] <= mean_coherence <= self.kairos_window[1]

        # GATE 4: FELT ENERGY
        # Compute felt energy for each decision type
        # (lower energy = more satisfying)

        # === DECISION LOGIC ===

        # CURIOSITY TRIGGERED: Low coherence (organs disagree)
        if coherence_score < coherence_gap_threshold:
            return self._generate_curiosity_question(
                organ_results=organ_results,
                organs=organs,
                coherences=coherences,
                lures=lures,
                intersection_count=intersection_count,
                coherence_score=coherence_score,
                in_kairos_window=in_kairos_window,
                question_type='clarification'
            )

        # CURIOSITY TRIGGERED: Low intersection (not enough organs agree)
        if intersection_count < self.tau_intersection:
            return self._generate_curiosity_question(
                organ_results=organ_results,
                organs=organs,
                coherences=coherences,
                lures=lures,
                intersection_count=intersection_count,
                coherence_score=coherence_score,
                in_kairos_window=in_kairos_window,
                question_type='exploration'
            )

        # NORMAL PROCESSING: Organs agree, decide action
        return self._select_by_felt_energy(
            organ_results=organ_results,
            organs=organs,
            coherences=coherences,
            lures=lures,
            intersection_count=intersection_count,
            coherence_score=coherence_score,
            in_kairos_window=in_kairos_window
        )

    def _generate_curiosity_question(
        self,
        organ_results: Dict,
        organs: List[str],
        coherences: np.ndarray,
        lures: np.ndarray,
        intersection_count: float,
        coherence_score: float,
        in_kairos_window: bool,
        question_type: str
    ) -> NexusDecision:
        """
        Generate curiosity question when organism doesn't understand.

        Strategy:
        - If clarification: Ask from organ with LOWEST coherence (most confused)
        - If exploration: Ask from organ with HIGHEST lure (most interested)
        """
        if question_type == 'clarification':
            # Ask from organ with lowest coherence (most confused)
            question_organ_idx = int(np.argmin(coherences))
            confidence = 0.3 + (1.0 - coherence_score) * 0.4  # Low confidence
        else:  # exploration
            # Ask from organ with highest lure (most interested)
            question_organ_idx = int(np.argmax(lures))
            confidence = 0.4 + coherence_score * 0.3  # Medium confidence

        question_organ = organs[question_organ_idx]

        # Select random question template
        question = random.choice(self.question_templates[question_organ])

        # Felt energy for curiosity question (medium-low energy)
        felt_energy = 0.4 + (1.0 - confidence) * 0.2

        return NexusDecision(
            decision_type='curiosity_question',
            confidence=confidence,
            contributing_organs=[question_organ],
            suggested_action=question,
            felt_energy=felt_energy,
            kairos_moment=in_kairos_window,
            intersection_count=intersection_count,
            coherence_score=coherence_score,
            in_kairos_window=in_kairos_window,
            question_organ=question_organ,
            question_type=question_type
        )

    def _select_by_felt_energy(
        self,
        organ_results: Dict,
        organs: List[str],
        coherences: np.ndarray,
        lures: np.ndarray,
        intersection_count: float,
        coherence_score: float,
        in_kairos_window: bool
    ) -> NexusDecision:
        """
        Select decision type by minimizing felt energy.

        Decision types:
        - reflection: Mirror back what was heard (LISTENING-led)
        - compassion: Validate feelings (EMPATHY-led)
        - insight: Offer perspective (WISDOM-led)
        - silence: Hold space (PRESENCE-led)
        """
        # Compute felt energy for each decision type
        # Energy = 1 - (organ_coherence * organ_lure * R_matrix_coupling)

        decisions = []

        # REFLECTION (LISTENING-led)
        listening_idx = organs.index('LISTENING')
        empathy_idx = organs.index('EMPATHY')
        coupling_LE = self.r_matrix.get_coupling('LISTENING', 'EMPATHY')
        reflection_energy = 1.0 - (coherences[listening_idx] * lures[listening_idx] * coupling_LE)
        decisions.append(('reflection', reflection_energy, [listening_idx, empathy_idx]))

        # COMPASSION (EMPATHY-led)
        authenticity_idx = organs.index('AUTHENTICITY')
        coupling_EA = self.r_matrix.get_coupling('EMPATHY', 'AUTHENTICITY')
        compassion_energy = 1.0 - (coherences[empathy_idx] * lures[empathy_idx] * coupling_EA)
        decisions.append(('compassion', compassion_energy, [empathy_idx, authenticity_idx]))

        # INSIGHT (WISDOM-led)
        wisdom_idx = organs.index('WISDOM')
        coupling_WE = self.r_matrix.get_coupling('WISDOM', 'EMPATHY')
        insight_energy = 1.0 - (coherences[wisdom_idx] * lures[wisdom_idx] * coupling_WE)
        decisions.append(('insight', insight_energy, [wisdom_idx, empathy_idx]))

        # SILENCE (PRESENCE-led)
        presence_idx = organs.index('PRESENCE')
        coupling_PL = self.r_matrix.get_coupling('PRESENCE', 'LISTENING')
        silence_energy = 1.0 - (coherences[presence_idx] * lures[presence_idx] * coupling_PL)
        decisions.append(('silence', silence_energy, [presence_idx, listening_idx]))

        # Select decision with lowest felt energy
        decision_type, felt_energy, organ_indices = min(decisions, key=lambda x: x[1])
        contributing_organs = [organs[i] for i in organ_indices]

        # Compute confidence
        base_confidence = coherence_score * 0.6 + intersection_count / 5.0 * 0.4

        # Kairos boost
        if in_kairos_window:
            confidence = min(base_confidence * self.kairos_boost, 1.0)
            kairos_moment = True
        else:
            confidence = base_confidence
            kairos_moment = False

        # Generate suggested action
        suggested_action = self._generate_action_text(
            decision_type=decision_type,
            confidence=confidence,
            organ_results=organ_results,
            contributing_organs=contributing_organs
        )

        return NexusDecision(
            decision_type=decision_type,
            confidence=confidence,
            contributing_organs=contributing_organs,
            suggested_action=suggested_action,
            felt_energy=felt_energy,
            kairos_moment=kairos_moment,
            intersection_count=intersection_count,
            coherence_score=coherence_score,
            in_kairos_window=in_kairos_window
        )

    def _generate_action_text(
        self,
        decision_type: str,
        confidence: float,
        organ_results: Dict,
        contributing_organs: List[str]
    ) -> str:
        """Generate suggested action text based on decision type."""
        # This is a simplified version - in production, this would integrate
        # with response generation system

        actions = {
            'reflection': "Reflect back what you heard with empathic presence.",
            'compassion': "Validate their feelings with warmth and holding.",
            'insight': "Offer a reframe or broader perspective gently.",
            'silence': "Hold space in silence, letting them feel into this."
        }

        return actions.get(decision_type, "Listen and be present.")


# Module-level convenience function
def create_conversational_nexus(r_matrix: 'ConversationalHebbianMemory') -> ConversationalNexus:
    """
    Create Conversational Nexus.

    Args:
        r_matrix: Hebbian R-matrix for organ coupling

    Returns:
        ConversationalNexus instance
    """
    return ConversationalNexus(r_matrix=r_matrix)


if __name__ == '__main__':
    """Test Conversational Nexus with simulated organ results."""

    print("="*70)
    print("CONVERSATIONAL NEXUS - Test")
    print("="*70)
    print()

    # Import R-matrix
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))

    from organs.orchestration.conversational_hebbian import ConversationalHebbianMemory

    # Create R-matrix and nexus
    r_matrix = ConversationalHebbianMemory()
    nexus = create_conversational_nexus(r_matrix)

    # Simulate 3 test scenarios
    from dataclasses import dataclass

    @dataclass
    class MockResult:
        coherence: float
        lure: float

    # TEST 1: Low coherence → Curiosity question
    print("TEST 1: Low Coherence (organs disagree)")
    print("-" * 70)
    organ_results_1 = {
        'LISTENING': MockResult(coherence=0.25, lure=0.40),
        'EMPATHY': MockResult(coherence=0.30, lure=0.35),
        'WISDOM': MockResult(coherence=0.65, lure=0.70),
        'AUTHENTICITY': MockResult(coherence=0.40, lure=0.45),
        'PRESENCE': MockResult(coherence=0.35, lure=0.50)
    }

    decision_1 = nexus.form_nexus(organ_results_1)
    print(f"Decision: {decision_1.decision_type}")
    print(f"Confidence: {decision_1.confidence:.2f}")
    print(f"Question: {decision_1.suggested_action}")
    print(f"From organ: {decision_1.question_organ}")
    print(f"Coherence: {decision_1.coherence_score:.2f}")
    print()

    # TEST 2: Low intersection → Curiosity question
    print("TEST 2: Low Intersection (not enough organs agree)")
    print("-" * 70)
    organ_results_2 = {
        'LISTENING': MockResult(coherence=0.75, lure=0.45),  # Low lure
        'EMPATHY': MockResult(coherence=0.80, lure=0.50),    # Low lure
        'WISDOM': MockResult(coherence=0.78, lure=0.85),     # High lure
        'AUTHENTICITY': MockResult(coherence=0.72, lure=0.40),  # Low lure
        'PRESENCE': MockResult(coherence=0.77, lure=0.35)    # Low lure
    }

    decision_2 = nexus.form_nexus(organ_results_2)
    print(f"Decision: {decision_2.decision_type}")
    print(f"Confidence: {decision_2.confidence:.2f}")
    print(f"Question: {decision_2.suggested_action}")
    print(f"From organ: {decision_2.question_organ}")
    print(f"Intersection: {decision_2.intersection_count:.1f} organs")
    print()

    # TEST 3: High coherence + intersection → Normal decision
    print("TEST 3: High Coherence + Intersection (organs agree)")
    print("-" * 70)
    organ_results_3 = {
        'LISTENING': MockResult(coherence=0.85, lure=0.75),
        'EMPATHY': MockResult(coherence=0.88, lure=0.85),
        'WISDOM': MockResult(coherence=0.82, lure=0.70),
        'AUTHENTICITY': MockResult(coherence=0.87, lure=0.80),
        'PRESENCE': MockResult(coherence=0.90, lure=0.85)
    }

    decision_3 = nexus.form_nexus(organ_results_3)
    print(f"Decision: {decision_3.decision_type}")
    print(f"Confidence: {decision_3.confidence:.2f}")
    print(f"Action: {decision_3.suggested_action}")
    print(f"Contributing organs: {', '.join(decision_3.contributing_organs)}")
    print(f"Felt energy: {decision_3.felt_energy:.2f}")
    print(f"Kairos moment: {decision_3.kairos_moment}")
    print(f"Coherence: {decision_3.coherence_score:.2f}")
    print()

    print("="*70)
    print("✅ Conversational Nexus operational")
    print("="*70)
