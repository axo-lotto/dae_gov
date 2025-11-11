"""
AUTHENTICITY Organ - Conversational Text Core
Detects genuineness, vulnerability, self-disclosure, and transparency signals.

Philosophy:
- Authenticity is congruence between inner and outer experience
- Vulnerability is courage to be seen without facade
- Self-disclosure is personal sharing with genuine intention
- Transparency is honest acknowledgment of limitations and uncertainty
"""

import re
import time
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field


@dataclass
class AuthenticityPattern:
    """Detected authenticity pattern."""
    pattern_type: str  # 'genuine', 'vulnerable', 'self_disclosure', 'transparent', 'congruent', 'anti_performance'
    strength: float  # Activation strength (0.0-2.0, amplified for deep authenticity)
    chunk_id: str
    position: int
    matched_keywords: List[str]
    confidence: float  # Pattern confidence (0.0-1.0)
    authenticity_quality: str  # 'surface', 'honest', 'vulnerable', 'transparent'
    co_occurring_patterns: List[str] = field(default_factory=list)


@dataclass
class AuthenticityResult:
    """Universal organ output for AUTHENTICITY."""
    coherence: float  # Overall authenticity coherence (0.0-1.0)
    patterns: List[AuthenticityPattern]
    lure: float  # Appetition pull toward deeper authenticity
    processing_time_ms: float

    # Additional AUTHENTICITY-specific metrics
    genuineness_score: float = 0.0  # Lack of facade (0.0-1.0)
    vulnerability_level: float = 0.0  # Courage to be seen (0.0-1.0)
    self_disclosure_depth: float = 0.0  # Personal sharing (0.0-1.0)
    transparency_score: float = 0.0  # Honest limitations (0.0-1.0)
    congruence_level: float = 0.0  # Inner/outer alignment (0.0-1.0)
    dominant_authenticity: Optional[str] = None  # 'surface', 'honest', 'vulnerable', 'transparent'


@dataclass
class AuthenticityConfig:
    """Configuration for AUTHENTICITY organ."""
    genuine_threshold: float = 0.4
    vulnerable_threshold: float = 0.6
    transparent_threshold: float = 0.7

    # Amplification for deep authenticity
    transparent_amplification: float = 2.0
    vulnerable_amplification: float = 1.7
    honest_amplification: float = 1.4


DEFAULT_AUTHENTICITY_CONFIG = AuthenticityConfig()


