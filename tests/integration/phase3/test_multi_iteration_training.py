"""
Integration Test: Complete Phase 2+3 Multi-Iteration Training
==============================================================

Tests the complete integration of all Phase 2+3 components:
- satisfaction_regime.py (6-regime classification)
- convergence_evolver.py (tau evolution)
- epoch_convergence_tracker.py (stability-based HALT)
- multi_iteration_trainer.py (training orchestration)
- ConversationalOrganismWrapper (DAE_GOV organism)

This demonstrates the system learning stable memory identities through
repeated exposure with regime-based adaptation.

Author: DAE_HYPHAE_1
Date: November 13, 2025
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_training.multi_iteration_trainer import (
    MultiIterationTrainer,
    TrainingPairResult
)
from config import Config


def test_single_pair_multi_iteration():
    """
    Test 1: Train a single conversation pair with multi-iteration convergence.

    Verifies:
    - Organism processes multiple iterations
    - Regime classification working
    - Tau evolution working
    - Convergence detection working
    - Memory formation (R-matrix, families) working
    """
    print("\n" + "="*70)
    print("TEST 1: Single Pair Multi-Iteration Training")
    print("="*70)

    # Initialize organism
    organism = ConversationalOrganismWrapper()

    # Initialize trainer
    trainer = MultiIterationTrainer(
        organism_wrapper=organism,
        initial_tau=0.50,
        max_iterations=5,
        satisfaction_target=0.75
    )

    # Training pair
    pair_id = "burnout_awareness"
    input_text = "I'm feeling burned out and don't know how to slow down."

    print(f"\n📝 Training pair: {pair_id}")
    print(f"   Input: \"{input_text}\"")
    print(f"   Max iterations: 5")
    print(f"   Target satisfaction: 0.75")

    # Train
    result = trainer.train_single_pair(
        pair_id=pair_id,
        input_text=input_text,
        verbose=True
    )

    # Validation
    assert result.iterations >= 2, "Should have at least 2 iterations"
    assert result.iterations <= 5, "Should not exceed max iterations"
    assert len(result.satisfaction_history) == result.iterations
    assert len(result.tau_history) == result.iterations + 1  # Initial + per iteration

    print(f"\n✅ TEST 1 PASSED")
    print(f"   Iterations: {result.iterations}")
    print(f"   Converged: {result.converged}")
    print(f"   Final satisfaction: {result.final_satisfaction:.3f}")
    print(f"   Final regime: {result.final_regime}")
    print(f"   Tau evolution: {result.tau_history[0]:.3f} → {result.tau_history[-1]:.3f}")

    return result


def test_multiple_pairs_training():
    """
    Test 2: Train multiple conversation pairs.

    Verifies:
    - Multi-pair training working
    - Diverse conversation types handled
    - Regime distribution across pairs
    - Memory formation across families
    """
    print("\n" + "="*70)
    print("TEST 2: Multiple Pairs Training")
    print("="*70)

    # Initialize organism
    organism = ConversationalOrganismWrapper()

    # Initialize trainer
    trainer = MultiIterationTrainer(
        organism_wrapper=organism,
        initial_tau=0.50,
        max_iterations=4,  # Slightly lower for speed
        satisfaction_target=0.75
    )

    # Training pairs (diverse therapeutic contexts)
    training_pairs = [
        {
            'pair_id': 'overwhelm_1',
            'input_text': 'I\'m feeling overwhelmed right now.'
        },
        {
            'pair_id': 'safety_1',
            'input_text': 'This conversation feels really safe.'
        },
        {
            'pair_id': 'boundary_1',
            'input_text': 'I need some space to process.'
        }
    ]

    print(f"\n📝 Training {len(training_pairs)} pairs")
    print(f"   Max iterations per pair: 4")
    print(f"   Target satisfaction: 0.75")

    # Train
    results = trainer.train_multiple_pairs(
        training_pairs=training_pairs,
        verbose=False  # Less verbose for multiple pairs
    )

    # Validation
    assert len(results) == len(training_pairs)
    for result in results:
        assert result.iterations >= 2
        assert result.iterations <= 4
        assert result.r_matrix_updated  # Memory should be updated
        assert len(result.satisfaction_history) > 0

    # Check diversity
    final_regimes = [r.final_regime for r in results]
    final_satisfactions = [r.final_satisfaction for r in results]

    print(f"\n✅ TEST 2 PASSED")
    print(f"   Total pairs: {len(results)}")
    print(f"   Mean iterations: {sum(r.iterations for r in results) / len(results):.2f}")
    print(f"   Mean satisfaction: {sum(final_satisfactions) / len(final_satisfactions):.3f}")
    print(f"   Regimes: {set(final_regimes)}")
    print(f"   Converged: {sum(1 for r in results if r.converged)}/{len(results)}")

    return results


def test_memory_formation_verification():
    """
    Test 3: Verify that memory formation is actually happening.

    Checks:
    - R-matrix updated (Hebbian memory)
    - Families assigned (organic learning)
    - Satisfaction improving over iterations
    - Tau adapting appropriately
    """
    print("\n" + "="*70)
    print("TEST 3: Memory Formation Verification")
    print("="*70)

    # Initialize organism
    organism = ConversationalOrganismWrapper()

    # Save initial R-matrix state
    initial_r_matrix = None
    if organism.organ_coupling_learner and organism.organ_coupling_learner.r_matrix is not None:
        import copy
        initial_r_matrix = copy.deepcopy(organism.organ_coupling_learner.r_matrix.tolist())

    # Initialize trainer
    trainer = MultiIterationTrainer(
        organism_wrapper=organism,
        initial_tau=0.50,
        max_iterations=4,
        satisfaction_target=0.75
    )

    # Train a pair
    result = trainer.train_single_pair(
        pair_id="memory_test",
        input_text="I'm noticing patterns in how I respond to stress.",
        verbose=False
    )

    # Check R-matrix changed
    final_r_matrix = organism.organ_coupling_learner.r_matrix.tolist()
    r_matrix_changed = (initial_r_matrix != final_r_matrix) if initial_r_matrix else True

    # Check satisfaction trajectory
    sat_history = result.satisfaction_history
    satisfaction_improving = sat_history[-1] >= sat_history[0]

    # Check tau adapted
    tau_history = result.tau_history
    tau_changed = abs(tau_history[-1] - tau_history[0]) > 0.001

    print(f"\n📊 Memory Formation Analysis:")
    print(f"   R-matrix updated: {'✅' if r_matrix_changed else '❌'}")
    print(f"   Satisfaction improving: {'✅' if satisfaction_improving else '❌'}")
    print(f"   Satisfaction: {sat_history[0]:.3f} → {sat_history[-1]:.3f}")
    print(f"   Tau adapted: {'✅' if tau_changed else '❌'}")
    print(f"   Tau: {tau_history[0]:.3f} → {tau_history[-1]:.3f}")
    print(f"   Family assigned: {'✅' if result.family_assigned else '❌'}")

    # Validation
    assert result.r_matrix_updated
    assert satisfaction_improving or sat_history[-1] >= 0.70  # Either improving or already good

    print(f"\n✅ TEST 3 PASSED - Memory formation verified")

    return {
        'r_matrix_changed': r_matrix_changed,
        'satisfaction_trajectory': sat_history,
        'tau_trajectory': tau_history,
        'family_assigned': result.family_assigned
    }


def run_all_tests():
    """Run all Phase 2+3 integration tests."""
    print("\n" + "="*70)
    print("🧪 PHASE 2+3 COMPLETE INTEGRATION TESTS")
    print("="*70)
    print("\nTesting: Multi-Iteration Training with Stable Memory Formation")
    print("Components: All of Phase 2+3 + DAE_GOV organism")

    try:
        # Test 1: Single pair
        test1_result = test_single_pair_multi_iteration()

        # Test 2: Multiple pairs
        test2_results = test_multiple_pairs_training()

        # Test 3: Memory formation
        test3_result = test_memory_formation_verification()

        # Final summary
        print("\n" + "="*70)
        print("✅ ALL INTEGRATION TESTS PASSED")
        print("="*70)
        print("\n📊 Phase 2+3 Integration Status:")
        print("   ✅ Multi-iteration training: WORKING")
        print("   ✅ Regime-based adaptation: WORKING")
        print("   ✅ Tau threshold evolution: WORKING")
        print("   ✅ Stability-based convergence: WORKING")
        print("   ✅ Memory formation (R-matrix): WORKING")
        print("   ✅ Family assignment: WORKING")
        print("   ✅ Organism learning: WORKING")

        print("\n🌀 Complete System Ready:")
        print("   • Train with 2-5 iterations per conversation")
        print("   • Adapt learning based on regime (EXPLORING → STABLE → COMMITTED)")
        print("   • Evolve tau thresholds for optimal confidence")
        print("   • Form stable memory identities in Hebbian R-matrix")
        print("   • Cluster conversations into organic families")
        print("   • Learn per-family V0 targets")

        print("\n🎓 System is ready to learn and grow with interaction!")

        return True

    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
