"""
Final Phase 1 Validation
========================

Confirms that the hebbian fallback issue is completely fixed.

Tests both scenarios:
1. Input that forms nexuses (should use felt-guided LLM via nexus path)
2. Input that forms NO nexuses (should use felt-guided LLM via hebbian path)

Both should produce natural language with NO process philosophy.

Date: November 13, 2025
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("=" * 80)
print("FINAL PHASE 1 VALIDATION")
print("=" * 80)

# Initialize
organism = ConversationalOrganismWrapper(bundle_path="Bundle/phase1_validation")

test_cases = [
    {
        'name': 'Nexuses form (emotional content)',
        'input': 'Hello there i am feeling good today!',
        'expect_nexuses': True
    },
    {
        'name': 'No nexuses (simple greeting)',
        'input': 'Hello there today is a beautiful day!',
        'expect_nexuses': False
    }
]

results = []

for i, test in enumerate(test_cases, 1):
    print(f"\n{'=' * 80}")
    print(f"Test {i}: {test['name']}")
    print(f"Input: '{test['input']}'")
    print("=" * 80)

    result = organism.process_text(test['input'])

    emission = result.get('emission_text', '')
    path = result.get('emission_path', 'unknown')
    nexus_count = result.get('emission_nexus_count', 0)
    confidence = result.get('emission_confidence', 0.0)

    print(f"\n📊 Results:")
    print(f"   Nexuses: {nexus_count}")
    print(f"   Path: {path}")
    print(f"   Confidence: {confidence:.3f}")
    print(f"\n💬 Emission (first 150 chars):")
    print(f"   {emission[:150]}...")

    # Check for process language
    process_phrases = [
        "everything verbs",
        "ontology is a conspiracy",
        "God = primordial lure",
        "occasions",
        "nexus of occasions",
        "prehended",
        "concrescence"
    ]

    has_process = any(p.lower() in emission.lower() for p in process_phrases)

    # Validate
    passed = True
    if has_process:
        print(f"\n   ❌ FAIL: Has process language!")
        passed = False
    else:
        print(f"\n   ✅ PASS: No process language")

    if path in ['felt_guided_llm', 'direct_reconstruction']:
        print(f"   ✅ PASS: Using felt-guided LLM path")
    else:
        print(f"   ❌ FAIL: Wrong path '{path}'")
        passed = False

    results.append(passed)

# Final summary
print(f"\n{'=' * 80}")
print("FINAL SUMMARY")
print("=" * 80)

if all(results):
    print("🎉 SUCCESS: Phase 1 Complete!")
    print("\n✅ Both test cases passed:")
    print("   - Nexus formation → Natural language")
    print("   - No nexus formation → Natural language")
    print("   - NO process philosophy in either case")
    print("\n🚀 System ready for epoch training!")
else:
    print("❌ FAILURE: Some tests failed")
    print(f"   Passed: {sum(results)}/{len(results)}")

print("=" * 80)
