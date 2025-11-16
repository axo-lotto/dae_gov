#!/usr/bin/env python3
"""
Diagnose Single-Family Clustering Root Cause
============================================

Hypothesis: 57D signatures lack discrimination because:
1. Organ coherences are too similar across different inputs
2. L2 normalization collapses information
3. Sparse vectors have high cosine similarity

This script analyzes the actual signature patterns to find why
crisis/collapse/safety/protective inputs cluster together.
"""

import json
import numpy as np
from pathlib import Path

def load_family_state():
    """Load current family state."""
    path = Path("persona_layer/organic_families.json")
    with open(path, 'r') as f:
        return json.load(f)

def analyze_centroid_structure():
    """Analyze the centroid to understand signature structure."""
    state = load_family_state()

    if not state.get('families'):
        print("No families found!")
        return

    centroid = np.array(state['families']['Family_001']['centroid'])

    print("=" * 80)
    print("CENTROID ANALYSIS (Family_001)")
    print("=" * 80)

    print(f"\nDimensions: {len(centroid)}")
    print(f"L2 Norm: {np.linalg.norm(centroid):.6f}")
    print(f"Min: {np.min(centroid):.6f}")
    print(f"Max: {np.max(centroid):.6f}")
    print(f"Mean: {np.mean(centroid):.6f}")
    print(f"Std: {np.std(centroid):.6f}")

    # Count zeros and near-zeros
    zero_count = np.sum(np.abs(centroid) < 1e-6)
    near_zero_count = np.sum(np.abs(centroid) < 0.01)

    print(f"\nZero dimensions: {zero_count}/{len(centroid)} ({100*zero_count/len(centroid):.1f}%)")
    print(f"Near-zero (<0.01): {near_zero_count}/{len(centroid)} ({100*near_zero_count/len(centroid):.1f}%)")

    # Top dimensions by magnitude
    sorted_indices = np.argsort(np.abs(centroid))[::-1]
    print(f"\nTop 10 dimensions by magnitude:")
    for i in range(10):
        idx = sorted_indices[i]
        print(f"  dim {idx:2d}: {centroid[idx]:+.6f}")

    # Analyze signature structure (assuming 57D = 11 organs × 5-7 dims each + extras)
    # Actually 57D structure: 40D base (11 organs × ~3.6 dims) + 17D RNX/TSK
    print(f"\n--- SIGNATURE STRUCTURE ---")

    # Hypothetical structure (we need to verify this)
    # From 57D_RNX_TSK_IMPLEMENTATION_COMPLETE_NOV16_2025.md:
    # Positions 0-10: Organ coherences (11 dims)
    # Positions 11-20: Organ shifts (11 dims)
    # Positions 21-30: Meta-atom activations (10 dims)
    # Positions 31-40: Transformation markers (10 dims)
    # Positions 41-48: Polyvagal/Zone/Urgency/RNX (8 dims)
    # Positions 49-56: Nexus/Pathway/Healing (8 dims)

    print("\nAssuming 57D structure:")
    print("  [0:11]   Organ coherences")
    print("  [11:22]  Organ shifts")
    print("  [22:32]  Meta-atom activations")
    print("  [32:42]  Transformation markers")
    print("  [42:50]  Polyvagal/Zone/Urgency/RNX")
    print("  [50:57]  Nexus/Pathway/Healing")

    if len(centroid) >= 57:
        print("\nActual values per segment:")
        segments = [
            ("Organ coherences", centroid[0:11]),
            ("Organ shifts", centroid[11:22]),
            ("Meta-atom activations", centroid[22:32]),
            ("Transformation markers", centroid[32:42]),
            ("Polyvagal/Zone/Urgency/RNX", centroid[42:50]),
            ("Nexus/Pathway/Healing", centroid[50:57]),
        ]

        for name, segment in segments:
            nonzero = np.sum(np.abs(segment) > 0.01)
            print(f"\n  {name}:")
            print(f"    Non-zero: {nonzero}/{len(segment)}")
            print(f"    Mean: {np.mean(segment):.4f}")
            print(f"    Max: {np.max(np.abs(segment)):.4f}")
            if nonzero > 0:
                print(f"    Values: {segment}")


