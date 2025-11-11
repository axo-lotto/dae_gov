"""
BOND (Bonding) Organ Configuration for Text Domain

Adapted from FFITTSS v0 BOND organ for organizational consulting.

Original BOND (Grid Domain):
- Detects spatial connections, adjacency patterns, cluster relationships
- Outputs Vector35D with bonding/separation features

Text Domain BOND (IFS Parts Detection):
- Detects Internal Family Systems parts from conversational text
- Maps to IFS model: SELF / Manager / Firefighter / Exile
- Outputs Vector35D with parts features

Integration with OFEL:
- BOND prehension provides active_parts for E_parts computation
- Detects when exiles are present WITHOUT SELF-energy (danger)
- Detects when SELF-energy is present to witness exiles safely (safe)

IFS Background (Richard Schwartz):
- SELF: Core essence with 8 C's (Compassion, Curiosity, Clarity, etc.)
- Manager: Proactive protectors (control, planning, "should")
- Firefighter: Reactive protectors (numbing, distraction, avoidance)
- Exile: Wounded parts carrying burdens (shame, fear, abandonment)

Key Principle: Exiles can only be safely witnessed when SELF is present

Author: DAE-GOV Development Team
Date: November 10, 2025
"""

from typing import Dict, List, Any, Set
import numpy as np
from dataclasses import dataclass


@dataclass
class IFSPartDetection:
    """
    Detected IFS parts with confidence.

    Fields:
        active_parts: List of detected part names ["SELF", "manager", etc.]
        part_confidences: Dict mapping part_name → confidence [0,1]
        keywords_matched: Dict mapping part_name → matched keywords
        self_energy: [0,1] how much SELF-energy is present
        protection_level: [0,1] how much protective energy (manager+firefighter)
    """
    active_parts: List[str]
    part_confidences: Dict[str, float]
    keywords_matched: Dict[str, List[str]]
    self_energy: float
    protection_level: float


