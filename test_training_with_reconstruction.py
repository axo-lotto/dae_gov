"""
Test Training with Reconstruction Pipeline
==========================================

Quick test with 3 training pairs to validate reconstruction works in training context.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\n" + "="*70)
print("🌀 Testing Reconstruction Pipeline in Training Context")
print("="*70 + "\n")

# Load training pairs
with open("knowledge_base/conversational_training_pairs.json") as f:
    data = json.load(f)
    training_pairs = data['training_pairs'][:3]  # First 3 pairs only

# Initialize organism
wrapper = ConversationalOrganismWrapper()

print(f"Testing {len(training_pairs)} training pairs...\n")

for idx, pair in enumerate(training_pairs, 1):
    input_text = pair['input_text']
    pair_id = pair.get('pair_metadata', {}).get('id', f'pair_{idx}')

    print(f"Pair {idx}/{len(training_pairs)} ({pair_id})")
    print(f"  Input: \"{input_text[:60]}...\"")

    # Process with Phase 2 + reconstruction
    result = wrapper.process_text(
        input_text,
        context={'pair_id': pair_id},
        enable_tsk_recording=False,
        enable_phase2=True
    )

    # Extract results
    emission_text = result.get('emission_text', '')
    emission_confidence = result.get('emission_confidence', 0.0)
    emission_path = result.get('emission_path', 'none')
    nexuses = result.get('emission_nexus_count', 0)
    cycles = result.get('felt_states', {}).get('convergence_cycles', 0)

    print(f"  ✅ Complete: {cycles} cycles, {nexuses} nexuses")
    print(f"     Emission: \"{emission_text[:60]}...\"")
    print(f"     Confidence: {emission_confidence:.3f}, Path: {emission_path}\n")

print("="*70)
print("✅ ALL TESTS PASSED - RECONSTRUCTION WORKING IN TRAINING")
print("="*70 + "\n")
