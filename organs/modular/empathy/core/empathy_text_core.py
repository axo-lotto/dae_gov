"""
EMPATHY Organ - Conversational Text Core
Detects emotional resonance, validation, compassion, and attunement signals.

Philosophy:
- Empathy is felt resonance, not cognitive understanding
- Compassion is warmth toward suffering
- Validation is witnessing without fixing
- Attunement is matching emotional energy
"""

import re
import time
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field


@dataclass
class EmpathyPattern:
    """Detected empathy pattern."""
    pattern_type: str  # 'validation', 'compassion', 'resonance', 'attunement', 'holding'
    strength: float  # Activation strength (0.0-2.0, amplified for deep empathy)
    chunk_id: str
    position: int
    matched_keywords: List[str]
    confidence: float  # Pattern confidence (0.0-1.0)
    empathy_quality: str  # 'cognitive', 'affective', 'compassionate', 'transformative'
    emotional_tone: Optional[str] = None  # 'warm', 'gentle', 'tender', 'fierce'
    co_occurring_patterns: List[str] = field(default_factory=list)


@dataclass
class EmpathyResult:
    """Universal organ output for EMPATHY."""
    coherence: float  # Overall empathy coherence (0.0-1.0)
    patterns: List[EmpathyPattern]
    lure: float  # Appetition pull toward deeper empathic connection
    processing_time_ms: float

    # Additional EMPATHY-specific metrics
    validation_score: float = 0.0  # Witnessing without fixing (0.0-1.0)
    compassion_level: float = 0.0  # Warmth toward suffering (0.0-1.0)
    resonance_depth: float = 0.0  # Emotional mirroring (0.0-1.0)
    attunement_quality: float = 0.0  # Energy matching (0.0-1.0)
    holding_capacity: float = 0.0  # Container strength (0.0-1.0)
    dominant_quality: Optional[str] = None  # 'cognitive', 'affective', 'compassionate', 'transformative'
    emotional_tone: Optional[str] = None  # 'warm', 'gentle', 'tender', 'fierce'


@dataclass
class EmpathyConfig:
    """Configuration for EMPATHY organ."""
    validation_threshold: float = 0.4
    compassion_threshold: float = 0.5
    resonance_threshold: float = 0.6
    transformative_threshold: float = 0.8

    # Amplification for deep empathy
    transformative_amplification: float = 2.0
    compassionate_amplification: float = 1.6
    affective_amplification: float = 1.3


DEFAULT_EMPATHY_CONFIG = EmpathyConfig()


