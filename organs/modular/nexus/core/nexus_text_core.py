"""
NEXUS Core Engine - Text Domain Implementation (Neo4j Memory Management)
===========================================================================

Implements the NEXUS (Neo4j Entity eXtension Unified System) organ for entity-aware
memory access. Detects entity mentions and queries Neo4j knowledge graph for contextual
grounding.

Architecture:
- LLM-free entity detection via keyword matching + entity_organ_tracker patterns
- 7 semantic atom pools for entity-memory patterns
- Neo4j multi-hop queries for relationship context
- Entity-native prehension: felt affordances → mature memory propositions
- Hebbian learning: Learn when entity queries help (via satisfaction feedback)

Process Philosophy Integration:
- Actual Occasions: TextOccasion entities representing text chunks
- Prehensions: Entity mention detection + Neo4j context retrieval
- Concrescence: Multi-entity integration and context coherence
- Satisfaction: When coherent entity-memory pattern emerges
- Felt Affordances: Entity signals stored during prehension (immature V0)
- Mature Propositions: Post-convergence entity insights (mature V0 context)

Universal Organ Pattern (12th Organ):
1. process_text_occasions(occasions, cycle) → NEXUSResult
2. _detect_entity_mentions(occasions) → List[EntityMention]
3. _calculate_atom_activations(occasions) → Dict[str, float]
4. _calculate_coherence_metrics(mentions, atoms) → float
5. _query_neo4j_context(user_id, entities) → str
6. _calculate_lure(coherence, num_entities) → float

Author: DAE_HYPHAE_1 + Claude Code
Date: November 15, 2025
Status: Quick Win #9 - Phase 1 Implementation
"""

import time
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import numpy as np
from pathlib import Path

# Import text-native architecture
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from transductive.text_occasion import TextOccasion
from organs.modular.nexus.organ_config.nexus_config import (
    NEXUSConfig,
    DEFAULT_NEXUS_CONFIG,
    NEXUS_SEMANTIC_ATOMS
)

# Import Neo4j knowledge graph
try:
    from knowledge_base.neo4j_knowledge_graph import Neo4jKnowledgeGraph
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    print("⚠️  NEXUS: Neo4j knowledge graph not available")

# Import entity-organ tracker for pattern prediction
try:
    from persona_layer.entity_organ_tracker import EntityOrganTracker
    ENTITY_TRACKER_AVAILABLE = True
except ImportError:
    ENTITY_TRACKER_AVAILABLE = False


@dataclass
class EntityMention:
    """Detected entity mention in text."""

    entity_value: str                   # "Emma", "work", "Rich"
    entity_type: str                    # "Person", "Place", "Organization", "Concept"
    confidence: float                   # Detection confidence (0.0-1.0)
    text_position: int                  # Position in text occasions
    activation_atoms: List[str]         # Which NEXUS atoms activated
    activation_strength: float          # Combined atom activation strength

    # Neo4j query results (populated after query)
    relationships: List[Dict] = field(default_factory=list)
    mention_history: List[Dict] = field(default_factory=list)
    co_occurring_entities: List[str] = field(default_factory=list)

    # Entity-organ pattern prediction (from entity_organ_tracker)
    predicted_organ_pattern: Optional[Dict[str, float]] = None
    predicted_polyvagal_state: Optional[str] = None
    predicted_v0_energy: Optional[float] = None


@dataclass
class NEXUSResult:
    """Result of NEXUS memory organ processing (universal organ output)."""

    coherence: float                    # Entity-memory pattern coherence (0.0-1.0)
    entity_mentions: List[EntityMention]  # All detected entities
    lure: float                         # Appetition pull toward memory context
    processing_time_ms: float           # Processing latency

    # Entity context for LLM (⭐ KEY OUTPUT)
    entity_context_string: str          # Formatted entity context from Neo4j
    entity_context_salience: float      # How relevant is entity context (0.0-1.0)

    # Semantic atoms for nexus formation (like other 11 organs)
    semantic_atoms: Dict[str, float]    # {atom_name: activation_strength}

    # Learning metadata
    entities_queried: List[str] = field(default_factory=list)
    query_depth: int = 2
    query_latency_ms: float = 0.0
    neo4j_available: bool = False


