"""
EO Configuration - Polyvagal State Detection (Text Domain)

Configuration parameters for the modular EO organ adapted for organizational governance text processing.
Detects polyvagal states (ventral vagal, sympathetic, dorsal vagal) via language patterns and semantic signals.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class EOConfig:
    """Configuration for EO Core Engine - Text Domain Adaptation"""

    # Core polyvagal detection settings
    polyvagal_threshold: float = 0.50                # Minimum threshold for polyvagal detection (moderate-low)
    state_sensitivity: float = 0.85                  # Sensitivity to polyvagal state shifts
    autonomic_amplification: float = 1.6             # Polyvagal signal amplification factor
    state_transition_awareness: float = 0.90         # Cross-state transition recognition

    # Polyvagal state keywords (learned & expanded via Hebbian memory)
    ventral_vagal_keywords: List[str] = None         # Safe & social (initialized in __post_init__)
    sympathetic_keywords: List[str] = None           # Fight/flight (initialized in __post_init__)
    dorsal_vagal_keywords: List[str] = None          # Shutdown/freeze (initialized in __post_init__)

    # Mathematical coherence settings (Levin integration)
    cosmic_salience_threshold: float = 0.55          # Threshold for polyvagal salience
    autonomic_coherence_weight: float = 0.90         # Weight for autonomic coherence (high)
    state_alignment_factor: float = 0.80             # State alignment factor

    # Vector35D enhancement settings (384-dim → 35-dim projection)
    vector35d_enhancement: bool = True               # Enable Vector35D polyvagal intelligence
    polyvagal_density_boost: float = 1.8             # Boost factor for polyvagal dimensions (highest)
    state_transition_boost: float = 1.6              # Boost factor for state transition detection

    # Pattern detection settings (text domain)
    state_cluster_radius: float = 0.22               # Cosine distance for state clustering
    state_persistence_threshold: int = 3             # Persistence count for state confirmation
    transition_detection_window: int = 6             # Sentence window for transition detection

    # Performance optimization
    max_polyvagal_patterns_per_conversation: int = 35 # Maximum polyvagal patterns
    state_history_limit: int = 150                   # Maximum state history entries
    polyvagal_memory_limit: int = 600                # Maximum polyvagal memory entries

    # Cross-organ collaboration weights (text domain)
    collaboration_patterns: Dict[str, float] = None

    def __post_init__(self):
        """Initialize polyvagal state patterns if not provided"""
        if self.ventral_vagal_keywords is None:
            self.ventral_vagal_keywords = [
                # Safe & social (Porges polyvagal theory)
                'safe', 'calm', 'grounded', 'centered', 'present', 'connected',
                'curious', 'open', 'receptive', 'engaged', 'playful', 'joyful',
                'relaxed', 'peaceful', 'ease', 'comfortable', 'secure', 'trusting',
                'collaborative', 'cooperative', 'attuned', 'responsive', 'empathic',
                # SELF-energy (8 Cs - ventral vagal overlap)
                'clarity', 'compassion', 'confidence', 'courage', 'creativity', 'connectedness',
                # Organizational ventral vagal
                'consensus', 'alignment', 'synergy', 'flow', 'resonance', 'harmony'
            ]

        if self.sympathetic_keywords is None:
            self.sympathetic_keywords = [
                # Fight/flight (mobilization)
                'urgent', 'crisis', 'panic', 'anxiety', 'stress', 'overwhelmed',
                'agitated', 'restless', 'hypervigilant', 'on edge', 'tense', 'pressured',
                'fight', 'defend', 'attack', 'confront', 'resist', 'push back',
                'flight', 'avoid', 'escape', 'withdraw', 'flee', 'run away',
                'angry', 'rage', 'fury', 'explosive', 'reactive', 'aggressive',
                'frantic', 'manic', 'racing', 'spinning', 'chaotic', 'scattered',
                # Organizational sympathetic
                'conflict', 'confrontation', 'escalation', 'tension', 'pressure', 'deadline',
                'firefighting', 'crisis mode', 'emergency', 'urgency', 'red alert'
            ]

        if self.dorsal_vagal_keywords is None:
            self.dorsal_vagal_keywords = [
                # Shutdown/freeze (immobilization)
                'numb', 'frozen', 'stuck', 'paralyzed', 'immobilized', 'trapped',
                'shutdown', 'collapse', 'exhaustion', 'burnout', 'depleted', 'drained',
                'dissociated', 'detached', 'disconnected', 'absent', 'foggy', 'spacey',
                'hopeless', 'despair', 'defeated', 'helpless', 'powerless', 'resigned',
                'apathetic', 'indifferent', 'empty', 'void', 'nothing', 'dead',
                'depressed', 'heavy', 'weighted', 'sinking', 'falling', 'drowning',
                # Organizational dorsal vagal
                'burnout', 'attrition', 'turnover', 'absenteeism', 'presenteeism',
                'disengagement', 'apathy', 'complacency', 'resignation', 'surrender'
            ]

        if self.collaboration_patterns is None:
            self.collaboration_patterns = {
                'NDAM': 0.95,  # Polyvagal state correlates with urgency (very strong)
                'SANS': 0.80,  # Polyvagal state has semantic patterns
                'BOND': 0.95,  # Polyvagal state correlates with IFS parts (very strong)
                'RNX': 0.95,   # Polyvagal state indicates reenactment (very strong)
                'CARD': 0.85   # Polyvagal state determines response (ventral=detailed, dorsal=brief)
            }

    def get_polyvagal_state_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get settings for different polyvagal states (text domain)"""
        return {
            'ventral_vagal': {
                'min_activation': 0.6,
                'max_activation': 1.0,
                'collaboration_boost': 0.40,
                'self_distance': 0.00,       # Ventral vagal IS SELF-energy
                'optimal_response': 'deep'   # Detailed, nuanced, trauma-informed
            },
            'sympathetic': {
                'min_activation': 0.7,
                'max_activation': 2.0,
                'collaboration_boost': 0.35,
                'self_distance': 0.45,       # Sympathetic is firefighter activation
                'optimal_response': 'brief'  # Clear, actionable, immediate
            },
            'dorsal_vagal': {
                'min_activation': 0.6,
                'max_activation': 1.8,
                'collaboration_boost': 0.30,
                'self_distance': 0.70,       # Dorsal vagal is shutdown (far from SELF)
                'optimal_response': 'minimal' # Gentle, spacious, no pressure
            },
            'mixed_state': {
                'min_activation': 0.5,
                'max_activation': 1.5,
                'collaboration_boost': 0.25,
                'self_distance': 0.50,       # Mixed state is transitional
                'optimal_response': 'adaptive' # Flexible based on predominant state
            },
            'state_transition': {
                'min_activation': 0.65,
                'max_activation': 1.6,
                'collaboration_boost': 0.35,
                'self_distance': 0.35,       # Transition toward SELF (ventral)
                'optimal_response': 'supportive' # Support the transition process
            }
        }

    def get_vector35d_dimensions(self) -> Dict[str, int]:
        """Get Vector35D dimensions used by EO (polyvagal projection)"""
        return {
            'polyvagal_density': 7,        # Enhanced polyvagal state density (highest boost)
            'autonomic_coherence': 11,     # Enhanced autonomic nervous system coherence
            'state_salience': 16,          # Enhanced state detection salience
            'transition_momentum': 23,     # Enhanced state transition detection
            'self_alignment': 29           # Enhanced SELF-energy alignment (ventral vagal)
        }

    def get_hebbian_learning_config(self) -> Dict[str, Any]:
        """Configuration for Hebbian learning of polyvagal patterns"""
        return {
            'learn_new_polyvagal_patterns': True,    # Learn novel polyvagal language
            'polyvagal_confidence_threshold': 0.85,  # Min confidence for pattern retention
            'pattern_reinforcement_rate': 0.05,      # R-matrix coupling rate (η)
            'pattern_decay_rate': 0.01,              # R-matrix decay rate (δ)
            'max_learned_polyvagal_patterns': 700,   # Maximum learned polyvagal patterns
            'cross_organ_coupling': {
                'BOND': 0.95,  # EO ↔ BOND (polyvagal ↔ IFS parts, very strong)
                'RNX': 0.95,   # EO ↔ RNX (polyvagal ↔ reenactment, very strong)
                'NDAM': 0.95   # EO ↔ NDAM (polyvagal ↔ urgency, very strong)
            }
        }

    def get_self_distance_modifier_config(self) -> Dict[str, Any]:
        """Configuration for polyvagal modifier in SELF-distance calculation"""
        return {
            'ventral_vagal_modifier': 0.0,     # No distance from SELF (ventral IS SELF)
            'sympathetic_modifier': +0.3,      # Moderate distance (mobilization)
            'dorsal_vagal_modifier': +0.5,     # High distance (immobilization/shutdown)
            'mixed_state_modifier': +0.2,      # Low-moderate distance (transitional)
            'transition_toward_ventral': -0.1, # Moving toward SELF (negative = closer)
            'transition_away_ventral': +0.2    # Moving away from SELF (positive = further)
        }


# Default configuration instance
DEFAULT_EO_CONFIG = EOConfig()
