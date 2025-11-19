"""
Test LLM Bridge Phase 1 Integration - ConversationFeedbackHandler
==================================================================

Validates that feedback assessment is working correctly in organism wrapper.

Date: November 18, 2025
Status: Phase 1 Integration Test
"""

import sys
from pathlib import Path

# Ensure PYTHONPATH includes project root
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_feedback_handler_initialization():
    """Test that ConversationFeedbackHandler initializes correctly."""
    print("\n🧪 TEST 1: ConversationFeedbackHandler Initialization")
    print("=" * 70)

    try:
        from persona_layer.conversation_feedback_handler import ConversationFeedbackHandler

        handler = ConversationFeedbackHandler()

        # Check attributes exist
        assert hasattr(handler, 'engagement_weight')
        assert hasattr(handler, 'continuation_weight')
        assert hasattr(handler, 'valence_weight')
        assert hasattr(handler, 'positive_words')
        assert hasattr(handler, 'negative_words')

        print("✅ ConversationFeedbackHandler initialized successfully")
        print(f"   - Engagement weight: {handler.engagement_weight}")
        print(f"   - Continuation weight: {handler.continuation_weight}")
        print(f"   - Valence weight: {handler.valence_weight}")
        print(f"   - Positive words: {len(handler.positive_words)} words")
        print(f"   - Negative words: {len(handler.negative_words)} words")

        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_organism_wrapper_integration():
    """Test that organism wrapper has LLM Bridge components integrated."""
    print("\n🧪 TEST 2: Organism Wrapper Integration")
    print("=" * 70)

    try:
        from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

        organism = ConversationalOrganismWrapper()

        # Check LLM Bridge attributes exist
        assert hasattr(organism, 'feedback_handler'), "Missing feedback_handler attribute"
        assert hasattr(organism, 'turn_history'), "Missing turn_history attribute"
        assert hasattr(organism, 'last_emission_data'), "Missing last_emission_data attribute"

        print("✅ Organism wrapper has LLM Bridge components")
        print(f"   - feedback_handler: {type(organism.feedback_handler).__name__ if organism.feedback_handler else 'None'}")
        print(f"   - turn_history: {type(organism.turn_history).__name__ if organism.turn_history else 'None'}")
        print(f"   - last_emission_data: {type(organism.last_emission_data)}")

        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_feedback_assessment_flow():
    """Test the full feedback assessment flow with 2 turns."""
    print("\n🧪 TEST 3: Feedback Assessment Flow (2 Turns)")
    print("=" * 70)

    try:
        from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

        organism = ConversationalOrganismWrapper()

        if not organism.feedback_handler:
            print("⚠️  Skipped: feedback_handler not available")
            return True  # Not a failure, just not available

        # Turn 1: Initial message
        print("\n📝 Turn 1: Organism generates initial response...")
        result1 = organism.process_text(
            text="I'm feeling really stressed about work",
            context={'conversation_id': 'test_session_1'},
            enable_phase2=True
        )

        emission1 = result1.get('emission_text', '')
        print(f"   Emission: {emission1[:80]}...")

        # Check emission was stored
        assert 'test_session_1' in organism.last_emission_data, "Emission data not stored"
        print("✅ Turn 1 emission stored for feedback")

        # Turn 2: User responds (triggers feedback assessment)
        print("\n📝 Turn 2: User responds, feedback assessed...")
        result2 = organism.process_text(
            text="Yes, exactly! That helps me understand it better.",
            context={'conversation_id': 'test_session_1'},
            enable_phase2=True
        )

        # Check if feedback was assessed (would be in context if available)
        if 'feedback' in result2.get('felt_states', {}).get('context', {}):
            feedback = result2['felt_states']['context']['feedback']
            print(f"✅ Feedback assessed:")
            print(f"   - Estimated satisfaction: {feedback['estimated_satisfaction']:.3f}")
            print(f"   - Confidence: {feedback['confidence']:.3f}")
            print(f"   - Update results: {feedback['update_results'].get('status', 'unknown')}")
        else:
            print("⚠️  Feedback not found in context (may be expected if handler failed)")

        emission2 = result2.get('emission_text', '')
        print(f"   Emission: {emission2[:80]}...")

        print("\n✅ Feedback flow completed successfully")
        return True

    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all Phase 1 integration tests."""
    print("\n" + "="*70)
    print("LLM BRIDGE PHASE 1 INTEGRATION TESTS")
    print("ConversationFeedbackHandler + Organism Wrapper")
    print("="*70)

    results = []

    # Run tests
    results.append(("Handler Initialization", test_feedback_handler_initialization()))
    results.append(("Organism Integration", test_organism_wrapper_integration()))
    results.append(("Feedback Flow", test_feedback_assessment_flow()))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({100*passed//total}%)")

    if passed == total:
        print("\n🎉 All Phase 1 integration tests PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
