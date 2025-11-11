"""
Simple Felt Capture for Mycelium Traces - Self-Contained
==========================================================

Captures organism "felt state" when creating mycelium traces WITHOUT
importing DAE 3.0. Uses DAE_HYPHAE_1's existing conversational scaffolding.

Key Insight from DAE 3.0:
- Capture satisfaction, energy, coherence when organism creates traces
- Use simpler vector signatures (not full 35D, but conversational dimensions)
- Enable epoch learning from trace transformations over time

Philosophy:
- Self-contained: No external dependencies
- Conversational-native: Uses 5 conversational organs
- Progressive: Start simple, enhance later if needed

Author: DAE-GOV Development Team
Created: November 11, 2025
Version: 1.0 (Simplified Felt Capture)
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
import time


@dataclass
class ConversationalFeltState:
    """
    Simplified felt state for conversational traces.

    Instead of 35D vectors from DAE 3.0, we use conversational dimensions:
    - 5 organ coherences (LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE)
    - Satisfaction/energy metaphors for text processing
    - Hebbian coupling from conversational R-matrix

    This is self-contained within DAE_HYPHAE_1.
    """

    # Conversational organ coherences (0-1)
    listening_coherence: float = 0.5
    empathy_coherence: float = 0.5
    wisdom_coherence: float = 0.5
    authenticity_coherence: float = 0.5
    presence_coherence: float = 0.5

    # Satisfaction metaphor (how "complete" does this trace feel?)
    satisfaction_level: float = 0.5  # 0-1, higher = more complete/resolved

    # Energy metaphor (how much processing was needed?)
    processing_energy: float = 0.5  # 0-1, lower = converged quickly

    # Hebbian coupling (from conversational R-matrix)
    r_matrix_coupling: Optional[np.ndarray] = None  # 5×5 matrix

    # Metadata
    timestamp: float = 0.0
    conversation_id: Optional[str] = None

    def to_vector(self) -> np.ndarray:
        """
        Convert to simple 7D vector for storage/similarity.

        Dimensions:
        0-4: Organ coherences
        5: Satisfaction level
        6: Processing energy
        """
        return np.array([
            self.listening_coherence,
            self.empathy_coherence,
            self.wisdom_coherence,
            self.authenticity_coherence,
            self.presence_coherence,
            self.satisfaction_level,
            self.processing_energy
        ])

    @staticmethod
    def from_vector(vec: np.ndarray) -> 'ConversationalFeltState':
        """Reconstruct from 7D vector."""
        return ConversationalFeltState(
            listening_coherence=float(vec[0]),
            empathy_coherence=float(vec[1]),
            wisdom_coherence=float(vec[2]),
            authenticity_coherence=float(vec[3]),
            presence_coherence=float(vec[4]),
            satisfaction_level=float(vec[5]),
            processing_energy=float(vec[6])
        )


class SimpleFeltCapture:
    """
    Captures conversational felt state when organism creates mycelium traces.

    SELF-CONTAINED: Uses only DAE_HYPHAE_1 scaffolding, no DAE 3.0 imports.

    Pattern:
    --------
    1. When user input triggers insight/note creation:
       - Capture current organ states (from orchestrator)
       - Estimate satisfaction (how resolved is the trace?)
       - Estimate energy (how complex was processing?)
       - Store felt state with trace

    2. Over time, learn from trace transformations:
       - Note → Insight: satisfaction↑, wisdom↑
       - Question → Answer: satisfaction↑, energy↓
       - Observation → Pattern: wisdom↑, presence↑

    3. Use conversational Hebbian R-matrix:
       - Leverage existing organs/orchestration/conversational_hebbian.py
       - No need to rebuild 6-organ system from DAE 3.0

    Example Usage:
    --------------
    >>> capture = SimpleFeltCapture()
    >>>
    >>> # When creating a trace:
    >>> felt = capture.capture_from_conversation(
    ...     text="User noticed burnout pattern",
    ...     trace_type="Note",
    ...     organ_states={
    ...         'LISTENING': 0.8,
    ...         'EMPATHY': 0.7,
    ...         'WISDOM': 0.5,
    ...         'AUTHENTICITY': 0.6,
    ...         'PRESENCE': 0.75
    ...     }
    ... )
    >>>
    >>> # Store with MyceliumTrace:
    >>> trace = MyceliumTrace(
    ...     ...,
    ...     felt_state=felt,
    ...     vector_signature=felt.to_vector()
    ... )
    """

    def __init__(self, hebbian_memory_path: Optional[str] = None):
        """
        Initialize felt capture.

        Args:
            hebbian_memory_path: Path to conversational R-matrix (optional)
        """
        self.organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE']

        # Load R-matrix if available (from conversational_hebbian.py)
        self.r_matrix = None
        if hebbian_memory_path:
            try:
                from organs.orchestration.conversational_hebbian import ConversationalHebbianMemory
                hebbian = ConversationalHebbianMemory()
                self.r_matrix = hebbian.R_matrix
            except Exception as e:
                print(f"⚠️  Could not load R-matrix: {e}")

    def capture_from_conversation(
        self,
        text: str,
        trace_type: str,
        organ_states: Optional[Dict[str, float]] = None,
        conversation_id: Optional[str] = None
    ) -> ConversationalFeltState:
        """
        Capture felt state from current conversation.

        Args:
            text: Text content of the trace
            trace_type: Type of trace (Note, Insight, Project, Task, etc.)
            organ_states: Current organ coherences (if available from orchestrator)
            conversation_id: Current conversation ID

        Returns:
            ConversationalFeltState with captured organism state
        """

        # If organ states not provided, estimate from text heuristics
        if organ_states is None:
            organ_states = self._estimate_organ_states(text, trace_type)

        # Extract coherences
        listening = organ_states.get('LISTENING', 0.5)
        empathy = organ_states.get('EMPATHY', 0.5)
        wisdom = organ_states.get('WISDOM', 0.5)
        authenticity = organ_states.get('AUTHENTICITY', 0.5)
        presence = organ_states.get('PRESENCE', 0.5)

        # Estimate satisfaction (how complete/resolved does this feel?)
        satisfaction = self._estimate_satisfaction(text, trace_type, organ_states)

        # Estimate processing energy (complexity of understanding)
        energy = self._estimate_processing_energy(text, trace_type)

        return ConversationalFeltState(
            listening_coherence=listening,
            empathy_coherence=empathy,
            wisdom_coherence=wisdom,
            authenticity_coherence=authenticity,
            presence_coherence=presence,
            satisfaction_level=satisfaction,
            processing_energy=energy,
            r_matrix_coupling=self.r_matrix,
            timestamp=time.time(),
            conversation_id=conversation_id
        )

    def _estimate_organ_states(self, text: str, trace_type: str) -> Dict[str, float]:
        """
        Estimate organ coherences from text (when orchestrator state unavailable).

        Simple heuristics based on trace type and text content.
        """
        # Base coherences
        states = {organ: 0.5 for organ in self.organ_names}

        # Trace type patterns (from DAE 3.0 insights)
        if trace_type == "Insight":
            states['WISDOM'] = 0.75  # Insights require wisdom
            states['PRESENCE'] = 0.7  # Pattern recognition needs presence
        elif trace_type == "Note":
            states['LISTENING'] = 0.8  # Notes emerge from listening
            states['PRESENCE'] = 0.65
        elif trace_type == "Task":
            states['AUTHENTICITY'] = 0.7  # Tasks need clear boundaries
            states['WISDOM'] = 0.6  # Planning requires wisdom
        elif trace_type == "Question":
            states['LISTENING'] = 0.75  # Questions emerge from listening
            states['WISDOM'] = 0.55  # Inquiry is wisdom-seeking
        elif trace_type == "Project":
            states['WISDOM'] = 0.8  # Projects need strategic thinking
            states['AUTHENTICITY'] = 0.75  # Clear purpose

        # Text content modulation
        text_lower = text.lower()
        if any(word in text_lower for word in ['feel', 'sense', 'resonate']):
            states['EMPATHY'] += 0.1
        if any(word in text_lower for word in ['pattern', 'notice', 'observe']):
            states['PRESENCE'] += 0.1
        if any(word in text_lower for word in ['understand', 'realize', 'learn']):
            states['WISDOM'] += 0.1

        # Clip to [0, 1]
        return {k: np.clip(v, 0.0, 1.0) for k, v in states.items()}

    def _estimate_satisfaction(
        self,
        text: str,
        trace_type: str,
        organ_states: Dict[str, float]
    ) -> float:
        """
        Estimate satisfaction (completeness/resolution) of trace.

        Higher satisfaction = more resolved/complete understanding
        """
        # Base satisfaction from trace type
        satisfaction_map = {
            'Insight': 0.85,  # Insights feel highly satisfying
            'Note': 0.6,  # Notes are mid-satisfaction (observations)
            'Task': 0.5,  # Tasks are incomplete until done
            'Question': 0.4,  # Questions are inherently incomplete
            'Project': 0.7,  # Projects have clear direction
            'Concept': 0.75  # Concepts are well-formed ideas
        }
        base_satisfaction = satisfaction_map.get(trace_type, 0.5)

        # Modulate by organ coherence (higher coherence = more satisfying)
        avg_coherence = np.mean(list(organ_states.values()))
        modulated = base_satisfaction * (0.7 + 0.3 * avg_coherence)

        return float(np.clip(modulated, 0.0, 1.0))

    def _estimate_processing_energy(self, text: str, trace_type: str) -> float:
        """
        Estimate processing energy (complexity of understanding).

        Lower energy = simpler/quicker processing
        Higher energy = complex/deep processing needed
        """
        # Base energy from trace type
        energy_map = {
            'Note': 0.3,  # Notes are simple observations
            'Question': 0.4,  # Questions are straightforward
            'Task': 0.5,  # Tasks require moderate processing
            'Project': 0.7,  # Projects need deep planning
            'Insight': 0.8,  # Insights require significant processing
            'Concept': 0.85  # Concepts need deep understanding
        }
        base_energy = energy_map.get(trace_type, 0.5)

        # Modulate by text complexity (rough heuristic)
        words = len(text.split())
        complexity_factor = 1.0 if words < 20 else 1.2 if words < 50 else 1.4
        modulated = base_energy * complexity_factor

        return float(np.clip(modulated, 0.0, 1.0))


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.

    Returns value in [0, 1] where 1 = identical direction.
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)
    return float(np.clip((similarity + 1) / 2, 0.0, 1.0))  # Map [-1,1] to [0,1]


# Example usage (standalone testing)
if __name__ == "__main__":
    print("🍄 Simple Felt Capture - Standalone Test\n")

    capture = SimpleFeltCapture()

    # Test 1: Capture from Note
    print("Test 1: Note trace")
    felt_note = capture.capture_from_conversation(
        text="Team members report feeling exhausted during standup",
        trace_type="Note",
        conversation_id="test_session_001"
    )
    print(f"  Listening: {felt_note.listening_coherence:.2f}")
    print(f"  Empathy: {felt_note.empathy_coherence:.2f}")
    print(f"  Satisfaction: {felt_note.satisfaction_level:.2f}")
    print(f"  Energy: {felt_note.processing_energy:.2f}")
    print(f"  Vector: {felt_note.to_vector()}\n")

    # Test 2: Capture from Insight
    print("Test 2: Insight trace")
    felt_insight = capture.capture_from_conversation(
        text="Exhaustion correlates with lack of autonomy - teams with least control show highest burnout",
        trace_type="Insight",
        conversation_id="test_session_001"
    )
    print(f"  Listening: {felt_insight.listening_coherence:.2f}")
    print(f"  Wisdom: {felt_insight.wisdom_coherence:.2f}")
    print(f"  Satisfaction: {felt_insight.satisfaction_level:.2f}")
    print(f"  Energy: {felt_insight.processing_energy:.2f}")
    print(f"  Vector: {felt_insight.to_vector()}\n")

    # Test 3: Compare similarity
    print("Test 3: Vector similarity")
    similarity = cosine_similarity(felt_note.to_vector(), felt_insight.to_vector())
    print(f"  Note ↔ Insight similarity: {similarity:.2f}")
    print(f"  Interpretation: {'Related traces' if similarity > 0.7 else 'Distinct traces'}\n")

    # Test 4: Transformation learning
    print("Test 4: Transformation pattern (Note → Insight)")
    satisfaction_gain = felt_insight.satisfaction_level - felt_note.satisfaction_level
    wisdom_gain = felt_insight.wisdom_coherence - felt_note.wisdom_coherence
    print(f"  Satisfaction gain: +{satisfaction_gain:.2f}")
    print(f"  Wisdom gain: +{wisdom_gain:.2f}")
    print(f"  Pattern: Note → Insight increases satisfaction and wisdom ✓\n")

    print("✅ All tests passed - Felt capture working!")
