#!/usr/bin/env python3
"""
Quick diagnostic to test variance-weighted signature extraction.

This tests whether:
1. Variance computation is working
2. Signatures are genuinely different
3. Similarity calculations are correct
"""

import sys
import json
import numpy as np
from pathlib import Path

sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.organ_signature_extractor import OrganSignatureExtractor
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("="*80)
print("🔬 VARIANCE-WEIGHTED SIGNATURE DIAGNOSTIC")
print("="*80)
print()

# Initialize organism and extractor
print("📦 Initializing organism...")
organism = ConversationalOrganismWrapper()
extractor = OrganSignatureExtractor()

# Load a few training pairs
print("📂 Loading training pairs...")
with open("/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/conversational_training_pairs_v4_319.json") as f:
    data = json.load(f)
    pairs = data["training_pairs"][:5]  # Just 5 pairs for quick test

print(f"   ✅ Loaded {len(pairs)} test pairs")
print()

# Process each pair and extract signatures
signatures = []
variances_per_pair = []

for i, pair in enumerate(pairs):
    user_input = pair.get('input_text', '')

    # Process through organism
    result = organism.process_text(
        text=user_input,
        context={},
        enable_tsk_recording=False
    )

    organ_results = result.get('felt_states', {}).get('organ_results', {})

    if not organ_results:
        print(f"   ⚠️  Pair {i+1}: No organ results")
        continue

    # Extract variance-weighted signature
    composite = extractor.extract_composite_signature_variance_weighted(
        organ_results=organ_results,
        conversation_id=f"diagnostic_{i+1}",
        satisfaction_score=0.8,
        emission_text="test",
        user_message=user_input,
        timestamp="2025-11-12",
        variance_amplification=1.0
    )

    # Compute organ variances manually for diagnostic
    organ_variances = extractor._compute_organ_variances(organ_results)

    signatures.append(composite.signature)
    variances_per_pair.append(organ_variances)

    print(f"   Pair {i+1}: {user_input[:60]}...")
    print(f"      Signature mean: {np.mean(composite.signature):.4f}")
    print(f"      Signature std:  {np.std(composite.signature):.4f}")
    print(f"      Organ variances:")
    for organ, var in sorted(organ_variances.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"         {organ:15s} var={var:.4f}")
    print()

# Analyze signature similarity
print("="*80)
print("📊 SIGNATURE SIMILARITY ANALYSIS")
print("="*80)
print()

if len(signatures) >= 2:
    # Compute pairwise cosine similarities
    from sklearn.metrics.pairwise import cosine_similarity

    signatures_array = np.array(signatures)
    similarity_matrix = cosine_similarity(signatures_array)

    print("Pairwise Cosine Similarities:")
    print()
    for i in range(len(signatures)):
        for j in range(i+1, len(signatures)):
            sim = similarity_matrix[i, j]
            print(f"   Pair {i+1} vs Pair {j+1}: {sim:.4f}", end="")
            if sim > 0.75:
                print(" ← WOULD CLUSTER (threshold 0.75)")
            else:
                print(" ← WOULD NOT CLUSTER")
    print()

    # Overall statistics
    upper_triangle = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]
    print(f"Similarity Statistics:")
    print(f"   Mean: {np.mean(upper_triangle):.4f}")
    print(f"   Std:  {np.std(upper_triangle):.4f}")
    print(f"   Min:  {np.min(upper_triangle):.4f}")
    print(f"   Max:  {np.max(upper_triangle):.4f}")
    print()

    # Check if ALL similarities > 0.75 (uniform problem)
    if np.all(upper_triangle > 0.75):
        print("❌ PROBLEM: ALL signatures > 0.75 similarity (still uniform!)")
        print("   Variance weighting NOT working correctly")
    elif np.mean(upper_triangle) > 0.80:
        print("⚠️  WARNING: Mean similarity > 0.80 (still too uniform)")
        print("   May need stronger variance amplification")
    else:
        print("✅ GOOD: Signatures show healthy diversity")
        print("   Variance weighting appears to be working")
    print()

# Analyze variance distributions
print("="*80)
print("📈 VARIANCE DISTRIBUTION ANALYSIS")
print("="*80)
print()

# Aggregate variances across all pairs
all_variances = {}
for organ_vars in variances_per_pair:
    for organ, var in organ_vars.items():
        if organ not in all_variances:
            all_variances[organ] = []
        all_variances[organ].append(var)

print("Organ Variance Statistics (across all pairs):")
print()
for organ in sorted(all_variances.keys()):
    vars = all_variances[organ]
    print(f"   {organ:15s} mean={np.mean(vars):.4f} std={np.std(vars):.4f} range=[{np.min(vars):.4f}, {np.max(vars):.4f}]")

print()

# Check if ALL variances are near zero (computation bug)
mean_variances = [np.mean(vars) for vars in all_variances.values()]
if np.max(mean_variances) < 0.01:
    print("❌ CRITICAL: ALL organ variances near zero!")
    print("   Variance computation is broken")
elif np.max(mean_variances) < 0.05:
    print("⚠️  WARNING: Organ variances very low")
    print("   May not provide enough discrimination")
else:
    print("✅ Organ variances show healthy range")
    print(f"   Max mean variance: {np.max(mean_variances):.4f}")

print()
print("="*80)
print("🎯 DIAGNOSTIC COMPLETE")
print("="*80)
