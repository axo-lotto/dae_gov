"""
Test Entity Horizon - Morpheable Memory Boundary
=================================================

Validates EntityHorizon class behavior across coherence spectrum.

Expected Results:
- Low coherence (0.3): 100 entities (focus on recent)
- Medium coherence (0.5-0.7): 100-500 (linear interpolation)
- High coherence (0.7+): 500 entities (deep memory)

Author: DAE_HYPHAE_1 + Claude Code
Date: November 17, 2025
"""

from persona_layer.entity_horizon import EntityHorizon, HorizonMetrics


def test_horizon_boundaries():
    """Test horizon size computation at key boundaries."""
    print("="*80)
    print("TEST 1: Horizon Size Boundaries")
    print("="*80)

    horizon = EntityHorizon()

    test_cases = [
        (0.0, 100, "Zero coherence"),
        (0.2, 100, "Below minimum threshold"),
        (0.3, 100, "Minimum threshold (NEXUS τ_recall)"),
        (0.5, 100, "Medium baseline"),
        (0.6, 300, "Medium-high (interpolated)"),
        (0.7, 500, "High threshold"),
        (0.85, 500, "Very high"),
        (1.0, 500, "Perfect coherence"),
    ]

    passed = 0
    for coherence, expected_size, description in test_cases:
        actual_size = horizon.compute_horizon_size(coherence)
        status = "✅" if actual_size == expected_size else "❌"
        print(f"  {status} Coherence {coherence:.2f} ({description})")
        print(f"      Expected: {expected_size}, Actual: {actual_size}")

        if actual_size == expected_size:
            passed += 1

    print(f"\n  Result: {passed}/{len(test_cases)} tests passed\n")
    return passed == len(test_cases)


def test_query_limits():
    """Test query limit computation."""
    print("="*80)
    print("TEST 2: Query Limit Computation")
    print("="*80)

    horizon = EntityHorizon()

    test_cases = [
        (100, 50, 33, "Minimum horizon"),
        (200, 100, 66, "Small horizon"),
        (300, 150, 100, "Medium horizon"),
        (500, 250, 150, "Maximum horizon"),
    ]

    passed = 0
    for horizon_size, expected_recent, expected_fuzzy, description in test_cases:
        recent, fuzzy = horizon.compute_query_limits(horizon_size)
        status = "✅" if recent == expected_recent and fuzzy == expected_fuzzy else "❌"
        print(f"  {status} Horizon {horizon_size} ({description})")
        print(f"      Recent limit: {recent} (expected {expected_recent})")
        print(f"      Fuzzy limit: {fuzzy} (expected {expected_fuzzy})")
        print(f"      Session reserve: {horizon_size - recent - fuzzy}")

        if recent == expected_recent and fuzzy == expected_fuzzy:
            passed += 1

    print(f"\n  Result: {passed}/{len(test_cases)} tests passed\n")
    return passed == len(test_cases)


def test_adaptive_horizon():
    """Test complete adaptive horizon computation."""
    print("="*80)
    print("TEST 3: Adaptive Horizon Computation")
    print("="*80)

    horizon = EntityHorizon()

    # Test scenarios matching DAE 3.0 coherence tiers
    scenarios = [
        {
            'coherence': 0.85,
            'tier': 'high',
            'total_available': 1000,
            'description': 'High coherence conversation'
        },
        {
            'coherence': 0.60,
            'tier': 'medium',
            'total_available': 500,
            'description': 'Medium coherence conversation'
        },
        {
            'coherence': 0.35,
            'tier': 'low',
            'total_available': 200,
            'description': 'Low coherence conversation'
        },
    ]

    for scenario in scenarios:
        print(f"\n  Scenario: {scenario['description']}")
        print(f"  Field coherence: {scenario['coherence']:.2f}")

        metrics = horizon.compute_adaptive_horizon(
            field_coherence=scenario['coherence'],
            total_entities_available=scenario['total_available']
        )

        print(f"  ✅ Horizon size: {metrics.horizon_size}")
        print(f"  ✅ Recent limit: {metrics.recent_limit}")
        print(f"  ✅ Fuzzy limit: {metrics.fuzzy_limit}")
        print(f"  ✅ Coherence tier: {horizon.get_coherence_tier(scenario['coherence'])}")
        print(f"  ✅ Retrieval gated: {'No' if horizon.should_gate_retrieval(scenario['coherence']) else 'Yes'}")

        # Verify tier matches expectation
        actual_tier = horizon.get_coherence_tier(scenario['coherence'])
        assert actual_tier == scenario['tier'], f"Tier mismatch: {actual_tier} != {scenario['tier']}"

    print(f"\n  ✅ All scenarios computed successfully\n")
    return True