class NEXUSTextCore:
    """
    NEXUS organ: Neo4j memory management through semantic atom activation.

    Makes entity memory FELT through organ activations, not just retrieved.

    This is the 12th organ in the DAE organism architecture.
    """

    def __init__(
        self,
        config: NEXUSConfig = None,
        enable_neo4j: bool = True,
        enable_entity_tracker: bool = True
    ):
        """
        Initialize NEXUS organ.

        Args:
            config: NEXUS configuration (defaults to DEFAULT_NEXUS_CONFIG)
            enable_neo4j: Whether to enable Neo4j queries (default: True)
            enable_entity_tracker: Whether to use entity-organ patterns (default: True)
        """
        self.config = config or DEFAULT_NEXUS_CONFIG

        # Load semantic atoms
        self.atoms = NEXUS_SEMANTIC_ATOMS

        # Initialize Neo4j knowledge graph (if available)
        self.neo4j = None
        self.neo4j_available = False
        if enable_neo4j and NEO4J_AVAILABLE:
            try:
                self.neo4j = Neo4jKnowledgeGraph(
                    uri=self.config.neo4j_uri,
                    user=self.config.neo4j_user,
                    password=self.config.neo4j_password,
                    database=self.config.neo4j_database
                )
                self.neo4j_available = (self.neo4j.driver is not None)
                if self.neo4j_available:
                    print(f"   ✅ NEXUS: Neo4j connected ({self.config.neo4j_uri})")
            except Exception as e:
                print(f"   ⚠️  NEXUS: Neo4j connection failed: {e}")
                self.neo4j_available = False

        # Load entity-organ tracker for pattern prediction (if available)
        self.entity_tracker = None
        if enable_entity_tracker and ENTITY_TRACKER_AVAILABLE:
            try:
                self.entity_tracker = EntityOrganTracker(
                    storage_path=self.config.entity_tracker_path
                )
                print(f"   ✅ NEXUS: Entity-organ tracker loaded")
            except Exception as e:
                print(f"   ⚠️  NEXUS: Entity tracker unavailable: {e}")
                self.entity_tracker = None

    def process_text_occasions(
        self,
        occasions: List[TextOccasion],
        cycle: int = 0,
        context: Optional[Dict[str, Any]] = None
    ) -> NEXUSResult:
        """
        Process text occasions through NEXUS organ (universal organ interface).

        Steps:
        1. Detect entity mentions via semantic atom activation
        2. Calculate atom activations (7D entity-memory space)
        3. Calculate overall coherence
        4. Query Neo4j for entity context (if coherence > threshold)
        5. Predict entity patterns from entity-organ tracker
        6. Calculate lure (appetition toward memory context)
        7. Return NEXUSResult

        Args:
            occasions: List of TextOccasion objects (words/phrases)
            cycle: Current processing cycle (0 for single-pass)
            context: Processing context (user_id, conversation_id, etc.)

        Returns:
            NEXUSResult with entity mentions, coherence, and context string
        """
        start_time = time.time()
        context = context or {}
        user_id = context.get('user_id', 'default_user')

        # Step 1: Calculate semantic atom activations
        atom_activations = self._calculate_atom_activations(occasions)

        # Step 2: Detect entity mentions
        entity_mentions = self._detect_entity_mentions(occasions, user_id, atom_activations)

        # Step 3: Calculate overall coherence
        overall_coherence = self._calculate_coherence(atom_activations, entity_mentions)

        # Step 4: Query Neo4j for entity context (if coherence high enough)
        entity_context_string = ""
        entities_queried = []
        query_latency_ms = 0.0

        if overall_coherence > self.config.context_salience_threshold and self.neo4j_available:
            # NEXUS atoms strongly activated → query Neo4j for entity context
            query_start = time.time()

            try:
                entity_context_string = self.neo4j.build_entity_context_string(
                    user_id=user_id,
                    max_entities=self.config.max_entities
                )
                query_latency_ms = (time.time() - query_start) * 1000
                entities_queried = [em.entity_value for em in entity_mentions]
            except Exception as e:
                print(f"   ⚠️  NEXUS: Neo4j query failed: {e}")
                entity_context_string = ""

        # Step 5: Predict entity patterns from entity-organ tracker
        if self.entity_tracker and self.config.use_entity_patterns:
            self._enrich_entity_patterns(entity_mentions, user_id)

        # Step 6: Calculate lure (appetition toward memory context)
        lure = self._calculate_lure(overall_coherence, len(entity_mentions))

        # Step 7: Build result
        processing_time_ms = (time.time() - start_time) * 1000

        return NEXUSResult(
            coherence=overall_coherence,
            entity_mentions=entity_mentions,
            lure=lure,
            processing_time_ms=processing_time_ms,
            entity_context_string=entity_context_string,
            entity_context_salience=overall_coherence,
            semantic_atoms=atom_activations,
            entities_queried=entities_queried,
            query_depth=self.config.relationship_depth,
            query_latency_ms=query_latency_ms,
            neo4j_available=self.neo4j_available
        )

    def _calculate_atom_activations(
        self,
        occasions: List[TextOccasion]
    ) -> Dict[str, float]:
        """
        Calculate activation strength for each of 7 NEXUS semantic atoms.

        Each atom scans text for keyword matches and returns average activation.

        Args:
            occasions: List of text occasions (words/phrases)

        Returns:
            {atom_name: activation_strength} dict
        """
        # Join occasions into continuous text for keyword matching
        text = " ".join([occ.text for occ in occasions]).lower()

        activations = {}

        for atom_name, keywords in self.atoms.items():
            # Find all keyword matches in text
            matches = []
            for keyword, strength in keywords.items():
                if keyword in text:
                    matches.append(strength)

            # Average activation strength (or 0.0 if no matches)
            if matches:
                activations[atom_name] = float(np.mean(matches))

        return activations

    def _detect_entity_mentions(
        self,
        occasions: List[TextOccasion],
        user_id: str,
        atom_activations: Dict[str, float]
    ) -> List[EntityMention]:
        """
        Detect entity mentions via semantic atom keyword matching.

        Priority:
        1. Check entity_recall atoms for known entities (from entity_organ_tracker)
        2. Check other atoms for entity-memory patterns

        Args:
            occasions: List of text occasions
            user_id: User identifier
            atom_activations: Already-calculated atom activations

        Returns:
            List of detected EntityMention objects
        """
        mentions = []
        text = " ".join([occ.text for occ in occasions]).lower()

        # Get entity_recall keywords (these are potential entity values)
        entity_keywords = self.atoms.get('entity_recall', {})

        for keyword, strength in entity_keywords.items():
            if keyword in text:
                # Check if this is a known entity from entity_tracker
                is_known_entity = False
                entity_type = "Concept"  # Default

                if self.entity_tracker:
                    pattern = self.entity_tracker.get_entity_pattern(keyword)
                    if pattern and pattern.get('mention_count', 0) > 0:
                        # Known entity from past mentions!
                        is_known_entity = True
                        entity_type = pattern.get('entity_type', 'Person')

                # Determine which atoms activated for this entity
                activated_atoms = [
                    atom_name for atom_name, activation in atom_activations.items()
                    if activation > 0.0
                ]

                # Calculate combined activation strength
                combined_strength = np.mean([atom_activations.get(a, 0.0) for a in activated_atoms]) if activated_atoms else strength

                mentions.append(EntityMention(
                    entity_value=keyword,
                    entity_type=entity_type,
                    confidence=strength if is_known_entity else strength * 0.7,  # Lower confidence for unknown
                    text_position=0,  # Would be calculated from occasions in production
                    activation_atoms=activated_atoms,
                    activation_strength=combined_strength
                ))

        return mentions

    def _calculate_coherence(
        self,
        atom_activations: Dict[str, float],
        entity_mentions: List[EntityMention]
    ) -> float:
        """
        Calculate overall NEXUS coherence from atom activations + entity mentions.

        Coherence formula:
            coherence = 0.7 * mean(atom_activations) + 0.3 * entity_factor

        Where entity_factor = min(num_entities / 3, 1.0) to reward multi-entity contexts.

        Args:
            atom_activations: {atom_name: activation} dict
            entity_mentions: Detected entity mentions

        Returns:
            Overall coherence score (0.0-1.0)
        """
        # Component 1: Mean atom activation (70% weight)
        if atom_activations:
            mean_activation = np.mean(list(atom_activations.values()))
        else:
            mean_activation = 0.0

        # Component 2: Entity factor (30% weight)
        # Rewards conversations with multiple entities (richer context)
        num_entities = len(entity_mentions)
        entity_factor = min(num_entities / 3.0, 1.0)  # Cap at 3 entities

        # Weighted combination
        coherence = 0.7 * mean_activation + 0.3 * entity_factor

        return float(np.clip(coherence, 0.0, 1.0))

    def _calculate_lure(
        self,
        coherence: float,
        num_entities: int
    ) -> float:
        """
        Calculate appetition pull toward entity-memory context.

        Higher lure when:
        - High coherence (strong entity patterns detected)
        - Multiple entities (rich context web)

        Formula:
            lure = coherence * (0.7 + 0.3 * entity_factor)

        Args:
            coherence: Overall NEXUS coherence (0.0-1.0)
            num_entities: Number of entities detected

        Returns:
            Lure strength (0.0-1.0)
        """
        entity_factor = min(num_entities / 3.0, 1.0)  # Cap at 3 entities
        lure = coherence * (0.7 + 0.3 * entity_factor)
        return float(np.clip(lure, 0.0, 1.0))

    def _enrich_entity_patterns(
        self,
        entity_mentions: List[EntityMention],
        user_id: str
    ):
        """
        Enrich entity mentions with predicted patterns from entity-organ tracker.

        For each detected entity, query the tracker for:
        - Typical organ activation pattern
        - Typical polyvagal state
        - Typical V0 energy

        This allows NEXUS to PREDICT when entity context will help based on learned patterns.

        Args:
            entity_mentions: List of EntityMention objects (modified in-place)
            user_id: User identifier
        """
        if not self.entity_tracker:
            return

        for mention in entity_mentions:
            try:
                pattern = self.entity_tracker.get_entity_pattern(mention.entity_value)

                if pattern:
                    # Enrich mention with predicted patterns
                    mention.predicted_organ_pattern = pattern.get('organ_boosts', {})
                    mention.predicted_polyvagal_state = pattern.get('typical_polyvagal_state')
                    mention.predicted_v0_energy = pattern.get('typical_v0_energy')

            except Exception as e:
                # Non-critical - continue without enrichment
                continue


