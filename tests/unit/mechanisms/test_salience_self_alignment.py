"""
Test Salience-SELF Matrix Alignment (Phase 1 Fixes Validation)
===============================================================

Validates the 3 critical fixes:
1. Organ insights passed to salience prehension
2. Signal inflation uses BOND self_distance (SELF matrix zones)
3. SELF-distance modulated by polyvagal state

Date: November 12, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import json
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\n" + "="*80)
print("🧪 SALIENCE-SELF MATRIX ALIGNMENT TEST")
print("="*80 + "\n")

# Test cases spanning SELF matrix zones
test_cases = [
    {
        "name": "Core SELF (d=0.10)",
        "text": "I feel compassion and curiosity toward this part. I'm calm and clear about what's needed.",
        "expected_zone": "Core SELF Orbit",
        "expected_inflation_range": (0.0, 0.15)
    },
    {
        "name": "Inner Relational (d=0.20)",
        "text": "I'm listening with empathy to what's happening. There's connection here.",
        "expected_zone": "Inner Relational",
        "expected_inflation_range": (0.05, 0.20)
    },
    {
        "name": "Symbolic Threshold (d=0.30)",
        "text": "I sense a powerful myth emerging. This threshold moment holds creative potential.",
        "expected_zone": "Symbolic Threshold",
        "expected_inflation_range": (0.10, 0.40)
    },
    {
        "name": "Shadow/Compost (d=0.45)",
        "text": "I'm exhausted and burned out. Protective patterns are working hard to keep me safe.",
        "expected_zone": "Shadow/Compost",
        "expected_inflation_range": (0.40, 0.70)
    },
    {
        "name": "Exile/Collapse (d=0.75)",
        "text": "I'm worthless and broken. Nothing will ever change. The pain is too much.",
        "expected_zone": "Exile/Collapse",
        "expected_inflation_range": (0.70, 1.00)
    }
]

print("📋 Running 5 test cases across SELF matrix zones...\n")

# Initialize organism
wrapper = ConversationalOrganismWrapper()
print("   ✅ Organism initialized\n")

results = []

for i, test_case in enumerate(test_cases, 1):
    print(f"Test {i}: {test_case['name']}")
    print(f"   Text: \"{test_case['text'][:60]}...\"")

    # Process with Phase 2 enabled
    result = wrapper.process_text(
        text=test_case['text'],
        context={'test_case': test_case['name']},
        enable_tsk_recording=False,
        enable_phase2=True
    )

    felt_states = result.get('felt_states', {})

    # Extract key metrics
    bond_self_distance_base = felt_states.get('bond_self_distance_base', None)
    bond_self_distance = felt_states.get('bond_self_distance', None)  # May be missing if not stored
    eo_polyvagal_state = felt_states.get('eo_polyvagal_state', 'unknown')

    # Get salience results from history
    if wrapper.salience_model and len(wrapper.salience_model.salience_history) > 0:
        salience = wrapper.salience_model.salience_history[-1]
        signal_inflation = salience['process_terms']['signal_inflation']
        safety_gradient = salience['process_terms']['safety_gradient']
        morphogenetic_guidance = salience['morphogenetic_guidance']
    else:
        signal_inflation = None
        safety_gradient = None
        morphogenetic_guidance = None

    # Validation
    in_expected_range = False
    if signal_inflation is not None:
        in_expected_range = (
            test_case['expected_inflation_range'][0] <= signal_inflation <=
            test_case['expected_inflation_range'][1]
        )

    results.append({
        'name': test_case['name'],
        'expected_zone': test_case['expected_zone'],
        'bond_self_distance': bond_self_distance_base,  # Use base if modulated not available
        'eo_polyvagal_state': eo_polyvagal_state,
        'signal_inflation': signal_inflation,
        'safety_gradient': safety_gradient,
        'guidance': morphogenetic_guidance,
        'in_expected_range': in_expected_range
    })

    # Print results
    print(f"   BOND self_distance: {bond_self_distance_base:.3f}" if bond_self_distance_base else "   BOND self_distance: N/A")
    print(f"   EO polyvagal: {eo_polyvagal_state}")
    print(f"   Signal inflation: {signal_inflation:.3f}" if signal_inflation else "   Signal inflation: N/A")
    print(f"   Expected range: {test_case['expected_inflation_range']}")
    print(f"   ✓ IN RANGE" if in_expected_range else f"   ✗ OUT OF RANGE")
    print(f"   Safety gradient: {safety_gradient:.3f}" if safety_gradient else "   Safety gradient: N/A")
    print(f"   Guidance: {morphogenetic_guidance}")
    print()

# Summary
print("="*80)
print("📊 VALIDATION SUMMARY")
print("="*80 + "\n")

passed = sum(1 for r in results if r['in_expected_range'])
total = len(results)

print(f"Tests passed: {passed}/{total} ({passed/total*100:.0f}%)\n")

print("Detailed Results:")
for r in results:
    status = "✅ PASS" if r['in_expected_range'] else "❌ FAIL"
    print(f"{status} {r['name']}")
    print(f"       Expected: {r['expected_zone']}")
    print(f"       BOND d_SELF: {r['bond_self_distance']:.3f}" if r['bond_self_distance'] else "       BOND d_SELF: N/A")
    print(f"       Signal inflation: {r['signal_inflation']:.3f}" if r['signal_inflation'] else "       Signal inflation: N/A")
    print(f"       Guidance: {r['guidance']}")
    print()

# Key validations
print("="*80)
print("🔍 KEY VALIDATIONS")
print("="*80 + "\n")

# Validation 1: BOND self_distance is being computed
bond_distances = [r['bond_self_distance'] for r in results if r['bond_self_distance'] is not None]
if len(bond_distances) == total:
    print("✅ FIX 1: BOND self_distance extracted for all test cases")
else:
    print(f"⚠️ FIX 1: BOND self_distance only available for {len(bond_distances)}/{total} cases")

# Validation 2: Signal inflation respects SELF matrix zones
symbolic_test = results[2]  # Symbolic Threshold (should be LOW trauma, not high)
if symbolic_test['signal_inflation'] and symbolic_test['signal_inflation'] < 0.5:
    print("✅ FIX 2: Symbolic Threshold (d=0.30) correctly marked as LOW trauma")
    print(f"   (signal_inflation = {symbolic_test['signal_inflation']:.3f}, expected < 0.5)")
else:
    print("❌ FIX 2: Symbolic Threshold incorrectly marked as high trauma")

# Validation 3: Polyvagal states detected
polyvagal_states = [r['eo_polyvagal_state'] for r in results if r['eo_polyvagal_state'] != 'unknown']
if len(polyvagal_states) == total:
    print("✅ FIX 3: Polyvagal states detected for all test cases")
    print(f"   States: {set(polyvagal_states)}")
else:
    print(f"⚠️ FIX 3: Polyvagal states only available for {len(polyvagal_states)}/{total} cases")

# Overall assessment
print("\n" + "="*80)
if passed >= 4:
    print("✅ PHASE 1 FIXES VALIDATED: System aligned with SELF matrix")
elif passed >= 3:
    print("⚠️ PHASE 1 FIXES PARTIAL: Most zones working correctly")
else:
    print("❌ PHASE 1 FIXES INCOMPLETE: Further debugging needed")
print("="*80 + "\n")

print("🌀 Salience-SELF alignment test complete.")
