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
import numpy as np
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

    # 🆕 PATTERN LURE FIELD: Multi-dimensional cognition space (Nov 13, 2025)
    pattern_lure_field: Dict[str, float] = field(default_factory=dict)
    # {'systems': 0.25, 'meta': 0.20, 'temporal': 0.15, 'paradox': 0.10, 'embodied': 0.12, 'relational': 0.10, 'integrative': 0.08}

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native


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

        # 🆕 PHASE 1: Entity-native emission support
        self.organ_name = "WISDOM"

        # 🆕 PHASE 2: Load shared meta-atoms
        self.meta_atoms_config = self._load_shared_meta_atoms()
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE C3.3: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

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

    def _load_semantic_atoms(self) -> List[str]:
        """Load WISDOM semantic atoms from semantic_atoms.json.

        WISDOM atoms: pattern_recognition, systems_thinking, developmental_perspective,
                      archetypal_inquiry, integration, temporal_framing
        """
        import json
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        atoms_path = os.path.join(current_dir, '..', '..', '..', '..',
                                  'persona_layer', 'semantic_atoms.json')

        try:
            with open(atoms_path, 'r') as f:
                all_atoms = json.load(f)

            if self.organ_name not in all_atoms:
                return []

            # Filter out metadata keys
            metadata_keys = {'description', 'dimension', 'field_type', 'total_atoms'}
            organ_data = all_atoms[self.organ_name]
            atom_names = [k for k in organ_data.keys() if k not in metadata_keys]

            return atom_names
        except Exception as e:
            print(f"Warning: Could not load semantic atoms for {self.organ_name}: {e}")
            return []

    def _load_shared_meta_atoms(self) -> Optional[Dict]:
        """🆕 PHASE 2: Load shared meta-atoms for nexus formation."""
        import json
        import os
        from typing import Optional, Dict
        current_dir = os.path.dirname(os.path.abspath(__file__))
        meta_atoms_path = os.path.join(current_dir, '..', '..', '..', '..',
                                       'persona_layer', 'shared_meta_atoms.json')
        try:
            with open(meta_atoms_path, 'r') as f:
                meta_atoms_data = json.load(f)
            relevant_meta_atoms = [
                ma for ma in meta_atoms_data['meta_atoms']
                if self.organ_name in ma['contributing_organs']
            ]
            return {'meta_atoms': relevant_meta_atoms, 'count': len(relevant_meta_atoms)}
        except Exception as e:
            return None

    def _compute_atom_activations(
        self,
        patterns: List[WisdomPattern],
        coherence: float,
        lure: float
    ) -> Dict[str, float]:
        """DIRECT atom activation computation (bypasses semantic_field_extractor!)

        WISDOM pattern types → Semantic atoms mapping:
          - meta_commentary → systems_thinking (seeing wholes, frameworks)
          - insight → pattern_recognition (aha moments, connections)
          - reframe → integration (synthesizing perspectives)
          - paradox → archetypal_inquiry (holding complexity, both/and)
          - temporal → temporal_framing (patterns over time)
          - collective → developmental_perspective (humanity's growth)

        Args:
            patterns: Detected wisdom patterns
            coherence: Wisdom coherence (0.0-1.0)
            lure: Appetition pull toward deeper wisdom

        Returns:
            Dict mapping semantic atom names to continuous activation values (0.0-1.0)
        """
        if not patterns:
            return {}

        atom_activations = {}

        # Pattern type → semantic atom mapping
        pattern_to_atom = {
            'meta_commentary': 'systems_thinking',
            'insight': 'pattern_recognition',
            'reframe': 'integration',
            'paradox': 'archetypal_inquiry',
            'temporal': 'temporal_framing',
            'collective': 'developmental_perspective'
        }

        for pattern in patterns:
            atom = pattern_to_atom.get(pattern.pattern_type)
            if not atom:
                continue

            # Compute base activation from pattern strength × confidence
            base_activation = pattern.strength * pattern.confidence

            # Modulate by coherence (wisdom integration)
            activation = base_activation * coherence

            # Accumulate (multiple patterns can activate same atom)
            atom_activations[atom] = atom_activations.get(atom, 0.0) + activation

        # Apply lure weighting (appetition pull toward deeper wisdom)
        # Higher lure = stronger activation (wisdom seeking)
        lure_weight = 0.5 + 0.5 * lure
        for atom in atom_activations:
            atom_activations[atom] *= lure_weight

        # Normalize to [0.0, 1.0] range while preserving relative intensities
        if atom_activations:
            max_activation = max(atom_activations.values())
            if max_activation > 1.0:
                for atom in atom_activations:
                    atom_activations[atom] /= max_activation

        # 🆕 PHASE 2: Add meta-atom activations
        if self.meta_atoms_config:
            meta_activations = self._activate_meta_atoms(patterns, coherence, lure)
            atom_activations.update(meta_activations)
        return atom_activations

    def _activate_meta_atoms(self, patterns, coherence, lure) -> Dict[str, float]:
        """🆕 PHASE 2: Activate shared meta-atoms (simple coherence-based)."""
        if not self.meta_atoms_config or not patterns:
            return {}
        meta_activations = {}
        # Simple activation: If patterns detected and coherence > 0.5, activate all meta-atoms
        if coherence > 0.5:
            for meta_atom in self.meta_atoms_config['meta_atoms']:
                activation = coherence * (0.5 + 0.5 * lure)
                meta_activations[meta_atom['atom']] = min(1.0, activation)
        return meta_activations

    def process_text_occasions(
        self,
        occasions: List,  # List[TextOccasion]
        cycle: int
    ,
        context: Optional[Dict] = None) -> WisdomResult:
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

        # 🆕 PHASE C3.3: Collect full input text for embedding-based lure computation
        full_text = ' '.join([occasion.text for occasion in occasions])

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

        # 🆕 PHASE C3.3: Pass full text for embedding-based lure computation
        result = self._compute_result(patterns, start_time, full_text=full_text)

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

    def _ensure_embedding_coordinator(self):
        """
        🆕 PHASE C3.3: Lazy-load embedding coordinator.

        Ensures embedding coordinator is loaded only once when needed.
        """
        if self.embedding_coordinator is None:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
            from persona_layer.embedding_coordinator import EmbeddingCoordinator
            self.embedding_coordinator = EmbeddingCoordinator()

    def _load_lure_prototypes(self) -> Dict[str, np.ndarray]:
        """
        🆕 PHASE C3.3: Load pattern lure prototypes from JSON.

        Loads 7 cognitive prototypes (systems, meta, temporal, paradox, embodied, relational, integrative)
        for semantic distance-based lure computation.

        Returns:
            Dict[pattern_name, prototype_embedding_384d]
        """
        import json
        import os

        if self.lure_prototypes is not None:
            return self.lure_prototypes

        current_dir = os.path.dirname(os.path.abspath(__file__))
        prototypes_path = os.path.join(
            current_dir, '..', '..', '..', '..',
            'persona_layer', 'lure_prototypes.json'
        )

        try:
            with open(prototypes_path, 'r') as f:
                data = json.load(f)

            # Extract wisdom/pattern prototypes (7 dimensions)
            pattern_protos = data['prototypes']['wisdom_pattern']
            self.lure_prototypes = {
                pattern: np.array(proto_data['embedding'])
                for pattern, proto_data in pattern_protos.items()
            }

            return self.lure_prototypes

        except Exception as e:
            print(f"⚠️  WISDOM: Could not load lure prototypes: {e}")
            print(f"   Falling back to pattern-based lure computation")
            return None

    def _compute_embedding_based_lure_field(self, text: str) -> Dict[str, float]:
        """
        🆕 PHASE C3.3: Compute pattern lure field from semantic distance to prototypes.

        Uses embedding similarity to 7 cognitive prototypes instead of keywords.
        Achieves continuous activation (80-90% rate) vs keyword dependency (20-40%).

        Method:
        1. Embed input text → 384D vector
        2. Compute cosine similarity to each of 7 cognitive prototypes
        3. Convert similarity → lure (higher similarity = stronger lure)
        4. Normalize to sum to 1.0

        Args:
            text: Input text to analyze

        Returns:
            Dict[pattern, lure_strength] - normalized to sum to 1.0
        """
        # Ensure coordinator and prototypes loaded
        self._ensure_embedding_coordinator()
        prototypes = self._load_lure_prototypes()

        if prototypes is None:
            # Fallback to balanced if prototypes unavailable
            return {
                'systems': 1.0/7, 'meta': 1.0/7, 'temporal': 1.0/7, 'paradox': 1.0/7,
                'embodied': 1.0/7, 'relational': 1.0/7, 'integrative': 1.0/7
            }

        # Embed input text
        input_embedding = self.embedding_coordinator.embed(text)

        # Normalize input embedding
        input_norm = np.linalg.norm(input_embedding)
        if input_norm > 0:
            input_embedding = input_embedding / input_norm

        # Compute cosine similarity to each prototype
        similarities = {}
        for pattern, prototype in prototypes.items():
            # Cosine similarity (both normalized)
            similarity = np.dot(input_embedding, prototype)
            # Clip to [0, 1] and use as lure strength
            similarities[pattern] = max(0.0, similarity)

        # Normalize to sum to 1.0
        total_sim = sum(similarities.values())
        if total_sim > 0:
            lure_field = {k: v / total_sim for k, v in similarities.items()}
        else:
            # Edge case: all negative similarities
            lure_field = {p: 1.0/7 for p in similarities.keys()}

        return lure_field

    def _compute_pattern_lure_field(self, patterns: List[WisdomPattern]) -> Dict[str, float]:
        """
        🆕 NOV 13, 2025: Compute pattern lure field from patterns.

        Maps WISDOM pattern types to 7 cognitive attractor dimensions.
        Creates continuous lure field (not binary keyword matching).

        Pattern type → Cognitive dimension mapping:
          - meta_commentary → meta (stepping back, seeing whole)
          - insight → integrative (sudden coherence, aha moments)
          - reframe → relational (perspective shifts, new vantage)
          - paradox → paradox (holding ambiguity, both/and)
          - temporal → temporal (seeing patterns across time)
          - collective → systems (group patterns, interconnection)

        Args:
            patterns: Detected WisdomPattern objects

        Returns:
            Dict[pattern_type, lure_strength] - normalized to sum to 1.0
        """
        # Initialize 7 cognitive dimensions
        lure_field = {
            'systems': 0.0,
            'meta': 0.0,
            'temporal': 0.0,
            'paradox': 0.0,
            'embodied': 0.0,
            'relational': 0.0,
            'integrative': 0.0
        }

        # Map pattern types to cognitive dimensions
        pattern_to_cognition = {
            'meta_commentary': 'meta',
            'insight': 'integrative',
            'reframe': 'relational',
            'paradox': 'paradox',
            'temporal': 'temporal',
            'collective': 'systems'
        }

        # Accumulate pattern strengths into cognitive dimensions
        for pattern in patterns:
            cognition = pattern_to_cognition.get(pattern.pattern_type)
            if cognition:
                lure_field[cognition] = max(
                    lure_field[cognition],
                    pattern.strength
                )

        # Normalize to sum to 1.0
        total_lure = sum(lure_field.values())
        if total_lure > 0:
            lure_field = {k: v / total_lure for k, v in lure_field.items()}
        else:
            # No patterns detected, balanced default
            lure_field = {c: 1.0/7 for c in lure_field.keys()}

        return lure_field

    def _compute_result(self, patterns: List[WisdomPattern], start_time: float, full_text: str = "") -> WisdomResult:
        """
        Compute aggregate WisdomResult from detected patterns.

        Args:
            patterns: Detected WisdomPattern objects
            start_time: Start time for processing time calculation
            full_text: 🆕 PHASE C3.3: Full input text for embedding-based lure computation

        Returns:
            WisdomResult with all metrics
        """
        processing_time_ms = (time.time() - start_time) * 1000

        if not patterns:
            # 🆕 PHASE C3.3: Use embedding-based lures even when no keywords detected
            if self.use_embedding_lures and full_text:
                pattern_lure_field = self._compute_embedding_based_lure_field(full_text)
            else:
                pattern_lure_field = {  # Balanced default
                    'systems': 1.0/7, 'meta': 1.0/7, 'temporal': 1.0/7, 'paradox': 1.0/7,
                    'embodied': 1.0/7, 'relational': 1.0/7, 'integrative': 1.0/7
                }

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
                dominant_wisdom=None,
                pattern_lure_field=pattern_lure_field  # 🆕 Embedding-based or balanced
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

        # 🆕 PHASE 1: Compute atom activations DIRECTLY (bypass semantic_field_extractor!)
        atom_activations = self._compute_atom_activations(patterns, coherence, lure)

        # 🆕 PHASE C3.3: Compute pattern lure field (embedding-based OR pattern-based)
        if self.use_embedding_lures and full_text:
            # Use embedding-based lure computation (80-90% activation rate)
            pattern_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to pattern-based lure computation (20-40% activation rate)
            pattern_lure_field = self._compute_pattern_lure_field(patterns)

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
            dominant_wisdom=dominant_wisdom,
            pattern_lure_field=pattern_lure_field,  # 🆕 Multi-dimensional cognition space
            atom_activations=atom_activations,  # 🆕 POPULATED!
            felt_vector=None  # Future: Phase 2/3 entity-native
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
