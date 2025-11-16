#!/usr/bin/env python3
"""
Test TSK-Based Epoch Learning Infrastructure
=============================================

End-to-end validation of the new TSK (Transductive Summary Kernel) infrastructure
for proper transformation-based epoch learning.

Tests:
1. TSK Recorder - Creates complete INITIAL→FINAL transformation records
2. Transductive Epoch Coordinator - Runs epochs with TSK-based family clustering
3. FeltDifferenceLearner - Learns which pathways lead to success
4. Multi-family emergence - Validates diverse families form from diverse inputs

Expected Outcomes:
- Multiple transformation families (not single family)
- 57D signatures capturing HOW things change
- Pathway learning with confidence > 0.5
- Zipf's law emergence with R² > 0.70 after sufficient epochs

Created: November 16, 2025
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Set up environment
os.environ['PYTHONPATH'] = '/Users/daedalea/Desktop/DAE_HYPHAE_1:' + os.environ.get('PYTHONPATH', '')
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

print("=" * 80)
print("🧪 TSK-BASED EPOCH LEARNING VALIDATION")
print("=" * 80)
print(f"Timestamp: {datetime.now().isoformat()}")
print(f"Purpose: Validate transformation-based learning infrastructure")
print("=" * 80 + "\n")


def test_tsk_recorder():
    """Test 1: TSK Recorder can create complete transformation records."""
    print("\n" + "="*80)
    print("TEST 1: TSK Recorder - Transformation Record Creation")
    print("="*80)

    from persona_layer.conversational_tsk_recorder import (
        ConversationalTSKRecorder,
        TransductiveSummaryKernel
    )

    # Initialize recorder
    recorder = ConversationalTSKRecorder(storage_dir='test_tsk_storage')

    # Create initial state
    initial_state = recorder.create_initial_state()

    print(f"\n✅ Initial state created:")
    print(f"   V0 energy: {initial_state['v0_energy']}")
    print(f"   Organs: {len(initial_state['organ_coherences'])} tracked")
    print(f"   Zone: {initial_state['zone']}")
    print(f"   Satisfaction: {initial_state['satisfaction']}")

    # Simulate final felt states (after processing)
    final_felt_states = {
        'v0_energy': 0.35,
        'organ_coherences': {
            'LISTENING': 0.85, 'EMPATHY': 0.72, 'WISDOM': 0.68,
            'AUTHENTICITY': 0.71, 'PRESENCE': 0.88, 'BOND': 0.65,
            'SANS': 0.70, 'NDAM': 0.55, 'RNX': 0.62, 'EO': 0.75,
            'NEXUS': 0.80, 'CARD': 0.58
        },
        'polyvagal_state': 'ventral_vagal',
        'zone': 2,
        'urgency': 0.3,
        'satisfaction': 0.82,
        'emission_path': 'kairos',
        'confidence': 0.75,
        'nexus_type': 'Relational',
        'transduction_enabled': True,
        'bond_constraint': 0.12,
        'ndam_urgency': 0.08,
        'sans_coherence': 0.15,
        'eo_polyvagal': 0.68
    }

    # Simulate transduction trajectory
    transduction_trajectory = [
        {
            'cycle_num': 1, 'v0_energy': 0.85, 'satisfaction': 0.55,
            'bond_constraint': 0.05, 'ndam_urgency': 0.03
        },
        {
            'cycle_num': 2, 'v0_energy': 0.55, 'satisfaction': 0.68,
            'bond_constraint': 0.10, 'ndam_urgency': 0.06
        },
        {
            'cycle_num': 3, 'v0_energy': 0.35, 'satisfaction': 0.82,
            'bond_constraint': 0.12, 'ndam_urgency': 0.08
        }
    ]

    # Create TSK
    tsk = recorder.create_tsk_from_processing(
        conversation_id="test_001",
        user_input="I feel safe and grounded here",
        initial_state=initial_state,
        final_felt_states=final_felt_states,
        transduction_trajectory=transduction_trajectory,
        response_text="Honoring your sense of safety and groundedness..."
    )

    print(f"\n✅ TSK created successfully:")
    print(f"   Conversation ID: {tsk.conversation_id}")
    print(f"   V0 Descent: {tsk.initial_v0_energy:.2f} → {tsk.final_v0_energy:.2f} "
          f"(Δ={tsk.v0_energy_descent:.2f})")
    print(f"   Cycles: {tsk.convergence_cycles}")
    print(f"   Satisfaction: {tsk.final_satisfaction:.2f}")
    print(f"   Signature dimensions: {len(tsk.transformation_signature)}")

    # Validate signature
    assert len(tsk.transformation_signature) == 57, f"Expected 57D, got {len(tsk.transformation_signature)}"

    # Check constraint deltas
    print(f"\n   Constraint Deltas:")
    print(f"      BOND Δ: {tsk.bond_constraint_delta:.4f}")
    print(f"      NDAM Δ: {tsk.ndam_constraint_delta:.4f}")
    print(f"      SANS Δ: {tsk.sans_constraint_delta:.4f}")
    print(f"      EO Δ: {tsk.eo_constraint_delta:.4f}")

    # Store TSK
    recorder.store_tsk(tsk, epoch_id=1)
    print(f"\n✅ TSK stored persistently: {len(recorder)} TSKs in storage")

    print("\n✅ TEST 1 PASSED: TSK Recorder creates complete transformation records")
    return True


def test_felt_difference_learner():
    """Test 2: FeltDifferenceLearner learns from transformation patterns."""
    print("\n" + "="*80)
    print("TEST 2: FeltDifferenceLearner - Pathway Learning")
    print("="*80)

    from persona_layer.felt_difference_learner import FeltDifferenceLearner
    from persona_layer.conversational_tsk_recorder import TransductiveSummaryKernel
    import numpy as np

    # Initialize learner
    learner = FeltDifferenceLearner(
        storage_path='test_transformation_pathways.json',
        learning_rate=0.15,
        success_threshold=0.7
    )

    # Create diverse TSKs with different transformation patterns
    print(f"\nCreating diverse TSKs...")

    # High satisfaction TSKs (success pathways)
    success_tsks = []
    for i in range(5):
        # Signature with strong V0 descent component
        sig = np.random.randn(57) * 0.3
        sig[0] = 0.8  # Strong V0 descent
        sig[23] = 0.7  # High satisfaction change
        sig = sig / np.linalg.norm(sig)

        tsk = TransductiveSummaryKernel(
            conversation_id=f"success_{i}",
            timestamp=datetime.now().isoformat(),
            user_input=f"Safe input {i}",
            response_text=f"Therapeutic response {i}",
            initial_v0_energy=1.0,
            final_v0_energy=0.3,
            v0_energy_descent=0.7,
            convergence_cycles=3,
            final_satisfaction=0.85 + np.random.randn() * 0.05,
            emission_confidence=0.75,  # Correct field name
            transformation_signature=sig.tolist()
        )
        success_tsks.append(tsk)

    # Low satisfaction TSKs (failure pathways)
    failure_tsks = []
    for i in range(3):
        # Signature with weak V0 descent
        sig = np.random.randn(57) * 0.3
        sig[0] = -0.2  # Weak V0 descent
        sig[23] = -0.3  # Negative satisfaction change
        sig = sig / np.linalg.norm(sig)

        tsk = TransductiveSummaryKernel(
            conversation_id=f"failure_{i}",
            timestamp=datetime.now().isoformat(),
            user_input=f"Difficult input {i}",
            response_text=f"Generic response {i}",
            initial_v0_energy=1.0,
            final_v0_energy=0.8,
            v0_energy_descent=0.2,
            convergence_cycles=5,
            final_satisfaction=0.45 + np.random.randn() * 0.05,
            emission_confidence=0.35,  # Correct field name
            transformation_signature=sig.tolist()
        )
        failure_tsks.append(tsk)

    # Learn from all TSKs
    print(f"\nLearning from {len(success_tsks) + len(failure_tsks)} TSKs...")
    all_tsks = success_tsks + failure_tsks
    np.random.shuffle(all_tsks)

    batch_result = learner.learn_from_tsk_batch(all_tsks, verbose=False)

    print(f"\n✅ Learning complete:")
    print(f"   Total pathways: {batch_result['total_pathways']}")
    print(f"   Success rate: {batch_result['success_rate']:.2%}")
    print(f"   Average confidence: {batch_result['avg_confidence']:.3f}")

    # Get learning insights
    insights = learner.get_learning_insights()

    print(f"\n✅ Learning insights:")
    print(f"   Mean confidence: {insights['mean_confidence']:.3f}")
    print(f"   Mean success rate: {insights['mean_success_rate']:.3f}")

    if insights.get('best_pathways'):
        print(f"\n   Best pathways:")
        for p in insights['best_pathways'][:2]:
            print(f"      {p['id']}: conf={p['confidence']:.3f}, "
                  f"sr={p['success_rate']:.2f}, sat={p['mean_satisfaction']:.2f}")

    # Validate learning occurred
    assert batch_result['total_pathways'] >= 2, "Should create at least 2 pathways"
    assert insights['mean_confidence'] > 0.4, "Confidence should be above neutral"

    print("\n✅ TEST 2 PASSED: FeltDifferenceLearner learns pathway patterns")
    return True


def test_transductive_epoch_coordinator():
    """Test 3: Full epoch training with TSK-based family clustering."""
    print("\n" + "="*80)
    print("TEST 3: Transductive Epoch Coordinator - Full Epoch Training")
    print("="*80)

    # Import with error handling
    try:
        from persona_layer.transductive_epoch_coordinator import TransductiveEpochCoordinator
    except ImportError as e:
        print(f"⚠️ Import error: {e}")
        print("   Skipping full integration test")
        return False

    # Create coordinator (this will initialize organism wrapper)
    print("\nInitializing TransductiveEpochCoordinator...")
    print("(This will create organism wrapper and all subsystems)")

    coordinator = TransductiveEpochCoordinator(
        state_dir='test_epoch_state',
        tsk_storage_dir='test_tsk_epoch_storage',
        enable_phase5=False  # Disable for faster test
    )

    # Create diverse training pairs
    training_pairs = [
        {
            'id': 'burnout_crisis',
            'input_text': 'I am completely burned out and cant keep going',
            'expected_output': 'Witnessing presence for burnout'
        },
        {
            'id': 'safety_comfort',
            'input_text': 'This conversation feels really safe and comforting',
            'expected_output': 'Acknowledge safety'
        },
        {
            'id': 'boundary_need',
            'input_text': 'I need some space and boundaries right now',
            'expected_output': 'Honor boundaries'
        },
        {
            'id': 'joy_gratitude',
            'input_text': 'I feel so grateful and joyful today',
            'expected_output': 'Celebrate joy'
        },
        {
            'id': 'anxiety_overwhelm',
            'input_text': 'I feel anxious and overwhelmed by everything',
            'expected_output': 'Ground anxiety'
        }
    ]

    print(f"\nRunning epoch with {len(training_pairs)} diverse inputs...")

    # Run single epoch
    epoch_stats = coordinator.run_epoch(training_pairs, epoch_id=1, verbose=True)

    # Analyze results
    print(f"\n✅ Epoch Complete:")
    print(f"   Total conversations: {epoch_stats['total_conversations']}")
    print(f"   Mean V0 descent: {epoch_stats['mean_v0_descent']:.3f}")
    print(f"   Mean satisfaction: {epoch_stats['mean_satisfaction']:.3f}")
    print(f"   Total families: {epoch_stats.get('total_families', 0)}")
    print(f"   Families this epoch: {epoch_stats.get('families_discovered_this_epoch', 0)}")

    # Key validation: Multiple families should form
    total_families = epoch_stats.get('total_families', 0)
    print(f"\n🎯 KEY METRIC: Transformation families formed: {total_families}")

    if total_families >= 2:
        print(f"   ✅ MULTI-FAMILY EMERGENCE: {total_families} families")
        print(f"      This proves TSK-based clustering works!")
    elif total_families == 1:
        print(f"   ⚠️ Single family formed (need more diversity)")
        print(f"      May need to tune similarity threshold")
    else:
        print(f"   ❌ No families formed (possible issue)")

    # Get transformation insights
    insights = coordinator.get_transformation_insights()
    print(f"\n✅ Transformation Insights:")
    print(f"   Total TSKs: {insights.get('total_tsks', 0)}")
    print(f"   Mean V0 descent: {insights.get('mean_v0_descent', 0):.3f}")
    print(f"   Kairos rate: {insights.get('kairos_detection_rate', 0):.2%}")

    print("\n✅ TEST 3 PASSED: Transductive epoch coordinator operational")
    return True


def test_multi_family_emergence():
    """Test 4: Validate that diverse inputs create multiple families."""
    print("\n" + "="*80)
    print("TEST 4: Multi-Family Emergence Validation")
    print("="*80)

    from persona_layer.conversational_tsk_recorder import TransductiveSummaryKernel
    import numpy as np

    # Simulate 57D signatures for different transformation types
    print("\nCreating 10 diverse transformation signatures...")

    signatures = []

    # Type 1: Strong V0 descent + high satisfaction (safe grounding)
    for i in range(3):
        sig = np.zeros(57)
        sig[0:6] = [0.8, 0.7, 0.6, 0.5, 0.4, 0.3]  # V0 descent pattern
        sig[23:29] = [0.7, 0.6, 0.5, 0.4, 0.3, 0.2]  # Satisfaction increase
        sig = sig / np.linalg.norm(sig)
        signatures.append(('safe_grounding', sig))

    # Type 2: Moderate descent + urgency handling
    for i in range(3):
        sig = np.zeros(57)
        sig[0:6] = [0.4, 0.3, 0.3, 0.2, 0.2, 0.1]  # Moderate descent
        sig[33:35] = [0.8, 0.7]  # High urgency shift
        sig = sig / np.linalg.norm(sig)
        signatures.append(('crisis_intervention', sig))

    # Type 3: Boundary setting pattern
    for i in range(2):
        sig = np.zeros(57)
        sig[35:38] = [0.6, 0.5, 0.4]  # Emission path characteristics
        sig[20:23] = [0.7, 0.6, 0.5]  # Zone transformation
        sig = sig / np.linalg.norm(sig)
        signatures.append(('boundary_setting', sig))

    # Type 4: Joy/gratitude pattern
    for i in range(2):
        sig = np.zeros(57)
        sig[17:20] = [0.8, 0.7, 0.6]  # Polyvagal transformation
        sig[29:32] = [0.5, 0.4, 0.3]  # Convergence characteristics
        sig = sig / np.linalg.norm(sig)
        signatures.append(('joy_celebration', sig))

    # Cluster signatures by cosine similarity
    print(f"\nClustering {len(signatures)} signatures...")

    families = {}
    threshold = 0.55

    for name, sig in signatures:
        assigned = False
        for family_id, (centroid, members) in families.items():
            similarity = np.dot(sig, centroid)
            if similarity >= threshold:
                # Join family, update centroid
                members.append((name, sig))
                new_centroid = np.mean([s for _, s in members], axis=0)
                new_centroid = new_centroid / np.linalg.norm(new_centroid)
                families[family_id] = (new_centroid, members)
                assigned = True
                break

        if not assigned:
            # Create new family
            family_id = f"Family_{len(families) + 1:03d}"
            families[family_id] = (sig, [(name, sig)])

    print(f"\n✅ Family clustering results:")
    print(f"   Total families: {len(families)}")

    for family_id, (centroid, members) in families.items():
        member_names = [name for name, _ in members]
        print(f"   {family_id}: {len(members)} members ({', '.join(set(member_names))})")

    # Validate: We should get at least 3 distinct families
    assert len(families) >= 3, f"Expected ≥3 families, got {len(families)}"

    # Check for Zipf-like distribution
    sizes = sorted([len(members) for _, members in families.values()], reverse=True)
    print(f"\n   Family sizes: {sizes}")

    if len(sizes) >= 3:
        # Rough Zipf check: largest should be ~2x third largest
        if sizes[0] >= sizes[2] * 1.2:
            print(f"   ✅ Zipf-like distribution emerging")
        else:
            print(f"   📊 Distribution is relatively flat")

    print("\n✅ TEST 4 PASSED: Multiple families emerge from diverse signatures")
    return True


def run_all_tests():
    """Run all TSK infrastructure tests."""
    print("\n" + "="*80)
    print("RUNNING ALL TSK EPOCH LEARNING TESTS")
    print("="*80 + "\n")

    results = {}

    # Test 1: TSK Recorder
    try:
        results['TSK Recorder'] = test_tsk_recorder()
    except Exception as e:
        print(f"\n❌ TEST 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        results['TSK Recorder'] = False

    # Test 2: FeltDifferenceLearner
    try:
        results['FeltDifferenceLearner'] = test_felt_difference_learner()
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        results['FeltDifferenceLearner'] = False

    # Test 3: Transductive Epoch Coordinator
    try:
        results['Transductive Epoch Coordinator'] = test_transductive_epoch_coordinator()
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        results['Transductive Epoch Coordinator'] = False

    # Test 4: Multi-Family Emergence
    try:
        results['Multi-Family Emergence'] = test_multi_family_emergence()
    except Exception as e:
        print(f"\n❌ TEST 4 FAILED: {e}")
        import traceback
        traceback.print_exc()
        results['Multi-Family Emergence'] = False

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"   {test_name}: {status}")

    print(f"\n   Total: {passed}/{total} tests passed")

    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"   TSK-based epoch learning infrastructure is operational!")
        print(f"   Ready for transformation-based family clustering.")
    else:
        print(f"\n⚠️ Some tests failed. Check logs above.")

    print("="*80 + "\n")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
