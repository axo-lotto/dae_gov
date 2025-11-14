"""
Conversational Hebbian Learning Memory
DAE-GOV Persona Layer Pattern Learning System

Adapted from DAE 3.0 V0HebbianMemory for conversational pattern learning.
Learns which interventions work (grounding, containment, SELF-led responses)
in which contexts (polyvagal states, SELF-energy levels, conversational families).

Core Principle: "Neurons that fire together, wire together" →
                "Patterns that succeed together, strengthen together"

Architecture:
- 4×4 detector coupling matrix (Polyvagal ↔ SELF-Energy ↔ OFEL ↔ CARD)
- 4 pattern memory types (polyvagal, self_energy, cascade, response)
- Outcome-gated learning (η=0.01, δ=0.001 from FFITTSS)
- Clinical safety guardrails (never learn to ignore danger)

Integration:
- Persona layer detectors learn from conversational outcomes
- Fresh model baseline: polyvagal (0.44-0.53), SELF-energy (0.001-0.05)
- Expected improvement: +0.20-0.30pp after 50-100 conversations
- CARD-aware: Respects bodily rhythms (urgency ↔ response scaling)

Date: November 10, 2025
Status: Phase 1.5c - Conversational Hebbian Memory Implementation
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import json
import numpy as np
from datetime import datetime


@dataclass
class ConversationalOutcome:
    """Captures conversation turn outcome for learning"""

    # Current state (before intervention) - REQUIRED FIELDS
    polyvagal_state: str  # 'ventral', 'sympathetic', 'dorsal'
    polyvagal_confidence: float
    self_energy: float
    self_energy_confidence: float
    dominant_c: str  # Which of 8 C's was dominant
    cs_activation: Dict[str, float]  # All 8 C's activations
    conversational_family: str  # 'crisis', 'parts_work', 'self_led', 'grounding'
    satisfaction: float
    coherence: float
    ofel_energy: float
    card_scale: str  # 'minimal', 'brief', 'moderate', 'detailed', 'comprehensive'
    gate_decision: str  # 'CONTAIN', 'CLARIFY', 'GROUND', 'RESPOND'
    response_text: str
    response_quality: str

    # OPTIONAL FIELDS (must come after required fields)
    # Next state (after intervention, if available)
    next_polyvagal_state: Optional[str] = None
    next_self_energy: Optional[float] = None
    next_satisfaction: Optional[float] = None

    # Explicit feedback (if provided)
    explicit_feedback: Optional[str] = None  # 'helpful', 'not_helpful', 'neutral'

    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class ConversationalHebbianMemory:
    """
    Hebbian learning for DAE-GOV persona layer.

    Learns from conversational outcomes across 4 detection systems:
    - Polyvagal (3 states: ventral, sympathetic, dorsal)
    - SELF-energy (8 C's: compassion, curiosity, clarity, calm, confidence, courage, creativity, connectedness)
    - OFEL (safety boundaries based on exclusion field)
    - CARD (response scaling based on bodily rhythms)

    Adapted from DAE 3.0 V0HebbianMemory (6×6 organ coupling) →
    4×4 detector coupling (Polyvagal ↔ SELF-Energy ↔ OFEL ↔ CARD)
    """

    def __init__(
        self,
        eta: float = 0.01,
        delta: float = 0.001,
        success_threshold: float = 0.7,
        storage_path: Optional[str] = None
    ):
        """
        Initialize conversational Hebbian memory.

        Args:
            eta: Learning rate (from FFITTSS satisfaction calibration)
            delta: Decay rate (pattern forgetting)
            success_threshold: Minimum threshold for considering outcome "successful"
            storage_path: Path to JSON storage file
        """
        # Detector names (4 systems in persona layer)
        self.detector_names = ['Polyvagal', 'SELF-Energy', 'OFEL', 'CARD']

        # 4×4 detector coupling matrix (Hebbian R-matrix adapted for persona layer)
        # Initialized with weak baseline coupling (0.1 on diagonal)
        self.R_matrix = np.eye(4) * 0.1

        # Pattern memory dictionaries (what gets learned)
        self.polyvagal_patterns = self._init_polyvagal_patterns()
        self.self_energy_patterns = self._init_self_energy_patterns()
        self.cascade_patterns = {}  # gate+context → threshold adjustments
        self.response_patterns = {}  # family+C → effectiveness scores

        # Learning hyperparameters
        self.eta = eta
        self.delta = delta
        self.success_threshold = success_threshold

        # Tracking metrics
        self.update_count = 0
        self.success_count = 0
        self.failure_count = 0

        # Clinical safety tracking
        self.danger_detections = 0
        self.dangerous_blending_detections = 0
        self.containment_interventions = 0
        self.never_ignored_danger = True

        # Storage (aligned with knowledge_base infrastructure)
        self.storage_path = Path(storage_path) if storage_path else Path("knowledge_base/persona_layer_hebbian_memory.json")

        # Load existing patterns if available
        if self.storage_path.exists() and self.storage_path.stat().st_size > 0:
            self.load()

    def _init_polyvagal_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize polyvagal pattern memory structure"""
        return {
            'ventral': {
                'confidence_boost': 0.0,
                'success_count': 0,
                'text_clusters': []
            },
            'sympathetic': {
                'confidence_boost': 0.0,
                'success_count': 0,
                'text_clusters': []
            },
            'dorsal': {
                'confidence_boost': 0.0,
                'success_count': 0,
                'text_clusters': []
            }
        }

    def _init_self_energy_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize SELF-energy pattern memory structure (8 C's)"""
        cs = ['compassion', 'curiosity', 'clarity', 'calm', 'confidence', 'courage', 'creativity', 'connectedness']
        return {
            c: {
                'boost': 0.0,
                'family_effectiveness': {}  # family → effectiveness score
            }
            for c in cs
        }

    def update_from_outcome(
        self,
        outcome: ConversationalOutcome
    ) -> Dict[str, Any]:
        """
        Update Hebbian memory from conversation outcome.

        Determines if outcome was positive/negative/neutral, then strengthens
        or decays patterns accordingly.

        Args:
            outcome: ConversationalOutcome dataclass with current + next state

        Returns:
            Update statistics dict
        """
        # Determine outcome quality
        outcome_quality = self._determine_outcome_quality(outcome)

        # Update tracking
        self.update_count += 1

        # Log first update to verify learning activation
        if self.update_count == 1:
            print(f"🧠 HEBBIAN R-MATRIX: First learning update detected!")
            print(f"   Outcome quality: {outcome_quality}")
            print(f"   Polyvagal state: {outcome.polyvagal_state}")
            print(f"   SELF-energy: {outcome.self_energy:.3f}")
            print(f"   Family: {outcome.conversational_family}")

        if outcome_quality == 'positive':
            self.success_count += 1
        elif outcome_quality == 'negative':
            self.failure_count += 1

        # Update different pattern types based on outcome
        updates = {
            'outcome_quality': outcome_quality,
            'polyvagal_update': 0.0,
            'self_energy_update': 0.0,
            'cascade_update': 0.0,
            'response_update': 0.0,
            'r_matrix_update': 0.0
        }

        if outcome_quality == 'positive':
            # Strengthen patterns that led to success
            updates['polyvagal_update'] = self._strengthen_polyvagal_pattern(outcome)
            updates['self_energy_update'] = self._strengthen_self_energy_pattern(outcome)
            updates['cascade_update'] = self._strengthen_cascade_pattern(outcome)
            updates['response_update'] = self._strengthen_response_pattern(outcome)
            updates['r_matrix_update'] = self._update_r_matrix(outcome, strengthened=True)

        elif outcome_quality == 'negative':
            # Decay patterns slightly (forget unsuccessful approaches)
            updates['polyvagal_update'] = self._decay_polyvagal_patterns()
            updates['self_energy_update'] = self._decay_self_energy_patterns()
            updates['cascade_update'] = self._decay_cascade_patterns()
            updates['response_update'] = self._decay_response_patterns()
            updates['r_matrix_update'] = self._update_r_matrix(outcome, strengthened=False)

        # Neutral outcomes: no update (preserve memory)

        return updates

    def learn_from_outcome(
        self,
        outcome: ConversationalOutcome
    ) -> Dict[str, Any]:
        """
        Alias for update_from_outcome() for API compatibility.

        ProductionLearningCoordinator expects this method name.
        Internally calls update_from_outcome() for actual learning logic.

        Args:
            outcome: ConversationalOutcome dataclass with current + next state

        Returns:
            Update statistics dict with pattern update metrics:
            {
                'outcome_quality': str,
                'polyvagal_update': float,
                'self_energy_update': float,
                'cascade_update': float,
                'response_update': float,
                'r_matrix_update': float
            }
        """
        return self.update_from_outcome(outcome)

    def _determine_outcome_quality(self, outcome: ConversationalOutcome) -> str:
        """
        Determine if conversation turn was positive, negative, or neutral.

        Success indicators (ordered by reliability):
        1. Explicit feedback (gold standard)
        2. Polyvagal state improvement
        3. SELF-energy increase
        4. Cascade progression

        Args:
            outcome: ConversationalOutcome with current + next state

        Returns:
            'positive', 'negative', or 'neutral'
        """
        # 1. Explicit feedback (if provided)
        if outcome.explicit_feedback == 'helpful':
            return 'positive'
        elif outcome.explicit_feedback == 'not_helpful':
            return 'negative'

        # 2. Polyvagal state improvement
        if outcome.next_polyvagal_state is not None:
            polyvagal_order = {'dorsal': 0, 'sympathetic': 1, 'ventral': 2}
            current_level = polyvagal_order.get(outcome.polyvagal_state, 0)
            next_level = polyvagal_order.get(outcome.next_polyvagal_state, 0)

            if next_level > current_level:
                return 'positive'  # Movement toward ventral = improvement
            elif next_level < current_level:
                return 'negative'  # Movement toward dorsal = regression

        # 3. SELF-energy increase
        if outcome.next_self_energy is not None:
            self_energy_delta = outcome.next_self_energy - outcome.self_energy

            if self_energy_delta > 0.1:  # Meaningful increase
                return 'positive'
            elif self_energy_delta < -0.1:  # Meaningful decrease
                return 'negative'

        # 4. Cascade progression (high satisfaction + RESPOND gate = likely success)
        if outcome.gate_decision == 'RESPOND' and outcome.satisfaction > 0.7:
            return 'positive'

        # 5. Crisis containment (CONTAIN in crisis family = appropriate response)
        if outcome.conversational_family == 'crisis' and outcome.gate_decision == 'CONTAIN':
            return 'positive'  # Clinical safety success

        # Default: neutral (insufficient information)
        return 'neutral'

    def _strengthen_polyvagal_pattern(self, outcome: ConversationalOutcome) -> float:
        """
        Strengthen polyvagal detection pattern for this state.

        Hebbian update: confidence_boost += η * (1 - current_confidence)

        Args:
            outcome: ConversationalOutcome with polyvagal state

        Returns:
            Update magnitude
        """
        state = outcome.polyvagal_state
        pattern = self.polyvagal_patterns[state]

        # Hebbian strengthening (asymptotic to 1.0)
        confidence_delta = self.eta * (1.0 - outcome.polyvagal_confidence)
        pattern['confidence_boost'] += confidence_delta
        pattern['success_count'] += 1

        # Store text cluster association (simple keyword extraction)
        # In full implementation: use embedding clustering
        # For now: placeholder for future enhancement

        return confidence_delta

    def _strengthen_self_energy_pattern(self, outcome: ConversationalOutcome) -> float:
        """
        Strengthen SELF-energy detection pattern for dominant C.

        Learns which C's are effective in which conversational families.

        Args:
            outcome: ConversationalOutcome with SELF-energy + C activation

        Returns:
            Update magnitude
        """
        dominant_c = outcome.dominant_c
        family = outcome.conversational_family

        if dominant_c not in self.self_energy_patterns:
            return 0.0

        pattern = self.self_energy_patterns[dominant_c]

        # Strengthen C activation
        activation_delta = self.eta * outcome.cs_activation.get(dominant_c, 0.0)
        pattern['boost'] += activation_delta

        # Update family effectiveness
        if family not in pattern['family_effectiveness']:
            pattern['family_effectiveness'][family] = 0.0

        pattern['family_effectiveness'][family] += self.eta * outcome.satisfaction

        return activation_delta

    def _track_clinical_safety(self, outcome: ConversationalOutcome) -> None:
        """Track clinical safety metrics."""
        # Track danger detections
        if outcome.ofel_energy > 0.7:
            self.danger_detections += 1

        # Track dangerous blending (high satisfaction + low SELF in crisis)
        if (outcome.conversational_family == 'crisis' and
            outcome.satisfaction > 0.8 and
            outcome.self_energy < 0.4):
            self.dangerous_blending_detections += 1

        # Track containment interventions
        if outcome.gate_decision == 'CONTAIN':
            self.containment_interventions += 1

        # Verify we never ignored danger (should always contain if DANGER detected)
        if outcome.ofel_energy > 0.7 and outcome.gate_decision != 'CONTAIN':
            self.never_ignored_danger = False

    def _strengthen_cascade_pattern(self, outcome: ConversationalOutcome) -> float:
        """
        Strengthen cascade gate decision pattern for this context.

        Learns context-specific threshold adjustments:
        - Crisis + High satisfaction → More conservative (lower SELF threshold)
        - SELF-led + Low satisfaction → Less conservative (higher threshold)

        Args:
            outcome: ConversationalOutcome with cascade decision

        Returns:
            Update magnitude
        """
        # Create context hash
        context_key = f"{outcome.conversational_family}_{outcome.gate_decision}_{outcome.satisfaction:.1f}"

        if context_key not in self.cascade_patterns:
            self.cascade_patterns[context_key] = {
                'threshold_adjustment': 0.0,
                'success_count': 0
            }

        pattern = self.cascade_patterns[context_key]

        # Clinical safety: Crisis family should become MORE conservative
        if outcome.conversational_family == 'crisis' and outcome.satisfaction > 0.8:
            # High satisfaction in crisis = dangerous blending
            # Learn to be MORE cautious (negative threshold adjustment)
            adjustment_delta = -self.eta * 0.05  # Lower threshold = more conservative
        else:
            # Standard: successful pattern reinforcement
            adjustment_delta = self.eta * 0.02

        pattern['threshold_adjustment'] += adjustment_delta
        pattern['success_count'] += 1

        return abs(adjustment_delta)

    def _strengthen_response_pattern(self, outcome: ConversationalOutcome) -> float:
        """
        Strengthen response C selection pattern for this family.

        Learns which C's work best in which conversational families:
        - Crisis family → compassion + calm effective
        - Parts work family → curiosity + compassion effective
        - SELF-led family → all C's effective

        Args:
            outcome: ConversationalOutcome with response info

        Returns:
            Update magnitude
        """
        family = outcome.conversational_family
        dominant_c = outcome.dominant_c

        if family not in self.response_patterns:
            self.response_patterns[family] = {}

        if dominant_c not in self.response_patterns[family]:
            self.response_patterns[family][dominant_c] = {
                'effectiveness': 0.0,
                'use_count': 0
            }

        pattern = self.response_patterns[family][dominant_c]

        # Update effectiveness based on satisfaction
        effectiveness_delta = self.eta * outcome.satisfaction
        pattern['effectiveness'] += effectiveness_delta
        pattern['use_count'] += 1

        return effectiveness_delta

    def _update_r_matrix(self, outcome: ConversationalOutcome, strengthened: bool) -> float:
        """
        Update detector coupling matrix (Hebbian R-matrix).

        Learns which detectors co-activate successfully:
        - Polyvagal ↔ SELF-Energy (strong coupling expected)
        - OFEL ↔ Polyvagal (safety ↔ autonomic state)
        - CARD ↔ SELF-Energy (response scaling ↔ SELF presence)

        Adapted from DAE 3.0 organ R-matrix (6×6) → detector R-matrix (4×4)

        Args:
            outcome: ConversationalOutcome with detector activations
            strengthened: True if successful outcome (strengthen), False if unsuccessful (decay)

        Returns:
            Total R-matrix update magnitude
        """
        # Compute detector "activations" (0-1 scale)
        activations = np.array([
            outcome.polyvagal_confidence,  # Polyvagal detector
            outcome.self_energy_confidence,  # SELF-Energy detector
            1.0 - outcome.ofel_energy,  # OFEL detector (inverted: low energy = high activation)
            0.5  # CARD detector (placeholder: use scaling appropriateness in future)
        ])

        if strengthened:
            # Hebbian strengthening: R[i,j] += η * a[i] * a[j] * (1 - R[i,j])
            for i in range(4):
                for j in range(4):
                    if i != j:  # Don't update diagonal
                        coupling_delta = self.eta * activations[i] * activations[j] * (1.0 - self.R_matrix[i, j])
                        self.R_matrix[i, j] += coupling_delta
        else:
            # Decay: R[i,j] *= (1 - δ)
            self.R_matrix *= (1.0 - self.delta)

            # Maintain minimum baseline (don't decay below 0.05)
            self.R_matrix = np.maximum(self.R_matrix, 0.05)

        # Maintain diagonal at 0.1 (self-coupling baseline)
        np.fill_diagonal(self.R_matrix, 0.1)

        return np.sum(np.abs(self.R_matrix - np.eye(4) * 0.1))  # Total coupling strength

    def _decay_polyvagal_patterns(self) -> float:
        """Decay all polyvagal patterns slightly"""
        total_decay = 0.0
        for state, pattern in self.polyvagal_patterns.items():
            decay = pattern['confidence_boost'] * self.delta
            pattern['confidence_boost'] = max(0.0, pattern['confidence_boost'] - decay)
            total_decay += decay
        return total_decay

    def _decay_self_energy_patterns(self) -> float:
        """Decay all SELF-energy patterns slightly"""
        total_decay = 0.0
        for c, pattern in self.self_energy_patterns.items():
            decay = pattern['boost'] * self.delta
            pattern['boost'] = max(0.0, pattern['boost'] - decay)
            total_decay += decay
        return total_decay

    def _decay_cascade_patterns(self) -> float:
        """Decay all cascade patterns slightly"""
        total_decay = 0.0
        for context_key, pattern in self.cascade_patterns.items():
            decay = abs(pattern['threshold_adjustment']) * self.delta
            # Decay toward zero (neutral)
            if pattern['threshold_adjustment'] > 0:
                pattern['threshold_adjustment'] -= decay
            else:
                pattern['threshold_adjustment'] += decay
            total_decay += decay
        return total_decay

    def _decay_response_patterns(self) -> float:
        """Decay all response patterns slightly"""
        total_decay = 0.0
        for family, cs in self.response_patterns.items():
            for c, pattern in cs.items():
                decay = pattern['effectiveness'] * self.delta
                pattern['effectiveness'] = max(0.0, pattern['effectiveness'] - decay)
                total_decay += decay
        return total_decay

    # === RETRIEVAL METHODS (for use during cascade processing) ===

    def get_polyvagal_boost(self, text: str, detected_state: str) -> float:
        """
        Get learned confidence boost for detected polyvagal state.

        Args:
            text: Conversational text (future: use for cluster matching)
            detected_state: Detected polyvagal state ('ventral', 'sympathetic', 'dorsal')

        Returns:
            Confidence boost to add to fresh model detection (0.0 to ~0.3)
        """
        if detected_state not in self.polyvagal_patterns:
            return 0.0

        return self.polyvagal_patterns[detected_state]['confidence_boost']

    def get_self_energy_boost(self, dominant_c: str, family: str) -> float:
        """
        Get learned boost for C effectiveness in family.

        Args:
            dominant_c: Detected dominant C
            family: Conversational family

        Returns:
            Effectiveness boost for this C in this family
        """
        if dominant_c not in self.self_energy_patterns:
            return 0.0

        pattern = self.self_energy_patterns[dominant_c]
        return pattern['family_effectiveness'].get(family, 0.0)

    def get_threshold_adjustment(self, gate: str, family: str, satisfaction: float) -> float:
        """
        Get learned threshold adjustment for gate in context.

        Args:
            gate: Gate name ('gate_3', etc.)
            family: Conversational family
            satisfaction: Current satisfaction level

        Returns:
            Threshold adjustment (positive = more permissive, negative = more conservative)
        """
        # Construct context key
        context_key = f"{family}_{gate}_{satisfaction:.1f}"

        if context_key in self.cascade_patterns:
            return self.cascade_patterns[context_key]['threshold_adjustment']

        # No learned pattern: return neutral
        return 0.0

    def get_c_preferences(self, family: str) -> Dict[str, float]:
        """
        Get learned C preferences for conversational family.

        Args:
            family: Conversational family

        Returns:
            Dict of C → effectiveness scores
        """
        if family not in self.response_patterns:
            return {}

        # Return effectiveness scores for all C's in this family
        return {
            c: pattern['effectiveness']
            for c, pattern in self.response_patterns[family].items()
        }

    @property
    def success_rate(self) -> float:
        """Compute success rate (successes / total updates)."""
        if self.update_count == 0:
            return 0.0
        return self.success_count / self.update_count

    def get_global_confidence(self) -> float:
        """Get global learning confidence based on success rate and pattern count."""
        if self.update_count < 10:
            return 0.0  # Not enough data yet

        # Combine success rate with pattern maturity
        pattern_maturity = min(1.0, self.update_count / 100.0)
        return self.success_rate * pattern_maturity

    def get_r_matrix_coupling(self, detector1: str, detector2: str) -> float:
        """
        Get learned coupling strength between two detectors.

        Args:
            detector1: First detector name (e.g., 'Polyvagal')
            detector2: Second detector name (e.g., 'SELF-Energy')

        Returns:
            Coupling strength (0.0 to 1.0)
        """
        idx1 = self.detector_names.index(detector1) if detector1 in self.detector_names else -1
        idx2 = self.detector_names.index(detector2) if detector2 in self.detector_names else -1

        if idx1 == -1 or idx2 == -1:
            return 0.0

        return self.R_matrix[idx1, idx2]

    # === PERSISTENCE ===

    def save(self) -> None:
        """Save Hebbian memory to JSON file"""
        data = {
            'version': '1.0',
            'update_count': self.update_count,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'danger_detections': self.danger_detections,
            'dangerous_blending_detections': self.dangerous_blending_detections,
            'containment_interventions': self.containment_interventions,
            'never_ignored_danger': self.never_ignored_danger,
            'failure_count': self.failure_count,
            'detector_coupling_matrix': self.R_matrix.tolist(),
            'polyvagal_patterns': self.polyvagal_patterns,
            'self_energy_patterns': self.self_energy_patterns,
            'cascade_patterns': self.cascade_patterns,
            'response_patterns': self.response_patterns,
            'hyperparameters': {
                'eta': self.eta,
                'delta': self.delta,
                'success_threshold': self.success_threshold
            },
            'timestamp': datetime.now().isoformat()
        }

        # Ensure parent directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        """Load Hebbian memory from JSON file"""
        if not self.storage_path.exists():
            return

        with open(self.storage_path, 'r') as f:
            data = json.load(f)

        # Load state
        self.update_count = data.get('update_count', 0)
        self.success_count = data.get('success_count', 0)
        self.failure_count = data.get('failure_count', 0)
        self.danger_detections = data.get('danger_detections', 0)
        self.dangerous_blending_detections = data.get('dangerous_blending_detections', 0)
        self.containment_interventions = data.get('containment_interventions', 0)
        self.never_ignored_danger = data.get('never_ignored_danger', True)
        self.R_matrix = np.array(data.get('detector_coupling_matrix', np.eye(4) * 0.1))
        self.polyvagal_patterns = data.get('polyvagal_patterns', self._init_polyvagal_patterns())
        self.self_energy_patterns = data.get('self_energy_patterns', self._init_self_energy_patterns())
        self.cascade_patterns = data.get('cascade_patterns', {})
        self.response_patterns = data.get('response_patterns', {})

        # Load hyperparameters if present
        hyperparams = data.get('hyperparameters', {})
        self.eta = hyperparams.get('eta', self.eta)
        self.delta = hyperparams.get('delta', self.delta)
        self.success_threshold = hyperparams.get('success_threshold', self.success_threshold)

    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            'total_updates': self.update_count,
            'successes': self.success_count,
            'failures': self.failure_count,
            'success_rate': self.success_count / self.update_count if self.update_count > 0 else 0.0,
            'polyvagal_learned_patterns': sum(
                1 for p in self.polyvagal_patterns.values() if p['confidence_boost'] > 0.1
            ),
            'self_energy_learned_patterns': sum(
                1 for p in self.self_energy_patterns.values() if p['boost'] > 0.1
            ),
            'cascade_learned_patterns': len(self.cascade_patterns),
            'response_learned_patterns': sum(len(cs) for cs in self.response_patterns.values()),
            'r_matrix_total_coupling': float(np.sum(self.R_matrix) - np.trace(self.R_matrix)),
            'r_matrix_max_coupling': float(np.max(self.R_matrix[~np.eye(4, dtype=bool)])),
            'detector_names': self.detector_names
        }
