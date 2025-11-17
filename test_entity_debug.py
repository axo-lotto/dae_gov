#!/usr/bin/env python3
"""
Quick diagnostic test for entity memory + EntityOrganTracker.
Runs 3 training pairs with debug logging to identify blocking issues.
"""

import sys
import os

# Set PYTHONPATH
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.user_superject_learner import UserSuperjectLearner
import json

print("="*80)
print("🔍 ENTITY MEMORY DEBUG TEST (3 pairs)")
print("="*80)

# Load training pairs
with open('knowledge_base/entity_memory_training_pairs.json', 'r') as f:
    data = json.load(f)
    training_pairs = data['training_pairs']

# Initialize organism
print("\n🌀 Initializing organism...")
wrapper = ConversationalOrganismWrapper()
learner = UserSuperjectLearner()

# Test 3 pairs
test_pairs = training_pairs[:3]

for idx, pair in enumerate(test_pairs, 1):
    print(f"\n{'='*80}")
    print(f"📝 Test Pair {idx}/3")
    print(f"{'='*80}")

    pair_id = pair.get('pair_id', f'test_{idx}')
    input_text = pair['input']

    # Setup user profile
    setup = pair.get('setup', {})
    user_id = setup.get('user_id', 'test_user')
    pre_existing = setup.get('pre_existing_entities', {})

    # Store pre-existing entities
    profile = learner.get_or_create_profile(user_id)
    if not profile.get('entities'):
        profile['entities'] = pre_existing
        learner._save_profile(user_id, profile)

    print(f"   Pair ID: {pair_id}")
    print(f"   User ID: {user_id}")
    print(f"   Input: \"{input_text[:60]}...\"")
    print(f"   Pre-existing entities: {len(pre_existing.get('relationships', []))}")

    # Process
    result = wrapper.process_text(
        input_text,
        context={'pair_id': pair_id},
        user_id=user_id,
        enable_tsk_recording=False,
        enable_phase2=True
    )

    print(f"\n   ✅ Processing complete")
    print(f"      Emission: \"{result['felt_states'].get('emission_text', '')[:60]}...\"")

print(f"\n{'='*80}")
print("🔍 CHECKING ENTITYORGANTRACKER FILE")
print(f"{'='*80}")

import os
tracker_path = 'persona_layer/entity_organ_tracker.json'
if os.path.exists(tracker_path):
    print(f"✅ EntityOrganTracker file EXISTS")
    with open(tracker_path, 'r') as f:
        data = json.load(f)
    print(f"   Tracked entities: {len(data.get('entities', {}))}")
    print(f"   Keys: {list(data.keys())}")
else:
    print(f"❌ EntityOrganTracker file NOT FOUND at {tracker_path}")

print(f"\n{'='*80}")
print("✅ DEBUG TEST COMPLETE")
print(f"{'='*80}\n")
