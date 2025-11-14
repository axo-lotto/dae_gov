"""
Test Family V0 Target Learning Integration
===========================================

Tests DAE 3.0 family-specific V0 optimization in full organism.

Expected behavior:
- Each family learns its optimal V0 convergence target
- High satisfaction conversations (>0.8) update target via EMA
- Family V0 targets guide future convergence (future enhancement)
- Per-family organ weights are tracked

Date: November 12, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_family_v0_integration():
    """Test Family V0 learning through conversation processing"""

    print("="*80)
    print("🧪 FAMILY V0 TARGET LEARNING INTEGRATION TEST")
    print("="*80)

    # Initialize organism
    print("\n📋 Initializing organism...")
    organism = ConversationalOrganismWrapper(bundle_path="Bundle")

    # Check if Family V0 learner loaded
    if not organism.family_v0_learner:
        print("\n❌ Family V0 learner not available!")
        return

    print("\n📊 Initial Family V0 states:")
    initial_reports = organism.family_v0_learner.get_all_families_report()
    if initial_reports:
        for report in initial_reports[:3]:  # Show first 3 families
            print(f"   {report['family_id']}:")
            print(f"      Target V0: {report['target_v0']:.3f}")
            print(f"      Updates: {report['total_updates']}")
            print(f"      Mean satisfaction: {report['satisfaction_mean']:.3f}")
    else:
        print("   (No families yet)")

    # Test inputs designed to trigger different satisfaction levels
    test_conversations = [
        {
            'name': 'High Satisfaction (Should Update V0)',
            'input': "This conversation feels really safe and grounding. Thank you for being here with me.",
            'expected_satisfaction': '>0.8'
        },
        {
            'name': 'High Satisfaction (Relational)',
            'input': "I feel deeply heard and understood right now. This is exactly what I needed.",
            'expected_satisfaction': '>0.8'
        },
        {
            'name': 'Moderate Satisfaction',
            'input': "I'm feeling confused about something.",
            'expected_satisfaction': '0.5-0.8'
        }
    ]

    print(f"\n🗣️  Processing {len(test_conversations)} conversations...")

    for i, conv in enumerate(test_conversations, 1):
        print(f"\n{'─'*80}")
        print(f"Conversation {i}: {conv['name']}")
        print(f"{'─'*80}")
        print(f"Input: \"{conv['input']}\"")
        print(f"Expected satisfaction: {conv['expected_satisfaction']}")

        # Process with Phase 2 and Phase 5 (enables family tracking + V0 learning)
        result = organism.process_text(
            text=conv['input'],
            enable_phase2=True,
            enable_tsk_recording=False
        )

        # Show satisfaction (drives V0 target updates)
        satisfaction = result['felt_states']['satisfaction_final']
        v0_energy = result['felt_states']['v0_energy']['final_energy']

        print(f"\nActual satisfaction: {satisfaction:.3f}")
        print(f"V0 energy (final): {v0_energy:.3f}")

        # Check if V0 target would update (satisfaction > 0.8)
        if satisfaction > 0.8:
            print(f"✅ High satisfaction - V0 target will update!")
        else:
            print(f"⚠️  Satisfaction too low - V0 target not updated")

        # Show family assignment (if available)
        if organism.phase5_learning:
            family_id = organism.phase5_learning.get_current_family_id()
            if family_id:
                print(f"Assigned to family: {family_id}")

    # Final Family V0 states
    print(f"\n{'='*80}")
    print("📊 FINAL FAMILY V0 STATES")
    print(f"{'='*80}")

    final_reports = organism.family_v0_learner.get_all_families_report()

    if final_reports:
        print(f"\nTotal families tracked: {len(final_reports)}")

        for report in final_reports[:3]:  # Show first 3
            family_id = report['family_id']

            # Find initial report for comparison
            initial_report = None
            for r in initial_reports:
                if r['family_id'] == family_id:
                    initial_report = r
                    break

            print(f"\n{family_id}:")
            print(f"   Target V0: {report['target_v0']:.3f}", end="")
            if initial_report and report['total_updates'] > initial_report['total_updates']:
                delta = report['target_v0'] - initial_report['target_v0']
                print(f" (Δ={delta:+.4f})")
            else:
                print()

            print(f"   V0 mean: {report['v0_mean']:.3f} ± {report['v0_std']:.3f}")
            print(f"   Satisfaction mean: {report['satisfaction_mean']:.3f}")
            print(f"   Convergence cycles: {report['convergence_cycles_mean']:.1f}")
            print(f"   Total updates: {report['total_updates']}")

            if report['top_organs']:
                print(f"   Top organs:")
                for organ, weight in report['top_organs'][:3]:
                    print(f"      • {organ}: {weight:.3f}")

    else:
        print("\n⚠️  No families tracked yet")

    # Validate learning occurred
    print(f"\n{'='*80}")
    print("✅ VALIDATION")
    print(f"{'='*80}")

    updates_occurred = False
    for report in final_reports:
        if report['total_updates'] > 0:
            updates_occurred = True
            break

    if updates_occurred:
        print(f"✅ SUCCESS: Family V0 learning is operational!")
        print(f"   Families are learning optimal V0 convergence targets")
    else:
        print(f"⚠️  WARNING: No V0 updates occurred")
        print(f"   (This may be expected if all satisfactions < 0.8)")

    print(f"\n✅ Family V0 integration test complete!")

if __name__ == '__main__':
    test_family_v0_integration()
