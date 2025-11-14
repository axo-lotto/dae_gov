"""
Test: Verify felt-guided LLM works when NO nexuses form
========================================================

Tests the exact user input that was failing with hebbian fallback.

Date: November 13, 2025
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("=" * 80)
print("TEST: No-Nexus Path → Felt-Guided LLM")
print("=" * 80)

# Initialize organism
print("\n📦 Initializing organism...")
organism = ConversationalOrganismWrapper(bundle_path="Bundle/test_no_nexus")

# User's exact failing input
user_input = "Hello there today is a beautiful day!"

print(f"\n💬 User input: '{user_input}'")
print("🔄 Processing...\n")

# Process
result = organism.process_text(user_input)

# Extract results
emission = result.get('emission_text', '')
confidence = result.get('emission_confidence', 0.0)
path = result.get('emission_path', 'unknown')
nexus_count = result.get('emission_nexus_count', 0)

print("\n" + "=" * 80)
print("📊 RESULTS:")
print("=" * 80)
print(f"Nexuses formed: {nexus_count}")
print(f"Emission path: {path}")
print(f"Confidence: {confidence:.3f}")
print(f"\n💬 Emission:\n   '{emission}'")

# Validation
print("\n" + "=" * 80)
print("✅ VALIDATION:")
print("=" * 80)

if nexus_count == 0:
    print("✅ PASS: No nexuses (as expected for this input)")
else:
    print(f"⚠️  UNEXPECTED: {nexus_count} nexuses formed")

if path == 'felt_guided_llm':
    print("✅ PASS: Felt-guided LLM path used!")
elif path == 'hebbian_fallback' or path == 'hebbian':
    print("❌ FAIL: Still using hebbian fallback!")
else:
    print(f"⚠️  UNEXPECTED: Path is '{path}'")

# Check for process language
process_phrases = [
    "everything verbs",
    "ontology is a conspiracy",
    "God = primordial lure",
    "occasions",
    "nexus of occasions"
]

has_process_language = any(phrase.lower() in emission.lower() for phrase in process_phrases)

if has_process_language:
    print("❌ FAIL: Still has process-aware language!")
    for phrase in process_phrases:
        if phrase.lower() in emission.lower():
            print(f"   Found: '{phrase}'")
else:
    print("✅ PASS: No process-aware language!")

# Final verdict
print("\n" + "=" * 80)
if path == 'felt_guided_llm' and not has_process_language:
    print("🎉 SUCCESS: Phase 1 fix complete!")
    print("   - No nexuses formed")
    print("   - Felt-guided LLM triggered")
    print("   - Natural language generated")
elif path == 'hebbian_fallback' or path == 'hebbian':
    print("❌ FAILURE: Hebbian fallback still being used")
    print("   User was correct: hebbian is obscuring the real issue")
else:
    print("⚠️  PARTIAL: Unexpected state")
print("=" * 80)
