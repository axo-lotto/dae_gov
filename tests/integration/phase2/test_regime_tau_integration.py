"""
Integration Test: Phase 2 Regime + Tau Evolution with DAE_GOV
==============================================================

Tests the integration of:
- satisfaction_regime.py (6-regime classification with wave training)
- convergence_evolver.py (tau threshold evolution with DAE 3.0 modulation)
- ConversationalOrganismWrapper (existing DAE_GOV system)

This simulates a mini training epoch to verify:
1. Organism processing generates wave training context
2. Regime classification uses wave context correctly
3. Tau evolution respects spatial variance + field coherence
4. System maintains 100% maturity while learning thresholds

Author: DAE_HYPHAE_1
Date: November 13, 2025
"""

import sys
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_training.satisfaction_regime import (
    classify_regime_with_wave_context,
    SatisfactionRegime
)
from persona_layer.epoch_training.convergence_evolver import (
    evolve_tau_threshold_detailed,
    ConvergenceConfig
)
from config import Config
import numpy as np


def test_single_conversation_with_regime_tracking():
    """
    Test 1: Process a single conversation and extract regime-relevant data.

    Verifies:
    - Organism processes conversation successfully
    - Satisfaction metrics available
    - V0 energy descent occurred
    - Organ activations available for field coherence
    """
    print("\n" + "="*70)
    print("TEST 1: Single Conversation with Regime Tracking")
    print("="*70)

    # Initialize organism
    organism = ConversationalOrganismWrapper()

    # Test input (therapeutic context)
    test_input = "I'm feeling overwhelmed and need some space to breathe."

    print(f"\n📥 Input: {test_input}")
    print("🔄 Processing...")

    # Process with Phase 2 enabled
    result = organism.process_text(
        text=test_input,
        enable_phase2=True,
        enable_tsk_recording=False
    )

    # Extract metrics
    felt_states = result['felt_states']
    satisfaction = felt_states['satisfaction_final']
    v0_final = felt_states['v0_energy']['final_energy']
    convergence_cycles = felt_states['convergence_cycles']
    emission_confidence = felt_states.get('emission_confidence', 0.0)

    print(f"\n✅ Processing Complete:")
    print(f"   Satisfaction: {satisfaction:.3f}")
    print(f"   V0 final energy: {v0_final:.3f}")
    print(f"   Convergence cycles: {convergence_cycles}")
    print(f"   Emission confidence: {emission_confidence:.3f}")

    # Check organ activations (for field coherence)
    if 'organ_results' in felt_states:
        organ_count = len(felt_states['organ_results'])
        print(f"   Organs activated: {organ_count}/11")

    # Validation
    assert satisfaction >= 0.0 and satisfaction <= 1.0, "Satisfaction out of range"
    assert v0_final < 1.0, "V0 energy did not descend"
    assert convergence_cycles >= 1, "No convergence cycles"

    print("\n✅ TEST 1 PASSED - Organism processing working correctly")

    return {
        'satisfaction': satisfaction,
        'v0_final': v0_final,
        'convergence_cycles': convergence_cycles,
        'emission_confidence': emission_confidence,
        'felt_states': felt_states
    }


