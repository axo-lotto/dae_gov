#!/usr/bin/env python3
"""
Test 65D Family Discrimination with Organ Agreement Metrics
============================================================

Compare discriminating power of:
- 57D signatures (base transformation + RNX/TSK)
- 65D signatures (57D + FAO organ agreement from FFITTSS T4)

Expected: 65D signatures should show LOWER cosine similarity between
different felt-state categories, enabling multi-family emergence.

Philosophy (FFITTSS T4 + Whitehead):
- Pairwise Agreement: How much organs converge on same felt-sense
- Organ Entropy: Diversity of organ activations
- Multiplicity Index: Degree of specialization before unification
- These create ORTHOGONAL directions that break single-family clustering

Date: November 16, 2025
Reference: FFITTSS T4/README.md, SIGNAL_AUDIT.md
"""

import numpy as np
from persona_layer.organ_signature_extractor import OrganSignatureExtractor


def create_crisis_felt_state():
    """Crisis: High NDAM, sympathetic, high urgency, organ disagreement."""
    return {
        'v0_initial': 1.0,
        'satisfaction': 0.3,
        'zone': 4,
        'urgency': 0.85,
        'organ_coherences': {
            'LISTENING': 0.45, 'EMPATHY': 0.42, 'WISDOM': 0.50,
            'AUTHENTICITY': 0.48, 'PRESENCE': 0.35, 'BOND': 0.60,
            'SANS': 0.40, 'NDAM': 0.95, 'RNX': 0.55, 'EO': 0.88, 'CARD': 0.72
        },
        'polyvagal_state': 'sympathetic'
    }, {
        'v0_final': 0.5,
        'satisfaction_final': 0.55,
        'zone': 3,
        'urgency': 0.65,
        'convergence_cycles': 4,
        'kairos_detected': False,
        'organ_coherences': {
            'LISTENING': 0.52, 'EMPATHY': 0.48, 'WISDOM': 0.55,
            'AUTHENTICITY': 0.50, 'PRESENCE': 0.42, 'BOND': 0.65,
            'SANS': 0.45, 'NDAM': 0.82, 'RNX': 0.60, 'EO': 0.78, 'CARD': 0.68
        },
        'polyvagal_state': 'sympathetic'
    }


def create_safety_felt_state():
    """Safety: Low NDAM, ventral, low urgency, high organ agreement."""
    return {
        'v0_initial': 0.8,
        'satisfaction': 0.6,
        'zone': 2,
        'urgency': 0.1,
        'organ_coherences': {
            'LISTENING': 0.82, 'EMPATHY': 0.85, 'WISDOM': 0.78,
            'AUTHENTICITY': 0.80, 'PRESENCE': 0.88, 'BOND': 0.75,
            'SANS': 0.83, 'NDAM': 0.25, 'RNX': 0.79, 'EO': 0.92, 'CARD': 0.76
        },
        'polyvagal_state': 'ventral'
    }, {
        'v0_final': 0.2,
        'satisfaction_final': 0.85,
        'zone': 1,
        'urgency': 0.0,
        'convergence_cycles': 2,
        'kairos_detected': True,
        'organ_coherences': {
            'LISTENING': 0.88, 'EMPATHY': 0.90, 'WISDOM': 0.85,
            'AUTHENTICITY': 0.87, 'PRESENCE': 0.92, 'BOND': 0.80,
            'SANS': 0.88, 'NDAM': 0.15, 'RNX': 0.84, 'EO': 0.95, 'CARD': 0.82
        },
        'polyvagal_state': 'ventral'
    }


def create_ambivalence_felt_state():
    """Ambivalence: Mixed state, high organ disagreement."""
    return {
        'v0_initial': 0.9,
        'satisfaction': 0.4,
        'zone': 3,
        'urgency': 0.45,
        'organ_coherences': {
            'LISTENING': 0.45, 'EMPATHY': 0.85, 'WISDOM': 0.35,
            'AUTHENTICITY': 0.90, 'PRESENCE': 0.30, 'BOND': 0.80,
            'SANS': 0.40, 'NDAM': 0.55, 'RNX': 0.25, 'EO': 0.60, 'CARD': 0.50
        },
        'polyvagal_state': 'mixed_state'
    }, {
        'v0_final': 0.4,
        'satisfaction_final': 0.65,
        'zone': 2,
        'urgency': 0.35,
        'convergence_cycles': 4,
        'kairos_detected': False,
        'organ_coherences': {
            'LISTENING': 0.52, 'EMPATHY': 0.82, 'WISDOM': 0.42,
            'AUTHENTICITY': 0.85, 'PRESENCE': 0.38, 'BOND': 0.75,
            'SANS': 0.48, 'NDAM': 0.45, 'RNX': 0.32, 'EO': 0.65, 'CARD': 0.55
        },
        'polyvagal_state': 'mixed_state'
    }


