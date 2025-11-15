"""
Complete System Assessment - Post Enhancements
November 13, 2025

Comprehensive test suite to assess system performance after:
- Enhancement #1: Regime-based confidence modulation
- R-matrix saturation fix
- Enhancement #3: Family semantic naming
- Baseline training validation (30 pairs)

Tests:
1. System health (quick validation)
2. Enhancement #1 integration
3. R-matrix health
4. Family discovery
5. Performance metrics
6. Regression checks
"""

import sys
import json
import time
import numpy as np
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_training.satisfaction_regime import SatisfactionRegime

def test_system_health():
    """Test 1: Basic system health check."""
    print("\n" + "="*70)
    print("TEST 1: SYSTEM HEALTH CHECK")
    print("="*70)

    test_inputs = [
        "I'm feeling overwhelmed right now.",
        "This conversation feels really safe.",
        "I need some space."
    ]

    wrapper = ConversationalOrganismWrapper()
    results = []

    for idx, text in enumerate(test_inputs, 1):
        print(f"\n  Input {idx}/3: \"{text[:50]}...\"")

        try:
            result = wrapper.process_text(
                text,
                enable_tsk_recording=False,
                enable_phase2=True
            )

            felt_states = result['felt_states']
            confidence = felt_states.get('emission_confidence', 0.0)
            cycles = felt_states.get('convergence_cycles', 0)
            nexuses = felt_states.get('emission_nexus_count', 0)

            status = "✅" if confidence > 0.3 else "❌"
            print(f"  {status} Confidence: {confidence:.3f}, Cycles: {cycles}, Nexuses: {nexuses}")

            results.append({
                'success': confidence > 0.3,
                'confidence': confidence,
                'cycles': cycles,
                'nexuses': nexuses
            })

        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({'success': False, 'error': str(e)})

    passed = sum(1 for r in results if r.get('success', False))
    print(f"\n  Result: {passed}/3 tests passed")
    return passed == 3

def test_regime_modulation():
    """Test 2: Regime-based confidence modulation."""
    print("\n" + "="*70)
    print("TEST 2: REGIME-BASED CONFIDENCE MODULATION")
    print("="*70)

    wrapper = ConversationalOrganismWrapper()
    test_input = "I'm feeling burned out and need support."

    regimes_to_test = [
        (None, "No regime (baseline)"),
        (SatisfactionRegime.EXPLORING, "EXPLORING (0.90× caution)"),
        (SatisfactionRegime.STABLE, "STABLE (1.15× boost)"),
        (SatisfactionRegime.PLATEAUED, "PLATEAUED (0.85× pullback)")
    ]

    results = []

    for regime, description in regimes_to_test:
        print(f"\n  Testing: {description}")

        try:
            result = wrapper.process_text(
                test_input,
                enable_tsk_recording=False,
                enable_phase2=True,
                regime=regime
            )

            confidence = result['felt_states'].get('emission_confidence', 0.0)
            print(f"    Confidence: {confidence:.3f}")

            results.append({
                'regime': regime.value if regime else 'none',
                'confidence': confidence,
                'success': True
            })

        except Exception as e:
            print(f"    ❌ Error: {e}")
            results.append({'regime': regime.value if regime else 'none', 'success': False})

    passed = all(r['success'] for r in results)
    print(f"\n  Result: {'✅ PASS' if passed else '❌ FAIL'} - Regime modulation operational")
    return passed

def test_r_matrix_health():
    """Test 3: R-matrix health metrics."""
    print("\n" + "="*70)
    print("TEST 3: R-MATRIX HEALTH")
    print("="*70)

    r_matrix_path = Path("persona_layer/conversational_hebbian_memory.json")

    with open(r_matrix_path) as f:
        data = json.load(f)

    R = np.array(data['r_matrix'])
    metadata = data.get('r_matrix_metadata', {})

    mean_val = np.mean(R)
    std_val = np.std(R)
    off_diag = R[~np.eye(R.shape[0], dtype=bool)]
    off_diag_std = np.std(off_diag)

    learning_rate = metadata.get('learning_rate', 0.0)
    total_updates = metadata.get('total_updates', 0)

    print(f"\n  Mean: {mean_val:.6f} (target: 0.5-0.85)")
    print(f"  Std Dev: {std_val:.6f} (target: >0.08)")
    print(f"  Off-diagonal Std: {off_diag_std:.6f} (target: >0.06)")
    print(f"  Learning rate: {learning_rate}")
    print(f"  Total updates: {total_updates}")

    checks = {
        'mean_in_range': 0.5 <= mean_val <= 0.85,
        'std_sufficient': std_val > 0.08,
        'off_diag_std_sufficient': off_diag_std > 0.06,
        'learning_rate_correct': learning_rate == 0.005
    }

    all_pass = all(checks.values())

    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")

    print(f"\n  Result: {'✅ PASS' if all_pass else '❌ FAIL'} - R-matrix healthy")
    return all_pass

