"""
BOND Configuration - IFS Parts Relationships Detection (Text Domain)

Configuration parameters for the modular BOND organ adapted for organizational governance text processing.
Detects Internal Family Systems (IFS) parts language: managers, firefighters, exiles, and SELF-energy.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class BONDConfig:
    """Configuration for BOND Core Engine - Text Domain Adaptation"""

    # Core IFS parts detection settings
    parts_threshold: float = 0.60                    # Minimum threshold for parts detection (moderate)
    ifs_sensitivity: float = 0.75                    # Sensitivity to IFS parts language
    self_energy_amplification: float = 1.4           # SELF-energy signal amplification factor
    parts_relationship_strength: float = 0.80        # Cross-parts relationship detection

    # IFS parts keywords (learned & expanded via Hebbian memory)
    manager_keywords: List[str] = None               # Initialized in __post_init__
    firefighter_keywords: List[str] = None           # Initialized in __post_init__
    exile_keywords: List[str] = None                 # Initialized in __post_init__
    self_energy_keywords: List[str] = None           # Initialized in __post_init__

    # Mathematical coherence settings (Levin integration)
    cosmic_salience_threshold: float = 0.60          # Threshold for parts salience
    parts_coherence_weight: float = 0.75             # Weight for parts coherence
    self_energy_alignment: float = 0.80              # SELF-energy alignment factor

    # Vector35D enhancement settings (384-dim → 35-dim projection)
    vector35d_enhancement: bool = True               # Enable Vector35D IFS intelligence
    self_energy_boost: float = 1.6                   # Boost factor for SELF-energy dimensions
    parts_polarization_boost: float = 1.3            # Boost factor for parts polarization

    # Pattern detection settings (text domain)
    parts_language_cluster_radius: float = 0.20      # Cosine distance for parts clustering
    blending_detection_threshold: float = 0.75       # Threshold for parts blending detection
    unblending_window: int = 8                       # Sentence window for unblending detection

    # Performance optimization
    max_parts_patterns_per_conversation: int = 25    # Maximum parts patterns per conversation
    parts_history_limit: int = 75                    # Maximum parts history entries
    parts_memory_limit: int = 400                    # Maximum parts memory entries

    # Cross-organ collaboration weights (text domain)
    collaboration_patterns: Dict[str, float] = None

    # Neo4j integration (Phase 4) - for tracking parts relationships over time
    neo4j_enabled: bool = False                      # Enable Neo4j parts tracking (Phase 4)

    def __post_init__(self):
        """Initialize IFS parts patterns if not provided"""
        if self.manager_keywords is None:
            self.manager_keywords = [
                # Proactive protective
                'should', 'must', 'have to', 'need to', 'supposed to', 'ought to',
                'plan', 'organize', 'control', 'manage', 'prepare', 'prevent',
                'responsible', 'duty', 'obligation', 'requirement', 'expectation',
                'professional', 'competent', 'capable', 'effective', 'efficient',
                'perfect', 'flawless', 'ideal', 'proper', 'appropriate',
                # Organizational managers
                'protocol', 'procedure', 'policy', 'standard', 'guideline', 'rule'
            ]

        if self.firefighter_keywords is None:
            self.firefighter_keywords = [
                # Reactive protective (high urgency)
                'crisis', 'emergency', 'panic', 'overwhelmed', 'cant take',
                'breaking point', 'collapse', 'shutdown', 'explosion', 'meltdown',
                'numb', 'detach', 'disconnect', 'escape', 'avoid', 'distract',
                'fix it now', 'make it stop', 'urgent', 'immediate', 'asap',
                # Firefighter behaviors
                'overwork', 'burnout', 'exhaustion', 'push through', 'power through',
                'blame', 'lash out', 'rage', 'attack', 'defend', 'justify'
            ]

        if self.exile_keywords is None:
            self.exile_keywords = [
                # Burdened parts (carrying trauma)
                'worthless', 'inadequate', 'failure', 'not good enough', 'defective',
                'abandoned', 'rejected', 'unwanted', 'invisible', 'forgotten',
                'shame', 'guilt', 'humiliation', 'embarrassment', 'disgrace',
                'hurt', 'wounded', 'damaged', 'broken', 'scarred',
                'helpless', 'powerless', 'trapped', 'stuck', 'frozen',
                # Exile emotional states
                'sad', 'lonely', 'afraid', 'terrified', 'despair', 'hopeless'
            ]

        if self.self_energy_keywords is None:
            self.self_energy_keywords = [
                # 8 Cs of SELF (Schwartz IFS)
                'calm', 'clarity', 'curiosity', 'compassion', 'confidence',
                'courage', 'creativity', 'connectedness',
                # SELF-led language
                'grounded', 'centered', 'present', 'aware', 'mindful', 'witnessing',
                'spacious', 'open', 'receptive', 'allowing', 'accepting',
                'curious', 'wondering', 'exploring', 'noticing', 'observing',
                # SELF-to-part language
                'part of me', 'sense of', 'aware of', 'notice', 'invite', 'welcome',
                'appreciate', 'honor', 'respect', 'value', 'trust'
            ]

        if self.collaboration_patterns is None:
            self.collaboration_patterns = {
                'NDAM': 0.90,  # Parts language correlates with urgency (firefighters)
                'SANS': 0.85,  # Parts language has semantic patterns (repetition)
                'RNX': 0.95,   # Parts language indicates reenactment (strong coupling)
                'EO': 0.95,    # Parts language correlates with polyvagal state (very strong)
                'CARD': 0.75   # Parts language determines response depth (SELF-led = deeper)
            }

    def get_parts_type_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get settings for different IFS parts types (text domain)"""
        return {
            'manager': {
                'min_activation': 0.5,
                'max_activation': 1.5,
                'collaboration_boost': 0.25,
                'self_distance': 0.25    # Managers relatively close to SELF
            },
            'firefighter': {
                'min_activation': 0.7,
                'max_activation': 2.0,
                'collaboration_boost': 0.40,
                'self_distance': 0.50    # Firefighters far from SELF (blended)
            },
            'exile': {
                'min_activation': 0.6,
                'max_activation': 1.8,
                'collaboration_boost': 0.35,
                'self_distance': 0.60    # Exiles in shadow (far from SELF)
            },
            'self_energy': {
                'min_activation': 0.8,
                'max_activation': 1.0,
                'collaboration_boost': 0.50,
                'self_distance': 0.00    # SELF is the reference point
            },
            'parts_blending': {
                'min_activation': 0.65,
                'max_activation': 1.7,
                'collaboration_boost': 0.30,
                'self_distance': 0.45    # Blending indicates distance from SELF
            },
            'unblending_process': {
                'min_activation': 0.70,
                'max_activation': 1.5,
                'collaboration_boost': 0.45,
                'self_distance': 0.15    # Unblending moves toward SELF
            }
        }

    def get_vector35d_dimensions(self) -> Dict[str, int]:
        """Get Vector35D dimensions used by BOND (IFS projection)"""
        return {
            'self_energy_density': 6,      # Enhanced SELF-energy detection
            'parts_polarization': 14,      # Enhanced parts conflict/harmony
            'ifs_coherence': 19,           # Enhanced IFS language coherence
            'blending_intensity': 24,      # Enhanced parts blending detection
            'unblending_momentum': 31      # Enhanced unblending process tracking
        }

    def get_hebbian_learning_config(self) -> Dict[str, Any]:
        """Configuration for Hebbian learning of IFS parts patterns"""
        return {
            'learn_new_parts_language': True,        # Learn novel IFS parts language
            'parts_confidence_threshold': 0.75,      # Min confidence for parts retention
            'pattern_reinforcement_rate': 0.05,      # R-matrix coupling rate (η)
            'pattern_decay_rate': 0.01,              # R-matrix decay rate (δ)
            'max_learned_parts_patterns': 600,       # Maximum learned IFS patterns
            'cross_organ_coupling': {
                'EO': 0.95,    # BOND ↔ EO (parts ↔ polyvagal state, very strong)
                'RNX': 0.95,   # BOND ↔ RNX (parts ↔ reenactment detection, very strong)
                'NDAM': 0.90   # BOND ↔ NDAM (parts ↔ urgency, strong)
            }
        }

    def get_self_distance_config(self) -> Dict[str, Any]:
        """Configuration for SELF-distance calculation (Math Addendum lines 421-535)"""
        return {
            'base_distance_formula': 'embedding_cosine',  # Base distance from SELF-energy keywords
            'polyvagal_modifier': True,                   # Add polyvagal state modifier (EO coupling)
            'self_energy_range': (0.00, 0.15),            # Core SELF range
            'manager_range': (0.15, 0.35),                # Proactive protectors
            'blending_range': (0.35, 0.50),               # Blended parts
            'firefighter_range': (0.40, 0.60),            # Reactive protectors
            'exile_range': (0.50, 0.75),                  # Burdened parts (shadow)
            'trauma_range': (0.75, 1.00)                  # Deep trauma (far from SELF)
        }


# Default configuration instance
DEFAULT_BOND_CONFIG = BONDConfig()
