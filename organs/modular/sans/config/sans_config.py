"""
SANS Configuration - Semantic Similarity Detection (Text Domain)

Configuration parameters for the modular SANS organ adapted for organizational governance text processing.
Detects semantic patterns, similarity relationships, and meaning-based connections in 384-dim embedding space.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SANSConfig:
    """Configuration for SANS Core Engine - Text Domain Adaptation"""

    # Core similarity detection settings
    similarity_threshold: float = 0.70               # Minimum threshold for semantic similarity (high)
    semantic_sensitivity: float = 0.8                # Sensitivity to semantic nuances
    pattern_recognition_boost: float = 1.2           # Semantic pattern amplification factor
    embedding_coherence: float = 0.85                # Cross-embedding coherence strength

    # 384-dim embedding settings (sentence-transformers)
    embedding_dim: int = 384                         # Semantic embedding dimensionality
    cosine_similarity_method: str = 'normalized'     # 'normalized' or 'raw'
    similarity_aggregation: str = 'weighted_mean'    # 'mean', 'weighted_mean', 'max', 'min'

    # Mathematical coherence settings (Levin integration)
    cosmic_salience_threshold: float = 0.70          # Threshold for semantic salience
    semantic_coherence_weight: float = 0.85          # Weight for semantic coherence
    universal_similarity_alignment: float = 0.65     # Universal similarity alignment factor

    # Vector35D enhancement settings (384-dim → 35-dim projection)
    vector35d_enhancement: bool = True               # Enable Vector35D semantic intelligence
    similarity_density_boost: float = 1.4            # Boost factor for similarity-related dimensions
    pattern_coherence_boost: float = 1.3             # Boost factor for pattern coherence

    # Pattern detection settings (text domain)
    semantic_cluster_radius: float = 0.15            # Cosine distance for clustering (0-1 scale)
    repetition_similarity_threshold: float = 0.85    # Threshold for repetition detection
    thematic_coherence_window: int = 10              # Sentence window for theme detection

    # Performance optimization
    max_similarity_patterns_per_conversation: int = 30  # Maximum similarity patterns per conversation
    semantic_history_limit: int = 100                # Maximum semantic history entries
    embedding_cache_limit: int = 500                 # Maximum cached embeddings

    # Cross-organ collaboration weights (text domain)
    collaboration_patterns: Dict[str, float] = None

    # FAISS integration (Phase 4)
    faiss_enabled: bool = False                      # Enable FAISS semantic search (Phase 4)
    faiss_index_type: str = 'IndexFlatIP'            # FAISS index type (inner product)
    faiss_nprobe: int = 10                           # FAISS search probes

    def __post_init__(self):
        """Initialize text domain patterns if not provided"""
        if self.collaboration_patterns is None:
            self.collaboration_patterns = {
                'NDAM': 0.75,  # Similarity reinforces urgency patterns (semantic coherence)
                'BOND': 0.85,  # Similarity detects IFS parts relationships (semantic affinity)
                'RNX': 0.90,   # Similarity identifies reenactment patterns (strong coupling)
                'EO': 0.80,    # Similarity correlates with polyvagal resonance
                'CARD': 0.65   # Similarity determines response complexity (matching depth)
            }

    def get_similarity_type_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get settings for different similarity types (text domain)"""
        return {
            'exact_repetition': {
                'min_similarity': 0.95,
                'max_distance': 0.05,
                'collaboration_boost': 0.2,
                'confidence_multiplier': 1.5
            },
            'thematic_resonance': {
                'min_similarity': 0.75,
                'max_distance': 0.25,
                'collaboration_boost': 0.3,
                'confidence_multiplier': 1.2
            },
            'semantic_echo': {
                'min_similarity': 0.70,
                'max_distance': 0.30,
                'collaboration_boost': 0.25,
                'confidence_multiplier': 1.1
            },
            'conceptual_affinity': {
                'min_similarity': 0.65,
                'max_distance': 0.35,
                'collaboration_boost': 0.2,
                'confidence_multiplier': 1.0
            },
            'reenactment_pattern': {
                'min_similarity': 0.80,
                'max_distance': 0.20,
                'collaboration_boost': 0.4,
                'confidence_multiplier': 1.6
            },
            'parts_language_consistency': {
                'min_similarity': 0.85,
                'max_distance': 0.15,
                'collaboration_boost': 0.35,
                'confidence_multiplier': 1.4
            }
        }

    def get_vector35d_dimensions(self) -> Dict[str, int]:
        """Get Vector35D dimensions used by SANS (semantic projection)"""
        return {
            'semantic_density': 5,         # Enhanced semantic pattern density
            'similarity_coherence': 10,    # Enhanced similarity relationship coherence
            'thematic_consistency': 18,    # Enhanced thematic pattern consistency
            'embedding_salience': 22,      # Enhanced semantic salience detection
            'pattern_resonance': 28        # Enhanced pattern recognition strength
        }

    def get_hebbian_learning_config(self) -> Dict[str, Any]:
        """Configuration for Hebbian learning of semantic patterns"""
        return {
            'learn_new_patterns': True,              # Learn novel semantic patterns
            'pattern_confidence_threshold': 0.85,    # Min confidence for pattern retention
            'similarity_reinforcement_rate': 0.05,   # R-matrix coupling rate (η)
            'similarity_decay_rate': 0.01,           # R-matrix decay rate (δ)
            'max_learned_patterns': 1000,            # Maximum learned semantic patterns
            'cross_organ_coupling': {
                'RNX': 0.90,   # SANS ↔ RNX (similarity ↔ reenactment detection)
                'BOND': 0.85,  # SANS ↔ BOND (similarity ↔ parts language)
                'NDAM': 0.75   # SANS ↔ NDAM (similarity ↔ urgency patterns)
            }
        }

    def get_faiss_config(self) -> Dict[str, Any]:
        """Configuration for FAISS semantic search (Phase 4)"""
        return {
            'index_type': self.faiss_index_type,
            'dimension': self.embedding_dim,
            'nprobe': self.faiss_nprobe,
            'k_neighbors': 5,                        # Top-k similar conversations
            'distance_metric': 'cosine',             # Cosine similarity
            'index_refresh_interval': 10,            # Rebuild index every N conversations
            'similarity_threshold_for_retrieval': 0.70  # Min similarity for retrieval
        }


# Default configuration instance
DEFAULT_SANS_CONFIG = SANSConfig()
