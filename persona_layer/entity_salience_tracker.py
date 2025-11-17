"""
Entity Salience Tracker - 3-Tier Temporal Decay (FFITTSS Pattern)
==================================================================

Implements FFITTSS-inspired multi-scale salience tracking for entity memory.
Tracks what matters NOW through 3-tier EMA decay + staleness pruning.

Philosophy (FFITTSS Legacy):
- Local (α=0.05): Entity-specific fast adaptation (half-life: 13 turns)
- Family (α=0.1): Relationship type medium adaptation (half-life: 7 turns)
- Global (α=0.05): Cross-entity theme slow adaptation (half-life: 14 turns)
- Staleness pruning: Remove entities not mentioned in 300+ turns
- L2 regularization: λ=0.001 prevents over-weighting

Integration (Layer 2 of 3-Layer Prehension):
- Extends EntityOrganTracker (organ pattern learning)
- Filters EntityHorizon retrieval (top-K salience)
- Used POST-RETRIEVAL by dae_interactive.py

Expected Evolution:
- Epochs 1-10: All entities equally salient
- Epochs 11-30: Recency bias emerges
- Epochs 31-100: Relationship salience patterns stabilize
- Epochs 100+: Long-term themes crystallize

Author: DAE_HYPHAE_1 + Claude Code
Date: November 17, 2025
Status: Phase 2 - Morpheable Horizon (Layer 2: Salience)
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class EntitySalienceMetrics:
    """
    Per-entity salience metrics with 3-tier decay.

    Attributes:
        entity_value: "Emma", "work project", etc.
        entity_type: "Person", "Place", "Preference", etc.

        # 3-Tier Salience (FFITTSS pattern)
        local_salience: EMA α=0.05 (entity-specific, fast)
        family_salience: EMA α=0.1 (relationship type, medium)
        global_salience: EMA α=0.05 (cross-entity theme, slow)

        # Temporal tracking
        mention_count: Total mentions across all turns
        first_mention_turn: Turn number of first mention
        last_mention_turn: Turn number of last mention
        turn_since_mention: Turns elapsed since last mention

        # Staleness detection
        is_stale: True if turn_since_mention > staleness_threshold

        # Composite salience
        composite_salience: Blended salience (local + family + global)
    """
    entity_value: str
    entity_type: str

    # 3-Tier salience
    local_salience: float = 0.0
    family_salience: float = 0.0
    global_salience: float = 0.0

    # Temporal
    mention_count: int = 0
    first_mention_turn: int = 0
    last_mention_turn: int = 0
    turn_since_mention: int = 0

    # Staleness
    is_stale: bool = False

    # Composite
    composite_salience: float = 0.0


class EntitySalienceTracker:
    """
    Multi-scale entity salience tracking with FFITTSS-inspired 3-tier decay.

    Layer 2 of the morpheable horizon architecture (HORIZON → SALIENCE → OPTIMIZATION).

    Determines "what matters now" through temporal decay and staleness pruning,
    ensuring memory stays bounded while feeling infinite.

    FFITTSS Patterns Implemented:
    - Local EMA (α=0.05): Entity-specific, fast adaptation (13-turn half-life)
    - Family EMA (α=0.1): Relationship type, medium adaptation (7-turn half-life)
    - Global EMA (α=0.05): Cross-entity theme, slow adaptation (14-turn half-life)
    - Staleness pruning: 300+ turns without mention → filtered out
    - L2 regularization: λ=0.001 prevents unbounded salience growth
    - Bounded updates: Only update every N turns (lazy propagation)

    Integration Points:
    - POST-RETRIEVAL: Filter entities from Neo4j queries
    - Replaces fixed limits with top-K salience filtering
    - Enables morpheable horizon based on conversational quality
    """

    # FFITTSS-inspired decay rates
    LOCAL_ALPHA = 0.05   # Fast entity-specific (half-life ≈ 13 turns)
    FAMILY_ALPHA = 0.1   # Medium relationship type (half-life ≈ 7 turns)
    GLOBAL_ALPHA = 0.05  # Slow cross-entity theme (half-life ≈ 14 turns)

    # Staleness threshold (FFITTSS: 300+ turns)
    STALENESS_THRESHOLD = 300

    # L2 regularization (prevents explosion)
    L2_LAMBDA = 0.001

    # Lazy propagation (update every N turns)
    UPDATE_INTERVAL = 1  # Update every turn for now (can increase to 5-10 for efficiency)

    # Salience blending weights (local, family, global)
    BLEND_WEIGHTS = (0.5, 0.3, 0.2)  # Local strongest, global weakest

    def __init__(
        self,
        storage_path: str = "persona_layer/state/active/entity_salience.json",
        staleness_threshold: int = 300,
        l2_lambda: float = 0.001
    ):
        """
        Initialize entity salience tracker.

        Args:
            storage_path: Path to persistent salience metrics (JSON)
            staleness_threshold: Turns without mention before stale (300)
            l2_lambda: L2 regularization strength (0.001)
        """
        self.storage_path = Path(storage_path)
        self.staleness_threshold = staleness_threshold
        self.l2_lambda = l2_lambda

        # Per-entity metrics
        self.entity_metrics: Dict[str, EntitySalienceMetrics] = {}

        # Family-level salience (relationship type averages)
        self.family_salience: Dict[str, float] = defaultdict(float)

        # Global salience (cross-entity theme)
        self.global_salience: float = 0.0

        # Current turn counter
        self.current_turn: int = 0

        # Last update turn (for lazy propagation)
        self.last_update_turn: int = 0

        # Load existing state
        self._load()

        print(f"✅ Entity Salience Tracker initialized (Phase 2 - Layer 2)")
        print(f"   Storage: {self.storage_path}")
        print(f"   Decay: local={self.LOCAL_ALPHA}, family={self.FAMILY_ALPHA}, global={self.GLOBAL_ALPHA}")
        print(f"   Staleness threshold: {self.staleness_threshold} turns")
        print(f"   Tracked entities: {len(self.entity_metrics)}")

    def update_salience(
        self,
        extracted_entities: List[Dict],
        current_turn: int,
        urgency_context: float = 0.0
    ):
        """
        Update entity salience based on current turn mentions.

        Args:
            extracted_entities: List of entities from entity extraction
                                [{'entity_value': 'Emma', 'entity_type': 'Person', ...}, ...]
            current_turn: Current turn number (from session manager)
            urgency_context: Optional urgency level from NDAM organ (0.0-1.0)
        """
        self.current_turn = current_turn

        # Lazy propagation: Only update if interval elapsed
        if current_turn - self.last_update_turn < self.UPDATE_INTERVAL:
            return

        # Process mentioned entities
        mentioned_entities = set()
        for entity_dict in extracted_entities:
            entity_value = entity_dict['entity_value']
            entity_type = entity_dict.get('entity_type', 'Unknown')
            mentioned_entities.add(entity_value)

            # Get or create metrics
            if entity_value not in self.entity_metrics:
                self.entity_metrics[entity_value] = EntitySalienceMetrics(
                    entity_value=entity_value,
                    entity_type=entity_type,
                    first_mention_turn=current_turn,
                    last_mention_turn=current_turn
                )

            metrics = self.entity_metrics[entity_value]

            # Update temporal tracking
            metrics.mention_count += 1
            metrics.last_mention_turn = current_turn
            metrics.turn_since_mention = 0
            metrics.is_stale = False

            # Boost based on urgency (crisis → higher salience)
            urgency_boost = 1.0 + urgency_context

            # Local salience: EMA update (entity-specific)
            metrics.local_salience = (
                self.LOCAL_ALPHA * urgency_boost +
                (1 - self.LOCAL_ALPHA) * metrics.local_salience
            )

            # Family salience: Update family average
            self.family_salience[entity_type] = (
                self.FAMILY_ALPHA * urgency_boost +
                (1 - self.FAMILY_ALPHA) * self.family_salience[entity_type]
            )
            metrics.family_salience = self.family_salience[entity_type]

            # Global salience: Update cross-entity theme
            self.global_salience = (
                self.GLOBAL_ALPHA * urgency_boost +
                (1 - self.GLOBAL_ALPHA) * self.global_salience
            )
            metrics.global_salience = self.global_salience

            # Apply L2 regularization (prevent explosion)
            metrics.local_salience *= (1 - self.l2_lambda)
            metrics.family_salience *= (1 - self.l2_lambda)
            metrics.global_salience *= (1 - self.l2_lambda)

            # Composite salience (blended)
            metrics.composite_salience = (
                self.BLEND_WEIGHTS[0] * metrics.local_salience +
                self.BLEND_WEIGHTS[1] * metrics.family_salience +
                self.BLEND_WEIGHTS[2] * metrics.global_salience
            )

        # Decay un-mentioned entities
        for entity_value, metrics in self.entity_metrics.items():
            if entity_value not in mentioned_entities:
                # Update turn_since_mention
                metrics.turn_since_mention = current_turn - metrics.last_mention_turn

                # Check staleness
                if metrics.turn_since_mention >= self.staleness_threshold:
                    metrics.is_stale = True

                # Decay all tiers (EMA with zero input)
                metrics.local_salience *= (1 - self.LOCAL_ALPHA)
                metrics.family_salience *= (1 - self.FAMILY_ALPHA)
                metrics.global_salience *= (1 - self.GLOBAL_ALPHA)

                # Apply L2 regularization
                metrics.local_salience *= (1 - self.l2_lambda)
                metrics.family_salience *= (1 - self.l2_lambda)
                metrics.global_salience *= (1 - self.l2_lambda)

                # Update composite
                metrics.composite_salience = (
                    self.BLEND_WEIGHTS[0] * metrics.local_salience +
                    self.BLEND_WEIGHTS[1] * metrics.family_salience +
                    self.BLEND_WEIGHTS[2] * metrics.global_salience
                )

        # Update last update turn
        self.last_update_turn = current_turn

    def filter_by_salience(
        self,
        entities: List[Dict],
        top_k: int,
        remove_stale: bool = True
    ) -> List[Dict]:
        """
        Filter entities by salience (top-K most salient).

        Args:
            entities: List of entities from Neo4j queries
            top_k: Number of top entities to return
            remove_stale: If True, filter out stale entities first

        Returns:
            Filtered list of entities (top-K by composite salience)
        """
        if not entities:
            return []

        # Add salience scores to entities
        scored_entities = []
        for entity in entities:
            entity_value = entity.get('entity_value') or entity.get('name')

            # Get salience metrics
            if entity_value in self.entity_metrics:
                metrics = self.entity_metrics[entity_value]

                # Skip stale if requested
                if remove_stale and metrics.is_stale:
                    continue

                # Add salience score
                entity['composite_salience'] = metrics.composite_salience
                entity['is_stale'] = metrics.is_stale
                scored_entities.append(entity)
            else:
                # New entity (no history) - neutral salience
                entity['composite_salience'] = 0.5
                entity['is_stale'] = False
                scored_entities.append(entity)

        # Sort by composite salience (descending)
        scored_entities.sort(key=lambda e: e['composite_salience'], reverse=True)

        # Return top-K
        return scored_entities[:top_k]

    def get_salience_distribution(self) -> Dict[str, float]:
        """
        Get salience distribution for debugging/visualization.

        Returns:
            Dictionary of entity_value → composite_salience
        """
        return {
            entity_value: metrics.composite_salience
            for entity_value, metrics in self.entity_metrics.items()
            if not metrics.is_stale
        }

    def get_stale_entities(self) -> List[str]:
        """Get list of stale entities (for pruning)."""
        return [
            entity_value
            for entity_value, metrics in self.entity_metrics.items()
            if metrics.is_stale
        ]

    def prune_stale_entities(self):
        """Remove stale entities from tracker (staleness pruning)."""
        stale_entities = self.get_stale_entities()
        for entity_value in stale_entities:
            del self.entity_metrics[entity_value]

        return len(stale_entities)

    def _load(self):
        """Load salience metrics from JSON."""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Load entity metrics
            for entity_value, metrics_dict in data.get('entity_metrics', {}).items():
                self.entity_metrics[entity_value] = EntitySalienceMetrics(**metrics_dict)

            # Load family salience
            self.family_salience = defaultdict(float, data.get('family_salience', {}))

            # Load global salience
            self.global_salience = data.get('global_salience', 0.0)

            # Load turn counter
            self.current_turn = data.get('current_turn', 0)
            self.last_update_turn = data.get('last_update_turn', 0)

        except Exception as e:
            print(f"⚠️  Error loading salience metrics: {e}")

    def save(self):
        """Save salience metrics to JSON."""
        # Ensure directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'entity_metrics': {
                entity_value: asdict(metrics)
                for entity_value, metrics in self.entity_metrics.items()
            },
            'family_salience': dict(self.family_salience),
            'global_salience': self.global_salience,
            'current_turn': self.current_turn,
            'last_update_turn': self.last_update_turn,
            'metadata': {
                'local_alpha': self.LOCAL_ALPHA,
                'family_alpha': self.FAMILY_ALPHA,
                'global_alpha': self.GLOBAL_ALPHA,
                'staleness_threshold': self.staleness_threshold,
                'l2_lambda': self.l2_lambda,
                'last_updated': datetime.now().isoformat()
            }
        }

        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)


# Module-level singleton for convenience
_default_salience_tracker = None

def get_default_salience_tracker() -> EntitySalienceTracker:
    """Get or create default EntitySalienceTracker singleton."""
    global _default_salience_tracker
    if _default_salience_tracker is None:
        _default_salience_tracker = EntitySalienceTracker()
    return _default_salience_tracker
