#!/usr/bin/env python3
"""
Family Clustering Diagnostic Tool
==================================

Analyzes why Phase 5 family clustering isn't differentiating.

Investigation:
1. Load existing Family_001 centroid
2. Simulate diverse organ signatures (EMPATHY-heavy vs WISDOM-heavy vs BOND-heavy)
3. Compute cosine similarities to Family_001
4. Test if threshold=0.55 would enable differentiation

Hypothesis:
- Family_001 centroid is too uniform (all dimensions ~0.13)
- Averaging across all organs creates "generic" pattern
- Need more discriminative signature extraction

Date: November 12, 2025
"""

import json
import numpy as np
from pathlib import Path

print("="*80)
print("🔬 FAMILY CLUSTERING DIAGNOSTIC")
print("="*80)
print()

# Load existing family
family_path = Path("persona_layer/organic_families.json")

if not family_path.exists():
    print("❌ No organic_families.json found!")
    exit(1)

with open(family_path) as f:
    data = json.load(f)

family_001 = data['families']['Family_001']
centroid = np.array(family_001['centroid'])

print("📊 Family_001 Centroid Analysis:")
print(f"   Shape: {centroid.shape}")
print(f"   L2 norm: {np.linalg.norm(centroid):.6f} (should be 1.0)")
print(f"   Mean: {np.mean(centroid):.6f}")
print(f"   Std: {np.std(centroid):.6f}")
print(f"   Min: {np.min(centroid):.6f}")
print(f"   Max: {np.max(centroid):.6f}")
print()

# Check if centroid is uniform
is_uniform = np.std(centroid) < 0.05
if is_uniform:
    print("⚠️  CENTROID IS NEARLY UNIFORM!")
    print("   This creates a 'generic' pattern that matches everything")
    print()

# Show organ activation breakdown
print("📈 Family_001 Organ Activations:")
for organ, activation in family_001['organ_activation_means'].items():
    print(f"   {organ:15s} {activation:.3f}")
print()

# Simulate diverse signatures
print("🧪 SIMULATING DIVERSE ORGAN SIGNATURES:")
print()

# Determine actual dimensionality from centroid
ndims = centroid.shape[0]
print(f"   Using {ndims}D signatures (detected from centroid)")
print()

# Test Case 1: EMPATHY-heavy signature
empathy_sig = np.ones(ndims) * 0.3  # Low baseline
empathy_sig[6:13] = 0.9  # High EMPATHY dims
empathy_sig = empathy_sig / np.linalg.norm(empathy_sig)

empathy_similarity = np.dot(empathy_sig, centroid)
print(f"1. EMPATHY-HEAVY (dims 6-13 @ 0.9):")
print(f"   Similarity to Family_001: {empathy_similarity:.4f}")
print(f"   Would join family? {empathy_similarity >= 0.85} (threshold=0.85)")
print(f"   Would join family? {empathy_similarity >= 0.55} (threshold=0.55)")
print()

# Test Case 2: WISDOM-heavy signature
wisdom_sig = np.ones(ndims) * 0.3
wisdom_sig[13:20] = 0.9  # High WISDOM dims
wisdom_sig = wisdom_sig / np.linalg.norm(wisdom_sig)

wisdom_similarity = np.dot(wisdom_sig, centroid)
print(f"2. WISDOM-HEAVY (dims 13-20 @ 0.9):")
print(f"   Similarity to Family_001: {wisdom_similarity:.4f}")
print(f"   Would join family? {wisdom_similarity >= 0.85} (threshold=0.85)")
print(f"   Would join family? {wisdom_similarity >= 0.55} (threshold=0.55)")
print()

# Test Case 3: BOND-heavy (trauma) signature
bond_sig = np.ones(ndims) * 0.3
bond_sig[32:37] = 0.9  # High BOND dims
bond_sig = bond_sig / np.linalg.norm(bond_sig)

bond_similarity = np.dot(bond_sig, centroid)
print(f"3. BOND-HEAVY (dims 32-37 @ 0.9):")
print(f"   Similarity to Family_001: {bond_similarity:.4f}")
print(f"   Would join family? {bond_similarity >= 0.85} (threshold=0.85)")
print(f"   Would join family? {bond_similarity >= 0.55} (threshold=0.55)")
print()

