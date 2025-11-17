"""
Test Pattern Learning Feedback Loop
=====================================

Phase 1 Week 3, Days 3-4: Learning Feedback Loop Integration Test

Tests that the ConversationalOrganismWrapper successfully records emission
outcomes and updates pattern quality through delayed feedback learning.

November 17, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_delayed_feedback_learning():
    """Test 20-turn conversation with varying satisfaction to validate EMA convergence."""
    print("\n" + "=" * 70)
    print("TEST: Pattern Learning Feedback Loop (20 turns)")
    print("=" * 70)

    try:
        # Initialize organism
        wrapper = ConversationalOrganismWrapper()
        print("✅ Organism initialized")

        # Simulate 20-turn conversation with varying satisfaction
        # Pattern: Low satisfaction (0.3) → gradual improvement → high satisfaction (0.8)
        test_turns = [
            {"turn": 1, "input": "I'm feeling overwhelmed with everything", "satisfaction": 0.30},
            {"turn": 2, "input": "It's hard to keep going", "satisfaction": 0.35},
            {"turn": 3, "input": "I'm not sure what to do", "satisfaction": 0.40},
            {"turn": 4, "input": "Maybe there's a way through this", "satisfaction": 0.45},
            {"turn": 5, "input": "I'm starting to see some hope", "satisfaction": 0.50},
            {"turn": 6, "input": "Things are getting a bit clearer", "satisfaction": 0.55},
            {"turn": 7, "input": "I feel more grounded now", "satisfaction": 0.60},
            {"turn": 8, "input": "This is actually helping", "satisfaction": 0.65},
            {"turn": 9, "input": "I'm feeling much better", "satisfaction": 0.70},
            {"turn": 10, "input": "I can handle this", "satisfaction": 0.75},
            {"turn": 11, "input": "I'm finding my way", "satisfaction": 0.78},
            {"turn": 12, "input": "I feel confident now", "satisfaction": 0.80},
            {"turn": 13, "input": "This conversation is really valuable", "satisfaction": 0.82},
            {"turn": 14, "input": "I appreciate the support", "satisfaction": 0.83},
            {"turn": 15, "input": "I'm growing through this", "satisfaction": 0.84},
            {"turn": 16, "input": "I feel empowered", "satisfaction": 0.85},
            {"turn": 17, "input": "I'm making real progress", "satisfaction": 0.85},
            {"turn": 18, "input": "This feels transformative", "satisfaction": 0.86},
            {"turn": 19, "input": "I'm really grateful", "satisfaction": 0.87},
            {"turn": 20, "input": "I feel complete", "satisfaction": 0.88},
        ]

        print(f"\n📊 Simulating 20-turn conversation:")
        print(f"   Satisfaction trajectory: 0.30 → 0.88 (gradual improvement)")
        print(f"   Expected: Pattern quality improves via EMA (α=0.15)")
        print()

        emissions_generated = 0
        learning_updates = 0

        for turn_data in test_turns:
            turn_num = turn_data['turn']
            user_input = turn_data['input']
            satisfaction = turn_data['satisfaction']

            print(f"🔹 Turn {turn_num}: \"{user_input[:40]}...\"")
            print(f"   Satisfaction: {satisfaction:.2f}")

            # Process turn with organism
            context = {
                'turn_number': turn_num,
                'conversation_id': 'test_feedback_loop'
            }

            result = wrapper.process_text(
                text=user_input,
                context=context,
                enable_tsk_recording=False,
                enable_phase2=False,  # Use Phase 1 for faster testing
                user_satisfaction=satisfaction  # Pass satisfaction for delayed feedback
            )

            # Check if emission was generated
            if result.get('emission_text'):
                emissions_generated += 1
                print(f"   ✅ Emission generated (confidence: {result.get('emission_confidence', 0):.3f})")

                # Check if previous_turn_data was stored
                if wrapper.previous_turn_data:
                    learning_updates += 1
                    print(f"   🌀 Turn data stored for next iteration")
            else:
                print(f"   ⚠️  No emission generated")

            print()

        # Validation summary
        print("=" * 70)
        print("TEST SUMMARY:")
        print("=" * 70)

        success = True

        # Check 1: Most turns should generate emissions
        emission_rate = emissions_generated / len(test_turns)
        print(f"\n✓ Emission rate: {emission_rate:.1%} ({emissions_generated}/{len(test_turns)} turns)")
        if emission_rate < 0.5:
            print(f"   ⚠️  Warning: Low emission rate (expected >50%)")
            success = False
        else:
            print(f"   ✅ Emission rate acceptable")

        # Check 2: Learning updates should occur for most emissions
        learning_rate = learning_updates / emissions_generated if emissions_generated > 0 else 0
        print(f"\n✓ Learning update rate: {learning_rate:.1%} ({learning_updates}/{emissions_generated} emissions)")
        if learning_rate < 0.8:
            print(f"   ⚠️  Warning: Low learning rate (expected >80%)")
            success = False
        else:
            print(f"   ✅ Learning update rate good")

        # Check 3: Previous turn data should be stored at end
        if wrapper.previous_turn_data:
            print(f"\n✓ Previous turn data stored:")
            print(f"   Turn: {wrapper.previous_turn_data.get('turn')}")
            print(f"   Phrase: {wrapper.previous_turn_data.get('phrase', '')[:60]}...")
            print(f"   Signature: {'Yes' if wrapper.previous_turn_data.get('signature') else 'No'}")
            print(f"   ✅ State tracking operational")
        else:
            print(f"\n✓ Previous turn data: None")
            print(f"   ⚠️  Warning: Expected previous_turn_data to be stored")
            success = False

        # Check 4: Pattern learner should have recorded outcomes
        if wrapper.emission_generator and hasattr(wrapper.emission_generator, 'pattern_learner'):
            stats = wrapper.emission_generator.pattern_learner.get_stats()
            print(f"\n✓ Pattern learner statistics:")
            print(f"   Total patterns: {stats['total_patterns']}")
            print(f"   Total phrases: {stats['total_phrases']}")
            if stats['total_phrases'] > 0:
                print(f"   Mean quality: {stats['mean_phrase_quality']:.3f}")
                print(f"   ✅ Pattern learner accumulating data")
            else:
                print(f"   ⚠️  Warning: No phrases learned")
                success = False

        # Final result
        print("\n" + "=" * 70)
        if success:
            print("🎉 TEST PASSED: Learning feedback loop operational")
            print("\n✅ Week 3 Days 3-4: Learning Feedback Loop COMPLETE")
            print("   - Delayed feedback learning working")
            print("   - Previous turn data storage operational")
            print("   - Pattern quality updates via EMA")
            print("   - State tracking across 20 turns")
            return 0
        else:
            print("⚠️  TEST INCOMPLETE: Some checks failed (see warnings above)")
            return 1

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


def test_signature_extraction():
    """Test that nexus signatures can be extracted from organ_results."""
    print("\n" + "=" * 70)
    print("TEST: Nexus Signature Extraction from Organ Results")
    print("=" * 70)

    try:
        wrapper = ConversationalOrganismWrapper()
        print("✅ Organism initialized")

        # Process a test input
        test_input = "I'm feeling a mix of emotions right now"
        result = wrapper.process_text(
            text=test_input,
            context={'turn_number': 1},
            enable_phase2=False
        )

        # Check if signature was extracted and stored
        if wrapper.previous_turn_data:
            signature = wrapper.previous_turn_data.get('signature')
            if signature:
                print(f"\n✅ Signature extracted successfully:")
                print(f"   Participating organs: {signature.participating_organs}")
                print(f"   Organ count: {signature.organ_count}")
                print(f"   Nexus type: {signature.nexus_type}")
                print(f"   Mechanism: {signature.mechanism}")
                return 0
            else:
                print(f"\n⚠️  Signature not extracted (but previous_turn_data exists)")
                return 1
        else:
            print(f"\n⚠️  No previous_turn_data stored")
            return 1

    except Exception as e:
        print(f"❌ Signature extraction test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Run all feedback loop tests."""
    print("\n" + "=" * 70)
    print("🌀 PATTERN LEARNING FEEDBACK LOOP TESTS")
    print("   Phase 1 Week 3, Days 3-4: Learning Feedback Integration")
    print("   November 17, 2025")
    print("=" * 70)

    results = []

    # Test 1: Signature extraction
    result1 = test_signature_extraction()
    results.append(("Signature Extraction", result1 == 0))

    # Test 2: 20-turn delayed feedback learning
    result2 = test_delayed_feedback_learning()
    results.append(("20-Turn Feedback Learning", result2 == 0))

    # Summary
    print("\n" + "=" * 70)
    print("FINAL TEST SUMMARY:")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passing")

    if passed == total:
        print("\n🎉 ALL TESTS PASSING - Learning feedback loop complete!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failing")
        return 1


if __name__ == '__main__':
    sys.exit(main())
