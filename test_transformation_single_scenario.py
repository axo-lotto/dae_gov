#!/usr/bin/env python3
"""
Test transformation signature implementation with single scenario.
Verifies initial state capture, transformation extraction, and family assignment.
"""

import sys
import os
import json

# Set PYTHONPATH
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_transformation_implementation():
    """Test transformation-based family learning with single scenario."""

    print("=" * 80)
    print("🧪 TESTING TRANSFORMATION SIGNATURE IMPLEMENTATION")
    print("=" * 80)

    # Initialize organism
    print("\n1️⃣  Initializing organism...")
    organism = ConversationalOrganismWrapper()

    # Enable Phase 5 learning
    if organism.phase5_learning:
        organism.phase5_learning.enable_learning = True
        print("   ✅ Organism initialized with Phase 5 learning enabled")
    else:
        print("   ❌ Phase 5 learning not available!")
        return False

    # Test with single scenario from IFS corpus (celebration/joy)
    test_input = "I just got the job! I can't believe it!"

    print(f"\n2️⃣  Processing test input: '{test_input}'")

    try:
        response = organism.process_text(
            text=test_input,
            context={'conversation_id': 'test_transformation_001'},
            enable_phase2=True
        )

        print("\n3️⃣  Processing complete - analyzing results...")

        # Extract results
        emission = response.get('emission_text', '')
        felt_states = response.get('felt_states', {})
        family_id = felt_states.get('phase5_family_id')
        confidence = response.get('emission_confidence', 0.0)
        v0_final = felt_states.get('v0_final', 0.0)

        print(f"\n📊 PROCESSING RESULTS:")
        print(f"   Emission: {emission[:80]}...")
        print(f"   Confidence: {confidence:.3f}")
        print(f"   V0 final: {v0_final:.3f}")
        print(f"   Family ID: {family_id}")

        # Check organic families file
        families_path = 'persona_layer/state/active/organic_families.json'

        if os.path.exists(families_path):
            with open(families_path) as f:
                families_data = json.load(f)
                families = families_data.get('families', {})

                print(f"\n📁 FAMILY FORMATION:")
                print(f"   Total families: {len(families)}")
                print(f"   Expected: 1 family (first conversation creates first family)")

                if family_id and family_id in families:
                    family = families[family_id]
                    print(f"\n🌀 {family_id.upper()} DETAILS:")
                    print(f"   Member count: {family['member_count']}")
                    print(f"   Maturity: {family['maturity']}")
                    print(f"   Avg satisfaction: {family['avg_satisfaction']:.3f}")
                    print(f"   Centroid shape: {len(family['centroid'])}D")

                    # Validate transformation signature dimensions
                    if len(family['centroid']) == 40:
                        print(f"   ✅ Centroid is 40D (transformation signature)")
                    else:
                        print(f"   ⚠️  Centroid is {len(family['centroid'])}D (expected 40D)")
        else:
            print(f"\n⚠️  Families file not found: {families_path}")

        # Validation checks
        print(f"\n✅ VALIDATION CHECKS:")
        checks_passed = 0
        total_checks = 6

        if emission and len(emission) > 0:
            print(f"   ✅ [1/6] Emission generated")
            checks_passed += 1
        else:
            print(f"   ❌ [1/6] Emission NOT generated")

        if confidence >= 0.3:
            print(f"   ✅ [2/6] Confidence ≥ 0.3 ({confidence:.3f})")
            checks_passed += 1
        else:
            print(f"   ❌ [2/6] Confidence < 0.3 ({confidence:.3f})")

        if v0_final < 1.0:
            print(f"   ✅ [3/6] V0 descent occurred ({v0_final:.3f})")
            checks_passed += 1
        else:
            print(f"   ❌ [3/6] No V0 descent ({v0_final:.3f})")

        if family_id:
            print(f"   ✅ [4/6] Family assigned ({family_id})")
            checks_passed += 1
        else:
            print(f"   ❌ [4/6] No family assigned")

        if os.path.exists(families_path):
            print(f"   ✅ [5/6] Families file exists")
            checks_passed += 1
        else:
            print(f"   ❌ [5/6] Families file missing")

        if family_id and os.path.exists(families_path):
            with open(families_path) as f:
                families_data = json.load(f)
                families = families_data.get('families', {})
                if family_id in families and len(families[family_id]['centroid']) == 40:
                    print(f"   ✅ [6/6] 40D transformation signature confirmed")
                    checks_passed += 1
                else:
                    print(f"   ❌ [6/6] Signature dimension mismatch")
        else:
            print(f"   ❌ [6/6] Cannot verify signature dimensions")

        print(f"\n{'='*80}")
        print(f"🎯 TEST RESULT: {checks_passed}/{total_checks} checks passed")

        if checks_passed == total_checks:
            print(f"✅ SUCCESS - Transformation implementation verified!")
            print(f"\n📋 NEXT STEP: Run full training with:")
            print(f"   python3 training/ifs_diversity_training.py --epochs 5 --reset")
            return True
        else:
            print(f"⚠️  PARTIAL SUCCESS - Review failed checks above")
            return False

    except Exception as e:
        print(f"\n❌ ERROR during processing:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_transformation_implementation()
    sys.exit(0 if success else 1)
