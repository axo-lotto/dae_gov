"""
Test Crisis/Urgency Training Pairs
===================================

Validates that crisis/urgency training pairs successfully activate NDAM organ
and create urgency variation (currently 100% stable at 0.000).

Expected Outcomes:
- Urgency range: 0.0 → 0.15-0.9
- NDAM activation: 0% → 40-60%
- New families: Crisis Response, Protective Boundary, Stress Regulation
- Zone transitions: Zone 1 → 4, Zone 4 → 4
- Polyvagal: sympathetic activation

Date: November 17, 2025
Purpose: Phase 1.1 - Crisis/Urgency Corpus Validation
"""

import sys
import json
import numpy as np
from pathlib import Path
from collections import Counter

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.phase5_learning_integration import Phase5LearningIntegration

def test_crisis_urgency_training():
    """
    Test 50 crisis/urgency training pairs.

    Validates:
    - NDAM organ activation
    - Urgency variation (not all 0.000)
    - Zone 4 transformations increase
    - Sympathetic polyvagal state activation
    - Crisis Response family emergence
    """

    print("=" * 80)
    print("🚨 TESTING CRISIS/URGENCY TRAINING PAIRS")
    print("=" * 80)

    # Load crisis/urgency training pairs
    crisis_pairs_path = Path("knowledge_base/crisis_urgency_training_pairs.json")

    if not crisis_pairs_path.exists():
        print(f"\n❌ Crisis pairs file not found: {crisis_pairs_path}")
        return

    with open(crisis_pairs_path, 'r') as f:
        crisis_data = json.load(f)

    training_pairs = crisis_data['training_pairs']

    print(f"\n📊 Training Configuration:")
    print(f"   Total pairs: {len(training_pairs)}")
    print(f"   High urgency: {len([p for p in training_pairs if p['category'] == 'high_urgency'])}")
    print(f"   Moderate stress: {len([p for p in training_pairs if p['category'] == 'moderate_stress'])}")
    print(f"   De-escalation: {len([p for p in training_pairs if p['category'] == 'de_escalation'])}")

    # Initialize organism
    print(f"\n🔧 Initializing organism...")
    organism = ConversationalOrganismWrapper()

    # Initialize Phase 5 learning
    phase5 = Phase5LearningIntegration()

    # Process all pairs and collect metrics
    print(f"\n🔄 Processing {len(training_pairs)} crisis/urgency pairs...")

    urgency_values = []
    ndam_activations = []
    zone_transitions = []
    polyvagal_states = []
    nexus_types = []
    satisfaction_values = []

    for i, pair in enumerate(training_pairs):
        pair_id = pair['pair_id']
        user_input = pair['user_input']
        expected = pair['expected_felt_state']

        if (i + 1) % 10 == 0:
            print(f"   Processing pair {i+1}/{len(training_pairs)}...")

        try:
            # Process through organism
            result = organism.process_text(
                user_input,
                context={},
                user_id="crisis_test_user",
                enable_phase2=True,
                enable_tsk_recording=True
            )

            # Extract urgency
            urgency = result.get('ndam_urgency', 0.0)
            urgency_values.append(urgency)

            # Extract NDAM activation (organ coherence)
            organ_coherences = result.get('organ_coherences', {})
            ndam_coherence = organ_coherences.get('NDAM', 0.0)
            ndam_activations.append(ndam_coherence)

            # Extract zone
            zone = result.get('zone', 1)
            zone_transitions.append(zone)

            # Extract polyvagal state
            polyvagal = result.get('polyvagal_state', 'ventral_vagal')
            polyvagal_states.append(polyvagal)

            # Extract nexus type (from transduction trajectory)
            transduction_trajectory = result.get('transduction_trajectory', [])
            if transduction_trajectory:
                final_nexus = transduction_trajectory[-1].get('current_type', 'Unknown')
                nexus_types.append(final_nexus)

            # Extract satisfaction
            satisfaction = result.get('satisfaction', 0.5)
            satisfaction_values.append(satisfaction)

            # Update Phase 5 learning (family assignment)
            if 'transformation_signature' in result:
                phase5.update_from_conversation(
                    conversation_id=pair_id,
                    user_message=user_input,
                    emission_text=result.get('emission', ''),
                    felt_state=result,
                    satisfaction_score=satisfaction
                )

        except Exception as e:
            print(f"\n   ⚠️  Error processing {pair_id}: {e}")
            continue

    print(f"\n✅ Processed {len(urgency_values)} pairs successfully")

    # =============================================================================
    # ANALYSIS
    # =============================================================================

    print("\n" + "=" * 80)
    print("⚡ URGENCY VARIATION ANALYSIS")
    print("=" * 80)

    if urgency_values:
        print(f"\nUrgency Statistics (n={len(urgency_values)}):")
        print(f"   Mean: {np.mean(urgency_values):.3f}")
        print(f"   Std:  {np.std(urgency_values):.3f}")
        print(f"   Min:  {np.min(urgency_values):.3f}")
        print(f"   Max:  {np.max(urgency_values):.3f}")

        # Urgency bins
        low_urgency = sum(1 for u in urgency_values if u < 0.2)
        moderate_urgency = sum(1 for u in urgency_values if 0.2 <= u < 0.5)
        high_urgency = sum(1 for u in urgency_values if 0.5 <= u < 0.8)
        crisis_urgency = sum(1 for u in urgency_values if u >= 0.8)

        print(f"\nUrgency Distribution:")
        print(f"   Low (0.0-0.2): {low_urgency} ({100*low_urgency/len(urgency_values):.1f}%)")
        print(f"   Moderate (0.2-0.5): {moderate_urgency} ({100*moderate_urgency/len(urgency_values):.1f}%)")
        print(f"   High (0.5-0.8): {high_urgency} ({100*high_urgency/len(urgency_values):.1f}%)")
        print(f"   Crisis (0.8-1.0): {crisis_urgency} ({100*crisis_urgency/len(urgency_values):.1f}%)")

        # Success criteria
        urgency_std = np.std(urgency_values)
        print(f"\n✅ SUCCESS CRITERIA:")
        print(f"   [{'✅' if urgency_std > 0.25 else '❌'}] Urgency std > 0.25 (got {urgency_std:.3f})")
        print(f"   [{'✅' if np.max(urgency_values) > 0.5 else '❌'}] Max urgency > 0.5 (got {np.max(urgency_values):.3f})")

    print("\n" + "=" * 80)
    print("🧠 NDAM ORGAN ACTIVATION")
    print("=" * 80)

    if ndam_activations:
        print(f"\nNDAM Coherence Statistics (n={len(ndam_activations)}):")
        print(f"   Mean: {np.mean(ndam_activations):.3f}")
        print(f"   Std:  {np.std(ndam_activations):.3f}")
        print(f"   Min:  {np.min(ndam_activations):.3f}")
        print(f"   Max:  {np.max(ndam_activations):.3f}")

        # Activation rate (coherence > 0.3)
        activated = sum(1 for a in ndam_activations if a > 0.3)
        activation_rate = 100 * activated / len(ndam_activations)

        print(f"\nNDAM Activation Rate (coherence > 0.3):")
        print(f"   Activated: {activated}/{len(ndam_activations)} ({activation_rate:.1f}%)")

        print(f"\n✅ SUCCESS CRITERIA:")
        print(f"   [{'✅' if activation_rate >= 40 else '❌'}] Activation rate ≥40% (got {activation_rate:.1f}%)")

    print("\n" + "=" * 80)
    print("🌀 ZONE TRANSFORMATION PATTERNS")
    print("=" * 80)

    if zone_transitions:
        zone_counter = Counter(zone_transitions)
        print(f"\nFinal Zone Distribution (n={len(zone_transitions)}):")
        for zone, count in sorted(zone_counter.items()):
            pct = 100 * count / len(zone_transitions)
            print(f"   Zone {zone}: {count} ({pct:.1f}%)")

        zone_4_rate = 100 * zone_counter.get(4, 0) / len(zone_transitions)
        zone_5_rate = 100 * zone_counter.get(5, 0) / len(zone_transitions)

        print(f"\n✅ SUCCESS CRITERIA:")
        print(f"   [{'✅' if zone_4_rate >= 20 else '❌'}] Zone 4 ≥20% (got {zone_4_rate:.1f}%)")
        print(f"   [{'✅' if zone_5_rate >= 5 else '⚠️ '}] Zone 5 ≥5% (got {zone_5_rate:.1f}%)")

    print("\n" + "=" * 80)
    print("🧠 POLYVAGAL STATE DISTRIBUTION")
    print("=" * 80)

    if polyvagal_states:
        poly_counter = Counter(polyvagal_states)
        print(f"\nPolyvagal State Distribution (n={len(polyvagal_states)}):")
        for state, count in poly_counter.most_common():
            pct = 100 * count / len(polyvagal_states)
            print(f"   {state}: {count} ({pct:.1f}%)")

        sympathetic_rate = 100 * poly_counter.get('sympathetic', 0) / len(polyvagal_states)

        print(f"\n✅ SUCCESS CRITERIA:")
        print(f"   [{'✅' if sympathetic_rate >= 15 else '❌'}] Sympathetic ≥15% (got {sympathetic_rate:.1f}%)")

    print("\n" + "=" * 80)
    print("🔗 NEXUS TYPE PATTERNS")
    print("=" * 80)

    if nexus_types:
        nexus_counter = Counter(nexus_types)
        print(f"\nNexus Type Distribution (n={len(nexus_types)}):")
        for nexus, count in nexus_counter.most_common():
            pct = 100 * count / len(nexus_types)
            print(f"   {nexus}: {count} ({pct:.1f}%)")

        urgency_nexus_rate = 100 * nexus_counter.get('Urgency', 0) / len(nexus_types)
        protective_nexus_rate = 100 * nexus_counter.get('Protective', 0) / len(nexus_types)

        print(f"\n✅ SUCCESS CRITERIA:")
        print(f"   [{'✅' if urgency_nexus_rate > 0 else '❌'}] Urgency nexus observed (got {urgency_nexus_rate:.1f}%)")
        print(f"   [{'✅' if protective_nexus_rate > 0 else '❌'}] Protective nexus observed (got {protective_nexus_rate:.1f}%)")

    print("\n" + "=" * 80)
    print("😊 SATISFACTION ANALYSIS")
    print("=" * 80)

    if satisfaction_values:
        print(f"\nSatisfaction Statistics (n={len(satisfaction_values)}):")
        print(f"   Mean: {np.mean(satisfaction_values):.3f}")
        print(f"   Std:  {np.std(satisfaction_values):.3f}")
        print(f"   Min:  {np.min(satisfaction_values):.3f}")
        print(f"   Max:  {np.max(satisfaction_values):.3f}")

    print("\n" + "=" * 80)
    print("👥 FAMILY FORMATION ANALYSIS")
    print("=" * 80)

    # Check organic families
    families_path = Path("persona_layer/organic_families.json")
    if families_path.exists():
        with open(families_path, 'r') as f:
            families_data = json.load(f)

        total_families = families_data.get('total_families', 0)
        print(f"\nOrganic Families:")
        print(f"   Total families: {total_families}")

        # Check if crisis pairs are in families
        crisis_pair_ids = [p['pair_id'] for p in training_pairs]
        conversation_to_family = families_data.get('conversation_to_family', {})

        crisis_in_families = sum(1 for pair_id in crisis_pair_ids if pair_id in conversation_to_family)

        print(f"   Crisis pairs in families: {crisis_in_families}/{len(crisis_pair_ids)}")

        if crisis_in_families > 0:
            # Show family distribution
            crisis_family_counter = Counter([
                conversation_to_family[pair_id]
                for pair_id in crisis_pair_ids
                if pair_id in conversation_to_family
            ])

            print(f"\n   Crisis pair family distribution:")
            for family_id, count in crisis_family_counter.most_common(5):
                pct = 100 * count / crisis_in_families
                print(f"      {family_id}: {count} ({pct:.1f}%)")

    print("\n" + "=" * 80)
    print("✅ CRISIS/URGENCY TRAINING TEST COMPLETE")
    print("=" * 80)

    return {
        'urgency_values': urgency_values,
        'ndam_activations': ndam_activations,
        'zone_transitions': zone_transitions,
        'polyvagal_states': polyvagal_states,
        'nexus_types': nexus_types,
        'satisfaction_values': satisfaction_values
    }


if __name__ == '__main__':
    try:
        results = test_crisis_urgency_training()
        print(f"\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
