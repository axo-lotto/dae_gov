"""
TextOccasion - Text-Native Actual Occasion (Whiteheadian Process Philosophy)

Entity-native implementation for organizational governance text processing.
Replaces grid-based ActualOccasion with discourse-aware text entities.

Architecture:
- Text chunks as fundamental units (not grid cells)
- Semantic neighbors (not spatial adjacency)
- Discourse roles and rhetorical positions (text-specific)
- Universal process philosophy lifecycle (prehension → concrescence → satisfaction)
- Emergent family classification via 35D felt signatures

Author: DAE-GOV Development Team
Created: November 10, 2025
Version: 1.0 (Text-Native Foundation)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import json
from pathlib import Path


@dataclass
class TextOccasion:
    """
    Text-native actual occasion following Whiteheadian process philosophy.

    Fundamental unit of text processing in DAE-GOV system. Each TextOccasion
    represents a meaningful chunk of governance text with:
    - Semantic identity (embedding)
    - Discourse structure (role, position)
    - Relational context (semantic neighbors)
    - Process lifecycle (prehension, concrescence, satisfaction)
    - Family membership (emergent classification)

    Key Differences from ActualOccasion (grid-domain):
    - 1D sequence position (not 2D grid coordinates)
    - Semantic neighbors (not spatial adjacency)
    - Discourse roles (not grid transformations)
    - Text-specific fields (rhetorical position, chunk hierarchy)
    """

    # === IDENTITY ===
    chunk_id: str                          # "doc_5_para_3_sent_2_chunk_1"
    position: int                          # Sequential position in text flow
    text: str                              # Original text chunk
    embedding: np.ndarray                  # 384-dim semantic vector (sentence-transformers)

    # === TEXT-SPECIFIC STRUCTURE ===
    # (not grid metaphors)
    discourse_role: Optional[str] = None           # "claim", "evidence", "question", "directive"
    rhetorical_position: Optional[str] = None      # "introduction", "body", "conclusion"
    chunk_hierarchy: Optional[Dict[str, int]] = None  # {"doc": 5, "para": 3, "sent": 2, "chunk": 1}

    # === SEMANTIC NEIGHBORS ===
    # (replaces grid adjacency)
    semantic_neighbors: List[str] = field(default_factory=list)  # chunk_ids with cosine > 0.7
    neighbor_similarities: Dict[str, float] = field(default_factory=dict)  # {chunk_id: similarity}

    # === UNIVERSAL PROCESS PHILOSOPHY ===
    # (from ActualOccasion, domain-agnostic)
    prehensions: Dict[str, Any] = field(default_factory=dict)  # {organ_name: prehension_data}
    satisfaction_level: float = 0.0                            # Convergence quality (0.0-1.0)
    convergence_cycles: int = 0                                # Cycles to reach satisfaction

    # === EMERGENT FAMILY CLASSIFICATION ===
    # (self-organizing via 35D felt signatures)
    family_id: Optional[str] = None        # e.g., "value_transform_family_1"
    family_confidence: float = 0.0         # Cosine similarity to family centroid
    felt_signature_35d: Optional[np.ndarray] = None  # 35D projection from Vector35D

    # === V0 ENERGY & REGIME ===
    # (from FFITTSSv0 architecture)
    v0_energy: float = 1.0                 # Current V0 energy (1.0 → ~0.3 during convergence)
    regime: Optional[str] = None           # "INITIALIZING", "CONVERGING", "STABLE", etc.

    # === TRAUMA-INFORMED FIELDS ===
    # (IFS + polyvagal + reenactment detection)
    self_distance: float = 0.5             # 0.0 (pure SELF) to 1.0 (deep trauma)
    polyvagal_state: Optional[str] = None  # "ventral_vagal", "sympathetic", "dorsal_vagal"
    detected_parts: List[str] = field(default_factory=list)  # ["manager", "exile"], etc.
    reenactment_patterns: List[str] = field(default_factory=list)  # ["urgency_loop"], etc.

    # === TSK GENEALOGY ===
    # (99.5% capture for complete observability)
    tsk_entry_id: Optional[str] = None     # Reference to TSK database entry
    processing_timestamp: Optional[float] = None  # Unix timestamp

    # === AFFORDANCES (Entity-Native Propositions) ===
    # (proto-propositions stored during prehension, matured post-convergence)
    felt_affordances: List[Dict[str, Any]] = field(default_factory=list)

    # === ENTITY-AWARE FIELDS ===
    # (November 14, 2025: Enable organism entity awareness during prehension)
    # Stored entities accessible to organs (user_name, family_members, preferences, etc.)
    known_entities: Dict[str, Any] = field(default_factory=dict)
    # Names/relationships detected in THIS occasion's text (e.g., ["Alice", "daughter"])
    entity_references: List[str] = field(default_factory=list)
    # Confidence that references match stored entities {reference: confidence}
    entity_match_confidence: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize derived fields and validate structure."""
        # Ensure embedding is numpy array
        if not isinstance(self.embedding, np.ndarray):
            if isinstance(self.embedding, list):
                self.embedding = np.array(self.embedding)
            else:
                raise ValueError(f"Embedding must be numpy array or list, got {type(self.embedding)}")

        # Validate embedding dimension (384-dim sentence-transformers)
        if self.embedding.shape[0] != 384:
            raise ValueError(f"Expected 384-dim embedding, got {self.embedding.shape[0]}")

        # Parse chunk_id to extract hierarchy if not provided
        if self.chunk_hierarchy is None and self.chunk_id:
            self.chunk_hierarchy = self._parse_chunk_id(self.chunk_id)

    def _parse_chunk_id(self, chunk_id: str) -> Dict[str, int]:
        """
        Parse chunk_id string to extract hierarchical structure.

        Example: "doc_5_para_3_sent_2_chunk_1" → {"doc": 5, "para": 3, "sent": 2, "chunk": 1}
        """
        parts = chunk_id.split('_')
        hierarchy = {}

        for i in range(0, len(parts), 2):
            if i + 1 < len(parts):
                level = parts[i]  # "doc", "para", "sent", "chunk"
                index = int(parts[i + 1])
                hierarchy[level] = index

        return hierarchy

    # ========================================================================
    # PREHENSION METHODS (Process Philosophy Lifecycle)
    # ========================================================================

    def add_organ_prehension(self, organ_name: str, organ_output: Dict[str, Any], cycle: int):
        """
        Store organ prehension during processing.

        Called by each organ (SANS, NDAM, BOND, RNX, EO, CARD) during organism
        processing cycle. Accumulates multi-organ perspective.

        Args:
            organ_name: "SANS", "NDAM", "BOND", etc.
            organ_output: {
                'coherence': float (0-1),
                'patterns': List[Dict],
                'lure': float,
                'processing_time': float,
                ...
            }
            cycle: Current convergence cycle number
        """
        if organ_name not in self.prehensions:
            self.prehensions[organ_name] = []

        # Store prehension with cycle context
        prehension_record = {
            'cycle': cycle,
            'coherence': organ_output.get('coherence', 0.0),
            'patterns': organ_output.get('patterns', []),
            'lure': organ_output.get('lure', 0.0),
            'processing_time': organ_output.get('processing_time', 0.0),
            'v0_energy': self.v0_energy  # Capture energy state at prehension time
        }

        self.prehensions[organ_name].append(prehension_record)

    def add_felt_affordance(
        self,
        organ_name: str,
        confidence: float,
        lure_intensity: float,
        pattern_type: Optional[str] = None,
        affordance_data: Optional[Dict[str, Any]] = None
    ):
        """
        Store felt affordance (proto-proposition) during prehension.

        Entity-native proposition strategy: Store felt affordances DURING organ
        processing (cycles 1-N), mature to full propositions POST-CONVERGENCE
        with mature V0 context.

        Args:
            organ_name: Source organ ("SANS", "BOND", etc.)
            confidence: Affordance strength (0-1)
            lure_intensity: Appetition strength (0-1)
            pattern_type: Optional pattern classification
            affordance_data: Additional context
        """
        affordance = {
            'position': self.position,
            'organ_name': organ_name,
            'confidence': confidence,
            'lure_intensity': lure_intensity,
            'pattern_type': pattern_type,
            'v0_energy': self.v0_energy,  # Immature energy (proto-proposition)
            'data': affordance_data or {}
        }

        self.felt_affordances.append(affordance)

    def mature_propositions(self, v0_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Mature felt affordances to full propositions POST-CONVERGENCE.

        Called after satisfaction convergence with mature V0 context:
        - Final energy (e.g., 0.29 vs initial 1.0)
        - Satisfaction level (e.g., 0.683)
        - Regime state ("COMMITTED")

        Returns:
            List of mature PropositionFeltInterpretation records
        """
        final_energy = v0_context.get('final_energy', self.v0_energy)
        satisfaction = v0_context.get('satisfaction', self.satisfaction_level)
        regime = v0_context.get('regime', self.regime)

        mature_propositions = []

        for affordance in self.felt_affordances:
            # Amplify confidence with mature V0 energy bonus
            energy_bonus = 1.0 - final_energy  # Lower energy = higher bonus (0.71 for energy=0.29)
            mature_confidence = affordance['confidence'] * (1.0 + energy_bonus * 0.3)

            # Modulate by satisfaction
            satisfaction_weight = satisfaction  # 0.683 → 68.3% weighting

            mature_prop = {
                'position': affordance['position'],
                'organ_name': affordance['organ_name'],
                'confidence': min(1.0, mature_confidence * satisfaction_weight),
                'lure_intensity': affordance['lure_intensity'],
                'pattern_type': affordance['pattern_type'],
                'immature_energy': affordance['v0_energy'],  # Original proto-energy
                'mature_energy': final_energy,               # Final mature energy
                'satisfaction': satisfaction,
                'regime': regime,
                'data': affordance['data']
            }

            mature_propositions.append(mature_prop)

        return mature_propositions

    def accumulate_affordance_salience(self) -> float:
        """
        Calculate total salience from all felt affordances.

        Used by organism to assess readiness for decision/convergence.
        Higher salience = stronger prehensive clarity.

        Returns:
            Total salience (sum of confidence × lure_intensity)
        """
        total_salience = 0.0

        for affordance in self.felt_affordances:
            confidence = affordance.get('confidence', 0.0)
            lure = affordance.get('lure_intensity', 0.0)
            total_salience += confidence * lure

        return total_salience

    # ========================================================================
    # SEMANTIC NEIGHBOR METHODS
    # ========================================================================

    def add_semantic_neighbor(self, chunk_id: str, similarity: float, threshold: float = 0.7):
        """
        Add semantic neighbor if similarity exceeds threshold.

        Replaces grid adjacency with semantic similarity graph.

        Args:
            chunk_id: Neighboring chunk ID
            similarity: Cosine similarity (0-1)
            threshold: Minimum similarity to consider neighbor (default 0.7)
        """
        if similarity >= threshold:
            if chunk_id not in self.semantic_neighbors:
                self.semantic_neighbors.append(chunk_id)
            self.neighbor_similarities[chunk_id] = similarity

    def get_top_neighbors(self, k: int = 5) -> List[Tuple[str, float]]:
        """
        Get top-k semantic neighbors sorted by similarity.

        Returns:
            List of (chunk_id, similarity) tuples
        """
        sorted_neighbors = sorted(
            self.neighbor_similarities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_neighbors[:k]

    # ========================================================================
    # FAMILY CLASSIFICATION METHODS
    # ========================================================================

    def assign_family(self, family_id: str, confidence: float, felt_signature: np.ndarray):
        """
        Assign this occasion to an emergent family.

        Called by OrganicFamilyManager after comparing 35D felt signature
        to existing family centroids.

        Args:
            family_id: Family identifier (e.g., "value_transform_family_1")
            confidence: Cosine similarity to family centroid
            felt_signature: 35D felt signature from Vector35D projection
        """
        self.family_id = family_id
        self.family_confidence = confidence
        self.felt_signature_35d = felt_signature

    def get_felt_signature(self) -> Optional[np.ndarray]:
        """
        Get 35D felt signature for family classification.

        Returns:
            35D numpy array or None if not yet computed
        """
        return self.felt_signature_35d

    # ========================================================================
    # TRAUMA-INFORMED METHODS
    # ========================================================================

    def update_self_distance(self, distance: float):
        """
        Update SELF-distance based on IFS parts + polyvagal state.

        Args:
            distance: 0.0 (pure SELF) to 1.0 (deep trauma)
        """
        self.self_distance = max(0.0, min(1.0, distance))

    def add_detected_part(self, part_name: str):
        """
        Add detected IFS part.

        Args:
            part_name: "manager", "firefighter", "exile", "SELF"
        """
        if part_name not in self.detected_parts:
            self.detected_parts.append(part_name)

    def add_reenactment_pattern(self, pattern: str):
        """
        Add detected reenactment pattern.

        Args:
            pattern: "urgency_loop", "scapegoating", etc.
        """
        if pattern not in self.reenactment_patterns:
            self.reenactment_patterns.append(pattern)

    # ========================================================================
    # SERIALIZATION METHODS
    # ========================================================================

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize to dictionary for TSK storage.

        Returns:
            Dictionary representation (JSON-serializable)
        """
        return {
            'chunk_id': self.chunk_id,
            'position': self.position,
            'text': self.text,
            'embedding': self.embedding.tolist(),  # Convert numpy to list
            'discourse_role': self.discourse_role,
            'rhetorical_position': self.rhetorical_position,
            'chunk_hierarchy': self.chunk_hierarchy,
            'semantic_neighbors': self.semantic_neighbors,
            'neighbor_similarities': self.neighbor_similarities,
            'prehensions': self.prehensions,
            'satisfaction_level': self.satisfaction_level,
            'convergence_cycles': self.convergence_cycles,
            'family_id': self.family_id,
            'family_confidence': self.family_confidence,
            'felt_signature_35d': self.felt_signature_35d.tolist() if self.felt_signature_35d is not None else None,
            'v0_energy': self.v0_energy,
            'regime': self.regime,
            'self_distance': self.self_distance,
            'polyvagal_state': self.polyvagal_state,
            'detected_parts': self.detected_parts,
            'reenactment_patterns': self.reenactment_patterns,
            'tsk_entry_id': self.tsk_entry_id,
            'processing_timestamp': self.processing_timestamp,
            'felt_affordances': self.felt_affordances
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextOccasion':
        """
        Deserialize from dictionary.

        Args:
            data: Dictionary from to_dict()

        Returns:
            TextOccasion instance
        """
        # Convert lists back to numpy arrays
        data['embedding'] = np.array(data['embedding'])
        if data.get('felt_signature_35d') is not None:
            data['felt_signature_35d'] = np.array(data['felt_signature_35d'])

        return cls(**data)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"TextOccasion("
            f"chunk_id='{self.chunk_id}', "
            f"position={self.position}, "
            f"family='{self.family_id}', "
            f"self_distance={self.self_distance:.2f}, "
            f"satisfaction={self.satisfaction_level:.2f})"
        )


# ========================================================================
# UTILITY FUNCTIONS
# ========================================================================

def create_text_occasions_from_chunks(
    chunks: List[Dict[str, Any]],
    embeddings: np.ndarray
) -> List[TextOccasion]:
    """
    Batch create TextOccasion entities from text chunks and embeddings.

    Args:
        chunks: List of chunk dicts with keys:
            - chunk_id: str
            - text: str
            - discourse_role: Optional[str]
            - rhetorical_position: Optional[str]
        embeddings: numpy array of shape (n_chunks, 384)

    Returns:
        List of TextOccasion instances
    """
    occasions = []

    for i, chunk in enumerate(chunks):
        occasion = TextOccasion(
            chunk_id=chunk['chunk_id'],
            position=i,
            text=chunk['text'],
            embedding=embeddings[i],
            discourse_role=chunk.get('discourse_role'),
            rhetorical_position=chunk.get('rhetorical_position')
        )
        occasions.append(occasion)

    return occasions


def compute_semantic_neighbors(
    occasions: List[TextOccasion],
    threshold: float = 0.7,
    max_neighbors: int = 10
):
    """
    Compute semantic neighbors for all occasions via cosine similarity.

    Modifies occasions in-place by adding semantic neighbors.

    Args:
        occasions: List of TextOccasion entities
        threshold: Minimum similarity to consider neighbor (default 0.7)
        max_neighbors: Maximum neighbors per occasion (default 10)
    """
    embeddings = np.array([occ.embedding for occ in occasions])

    # Normalize embeddings for cosine similarity
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Compute pairwise cosine similarities
    similarities = embeddings_norm @ embeddings_norm.T

    # Add neighbors to each occasion
    for i, occasion in enumerate(occasions):
        # Get indices sorted by similarity (excluding self)
        neighbor_indices = np.argsort(similarities[i])[::-1][1:max_neighbors+1]

        for j in neighbor_indices:
            similarity = similarities[i, j]
            if similarity >= threshold:
                occasion.add_semantic_neighbor(
                    occasions[j].chunk_id,
                    float(similarity),
                    threshold
                )


if __name__ == "__main__":
    """
    Basic validation test for TextOccasion class.
    """
    print("🧪 TextOccasion Validation Test")
    print("=" * 60)

    # Create sample text occasion
    sample_embedding = np.random.randn(384)
    sample_embedding /= np.linalg.norm(sample_embedding)  # Normalize

    occasion = TextOccasion(
        chunk_id="doc_1_para_1_sent_1_chunk_1",
        position=0,
        text="The board expressed concern about burnout patterns in the executive team.",
        embedding=sample_embedding,
        discourse_role="claim",
        rhetorical_position="introduction"
    )

    print(f"✅ Created: {occasion}")
    print(f"   Hierarchy: {occasion.chunk_hierarchy}")

    # Test prehension
    occasion.add_organ_prehension(
        "BOND",
        {
            'coherence': 0.75,
            'patterns': [{'type': 'urgency_detected'}],
            'lure': 0.8
        },
        cycle=1
    )
    print(f"✅ Added prehension: {len(occasion.prehensions)} organs")

    # Test affordance
    occasion.add_felt_affordance(
        organ_name="BOND",
        confidence=0.75,
        lure_intensity=0.8,
        pattern_type="urgency_pattern"
    )
    print(f"✅ Added affordance: {len(occasion.felt_affordances)} affordances")

    # Test maturation
    mature_props = occasion.mature_propositions({
        'final_energy': 0.29,
        'satisfaction': 0.683,
        'regime': 'COMMITTED'
    })
    print(f"✅ Matured propositions: {len(mature_props)} propositions")
    print(f"   Mature confidence: {mature_props[0]['confidence']:.3f}")

    # Test serialization
    occasion_dict = occasion.to_dict()
    occasion_restored = TextOccasion.from_dict(occasion_dict)
    print(f"✅ Serialization: restored={occasion_restored.chunk_id}")

    print("\n✅ ALL TESTS PASSED - TextOccasion operational")