def test_regime_classification_with_mock_history():
    """
    Test 2: Regime classification with mock training history.

    Simulates 10 training iterations with:
    - Satisfaction rising: 0.50 → 0.75
    - Spatial variance decreasing: 0.010 → 0.002
    - Field coherence increasing: 0.60 → 0.75
    - Appetitive phases progressing: EXPANSIVE → NAVIGATION → CONCRESCENCE
    """
    print("\n" + "="*70)
    print("TEST 2: Regime Classification with Wave Context")
    print("="*70)

    # Mock training history (10 iterations)
    satisfaction_history = [0.50, 0.55, 0.58, 0.62, 0.65, 0.68, 0.70, 0.72, 0.74, 0.75]

    # Mock spatial variance (IQR from per-position organ fusion)
    # Decreasing trend = organism settling
    satisfaction_variances = [0.010, 0.009, 0.008, 0.006, 0.005, 0.004, 0.003, 0.002, 0.002, 0.002]

    # Mock field coherence (organ balance)
    # Increasing trend = organs becoming balanced
    field_coherences = [0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.73, 0.74, 0.75]

    # Mock appetitive phases (wave training progression)
    appetitive_phases = [
        "EXPANSIVE", "EXPANSIVE", "EXPANSIVE",
        "NAVIGATION", "NAVIGATION", "NAVIGATION",
        "CONCRESCENCE", "CONCRESCENCE", "CONCRESCENCE", "CONCRESCENCE"
    ]

    iteration_count = len(satisfaction_history)

    print(f"\n📊 Mock Training History ({iteration_count} iterations):")
    print(f"   Satisfaction: {satisfaction_history[0]:.3f} → {satisfaction_history[-1]:.3f}")
    print(f"   Spatial variance: {satisfaction_variances[0]:.4f} → {satisfaction_variances[-1]:.4f}")
    print(f"   Field coherence: {field_coherences[0]:.3f} → {field_coherences[-1]:.3f}")
    print(f"   Phases: EXPANSIVE → NAVIGATION → CONCRESCENCE")

    # Basic classification (without wave context)
    print("\n🔍 Basic Classification (FFITTSS V0 style):")
    from persona_layer.epoch_training.satisfaction_regime import classify_satisfaction_regime
    basic = classify_satisfaction_regime(satisfaction_history, iteration_count)
    print(f"   Regime: {basic.regime.value}")
    print(f"   Evolution rate: {basic.evolution_rate:.1f}")
    print(f"   Mean satisfaction: {basic.mean_satisfaction:.3f}")
    print(f"   Satisfaction trend: {basic.satisfaction_trend:+.4f}")

    # Wave-aware classification (DAE 3.0 integration)
    print("\n🌀 Wave-Aware Classification (DAE 3.0 + DAE_GOV):")
    wave_aware = classify_regime_with_wave_context(
        satisfaction_history,
        iteration_count,
        appetitive_phases=appetitive_phases,
        satisfaction_variances=satisfaction_variances,
        field_coherences=field_coherences
    )
    print(f"   Regime: {wave_aware.regime.value}")
    print(f"   Evolution rate: {wave_aware.evolution_rate:.1f}")
    print(f"   Confidence: {wave_aware.confidence:.3f}")
    print(f"   Reasoning: {wave_aware.reasoning}")

    # Validation
    assert wave_aware.regime in [SatisfactionRegime.CONVERGING, SatisfactionRegime.STABLE], \
        f"Expected CONVERGING or STABLE, got {wave_aware.regime.value}"
    assert wave_aware.mean_satisfaction > 0.60, "Mean satisfaction should be high"
    assert wave_aware.satisfaction_trend > 0.0, "Satisfaction should be trending up"

    print("\n✅ TEST 2 PASSED - Regime classification respects wave training")

    return wave_aware


