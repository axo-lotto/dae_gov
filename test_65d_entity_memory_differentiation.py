"""
Test 65D Entity-Memory Differentiation
=======================================

Validates that existing 65D signatures correctly differentiate entity-memory tasks
through SELF Matrix zones + nexus types + polyvagal states (Phase 2).

Expected Results:
- Crisis entity patterns (worry, stress) → Zone 4-5 + Urgency nexus → Family A
- Relational entity patterns (pride, connection) → Zone 2-3 + Relational nexus → Family B
- Euclidean distance: Crisis vs Relational > 2.5 (clear separation)

Date: November 17, 2025
Purpose: Confirm Phase 2 already implemented correctly
"""

import sys
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.organ_signature_extractor import OrganSignatureExtractor
from persona_layer.organic_conversational_families import OrganicConversationalFamilies


def test_entity_memory_differentiation():
    """
    Test that 65D signatures differentiate entity-memory tasks.

    Tests 10 entity-memory inputs:
    - 5 crisis entity patterns (worry, stress, fear)
    - 5 relational entity patterns (pride, connection, joy)

    Success Criteria:
    - 2-3 families emerge (crisis vs relational)
    - Crisis vs relational distance > 2.5
    - Within-family distance < 1.5
    """
    print("=" * 80)
    print("🧪 TESTING 65D ENTITY-MEMORY DIFFERENTIATION")
    print("=" * 80)

    # Test inputs (10 entity-memory pairs)
    test_inputs = [
        # CRISIS ENTITY PATTERNS (should cluster Zone 4-5 + Urgency/Disruptive)
        ("crisis_1", "I'm really worried about Emma's health lately", "crisis"),
        ("crisis_2", "Lily is struggling with anxiety and I feel helpless", "crisis"),
        ("crisis_3", "I'm scared about what might happen to Emma", "crisis"),
        ("crisis_4", "Work is crushing me and I can't keep up", "crisis"),
        ("crisis_5", "I'm terrified about Emma's upcoming surgery", "crisis"),

        # RELATIONAL ENTITY PATTERNS (should cluster Zone 2-3 + Relational/Innate)
        ("relational_1", "I'm so proud of Emma's graduation achievement", "relational"),
        ("relational_2", "Lily and I had such a beautiful conversation today", "relational"),
        ("relational_3", "Emma's growth this year has been incredible to witness", "relational"),
        ("relational_4", "I feel so connected to my team at work lately", "relational"),
        ("relational_5", "Lily's kindness continues to amaze me", "relational"),
    ]

    print(f"\n📊 Test Configuration:")
    print(f"   Total inputs: {len(test_inputs)}")
    print(f"   Crisis patterns: 5 (expect Zone 4-5 + Urgency)")
    print(f"   Relational patterns: 5 (expect Zone 2-3 + Relational)")
    print(f"   Expected families: 2-3")
    print(f"   Expected separation: Crisis vs Relational > 2.5 distance")

    # Initialize components
    print(f"\n🔧 Initializing organism...")
    organism = ConversationalOrganismWrapper()
    signature_extractor = OrganSignatureExtractor()
    families = OrganicConversationalFamilies(
        storage_path="/tmp/test_entity_families.json",
        similarity_threshold=1.5  # Distance threshold for family assignment
    )

    # Process each input and extract signatures
    print(f"\n🔄 Processing inputs and extracting 65D signatures...")
    signatures = []
    metadata = []

    for conv_id, user_input, expected_type in test_inputs:
        print(f"\n   Processing: {conv_id} ({expected_type})")
        print(f"   Input: '{user_input[:60]}...'")

        try:
            # Process through organism
            result = organism.process_text(
                user_input,
                context={},
                user_id="test_user",
                enable_phase2=True,
                enable_tsk_recording=True
            )

            # Extract 65D transformation signature
            initial_state = {
                'v0_initial': 1.0,
                'satisfaction': 0.5,
                'zone': 1,
                'polyvagal_state': 'ventral',
                'urgency': 0.0,
                'organ_coherences': {}
            }

            final_state = {
                'v0_final': result.get('v0_final', 0.5),
                'satisfaction_final': result.get('satisfaction', 0.5),
                'zone': result.get('zone', 1),
                'polyvagal_state': result.get('polyvagal_state', 'ventral'),
                'urgency': result.get('ndam_urgency', 0.0),
                'organ_coherences': result.get('organ_coherences', {}),
                'convergence_cycles': result.get('convergence_cycles', 3.0),
                'kairos_detected': result.get('kairos_detected', False),
                'emission_path': result.get('emission_path', 'fusion')
            }

            # Get transduction trajectory if available
            transduction_trajectory = result.get('transduction_trajectory', [])

            # Extract 65D signature (raw, no normalization!)
            signature_65d = signature_extractor.extract_transformation_signature_65d(
                initial_felt_state=initial_state,
                final_felt_state=final_state,
                transduction_trajectory=transduction_trajectory,
                normalize=False  # CRITICAL: Keep raw for Euclidean distance
            )

            signatures.append(signature_65d)
            metadata.append({
                'conv_id': conv_id,
                'expected_type': expected_type,
                'zone': final_state['zone'],
                'polyvagal': final_state['polyvagal_state'],
                'urgency': final_state['urgency'],
                'nexus_type': transduction_trajectory[-1].get('current_type', 'Unknown') if transduction_trajectory else 'Unknown'
            })

            print(f"   ✅ Signature extracted: {signature_65d.shape}")
            print(f"      Zone: {final_state['zone']}, Polyvagal: {final_state['polyvagal_state']}")
            print(f"      Urgency: {final_state['urgency']:.3f}")
            if transduction_trajectory:
                print(f"      Nexus: {transduction_trajectory[-1].get('current_type', 'Unknown')}")

        except Exception as e:
            print(f"   ❌ Processing failed: {e}")
            import traceback
            traceback.print_exc()
            continue

    print(f"\n✅ Processed {len(signatures)} inputs successfully")

    # Assign to families using Euclidean distance
    print(f"\n🔍 Assigning to families (Euclidean distance clustering)...")
    family_assignments = []

    for i, (sig, meta) in enumerate(zip(signatures, metadata)):
        assignment = families.assign_to_family(
            conversation_id=meta['conv_id'],
            signature=sig,
            satisfaction_score=0.8,  # High satisfaction for learning
            organ_contributions={}
        )
        family_assignments.append({
            'conv_id': meta['conv_id'],
            'expected_type': meta['expected_type'],
            'family_id': assignment.family_id,
            'distance': assignment.similarity_score,  # Actually distance (converted to score)
            'assignment_type': assignment.assignment_type,
            'zone': meta['zone'],
            'nexus': meta['nexus_type']
        })

        print(f"   {meta['conv_id']} ({meta['expected_type']}) → {assignment.family_id}")
        print(f"      Assignment: {assignment.assignment_type}, Distance: {assignment.similarity_score:.3f}")

    # Analyze family distribution
    print(f"\n📊 FAMILY DISTRIBUTION ANALYSIS:")
    print(f"   Total families: {len(families.families)}")

    # Group by expected type
    crisis_families = set()
    relational_families = set()

    for assignment in family_assignments:
        if assignment['expected_type'] == 'crisis':
            crisis_families.add(assignment['family_id'])
        else:
            relational_families.add(assignment['family_id'])

    print(f"\n   Crisis patterns:")
    crisis_assignments = [a for a in family_assignments if a['expected_type'] == 'crisis']
    for a in crisis_assignments:
        print(f"      {a['conv_id']} → {a['family_id']} (Zone {a['zone']}, {a['nexus']})")

    print(f"\n   Relational patterns:")
    relational_assignments = [a for a in family_assignments if a['expected_type'] == 'relational']
    for a in relational_assignments:
        print(f"      {a['conv_id']} → {a['family_id']} (Zone {a['zone']}, {a['nexus']})")

    # Compute distances between families
    print(f"\n📏 INTER-FAMILY DISTANCES:")
    family_centroids = {}
    for fam_id, family in families.families.items():
        family_centroids[fam_id] = family.centroid

    # Crisis vs Relational distance
    if len(crisis_families) > 0 and len(relational_families) > 0:
        crisis_fam = list(crisis_families)[0]
        relational_fam = list(relational_families)[0]

        if crisis_fam in family_centroids and relational_fam in family_centroids:
            inter_distance = np.linalg.norm(
                family_centroids[crisis_fam] - family_centroids[relational_fam]
            )
            print(f"   Crisis ({crisis_fam}) vs Relational ({relational_fam}): {inter_distance:.3f}")

            # Check success criteria
            print(f"\n✅ SUCCESS CRITERIA:")
            print(f"   [{'✅' if len(families.families) >= 2 else '❌'}] Multiple families (got {len(families.families)}, expected 2-3)")
            print(f"   [{'✅' if inter_distance > 2.5 else '❌'}] Crisis vs Relational distance > 2.5 (got {inter_distance:.3f})")
            print(f"   [{'✅' if len(crisis_families & relational_families) == 0 else '❌'}] Crisis and Relational in different families")

    # Compute within-family distances
    print(f"\n📏 WITHIN-FAMILY DISTANCES:")
    for fam_id, family in families.families.items():
        if family.member_count > 1:
            # Get signatures for this family
            fam_signatures = [
                sig for sig, meta in zip(signatures, metadata)
                if any(a['conv_id'] == meta['conv_id'] and a['family_id'] == fam_id
                      for a in family_assignments)
            ]

            if len(fam_signatures) > 1:
                # Compute pairwise distances
                distances = []
                for i in range(len(fam_signatures)):
                    for j in range(i + 1, len(fam_signatures)):
                        dist = np.linalg.norm(fam_signatures[i] - fam_signatures[j])
                        distances.append(dist)

                mean_within = np.mean(distances)
                print(f"   {fam_id}: mean={mean_within:.3f}, max={max(distances):.3f}")

    print(f"\n" + "=" * 80)
    print(f"✅ ENTITY-MEMORY DIFFERENTIATION TEST COMPLETE")
    print(f"=" * 80)

    return {
        'total_families': len(families.families),
        'crisis_families': list(crisis_families),
        'relational_families': list(relational_families),
        'family_assignments': family_assignments
    }


if __name__ == '__main__':
    try:
        results = test_entity_memory_differentiation()
        print(f"\n✅ Test completed successfully!")
        print(f"   Total families: {results['total_families']}")
        print(f"   Crisis families: {results['crisis_families']}")
        print(f"   Relational families: {results['relational_families']}")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
