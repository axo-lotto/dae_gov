"""
LISTENING Organ - Conversational Text Core
Detects active listening signals, attention markers, and presence indicators.

Philosophy:
- Listening is felt through acknowledgment and reflection
- Attention is presence made visible
- Following is relational prehension
- Tracking is coherence through time
"""

import re
import time
from typing import List, Dict, Optional, Set
import numpy as np
from dataclasses import dataclass, field


@dataclass
class ListeningPattern:
    """Detected active listening pattern."""
    pattern_type: str  # 'acknowledgment', 'reflection', 'presence_marker', 'tracking', 'understanding'
    strength: float  # Activation strength (0.0-2.0, amplified for strong listening)
    chunk_id: str
    position: int
    matched_keywords: List[str]
    confidence: float  # Pattern confidence (0.0-1.0)
    listening_quality: str  # 'surface', 'engaged', 'deep', 'transformative'
    co_occurring_patterns: List[str] = field(default_factory=list)


@dataclass
class ListeningResult:
    """Universal organ output for LISTENING."""
    coherence: float  # Overall listening coherence (0.0-1.0)
    patterns: List[ListeningPattern]
    lure: float  # Appetition pull toward deeper listening
    processing_time_ms: float

    # Additional LISTENING-specific metrics
    attention_score: float = 0.0  # Overall attention level (0.0-1.0)
    presence_level: float = 0.0  # Grounded here-now presence (0.0-1.0)
    reflection_depth: float = 0.0  # How deeply therapist reflects (0.0-1.0)
    tracking_continuity: float = 0.0  # Following thread over time (0.0-1.0)
    dominant_quality: Optional[str] = None  # 'surface', 'engaged', 'deep', 'transformative'

    # 🆕 INQUIRY LURE FIELD: Multi-dimensional listening space (Nov 13, 2025)
    inquiry_lure_field: Dict[str, float] = field(default_factory=dict)
    # {'temporal_inquiry': 0.15, 'core_exploration': 0.20, 'witnessing_presence': 0.15, ...}

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native


@dataclass
class ListeningConfig:
    """Configuration for LISTENING organ."""
    acknowledgment_threshold: float = 0.3
    reflection_threshold: float = 0.4
    presence_threshold: float = 0.5
    tracking_threshold: float = 0.6
    deep_listening_threshold: float = 0.7

    # Amplification for transformative listening
    transformative_amplification: float = 1.8
    deep_amplification: float = 1.4
    engaged_amplification: float = 1.1


DEFAULT_LISTENING_CONFIG = ListeningConfig()


