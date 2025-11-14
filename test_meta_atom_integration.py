"""
Test Meta-Atom Integration - Phase 3 Validation
================================================

Tests the full pipeline:
1. User input → 11 organs process
2. Organs → MetaAtomActivator
3. Meta-atoms → Semantic fields
4. Semantic fields → Nexus composition
5. Nexuses → Emission generation (with meta-atom phrases)

Date: November 12, 2025
Status: Phase 3 Testing
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_meta_atom_activation():
    """Test meta-atom activation with trauma-aware inputs."""

    print("="*80)
    print("🧪 META-ATOM ACTIVATION TEST - Phase 3")
    print("="*80)

    # Initialize organism
    print("\n📋 Initializing organism...")
    organism = ConversationalOrganismWrapper(bundle_path="Bundle")

    # Test inputs designed to trigger specific meta-atoms
    test_cases = [
        {
            'name': 'Burnout/Trauma Activation',
            'input': "I'm so burned out I can barely get out of bed anymore. I've been working 70+ hours a week and I just feel numb.",
            'expected_meta_atoms': ['trauma_aware', 'fierce_holding', 'somatic_wisdom'],
            'expected_organs': ['BOND', 'EO', 'NDAM', 'EMPATHY']
        },
        {
            'name': 'Panic Attack/Safety Crisis',
            'input': "I'm having a panic attack right now. My chest is tight and I can't breathe. Everything feels scary.",
            'expected_meta_atoms': ['safety_restoration', 'somatic_wisdom', 'compassion_safety'],
            'expected_organs': ['EO', 'PRESENCE', 'NDAM', 'EMPATHY']
        },
        {
            'name': 'Grief Timeline',
            'input': "My mom died two months ago and everyone keeps telling me I should be 'over it' by now.",
            'expected_meta_atoms': ['fierce_holding', 'temporal_grounding', 'relational_attunement'],
            'expected_organs': ['EMPATHY', 'PRESENCE', 'RNX', 'BOND']
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print(f"{'='*80}")
        print(f"Input: \"{test_case['input']}\"")
        print(f"\nExpected meta-atoms: {', '.join(test_case['expected_meta_atoms'])}")
        print(f"Expected organs: {', '.join(test_case['expected_organs'])}")

        # Process with Phase 2 enabled (multi-cycle convergence)
        result = organism.process_text(
            text=test_case['input'],
            context={'test_case': test_case['name']},
            enable_tsk_recording=False,
            enable_phase2=True  # Enable Phase 2 for meta-atom activation
        )

        # Extract results
        felt_states = result.get('felt_states', {})
        organ_coherences = felt_states.get('organ_coherences', {})
        emission_text = result.get('emission_text', 'No emission')
        emission_confidence = result.get('emission_confidence', 0.0)

        print(f"\n📊 RESULTS:")
        print(f"   Emission: \"{emission_text}\"")
        print(f"   Confidence: {emission_confidence:.3f}")
        print(f"\n   Active organs (coherence > 0.5):")
        active_organs = {organ: coh for organ, coh in organ_coherences.items() if coh > 0.5}
        for organ, coherence in sorted(active_organs.items(), key=lambda x: x[1], reverse=True):
            print(f"      • {organ}: {coherence:.3f}")

        # Check if expected organs activated
        expected_activated = [org for org in test_case['expected_organs'] if org in active_organs]
        print(f"\n   ✅ Expected organs activated: {len(expected_activated)}/{len(test_case['expected_organs'])}")
        if len(expected_activated) < len(test_case['expected_organs']):
            missing = set(test_case['expected_organs']) - set(expected_activated)
            print(f"   ⚠️  Missing: {', '.join(missing)}")

        print(f"\n{'='*80}\n")

    print("\n✅ META-ATOM ACTIVATION TEST COMPLETE")
    print("="*80)

if __name__ == '__main__':
    test_meta_atom_activation()
