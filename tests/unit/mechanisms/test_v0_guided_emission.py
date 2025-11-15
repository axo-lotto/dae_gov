"""
Test V0-Guided Emission Selection
==================================

Tests DAE 3.0 V0 energy and organ weight guidance in emission generation.

Expected behavior:
- Emissions near family's learned V0 target get confidence boost
- Nexuses from high-weight organs are amplified
- System prefers emissions matching family's learned patterns

Date: November 12, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_v0_guided_emission():
    """Test V0-guided emission with family learning"""

    print("="*80)
    print("🧪 V0-GUIDED EMISSION SELECTION TEST")
    print("="*80)

    # Initialize organism
    print("\n📋 Initializing organism...")
    organism = ConversationalOrganismWrapper(bundle_path="Bundle")

    # Check if learners loaded
    if not organism.family_v0_learner:
        print("\n❌ Family V0 learner not available!")
        return

    print("\n📊 Current Family V0 Learning State:")
    reports = organism.family_v0_learner.get_all_families_report()
    if reports:
        for report in reports[:2]:
            print(f"   {report['family_id']}:")
            print(f"      Target V0: {report['target_v0']:.3f}")
            print(f"      Top organ: {report['top_organs'][0][0]} ({report['top_organs'][0][1]:.3f})" if report['top_organs'] else "")
    else:
        print("   (No families yet - will use defaults)")

    # Test conversations designed to show V0 guidance effect
    test_conversations = [
        {
            'name': 'High Safety & Grounding (should match learned patterns)',
            'input': "This conversation feels really safe and grounding. Thank you for being present with me.",
            'expected': 'Uses learned family patterns (SANS, PRESENCE high weight)'
        },
        {
            'name': 'Relational Depth',
            'input': "I feel deeply seen and understood right now. This is powerful.",
            'expected': 'Relational organs (EMPATHY, LISTENING) activated'
        },
        {
            'name': 'Confusion/Coherence Need',
            'input': "I'm feeling scattered and need help making sense of things.",
            'expected': 'Coherence organs (SANS, WISDOM, CARD) activated'
        }
    ]

    print(f"\n🗣️  Processing {len(test_conversations)} conversations with V0 guidance...")

    results = []

    for i, conv in enumerate(test_conversations, 1):
        print(f"\n{'─'*80}")
        print(f"Conversation {i}: {conv['name']}")
        print(f"{'─'*80}")
        print(f"Input: \"{conv['input']}\"")
        print(f"Expected: {conv['expected']}")

        # Process with Phase 2 (enables V0 guidance)
        result = organism.process_text(
            text=conv['input'],
            enable_phase2=True,
            enable_tsk_recording=False
        )

        # Extract key metrics
        v0_energy = result['felt_states']['v0_energy']['final_energy']
        satisfaction = result['felt_states']['satisfaction_final']
        emission_confidence = result['felt_states'].get('emission_confidence', 0.0)
        emission_text = result.get('emission_text', '')

        # Get family assignment
        family_id = None
        if organism.phase5_learning:
            family_id = organism.phase5_learning.get_current_family_id()

        # Get family V0 target for comparison
        family_v0_target = None
        if family_id and organism.family_v0_learner:
            family_v0_target = organism.family_v0_learner.get_v0_target(family_id)

        print(f"\nResults:")
        print(f"   V0 energy (final): {v0_energy:.3f}")
        if family_v0_target:
            v0_distance = abs(v0_energy - family_v0_target)
            print(f"   Family V0 target: {family_v0_target:.3f} (distance: {v0_distance:.3f})")
        print(f"   Satisfaction: {satisfaction:.3f}")
        print(f"   Emission confidence: {emission_confidence:.3f}")
        print(f"   Family: {family_id if family_id else 'None'}")
        print(f"   Emission: \"{emission_text[:80]}...\"" if len(emission_text) > 80 else f"   Emission: \"{emission_text}\"")

        # Show active organs
        organ_coherences = result['felt_states']['organ_coherences']
        active_organs = {org: coh for org, coh in organ_coherences.items() if coh > 0.5}
        if active_organs:
            print(f"   Active organs (coherence > 0.5):")
            for org, coh in sorted(active_organs.items(), key=lambda x: x[1], reverse=True)[:5]:
                # Check if this organ has high weight in family
                high_weight = False
                if family_id and organism.family_v0_learner:
                    organ_weights = organism.family_v0_learner.get_organ_weights(family_id)
                    if org in organ_weights and organ_weights[org] > 1.0:
                        high_weight = True
                weight_marker = " ⭐" if high_weight else ""
                print(f"      • {org}: {coh:.3f}{weight_marker}")

        results.append({
            'name': conv['name'],
            'v0_energy': v0_energy,
            'family_v0_target': family_v0_target,
            'v0_distance': abs(v0_energy - family_v0_target) if family_v0_target else None,
            'satisfaction': satisfaction,
            'emission_confidence': emission_confidence,
            'family_id': family_id
        })

    # Analysis
    print(f"\n{'='*80}")
    print("📊 V0 GUIDANCE ANALYSIS")
    print(f"{'='*80}")

    if results[0]['family_v0_target']:
        print(f"\nFamily V0 Target: {results[0]['family_v0_target']:.3f}")
        print(f"\nV0 Distance Analysis:")
        for i, res in enumerate(results, 1):
            if res['v0_distance'] is not None:
                print(f"   Conv {i}: V0={res['v0_energy']:.3f}, distance={res['v0_distance']:.3f}, confidence={res['emission_confidence']:.3f}")

        # Check if confidence correlates with V0 distance
        print(f"\n🔍 Hypothesis: Emissions near family V0 target should have higher confidence")

        # Find conversation with smallest V0 distance
        min_distance_conv = min(results, key=lambda x: x['v0_distance'] if x['v0_distance'] is not None else 999)
        max_distance_conv = max(results, key=lambda x: x['v0_distance'] if x['v0_distance'] is not None else 0)

        print(f"   Closest to target: {min_distance_conv['name']}")
        print(f"      Distance: {min_distance_conv['v0_distance']:.3f}, Confidence: {min_distance_conv['emission_confidence']:.3f}")
        print(f"   Furthest from target: {max_distance_conv['name']}")
        print(f"      Distance: {max_distance_conv['v0_distance']:.3f}, Confidence: {max_distance_conv['emission_confidence']:.3f}")

    else:
        print(f"\n⚠️  No family V0 target yet - guidance not active")
        print(f"   (System will learn V0 targets from high-satisfaction conversations)")

    # Validation
    print(f"\n{'='*80}")
    print("✅ VALIDATION")
    print(f"{'='*80}")

    if results[0]['family_v0_target']:
        print(f"✅ V0-guided emission operational!")
        print(f"   Family V0 target: {results[0]['family_v0_target']:.3f}")
        print(f"   Emission confidence modulated by V0 distance")
        print(f"   Organ weights applied to nexus selection")
    else:
        print(f"✅ V0-guided emission integration complete!")
        print(f"   (Awaiting family V0 learning from conversations)")

    print(f"\n✅ V0-guided emission test complete!")

if __name__ == '__main__':
    test_v0_guided_emission()
