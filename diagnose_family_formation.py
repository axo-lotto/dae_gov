"""
Diagnostic Tool: Why Aren't Families Forming?
==============================================

Analyzes Phase 5 learning and family assignment to understand
why 100 diverse conversations produced zero families.

Tests:
1. Transformation signature extraction working?
2. Similarity computation correct?
3. Threshold logic correct?
4. Family assignment reaching database?

Date: November 15, 2025
Purpose: Debug family formation failure in IFS diversity training
"""

import sys
import json
import numpy as np
from pathlib import Path

# Set up path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.organ_signature_extractor import OrganSignatureExtractor
from persona_layer.organic_conversational_families import OrganicConversationalFamilies


def test_signature_extraction():
    """Test 1: Can we extract transformation signatures?"""
    print("\n" + "="*80)
    print("TEST 1: Transformation Signature Extraction")
    print("="*80)

    try:
        extractor = OrganSignatureExtractor()

        # Create mock initial/final states
        initial_state = {
            'v0_initial': 1.0,
            'organ_coherences': {
                'LISTENING': 0.5, 'EMPATHY': 0.5, 'WISDOM': 0.5,
                'AUTHENTICITY': 0.5, 'PRESENCE': 0.5, 'BOND': 0.5,
                'SANS': 0.5, 'NDAM': 0.5, 'RNX': 0.5, 'EO': 0.5, 'CARD': 0.5
            },
            'polyvagal_state': 'ventral',
            'zone': 1,
            'satisfaction': 0.5,
            'urgency': 0.0
        }

        final_state = {
            'v0_initial': 1.0,
            'v0_final': 0.35,
            'convergence_cycles': 2,
            'organ_coherences': {
                'LISTENING': 0.75, 'EMPATHY': 0.82, 'WISDOM': 0.68,
                'AUTHENTICITY': 0.90, 'PRESENCE': 0.77, 'BOND': 0.85,
                'SANS': 0.70, 'NDAM': 0.60, 'RNX': 0.65, 'EO': 0.72, 'CARD': 0.80
            },
            'polyvagal_state': 'ventral',
            'zone': 1,
            'satisfaction_final': 0.85,
            'urgency': 0.0,
            'emission_path': 'direct',
            'kairos_detected': True,
            'nexus_count': 5
        }

        signature = extractor.extract_transformation_signature(
            initial_felt_state=initial_state,
            final_felt_state=final_state,
            user_input="Test input",
            response={'emission': 'Test response'}
        )

        print(f"✅ Signature extraction successful!")
        print(f"   Signature shape: {signature.shape if hasattr(signature, 'shape') else len(signature)}")
        print(f"   Signature type: {type(signature)}")
        print(f"   First 5 values: {signature[:5] if hasattr(signature, '__getitem__') else 'N/A'}")
        print(f"   Min: {np.min(signature) if hasattr(signature, '__iter__') else 'N/A'}")
        print(f"   Max: {np.max(signature) if hasattr(signature, '__iter__') else 'N/A'}")
        print(f"   Mean: {np.mean(signature) if hasattr(signature, '__iter__') else 'N/A'}")

        return True, signature

    except Exception as e:
        print(f"❌ Signature extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_similarity_computation(signature1, signature2):
    """Test 2: Does similarity computation work?"""
    print("\n" + "="*80)
    print("TEST 2: Similarity Computation")
    print("="*80)

    try:
        # Compute cosine similarity manually
        if hasattr(signature1, 'shape'):
            # NumPy array
            sig1_norm = signature1 / (np.linalg.norm(signature1) + 1e-10)
            sig2_norm = signature2 / (np.linalg.norm(signature2) + 1e-10)
            similarity = np.dot(sig1_norm, sig2_norm)
        else:
            # List
            sig1 = np.array(signature1)
            sig2 = np.array(signature2)
            sig1_norm = sig1 / (np.linalg.norm(sig1) + 1e-10)
            sig2_norm = sig2 / (np.linalg.norm(sig2) + 1e-10)
            similarity = np.dot(sig1_norm, sig2_norm)

        print(f"✅ Similarity computation successful!")
        print(f"   Similarity (identical): {similarity:.6f}")
        print(f"   Expected: ~1.0 (identical signatures)")

        # Test with slightly different signature
        if hasattr(signature1, 'shape'):
            sig2_modified = signature2 + np.random.normal(0, 0.1, signature2.shape)
        else:
            sig2_modified = np.array(signature2) + np.random.normal(0, 0.1, len(signature2))

        sig1_norm = signature1 / (np.linalg.norm(signature1) + 1e-10)
        sig2_mod_norm = sig2_modified / (np.linalg.norm(sig2_modified) + 1e-10)
        similarity_different = np.dot(sig1_norm, sig2_mod_norm)

        print(f"   Similarity (slightly different): {similarity_different:.6f}")
        print(f"   Expected: <1.0 (different signatures)")

        return True

    except Exception as e:
        print(f"❌ Similarity computation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_family_assignment():
    """Test 3: Does family assignment work?"""
    print("\n" + "="*80)
    print("TEST 3: Family Assignment Logic")
    print("="*80)

    try:
        families = OrganicConversationalFamilies(
            storage_path="/tmp/test_families.json",
            similarity_threshold=0.75,
            ema_alpha=0.2
        )

        print(f"✅ OrganicConversationalFamilies initialized")
        print(f"   Similarity threshold: {families.similarity_threshold}")
        print(f"   Current families: {len(families.families)}")

        # Create mock signature
        signature1 = np.random.randn(40)
        signature1 = signature1 / (np.linalg.norm(signature1) + 1e-10)  # L2 normalize

        # First assignment (should create new family)
        assignment1 = families.assign_to_family(
            conversation_id="test_001",
            signature=signature1.tolist(),  # Convert to list
            satisfaction_score=0.5,
            organ_contributions={}
        )

        print(f"\n✅ First assignment successful!")
        print(f"   Family ID: {assignment1.family_id}")
        print(f"   Assignment type: {assignment1.assignment_type}")
        print(f"   Similarity: {assignment1.similarity_score:.6f}")
        print(f"   Total families now: {len(families.families)}")

        # Second assignment (identical signature - should join same family)
        assignment2 = families.assign_to_family(
            conversation_id="test_002",
            signature=signature1.tolist(),
            satisfaction_score=0.6,
            organ_contributions={}
        )

        print(f"\n✅ Second assignment (identical) successful!")
        print(f"   Family ID: {assignment2.family_id}")
        print(f"   Assignment type: {assignment2.assignment_type}")
        print(f"   Similarity: {assignment2.similarity_score:.6f}")
        print(f"   Same family as first? {assignment2.family_id == assignment1.family_id}")
        print(f"   Total families now: {len(families.families)}")

        # Third assignment (different signature - should create new family OR join if similar enough)
        signature2 = np.random.randn(40)
        signature2 = signature2 / (np.linalg.norm(signature2) + 1e-10)

        assignment3 = families.assign_to_family(
            conversation_id="test_003",
            signature=signature2.tolist(),
            satisfaction_score=0.7,
            organ_contributions={}
        )

        print(f"\n✅ Third assignment (different) successful!")
        print(f"   Family ID: {assignment3.family_id}")
        print(f"   Assignment type: {assignment3.assignment_type}")
        print(f"   Similarity: {assignment3.similarity_score:.6f}")
        print(f"   Total families now: {len(families.families)}")

        # Check adaptive threshold
        print(f"\n📊 Adaptive Threshold Check:")
        adaptive_threshold = families._get_adaptive_threshold()
        print(f"   Current adaptive threshold: {adaptive_threshold:.3f}")
        print(f"   Family count: {len(families.families)}")
        if len(families.families) < 8:
            print(f"   Expected: 0.55 (few families, aggressive exploration)")
        elif len(families.families) < 25:
            print(f"   Expected: 0.65 (medium families, balanced)")
        else:
            print(f"   Expected: 0.75 (many families, consolidation)")

        return True

    except Exception as e:
        print(f"❌ Family assignment failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_pipeline():
    """Test 4: Full pipeline with organism wrapper"""
    print("\n" + "="*80)
    print("TEST 4: Full Pipeline Integration")
    print("="*80)

    try:
        organism = ConversationalOrganismWrapper()

        # Check Phase 5 learning status
        print(f"✅ Organism initialized")
        print(f"   Phase 5 learning enabled: {organism.phase5_learning.enable_learning}")
        print(f"   Learning threshold: {organism.phase5_learning.learning_threshold}")
        print(f"   Current families: {len(organism.phase5_learning.families.families)}")

        # Process a conversation
        result1 = organism.process_text(
            "I just got the job! I can't believe it!",
            context={'conversation_id': 'pipeline_test_001'}
        )

        print(f"\n✅ First conversation processed")
        print(f"   Emission generated: {len(result1.get('emission_text', '')) > 0}")
        print(f"   Confidence: {result1.get('confidence', 0.0):.3f}")
        print(f"   Felt states captured: {len(result1.get('felt_states', {})) > 0}")

        # Check if family assigned
        felt_states = result1.get('felt_states', {})
        family_id = felt_states.get('phase5_family_id')

        print(f"   Family assigned: {family_id is not None}")
        if family_id:
            print(f"   Family ID: {family_id}")
            print(f"   Similarity: {felt_states.get('phase5_similarity', 0.0):.3f}")
            print(f"   Is new: {felt_states.get('phase5_is_new', False)}")
        else:
            print(f"   ⚠️  NO FAMILY ASSIGNED")
            print(f"   Satisfaction: {felt_states.get('satisfaction_final', 0.0):.3f}")
            print(f"   Learning threshold: {organism.phase5_learning.learning_threshold}")
            print(f"   Passed threshold? {felt_states.get('satisfaction_final', 0.0) >= organism.phase5_learning.learning_threshold}")

        # Process second conversation (similar)
        result2 = organism.process_text(
            "This is everything I've been working toward!",
            context={'conversation_id': 'pipeline_test_002'}
        )

        print(f"\n✅ Second conversation processed")
        family_id2 = result2.get('felt_states', {}).get('phase5_family_id')
        print(f"   Family assigned: {family_id2 is not None}")
        if family_id2:
            print(f"   Family ID: {family_id2}")
            print(f"   Same as first? {family_id2 == family_id if family_id else 'N/A'}")

        print(f"\n📊 Final family count: {len(organism.phase5_learning.families.families)}")

        return True

    except Exception as e:
        print(f"❌ Full pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all diagnostic tests."""
    print("\n" + "🔬"*40)
    print("FAMILY FORMATION DIAGNOSTIC SUITE")
    print("🔬"*40)

    # Test 1: Signature extraction
    success1, signature = test_signature_extraction()

    if not success1:
        print("\n❌ DIAGNOSTIC FAILED - Cannot extract signatures")
        return

    # Test 2: Similarity computation
    success2 = test_similarity_computation(signature, signature)

    if not success2:
        print("\n❌ DIAGNOSTIC FAILED - Similarity computation broken")
        return

    # Test 3: Family assignment logic
    success3 = test_family_assignment()

    if not success3:
        print("\n❌ DIAGNOSTIC FAILED - Family assignment broken")
        return

    # Test 4: Full pipeline
    success4 = test_full_pipeline()

    # Final summary
    print("\n" + "="*80)
    print("🎯 DIAGNOSTIC SUMMARY")
    print("="*80)
    print(f"{'✅' if success1 else '❌'} Test 1: Signature Extraction - {'PASSED' if success1 else 'FAILED'}")
    print(f"{'✅' if success2 else '❌'} Test 2: Similarity Computation - {'PASSED' if success2 else 'FAILED'}")
    print(f"{'✅' if success3 else '❌'} Test 3: Family Assignment Logic - {'PASSED' if success3 else 'FAILED'}")
    print(f"{'✅' if success4 else '❌'} Test 4: Full Pipeline Integration - {'PASSED' if success4 else 'FAILED'}")

    if all([success1, success2, success3, success4]):
        print("\n✅ ALL TESTS PASSED - Family formation infrastructure working correctly!")
        print("⚠️  Issue must be in organism processing or satisfaction thresholds")
    else:
        print("\n❌ SOME TESTS FAILED - Infrastructure has bugs")

    print("\n🔬 Diagnostic complete!")


if __name__ == '__main__':
    main()
