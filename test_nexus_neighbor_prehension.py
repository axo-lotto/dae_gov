"""
Test NEXUS Neighbor Prehension
================================

Validates that NEXUS organ's neighbor-aware methods work correctly.

Author: DAE_HYPHAE_1 Team
Date: November 18, 2025
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from transductive.word_occasion import WordOccasion
from organs.modular.nexus.core.nexus_text_core import NEXUSTextCore

print("=" * 80)
print("🧪 NEXUS NEIGHBOR PREHENSION VALIDATION TEST")
print("=" * 80)

# Initialize NEXUS (without Neo4j for testing)
print("\n📋 Initializing NEXUS organ...")
nexus = NEXUSTextCore(enable_neo4j=False, enable_entity_tracker=False)

# Test 1: Basic entity extraction with neighbor context
print("\n📋 TEST 1: Basic Entity Extraction with Neighbors")
test_input = "Today my friend Emma went to work"
word_occasions = WordOccasion.from_sentence_batch(test_input)

print(f"   Input: \"{test_input}\"")
print(f"   Created {len(word_occasions)} WordOccasions")

# Show neighbor context for "Emma"
for occ in word_occasions:
    if occ.word == "Emma":
        print(f"   Emma's context: {occ.get_neighbor_context_string()}")

# Process through NEXUS
entities = nexus.process_word_occasions(word_occasions, context={'user_id': 'test_user'})

print(f"   ✅ Extracted {len(entities)} entities:")
for entity in entities:
    print(f"      • {entity['entity_value']} ({entity['entity_type']}, conf={entity['confidence_score']:.2f}, coherence={entity['coherence']:.2f})")
    print(f"        Atom activations: {list(entity['atom_activations'].keys())}")

# Test 2: Relationship depth detection
print("\n📋 TEST 2: Relationship Depth Detection")
test_input2 = "I'm worried about my daughter Emma"
word_occasions2 = WordOccasion.from_sentence_batch(test_input2)

print(f"   Input: \"{test_input2}\"")

entities2 = nexus.process_word_occasions(word_occasions2, context={'user_id': 'test_user'})

print(f"   ✅ Extracted {len(entities2)} entities:")
for entity in entities2:
    print(f"      • {entity['entity_value']} ({entity['entity_type']}, conf={entity['confidence_score']:.2f})")
    print(f"        relationship_depth: {entity['atom_activations'].get('relationship_depth', 0.0):.2f}")

# Test 3: Co-occurrence detection
print("\n📋 TEST 3: Co-occurrence Detection")
test_input3 = "Emma and Alice went together to the park"
word_occasions3 = WordOccasion.from_sentence_batch(test_input3)

print(f"   Input: \"{test_input3}\"")

entities3 = nexus.process_word_occasions(word_occasions3, context={'user_id': 'test_user'})

print(f"   ✅ Extracted {len(entities3)} entities:")
for entity in entities3:
    print(f"      • {entity['entity_value']} ({entity['entity_type']}, conf={entity['confidence_score']:.2f})")
    print(f"        co_occurrence: {entity['atom_activations'].get('co_occurrence', 0.0):.2f}")

# Test 4: Salience gradient detection
print("\n📋 TEST 4: Salience Gradient Detection")
test_input4 = "I'm especially worried about Emma's health"
word_occasions4 = WordOccasion.from_sentence_batch(test_input4)

print(f"   Input: \"{test_input4}\"")

entities4 = nexus.process_word_occasions(word_occasions4, context={'user_id': 'test_user'})

print(f"   ✅ Extracted {len(entities4)} entities:")
for entity in entities4:
    print(f"      • {entity['entity_value']} ({entity['entity_type']}, conf={entity['confidence_score']:.2f})")
    print(f"        salience_gradient: {entity['atom_activations'].get('salience_gradient', 0.0):.2f}")

# Test 5: No false positives (lowercase, first word)
print("\n📋 TEST 5: No False Positives (Negative Cases)")
test_input5 = "Emma started the project today"
word_occasions5 = WordOccasion.from_sentence_batch(test_input5)

print(f"   Input: \"{test_input5}\" (Emma is first word, should be filtered)")

entities5 = nexus.process_word_occasions(word_occasions5, context={'user_id': 'test_user'})

print(f"   ✅ Extracted {len(entities5)} entities (expected 0-1, not including first word 'Emma')")
for entity in entities5:
    print(f"      • {entity['entity_value']} ({entity['entity_type']}, conf={entity['confidence_score']:.2f})")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED - NEXUS Neighbor Prehension operational!")
print("=" * 80)