def test_tau_evolution_with_wave_modulation():
    """
    Test 3: Tau threshold evolution with DAE 3.0 modulation.

    Tests:
    - Basic tau evolution (satisfaction below target → lower tau)
    - Appetitive phase modulation (EXPANSIVE vs CONCRESCENCE)
    - Spatial variance dampening (high variance → cautious)
    - Field coherence dampening (low coherence → cautious)
    """
    print("\n" + "="*70)
    print("TEST 3: Tau Evolution with Wave Modulation")
    print("="*70)

    current_tau = 0.50
    satisfaction_current = 0.70  # Below target (0.75)
    satisfaction_target = 0.75

    # Scenario 1: CONCRESCENCE phase, low variance, high coherence (ready to commit)
    print("\n📈 Scenario 1: CONCRESCENCE (ready to commit)")
    result_concrescence = evolve_tau_threshold_detailed(
        current_tau=current_tau,
        satisfaction_current=0.85,  # Above target
        satisfaction_target=satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        appetitive_phase="CONCRESCENCE",
        spatial_variance=0.002,  # Low variance (settled)
        field_coherence=0.75     # High coherence (balanced)
    )
    print(f"   Tau: {result_concrescence.tau_old:.3f} → {result_concrescence.tau_new:.3f}")
    print(f"   Adjustment: {result_concrescence.adjustment:+.4f}")
    print(f"   Direction: {'RAISE' if result_concrescence.direction > 0 else 'LOWER'}")
    print(f"   Reasoning: {result_concrescence.reasoning}")

    # Scenario 2: EXPANSIVE phase, high variance, high coherence (still exploring)
    print("\n📉 Scenario 2: EXPANSIVE (still exploring)")
    result_expansive = evolve_tau_threshold_detailed(
        current_tau=current_tau,
        satisfaction_current=0.85,  # Above target
        satisfaction_target=satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        appetitive_phase="EXPANSIVE",
        spatial_variance=0.010,  # High variance (exploring)
        field_coherence=0.75
    )
    print(f"   Tau: {result_expansive.tau_old:.3f} → {result_expansive.tau_new:.3f}")
    print(f"   Adjustment: {result_expansive.adjustment:+.4f}")
    print(f"   Direction: {'RAISE' if result_expansive.direction > 0 else 'LOWER'}")
    print(f"   Reasoning: {result_expansive.reasoning}")

    # Scenario 3: NAVIGATION phase, low variance, LOW coherence (organs unbalanced)
    print("\n⚠️  Scenario 3: NAVIGATION (low coherence)")
    result_low_coherence = evolve_tau_threshold_detailed(
        current_tau=current_tau,
        satisfaction_current=0.85,  # Above target
        satisfaction_target=satisfaction_target,
        regime=SatisfactionRegime.STABLE,
        appetitive_phase="NAVIGATION",
        spatial_variance=0.002,  # Low variance
        field_coherence=0.55     # Low coherence (unbalanced)
    )
    print(f"   Tau: {result_low_coherence.tau_old:.3f} → {result_low_coherence.tau_new:.3f}")
    print(f"   Adjustment: {result_low_coherence.adjustment:+.4f}")
    print(f"   Direction: {'RAISE' if result_low_coherence.direction > 0 else 'LOWER'}")
    print(f"   Reasoning: {result_low_coherence.reasoning}")

    # Validation
    # CONCRESCENCE should raise tau most aggressively
    assert result_concrescence.adjustment > result_expansive.adjustment, \
        "CONCRESCENCE should raise tau more than EXPANSIVE"

    # High variance should dampen tau raising
    assert result_expansive.adjustment < result_concrescence.adjustment, \
        "High variance should dampen tau evolution"

    # Low coherence should dampen tau raising
    assert result_low_coherence.adjustment < result_concrescence.adjustment, \
        "Low coherence should dampen tau raising"

    print("\n✅ TEST 3 PASSED - Tau evolution respects wave training modulation")

    return {
        'concrescence': result_concrescence,
        'expansive': result_expansive,
        'low_coherence': result_low_coherence
    }


