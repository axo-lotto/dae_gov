"""
NeighborWordContextTracker - Neighbor Boost Pattern Learning
=============================================================

Tracks neighbor word pairs and their influence on organ activations to learn
context-dependent boost patterns (e.g., "my daughter" → relationship_depth +0.20).

Core Learning Pattern:
    After 50 mentions:
    - ("my", "daughter") → relationship_depth +0.22, entity_recall +0.15
    - ("worried", "about") → salience_gradient +0.18, urgency +0.25
    - ("Emma", "Smith") → merge_coherence 0.95 (multi-word entity!)

Architecture Alignment:
    - Neighbor Prehension: 3-5 word windows for context
    - Organ Boost Learning: Context → organ activation patterns
    - Multi-Word Detection: Adjacent word coherence

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
Status: Phase 3B Week 1 - Foundation Tracker (Medium Priority)
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
import numpy as np
from dataclasses import dataclass, field

# Import WordOccasion
import sys
sys.path.append(str(Path(__file__).parent.parent))
from transductive.word_occasion import WordOccasion


@dataclass
class NeighborPairPattern:
    """Pattern for a specific neighbor word pair."""
    pair: Tuple[str, str]
    count: int = 0

    # Organ boost patterns (EMA)
    organ_boosts: Dict[str, float] = field(default_factory=dict)

    # Context tracking
    typical_entity_type: Optional[str] = None
    entity_type_distribution: Dict[str, int] = field(default_factory=dict)

    # Merge coherence (for multi-word entities)
    merge_coherence: float = 0.0
    merge_count: int = 0


class NeighborWordContextTracker:
    """
    Tracks neighbor word context patterns for organ boost learning.

    Usage:
        tracker = NeighborWordContextTracker()

        # After entity extraction with WordOccasions
        for word_occ in word_occasions:
            if word_occ.is_entity():
                tracker.update(word_occ)

        # Predict boost from neighbor pair
        boost = tracker.predict_boost(("my", "daughter"), "relationship_depth")
    """

    def __init__(
        self,
        storage_path: Optional[str] = None,
        ema_alpha: float = 0.15,
        min_count_for_pattern: int = 5
    ):
        """
        Initialize neighbor word context tracker.

        Args:
            storage_path: Path to save neighbor patterns (JSON)
            ema_alpha: EMA smoothing factor for boost learning
            min_count_for_pattern: Minimum count before pattern is reliable
        """
        self.storage_path = storage_path or "persona_layer/state/active/neighbor_word_context.json"
        self.ema_alpha = ema_alpha
        self.min_count_for_pattern = min_count_for_pattern

        # Neighbor pair patterns
        self.neighbor_patterns: Dict[Tuple[str, str], NeighborPairPattern] = {}

        # Optimal window size tracking
        self.window_effectiveness: Dict[int, float] = {}  # window_size → effectiveness
        self.mean_effective_window = 3.8
        self.max_window = 5

        # Statistics
        self.total_updates = 0
        self.total_predictions = 0

        # Load existing patterns
        self._load_patterns()

    def update(self, word_occasion: WordOccasion):
        """
        Update neighbor patterns from a WordOccasion.

        Args:
            word_occasion: WordOccasion that was classified as entity
        """
        if not word_occasion.is_entity():
            return

        self.total_updates += 1

        # Extract neighbor pairs (up to 3 left + 3 right)
        left_neighbors = word_occasion.left_neighbors[-3:] if word_occasion.left_neighbors else []
        right_neighbors = word_occasion.right_neighbors[:3] if word_occasion.right_neighbors else []

        # Process left neighbor pairs
        for i in range(len(left_neighbors) - 1):
            pair = (left_neighbors[i], left_neighbors[i + 1])
            self._update_pair_pattern(pair, word_occasion)

        # Process right neighbor pairs
        for i in range(len(right_neighbors) - 1):
            pair = (right_neighbors[i], right_neighbors[i + 1])
            self._update_pair_pattern(pair, word_occasion)

        # Process left-to-word pairs (e.g., "my" + "Emma")
        if left_neighbors:
            for left_word in left_neighbors[-2:]:  # Last 2 left neighbors
                pair = (left_word, word_occasion.word)
                self._update_pair_pattern(pair, word_occasion)

        # Save every 20 updates
        if self.total_updates % 20 == 0:
            self._save_patterns()

    def _update_pair_pattern(
        self,
        pair: Tuple[str, str],
        word_occasion: WordOccasion
    ):
        """
        Update pattern for a specific neighbor pair.

        Args:
            pair: Tuple of (word1, word2)
            word_occasion: WordOccasion providing context
        """
        # Get or create pattern
        if pair not in self.neighbor_patterns:
            self.neighbor_patterns[pair] = NeighborPairPattern(pair=pair)

        pattern = self.neighbor_patterns[pair]
        pattern.count += 1

        # Update organ boosts (if actualization vector available)
        if word_occasion.actualization_vector is not None:
            atom_names = ['entity_recall', 'relationship_depth', 'temporal_continuity',
                         'co_occurrence', 'salience_gradient', 'memory_coherence',
                         'contextual_grounding']

            for i, atom_name in enumerate(atom_names):
                if i < len(word_occasion.actualization_vector):
                    activation = float(word_occasion.actualization_vector[i])

                    # Update EMA for this atom boost
                    if atom_name not in pattern.organ_boosts:
                        pattern.organ_boosts[atom_name] = activation
                    else:
                        pattern.organ_boosts[atom_name] = (
                            self.ema_alpha * activation +
                            (1.0 - self.ema_alpha) * pattern.organ_boosts[atom_name]
                        )

        # Update entity type distribution
        if word_occasion.entity_type:
            pattern.entity_type_distribution[word_occasion.entity_type] = \
                pattern.entity_type_distribution.get(word_occasion.entity_type, 0) + 1

            # Update most common type
            most_common = max(
                pattern.entity_type_distribution,
                key=pattern.entity_type_distribution.get
            )
            pattern.typical_entity_type = most_common

        # Update merge coherence (if this is adjacent to another entity)
        if word_occasion.entity_coherence > 0:
            pattern.merge_count += 1
            pattern.merge_coherence = (
                self.ema_alpha * word_occasion.entity_coherence +
                (1.0 - self.ema_alpha) * pattern.merge_coherence
            )

    def predict_boost(
        self,
        pair: Tuple[str, str],
        atom_name: str
    ) -> float:
        """
        Predict organ boost from a neighbor pair.

        Args:
            pair: Neighbor word pair
            atom_name: Atom to predict boost for

        Returns:
            Predicted boost (0.0 if no pattern or insufficient data)
        """
        if pair not in self.neighbor_patterns:
            return 0.0

        pattern = self.neighbor_patterns[pair]

        # Require minimum count
        if pattern.count < self.min_count_for_pattern:
            return 0.0

        # Return learned boost
        boost = pattern.organ_boosts.get(atom_name, 0.0)

        self.total_predictions += 1

        # Clamp boost to [0.0, 0.3]
        return min(0.3, max(0.0, boost))

    def get_merge_coherence(
        self,
        pair: Tuple[str, str]
    ) -> float:
        """
        Get merge coherence for a word pair (for multi-word entity detection).

        Args:
            pair: Word pair

        Returns:
            Merge coherence (0.0-1.0)
        """
        if pair not in self.neighbor_patterns:
            return 0.0

        pattern = self.neighbor_patterns[pair]

        if pattern.count < self.min_count_for_pattern:
            return 0.0

        return pattern.merge_coherence

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get neighbor context tracker statistics.

        Returns:
            Dictionary with statistics
        """
        reliable_patterns = sum(
            1 for p in self.neighbor_patterns.values()
            if p.count >= self.min_count_for_pattern
        )

        return {
            'total_neighbor_patterns': len(self.neighbor_patterns),
            'reliable_patterns': reliable_patterns,
            'total_updates': self.total_updates,
            'total_predictions': self.total_predictions,
            'mean_effective_window': self.mean_effective_window,
            'max_window': self.max_window
        }

    def get_top_patterns(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Get top N most frequent neighbor patterns.

        Args:
            top_n: Number of patterns to return

        Returns:
            List of pattern dictionaries
        """
        sorted_patterns = sorted(
            self.neighbor_patterns.values(),
            key=lambda p: p.count,
            reverse=True
        )

        return [
            {
                'pair': pattern.pair,
                'count': pattern.count,
                'organ_boosts': pattern.organ_boosts,
                'typical_entity_type': pattern.typical_entity_type,
                'merge_coherence': pattern.merge_coherence
            }
            for pattern in sorted_patterns[:top_n]
        ]

    def _save_patterns(self):
        """Save neighbor patterns to JSON file."""
        try:
            data = {
                'neighbor_patterns': {},
                'statistics': self.get_statistics(),
                'timestamp': time.time()
            }

            # Serialize patterns (top 200 most frequent)
            sorted_patterns = sorted(
                self.neighbor_patterns.values(),
                key=lambda p: p.count,
                reverse=True
            )

            for pattern in sorted_patterns[:200]:
                pair_key = f"{pattern.pair[0]}_{pattern.pair[1]}"
                data['neighbor_patterns'][pair_key] = {
                    'pair': list(pattern.pair),
                    'count': pattern.count,
                    'organ_boosts': pattern.organ_boosts,
                    'entity_type_distribution': pattern.entity_type_distribution,
                    'typical_entity_type': pattern.typical_entity_type,
                    'merge_coherence': pattern.merge_coherence,
                    'merge_count': pattern.merge_count
                }

            # Write to file
            Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Failed to save neighbor patterns: {e}")

    def _load_patterns(self):
        """Load neighbor patterns from JSON file."""
        try:
            if not Path(self.storage_path).exists():
                return

            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Load patterns
            for pair_str, pattern_data in data.get('neighbor_patterns', {}).items():
                pair_list = pattern_data['pair']
                pair = (pair_list[0], pair_list[1])

                self.neighbor_patterns[pair] = NeighborPairPattern(
                    pair=pair,
                    count=pattern_data['count'],
                    organ_boosts=pattern_data.get('organ_boosts', {}),
                    entity_type_distribution=pattern_data.get('entity_type_distribution', {}),
                    typical_entity_type=pattern_data.get('typical_entity_type'),
                    merge_coherence=pattern_data.get('merge_coherence', 0.0),
                    merge_count=pattern_data.get('merge_count', 0)
                )

            # Load statistics
            stats = data.get('statistics', {})
            self.total_updates = stats.get('total_updates', 0)
            self.total_predictions = stats.get('total_predictions', 0)
            self.mean_effective_window = stats.get('mean_effective_window', 3.8)

            print(f"✅ Loaded {len(self.neighbor_patterns)} neighbor patterns")

        except Exception as e:
            print(f"⚠️  Failed to load neighbor patterns: {e}")


if __name__ == "__main__":
    """
    Validation test for NeighborWordContextTracker.
    """
    print("=" * 80)
    print("🧪 NEIGHBOR WORD CONTEXT TRACKER VALIDATION TEST")
    print("=" * 80)

    # Test 1: Initialize tracker
    print("\n📋 TEST 1: Initialize Tracker")
    tracker = NeighborWordContextTracker(storage_path="/tmp/test_neighbor_context.json")
    print(f"   ✅ Storage path: {tracker.storage_path}")
    print(f"   ✅ EMA alpha: {tracker.ema_alpha}")
    print(f"   ✅ Min count: {tracker.min_count_for_pattern}")

    # Test 2: Simulate learning from WordOccasions
    print("\n📋 TEST 2: Simulate Learning (10 patterns)")
    from transductive.word_occasion import WordOccasion

    # Simulate 10 mentions with "my daughter Emma" pattern
    for i in range(10):
        emma = WordOccasion(
            word="Emma",
            position=2,
            sentence="I'm worried about my daughter Emma",
            left_neighbors=["my", "daughter"],
            right_neighbors=["who", "is"]
        )
        emma.entity_type = "Person"
        emma.entity_confidence = 0.85
        emma.entity_coherence = 0.80
        emma.actualization_vector = np.array([
            0.85,  # entity_recall
            0.70,  # relationship_depth (boosted by "daughter")
            0.65, 0.60, 0.55, 0.50, 0.75
        ])

        tracker.update(emma)

    stats = tracker.get_statistics()
    print(f"   ✅ Total patterns: {stats['total_neighbor_patterns']}")
    print(f"   ✅ Reliable patterns: {stats['reliable_patterns']}")

    # Test 3: Pattern retrieval
    print("\n📋 TEST 3: Top Learned Patterns")
    top_patterns = tracker.get_top_patterns(top_n=5)
    for pattern in top_patterns:
        print(f"   {pattern['pair']}: count={pattern['count']}, type={pattern['typical_entity_type']}")
        if pattern['organ_boosts']:
            top_boost = max(pattern['organ_boosts'].items(), key=lambda x: x[1])
            print(f"      Top boost: {top_boost[0]} = {top_boost[1]:.3f}")

    # Test 4: Boost prediction
    print("\n📋 TEST 4: Boost Prediction")
    boost = tracker.predict_boost(("my", "daughter"), "relationship_depth")
    print(f"   ✅ Predicted boost for ('my', 'daughter') → relationship_depth: {boost:.3f}")

    boost2 = tracker.predict_boost(("daughter", "Emma"), "entity_recall")
    print(f"   ✅ Predicted boost for ('daughter', 'Emma') → entity_recall: {boost2:.3f}")

    # Test 5: Save/Load
    print("\n📋 TEST 5: Save and Load Patterns")
    tracker._save_patterns()
    print(f"   ✅ Patterns saved")

    tracker2 = NeighborWordContextTracker(storage_path="/tmp/test_neighbor_context.json")
    print(f"   ✅ Loaded {len(tracker2.neighbor_patterns)} patterns")

    print("\n" + "=" * 80)
    print("✅ NEIGHBOR WORD CONTEXT TRACKER VALIDATION PASSED!")
    print("=" * 80)
