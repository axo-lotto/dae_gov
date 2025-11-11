"""
PRESENCE Organ - Conversational Text Core
Detects somatic grounding, embodied awareness, and here-now presence signals.

Philosophy:
- Presence is felt through somatic grounding and embodied awareness
- Temporal immediacy is "nowness" quality
- Attention stability is sustained focus without drift
- Presence emerges through body-mind integration
"""

import re
import time
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field


@dataclass
class PresencePattern:
    """Detected presence pattern."""
    pattern_type: str  # 'here_now', 'somatic', 'embodied', 'temporal', 'presence_marker', 'focus'
    strength: float  # Activation strength (0.0-2.0, amplified for deep presence)
    chunk_id: str
    position: int
    matched_keywords: List[str]
    confidence: float  # Pattern confidence (0.0-1.0)
    presence_quality: str  # 'mental', 'embodied', 'relational', 'transcendent'
    co_occurring_patterns: List[str] = field(default_factory=list)


@dataclass
class PresenceResult:
    """Universal organ output for PRESENCE."""
    coherence: float  # Overall presence coherence (0.0-1.0)
    patterns: List[PresencePattern]
    lure: float  # Appetition pull toward deeper presence
    processing_time_ms: float

    # Additional PRESENCE-specific metrics
    here_now_score: float = 0.0  # Temporal presence (0.0-1.0)
    somatic_grounding: float = 0.0  # Body awareness (0.0-1.0)
    embodied_sensing: float = 0.0  # Felt experience (0.0-1.0)
    temporal_immediacy: float = 0.0  # Nowness quality (0.0-1.0)
    attention_stability: float = 0.0  # Focus continuity (0.0-1.0)
    dominant_presence: Optional[str] = None  # 'mental', 'embodied', 'relational', 'transcendent'


@dataclass
class PresenceConfig:
    """Configuration for PRESENCE organ."""
    here_now_threshold: float = 0.4
    somatic_threshold: float = 0.5
    embodied_threshold: float = 0.6
    transcendent_threshold: float = 0.8

    # Amplification for deep presence
    transcendent_amplification: float = 2.0
    embodied_amplification: float = 1.6
    somatic_amplification: float = 1.3


DEFAULT_PRESENCE_CONFIG = PresenceConfig()


