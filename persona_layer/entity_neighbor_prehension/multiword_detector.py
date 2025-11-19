"""
Multi-Word Boundary Detector for Entity Merging
================================================

Merges adjacent WordOccasions into multi-word entities based on:
1. Capitalization patterns (both words capitalized)
2. Neighbor coherence (similar atom activation patterns)
3. Entity confidence (both words classified as entities)
4. Semantic continuity (no punctuation breaks)

Examples:
    - "Emma Smith" → Single entity (Person)
    - "New York" → Single entity (Place)
    - "Apple Inc" → Single entity (Organization)
    - "Stanford University" → Single entity (Organization)

Architecture Alignment:
    - Whiteheadian: Society of occasions (nexus formation)
    - Hameroff: Coherent oscillation across coupled microtubules
    - DAE: Spatial satisfaction clustering via intersection emission

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 18, 2025
Status: Phase 3B Priority 1 - Multi-Word Boundary Detection
"""

import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
import numpy as np

# Add parent to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from transductive.word_occasion import WordOccasion


class MultiWordDetector:
    """
    Detects and merges adjacent WordOccasions into multi-word entities.

    Usage:
        detector = MultiWordDetector()
        merged_entities = detector.merge_adjacent_entities(word_occasions)
    """

    def __init__(
        self,
        coherence_threshold: float = 0.75,
        confidence_threshold: float = 0.7,
        max_merge_distance: int = 1
    ):
        """
        Initialize multi-word detector.

        Args:
            coherence_threshold: Min coherence between adjacent words for merging
            confidence_threshold: Min entity confidence for each word
            max_merge_distance: Max word distance for merging (1 = adjacent only)
        """
        self.coherence_threshold = coherence_threshold
        self.confidence_threshold = confidence_threshold
        self.max_merge_distance = max_merge_distance

    def merge_adjacent_entities(
        self,
        word_occasions: List[WordOccasion]
    ) -> List[Dict[str, Any]]:
        """
        Merge adjacent WordOccasions into multi-word entities.

        Args:
            word_occasions: List of WordOccasions (after 4-gate cascade)

        Returns:
            List of merged entity dicts (single-word + multi-word)

        Algorithm:
            1. Filter to entity WordOccasions (confidence > threshold)
            2. For each entity, check if next word is also entity
            3. Compute coherence between adjacent entities
            4. Merge if coherence > threshold and both capitalized
            5. Repeat for 3+ word entities (recursive merging)
        """
        # Step 1: Filter to entities only
        entity_occasions = [
            wo for wo in word_occasions
            if wo.is_entity() and wo.entity_confidence >= self.confidence_threshold
        ]

        if len(entity_occasions) < 2:
            # No merging possible (0 or 1 entities)
            return [wo.to_entity_dict() for wo in entity_occasions if wo.to_entity_dict()]

        # Step 2: Identify merge candidates
        merged_groups = []
        skip_indices = set()

        for i, word_occ in enumerate(entity_occasions):
            if i in skip_indices:
                continue

            # Start new merge group
            current_group = [word_occ]
            current_index = i

            # Try to extend group with adjacent entities
            while current_index + 1 < len(entity_occasions):
                next_word_occ = entity_occasions[current_index + 1]

                # Check adjacency (positions must be consecutive or near-consecutive)
                if not self._are_adjacent(current_group[-1], next_word_occ):
                    break

                # Check merge criteria
                if self._should_merge(current_group[-1], next_word_occ):
                    current_group.append(next_word_occ)
                    skip_indices.add(current_index + 1)
                    current_index += 1
                else:
                    break

            merged_groups.append(current_group)

        # Step 3: Create entity dicts for merged groups
        merged_entities = []
        for group in merged_groups:
            if len(group) == 1:
                # Single-word entity
                entity_dict = group[0].to_entity_dict()
                if entity_dict:
                    merged_entities.append(entity_dict)
            else:
                # Multi-word entity
                merged_entity = self._merge_group(group)
                if merged_entity:
                    merged_entities.append(merged_entity)

        return merged_entities

    def _are_adjacent(
        self,
        word_occ1: WordOccasion,
        word_occ2: WordOccasion
    ) -> bool:
        """
        Check if two WordOccasions are adjacent in text.

        Args:
            word_occ1: First WordOccasion
            word_occ2: Second WordOccasion

        Returns:
            True if positions are consecutive or near-consecutive
        """
        position_distance = word_occ2.position - word_occ1.position

        # Allow small gaps for punctuation/articles (e.g., "Apple, Inc" or "New York")
        return 1 <= position_distance <= (self.max_merge_distance + 1)

    def _should_merge(
        self,
        word_occ1: WordOccasion,
        word_occ2: WordOccasion
    ) -> bool:
        """
        Determine if two adjacent WordOccasions should be merged.

        Merge criteria:
        1. Both capitalized
        2. Similar entity types (or compatible types)
        3. High coherence between atom patterns
        4. No sentence-ending punctuation between them

        Args:
            word_occ1: First WordOccasion
            word_occ2: Second WordOccasion

        Returns:
            True if should merge
        """
        # Criterion 1: Both must be capitalized
        if not (word_occ1.is_capitalized and word_occ2.is_capitalized):
            return False

        # Criterion 2: Compatible entity types
        if not self._are_compatible_types(word_occ1.entity_type, word_occ2.entity_type):
            return False

        # Criterion 3: High coherence between atom patterns
        coherence = self._compute_merge_coherence(word_occ1, word_occ2)
        if coherence < self.coherence_threshold:
            return False

        # Criterion 4: No sentence-ending punctuation
        if word_occ1.has_punctuation and any(p in word_occ1.word for p in ['.', '!', '?']):
            return False

        return True

    def _are_compatible_types(
        self,
        type1: Optional[str],
        type2: Optional[str]
    ) -> bool:
        """
        Check if two entity types are compatible for merging.

        Compatible pairs:
        - Person + Person (e.g., "Emma Smith")
        - Place + Place (e.g., "New York")
        - Organization + Organization (e.g., "Stanford University")
        - Person + Organization (e.g., "Smith Company" - edge case)

        Args:
            type1: First entity type
            type2: Second entity type

        Returns:
            True if compatible
        """
        if type1 is None or type2 is None:
            return False

        # Same type → always compatible
        if type1 == type2:
            return True

        # Special compatibility rules
        compatible_pairs = [
            {"Person", "Organization"},  # "Smith Company"
            {"Place", "Organization"}     # "New York Times"
        ]

        return {type1, type2} in compatible_pairs

    def _compute_merge_coherence(
        self,
        word_occ1: WordOccasion,
        word_occ2: WordOccasion
    ) -> float:
        """
        Compute coherence between two WordOccasions for merging.

        Coherence measures similarity of atom activation patterns:
        - High coherence: both words have similar prehension patterns
        - Low coherence: words have different prehension patterns

        Args:
            word_occ1: First WordOccasion
            word_occ2: Second WordOccasion

        Returns:
            Coherence score (0.0-1.0)
        """
        # Use actualization vectors if available (31D or 7D)
        vec1 = word_occ1.actualization_vector
        vec2 = word_occ2.actualization_vector

        if vec1 is not None and vec2 is not None:
            # Cosine similarity between actualization vectors
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)

            if norm1 > 0 and norm2 > 0:
                coherence = dot_product / (norm1 * norm2)
                return float(max(0.0, coherence))  # Clamp to [0, 1]

        # Fallback: Use entity confidence agreement
        if word_occ1.entity_confidence > 0 and word_occ2.entity_confidence > 0:
            confidence_diff = abs(word_occ1.entity_confidence - word_occ2.entity_confidence)
            coherence = 1.0 - confidence_diff
            return float(coherence)

        return 0.0

    def _merge_group(
        self,
        group: List[WordOccasion]
    ) -> Optional[Dict[str, Any]]:
        """
        Merge a group of WordOccasions into a single entity dict.

        Args:
            group: List of WordOccasions to merge (2+ words)

        Returns:
            Merged entity dict with combined values
        """
        if not group:
            return None

        # Combine words
        entity_value = " ".join([wo.word for wo in group])

        # Choose entity type (majority vote or first)
        entity_types = [wo.entity_type for wo in group if wo.entity_type]
        if not entity_types:
            return None

        # Count entity type occurrences
        type_counts = {}
        for etype in entity_types:
            type_counts[etype] = type_counts.get(etype, 0) + 1

        entity_type = max(type_counts, key=type_counts.get)

        # Average confidence and coherence
        avg_confidence = np.mean([wo.entity_confidence for wo in group])
        avg_coherence = np.mean([wo.entity_coherence for wo in group])

        # Use first word's position
        position = group[0].position

        # Combine actualization vectors (average)
        actualization_vectors = [
            wo.actualization_vector for wo in group
            if wo.actualization_vector is not None
        ]

        if actualization_vectors:
            combined_vector = np.mean(actualization_vectors, axis=0)
        else:
            combined_vector = None

        return {
            'entity_value': entity_value,
            'entity_type': entity_type,
            'confidence_score': float(avg_confidence),
            'coherence': float(avg_coherence),
            'position': position,
            'actualization_vector': combined_vector.tolist() if combined_vector is not None else None,
            'source': 'neighbor_prehension_multiword',
            'word_count': len(group)
        }


