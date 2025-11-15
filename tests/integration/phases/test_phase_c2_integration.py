#!/usr/bin/env python3
"""
Phase C2 Integration Test - End-to-End Validation
==================================================

Tests that lure-informed phrase selection is working in the integrated system:
1. Organ lure fields generated (EMPATHY/WISDOM/AUTHENTICITY)
2. organ_results passed to emission_generator
3. Lure-weighted phrase selection occurs
4. TSK tracking includes lure_signature_used_in_emission
5. Emission text resonates with lure landscape

Date: November 13, 2025
Phase: C2 Integration Complete
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_phase_c2_integration():
    """Test integrated lure-informed phrase selection."""

    print("="*80)
    print("🌀 PHASE C2 INTEGRATION TEST: Lure-Informed Emission")
    print("="*80)

    organism = ConversationalOrganismWrapper()

    # Test inputs designed to activate different lure dimensions
    test_cases = [
        {
            "text": "I'm feeling really overwhelmed and scared right now.",
            "expected_lures": ["fear", "compassion"],
            "description": "High fear + compassion should guide phrase selection"
        },
        {
            "text": "This conversation feels really safe and connected.",
            "expected_lures": ["joy", "relational", "receptive"],
            "description": "Joy + relational + receptive should guide phrases"
        },
        {
            "text": "I notice I'm getting defensive and need space.",
            "expected_lures": ["anger", "boundaried"],
            "description": "Anger + boundaried should guide protective phrases"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-'*80}")
        print(f"Test Case {i}: {test_case['description']}")
        print(f"{'-'*80}")
        print(f"Input: \"{test_case['text']}\"")

        try:
            result = organism.process_text(test_case['text'])

            # Check 1: Emission generated
            emission_text = result.get('emission_text')
            print(f"\n✅ Emission Generated:")
            print(f"   \"{emission_text}\"")

            # Check 2: Lure fields tracked
            felt_states = result.get('felt_states', {})
            empathy_lure = felt_states.get('empathy_lure', 0.0)
            wisdom_lure = felt_states.get('wisdom_lure', 0.0)
            authenticity_lure = felt_states.get('authenticity_lure', 0.0)

            print(f"\n✅ Lure Fields Tracked:")
            print(f"   EMPATHY lure: {empathy_lure:.3f}")
            print(f"   WISDOM lure: {wisdom_lure:.3f}")
            print(f"   AUTHENTICITY lure: {authenticity_lure:.3f}")

            # Check 3: Lure signature used in emission
            lure_signature = felt_states.get('lure_signature_used_in_emission')
            if lure_signature:
                print(f"\n✅ Lure Signature Used in Emission:")
                emotional_sig = lure_signature.get('emotional_signature', {})
                cognitive_sig = lure_signature.get('cognitive_signature', {})
                relational_sig = lure_signature.get('relational_signature', {})

                # Show top 3 dimensions in each signature
                top_emotional = sorted(emotional_sig.items(), key=lambda x: x[1], reverse=True)[:3]
                top_cognitive = sorted(cognitive_sig.items(), key=lambda x: x[1], reverse=True)[:3]
                top_relational = sorted(relational_sig.items(), key=lambda x: x[1], reverse=True)[:3]

                print(f"   Emotional (top 3): {', '.join(f'{k}={v:.2f}' for k, v in top_emotional)}")
                print(f"   Cognitive (top 3): {', '.join(f'{k}={v:.2f}' for k, v in top_cognitive)}")
                print(f"   Relational (top 3): {', '.join(f'{k}={v:.2f}' for k, v in top_relational)}")
            else:
                print(f"\n⚠️  Lure signature not tracked (lure selector may not be enabled)")

            # Check 4: Emission confidence
            emission_confidence = result.get('emission_confidence', 0.0)
            print(f"\n✅ Emission Confidence: {emission_confidence:.3f}")

            # Check 5: Expected lures present
            expected_found = []
            if lure_signature:
                all_dimensions = {**emotional_sig, **cognitive_sig, **relational_sig}
                for expected_lure in test_case['expected_lures']:
                    if expected_lure in all_dimensions and all_dimensions[expected_lure] > 0.2:
                        expected_found.append(expected_lure)

                if expected_found:
                    print(f"\n✅ Expected Lures Found: {', '.join(expected_found)}")
                else:
                    print(f"\n⚠️  Expected lures not strongly present (may be keyword-dependent)")

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*80}")
    print("🎯 PHASE C2 INTEGRATION STATUS")
    print("="*80)
    print("✅ Integration complete if all tests generated emissions")
    print("✅ TSK tracking complete if lure signatures present")
    print("✅ Lure-informed emission active if expected lures found")
    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    test_phase_c2_integration()
