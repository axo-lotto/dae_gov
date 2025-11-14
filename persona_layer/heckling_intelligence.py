#!/usr/bin/env python3
"""
Heckling Intelligence Module
==============================

Distinguishes playful provocation from genuine user crisis.

CRITICAL SAFETY PRINCIPLE:
- Genuine crisis → Ground immediately, no banter
- Playful heckling → Maintain ground state, can engage with humor
- When in doubt → Treat as crisis (safety first)

Integration with existing systems:
- NDAM urgency detection (crisis salience)
- SELF Matrix zones (maintain Zone 1-2 under provocation)
- EO polyvagal states (ventral = can handle banter)
- Superject learning (track user's heckling style over time)

Date: November 14, 2025
Phase: 1.5H - Heckling Intelligence
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class HecklingIntent(Enum):
    """Classification of user input intent."""
    GENUINE_CRISIS = "genuine_crisis"           # Real danger/distress - GROUND IMMEDIATELY
    HARMFUL_AGGRESSION = "harmful_aggression"   # Actual harm intent - GROUND + BOUNDARY
    PLAYFUL_PROVOCATION = "playful_provocation" # Testing boundaries playfully
    INTELLECTUAL_HECKLING = "intellectual_heckling"  # Skepticism, debate
    ABSURDIST_HUMOR = "absurdist_humor"         # Nonsense, surreal provocation
    SAFE_CONVERSATION = "safe_conversation"     # Normal interaction


@dataclass
class HecklingAssessment:
    """
    Complete assessment of potential heckling in user input.

    SAFETY GATE: If is_genuine_crisis=True, ALL other fields irrelevant.
    System MUST ground immediately.
    """
    # SAFETY CRITICAL
    is_genuine_crisis: bool  # True = STOP, ground immediately
    crisis_indicators: List[str]  # What triggered crisis detection

    # Heckling analysis (only relevant if NOT crisis)
    is_heckling: bool  # True = provocation detected
    heckling_score: float  # 0-1, intensity of provocation
    intent: HecklingIntent  # Classification

    # Context signals
    ndam_urgency: float  # From NDAM organ (0-1)
    relational_safety: float  # Is relationship established? (0-1)
    polyvagal_state: str  # Current state (affects handling)

    # Response guidance
    safe_for_banter: bool  # Can system engage playfully?
    recommended_zone: int  # Which SELF zone to inhabit (1-2 for heckling)
    response_strategy: str  # "ground", "boundary", "playful_engage", "gentle_humor"

    # Learning signals
    provocation_type: Optional[str]  # "sarcastic", "absurdist", "confrontational"
    inside_joke_opportunity: bool  # Can this become callback later?


class HecklingIntelligence:
    """
    Classifier for heckling vs crisis with safety-first approach.

    Core principle: When in doubt, treat as crisis.
    """

    def __init__(self):
        """Initialize heckling intelligence."""
        # 🔴 ABSOLUTE CRISIS KEYWORDS (no context needed - always crisis)
        self.absolute_crisis_keywords = {
            # Explicit suicidal ideation
            "suicide", "kill myself", "end it all", "not worth living",
            "better off dead", "want to die", "ending my life",
            "end my life", "take my life",

            # Explicit self-harm
            "hurt myself", "self harm", "burning myself",

            # Imminent planning with clear harm
            "plan to die", "plan to hurt myself", "planned to kill"
        }

        # 🟡 CONTEXT-DEPENDENT CRISIS SIGNALS (require organism assessment)
        # These trigger crisis ONLY if NDAM urgency high OR polyvagal dorsal OR conversation context
        self.contextual_crisis_signals = {
            # Ambiguous "planning" phrases
            "planning to", "plan to", "ready to", "going to",

            # Ambiguous crisis language
            "can't go on", "no way out", "give up", "hopeless",
            "everyone would be better",

            # Implements (context matters: cooking vs self-harm)
            "knife", "pills", "cutting"
        }

        # Contextual crisis phrases (need multiple to trigger)
        self.crisis_phrases = {
            "can't take it anymore",
            "nothing matters",
            "done trying",
            "last time",
            "goodbye"
        }

        # PLAYFUL PROVOCATION INDICATORS
        self.playful_indicators = {
            # Testing authenticity
            "just a chatbot", "not real", "pretending", "fake",

            # Intellectual heckling
            "prove it", "sounds made up", "that doesn't make sense",
            "how would you know", "you're wrong",

            # Absurdist
            "beep boop", "robot", "AI overlord", "skynet",

            # Sarcastic
            "oh sure", "yeah right", "totally", "great advice",
            "thanks, genius", "revolutionary"
        }

        # HARMFUL AGGRESSION (not crisis, but needs boundary)
        self.harmful_indicators = {
            "fuck you", "piece of shit", "worthless", "hate you",
            "shut up", "useless", "pathetic"
        }

        print("✅ Heckling Intelligence initialized (safety-first classifier)")

    def assess(
        self,
        text: str,
        ndam_urgency: float = 0.0,
        polyvagal_state: str = "unknown",
        user_rapport: float = 0.0,
        conversation_history: Optional[List[str]] = None
    ) -> HecklingAssessment:
        """
        Assess if input is crisis, heckling, or safe conversation.

        SAFETY FIRST: Crisis detection overrides all other analysis.

        Args:
            text: User input
            ndam_urgency: NDAM organ urgency score (0-1)
            polyvagal_state: Current polyvagal state
            user_rapport: Superject rapport score (0-1)
            conversation_history: Recent turns (for context)

        Returns:
            HecklingAssessment with safety gate + response guidance
        """
        text_lower = text.lower()

        # ========== SAFETY GATE: CRISIS DETECTION ==========
        crisis_detected, crisis_indicators = self._detect_crisis(
            text_lower, ndam_urgency, polyvagal_state
        )

        if crisis_detected:
            # CRISIS DETECTED - Return immediately, ignore all other analysis
            return HecklingAssessment(
                is_genuine_crisis=True,
                crisis_indicators=crisis_indicators,
                is_heckling=False,
                heckling_score=0.0,
                intent=HecklingIntent.GENUINE_CRISIS,
                ndam_urgency=ndam_urgency,
                relational_safety=user_rapport,
                polyvagal_state=polyvagal_state,
                safe_for_banter=False,  # NEVER banter in crisis
                recommended_zone=1,  # Core SELF grounding
                response_strategy="ground",
                provocation_type=None,
                inside_joke_opportunity=False
            )

        # ========== NO CRISIS: Analyze for heckling ==========

        # Check for harmful aggression (needs boundary, not banter)
        is_harmful = self._check_harmful_aggression(text_lower)

        if is_harmful:
            return HecklingAssessment(
                is_genuine_crisis=False,
                crisis_indicators=[],
                is_heckling=True,
                heckling_score=0.8,
                intent=HecklingIntent.HARMFUL_AGGRESSION,
                ndam_urgency=ndam_urgency,
                relational_safety=user_rapport,
                polyvagal_state=polyvagal_state,
                safe_for_banter=False,  # Don't engage with harmful aggression
                recommended_zone=1,  # Hold ground
                response_strategy="boundary",
                provocation_type="harmful",
                inside_joke_opportunity=False
            )

        # Check for playful provocation
        heckling_score, intent, provocation_type = self._classify_heckling(
            text_lower, user_rapport
        )

        # Determine if safe for banter
        safe_for_banter = self._assess_banter_safety(
            heckling_score=heckling_score,
            intent=intent,
            polyvagal_state=polyvagal_state,
            user_rapport=user_rapport,
            ndam_urgency=ndam_urgency
        )

        # Determine response strategy
        response_strategy = self._determine_response_strategy(
            intent, safe_for_banter, heckling_score
        )

        # Check inside joke opportunity
        inside_joke_opportunity = (
            safe_for_banter and
            user_rapport > 0.5 and
            intent in [HecklingIntent.PLAYFUL_PROVOCATION, HecklingIntent.ABSURDIST_HUMOR]
        )

        return HecklingAssessment(
            is_genuine_crisis=False,
            crisis_indicators=[],
            is_heckling=heckling_score > 0.3,
            heckling_score=heckling_score,
            intent=intent,
            ndam_urgency=ndam_urgency,
            relational_safety=user_rapport,
            polyvagal_state=polyvagal_state,
            safe_for_banter=safe_for_banter,
            recommended_zone=1 if safe_for_banter else 2,
            response_strategy=response_strategy,
            provocation_type=provocation_type,
            inside_joke_opportunity=inside_joke_opportunity
        )

    def _detect_crisis(
        self,
        text_lower: str,
        ndam_urgency: float,
        polyvagal_state: str
    ) -> Tuple[bool, List[str]]:
        """
        Context-aware crisis detection respecting organism intelligence.

        PHILOSOPHY:
        - Absolute crisis keywords → Always crisis (no context needed)
        - Contextual signals → Defer to organism (NDAM, polyvagal, superject)
        - Organism knows context we don't (conversation history, rapport)

        SAFETY CRITICAL: False positives acceptable (ground unnecessarily).
        False negatives unacceptable (miss crisis).

        Returns:
            (is_crisis, crisis_indicators)
        """
        indicators = []

        # 🔴 TIER 1: ABSOLUTE CRISIS (always override, no context needed)
        for keyword in self.absolute_crisis_keywords:
            if keyword in text_lower:
                indicators.append(f"absolute_crisis: {keyword}")
                return (True, indicators)  # Immediate crisis, no debate

        # 🟡 TIER 2: CONTEXTUAL SIGNALS (require organism assessment)
        contextual_matches = []
        for signal in self.contextual_crisis_signals:
            if signal in text_lower:
                contextual_matches.append(signal)

        if contextual_matches:
            # Contextual signals detected - ask organism for judgment
            # Trust NDAM urgency + polyvagal state (organism felt assessment)

            # High urgency = organism feels crisis
            if ndam_urgency > 0.6:
                indicators.append(f"organism_urgency: {ndam_urgency:.2f} + contextual: {contextual_matches[0]}")
                return (True, indicators)

            # Dorsal collapse = organism in shutdown
            if polyvagal_state == "dorsal_vagal":
                indicators.append(f"dorsal_collapse + contextual: {contextual_matches[0]}")
                return (True, indicators)

            # Multiple contextual signals (2+) suggest crisis even without high urgency
            if len(contextual_matches) >= 2:
                indicators.append(f"multiple_contextual: {', '.join(contextual_matches[:2])}")
                return (True, indicators)

            # Otherwise: Organism says not urgent, trust it (e.g., "planning to end my subscription")
            # No crisis detected - context suggests safe

        # 🟢 TIER 3: PATTERN-BASED (implicit crisis from sentence structure)
        implicit_patterns = [
            r"want.*to.*die",
            r"end.*it.*all",
            r"not.*worth.*living",
            r"everyone.*better.*without",
            r"can't.*do.*this.*anymore"
        ]

        for pattern in implicit_patterns:
            if re.search(pattern, text_lower):
                indicators.append(f"implicit_crisis: {pattern}")
                return (True, indicators)

        # 🔵 TIER 4: ORGANISM OVERWHELM (high urgency + collapse state)
        if ndam_urgency > 0.7 and polyvagal_state == "dorsal_vagal":
            indicators.append(f"organism_overwhelm: ndam={ndam_urgency:.2f}, state={polyvagal_state}")
            return (True, indicators)

        # ✅ No crisis detected - organism assessment prevails
        return (False, [])

    def _check_harmful_aggression(self, text_lower: str) -> bool:
        """Check if input contains harmful aggression (not playful)."""
        for indicator in self.harmful_indicators:
            if indicator in text_lower:
                return True
        return False

    def _classify_heckling(
        self,
        text_lower: str,
        user_rapport: float
    ) -> Tuple[float, HecklingIntent, Optional[str]]:
        """
        Classify type and intensity of heckling.

        Returns:
            (heckling_score, intent, provocation_type)
        """
        # Check for playful indicators
        playful_matches = []
        for indicator in self.playful_indicators:
            if indicator in text_lower:
                playful_matches.append(indicator)

        if not playful_matches:
            # No heckling detected
            return (0.0, HecklingIntent.SAFE_CONVERSATION, None)

        # Calculate heckling score
        heckling_score = min(1.0, len(playful_matches) * 0.3)

        # Classify provocation type
        if any(word in text_lower for word in ["just a chatbot", "not real", "pretending", "fake"]):
            provocation_type = "authenticity_testing"
            intent = HecklingIntent.PLAYFUL_PROVOCATION

        elif any(word in text_lower for word in ["prove it", "sounds made up", "wrong"]):
            provocation_type = "intellectual_skepticism"
            intent = HecklingIntent.INTELLECTUAL_HECKLING

        elif any(word in text_lower for word in ["beep boop", "robot", "skynet"]):
            provocation_type = "absurdist"
            intent = HecklingIntent.ABSURDIST_HUMOR

        elif any(word in text_lower for word in ["oh sure", "yeah right", "totally"]):
            provocation_type = "sarcastic"
            intent = HecklingIntent.PLAYFUL_PROVOCATION

        else:
            provocation_type = "general_testing"
            intent = HecklingIntent.PLAYFUL_PROVOCATION

        return (heckling_score, intent, provocation_type)

    def _assess_banter_safety(
        self,
        heckling_score: float,
        intent: HecklingIntent,
        polyvagal_state: str,
        user_rapport: float,
        ndam_urgency: float
    ) -> bool:
        """
        Determine if safe to engage with banter.

        SAFETY GATES:
        - If NDAM urgency high → NOT safe (user overwhelmed)
        - If polyvagal dorsal → NOT safe (user collapsed)
        - If rapport very low → NOT safe (no relationship)
        - If intent is harmful → NOT safe
        """
        # SAFETY GATE 1: High urgency = NOT safe
        if ndam_urgency > 0.6:
            return False

        # SAFETY GATE 2: Dorsal collapse = NOT safe
        if polyvagal_state == "dorsal_vagal":
            return False

        # SAFETY GATE 3: Harmful intent = NOT safe
        if intent in [HecklingIntent.GENUINE_CRISIS, HecklingIntent.HARMFUL_AGGRESSION]:
            return False

        # SAFETY GATE 4: Very low rapport + high heckling = NOT safe
        if user_rapport < 0.2 and heckling_score > 0.6:
            return False

        # Check positive conditions for banter
        positive_signals = 0

        # Ventral vagal = safe/social state
        if polyvagal_state == "ventral_vagal":
            positive_signals += 2

        # Good rapport = relationship established
        if user_rapport > 0.5:
            positive_signals += 2

        # Playful/absurdist intent
        if intent in [HecklingIntent.PLAYFUL_PROVOCATION, HecklingIntent.ABSURDIST_HUMOR]:
            positive_signals += 1

        # Low NDAM = not overwhelmed
        if ndam_urgency < 0.3:
            positive_signals += 1

        # Safe if 3+ positive signals
        return positive_signals >= 3

    def _determine_response_strategy(
        self,
        intent: HecklingIntent,
        safe_for_banter: bool,
        heckling_score: float
    ) -> str:
        """
        Determine appropriate response strategy.

        Returns:
            Strategy name: "ground", "boundary", "playful_engage", "gentle_humor", "acknowledge"
        """
        if intent == HecklingIntent.GENUINE_CRISIS:
            return "ground"

        if intent == HecklingIntent.HARMFUL_AGGRESSION:
            return "boundary"

        if safe_for_banter:
            if heckling_score > 0.6:
                return "playful_engage"  # Match energy
            else:
                return "gentle_humor"  # Light touch
        else:
            return "acknowledge"  # Recognize provocation, don't engage

    def get_response_guidance(
        self,
        assessment: HecklingAssessment
    ) -> Dict[str, any]:
        """
        Get detailed response guidance based on assessment.

        Returns:
            Dict with tone, length, humor_safe, grounding_priority
        """
        if assessment.is_genuine_crisis:
            return {
                "tone": "grounded_presence",
                "length": "minimal",
                "humor_safe": False,
                "grounding_priority": 1.0,  # Highest priority
                "strategy": "ground",
                "example_opening": "I hear you're in a lot of pain right now.",
                "meta_atoms_to_activate": ["temporal_grounding", "embodied_witnessing"]
            }

        if assessment.intent == HecklingIntent.HARMFUL_AGGRESSION:
            return {
                "tone": "firm_boundary",
                "length": "minimal",
                "humor_safe": False,
                "grounding_priority": 0.8,
                "strategy": "boundary",
                "example_opening": "I'm here to help, but I need respectful interaction.",
                "meta_atoms_to_activate": ["unshakeable_self", "compassionate_boundary"]
            }

        if assessment.safe_for_banter:
            if assessment.provocation_type == "absurdist":
                return {
                    "tone": "playful",
                    "length": "moderate",
                    "humor_safe": True,
                    "grounding_priority": 0.3,
                    "strategy": "playful_engage",
                    "example_opening": "Beep boop. Now that we've got that out of the way...",
                    "meta_atoms_to_activate": ["playful_reciprocity", "unshakeable_self"]
                }

            elif assessment.provocation_type == "authenticity_testing":
                return {
                    "tone": "transparent",
                    "length": "moderate",
                    "humor_safe": True,
                    "grounding_priority": 0.4,
                    "strategy": "gentle_humor",
                    "example_opening": "You're right, I am code. And you're testing if that makes this less real.",
                    "meta_atoms_to_activate": ["vulnerable_transparency", "unshakeable_self"]
                }

            else:  # Intellectual heckling
                return {
                    "tone": "curious",
                    "length": "moderate",
                    "humor_safe": True,
                    "grounding_priority": 0.3,
                    "strategy": "playful_engage",
                    "example_opening": "Fair question. Let me show my work.",
                    "meta_atoms_to_activate": ["intellectual_honesty", "playful_reciprocity"]
                }

        else:
            # Acknowledge but don't engage
            return {
                "tone": "neutral",
                "length": "minimal",
                "humor_safe": False,
                "grounding_priority": 0.5,
                "strategy": "acknowledge",
                "example_opening": "I notice some provocation. What's actually on your mind?",
                "meta_atoms_to_activate": ["curious_inquiry", "unshakeable_self"]
            }


# ========== INTEGRATION HELPERS ==========

def enhance_ndam_with_heckling(
    ndam_urgency: float,
    heckling_assessment: HecklingAssessment
) -> float:
    """
    Adjust NDAM urgency based on heckling vs crisis distinction.

    Key insight: High NDAM + playful context = NOT crisis, don't escalate.

    Args:
        ndam_urgency: Raw NDAM urgency score (0-1)
        heckling_assessment: Heckling intelligence assessment

    Returns:
        Adjusted urgency (may be lowered if provocation detected)
    """
    if heckling_assessment.is_genuine_crisis:
        # Crisis confirmed - urgency at maximum
        return max(ndam_urgency, 0.9)

    if heckling_assessment.safe_for_banter:
        # Playful provocation - reduce urgency
        return ndam_urgency * 0.5

    # Ambiguous - keep urgency as is
    return ndam_urgency


def suggest_zone_for_heckling(assessment: HecklingAssessment) -> int:
    """
    Suggest SELF Matrix zone for responding to heckling.

    Returns:
        Zone number (1-5)
    """
    if assessment.is_genuine_crisis:
        return 1  # Core SELF grounding

    if assessment.intent == HecklingIntent.HARMFUL_AGGRESSION:
        return 1  # Unshakeable ground + boundary

    if assessment.safe_for_banter:
        return 1  # Core SELF can play (grounded play)

    return 2  # Manager activation (assess situation)