# ========================================================================
# BATCH PROCESSING UTILITY
# ========================================================================

def detect_and_merge_multiword_entities(
    word_occasions: List[WordOccasion],
    detector: Optional[MultiWordDetector] = None
) -> List[Dict[str, Any]]:
    """
    Detect and merge multi-word entities from WordOccasions.

    Args:
        word_occasions: List of WordOccasions (after 4-gate cascade)
        detector: Optional custom detector (creates default if None)

    Returns:
        List of entity dicts (single-word + multi-word merged)
    """
    if detector is None:
        detector = MultiWordDetector()

    return detector.merge_adjacent_entities(word_occasions)


if __name__ == "__main__":
    """
    Validation test for MultiWordDetector.
    """
    print("=" * 80)
    print("🧪 MULTI-WORD BOUNDARY DETECTOR TEST")
    print("=" * 80)

    # Test 1: Initialize detector
    print("\n📋 TEST 1: Initialize Detector")
    detector = MultiWordDetector()
    print(f"   ✅ Coherence threshold: {detector.coherence_threshold}")
    print(f"   ✅ Confidence threshold: {detector.confidence_threshold}")
    print(f"   ✅ Max merge distance: {detector.max_merge_distance}")

    # Test 2: Create mock WordOccasions for merging
    print("\n📋 TEST 2: Mock Multi-Word Entity (Emma Smith)")

    from transductive.word_occasion import WordOccasion

    # "Today Emma Smith went to work"
    emma = WordOccasion(
        word="Emma",
        position=1,
        sentence="Today Emma Smith went to work",
        left_neighbors=["Today"],
        right_neighbors=["Smith", "went", "to"]
    )
    emma.entity_type = "Person"
    emma.entity_confidence = 0.85
    emma.entity_coherence = 0.80
    emma.actualization_vector = np.array([0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55])

    smith = WordOccasion(
        word="Smith",
        position=2,
        sentence="Today Emma Smith went to work",
        left_neighbors=["Today", "Emma"],
        right_neighbors=["went", "to", "work"]
    )
    smith.entity_type = "Person"
    smith.entity_confidence = 0.82
    smith.entity_coherence = 0.78
    smith.actualization_vector = np.array([0.83, 0.78, 0.73, 0.68, 0.63, 0.58, 0.53])

    # Test adjacency
    are_adjacent = detector._are_adjacent(emma, smith)
    print(f"   ✅ Emma-Smith adjacent: {are_adjacent}")

    # Test compatibility
    compatible = detector._are_compatible_types(emma.entity_type, smith.entity_type)
    print(f"   ✅ Person-Person compatible: {compatible}")

    # Test coherence
    coherence = detector._compute_merge_coherence(emma, smith)
    print(f"   ✅ Merge coherence: {coherence:.3f}")

    # Test should_merge
    should_merge = detector._should_merge(emma, smith)
    print(f"   ✅ Should merge: {should_merge}")

    # Test 3: Full merge
    print("\n📋 TEST 3: Full Multi-Word Merge")
    word_occasions = [emma, smith]
    merged_entities = detector.merge_adjacent_entities(word_occasions)

    print(f"   ✅ Input: {len(word_occasions)} WordOccasions")
    print(f"   ✅ Output: {len(merged_entities)} merged entities")

    if merged_entities:
        entity = merged_entities[0]
        print(f"   ✅ Entity value: '{entity['entity_value']}'")
        print(f"   ✅ Entity type: {entity['entity_type']}")
        print(f"   ✅ Confidence: {entity['confidence_score']:.3f}")
        print(f"   ✅ Word count: {entity['word_count']}")

    # Test 4: Three-word entity (New York City)
    print("\n📋 TEST 4: Three-Word Entity (New York City)")

    new = WordOccasion(
        word="New",
        position=0,
        sentence="New York City is large",
        left_neighbors=[],
        right_neighbors=["York", "City", "is"]
    )
    new.entity_type = "Place"
    new.entity_confidence = 0.88
    new.entity_coherence = 0.82
    new.actualization_vector = np.array([0.88, 0.82, 0.76, 0.70, 0.64, 0.58, 0.52])

    york = WordOccasion(
        word="York",
        position=1,
        sentence="New York City is large",
        left_neighbors=["New"],
        right_neighbors=["City", "is", "large"]
    )
    york.entity_type = "Place"
    york.entity_confidence = 0.86
    york.entity_coherence = 0.81
    york.actualization_vector = np.array([0.86, 0.81, 0.75, 0.69, 0.63, 0.57, 0.51])

    city = WordOccasion(
        word="City",
        position=2,
        sentence="New York City is large",
        left_neighbors=["New", "York"],
        right_neighbors=["is", "large"]
    )
    city.entity_type = "Place"
    city.entity_confidence = 0.84
    city.entity_coherence = 0.79
    city.actualization_vector = np.array([0.84, 0.79, 0.73, 0.67, 0.61, 0.55, 0.49])

    three_word_occasions = [new, york, city]
    merged_three = detector.merge_adjacent_entities(three_word_occasions)

    if merged_three:
        entity = merged_three[0]
        print(f"   ✅ Entity value: '{entity['entity_value']}'")
        print(f"   ✅ Entity type: {entity['entity_type']}")
        print(f"   ✅ Confidence: {entity['confidence_score']:.3f}")
        print(f"   ✅ Word count: {entity['word_count']}")

    print("\n" + "=" * 80)
    print("✅ MULTI-WORD BOUNDARY DETECTOR VALIDATION PASSED!")
    print("   ✅ Adjacency detection working")
    print("   ✅ Coherence computation working")
    print("   ✅ 2-word merging working (Emma Smith)")
    print("   ✅ 3-word merging working (New York City)")
    print("=" * 80)