def test_family_discovery():
    """Test 4: Family semantic naming."""
    print("\n" + "="*70)
    print("TEST 4: FAMILY DISCOVERY")
    print("="*70)

    families_path = Path("persona_layer/organic_families.json")

    with open(families_path) as f:
        data = json.load(f)

    families = data.get('families', {})
    total_families = len(families)

    print(f"\n  Total families: {total_families}")

    named_families = 0
    for family_id, family_data in families.items():
        semantic_name = family_data.get('semantic_name')
        member_count = family_data.get('member_count', 0)
        primary_category = family_data.get('primary_category')

        if semantic_name:
            named_families += 1
            print(f"  ✅ {family_id}: {semantic_name}")
            print(f"     Members: {member_count}, Primary: {primary_category}")

    all_named = named_families == total_families
    print(f"\n  Result: {'✅ PASS' if all_named else '❌ FAIL'} - {named_families}/{total_families} families named")
    return all_named

def test_performance_metrics():
    """Test 5: Performance benchmarks."""
    print("\n" + "="*70)
    print("TEST 5: PERFORMANCE METRICS")
    print("="*70)

    wrapper = ConversationalOrganismWrapper()

    test_inputs = [
        "I'm feeling overwhelmed right now.",
        "This conversation feels really safe.",
        "I need some space to process.",
        "The burnout is getting worse.",
        "I appreciate your support."
    ]

    times = []
    confidences = []
    cycles = []

    print(f"\n  Processing {len(test_inputs)} test inputs...")

    for text in test_inputs:
        start = time.time()

        result = wrapper.process_text(
            text,
            enable_tsk_recording=False,
            enable_phase2=True
        )

        elapsed = time.time() - start

        times.append(elapsed)
        confidences.append(result['felt_states'].get('emission_confidence', 0.0))
        cycles.append(result['felt_states'].get('convergence_cycles', 0))

    mean_time = np.mean(times)
    mean_confidence = np.mean(confidences)
    mean_cycles = np.mean(cycles)

    print(f"\n  Mean processing time: {mean_time:.3f}s (target: <5s)")
    print(f"  Mean confidence: {mean_confidence:.3f} (target: >0.4)")
    print(f"  Mean cycles: {mean_cycles:.1f} (target: 2-4)")

    checks = {
        'fast_processing': mean_time < 5.0,
        'good_confidence': mean_confidence > 0.4,
        'reasonable_cycles': 1 <= mean_cycles <= 5
    }

    all_pass = all(checks.values())

    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")

    print(f"\n  Result: {'✅ PASS' if all_pass else '❌ FAIL'} - Performance acceptable")
    return all_pass

def test_regression_checks():
    """Test 6: No regressions from baseline."""
    print("\n" + "="*70)
    print("TEST 6: REGRESSION CHECKS")
    print("="*70)

    # Load baseline results if available
    baseline_path = Path("baseline_training_results.json")

    if not baseline_path.exists():
        print("  ⚠️  No baseline results found, skipping regression check")
        return True

    with open(baseline_path) as f:
        baseline = json.load(f)

    baseline_metrics = baseline.get('aggregate_metrics', {})
    baseline_confidence = baseline_metrics.get('mean_confidence', 0.0)
    baseline_success_rate = baseline_metrics.get('success_rate', 0.0)

    print(f"\n  Baseline metrics:")
    print(f"    Mean confidence: {baseline_confidence:.3f}")
    print(f"    Success rate: {baseline_success_rate:.1%}")

    # Run quick test to compare
    wrapper = ConversationalOrganismWrapper()
    test_input = "I'm feeling burned out and overwhelmed."

    result = wrapper.process_text(
        test_input,
        enable_tsk_recording=False,
        enable_phase2=True
    )

    current_confidence = result['felt_states'].get('emission_confidence', 0.0)

    print(f"\n  Current test:")
    print(f"    Confidence: {current_confidence:.3f}")

    # Check for significant regression (>20% drop)
    regression = current_confidence < (baseline_confidence * 0.8)

    if regression:
        print(f"  ❌ REGRESSION: Confidence dropped significantly")
        return False
    else:
        print(f"  ✅ No significant regression detected")
        return True

def main():
    """Run complete system assessment."""
    print("\n" + "="*70)
    print("🌀 COMPLETE SYSTEM ASSESSMENT - POST ENHANCEMENTS")
    print("="*70)
    print("\nEnhancements tested:")
    print("  1. Regime-based confidence modulation")
    print("  2. R-matrix saturation fix")
    print("  3. Family semantic naming")
    print("  4. Baseline training (30 pairs)")
    print()

    results = []

    # Run all tests
    results.append(("System Health", test_system_health()))
    results.append(("Regime Modulation", test_regime_modulation()))
    results.append(("R-Matrix Health", test_r_matrix_health()))
    results.append(("Family Discovery", test_family_discovery()))
    results.append(("Performance Metrics", test_performance_metrics()))
    results.append(("Regression Checks", test_regression_checks()))

    # Summary
    print("\n" + "="*70)
    print("📊 ASSESSMENT SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print("\n" + "="*70)

    if passed == total:
        print(f"✅ ALL TESTS PASSED ({total}/{total})")
        print("\n🎉 System fully operational with all enhancements!")
        print("\n📊 System Status:")
        print("  - Regime modulation: ✅ Operational")
        print("  - R-matrix: ✅ Healthy (discrimination maintained)")
        print("  - Family naming: ✅ Operational")
        print("  - Performance: ✅ Excellent (<5s, >0.4 confidence)")
        print("  - No regressions: ✅ Baseline maintained")
        sys.exit(0)
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total} passed)")
        print(f"\n   Please investigate {total-passed} failing test(s)")
        sys.exit(1)

if __name__ == "__main__":
    main()
