"""
Debug Pattern Extraction - Why 0 Entities Found?
=================================================

Test pattern-based entity extraction with sample training data.

Date: November 19, 2025
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent))

from persona_layer.entity_neighbor_prehension.entity_neighbor_prehension import EntityNeighborPrehension
from transductive.word_occasion import create_word_occasions_from_text

def test_pattern_extraction():
    """Test pattern extraction with actual training pair text."""
    print("\n" + "="*80)
    print("🔍 PATTERN EXTRACTION DEBUG TEST")
    print("="*80)

    # Initialize extractor
    extractor = EntityNeighborPrehension()

    # Sample test cases from actual training data
    test_cases = [
        "Do you remember my daughter Emma's name?",
        "What do you know about my daughter?",
        "Today Emma went to work",
        "I'm worried about my daughter Emma",
        "She went to the hospital yesterday"
    ]

    for i, test_text in enumerate(test_cases, 1):
        print(f"\n📋 TEST {i}: \"{test_text}\"")
        print(f"   {'='*70}")

        # Create WordOccasions
        word_occasions = create_word_occasions_from_text(test_text, neighbor_window_size=5)
        print(f"   Created {len(word_occasions)} WordOccasions")

        # Test pattern extraction on each word
        entities_found = []
        for word_occ in word_occasions:
            # Call pattern extraction directly
            entity_type, confidence = extractor._simple_pattern_extraction(word_occ)

            print(f"      [{word_occ.position}] '{word_occ.word}' ", end="")
            print(f"(left={word_occ.left_neighbors[-2:] if word_occ.left_neighbors else []}, ", end="")
            print(f"right={word_occ.right_neighbors[:2] if word_occ.right_neighbors else []})", end="")

            if entity_type and confidence >= 0.55:
                print(f" → {entity_type} ({confidence:.2f}) ✅")
                entities_found.append({
                    'word': word_occ.word,
                    'type': entity_type,
                    'confidence': confidence
                })
            else:
                print(f" → None")

        # Now test full extraction pipeline
        print(f"\n   Full extraction pipeline:")
        extracted_entities, _ = extractor.extract_entities(
            test_text,
            neighbor_window_size=5,
            return_word_occasions=True
        )
        print(f"      Entities extracted: {len(extracted_entities)}")
        for entity in extracted_entities:
            print(f"         - {entity['entity_value']} ({entity['entity_type']}, conf={entity['confidence_score']:.2f})")

        print(f"\n   ✅ Pattern extraction found: {len(entities_found)} entities")
        print(f"   ✅ Full pipeline returned: {len(extracted_entities)} entities")

        if len(entities_found) != len(extracted_entities):
            print(f"   ⚠️  MISMATCH: Pattern found {len(entities_found)} but pipeline returned {len(extracted_entities)}")

    print("\n" + "="*80)
    print("🔍 PATTERN EXTRACTION DEBUG COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_pattern_extraction()
