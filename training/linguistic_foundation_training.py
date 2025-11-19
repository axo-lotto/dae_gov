#!/usr/bin/env python3
"""
Phase 0A: Linguistic Foundation Training
========================================

Train WordOccasionTracker on linguistic ground truth corpus.
Learn POS tags, entity types, neighbor patterns from spaCy annotations.

🌀 Process Philosophy Alignment:
- Word occasions = actual occasions (experiencing subjects)
- Ground truth annotations = eternal objects (pure potentials)
- Learning = ingression of eternal objects into actual occasions

Author: DAE_HYPHAE_1 Team + Claude Code
Date: November 19, 2025
Status: Phase 0A - Pure Process Baseline
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from persona_layer.word_occasion_tracker import WordOccasionTracker


def load_corpus(corpus_path: str = "knowledge_base/linguistic_ground_truth_corpus.json"):
    """Load linguistic ground truth corpus."""
    with open(corpus_path, 'r') as f:
        return json.load(f)


def train_epoch(tracker: WordOccasionTracker, corpus: dict, epoch_num: int):
    """
    Train one epoch on the linguistic corpus.

    Args:
        tracker: WordOccasionTracker instance
        corpus: Loaded corpus dictionary
        epoch_num: Current epoch number
    """
    training_pairs = corpus['training_pairs']

    print(f"\n{'='*80}")
    print(f"🌀 EPOCH {epoch_num} - LINGUISTIC FOUNDATION TRAINING")
    print(f"{'='*80}\n")

    for i, pair in enumerate(training_pairs):
        ground_truth = pair['ground_truth']

        # Update tracker with ground truth annotations
        tracker.update_from_ground_truth(ground_truth)

        # Progress indicator
        if (i + 1) % 50 == 0:
            stats = tracker.get_statistics()
            print(f"   Pair {i+1}/{len(training_pairs)}: "
                  f"{stats['total_word_patterns']} word patterns learned")

    # Final stats for epoch
    stats = tracker.get_statistics()

    print(f"\n✅ EPOCH {epoch_num} COMPLETE")
    print(f"   Word patterns: {stats['total_word_patterns']}")
    print(f"   Words with sufficient mentions (≥3): {stats['words_with_sufficient_mentions']}")
    print(f"   Total updates: {stats['total_updates']}")

    return stats


def main(num_epochs: int = 10):
    """
    Run Phase 0A linguistic foundation training.

    Args:
        num_epochs: Number of training epochs
    """
    print("="*80)
    print("🧠 PHASE 0A: LINGUISTIC FOUNDATION TRAINING")
    print("="*80)
    print()

    # Load corpus
    print("📝 Loading linguistic ground truth corpus...")
    corpus = load_corpus()
    print(f"   ✅ Loaded {corpus['metadata']['total_sentences']} sentences")
    print(f"   Categories: {', '.join(corpus['metadata']['categories'])}")
    print()

    # Initialize tracker
    print("🌀 Initializing WordOccasionTracker...")
    tracker = WordOccasionTracker(
        storage_path="persona_layer/state/active/word_occasion_patterns_phase0a.json",
        ema_alpha=0.15,
        min_mentions_for_pattern=3
    )
    print("   ✅ Tracker initialized")

    # Training loop
    for epoch in range(1, num_epochs + 1):
        stats = train_epoch(tracker, corpus, epoch)

    # Final summary
    print("\n" + "="*80)
    print("✅ PHASE 0A TRAINING COMPLETE")
    print("="*80)

    final_stats = tracker.get_statistics()

    print(f"\n📊 FINAL STATISTICS:")
    print(f"   Total word patterns: {final_stats['total_word_patterns']}")
    print(f"   Words with ≥3 mentions: {final_stats['words_with_sufficient_mentions']}")
    print(f"   Total updates: {final_stats['total_updates']}")

    # Show top 10 learned words
    print(f"\n📈 TOP 10 LEARNED WORDS (by mention count):")
    sorted_patterns = sorted(
        tracker.word_patterns.items(),
        key=lambda x: x[1].mention_count,
        reverse=True
    )[:10]

    for word, pattern in sorted_patterns:
        # Get most common POS tag
        pos_dist = pattern.organ_activations.get('pos_distribution', {})
        most_common_pos = max(pos_dist.items(), key=lambda x: x[1])[0] if pos_dist else "UNKNOWN"

        # Get most common entity type if any
        entity_dist = pattern.entity_type_distribution
        most_common_entity = max(entity_dist.items(), key=lambda x: x[1])[0] if entity_dist else "None"

        print(f"   {word:15s} mentions={pattern.mention_count:3d}  "
              f"POS={most_common_pos:8s}  entity={most_common_entity}")

    print()
    print("🌀 Phase 0A linguistic foundation established!")
    print("   Next: Phase 0B - Entity-Memory Integration")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Phase 0A Linguistic Foundation Training")
    parser.add_argument("--epochs", type=int, default=10,
                        help="Number of training epochs (default: 10)")

    args = parser.parse_args()

    main(num_epochs=args.epochs)
