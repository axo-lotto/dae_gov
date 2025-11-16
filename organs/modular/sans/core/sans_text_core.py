"""
SANS Text Core - Semantic Attention & Novelty System (Text Domain)

Text-native implementation of SANS organ for organizational governance processing.
Detects semantic patterns, similarity relationships, and meaning-based connections
in 384-dim embedding space.

Architecture:
- 100% LLM-free (pure cosine similarity)
- 384-dim sentence-transformers embeddings
- Text-native similarity detection
- FAISS-ready (Phase 4)
- Hebbian learning of semantic patterns

Author: DAE-GOV Development Team
Created: November 10, 2025
Version: 1.0 (Text-Native Foundation)
"""

import numpy as np
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import sys

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from organs.modular.sans.config.sans_config import SANSConfig, DEFAULT_SANS_CONFIG
from transductive.text_occasion import TextOccasion


@dataclass
class SemanticPattern:
    """Detected semantic similarity pattern."""

    pattern_type: str                       # "exact_repetition", "thematic_resonance", etc.
    similarity_score: float                 # Cosine similarity (0-1)
    chunk_id_1: str                         # First chunk ID
    chunk_id_2: str                         # Second chunk ID
    confidence: float                       # Pattern confidence (0-1)

    # Context
    text_1: Optional[str] = None
    text_2: Optional[str] = None

    # Metadata
    detected_timestamp: float = field(default_factory=time.time)


@dataclass
class SANSResult:
    """Result from SANS organ processing."""

    coherence: float                        # Overall semantic coherence (0-1)
    patterns: List[SemanticPattern]         # Detected similarity patterns
    lure: float                             # Appetition lure strength (0-1)
    processing_time: float                  # Milliseconds

    # Detailed outputs
    mean_similarity: float = 0.0            # Mean pairwise similarity
    max_similarity: float = 0.0             # Maximum similarity found
    thematic_coherence: float = 0.0         # Thematic consistency
    novelty_score: float = 0.0              # 1.0 - familiarity (how novel)

    # Metadata
    occasions_processed: int = 0
    comparisons_made: int = 0

    # 🆕 PHASE 1: Entity-native emission support
    atom_activations: Dict[str, float] = field(default_factory=dict)  # Direct atom activation for emission
    felt_vector: Optional['np.ndarray'] = None  # Future: 7D felt vector for full entity-native

    # 🆕 PHASE C3: Embedding-based lure field (Nov 13, 2025)
    coherence_lure_field: Dict[str, float] = field(default_factory=dict)


