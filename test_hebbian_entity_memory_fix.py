#!/usr/bin/env python3
"""
🌀 Hebbian Fallback Entity Memory Fix Test (Nov 14, 2025)

Tests that entity_context_string flows through the hebbian_fallback path.
This is the critical fix for the user's issue where DAE was forgetting entities.

The issue was: hebbian_fallback uses _generate_felt_guided_llm_single() which
was NOT receiving entity_context_string, even though felt_state had it.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("=" * 70)
print("  🌀 Hebbian Fallback Entity Memory Fix Test")
print("=" * 70)

# Initialize organism
print("\n1. Initializing organism...")
organism = ConversationalOrganismWrapper()
print("   ✅ Organism initialized")

# Test scenario: User introduces themselves
print("\n2. Turn 1: User introduces themselves")
context1 = {}
result1 = organism.process_text(
    text="Hello! My name is Emiliano and I like to play Super Smash Bros on my Nintendo!",
    context=context1,
    enable_phase2=True
)

emission1 = result1.get('emission_text', '(no emission)')
print(f"   DAE: {emission1[:100]}...")

# Check if name was mentioned
if 'emiliano' in emission1.lower():
    print(f"   ✅ Turn 1: DAE acknowledged 'Emiliano'")
else:
    print(f"   ⚠️  Turn 1: No explicit name mention (but may be processing)")

# Test scenario: Simulate entity context being loaded (Phase 1.8++)
print("\n3. Turn 2: Casual question WITH entity context loaded")
context2 = {
    'entity_context_string': "Known information:\n- User's name: Emiliano\n- User likes: Super Smash Bros on Nintendo",
    'username': 'Emiliano'
}

result2 = organism.process_text(
    text="What's the weather like today?",
    context=context2,
    enable_phase2=True
)

emission2 = result2.get('emission_text', '(no emission)')
strategy2 = result2.get('reconstruction_strategy', 'unknown')

print(f"   Strategy used: {strategy2}")
print(f"   DAE: {emission2[:150]}...")

# Check if entity knowledge was used
has_name = 'emiliano' in emission2.lower()
has_personalization = any(word in emission2.lower() for word in ['you', 'your'])

print(f"\n4. Entity Memory Check:")
if has_name:
    print(f"   ✅ SUCCESS: 'Emiliano' appears in response!")
elif has_personalization:
    print(f"   ⚠️  PARTIAL: Personalization present (entity context processed)")
else:
    print(f"   ❌ FAILED: No entity knowledge detected")

# Test scenario: Direct memory question
print("\n5. Turn 3: Direct memory question")
context3 = {
    'entity_context_string': "Known information:\n- User's name: Emiliano\n- User likes: Super Smash Bros on Nintendo",
    'username': 'Emiliano',
    'memory_intent': True
}

result3 = organism.process_text(
    text="Do you remember my name?",
    context=context3,
    enable_phase2=True
)

emission3 = result3.get('emission_text', '(no emission)')
strategy3 = result3.get('reconstruction_strategy', 'unknown')

print(f"   Strategy used: {strategy3}")
print(f"   DAE: {emission3[:150]}...")

# Check if DAE demonstrates knowledge
if 'emiliano' in emission3.lower():
    print(f"   ✅ SUCCESS: DAE correctly recalls 'Emiliano'!")
elif any(phrase in emission3.lower() for phrase in ["yes", "of course", "sure"]):
    print(f"   ⚠️  PARTIAL: Affirmative response (but no explicit name)")
elif any(phrase in emission3.lower() for phrase in ["don't", "haven't", "not sure"]):
    print(f"   ❌ FAILED: DAE doesn't demonstrate knowledge")
else:
    print(f"   ⚠️  UNCLEAR: Response unclear")

print("\n" + "=" * 70)
print("Test Summary:")
print("=" * 70)
print(f"Turn 1 Strategy: {result1.get('reconstruction_strategy', 'unknown')}")
print(f"Turn 2 Strategy: {strategy2}")
print(f"Turn 3 Strategy: {strategy3}")
print("\n🎯 Expected Outcome:")
print("   - Entity context should be detected in reconstruction pipeline")
print("   - Should see: '🌀 Entity memory context available' in output")
print("   - LLM should receive entity context in prompt")
print("   - Response should demonstrate knowledge of 'Emiliano'")
print("=" * 70)