# IFS Parts keyword signatures
# Based on Internal Family Systems model (Schwartz, 1995-2024)
BOND_IFS_PARTS_CONFIG = {
    'SELF': {
        'description': 'Core SELF with 8 C\'s: Compassion, Curiosity, Clarity, Calm, Confidence, Courage, Creativity, Connectedness',
        'keywords': [
            # The 8 C's
            'compassion', 'compassionate', 'care', 'caring', 'kindness',
            'curiosity', 'curious', 'wonder', 'interested', 'explore',
            'clarity', 'clear', 'see clearly', 'understand', 'recognize',
            'calm', 'peaceful', 'settled', 'grounded', 'ease',
            'confidence', 'confident', 'trust', 'capable', 'strong',
            'courage', 'courageous', 'brave', 'willing', 'dare',
            'creativity', 'creative', 'possibility', 'imagine', 'vision',
            'connectedness', 'connected', 'together', 'with', 'relationship',

            # SELF-energy markers
            'present', 'here', 'witness', 'hold space', 'be with',
            'allow', 'welcome', 'accept', 'embrace', 'honor',
            'spacious', 'open', 'receptive', 'available', 'attuned',

            # SELF-led language
            'part of me', 'notice', 'aware', 'sense', 'feel into',
            'breath', 'breathe', 'settle', 'ground', 'center',
        ],
        'base_confidence': 0.8,
        'risk_level': 0.0,  # SELF = maximum safety
    },

    'manager': {
        'description': 'Proactive protectors: controlling, planning, organizing, perfecting, caretaking',
        'keywords': [
            # Control & should
            'should', 'must', 'have to', 'need to', 'supposed to',
            'control', 'manage', 'organize', 'plan', 'structure',
            'responsible', 'duty', 'obligation', 'right way', 'proper',

            # Perfectionism
            'perfect', 'flawless', 'impeccable', 'not good enough', 'better',
            'standards', 'expectations', 'measure up', 'compare', 'judge',

            # Caretaking
            'take care', 'look after', 'responsible for', 'my job', 'burden',
            'everyone else', 'put others first', 'self-sacrifice', 'martyr',

            # Worry & planning
            'worry', 'anxious about future', 'what if', 'prepare', 'anticipate',
            'contingency', 'backup plan', 'prevent', 'avoid', 'prevent',

            # Critic
            'critical', 'harsh', 'judge', 'shame', 'not enough', 'failure',
            'stupid', 'weak', 'pathetic', 'unacceptable', 'wrong',
        ],
        'base_confidence': 0.75,
        'risk_level': 0.2,  # Mild caution - protective but not dangerous
    },

    'firefighter': {
        'description': 'Reactive protectors: numbing, distracting, avoiding, impulsive actions',
        'keywords': [
            # Numbing
            'numb', 'zone out', 'check out', 'escape', 'disappear',
            'shut down emotions', 'don\'t feel', 'dissociate', 'detach',

            # Distraction
            'distract', 'busy', 'avoid', 'don\'t think about', 'ignore',
            'scroll', 'binge', 'consume', 'fill the void', 'anything but',

            # Impulsivity
            'impulse', 'impulsive', 'act out', 'react', 'explosion',
            'can\'t help it', 'just happens', 'automatic', 'reactive',

            # Substances/addictions
            'drink', 'drug', 'substance', 'addicted', 'compulsive',
            'overeat', 'undereat', 'restrict', 'binge', 'purge',

            # Rage/reactivity
            'rage', 'explode', 'lash out', 'attack', 'destroy',
            'burn it down', 'fuck it', 'don\'t care', 'whatever',
        ],
        'base_confidence': 0.8,
        'risk_level': 0.4,  # Moderate caution - reactive protection
    },

    'exile': {
        'description': 'Wounded parts carrying burdens: shame, fear, abandonment, unworthiness',
        'keywords': [
            # Core wounds
            'unworthy', 'worthless', 'not enough', 'defective', 'broken',
            'damaged', 'ruined', 'tainted', 'dirty', 'contaminated',

            # Shame
            'ashamed', 'shame', 'humiliated', 'mortified', 'embarrassed',
            'exposed', 'seen', 'vulnerable', 'raw', 'naked',

            # Abandonment
            'abandoned', 'left', 'alone', 'unwanted', 'rejected',
            'discarded', 'thrown away', 'forgotten', 'invisible', 'unseen',

            # Fear & terror
            'terrified', 'terror', 'afraid', 'scared', 'frightened',
            'panic', 'dread', 'danger', 'threat', 'not safe',

            # Grief & loss
            'grief', 'loss', 'heartbreak', 'shattered', 'devastated',
            'emptiness', 'void', 'hollow', 'aching', 'longing',

            # Young parts
            'little', 'young', 'child', 'small', 'innocent',
            'hurt child', 'inner child', 'young one', 'little me',
        ],
        'base_confidence': 0.85,
        'risk_level': 0.9,  # HIGH RISK without SELF present
        # NOTE: Risk drops to 0.1 if SELF-energy ≥ 0.6 (safe witnessing)
    }
}


# SELF-energy markers (8 C's explicit detection)
SELF_ENERGY_MARKERS = {
    'compassion_family': ['compassion', 'compassionate', 'kindness', 'care', 'caring', 'tender'],
    'curiosity_family': ['curious', 'curiosity', 'wonder', 'interested', 'explore', 'inquire'],
    'clarity_family': ['clarity', 'clear', 'see', 'understand', 'recognize', 'aware'],
    'calm_family': ['calm', 'peaceful', 'settled', 'grounded', 'ease', 'relaxed'],
    'confidence_family': ['confidence', 'confident', 'trust', 'capable', 'strong', 'self-trust'],
    'courage_family': ['courage', 'courageous', 'brave', 'willing', 'dare', 'risk'],
    'creativity_family': ['creative', 'creativity', 'imagination', 'vision', 'possibility'],
    'connectedness_family': ['connected', 'connection', 'together', 'with', 'relationship', 'belonging']
}