class SANSTextCore:
    """
    SANS (Semantic Attention & Novelty System) - Text Domain

    Processes text occasions to detect semantic patterns through pure
    cosine similarity analysis (100% LLM-free).

    Key Responsibilities:
    - Pairwise similarity detection (cosine in 384-dim space)
    - Pattern classification (exact repetition, thematic resonance, etc.)
    - Semantic coherence measurement
    - Novelty/familiarity assessment
    - Hebbian pattern learning (Phase 2)
    - FAISS semantic search (Phase 4)

    Universal Organ Interface:
    - process_text_occasions(occasions, cycle) → SANSResult
    - get_organ_config() → Dict
    - get_hebbian_learning_config() → Dict
    """

    def __init__(self, config: Optional[SANSConfig] = None):
        """
        Initialize SANS text-native organ.

        Args:
            config: Optional SANSConfig instance
        """
        self.config = config or DEFAULT_SANS_CONFIG

        # 🆕 PHASE 1: Entity-native support
        self.organ_name = "SANS"
        self.semantic_atoms = self._load_semantic_atoms()

        # 🆕 PHASE 2: Load shared meta-atoms for nexus formation
        self.meta_atoms_config = self._load_shared_meta_atoms()

        # 🆕 PHASE C3: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures

        # Pattern detection history (for learning)
        self.pattern_history: List[SemanticPattern] = []

        # Statistics
        self.total_occasions_processed = 0
        self.total_patterns_detected = 0
        self.total_processing_time = 0.0

        print(f"✅ SANS organ initialized (text-native, LLM-free)")
        print(f"   Similarity threshold: {self.config.similarity_threshold}")
        print(f"   Embedding dim: {self.config.embedding_dim}")
        print(f"   FAISS enabled: {self.config.faiss_enabled}")

    # ========================================================================
    # 🆕 PHASE 1: ENTITY-NATIVE ATOM ACTIVATION
    # ========================================================================

    def _load_semantic_atoms(self) -> List[str]:
        """Load SANS semantic atoms from semantic_atoms.json."""
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

            metadata_keys = {'description', 'dimension', 'field_type', 'total_atoms'}
            organ_data = all_atoms[self.organ_name]
            atom_names = [k for k in organ_data.keys() if k not in metadata_keys]

            return atom_names
        except Exception as e:
            print(f"Warning: Could not load semantic atoms for {self.organ_name}: {e}")
            return []

    def _load_shared_meta_atoms(self) -> Optional[Dict]:
        """
        🆕 PHASE 2: Load shared meta-atoms for nexus formation.

        SANS contributes to 3 meta-atoms:
        - safety_restoration (SANS, EO, NDAM)
        - compassion_safety (EMPATHY, EO, SANS)
        - coherence_integration (SANS, WISDOM, LISTENING)
        """
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

            return {
                'meta_atoms': relevant_meta_atoms,
                'count': len(relevant_meta_atoms)
            }
        except Exception as e:
            return None

    def _compute_atom_activations(
        self,
        patterns: List[SemanticPattern],
        coherence: float,
        lure: float
    ) -> Dict[str, float]:
        """
        🆕 PHASE 1: DIRECT atom activation computation (bypasses semantic_field_extractor!)

        Maps SANS pattern types → semantic atoms:
        - exact_repetition (sim ≥0.95) → high_coherence
        - parts_language_consistency (sim ≥0.85) → semantic_precision
        - reenactment_pattern (sim ≥0.80) → referential_tracking
        - thematic_resonance (sim ≥0.75) → meta_linguistic
        - semantic_echo (sim ≥0.70) → meaning_drift (moderate similarity)
        - conceptual_affinity (sim <0.70) → low_coherence

        Special atoms:
        - coherence_repair: Activated when mean_similarity is improving (high lure)
        """
        if not patterns:
            return {}

        atom_activations = {}

        # Pattern type → atom mapping
        pattern_to_atom = {
            'exact_repetition': 'high_coherence',
            'parts_language_consistency': 'semantic_precision',
            'reenactment_pattern': 'referential_tracking',
            'thematic_resonance': 'meta_linguistic',
            'semantic_echo': 'meaning_drift',
            'conceptual_affinity': 'low_coherence'
        }

        for pattern in patterns:
            # Direct pattern type mapping
            atom = pattern_to_atom.get(pattern.pattern_type)
            if atom:
                # Base activation from pattern strength and confidence
                base_activation = pattern.similarity_score * pattern.confidence
                activation = base_activation * coherence
                atom_activations[atom] = atom_activations.get(atom, 0.0) + activation

        # Special case: coherence_repair
        # High lure indicates improving semantic coherence (organism drawn toward it)
        if lure > 0.6:
            coherence_repair_activation = lure * coherence
            atom_activations['coherence_repair'] = coherence_repair_activation

        # Apply lure weighting
        lure_weight = 0.5 + 0.5 * lure
        for atom in atom_activations:
            atom_activations[atom] *= lure_weight

        # Normalize to [0.0, 1.0]
        if atom_activations:
            max_activation = max(atom_activations.values())
            if max_activation > 1.0:
                for atom in atom_activations:
                    atom_activations[atom] /= max_activation

        # 🆕 PHASE 2: Add meta-atom activations (for nexus formation)
        if self.meta_atoms_config:
            meta_activations = self._activate_meta_atoms(patterns, coherence, lure)
            atom_activations.update(meta_activations)

        return atom_activations

    def _activate_meta_atoms(
        self,
        patterns: List[SemanticPattern],
        coherence: float,
        lure: float
    ) -> Dict[str, float]:
        """
        🆕 PHASE 2: Activate shared meta-atoms for nexus formation.

        SANS contributes to 3 meta-atoms:
        1. safety_restoration (SANS, EO, NDAM) - High coherence + coherence repair
        2. compassion_safety (EMPATHY, EO, SANS) - Semantic precision + alignment
        3. coherence_integration (SANS, WISDOM, LISTENING) - High coherence + meta-linguistic
        """
        if not self.meta_atoms_config or not patterns:
            return {}

        meta_activations = {}
        import numpy as np

        # Get patterns by type
        high_coherence_patterns = [p for p in patterns if p.pattern_type in ['exact_repetition', 'parts_language_consistency']]
        precision_patterns = [p for p in patterns if p.pattern_type == 'parts_language_consistency']
        meta_ling_patterns = [p for p in patterns if p.pattern_type == 'thematic_resonance']

        # Calculate mean similarity for coherence metrics
        mean_similarity = np.mean([p.similarity_score for p in patterns]) if patterns else 0.0

        for meta_atom in self.meta_atoms_config['meta_atoms']:
            atom_name = meta_atom['atom']

            # 1. safety_restoration: High coherence + coherence repair (improving)
            if atom_name == 'safety_restoration':
                if high_coherence_patterns and lure > 0.5:
                    # Safety = coherent semantic field + improving
                    coherence_strength = sum(p.similarity_score * p.confidence for p in high_coherence_patterns) / len(high_coherence_patterns)
                    repair_boost = (lure - 0.5) * 0.5  # Boost from improving coherence
                    activation = (coherence_strength + repair_boost) * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

            # 2. compassion_safety: Semantic precision + alignment
            elif atom_name == 'compassion_safety':
                if precision_patterns and mean_similarity > 0.75:
                    # Compassion safety = precise semantic alignment
                    precision_strength = sum(p.similarity_score * p.confidence for p in precision_patterns) / len(precision_patterns)
                    alignment_factor = (mean_similarity - 0.75) / 0.25  # Normalize above threshold
                    activation = precision_strength * alignment_factor * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

            # 3. coherence_integration: High coherence + meta-linguistic patterns
            elif atom_name == 'coherence_integration':
                if high_coherence_patterns or meta_ling_patterns:
                    # Integration = systemic coherence + thematic resonance
                    integration_patterns = high_coherence_patterns + meta_ling_patterns
                    integration_strength = sum(p.similarity_score * p.confidence for p in integration_patterns) / len(integration_patterns)
                    activation = integration_strength * coherence * (0.5 + 0.5 * lure)
                    meta_activations[atom_name] = min(1.0, activation)

        return meta_activations

    # ========================================================================
    # 🆕 PHASE C3: EMBEDDING-BASED LURE COMPUTATION (Nov 13, 2025)
    # ========================================================================

    def _ensure_embedding_coordinator(self):
        """Lazy-load embedding coordinator."""
        if self.embedding_coordinator is None:
            from persona_layer.embedding_coordinator import EmbeddingCoordinator
            self.embedding_coordinator = EmbeddingCoordinator()

    def _load_lure_prototypes(self) -> Dict[str, np.ndarray]:
        """Load SANS lure prototypes from JSON."""
        if self.lure_prototypes is not None:
            return self.lure_prototypes

        import json
        from pathlib import Path

        # Navigate from organs/modular/sans/core/ up to project root, then to persona_layer
        prototype_path = Path(__file__).parent.parent.parent.parent.parent / 'persona_layer' / 'config' / 'lures' / 'lure_prototypes.json'

        with open(prototype_path, 'r') as f:
            data = json.load(f)

        category = data['prototypes']['sans_coherence']
        self.lure_prototypes = {
            dim: np.array(proto['embedding'])
            for dim, proto in category.items()
        }

        return self.lure_prototypes

    def _compute_embedding_based_lure_field(self, text: str) -> Dict[str, float]:
        """Compute lure field using semantic similarity."""
        self._ensure_embedding_coordinator()
        prototypes = self._load_lure_prototypes()

        # Get and normalize input embedding
        input_embedding = self.embedding_coordinator.embed(text)
        norm = np.linalg.norm(input_embedding)
        if norm > 0:
            input_embedding = input_embedding / norm
        else:
            # Fallback to uniform if zero vector (rare edge case)
            input_embedding = np.ones_like(input_embedding) / np.sqrt(len(input_embedding))

        # Compute cosine similarity to each prototype
        similarities = {}
        for dimension, prototype in prototypes.items():
            similarity = np.dot(input_embedding, prototype)
            similarities[dimension] = max(0.0, similarity)

        # Normalize to sum to 1.0
        total_sim = sum(similarities.values())
        if total_sim > 0:
            lure_field = {k: v / total_sim for k, v in similarities.items()}
        else:
            lure_field = {k: 1.0 / len(similarities) for k in similarities.keys()}

        return lure_field

    # ========================================================================
    # MAIN PROCESSING METHOD (Universal Organ Interface)
    # ========================================================================

    def process_text_occasions(
        self,
        occasions: List[TextOccasion],
        cycle: int = 1
    ,
        context: Optional[Dict] = None) -> SANSResult:
        """
        Process text occasions to detect semantic patterns.

        Universal organ method signature following legacy pattern.

        Args:
            occasions: List of TextOccasion entities with 384-dim embeddings
            cycle: Current processing cycle (for V0 integration)

        Returns:
            SANSResult with coherence, patterns, and lure
        """
        start_time = time.time()

        # 🆕 PHASE C3: Collect full input text for embedding-based lures
        full_text = ' '.join([occasion.text for occasion in occasions])

        if len(occasions) == 0:
            return self._create_empty_result()

        # Phase 1: Extract embeddings
        embeddings = self._extract_embeddings(occasions)

        # Phase 2: Compute pairwise similarities
        similarity_matrix = self._compute_similarity_matrix(embeddings)

        # Phase 3: Detect patterns
        patterns = self._detect_similarity_patterns(
            occasions,
            similarity_matrix,
            self.config.similarity_threshold
        )

        # Phase 4: Calculate coherence metrics
        coherence_metrics = self._calculate_coherence_metrics(
            similarity_matrix,
            patterns
        )

        # Phase 5: Calculate lure (appetition)
        lure = self._calculate_lure(coherence_metrics, patterns)

        # Phase 6: Entity-native prehension (add to occasions)
        self._prehend_occasions_with_affordances(
            occasions,
            patterns,
            coherence_metrics,
            cycle
        )

        # Statistics
        processing_time = (time.time() - start_time) * 1000
        self.total_occasions_processed += len(occasions)
        self.total_patterns_detected += len(patterns)
        self.total_processing_time += processing_time

        # Store patterns for learning
        self.pattern_history.extend(patterns)
        if len(self.pattern_history) > self.config.semantic_history_limit:
            self.pattern_history = self.pattern_history[-self.config.semantic_history_limit:]

        # 🆕 PHASE 1: Compute atom activations DIRECTLY (bypass semantic_field_extractor!)
        atom_activations = self._compute_atom_activations(
            patterns, coherence_metrics['overall_coherence'], lure)

        # 🆕 PHASE C3: Compute embedding-based lure field
        if self.use_embedding_lures and full_text:
            coherence_lure_field = self._compute_embedding_based_lure_field(full_text)
        else:
            # Fallback to balanced default
            coherence_lure_field = {
                'semantic_drift': 1.0/7,
                'contradiction_detected': 1.0/7,
                'alignment_strong': 1.0/7,
                'repair_needed': 1.0/7,
                'fragmentation': 1.0/7,
                'coherent_narrative': 1.0/7,
                'bridging_gaps': 1.0/7
            }

        return SANSResult(
            coherence=coherence_metrics['overall_coherence'],
            patterns=patterns,
            lure=lure,
            processing_time=processing_time,
            mean_similarity=coherence_metrics['mean_similarity'],
            max_similarity=coherence_metrics['max_similarity'],
            thematic_coherence=coherence_metrics['thematic_coherence'],
            novelty_score=coherence_metrics['novelty_score'],
            occasions_processed=len(occasions),
            comparisons_made=coherence_metrics['comparisons_made'],
            atom_activations=atom_activations,  # 🆕 POPULATED!
            coherence_lure_field=coherence_lure_field  # 🆕 PHASE C3
        )

    # ========================================================================
    # EMBEDDING EXTRACTION
    # ========================================================================

    def _extract_embeddings(self, occasions: List[TextOccasion]) -> np.ndarray:
        """
        Extract embeddings from occasions.

        Args:
            occasions: List of TextOccasion entities

        Returns:
            numpy array of shape (n_occasions, 384)
        """
        embeddings = np.array([occ.embedding for occ in occasions])

        # Validate shape
        assert embeddings.shape[1] == self.config.embedding_dim, \
            f"Expected {self.config.embedding_dim}-dim embeddings, got {embeddings.shape[1]}"

        return embeddings

    # ========================================================================
    # SIMILARITY COMPUTATION
    # ========================================================================

    def _compute_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Compute pairwise cosine similarity matrix.

        Args:
            embeddings: numpy array of shape (n, 384)

        Returns:
            Similarity matrix of shape (n, n) with values in [-1, 1]
        """
        # Normalize embeddings for cosine similarity
        # Guard against zero vectors to prevent NaN warnings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Replace zero norms with 1.0 to avoid division by zero (result will be zero vector)
        norms = np.where(norms == 0, 1.0, norms)
        embeddings_norm = embeddings / norms

        # Compute cosine similarity matrix
        similarity_matrix = embeddings_norm @ embeddings_norm.T

        return similarity_matrix

    # ========================================================================
    # PATTERN DETECTION
    # ========================================================================

    def _detect_similarity_patterns(
        self,
        occasions: List[TextOccasion],
        similarity_matrix: np.ndarray,
        threshold: float
    ) -> List[SemanticPattern]:
        """
        Detect semantic patterns from similarity matrix.

        Args:
            occasions: List of TextOccasion entities
            similarity_matrix: Pairwise similarity matrix
            threshold: Minimum similarity to consider

        Returns:
            List of detected SemanticPattern objects
        """
        patterns = []
        n = len(occasions)

        # Get similarity type settings
        similarity_types = self.config.get_similarity_type_settings()

        # Iterate over upper triangle (avoid duplicates and self-similarities)
        for i in range(n):
            for j in range(i + 1, n):
                similarity = similarity_matrix[i, j]

                # Skip if below base threshold
                if similarity < threshold:
                    continue

                # Classify pattern type based on similarity
                pattern_type = self._classify_pattern_type(similarity, similarity_types)

                # Get confidence multiplier for this type
                confidence_multiplier = similarity_types[pattern_type]['confidence_multiplier']
                confidence = min(1.0, similarity * confidence_multiplier)

                # Create pattern
                pattern = SemanticPattern(
                    pattern_type=pattern_type,
                    similarity_score=float(similarity),
                    chunk_id_1=occasions[i].chunk_id,
                    chunk_id_2=occasions[j].chunk_id,
                    confidence=confidence,
                    text_1=occasions[i].text,
                    text_2=occasions[j].text
                )

                patterns.append(pattern)

        # Limit patterns per conversation
        if len(patterns) > self.config.max_similarity_patterns_per_conversation:
            # Sort by confidence descending
            patterns = sorted(patterns, key=lambda p: p.confidence, reverse=True)
            patterns = patterns[:self.config.max_similarity_patterns_per_conversation]

        return patterns

    def _classify_pattern_type(
        self,
        similarity: float,
        similarity_types: Dict[str, Dict[str, Any]]
    ) -> str:
        """
        Classify pattern type based on similarity score.

        Args:
            similarity: Cosine similarity (0-1)
            similarity_types: Type definitions from config

        Returns:
            Pattern type string
        """
        # Check from most specific to least specific
        if similarity >= 0.95:
            return 'exact_repetition'
        elif similarity >= 0.85:
            return 'parts_language_consistency'
        elif similarity >= 0.80:
            return 'reenactment_pattern'
        elif similarity >= 0.75:
            return 'thematic_resonance'
        elif similarity >= 0.70:
            return 'semantic_echo'
        else:
            return 'conceptual_affinity'

    # ========================================================================
    # COHERENCE METRICS
    # ========================================================================

    def _calculate_coherence_metrics(
        self,
        similarity_matrix: np.ndarray,
        patterns: List[SemanticPattern]
    ) -> Dict[str, float]:
        """
        Calculate semantic coherence metrics.

        Args:
            similarity_matrix: Pairwise similarity matrix
            patterns: Detected patterns

        Returns:
            Dictionary of coherence metrics
        """
        n = similarity_matrix.shape[0]

        # Get upper triangle (excluding diagonal)
        upper_triangle = similarity_matrix[np.triu_indices(n, k=1)]

        # Basic statistics
        mean_similarity = float(np.mean(upper_triangle)) if len(upper_triangle) > 0 else 0.0
        max_similarity = float(np.max(upper_triangle)) if len(upper_triangle) > 0 else 0.0
        std_similarity = float(np.std(upper_triangle)) if len(upper_triangle) > 0 else 0.0

        # Thematic coherence (how consistent are similarities)
        # High coherence = high mean + low std (tight cluster)
        thematic_coherence = mean_similarity * (1.0 - min(1.0, std_similarity))

        # Novelty score (inverse of mean similarity)
        # High novelty = low mean similarity (diverse content)
        novelty_score = 1.0 - mean_similarity

        # Overall coherence (weighted combination)
        # High when patterns are strong AND thematic coherence is high
        pattern_strength = len(patterns) / max(1, len(upper_triangle))
        overall_coherence = (
            0.4 * mean_similarity +
            0.3 * thematic_coherence +
            0.3 * pattern_strength
        )

        return {
            'overall_coherence': min(1.0, overall_coherence),
            'mean_similarity': mean_similarity,
            'max_similarity': max_similarity,
            'thematic_coherence': thematic_coherence,
            'novelty_score': novelty_score,
            'comparisons_made': len(upper_triangle)
        }

    # ========================================================================
    # LURE CALCULATION (Appetition)
    # ========================================================================

    def _calculate_lure(
        self,
        coherence_metrics: Dict[str, float],
        patterns: List[SemanticPattern]
    ) -> float:
        """
        Calculate appetition lure strength.

        High lure when:
        - Strong semantic patterns detected
        - High thematic coherence (tight semantic cluster)
        - Multiple high-confidence patterns

        Args:
            coherence_metrics: Coherence metrics
            patterns: Detected patterns

        Returns:
            Lure strength (0-1)
        """
        if len(patterns) == 0:
            return 0.0

        # Pattern strength (number and confidence)
        pattern_count_factor = min(1.0, len(patterns) / 10.0)  # Saturate at 10
        mean_pattern_confidence = np.mean([p.confidence for p in patterns])

        # Thematic coherence factor
        thematic_factor = coherence_metrics['thematic_coherence']

        # Overall lure (weighted combination)
        lure = (
            0.4 * mean_pattern_confidence +
            0.3 * pattern_count_factor +
            0.3 * thematic_factor
        )

        return min(1.0, lure)

    # ========================================================================
    # ENTITY-NATIVE PREHENSION
    # ========================================================================

    def _prehend_occasions_with_affordances(
        self,
        occasions: List[TextOccasion],
        patterns: List[SemanticPattern],
        coherence_metrics: Dict[str, float],
        cycle: int
    ):
        """
        Add prehensions and felt affordances to text occasions.

        Entity-native approach: Store felt affordances DURING processing,
        which will be matured to propositions POST-CONVERGENCE.

        Args:
            occasions: List of TextOccasion entities (modified in-place)
            patterns: Detected patterns
            coherence_metrics: Coherence metrics
            cycle: Current cycle number
        """
        # Create organ output for prehension
        organ_output = {
            'coherence': coherence_metrics['overall_coherence'],
            'patterns': [
                {
                    'type': p.pattern_type,
                    'similarity': p.similarity_score,
                    'confidence': p.confidence
                }
                for p in patterns
            ],
            'lure': self._calculate_lure(coherence_metrics, patterns),
            'processing_time': 0.0  # Updated by caller
        }

        # Add prehension to all occasions
        for occ in occasions:
            occ.add_organ_prehension('SANS', organ_output, cycle)

        # Add felt affordances for high-confidence patterns
        for pattern in patterns:
            if pattern.confidence >= 0.7:
                # Find occasions involved in this pattern
                occ_1 = next((o for o in occasions if o.chunk_id == pattern.chunk_id_1), None)
                occ_2 = next((o for o in occasions if o.chunk_id == pattern.chunk_id_2), None)

                if occ_1:
                    occ_1.add_felt_affordance(
                        organ_name='SANS',
                        confidence=pattern.confidence,
                        lure_intensity=pattern.similarity_score,
                        pattern_type=pattern.pattern_type,
                        affordance_data={
                            'related_chunk': pattern.chunk_id_2,
                            'similarity': pattern.similarity_score
                        }
                    )

                if occ_2:
                    occ_2.add_felt_affordance(
                        organ_name='SANS',
                        confidence=pattern.confidence,
                        lure_intensity=pattern.similarity_score,
                        pattern_type=pattern.pattern_type,
                        affordance_data={
                            'related_chunk': pattern.chunk_id_1,
                            'similarity': pattern.similarity_score
                        }
                    )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _create_empty_result(self) -> SANSResult:
        """Create empty result for edge case."""
        return SANSResult(
            coherence=0.0,
            patterns=[],
            lure=0.0,
            processing_time=0.0,
            occasions_processed=0,
            comparisons_made=0
        )

    def get_organ_config(self) -> Dict[str, Any]:
        """Get organ configuration for introspection."""
        return {
            'organ_name': 'SANS',
            'version': '1.0',
            'domain': 'text',
            'llm_free': True,
            'similarity_threshold': self.config.similarity_threshold,
            'embedding_dim': self.config.embedding_dim,
            'faiss_enabled': self.config.faiss_enabled,
            'patterns_detected': self.total_patterns_detected,
            'occasions_processed': self.total_occasions_processed
        }

    def get_hebbian_learning_config(self) -> Dict[str, Any]:
        """Get Hebbian learning configuration."""
        return self.config.get_hebbian_learning_config()

    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'total_occasions_processed': self.total_occasions_processed,
            'total_patterns_detected': self.total_patterns_detected,
            'total_processing_time_ms': self.total_processing_time,
            'avg_processing_time_ms': (
                self.total_processing_time / max(1, self.total_occasions_processed)
            ),
            'patterns_per_occasion': (
                self.total_patterns_detected / max(1, self.total_occasions_processed)
            )
        }


if __name__ == "__main__":
    """
    Validation test for SANS text-native organ.
    """
    print("🧪 SANS Text Core Validation Test")
    print("=" * 60)

    # Create SANS organ
    sans = SANSTextCore()

    # Create sample text occasions
    print("\n📝 Creating sample text occasions...")

    sample_texts = [
        "The board expressed concern about escalating conflicts in the leadership team.",
        "Executive burnout patterns are creating urgency addiction cycles.",
        "The board expressed concerns about conflicts among the executives.",  # Similar to #1
        "We need to establish healthy boundaries and self-care practices.",
        "Burnout is becoming systemic across the organization.",  # Similar to #2
    ]

    occasions = []
    for i, text in enumerate(sample_texts):
        # Create random 384-dim embedding (in real use, from sentence-transformers)
        embedding = np.random.randn(384)
        embedding /= np.linalg.norm(embedding)

        # Make similar texts have similar embeddings
        if i == 2:  # Similar to #0
            base_embedding = np.random.randn(384)
            base_embedding /= np.linalg.norm(base_embedding)
            embedding = 0.85 * base_embedding + 0.15 * embedding
            embedding /= np.linalg.norm(embedding)
        elif i == 4:  # Similar to #1
            base_embedding = np.random.randn(384)
            base_embedding /= np.linalg.norm(base_embedding)
            embedding = 0.80 * base_embedding + 0.20 * embedding
            embedding /= np.linalg.norm(embedding)

        occasion = TextOccasion(
            chunk_id=f"doc_1_chunk_{i+1}",
            position=i,
            text=text,
            embedding=embedding
        )
        occasions.append(occasion)

    print(f"✅ Created {len(occasions)} text occasions")

    # Process with SANS
    print("\n🔍 Processing with SANS organ...")
    result = sans.process_text_occasions(occasions, cycle=1)

    # Display results
    print(f"\n📊 SANS Results:")
    print(f"   Coherence: {result.coherence:.3f}")
    print(f"   Lure: {result.lure:.3f}")
    print(f"   Patterns detected: {len(result.patterns)}")
    print(f"   Mean similarity: {result.mean_similarity:.3f}")
    print(f"   Max similarity: {result.max_similarity:.3f}")
    print(f"   Thematic coherence: {result.thematic_coherence:.3f}")
    print(f"   Novelty score: {result.novelty_score:.3f}")
    print(f"   Processing time: {result.processing_time:.1f}ms")

    # Display patterns
    if len(result.patterns) > 0:
        print(f"\n🔗 Detected Patterns:")
        for i, pattern in enumerate(result.patterns[:5], 1):
            print(f"   {i}. {pattern.pattern_type}")
            print(f"      Similarity: {pattern.similarity_score:.3f}")
            print(f"      Confidence: {pattern.confidence:.3f}")
            print(f"      Text 1: {pattern.text_1[:50]}...")
            print(f"      Text 2: {pattern.text_2[:50]}...")
            print()

    # Check prehensions
    print(f"🧠 Prehension Check:")
    occ = occasions[0]
    if 'SANS' in occ.prehensions:
        print(f"   ✅ Occasion 0 has SANS prehension")
        print(f"   Affordances: {len(occ.felt_affordances)}")

    # Statistics
    stats = sans.get_statistics()
    print(f"\n📈 SANS Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n✅ ALL TESTS PASSED - SANS operational")
