"""
Word-Entity Bridge - Phase 0B Entity-Memory Integration
=======================================================

Bridges word-level patterns (Phase 0A) with entity-level patterns to create
unified word-entity co-learning.

Philosophy:
- Words are not learned in isolation—they're learned in relation to entities
- "daughter" near "Emma" has different felt-significance than "daughter" near "Lily"
- Entity context enhances word pattern predictions
- Word neighbors enhance entity extraction

Integration Points:
- Links WordOccasionTracker (Phase 0A) with EntityOrganTracker
- Called during training after entity extraction
- Enhances Phase 0.5 Tier 2 predictions with entity context

Expected Evolution:
- Epoch 1-5: Co-occurrence patterns emerge
- Epoch 5-10: Entity-contextualized confidence boosts active
- Epoch 10-20: Stable word-entity associations for improved extraction

Date: November 19, 2025
Status: Phase 0B Implementation
"""

import json
import time
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, field, asdict
from collections import defaultdict


@dataclass
class EntityNeighborStats:
    """Statistics for how a word co-occurs with a specific entity"""
    entity_value: str
    entity_type: str
    count: int = 0

    # Relative position distribution (-3 to +3)
    relative_positions: Dict[int, int] = field(default_factory=dict)

    # Typical organ activations when word+entity co-occur
    typical_organs: Dict[str, float] = field(default_factory=dict)

    # Temporal tracking
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)


@dataclass
class WordEntityPattern:
    """Co-occurrence pattern between a word and entities"""
    word: str

    # Which entities appear near this word
    entity_neighbors: Dict[str, EntityNeighborStats] = field(default_factory=dict)

    # Overall statistics
    total_mentions: int = 0
    total_entity_cooccurrences: int = 0

    # Metadata
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)


