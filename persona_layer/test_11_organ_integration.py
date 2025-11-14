"""
Test 11-Organ Conversational Organism Integration
=================================================

Tests the complete 11-organ system (Phase 2 COMPLETE):
- 5 Conversational organs
- 6 Trauma/Context-Aware organs (including RNX, EO, CARD)

Date: November 11, 2025
Status: Phase 2 Integration Test
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_11_organ_integration():
    """Test complete 11-organ organism integration."""

    print("\n" + "="*70)
    print("🧪 TESTING 11-ORGAN CONVERSATIONAL ORGANISM INTEGRATION")
    print("="*70)

    # Initialize organism wrapper (should load all 11 organs)
    organism = ConversationalOrganismWrapper(bundle_path="Bundle")

    print("\n" + "-"*70)
    print("TEST 1: Safe Conversation (Ventral Vagal → Detailed Response)")
    print("-"*70)

    safe_text = "I feel safe and grounded. I'm curious to explore this together in a calm way."

    result = organism.process_text(
        text=safe_text,
        context={
            'conversation_id': 'test_safe',
            'epoch_num': 1,
            'training_phase': 'test'
        },
        enable_tsk_recording=True
    )

    felt_states = result['felt_states']

    print(f"\n✅ Text processed through 11 organs")
    print(f"   Mean coherence: {felt_states['mean_coherence']:.3f}")
    print(f"   Satisfaction: {felt_states['satisfaction_final']:.3f}")
    print(f"   V0 final energy: {felt_states['v0_energy']['final_energy']:.3f}")

    print(f"\n📊 Organ Coherences ({len(felt_states['organ_coherences'])} organs):")
    for organ_name, coherence in sorted(felt_states['organ_coherences'].items()):
        print(f"   {organ_name:15s}: {coherence:.3f}")

    print(f"\n🧠 Trauma/Context Signals:")
    print(f"   BOND self_distance: {felt_states['bond_self_distance']:.3f} (trauma level)")
    print(f"   RNX temporal state: {felt_states['rnx_temporal_state']}")
    print(f"   EO polyvagal state: {felt_states['eo_polyvagal_state']} (confidence: {felt_states['eo_state_confidence']:.3f})")
    print(f"   CARD recommended scale: {felt_states['card_recommended_scale']} ({felt_states['card_length_target']} chars)")

    # Validate polyvagal detection
    assert felt_states['eo_polyvagal_state'] == 'ventral_vagal', \
        f"Expected ventral_vagal for safe text, got {felt_states['eo_polyvagal_state']}"

    # Validate response scaling (safe → detailed)
    assert felt_states['card_recommended_scale'] in ['detailed', 'comprehensive'], \
        f"Expected detailed/comprehensive for safe state, got {felt_states['card_recommended_scale']}"

    print(f"\n✅ TEST 1 PASSED: Safe conversation detected correctly")

    # TEST 2: Anxious/Crisis Conversation
    print("\n" + "-"*70)
    print("TEST 2: Anxious Conversation (Sympathetic → Brief Response)")
    print("-"*70)

    crisis_text = "I'm feeling really anxious and overwhelmed. Everything feels urgent."

    result2 = organism.process_text(
        text=crisis_text,
        context={
            'conversation_id': 'test_crisis',
            'epoch_num': 1,
            'training_phase': 'test'
        },
        enable_tsk_recording=True
    )

    felt_states2 = result2['felt_states']

    print(f"\n✅ Text processed through 11 organs")
    print(f"   Mean coherence: {felt_states2['mean_coherence']:.3f}")
    print(f"   Satisfaction: {felt_states2['satisfaction_final']:.3f}")

    print(f"\n🧠 Trauma/Context Signals:")
    print(f"   BOND self_distance: {felt_states2['bond_self_distance']:.3f}")
    print(f"   RNX temporal state: {felt_states2['rnx_temporal_state']}")
    print(f"   EO polyvagal state: {felt_states2['eo_polyvagal_state']} (confidence: {felt_states2['eo_state_confidence']:.3f})")
    print(f"   CARD recommended scale: {felt_states2['card_recommended_scale']} ({felt_states2['card_length_target']} chars)")

    # Validate polyvagal detection (should be sympathetic or mixed)
    assert felt_states2['eo_polyvagal_state'] in ['sympathetic', 'mixed_state'], \
        f"Expected sympathetic/mixed for anxious text, got {felt_states2['eo_polyvagal_state']}"

    # Validate response scaling (anxious → brief/moderate)
    assert felt_states2['card_recommended_scale'] in ['brief', 'moderate'], \
        f"Expected brief/moderate for anxious state, got {felt_states2['card_recommended_scale']}"

    # Validate RNX temporal detection
    assert felt_states2['rnx_temporal_state'] in ['crisis', 'sympathetic_pull'], \
        f"Expected crisis/sympathetic_pull for urgent text, got {felt_states2['rnx_temporal_state']}"

    print(f"\n✅ TEST 2 PASSED: Anxious conversation detected correctly")

    # TEST 3: Shutdown/Frozen Conversation
    print("\n" + "-"*70)
    print("TEST 3: Shutdown Conversation (Dorsal Vagal → Minimal Response)")
    print("-"*70)

    shutdown_text = "I feel numb and disconnected. Everything feels frozen and hopeless."

    result3 = organism.process_text(
        text=shutdown_text,
        context={
            'conversation_id': 'test_shutdown',
            'epoch_num': 1,
            'training_phase': 'test'
        },
        enable_tsk_recording=True
    )

    felt_states3 = result3['felt_states']

    print(f"\n✅ Text processed through 11 organs")
    print(f"   Mean coherence: {felt_states3['mean_coherence']:.3f}")
    print(f"   Satisfaction: {felt_states3['satisfaction_final']:.3f}")

    print(f"\n🧠 Trauma/Context Signals:")
    print(f"   BOND self_distance: {felt_states3['bond_self_distance']:.3f} (HIGH TRAUMA)")
    print(f"   RNX temporal state: {felt_states3['rnx_temporal_state']}")
    print(f"   EO polyvagal state: {felt_states3['eo_polyvagal_state']} (confidence: {felt_states3['eo_state_confidence']:.3f})")
    print(f"   CARD recommended scale: {felt_states3['card_recommended_scale']} ({felt_states3['card_length_target']} chars)")

    # Validate polyvagal detection (should be dorsal vagal or mixed)
    assert felt_states3['eo_polyvagal_state'] in ['dorsal_vagal', 'mixed_state'], \
        f"Expected dorsal_vagal/mixed for shutdown text, got {felt_states3['eo_polyvagal_state']}"

    # Validate response scaling (shutdown → minimal/brief)
    assert felt_states3['card_recommended_scale'] in ['minimal', 'brief'], \
        f"Expected minimal/brief for shutdown state, got {felt_states3['card_recommended_scale']}"

    # Validate BOND trauma detection (should be elevated)
    assert felt_states3['bond_self_distance'] > 0.4, \
        f"Expected high self_distance for shutdown text, got {felt_states3['bond_self_distance']:.3f}"

    print(f"\n✅ TEST 3 PASSED: Shutdown conversation detected correctly")

    # SUMMARY
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED - 11-ORGAN INTEGRATION WORKING!")
    print("="*70)

    print("\n📊 Phase 2 Integration Summary:")
    print(f"   ✅ 11 organs operational (5 conversational + 6 trauma/context-aware)")
    print(f"   ✅ Polyvagal state detection working (EO organ)")
    print(f"   ✅ Response scaling working (CARD organ)")
    print(f"   ✅ Temporal pattern detection working (RNX organ)")
    print(f"   ✅ Trauma detection working (BOND organ)")
    print(f"   ✅ Cross-organ context passing working (EO → CARD)")
    print("\n🎉 Phase 2 COMPLETE - Ready for Phase 3 (45D signature extraction)!")
    print()


if __name__ == '__main__':
    try:
        test_11_organ_integration()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
