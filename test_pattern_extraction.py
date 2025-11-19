"""
Test Pattern-Based Entity Extraction (Fix #2)

Tests the new _simple_pattern_extraction() method to validate:
- Capitalized person names
- Location words
- Family words with possessives
- Profession words with possessives
"""

import sys
import os

# Set PYTHONPATH
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.entity_neighbor_prehension.entity_neighbor_prehension import EntityNeighborPrehension

def test_pattern_extraction():
    """Test pattern-based entity extraction with diverse inputs."""

    # Initialize entity prehension
    prehension = EntityNeighborPrehension()

    # Test cases covering all 4 patterns + ~40 entity types
    test_inputs = [
        # Pattern 1: Capitalized person names
        "I saw Emma at the store yesterday",
        "John helped me with my homework",

        # Pattern 2: Location words
        "I went to the hospital for my checkup",
        "She works at the office downtown",
        "We met at the park near school",

        # Pattern 3: Family words with possessives
        "My daughter is starting kindergarten",
        "His father is a retired teacher",
        "Our grandmother lives nearby",

        # Pattern 4: Profession words with possessives
        "My therapist suggested meditation",
        "Her doctor recommended rest",
        "Our manager approved the request",

        # Mixed entities (multiple patterns)
        "I took my son to the hospital to see my doctor",
        "Emma and I visited our friend at work",

        # No entities (should find 0)
        "I feel anxious about tomorrow",
        "The weather is nice today",
    ]

    print("\n" + "="*80)
    print("🔍 TESTING PATTERN-BASED ENTITY EXTRACTION (Fix #2)")
    print("="*80 + "\n")

    total_inputs = len(test_inputs)
    total_entities = 0

    for i, input_text in enumerate(test_inputs, 1):
        print(f"\n{'─'*80}")
        print(f"Test {i}/{total_inputs}: \"{input_text}\"")
        print(f"{'─'*80}")

        # Extract entities
        entities, word_occasions = prehension.extract_entities(
            input_text,
            return_word_occasions=True
        )

        # Report results
        if entities:
            print(f"✅ Found {len(entities)} entities:")
            for entity in entities:
                entity_value = entity.get('entity_value', 'Unknown')
                entity_type = entity.get('entity_type', 'Unknown')
                confidence = entity.get('confidence_score', 0.0)
                print(f"   - {entity_value:20s} → {entity_type:10s} (confidence: {confidence:.2f})")
            total_entities += len(entities)
        else:
            print("❌ No entities found")

        # Show word occasions stats
        print(f"\n   📊 Word occasions: {len(word_occasions)} words processed")

    print("\n" + "="*80)
    print(f"✅ EXTRACTION COMPLETE")
    print("="*80)
    print(f"Total inputs:    {total_inputs}")
    print(f"Total entities:  {total_entities}")
    print(f"Avg per input:   {total_entities / total_inputs:.1f}")
    print(f"\nExpected range:  15-30 entities (covers ~40 patterns)")

    if total_entities >= 15:
        print("✅ SUCCESS: Pattern extraction working as expected!")
    else:
        print("⚠️  WARNING: Lower than expected entity extraction")

    print("\n")

if __name__ == "__main__":
    test_pattern_extraction()
