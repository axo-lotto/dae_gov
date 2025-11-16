"""
Simple single-conversation test of Phase 5 learning.
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("🌀 Testing Phase 5 Learning - Single Conversation")
print("="*80)

organism = ConversationalOrganismWrapper()

print("\n📝 Processing: 'I just got the job! I can't believe it!'")
result = organism.process_text(
    "I just got the job! I can't believe it!",
    context={'conversation_id': 'test_phase5_001'}
)

print("\n=== RESULTS ===")
print(f"✅ Emission: {result.get('emission_text', 'None')[:100]}...")
print(f"✅ Confidence: {result.get('confidence', 0.0):.3f}")

felt_states = result.get('felt_states', {})
print(f"\n📊 Felt States:")
for key, value in felt_states.items():
    if 'phase5' in key.lower():
        print(f"   {key}: {value}")

phase5_family = felt_states.get('phase5_family_id')
if phase5_family:
    print(f"\n✅ SUCCESS: Family assigned: {phase5_family}")
    print(f"   Similarity: {felt_states.get('phase5_similarity', 0.0):.3f}")
    print(f"   Is new: {felt_states.get('phase5_is_new', False)}")
else:
    print(f"\n❌ FAIL: No family assigned")
    print(f"   Check logs above for 'Phase 5' or errors")
