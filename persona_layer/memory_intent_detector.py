#!/usr/bin/env python3
"""
Memory Intent Detector - Phase 1.8
====================================

Detects when user wants DAE to remember information.

Patterns detected:
- Explicit memory requests: "can you remember...", "don't forget..."
- Name introductions: "my name is...", "call me..."
- Others' names: "their names are...", "named..."
- Relationships: "my father", "my children", etc.

Date: November 14, 2025
Phase: 1.8 - Entity Extraction & Memory
"""

import re
from typing import Tuple, Dict, List, Any


class MemoryIntentDetector:
    """
    Detects memory intent in user input.

    Returns whether user wants information remembered, what type of
    memory intent it is, and confidence level.
    """

    # Memory request patterns (explicit)
    EXPLICIT_MEMORY_PATTERNS = [
        (r'\b(can you |please |could you |would you )?(remember|recall|memorize|store|save)', 0.9),
        (r'\b(don\'?t forget|keep in mind|note that|make sure you remember)', 0.85),
        (r'\btake note', 0.8),
    ]

    # Self-introduction patterns
    SELF_INTRO_PATTERNS = [
        (r'\bmy name is ([A-Z][a-z]+)', 0.95),
        (r'\bi\'?m called ([A-Z][a-z]+)', 0.90),
        (r'\bcall me ([A-Z][a-z]+)', 0.90),
        (r'\bi am ([A-Z][a-z]+)', 0.85),  # "I am John"
        (r'\bthis is ([A-Z][a-z]+)(?:\s+speaking)?', 0.80),  # "This is John"
    ]

    # Others' names patterns
    OTHERS_NAMES_PATTERNS = [
        (r'\b(their|his|her) names? (are|is)', 0.90),
        (r'\bnamed ([A-Z][a-z]+(?:,?\s+(?:and\s+)?[A-Z][a-z]+)*)', 0.85),
        (r'\b(these are|here are|meet)(?:\s+my)?(?:\s+\w+)?\s*:\s*([A-Z])', 0.80),
    ]

    # Relationship patterns
    RELATIONSHIP_PATTERNS = [
        (r'\bi\'?m a (father|mother|parent|husband|wife|brother|sister|son|daughter)', 0.90),
        (r'\bmy (father|mother|parent|husband|wife|brother|sister|son|daughter|child|children)', 0.85),
        (r'\b(father|mother|parent) of (\d+|one|two|three|four|five|six|seven|eight|nine|ten)', 0.90),
    ]

    def __init__(self):
        """Initialize detector."""
        pass

    def detect(self, text: str) -> Tuple[bool, str, float, Dict[str, Any]]:
        """
        Detect memory intent in user input.

        Args:
            text: User's message

        Returns:
            (intent_detected, intent_type, confidence, context)

            intent_type values:
            - 'explicit_request': User explicitly asks to remember
            - 'self_introduction': User introduces themselves
            - 'others_introduction': User mentions others' names
            - 'relationship_statement': User describes relationships
            - 'none': No memory intent detected

            context: Additional extracted information
        """
        text_lower = text.lower()
        context = {}

        # Check self-introduction FIRST (most specific - includes name extraction)
        # 🌀 CRITICAL FIX (Nov 14, 2025): Moved before explicit_request to extract names
        # from "my name is X, can you remember?" type inputs
        for pattern, confidence in self.SELF_INTRO_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Extract name from the matched pattern
                if match.groups() and match.group(1):
                    context['extracted_name'] = match.group(1)
                return (True, 'self_introduction', confidence, context)

        # Check explicit memory requests (after self-introduction)
        for pattern, confidence in self.EXPLICIT_MEMORY_PATTERNS:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                context['explicit_request'] = True
                return (True, 'explicit_request', confidence, context)

        # Check others' names
        for pattern, confidence in self.OTHERS_NAMES_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                context['mentions_others'] = True
                return (True, 'others_introduction', confidence, context)

        # Check relationship statements
        for pattern, confidence in self.RELATIONSHIP_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                context['relationship_mentioned'] = True
                if match.groups():
                    context['relationship_type'] = match.group(1)
                return (True, 'relationship_statement', confidence, context)

        # No memory intent detected
        return (False, 'none', 0.0, {})

    def should_acknowledge_memory(self, intent_type: str, confidence: float) -> bool:
        """
        Determine if DAE should explicitly acknowledge memory storage.

        Args:
            intent_type: Type of memory intent detected
            confidence: Confidence level

        Returns:
            True if should acknowledge, False otherwise
        """
        # Always acknowledge explicit requests
        if intent_type == 'explicit_request' and confidence > 0.7:
            return True

        # Acknowledge self-introductions
        if intent_type == 'self_introduction' and confidence > 0.8:
            return True

        # Acknowledge others' names if confidence is high
        if intent_type == 'others_introduction' and confidence > 0.8:
            return True

        # Don't explicitly acknowledge relationships (too intrusive)
        # Just quietly remember them
        if intent_type == 'relationship_statement':
            return False

        return False

    def get_acknowledgment_template(self, intent_type: str) -> str:
        """
        Get natural language template for acknowledging memory storage.

        Args:
            intent_type: Type of memory intent

        Returns:
            Template string with {placeholders}
        """
        templates = {
            'explicit_request': [
                "Of course, I'll remember that.",
                "Got it, I'll keep that in mind.",
                "Absolutely, I'll remember.",
            ],
            'self_introduction': [
                "Nice to meet you, {name}!",
                "{name}, lovely to meet you!",
                "Great to meet you, {name}!",
            ],
            'others_introduction': [
                "I'll remember {names}.",
                "Got it - {names}.",
                "I'll keep that in mind - {names}.",
            ],
        }

        return templates.get(intent_type, ["I understand."])[0]


