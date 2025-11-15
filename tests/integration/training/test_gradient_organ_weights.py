"""
Test Gradient-Based Organ Weight Learning
==========================================

Compares DAE 3.0 gradient-based organ weight learning vs EMA baseline.

Expected behavior:
- Gradient-based: w[organ] += η · (coherence - mean) · R₃
- EMA baseline: w[organ] = 0.9 * w[organ] + 0.1 * coherence

Hypothesis:
- Gradient-based should amplify organs above mean, suppress below mean
- EMA should smoothly track coherences without differentiation
- Gradient-based should show faster convergence to optimal weights

Date: November 12, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from persona_layer.family_v0_learner import FamilyV0Learner

def test_gradient_vs_ema():
    """Compare gradient-based vs EMA organ weight learning"""

    print("="*80)
    print("🧪 GRADIENT-BASED ORGAN WEIGHT LEARNING TEST")
    print("="*80)

    # Initialize two learners: gradient-based and EMA
    print("\n📋 Initializing learners...")

    learner_gradient = FamilyV0Learner(
        families_path=Path("/tmp/test_gradient_families.json"),
        learning_rate=0.1,
        organ_learning_rate=0.05,
        use_gradient_weights=True  # Gradient-based
    )

    learner_ema = FamilyV0Learner(
        families_path=Path("/tmp/test_ema_families.json"),
        learning_rate=0.1,
        organ_learning_rate=0.05,
        use_gradient_weights=False  # EMA baseline
    )

    print("   ✅ Gradient-based learner initialized (use_gradient_weights=True)")
    print("   ✅ EMA baseline learner initialized (use_gradient_weights=False)")

    # Simulate conversations with varying organ patterns
    family_id = "TestFamily_001"

    test_conversations = [
        {
            'name': 'High SANS + PRESENCE (above mean)',
            'organ_coherences': {
                'LISTENING': 0.6,
                'EMPATHY': 0.55,
                'WISDOM': 0.5,
                'PRESENCE': 0.85,  # High
                'SANS': 0.90,      # High
                'CARD': 0.5,
                'BOND': 0.4,
                'NDAM': 0.45
            },
            'r_matrix_coupling': 0.05,  # Realistic coupling from R-matrix
            'v0_final': 0.25,
            'satisfaction': 0.88,
            'convergence_cycles': 2
        },
        {
            'name': 'High EMPATHY + LISTENING (relational)',
            'organ_coherences': {
                'LISTENING': 0.88,  # High
                'EMPATHY': 0.92,    # High
                'WISDOM': 0.55,
                'PRESENCE': 0.65,
                'SANS': 0.50,
                'CARD': 0.45,
                'BOND': 0.35,
                'NDAM': 0.40
            },
            'r_matrix_coupling': 0.06,
            'v0_final': 0.22,
            'satisfaction': 0.91,
            'convergence_cycles': 2
        },
        {
            'name': 'Balanced activation',
            'organ_coherences': {
                'LISTENING': 0.70,
                'EMPATHY': 0.72,
                'WISDOM': 0.68,
                'PRESENCE': 0.75,
                'SANS': 0.73,
                'CARD': 0.69,
                'BOND': 0.65,
                'NDAM': 0.71
            },
            'r_matrix_coupling': 0.05,
            'v0_final': 0.28,
            'satisfaction': 0.85,
            'convergence_cycles': 3
        },
        {
            'name': 'High SANS again (reinforcement)',
            'organ_coherences': {
                'LISTENING': 0.58,
                'EMPATHY': 0.55,
                'WISDOM': 0.62,
                'PRESENCE': 0.80,
                'SANS': 0.87,      # High again
                'CARD': 0.52,
                'BOND': 0.45,
                'NDAM': 0.50
            },
            'r_matrix_coupling': 0.06,
            'v0_final': 0.24,
            'satisfaction': 0.89,
            'convergence_cycles': 2
        }
    ]

    print(f"\n🗣️  Processing {len(test_conversations)} conversations...")

    # Track weight evolution
    gradient_weights_history = []
    ema_weights_history = []

    for i, conv in enumerate(test_conversations, 1):
        print(f"\n{'─'*80}")
        print(f"Conversation {i}: {conv['name']}")
        print(f"{'─'*80}")

        # Compute mean coherence for reference
        mean_coherence = np.mean(list(conv['organ_coherences'].values()))
        print(f"Mean coherence: {mean_coherence:.3f}")
        print(f"R-matrix coupling: {conv['r_matrix_coupling']:.3f}")

        # Update both learners
        learner_gradient.update_family_v0(
            family_id=family_id,
            v0_final=conv['v0_final'],
            satisfaction=conv['satisfaction'],
            convergence_cycles=conv['convergence_cycles'],
            organ_coherences=conv['organ_coherences'],
            r_matrix_coupling=conv['r_matrix_coupling'],
            verbose=False
        )

        learner_ema.update_family_v0(
            family_id=family_id,
            v0_final=conv['v0_final'],
            satisfaction=conv['satisfaction'],
            convergence_cycles=conv['convergence_cycles'],
            organ_coherences=conv['organ_coherences'],
            r_matrix_coupling=conv['r_matrix_coupling'],  # Passed but not used in EMA
            verbose=False
        )

        # Get current weights
        gradient_weights = learner_gradient.get_organ_weights(family_id)
        ema_weights = learner_ema.get_organ_weights(family_id)

        gradient_weights_history.append(gradient_weights.copy())
        ema_weights_history.append(ema_weights.copy())

        # Show top 3 organs from each method
        print(f"\n   Gradient-based top 3:")
        for organ, weight in sorted(gradient_weights.items(), key=lambda x: x[1], reverse=True)[:3]:
            deviation = conv['organ_coherences'].get(organ, mean_coherence) - mean_coherence
            print(f"      • {organ}: {weight:.3f} (coherence deviation: {deviation:+.3f})")

        print(f"\n   EMA baseline top 3:")
        for organ, weight in sorted(ema_weights.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"      • {organ}: {weight:.3f}")

    # Final comparison
    print(f"\n{'='*80}")
    print("📊 FINAL WEIGHT COMPARISON")
    print(f"{'='*80}")

    final_gradient = learner_gradient.get_organ_weights(family_id)
    final_ema = learner_ema.get_organ_weights(family_id)

    # Compute weight variance (measure of differentiation)
    gradient_variance = np.var(list(final_gradient.values()))
    ema_variance = np.var(list(final_ema.values()))

    print(f"\n📈 Weight Differentiation:")
    print(f"   Gradient-based variance: {gradient_variance:.4f}")
    print(f"   EMA baseline variance: {ema_variance:.4f}")
    print(f"   Differentiation ratio: {gradient_variance / ema_variance:.2f}× (higher = more selective)")

    # Show all organs sorted by gradient weight
    print(f"\n🏆 Final Organ Weights (Gradient-Based):")
    for organ, weight in sorted(final_gradient.items(), key=lambda x: x[1], reverse=True):
        ema_weight = final_ema.get(organ, 0.0)
        delta = weight - ema_weight
        print(f"   {organ:12s}: {weight:.3f} (EMA: {ema_weight:.3f}, Δ={delta:+.3f})")

    # Validate gradient-based learning
    print(f"\n{'='*80}")
    print("✅ VALIDATION")
    print(f"{'='*80}")

    # Check if gradient-based shows higher differentiation
    if gradient_variance > ema_variance:
        print(f"✅ SUCCESS: Gradient-based shows {gradient_variance / ema_variance:.2f}× higher differentiation!")
        print(f"   This indicates stronger organ specialization")
    else:
        print(f"⚠️  WARNING: Gradient-based variance not higher than EMA")
        print(f"   Expected behavior: gradient amplifies deviations from mean")

    # Check if SANS weight increased (it was consistently above mean)
    sans_gradient = final_gradient.get('SANS', 0.0)
    sans_ema = final_ema.get('SANS', 0.0)

    print(f"\n🔍 SANS Organ (consistently high coherence):")
    print(f"   Gradient-based: {sans_gradient:.3f}")
    print(f"   EMA baseline: {sans_ema:.3f}")
    if sans_gradient > sans_ema:
        print(f"   ✅ Gradient correctly amplified SANS (+{sans_gradient - sans_ema:.3f})")
    else:
        print(f"   ⚠️  Gradient did not amplify SANS as expected")

    # Check if low organs suppressed
    bond_gradient = final_gradient.get('BOND', 0.0)
    bond_ema = final_ema.get('BOND', 0.0)

    print(f"\n🔍 BOND Organ (consistently low coherence):")
    print(f"   Gradient-based: {bond_gradient:.3f}")
    print(f"   EMA baseline: {bond_ema:.3f}")
    if bond_gradient < bond_ema:
        print(f"   ✅ Gradient correctly suppressed BOND ({bond_gradient - bond_ema:.3f})")
    else:
        print(f"   ⚠️  Gradient did not suppress BOND as expected")

    print(f"\n✅ Gradient-based organ weight learning test complete!")

if __name__ == '__main__':
    test_gradient_vs_ema()
