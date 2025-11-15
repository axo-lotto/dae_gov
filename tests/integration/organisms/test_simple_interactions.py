#!/usr/bin/env python3
"""
Test simple interactions for stable foundation building.

Tests basic greetings, transitions, and simple responses to ensure
natural language without exposing internal machinery.

NOV 13, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_simple_interactions():
    """Test basic conversational interactions."""

    print("🧪 SIMPLE INTERACTION TEST")
    print("="*70)
    print("Testing natural language responses without technical exposure")
    print()

    # Initialize organism
    print("📋 Initializing organism...")
    organism = ConversationalOrganismWrapper(bundle_path="Bundle")
    print("✅ Organism initialized")
    print()

    # Test cases: simple greetings and transitions
    test_cases = [
        {
            "name": "Simple Greeting",
            "input": "Hey there!",
            "expect": "Natural, friendly greeting"
        },
        {
            "name": "How are you?",
            "input": "How are you doing?",
            "expect": "Simple presence acknowledgment"
        },
        {
            "name": "Feeling stuck",
            "input": "I'm feeling stuck",
            "expect": "Empathic presence, no jargon"
        },
        {
            "name": "Need space",
            "input": "I need some space right now",
            "expect": "Respecting boundary, gentle"
        },
        {
            "name": "Feeling safe",
            "input": "This feels safe",
            "expect": "Witnessing, spacious"
        }
    ]

    passes = 0
    failures = []

    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: {test['name']}")
        print(f"Input: \"{test['input']}\"")

        # Process
        result = organism.process_text(test['input'], context={'turn': i}, enable_phase2=True)
        felt_states = result.get('felt_states', {})
        emission = felt_states.get('emission_text', '')
        confidence = felt_states.get('emission_confidence', 0.0)

        print(f"Emission: \"{emission}\"")
        print(f"Confidence: {confidence:.3f}")

        # Check for technical exposure
        technical_names = [
            'kairos_emergence', 'temporal_grounding', 'compassion_safety',
            'trauma_aware', 'window_of_tolerance', 'coherence_integration',
            'somatic_wisdom', 'relational_attunement', 'fierce_holding',
            'safety_restoration'
        ]

        exposed = [name for name in technical_names if name in emission.lower()]

        if exposed:
            print(f"❌ FAIL: Exposed meta-atom names: {exposed}")
            failures.append({
                'test': test['name'],
                'exposed': exposed,
                'emission': emission
            })
        else:
            # Check for monosyllabic responses
            words = emission.strip().split()
            if len(words) == 1 and words[0].lower() in ['safe', 'breathe', 'here', 'pause']:
                print(f"⚠️  WARNING: Monosyllabic response: {emission}")
                failures.append({
                    'test': test['name'],
                    'issue': 'monosyllabic',
                    'emission': emission
                })
            else:
                print(f"✅ PASS")
                passes += 1

        print()

    # Summary
    print("="*70)
    print(f"Results: {passes}/{len(test_cases)} passed")

    if failures:
        print(f"\n⚠️  {len(failures)} issues found:")
        for fail in failures:
            print(f"  - {fail['test']}: {fail.get('exposed') or fail.get('issue')}")
            print(f"    Emission: \"{fail['emission']}\"")
    else:
        print("\n✅ All tests passed - stable foundation confirmed!")

    return passes == len(test_cases)

if __name__ == '__main__':
    success = test_simple_interactions()
    sys.exit(0 if success else 1)
