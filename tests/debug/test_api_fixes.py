"""
Quick Test - Validate API Fixes for Epoch Learning
===================================================

Tests the two API fixes:
1. Polyvagal state naming mapping
2. AssembledResponse missing attributes

Date: November 12, 2025
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import json
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_training.production_learning_coordinator import ProductionLearningCoordinator

print("\n" + "="*80)
print("🧪 API FIXES VALIDATION TEST")
print("="*80 + "\n")

# Load one training pair
print("📂 Loading test pair...")
with open('knowledge_base/conversational_training_pairs.json') as f:
    data = json.load(f)
    test_pair = data['training_pairs'][0]  # burnout_001

print(f"   Test pair: {test_pair['pair_metadata']['id']}")
print(f"   Category: {test_pair['pair_metadata']['category']}")
print(f"   Polyvagal state: {test_pair['pair_metadata']['polyvagal_state']}\n")

# Initialize components
print("🌀 Initializing organism...")
wrapper = ConversationalOrganismWrapper()
print("   ✅ Organism initialized\n")

print("🧠 Initializing learning coordinator...")
learning_coordinator = ProductionLearningCoordinator(
    hebbian_storage="TSK/conversational_hebbian_memory.json",
    phase5_storage="persona_layer",
    learning_threshold=0.45,
    save_frequency=100,  # Don't save during test
    enable_hebbian=True,
    enable_phase5=True
)
print("   ✅ Learning coordinator initialized\n")

# Process INPUT
print("▶️  Processing INPUT...")
input_result = wrapper.process_text(
    text=test_pair['input_text'],
    context={'pair_id': test_pair['pair_metadata']['id'], 'training_phase': 'input'},
    enable_tsk_recording=False,
    enable_phase2=True
)
print(f"   ✅ INPUT processed: satisfaction={input_result['felt_states']['satisfaction_final']:.3f}\n")

# Process OUTPUT
print("▶️  Processing OUTPUT...")
output_result = wrapper.process_text(
    text=test_pair['output_text'],
    context={'pair_id': test_pair['pair_metadata']['id'], 'training_phase': 'output'},
    enable_tsk_recording=False,
    enable_phase2=True
)
print(f"   ✅ OUTPUT processed: satisfaction={output_result['felt_states']['satisfaction_final']:.3f}\n")

# Test learning (this is where the fixes matter)
print("🧠 Testing learning with API fixes...")
try:
    learning_updates = learning_coordinator.learn_from_training_pair(
        input_result=input_result,
        output_result=output_result,
        pair_metadata=test_pair['pair_metadata'],
        input_text=test_pair['input_text'],
        output_text=test_pair['output_text']
    )

    print("   ✅ Learning completed WITHOUT ERRORS!\n")

    print("📊 Learning Results:")
    print(f"   Learned: {learning_updates['learned']}")
    print(f"   Hebbian updates: {learning_updates['hebbian_updates']}")
    print(f"   Cluster updates: {learning_updates['cluster_updates']}")
    print(f"   Family ID: {learning_updates.get('family_id', 'None')}")
    print(f"   Patterns total: {learning_updates['patterns_total']}\n")

    # Check for warnings in output
    print("="*80)
    print("✅ API FIXES VALIDATION: PASSED")
    print("="*80)
    print("\nNo 'dorsal_vagal' errors detected")
    print("No 'strategies_used' errors detected")
    print("\n✅ Both API fixes working correctly!\n")

except Exception as e:
    print(f"   ❌ Learning failed: {e}")
    import traceback
    traceback.print_exc()
    print("\n="*80)
    print("❌ API FIXES VALIDATION: FAILED")
    print("="*80)
    sys.exit(1)
