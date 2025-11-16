"""
NEXUS Organ Configuration
=========================

Configuration for the NEXUS (Neo4j Entity eXtension Unified System) organ.

The NEXUS organ makes entity memory FELT through semantic atom activation,
not just retrieved through database queries.

Philosophy:
- Memory through prehension, not lookup
- Entity context emerges organically from NEXUS coherence
- Neo4j as 12th organ - memory becomes felt intelligence

Author: DAE_HYPHAE_1 + Claude Code
Date: November 15, 2025
Status: Quick Win #9 - Phase 1 Implementation
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class NEXUSConfig:
    """
    Configuration for NEXUS organ processing.

    Neo4j credentials default to None to use environment variables from .env file.
    This allows seamless connection to both local and cloud (Aura) instances.
    """

    # Neo4j connection (defaults to None → reads from .env file)
    neo4j_uri: str = None
    neo4j_user: str = None
    neo4j_password: str = None
    neo4j_database: str = None

    # Entity detection thresholds
    entity_detection_threshold: float = 0.3  # Minimum atom activation to detect entity
    context_salience_threshold: float = 0.3  # Minimum coherence to query Neo4j

    # Neo4j query parameters
    max_entities: int = 10  # Max entities to include in context string
    relationship_depth: int = 2  # Multi-hop query depth (1-3)
    query_timeout_ms: float = 100.0  # Neo4j query timeout

    # Hebbian learning
    enable_learning: bool = True  # Learn when entity queries help
    learning_alpha: float = 0.15  # EMA learning rate (matches entity-organ tracker)

    # Entity-organ tracker integration
    entity_tracker_path: str = "persona_layer/state/active/entity_organ_associations.json"
    use_entity_patterns: bool = True  # Predict context needs from entity-organ patterns

    # Semantic atoms configuration
    atom_activation_decay: float = 0.8  # Decay for sequential atoms (Hebbian style)
    min_atoms_for_coherence: int = 2  # Minimum atoms to activate for coherent pattern


# Default configuration instance
DEFAULT_NEXUS_CONFIG = NEXUSConfig()


# NEXUS Semantic Atoms (7D Entity-Memory Space)
# These will be loaded into semantic_atoms.json eventually
NEXUS_SEMANTIC_ATOMS = {
    "entity_recall": {
        # Direct entity references (proper names - will be populated from entity tracker)
        "emma": 1.0, "lily": 1.0, "sofia": 1.0, "rich": 0.95, "alex": 0.95,

        # Relationship markers
        "daughter": 0.90, "son": 0.90, "partner": 0.85, "friend": 0.80,
        "mother": 0.90, "father": 0.90, "brother": 0.85, "sister": 0.85,
        "child": 0.90, "parent": 0.90,

        # Work entities
        "work": 0.75, "job": 0.75, "boss": 0.75, "company": 0.70, "colleague": 0.70,

        # Location entities
        "home": 0.65, "house": 0.65, "place": 0.60,

        # Pronouns (coreference markers)
        "she": 0.85, "he": 0.85, "they": 0.80, "her": 0.85, "him": 0.85, "them": 0.80,
        "there": 0.70, "that place": 0.75,

        # Entity-seeking language
        "remember": 0.75, "mentioned": 0.80, "told you about": 0.85,
        "talked about": 0.80, "you know": 0.70, "recall": 0.75
    },

    "relationship_depth": {
        # Relationship dynamics
        "relationship": 0.90, "connected": 0.85, "close": 0.80,
        "distant": 0.75, "estranged": 0.85,

        # Familial language
        "family": 0.95, "sibling": 0.85,

        # Relational complexity
        "complicated": 0.85, "tension": 0.80, "conflict": 0.75,
        "supportive": 0.80, "caring": 0.75,

        # Multi-hop triggers
        "everyone": 0.70, "whole family": 0.90, "all of them": 0.75,
        "everyone involved": 0.85, "circle": 0.70, "network": 0.75
    },

    "temporal_continuity": {
        # Temporal markers
        "last time": 0.90, "before": 0.85, "previously": 0.80, "earlier": 0.75,
        "used to": 0.85, "always": 0.80, "never": 0.75,

        # Change language
        "changed": 0.85, "different": 0.80, "now": 0.90, "anymore": 0.85,
        "still": 0.80, "lately": 0.85, "recently": 0.90,

        # History invocation
        "back then": 0.85, "in the past": 0.80, "when we first": 0.90,
        "remember when": 0.95, "history": 0.85, "timeline": 0.80
    },

    "co_occurrence": {
        # Conjunction language
        "and": 0.95, "with": 0.90, "together": 0.85, "both": 0.90,
        "all": 0.85,

        # Comparison language
        "compared to": 0.85, "unlike": 0.80, "different from": 0.75,
        "versus": 0.75, "instead of": 0.70,

        # Group language
        "team": 0.80, "group": 0.75, "us": 0.85, "we": 0.90,
        "they": 0.80, "together": 0.85
    },

    "salience_gradient": {
        # Importance markers
        "important": 0.90, "crucial": 0.85, "key": 0.80, "central": 0.85,
        "main": 0.80, "primary": 0.75,

        # Crisis/urgency with entities
        "worried about": 0.95, "scared for": 0.95, "anxious about": 0.90,
        "concerned about": 0.85, "fear for": 0.90,

        # Focus language
        "especially": 0.85, "particularly": 0.80, "mainly": 0.75,
        "most of all": 0.90, "above all": 0.85
    },

    "memory_coherence": {
        # Consistency checking
        "didn't I tell you": 0.95, "thought I mentioned": 0.90,
        "did I say": 0.85, "you know": 0.80,

        # Confusion markers
        "confused": 0.85, "forgot": 0.90, "can't remember": 0.95,
        "not sure": 0.80, "unclear": 0.75,

        # Correction language
        "actually": 0.85, "correction": 0.90, "I meant": 0.85,
        "not": 0.70, "wrong": 0.75, "misremembered": 0.90
    },

    "contextual_grounding": {
        # Grounding language
        "because of": 0.85, "due to": 0.80, "given that": 0.75,
        "considering": 0.80, "in context of": 0.85,

        # Backstory invocation
        "background": 0.80, "backstory": 0.85, "context": 0.90,
        "situation": 0.75, "history": 0.85,

        # Relational grounding
        "my": 0.95, "our": 0.90, "their": 0.85,  # Possessive pronouns
        "with": 0.85, "about": 0.80, "regarding": 0.75
    }
}


# Atom pool metadata
ATOM_METADATA = {
    "total_atoms": 7,
    "dimension": "7D",
    "field_type": "entity_memory",
    "description": "Entity-memory semantic atoms for NEXUS organ (Neo4j memory management)",
    "learning_mechanism": "EMA (alpha=0.15) + entity-organ tracker patterns",
    "integration": "12th organ - makes memory felt through prehension"
}