# ===== Utility Functions =====

def quick_memory_check(text: str) -> bool:
    """
    Quick check if user wants something remembered.

    Args:
        text: User's message

    Returns:
        True if memory intent detected, False otherwise

    Example:
        >>> quick_memory_check("can you remember my name?")
        True
        >>> quick_memory_check("how are you?")
        False
    """
    detector = MemoryIntentDetector()
    detected, _, confidence, _ = detector.detect(text)
    return detected and confidence > 0.7


def extract_memory_intent(text: str) -> Dict[str, Any]:
    """
    Extract complete memory intent information.

    Args:
        text: User's message

    Returns:
        Dict with intent info

    Example:
        >>> extract_memory_intent("my name is Alice")
        {'detected': True, 'type': 'self_introduction',
         'confidence': 0.95, 'name': 'Alice'}
    """
    detector = MemoryIntentDetector()
    detected, intent_type, confidence, context = detector.detect(text)

    return {
        'detected': detected,
        'type': intent_type,
        'confidence': confidence,
        'context': context,
        'should_acknowledge': detector.should_acknowledge_memory(intent_type, confidence)
    }


if __name__ == '__main__':
    # Test cases
    detector = MemoryIntentDetector()

    test_cases = [
        "Hello there, my name is ET and i am a father of six",
        "their names are: alice, jaime, pepe, nana, jaime, and bobby can you remember them?",
        "can you remember my birthday is June 5th?",
        "I'm called John",
        "my father's name is Robert",
        "how are you doing today?",
    ]

    print("Memory Intent Detection Tests:\n")
    for test in test_cases:
        detected, intent_type, confidence, context = detector.detect(test)
        print(f"Input: {test}")
        print(f"  Detected: {detected}")
        print(f"  Type: {intent_type}")
        print(f"  Confidence: {confidence:.2f}")
        print(f"  Context: {context}")
        print(f"  Should acknowledge: {detector.should_acknowledge_memory(intent_type, confidence)}")
        print()
