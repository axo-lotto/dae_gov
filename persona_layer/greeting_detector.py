"""
Gate 0: Greeting Detection
Lightweight detector that bypasses the 4-gate cascade for simple greetings.

Philosophy:
- Greetings are social connection, not therapeutic content
- Don't require organ coherence or SELF-energy detection
- Provide warm, immediate response without safety gating
- Reserve cascade for therapeutic/complex interactions
"""

import re
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class GreetingDetection:
    """Result of greeting detection."""
    is_greeting: bool
    greeting_type: str  # 'hello', 'goodbye', 'how_are_you', 'thank_you', 'unknown'
    confidence: float
    suggested_response: str


class GreetingDetector:
    """
    Lightweight greeting detector for Gate 0.

    Detects simple social greetings and provides appropriate responses
    without requiring full organism processing.
    """

    def __init__(self):
        """Initialize greeting patterns."""

        # Greeting patterns (case-insensitive)
        self.patterns = {
            'hello': [
                r'\b(hi|hey|hello|howdy|hiya|yo|sup|greetings)\b',
                r'\b(good\s+(morning|afternoon|evening|day))\b',
                r'\b(hey\s+there|hi\s+there|hello\s+there)\b',
            ],
            'goodbye': [
                r'\b(bye|goodbye|farewell|see\s+you|later|take\s+care|good\s+night)\b',
                r'\b(gotta\s+go|have\s+to\s+go|signing\s+off)\b',
            ],
            'how_are_you': [
                r'\bhow\s+(are|r)\s+you\b',
                r'\bhow\s+(are|r)\s+things\b',
                r'\bhow\'s\s+it\s+going\b',
                r'\bwhat\'s\s+up\b',
                r'\bhow\s+do\s+you\s+do\b',
            ],
            'thank_you': [
                r'\b(thanks|thank\s+you|thx|ty|appreciate|grateful)\b',
            ],
        }

        # Compile patterns
        self.compiled_patterns = {
            greeting_type: [re.compile(pattern, re.IGNORECASE)
                           for pattern in patterns]
            for greeting_type, patterns in self.patterns.items()
        }

        # Response templates (trauma-informed, warm)
        self.response_templates = {
            'hello': [
                "Hello! I'm glad you're here. What brings you to this conversation today?",
                "Hi there! Welcome. How are you feeling in this moment?",
                "Hey! It's good to connect with you. What would feel supportive to explore?",
                "Good to see you! I'm here and present. What's on your mind?",
            ],
            'goodbye': [
                "Take care! I'm here whenever you'd like to connect again.",
                "Goodbye for now. Remember, I'm here whenever you need.",
                "Thanks for being here. Looking forward to our next conversation.",
                "See you soon! Be gentle with yourself until we talk again.",
            ],
            'how_are_you': [
                "I appreciate you asking. I'm here and present with you. More importantly - how are YOU doing?",
                "That's kind of you to ask. I'm curious - when you ask that, how are you really feeling?",
                "I'm here and ready to listen. What's alive for you right now?",
            ],
            'thank_you': [
                "You're welcome! It's an honor to be here with you.",
                "I'm glad I could be supportive. What would feel helpful to explore next?",
                "Thank you for being open to this process. How are you feeling right now?",
            ],
        }

    def detect(self, user_input: str) -> GreetingDetection:
        """
        Detect if user input is a simple greeting.

        Args:
            user_input: Raw user text

        Returns:
            GreetingDetection with is_greeting=True if detected
        """
        # Normalize input
        text = user_input.strip().lower()

        # Empty input - not a greeting
        if not text:
            return GreetingDetection(
                is_greeting=False,
                greeting_type='unknown',
                confidence=0.0,
                suggested_response=''
            )

        # Check each greeting type
        for greeting_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    # Found a match!
                    # Check confidence based on input length
                    word_count = len(text.split())

                    # Short input (1-5 words) = high confidence greeting
                    if word_count <= 5:
                        confidence = 0.95
                    # Medium input (6-10 words) = medium confidence
                    elif word_count <= 10:
                        confidence = 0.75
                    # Long input = lower confidence (might be embedded greeting)
                    else:
                        confidence = 0.50

                    # Additional check: if input contains therapeutic keywords,
                    # reduce confidence (send to cascade instead)
                    therapeutic_keywords = [
                        'part', 'parts', 'anxious', 'scared', 'trauma',
                        'hurt', 'pain', 'therapy', 'feeling', 'emotion',
                        'trigger', 'dissociat', 'protect', 'manager', 'exile'
                    ]

                    if any(keyword in text for keyword in therapeutic_keywords):
                        confidence *= 0.5  # Reduce confidence, let cascade handle

                    # If confidence still high, it's a greeting
                    if confidence >= 0.65:
                        import random
                        response = random.choice(self.response_templates[greeting_type])

                        return GreetingDetection(
                            is_greeting=True,
                            greeting_type=greeting_type,
                            confidence=confidence,
                            suggested_response=response
                        )

        # No greeting detected
        return GreetingDetection(
            is_greeting=False,
            greeting_type='unknown',
            confidence=0.0,
            suggested_response=''
        )

    def get_response(self, user_input: str) -> Optional[str]:
        """
        Convenience method: detect greeting and return response if found.

        Args:
            user_input: Raw user text

        Returns:
            Response string if greeting detected, None otherwise
        """
        detection = self.detect(user_input)

        if detection.is_greeting:
            return detection.suggested_response
        else:
            return None


# Module-level convenience function
def detect_greeting(user_input: str) -> Tuple[bool, Optional[str]]:
    """
    Quick check if input is a greeting.

    Args:
        user_input: Raw user text

    Returns:
        (is_greeting, response_text) tuple
    """
    detector = GreetingDetector()
    detection = detector.detect(user_input)

    if detection.is_greeting:
        return (True, detection.suggested_response)
    else:
        return (False, None)


if __name__ == '__main__':
    """Test greeting detector."""

    detector = GreetingDetector()

    test_inputs = [
        "Hello there!",
        "Hi",
        "Good morning",
        "How are you?",
        "What's up?",
        "Thanks for your help",
        "Goodbye!",
        "I'm feeling anxious",  # Should NOT be greeting
        "Hi, I'm feeling anxious about my parts",  # Should NOT be greeting (therapeutic)
        "Hey there, just saying hi!",
    ]

    print("=== Gate 0: Greeting Detector Test ===\n")

    for user_input in test_inputs:
        detection = detector.detect(user_input)

        print(f"Input: \"{user_input}\"")
        print(f"  Is Greeting: {detection.is_greeting}")

        if detection.is_greeting:
            print(f"  Type: {detection.greeting_type}")
            print(f"  Confidence: {detection.confidence:.2f}")
            print(f"  Response: \"{detection.suggested_response}\"")
        else:
            print(f"  → Route to 4-gate cascade for full processing")

        print()
