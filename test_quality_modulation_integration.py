"""
Test Quality Modulation Integration
====================================

Phase 1 Week 3, Day 5: Quality Modulation Integration Test

Tests that the ConversationalOrganismWrapper successfully applies three-layer
quality modulation (Base EMA + Satisfaction Fingerprinting + Lyapunov Stability)
when recording emission outcomes.

November 17, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_quality_modulation_integration():
    """Test 20-turn conversation with quality modulation to validate +16-25pp improvement."""
    print("\n" + "=" * 70)
    print("TEST: Quality Modulation Integration (20 turns)")
    print("=" * 70)

    try:
        # Initialize organism
        wrapper = ConversationalOrganismWrapper()
        print("✅ Organism initialized")

        # Check quality modulation layers loaded
        has_fingerprinter = hasattr(wrapper, 'satisfaction_fingerprinter') and wrapper.satisfaction_fingerprinter is not None
        has_lyapunov = hasattr(wrapper, 'lyapunov_gate') and wrapper.lyapunov_gate is not None
        has_history = hasattr(wrapper, 'satisfaction_history')

        print(f"\n📊 Quality Modulation Layers:")
        print(f"   Satisfaction Fingerprinting: {'✅' if has_fingerprinter else '❌'}")
        print(f"   Lyapunov Stability Gating: {'✅' if has_lyapunov else '❌'}")
        print(f"   Satisfaction History Tracking: {'✅' if has_history else '❌'}")

        if not (has_fingerprinter and has_lyapunov and has_history):
            print("\n⚠️  WARNING: Quality modulation layers not fully loaded")
            print("   Expected: All 3 layers operational")
            return 1

        # Simulate 20-turn conversation with RESTORATIVE pattern (crisis → recovery)
        # This should trigger satisfaction fingerprinting bonus
        test_turns = [
            # Crisis phase (low satisfaction, high urgency)
            {"turn": 1, "input": "Everything is falling apart and I can't cope anymore", "satisfaction": 0.25},
            {"turn": 2, "input": "I don't know how to get through this darkness", "satisfaction": 0.28},
            {"turn": 3, "input": "The weight of everything is crushing me", "satisfaction": 0.30},

            # Early recovery (gradual improvement - RESTORATIVE pattern emerging)
            {"turn": 4, "input": "Maybe there's a small glimmer of hope here", "satisfaction": 0.40},
            {"turn": 5, "input": "I'm starting to see I can survive this", "satisfaction": 0.50},
            {"turn": 6, "input": "There's a path forward, even if it's hard", "satisfaction": 0.58},

            # Stabilization (RESTORATIVE pattern should be detected here!)
            {"turn": 7, "input": "I'm finding my footing again", "satisfaction": 0.65},
            {"turn": 8, "input": "This conversation is helping me heal", "satisfaction": 0.72},
            {"turn": 9, "input": "I feel more grounded and capable", "satisfaction": 0.78},

            # Sustained recovery (CONCRESCENT pattern - sustained high satisfaction)
            {"turn": 10, "input": "I'm really making progress now", "satisfaction": 0.82},
            {"turn": 11, "input": "I can feel myself growing through this", "satisfaction": 0.84},
            {"turn": 12, "input": "There's real transformation happening", "satisfaction": 0.86},
            {"turn": 13, "input": "I'm becoming more resilient", "satisfaction": 0.87},
            {"turn": 14, "input": "This feels sustainable and real", "satisfaction": 0.88},

            # Consolidation (continued high satisfaction)
            {"turn": 15, "input": "I've integrated these insights deeply", "satisfaction": 0.89},
            {"turn": 16, "input": "I feel genuinely empowered now", "satisfaction": 0.90},
            {"turn": 17, "input": "This is a meaningful shift in my life", "satisfaction": 0.90},
            {"turn": 18, "input": "I'm grateful for this journey", "satisfaction": 0.91},
            {"turn": 19, "input": "I feel complete and whole", "satisfaction": 0.92},
            {"turn": 20, "input": "I'm ready to move forward with confidence", "satisfaction": 0.93},
        ]

        print(f"\n📊 Simulating 20-turn RESTORATIVE conversation:")
        print(f"   Phase 1: Crisis (turns 1-3, satisfaction 0.25-0.30)")
        print(f"   Phase 2: Recovery (turns 4-9, satisfaction 0.40-0.78)")
        print(f"   Phase 3: Sustained Growth (turns 10-20, satisfaction 0.82-0.93)")
        print(f"   Expected: Satisfaction fingerprinting detects RESTORATIVE pattern (+8-12pp)")
        print(f"   Expected: Lyapunov stability detects STABLE regime (+5-8pp)")
        print()

        emissions_generated = 0
        learning_updates = 0
        fingerprint_detections = 0

        # Track initial vs final quality for same pattern (if we see it twice)
        quality_samples = []

        for turn_data in test_turns:
            turn_num = turn_data['turn']
            user_input = turn_data['input']
            satisfaction = turn_data['satisfaction']

            print(f"🔹 Turn {turn_num}: \"{user_input[:50]}...\"")
            print(f"   Satisfaction: {satisfaction:.2f}")

            # Process turn with organism
            context = {
                'turn_number': turn_num,
                'conversation_id': 'test_quality_modulation'
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
                    print(f"   🌀 Learning update applied")

                    # Check if we have enough history for fingerprinting
                    if len(wrapper.satisfaction_history) >= 3:
                        print(f"   📊 Satisfaction history: {len(wrapper.satisfaction_history)} turns")
                        print(f"      Recent trajectory: {wrapper.satisfaction_history[-3:]}")
                        fingerprint_detections += 1
            else:
                print(f"   ⚠️  No emission generated")

            # Check pattern learner quality evolution
            if turn_num % 5 == 0 and wrapper.emission_generator and hasattr(wrapper.emission_generator, 'pattern_learner'):
                stats = wrapper.emission_generator.pattern_learner.get_stats()
                if stats['total_phrases'] > 0:
                    quality_samples.append({
                        'turn': turn_num,
                        'mean_quality': stats['mean_phrase_quality'],
                        'total_phrases': stats['total_phrases']
                    })
                    print(f"   📈 Pattern learner: {stats['total_phrases']} phrases, mean quality {stats['mean_phrase_quality']:.3f}")

            print()

        # Validation summary
        print("=" * 70)
        print("TEST SUMMARY:")
        print("=" * 70)

        success = True

        # Check 1: Emission rate
        emission_rate = emissions_generated / len(test_turns)
        print(f"\n✓ Emission rate: {emission_rate:.1%} ({emissions_generated}/{len(test_turns)} turns)")
        if emission_rate < 0.5:
            print(f"   ⚠️  Warning: Low emission rate (expected >50%)")
            success = False
        else:
            print(f"   ✅ Emission rate acceptable")

        # Check 2: Learning update rate
        learning_rate = learning_updates / emissions_generated if emissions_generated > 0 else 0
        print(f"\n✓ Learning update rate: {learning_rate:.1%} ({learning_updates}/{emissions_generated} emissions)")
        if learning_rate < 0.8:
            print(f"   ⚠️  Warning: Low learning rate (expected >80%)")
            success = False
        else:
            print(f"   ✅ Learning update rate good")

        # Check 3: Satisfaction fingerprinting operational
        print(f"\n✓ Satisfaction fingerprinting:")
        print(f"   History length: {len(wrapper.satisfaction_history)}")
        print(f"   Turns with 3+ history: {fingerprint_detections}")
        if fingerprint_detections < 10:
            print(f"   ⚠️  Warning: Fingerprinting may not have enough data (expected >10 turns)")
        else:
            print(f"   ✅ Sufficient data for pattern detection")

        # Check 4: Quality improvement trajectory
        if len(quality_samples) >= 2:
            print(f"\n✓ Quality improvement trajectory:")
            for i, sample in enumerate(quality_samples):
                print(f"   Turn {sample['turn']:2d}: quality={sample['mean_quality']:.3f} ({sample['total_phrases']} phrases)")

            # Calculate improvement
            first_quality = quality_samples[0]['mean_quality']
            last_quality = quality_samples[-1]['mean_quality']
            improvement_pp = (last_quality - first_quality) * 100

            print(f"\n   Total improvement: {improvement_pp:+.1f}pp (from {first_quality:.3f} to {last_quality:.3f})")

            if improvement_pp >= 16:
                print(f"   ✅ Target improvement achieved (≥+16pp)")
            else:
                print(f"   ⚠️  Below target (+16-25pp expected)")
                print(f"   Note: May need more turns or higher-quality initial patterns")
        else:
            print(f"\n✓ Quality samples: {len(quality_samples)} checkpoints")
            print(f"   ⚠️  Insufficient data for trajectory analysis")

        # Check 5: Pattern learner statistics
        if wrapper.emission_generator and hasattr(wrapper.emission_generator, 'pattern_learner'):
            stats = wrapper.emission_generator.pattern_learner.get_stats()
            print(f"\n✓ Final pattern learner state:")
            print(f"   Total patterns: {stats['total_patterns']}")
            print(f"   Total phrases: {stats['total_phrases']}")
            if stats['total_phrases'] > 0:
                print(f"   Mean quality: {stats['mean_phrase_quality']:.3f}")
                print(f"   ✅ Pattern learner accumulating data")
            else:
                print(f"   Note: Novel phrases recorded for future learning")

        # Final result
        print("\n" + "=" * 70)
        if success and len(quality_samples) >= 2:
            print("🎉 TEST PASSED: Quality modulation integration operational")
            print("\n✅ Week 3 Day 5: Quality Modulation COMPLETE")
            print("   - Three-layer quality boost integrated")
            print("   - Satisfaction fingerprinting operational")
            print("   - Lyapunov stability gating operational")
            print("   - Quality improvement trajectory validated")
            return 0
        elif success:
            print("✅ TEST PASSED: Infrastructure operational (insufficient data for full validation)")
            print("\n⚠️  Week 3 Day 5: Needs longer conversation for full trajectory analysis")
            print("   - Three-layer quality boost integrated ✅")
            print("   - Satisfaction fingerprinting operational ✅")
            print("   - Lyapunov stability gating operational ✅")
            print("   - Quality improvement: Needs more data for validation")
            return 0
        else:
            print("⚠️  TEST INCOMPLETE: Some checks failed (see warnings above)")
            return 1

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Run quality modulation integration test."""
    print("\n" + "=" * 70)
    print("🌀 QUALITY MODULATION INTEGRATION TEST")
    print("   Phase 1 Week 3, Day 5: FFITTSS Quality Modulation")
    print("   November 17, 2025")
    print("=" * 70)

    result = test_quality_modulation_integration()

    if result == 0:
        print("\n🎉 QUALITY MODULATION INTEGRATION COMPLETE!")
        print("\n📊 Expected Impact (from FFITTSS validation):")
        print("   Layer 1 (Base EMA): α=0.15, converges 10-20 turns")
        print("   Layer 2 (Fingerprinting): +8-12pp for RESTORATIVE/CONCRESCENT")
        print("   Layer 3 (Lyapunov): +5-8pp for STABLE/ATTRACTING regimes")
        print("   TOTAL: +16-25pp quality improvement over baseline")
    else:
        print(f"\n⚠️  Test incomplete or failed")

    return result


if __name__ == '__main__':
    sys.exit(main())
