#!/usr/bin/env python3
"""
LLM Activation Diversity Analysis
==================================

Analyze the 83 cached LLM activations to determine if they provide
sufficient diversity to enable multi-family differentiation.

Compares:
- Variance across organs
- Variance across zones
- Cosine similarity between pairs
- Expected family count based on clustering

Date: November 13, 2025
"""

import json
import numpy as np
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity

print("=" * 80)
print("📊 LLM ACTIVATION DIVERSITY ANALYSIS")
print("=" * 80)
print()

# Load cache
CACHE_PATH = "persona_layer/llm_activation_cache_local.json"
TRAINING_PAIRS_PATH = "knowledge_base/zones_1_4_training_pairs.json"

print("Loading data...")
with open(CACHE_PATH) as f:
    cache = json.load(f)

with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"]

# Create pair_id → zone mapping
pair_zones = {p["pair_metadata"]["id"]: p["pair_metadata"]["zone"]
              for p in training_pairs}

print(f"✅ Loaded {len(cache)} cached activations")
print()

# Convert to numpy array
organs = ["LISTENING", "EMPATHY", "WISDOM", "AUTHENTICITY", "PRESENCE",
          "BOND", "SANS", "NDAM", "RNX", "EO", "CARD"]

# Build activation matrix: (83 pairs, 11 organs)
activation_matrix = []
pair_ids = []
zones = []

for pair_id, acts in cache.items():
    if pair_id in pair_zones:
        vector = [acts.get(organ, 0.0) for organ in organs]
        activation_matrix.append(vector)
        pair_ids.append(pair_id)
        zones.append(pair_zones[pair_id])

X = np.array(activation_matrix)
print(f"Activation matrix: {X.shape} (83 pairs × 11 organs)")
print()

# 1. Overall statistics
print("1️⃣  Overall Statistics")
print("=" * 80)
print(f"   Mean activation: {X.mean():.3f}")
print(f"   Std activation: {X.std():.3f}")
print(f"   Min activation: {X.min():.3f}")
print(f"   Max activation: {X.max():.3f}")
print()

# Count extreme values
extreme_1 = (X == 1.0).sum()
extreme_0 = (X == 0.0).sum()
moderate = ((X > 0.0) & (X < 1.0)).sum()
total = X.size

print(f"   Extreme 1.0: {extreme_1}/{total} ({extreme_1/total*100:.1f}%)")
print(f"   Extreme 0.0: {extreme_0}/{total} ({extreme_0/total*100:.1f}%)")
print(f"   Moderate (0<x<1): {moderate}/{total} ({moderate/total*100:.1f}%)")
print()

# 2. Per-organ variance
print("2️⃣  Per-Organ Variance")
print("=" * 80)
organ_variances = []
for i, organ in enumerate(organs):
    variance = X[:, i].var()
    organ_variances.append((organ, variance))
    print(f"   {organ:15s}: variance={variance:.4f}")

avg_variance = np.mean([v for _, v in organ_variances])
print(f"\n   Average variance: {avg_variance:.4f}")
print()

# 3. Per-zone statistics
print("3️⃣  Per-Zone Statistics")
print("=" * 80)
zone_data = defaultdict(list)
for i, zone in enumerate(zones):
    zone_data[zone].append(X[i])

for zone in sorted(zone_data.keys()):
    zone_matrix = np.array(zone_data[zone])
    print(f"   Zone {zone}:")
    print(f"      Count: {len(zone_matrix)}")
    print(f"      Mean: {zone_matrix.mean():.3f}")
    print(f"      Std: {zone_matrix.std():.3f}")

print()

# 4. Pairwise cosine similarity
print("4️⃣  Pairwise Cosine Similarity")
print("=" * 80)

cos_sim = cosine_similarity(X)
np.fill_diagonal(cos_sim, np.nan)  # Ignore self-similarity

mean_sim = np.nanmean(cos_sim)
min_sim = np.nanmin(cos_sim)
max_sim = np.nanmax(cos_sim)

print(f"   Mean similarity: {mean_sim:.4f}")
print(f"   Min similarity: {min_sim:.4f}")
print(f"   Max similarity: {max_sim:.4f}")
print()

# Distribution of similarities
bins = [0.0, 0.5, 0.65, 0.8, 0.9, 0.95, 1.0]
hist, _ = np.histogram(cos_sim[~np.isnan(cos_sim)], bins=bins)
print("   Similarity distribution:")
for i in range(len(bins)-1):
    print(f"      [{bins[i]:.2f}, {bins[i+1]:.2f}): {hist[i]} pairs ({hist[i]/(83*82)*100:.1f}%)")
print()

# 5. Expected family count (clustering simulation)
print("5️⃣  Expected Family Count (Clustering Simulation)")
print("=" * 80)

# Simulate family formation using cosine similarity threshold=0.65
SIMILARITY_THRESHOLD = 0.65
families = []
assigned = set()

for i in range(len(X)):
    if i in assigned:
        continue

    # Start new family with pair i
    family = {i}
    assigned.add(i)

    # Find similar pairs
    for j in range(len(X)):
        if j in assigned:
            continue

        # Check if j is similar to any family member
        if any(cos_sim[j, member] >= SIMILARITY_THRESHOLD for member in family):
            family.add(j)
            assigned.add(j)

    families.append(family)

print(f"   Similarity threshold: {SIMILARITY_THRESHOLD}")
print(f"   Expected families: {len(families)}")
print()

# Show family sizes and zones
for fam_idx, family in enumerate(sorted(families, key=len, reverse=True), 1):
    fam_zones = [zones[i] for i in family]
    zone_counts = {}
    for z in fam_zones:
        zone_counts[z] = zone_counts.get(z, 0) + 1
    print(f"   Family {fam_idx}: {len(family)} members")
    print(f"      Zones: {dict(sorted(zone_counts.items()))}")

print()

# 6. Verdict
print("=" * 80)
print("📊 VERDICT")
print("=" * 80)
print()

if len(families) > 1:
    print(f"✅ DIVERSITY DETECTED: {len(families)} families expected")
    print(f"   Baseline: 1 family (keyword-based)")
    print(f"   LLM-augmented: {len(families)} families")
    print()
    print(f"   Mean variance: {avg_variance:.4f} (>0 indicates differentiation)")
    print(f"   Mean similarity: {mean_sim:.4f} (<1.0 indicates diversity)")
    print()
    print("   ✅ LLM activations provide sufficient diversity for multi-family formation!")
else:
    print(f"⚠️  LIMITED DIVERSITY: Only {len(families)} family expected")
    print(f"   Mean variance: {avg_variance:.4f}")
    print(f"   Mean similarity: {mean_sim:.4f}")
    print()
    print("   Possible causes:")
    print(f"   - Too many extreme values (1.0: {extreme_1/total*100:.1f}%, 0.0: {extreme_0/total*100:.1f}%)")
    print(f"   - LLM prompt may need refinement")
    print(f"   - Need full 240 activations for better coverage")

print("=" * 80)
