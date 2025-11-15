#!/usr/bin/env python3
"""
🌀 Direct Entity Memory Fix Test (Nov 14, 2025)

Quick test to verify entity_context_string flows through the complete pipeline
after the fix to conversational_organism_wrapper.py line 842.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("=" * 70)
print("  🌀 Direct Entity Memory Fix Test")
print("=" * 70)

# Initialize organism
print("\n1. Initializing organism...")
organism = ConversationalOrganismWrapper()
print("   ✅ Organism initialized")

# Test 1: Context with entity_context_string
print("\n2. Testing with entity_context_string in context...")
context = {
    'entity_context_string': "Known information:\n- User's name: Sarah\n- Family: Two daughters (Emma, Lily)",
    'username': 'Sarah'
}

user_input = "What should I do about work stress?"

print(f"   User input: {user_input}")
print(f"   Entity context: {context['entity_context_string'][:60]}...")

# Process
print("\n3. Processing through organism...")
result = organism.process_text(
    text=user_input,
    context=context,
    enable_phase2=True
)

# Extract emission
emission_text = result.get('emission_text', '(no emission)')
emission_confidence = result.get('emission_confidence', 0.0)

print(f"\n4. Results:")
print(f"   Emission: {emission_text[:200]}...")
print(f"   Confidence: {emission_confidence:.3f}")

# Check if entity knowledge appears
print(f"\n5. Entity Knowledge Check:")
if 'sarah' in emission_text.lower():
    print(f"   ✅ SUCCESS: 'Sarah' found in emission!")
elif 'emma' in emission_text.lower() or 'lily' in emission_text.lower():
    print(f"   ✅ SUCCESS: Daughter names found in emission!")
elif any(word in emission_text.lower() for word in ['you', 'your']):
    print(f"   ⚠️  PARTIAL: Personalization present but no explicit entity reference")
else:
    print(f"   ❌ FAILED: No entity knowledge detected in emission")

print("\n" + "=" * 70)
print("Test complete!")
print("=" * 70)