# Quick test
if __name__ == '__main__':
    print("🧪 Testing NEXUSTextCore...")

    # Initialize NEXUS organ
    nexus = NEXUSTextCore(enable_neo4j=False, enable_entity_tracker=False)

    # Create sample text occasions
    input_text = "I'm worried about Emma and her kindergarten transition"
    occasions = [
        TextOccasion(
            text=word,
            chunk_id=f"test_{i}",
            position=i,
            embedding=np.zeros(384)  # Dummy embedding for test
        )
        for i, word in enumerate(input_text.split())
    ]

    print(f"\nProcessing text: '{input_text}'")

    # Process occasions
    result = nexus.process_text_occasions(occasions, cycle=0, context={'user_id': 'test_user'})

    print(f"\n✅ NEXUS Processing Complete:")
    print(f"   Coherence: {result.coherence:.3f}")
    print(f"   Lure: {result.lure:.3f}")
    print(f"   Entities detected: {len(result.entity_mentions)}")
    for mention in result.entity_mentions:
        print(f"      - {mention.entity_value} ({mention.entity_type}): confidence={mention.confidence:.2f}")
    print(f"   Semantic atoms activated: {len(result.semantic_atoms)}")
    for atom, strength in sorted(result.semantic_atoms.items(), key=lambda x: x[1], reverse=True):
        print(f"      - {atom}: {strength:.3f}")
    print(f"   Processing time: {result.processing_time_ms:.1f}ms")
    print(f"   Neo4j available: {result.neo4j_available}")

    print("\n✅ NEXUSTextCore test complete!")
