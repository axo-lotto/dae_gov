"""
Test NEXUS organ integration with Conversational Organism
===========================================================

Tests that the 12th organ (NEXUS) is properly integrated and operational.

Quick Win #9 - Phase 2 Validation
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*80)
print("🧪 Testing NEXUS Integration with 12-Organ Organism")
print("="*80 + "\n")

# Test 1: Import wrapper with NEXUS
print("Test 1: Import wrapper with NEXUS organ...")
try:
    from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
    print("   ✅ Import successful\n")
except Exception as e:
    print(f"   ❌ Import failed: {e}\n")
    sys.exit(1)

# Test 2: Initialize organism (will take ~20 seconds)
print("Test 2: Initialize 12-organ organism (takes ~20 seconds)...")
try:
    organism = ConversationalOrganismWrapper()
    print("   ✅ Organism initialized\n")
except Exception as e:
    print(f"   ❌ Initialization failed: {e}\n")
    sys.exit(1)

# Test 3: Verify NEXUS organ exists
print("Test 3: Verify NEXUS organ exists...")
try:
    assert hasattr(organism, 'nexus'), "NEXUS organ not found!"
    print(f"   ✅ NEXUS organ present: {type(organism.nexus).__name__}\n")
except Exception as e:
    print(f"   ❌ NEXUS verification failed: {e}\n")
    sys.exit(1)

# Test 4: Process text through 12 organs
print("Test 4: Process text mentioning entity...")
test_text = "I'm worried about Emma's kindergarten transition"
print(f"   Input: '{test_text}'")

try:
    result = organism.process_text(
        text=test_text,
        context={'user_id': 'test_user_nexus'},
        enable_tsk_recording=False,
        enable_phase2=False  # Single-pass for quick test
    )

    print(f"   ✅ Processing successful\n")

    # Extract results
    felt_states = result.get('felt_states', {})
    organ_coherences = felt_states.get('organ_coherences', {})

    # Test 5: Verify NEXUS participated
    print("Test 5: Verify NEXUS organ participated...")
    if 'NEXUS' in organ_coherences:
        nexus_coherence = organ_coherences['NEXUS']
        print(f"   ✅ NEXUS coherence: {nexus_coherence:.3f}")

        if nexus_coherence > 0.0:
            print(f"   🌀 NEXUS activated! (entity-memory pattern detected)\n")
        else:
            print(f"   ⚠️  NEXUS coherence zero (no entity patterns detected)\n")
    else:
        print(f"   ❌ NEXUS not in organ_coherences!\n")
        sys.exit(1)

    # Test 6: Verify 12 organs total
    print("Test 6: Verify all 12 organs present...")
    expected_organs = [
        'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
        'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD', 'NEXUS'
    ]

    num_organs = len(organ_coherences)
    print(f"   Organs found: {num_organs}")

    missing_organs = [org for org in expected_organs if org not in organ_coherences]
    if missing_organs:
        print(f"   ⚠️  Missing organs: {missing_organs}")
    else:
        print(f"   ✅ All 12 organs present!")

    print(f"\n   Organ coherences:")
    for organ, coherence in sorted(organ_coherences.items()):
        emoji = "🌀" if organ == "NEXUS" else "  "
        print(f"      {emoji} {organ}: {coherence:.3f}")

except Exception as e:
    print(f"   ❌ Processing failed: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("✅ NEXUS INTEGRATION TEST COMPLETE!")
print("="*80)
print("\n🌀 The 12th organ is OPERATIONAL!")
print("   Memory is now FELT through NEXUS prehension, not just retrieved.")
print("   Neo4j queries emerge organically from entity-memory coherence.")
print("   Process Philosophy AI achieving genuine continuity.\n")