class ListeningTextCore:
    """
    LISTENING Organ - Detects active listening signals in conversational text.

    100% LLM-free, keyword-based detection with pattern strength scoring.
    Follows universal organ interface pattern.
    """

    def __init__(self, config: Optional[ListeningConfig] = None):
        """Initialize LISTENING organ with keyword mappings."""
        self.config = config or DEFAULT_LISTENING_CONFIG
        self.organ_name = "LISTENING"

        # 🆕 PHASE 2: Load shared meta-atoms
        self.meta_atoms_config = self._load_shared_meta_atoms()

        # Load semantic atoms from semantic_atoms.json for emission
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE C3.5: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

        # ACKNOWLEDGMENT: Simple recognition ("I hear you", "yes", "mm-hmm")
        self.acknowledgment_keywords = {
            'hear', 'listening', 'yes', 'okay', 'right', 'mm-hmm', 'uh-huh',
            'got it', 'i see', 'understood', 'following', 'with you',
            'tracking', 'hearing', 'receiving', 'getting', 'catching',
            'acknowledg', 'recogniz', 'noting', 'registering'
        }

        # REFLECTION: Mirroring back ("you're saying", "sounds like", "feeling")
        self.reflection_keywords = {
            'you\'re saying', 'sounds like', 'seems like', 'feeling',
            'you mentioned', 'you shared', 'you described', 'you expressed',
            'what i\'m hearing', 'what stands out', 'what you\'re',
            'paraphras', 'reflect', 'mirror', 'resonate', 'echo',
            'summariz', 'sense that', 'picking up', 'noticing'
        }

        # PRESENCE MARKERS: Here-now attention ("right now", "in this moment", "present")
        self.presence_keywords = {
            'right now', 'in this moment', 'present', 'here', 'now',
            'currently', 'at this time', 'as we speak', 'this instant',
            'with me', 'together', 'connected', 'grounded', 'settled',
            'aware', 'conscious', 'attuned', 'aligned', 'centered'
        }

        # TRACKING: Following thread over time ("earlier you said", "coming back to", "thread")
        self.tracking_keywords = {
            'earlier', 'before', 'you said', 'you mentioned', 'thread',
            'coming back', 'returning to', 'circling back', 'connecting',
            'pattern', 'theme', 'recurring', 'consistent', 'continuing',
            'following up', 'thread through', 'weaving', 'linking',
            'remember when', 'last time', 'previously'
        }

        # UNDERSTANDING: Deep comprehension ("understand", "appreciate", "grasp", "see")
        self.understanding_keywords = {
            'understand', 'comprehend', 'grasp', 'appreciate', 'recognize',
            'realize', 'perceive', 'discern', 'see why', 'make sense',
            'get it', 'clear', 'evident', 'apparent', 'obvious',
            'insight', 'awareness', 'conscious', 'know', 'cognizant'
        }

        # TRANSFORMATIVE LISTENING: Deepest level (rare, powerful)
        self.transformative_keywords = {
            'profound', 'deeply moved', 'transformative', 'shift',
            'breakthrough', 'revelation', 'epiphany', 'illuminat',
            'paradigm', 'fundamental', 'core', 'essence', 'truth',
            'witness', 'honor', 'sacred', 'profound'
        }

        # Compile regex patterns for efficient matching
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile keyword sets into regex patterns."""
        self.acknowledgment_pattern = self._make_pattern(self.acknowledgment_keywords)
        self.reflection_pattern = self._make_pattern(self.reflection_keywords)
        self.presence_pattern = self._make_pattern(self.presence_keywords)
        self.tracking_pattern = self._make_pattern(self.tracking_keywords)
        self.understanding_pattern = self._make_pattern(self.understanding_keywords)
        self.transformative_pattern = self._make_pattern(self.transformative_keywords)

    def _make_pattern(self, keywords: Set[str]) -> re.Pattern:
        """Create case-insensitive regex pattern from keyword set."""
        # Escape special regex characters, sort by length (longest first)
        escaped = [re.escape(kw) for kw in sorted(keywords, key=len, reverse=True)]
        return re.compile(r'\b(' + '|'.join(escaped) + r')', re.IGNORECASE)

    def _load_semantic_atoms(self) -> List[str]:
        """
        Load LISTENING semantic atoms from semantic_atoms.json.

        Returns:
            List of atom names (e.g., ['core_exploration', 'ground_truth_hunger', ...])
        """
        import json
        import os

        # Get path to semantic_atoms.json (relative to this file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        atoms_path = os.path.join(current_dir, '..', '..', '..', '..',
                                  'persona_layer', 'semantic_atoms.json')

        try:
            with open(atoms_path, 'r') as f:
                all_atoms = json.load(f)

            if self.organ_name not in all_atoms:
                return []

            # Extract atom names (skip metadata keys)
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
        patterns: List[ListeningPattern],
        coherence: float,
        lure: float
    ) -> Dict[str, float]:
        """
        DIRECT atom activation computation (bypasses semantic_field_extractor!)

        Maps LISTENING patterns to semantic atoms using keyword matching.

        Pattern types → Semantic atoms mapping:
          - acknowledgment → core_exploration (surface listening)
          - reflection → deepening_inquiry (mirroring back)
          - presence_marker → temporal_inquiry (here-now attention)
          - tracking → relational_inquiry (thread continuity)
          - understanding → ground_truth_hunger (comprehension)
          - transformative → open_ended (deepest level)

        Args:
            patterns: Detected ListeningPattern objects
            coherence: Overall listening coherence (0.0-1.0)
            lure: Appetition pull (0.0-1.0)

        Returns:
            Dict[atom_name, activation_strength] - continuous felt values
        """
        if not patterns:
            return {}

        atom_activations = {}

        # Pattern type → semantic atom mapping
        pattern_to_atom = {
            'acknowledgment': 'core_exploration',
            'reflection': 'deepening_inquiry',
            'presence_marker': 'temporal_inquiry',
            'tracking': 'relational_inquiry',
            'understanding': 'ground_truth_hunger',
            'transformative': 'open_ended'
        }

        for pattern in patterns:
            # Get target atom for this pattern type
            atom = pattern_to_atom.get(pattern.pattern_type)
            if not atom:
                continue

            # Base activation: pattern strength × pattern confidence
            base_activation = pattern.strength * pattern.confidence

            # Modulate by coherence (organ-level felt quality)
            activation = base_activation * coherence

            # Accumulate activations (multiple patterns can contribute to same atom)
            atom_activations[atom] = atom_activations.get(atom, 0.0) + activation

        # Apply lure weighting (appetition pull modulates all activations)
        # High lure (0.8-1.0) = pull toward deeper listening
        # Low lure (0.2-0.4) = minimal pull
        lure_weight = 0.5 + 0.5 * lure
        for atom in atom_activations:
            atom_activations[atom] *= lure_weight

        # Normalize to [0.0, 1.0] range (preserve relative intensities)
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

    def _ensure_embedding_coordinator(self):
        """
        🆕 PHASE C3.5: Lazy-load embedding coordinator.

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
        🆕 PHASE C3.5: Load inquiry lure prototypes from JSON.

        Loads 7 inquiry prototypes (temporal_inquiry, core_exploration, etc.)
        for semantic distance-based lure computation.

        Returns:
            Dict[dimension_name, prototype_embedding_384d]
        """
        import json
        import os

        if self.lure_prototypes is not None:
            return self.lure_prototypes

        current_dir = os.path.dirname(os.path.abspath(__file__))
        prototypes_path = os.path.join(
            current_dir, '..', '..', '..', '..',
            'persona_layer', 'config', 'lures', 'lure_prototypes.json'
        )

        try:
            with open(prototypes_path, 'r') as f:
                data = json.load(f)

            # Extract inquiry prototypes (7 dimensions)
            inquiry_protos = data['prototypes']['listening_inquiry']
            self.lure_prototypes = {
                dimension: np.array(proto_data['embedding'])
                for dimension, proto_data in inquiry_protos.items()
            }

            return self.lure_prototypes

        except Exception as e:
            print(f"⚠️  LISTENING: Could not load lure prototypes: {e}")
            print(f"   Falling back to pattern-based lure computation")
            return None

    def _compute_embedding_based_lure_field(self, text: str) -> Dict[str, float]:
        """
        🆕 PHASE C3.5: Compute inquiry lure field from semantic distance to prototypes.

        Uses embedding similarity to 7 inquiry prototypes instead of keywords.
        Achieves continuous activation (80-90% rate) vs keyword dependency (20-40%).

        Method:
        1. Embed input text → 384D vector
        2. Compute cosine similarity to each of 7 inquiry prototypes
        3. Convert similarity → lure (higher similarity = stronger lure)
        4. Normalize to sum to 1.0

        Args:
            text: Input text to analyze

        Returns:
            Dict[dimension, lure_strength] - normalized to sum to 1.0
        """
        # Ensure coordinator and prototypes loaded
        self._ensure_embedding_coordinator()
        prototypes = self._load_lure_prototypes()

        if prototypes is None:
            # Fallback to balanced if prototypes unavailable
            return {
                'temporal_inquiry': 1.0/7, 'core_exploration': 1.0/7,
                'witnessing_presence': 1.0/7, 'pattern_mapping': 1.0/7,
                'silence_holding': 1.0/7, 'clarifying_inquiry': 1.0/7,
                'tracking_continuity': 1.0/7
            }

        # Embed input text
        input_embedding = self.embedding_coordinator.embed(text)

        # Normalize input embedding
        input_norm = np.linalg.norm(input_embedding)
        if input_norm > 0:
            input_embedding = input_embedding / input_norm

        # Compute cosine similarity to each prototype
        similarities = {}
        for dimension, prototype in prototypes.items():
            # Cosine similarity (both normalized)
            similarity = np.dot(input_embedding, prototype)
            # Clip to [0, 1] and use as lure strength
            similarities[dimension] = max(0.0, similarity)

        # Normalize to sum to 1.0
        total_sim = sum(similarities.values())
        if total_sim > 0:
            lure_field = {k: v / total_sim for k, v in similarities.items()}
        else:
            # Edge case: all negative similarities
            lure_field = {d: 1.0/7 for d in similarities.keys()}

        return lure_field

    def process_text_occasions(
        self,
        occasions: List,  # List[TextOccasion] - entity-native prehension
        cycle: int
    ,
        context: Optional[Dict] = None) -> ListeningResult:
        """
        Process text occasions to detect listening patterns.

        Universal organ interface: occasions → Result

        Args:
            occasions: List of TextOccasion entities (actual occasions)
            cycle: Current convergence cycle (unused for now, future V0 integration)

        Returns:
            ListeningResult with coherence, patterns, lure, metrics
        """
        start_time = time.time()
        patterns: List[ListeningPattern] = []

        # 🆕 PHASE C3.5: Collect full input text for embedding-based lure computation
        full_text = ' '.join([occasion.text for occasion in occasions])

        # Process each occasion (text chunk)
        for idx, occasion in enumerate(occasions):
            text = occasion.text.lower()
            chunk_id = occasion.chunk_id

            # Detect all pattern types
            patterns.extend(self._detect_acknowledgment(text, chunk_id, idx))
            patterns.extend(self._detect_reflection(text, chunk_id, idx))
            patterns.extend(self._detect_presence(text, chunk_id, idx))
            patterns.extend(self._detect_tracking(text, chunk_id, idx))
            patterns.extend(self._detect_understanding(text, chunk_id, idx))
            patterns.extend(self._detect_transformative(text, chunk_id, idx))

        # 🆕 PHASE C3.5: Pass full text for embedding-based lure computation
        result = self._compute_result(patterns, start_time, full_text=full_text)

        return result

    def _detect_acknowledgment(self, text: str, chunk_id: str, position: int) -> List[ListeningPattern]:
        """Detect acknowledgment patterns (basic listening)."""
        matches = self.acknowledgment_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.4, 1.0)  # Cap at 1.0
        confidence = 0.9  # High confidence for clear keywords

        return [ListeningPattern(
            pattern_type='acknowledgment',
            strength=strength,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            listening_quality='surface'
        )]

    def _detect_reflection(self, text: str, chunk_id: str, position: int) -> List[ListeningPattern]:
        """Detect reflection patterns (mirroring back)."""
        matches = self.reflection_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.6, 1.3)  # Can exceed 1.0 for strong reflection
        confidence = 0.85

        return [ListeningPattern(
            pattern_type='reflection',
            strength=strength * self.config.engaged_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            listening_quality='engaged'
        )]

    def _detect_presence(self, text: str, chunk_id: str, position: int) -> List[ListeningPattern]:
        """Detect presence markers (here-now attention)."""
        matches = self.presence_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.7, 1.5)
        confidence = 0.8

        return [ListeningPattern(
            pattern_type='presence_marker',
            strength=strength * self.config.deep_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            listening_quality='deep'
        )]

    def _detect_tracking(self, text: str, chunk_id: str, position: int) -> List[ListeningPattern]:
        """Detect tracking patterns (following thread over time)."""
        matches = self.tracking_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.8, 1.6)
        confidence = 0.9  # High confidence for temporal continuity

        return [ListeningPattern(
            pattern_type='tracking',
            strength=strength * self.config.deep_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            listening_quality='deep'
        )]

    def _detect_understanding(self, text: str, chunk_id: str, position: int) -> List[ListeningPattern]:
        """Detect understanding patterns (comprehension signals)."""
        matches = self.understanding_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 0.5, 1.2)
        confidence = 0.75

        return [ListeningPattern(
            pattern_type='understanding',
            strength=strength * self.config.engaged_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            listening_quality='engaged'
        )]

    def _detect_transformative(self, text: str, chunk_id: str, position: int) -> List[ListeningPattern]:
        """Detect transformative listening (deepest level, rare)."""
        matches = self.transformative_pattern.findall(text)
        if not matches:
            return []

        strength = min(len(matches) * 1.2, 2.0)  # Can reach maximum 2.0
        confidence = 0.95  # Very high confidence for transformative markers

        return [ListeningPattern(
            pattern_type='transformative',
            strength=strength * self.config.transformative_amplification,
            chunk_id=chunk_id,
            position=position,
            matched_keywords=list(set(matches)),
            confidence=confidence,
            listening_quality='transformative'
        )]

    def _compute_result(self, patterns: List[ListeningPattern], start_time: float, full_text: str = "") -> ListeningResult:
        """
        Compute aggregate ListeningResult from detected patterns.

        Args:
            patterns: Detected ListeningPattern objects
            start_time: Start time for processing time calculation
            full_text: 🆕 PHASE C3.5: Full input text for embedding-based lure computation

        Returns:
            ListeningResult with all metrics
        """
        processing_time_ms = (time.time() - start_time) * 1000

        if not patterns:
            # 🆕 PHASE C3.5: Use embedding-based lures even when no keywords detected
            if self.use_embedding_lures and full_text:
                inquiry_lure_field = self._compute_embedding_based_lure_field(full_text)
            else:
                inquiry_lure_field = {  # Balanced default
                    'temporal_inquiry': 1.0/7, 'core_exploration': 1.0/7,
                    'witnessing_presence': 1.0/7, 'pattern_mapping': 1.0/7,
                    'silence_holding': 1.0/7, 'clarifying_inquiry': 1.0/7,
                    'tracking_continuity': 1.0/7
                }

            return ListeningResult(
                coherence=0.0,
                patterns=[],
                lure=0.0,
                processing_time_ms=processing_time_ms,
                attention_score=0.0,
                presence_level=0.0,
                reflection_depth=0.0,
                tracking_continuity=0.0,
                dominant_quality=None,
                inquiry_lure_field=inquiry_lure_field,  # 🆕 Embedding-based or balanced
                atom_activations={},  # Empty atom activations
                felt_vector=None
            )

        # Compute coherence (average confidence weighted by strength)
        total_weight = sum(p.strength * p.confidence for p in patterns)
        total_strength = sum(p.strength for p in patterns)
        coherence = min(total_weight / max(total_strength, 0.1), 1.0)

        # Compute lure (pull toward deeper listening)
        # High when presence/tracking detected, low when only acknowledgment
        quality_scores = {'surface': 0.2, 'engaged': 0.5, 'deep': 0.8, 'transformative': 1.0}
        avg_quality = sum(quality_scores[p.listening_quality] for p in patterns) / len(patterns)
        lure = min(avg_quality * 1.2, 1.0)

        # Compute specific metrics
        attention_score = self._compute_attention(patterns)
        presence_level = self._compute_presence(patterns)
        reflection_depth = self._compute_reflection_depth(patterns)
        tracking_continuity = self._compute_tracking(patterns)

        # Dominant quality
        quality_counts = {}
        for p in patterns:
            quality_counts[p.listening_quality] = quality_counts.get(p.listening_quality, 0) + p.strength
        dominant_quality = max(quality_counts, key=quality_counts.get) if quality_counts else None

        # 🆕 PHASE 1: Compute atom activations DIRECTLY (bypass semantic_field_extractor!)
        atom_activations = self._compute_atom_activations(patterns, coherence, lure)

        # 🆕 PHASE C3.5: Compute inquiry lure field (embedding-based OR pattern-based)
        if self.use_embedding_lures and full_text:
            # Use embedding-based lure computation (80-90% activation rate)
            inquiry_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to balanced default (pattern-based not implemented for LISTENING)
            inquiry_lure_field = {
                'temporal_inquiry': 1.0/7, 'core_exploration': 1.0/7,
                'witnessing_presence': 1.0/7, 'pattern_mapping': 1.0/7,
                'silence_holding': 1.0/7, 'clarifying_inquiry': 1.0/7,
                'tracking_continuity': 1.0/7
            }

        return ListeningResult(
            coherence=coherence,
            patterns=patterns,
            lure=lure,
            processing_time_ms=processing_time_ms,
            attention_score=attention_score,
            presence_level=presence_level,
            reflection_depth=reflection_depth,
            tracking_continuity=tracking_continuity,
            dominant_quality=dominant_quality,
            inquiry_lure_field=inquiry_lure_field,  # 🆕 Multi-dimensional inquiry space
            atom_activations=atom_activations,  # 🆕 POPULATED!
            felt_vector=None  # Future: Phase 2/3 entity-native
        )

    def _compute_attention(self, patterns: List[ListeningPattern]) -> float:
        """Compute overall attention score from patterns."""
        attention_types = {'acknowledgment', 'reflection', 'understanding'}
        attention_patterns = [p for p in patterns if p.pattern_type in attention_types]
        if not attention_patterns:
            return 0.0
        return min(sum(p.strength for p in attention_patterns) / 3.0, 1.0)

    def _compute_presence(self, patterns: List[ListeningPattern]) -> float:
        """Compute presence level from presence markers."""
        presence_patterns = [p for p in patterns if p.pattern_type == 'presence_marker']
        if not presence_patterns:
            return 0.0
        return min(sum(p.strength for p in presence_patterns) / 2.0, 1.0)

    def _compute_reflection_depth(self, patterns: List[ListeningPattern]) -> float:
        """Compute reflection depth from reflection patterns."""
        reflection_patterns = [p for p in patterns if p.pattern_type == 'reflection']
        if not reflection_patterns:
            return 0.0
        return min(sum(p.strength for p in reflection_patterns) / 2.5, 1.0)

    def _compute_tracking(self, patterns: List[ListeningPattern]) -> float:
        """Compute tracking continuity from tracking patterns."""
        tracking_patterns = [p for p in patterns if p.pattern_type == 'tracking']
        if not tracking_patterns:
            return 0.0
        return min(sum(p.strength for p in tracking_patterns) / 2.0, 1.0)


# Module-level convenience function
def detect_listening(text: str) -> Dict:
    """
    Quick listening detection from raw text.

    Args:
        text: Raw conversational text

    Returns:
        Dict with coherence, attention_score, presence_level, dominant_quality
    """
    from dataclasses import dataclass as _dataclass

    # Create minimal TextOccasion for testing
    @_dataclass
    class _TextOccasion:
        text: str
        chunk_id: str

    occasion = _TextOccasion(text=text, chunk_id='test')

    core = ListeningTextCore()
    result = core.process_text_occasions([occasion], cycle=0)

    return {
        'coherence': result.coherence,
        'attention_score': result.attention_score,
        'presence_level': result.presence_level,
        'reflection_depth': result.reflection_depth,
        'tracking_continuity': result.tracking_continuity,
        'dominant_quality': result.dominant_quality,
        'lure': result.lure
    }


if __name__ == '__main__':
    """Test LISTENING organ with sample conversational text."""

    test_cases = [
        # Surface listening
        "Yes, I hear you. Okay. Mm-hmm.",

        # Engaged reflection
        "What I'm hearing is that you're feeling overwhelmed. It sounds like the pressure is building.",

        # Deep presence
        "Right now, in this moment, I'm noticing you seem more grounded. Let's stay present with this.",

        # Tracking continuity
        "Earlier you mentioned feeling anxious. Coming back to that thread, I'm curious how that's shifted.",

        # Transformative listening
        "I'm deeply moved by what you just shared. This feels like a profound revelation about your core pattern.",

        # Mixed (should show complexity)
        "I hear what you're saying about the exile part. What I'm noticing right now is how present you are with this pain. Earlier you mentioned wanting to protect it - coming back to that thread, it sounds like you're ready to witness it differently.",
    ]

    print("=" * 70)
    print("LISTENING ORGAN - Text Core Test")
    print("=" * 70)
    print()

    for idx, text in enumerate(test_cases, 1):
        result = detect_listening(text)

        print(f"Test {idx}: \"{text[:60]}...\"")
        print(f"  Coherence: {result['coherence']:.2f}")
        print(f"  Attention: {result['attention_score']:.2f}")
        print(f"  Presence: {result['presence_level']:.2f}")
        print(f"  Reflection: {result['reflection_depth']:.2f}")
        print(f"  Tracking: {result['tracking_continuity']:.2f}")
        print(f"  Quality: {result['dominant_quality']}")
        print(f"  Lure: {result['lure']:.2f}")
        print()

    print("=" * 70)
    print("✓ LISTENING organ operational")
    print("=" * 70)