# Test Case 4: Compute similarity between diverse signatures
empathy_wisdom_similarity = np.dot(empathy_sig, wisdom_sig)
empathy_bond_similarity = np.dot(empathy_sig, bond_sig)
wisdom_bond_similarity = np.dot(wisdom_sig, bond_sig)

print("🔀 SIMILARITY BETWEEN DIVERSE SIGNATURES:")
print(f"   EMPATHY ↔ WISDOM: {empathy_wisdom_similarity:.4f}")
print(f"   EMPATHY ↔ BOND:   {empathy_bond_similarity:.4f}")
print(f"   WISDOM ↔ BOND:    {wisdom_bond_similarity:.4f}")
print()

# Analysis
print("="*80)
print("🔍 DIAGNOSTIC FINDINGS")
print("="*80)
print()

if empathy_similarity >= 0.55 and wisdom_similarity >= 0.55 and bond_similarity >= 0.55:
    print("❌ PROBLEM CONFIRMED: Uniform centroid matches all signatures!")
    print()
    print("   Root Cause:")
    print("   - Family_001 centroid is nearly uniform (std={:.4f})".format(np.std(centroid)))
    print("   - Averaging across 30 conversations smoothed out discrimination")
    print("   - ALL organ patterns look similar to uniform centroid")
    print()
    print("   Why threshold reduction FAILED:")
    print("   - Even diverse signatures (EMPATHY vs WISDOM vs BOND) score ≥0.55")
    print("   - Lowering threshold doesn't help if centroid is too generic")
    print()
    print("   Solutions:")
    print("   1. Reset families and use more discriminative signatures")
    print("   2. Use L1-normalized or raw signatures (not L2-normalized)")
    print("   3. Weight organs differently during signature extraction")
    print("   4. Use cosine distance instead of similarity for clustering")
    print("   5. Initialize with pre-seeded diverse centroids")
    print()

elif empathy_similarity < 0.55 or wisdom_similarity < 0.55 or bond_similarity < 0.55:
    print("✅ CENTROID IS DISCRIMINATIVE - Threshold reduction should work!")
    print()
    print(f"   EMPATHY similarity: {empathy_similarity:.4f}")
    print(f"   WISDOM similarity: {wisdom_similarity:.4f}")
    print(f"   BOND similarity: {bond_similarity:.4f}")
    print()
    print("   At threshold=0.55, some signatures would form new families")
    print("   Recommendation: Continue with more epochs or check signature extraction")
    print()

# Check actual training data distribution
print("📋 TRAINING DATA CONTEXT:")
print(f"   Total conversations learned: {len(family_001['member_conversations'])}")
print(f"   Domains: workplace_trauma (only from epochs 6-20)")
print(f"   New domains added (epochs 21-26): grief, crisis")
print()
print("   Hypothesis: All 30 conversations are similar domain (workplace trauma)")
print("   If true: System correctly identified 1 family for 1 domain")
print("   Expected: New domains (grief, crisis) should form families 2-3")
print()

print("="*80)
print("🚀 RECOMMENDED NEXT STEPS")
print("="*80)
print()
print("1. Check if NEW conversations (grief/crisis) were actually LEARNED")
print("   - Review epochs 21-26 learning reports")
print("   - Verify satisfaction_score ≥ threshold for new domains")
print()
print("2. If not learned: Lower satisfaction threshold (currently 0.55)")
print("   - Try 0.45 or 0.40 to enable learning from more conversations")
print()
print("3. If learned but still 1 family: Signature extraction issue")
print("   - Signatures may not be discriminative enough")
print("   - Consider organ-weighted signatures or sparse encoding")
print()
print("4. Nuclear option: Reset families and restart learning")
print("   - Delete organic_families.json")
print("   - Re-run epochs with new signature extraction")
print()

print("💡 INSIGHT: The issue may be satisfaction_threshold, not similarity_threshold!")
print("   - similarity_threshold controls family membership")
print("   - learning_threshold controls WHEN to learn")
print("   - If new domains scored < 0.55 satisfaction, they were NEVER learned")
print()
