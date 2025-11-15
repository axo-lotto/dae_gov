"""
Test R-Matrix Learning Integration
====================================

Tests DAE 3.0 organ coupling learning in full organism.

Expected behavior:
- R-matrix starts as identity (all couplings = 0 or 1.0 on diagonal)
- After processing conversations, organ couplings strengthen
- Synergies emerge: BOND+EO+NDAM (trauma triad), EMPATHY+LISTENING+PRESENCE (relational)

Date: November 12, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_r_matrix_learning():
    """Test R-matrix learning through conversation processing"""

    print("="*80)
    print("🧪 R-MATRIX LEARNING INTEGRATION TEST")
    print("="*80)

    # Initialize organism
    print("\n📋 Initializing organism...")
    organism = ConversationalOrganismWrapper(bundle_path="Bundle")

    # Check if R-matrix learner loaded
    if not organism.organ_coupling_learner:
        print("\n❌ Organ coupling learner not available!")
        return

    print("\n📊 Initial R-matrix state:")
    initial_report = organism.organ_coupling_learner.get_synergy_report()
    print(f"   Mean coupling: {initial_report['mean_coupling']:.4f}")
    print(f"   Trauma triad: {initial_report['synergy_groups']['trauma_triad']:.4f}")
    print(f"   Relational attunement: {initial_report['synergy_groups']['relational_attunement']:.4f}")

    # Test inputs designed to activate different organ combinations
    test_conversations = [
        {
            'name': 'Trauma Activation (BOND+EO+NDAM)',
            'input': "I'm having a panic attack and everything feels terrifying. I can't breathe."
        },
        {
            'name': 'Relational Safety (EMPATHY+LISTENING+PRESENCE)',
            'input': "This conversation feels really safe. Thank you for being here with me."
        },
        {
            'name': 'Coherence Need (SANS+WISDOM+CARD)',
            'input': "I feel confused and scattered. Can you help me make sense of what's happening?"
        }
    ]

    print(f"\n🗣️  Processing {len(test_conversations)} conversations...")

    for i, conv in enumerate(test_conversations, 1):
        print(f"\n{'─'*80}")
        print(f"Conversation {i}: {conv['name']}")
        print(f"{'─'*80}")
        print(f"Input: \"{conv['input']}\"")

        # Process with Phase 2 (enables R-matrix learning)
        result = organism.process_text(
            text=conv['input'],
            enable_phase2=True,
            enable_tsk_recording=False
        )

        # Show satisfaction (drives coupling strength)
        satisfaction = result['felt_states']['satisfaction_final']
        print(f"\nSatisfaction: {satisfaction:.3f}")

        # Show active organs
        organ_coherences = result['felt_states']['organ_coherences']
        active_organs = {org: coh for org, coh in organ_coherences.items() if coh > 0.5}
        print(f"Active organs (coherence > 0.5):")
        for org, coh in sorted(active_organs.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {org}: {coh:.3f}")

    # Final R-matrix state
    print(f"\n{'='*80}")
    print("📊 FINAL R-MATRIX STATE")
    print(f"{'='*80}")

    final_report = organism.organ_coupling_learner.get_synergy_report()
    print(f"\nMean coupling: {final_report['mean_coupling']:.4f} (was {initial_report['mean_coupling']:.4f})")
    print(f"Std coupling: {final_report['std_coupling']:.4f}")
    print(f"Max coupling: {final_report['max_coupling']:.4f}")

    print(f"\n🧬 Synergy Groups:")
    for group_name, strength in final_report['synergy_groups'].items():
        initial_strength = initial_report['synergy_groups'][group_name]
        change = strength - initial_strength
        print(f"   • {group_name}: {strength:.4f} (Δ={change:+.4f})")

    print(f"\n🏆 Top 10 Learned Couplings:")
    for i, coupling in enumerate(final_report['top_couplings'][:10], 1):
        print(f"   {i}. {coupling['organs']}: {coupling['strength']:.4f}")

    print(f"\n✅ R-matrix learning test complete!")
    print(f"   Total coupling updates: {final_report['total_updates']}")

    # Validate learning occurred
    if final_report['mean_coupling'] > initial_report['mean_coupling']:
        print(f"\n✅ SUCCESS: R-matrix learned organ couplings!")
        print(f"   Mean coupling increased: {initial_report['mean_coupling']:.4f} → {final_report['mean_coupling']:.4f}")
    else:
        print(f"\n⚠️  WARNING: R-matrix coupling did not increase")

if __name__ == '__main__':
    test_r_matrix_learning()
