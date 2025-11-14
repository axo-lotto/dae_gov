"""
CARD Configuration - Response Scaling & Detail Calibration (Text Domain)

Configuration parameters for the modular CARD organ adapted for organizational governance text processing.
Calibrates response detail/depth based on polyvagal state, urgency, and SELF-energy presence.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class CARDConfig:
    """Configuration for CARD Core Engine - Text Domain Adaptation"""

    # Core response calibration settings
    calibration_threshold: float = 0.50              # Minimum threshold for calibration (moderate-low)
    detail_sensitivity: float = 0.70                 # Sensitivity to detail requirements
    depth_amplification: float = 1.2                 # Response depth amplification factor
    adaptive_scaling: float = 0.85                   # Cross-organ adaptive scaling strength

    # Response scale settings (text domain)
    minimal_response_length: int = 50                # Minimum response length (dorsal vagal)
    brief_response_length: int = 150                 # Brief response length (sympathetic)
    moderate_response_length: int = 300              # Moderate response length (default)
    detailed_response_length: int = 600              # Detailed response length (ventral vagal)
    comprehensive_response_length: int = 1000        # Comprehensive response length (SELF-led deep work)

    # Mathematical coherence settings (Levin integration)
    cosmic_salience_threshold: float = 0.50          # Threshold for calibration salience
    scaling_coherence_weight: float = 0.65           # Weight for scaling coherence
    adaptive_alignment_factor: float = 0.75          # Adaptive alignment factor

    # Vector35D enhancement settings (384-dim → 35-dim projection)
    vector35d_enhancement: bool = True               # Enable Vector35D calibration intelligence
    scaling_density_boost: float = 1.2               # Boost factor for scaling dimensions
    depth_calibration_boost: float = 1.3             # Boost factor for depth calibration

    # Pattern detection settings (text domain)
    calibration_window: int = 10                     # Sentence window for calibration assessment
    detail_consistency_threshold: float = 0.65       # Threshold for detail consistency
    adaptive_adjustment_rate: float = 0.15           # Rate of adaptive scaling adjustment

    # Performance optimization
    max_calibration_adjustments_per_conversation: int = 10  # Maximum calibration adjustments
    calibration_history_limit: int = 50              # Maximum calibration history entries
    scaling_memory_limit: int = 200                  # Maximum scaling memory entries

    # Cross-organ collaboration weights (text domain)
    collaboration_patterns: Dict[str, float] = None

    def __post_init__(self):
        """Initialize calibration patterns if not provided"""
        if self.collaboration_patterns is None:
            self.collaboration_patterns = {
                'NDAM': 0.70,  # Urgency determines response (urgent=brief, calm=detailed)
                'SANS': 0.65,  # Semantic complexity influences detail (simple=brief, complex=detailed)
                'BOND': 0.75,  # IFS parts determine depth (SELF-led=deep, firefighter=brief)
                'RNX': 0.70,   # Reenactment determines approach (trauma-informed depth)
                'EO': 0.85     # Polyvagal state determines scale (ventral=detailed, dorsal=minimal)
            }

    def get_response_scale_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get settings for different response scales (text domain)"""
        return {
            'minimal': {
                'target_length': self.minimal_response_length,
                'polyvagal_state': 'dorsal_vagal',
                'urgency_level': 'extreme',
                'self_distance': 0.70,
                'description': 'Gentle, spacious, no pressure (shutdown state)'
            },
            'brief': {
                'target_length': self.brief_response_length,
                'polyvagal_state': 'sympathetic',
                'urgency_level': 'high',
                'self_distance': 0.45,
                'description': 'Clear, actionable, immediate (mobilization state)'
            },
            'moderate': {
                'target_length': self.moderate_response_length,
                'polyvagal_state': 'mixed',
                'urgency_level': 'moderate',
                'self_distance': 0.30,
                'description': 'Balanced, adaptive, context-sensitive'
            },
            'detailed': {
                'target_length': self.detailed_response_length,
                'polyvagal_state': 'ventral_vagal',
                'urgency_level': 'low',
                'self_distance': 0.10,
                'description': 'Nuanced, trauma-informed, SELF-led'
            },
            'comprehensive': {
                'target_length': self.comprehensive_response_length,
                'polyvagal_state': 'ventral_vagal',
                'urgency_level': 'none',
                'self_distance': 0.05,
                'description': 'Deep exploration, IFS-informed, full SELF-energy'
            }
        }

    def get_calibration_rules(self) -> Dict[str, Dict[str, Any]]:
        """Get calibration rules based on organ signals"""
        return {
            # EO (polyvagal) dominates calibration
            'polyvagal_dominant': {
                'ventral_vagal': 'detailed',       # Safe → detailed response
                'sympathetic': 'brief',            # Activated → brief response
                'dorsal_vagal': 'minimal',         # Shutdown → minimal response
                'weight': 0.40
            },
            # BOND (IFS parts) modulates depth
            'parts_modulation': {
                'self_energy': 'comprehensive',    # SELF-led → comprehensive
                'manager': 'moderate',             # Manager → moderate
                'firefighter': 'brief',            # Firefighter → brief
                'exile': 'detailed',               # Exile → detailed (trauma-informed)
                'weight': 0.30
            },
            # NDAM (urgency) constrains length
            'urgency_constraint': {
                'extreme': 'minimal',              # Extreme urgency → minimal
                'high': 'brief',                   # High urgency → brief
                'moderate': 'moderate',            # Moderate urgency → moderate
                'low': 'detailed',                 # Low urgency → detailed
                'none': 'comprehensive',           # No urgency → comprehensive
                'weight': 0.20
            },
            # RNX (reenactment) adds trauma-informed depth
            'reenactment_depth': {
                'detected': 'detailed',            # Reenactment → trauma-informed depth
                'not_detected': 'default',         # No reenactment → default calibration
                'weight': 0.10
            }
        }

    def get_vector35d_dimensions(self) -> Dict[str, int]:
        """Get Vector35D dimensions used by CARD (calibration projection)"""
        return {
            'calibration_density': 4,      # Enhanced calibration pattern density
            'detail_coherence': 15,        # Enhanced detail requirement coherence
            'depth_salience': 27,          # Enhanced depth calibration detection
            'adaptive_scaling': 33,        # Enhanced adaptive scaling intelligence
            'response_optimization': 35    # Enhanced response optimization (last dimension)
        }

    def get_hebbian_learning_config(self) -> Dict[str, Any]:
        """Configuration for Hebbian learning of calibration patterns"""
        return {
            'learn_new_calibration_patterns': True,  # Learn novel calibration patterns
            'calibration_confidence_threshold': 0.70, # Min confidence for pattern retention
            'pattern_reinforcement_rate': 0.05,      # R-matrix coupling rate (η)
            'pattern_decay_rate': 0.01,              # R-matrix decay rate (δ)
            'max_learned_calibration_patterns': 400, # Maximum learned calibration patterns
            'cross_organ_coupling': {
                'EO': 0.85,    # CARD ↔ EO (calibration ↔ polyvagal state, strong)
                'BOND': 0.75,  # CARD ↔ BOND (calibration ↔ parts, moderate-strong)
                'NDAM': 0.70   # CARD ↔ NDAM (calibration ↔ urgency, moderate)
            }
        }

    def get_adaptive_scaling_config(self) -> Dict[str, Any]:
        """Configuration for adaptive response scaling"""
        return {
            'enable_adaptive_scaling': True,         # Enable real-time adaptive scaling
            'scaling_adjustment_rate': self.adaptive_adjustment_rate,
            'min_scale_factor': 0.5,                 # Minimum scale factor (50% of baseline)
            'max_scale_factor': 2.0,                 # Maximum scale factor (200% of baseline)
            'feedback_integration': True,            # Learn from conversation outcomes
            'organism_confidence_threshold': 0.75,   # Min confidence for adaptive adjustments
            'conversation_success_threshold': 0.70   # Min success rate for pattern retention
        }


# Default configuration instance
DEFAULT_CARD_CONFIG = CARDConfig()
