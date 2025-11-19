"""
Phase 0B Entity-Word Integration Training
==========================================

Unified training script that combines:
- Phase 0A: Word pattern learning (WordOccasionTracker)
- Phase 0B: Word-entity co-learning (WordEntityBridge)
- Entity memory: Entity-organ associations (EntityOrganTracker)

This creates bidirectional word-entity learning where:
- Words learn which entities they appear near
- Entities learn which words typically surround them
- Co-learning emerges through shared context

Expected trajectory:
- Epoch 1: Baseline (word patterns only, 0 entity co-occurrences)
- Epoch 5: Early co-learning (~200 co-occurrence patterns)
- Epoch 10: Pattern emergence (~450 co-occurrence patterns)
- Epoch 20: Stable integration (~750 co-occurrence patterns)

Date: November 19, 2025
Status: Phase 0B Implementation
"""

import sys
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.word_occasion_tracker import WordOccasionTracker
from persona_layer.word_entity_bridge import WordEntityBridge
from persona_layer.entity_organ_tracker import EntityOrganTracker


def tokenize_and_create_occasions(text: str, user_id: str) -> List[Any]:
    """
    Tokenize text and create WordOccasion objects.

    Simple whitespace tokenization for Phase 0B.
    """
    # Import WordOccasion from transductive module
    sys.path.append(str(Path(__file__).parent.parent))
    from transductive.word_occasion import WordOccasion

    tokens = text.split()
    occasions = []

    for position, token in enumerate(tokens):
        # WordOccasion expects: word, position, sentence (mandatory)
        occasion = WordOccasion(
            word=token,
            position=position,
            sentence=text
        )
        occasions.append(occasion)

    return occasions


def extract_entities_simple(text: str) -> List[Dict[str, Any]]:
    """
    Simple entity extraction for Phase 0B training.

    Extracts capitalized words as Person entities.
    This is a placeholder - would use LLM or pattern-based extraction in production.
    """
    tokens = text.split()
    entities = []

    for position, token in enumerate(tokens):
        # Simple heuristic: capitalized words that aren't sentence starters
        if token[0].isupper() and position > 0:
            entities.append({
                'entity_value': token.strip(',.!?'),
                'entity_type': 'Person',
                'position': position,
                'start_idx': position,
                'end_idx': position
            })

    return entities


