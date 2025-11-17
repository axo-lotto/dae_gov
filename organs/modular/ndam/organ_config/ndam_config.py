"""
NDAM Configuration - Narrative Dynamics & Urgency Detection (Text Domain)

Configuration parameters for the modular NDAM organ adapted for organizational governance text processing.
Detects narrative urgency, crisis patterns, and temporal dynamics in conversations.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class NDAMConfig:
    """Configuration for NDAM Core Engine - Text Domain Adaptation"""

    # Core urgency detection settings
    urgency_threshold: float = 0.75                  # Minimum threshold for urgency detection (high)
    narrative_sensitivity: float = 0.7               # Sensitivity to narrative dynamics
    crisis_amplification: float = 1.3                # Crisis signal amplification factor
    temporal_awareness: float = 0.8                  # Cross-temporal pattern recognition

    # Text domain urgency keywords (learned & expanded via Hebbian memory)
    urgency_keywords: List[str] = None               # Initialized in __post_init__

    # Mathematical coherence settings (Levin integration)
    cosmic_salience_threshold: float = 0.65          # Threshold for narrative salience
    narrative_coherence_weight: float = 0.8          # Weight for narrative coherence
    temporal_constraint_alignment: float = 0.6       # Temporal constraint alignment factor

    # Vector35D enhancement settings (384-dim → 35-dim semantic)
    vector35d_enhancement: bool = True               # Enable Vector35D narrative intelligence
    urgency_density_boost: float = 1.5               # Boost factor for urgency-related dimensions
    temporal_pattern_boost: float = 1.3              # Boost factor for temporal dimensions

    # Pattern detection settings (text domain)
    keyword_match_radius: float = 2.0                # Semantic radius for keyword matching
    repetition_threshold: int = 3                    # Repetition count for pattern detection
    escalation_detection_window: int = 5             # Sentence window for escalation detection

    # Performance optimization
    max_urgency_patterns_per_conversation: int = 20  # Maximum urgency patterns per conversation
    narrative_history_limit: int = 50                # Maximum narrative history entries
    keyword_memory_limit: int = 300                  # Maximum keyword memory entries

    # Cross-organ collaboration weights (text domain)
    collaboration_patterns: Dict[str, float] = None

    def __post_init__(self):
        """Initialize text domain patterns if not provided"""
        if self.urgency_keywords is None:
            self.urgency_keywords = [
                # Crisis indicators (organizational)
                'urgent', 'crisis', 'emergency', 'critical', 'immediate',
                'escalating', 'breaking down', 'collapse', 'failing',

                # Temporal pressure
                'deadline', 'overdue', 'behind schedule', 'running out', 'too late',
                'time-sensitive', 'now', 'asap', 'right away',

                # Emotional intensity (organizational)
                'exhausted', 'overwhelmed', 'burned out', 'cant take', 'breaking point',
                'desperate', 'panic', 'anxiety', 'stress',

                # Organizational dysfunction
                'conflict', 'tension', 'blame', 'scapegoat', 'toxic',
                'dysfunction', 'breakdown', 'rupture', 'fragmentation',

                # IFS firefighter activation (high urgency, protective)
                'must fix', 'have to', 'need to', 'should', 'supposed to',
                'responsibility', 'obligation', 'duty', 'requirement',

                # 🆕 PERSONAL/THERAPEUTIC CRISIS (coherent attractors for exile energy)
                # Fear/Terror
                'terrified', 'terror', 'fear', 'scared', 'frightened', 'afraid',

                # Crushing/Suffocating
                'crushing', 'crushed', 'suffocating', 'suffocate', 'cant breathe',
                'breathe', 'choking', 'drowning',

                # Spiraling/Losing Control
                'spiraling', 'spiral', 'spinning', 'losing control', 'out of control',
                'falling apart', 'unraveling',

                # Shame/Exile (IFS exile energy)
                'ashamed', 'shame', 'humiliated', 'humiliation', 'worthless',
                'defective', 'broken', 'damaged',

                # Shutdown/Dissociation (dorsal vagal)
                'shut down', 'shutdown', 'numb', 'frozen', 'disconnected',
                'empty', 'void', 'nothing', 'collapse',

                # Rage/Destructive Energy
                'rage', 'furious', 'destroy', 'explode', 'violence',

                # Abandonment/Isolation
                'abandoned', 'alone', 'isolated', 'rejected', 'unwanted'
            ]

        if self.collaboration_patterns is None:
            self.collaboration_patterns = {
                'SANS': 0.75,  # Urgency creates semantic focus (high similarity detection)
                'BOND': 0.90,  # Urgency activates IFS firefighters (strong coupling)
                'RNX': 0.85,   # Urgency indicates potential reenactment (trauma loop)
                'EO': 0.95,    # Urgency correlates with polyvagal state (sympathetic/dorsal)
                'CARD': 0.70   # Urgency determines response detail (brevity under pressure)
            }

    def get_urgency_type_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get settings for different urgency types (text domain)"""
        return {
            'crisis_urgency': {
                'min_strength': 0.7,
                'max_strength': 2.0,
                'collaboration_boost': 0.3,
                'response_priority': 'immediate'
            },
            'temporal_pressure': {
                'min_strength': 0.6,
                'max_strength': 1.5,
                'collaboration_boost': 0.25,
                'response_priority': 'high'
            },
            'emotional_intensity': {
                'min_strength': 0.5,
                'max_strength': 1.8,
                'collaboration_boost': 0.35,
                'response_priority': 'high'
            },
            'organizational_dysfunction': {
                'min_strength': 0.6,
                'max_strength': 1.7,
                'collaboration_boost': 0.3,
                'response_priority': 'medium'
            },
            'firefighter_activation': {
                'min_strength': 0.7,
                'max_strength': 2.0,
                'collaboration_boost': 0.4,
                'response_priority': 'immediate'
            },
            'narrative_escalation': {
                'min_strength': 0.65,
                'max_strength': 1.6,
                'collaboration_boost': 0.25,
                'response_priority': 'medium'
            }
        }

    def get_vector35d_dimensions(self) -> Dict[str, int]:
        """Get Vector35D dimensions used by NDAM (semantic projection)"""
        return {
            'urgency_density': 8,        # Enhanced urgency keyword density
            'temporal_coherence': 12,    # Enhanced temporal pattern coherence
            'emotional_intensity': 20,   # Enhanced emotional signal strength
            'narrative_momentum': 25,    # Enhanced narrative escalation detection
            'crisis_salience': 30        # Enhanced crisis pattern recognition
        }

    def get_hebbian_learning_config(self) -> Dict[str, Any]:
        """Configuration for Hebbian learning of urgency patterns"""
        return {
            'learn_new_keywords': True,           # Learn novel urgency indicators
            'keyword_confidence_threshold': 0.80, # Min confidence for keyword retention
            'pattern_reinforcement_rate': 0.05,   # R-matrix coupling rate (η)
            'pattern_decay_rate': 0.01,           # R-matrix decay rate (δ)
            'max_learned_keywords': 500,          # Maximum learned keyword vocabulary
            'cross_organ_coupling': {
                'EO': 0.85,   # NDAM ↔ EO (urgency ↔ polyvagal state)
                'BOND': 0.80, # NDAM ↔ BOND (urgency ↔ firefighter activation)
                'RNX': 0.75   # NDAM ↔ RNX (urgency ↔ reenactment detection)
            }
        }


# Default configuration instance
DEFAULT_NDAM_CONFIG = NDAMConfig()
