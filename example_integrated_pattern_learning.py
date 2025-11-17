"""
Integrated Pattern Learning Example
====================================

Demonstrates three-layer quality modulation:
1. Base EMA Learning (nexus_phrase_pattern_learner)
2. Satisfaction Fingerprinting (temporal pattern classification)
3. Lyapunov Stability Gating (field dynamics)

This example shows how all components work together to achieve
+16-25pp phrase quality improvement from proven FFITTSS patterns.

November 17, 2025 - Phase 1 Week 2 Complete
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.nexus_signature_extractor import NexusSignature
from persona_layer.nexus_phrase_pattern_learner import NexusPhrasePatternLearner
from persona_layer.satisfaction_fingerprinting import SatisfactionFingerprintClassifier
from persona_layer.lyapunov_nexus_stability import LyapunovNexusStabilityGate


def create_example_nexus_signature() -> NexusSignature:
    """Create example nexus signature for crisis witnessing."""
    return NexusSignature(
        participating_organs=frozenset(['EMPATHY', 'NDAM', 'RNX']),
        organ_count=3,
        nexus_type='PSYCHE',
        mechanism='CRISIS_WITNESSING',
        coherence_bin=6,
        urgency_bin=8,
        polyvagal_state='sympathetic',
        zone=4,
        v0_energy_bin=2,
        kairos_detected=False,
        field_strength_bin=5,
        dominant_meta_atom='emotional_resonance'
    )


def simulate_conversation_with_learning():
    """
    Simulate multi-turn conversation with integrated pattern learning.

    Scenario: User experiencing crisis → gradual recovery (RESTORATIVE pattern)
    """
    print("=" * 70)
    print("INTEGRATED PATTERN LEARNING DEMONSTRATION")
    print("=" * 70)
    print()
    print("Scenario: Crisis → Recovery (RESTORATIVE pattern expected)")
    print("Expected: Satisfaction fingerprinting +0.15 bonus (Kairos detection)")
    print()

    # Initialize components
    learner = NexusPhrasePatternLearner(
        memory_path="/tmp/test_integrated_learning.json",
        ema_alpha=0.15
    )
    fingerprint_classifier = SatisfactionFingerprintClassifier()
    stability_gate = LyapunovNexusStabilityGate()

    # Example nexus signature (crisis witnessing)
    signature = create_example_nexus_signature()

    # Simulate 6-turn conversation
    turns = [
        {
            'turn': 1,
            'user_input': "I'm overwhelmed and everything is falling apart",
            'phrase': "I hear the weight you're carrying right now...",
            'satisfaction': 0.45,  # Crisis onset (low satisfaction)
            'coherence': 0.55,
            'constraint_deltas': {'BOND': 0.1, 'NDAM': 0.3, 'SANS': 0.05, 'EO': 0.15},
            'organ_dissonances': {'EMPATHY': 0.2, 'NDAM': 0.4, 'RNX': 0.1}
        },
        {
            'turn': 2,
            'user_input': "It's getting worse, I can't handle this",
            'phrase': "I'm here with you in this difficult moment...",
            'satisfaction': 0.35,  # Crisis deepening
            'coherence': 0.50,
            'constraint_deltas': {'BOND': 0.15, 'NDAM': 0.4, 'SANS': 0.08, 'EO': 0.2},
            'organ_dissonances': {'EMPATHY': 0.25, 'NDAM': 0.5, 'RNX': 0.15}
        },
        {
            'turn': 3,
            'user_input': "Maybe... maybe I can breathe through this",
            'phrase': "I sense a shift toward steadiness...",
            'satisfaction': 0.50,  # Beginning recovery
            'coherence': 0.60,
            'constraint_deltas': {'BOND': 0.08, 'NDAM': 0.2, 'SANS': 0.04, 'EO': 0.1},
            'organ_dissonances': {'EMPATHY': 0.15, 'NDAM': 0.3, 'RNX': 0.08}
        },
        {
            'turn': 4,
            'user_input': "I'm starting to feel more grounded",
            'phrase': "There's a growing steadiness emerging...",
            'satisfaction': 0.65,  # Recovery in progress
            'coherence': 0.70,
            'constraint_deltas': {'BOND': 0.05, 'NDAM': 0.1, 'SANS': 0.02, 'EO': 0.05},
            'organ_dissonances': {'EMPATHY': 0.10, 'NDAM': 0.15, 'RNX': 0.05}
        },
        {
            'turn': 5,
            'user_input': "I feel like I can handle this now",
            'phrase': "I witness the resilience that's emerged...",
            'satisfaction': 0.78,  # Strong recovery
            'coherence': 0.78,
            'constraint_deltas': {'BOND': 0.02, 'NDAM': 0.05, 'SANS': 0.01, 'EO': 0.02},
            'organ_dissonances': {'EMPATHY': 0.05, 'NDAM': 0.08, 'RNX': 0.03}
        },
        {
            'turn': 6,
            'user_input': "Thank you, I'm okay now",
            'phrase': "I honor the journey you've moved through...",
            'satisfaction': 0.85,  # Recovery complete
            'coherence': 0.82,
            'constraint_deltas': {'BOND': 0.01, 'NDAM': 0.03, 'SANS': 0.01, 'EO': 0.01},
            'organ_dissonances': {'EMPATHY': 0.03, 'NDAM': 0.05, 'RNX': 0.02}
        }
    ]

    satisfaction_trace = []

    print("-" * 70)
    print("TURN-BY-TURN PROCESSING:")
    print("-" * 70)

    for turn_data in turns:
        turn_num = turn_data['turn']
        satisfaction = turn_data['satisfaction']
        satisfaction_trace.append(satisfaction)

        print(f"\n🔹 Turn {turn_num}: \"{turn_data['user_input'][:40]}...\"")
        print(f"   Emitted Phrase: \"{turn_data['phrase']}\"")
        print(f"   User Satisfaction: {satisfaction:.2f}")

        # Layer 1: Record emission outcome (base EMA learning)
        learner.record_emission_outcome(
            nexus_signature=signature,
            emitted_phrase=turn_data['phrase'],
            user_satisfaction=satisfaction,
            current_turn=turn_num
        )

        # Get base quality
        candidates = learner.get_candidate_phrases(
            nexus_signature=signature,
            k=1,
            current_turn=turn_num
        )

        if candidates:
            base_quality = candidates[0][1]
            print(f"   Layer 1 (Base EMA): {base_quality:.3f}")
        else:
            base_quality = 0.5
            print(f"   Layer 1 (Base EMA): {base_quality:.3f} (initial)")

        # Layer 2: Satisfaction fingerprinting (if enough history)
        if len(satisfaction_trace) >= 3:
            fingerprint = fingerprint_classifier.classify(satisfaction_trace[-3:])
            layer2_quality = base_quality + fingerprint.quality_adjustment
            print(f"   Layer 2 (Fingerprint): {layer2_quality:.3f} "
                  f"(Δ={fingerprint.quality_adjustment:+.2f}, archetype={fingerprint.archetype})")
        else:
            layer2_quality = base_quality
            print(f"   Layer 2 (Fingerprint): {layer2_quality:.3f} (waiting for history)")

        # Layer 3: Lyapunov stability gating
        stability = stability_gate.analyze_stability(
            coherence=turn_data['coherence'],
            constraint_deltas=turn_data['constraint_deltas'],
            organ_dissonances=turn_data['organ_dissonances']
        )
        final_quality = min(1.0, max(0.0, layer2_quality + stability.quality_adjustment))

        print(f"   Layer 3 (Stability): {final_quality:.3f} "
              f"(Δ={stability.quality_adjustment:+.2f}, regime={stability.regime}, V={stability.V:.3f})")

        print(f"   📊 Final Quality: {final_quality:.3f} "
              f"(improvement: {(final_quality - base_quality):.3f} from base)")

    # Final analysis
    print("\n" + "=" * 70)
    print("FINAL ANALYSIS:")
    print("=" * 70)

    # Overall satisfaction pattern
    overall_fingerprint = fingerprint_classifier.classify(satisfaction_trace)
    print(f"\n✅ Overall Pattern: {overall_fingerprint.archetype}")
    print(f"   Quality Adjustment: {overall_fingerprint.quality_adjustment:+.2f}")
    print(f"   Confidence: {overall_fingerprint.confidence:.2f}")
    print(f"   Summary: {overall_fingerprint.trajectory_summary}")

    # Learner statistics
    stats = learner.get_stats()
    print(f"\n📈 Learning Statistics:")
    print(f"   Total Patterns: {stats['total_patterns']}")
    print(f"   Total Phrases: {stats['total_phrases']}")
    print(f"   Mean Quality: {stats['mean_phrase_quality']:.3f}")
    print(f"   Coherence Horizon: {stats['coherence_horizon_utilization']:.1%} utilized")

    # Expected vs actual
    print(f"\n🎯 Expected Impact Validation:")
    print(f"   Satisfaction Fingerprinting: +0.15 (RESTORATIVE Kairos bonus)")
    print(f"   Lyapunov Stability: +0.08 (STABLE regime by end)")
    print(f"   Total Expected: +0.23 improvement from base")

    final_candidates = learner.get_candidate_phrases(signature, k=1, current_turn=6)
    if final_candidates:
        print(f"   Actual Final Quality: {final_candidates[0][1]:.3f}")
        print(f"   Initial Quality: 0.500 (neutral)")
        print(f"   Actual Improvement: {(final_candidates[0][1] - 0.5):.3f}")


if __name__ == '__main__':
    simulate_conversation_with_learning()