def test_coherence_gating():
    """Test coherence-based retrieval gating."""
    print("="*80)
    print("TEST 4: Coherence Gating (NEXUS τ_recall pattern)")
    print("="*80)

    horizon = EntityHorizon()

    test_cases = [
        (0.0, False, "Zero coherence → gate"),
        (0.2, False, "Below threshold → gate"),
        (0.3, True, "At threshold → allow"),
        (0.5, True, "Medium → allow"),
        (0.7, True, "High → allow"),
    ]

    passed = 0
    for coherence, should_retrieve, description in test_cases:
        actual = horizon.should_gate_retrieval(coherence)
        status = "✅" if actual == should_retrieve else "❌"
        action = "RETRIEVE" if actual else "GATE"
        print(f"  {status} Coherence {coherence:.2f}: {action} ({description})")

        if actual == should_retrieve:
            passed += 1

    print(f"\n  Result: {passed}/{len(test_cases)} tests passed\n")
    return passed == len(test_cases)


def test_utilization_tracking():
    """Test horizon utilization tracking."""
    print("="*80)
    print("TEST 5: Horizon Utilization Tracking")
    print("="*80)

    horizon = EntityHorizon()

    # Compute horizon
    metrics = horizon.compute_adaptive_horizon(field_coherence=0.65)
    print(f"  Computed horizon: {metrics.horizon_size} entities")

    # Simulate retrieval
    entities_retrieved = 150
    horizon.update_retrieval_stats(entities_retrieved)

    # Check tracking
    assert horizon.last_metrics is not None
    assert horizon.last_metrics.entities_retrieved == entities_retrieved

    utilization = horizon.last_metrics.horizon_utilization
    expected_utilization = entities_retrieved / metrics.horizon_size

    print(f"  ✅ Entities retrieved: {entities_retrieved}")
    print(f"  ✅ Horizon utilization: {utilization*100:.1f}%")
    print(f"  ✅ Expected: {expected_utilization*100:.1f}%")

    assert abs(utilization - expected_utilization) < 0.01, "Utilization mismatch"

    print(f"\n  ✅ Utilization tracking validated\n")
    return True


def test_morphing_behavior():
    """Test that horizon actually morphs with coherence."""
    print("="*80)
    print("TEST 6: Morphing Behavior (Adaptive Depth)")
    print("="*80)

    horizon = EntityHorizon()

    print("\n  Simulating conversation with increasing coherence:\n")

    coherence_progression = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    previous_size = 0

    for i, coherence in enumerate(coherence_progression, 1):
        size = horizon.compute_horizon_size(coherence)
        recent, fuzzy = horizon.compute_query_limits(size)

        change = "↑" if size > previous_size else ("↓" if size < previous_size else "→")
        print(f"  Turn {i}: coherence={coherence:.2f} → horizon={size} {change}")
        print(f"          (recent={recent}, fuzzy={fuzzy})")

        # Verify monotonic increase
        if i > 1:
            assert size >= previous_size, f"Horizon should not shrink with increasing coherence"

        previous_size = size

    print(f"\n  ✅ Horizon morphs correctly with coherence\n")
    return True


def main():
    """Run all entity horizon tests."""
    print("\n" + "="*80)
    print("🌀 ENTITY HORIZON VALIDATION")
    print("="*80)
    print("Testing morpheable memory boundary (FFITTSS-inspired)")
    print("="*80 + "\n")

    tests = [
        ("Horizon Boundaries", test_horizon_boundaries),
        ("Query Limits", test_query_limits),
        ("Adaptive Horizon", test_adaptive_horizon),
        ("Coherence Gating", test_coherence_gating),
        ("Utilization Tracking", test_utilization_tracking),
        ("Morphing Behavior", test_morphing_behavior),
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}\n")

    # Summary
    print("="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"  Tests passed: {passed}/{total}")
    print(f"  Success rate: {passed/total*100:.1f}%")

    if passed == total:
        print(f"\n  ✅ All tests PASSED - EntityHorizon validated!\n")
    else:
        print(f"\n  ⚠️  Some tests failed - review output above\n")

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
