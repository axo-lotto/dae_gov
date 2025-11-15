#!/usr/bin/env python3
"""
Phase B6: Validate Generative Processual Emission

Tests that conversational organs (EMPATHY/WISDOM/AUTHENTICITY) now
participate continuously via lure attractors, enabling generative
processual emission instead of passive template matching.

Expected improvements:
- EMPATHY: 20% → 80-100% activation
- WISDOM: 20% → 70-90% activation
- AUTHENTICITY: 0% → 60-80% activation
"""

import sys
from dataclasses import dataclass

sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


@dataclass
class MockTextOccasion:
    text: str
    chunk_id: str = "test_0_0"


def test_generative_processual_emission():
    """Validate generative processual emission with 6 lure organs."""

    organism = ConversationalOrganismWrapper()

    test_inputs = [
        "I'm feeling overwhelmed right now.",
        "This conversation feels really safe and connected.",
        "I notice I'm getting defensive here.",
        "There's so much grief in this moment.",
        "I just need someone to validate that I'm not crazy."
    ]

    print("\n" + "="*80)
    print("🌀 PHASE B6: GENERATIVE PROCESSUAL EMISSION VALIDATION")
    print("="*80)
    print("\nTesting 6-organ lure attractor system:")
    print("  EO (polyvagal state) + NDAM (salience) + RNX (temporal)")
    print("  + EMPATHY (emotional) + WISDOM (pattern) + AUTHENTICITY (vulnerability)")
    print("\n" + "="*80)

    total_organs = 11
    organ_activation_counts = {
        'EMPATHY': 0, 'WISDOM': 0, 'AUTHENTICITY': 0,
        'EO': 0, 'NDAM': 0, 'RNX': 0,
        'LISTENING': 0, 'PRESENCE': 0, 'BOND': 0, 'SANS': 0, 'CARD': 0
    }
    total_lure_contribution = []

    for i, text in enumerate(test_inputs, 1):
        result = organism.process_text(text)

        print(f"\n{'-'*80}")
        print(f"Test {i}/{len(test_inputs)}: {text[:60]}...")
        print(f"{'-'*80}")

        # Count active organs from felt_states
        active_organs = 0
        organ_names = ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                      'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']

        for organ_name in organ_names:
            coherence_key = f'{organ_name.lower()}_coherence'
            coherence = result['felt_states'].get(coherence_key, 0.0)
            if coherence > 0:
                active_organs += 1
                organ_activation_counts[organ_name] += 1

        print(f"  Active Organs: {active_organs}/{total_organs}")
        print(f"  V0 Cycles: {result['felt_states'].get('v0_cycles', 0)}")
        print(f"  Nexuses Formed: {result['felt_states'].get('nexus_count', 0)}")

        # Extract lure information
        lure_contrib = result['felt_states'].get('lure_contribution_to_v0', 0.0)
        total_lure_contribution.append(lure_contrib)

        print(f"\n  🆕 Lure Attractor Status:")
        print(f"    EO:           lure={result['felt_states'].get('eo_lure', 0):.3f}")
        print(f"    NDAM:         lure={result['felt_states'].get('ndam_lure', 0):.3f}")
        print(f"    RNX:          lure={result['felt_states'].get('rnx_lure', 0):.3f}")
        print(f"    EMPATHY:      lure={result['felt_states'].get('empathy_lure', 0):.3f}")
        print(f"    WISDOM:       lure={result['felt_states'].get('wisdom_lure', 0):.3f}")
        print(f"    AUTHENTICITY: lure={result['felt_states'].get('authenticity_lure', 0):.3f}")
        print(f"    → Total V0 contribution: {lure_contrib:.3f}")

        print(f"\n  Emission: {result.get('emission_text', 'None')[:80] if result.get('emission_text') else 'None'}...")
        print(f"    Confidence: {result.get('emission_confidence', 0):.3f}")

    # Summary statistics
    print("\n" + "="*80)
    print("📊 ACTIVATION SUMMARY (Conversational Lure Organs)")
    print("="*80)

    print(f"\nConversational Organs (Lure Attractors - Phase B):")
    for organ_name in ['EMPATHY', 'WISDOM', 'AUTHENTICITY']:
        activation_rate = (organ_activation_counts[organ_name] / len(test_inputs)) * 100
        status = "✅" if activation_rate >= 60 else "⚠️ " if activation_rate >= 40 else "❌"
        print(f"  {status} {organ_name:12s}: {activation_rate:5.1f}% ({organ_activation_counts[organ_name]}/{len(test_inputs)})")

    print(f"\nContext Organs (Lure Attractors - Phase A):")
    for organ_name in ['EO', 'NDAM', 'RNX']:
        activation_rate = (organ_activation_counts[organ_name] / len(test_inputs)) * 100
        status = "✅" if activation_rate >= 80 else "⚠️ " if activation_rate >= 40 else "❌"
        print(f"  {status} {organ_name:12s}: {activation_rate:5.1f}% ({organ_activation_counts[organ_name]}/{len(test_inputs)})")

    print(f"\nOther Organs:")
    for organ_name in ['LISTENING', 'PRESENCE', 'BOND', 'SANS', 'CARD']:
        activation_rate = (organ_activation_counts[organ_name] / len(test_inputs)) * 100
        status = "✅" if activation_rate >= 60 else "⚠️ " if activation_rate >= 40 else "❌"
        print(f"  {status} {organ_name:12s}: {activation_rate:5.1f}% ({organ_activation_counts[organ_name]}/{len(test_inputs)})")

    # Lure contribution stats
    avg_lure = sum(total_lure_contribution) / len(total_lure_contribution)
    print(f"\nLure Contribution to V0:")
    print(f"  Average: {avg_lure:.3f}")
    print(f"  Range: {min(total_lure_contribution):.3f} - {max(total_lure_contribution):.3f}")

    # Success criteria
    empathy_success = organ_activation_counts['EMPATHY'] >= len(test_inputs) * 0.60
    wisdom_success = organ_activation_counts['WISDOM'] >= len(test_inputs) * 0.60
    authenticity_success = organ_activation_counts['AUTHENTICITY'] >= len(test_inputs) * 0.50

    print("\n" + "="*80)
    print("🎯 GENERATIVE PROCESSUAL EMISSION STATUS")
    print("="*80)
    print(f"  {'✅' if empathy_success else '❌'} EMPATHY lure attractor: {'WORKING' if empathy_success else 'NEEDS TUNING'}")
    print(f"  {'✅' if wisdom_success else '❌'} WISDOM lure attractor: {'WORKING' if wisdom_success else 'NEEDS TUNING'}")
    print(f"  {'✅' if authenticity_success else '⚠️ '} AUTHENTICITY lure attractor: {'WORKING' if authenticity_success else 'PARTIAL (keyword limited)'}")

    if empathy_success and wisdom_success:
        print(f"\n✅ GENERATIVE PROCESSUAL EMISSION ACTIVE")
        print("   Conversational organs participating continuously via lure attractors.")
        print("   System bridged from passive to generative emission.")
    else:
        print(f"\n⚠️  GENERATIVE PROCESSUAL EMISSION PARTIAL")
        print("   Some organs still keyword-dependent.")

    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    test_generative_processual_emission()
