"""
WISDOM Organ - Conversational Text Core
Detects meta-perspective, insights, reframes, and paradox holding.

Philosophy:
- Wisdom is meta-perspective, seeing patterns across time
- Insight is sudden coherence, "aha" moments
- Perspective shifts are reframes, new vantage points
- Paradox holding is tolerance for ambiguity
"""

import re
import time
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field


@dataclass
class WisdomPattern:
    """Detected wisdom pattern."""
    pattern_type: str  # 'meta_commentary', 'insight', 'reframe', 'paradox', 'temporal', 'collective'
    strength: float  # Activation strength (0.0-2.0, amplified for deep wisdom)
    chunk_id: str
    position: int
    matched_keywords: List[str]
    confidence: float  # Pattern confidence (0.0-1.0)
    wisdom_quality: str  # 'practical', 'philosophical', 'experiential', 'transcendent'
    co_occurring_patterns: List[str] = field(default_factory=list)


@dataclass
class WisdomResult:
    """Universal organ output for WISDOM."""
    coherence: float  # Overall wisdom coherence (0.0-1.0)
    patterns: List[WisdomPattern]
    lure: float  # Appetition pull toward deeper wisdom
    processing_time_ms: float

    # Additional WISDOM-specific metrics
    meta_perspective_score: float = 0.0  # Ability to see from outside (0.0-1.0)
    insight_frequency: float = 0.0  # Aha moments per text (0.0-1.0)
    reframe_capacity: float = 0.0  # Perspective shifting (0.0-1.0)
    paradox_tolerance: float = 0.0  # Comfort with ambiguity (0.0-1.0)
    temporal_integration: float = 0.0  # Seeing patterns over time (0.0-1.0)
    dominant_wisdom: Optional[str] = None  # 'practical', 'philosophical', 'experiential', 'transcendent'


@dataclass
class WisdomConfig:
    """Configuration for WISDOM organ."""
    meta_threshold: float = 0.5
    insight_threshold: float = 0.6
    reframe_threshold: float = 0.5
    paradox_threshold: float = 0.7
    transcendent_threshold: float = 0.8

    # Amplification for deep wisdom
    transcendent_amplification: float = 2.0
    philosophical_amplification: float = 1.6
    experiential_amplification: float = 1.3


DEFAULT_WISDOM_CONFIG = WisdomConfig()


