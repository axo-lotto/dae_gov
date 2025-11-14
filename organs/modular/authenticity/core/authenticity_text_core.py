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
import numpy as np
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

    # 🆕 VULNERABILITY LURE FIELD: Multi-dimensional relational space (Nov 13, 2025)
    vulnerability_lure_field: Dict[str, float] = field(default_factory=dict)
    # {'vulnerable': 0.30, 'honest': 0.20, 'guarded': 0.15, 'performative': 0.10, 'emergent': 0.12, 'receptive': 0.08, 'boundaried': 0.05}

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native


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

        # 🆕 PHASE 1: Entity-native emission support
        self.organ_name = "AUTHENTICITY"

        # 🆕 PHASE 2: Load shared meta-atoms
        self.meta_atoms_config = self._load_shared_meta_atoms()
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE C3.4: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

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

    def _load_semantic_atoms(self) -> List[str]:
        """Load AUTHENTICITY semantic atoms from semantic_atoms.json.

        AUTHENTICITY atoms: core_truth_seeking, edge_exploration, voice_reclamation,
                            integrity_alignment, shadow_integration, permission_giving
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
        patterns: List[AuthenticityPattern],
        coherence: float,
        lure: float
    ) -> Dict[str, float]:
        """DIRECT atom activation computation (bypasses semantic_field_extractor!)

        AUTHENTICITY pattern types → Semantic atoms mapping:
          - genuine → core_truth_seeking (honest expression)
          - vulnerable → edge_exploration (courage at edge)
          - self_disclosure → voice_reclamation (personal sharing)
          - transparent → integrity_alignment (honest limitations)
          - congruent → shadow_integration (inner/outer alignment)
          - anti_performance → permission_giving (dropping facade)

        Args:
            patterns: Detected authenticity patterns
            coherence: Authenticity coherence (0.0-1.0)
            lure: Appetition pull toward deeper authenticity

        Returns:
            Dict mapping semantic atom names to continuous activation values (0.0-1.0)
        """
        if not patterns:
            return {}

        atom_activations = {}

        # Pattern type → semantic atom mapping
        pattern_to_atom = {
            'genuine': 'core_truth_seeking',
            'vulnerable': 'edge_exploration',
            'self_disclosure': 'voice_reclamation',
            'transparent': 'integrity_alignment',
            'congruent': 'shadow_integration',
            'anti_performance': 'permission_giving'
        }

        for pattern in patterns:
            atom = pattern_to_atom.get(pattern.pattern_type)
            if not atom:
                continue

            # Compute base activation from pattern strength × confidence
            base_activation = pattern.strength * pattern.confidence

            # Modulate by coherence (authenticity integration)
            activation = base_activation * coherence

            # Accumulate (multiple patterns can activate same atom)
            atom_activations[atom] = atom_activations.get(atom, 0.0) + activation

        # Apply lure weighting (appetition pull toward authenticity)
        # Higher lure = stronger activation (authenticity seeking)
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

        # 🆕 PHASE C3.4: Collect full input text for embedding-based lure computation
        full_text = ' '.join([occasion.text for occasion in occasions])

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

        # 🆕 PHASE C3.4: Pass full text for embedding-based lure computation
        result = self._compute_result(patterns, start_time, full_text=full_text)

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

    def _ensure_embedding_coordinator(self):
        """
        🆕 PHASE C3.4: Lazy-load embedding coordinator.

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
        🆕 PHASE C3.4: Load vulnerability lure prototypes from JSON.

        Loads 7 vulnerability prototypes (vulnerable, honest, guarded, performative,
        emergent, receptive, boundaried) for semantic distance-based lure computation.

        Returns:
            Dict[stance_name, prototype_embedding_384d]
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

            # Extract authenticity/vulnerability prototypes (7 dimensions)
            vulnerability_protos = data['prototypes']['authenticity_vulnerability']
            self.lure_prototypes = {
                stance: np.array(proto_data['embedding'])
                for stance, proto_data in vulnerability_protos.items()
            }

            return self.lure_prototypes

        except Exception as e:
            print(f"⚠️  AUTHENTICITY: Could not load lure prototypes: {e}")
            print(f"   Falling back to pattern-based lure computation")
            return None

    def _compute_embedding_based_lure_field(self, text: str) -> Dict[str, float]:
        """
        🆕 PHASE C3.4: Compute vulnerability lure field from semantic distance to prototypes.

        Uses embedding similarity to 7 vulnerability prototypes instead of keywords.
        Achieves continuous activation (80-90% rate) vs keyword dependency (20-40%).

        Method:
        1. Embed input text → 384D vector
        2. Compute cosine similarity to each of 7 vulnerability prototypes
        3. Convert similarity → lure (higher similarity = stronger lure)
        4. Normalize to sum to 1.0

        Args:
            text: Input text to analyze

        Returns:
            Dict[stance, lure_strength] - normalized to sum to 1.0
        """
        # Ensure coordinator and prototypes loaded
        self._ensure_embedding_coordinator()
        prototypes = self._load_lure_prototypes()

        if prototypes is None:
            # Fallback to balanced if prototypes unavailable
            return {
                'vulnerable': 1.0/7, 'honest': 1.0/7, 'guarded': 1.0/7, 'performative': 1.0/7,
                'emergent': 1.0/7, 'receptive': 1.0/7, 'boundaried': 1.0/7
            }

        # Embed input text
        input_embedding = self.embedding_coordinator.embed(text)

        # Normalize input embedding
        input_norm = np.linalg.norm(input_embedding)
        if input_norm > 0:
            input_embedding = input_embedding / input_norm

        # Compute cosine similarity to each prototype
        similarities = {}
        for stance, prototype in prototypes.items():
            # Cosine similarity (both normalized)
            similarity = np.dot(input_embedding, prototype)
            # Clip to [0, 1] and use as lure strength
            similarities[stance] = max(0.0, similarity)

        # Normalize to sum to 1.0
        total_sim = sum(similarities.values())
        if total_sim > 0:
            lure_field = {k: v / total_sim for k, v in similarities.items()}
        else:
            # Edge case: all negative similarities
            lure_field = {s: 1.0/7 for s in similarities.keys()}

        return lure_field

    def _compute_vulnerability_lure_field(self, patterns: List[AuthenticityPattern]) -> Dict[str, float]:
        """
        🆕 NOV 13, 2025: Compute vulnerability lure field from patterns.

        Maps AUTHENTICITY pattern types to 7 relational vulnerability dimensions.
        Creates continuous lure field (not binary keyword matching).

        Pattern type → Vulnerability dimension mapping:
          - vulnerable → vulnerable (open, exposed, tender)
          - genuine → honest (truthful, real, congruent)
          - self_disclosure → emergent (becoming, unfolding)
          - transparent → honest (acknowledging limitations)
          - congruent → honest (inner/outer alignment)
          - anti_performance → receptive (no facade, open to change)

        Note: 'guarded', 'performative', 'boundaried' are not directly detected
        by current patterns, but included in balanced default for completeness.

        Args:
            patterns: Detected AuthenticityPattern objects

        Returns:
            Dict[stance, lure_strength] - normalized to sum to 1.0
        """
        # Initialize 7 vulnerability dimensions
        lure_field = {
            'vulnerable': 0.0,
            'honest': 0.0,
            'guarded': 0.0,
            'performative': 0.0,
            'emergent': 0.0,
            'receptive': 0.0,
            'boundaried': 0.0
        }

        # Map pattern types to vulnerability dimensions
        pattern_to_vulnerability = {
            'vulnerable': 'vulnerable',
            'genuine': 'honest',
            'self_disclosure': 'emergent',
            'transparent': 'honest',
            'congruent': 'honest',
            'anti_performance': 'receptive'
        }

        # Accumulate pattern strengths into vulnerability dimensions
        for pattern in patterns:
            vulnerability = pattern_to_vulnerability.get(pattern.pattern_type)
            if vulnerability:
                lure_field[vulnerability] = max(
                    lure_field[vulnerability],
                    pattern.strength
                )

        # Normalize to sum to 1.0
        total_lure = sum(lure_field.values())
        if total_lure > 0:
            lure_field = {k: v / total_lure for k, v in lure_field.items()}
        else:
            # No patterns detected, balanced default
            lure_field = {v: 1.0/7 for v in lure_field.keys()}

        return lure_field

    def _compute_result(self, patterns: List[AuthenticityPattern], start_time: float, full_text: str = "") -> AuthenticityResult:
        """
        Compute aggregate AuthenticityResult from detected patterns.

        Args:
            patterns: Detected AuthenticityPattern objects
            start_time: Start time for processing time calculation
            full_text: 🆕 PHASE C3.4: Full input text for embedding-based lure computation

        Returns:
            AuthenticityResult with all metrics
        """
        processing_time_ms = (time.time() - start_time) * 1000

        if not patterns:
            # 🆕 PHASE C3.4: Use embedding-based lures even when no keywords detected
            if self.use_embedding_lures and full_text:
                vulnerability_lure_field = self._compute_embedding_based_lure_field(full_text)
            else:
                vulnerability_lure_field = {  # Balanced default
                    'vulnerable': 1.0/7, 'honest': 1.0/7, 'guarded': 1.0/7, 'performative': 1.0/7,
                    'emergent': 1.0/7, 'receptive': 1.0/7, 'boundaried': 1.0/7
                }

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
                dominant_authenticity=None,
                vulnerability_lure_field=vulnerability_lure_field  # 🆕 Embedding-based or balanced
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

        # 🆕 PHASE 1: Compute atom activations DIRECTLY (bypass semantic_field_extractor!)
        atom_activations = self._compute_atom_activations(patterns, coherence, lure)

        # 🆕 PHASE C3.4: Compute vulnerability lure field (embedding-based OR pattern-based)
        if self.use_embedding_lures and full_text:
            # Use embedding-based lure computation (80-90% activation rate)
            vulnerability_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to pattern-based lure computation (20-40% activation rate)
            vulnerability_lure_field = self._compute_vulnerability_lure_field(patterns)

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
            dominant_authenticity=dominant_authenticity,
            vulnerability_lure_field=vulnerability_lure_field,  # 🆕 Multi-dimensional relational space
            atom_activations=atom_activations,  # 🆕 POPULATED!
            felt_vector=None  # Future: Phase 2/3 entity-native
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
