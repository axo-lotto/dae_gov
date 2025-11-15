"""
Baseline Training Session - System Health Assessment
=====================================================

Runs 30 training pairs through Phase 2 + Salience system to assess:
- Memory handling
- Convergence stability
- Nexus formation consistency
- Emission quality over time
- R-matrix learning
- Organic family growth
- Salience model calibration
- Performance/memory metrics

Known limitations going in:
- Keyword-based organs (acceptable for baseline)
- 2 tests failed in Phase 2 (short texts - training pairs are medium length)
- Kairos window may need tuning (defer until after training)

Expected outcomes:
- Emission confidence: 0.45 → 0.55-0.65 over epochs
- Nexus formation: 1-3 per pair (simple) → 3-5 (after R-matrix learning)
- R-matrix: Off-diagonal elements grow from 0.0 → 0.2-0.4
- Organic families: 3-5 families emerge
- No crashes, no memory leaks, stable convergence

Date: November 12, 2025
"""

import sys
import json
import time
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\n" + "="*80)
print("🌀 BASELINE TRAINING SESSION - SYSTEM HEALTH ASSESSMENT")
print("="*80 + "\n")

# Configuration
TRAINING_PAIRS_PATH = "knowledge_base/conversational_training_pairs.json"
OUTPUT_PATH = "baseline_training_results.json"
NUM_PAIRS = 30  # All available training pairs
ENABLE_PHASE2 = True  # Multi-cycle V0 convergence
ENABLE_SALIENCE = True  # Trauma-aware monitoring (always on with Phase 2)

print(f"📋 Configuration:")
print(f"   Training pairs: {TRAINING_PAIRS_PATH}")
print(f"   Num pairs: {NUM_PAIRS}")
print(f"   Phase 2: {ENABLE_PHASE2}")
print(f"   Salience: {ENABLE_SALIENCE}")
print(f"   Output: {OUTPUT_PATH}\n")

# Load training pairs
print(f"📂 Loading training pairs...")
try:
    with open(TRAINING_PAIRS_PATH) as f:
        data = json.load(f)
        training_pairs = data.get('training_pairs', [])
        metadata = data.get('metadata', {})
        statistics = data.get('statistics', {})

    print(f"   ✅ Loaded {len(training_pairs)} training pairs")
    print(f"   Categories: {list(statistics.get('categories', {}).keys())}")
    print(f"   Mean input length: {statistics.get('mean_input_length', 0):.1f} chars")
    print(f"   Mean output length: {statistics.get('mean_output_length', 0):.1f} chars\n")
except Exception as e:
    print(f"   ❌ Error loading training pairs: {e}")
    sys.exit(1)

# Initialize organism
print(f"🌀 Initializing organism...")
try:
    wrapper = ConversationalOrganismWrapper()
    print(f"   ✅ Organism initialized\n")
except Exception as e:
    print(f"   ❌ Error initializing organism: {e}")
    traceback.print_exc()
    sys.exit(1)

# Training loop
results = []
metrics = {
    'confidence_history': [],
    'nexus_count_history': [],
    'cycle_history': [],
    'v0_final_history': [],
    'salience_trauma_history': [],
    'processing_time_history': [],
    'error_count': 0,
    'success_count': 0
}

print(f"🎯 Beginning training loop ({NUM_PAIRS} pairs)...\n")
print(f"{'='*80}\n")