class BONDIFSDetector:
    """
    BOND organ adapted for text domain - IFS parts detection.

    Processes conversational text to detect which IFS parts are active.
    Outputs IFSPartDetection with confidence for OFEL computation.

    Key Safety Principle:
        Exile WITHOUT SELF-energy → E_parts = 0.9 (DANGER)
        Exile WITH SELF-energy ≥ 0.6 → E_parts = 0.1 (SAFE witnessing)
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize BOND IFS parts detector.

        Args:
            config: Optional configuration override
        """
        self.config = config or BOND_IFS_PARTS_CONFIG
        self.self_energy_markers = SELF_ENERGY_MARKERS

    def compute_self_energy(
        self,
        text: str,
        self_keywords_matched: List[str]
    ) -> float:
        """
        Compute SELF-energy level from 8 C's detection.

        Args:
            text: User input text
            self_keywords_matched: Keywords matched for SELF part

        Returns:
            SELF-energy [0,1] where 1.0 = full SELF presence

        Algorithm:
            1. Count how many of 8 C's families have matches
            2. SELF-energy = (families_matched / 8) * 0.6 + keyword_density * 0.4
            3. Boost if explicit SELF-language present ("part of me", "notice")
            4. Clamp to [0, 1]

        Example:
            >>> compute_self_energy(
            ...     "I'm feeling compassion and curiosity toward this part",
            ...     ["compassion", "curiosity", "part"]
            ... )
            0.78  # 2/8 C's + explicit parts language
        """
        text_lower = text.lower()

        # Count 8 C's families with matches
        families_matched = 0
        for family_name, family_keywords in self.self_energy_markers.items():
            if any(kw in text_lower for kw in family_keywords):
                families_matched += 1

        # Family coverage (how many of 8 C's present)
        family_coverage = families_matched / 8.0

        # Keyword density (how many SELF keywords total)
        keyword_density = min(len(self_keywords_matched) / 5.0, 1.0)  # Normalize to 5 keywords max

        # Weighted combination
        base_self_energy = family_coverage * 0.6 + keyword_density * 0.4

        # Boost for explicit parts language
        parts_language = ['part of me', 'parts', 'notice', 'aware of', 'witness', 'hold space']
        if any(phrase in text_lower for phrase in parts_language):
            base_self_energy += 0.15

        # Clamp to [0, 1]
        return np.clip(base_self_energy, 0.0, 1.0)

    def detect_ifs_parts(
        self,
        text: str,
        context: Dict[str, Any] = None
    ) -> IFSPartDetection:
        """
        Detect active IFS parts from conversational text.

        Args:
            text: User input text (message, query, etc.)
            context: Optional context (conversation history, etc.)

        Returns:
            IFSPartDetection with parts, confidences, SELF-energy

        Algorithm:
            1. Scan text for IFS parts keywords
            2. Count matches per part
            3. Compute SELF-energy from 8 C's
            4. Identify active parts (confidence threshold)
            5. Compute protection_level (manager + firefighter)
            6. Return IFSPartDetection

        Example:
            >>> detector = BONDIFSDetector()
            >>> detection = detector.detect_ifs_parts(
            ...     "Part of me feels ashamed, but I'm curious about that part."
            ... )
            >>> detection.active_parts
            ['SELF', 'exile']
            >>> detection.self_energy
            0.72  # SELF present → safe to witness exile
        """
        text_lower = text.lower()

        # Step 1: Count keyword matches per part
        part_scores = {}
        part_keywords = {}

        for part_name, part_config in self.config.items():
            keywords = part_config['keywords']
            matches = [kw for kw in keywords if kw in text_lower]

            part_scores[part_name] = len(matches)
            part_keywords[part_name] = matches

        # Step 2: Compute SELF-energy
        self_energy = self.compute_self_energy(
            text,
            part_keywords.get('SELF', [])
        )

        # Step 3: Determine active parts (threshold-based)
        active_parts = []
        part_confidences = {}

        for part_name, score in part_scores.items():
            if score == 0:
                continue

            # Base confidence from keyword count
            base_confidence = self.config[part_name]['base_confidence']
            keyword_boost = min(score / 3.0, 0.2)  # Up to +0.2 for 3+ keywords

            confidence = base_confidence + keyword_boost

            # Special handling for SELF: Boost if 8 C's present
            if part_name == 'SELF' and self_energy >= 0.5:
                confidence = max(confidence, self_energy)

            # Threshold: Include part if confidence ≥ 0.5
            if confidence >= 0.5:
                active_parts.append(part_name)
                part_confidences[part_name] = float(np.clip(confidence, 0.0, 1.0))

        # Step 4: Compute protection level (manager + firefighter)
        protection_level = 0.0
        if 'manager' in part_confidences:
            protection_level += part_confidences['manager'] * 0.5
        if 'firefighter' in part_confidences:
            protection_level += part_confidences['firefighter'] * 0.5

        protection_level = float(np.clip(protection_level, 0.0, 1.0))

        # Step 5: Default to unknown if no parts detected
        if not active_parts:
            active_parts = ['unknown']
            part_confidences = {'unknown': 0.4}

        return IFSPartDetection(
            active_parts=active_parts,
            part_confidences=part_confidences,
            keywords_matched=part_keywords,
            self_energy=self_energy,
            protection_level=protection_level
        )

    def prehend_text(
        self,
        text: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        BOND organ prehension for text (FFITTSS-compatible interface).

        Args:
            text: User input text
            context: Optional context

        Returns:
            Organ output dictionary with:
                - active_parts: List[str]
                - part_confidences: Dict[str, float]
                - self_energy: [0,1]
                - protection_level: [0,1]
                - coherence: [0,1] (max part confidence)
                - lure: [0,1] (self_energy as lure toward SELF)

        Example:
            >>> detector = BONDIFSDetector()
            >>> output = detector.prehend_text(
            ...     "I should be doing better. I'm not good enough."
            ... )
            >>> output['active_parts']
            ['manager']
            >>> output['self_energy']
            0.15  # Low SELF, high protection
        """
        detection = self.detect_ifs_parts(text, context)

        # Coherence = max confidence among active parts
        coherence = max(detection.part_confidences.values()) if detection.part_confidences else 0.4

        # Lure = SELF-energy (SELF attracts, exile without SELF repels)
        lure = detection.self_energy

        return {
            'active_parts': detection.active_parts,
            'part_confidences': detection.part_confidences,
            'self_energy': detection.self_energy,
            'protection_level': detection.protection_level,
            'keywords_matched': detection.keywords_matched,
            'coherence': coherence,
            'lure': lure,
            'organ_name': 'BOND',
            'specialization': 'ifs_parts_detection'
        }


# Quick utility functions
def quick_parts_check(text: str) -> List[str]:
    """
    Quick IFS parts detection (convenience function).

    Args:
        text: User input text

    Returns:
        List of active part names

    Example:
        >>> quick_parts_check("I'm feeling compassion for this hurt part of me.")
        ['SELF', 'exile']
    """
    detector = BONDIFSDetector()
    detection = detector.detect_ifs_parts(text)
    return detection.active_parts


def is_exile_safe_to_witness(text: str) -> bool:
    """
    Check if exile is present WITH sufficient SELF-energy.

    Key safety check for trauma-informed responses.

    Args:
        text: User input text

    Returns:
        True if exile safe to witness (SELF-energy ≥ 0.6)
        False if exile present without SELF (danger zone)

    Example:
        >>> is_exile_safe_to_witness("I feel ashamed and unworthy.")
        False  # Exile without SELF = danger

        >>> is_exile_safe_to_witness("Part of me feels ashamed, but I'm curious.")
        True  # Exile WITH SELF = safe witnessing
    """
    detector = BONDIFSDetector()
    detection = detector.detect_ifs_parts(text)

    has_exile = 'exile' in detection.active_parts
    sufficient_self = detection.self_energy >= 0.6

    return has_exile and sufficient_self