class PresenceTextCore:
    """
    PRESENCE Organ - Detects somatic grounding and embodied awareness in conversational text.

    100% LLM-free, keyword-based detection with presence pattern recognition.
    Follows universal organ interface pattern.
    """

    def __init__(self, config: Optional[PresenceConfig] = None):
        """Initialize PRESENCE organ with keyword mappings."""
        self.config = config or DEFAULT_PRESENCE_CONFIG

        # HERE-NOW: Temporal presence ("right now", "this moment", "present")
        self.here_now_keywords = {
            'right now', 'this moment', 'present', 'now', 'immediate',
            'current', 'presently', 'at this time', 'as we speak',
            'in this instant', 'here and now', 'immediately', 'currently',
            'contemporaneous', 'instant'
        }

        # SOMATIC GROUNDING: Body awareness ("in my body", "grounded", "rooted", "feet on")
        self.somatic_keywords = {
            'in my body', 'grounded', 'rooted', 'feet on', 'planted',
            'anchored', 'settled', 'stable', 'solid ground', 'earth',
            'centered', 'balanced', 'weighted', 'foundation', 'base',
            'embodied', 'physical', 'bodily', 'corporeal'
        }

        # EMBODIED SENSING: Felt experience ("notice", "sense", "aware", "feel", "perceive")
        self.embodied_keywords = {
            'notice', 'noticing', 'sense', 'sensing', 'aware', 'awareness',
            'feel', 'feeling', 'perceive', 'perceiving', 'experience',
            'experiencing', 'observe', 'observing', 'attentive', 'attuned',
            'conscious of', 'cognizant', 'mindful', 'sensitive to'
        }

        # TEMPORAL IMMEDIACY: Nowness quality ("now", "immediate", "instant", "moment")
        self.temporal_keywords = {
            'now', 'immediate', 'instant', 'moment', 'momentary',
            'present time', 'current moment', 'this second', 'right here',
            'here', 'temporal', 'contemporary', 'instantaneous',
            'simultaneous', 'concurrent'
        }

        # PRESENCE MARKERS: Explicit presence ("here", "with you", "fully", "completely")
        self.presence_marker_keywords = {
            'here', 'with you', 'fully present', 'completely here',
            'fully', 'completely', 'entirely', 'wholly', 'totally',
            'undivided', 'engaged', 'absorbed', 'immersed', 'attentive'
        }

        # FOCUS: Sustained attention ("focused", "attention", "concentrate", "staying with")
        self.focus_keywords = {
            'focused', 'focusing', 'attention', 'attending', 'concentrate',
            'concentrating', 'staying with', 'staying present', 'remain with',
            'hold attention', 'sustained', 'continuous', 'unbroken',
            'steady', 'stable focus'
        }

        # Compile regex patterns
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile keyword sets into regex patterns."""
        self.here_now_pattern = self._make_pattern(self.here_now_keywords)
        self.somatic_pattern = self._make_pattern(self.somatic_keywords)
        self.embodied_pattern = self._make_pattern(self.embodied_keywords)
        self.temporal_pattern = self._make_pattern(self.temporal_keywords)
        self.presence_marker_pattern = self._make_pattern(self.presence_marker_keywords)
        self.focus_pattern = self._make_pattern(self.focus_keywords)

    def _make_pattern(self, keywords: Set[str]) -> re.Pattern:
        """Create case-insensitive regex pattern from keyword set."""
        escaped = [re.escape(kw) for kw in sorted(keywords, key=len, reverse=True)]
        return re.compile(r'\b(' + '|'.join(escaped) + r')', re.IGNORECASE)

    def process_text_occasions(
        self,
        occasions: List,  # List[TextOccasion]
        cycle: int
    ) -> PresenceResult:
        """
        Process text occasions to detect presence patterns.

        Universal organ interface: occasions → Result

        Args:
            occasions: List of TextOccasion entities (actual occasions)
            cycle: Current convergence cycle (unused for now, future V0 integration)

        Returns:
            PresenceResult with coherence, patterns, lure, metrics
        """
        start_time = time.time()
        patterns: List[PresencePattern] = []

        # Process each occasion (text chunk)
        for idx, occasion in enumerate(occasions):
            text = occasion.text.lower()
            chunk_id = occasion.chunk_id

            # Detect all pattern types
            patterns.extend(self._detect_here_now(text, chunk_id, idx))
            patterns.extend(self._detect_somatic(text, chunk_id, idx))
            patterns.extend(self._detect_embodied(text, chunk_id, idx))
            patterns.extend(self._detect_temporal(text, chunk_id, idx))
            patterns.extend(self._detect_presence_marker(text, chunk_id, idx))
            patterns.extend(self._detect_focus(text, chunk_id, idx))

        # Compute aggregate metrics
        result = self._compute_result(patterns, start_time)

        return result

    def _detect_here_now(self, text: str, chunk_id: str, position: int) -> List[PresencePattern]:
        """Detect here-now patterns (temporal presence)."""
        matches = self.here_now_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.6, 1.4)
        confidence = 0.85

        return [PresencePattern(
            pattern_type='here_now',
            strength=strength,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            presence_quality='mental'
        )]

    def _detect_somatic(self, text: str, chunk_id: str, position: int) -> List[PresencePattern]:
        """Detect somatic grounding patterns (body awareness)."""
        matches = self.somatic_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.8, 1.6)
        confidence = 0.9

        return [PresencePattern(
            pattern_type='somatic',
            strength=strength * self.config.somatic_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            presence_quality='embodied'
        )]

    def _detect_embodied(self, text: str, chunk_id: str, position: int) -> List[PresencePattern]:
        """Detect embodied sensing patterns (felt experience)."""
        matches = self.embodied_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.7, 1.5)
        confidence = 0.85

        return [PresencePattern(
            pattern_type='embodied',
            strength=strength * self.config.embodied_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            presence_quality='embodied'
        )]

    def _detect_temporal(self, text: str, chunk_id: str, position: int) -> List[PresencePattern]:
        """Detect temporal immediacy patterns (nowness quality)."""
        matches = self.temporal_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.65, 1.3)
        confidence = 0.8

        return [PresencePattern(
            pattern_type='temporal',
            strength=strength,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            presence_quality='mental'
        )]

    def _detect_presence_marker(self, text: str, chunk_id: str, position: int) -> List[PresencePattern]:
        """Detect presence marker patterns (explicit presence)."""
        matches = self.presence_marker_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.75, 1.6)
        confidence = 0.9

        return [PresencePattern(
            pattern_type='presence_marker',
            strength=strength * self.config.embodied_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            presence_quality='relational'
        )]

    def _detect_focus(self, text: str, chunk_id: str, position: int) -> List[PresencePattern]:
        """Detect focus patterns (sustained attention)."""
        matches = self.focus_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.9, 1.8)
        confidence = 0.95

        return [PresencePattern(
            pattern_type='focus',
            strength=strength * self.config.transcendent_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            presence_quality='transcendent'
        )]

    def _compute_result(self, patterns: List[PresencePattern], start_time: float) -> PresenceResult:
        """Compute aggregate PresenceResult from detected patterns."""
        processing_time_ms = (time.time() - start_time) * 1000

        if not patterns:
            return PresenceResult(
                coherence=0.0,
                patterns=[],
                lure=0.0,
                processing_time_ms=processing_time_ms,
                here_now_score=0.0,
                somatic_grounding=0.0,
                embodied_sensing=0.0,
                temporal_immediacy=0.0,
                attention_stability=0.0,
                dominant_presence=None
            )

        # Compute coherence (average confidence weighted by strength)
        total_weight = sum(p.strength * p.confidence for p in patterns)
        total_strength = sum(p.strength for p in patterns)
        coherence = min(total_weight / max(total_strength, 0.1), 1.0)

        # Compute lure (pull toward deeper presence)
        quality_scores = {
            'mental': 0.3,
            'embodied': 0.7,
            'relational': 0.85,
            'transcendent': 1.0
        }
        avg_quality = sum(quality_scores[p.presence_quality] for p in patterns) / len(patterns)
        lure = min(avg_quality * 1.3, 1.0)

        # Compute specific metrics
        here_now_score = self._compute_here_now(patterns)
        somatic_grounding = self._compute_somatic(patterns)
        embodied_sensing = self._compute_embodied(patterns)
        temporal_immediacy = self._compute_temporal(patterns)
        attention_stability = self._compute_focus(patterns)

        # Dominant presence quality
        quality_counts = {}
        for p in patterns:
            quality_counts[p.presence_quality] = quality_counts.get(p.presence_quality, 0) + p.strength
        dominant_presence = max(quality_counts, key=quality_counts.get) if quality_counts else None

        return PresenceResult(
            coherence=coherence,
            patterns=patterns,
            lure=lure,
            processing_time_ms=processing_time_ms,
            here_now_score=here_now_score,
            somatic_grounding=somatic_grounding,
            embodied_sensing=embodied_sensing,
            temporal_immediacy=temporal_immediacy,
            attention_stability=attention_stability,
            dominant_presence=dominant_presence
        )

    def _compute_here_now(self, patterns: List[PresencePattern]) -> float:
        """Compute here-now score from here_now patterns."""
        here_now_patterns = [p for p in patterns if p.pattern_type == 'here_now']
        if not here_now_patterns:
            return 0.0
        return min(sum(p.strength for p in here_now_patterns) / 2.5, 1.0)

    def _compute_somatic(self, patterns: List[PresencePattern]) -> float:
        """Compute somatic grounding from somatic patterns."""
        somatic_patterns = [p for p in patterns if p.pattern_type == 'somatic']
        if not somatic_patterns:
            return 0.0
        return min(sum(p.strength for p in somatic_patterns) / 2.0, 1.0)

    def _compute_embodied(self, patterns: List[PresencePattern]) -> float:
        """Compute embodied sensing from embodied patterns."""
        embodied_patterns = [p for p in patterns if p.pattern_type == 'embodied']
        if not embodied_patterns:
            return 0.0
        return min(sum(p.strength for p in embodied_patterns) / 2.0, 1.0)

    def _compute_temporal(self, patterns: List[PresencePattern]) -> float:
        """Compute temporal immediacy from temporal patterns."""
        temporal_patterns = [p for p in patterns if p.pattern_type == 'temporal']
        if not temporal_patterns:
            return 0.0
        return min(sum(p.strength for p in temporal_patterns) / 2.0, 1.0)

    def _compute_focus(self, patterns: List[PresencePattern]) -> float:
        """Compute attention stability from focus patterns."""
        focus_patterns = [p for p in patterns if p.pattern_type == 'focus']
        if not focus_patterns:
            return 0.0
        return min(sum(p.strength for p in focus_patterns) / 2.5, 1.0)


# Module-level convenience function
def detect_presence(text: str) -> Dict:
    """
    Quick presence detection from raw text.

    Args:
        text: Raw conversational text

    Returns:
        Dict with coherence, here_now, somatic_grounding, etc.
    """
    from dataclasses import dataclass as _dataclass

    @_dataclass
    class _TextOccasion:
        text: str
        chunk_id: str

    occasion = _TextOccasion(text=text, chunk_id='test')

    core = PresenceTextCore()
    result = core.process_text_occasions([occasion], cycle=0)

    return {
        'coherence': result.coherence,
        'here_now_score': result.here_now_score,
        'somatic_grounding': result.somatic_grounding,
        'embodied_sensing': result.embodied_sensing,
        'temporal_immediacy': result.temporal_immediacy,
        'attention_stability': result.attention_stability,
        'dominant_presence': result.dominant_presence,
        'lure': result.lure
    }


if __name__ == '__main__':
    """Test PRESENCE organ with sample conversational text."""

    test_cases = [
        # Mental/temporal presence
        "Right now, in this moment, I'm present and aware of what's happening.",

        # Somatic grounding
        "I feel grounded, rooted in my body, feet planted on the earth. I'm anchored and centered.",

        # Embodied sensing
        "I notice the sensation in my chest. I'm sensing tightness, aware of my breathing, feeling the weight of my body.",

        # Temporal immediacy
        "Now. This instant. The immediate moment is all there is.",

        # Relational presence
        "I'm here with you, fully present and completely engaged. Undivided attention.",

        # Deep focus (transcendent)
        "My attention is focused and sustained. I'm staying with this, holding steady concentration without drift.",

        # Mixed deep presence
        "Right now, I'm grounded in my body, sensing my breath, fully here with you. My attention is focused and I notice everything - the weight of my feet, the quality of this moment, the immediacy of being present.",
    ]

    print("=" * 70)
    print("PRESENCE ORGAN - Text Core Test")
    print("=" * 70)
    print()

    for idx, text in enumerate(test_cases, 1):
        result = detect_presence(text)

        print(f"Test {idx}: \"{text[:60]}...\"")
        print(f"  Coherence: {result['coherence']:.2f}")
        print(f"  Here-Now: {result['here_now_score']:.2f}")
        print(f"  Somatic: {result['somatic_grounding']:.2f}")
        print(f"  Embodied: {result['embodied_sensing']:.2f}")
        print(f"  Temporal: {result['temporal_immediacy']:.2f}")
        print(f"  Focus: {result['attention_stability']:.2f}")
        print(f"  Dominant: {result['dominant_presence']}")
        print(f"  Lure: {result['lure']:.2f}")
        print()

    print("=" * 70)
    print("✓ PRESENCE organ operational")
    print("=" * 70)