for idx, pair in enumerate(training_pairs[:NUM_PAIRS], 1):
    input_text = pair['input_text']
    output_text = pair['output_text']
    pair_metadata = pair.get('pair_metadata', {})

    print(f"📝 Training Pair {idx}/{NUM_PAIRS}")
    print(f"   ID: {pair_metadata.get('id', 'unknown')}")
    print(f"   Category: {pair_metadata.get('category', 'unknown')}")
    print(f"   Input length: {len(input_text)} chars")
    print(f"   Output length: {len(output_text)} chars")

    start_time = time.time()

    try:
        # Process through Phase 2 + Salience
        result = wrapper.process_text(
            input_text,
            context={'pair_id': pair_metadata.get('id', f'pair_{idx}')},
            enable_tsk_recording=False,  # Don't need TSK for baseline
            enable_phase2=ENABLE_PHASE2
        )

        processing_time = time.time() - start_time

        # Extract metrics
        felt_states = result['felt_states']
        emission_text = felt_states.get('emission_text', '')
        emission_confidence = felt_states.get('emission_confidence', 0.0)
        emission_path = felt_states.get('emission_path', 'none')
        nexus_count = felt_states.get('emission_nexus_count', 0)
        cycles = felt_states.get('convergence_cycles', 0)
        v0_final = felt_states.get('v0_energy', {}).get('final_energy', 1.0)

        # Salience metrics
        salience_trauma = felt_states.get('salience_trauma_markers', {})
        signal_inflation = salience_trauma.get('signal_inflation', 0.0)
        safety_gradient = salience_trauma.get('safety_gradient', 1.0)

        print(f"   ✅ Processing complete ({processing_time:.2f}s)")
        print(f"      Convergence: {cycles} cycles")
        print(f"      V0 energy: 1.0 → {v0_final:.3f}")
        print(f"      Nexuses: {nexus_count}")
        print(f"      Emission confidence: {emission_confidence:.3f}")
        print(f"      Path: {emission_path}")
        if salience_trauma:
            print(f"      Trauma markers: signal_inflation={signal_inflation:.2f}, safety={safety_gradient:.2f}")

        # Truncate emission for display
        if emission_text:
            display_emission = emission_text[:80] + "..." if len(emission_text) > 80 else emission_text
            print(f"      Emission: \"{display_emission}\"")

        # Store results
        results.append({
            'pair_id': pair_metadata.get('id', f'pair_{idx}'),
            'category': pair_metadata.get('category', 'unknown'),
            'input_length': len(input_text),
            'output_length': len(output_text),
            'emission_confidence': emission_confidence,
            'nexus_count': nexus_count,
            'cycles': cycles,
            'v0_final': v0_final,
            'signal_inflation': signal_inflation,
            'safety_gradient': safety_gradient,
            'processing_time': processing_time,
            'emission_path': emission_path,
            'success': True
        })

        # Update metrics
        metrics['confidence_history'].append(emission_confidence)
        metrics['nexus_count_history'].append(nexus_count)
        metrics['cycle_history'].append(cycles)
        metrics['v0_final_history'].append(v0_final)
        metrics['salience_trauma_history'].append(signal_inflation)
        metrics['processing_time_history'].append(processing_time)
        metrics['success_count'] += 1

    except Exception as e:
        processing_time = time.time() - start_time
        print(f"   ❌ Error processing pair: {e}")
        traceback.print_exc()

        results.append({
            'pair_id': pair_metadata.get('id', f'pair_{idx}'),
            'category': pair_metadata.get('category', 'unknown'),
            'error': str(e),
            'processing_time': processing_time,
            'success': False
        })

        metrics['error_count'] += 1

    print()  # Blank line between pairs

# Calculate aggregate statistics
print(f"{'='*80}")
print(f"📊 BASELINE TRAINING RESULTS")
print(f"{'='*80}\n")

print(f"✅ Success Rate: {metrics['success_count']}/{NUM_PAIRS} ({metrics['success_count']/NUM_PAIRS*100:.1f}%)")
print(f"❌ Errors: {metrics['error_count']}\n")

if metrics['confidence_history']:
    print(f"📈 Emission Confidence:")
    print(f"   Mean: {np.mean(metrics['confidence_history']):.3f}")
    print(f"   Std: {np.std(metrics['confidence_history']):.3f}")
    print(f"   Min: {np.min(metrics['confidence_history']):.3f}")
    print(f"   Max: {np.max(metrics['confidence_history']):.3f}")

    # Check for improvement over time
    first_10 = np.mean(metrics['confidence_history'][:10])
    last_10 = np.mean(metrics['confidence_history'][-10:])
    improvement = last_10 - first_10
    print(f"   First 10 avg: {first_10:.3f}")
    print(f"   Last 10 avg: {last_10:.3f}")
    print(f"   Improvement: {improvement:+.3f} ({improvement/first_10*100:+.1f}%)\n")

if metrics['nexus_count_history']:
    print(f"🌀 Nexus Formation:")
    print(f"   Mean: {np.mean(metrics['nexus_count_history']):.2f}")
    print(f"   Std: {np.std(metrics['nexus_count_history']):.2f}")
    print(f"   Min: {np.min(metrics['nexus_count_history'])}")
    print(f"   Max: {np.max(metrics['nexus_count_history'])}\n")

if metrics['cycle_history']:
    print(f"⏱️  Convergence Cycles:")
    print(f"   Mean: {np.mean(metrics['cycle_history']):.2f}")
    print(f"   Std: {np.std(metrics['cycle_history']):.2f}")
    print(f"   Min: {np.min(metrics['cycle_history'])}")
    print(f"   Max: {np.max(metrics['cycle_history'])}\n")

if metrics['v0_final_history']:
    print(f"🔋 V0 Final Energy:")
    print(f"   Mean: {np.mean(metrics['v0_final_history']):.3f}")
    print(f"   Std: {np.std(metrics['v0_final_history']):.3f}")
    print(f"   Min: {np.min(metrics['v0_final_history']):.3f}")
    print(f"   Max: {np.max(metrics['v0_final_history']):.3f}\n")

if metrics['salience_trauma_history']:
    print(f"🛡️  Trauma Detection (signal_inflation):")
    print(f"   Mean: {np.mean(metrics['salience_trauma_history']):.3f}")
    print(f"   High trauma count (>0.7): {sum(1 for x in metrics['salience_trauma_history'] if x > 0.7)}/{len(metrics['salience_trauma_history'])}\n")