class AuthenticityTextCore:
    """
    AUTHENTICITY Organ - Detects genuineness and vulnerability in conversational text.

    100% LLM-free, keyword-based detection with authenticity pattern recognition.
    Follows universal organ interface pattern.
    """

    def __init__(self, config: Optional[AuthenticityConfig] = None):
        """Initialize AUTHENTICITY organ with keyword mappings."""
        self.config = config or DEFAULT_AUTHENTICITY_CONFIG

        # GENUINE EXPRESSION: "honestly", "to be real", "truth is"
        self.genuine_keywords = {
            'honestly', 'to be honest', 'truth is', 'truthfully',
            'to be real', 'real talk', 'being real', 'straight up',
            'frankly', 'candidly', 'sincerely', 'genuine', 'genuinely',
            'actually', 'in truth', 'truly'
        }

        # VULNERABILITY: "scared", "risky", "hard to say", "vulnerable"
        self.vulnerable_keywords = {
            'scared', 'afraid', 'nervous', 'anxious', 'worried',
            'risky', 'risk', 'hard to say', 'difficult to admit',
            'vulnerable', 'exposed', 'raw', 'open', 'unprotected',
            'tender', 'fragile', 'delicate', 'shaky', 'uncertain'
        }

        # SELF-DISCLOSURE: "I feel", "I notice", "for me", "my experience"
        self.self_disclosure_keywords = {
            'i feel', 'i notice', 'i sense', 'i experience',
            'for me', 'in my experience', 'my experience',
            'i\'m feeling', 'i\'m noticing', 'what i feel',
            'my sense', 'my impression', 'my truth', 'personally'
        }

        # TRANSPARENCY: "I don't know", "unsure", "confused", "unclear"
        self.transparency_keywords = {
            'i don\'t know', 'not sure', 'unsure', 'uncertain',
            'confused', 'unclear', 'don\'t understand', 'struggling',
            'haven\'t figured out', 'still learning', 'questioning',
            'don\'t have answers', 'admitting', 'acknowledge',
            'can\'t pretend', 'won\'t pretend'
        }

        # CONGRUENCE: "aligned", "congruent", "true to", "integrity"
        self.congruence_keywords = {
            'aligned', 'congruent', 'true to myself', 'integrity',
            'authentic', 'real self', 'whole self', 'integrated',
            'consistent', 'coherent', 'unified', 'in sync'
        }

        # ANTI-PERFORMANCE: "not trying to", "no agenda", "just being"
        self.anti_performance_keywords = {
            'not trying to', 'no agenda', 'just being', 'not performing',
            'no act', 'not pretending', 'unfiltered', 'unedited',
            'not polished', 'messy', 'imperfect', 'flawed'
        }

        # Compile regex patterns
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile keyword sets into regex patterns."""
        self.genuine_pattern = self._make_pattern(self.genuine_keywords)
        self.vulnerable_pattern = self._make_pattern(self.vulnerable_keywords)
        self.self_disclosure_pattern = self._make_pattern(self.self_disclosure_keywords)
        self.transparency_pattern = self._make_pattern(self.transparency_keywords)
        self.congruence_pattern = self._make_pattern(self.congruence_keywords)
        self.anti_performance_pattern = self._make_pattern(self.anti_performance_keywords)

    def _make_pattern(self, keywords: Set[str]) -> re.Pattern:
        """Create case-insensitive regex pattern from keyword set."""
        escaped = [re.escape(kw) for kw in sorted(keywords, key=len, reverse=True)]
        return re.compile(r'\b(' + '|'.join(escaped) + r')', re.IGNORECASE)

    def process_text_occasions(
        self,
        occasions: List,  # List[TextOccasion]
        cycle: int
    ) -> AuthenticityResult:
        """
        Process text occasions to detect authenticity patterns.

        Universal organ interface: occasions → Result

        Args:
            occasions: List of TextOccasion entities (actual occasions)
            cycle: Current convergence cycle (unused for now, future V0 integration)

        Returns:
            AuthenticityResult with coherence, patterns, lure, metrics
        """
        start_time = time.time()
        patterns: List[AuthenticityPattern] = []

        # Process each occasion (text chunk)
        for idx, occasion in enumerate(occasions):
            text = occasion.text.lower()
            chunk_id = occasion.chunk_id

            # Detect all pattern types
            patterns.extend(self._detect_genuine(text, chunk_id, idx))
            patterns.extend(self._detect_vulnerable(text, chunk_id, idx))
            patterns.extend(self._detect_self_disclosure(text, chunk_id, idx))
            patterns.extend(self._detect_transparency(text, chunk_id, idx))
            patterns.extend(self._detect_congruence(text, chunk_id, idx))
            patterns.extend(self._detect_anti_performance(text, chunk_id, idx))

        # Compute aggregate metrics
        result = self._compute_result(patterns, start_time)

        return result

    def _detect_genuine(self, text: str, chunk_id: str, position: int) -> List[AuthenticityPattern]:
        """Detect genuine expression patterns (honest communication)."""
        matches = self.genuine_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.6, 1.3)
        confidence = 0.85

        return [AuthenticityPattern(
            pattern_type='genuine',
            strength=strength * self.config.honest_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            authenticity_quality='honest'
        )]

    def _detect_vulnerable(self, text: str, chunk_id: str, position: int) -> List[AuthenticityPattern]:
        """Detect vulnerability patterns (courage to be seen)."""
        matches = self.vulnerable_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.8, 1.6)
        confidence = 0.9

        return [AuthenticityPattern(
            pattern_type='vulnerable',
            strength=strength * self.config.vulnerable_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            authenticity_quality='vulnerable'
        )]

    def _detect_self_disclosure(self, text: str, chunk_id: str, position: int) -> List[AuthenticityPattern]:
        """Detect self-disclosure patterns (personal sharing)."""
        matches = self.self_disclosure_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.7, 1.4)
        confidence = 0.8

        return [AuthenticityPattern(
            pattern_type='self_disclosure',
            strength=strength * self.config.honest_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            authenticity_quality='honest'
        )]

    def _detect_transparency(self, text: str, chunk_id: str, position: int) -> List[AuthenticityPattern]:
        """Detect transparency patterns (honest limitations)."""
        matches = self.transparency_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.9, 1.8)
        confidence = 0.95

        return [AuthenticityPattern(
            pattern_type='transparent',
            strength=strength * self.config.transparent_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            authenticity_quality='transparent'
        )]

    def _detect_congruence(self, text: str, chunk_id: str, position: int) -> List[AuthenticityPattern]:
        """Detect congruence patterns (inner/outer alignment)."""
        matches = self.congruence_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.75, 1.5)
        confidence = 0.85

        return [AuthenticityPattern(
            pattern_type='congruent',
            strength=strength * self.config.honest_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            authenticity_quality='honest'
        )]

    def _detect_anti_performance(self, text: str, chunk_id: str, position: int) -> List[AuthenticityPattern]:
        """Detect anti-performance patterns (rejecting facade)."""
        matches = self.anti_performance_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 1.0, 1.7)
        confidence = 0.9

        return [AuthenticityPattern(
            pattern_type='anti_performance',
            strength=strength * self.config.vulnerable_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            authenticity_quality='vulnerable'
        )]

    def _compute_result(self, patterns: List[AuthenticityPattern], start_time: float) -> AuthenticityResult:
        """Compute aggregate AuthenticityResult from detected patterns."""
        processing_time_ms = (time.time() - start_time) * 1000

        if not patterns:
            return AuthenticityResult(
                coherence=0.0,
                patterns=[],
                lure=0.0,
                processing_time_ms=processing_time_ms,
                genuineness_score=0.0,
                vulnerability_level=0.0,
                self_disclosure_depth=0.0,
                transparency_score=0.0,
                congruence_level=0.0,
                dominant_authenticity=None
            )

        # Compute coherence (average confidence weighted by strength)
        total_weight = sum(p.strength * p.confidence for p in patterns)
        total_strength = sum(p.strength for p in patterns)
        coherence = min(total_weight / max(total_strength, 0.1), 1.0)

        # Compute lure (pull toward deeper authenticity)
        quality_scores = {
            'surface': 0.2,
            'honest': 0.5,
            'vulnerable': 0.8,
            'transparent': 1.0
        }
        avg_quality = sum(quality_scores[p.authenticity_quality] for p in patterns) / len(patterns)
        lure = min(avg_quality * 1.3, 1.0)

        # Compute specific metrics
        genuineness_score = self._compute_genuineness(patterns)
        vulnerability_level = self._compute_vulnerability(patterns)
        self_disclosure_depth = self._compute_self_disclosure(patterns)
        transparency_score = self._compute_transparency(patterns)
        congruence_level = self._compute_congruence(patterns)

        # Dominant authenticity quality
        quality_counts = {}
        for p in patterns:
            quality_counts[p.authenticity_quality] = quality_counts.get(p.authenticity_quality, 0) + p.strength
        dominant_authenticity = max(quality_counts, key=quality_counts.get) if quality_counts else None

        return AuthenticityResult(
            coherence=coherence,
            patterns=patterns,
            lure=lure,
            processing_time_ms=processing_time_ms,
            genuineness_score=genuineness_score,
            vulnerability_level=vulnerability_level,
            self_disclosure_depth=self_disclosure_depth,
            transparency_score=transparency_score,
            congruence_level=congruence_level,
            dominant_authenticity=dominant_authenticity
        )

    def _compute_genuineness(self, patterns: List[AuthenticityPattern]) -> float:
        """Compute genuineness score from genuine + congruent patterns."""
        genuine_types = {'genuine', 'congruent'}
        genuine_patterns = [p for p in patterns if p.pattern_type in genuine_types]
        if not genuine_patterns:
            return 0.0
        return min(sum(p.strength for p in genuine_patterns) / 2.5, 1.0)

    def _compute_vulnerability(self, patterns: List[AuthenticityPattern]) -> float:
        """Compute vulnerability level from vulnerable + anti_performance patterns."""
        vulnerable_types = {'vulnerable', 'anti_performance'}
        vulnerable_patterns = [p for p in patterns if p.pattern_type in vulnerable_types]
        if not vulnerable_patterns:
            return 0.0
        return min(sum(p.strength for p in vulnerable_patterns) / 3.0, 1.0)

    def _compute_self_disclosure(self, patterns: List[AuthenticityPattern]) -> float:
        """Compute self-disclosure depth from self_disclosure patterns."""
        disclosure_patterns = [p for p in patterns if p.pattern_type == 'self_disclosure']
        if not disclosure_patterns:
            return 0.0
        return min(sum(p.strength for p in disclosure_patterns) / 2.0, 1.0)

    def _compute_transparency(self, patterns: List[AuthenticityPattern]) -> float:
        """Compute transparency score from transparent patterns."""
        transparent_patterns = [p for p in patterns if p.pattern_type == 'transparent']
        if not transparent_patterns:
            return 0.0
        return min(sum(p.strength for p in transparent_patterns) / 2.0, 1.0)

    def _compute_congruence(self, patterns: List[AuthenticityPattern]) -> float:
        """Compute congruence level from all patterns (overall alignment)."""
        if not patterns:
            return 0.0
        # Congruence is strength of alignment across all authenticity signals
        total_strength = sum(p.strength for p in patterns)
        return min(total_strength / 4.0, 1.0)


# Module-level convenience function
def detect_authenticity(text: str) -> Dict:
    """
    Quick authenticity detection from raw text.

    Args:
        text: Raw conversational text

    Returns:
        Dict with coherence, genuineness, vulnerability, etc.
    """
    from dataclasses import dataclass as _dataclass

    @_dataclass
    class _TextOccasion:
        text: str
        chunk_id: str

    occasion = _TextOccasion(text=text, chunk_id='test')

    core = AuthenticityTextCore()
    result = core.process_text_occasions([occasion], cycle=0)

    return {
        'coherence': result.coherence,
        'genuineness_score': result.genuineness_score,
        'vulnerability_level': result.vulnerability_level,
        'self_disclosure_depth': result.self_disclosure_depth,
        'transparency_score': result.transparency_score,
        'congruence_level': result.congruence_level,
        'dominant_authenticity': result.dominant_authenticity,
        'lure': result.lure
    }


if __name__ == '__main__':
    """Test AUTHENTICITY organ with sample conversational text."""

    test_cases = [
        # Surface honest
        "Honestly, I think that's a good idea. To be real, it makes sense.",

        # Vulnerable sharing
        "I'm scared to say this, but it feels risky. I feel vulnerable admitting this to you.",

        # Self-disclosure
        "I feel uncertain about this. For me, my experience has been that I notice discomfort when things aren't clear.",

        # Transparent limitations
        "I don't know the answer. I'm unsure and confused. I haven't figured this out yet and I won't pretend I have.",

        # Congruent authenticity
        "I feel aligned with my truth here. This is congruent with my authentic self - I'm being my real, whole self.",

        # Deep authenticity (mixed)
        "Honestly, I'm scared to say this, but I don't know what I'm doing. I feel vulnerable admitting my confusion. For me, not pretending feels more aligned with my integrity, even though it's risky.",
    ]

    print("=" * 70)
    print("AUTHENTICITY ORGAN - Text Core Test")
    print("=" * 70)
    print()

    for idx, text in enumerate(test_cases, 1):
        result = detect_authenticity(text)

        print(f"Test {idx}: \"{text[:60]}...\"")
        print(f"  Coherence: {result['coherence']:.2f}")
        print(f"  Genuineness: {result['genuineness_score']:.2f}")
        print(f"  Vulnerability: {result['vulnerability_level']:.2f}")
        print(f"  Self-disclosure: {result['self_disclosure_depth']:.2f}")
        print(f"  Transparency: {result['transparency_score']:.2f}")
        print(f"  Congruence: {result['congruence_level']:.2f}")
        print(f"  Dominant: {result['dominant_authenticity']}")
        print(f"  Lure: {result['lure']:.2f}")
        print()

    print("=" * 70)
    print("✓ AUTHENTICITY organ operational")
    print("=" * 70)
