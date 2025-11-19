"""
WordOccasionTracker - Word-Level Pattern Learning for Neighbor Prehension
===========================================================================

Accumulates word-level organ activations, neighbor patterns, and entity
classification patterns to enable LLM-free entity extraction through learned
felt-state associations.

Core Learning Pattern:
    Word "Emma" at position 5 with:
    - Left neighbors: ["worried", "about", "my", "daughter"]
    - Right neighbors: ["who", "is"]
    - NEXUS atoms: {entity_recall: 0.85, relationship_depth: 0.70, ...}
    - Entity type: Person (confidence 0.87)

    After 15 mentions → Learn:
    - "daughter" + capitalized word → Person entity (relationship_depth boost)
    - Typical confidence: 0.87 (EMA, α=0.15)
    - Typical coherence: 0.82

Architecture Alignment:
    - Level 1 Learning (Per-Turn): Captures word occasions every turn
    - Level 6 Learning (Entity-Organ): Extends with word-level granularity
    - Hebbian Reinforcement: Pattern strength increases with repetition

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
Status: Phase 3B Week 1 - Foundation Tracker (Critical Priority)
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple, Union
import numpy as np
from dataclasses import dataclass, field

# Import WordOccasion
import sys
sys.path.append(str(Path(__file__).parent.parent))
from transductive.word_occasion import WordOccasion


@dataclass
class WordPattern:
    """
    Learned pattern for a specific word across multiple mentions.
    """
    word: str
    mention_count: int = 0
    positions: List[int] = field(default_factory=list)

    # Neighbor accumulation
    left_neighbors: Dict[str, int] = field(default_factory=dict)
    right_neighbors: Dict[str, int] = field(default_factory=dict)

    # Organ activations (running statistics)
    organ_activations: Dict[str, Dict[str, float]] = field(default_factory=dict)

    # Entity classification distribution
    entity_type_distribution: Dict[str, int] = field(default_factory=dict)

    # EMA tracking
    confidence_ema: float = 0.5
    coherence_ema: float = 0.5

    # Metadata
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)


class WordOccasionTracker:
    """
    Tracks word-level patterns for neighbor prehension learning.

    Usage:
        tracker = WordOccasionTracker()
        tracker.update(word_occasions)  # After each turn

        # Prediction
        predicted_type, confidence = tracker.predict_entity_type(
            word="Emma",
            left_neighbors=["my", "daughter"],
            right_neighbors=["went", "to"]
        )
    """

    def __init__(
        self,
        storage_path: Optional[str] = None,
        ema_alpha: float = 0.15,
        min_mentions_for_pattern: int = 3
    ):
        """
        Initialize word occasion tracker.

        Args:
            storage_path: Path to save word patterns (JSON)
            ema_alpha: EMA smoothing factor for confidence/coherence
            min_mentions_for_pattern: Minimum mentions before pattern is usable
        """
        self.storage_path = storage_path or "persona_layer/state/active/word_occasion_patterns.json"
        self.ema_alpha = ema_alpha
        self.min_mentions_for_pattern = min_mentions_for_pattern

        # Word patterns storage
        self.word_patterns: Dict[str, WordPattern] = {}

        # Word pair patterns (for multi-word detection)
        self.word_pair_patterns: Dict[Tuple[str, str], Dict[str, Any]] = {}

        # Statistics
        self.total_updates = 0
        self.total_predictions = 0
        self.prediction_accuracy = 0.0

        # Load existing patterns
        self._load_patterns()

    def update(self, word_occasions: List[WordOccasion]):
        """
        Update word patterns from list of WordOccasions.

        🌀 Phase 3B Fix #1 (Nov 18, 2025): Track ALL words, not just entities
        This allows pattern learning even when entity extraction fails (chicken-and-egg problem).

        Args:
            word_occasions: List of WordOccasions from current turn
        """
        for word_occ in word_occasions:
            # 🌀 Track ALL words, not just entities
            # This allows pattern learning to bootstrap entity extraction
            self._update_word_pattern(word_occ)

            # Update word pair patterns (for multi-word detection)
            self._update_word_pair_patterns(word_occ, word_occasions)

        self.total_updates += 1

        # Save every 10 updates
        if self.total_updates % 10 == 0:
            self._save_patterns()

    def _update_word_pattern(self, word_occ: WordOccasion):
        """
        Update pattern for a single word (tracks ALL words).

        🌀 Phase 3B Fix #1 (Nov 18, 2025): Tracks all words, not just entities.
        Entity-specific fields (entity_type, confidence, coherence) are updated
        conditionally only when the word is classified as an entity.

        Args:
            word_occ: WordOccasion from current turn (entity or non-entity)
        """
        word = word_occ.word

        # Get or create pattern
        if word not in self.word_patterns:
            self.word_patterns[word] = WordPattern(word=word)

        pattern = self.word_patterns[word]

        # Update mention count and position
        pattern.mention_count += 1
        pattern.positions.append(word_occ.position)
        pattern.last_seen = time.time()

        # Accumulate neighbors
        for left_neighbor in word_occ.left_neighbors:
            pattern.left_neighbors[left_neighbor] = pattern.left_neighbors.get(left_neighbor, 0) + 1

        for right_neighbor in word_occ.right_neighbors:
            pattern.right_neighbors[right_neighbor] = pattern.right_neighbors.get(right_neighbor, 0) + 1

        # Update organ activations (running mean + std)
        if word_occ.actualization_vector is not None:
            # Use actualization vector (7D from NEXUS atoms)
            atom_names = ['entity_recall', 'relationship_depth', 'temporal_continuity',
                         'co_occurrence', 'salience_gradient', 'memory_coherence',
                         'contextual_grounding']

            for i, atom_name in enumerate(atom_names):
                if i < len(word_occ.actualization_vector):
                    activation = float(word_occ.actualization_vector[i])
                    self._update_running_stats(pattern.organ_activations, atom_name, activation)

        # Update entity type distribution
        if word_occ.entity_type:
            pattern.entity_type_distribution[word_occ.entity_type] = \
                pattern.entity_type_distribution.get(word_occ.entity_type, 0) + 1

        # Update EMA for confidence and coherence
        if word_occ.entity_confidence > 0:
            pattern.confidence_ema = (
                self.ema_alpha * word_occ.entity_confidence +
                (1.0 - self.ema_alpha) * pattern.confidence_ema
            )

        if word_occ.entity_coherence > 0:
            pattern.coherence_ema = (
                self.ema_alpha * word_occ.entity_coherence +
                (1.0 - self.ema_alpha) * pattern.coherence_ema
            )

    def _update_running_stats(
        self,
        stats_dict: Dict[str, Dict[str, float]],
        key: str,
        value: float
    ):
        """
        Update running mean and standard deviation.

        Args:
            stats_dict: Dictionary to store stats
            key: Statistic key (e.g., "entity_recall")
            value: New value to incorporate
        """
        if key not in stats_dict:
            stats_dict[key] = {'mean': value, 'std': 0.0, 'count': 1}
        else:
            stats = stats_dict[key]
            count = stats['count']
            old_mean = stats['mean']

            # Update mean
            new_mean = (old_mean * count + value) / (count + 1)

            # Update variance (Welford's online algorithm)
            if count > 1:
                old_variance = stats['std'] ** 2
                new_variance = (
                    (count - 1) * old_variance +
                    (value - old_mean) * (value - new_mean)
                ) / count
                stats['std'] = float(np.sqrt(max(0, new_variance)))

            stats['mean'] = new_mean
            stats['count'] = count + 1

    def _update_word_pair_patterns(
        self,
        word_occ: WordOccasion,
        all_word_occasions: List[WordOccasion]
    ):
        """
        Update word pair patterns for multi-word entity detection.

        Args:
            word_occ: Current WordOccasion
            all_word_occasions: All WordOccasions from this turn
        """
        # Find adjacent entity
        for other_occ in all_word_occasions:
            if not other_occ.is_entity():
                continue

            # Check if adjacent (position difference = 1)
            if abs(word_occ.position - other_occ.position) == 1:
                # Create word pair key (ordered by position)
                if word_occ.position < other_occ.position:
                    pair_key = (word_occ.word, other_occ.word)
                else:
                    pair_key = (other_occ.word, word_occ.word)

                # Update pair pattern
                if pair_key not in self.word_pair_patterns:
                    self.word_pair_patterns[pair_key] = {
                        'count': 0,
                        'merge_coherence': 0.0,
                        'entity_type': None
                    }

                pair_pattern = self.word_pair_patterns[pair_key]
                pair_pattern['count'] += 1

                # Compute merge coherence (cosine similarity of actualization vectors)
                if (word_occ.actualization_vector is not None and
                    other_occ.actualization_vector is not None):
                    vec1 = word_occ.actualization_vector
                    vec2 = other_occ.actualization_vector

                    dot_product = np.dot(vec1, vec2)
                    norm1 = np.linalg.norm(vec1)
                    norm2 = np.linalg.norm(vec2)

                    if norm1 > 0 and norm2 > 0:
                        coherence = float(dot_product / (norm1 * norm2))

                        # Update EMA
                        pair_pattern['merge_coherence'] = (
                            self.ema_alpha * coherence +
                            (1.0 - self.ema_alpha) * pair_pattern['merge_coherence']
                        )

                # Store most common entity type for pair
                if word_occ.entity_type:
                    pair_pattern['entity_type'] = word_occ.entity_type

    def predict_entity_type(
        self,
        word: str,
        left_neighbors: List[str],
        right_neighbors: List[str]
    ) -> Tuple[Optional[str], float]:
        """
        Predict entity type for a word based on learned patterns.

        Args:
            word: The word to classify
            left_neighbors: Left neighbor words
            right_neighbors: Right neighbor words

        Returns:
            (predicted_entity_type, confidence)
            Returns (None, 0.0) if no pattern or confidence too low
        """
        # Check if we have pattern for this word
        if word not in self.word_patterns:
            return None, 0.0

        pattern = self.word_patterns[word]

        # Require minimum mentions
        if pattern.mention_count < self.min_mentions_for_pattern:
            return None, 0.0

        # Get most common entity type
        if not pattern.entity_type_distribution:
            return None, 0.0

        most_common_type = max(
            pattern.entity_type_distribution,
            key=pattern.entity_type_distribution.get
        )

        # Base confidence from EMA
        base_confidence = pattern.confidence_ema

        # Boost confidence if neighbors match learned patterns
        neighbor_boost = self._compute_neighbor_boost(
            pattern, left_neighbors, right_neighbors
        )

        final_confidence = min(1.0, base_confidence + neighbor_boost)

        self.total_predictions += 1

        return most_common_type, final_confidence

    def _compute_neighbor_boost(
        self,
        pattern: WordPattern,
        left_neighbors: List[str],
        right_neighbors: List[str]
    ) -> float:
        """
        Compute confidence boost based on neighbor matching.

        Args:
            pattern: Learned word pattern
            left_neighbors: Current left neighbors
            right_neighbors: Current right neighbors

        Returns:
            Boost value (0.0-0.2)
        """
        boost = 0.0

        # Check left neighbor matches
        for neighbor in left_neighbors[-3:]:  # Last 3 left neighbors
            if neighbor in pattern.left_neighbors:
                frequency = pattern.left_neighbors[neighbor] / pattern.mention_count
                boost += frequency * 0.1  # Max 0.1 boost from left

        # Check right neighbor matches
        for neighbor in right_neighbors[:3]:  # First 3 right neighbors
            if neighbor in pattern.right_neighbors:
                frequency = pattern.right_neighbors[neighbor] / pattern.mention_count
                boost += frequency * 0.1  # Max 0.1 boost from right

        return min(0.2, boost)  # Cap at 0.2 total

    def update_from_ground_truth(self, ground_truth: Dict[str, Any]):
        """
        Update word patterns from linguistic ground truth annotations.

        🌀 Phase 0A: Linguistic Foundation (Nov 19, 2025)
        Learn POS tags, entity types, dependencies from spaCy annotations.

        Args:
            ground_truth: Dict with keys ['text', 'tokens', 'entities', 'noun_chunks']
                tokens: List of dicts with 'word', 'pos', 'tag', 'entity_type', 'entity_iob', etc.
                entities: List of dicts with 'text', 'type', 'start', 'end'
                noun_chunks: List of dicts with 'text', 'start', 'end', 'root'
        """
        tokens = ground_truth.get('tokens', [])

        for token_data in tokens:
            word = token_data['word']

            # Skip punctuation and stopwords for now (focus on content words)
            if token_data.get('is_punct', False):
                continue

            # Get or create pattern
            if word not in self.word_patterns:
                self.word_patterns[word] = WordPattern(word=word)

            pattern = self.word_patterns[word]

            # Update mention count
            pattern.mention_count += 1
            pattern.last_seen = time.time()

            # Learn POS tag distribution
            pos_tag = token_data.get('pos', 'UNKNOWN')
            if 'pos_distribution' not in pattern.organ_activations:
                pattern.organ_activations['pos_distribution'] = {}
            pattern.organ_activations['pos_distribution'][pos_tag] = \
                pattern.organ_activations['pos_distribution'].get(pos_tag, 0) + 1

            # Learn entity type if present
            entity_type = token_data.get('entity_type')
            if entity_type:
                pattern.entity_type_distribution[entity_type] = \
                    pattern.entity_type_distribution.get(entity_type, 0) + 1

        # Learn neighbor patterns from adjacent tokens
        for i, token in enumerate(tokens):
            if token.get('is_punct', False):
                continue

            word = token['word']

            # Left neighbors (up to 2 words back)
            for j in range(max(0, i-2), i):
                if not tokens[j].get('is_punct', False):
                    left_neighbor = tokens[j]['word']
                    if word in self.word_patterns:
                        self.word_patterns[word].left_neighbors[left_neighbor] = \
                            self.word_patterns[word].left_neighbors.get(left_neighbor, 0) + 1

            # Right neighbors (up to 2 words forward)
            for j in range(i+1, min(len(tokens), i+3)):
                if not tokens[j].get('is_punct', False):
                    right_neighbor = tokens[j]['word']
                    if word in self.word_patterns:
                        self.word_patterns[word].right_neighbors[right_neighbor] = \
                            self.word_patterns[word].right_neighbors.get(right_neighbor, 0) + 1

        self.total_updates += 1

        # Save every 10 updates
        if self.total_updates % 10 == 0:
            self._save_patterns()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get tracker statistics.

        Returns:
            Dictionary with tracker stats
        """
        return {
            'total_word_patterns': len(self.word_patterns),
            'total_word_pair_patterns': len(self.word_pair_patterns),
            'total_updates': self.total_updates,
            'total_predictions': self.total_predictions,
            'prediction_accuracy': self.prediction_accuracy,
            'words_with_sufficient_mentions': sum(
                1 for p in self.word_patterns.values()
                if p.mention_count >= self.min_mentions_for_pattern
            )
        }

    # =========================================================================
    # 🌀 PHASE 0.5: HYBRID WORD-FAMILY ARCHITECTURE (Nov 19, 2025)
    # =========================================================================
    # Embedding-based family transfer for scalable learning beyond corpus

    def _find_similar_via_embeddings(
        self,
        word: str,
        threshold: float = 0.70,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Find learned words with high embedding similarity (cosine > threshold).

        Uses spaCy 96D word vectors to find semantic neighbors among learned patterns.
        This enables family-based transfer: "daughter" → "child", "worried" → "anxious"

        🌀 Process Philosophy: Embeddings as eternal objects guiding occasion formation

        Args:
            word: Novel word to find similar learned words for
            threshold: Minimum cosine similarity (default: 0.70)
            top_k: Maximum number of similar words to return

        Returns:
            List of (similar_word, similarity_score) tuples, sorted by similarity descending
        """
        try:
            import spacy

            # Load spaCy model (cached after first load)
            if not hasattr(self, '_nlp'):
                self._nlp = spacy.load('en_core_web_sm')

            # Get embedding for novel word
            novel_token = self._nlp(word)
            if not novel_token[0].has_vector:
                # Word not in spaCy vocabulary
                return []

            novel_vec = novel_token[0].vector

            # Find similar words among learned patterns
            similarities = []
            for learned_word, pattern in self.word_patterns.items():
                # Skip if insufficient mentions
                if pattern.mention_count < self.min_mentions_for_pattern:
                    continue

                # Get embedding for learned word
                learned_token = self._nlp(learned_word)
                if not learned_token[0].has_vector:
                    continue

                learned_vec = learned_token[0].vector

                # Compute cosine similarity
                dot_product = np.dot(novel_vec, learned_vec)
                norm_product = np.linalg.norm(novel_vec) * np.linalg.norm(learned_vec)

                if norm_product > 0:
                    similarity = dot_product / norm_product

                    if similarity >= threshold:
                        similarities.append((learned_word, float(similarity)))

            # Sort by similarity descending, return top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]

        except Exception as e:
            print(f"⚠️  Embedding similarity failed for '{word}': {e}")
            return []

    def _transfer_from_family(
        self,
        word: str,
        similar_words: List[Tuple[str, float]],
        decay_factor: float = 0.7
    ) -> Optional[WordPattern]:
        """
        Transfer learned patterns from similar words (family-based generalization).

        Weighted transfer based on embedding similarity:
        - POS distribution: Average weighted by similarity
        - Entity types: Merge weighted distributions
        - Neighbor patterns: Union of top neighbors (weighted)
        - Confidence: Decay by factor (medium confidence 0.5-0.7)

        🌀 Process Philosophy: Family as nexus of similar occasions, patterns as propositions

        Args:
            word: Novel word to create pattern for
            similar_words: List of (similar_word, similarity) from _find_similar_via_embeddings
            decay_factor: Confidence decay for transferred patterns (default: 0.7)

        Returns:
            Transferred WordPattern with medium confidence, or None if transfer fails
        """
        if not similar_words:
            return None

        try:
            # Initialize transferred pattern
            transferred = WordPattern(word=word)
            transferred.mention_count = 1  # Virtual mention
            transferred.first_seen = time.time()
            transferred.last_seen = time.time()

            # Aggregate POS distribution (weighted average)
            pos_dist = {}
            entity_type_dist = {}
            left_neighbors = {}
            right_neighbors = {}
            organ_activations = {}

            total_weight = sum(sim for _, sim in similar_words)

            for similar_word, similarity in similar_words:
                if similar_word not in self.word_patterns:
                    continue

                pattern = self.word_patterns[similar_word]
                weight = similarity / total_weight

                # Transfer POS distribution (if available)
                if hasattr(pattern, 'pos_distribution'):
                    for pos, count in pattern.pos_distribution.items():
                        pos_dist[pos] = pos_dist.get(pos, 0) + (count * weight)

                # Transfer entity type distribution
                for entity_type, count in pattern.entity_type_distribution.items():
                    entity_type_dist[entity_type] = entity_type_dist.get(entity_type, 0) + (count * weight)

                # Transfer top neighbors (union with weights)
                for neighbor, count in list(pattern.left_neighbors.items())[:10]:
                    left_neighbors[neighbor] = left_neighbors.get(neighbor, 0) + (count * weight)

                for neighbor, count in list(pattern.right_neighbors.items())[:10]:
                    right_neighbors[neighbor] = right_neighbors.get(neighbor, 0) + (count * weight)

                # Transfer organ activations (weighted mean)
                for organ, stats in pattern.organ_activations.items():
                    # Handle both dict and non-dict stats formats
                    if isinstance(stats, dict):
                        mean_val = stats.get('mean', 0.0)
                        std_val = stats.get('std', 0.0)
                    else:
                        # If stats is a scalar, treat it as mean
                        mean_val = float(stats)
                        std_val = 0.0

                    if organ not in organ_activations:
                        organ_activations[organ] = {'mean': 0.0, 'std': 0.0, 'count': 0}
                    organ_activations[organ]['mean'] += mean_val * weight
                    organ_activations[organ]['std'] += std_val * weight

                # Transfer confidence/coherence (weighted average)
                transferred.confidence_ema += pattern.confidence_ema * weight
                transferred.coherence_ema += pattern.coherence_ema * weight

            # Assign transferred data
            if hasattr(transferred, 'pos_distribution'):
                transferred.pos_distribution = {k: int(v) for k, v in pos_dist.items()}
            transferred.entity_type_distribution = {k: int(v) for k, v in entity_type_dist.items()}
            transferred.left_neighbors = {k: int(v) for k, v in left_neighbors.items()}
            transferred.right_neighbors = {k: int(v) for k, v in right_neighbors.items()}
            transferred.organ_activations = organ_activations

            # Apply decay factor to confidence (medium confidence range)
            transferred.confidence_ema *= decay_factor
            transferred.coherence_ema *= decay_factor

            return transferred

        except Exception as e:
            print(f"⚠️  Pattern transfer failed for '{word}': {e}")
            return None

    def predict_pattern_for_novel_word(
        self,
        word: str,
        context: Optional[Dict[str, Any]] = None,
        return_source: bool = False
    ) -> Union[Tuple[Optional[WordPattern], float], Tuple[Optional[WordPattern], float, str]]:
        """
        3-Tier cascade prediction for novel words (learned → family → LLM).

        Tier 1: Learned pattern (HIGH confidence 0.8-0.95)
            - Word exists in learned patterns with sufficient mentions
            - Return stored pattern directly

        Tier 2: Family transfer via embeddings (MEDIUM confidence 0.5-0.7)
            - Find similar words via spaCy embeddings (cosine > 0.70)
            - Transfer weighted patterns from semantic family
            - Enables: "daughter" → "child", "anxious" → "worried"

        Tier 3: LLM fallback (LOW confidence 0.3-0.5) [FUTURE - Phase 1]
            - Query LLM for entity prediction
            - Learn from LLM output (symbiotic learning)
            - Continuous improvement from each conversation

        🌀 Process Philosophy:
        - Tier 1 = Actual occasions (concrete learning)
        - Tier 2 = Eternal objects (abstract families)
        - Tier 3 = Hybrid lure (LLM-guided prehension)

        Args:
            word: Novel word to predict pattern for
            context: Optional context dict (left/right neighbors, sentence, etc.)
            return_source: If True, return (pattern, confidence, source_tier)

        Returns:
            If return_source=False: (pattern, confidence)
            If return_source=True: (pattern, confidence, source_tier)
                where source_tier in ['learned', 'family', 'llm', 'none']
        """
        # Tier 1: Learned pattern (HIGH confidence)
        if word in self.word_patterns:
            pattern = self.word_patterns[word]
            if pattern.mention_count >= self.min_mentions_for_pattern:
                confidence = 0.80 + min(pattern.confidence_ema * 0.15, 0.15)  # 0.80-0.95
                if return_source:
                    return pattern, confidence, 'learned'
                return pattern, confidence

        # Tier 2: Family transfer via embeddings (MEDIUM confidence)
        similar_words = self._find_similar_via_embeddings(word, threshold=0.70, top_k=5)

        if similar_words:
            transferred_pattern = self._transfer_from_family(word, similar_words, decay_factor=0.7)

            if transferred_pattern:
                # Confidence based on best similarity score
                best_similarity = similar_words[0][1]
                confidence = 0.50 + (best_similarity - 0.70) * 0.50  # 0.50-0.65 range

                if return_source:
                    return transferred_pattern, confidence, 'family'
                return transferred_pattern, confidence

        # Tier 3: LLM fallback (LOW confidence) [FUTURE - Phase 1]
        # TODO: Implement LLM query + symbiotic learning
        # For now, return None (no prediction)

        if return_source:
            return None, 0.0, 'none'
        return None, 0.0

    # =========================================================================
    # END PHASE 0.5 METHODS
    # =========================================================================

    # =========================================================================
    # PHASE 0B METHODS - Entity-Contextualized Prediction
    # =========================================================================

    def predict_with_entity_context(
        self,
        word: str,
        nearby_entities: Optional[List[Dict[str, Any]]] = None,
        context: Optional[Dict[str, Any]] = None,
        word_entity_bridge: Optional[Any] = None
    ) -> Tuple[Optional[WordPattern], float, str]:
        """
        Phase 0B: Entity-contextualized word prediction.

        Enhances Phase 0.5 cascade with entity context for improved confidence.

        Args:
            word: Word to predict pattern for
            nearby_entities: List of {value, type, distance} dicts for entities near word
            context: Optional context dict
            word_entity_bridge: WordEntityBridge instance (from Phase 0B)

        Returns:
            (pattern, confidence, source) where source includes entity context info
        """
        # Get base prediction from 3-tier cascade
        base_pattern, base_confidence, base_source = self.predict_pattern_for_novel_word(
            word=word,
            context=context,
            return_source=True
        )

        # If no bridge provided, return base prediction
        if word_entity_bridge is None or nearby_entities is None:
            return base_pattern, base_confidence, base_source

        # Enhance with entity context if available
        try:
            enhanced_pattern, enhanced_confidence, entity_source = \
                word_entity_bridge.predict_with_entity_context(
                    word=word,
                    nearby_entities=nearby_entities,
                    base_prediction=(base_pattern, base_confidence)
                )

            # If entity context provided boost, update source
            if entity_source != 'base':
                return enhanced_pattern, enhanced_confidence, f"{base_source}_with_{entity_source}"
            else:
                return base_pattern, base_confidence, base_source

        except Exception as e:
            print(f"⚠️  Entity context enhancement failed for '{word}': {e}")
            return base_pattern, base_confidence, base_source

    # =========================================================================
    # END PHASE 0B METHODS
    # =========================================================================

    def _save_patterns(self):
        """Save word patterns to JSON file."""
        try:
            # Convert to serializable format
            data = {
                'word_patterns': {},
                'word_pair_patterns': {},
                'statistics': self.get_statistics(),
                'timestamp': time.time()
            }

            # Serialize word patterns
            for word, pattern in self.word_patterns.items():
                data['word_patterns'][word] = {
                    'mention_count': pattern.mention_count,
                    'positions': pattern.positions[-10:],  # Last 10 positions
                    'left_neighbors': dict(sorted(
                        pattern.left_neighbors.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:20]),  # Top 20 neighbors
                    'right_neighbors': dict(sorted(
                        pattern.right_neighbors.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:20]),
                    'organ_activations': pattern.organ_activations,
                    'entity_type_distribution': pattern.entity_type_distribution,
                    'confidence_ema': pattern.confidence_ema,
                    'coherence_ema': pattern.coherence_ema,
                    'first_seen': pattern.first_seen,
                    'last_seen': pattern.last_seen
                }

            # Serialize word pair patterns
            for pair_key, pair_pattern in self.word_pair_patterns.items():
                data['word_pair_patterns'][f"{pair_key[0]}_{pair_key[1]}"] = pair_pattern

            # Write to file
            Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Failed to save word patterns: {e}")

    def _load_patterns(self):
        """Load word patterns from JSON file."""
        try:
            if not Path(self.storage_path).exists():
                return

            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Load word patterns
            for word, pattern_data in data.get('word_patterns', {}).items():
                self.word_patterns[word] = WordPattern(
                    word=word,
                    mention_count=pattern_data['mention_count'],
                    positions=pattern_data['positions'],
                    left_neighbors=pattern_data['left_neighbors'],
                    right_neighbors=pattern_data['right_neighbors'],
                    organ_activations=pattern_data['organ_activations'],
                    entity_type_distribution=pattern_data['entity_type_distribution'],
                    confidence_ema=pattern_data['confidence_ema'],
                    coherence_ema=pattern_data['coherence_ema'],
                    first_seen=pattern_data['first_seen'],
                    last_seen=pattern_data['last_seen']
                )

            # Load word pair patterns
            for pair_str, pair_pattern in data.get('word_pair_patterns', {}).items():
                words = pair_str.split('_', 1)
                if len(words) == 2:
                    self.word_pair_patterns[(words[0], words[1])] = pair_pattern

            # Load statistics
            stats = data.get('statistics', {})
            self.total_updates = stats.get('total_updates', 0)
            self.total_predictions = stats.get('total_predictions', 0)
            self.prediction_accuracy = stats.get('prediction_accuracy', 0.0)

            print(f"✅ Loaded {len(self.word_patterns)} word patterns, {len(self.word_pair_patterns)} pair patterns")

        except Exception as e:
            print(f"⚠️  Failed to load word patterns: {e}")


if __name__ == "__main__":
    """
    Validation test for WordOccasionTracker.
    """
    print("=" * 80)
    print("🧪 WORD OCCASION TRACKER VALIDATION TEST")
    print("=" * 80)

    # Test 1: Initialize tracker
    print("\n📋 TEST 1: Initialize Tracker")
    tracker = WordOccasionTracker(storage_path="/tmp/test_word_patterns.json")
    print(f"   ✅ Storage path: {tracker.storage_path}")
    print(f"   ✅ EMA alpha: {tracker.ema_alpha}")
    print(f"   ✅ Min mentions: {tracker.min_mentions_for_pattern}")

    # Test 2: Create mock WordOccasions
    print("\n📋 TEST 2: Mock Word Occasion Learning")
    from transductive.word_occasion import WordOccasion

    # Simulate 5 mentions of "Emma" with similar patterns
    for i in range(5):
        emma = WordOccasion(
            word="Emma",
            position=i + 1,
            sentence=f"Sentence {i} about Emma",
            left_neighbors=["my", "daughter"] if i % 2 == 0 else ["worried", "about"],
            right_neighbors=["went", "to"]
        )
        emma.entity_type = "Person"
        emma.entity_confidence = 0.85 + (i * 0.01)
        emma.entity_coherence = 0.80 + (i * 0.01)
        emma.actualization_vector = np.array([0.85, 0.70, 0.65, 0.60, 0.55, 0.50, 0.75])

        tracker.update([emma])

    stats = tracker.get_statistics()
    print(f"   ✅ Total word patterns: {stats['total_word_patterns']}")
    print(f"   ✅ Words with sufficient mentions: {stats['words_with_sufficient_mentions']}")

    # Test 3: Pattern retrieval
    print("\n📋 TEST 3: Pattern Retrieval")
    if "Emma" in tracker.word_patterns:
        pattern = tracker.word_patterns["Emma"]
        print(f"   ✅ Mention count: {pattern.mention_count}")
        print(f"   ✅ Confidence EMA: {pattern.confidence_ema:.3f}")
        print(f"   ✅ Left neighbors: {dict(list(pattern.left_neighbors.items())[:3])}")
        print(f"   ✅ Entity type dist: {pattern.entity_type_distribution}")

    # Test 4: Prediction
    print("\n📋 TEST 4: Entity Type Prediction")
    predicted_type, confidence = tracker.predict_entity_type(
        word="Emma",
        left_neighbors=["my", "daughter"],
        right_neighbors=["went", "to"]
    )
    print(f"   ✅ Predicted type: {predicted_type}")
    print(f"   ✅ Confidence: {confidence:.3f}")

    # Test 5: Save/Load
    print("\n📋 TEST 5: Save and Load Patterns")
    tracker._save_patterns()
    print(f"   ✅ Patterns saved")

    tracker2 = WordOccasionTracker(storage_path="/tmp/test_word_patterns.json")
    print(f"   ✅ Loaded {len(tracker2.word_patterns)} patterns")

    print("\n" + "=" * 80)
    print("✅ WORD OCCASION TRACKER VALIDATION PASSED!")
    print("=" * 80)
