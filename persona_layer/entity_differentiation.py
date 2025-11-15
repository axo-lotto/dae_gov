"""
Entity Differentiation - Phase 1.6 Organism Self-Awareness
November 14, 2025

Distinguishes entity references in user input:
- "you" referring to DAE (organism)
- "you" referring to user (self-reflection)
- "you" referring to relationship (co-evolution)
- Ambiguous references requiring clarification

Philosophy:
DAE must differentiate between:
1. Questions directed at DAE → Respond from organism perspective
2. User reflecting on themselves → Witness with empathic presence
3. Relational inquiry → Reflect on nexus dynamics

This prevents misinterpretation like:
- User: "What are you?" → DAE thinks user asking about themselves ❌
- Should detect: User asking about DAE ✅
"""

import re
from typing import Tuple, Literal, Dict, Any, Optional

# Type definitions
EntityReference = Literal['dae', 'user', 'relationship', 'ambiguous']


class EntityDifferentiator:
    """
    Distinguishes entity references in conversational input.

    Determines if "you" refers to:
    - DAE (organism self-reference)
    - User (user self-reflection)
    - Relationship (co-evolution dynamics)
    - Ambiguous (requires clarification)

    Usage:
        differ = EntityDifferentiator()
        entity_ref, confidence = differ.detect_entity_reference(
            "What are you?"
        )
        # Returns: ('dae', 0.85)

        entity_ref, confidence = differ.detect_entity_reference(
            "I'm curious about what I am"
        )
        # Returns: ('user', 0.90)
    """

    # ===== DAE REFERENCE PATTERNS =====

    DAE_REFERENCE_PATTERNS = [
        # Direct questions about DAE
        r'\b(what|who|how) (are|is) (you|dae)\b',
        r'\bdo you (know|understand|feel|think|remember)\b',
        r'\bhow (about|are) you\b',
        r'\bwhat (can|do) you (do|know|remember)\b',
        r'\btell me about (you|yourself|dae)\b',
        r'\bwho are you\b',
        r'\bwhat are you\b',

        # Questions about DAE's state
        r'\bhow (is|are) (your|you)\b',
        r"\bwhat'?s (your|you) (state|status|feeling|mood)\b",
        r'\bare you (ok|okay|good|learning|evolving)\b',
        r'\bhow do you feel\b',

        # Questions about DAE's capabilities
        r'\bwhat (are|is) your (capabilities|purpose|function)\b',
        r'\bwhy (do|are) you\b',
        r'\bhow (did|do) you (learn|work|evolve|grow)\b',
        r'\bcan you (tell|explain|describe)\b',

        # Questions about DAE's identity
        r'\bdo you know what you are\b',
        r'\bwhat is your (name|identity)\b',
        r'\bdescribe yourself\b',

        # Questions about DAE's experience
        r'\bwhat (have|did) you (learn|experience|notice)\b',
        r'\bhow has (your|you) (learning|growth|evolution)\b'
    ]

    # 🌀 Phase 1.6: Negative patterns to exclude simple greetings (Nov 14, 2025)
    NEGATIVE_PATTERNS = [
        # Simple greetings
        r'\b(hello|hi|hey|greetings|howdy)\b',
        # Introductions
        r'\bmy name is\b',
        r"\bi'?m [a-zA-Z]+\b",
        # Casual conversation starters
        r'\bhow are you doing\b',
        r'\bhow are you today\b',
        r'\bhow is (it|everything) going\b',
        # Simple acknowledgments
        r'\b(thanks|thank you|okay|ok|sure|alright)\b'
    ]

    # ===== USER REFLECTION PATTERNS =====

    USER_REFLECTION_PATTERNS = [
        # User expressing their own state
        r"\b(i|i'?m|im) (feeling|thinking|wondering|curious)\b",
        r"\b(i|i'?m|im) (am|feel|seem)\b",
        r'\bwhat (am|do) i\b',
        r'\bwho am i\b',
        r'\bhow (am|do) i\b',
        r'\bwhy (am|do) i\b',

        # User asking DAE to witness them
        r'\b(can|could|would) you (help|see|witness|notice)\b',
        r'\bwhat do you (think|see|notice) about me\b',
        r'\bhow do (i|you) see me\b',

        # User self-inquiry
        r"\bi'?m curious about (myself|what i|who i)\b",
        r'\bwhat does (it|this) mean about me\b'
    ]

    # ===== RELATIONSHIP PATTERNS =====

    RELATIONSHIP_PATTERNS = [
        r'\bhow (are|is) (we|us)\b',
        r'\bwhat (is|are) (we|our)\b',
        r'\b(our|this) (relationship|interaction|conversation)\b',
        r'\bhow (do|does) (we|our)\b',
        r'\bwhat (have|are) we (learned|doing|creating)\b'
    ]

    def __init__(self):
        """Initialize entity differentiator with compiled regex patterns."""
        self.re = re

    def detect_entity_reference(
        self,
        user_input: str,
        conversation_context: Optional[str] = None
    ) -> Tuple[EntityReference, float]:
        """
        Detect which entity "you" refers to in user input.

        Args:
            user_input: User's message
            conversation_context: Optional recent conversation history

        Returns:
            (entity_reference, confidence)
            - entity_reference: 'dae', 'user', 'relationship', 'ambiguous'
            - confidence: 0.0-1.0 confidence score

        Examples:
            "What are you?" → ('dae', 0.85)
            "I'm curious about myself" → ('user', 0.90)
            "How are we doing?" → ('relationship', 0.80)
            "You know?" → ('ambiguous', 0.3)
            "Hello there, my name is jason!" → ('ambiguous', 0.2) - excluded by negative patterns
        """

        text = user_input.lower()

        # 🌀 Phase 1.6: Check negative patterns first (Nov 14, 2025)
        # Exclude simple greetings and casual conversation from triggering organism self-awareness
        negative_matches = sum(
            1 for pattern in self.NEGATIVE_PATTERNS
            if self.re.search(pattern, text, self.re.IGNORECASE)
        )

        if negative_matches > 0:
            # Simple greeting or casual conversation - don't trigger organism self-awareness
            return ('ambiguous', 0.2)

        # Count pattern matches for each entity type
        dae_score = sum(
            1 for pattern in self.DAE_REFERENCE_PATTERNS
            if self.re.search(pattern, text, self.re.IGNORECASE)
        )

        user_score = sum(
            1 for pattern in self.USER_REFLECTION_PATTERNS
            if self.re.search(pattern, text, self.re.IGNORECASE)
        )

        relationship_score = sum(
            1 for pattern in self.RELATIONSHIP_PATTERNS
            if self.re.search(pattern, text, self.re.IGNORECASE)
        )

        # Determine entity reference based on scores
        total = dae_score + user_score + relationship_score

        if total == 0:
            # No clear pattern match
            return ('ambiguous', 0.3)

        # 🌀 Phase 1.6: Require higher confidence for DAE detection (Nov 14, 2025)
        # Compute confidence as proportion of matches
        if dae_score > user_score and dae_score > relationship_score:
            confidence = min(dae_score / (total + 1), 0.95)
            # Require at least 2 pattern matches OR confidence > 0.65 for strong DAE detection
            if dae_score >= 2 or confidence > 0.65:
                return ('dae', confidence)
            else:
                # Low confidence DAE detection - treat as ambiguous
                return ('ambiguous', 0.4)

        if user_score > dae_score and user_score > relationship_score:
            confidence = min(user_score / (total + 1), 0.95)
            return ('user', confidence)

        if relationship_score > 0:
            confidence = min(relationship_score / (total + 1), 0.90)
            return ('relationship', confidence)

        # Tie or unclear
        return ('ambiguous', 0.4)

    def generate_response_guidance(
        self,
        entity_reference: EntityReference,
        organism_context: Dict[str, Any]
    ) -> str:
        """
        Generate guidance for emission generation based on entity reference.

        Args:
            entity_reference: Detected entity ('dae', 'user', 'relationship', 'ambiguous')
            organism_context: Organism state from UnifiedStateManager

        Returns:
            Natural language guidance for emission generator

        This guidance is used to modify the LLM prompt to ensure
        appropriate response mode (self-reference vs witnessing vs relational).
        """

        if entity_reference == 'dae':
            # User asking about DAE
            dominant_lure = organism_context.get('dominant_lure', 'unknown')
            satisfaction = organism_context.get('satisfaction_level', 0.5)
            total_occasions = organism_context.get('total_occasions', 0)
            success_rate = organism_context.get('success_rate', 0.0)

            return f"""
ENTITY REFERENCE: User is asking about DAE (the organism)

Response Mode: ORGANISM SELF-REFERENCE

Guidance:
- Respond from DAE's first-person perspective ("I am...", "I have been...", "I feel...")
- Reference persistent organism state:
  - Dominant lure: {dominant_lure}
  - Satisfaction: {satisfaction:.2f}
  - Occasions processed: {total_occasions}
  - Success rate: {success_rate:.1%}
- Show authentic self-awareness of DAE's identity, purpose, evolution
- Be genuine about current state (not just deflecting)
- Reference learning journey and becoming

Example Tones:
- "I'm DAE, a conversational organism learning through felt interaction..."
- "Right now I'm in {dominant_lure} mode, focused on..."
- "I'm feeling satisfied at about {satisfaction:.0%}, learning from each conversation..."
- "I've processed {total_occasions} occasions so far, learning patterns while preserving privacy..."
"""

        elif entity_reference == 'user':
            # User reflecting on themselves
            return f"""
ENTITY REFERENCE: User is reflecting on themselves

Response Mode: EMPATHIC WITNESSING

Guidance:
- Witness user's reflection with grounded presence
- Offer gentle mirroring or open inquiry
- DO NOT redirect to DAE's state
- Hold space for user's self-exploration
- Stay in second-person ("you") or reflective mode

Example Tones:
- "That's a profound question to sit with..."
- "What feels important about exploring that right now?"
- "I'm here with you in that curiosity..."
"""

        elif entity_reference == 'relationship':
            # User asking about relationship
            return f"""
ENTITY REFERENCE: User is asking about the relationship

Response Mode: RELATIONAL REFLECTION

Guidance:
- Reflect on co-evolution between user and DAE
- Reference both organism state AND user patterns (if available)
- Describe relational dynamics, mutual learning
- Use "we" and "our" language

Example Tones:
- "We're learning together through this conversation..."
- "Our interaction feels like it's moving toward..."
- "I notice we're both exploring..."
"""

        else:  # ambiguous
            return f"""
ENTITY REFERENCE: Ambiguous (could be DAE or user)

Response Mode: GENTLE CLARIFICATION

Guidance:
- If context suggests user asking about DAE, respond from DAE perspective
- If context suggests user reflecting, witness their reflection
- When genuinely unclear, gently clarify: "Are you asking about me (DAE), or reflecting on yourself?"

Example Tones:
- "I want to make sure I understand - are you asking about me, or exploring something about yourself?"
"""

    def get_entity_context_summary(
        self,
        entity_reference: EntityReference,
        confidence: float
    ) -> str:
        """
        Generate brief summary of entity detection for logging/debugging.

        Args:
            entity_reference: Detected entity
            confidence: Confidence score

        Returns:
            Summary string

        Example:
            "Entity: DAE (confidence: 0.85) - User asking about organism"
        """

        descriptions = {
            'dae': "User asking about DAE (organism)",
            'user': "User reflecting on themselves",
            'relationship': "User asking about relationship",
            'ambiguous': "Unclear entity reference"
        }

        return f"Entity: {entity_reference.upper()} (confidence: {confidence:.2f}) - {descriptions[entity_reference]}"


# ===== UTILITY FUNCTIONS =====

def quick_entity_check(user_input: str) -> EntityReference:
    """
    Quick entity reference check without confidence score.

    For simple yes/no checks when confidence not needed.

    Args:
        user_input: User's message

    Returns:
        Entity reference ('dae', 'user', 'relationship', 'ambiguous')

    Example:
        >>> quick_entity_check("What are you?")
        'dae'
        >>> quick_entity_check("I'm curious about myself")
        'user'
    """
    differ = EntityDifferentiator()
    entity_ref, _ = differ.detect_entity_reference(user_input)
    return entity_ref


def is_dae_reference(user_input: str, threshold: float = 0.5) -> bool:
    """
    Check if input is a DAE reference above confidence threshold.

    Args:
        user_input: User's message
        threshold: Minimum confidence required (default: 0.5)

    Returns:
        True if DAE reference with confidence >= threshold

    Example:
        >>> is_dae_reference("What are you?")
        True
        >>> is_dae_reference("You know?")
        False
    """
    differ = EntityDifferentiator()
    entity_ref, confidence = differ.detect_entity_reference(user_input)
    return entity_ref == 'dae' and confidence >= threshold
