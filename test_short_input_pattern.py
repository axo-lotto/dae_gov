"""
Test Pattern Extraction on Short Inputs
========================================

Test why "Where do I work?" finds 0-1 entities.

Date: November 19, 2025
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from persona_layer.entity_neighbor_prehension.entity_neighbor_prehension import EntityNeighborPrehension
from transductive.word_occasion import create_word_occasions_from_text

# Test the exact training pair inputs
test_inputs = [
    "Where do I work?",
    "Do you remember my daughter Emma's name?",
    "What do you know about my daughter?",
    "Who is Emma?"
]

extractor = EntityNeighborPrehension()

for text in test_inputs:
    print(f"\n{'='*70}")
    print(f"Input: \"{text}\"")
    print(f"{'='*70}")

    # Extract with pattern
    entities, word_occasions = extractor.extract_entities(text, return_word_occasions=True)

    print(f"Words: {[wo.word for wo in word_occasions]}")
    print(f"Entities found: {len(entities)}")

    for ent in entities:
        print(f"   - {ent['entity_value']} ({ent['entity_type']}, conf={ent['confidence_score']:.2f})")

    if len(entities) == 0:
        print("   (No entities found)")

        # Show why each word failed
        for wo in word_occasions:
            entity_type, conf = extractor._simple_pattern_extraction(wo)
            if entity_type and conf >= 0.55:
                print(f"   ⚠️  Word '{wo.word}' matched {entity_type} ({conf:.2f}) but didn't pass!")
