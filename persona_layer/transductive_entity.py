#!/usr/bin/env python3
"""
Transductive Entity - Phase 1.8 TSK Integration
================================================

Entities as transductive occasions with felt-state fingerprints.

Each entity (person, relationship, fact) is not just static data but a
living transductive process with:
- Felt-state context (when/how entity was introduced)
- Prehensive history (how organs interpreted entity mentions)
- Relational affinity (connections to other entities)
- Satisfaction trajectory (successful/unsuccessful references)

This allows DAE to differentiate "Alice" (mentioned in crisis) from
"Alice" (mentioned in joy) and treat them with appropriate nuance.

Based on:
- ActualOccasion structure (transductive/actual_occasion.py)
- NexusTransductionState (persona_layer/nexus_transduction_state.py)
- TSK architecture (Takuan-Stiegler-Kairos)

Date: November 14, 2025
Phase: 1.8 - Entity Extraction with Transductive Enrichment
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import numpy as np


@dataclass
class TransductiveFeltContext:
    """
    Felt-state context when entity was mentioned.

    Captures the organism's state during entity extraction,
    creating a "felt fingerprint" for this entity reference.
    """
    # Organism state at extraction
    timestamp: str
    turn_number: int

    # Felt states (from organism processing)
    polyvagal_state: str = "unknown"  # ventral_vagal, sympathetic, dorsal_vagal
    self_distance: float = 0.5  # BOND SELF-distance (0=exiled, 1=Self-led)
    urgency_level: float = 0.0  # NDAM crisis urgency (0-1)

    # Nexus context
    dominant_nexuses: List[str] = field(default_factory=list)  # Top 3 nexuses active
    nexus_category: str = "UNKNOWN"  # GUT, PSYCHE, SOCIAL_CONTEXT
    is_crisis_moment: bool = False  # Crisis-oriented vs Constitutional

    # V0 convergence context
    v0_energy: float = 0.5  # Appetition satisfaction (0=satisfied, 1=unsatisfied)
    satisfaction: float = 0.5  # Overall satisfaction (0-1)
    convergence_cycles: int = 1  # How many cycles to converge

    # Active organs (57D signature snapshot)
    active_organs: List[str] = field(default_factory=list)
    organ_signature_snapshot: Optional[List[float]] = None  # 57D vector

    # Transduction pathway context
    transduction_mechanism: Optional[str] = None  # How nexus formed
    transduction_pathway: Optional[str] = None  # 9 primary pathways
    healing_trajectory: bool = False  # Healing vs Crisis trajectory


@dataclass
class EntityRelation:
    """
    Relationship to another entity.

    Examples:
    - "Alice" -> related_to: "ET", relation_type: "child_of"
    - "Alice" -> related_to: "Jaime", relation_type: "sibling"
    """
    related_entity_id: str  # ID of related entity
    relation_type: str  # "child_of", "sibling", "parent_of", "colleague", etc.
    strength: float = 1.0  # Relationship strength (0-1)
    first_mentioned: str = ""  # When relation was first established
    last_confirmed: str = ""  # Last time relation was referenced


@dataclass
class EntityPrehension:
    """
    How organs "prehended" (interpreted) this entity mention.

    Tracks which organs activated strongly when entity was mentioned,
    creating a prehensive signature for this entity.
    """
    timestamp: str
    turn_number: int

    # Organ activations during this mention
    organ_activations: Dict[str, float] = field(default_factory=dict)  # organ_name -> activation
    top_organs: List[str] = field(default_factory=list)  # Top 3 activated organs

    # Semantic atoms activated
    activated_atoms: Dict[str, List[str]] = field(default_factory=dict)  # organ -> [atoms]

    # User's emotional state during mention (inferred)
    inferred_user_emotion: Optional[str] = None  # joy, stress, neutral, etc.
    user_satisfaction: Optional[float] = None  # Did user seem satisfied with response?


@dataclass
class TransductiveEntity:
    """
    Entity as transductive occasion - not static data but living process.

    Represents a person, relationship, fact, or preference with:
    - Core identity (name, type, value)
    - Felt-state fingerprints (context of each mention)
    - Prehensive history (how organism interpreted mentions)
    - Relational web (connections to other entities)
    - Satisfaction trajectory (successful/failed references)

    This allows differentiation: "Alice" mentioned in crisis ≠ "Alice" in joy.
    """

    # === CORE IDENTITY ===
    entity_id: str  # Unique ID (auto-generated)
    entity_type: str  # "person", "relationship", "fact", "preference"

    # Primary data
    name: Optional[str] = None  # For person entities
    value: Optional[Any] = None  # For fact/preference entities
    role: Optional[str] = None  # "father", "child", "colleague", etc.

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_mentioned: str = field(default_factory=lambda: datetime.now().isoformat())
    mention_count: int = 1

    # === TRANSDUCTIVE CONTEXT ===

    # Felt-state fingerprints (one per mention)
    felt_contexts: List[TransductiveFeltContext] = field(default_factory=list)

    # Prehensive history (how organs interpreted this entity)
    prehensions: List[EntityPrehension] = field(default_factory=list)

    # === RELATIONAL WEB ===

    # Connections to other entities
    relations: List[EntityRelation] = field(default_factory=list)

    # Affinity to other entities (learned from co-occurrence)
    entity_affinities: Dict[str, float] = field(default_factory=dict)  # entity_id -> affinity

    # === SATISFACTION TRAJECTORY ===

    # Did mentioning this entity lead to positive outcomes?
    satisfaction_history: List[float] = field(default_factory=list)  # Per mention
    average_satisfaction: float = 0.5

    # Confidence in entity data (decreases if contradicted)
    confidence: float = 1.0

    # === DIFFERENTIATION METADATA ===

    # Felt signature (composite of all mentions)
    composite_polyvagal_bias: Optional[str] = None  # Most common polyvagal state
    composite_urgency_level: float = 0.0  # Average urgency when mentioned
    composite_nexus_category: Optional[str] = None  # Most common nexus category

    # Crisis vs Healing association
    crisis_mentions: int = 0  # Mentioned during crisis
    healing_mentions: int = 0  # Mentioned during healing

    # === ADDITIONAL METADATA ===

    # Source of extraction
    source_text_snippets: List[str] = field(default_factory=list)  # Original text
    extraction_confidence: float = 1.0  # How confident was extraction?

    # User feedback
    user_corrected: bool = False  # Did user correct entity info?
    correction_history: List[Dict[str, Any]] = field(default_factory=list)

    def add_mention(
        self,
        felt_context: TransductiveFeltContext,
        prehension: Optional[EntityPrehension] = None,
        source_text: Optional[str] = None,
        satisfaction: Optional[float] = None
    ):
        """
        Record a new mention of this entity.

        Updates:
        - mention_count
        - last_mentioned
        - felt_contexts
        - prehensions
        - satisfaction_history
        - composite signatures
        """
        self.mention_count += 1
        self.last_mentioned = datetime.now().isoformat()

        # Add felt context
        self.felt_contexts.append(felt_context)

        # Add prehension if provided
        if prehension:
            self.prehensions.append(prehension)

        # Add source text
        if source_text:
            self.source_text_snippets.append(source_text)

        # Add satisfaction
        if satisfaction is not None:
            self.satisfaction_history.append(satisfaction)
            self.average_satisfaction = np.mean(self.satisfaction_history)

        # Update composite signatures
        self._update_composite_signatures()

        # Track crisis vs healing
        if felt_context.is_crisis_moment:
            self.crisis_mentions += 1
        elif felt_context.healing_trajectory:
            self.healing_mentions += 1

    def _update_composite_signatures(self):
        """Update composite felt signatures from all mentions."""
        if not self.felt_contexts:
            return

        # Most common polyvagal state
        polyvagal_counts = {}
        for ctx in self.felt_contexts:
            state = ctx.polyvagal_state
            polyvagal_counts[state] = polyvagal_counts.get(state, 0) + 1

        if polyvagal_counts:
            self.composite_polyvagal_bias = max(polyvagal_counts, key=polyvagal_counts.get)

        # Average urgency
        urgency_levels = [ctx.urgency_level for ctx in self.felt_contexts]
        self.composite_urgency_level = np.mean(urgency_levels) if urgency_levels else 0.0

        # Most common nexus category
        nexus_counts = {}
        for ctx in self.felt_contexts:
            cat = ctx.nexus_category
            nexus_counts[cat] = nexus_counts.get(cat, 0) + 1

        if nexus_counts:
            self.composite_nexus_category = max(nexus_counts, key=nexus_counts.get)

    def add_relation(self, related_entity_id: str, relation_type: str, strength: float = 1.0):
        """Add a relationship to another entity."""
        # Check if relation already exists
        for rel in self.relations:
            if rel.related_entity_id == related_entity_id and rel.relation_type == relation_type:
                # Update existing relation
                rel.strength = max(rel.strength, strength)
                rel.last_confirmed = datetime.now().isoformat()
                return

        # Create new relation
        relation = EntityRelation(
            related_entity_id=related_entity_id,
            relation_type=relation_type,
            strength=strength,
            first_mentioned=datetime.now().isoformat(),
            last_confirmed=datetime.now().isoformat()
        )
        self.relations.append(relation)

    def get_differentiation_summary(self) -> str:
        """
        Get human-readable summary of entity's felt signature.

        Used for LLM context to provide nuanced understanding.
        """
        if not self.felt_contexts:
            return f"{self.name or self.value} (no context yet)"

        parts = []

        # Basic info
        if self.name:
            parts.append(f"'{self.name}'")

        # Mention frequency
        parts.append(f"mentioned {self.mention_count}x")

        # Felt signature
        if self.composite_polyvagal_bias and self.composite_polyvagal_bias != "unknown":
            parts.append(f"typically in {self.composite_polyvagal_bias} state")

        # Crisis vs healing
        if self.crisis_mentions > self.healing_mentions:
            parts.append("often in crisis context")
        elif self.healing_mentions > self.crisis_mentions:
            parts.append("often in healing context")

        # Urgency
        if self.composite_urgency_level > 0.7:
            parts.append("high urgency association")
        elif self.composite_urgency_level < 0.3:
            parts.append("calm association")

        # Satisfaction
        if self.average_satisfaction > 0.7:
            parts.append("positive reference pattern")
        elif self.average_satisfaction < 0.3:
            parts.append("challenging reference pattern")

        return " - ".join(parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'name': self.name,
            'value': self.value,
            'role': self.role,
            'created_at': self.created_at,
            'last_mentioned': self.last_mentioned,
            'mention_count': self.mention_count,
            'felt_contexts': [
                {
                    'timestamp': ctx.timestamp,
                    'turn_number': ctx.turn_number,
                    'polyvagal_state': ctx.polyvagal_state,
                    'self_distance': ctx.self_distance,
                    'urgency_level': ctx.urgency_level,
                    'dominant_nexuses': ctx.dominant_nexuses,
                    'nexus_category': ctx.nexus_category,
                    'is_crisis_moment': ctx.is_crisis_moment,
                    'v0_energy': ctx.v0_energy,
                    'satisfaction': ctx.satisfaction,
                    'convergence_cycles': ctx.convergence_cycles,
                    'active_organs': ctx.active_organs,
                    'transduction_mechanism': ctx.transduction_mechanism,
                    'healing_trajectory': ctx.healing_trajectory
                }
                for ctx in self.felt_contexts
            ],
            'prehensions': [
                {
                    'timestamp': p.timestamp,
                    'turn_number': p.turn_number,
                    'organ_activations': p.organ_activations,
                    'top_organs': p.top_organs,
                    'activated_atoms': p.activated_atoms,
                    'inferred_user_emotion': p.inferred_user_emotion,
                    'user_satisfaction': p.user_satisfaction
                }
                for p in self.prehensions
            ],
            'relations': [
                {
                    'related_entity_id': r.related_entity_id,
                    'relation_type': r.relation_type,
                    'strength': r.strength,
                    'first_mentioned': r.first_mentioned,
                    'last_confirmed': r.last_confirmed
                }
                for r in self.relations
            ],
            'entity_affinities': self.entity_affinities,
            'satisfaction_history': self.satisfaction_history,
            'average_satisfaction': self.average_satisfaction,
            'confidence': self.confidence,
            'composite_polyvagal_bias': self.composite_polyvagal_bias,
            'composite_urgency_level': float(self.composite_urgency_level),
            'composite_nexus_category': self.composite_nexus_category,
            'crisis_mentions': self.crisis_mentions,
            'healing_mentions': self.healing_mentions,
            'source_text_snippets': self.source_text_snippets,
            'extraction_confidence': self.extraction_confidence,
            'user_corrected': self.user_corrected,
            'correction_history': self.correction_history
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TransductiveEntity':
        """Load from dictionary."""
        # Reconstruct felt contexts
        felt_contexts = [
            TransductiveFeltContext(**ctx)
            for ctx in data.get('felt_contexts', [])
        ]

        # Reconstruct prehensions
        prehensions = [
            EntityPrehension(**p)
            for p in data.get('prehensions', [])
        ]

        # Reconstruct relations
        relations = [
            EntityRelation(**r)
            for r in data.get('relations', [])
        ]

        return cls(
            entity_id=data['entity_id'],
            entity_type=data['entity_type'],
            name=data.get('name'),
            value=data.get('value'),
            role=data.get('role'),
            created_at=data['created_at'],
            last_mentioned=data['last_mentioned'],
            mention_count=data['mention_count'],
            felt_contexts=felt_contexts,
            prehensions=prehensions,
            relations=relations,
            entity_affinities=data.get('entity_affinities', {}),
            satisfaction_history=data.get('satisfaction_history', []),
            average_satisfaction=data.get('average_satisfaction', 0.5),
            confidence=data.get('confidence', 1.0),
            composite_polyvagal_bias=data.get('composite_polyvagal_bias'),
            composite_urgency_level=data.get('composite_urgency_level', 0.0),
            composite_nexus_category=data.get('composite_nexus_category'),
            crisis_mentions=data.get('crisis_mentions', 0),
            healing_mentions=data.get('healing_mentions', 0),
            source_text_snippets=data.get('source_text_snippets', []),
            extraction_confidence=data.get('extraction_confidence', 1.0),
            user_corrected=data.get('user_corrected', False),
            correction_history=data.get('correction_history', [])
        )


def create_entity_from_extraction(
    name: Optional[str] = None,
    value: Optional[Any] = None,
    entity_type: str = "person",
    role: Optional[str] = None,
    felt_context: Optional[TransductiveFeltContext] = None,
    source_text: Optional[str] = None
) -> TransductiveEntity:
    """
    Create a TransductiveEntity from extracted data.

    Args:
        name: Entity name (for person entities)
        value: Entity value (for fact/preference entities)
        entity_type: Type of entity
        role: Role/relationship type
        felt_context: Felt-state context at extraction
        source_text: Original text snippet

    Returns:
        TransductiveEntity instance
    """
    entity_id = f"{entity_type}_{name or value}_{datetime.now().timestamp()}"

    entity = TransductiveEntity(
        entity_id=entity_id,
        entity_type=entity_type,
        name=name,
        value=value,
        role=role
    )

    # Add initial mention if context provided
    if felt_context:
        entity.add_mention(
            felt_context=felt_context,
            source_text=source_text
        )
    elif source_text:
        entity.source_text_snippets.append(source_text)

    return entity


if __name__ == '__main__':
    # Test transductive entity creation
    print("=== TRANSDUCTIVE ENTITY TEST ===\n")

    # Create felt context (crisis moment)
    crisis_context = TransductiveFeltContext(
        timestamp=datetime.now().isoformat(),
        turn_number=5,
        polyvagal_state="sympathetic",
        self_distance=0.2,  # Exiled
        urgency_level=0.8,  # High urgency
        dominant_nexuses=["Urgency", "Disruptive", "Protective"],
        nexus_category="GUT",
        is_crisis_moment=True,
        v0_energy=0.7,
        satisfaction=0.3,
        convergence_cycles=4,
        active_organs=["NDAM", "BOND", "EO"],
        transduction_mechanism="signal_inflation"
    )

    # Create entity with crisis context
    entity_alice = create_entity_from_extraction(
        name="Alice",
        entity_type="person",
        role="child",
        felt_context=crisis_context,
        source_text="Alice is having a hard time at school"
    )

    print(f"Entity ID: {entity_alice.entity_id}")
    print(f"Name: {entity_alice.name}")
    print(f"Mention count: {entity_alice.mention_count}")
    print(f"Crisis mentions: {entity_alice.crisis_mentions}")
    print(f"Composite urgency: {entity_alice.composite_urgency_level:.2f}")
    print(f"Differentiation summary: {entity_alice.get_differentiation_summary()}")
    print()

    # Add a healing mention
    healing_context = TransductiveFeltContext(
        timestamp=datetime.now().isoformat(),
        turn_number=10,
        polyvagal_state="ventral_vagal",
        self_distance=0.8,  # Self-led
        urgency_level=0.2,  # Low urgency
        dominant_nexuses=["Relational", "Innate", "Pre-Existing"],
        nexus_category="PSYCHE",
        is_crisis_moment=False,
        healing_trajectory=True,
        v0_energy=0.3,
        satisfaction=0.8,
        convergence_cycles=2,
        active_organs=["PRESENCE", "WISDOM", "LISTENING"],
        transduction_mechanism="mutual_satisfaction"
    )

    entity_alice.add_mention(
        felt_context=healing_context,
        source_text="Alice is doing much better now",
        satisfaction=0.9
    )

    print("After healing mention:")
    print(f"Mention count: {entity_alice.mention_count}")
    print(f"Crisis mentions: {entity_alice.crisis_mentions}")
    print(f"Healing mentions: {entity_alice.healing_mentions}")
    print(f"Average satisfaction: {entity_alice.average_satisfaction:.2f}")
    print(f"Differentiation summary: {entity_alice.get_differentiation_summary()}")
    print()

    print("✅ Transductive entity test complete!")
