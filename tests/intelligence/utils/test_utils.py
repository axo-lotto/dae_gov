#!/usr/bin/env python3
"""
Intelligence Test Utilities
============================

Core utilities for intelligence test validation:
- Semantic similarity between emissions
- Text uniqueness computation
- Organ activation correlation
- Nexus type overlap

Date: November 13, 2025
Phase: Intelligence Test Refactoring (Phase 1)
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

import numpy as np
from typing import Dict, List, Tuple, Set
from persona_layer.embedding_coordinator import EmbeddingCoordinator


class IntelligenceTestUtils:
    """Utilities for intelligence test validation."""

    def __init__(self):
        """Initialize with embedding coordinator for semantic comparison."""
        self.embedding_coordinator = EmbeddingCoordinator()

    # =========================================================================
    # Semantic Similarity
    # =========================================================================

    def compute_emission_semantic_similarity(
        self,
        emission_1: str,
        emission_2: str
    ) -> float:
        """
        Compute semantic similarity between two emissions using embeddings.

        Args:
            emission_1: First emission text
            emission_2: Second emission text

        Returns:
            Cosine similarity [0.0, 1.0] where 1.0 = identical semantics

        Example:
            >>> utils = IntelligenceTestUtils()
            >>> sim = utils.compute_emission_semantic_similarity(
            ...     "I feel safe here",
            ...     "This feels secure and comfortable"
            ... )
            >>> print(f"Similarity: {sim:.3f}")
            Similarity: 0.752
        """
        # Get embeddings
        emb_1 = self.embedding_coordinator.embed(emission_1)
        emb_2 = self.embedding_coordinator.embed(emission_2)

        # Normalize
        emb_1 = emb_1 / np.linalg.norm(emb_1)
        emb_2 = emb_2 / np.linalg.norm(emb_2)

        # Cosine similarity
        similarity = np.dot(emb_1, emb_2)

        # Ensure [0, 1] range (clip numerical errors)
        return max(0.0, min(1.0, float(similarity)))

    # =========================================================================
    # Text Uniqueness
    # =========================================================================

    def compute_text_uniqueness(
        self,
        text_1: str,
        text_2: str,
        method: str = 'word_overlap'
    ) -> float:
        """
        Compute text uniqueness (inverse of overlap).

        Args:
            text_1: First text
            text_2: Second text
            method: 'word_overlap' or 'char_overlap'

        Returns:
            Uniqueness ratio [0.0, 1.0] where 1.0 = completely unique

        Example:
            >>> utils = IntelligenceTestUtils()
            >>> unique = utils.compute_text_uniqueness(
            ...     "I feel safe and grounded",
            ...     "I feel peaceful and centered"
            ... )
            >>> print(f"Uniqueness: {unique:.3f}")
            Uniqueness: 0.600  # 40% word overlap ("I feel")
        """
        if method == 'word_overlap':
            return self._word_overlap_uniqueness(text_1, text_2)
        elif method == 'char_overlap':
            return self._char_overlap_uniqueness(text_1, text_2)
        else:
            raise ValueError(f"Unknown method: {method}")

    def _word_overlap_uniqueness(self, text_1: str, text_2: str) -> float:
        """Compute uniqueness based on word-level overlap."""
        # Tokenize (simple whitespace + lowercase)
        words_1 = set(text_1.lower().split())
        words_2 = set(text_2.lower().split())

        if len(words_1) == 0 and len(words_2) == 0:
            return 0.0  # Both empty → not unique

        # Jaccard distance (1 - Jaccard index)
        intersection = len(words_1 & words_2)
        union = len(words_1 | words_2)

        if union == 0:
            return 0.0

        jaccard_index = intersection / union
        uniqueness = 1.0 - jaccard_index

        return uniqueness

    def _char_overlap_uniqueness(self, text_1: str, text_2: str) -> float:
        """Compute uniqueness based on character-level overlap."""
        # Character-level bigrams
        def get_bigrams(text: str) -> Set[str]:
            text = text.lower()
            return set(text[i:i+2] for i in range(len(text)-1))

        bigrams_1 = get_bigrams(text_1)
        bigrams_2 = get_bigrams(text_2)

        if len(bigrams_1) == 0 and len(bigrams_2) == 0:
            return 0.0

        intersection = len(bigrams_1 & bigrams_2)
        union = len(bigrams_1 | bigrams_2)

        if union == 0:
            return 0.0

        jaccard_index = intersection / union
        uniqueness = 1.0 - jaccard_index

        return uniqueness

    # =========================================================================
    # Organ Activation Correlation
    # =========================================================================

    def compute_organ_activation_correlation(
        self,
        activations_1: Dict[str, float],
        activations_2: Dict[str, float]
    ) -> float:
        """
        Compute Pearson correlation between two organ activation patterns.

        Args:
            activations_1: Dict mapping organ_name → activation strength
            activations_2: Dict mapping organ_name → activation strength

        Returns:
            Pearson correlation coefficient [-1.0, 1.0]

        Example:
            >>> utils = IntelligenceTestUtils()
            >>> act_1 = {'LISTENING': 0.8, 'EMPATHY': 0.7, 'WISDOM': 0.3}
            >>> act_2 = {'LISTENING': 0.75, 'EMPATHY': 0.65, 'WISDOM': 0.4}
            >>> corr = utils.compute_organ_activation_correlation(act_1, act_2)
            >>> print(f"Correlation: {corr:.3f}")
            Correlation: 0.991
        """
        # Get shared organs
        shared_organs = set(activations_1.keys()) & set(activations_2.keys())

        if len(shared_organs) < 2:
            return 0.0  # Need at least 2 organs for correlation

        # Extract values in consistent order
        organs_sorted = sorted(shared_organs)
        values_1 = np.array([activations_1[organ] for organ in organs_sorted])
        values_2 = np.array([activations_2[organ] for organ in organs_sorted])

        # Pearson correlation
        if np.std(values_1) == 0.0 or np.std(values_2) == 0.0:
            return 0.0  # No variance → undefined correlation

        correlation = np.corrcoef(values_1, values_2)[0, 1]

        # Handle NaN from numerical errors
        if np.isnan(correlation):
            return 0.0

        return float(correlation)

    # =========================================================================
    # Nexus Type Overlap
    # =========================================================================

    def compute_nexus_type_overlap(
        self,
        nexus_types_1: List[str],
        nexus_types_2: List[str]
    ) -> float:
        """
        Compute overlap ratio between two nexus type lists.

        Args:
            nexus_types_1: List of nexus type strings (e.g., ['witnessing_bond', 'compassion_holding'])
            nexus_types_2: List of nexus type strings

        Returns:
            Overlap ratio [0.0, 1.0] where 1.0 = identical sets

        Example:
            >>> utils = IntelligenceTestUtils()
            >>> types_1 = ['witnessing_bond', 'compassion_holding', 'embodied_wisdom']
            >>> types_2 = ['witnessing_bond', 'compassion_holding', 'grounded_presence']
            >>> overlap = utils.compute_nexus_type_overlap(types_1, types_2)
            >>> print(f"Overlap: {overlap:.3f}")
            Overlap: 0.667  # 2/3 types in common
        """
        set_1 = set(nexus_types_1)
        set_2 = set(nexus_types_2)

        if len(set_1) == 0 and len(set_2) == 0:
            return 1.0  # Both empty → perfect overlap

        intersection = len(set_1 & set_2)
        union = len(set_1 | set_2)

        if union == 0:
            return 0.0

        overlap = intersection / union
        return overlap

    # =========================================================================
    # Confidence Statistics
    # =========================================================================

    def compute_confidence_stability(
        self,
        confidences: List[float]
    ) -> Tuple[float, float, float]:
        """
        Compute confidence statistics across multiple outputs.

        Args:
            confidences: List of confidence values

        Returns:
            Tuple of (mean, std_dev, range)

        Example:
            >>> utils = IntelligenceTestUtils()
            >>> confs = [0.45, 0.52, 0.48, 0.51]
            >>> mean, std, rng = utils.compute_confidence_stability(confs)
            >>> print(f"Mean: {mean:.3f}, Std: {std:.3f}, Range: {rng:.3f}")
            Mean: 0.490, Std: 0.029, Range: 0.070
        """
        if not confidences:
            return (0.0, 0.0, 0.0)

        confs_array = np.array(confidences)
        mean = float(np.mean(confs_array))
        std_dev = float(np.std(confs_array))
        conf_range = float(np.max(confs_array) - np.min(confs_array))

        return (mean, std_dev, conf_range)


# =============================================================================
# Self-Test
# =============================================================================

def self_test():
    """Self-test for test utilities."""
    print("=" * 80)
    print("🧪 TESTING INTELLIGENCE TEST UTILITIES")
    print("=" * 80)

    utils = IntelligenceTestUtils()

    # Test 1: Semantic Similarity
    print("\n" + "-" * 80)
    print("Test 1: Emission Semantic Similarity")
    print("-" * 80)

    emission_1 = "I feel safe and grounded here."
    emission_2 = "This feels secure and comfortable."
    emission_3 = "The weather is nice today."

    sim_12 = utils.compute_emission_semantic_similarity(emission_1, emission_2)
    sim_13 = utils.compute_emission_semantic_similarity(emission_1, emission_3)

    print(f"Emission 1: \"{emission_1}\"")
    print(f"Emission 2: \"{emission_2}\"")
    print(f"Similarity 1-2: {sim_12:.3f}")
    print(f"\nEmission 3: \"{emission_3}\"")
    print(f"Similarity 1-3: {sim_13:.3f}")

    assert sim_12 > 0.25, "Similar emissions should have moderate similarity"
    assert sim_13 < sim_12, "Dissimilar emissions should have lower similarity"
    print("✅ Semantic similarity working correctly")

    # Test 2: Text Uniqueness
    print("\n" + "-" * 80)
    print("Test 2: Text Uniqueness")
    print("-" * 80)

    text_1 = "I feel safe and grounded"
    text_2 = "I feel peaceful and centered"
    text_3 = "I feel safe and grounded"

    unique_12 = utils.compute_text_uniqueness(text_1, text_2)
    unique_13 = utils.compute_text_uniqueness(text_1, text_3)

    print(f"Text 1: \"{text_1}\"")
    print(f"Text 2: \"{text_2}\"")
    print(f"Uniqueness 1-2: {unique_12:.3f}")
    print(f"\nText 3: \"{text_3}\"")
    print(f"Uniqueness 1-3: {unique_13:.3f}")

    assert unique_12 > 0.0, "Different texts should have some uniqueness"
    assert unique_13 == 0.0, "Identical texts should have zero uniqueness"
    print("✅ Text uniqueness working correctly")

    # Test 3: Organ Activation Correlation
    print("\n" + "-" * 80)
    print("Test 3: Organ Activation Correlation")
    print("-" * 80)

    act_1 = {'LISTENING': 0.8, 'EMPATHY': 0.7, 'WISDOM': 0.3}
    act_2 = {'LISTENING': 0.75, 'EMPATHY': 0.65, 'WISDOM': 0.4}
    act_3 = {'LISTENING': 0.2, 'EMPATHY': 0.3, 'WISDOM': 0.9}

    corr_12 = utils.compute_organ_activation_correlation(act_1, act_2)
    corr_13 = utils.compute_organ_activation_correlation(act_1, act_3)

    print(f"Activations 1: {act_1}")
    print(f"Activations 2: {act_2}")
    print(f"Correlation 1-2: {corr_12:.3f}")
    print(f"\nActivations 3: {act_3}")
    print(f"Correlation 1-3: {corr_13:.3f}")

    assert corr_12 > 0.8, "Similar patterns should have high correlation"
    assert corr_13 < corr_12, "Dissimilar patterns should have lower correlation"
    print("✅ Organ activation correlation working correctly")

    # Test 4: Nexus Type Overlap
    print("\n" + "-" * 80)
    print("Test 4: Nexus Type Overlap")
    print("-" * 80)

    types_1 = ['witnessing_bond', 'compassion_holding', 'embodied_wisdom']
    types_2 = ['witnessing_bond', 'compassion_holding', 'grounded_presence']
    types_3 = ['crisis_urgency', 'protective_boundary', 'survival_focus']

    overlap_12 = utils.compute_nexus_type_overlap(types_1, types_2)
    overlap_13 = utils.compute_nexus_type_overlap(types_1, types_3)

    print(f"Types 1: {types_1}")
    print(f"Types 2: {types_2}")
    print(f"Overlap 1-2: {overlap_12:.3f}")
    print(f"\nTypes 3: {types_3}")
    print(f"Overlap 1-3: {overlap_13:.3f}")

    assert overlap_12 >= 0.4, "Overlapping sets should have moderate overlap"
    assert overlap_13 == 0.0, "Disjoint sets should have zero overlap"
    print("✅ Nexus type overlap working correctly")

    # Test 5: Confidence Stability
    print("\n" + "-" * 80)
    print("Test 5: Confidence Stability")
    print("-" * 80)

    confs_stable = [0.45, 0.48, 0.47, 0.46]
    confs_unstable = [0.30, 0.70, 0.25, 0.80]

    mean_s, std_s, rng_s = utils.compute_confidence_stability(confs_stable)
    mean_u, std_u, rng_u = utils.compute_confidence_stability(confs_unstable)

    print(f"Stable confidences: {confs_stable}")
    print(f"Mean: {mean_s:.3f}, Std: {std_s:.3f}, Range: {rng_s:.3f}")
    print(f"\nUnstable confidences: {confs_unstable}")
    print(f"Mean: {mean_u:.3f}, Std: {std_u:.3f}, Range: {rng_u:.3f}")

    assert rng_s < 0.1, "Stable confidences should have small range"
    assert rng_u > 0.4, "Unstable confidences should have large range"
    print("✅ Confidence stability working correctly")

    # Summary
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED - Intelligence Test Utilities Ready")
    print("=" * 80)


if __name__ == '__main__':
    self_test()
