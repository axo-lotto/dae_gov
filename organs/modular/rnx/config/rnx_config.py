"""
RNX Configuration - Trauma Reenactment Detection (Text Domain)

Configuration parameters for the modular RNX organ adapted for organizational governance text processing.
Detects trauma reenactment patterns via 4-layer detection strategy (Hebbian, Template, Neo4j, FAISS).
Goal: Minimize LLM reliance through learned pattern recognition.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class RNXConfig:
    """Configuration for RNX Core Engine - Text Domain Adaptation"""

    # Core reenactment detection settings
    reenactment_threshold: float = 0.65              # Minimum threshold for reenactment detection
    trauma_sensitivity: float = 0.80                 # Sensitivity to trauma patterns
    pattern_recognition_boost: float = 1.5           # Reenactment pattern amplification factor
    temporal_loop_awareness: float = 0.85            # Cross-temporal pattern recognition

    # 4-Layer Detection Strategy (from Math Addendum lines 721-857)
    layer1_hebbian_threshold: float = 0.80           # Layer 1: Hebbian memory confidence
    layer2_template_threshold: float = 0.70          # Layer 2: Template matching confidence
    layer3_graph_threshold: float = 0.65             # Layer 3: Neo4j graph confidence
    layer4_faiss_threshold: float = 0.60             # Layer 4: FAISS semantic confidence

    # Reenactment pattern templates (learned & expanded via Hebbian memory)
    reenactment_templates: List[str] = None          # Initialized in __post_init__

    # Mathematical coherence settings (Levin integration)
    cosmic_salience_threshold: float = 0.65          # Threshold for reenactment salience
    trauma_coherence_weight: float = 0.85            # Weight for trauma coherence
    temporal_loop_alignment: float = 0.75            # Temporal loop alignment factor

    # Vector35D enhancement settings (384-dim → 35-dim projection)
    vector35d_enhancement: bool = True               # Enable Vector35D reenactment intelligence
    reenactment_density_boost: float = 1.7           # Boost factor for reenactment dimensions
    temporal_loop_boost: float = 1.5                 # Boost factor for temporal loop detection

    # Pattern detection settings (text domain)
    reenactment_cluster_radius: float = 0.18         # Cosine distance for reenactment clustering
    repetition_loop_threshold: int = 2               # Repetition count for loop detection
    temporal_window: int = 20                        # Sentence window for temporal pattern detection

    # Performance optimization
    max_reenactment_patterns_per_conversation: int = 15  # Maximum reenactment patterns
    reenactment_history_limit: int = 100             # Maximum reenactment history entries
    template_memory_limit: int = 200                 # Maximum reenactment templates

    # Cross-organ collaboration weights (text domain)
    collaboration_patterns: Dict[str, float] = None

    # Layer enablement (Phase 4: Neo4j, FAISS integration)
    layer1_hebbian_enabled: bool = True              # Layer 1: Always enabled (core learning)
    layer2_template_enabled: bool = True             # Layer 2: Always enabled (predefined patterns)
    layer3_graph_enabled: bool = False               # Layer 3: Enable in Phase 4 (Neo4j)
    layer4_faiss_enabled: bool = False               # Layer 4: Enable in Phase 4 (FAISS)

    # LLM reduction tracking
    llm_fallback_rate_baseline: float = 0.75         # Week 1 baseline (75% LLM-primary)
    llm_fallback_rate_target_week12: float = 0.25    # Week 12 target (25% LLM-primary)
    llm_fallback_rate_target_week24: float = 0.20    # Week 24 target (20% LLM-primary)

    def __post_init__(self):
        """Initialize reenactment pattern templates if not provided"""
        if self.reenactment_templates is None:
            self.reenactment_templates = [
                # Organizational reenactment patterns
                'urgency_loop',           # Chronic crisis → urgency addiction
                'scapegoating',           # Blame shifting → victim/persecutor roles
                'triangulation',          # 3-person conflict → drama triangle
                'rescue_burnout',         # Over-functioning → collapse cycle
                'conflict_avoidance',     # Suppress → explosion cycle
                'power_struggle',         # Domination ↔ submission loop
                'perfectionism_loop',     # Impossible standards → failure → shame
                'abandonment_reenactment', # Fear of rejection → self-sabotage
                'control_rebellion',      # Over-control → rebellion → punishment
                'victim_persecutor',      # Karpman drama triangle roles

                # IFS-informed reenactment patterns (BOND coupling)
                'manager_exhaustion',     # Manager burnout → firefighter takeover
                'firefighter_spiral',     # Reactive protection → escalation
                'exile_flooding',         # Exile breakthrough → system overwhelm
                'parts_war',              # Internal conflict externalized

                # Temporal patterns (NDAM coupling)
                'crisis_addiction',       # Urgency as baseline (firefighter dominance)
                'deadline_panic',         # Last-minute crisis (manager → firefighter)
                'burnout_cycle',          # Over-functioning → collapse → repeat

                # Polyvagal patterns (EO coupling)
                'freeze_response',        # Dorsal shutdown → immobilization
                'fight_flight',           # Sympathetic activation → aggression/flee
                'fawn_response',          # Appeasement → self-abandonment
                'dissociation',           # Dorsal disconnect → numbness
            ]

        if self.collaboration_patterns is None:
            self.collaboration_patterns = {
                'NDAM': 0.85,  # Reenactment correlates with urgency (crisis addiction)
                'SANS': 0.90,  # Reenactment has strong semantic patterns (repetition)
                'BOND': 0.95,  # Reenactment indicates IFS parts activation (very strong)
                'EO': 0.95,    # Reenactment correlates with polyvagal state (very strong)
                'CARD': 0.70   # Reenactment determines response (trauma-informed depth)
            }

    def get_reenactment_type_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get settings for different reenactment types (text domain)"""
        return {
            'urgency_loop': {
                'min_confidence': 0.70,
                'max_confidence': 1.0,
                'collaboration_boost': 0.35,
                'llm_needed': False
            },
            'scapegoating': {
                'min_confidence': 0.75,
                'max_confidence': 1.0,
                'collaboration_boost': 0.40,
                'llm_needed': False
            },
            'triangulation': {
                'min_confidence': 0.65,
                'max_confidence': 1.0,
                'collaboration_boost': 0.30,
                'llm_needed': False
            },
            'rescue_burnout': {
                'min_confidence': 0.70,
                'max_confidence': 1.0,
                'collaboration_boost': 0.35,
                'llm_needed': False
            },
            'parts_war': {
                'min_confidence': 0.80,
                'max_confidence': 1.0,
                'collaboration_boost': 0.45,
                'llm_needed': False
            },
            'novel_pattern': {
                'min_confidence': 0.50,
                'max_confidence': 0.75,
                'collaboration_boost': 0.20,
                'llm_needed': True   # LLM fallback for novel patterns
            }
        }

    def get_vector35d_dimensions(self) -> Dict[str, int]:
        """Get Vector35D dimensions used by RNX (reenactment projection)"""
        return {
            'reenactment_density': 9,      # Enhanced reenactment pattern density
            'temporal_loop_coherence': 13, # Enhanced temporal loop coherence
            'trauma_salience': 21,         # Enhanced trauma pattern recognition
            'pattern_repetition': 26,      # Enhanced repetition detection
            'polyvagal_coupling': 32       # Enhanced polyvagal-reenactment coupling
        }

    def get_hebbian_learning_config(self) -> Dict[str, Any]:
        """Configuration for Hebbian learning of reenactment patterns (Layer 1)"""
        return {
            'learn_new_reenactments': True,          # Learn novel reenactment patterns
            'reenactment_confidence_threshold': 0.80, # Min confidence for pattern retention
            'pattern_reinforcement_rate': 0.05,      # R-matrix coupling rate (η)
            'pattern_decay_rate': 0.01,              # R-matrix decay rate (δ)
            'max_learned_reenactments': 800,         # Maximum learned reenactment patterns
            'cross_organ_coupling': {
                'EO': 0.95,    # RNX ↔ EO (reenactment ↔ polyvagal state, very strong)
                'BOND': 0.95,  # RNX ↔ BOND (reenactment ↔ parts activation, very strong)
                'SANS': 0.90   # RNX ↔ SANS (reenactment ↔ semantic patterns, strong)
            }
        }

    def get_layer_detection_config(self) -> Dict[str, Any]:
        """Configuration for 4-layer reenactment detection strategy"""
        return {
            'layer1_hebbian': {
                'enabled': self.layer1_hebbian_enabled,
                'confidence_threshold': self.layer1_hebbian_threshold,
                'description': 'Learned patterns from accumulated knowledge',
                'expected_hit_rate_week1': 0.10,
                'expected_hit_rate_week12': 0.50,
                'expected_hit_rate_week24': 0.60
            },
            'layer2_template': {
                'enabled': self.layer2_template_enabled,
                'confidence_threshold': self.layer2_template_threshold,
                'description': 'Predefined trauma reenactment templates',
                'expected_hit_rate': 0.25    # Constant (predefined patterns)
            },
            'layer3_graph': {
                'enabled': self.layer3_graph_enabled,
                'confidence_threshold': self.layer3_graph_threshold,
                'description': 'Neo4j relationship-based detection',
                'expected_hit_rate_after_phase4': 0.15
            },
            'layer4_faiss': {
                'enabled': self.layer4_faiss_enabled,
                'confidence_threshold': self.layer4_faiss_threshold,
                'description': 'FAISS historical corpus similarity',
                'expected_hit_rate_after_phase4': 0.10
            },
            'llm_fallback': {
                'description': 'LLM fallback for novel patterns',
                'baseline_rate': self.llm_fallback_rate_baseline,
                'target_rate_week12': self.llm_fallback_rate_target_week12,
                'target_rate_week24': self.llm_fallback_rate_target_week24
            }
        }


# Default configuration instance
DEFAULT_RNX_CONFIG = RNXConfig()
