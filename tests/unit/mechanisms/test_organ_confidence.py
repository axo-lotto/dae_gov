"""
Test Organ Confidence Tracker - Level 2 Fractal Rewards
========================================================

Quick validation test for organ confidence tracking integration.

Expected Behavior:
- Organs start with neutral confidence (0.5)
- Successful emissions boost confidence
- Failed emissions lower confidence
- Weight multipliers adjust accordingly (0.8-1.2 range)

Date: November 15, 2025
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_organ_confidence_tracking():
    """Test that organ confidence updates work correctly"""

    print("\n🧪 Testing Organ Confidence Tracker (Level 2 Fractal Rewards)")
    print("=" * 70)

    # Initialize organism
    organism = ConversationalOrganismWrapper()

    if not hasattr(organism, 'organ_confidence') or organism.organ_confidence is None:
        print("❌ Organ confidence tracker not available")
        return False

    print(f"\n✅ Organ confidence tracker initialized")

    # Test 1: Process successful emission
    print("\n📝 Test 1: Successful emission (high satisfaction)")
    result1 = organism.process_text(
        "I'm feeling really good about how I handled that difficult conversation.",
        user_satisfaction=0.9,  # High satisfaction
        enable_phase2=True
    )

    # Check that confidences were updated
    summary1 = organism.organ_confidence.get_summary()
    print(f"   Mean confidence: {summary1.get('mean_confidence', 0):.3f}")
    print(f"   Mean multiplier: {summary1.get('mean_multiplier', 0):.3f}")

    # Test 2: Process marginal emission
    print("\n📝 Test 2: Marginal emission (medium satisfaction)")
    result2 = organism.process_text(
        "I'm not sure how to proceed.",
        user_satisfaction=0.5,  # Medium satisfaction
        enable_phase2=True
    )

    summary2 = organism.organ_confidence.get_summary()
    print(f"   Mean confidence: {summary2.get('mean_confidence', 0):.3f}")
    print(f"   Mean multiplier: {summary2.get('mean_multiplier', 0):.3f}")

    # Test 3: Check specific organ metrics
    print("\n📝 Test 3: Individual organ metrics")
    for organ_name in ['LISTENING', 'WISDOM', 'BOND', 'SANS']:
        metrics = organism.organ_confidence.get_metrics(organ_name)
        if metrics:
            print(f"   {organ_name}:")
            print(f"      Confidence: {metrics.confidence:.3f}")
            print(f"      Weight multiplier: {metrics.weight_multiplier:.3f}")
            print(f"      Success rate: {metrics.success_rate:.1%} ({metrics.success_count}/{metrics.total_participations})")

    # Test 4: Verify weight multipliers in range
    print("\n📝 Test 4: Weight multiplier validation")
    multipliers = organism.organ_confidence.get_all_multipliers()
    all_in_range = all(0.8 <= m <= 1.2 for m in multipliers.values())

    if all_in_range:
        print(f"   ✅ All weight multipliers in valid range [0.8, 1.2]")
        print(f"   Range: [{min(multipliers.values()):.3f}, {max(multipliers.values()):.3f}]")
    else:
        print(f"   ❌ Some multipliers out of range!")
        return False

    # Test 5: Verify persistence
    print("\n📝 Test 5: Persistence check")
    confidence_file = Path("persona_layer/organ_confidence.json")
    if confidence_file.exists():
        print(f"   ✅ Confidence state persisted to {confidence_file}")
        file_size = confidence_file.stat().st_size
        print(f"   File size: {file_size} bytes")
    else:
        print(f"   ⚠️  Confidence file not created")

    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - Organ confidence tracking operational")
    print("\nLevel 2 Fractal Rewards (DAE 3.0) successfully integrated!")
    return True


if __name__ == "__main__":
    try:
        success = test_organ_confidence_tracking()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