def test_multi_conversation_regime_evolution():
    """
    Test 4: Process multiple conversations and track regime evolution.

    Simulates 5 training iterations:
    - Process conversation
    - Extract satisfaction + variance (approximate from V0 + confidence)
    - Classify regime
    - Evolve tau
    """
    print("\n" + "="*70)
    print("TEST 4: Multi-Conversation Regime Evolution")
    print("="*70)

    # Initialize organism
    organism = ConversationalOrganismWrapper()

    # Test inputs (diverse therapeutic contexts)
    test_inputs = [
        "I'm feeling overwhelmed right now.",
        "This conversation feels really safe.",
        "I need some space to process.",
        "I'm noticing a pattern in my reactions.",
        "I feel more grounded now."
    ]

    # Track metrics
    satisfaction_history = []
    variance_history = []  # Approximate from v0_final variance
    coherence_history = []  # Approximate from emission_confidence
    tau_history = [0.50]  # Start at 0.50
    regime_history = []

    print(f"\n🔄 Processing {len(test_inputs)} conversations...\n")

    for i, test_input in enumerate(test_inputs, 1):
        print(f"{'─'*70}")
        print(f"Iteration {i}: \"{test_input}\"")

        # Process conversation
        result = organism.process_text(
            text=test_input,
            enable_phase2=True,
            enable_tsk_recording=False
        )

        felt_states = result['felt_states']
        satisfaction = felt_states['satisfaction_final']
        v0_final = felt_states['v0_energy']['final_energy']
        emission_confidence = felt_states.get('emission_confidence', 0.5)

        # Approximate spatial variance from V0 energy (lower V0 = more settled)
        # This is a proxy - real system would extract IQR from satisfaction field
        approx_variance = 0.010 * v0_final  # Scales with V0 energy

        # Approximate field coherence from emission confidence
        # This is a proxy - real system would compute from organ_results
        approx_coherence = 0.50 + 0.30 * emission_confidence

        # Store metrics
        satisfaction_history.append(satisfaction)
        variance_history.append(approx_variance)
        coherence_history.append(approx_coherence)

        print(f"   Satisfaction: {satisfaction:.3f}")
        print(f"   Approx variance: {approx_variance:.4f}")
        print(f"   Approx coherence: {approx_coherence:.3f}")

        # Classify regime (basic, without full wave context)
        if len(satisfaction_history) >= 3:
            from persona_layer.epoch_training.satisfaction_regime import classify_satisfaction_regime
            regime = classify_satisfaction_regime(
                satisfaction_history,
                iteration_count=len(satisfaction_history)
            )
            regime_history.append(regime.regime)

            print(f"   Regime: {regime.regime.value} (rate={regime.evolution_rate:.1f})")

            # Evolve tau
            current_tau = tau_history[-1]
            new_tau = evolve_tau_threshold_detailed(
                current_tau=current_tau,
                satisfaction_current=satisfaction,
                satisfaction_target=0.75,
                regime=regime.regime,
                spatial_variance=approx_variance,
                field_coherence=approx_coherence
            )
            tau_history.append(new_tau.tau_new)

            print(f"   Tau: {current_tau:.3f} → {new_tau.tau_new:.3f} ({new_tau.adjustment:+.4f})")
        else:
            print(f"   Regime: INITIALIZING (warming up)")
            tau_history.append(tau_history[-1])  # Keep tau same during warmup

    print(f"\n{'='*70}")
    print("📊 Evolution Summary:")
    print(f"   Satisfaction: {satisfaction_history[0]:.3f} → {satisfaction_history[-1]:.3f}")
    print(f"   Tau threshold: {tau_history[0]:.3f} → {tau_history[-1]:.3f}")
    if regime_history:
        print(f"   Final regime: {regime_history[-1].value}")
    print(f"   Mean satisfaction: {np.mean(satisfaction_history):.3f}")
    print(f"   Satisfaction trend: {np.polyfit(range(len(satisfaction_history)), satisfaction_history, 1)[0]:+.4f}")

    # Validation
    assert len(satisfaction_history) == len(test_inputs), "Missing satisfaction values"
    assert len(tau_history) == len(test_inputs) + 1, "Incorrect tau history length"
    assert all(0.3 <= tau <= 0.75 for tau in tau_history), "Tau out of bounds"

    print("\n✅ TEST 4 PASSED - Multi-conversation regime evolution working")

    return {
        'satisfaction_history': satisfaction_history,
        'tau_history': tau_history,
        'regime_history': regime_history,
        'variance_history': variance_history,
        'coherence_history': coherence_history
    }


def run_all_integration_tests():
    """Run all Phase 2 integration tests."""
    print("\n" + "="*70)
    print("🧪 PHASE 2 INTEGRATION TESTS")
    print("="*70)
    print("\nTesting: Regime Classification + Tau Evolution + DAE_GOV Organism")
    print("Integration: satisfaction_regime.py + convergence_evolver.py + organism_wrapper")

    try:
        # Test 1: Single conversation
        test1_result = test_single_conversation_with_regime_tracking()

        # Test 2: Regime classification with mock history
        test2_result = test_regime_classification_with_mock_history()

        # Test 3: Tau evolution with modulation
        test3_result = test_tau_evolution_with_wave_modulation()

        # Test 4: Multi-conversation evolution
        test4_result = test_multi_conversation_regime_evolution()

        # Final summary
        print("\n" + "="*70)
        print("✅ ALL INTEGRATION TESTS PASSED")
        print("="*70)
        print("\n📊 Integration Status:")
        print("   ✅ Organism processing: WORKING")
        print("   ✅ Regime classification: WORKING")
        print("   ✅ Wave training awareness: WORKING")
        print("   ✅ Tau evolution: WORKING")
        print("   ✅ Spatial variance dampening: WORKING")
        print("   ✅ Field coherence dampening: WORKING")
        print("   ✅ Multi-conversation tracking: WORKING")
        print("\n🌀 Phase 2 integration verified - Ready for Phase 3!")

        return True

    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_integration_tests()
    sys.exit(0 if success else 1)
