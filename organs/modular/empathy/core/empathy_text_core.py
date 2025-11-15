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
import numpy as np
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

    # 🆕 EMOTIONAL LURE FIELD: Multi-dimensional affect space (Nov 13, 2025)
    emotional_lure_field: Dict[str, float] = field(default_factory=dict)
    # {'joy': 0.15, 'grief': 0.45, 'fear': 0.10, 'anger': 0.08, 'compassion': 0.12, 'shame': 0.05, 'neutral': 0.05}

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native


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
        self.organ_name = "EMPATHY"

        # 🆕 PHASE 2: Load shared meta-atoms
        self.meta_atoms_config = self._load_shared_meta_atoms()

        # Load semantic atoms from semantic_atoms.json for emission
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE C3.2: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

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

    def _load_semantic_atoms(self) -> List[str]:
        """
        Load EMPATHY semantic atoms from semantic_atoms.json.

        Returns:
            List of atom names (e.g., ['core_feeling', 'somatic_tracking', ...])
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
        patterns: List[EmpathyPattern],
        coherence: float,
        lure: float
    ) -> Dict[str, float]:
        """
        DIRECT atom activation computation (bypasses semantic_field_extractor!)

        Maps EMPATHY patterns to semantic atoms using pattern type matching.

        Pattern types → Semantic atoms mapping:
          - validation → core_feeling (witnessing emotion)
          - compassion → compassionate_presence (warmth toward suffering)
          - resonance → emotional_depth (deep mirroring)
          - attunement → relational_attunement (energy matching)
          - holding → somatic_tracking (body-based container)
          - fierce_compassion → compassionate_presence (protective warmth)
          - transformative → metaphorical_quality (poetic depth)

        Args:
            patterns: Detected EmpathyPattern objects
            coherence: Overall empathy coherence (0.0-1.0)
            lure: Appetition pull (0.0-1.0)

        Returns:
            Dict[atom_name, activation_strength] - continuous felt values
        """
        if not patterns:
            return {}

        atom_activations = {}

        # Pattern type → semantic atom mapping
        pattern_to_atom = {
            'validation': 'core_feeling',
            'compassion': 'compassionate_presence',
            'resonance': 'emotional_depth',
            'attunement': 'relational_attunement',
            'holding': 'somatic_tracking',
            'fierce_compassion': 'compassionate_presence',  # Also maps to compassionate_presence
            'transformative': 'metaphorical_quality'
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
        # High lure (0.8-1.0) = pull toward deeper empathy
        # Low lure (0.3-0.5) = minimal pull
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

    def process_text_occasions(
        self,
        occasions: List,  # List[TextOccasion]
        cycle: int
    ,
        context: Optional[Dict] = None) -> EmpathyResult:
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

        # 🆕 PHASE C3.2: Collect full input text for embedding-based lure computation
        full_text = ' '.join([occasion.text for occasion in occasions])

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

        # 🆕 PHASE C3.2: Pass full text for embedding-based lure computation
        result = self._compute_result(patterns, start_time, full_text=full_text)

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

    def _ensure_embedding_coordinator(self):
        """
        🆕 PHASE C3.2: Lazy-load embedding coordinator.

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
        🆕 PHASE C3.2: Load emotional lure prototypes from JSON.

        Loads 7 emotional prototypes (joy, grief, fear, anger, compassion, shame, neutral)
        for semantic distance-based lure computation.

        Returns:
            Dict[emotion_name, prototype_embedding_384d]
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

            # Extract emotional prototypes (7 dimensions)
            emotional_protos = data['prototypes']['empathy_emotional']
            self.lure_prototypes = {
                emotion: np.array(proto_data['embedding'])
                for emotion, proto_data in emotional_protos.items()
            }

            return self.lure_prototypes

        except Exception as e:
            print(f"⚠️  EMPATHY: Could not load lure prototypes: {e}")
            print(f"   Falling back to pattern-based lure computation")
            return None

    def _compute_embedding_based_lure_field(self, text: str) -> Dict[str, float]:
        """
        🆕 PHASE C3.2: Compute emotional lure field from semantic distance to prototypes.

        Uses embedding similarity to 7 emotional prototypes instead of keywords.
        Achieves continuous activation (80-90% rate) vs keyword dependency (20-40%).

        Method:
        1. Embed input text → 384D vector
        2. Compute cosine similarity to each of 7 emotional prototypes
        3. Convert similarity → lure (higher similarity = stronger lure)
        4. Normalize to sum to 1.0

        Args:
            text: Input text to analyze

        Returns:
            Dict[emotion, lure_strength] - normalized to sum to 1.0
        """
        # Ensure coordinator and prototypes loaded
        self._ensure_embedding_coordinator()
        prototypes = self._load_lure_prototypes()

        if prototypes is None:
            # Fallback to balanced if prototypes unavailable
            return {
                'joy': 1.0/7, 'grief': 1.0/7, 'fear': 1.0/7, 'anger': 1.0/7,
                'compassion': 1.0/7, 'shame': 1.0/7, 'neutral': 1.0/7
            }

        # Embed input text
        input_embedding = self.embedding_coordinator.embed(text)

        # Normalize input embedding
        input_norm = np.linalg.norm(input_embedding)
        if input_norm > 0:
            input_embedding = input_embedding / input_norm

        # Compute cosine similarity to each prototype
        similarities = {}
        for emotion, prototype in prototypes.items():
            # Cosine similarity (both normalized)
            similarity = np.dot(input_embedding, prototype)
            # Clip to [0, 1] and use as lure strength
            similarities[emotion] = max(0.0, similarity)

        # Normalize to sum to 1.0
        total_sim = sum(similarities.values())
        if total_sim > 0:
            lure_field = {k: v / total_sim for k, v in similarities.items()}
        else:
            # Edge case: all negative similarities
            lure_field = {e: 1.0/7 for e in similarities.keys()}

        return lure_field

    def _compute_emotional_lure_field(self, patterns: List[EmpathyPattern]) -> Dict[str, float]:
        """
        🆕 NOV 13, 2025: Compute emotional lure field from patterns.

        Maps EMPATHY pattern types to 7 emotional attractor dimensions.
        Creates continuous lure field (not binary keyword matching).

        Pattern type → Emotional dimension mapping:
          - validation → neutral (witnessing, cognitive)
          - compassion → compassion (warmth toward suffering)
          - resonance → grief (deep emotional mirroring)
          - attunement → joy (energy matching, connection)
          - holding → compassion (somatic container)
          - fierce_compassion → anger (protective boundaries)
          - transformative → grief (transformation through loss/depth)

        Args:
            patterns: Detected EmpathyPattern objects

        Returns:
            Dict[emotion, lure_strength] - normalized to sum to 1.0
        """
        # Initialize 7 emotional dimensions
        lure_field = {
            'joy': 0.0,
            'grief': 0.0,
            'fear': 0.0,
            'anger': 0.0,
            'compassion': 0.0,
            'shame': 0.0,
            'neutral': 0.0
        }

        # Map pattern types to emotional dimensions
        pattern_to_emotion = {
            'validation': 'neutral',
            'compassion': 'compassion',
            'resonance': 'grief',
            'attunement': 'joy',
            'holding': 'compassion',
            'fierce_compassion': 'anger',
            'transformative': 'grief'
        }

        # Accumulate pattern strengths into emotional dimensions
        for pattern in patterns:
            emotion = pattern_to_emotion.get(pattern.pattern_type)
            if emotion:
                lure_field[emotion] = max(
                    lure_field[emotion],
                    pattern.strength
                )

        # Normalize to sum to 1.0
        total_lure = sum(lure_field.values())
        if total_lure > 0:
            lure_field = {k: v / total_lure for k, v in lure_field.items()}
        else:
            # No patterns detected, balanced default
            lure_field = {e: 1.0/7 for e in lure_field.keys()}

        return lure_field

    def _compute_result(self, patterns: List[EmpathyPattern], start_time: float, full_text: str = "") -> EmpathyResult:
        """
        Compute aggregate EmpathyResult from detected patterns.

        Args:
            patterns: Detected EmpathyPattern objects
            start_time: Start time for processing time calculation
            full_text: 🆕 PHASE C3.2: Full input text for embedding-based lure computation

        Returns:
            EmpathyResult with all metrics
        """
        processing_time_ms = (time.time() - start_time) * 1000

        if not patterns:
            # 🆕 PHASE C3.2: Use embedding-based lures even when no keywords detected
            if self.use_embedding_lures and full_text:
                emotional_lure_field = self._compute_embedding_based_lure_field(full_text)
            else:
                emotional_lure_field = {  # Balanced default
                    'joy': 1.0/7, 'grief': 1.0/7, 'fear': 1.0/7, 'anger': 1.0/7,
                    'compassion': 1.0/7, 'shame': 1.0/7, 'neutral': 1.0/7
                }

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
                emotional_tone=None,
                emotional_lure_field=emotional_lure_field,  # 🆕 Embedding-based or balanced
                atom_activations={},  # Empty atom activations
                felt_vector=None
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

        # 🆕 PHASE 1: Compute atom activations DIRECTLY (bypass semantic_field_extractor!)
        atom_activations = self._compute_atom_activations(patterns, coherence, lure)

        # 🆕 PHASE C3.2: Compute emotional lure field (embedding-based OR pattern-based)
        if self.use_embedding_lures and full_text:
            # Use embedding-based lure computation (80-90% activation rate)
            emotional_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to pattern-based lure computation (20-40% activation rate)
            emotional_lure_field = self._compute_emotional_lure_field(patterns)

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
            emotional_tone=emotional_tone,
            emotional_lure_field=emotional_lure_field,  # 🆕 Multi-dimensional affect space
            atom_activations=atom_activations,  # 🆕 POPULATED!
            felt_vector=None  # Future: Phase 2/3 entity-native
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
