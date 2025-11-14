#!/usr/bin/env python3
"""
Quick test of SANS embedding integration in Arc Training
Tests semantic similarity computation with real embeddings.
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

import json
from persona_layer.arc_inspired_trainer import ArcInspiredTrainer
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("="*80)
print("🧪 Testing SANS Embedding Integration in Arc Training")
print("="*80)
print()

# Load training pairs
print("📂 Loading training pairs...")
with open('knowledge_base/conversational_training_pairs.json', 'r') as f:
    training_data = json.load(f)
    training_pairs = training_data['training_pairs']

print(f"✅ Loaded {len(training_pairs)} pairs")
print()

# Initialize organism
print("🌀 Initializing organism...")
organism = ConversationalOrganismWrapper()
print()

# Initialize trainer with SANS embeddings
print("🔧 Initializing Arc trainer with SANS embeddings...")
trainer = ArcInspiredTrainer(
    organism_wrapper=organism,
    training_pairs=training_pairs,
    enable_learning=False,  # Don't learn during test
    assessment_threshold=0.65
)
print()

# Test semantic similarity with sample responses
print("="*80)
print("📊 Testing Semantic Similarity Computation")
print("="*80)
print()

test_cases = [
    {
        "prediction": "I'm listening.",
        "target": "I hear what you're saying and I'm here with you.",
        "expected_range": "moderate (0.4-0.6)"
    },
    {
        "prediction": "Here",
        "target": "Being made the container for a system's shadow is a profound burden.",
        "expected_range": "low (0.0-0.3)"
    },
    {
        "prediction": "I'm with you I'm listening.",
        "target": "It sounds like you're finding your voice in a space that feels safe enough to be authentic.",
        "expected_range": "low-moderate (0.2-0.4)"
    },
    {
        "prediction": "I hear you struggling with burnout and exhaustion.",
        "target": "Burnout is a systemic issue, not a personal failing. Your exhaustion is real.",
        "expected_range": "high (0.6-0.8)"
    }
]

if trainer.use_embeddings:
    print("✅ SANS embeddings ACTIVE")
    print()

    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}:")
        print(f"   Prediction: \"{test['prediction']}\"")
        print(f"   Target: \"{test['target']}\"")
        print(f"   Expected: {test['expected_range']}")

        # Compute similarity
        pred_embedding = trainer.embedder.encode(test['prediction'], convert_to_numpy=True)
        target_embedding = trainer.embedder.encode(test['target'], convert_to_numpy=True)

        import numpy as np
        pred_norm = pred_embedding / np.linalg.norm(pred_embedding)
        target_norm = target_embedding / np.linalg.norm(target_embedding)

        cosine_sim = float(np.dot(pred_norm, target_norm))
        semantic_sim = (cosine_sim + 1.0) / 2.0

        print(f"   ✅ Semantic similarity: {semantic_sim:.3f}")
        print()
else:
    print("⚠️  SANS embeddings NOT available (fallback mode)")
    print("   Similarity will be length-based")
    print()

print("="*80)
print("✅ Test Complete")
print("="*80)
print()

# Compare to epochs 11-13 results
print("📈 Comparison to Previous Results:")
print()
print("Epochs 11-13 (Length-based):")
print("   Mean semantic similarity: 0.11")
print("   Success rate: 0/150 (0%)")
print()
print("Expected with SANS Embeddings:")
print("   Mean semantic similarity: 0.35-0.45 (3-4× improvement)")
print("   Success rate: 10-20% (predicted)")
print()