class EmpathyTextCore:
    """
    EMPATHY Organ - Detects empathic resonance in conversational text.

    100% LLM-free, keyword-based detection with emotional pattern recognition.
    Follows universal organ interface pattern.
    """

    def __init__(self, config: Optional[EmpathyConfig] = None):
        """Initialize EMPATHY organ with keyword mappings."""
        self.config = config or DEFAULT_EMPATHY_CONFIG

        # VALIDATION: Witnessing without fixing ("that makes sense", "I get that", "valid")
        self.validation_keywords = {
            'makes sense', 'valid', 'understandable', 'reasonable', 'natural',
            'of course', 'absolutely', 'totally', 'completely normal',
            'anyone would', 'expected', 'warranted', 'justified',
            'legitimate', 'real', 'genuine', 'true', 'authentic response',
            'human', 'normal reaction', 'makes perfect sense',
            'i get that', 'i see that', 'i understand that'
        }

        # COMPASSION: Warmth toward suffering ("I'm sorry", "that's painful", "tender")
        self.compassion_keywords = {
            'sorry', 'painful', 'hurting', 'suffering', 'tender',
            'gentle', 'care', 'caring', 'compassion', 'warmth',
            'soften', 'kindness', 'kind', 'sweet', 'loving',
            'love', 'heart goes out', 'feel for you', 'with you',
            'ache', 'aching', 'tenderness', 'sympathy', 'empathy'
        }

        # RESONANCE: Emotional mirroring ("feeling with you", "I feel that too", "resonates")
        self.resonance_keywords = {
            'resonate', 'resonating', 'feel with', 'feeling with',
            'feel that too', 'same feeling', 'know that feeling',
            'familiar', 'recognize', 'mirror', 'mirroring',
            'echo', 'echoing', 'parallel', 'similar', 'shared',
            'common', 'universal', 'we all', 'human experience',
            'not alone', 'together in this'
        }

        # ATTUNEMENT: Energy matching ("matching your pace", "with your energy", "attuned")
        self.attunement_keywords = {
            'attuned', 'attune', 'matching', 'match your',
            'with your pace', 'with your energy', 'alongside',
            'beside you', 'walking with', 'moving with',
            'in sync', 'synchronized', 'calibrated', 'aligned',
            'harmonized', 'tuned in', 'dialed in', 'responsive'
        }

        # HOLDING: Container strength ("I can hold this", "space for", "here for you")
        self.holding_keywords = {
            'hold', 'holding', 'space for', 'room for', 'contain',
            'here for you', 'with you', 'not going anywhere',
            'stay with', 'staying with', 'won\'t leave', 'steady',
            'stable', 'grounded', 'anchor', 'safe', 'safety',
            'protected', 'secure', 'strong enough', 'can handle'
        }

        # FIERCE COMPASSION: Protective empathy ("that's not okay", "you deserve", "your worth")
        self.fierce_compassion_keywords = {
            'not okay', 'deserve better', 'worthy', 'worth',
            'right to', 'entitled to', 'boundaries', 'protect',
            'stand up', 'advocate', 'fight for', 'fierce',
            'strong', 'powerful', 'claim your', 'reclaim',
            'dignity', 'respect', 'honor yourself', 'sacred'
        }

        # DEEP EMPATHY: Transformative ("witnessing your soul", "profound", "sacred space")
        self.transformative_keywords = {
            'witness', 'witnessing', 'behold', 'see you',
            'truly see', 'soul', 'spirit', 'essence', 'core',
            'profound', 'deep', 'sacred', 'holy', 'precious',
            'transformation', 'transforming', 'shift', 'breakthrough',
            'honor', 'honoring', 'reverence', 'awe', 'moved'
        }

        # Compile regex patterns
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile keyword sets into regex patterns."""
        self.validation_pattern = self._make_pattern(self.validation_keywords)
        self.compassion_pattern = self._make_pattern(self.compassion_keywords)
        self.resonance_pattern = self._make_pattern(self.resonance_keywords)
        self.attunement_pattern = self._make_pattern(self.attunement_keywords)
        self.holding_pattern = self._make_pattern(self.holding_keywords)
        self.fierce_pattern = self._make_pattern(self.fierce_compassion_keywords)
        self.transformative_pattern = self._make_pattern(self.transformative_keywords)

    def _make_pattern(self, keywords: Set[str]) -> re.Pattern:
        """Create case-insensitive regex pattern from keyword set."""
        escaped = [re.escape(kw) for kw in sorted(keywords, key=len, reverse=True)]
        return re.compile(r'\b(' + '|'.join(escaped) + r')', re.IGNORECASE)

    def process_text_occasions(
        self,
        occasions: List,  # List[TextOccasion]
        cycle: int
    ) -> EmpathyResult:
        """
        Process text occasions to detect empathy patterns.

        Universal organ interface: occasions → Result

        Args:
            occasions: List of TextOccasion entities (actual occasions)
            cycle: Current convergence cycle (unused for now, future V0 integration)

        Returns:
            EmpathyResult with coherence, patterns, lure, metrics
        """
        start_time = time.time()
        patterns: List[EmpathyPattern] = []

        # Process each occasion (text chunk)
        for idx, occasion in enumerate(occasions):
            text = occasion.text.lower()
            chunk_id = occasion.chunk_id

            # Detect all pattern types
            patterns.extend(self._detect_validation(text, chunk_id, idx))
            patterns.extend(self._detect_compassion(text, chunk_id, idx))
            patterns.extend(self._detect_resonance(text, chunk_id, idx))
            patterns.extend(self._detect_attunement(text, chunk_id, idx))
            patterns.extend(self._detect_holding(text, chunk_id, idx))
            patterns.extend(self._detect_fierce_compassion(text, chunk_id, idx))
            patterns.extend(self._detect_transformative(text, chunk_id, idx))

        # Compute aggregate metrics
        result = self._compute_result(patterns, start_time)

        return result

    def _detect_validation(self, text: str, chunk_id: str, position: int) -> List[EmpathyPattern]:
        """Detect validation patterns (witnessing without fixing)."""
        matches = self.validation_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.5, 1.2)
        confidence = 0.85

        return [EmpathyPattern(
            pattern_type='validation',
            strength=strength,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            empathy_quality='cognitive',
            emotional_tone='warm'
        )]

    def _detect_compassion(self, text: str, chunk_id: str, position: int) -> List[EmpathyPattern]:
        """Detect compassion patterns (warmth toward suffering)."""
        matches = self.compassion_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.7, 1.5)
        confidence = 0.9

        return [EmpathyPattern(
            pattern_type='compassion',
            strength=strength * self.config.compassionate_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            empathy_quality='compassionate',
            emotional_tone='tender'
        )]

    def _detect_resonance(self, text: str, chunk_id: str, position: int) -> List[EmpathyPattern]:
        """Detect resonance patterns (emotional mirroring)."""
        matches = self.resonance_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.8, 1.6)
        confidence = 0.8

        return [EmpathyPattern(
            pattern_type='resonance',
            strength=strength * self.config.affective_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            empathy_quality='affective',
            emotional_tone='warm'
        )]

    def _detect_attunement(self, text: str, chunk_id: str, position: int) -> List[EmpathyPattern]:
        """Detect attunement patterns (energy matching)."""
        matches = self.attunement_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.9, 1.7)
        confidence = 0.85

        return [EmpathyPattern(
            pattern_type='attunement',
            strength=strength * self.config.affective_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            empathy_quality='affective',
            emotional_tone='gentle'
        )]

    def _detect_holding(self, text: str, chunk_id: str, position: int) -> List[EmpathyPattern]:
        """Detect holding patterns (container strength)."""
        matches = self.holding_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.75, 1.6)
        confidence = 0.9

        return [EmpathyPattern(
            pattern_type='holding',
            strength=strength * self.config.compassionate_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            empathy_quality='compassionate',
            emotional_tone='steady'
        )]

    def _detect_fierce_compassion(self, text: str, chunk_id: str, position: int) -> List[EmpathyPattern]:
        """Detect fierce compassion (protective empathy)."""
        matches = self.fierce_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 1.1, 1.8)
        confidence = 0.95

        return [EmpathyPattern(
            pattern_type='fierce_compassion',
            strength=strength * self.config.compassionate_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            empathy_quality='compassionate',
            emotional_tone='fierce'
        )]

    def _detect_transformative(self, text: str, chunk_id: str, position: int) -> List[EmpathyPattern]:
        """Detect transformative empathy (deepest level)."""
        matches = self.transformative_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 1.3, 2.0)  # Can reach maximum 2.0
        confidence = 0.95

        return [EmpathyPattern(
            pattern_type='transformative',
            strength=strength * self.config.transformative_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            empathy_quality='transformative',
            emotional_tone='reverent'
        )]

    def _compute_result(self, patterns: List[EmpathyPattern], start_time: float) -> EmpathyResult:
        """Compute aggregate EmpathyResult from detected patterns."""
        processing_time_ms = (time.time() - start_time) * 1000

        if not patterns:
            return EmpathyResult(
                coherence=0.0,
                patterns=[],
                lure=0.0,
                processing_time_ms=processing_time_ms,
                validation_score=0.0,
                compassion_level=0.0,
                resonance_depth=0.0,
                attunement_quality=0.0,
                holding_capacity=0.0,
                dominant_quality=None,
                emotional_tone=None
            )

        # Compute coherence (average confidence weighted by strength)
        total_weight = sum(p.strength * p.confidence for p in patterns)
        total_strength = sum(p.strength for p in patterns)
        coherence = min(total_weight / max(total_strength, 0.1), 1.0)

        # Compute lure (pull toward deeper empathy)
        quality_scores = {
            'cognitive': 0.3,
            'affective': 0.6,
            'compassionate': 0.85,
            'transformative': 1.0
        }
        avg_quality = sum(quality_scores[p.empathy_quality] for p in patterns) / len(patterns)
        lure = min(avg_quality * 1.3, 1.0)

        # Compute specific metrics
        validation_score = self._compute_validation(patterns)
        compassion_level = self._compute_compassion(patterns)
        resonance_depth = self._compute_resonance(patterns)
        attunement_quality = self._compute_attunement(patterns)
        holding_capacity = self._compute_holding(patterns)

        # Dominant quality and tone
        quality_counts = {}
        for p in patterns:
            quality_counts[p.empathy_quality] = quality_counts.get(p.empathy_quality, 0) + p.strength
        dominant_quality = max(quality_counts, key=quality_counts.get) if quality_counts else None

        # Emotional tone (most frequent)
        tone_counts = {}
        for p in patterns:
            if p.emotional_tone:
                tone_counts[p.emotional_tone] = tone_counts.get(p.emotional_tone, 0) + p.strength
        emotional_tone = max(tone_counts, key=tone_counts.get) if tone_counts else None

        return EmpathyResult(
            coherence=coherence,
            patterns=patterns,
            lure=lure,
            processing_time_ms=processing_time_ms,
            validation_score=validation_score,
            compassion_level=compassion_level,
            resonance_depth=resonance_depth,
            attunement_quality=attunement_quality,
            holding_capacity=holding_capacity,
            dominant_quality=dominant_quality,
            emotional_tone=emotional_tone
        )

    def _compute_validation(self, patterns: List[EmpathyPattern]) -> float:
        """Compute validation score from validation patterns."""
        validation_patterns = [p for p in patterns if p.pattern_type == 'validation']
        if not validation_patterns:
            return 0.0
        return min(sum(p.strength for p in validation_patterns) / 2.5, 1.0)

    def _compute_compassion(self, patterns: List[EmpathyPattern]) -> float:
        """Compute compassion level from compassion + fierce patterns."""
        compassion_types = {'compassion', 'fierce_compassion', 'holding'}
        compassion_patterns = [p for p in patterns if p.pattern_type in compassion_types]
        if not compassion_patterns:
            return 0.0
        return min(sum(p.strength for p in compassion_patterns) / 3.0, 1.0)

    def _compute_resonance(self, patterns: List[EmpathyPattern]) -> float:
        """Compute resonance depth from resonance patterns."""
        resonance_patterns = [p for p in patterns if p.pattern_type == 'resonance']
        if not resonance_patterns:
            return 0.0
        return min(sum(p.strength for p in resonance_patterns) / 2.0, 1.0)

    def _compute_attunement(self, patterns: List[EmpathyPattern]) -> float:
        """Compute attunement quality from attunement patterns."""
        attunement_patterns = [p for p in patterns if p.pattern_type == 'attunement']
        if not attunement_patterns:
            return 0.0
        return min(sum(p.strength for p in attunement_patterns) / 2.0, 1.0)

    def _compute_holding(self, patterns: List[EmpathyPattern]) -> float:
        """Compute holding capacity from holding patterns."""
        holding_patterns = [p for p in patterns if p.pattern_type == 'holding']
        if not holding_patterns:
            return 0.0
        return min(sum(p.strength for p in holding_patterns) / 2.0, 1.0)


# Module-level convenience function
def detect_empathy(text: str) -> Dict:
    """
    Quick empathy detection from raw text.

    Args:
        text: Raw conversational text

    Returns:
        Dict with coherence, validation, compassion, resonance, etc.
    """
    from dataclasses import dataclass as _dataclass

    @_dataclass
    class _TextOccasion:
        text: str
        chunk_id: str

    occasion = _TextOccasion(text=text, chunk_id='test')

    core = EmpathyTextCore()
    result = core.process_text_occasions([occasion], cycle=0)

    return {
        'coherence': result.coherence,
        'validation_score': result.validation_score,
        'compassion_level': result.compassion_level,
        'resonance_depth': result.resonance_depth,
        'attunement_quality': result.attunement_quality,
        'holding_capacity': result.holding_capacity,
        'dominant_quality': result.dominant_quality,
        'emotional_tone': result.emotional_tone,
        'lure': result.lure
    }


if __name__ == '__main__':
    """Test EMPATHY organ with sample conversational text."""

    test_cases = [
        # Cognitive validation
        "That makes sense. Your reaction is completely understandable and valid.",

        # Affective resonance
        "I feel that too. What you're describing resonates deeply - we all know that feeling of being unseen.",

        # Compassionate holding
        "I'm so sorry you're hurting. I can hold this with you. You're not alone in this pain.",

        # Fierce compassion
        "That's not okay. You deserve better. Your worth is not defined by how they treated you.",

        # Transformative witnessing
        "I witness you. I see your soul in this moment. What you're sharing is sacred and profound.",

        # Mixed (complex empathy)
        "That makes complete sense - your pain is real and valid. I'm holding space for this with you. I feel the ache of what you're describing. You're not alone, and you deserve tender care right now.",
    ]

    print("=" * 70)
    print("EMPATHY ORGAN - Text Core Test")
    print("=" * 70)
    print()

    for idx, text in enumerate(test_cases, 1):
        result = detect_empathy(text)

        print(f"Test {idx}: \"{text[:60]}...\"")
        print(f"  Coherence: {result['coherence']:.2f}")
        print(f"  Validation: {result['validation_score']:.2f}")
        print(f"  Compassion: {result['compassion_level']:.2f}")
        print(f"  Resonance: {result['resonance_depth']:.2f}")
        print(f"  Attunement: {result['attunement_quality']:.2f}")
        print(f"  Holding: {result['holding_capacity']:.2f}")
        print(f"  Quality: {result['dominant_quality']}")
        print(f"  Tone: {result['emotional_tone']}")
        print(f"  Lure: {result['lure']:.2f}")
        print()

    print("=" * 70)
    print("✓ EMPATHY organ operational")
    print("=" * 70)
