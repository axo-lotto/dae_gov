#!/usr/bin/env python3
"""
Test Phase 1 Emission Fix - Validate nexus formation with direct atom activations
==================================================================================

This test validates that:
1. All 11 organs compute atom_activations directly
2. Nexuses form from organ intersections
3. Emission generation succeeds

Expected: Nexus count ≥ 5, Emission text != None
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_phase1_fix():
    """Test that Phase 1 emission fix works end-to-end."""

    print("\n" + "="*70)
    print("🧪 PHASE 1 EMISSION FIX VALIDATION TEST")
    print("="*70 + "\n")

    # Initialize wrapper
    wrapper = ConversationalOrganismWrapper()

    # Test text (therapeutic response with rich organ activations)
    test_text = """
    I hear the exhaustion in your words. This level of depletion isn't sustainable.
    When a team is burning out, it's a sign the system needs adjustment, not that people
    need to try harder. Let's take a moment to ground together and explore what boundaries
    might help protect your team's wellbeing and create space for recovery.
    """

    print("📝 Processing therapeutic response text:")
    print(f"   Text: \"{test_text.strip()[:80]}...\"")
    print()

    result = wrapper.process_text(
        text=test_text,
        context={
            'conversation_id': 'phase1_validation',
            'training_phase': 'test'
        },
        enable_tsk_recording=True
    )

    felt_states = result['felt_states']

    print("✅ Processing complete!")
    print()

    # Validation 1: Check organ coherences
    print("🔍 Validation 1: Organ Coherences")
    organ_coherences = felt_states['organ_coherences']
    print(f"   Organs with coherence: {len(organ_coherences)}/11")
    for organ, coherence in organ_coherences.items():
        print(f"     {organ:15s}: {coherence:.3f}")
    print()

    # Validation 2: Check emission generation
    print("🔍 Validation 2: Emission Generation")
    emission_nexus_count = felt_states.get('emission_nexus_count', 0)
    emission_text = felt_states.get('emission_text', None)
    emission_confidence = felt_states.get('emission_confidence', 0.0)
    emission_path = felt_states.get('emission_path', 'none')

    print(f"   Nexus count: {emission_nexus_count}")
    print(f"   Emission text: {emission_text[:80] if emission_text else 'None'}...")
    print(f"   Emission confidence: {emission_confidence:.3f}")
    print(f"   Emission path: {emission_path}")
    print()

    # Validation criteria
    print("🎯 Validation Results:")
    print("="*70)

    success = True

    # Criterion 1: Nexus count ≥ 5 (was 0 before fix)
    if emission_nexus_count >= 5:
        print(f"   ✅ PASS: Nexus count = {emission_nexus_count} (≥5)")
    else:
        print(f"   ❌ FAIL: Nexus count = {emission_nexus_count} (<5)")
        success = False

    # Criterion 2: Emission text generated
    if emission_text:
        print(f"   ✅ PASS: Emission text generated ({len(emission_text)} chars)")
    else:
        print(f"   ❌ FAIL: No emission text generated")
        success = False

    # Criterion 3: Emission confidence ≥ 0.6
    if emission_confidence >= 0.6:
        print(f"   ✅ PASS: Emission confidence = {emission_confidence:.3f} (≥0.6)")
    else:
        print(f"   ⚠️  WARN: Emission confidence = {emission_confidence:.3f} (<0.6)")

    # Criterion 4: Multiple organs participate (≥3)
    organs_with_coherence = sum(1 for c in organ_coherences.values() if c > 0)
    if organs_with_coherence >= 3:
        print(f"   ✅ PASS: {organs_with_coherence} organs participate (≥3)")
    else:
        print(f"   ⚠️  WARN: Only {organs_with_coherence} organs participate (<3)")

    print("="*70)

    if success:
        print("\n🎉 ✅ PHASE 1 EMISSION FIX: SUCCESS!")
        print("   - Nexuses form correctly from direct atom activations")
        print("   - Emission generation works end-to-end")
        print("   - The '0 nexuses' problem is SOLVED ✨")
    else:
        print("\n❌ PHASE 1 EMISSION FIX: FAILED")
        print("   - Issue: Nexuses or emission generation not working")
        print("   - Check organ atom_activations and semantic field building")

    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    test_phase1_fix()