def compute_synthetic_signature_similarity():
    """
    Generate synthetic signatures for different input types
    and compute their cosine similarity to understand why clustering fails.
    """
    print("\n" + "=" * 80)
    print("SYNTHETIC SIGNATURE SIMILARITY ANALYSIS")
    print("=" * 80)

    # Create synthetic 57D signatures representing expected patterns

    # Crisis: High NDAM, High EO (sympathetic), High urgency
    crisis_sig = np.zeros(57)
    crisis_sig[0:11] = [0.9, 0.3, 0.4, 0.5, 0.3, 0.2, 0.5, 0.95, 0.6, 0.85, 0.4]  # High NDAM (7), EO (9)
    crisis_sig[42] = 0.9  # Urgency
    crisis_sig[43] = 4.0  # Zone 4
    crisis_sig[44] = 1.0  # Sympathetic

    # Collapse: High dorsal, low urgency, zone 5
    collapse_sig = np.zeros(57)
    collapse_sig[0:11] = [0.3, 0.2, 0.3, 0.4, 0.2, 0.8, 0.4, 0.3, 0.7, 0.5, 0.3]  # High BOND (5), RNX (8)
    collapse_sig[42] = 0.2  # Low urgency
    collapse_sig[43] = 5.0  # Zone 5
    collapse_sig[44] = -1.0  # Dorsal

    # Safety: Ventral, zone 1, grounded
    safety_sig = np.zeros(57)
    safety_sig[0:11] = [0.8, 0.7, 0.6, 0.7, 0.9, 0.4, 0.7, 0.4, 0.3, 0.8, 0.6]  # High PRESENCE (4), EO (9)
    safety_sig[42] = 0.0  # No urgency
    safety_sig[43] = 1.0  # Zone 1
    safety_sig[44] = 1.0  # Ventral

    # Protective: Manager parts active, mixed state
    protective_sig = np.zeros(57)
    protective_sig[0:11] = [0.6, 0.5, 0.7, 0.5, 0.6, 0.7, 0.6, 0.5, 0.6, 0.6, 0.5]  # Balanced
    protective_sig[42] = 0.4  # Medium urgency
    protective_sig[43] = 3.0  # Zone 3
    protective_sig[44] = 0.0  # Mixed

    signatures = {
        'crisis': crisis_sig,
        'collapse': collapse_sig,
        'safety': safety_sig,
        'protective': protective_sig
    }

    # Normalize all signatures (L2)
    for name in signatures:
        norm = np.linalg.norm(signatures[name])
        if norm > 1e-6:
            signatures[name] = signatures[name] / norm

    print("\nCosine similarities between synthetic signatures (before normalization artifacts):")
    names = list(signatures.keys())
    for i, name1 in enumerate(names):
        for name2 in names[i+1:]:
            sim = np.dot(signatures[name1], signatures[name2])
            print(f"  {name1:12s} vs {name2:12s}: {sim:.4f}")

    print("\n🔑 KEY INSIGHT: L2 normalization makes all vectors unit vectors,")
    print("   and cosine similarity becomes dot product.")
    print("   If organ coherences are similar (all 0.3-0.8), normalized signatures cluster!")


def analyze_actual_signature_extraction():
    """
    Explain the actual signature extraction pipeline to identify the issue.
    """
    print("\n" + "=" * 80)
    print("ACTUAL SIGNATURE EXTRACTION PIPELINE ANALYSIS")
    print("=" * 80)

    print("""
The 57D signature is extracted in:
  persona_layer/phase5_learning_integration.py : _extract_57d_signature()

SUSPECTED ISSUE:
  The signature includes organ COHERENCES (0-1 range), but:
  1. Most organs return coherence 0.3-0.8 for ANY input
  2. L2 normalization collapses variance
  3. Result: all signatures point in same direction (high similarity)

EXAMPLE:
  Crisis input:  BOND=0.45, SANS=0.52, NDAM=0.78, RNX=0.41, EO=0.65, CARD=0.55
  Safety input:  BOND=0.52, SANS=0.48, NDAM=0.35, RNX=0.44, EO=0.72, CARD=0.58

  These look different, but after normalization:
    dot product ≈ 0.85-0.95 (high similarity!)

WHY THIS HAPPENS:
  - Organ coherences are bounded [0, 1]
  - Most coherences cluster around 0.4-0.7 (reasonable activation)
  - Small differences (0.35 vs 0.78) become negligible after L2 normalization
  - The signature space is "sparse" (few dimensions dominate)

SOLUTION OPTIONS:
  1. Use transformation signatures (delta coherence), not absolute coherence
  2. Include more discriminating features (raw polyvagal state, zone integer, etc.)
  3. Increase threshold to 0.85+ (force tighter clustering)
  4. Use different distance metric (Euclidean instead of cosine)
  5. Don't L2 normalize (use raw coherence vectors)
""")


def recommend_fixes():
    """
    Provide actionable recommendations based on analysis.
    """
    print("\n" + "=" * 80)
    print("RECOMMENDED FIXES FOR MULTI-FAMILY EMERGENCE")
    print("=" * 80)

    print("""
1. **QUICK FIX: Increase similarity threshold**
   - Change adaptive threshold to 0.85-0.95 (currently 0.55)
   - File: persona_layer/organic_conversational_families.py:419-444
   - Effect: Forces family separation, but may be too restrictive

2. **BETTER FIX: Include categorical features as discrete dimensions**
   - Add one-hot encoded polyvagal state: [ventral=1,0,0], [sympathetic=0,1,0], [dorsal=0,0,1]
   - Add zone as categorical: zone_1=1 vs zone_5=1 (not continuous 1-5)
   - These create orthogonal directions that break clustering

3. **BEST FIX: Use transformation deltas, not absolute coherences**
   - Track: delta_coherence = post_coherence - pre_coherence
   - High NDAM shift (+0.5) vs low NDAM shift (-0.1) creates discrimination
   - This is what "TSK" (Transductive State Knowledge) should capture

4. **DON'T L2 NORMALIZE (experimental)**
   - Raw coherence vectors maintain absolute magnitude information
   - Crisis (high values) vs collapse (low values) become distinct
   - Risk: Need to adjust similarity metric

5. **ADD NEXUS TYPE AS CATEGORICAL**
   - 14 nexus types = 14 orthogonal dimensions
   - crisis_nexus vs safety_nexus creates family separation
   - This leverages existing infrastructure!
""")


def main():
    """Run all diagnostic analyses."""
    print("=" * 80)
    print("SINGLE-FAMILY CLUSTERING ROOT CAUSE DIAGNOSIS")
    print("=" * 80)

    analyze_centroid_structure()
    compute_synthetic_signature_similarity()
    analyze_actual_signature_extraction()
    recommend_fixes()

    print("\n" + "=" * 80)
    print("DIAGNOSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
