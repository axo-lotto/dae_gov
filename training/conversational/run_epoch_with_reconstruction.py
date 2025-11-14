"""
Epoch Training with Reconstruction Pipeline
===========================================

Run baseline training with reconstruction pipeline active to validate SELF matrix improvements.
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
import numpy as np

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\n" + "="*80)
print("🌀 EPOCH TRAINING WITH RECONSTRUCTION PIPELINE")
print("="*80 + "\n")

# Configuration
TRAINING_PAIRS_PATH = "knowledge_base/conversational_training_pairs.json"
OUTPUT_PATH = "epoch_with_reconstruction_results.json"
NUM_PAIRS = 30
ENABLE_PHASE2 = True

print(f"📋 Configuration:")
print(f"   Training pairs: {TRAINING_PAIRS_PATH}")
print(f"   Num pairs: {NUM_PAIRS}")
print(f"   Phase 2: {ENABLE_PHASE2}")
print(f"   Reconstruction: ENABLED (authentic voice)")
print(f"   Output: {OUTPUT_PATH}\n")

# Load training pairs
print(f"📂 Loading training pairs...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data['training_pairs']
print(f"   ✅ Loaded {len(training_pairs)} training pairs\n")

# Initialize organism
print(f"🌀 Initializing organism...")
wrapper = ConversationalOrganismWrapper()
print(f"   ✅ Organism initialized")
print(f"   ✅ Reconstruction pipeline: {wrapper.reconstruction_pipeline is not None}\n")

# Training loop
results = []
metrics = {
    'confidence_history': [],
    'nexus_count_history': [],
    'cycle_history': [],
    'v0_final_history': [],
    'zone_history': [],
    'safe_emission_history': [],
    'processing_time_history': [],
    'error_count': 0,
    'success_count': 0
}

print(f"🎯 Beginning training loop ({NUM_PAIRS} pairs)...\n")
print(f"{'='*80}\n")

for idx, pair in enumerate(training_pairs[:NUM_PAIRS], 1):
    input_text = pair['input_text']
    pair_id = pair.get('pair_metadata', {}).get('id', f'pair_{idx}')
    category = pair.get('pair_metadata', {}).get('category', 'unknown')

    print(f"📝 Training Pair {idx}/{NUM_PAIRS} ({pair_id}, {category})")

    start_time = time.time()

    try:
        # Process with Phase 2 + reconstruction
        result = wrapper.process_text(
            input_text,
            context={'pair_id': pair_id},
            enable_tsk_recording=False,
            enable_phase2=ENABLE_PHASE2
        )

        processing_time = time.time() - start_time

        # Extract metrics
        felt_states = result['felt_states']
        emission_text = result.get('emission_text', '')
        emission_confidence = result.get('emission_confidence', 0.0)
        emission_path = result.get('emission_path', 'none')
        nexus_count = result.get('emission_nexus_count', 0)
        cycles = felt_states.get('convergence_cycles', 0)
        v0_final = felt_states.get('v0_energy', {}).get('final_energy', 1.0)

        # SELF matrix metrics (may not be in return dict yet)
        zone_id = felt_states.get('zone_id', 0)
        safe_emission = felt_states.get('safe_emission', True)

        print(f"   ✅ Complete ({processing_time:.2f}s)")
        print(f"      Cycles: {cycles}, V0: 1.0 → {v0_final:.3f}")
        print(f"      Nexuses: {nexus_count}, Confidence: {emission_confidence:.3f}")
        print(f"      Path: {emission_path}")
        if zone_id > 0:
            print(f"      Zone: {zone_id}, Safe: {safe_emission}")

        # Store results
        results.append({
            'pair_id': pair_id,
            'category': category,
            'emission_confidence': emission_confidence,
            'nexus_count': nexus_count,
            'cycles': cycles,
            'v0_final': v0_final,
            'zone_id': zone_id,
            'safe_emission': safe_emission,
            'processing_time': processing_time,
            'emission_path': emission_path,
            'success': True
        })

        # Update metrics
        metrics['confidence_history'].append(emission_confidence)
        metrics['nexus_count_history'].append(nexus_count)
        metrics['cycle_history'].append(cycles)
        metrics['v0_final_history'].append(v0_final)
        metrics['zone_history'].append(zone_id)
        metrics['safe_emission_history'].append(1 if safe_emission else 0)
        metrics['processing_time_history'].append(processing_time)
        metrics['success_count'] += 1

    except Exception as e:
        processing_time = time.time() - start_time
        print(f"   ❌ Error: {e}")

        results.append({
            'pair_id': pair_id,
            'category': category,
            'error': str(e),
            'processing_time': processing_time,
            'success': False
        })

        metrics['error_count'] += 1

    print()

# Calculate aggregate statistics
print(f"{'='*80}")
print(f"📊 TRAINING RESULTS WITH RECONSTRUCTION")
print(f"{'='*80}\n")

print(f"✅ Success Rate: {metrics['success_count']}/{NUM_PAIRS} ({metrics['success_count']/NUM_PAIRS*100:.1f}%)")
print(f"❌ Errors: {metrics['error_count']}\n")

if metrics['confidence_history']:
    print(f"📈 Emission Confidence:")
    print(f"   Mean: {np.mean(metrics['confidence_history']):.3f}")
    print(f"   Std: {np.std(metrics['confidence_history']):.3f}")
    print(f"   Min: {np.min(metrics['confidence_history']):.3f}")
    print(f"   Max: {np.max(metrics['confidence_history']):.3f}")

    # Compare to baseline (0.465)
    baseline = 0.465
    improvement = np.mean(metrics['confidence_history']) - baseline
    print(f"   Baseline: {baseline:.3f}")
    print(f"   Improvement: {improvement:+.3f} ({improvement/baseline*100:+.1f}%)\n")

if metrics['nexus_count_history']:
    print(f"🌀 Nexus Formation:")
    print(f"   Mean: {np.mean(metrics['nexus_count_history']):.2f}")
    print(f"   Std: {np.std(metrics['nexus_count_history']):.2f}\n")

if metrics['cycle_history']:
    print(f"⏱️  Convergence Cycles:")
    print(f"   Mean: {np.mean(metrics['cycle_history']):.2f}")
    print(f"   Std: {np.std(metrics['cycle_history']):.2f}\n")

if metrics['zone_history']:
    zone_counts = {}
    for zone in metrics['zone_history']:
        zone_counts[zone] = zone_counts.get(zone, 0) + 1
    print(f"🛡️  SELF Matrix Zones:")
    for zone, count in sorted(zone_counts.items()):
        print(f"   Zone {zone}: {count}/{len(metrics['zone_history'])} ({count/len(metrics['zone_history'])*100:.1f}%)")
    print()

if metrics['safe_emission_history']:
    safe_count = sum(metrics['safe_emission_history'])
    print(f"✅ Safety Validation:")
    print(f"   Safe emissions: {safe_count}/{len(metrics['safe_emission_history'])} ({safe_count/len(metrics['safe_emission_history'])*100:.1f}%)\n")

# Save results
output_data = {
    'metadata': {
        'training_date': datetime.now().isoformat(),
        'num_pairs': NUM_PAIRS,
        'enable_phase2': ENABLE_PHASE2,
        'reconstruction_enabled': True,
        'training_pairs_path': TRAINING_PAIRS_PATH
    },
    'aggregate_metrics': {
        'success_rate': metrics['success_count'] / NUM_PAIRS,
        'mean_confidence': float(np.mean(metrics['confidence_history'])),
        'mean_nexus_count': float(np.mean(metrics['nexus_count_history'])),
        'mean_cycles': float(np.mean(metrics['cycle_history'])),
        'mean_v0_final': float(np.mean(metrics['v0_final_history'])),
        'mean_processing_time': float(np.mean(metrics['processing_time_history'])),
        'baseline_improvement': float(np.mean(metrics['confidence_history']) - 0.465)
    },
    'pair_results': results
}

with open(OUTPUT_PATH, 'w') as f:
    json.dump(output_data, f, indent=2)
print(f"💾 Results saved to: {OUTPUT_PATH}\n")

print(f"{'='*80}")
print(f"🌀 TRAINING WITH RECONSTRUCTION COMPLETE")
print(f"{'='*80}\n")