if metrics['processing_time_history']:
    print(f"⚡ Processing Time:")
    print(f"   Mean: {np.mean(metrics['processing_time_history']):.2f}s")
    print(f"   Std: {np.std(metrics['processing_time_history']):.2f}s")
    print(f"   Min: {np.min(metrics['processing_time_history']):.2f}s")
    print(f"   Max: {np.max(metrics['processing_time_history']):.2f}s\n")

# Save results
output_data = {
    'metadata': {
        'training_date': datetime.now().isoformat(),
        'num_pairs': NUM_PAIRS,
        'enable_phase2': ENABLE_PHASE2,
        'enable_salience': ENABLE_SALIENCE,
        'training_pairs_path': TRAINING_PAIRS_PATH
    },
    'aggregate_metrics': {
        'success_rate': metrics['success_count'] / NUM_PAIRS,
        'error_count': metrics['error_count'],
        'mean_confidence': float(np.mean(metrics['confidence_history'])) if metrics['confidence_history'] else 0.0,
        'mean_nexus_count': float(np.mean(metrics['nexus_count_history'])) if metrics['nexus_count_history'] else 0.0,
        'mean_cycles': float(np.mean(metrics['cycle_history'])) if metrics['cycle_history'] else 0.0,
        'mean_v0_final': float(np.mean(metrics['v0_final_history'])) if metrics['v0_final_history'] else 0.0,
        'mean_trauma_detection': float(np.mean(metrics['salience_trauma_history'])) if metrics['salience_trauma_history'] else 0.0,
        'mean_processing_time': float(np.mean(metrics['processing_time_history'])) if metrics['processing_time_history'] else 0.0
    },
    'time_series': {
        'confidence_history': metrics['confidence_history'],
        'nexus_count_history': metrics['nexus_count_history'],
        'cycle_history': metrics['cycle_history'],
        'v0_final_history': metrics['v0_final_history'],
        'salience_trauma_history': metrics['salience_trauma_history'],
        'processing_time_history': metrics['processing_time_history']
    },
    'pair_results': results
}

try:
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"💾 Results saved to: {OUTPUT_PATH}\n")
except Exception as e:
    print(f"❌ Error saving results: {e}\n")

# Health assessment
print(f"{'='*80}")
print(f"🏥 SYSTEM HEALTH ASSESSMENT")
print(f"{'='*80}\n")

health_checks = []

# Check 1: Success rate
success_rate = metrics['success_count'] / NUM_PAIRS
health_checks.append(("Success rate ≥90%", success_rate >= 0.9, f"{success_rate*100:.1f}%"))

# Check 2: Mean confidence
mean_conf = np.mean(metrics['confidence_history']) if metrics['confidence_history'] else 0.0
health_checks.append(("Mean confidence ≥0.45", mean_conf >= 0.45, f"{mean_conf:.3f}"))

# Check 3: Nexus formation
mean_nexus = np.mean(metrics['nexus_count_history']) if metrics['nexus_count_history'] else 0.0
health_checks.append(("Mean nexuses ≥1.0", mean_nexus >= 1.0, f"{mean_nexus:.2f}"))

# Check 4: Convergence cycles
mean_cycles = np.mean(metrics['cycle_history']) if metrics['cycle_history'] else 0.0
health_checks.append(("Mean cycles 2-5", 2 <= mean_cycles <= 5, f"{mean_cycles:.2f}"))

# Check 5: V0 convergence
mean_v0 = np.mean(metrics['v0_final_history']) if metrics['v0_final_history'] else 1.0
health_checks.append(("Mean V0 final ≤0.3", mean_v0 <= 0.3, f"{mean_v0:.3f}"))

# Check 6: Processing time
mean_time = np.mean(metrics['processing_time_history']) if metrics['processing_time_history'] else 0.0
health_checks.append(("Mean processing ≤5s", mean_time <= 5.0, f"{mean_time:.2f}s"))

# Check 7: Trauma detection functional
trauma_detected = any(x > 0.5 for x in metrics['salience_trauma_history'])
health_checks.append(("Trauma detection working", trauma_detected, "Detected in training"))

all_passed = True
for check_name, passed, value in health_checks:
    status = "✅" if passed else "❌"
    print(f"{status} {check_name}: {value}")
    if not passed:
        all_passed = False

print()
if all_passed:
    print("🎉 ALL HEALTH CHECKS PASSED - SYSTEM READY FOR PRODUCTION")
else:
    print("⚠️  SOME HEALTH CHECKS FAILED - REVIEW RESULTS AND TUNE PARAMETERS")

print(f"\n{'='*80}")
print(f"🌀 BASELINE TRAINING COMPLETE")
print(f"{'='*80}\n")

print(f"📁 Next steps:")
print(f"   1. Review {OUTPUT_PATH} for detailed metrics")
print(f"   2. Check persona_layer/conversational_hebbian_memory.json for R-matrix growth")
print(f"   3. Check persona_layer/organic_families.json for family formation")
print(f"   4. If health checks passed, proceed with expanded training corpus")
print(f"   5. If health checks failed, tune parameters in SYSTEM_TUNABLE_PARAMETERS.md\n")
