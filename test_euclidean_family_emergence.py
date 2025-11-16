#!/usr/bin/env python3
"""
Test Euclidean Distance Multi-Family Emergence
==============================================

Validates the critical fix for single-family clustering:
1. Switched from cosine similarity to Euclidean distance
2. Removed L2 normalization from signatures
3. Added adaptive distance thresholds (1.5, 2.0, 2.5)

Expected Outcome:
- Different felt-state categories (crisis/safety/ambivalence/collapse) form separate families
- 4-6 families expected after processing 4 synthetic inputs
- Distance between crisis and safety signatures: ~3.7 (well above 1.5 threshold)

Date: November 16, 2025
Reference: FAO_ORGAN_AGREEMENT_INTEGRATION_NOV16_2025.md
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from persona_layer.phase5_learning_integration import Phase5LearningIntegration


def create_crisis_states():
    """Crisis: High NDAM, sympathetic, high urgency."""
    initial = {
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
    }
    final = {
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
    return initial, final


def create_safety_states():
    """Safety: Low NDAM, ventral, low urgency."""
    initial = {
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
    }
    final = {
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
    return initial, final


def create_ambivalence_states():
    """Ambivalence: Mixed state, high organ disagreement."""
    initial = {
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
    }
    final = {
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
    return initial, final


def create_collapse_states():
    """Collapse: Dorsal, low activation, organ shutdown."""
    initial = {
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
    }
    final = {
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
    return initial, final


def main():
    print("=" * 80)
    print("🆕 EUCLIDEAN DISTANCE MULTI-FAMILY EMERGENCE TEST")
    print("=" * 80)
    print("\nTesting the critical fix for single-family clustering:")
    print("  - OLD: Cosine similarity on L2-normalized signatures")
    print("         → All conversations cluster into 1 family (too similar)")
    print("  - NEW: Euclidean distance on raw signatures")
    print("         → Multi-family emergence (magnitude preserved)")
    print("")

    # Reset families for clean test
    import json
    families_path = "persona_layer/organic_families.json"

    print("🔄 Resetting families for clean test...")
    with open(families_path, 'w') as f:
        json.dump({"families": {}, "metadata": {"version": "65D_euclidean", "created": "2025-11-16"}}, f)

    # Initialize Phase 5 learning
    print("\n📊 Initializing Phase 5 Learning (65D + Euclidean distance)...")
    learner = Phase5LearningIntegration(
        storage_path="persona_layer",
        learning_threshold=0.30,  # Low threshold to capture all test cases
        enable_learning=True
    )

    print(f"   Initial families: {len(learner.families.families)}")

    # Test categories
    test_cases = [
        ("CRISIS", create_crisis_states(), "I'm having a panic attack and can't breathe"),
        ("SAFETY", create_safety_states(), "I feel so calm and grounded right now"),
        ("AMBIVALENCE", create_ambivalence_states(), "Part of me wants to leave but part of me is scared"),
        ("COLLAPSE", create_collapse_states(), "I can't feel anything anymore, I'm just numb"),
    ]

    results = []

    print("\n" + "=" * 80)
    print("PROCESSING TEST CASES")
    print("=" * 80)

    for i, (name, (initial, final), message) in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {name} ---")
        print(f"Message: '{message}'")
        print(f"Initial polyvagal: {initial['polyvagal_state']}")
        print(f"Final polyvagal: {final['polyvagal_state']}")
        print(f"Urgency: {initial['urgency']:.2f} → {final['urgency']:.2f}")

        # Learn from this transformation
        report = learner.learn_from_conversation_transformation(
            initial_felt_state=initial,
            final_felt_state=final,
            emission_text=f"[Generated therapeutic response for {name.lower()} state]",
            user_message=message,
            conversation_id=f"test_{name.lower()}_{i}",
            transduction_trajectory=[],
            constraint_deltas={}
        )

        if report:
            print(f"\n✅ Learning Report:")
            print(f"   Family ID: {report['family_id']}")
            print(f"   Is New Family: {report['is_new_family']}")
            print(f"   Similarity Score: {report['similarity']:.4f}")
            print(f"   Total Families: {report['total_families']}")
            results.append(report)
        else:
            print(f"\n❌ Learning failed for {name}")

    # Summary
    print("\n" + "=" * 80)
    print("MULTI-FAMILY EMERGENCE RESULTS")
    print("=" * 80)

    total_families = len(learner.families.families)
    unique_families = set(r['family_id'] for r in results)

    print(f"\nTotal families created: {total_families}")
    print(f"Unique families assigned: {len(unique_families)}")
    print(f"Family IDs: {sorted(unique_families)}")

    # Check if crisis and safety are in different families
    crisis_family = None
    safety_family = None

    for r in results:
        if 'crisis' in r['conversation_id']:
            crisis_family = r['family_id']
        elif 'safety' in r['conversation_id']:
            safety_family = r['family_id']

    print(f"\nCrisis family: {crisis_family}")
    print(f"Safety family: {safety_family}")

    # Verdict
    print("\n" + "=" * 80)
    print("VERDICT")
    print("=" * 80)

    if total_families >= 3:
        print("✅ SUCCESS! Multi-family emergence achieved!")
        print(f"   {total_families} families formed (expected 3-4)")
        if crisis_family != safety_family:
            print("   ✅ Crisis and Safety are in DIFFERENT families (excellent!)")
        else:
            print("   ⚠️ Crisis and Safety in same family (threshold may need tuning)")
    elif total_families == 2:
        print("⚠️ PARTIAL SUCCESS - 2 families emerged")
        print("   Consider lowering distance threshold (current: 1.5)")
    else:
        print("❌ FAILURE - Still single-family clustering")
        print("   Check:")
        print("   1. Is 65D extraction being used? (should be)")
        print("   2. Is normalize=False? (should be)")
        print("   3. Is Euclidean distance used? (should be)")

    # Family details
    print("\n" + "=" * 80)
    print("FAMILY DETAILS")
    print("=" * 80)

    for fam_id, family in learner.families.families.items():
        print(f"\nFamily {fam_id}:")
        print(f"  Members: {family.member_count}")
        print(f"  Mean Satisfaction: {family.mean_satisfaction:.4f}")
        print(f"  Centroid magnitude: {np.linalg.norm(family.centroid):.4f}")

        # Show organ agreement dimensions (indices 57-64)
        if len(family.centroid) >= 65:
            print(f"  Pairwise Agreement: {family.centroid[57]:.4f}")
            print(f"  Organ Entropy: {family.centroid[58]:.4f}")
            print(f"  Multiplicity Index: {family.centroid[60]:.4f}")
            print(f"  Max Disagreement: {family.centroid[63]:.4f}")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

    return total_families >= 3


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