class WordEntityBridge:
    """
    Bridges word patterns with entity patterns for co-learning.

    Key Capabilities:
    1. Track word-entity co-occurrences during training
    2. Enhance word predictions with entity context
    3. Suggest entity candidates based on word neighbors
    4. Enable organic word-entity co-evolution
    """

    def __init__(
        self,
        storage_path: str = "persona_layer/state/active/word_entity_cooccurrence.json",
        ema_alpha: float = 0.15,
        context_window: int = 3,  # ±3 tokens
        min_cooccurrences: int = 3  # Need 3+ to use pattern
    ):
        """
        Initialize word-entity bridge.

        Args:
            storage_path: Path to persistent co-occurrence patterns (JSON)
            ema_alpha: EMA smoothing for organ activations
            context_window: How many tokens left/right to check for entities
            min_cooccurrences: Minimum co-occurrences before using pattern
        """
        self.storage_path = Path(storage_path)
        self.ema_alpha = ema_alpha
        self.context_window = context_window
        self.min_cooccurrences = min_cooccurrences

        # Word-entity co-occurrence patterns
        self.patterns: Dict[str, WordEntityPattern] = {}

        # Load existing patterns
        self._load_patterns()

        print(f"✅ WordEntityBridge initialized")
        print(f"   Storage: {self.storage_path}")
        print(f"   Patterns loaded: {len(self.patterns)}")
        print(f"   Context window: ±{self.context_window} tokens")

    def _load_patterns(self):
        """Load existing word-entity patterns from disk"""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Reconstruct patterns from dict
            for word, pattern_dict in data.get('patterns', {}).items():
                # Reconstruct EntityNeighborStats objects
                entity_neighbors = {}
                for entity_value, stats_dict in pattern_dict.get('entity_neighbors', {}).items():
                    # Convert relative_positions keys back to int
                    relative_positions = {
                        int(k): v for k, v in stats_dict.get('relative_positions', {}).items()
                    }
                    entity_neighbors[entity_value] = EntityNeighborStats(
                        entity_value=stats_dict['entity_value'],
                        entity_type=stats_dict['entity_type'],
                        count=stats_dict['count'],
                        relative_positions=relative_positions,
                        typical_organs=stats_dict.get('typical_organs', {}),
                        first_seen=stats_dict.get('first_seen', time.time()),
                        last_seen=stats_dict.get('last_seen', time.time())
                    )

                self.patterns[word] = WordEntityPattern(
                    word=word,
                    entity_neighbors=entity_neighbors,
                    total_mentions=pattern_dict.get('total_mentions', 0),
                    total_entity_cooccurrences=pattern_dict.get('total_entity_cooccurrences', 0),
                    first_seen=pattern_dict.get('first_seen', time.time()),
                    last_seen=pattern_dict.get('last_seen', time.time())
                )

        except Exception as e:
            print(f"⚠️  Failed to load word-entity patterns: {e}")

    def save_patterns(self):
        """Save word-entity patterns to disk"""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert patterns to dict (handle nested dataclasses)
            patterns_dict = {}
            for word, pattern in self.patterns.items():
                entity_neighbors_dict = {}
                for entity_value, stats in pattern.entity_neighbors.items():
                    # Convert relative_positions keys to strings for JSON
                    relative_positions_str = {
                        str(k): v for k, v in stats.relative_positions.items()
                    }
                    entity_neighbors_dict[entity_value] = {
                        'entity_value': stats.entity_value,
                        'entity_type': stats.entity_type,
                        'count': stats.count,
                        'relative_positions': relative_positions_str,
                        'typical_organs': stats.typical_organs,
                        'first_seen': stats.first_seen,
                        'last_seen': stats.last_seen
                    }

                patterns_dict[word] = {
                    'word': pattern.word,
                    'entity_neighbors': entity_neighbors_dict,
                    'total_mentions': pattern.total_mentions,
                    'total_entity_cooccurrences': pattern.total_entity_cooccurrences,
                    'first_seen': pattern.first_seen,
                    'last_seen': pattern.last_seen
                }

            data = {
                'patterns': patterns_dict,
                'metadata': {
                    'total_patterns': len(self.patterns),
                    'last_updated': time.time()
                }
            }

            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Failed to save word-entity patterns: {e}")

    def update_word_entity_cooccurrence(
        self,
        word_occasions: List[Any],
        entities: List[Dict[str, Any]],
        organ_results: Dict[str, Any]
    ):
        """
        Update word-entity co-occurrence patterns after processing a conversation.

        Args:
            word_occasions: List of WordOccasion objects from tokenization
            entities: List of extracted entities (dicts with value, type, indices)
            organ_results: Organ activation results from this turn
        """
        if not word_occasions or not entities:
            return

        # Get organ coherences for this turn
        organ_coherences = organ_results.get('organ_coherences', {})

        # Build entity position map
        entity_map = {}  # position -> (entity_value, entity_type)
        for entity in entities:
            entity_value = entity.get('value', entity.get('entity_value', ''))
            entity_type = entity.get('type', entity.get('entity_type', 'Unknown'))

            # Get indices (could be start/end or just position)
            if 'start_idx' in entity and 'end_idx' in entity:
                for idx in range(entity['start_idx'], entity['end_idx'] + 1):
                    entity_map[idx] = (entity_value, entity_type)
            elif 'position' in entity:
                entity_map[entity['position']] = (entity_value, entity_type)

        # Process each word occasion
        for occasion in word_occasions:
            word = occasion.word.lower()
            position = occasion.position

            # Initialize pattern if needed
            if word not in self.patterns:
                self.patterns[word] = WordEntityPattern(word=word)

            pattern = self.patterns[word]
            pattern.total_mentions += 1
            pattern.last_seen = time.time()

            # Check for entities within context window
            for offset in range(-self.context_window, self.context_window + 1):
                if offset == 0:
                    continue

                check_position = position + offset
                if check_position in entity_map:
                    entity_value, entity_type = entity_map[check_position]

                    # Initialize entity neighbor stats if needed
                    if entity_value not in pattern.entity_neighbors:
                        pattern.entity_neighbors[entity_value] = EntityNeighborStats(
                            entity_value=entity_value,
                            entity_type=entity_type
                        )

                    stats = pattern.entity_neighbors[entity_value]
                    stats.count += 1
                    stats.last_seen = time.time()

                    # Update relative position distribution
                    if offset not in stats.relative_positions:
                        stats.relative_positions[offset] = 0
                    stats.relative_positions[offset] += 1

                    # Update typical organ activations (EMA)
                    for organ_name, coherence in organ_coherences.items():
                        if organ_name not in stats.typical_organs:
                            stats.typical_organs[organ_name] = coherence
                        else:
                            stats.typical_organs[organ_name] = (
                                (1 - self.ema_alpha) * stats.typical_organs[organ_name] +
                                self.ema_alpha * coherence
                            )

                    pattern.total_entity_cooccurrences += 1

    def predict_with_entity_context(
        self,
        word: str,
        nearby_entities: List[Dict[str, str]],
        base_prediction: Tuple[Any, float]
    ) -> Tuple[Any, float, str]:
        """
        Enhance word prediction with entity context.

        Args:
            word: Word to predict pattern for
            nearby_entities: List of entities near this word (value, type, distance)
            base_prediction: (pattern, confidence) from Phase 0.5 cascade

        Returns:
            (enhanced_pattern, adjusted_confidence, source)
        """
        base_pattern, base_confidence = base_prediction

        # No entity context available
        if not nearby_entities:
            return base_pattern, base_confidence, 'base'

        # No pattern for this word
        if word.lower() not in self.patterns:
            return base_pattern, base_confidence, 'base'

        pattern = self.patterns[word.lower()]

        # Check if any nearby entities match our co-occurrence patterns
        best_match_confidence_boost = 0.0
        matched_entity = None

        for entity in nearby_entities:
            entity_value = entity.get('value', '')
            distance = entity.get('distance', 999)

            if entity_value in pattern.entity_neighbors:
                stats = pattern.entity_neighbors[entity_value]

                # Only use if we have enough co-occurrences
                if stats.count >= self.min_cooccurrences:
                    # Confidence boost based on co-occurrence frequency
                    # and distance match
                    frequency_factor = min(stats.count / 20.0, 1.0)  # Cap at 20
                    distance_factor = 1.0 if abs(distance) <= self.context_window else 0.5

                    confidence_boost = 0.15 * frequency_factor * distance_factor

                    if confidence_boost > best_match_confidence_boost:
                        best_match_confidence_boost = confidence_boost
                        matched_entity = entity_value

        if best_match_confidence_boost > 0:
            adjusted_confidence = min(base_confidence + best_match_confidence_boost, 0.95)
            return base_pattern, adjusted_confidence, f'entity_context_{matched_entity}'

        return base_pattern, base_confidence, 'base'

    def suggest_entity_candidates(
        self,
        word_sequence: List[Tuple[str, int]]
    ) -> List[Dict[str, Any]]:
        """
        Suggest entity candidates based on word neighbor patterns.

        Args:
            word_sequence: List of (word, position) tuples

        Returns:
            List of entity candidates with {position, suggested_type, confidence}
        """
        candidates = []

        for i, (word, position) in enumerate(word_sequence):
            word_lower = word.lower()

            # Check if this word has strong entity associations
            if word_lower in self.patterns:
                pattern = self.patterns[word_lower]

                # Find most common entity type for this word
                entity_type_counts = defaultdict(int)
                for entity_value, stats in pattern.entity_neighbors.items():
                    if stats.count >= self.min_cooccurrences:
                        entity_type_counts[stats.entity_type] += stats.count

                if entity_type_counts:
                    # Suggest most common entity type
                    best_type = max(entity_type_counts.items(), key=lambda x: x[1])
                    entity_type, count = best_type

                    confidence = min(count / 30.0, 0.85)  # Cap at 0.85

                    # Check for capitalized words nearby (strong Person signal)
                    capitalized_nearby = False
                    for j in range(max(0, i-2), min(len(word_sequence), i+3)):
                        if j != i:
                            nearby_word = word_sequence[j][0]
                            if nearby_word and nearby_word[0].isupper():
                                capitalized_nearby = True
                                break

                    if entity_type == "Person" and capitalized_nearby:
                        confidence += 0.10  # Boost confidence

                    candidates.append({
                        'position': position,
                        'suggested_type': entity_type,
                        'confidence': confidence,
                        'trigger_word': word
                    })

        return candidates

    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get summary statistics of word-entity patterns"""
        total_patterns = len(self.patterns)
        total_cooccurrences = sum(p.total_entity_cooccurrences for p in self.patterns.values())

        # Count patterns with sufficient cooccurrences
        active_patterns = sum(
            1 for p in self.patterns.values()
            if any(s.count >= self.min_cooccurrences for s in p.entity_neighbors.values())
        )

        return {
            'total_patterns': total_patterns,
            'active_patterns': active_patterns,
            'total_cooccurrences': total_cooccurrences,
            'avg_cooccurrences_per_pattern': total_cooccurrences / total_patterns if total_patterns > 0 else 0
        }