def create_collapse_felt_state():
    """Collapse: Dorsal, low activation, organ shutdown."""
    return {
        'v0_initial': 0.7,
        'satisfaction': 0.35,
        'zone': 5,
        'urgency': 0.2,
        'organ_coherences': {
            'LISTENING': 0.25, 'EMPATHY': 0.30, 'WISDOM': 0.28,
            'AUTHENTICITY': 0.22, 'PRESENCE': 0.15, 'BOND': 0.35,
            'SANS': 0.32, 'NDAM': 0.40, 'RNX': 0.20, 'EO': 0.45, 'CARD': 0.38
        },
        'polyvagal_state': 'dorsal'
    }, {
        'v0_final': 0.6,
        'satisfaction_final': 0.45,
        'zone': 4,
        'urgency': 0.25,
        'convergence_cycles': 3,
        'kairos_detected': False,
        'organ_coherences': {
            'LISTENING': 0.32, 'EMPATHY': 0.35, 'WISDOM': 0.30,
            'AUTHENTICITY': 0.28, 'PRESENCE': 0.22, 'BOND': 0.40,
            'SANS': 0.38, 'NDAM': 0.35, 'RNX': 0.25, 'EO': 0.50, 'CARD': 0.42
        },
        'polyvagal_state': 'dorsal'
    }


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def main():
    print("=" * 80)
    print("65D FAMILY DISCRIMINATION TEST")
    print("Comparing 57D vs 65D signatures with Organ Agreement Metrics")
    print("=" * 80)

    extractor = OrganSignatureExtractor()

    # Create synthetic felt states
    categories = {
        'crisis': create_crisis_felt_state(),
        'safety': create_safety_felt_state(),
        'ambivalence': create_ambivalence_felt_state(),
        'collapse': create_collapse_felt_state()
    }

    # Extract signatures
    signatures_57d = {}
    signatures_65d = {}

    for name, (initial, final) in categories.items():
        signatures_57d[name] = extractor.extract_transformation_signature_57d(initial, final)
        signatures_65d[name] = extractor.extract_transformation_signature_65d(initial, final)

    # Compute pairwise similarities
    print("\n" + "=" * 80)
    print("PAIRWISE COSINE SIMILARITIES")
    print("=" * 80)

    category_names = list(categories.keys())
    similarities_57d = {}
    similarities_65d = {}

    print("\n57D SIGNATURES (base):")
    for i, name1 in enumerate(category_names):
        for name2 in category_names[i+1:]:
            sim = cosine_similarity(signatures_57d[name1], signatures_57d[name2])
            key = f"{name1} vs {name2}"
            similarities_57d[key] = sim
            print(f"  {key:30s}: {sim:.4f}")

    print("\n65D SIGNATURES (with organ agreement):")
    for i, name1 in enumerate(category_names):
        for name2 in category_names[i+1:]:
            sim = cosine_similarity(signatures_65d[name1], signatures_65d[name2])
            key = f"{name1} vs {name2}"
            similarities_65d[key] = sim
            print(f"  {key:30s}: {sim:.4f}")

    # Compare improvements
    print("\n" + "=" * 80)
    print("SIMILARITY REDUCTION (lower = better discrimination)")
    print("=" * 80)

    for key in similarities_57d:
        diff = similarities_57d[key] - similarities_65d[key]
        improvement = (diff / similarities_57d[key]) * 100 if similarities_57d[key] > 0 else 0
        print(f"  {key:30s}: {diff:+.4f} ({improvement:+.1f}% improvement)")

    # Summary statistics
    mean_57d = np.mean(list(similarities_57d.values()))
    mean_65d = np.mean(list(similarities_65d.values()))
    std_57d = np.std(list(similarities_57d.values()))
    std_65d = np.std(list(similarities_65d.values()))

    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    print(f"\n57D Signatures:")
    print(f"  Mean similarity: {mean_57d:.4f}")
    print(f"  Std similarity:  {std_57d:.4f}")

    print(f"\n65D Signatures:")
    print(f"  Mean similarity: {mean_65d:.4f}")
    print(f"  Std similarity:  {std_65d:.4f}")

    improvement_mean = ((mean_57d - mean_65d) / mean_57d) * 100
    print(f"\nOverall improvement: {improvement_mean:.1f}% reduction in mean similarity")

    # Show organ agreement dimensions for each category
    print("\n" + "=" * 80)
    print("ORGAN AGREEMENT DIMENSIONS BY CATEGORY")
    print("=" * 80)

    for name in category_names:
        sig = signatures_65d[name]
        print(f"\n{name.upper()}:")
        print(f"  Pairwise Agreement: {sig[57]:.4f}")
        print(f"  Organ Entropy:      {sig[58]:.4f}")
        print(f"  Nexus Coherence:    {sig[59]:.4f}")
        print(f"  Multiplicity Index: {sig[60]:.4f}")
        print(f"  Max Disagreement:   {sig[63]:.4f}")

    # Verdict
    print("\n" + "=" * 80)
    print("VERDICT")
    print("=" * 80)

    if improvement_mean > 5:
        print("✅ 65D signatures show SIGNIFICANT improvement in family discrimination!")
        print("   - Organ agreement metrics create orthogonal directions")
        print("   - Different felt-states are more separable")
        print("   - Multi-family emergence is more likely")
    elif improvement_mean > 2:
        print("⚠️ 65D signatures show MODERATE improvement")
        print("   - Some discrimination gain from agreement metrics")
        print("   - May need higher similarity threshold (0.80+)")
    else:
        print("❌ 65D signatures show MINIMAL improvement")
        print("   - L2 normalization still dominating")
        print("   - Consider: Don't normalize, or use Euclidean distance")

    # Recommendation
    print("\n" + "=" * 80)
    print("RECOMMENDED NEXT STEPS")
    print("=" * 80)
    print("""
1. If improvement > 10%: Integrate 65D into Phase 5 learning
   - Modify phase5_learning_integration.py to use extract_transformation_signature_65d()
   - Update organic_families.json schema to 65D centroids

2. If improvement 2-10%: Increase similarity threshold to 0.85+
   - File: persona_layer/organic_conversational_families.py
   - Method: _get_adaptive_threshold()

3. If improvement < 2%: Consider non-normalized signatures
   - Remove L2 normalization from 65D method
   - Use Euclidean distance instead of cosine similarity

4. Track organ agreement patterns per family
   - High agreement families = consensus patterns
   - High multiplicity families = specialization patterns
   - This enables Whiteheadian "many become one" learning
""")

    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
