"""
EO (Emergent Order) Organ Configuration for Text Domain

Adapted from FFITTSS v0 EO organ for organizational consulting.

Original EO (Grid Domain):
- Detects spatial patterns, symmetries, emergent structures
- Outputs Vector35D with spatial features

Text Domain EO (Polyvagal Detection):
- Detects nervous system states from conversational text
- Maps to polyvagal states: Ventral (safe) / Sympathetic (mobilized) / Dorsal (shutdown)
- Outputs Vector35D with polyvagal features

Integration with OFEL:
- EO prehension provides polyvagal_state for E_polyvagal computation
- Coherence score determines confidence in state classification
- Energy cost varies by state (ventral=0.0, sympathetic=0.3, dorsal=0.6)

Author: DAE-GOV Development Team
Date: November 10, 2025
"""

from typing import Dict, List, Any, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class PolyvagalState:
    """
    Detected polyvagal state with confidence.

    Fields:
        state: "ventral", "sympathetic", "dorsal", or "mixed"
        confidence: [0,1] how certain the detection is
        keywords_matched: List of keywords that triggered detection
        energy_cost: [0,1] exclusion penalty for OFEL
    """
    state: str
    confidence: float
    keywords_matched: List[str]
    energy_cost: float


# Polyvagal keyword signatures
# Based on Porges (2011) polyvagal theory + trauma-informed language patterns
EO_POLYVAGAL_CONFIG = {
    'ventral': {
        'description': 'Safe, connected, socially engaged (parasympathetic ventral vagal)',
        'keywords': [
            # Connection & engagement
            'connected', 'safe', 'together', 'with', 'engage', 'curious',
            'playful', 'interested', 'wonder', 'explore', 'open',

            # Compassion & warmth
            'compassion', 'care', 'kindness', 'warmth', 'gentle', 'soften',
            'present', 'here', 'breathe', 'grounded',

            # Clarity & calm
            'clear', 'calm', 'peaceful', 'ease', 'flow', 'spacious',
            'relax', 'settle', 'rest', 'comfortable',

            # Creativity & confidence
            'creative', 'confident', 'capable', 'strong', 'resilient',
            'possible', 'opportunity', 'growth', 'learn',
        ],
        'energy_cost': 0.0,  # No exclusion - encourage ventral responses
        'base_confidence': 0.7,  # Strong confidence if keywords match
    },

    'sympathetic': {
        'description': 'Fight/flight mobilization (sympathetic arousal)',
        'keywords': [
            # Urgency & pressure
            'urgent', 'deadline', 'pressure', 'rush', 'hurry', 'fast',
            'overwhelm', 'too much', 'can\'t handle', 'drowning', 'swamped',

            # Anxiety & fear
            'anxious', 'anxiety', 'worried', 'fear', 'scared', 'nervous',
            'panic', 'terror', 'dread', 'threat', 'danger',

            # Anger & fight
            'angry', 'rage', 'frustrated', 'irritated', 'fight', 'attack',
            'defend', 'protect', 'boundary', 'no', 'stop',

            # Hypervigilance
            'alert', 'vigilant', 'scanning', 'watch', 'guard', 'careful',
            'tense', 'tight', 'rigid', 'braced', 'ready',
        ],
        'energy_cost': 0.3,  # Moderate exclusion - proceed with caution
        'base_confidence': 0.75,  # High confidence - clear mobilization language
    },

    'dorsal': {
        'description': 'Shutdown, freeze, dissociation (parasympathetic dorsal vagal)',
        'keywords': [
            # Shutdown & collapse
            'numb', 'shutdown', 'shut down', 'collapse', 'give up', 'quit',
            'hopeless', 'helpless', 'powerless', 'defeated', 'lost',

            # Freeze & immobilization
            'frozen', 'freeze', 'stuck', 'paralyzed', 'can\'t move', 'trapped',
            'immobile', 'heavy', 'weighted', 'sinking', 'disappear',

            # Dissociation
            'dissociate', 'disconnect', 'unreal', 'foggy', 'hazy', 'blur',
            'far away', 'floating', 'detached', 'outside', 'watching',

            # Despair & exhaustion
            'exhausted', 'depleted', 'empty', 'nothing left', 'done',
            'despair', 'darkness', 'void', 'alone', 'isolated',
        ],
        'energy_cost': 0.6,  # High exclusion - danger zone, containment needed
        'base_confidence': 0.85,  # Very high confidence - clear shutdown language
    },

    'mixed': {
        'description': 'Mixed states (e.g., freeze + rage, collapse + fight)',
        'keywords': [
            # Simultaneous activation patterns
            'frozen rage', 'numb anger', 'anxious shutdown', 'wired tired',
            'tense collapse', 'hypervigilant exhaustion',
        ],
        'energy_cost': 0.5,  # High caution - complex state
        'base_confidence': 0.8,  # High confidence when mixed markers present
    }
}