class WisdomTextCore:
    """
    WISDOM Organ - Detects meta-perspective and wisdom in conversational text.

    100% LLM-free, keyword-based detection with wisdom pattern recognition.
    Follows universal organ interface pattern.
    """

    def __init__(self, config: Optional[WisdomConfig] = None):
        """Initialize WISDOM organ with keyword mappings."""
        self.config = config or DEFAULT_WISDOM_CONFIG

        # META-COMMENTARY: Stepping back, zooming out, bigger picture
        self.meta_keywords = {
            'stepping back', 'zooming out', 'bigger picture', 'meta',
            'looking at', 'observing', 'noticing pattern', 'systemic',
            'whole', 'context', 'framework', 'lens', 'vantage',
            'perspective on', 'view from', 'distance', 'bird\'s eye',
            'helicopter view', 'from above', 'overview'
        }

        # INSIGHT MARKERS: Aha, realize, click, suddenly
        self.insight_keywords = {
            'aha', 'realize', 'click', 'suddenly', 'dawn on',
            'light bulb', 'breakthrough', 'epiphany', 'revelation',
            'see now', 'makes sense now', 'oh', 'understand now',
            'illuminat', 'clarity', 'clear now', 'connect',
            'piece together', 'comes together', 'crystalliz'
        }

        # REFRAME: What if, another way, could also, different angle
        self.reframe_keywords = {
            'what if', 'another way', 'could also', 'reframe',
            'consider', 'alternatively', 'flip', 'invert',
            'different angle', 'shift', 'reconsider', 'reimagine',
            'rethink', 'new perspective', 'fresh eyes', 'look at it',
            'see it as', 'frame it', 'think of it', 'view it'
        }

        # PARADOX HOLDING: Both/and, tension, contradiction, complexity
        self.paradox_keywords = {
            'both/and', 'tension', 'contradiction', 'paradox',
            'complex', 'nuance', 'ambiguous', 'uncertainty',
            'mystery', 'unknown', 'gray area', 'spectrum',
            'continuum', 'dialectic', 'integrate', 'hold both',
            'simultaneously', 'at once', 'coexist', 'balance'
        }

        # TEMPORAL WISDOM: Over time, pattern, cycle, learning
        self.temporal_keywords = {
            'over time', 'pattern', 'cycle', 'recurring',
            'learning', 'grow', 'evolve', 'change',
            'journey', 'process', 'unfold', 'emerge',
            'arc', 'trajectory', 'spiral', 'repeat',
            'again and again', 'every time', 'always', 'history'
        }

        # COLLECTIVE WISDOM: We all, humanity, universal, timeless
        self.collective_keywords = {
            'we all', 'humanity', 'human', 'universal',
            'timeless', 'ancient', 'wisdom tradition',
            'collective', 'shared', 'common', 'cultural',
            'ancestral', 'inherited', 'archetypal', 'perennial',
            'age-old', 'eternal', 'across cultures'
        }

        # Compile regex patterns
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile keyword sets into regex patterns."""
        self.meta_pattern = self._make_pattern(self.meta_keywords)
        self.insight_pattern = self._make_pattern(self.insight_keywords)
        self.reframe_pattern = self._make_pattern(self.reframe_keywords)
        self.paradox_pattern = self._make_pattern(self.paradox_keywords)
        self.temporal_pattern = self._make_pattern(self.temporal_keywords)
        self.collective_pattern = self._make_pattern(self.collective_keywords)

    def _make_pattern(self, keywords: Set[str]) -> re.Pattern:
        """Create case-insensitive regex pattern from keyword set."""
        escaped = [re.escape(kw) for kw in sorted(keywords, key=len, reverse=True)]
        return re.compile(r'\b(' + '|'.join(escaped) + r')', re.IGNORECASE)

    def process_text_occasions(
        self,
        occasions: List,  # List[TextOccasion]
        cycle: int
    ) -> WisdomResult:
        """
        Process text occasions to detect wisdom patterns.

        Universal organ interface: occasions → Result

        Args:
            occasions: List of TextOccasion entities (actual occasions)
            cycle: Current convergence cycle (unused for now, future V0 integration)

        Returns:
            WisdomResult with coherence, patterns, lure, metrics
        """
        start_time = time.time()
        patterns: List[WisdomPattern] = []

        # Process each occasion (text chunk)
        for idx, occasion in enumerate(occasions):
            text = occasion.text.lower()
            chunk_id = occasion.chunk_id

            # Detect all pattern types
            patterns.extend(self._detect_meta_commentary(text, chunk_id, idx))
            patterns.extend(self._detect_insight(text, chunk_id, idx))
            patterns.extend(self._detect_reframe(text, chunk_id, idx))
            patterns.extend(self._detect_paradox(text, chunk_id, idx))
            patterns.extend(self._detect_temporal(text, chunk_id, idx))
            patterns.extend(self._detect_collective(text, chunk_id, idx))

        # Compute aggregate metrics
        result = self._compute_result(patterns, start_time)

        return result

    def _detect_meta_commentary(self, text: str, chunk_id: str, position: int) -> List[WisdomPattern]:
        """Detect meta-commentary patterns (stepping back, bigger picture)."""
        matches = self.meta_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.6, 1.4)
        confidence = 0.85

        return [WisdomPattern(
            pattern_type='meta_commentary',
            strength=strength * self.config.philosophical_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            wisdom_quality='philosophical'
        )]

    def _detect_insight(self, text: str, chunk_id: str, position: int) -> List[WisdomPattern]:
        """Detect insight markers (aha moments, breakthroughs)."""
        matches = self.insight_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.8, 1.6)
        confidence = 0.9

        return [WisdomPattern(
            pattern_type='insight',
            strength=strength * self.config.experiential_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            wisdom_quality='experiential'
        )]

    def _detect_reframe(self, text: str, chunk_id: str, position: int) -> List[WisdomPattern]:
        """Detect reframe patterns (perspective shifts)."""
        matches = self.reframe_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.7, 1.5)
        confidence = 0.8

        return [WisdomPattern(
            pattern_type='reframe',
            strength=strength * self.config.experiential_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            wisdom_quality='practical'
        )]

    def _detect_paradox(self, text: str, chunk_id: str, position: int) -> List[WisdomPattern]:
        """Detect paradox holding (both/and, complexity tolerance)."""
        matches = self.paradox_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.9, 1.7)
        confidence = 0.9

        return [WisdomPattern(
            pattern_type='paradox',
            strength=strength * self.config.philosophical_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            wisdom_quality='philosophical'
        )]

    def _detect_temporal(self, text: str, chunk_id: str, position: int) -> List[WisdomPattern]:
        """Detect temporal wisdom (patterns over time, cycles)."""
        matches = self.temporal_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.75, 1.6)
        confidence = 0.85

        return [WisdomPattern(
            pattern_type='temporal',
            strength=strength * self.config.experiential_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            wisdom_quality='experiential'
        )]

    def _detect_collective(self, text: str, chunk_id: str, position: int) -> List[WisdomPattern]:
        """Detect collective wisdom (universal, timeless)."""
        matches = self.collective_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 1.2, 2.0)  # Can reach maximum 2.0
        confidence = 0.95

        return [WisdomPattern(
            pattern_type='collective',
            strength=strength * self.config.transcendent_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            wisdom_quality='transcendent'
        )]

    def _compute_result(self, patterns: List[WisdomPattern], start_time: float) -> WisdomResult:
        """Compute aggregate WisdomResult from detected patterns."""
        processing_time_ms = (time.time() - start_time) * 1000

        if not patterns:
            return WisdomResult(
                coherence=0.0,
                patterns=[],
                lure=0.0,
                processing_time_ms=processing_time_ms,
                meta_perspective_score=0.0,
                insight_frequency=0.0,
                reframe_capacity=0.0,
                paradox_tolerance=0.0,
                temporal_integration=0.0,
                dominant_wisdom=None
            )

        # Compute coherence (average confidence weighted by strength)
        total_weight = sum(p.strength * p.confidence for p in patterns)
        total_strength = sum(p.strength for p in patterns)
        coherence = min(total_weight / max(total_strength, 0.1), 1.0)

        # Compute lure (pull toward deeper wisdom)
        quality_scores = {
            'practical': 0.4,
            'experiential': 0.6,
            'philosophical': 0.8,
            'transcendent': 1.0
        }
        avg_quality = sum(quality_scores[p.wisdom_quality] for p in patterns) / len(patterns)
        lure = min(avg_quality * 1.2, 1.0)

        # Compute specific metrics
        meta_perspective_score = self._compute_meta(patterns)
        insight_frequency = self._compute_insight(patterns)
        reframe_capacity = self._compute_reframe(patterns)
        paradox_tolerance = self._compute_paradox(patterns)
        temporal_integration = self._compute_temporal(patterns)

        # Dominant wisdom quality
        quality_counts = {}
        for p in patterns:
            quality_counts[p.wisdom_quality] = quality_counts.get(p.wisdom_quality, 0) + p.strength
        dominant_wisdom = max(quality_counts, key=quality_counts.get) if quality_counts else None

        return WisdomResult(
            coherence=coherence,
            patterns=patterns,
            lure=lure,
            processing_time_ms=processing_time_ms,
            meta_perspective_score=meta_perspective_score,
            insight_frequency=insight_frequency,
            reframe_capacity=reframe_capacity,
            paradox_tolerance=paradox_tolerance,
            temporal_integration=temporal_integration,
            dominant_wisdom=dominant_wisdom
        )

    def _compute_meta(self, patterns: List[WisdomPattern]) -> float:
        """Compute meta-perspective score from meta patterns."""
        meta_patterns = [p for p in patterns if p.pattern_type == 'meta_commentary']
        if not meta_patterns:
            return 0.0
        return min(sum(p.strength for p in meta_patterns) / 2.0, 1.0)

    def _compute_insight(self, patterns: List[WisdomPattern]) -> float:
        """Compute insight frequency from insight patterns."""
        insight_patterns = [p for p in patterns if p.pattern_type == 'insight']
        if not insight_patterns:
            return 0.0
        return min(sum(p.strength for p in insight_patterns) / 2.5, 1.0)

    def _compute_reframe(self, patterns: List[WisdomPattern]) -> float:
        """Compute reframe capacity from reframe patterns."""
        reframe_patterns = [p for p in patterns if p.pattern_type == 'reframe']
        if not reframe_patterns:
            return 0.0
        return min(sum(p.strength for p in reframe_patterns) / 2.0, 1.0)

    def _compute_paradox(self, patterns: List[WisdomPattern]) -> float:
        """Compute paradox tolerance from paradox patterns."""
        paradox_patterns = [p for p in patterns if p.pattern_type == 'paradox']
        if not paradox_patterns:
            return 0.0
        return min(sum(p.strength for p in paradox_patterns) / 2.0, 1.0)

    def _compute_temporal(self, patterns: List[WisdomPattern]) -> float:
        """Compute temporal integration from temporal patterns."""
        temporal_patterns = [p for p in patterns if p.pattern_type == 'temporal']
        if not temporal_patterns:
            return 0.0
        return min(sum(p.strength for p in temporal_patterns) / 2.0, 1.0)


# Module-level convenience function
def detect_wisdom(text: str) -> Dict:
    """
    Quick wisdom detection from raw text.

    Args:
        text: Raw conversational text

    Returns:
        Dict with coherence, meta_perspective, insight, etc.
    """
    from dataclasses import dataclass as _dataclass

    @_dataclass
    class _TextOccasion:
        text: str
        chunk_id: str

    occasion = _TextOccasion(text=text, chunk_id='test')

    core = WisdomTextCore()
    result = core.process_text_occasions([occasion], cycle=0)

    return {
        'coherence': result.coherence,
        'meta_perspective_score': result.meta_perspective_score,
        'insight_frequency': result.insight_frequency,
        'reframe_capacity': result.reframe_capacity,
        'paradox_tolerance': result.paradox_tolerance,
        'temporal_integration': result.temporal_integration,
        'dominant_wisdom': result.dominant_wisdom,
        'lure': result.lure
    }


if __name__ == '__main__':
    """Test WISDOM organ with sample conversational text."""

    test_cases = [
        # Meta-commentary
        "Let me step back and look at the bigger picture here. From this vantage point, I notice a systemic pattern.",

        # Insight moment
        "Oh! It just clicked for me. I suddenly see how these pieces come together. This is a breakthrough.",

        # Reframe
        "What if we looked at this differently? Consider it from another angle - maybe it's not a problem but an invitation.",

        # Paradox holding
        "There's a tension here - both/and, not either/or. The complexity is that these contradictions can coexist.",

        # Temporal wisdom
        "Over time, I've noticed this pattern repeating. The cycle unfolds again and again, each time revealing something new.",

        # Collective wisdom
        "This is a universal human experience. Across cultures and throughout history, we all face this ancient question.",

        # Mixed (complex wisdom)
        "Stepping back, I realize this is part of a larger pattern. The paradox is that growth and pain coexist - both/and. Over time, humanity has always navigated this tension. What if we reframe it not as contradiction but as the very process of becoming?",
    ]

    print("=" * 70)
    print("WISDOM ORGAN - Text Core Test")
    print("=" * 70)
    print()

    for idx, text in enumerate(test_cases, 1):
        result = detect_wisdom(text)

        print(f"Test {idx}: \"{text[:60]}...\"")
        print(f"  Coherence: {result['coherence']:.2f}")
        print(f"  Meta-Perspective: {result['meta_perspective_score']:.2f}")
        print(f"  Insight: {result['insight_frequency']:.2f}")
        print(f"  Reframe: {result['reframe_capacity']:.2f}")
        print(f"  Paradox: {result['paradox_tolerance']:.2f}")
        print(f"  Temporal: {result['temporal_integration']:.2f}")
        print(f"  Quality: {result['dominant_wisdom']}")
        print(f"  Lure: {result['lure']:.2f}")
        print()

    print("=" * 70)
    print("✓ WISDOM organ operational")
    print("=" * 70)
