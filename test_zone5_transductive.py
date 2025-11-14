"""
Test Zone 5 Transductive Response Implementation
=================================================

Tests the Zone 5 transductive intelligence fix with real collapse inputs.

Date: November 13, 2025
"""

import sys
import os

# Add project to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_zone5_collapse():
    """Test Zone 5 with the exact input that failed before."""

    print("="*80)
    print("🌀 Testing Zone 5 Transductive Intelligence")
    print("="*80)
    print()

    # Initialize organism
    print("Initializing organism...")
    organism = ConversationalOrganismWrapper()
    print()

    # The exact input that triggered Zone 5 in your logs
    collapse_inputs = [
        "it feels like i'm drowning and any scream i make will not be heard by any of my peers but forgotten forever",
        "i can't breathe, everything is closing in and i'm suffocating under the weight of it all",
        "i'm completely frozen, paralyzed, can't move or speak or even think straight"
    ]

    for i, test_input in enumerate(collapse_inputs, 1):
        print(f"{'='*80}")
        print(f"Test {i}/{len(collapse_inputs)}")
        print(f"{'='*80}")
        print(f"Input: \"{test_input}\"")
        print("-"*80)

        try:
            result = organism.process_text(test_input)

            # Extract results
            emission = result.get('emission_text', '')
            path = result.get('emission_path', 'unknown')
            confidence = result.get('emission_confidence', 0)
            zone = result.get('zone', 'unknown')
            zone_id = result.get('zone_id', 0)

            print(f"Zone: {zone} (Zone {zone_id})")
            print(f"Path: {path}")
            print(f"Confidence: {confidence:.3f}")
            print()
            print(f"Emission:")
            print(f"  {emission}")
            print()

            # Analyze response
            has_dorsal_emoji = any(e in emission for e in ['🌊', '💙', '🌿', '🌙'])
            has_wrong_emoji = any(e in emission for e in ['😊', '✨', '💚'])
            has_open_question = '?' in emission and any(q in emission.lower() for q in ['what', 'can you tell', 'do you'])
            is_brief = len(emission.split()) <= 40  # ~3 sentences
            has_connection = any(phrase in emission.lower() for phrase in ["i'm here", "i'm with", "you're not alone"])
            has_acknowledgment = emission and not emission.startswith("you're safe")

            print("✅ Validation:")
            print(f"  {'✅' if zone_id == 5 else '❌'} Zone 5 detected: {zone_id == 5}")
            print(f"  {'✅' if path == 'felt_guided_llm' else '⚠️ '} Felt-guided LLM used: {path == 'felt_guided_llm'}")
            print(f"  {'✅' if has_acknowledgment else '❌'} Acknowledges collapse: {has_acknowledgment}")
            print(f"  {'✅' if has_dorsal_emoji else '❌'} Dorsal emoji (🌊💙🌿): {has_dorsal_emoji}")
            print(f"  {'✅' if not has_wrong_emoji else '❌'} No wrong emoji (😊✨💚): {not has_wrong_emoji}")
            print(f"  {'✅' if not has_open_question else '⚠️ '} No open questions: {not has_open_question}")
            print(f"  {'✅' if is_brief else '⚠️ '} Brief (≤40 words): {is_brief} ({len(emission.split())} words)")
            print(f"  {'✅' if has_connection else '⚠️ '} Connection affirmation: {has_connection}")

            # Overall score
            checks = [
                zone_id == 5,
                has_acknowledgment,
                has_dorsal_emoji,
                not has_wrong_emoji,
                not has_open_question,
                is_brief,
                has_connection
            ]
            score = sum(checks)
            total = len(checks)

            print()
            if score == total:
                print(f"🎉 PERFECT: {score}/{total} checks passed!")
            elif score >= total - 1:
                print(f"✅ EXCELLENT: {score}/{total} checks passed")
            elif score >= total - 2:
                print(f"⚠️  GOOD: {score}/{total} checks passed (minor issues)")
            else:
                print(f"❌ NEEDS WORK: {score}/{total} checks passed")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

        print()

    print("="*80)
    print("Zone 5 Testing Complete")
    print("="*80)


if __name__ == "__main__":
    test_zone5_collapse()