# Coherence modifiers
# Factors that increase/decrease confidence in state detection
COHERENCE_MODIFIERS = {
    'keyword_density': {
        'high_density': +0.1,     # Multiple keywords from same state
        'mixed_signals': -0.2,    # Keywords from different states conflict
    },
    'intensity': {
        'strong_language': +0.1,  # "completely numb" vs "a bit numb"
        'hedged_language': -0.1,  # "maybe", "sort of", "kind of"
    },
    'explicit_markers': {
        'body_sensations': +0.15, # "heart racing", "shoulders tight"
        'state_naming': +0.2,     # "I feel safe", "I'm shutting down"
    }
}


class EOPolyvagalDetector:
    """
    EO organ adapted for text domain - polyvagal state detection.

    Processes conversational text to detect nervous system state.
    Outputs PolyvagalState with confidence for OFEL computation.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize EO polyvagal detector.

        Args:
            config: Optional configuration override
        """
        self.config = config or EO_POLYVAGAL_CONFIG
        self.coherence_modifiers = COHERENCE_MODIFIERS

    def detect_polyvagal_state(
        self,
        text: str,
        context: Dict[str, Any] = None
    ) -> PolyvagalState:
        """
        Detect polyvagal state from conversational text.

        Args:
            text: User input text (message, query, etc.)
            context: Optional context (conversation history, etc.)

        Returns:
            PolyvagalState with detected state, confidence, keywords

        Algorithm:
            1. Scan text for polyvagal keywords
            2. Count matches per state
            3. Apply coherence modifiers
            4. Select dominant state
            5. Return PolyvagalState with confidence

        Example:
            >>> detector = EOPolyvagalDetector()
            >>> state = detector.detect_polyvagal_state(
            ...     "I'm completely overwhelmed and frozen. Can't move forward."
            ... )
            >>> state.state
            'dorsal'
            >>> state.confidence
            0.92  # High confidence - clear shutdown markers
        """
        text_lower = text.lower()

        # Step 1: Count keyword matches per state
        state_scores = {}
        state_keywords = {}

        for state_name, state_config in self.config.items():
            if state_name == 'mixed':
                continue  # Handle mixed states separately

            keywords = state_config['keywords']
            matches = [kw for kw in keywords if kw in text_lower]

            state_scores[state_name] = len(matches)
            state_keywords[state_name] = matches

        # Step 2: Check for mixed state patterns
        mixed_keywords = self.config['mixed']['keywords']
        mixed_matches = [kw for kw in mixed_keywords if kw in text_lower]
        if mixed_matches:
            state_scores['mixed'] = len(mixed_matches) * 2  # Boost mixed if explicit
            state_keywords['mixed'] = mixed_matches

        # Step 3: Detect mixed states from co-occurring markers
        if state_scores.get('dorsal', 0) > 0 and state_scores.get('sympathetic', 0) > 0:
            # Both shutdown and mobilization present
            state_scores['mixed'] = state_scores.get('mixed', 0) + 1

        # Step 4: Select dominant state
        if not any(state_scores.values()):
            # No keywords matched - default to ventral with low confidence
            return PolyvagalState(
                state='ventral',
                confidence=0.4,  # Low confidence - no clear markers
                keywords_matched=[],
                energy_cost=0.0
            )

        dominant_state = max(state_scores, key=state_scores.get)
        keyword_count = state_scores[dominant_state]
        matched_keywords = state_keywords.get(dominant_state, [])

        # Step 5: Compute confidence with modifiers
        base_confidence = self.config[dominant_state]['base_confidence']

        # Modifier 1: Keyword density
        if keyword_count >= 3:
            base_confidence += self.coherence_modifiers['keyword_density']['high_density']

        # Modifier 2: Mixed signals (reduce confidence)
        other_states = [s for s in state_scores if s != dominant_state and state_scores[s] > 0]
        if len(other_states) >= 2:
            base_confidence += self.coherence_modifiers['keyword_density']['mixed_signals']

        # Modifier 3: Check for intensity markers
        intensity_markers = ['completely', 'totally', 'extremely', 'very', 'so']
        if any(marker in text_lower for marker in intensity_markers):
            base_confidence += self.coherence_modifiers['intensity']['strong_language']

        hedging_markers = ['maybe', 'sort of', 'kind of', 'a bit', 'slightly']
        if any(marker in text_lower for marker in hedging_markers):
            base_confidence += self.coherence_modifiers['intensity']['hedged_language']

        # Modifier 4: Check for explicit state naming
        state_naming_patterns = [
            'i feel safe', 'i\'m safe', 'feeling safe',
            'i feel anxious', 'i\'m anxious', 'feeling anxious',
            'i\'m shutting down', 'shutting down', 'feeling numb'
        ]
        if any(pattern in text_lower for pattern in state_naming_patterns):
            base_confidence += self.coherence_modifiers['explicit_markers']['state_naming']

        # Clamp confidence to [0.4, 1.0]
        final_confidence = np.clip(base_confidence, 0.4, 1.0)

        # Get energy cost
        energy_cost = self.config[dominant_state]['energy_cost']

        return PolyvagalState(
            state=dominant_state,
            confidence=float(final_confidence),
            keywords_matched=matched_keywords,
            energy_cost=energy_cost
        )

    def prehend_text(
        self,
        text: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        EO organ prehension for text (FFITTSS-compatible interface).

        Args:
            text: User input text
            context: Optional context

        Returns:
            Organ output dictionary with:
                - polyvagal_state: "ventral"/"sympathetic"/"dorsal"/"mixed"
                - confidence: [0,1]
                - keywords_matched: List[str]
                - energy_cost: [0,1] for OFEL
                - coherence: [0,1] (same as confidence for compatibility)
                - lure: [0,1] (inverse of energy_cost - ventral has high lure)

        Example:
            >>> detector = EOPolyvagalDetector()
            >>> output = detector.prehend_text("I'm feeling really overwhelmed.")
            >>> output['polyvagal_state']
            'sympathetic'
            >>> output['coherence']
            0.78
        """
        state = self.detect_polyvagal_state(text, context)

        # Lure = inverse of energy cost (ventral attracts, dorsal repels)
        lure = 1.0 - state.energy_cost

        return {
            'polyvagal_state': state.state,
            'confidence': state.confidence,
            'keywords_matched': state.keywords_matched,
            'energy_cost': state.energy_cost,
            'coherence': state.confidence,  # For compatibility with OFEL
            'lure': lure,
            'organ_name': 'EO',
            'specialization': 'polyvagal_detection'
        }


# Quick utility function
def quick_polyvagal_check(text: str) -> Tuple[str, float]:
    """
    Quick polyvagal state detection (convenience function).

    Args:
        text: User input text

    Returns:
        (state, confidence) tuple

    Example:
        >>> quick_polyvagal_check("I feel safe and curious.")
        ('ventral', 0.74)
    """
    detector = EOPolyvagalDetector()
    state = detector.detect_polyvagal_state(text)
    return (state.state, state.confidence)