def run_phase0b_training(
    num_epochs: int = 1,
    training_pairs_path: str = "knowledge_base/entity_memory_training_pairs.json",
    verbose: bool = True
):
    """
    Run Phase 0B entity-word integration training.

    Args:
        num_epochs: Number of training epochs
        training_pairs_path: Path to training pairs JSON
        verbose: Print progress
    """

    print("=" * 70)
    print("PHASE 0B: ENTITY-WORD INTEGRATION TRAINING")
    print("=" * 70)
    print(f"Epochs: {num_epochs}")
    print(f"Training pairs: {training_pairs_path}")
    print()

    # Load training pairs
    with open(training_pairs_path, 'r') as f:
        data = json.load(f)

    training_pairs = data.get('training_pairs', [])

    print(f"✅ Loaded {len(training_pairs)} training pairs")
    print()

    # Initialize components
    print("Initializing Phase 0B components...")

    # Phase 0A: Word patterns
    word_tracker = WordOccasionTracker(
        storage_path="persona_layer/state/active/word_occasion_patterns_phase0b.json",
        ema_alpha=0.15
    )

    # Phase 0B: Word-entity bridge
    word_entity_bridge = WordEntityBridge(
        storage_path="persona_layer/state/active/word_entity_cooccurrence.json",
        ema_alpha=0.15,
        context_window=3,
        min_cooccurrences=3
    )

    # Entity memory: Entity-organ tracker (clear old state for Phase 0B)
    entity_assoc_path = Path("persona_layer/state/active/entity_organ_associations.json")
    if entity_assoc_path.exists():
        # Backup old state
        import shutil
        backup_path = entity_assoc_path.parent / "entity_organ_associations_backup.json"
        shutil.copy(entity_assoc_path, backup_path)
        print(f"   Backed up old entity associations to {backup_path}")
        entity_assoc_path.unlink()  # Remove old file

    entity_tracker = EntityOrganTracker(
        storage_path="persona_layer/state/active/entity_organ_associations.json",
        ema_alpha=0.15
    )

    # Organism wrapper (for organ results) - no user_id parameter
    wrapper = ConversationalOrganismWrapper()

    print("✅ All components initialized")
    print()

    # Training loop
    for epoch in range(1, num_epochs + 1):
        print(f"{'='*70}")
        print(f"EPOCH {epoch}/{num_epochs}")
        print(f"{'='*70}")

        epoch_start = time.time()

        for idx, pair in enumerate(training_pairs, 1):
            if verbose and idx % 10 == 0:
                print(f"  Processing pair {idx}/{len(training_pairs)}...")

            user_input = pair['input']
            user_id = pair.get('user_id', 'user_20251117_160809')

            # 1. Extract entities
            entities = extract_entities_simple(user_input)

            # 2. Create word occasions
            word_occasions = tokenize_and_create_occasions(user_input, user_id)

            # 3. Process through organism (get organ results)
            try:
                result = wrapper.process_text(user_input, user_id=user_id)
                organ_results = result.get('felt_states', {})
            except Exception as e:
                if verbose:
                    print(f"⚠️  Organism processing failed for pair {idx}: {e}")
                organ_results = {}

            # 4. Update word patterns (Phase 0A)
            # Note: WordOccasionTracker.update() only needs word_occasions
            # Organ activations are embedded in word_occasions via actualization_vector
            word_tracker.update(word_occasions)

            # 5. Update word-entity co-occurrence (Phase 0B)
            word_entity_bridge.update_word_entity_cooccurrence(
                word_occasions=word_occasions,
                entities=entities,
                organ_results=organ_results
            )

            # 6. Update entity patterns (with word occasions for Phase 0B)
            if entities:
                felt_state = {
                    'polyvagal_state': 'mixed',
                    'v0_energy': result.get('v0_energy', 0.5) if result else 0.5,
                    'urgency': 0.0,
                    'self_distance': 0.0
                }

                entity_tracker.update(
                    extracted_entities=entities,
                    organ_results=organ_results,
                    felt_state=felt_state,
                    word_occasions=word_occasions  # Phase 0B parameter
                )

        # Save after each epoch
        # word_tracker saves automatically on update()
        word_entity_bridge.save_patterns()
        entity_tracker._save()

        epoch_time = time.time() - epoch_start

        # Epoch summary
        print()
        print(f"EPOCH {epoch} COMPLETE")
        print(f"  Time: {epoch_time:.2f}s")

        bridge_summary = word_entity_bridge.get_pattern_summary()
        print(f"  Word-entity patterns: {bridge_summary['total_patterns']}")
        print(f"  Active patterns: {bridge_summary['active_patterns']}")
        print(f"  Total co-occurrences: {bridge_summary['total_cooccurrences']}")

        entity_summary = entity_tracker.get_summary()
        print(f"  Tracked entities: {entity_summary.get('total_entities', 0)}")
        print(f"  Entities with patterns: {entity_summary.get('entities_with_patterns', 0)}")
        print()

    # Final summary
    print("=" * 70)
    print("PHASE 0B TRAINING COMPLETE")
    print("=" * 70)
    print()
    print("Final Metrics:")
    print(f"  Word patterns learned: {len(word_tracker.patterns)}")
    print(f"  Word-entity co-occurrence patterns: {bridge_summary['total_patterns']}")
    print(f"  Active co-occurrence patterns (≥3 mentions): {bridge_summary['active_patterns']}")
    print(f"  Total co-occurrences recorded: {bridge_summary['total_cooccurrences']}")
    print(f"  Entities tracked: {entity_summary.get('total_entities', 0)}")
    print()

    # Show top word-entity patterns
    print("Top 10 Word-Entity Patterns:")
    print("-" * 70)

    sorted_patterns = sorted(
        word_entity_bridge.patterns.items(),
        key=lambda x: x[1].total_entity_cooccurrences,
        reverse=True
    )[:10]

    for word, pattern in sorted_patterns:
        print(f"  '{word}': {pattern.total_entity_cooccurrences} co-occurrences")
        for entity_value, stats in list(pattern.entity_neighbors.items())[:3]:
            print(f"    - {entity_value} ({stats.count}x)")

    print()
    print("✅ Phase 0B training data saved:")
    print(f"   - Word patterns: {word_tracker.storage_path}")
    print(f"   - Word-entity bridge: {word_entity_bridge.storage_path}")
    print(f"   - Entity tracker: {entity_tracker.storage_path}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 0B Entity-Word Integration Training")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs")
    parser.add_argument("--training-pairs", type=str,
                       default="knowledge_base/entity_memory_training_pairs.json",
                       help="Path to training pairs JSON")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    run_phase0b_training(
        num_epochs=args.epochs,
        training_pairs_path=args.training_pairs,
        verbose=args.verbose
    )
