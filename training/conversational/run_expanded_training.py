"""
Expanded Training Session - Epoch Learning with Real Memory Integration
=========================================================================

Builds on baseline training (30 pairs successful) by adding:
- ProductionLearningCoordinator (R-matrix + Phase5 learning)
- RealTimeHealthMonitor (every 5 pairs)
- PostTrainingAnalyzer (end of epoch)
- True INPUT→OUTPUT processing (learns transformation patterns)

Expected outcomes (Epoch 1, 30 pairs):
- R-matrix: 0.0 → 0.15-0.25 (off-diagonal elements)
- Organic families: 2-4 families discovered
- Hebbian patterns: 80-120 patterns learned
- Emission confidence: 0.45 → 0.55-0.65 (improvement via learning)

Date: November 12, 2025
Status: Integrates validated baseline training + epoch learning infrastructure
"""

import sys
import json
import time
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.epoch_training.production_learning_coordinator import ProductionLearningCoordinator
from persona_layer.epoch_training.signal_collector import SignalCollector
from persona_layer.epoch_training.health_monitor import (
    PreTrainingHealthCheck,
    RealTimeHealthMonitor,
    PostTrainingAnalyzer
)

print("\n" + "="*80)
print("🌀 EXPANDED TRAINING SESSION - EPOCH 1 WITH LEARNING")
print("="*80 + "\n")

# Configuration
TRAINING_PAIRS_PATH = "knowledge_base/conversational_training_pairs.json"
OUTPUT_DIR = Path("persona_layer/epoch_training/training_logs")
EPOCH_NUM = 1
NUM_PAIRS = 30  # Start with same 30 pairs from baseline
ENABLE_PHASE2 = True  # Multi-cycle V0 convergence
ENABLE_SALIENCE = True  # Trauma-aware monitoring
LEARNING_THRESHOLD = 0.45  # Lower for trauma-focused training (vs 0.7 default)
SAVE_FREQUENCY = 5  # Save learning every 5 pairs
HEALTH_CHECK_INTERVAL = 5  # Monitor health every 5 pairs

print(f"📋 Configuration:")
print(f"   Training pairs: {TRAINING_PAIRS_PATH}")
print(f"   Epoch: {EPOCH_NUM}")
print(f"   Num pairs: {NUM_PAIRS}")
print(f"   Phase 2: {ENABLE_PHASE2}")
print(f"   Salience: {ENABLE_SALIENCE}")
print(f"   Learning threshold: {LEARNING_THRESHOLD}")
print(f"   Save frequency: Every {SAVE_FREQUENCY} pairs")
print(f"   Health check interval: Every {HEALTH_CHECK_INTERVAL} pairs\n")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ================================================================
# TIER 1: PRE-TRAINING HEALTH CHECK
# ================================================================
print(f"1️⃣ TIER 1: PRE-TRAINING HEALTH CHECK")
print("="*80 + "\n")

try:
    checker = PreTrainingHealthCheck()
    health_status = checker.run_health_check()

    print(f"   Status: {health_status['status']}")

    if health_status['status'] == 'CRITICAL':
        print(f"\n❌ CRITICAL: Cannot proceed with training")
        print(f"   Failed checks: {[c['check'] for c in health_status['checks'] if not c['passed']]}")
        print(f"   Recommendations: {health_status.get('recommendations', [])}")
        sys.exit(1)

    if health_status['status'] == 'WARNING':
        print(f"\n⚠️  WARNING: Some checks failed, but training can proceed")
        print(f"   Failed checks: {[c['check'] for c in health_status['checks'] if not c['passed']]}")

    print(f"\n✅ Pre-training health check complete\n")

except Exception as e:
    print(f"\n⚠️  Pre-training health check not available (optional): {e}")
    print(f"   Proceeding with training...\n")

# ================================================================
# TIER 2: INITIALIZE COMPONENTS
# ================================================================
print(f"2️⃣ TIER 2: INITIALIZING COMPONENTS")
print("="*80 + "\n")

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

# Initialize organism wrapper
print(f"🌀 Initializing organism...")
try:
    wrapper = ConversationalOrganismWrapper()
    print(f"   ✅ Organism initialized\n")
except Exception as e:
    print(f"   ❌ Error initializing organism: {e}")
    traceback.print_exc()
    sys.exit(1)

# Initialize signal collector
print(f"📊 Initializing signal collector...")
try:
    signal_collector = SignalCollector()
    print(f"   ✅ Signal collector initialized\n")
except Exception as e:
    print(f"   ⚠️  Signal collector not available: {e}")
    signal_collector = None
    print(f"   Proceeding without signal collection...\n")

# Initialize real-time health monitor
print(f"🏥 Initializing real-time health monitor...")
try:
    health_monitor = RealTimeHealthMonitor(check_interval=HEALTH_CHECK_INTERVAL)
    print(f"   ✅ Health monitor initialized")
    print(f"   Check interval: Every {HEALTH_CHECK_INTERVAL} pairs\n")
except Exception as e:
    print(f"   ⚠️  Health monitor not available: {e}")
    health_monitor = None
    print(f"   Proceeding without real-time monitoring...\n")

# Initialize production learning coordinator
print(f"🧠 Initializing production learning coordinator...")
try:
    learning_coordinator = ProductionLearningCoordinator(
        hebbian_storage="TSK/conversational_hebbian_memory.json",
        phase5_storage="persona_layer",
        learning_threshold=LEARNING_THRESHOLD,
        save_frequency=SAVE_FREQUENCY,
        enable_hebbian=True,
        enable_phase5=True
    )
    print(f"   ✅ Production learning coordinator initialized\n")
except Exception as e:
    print(f"   ❌ Error initializing learning coordinator: {e}")
    traceback.print_exc()
    sys.exit(1)

# ================================================================
# TIER 3: TRAINING LOOP WITH LEARNING
# ================================================================
print(f"3️⃣ TIER 3: TRAINING LOOP (INPUT→OUTPUT PROCESSING + LEARNING)")
print("="*80 + "\n")

results = []
metrics = {
    # Organism metrics
    'input_confidence_history': [],
    'output_confidence_history': [],
    'input_nexus_history': [],
    'output_nexus_history': [],
    'input_cycles_history': [],
    'output_cycles_history': [],
    'input_v0_history': [],
    'output_v0_history': [],
    'input_satisfaction_history': [],
    'output_satisfaction_history': [],
    'satisfaction_delta_history': [],
    'trauma_reduction_history': [],  # INPUT trauma - OUTPUT trauma

    # Learning metrics
    'hebbian_updates_history': [],
    'cluster_updates_history': [],
    'family_matured_history': [],
    'patterns_total_history': [],

    # Performance metrics
    'processing_time_history': [],
    'error_count': 0,
    'success_count': 0
}

for idx, pair in enumerate(training_pairs[:NUM_PAIRS], 1):
    input_text = pair['input_text']
    output_text = pair['output_text']
    pair_metadata = pair.get('pair_metadata', {})

    print(f"📘 Training Pair {idx}/{NUM_PAIRS}")
    print(f"   ID: {pair_metadata.get('id', 'unknown')}")
    print(f"   Category: {pair_metadata.get('category', 'unknown')}")
    print(f"   Input length: {len(input_text)} chars")
    print(f"   Output length: {len(output_text)} chars")

    start_time = time.time()

    try:
        # ====================================================================
        # PROCESS INPUT TEXT
        # ====================================================================
        print(f"   ▶️  Processing INPUT...")
        input_result = wrapper.process_text(
            text=input_text,
            context={
                'pair_id': pair_metadata.get('id', f'pair_{idx}'),
                'epoch_num': EPOCH_NUM,
                'training_phase': 'input'
            },
            enable_tsk_recording=False,  # Disable TSK for performance
            enable_phase2=ENABLE_PHASE2
        )

        # Extract INPUT metrics
        input_felt_states = input_result['felt_states']
        input_confidence = input_felt_states.get('emission_confidence', 0.0)
        input_nexus_count = input_felt_states.get('emission_nexus_count', 0)
        input_cycles = input_felt_states.get('convergence_cycles', 0)
        input_v0_final = input_felt_states.get('v0_energy', {}).get('final_energy', 1.0)
        input_satisfaction = input_felt_states.get('satisfaction_final', 0.0)

        # INPUT trauma markers
        input_trauma = input_felt_states.get('salience_trauma_markers', {})
        input_signal_inflation = input_trauma.get('signal_inflation', 0.0)

        print(f"      INPUT: confidence={input_confidence:.3f}, nexuses={input_nexus_count}, "
              f"cycles={input_cycles}, V0={input_v0_final:.3f}, satisfaction={input_satisfaction:.3f}")

        # ====================================================================
        # PROCESS OUTPUT TEXT
        # ====================================================================
        print(f"   ▶️  Processing OUTPUT...")
        output_result = wrapper.process_text(
            text=output_text,
            context={
                'pair_id': pair_metadata.get('id', f'pair_{idx}'),
                'epoch_num': EPOCH_NUM,
                'training_phase': 'output'
            },
            enable_tsk_recording=False,  # Disable TSK for performance
            enable_phase2=ENABLE_PHASE2
        )

        # Extract OUTPUT metrics
        output_felt_states = output_result['felt_states']
        output_confidence = output_felt_states.get('emission_confidence', 0.0)
        output_nexus_count = output_felt_states.get('emission_nexus_count', 0)
        output_cycles = output_felt_states.get('convergence_cycles', 0)
        output_v0_final = output_felt_states.get('v0_energy', {}).get('final_energy', 1.0)
        output_satisfaction = output_felt_states.get('satisfaction_final', 0.0)

        # OUTPUT trauma markers
        output_trauma = output_felt_states.get('salience_trauma_markers', {})
        output_signal_inflation = output_trauma.get('signal_inflation', 0.0)

        print(f"      OUTPUT: confidence={output_confidence:.3f}, nexuses={output_nexus_count}, "
              f"cycles={output_cycles}, V0={output_v0_final:.3f}, satisfaction={output_satisfaction:.3f}")

        # Calculate deltas
        satisfaction_delta = output_satisfaction - input_satisfaction
        trauma_reduction = input_signal_inflation - output_signal_inflation

        print(f"      DELTA: satisfaction={satisfaction_delta:+.3f}, trauma_reduction={trauma_reduction:+.3f}")

        # ====================================================================
        # REAL LEARNING (NOT SIMULATED)
        # ====================================================================
        print(f"   🧠 Learning from pair...")
        learning_updates = learning_coordinator.learn_from_training_pair(
            input_result=input_result,
            output_result=output_result,
            pair_metadata=pair_metadata,
            input_text=input_text,
            output_text=output_text
        )

        print(f"      Learned: {learning_updates['learned']}")
        print(f"      Hebbian updates: {learning_updates['hebbian_updates']}")
        print(f"      Cluster updates: {learning_updates['cluster_updates']}")
        print(f"      Family matured: {learning_updates['family_matured']}")
        print(f"      Patterns total: {learning_updates['patterns_total']}")

        processing_time = time.time() - start_time

        print(f"   ✅ Processing complete ({processing_time:.2f}s)")

        # ====================================================================
        # COLLECT SIGNALS (if available)
        # ====================================================================
        if signal_collector:
            try:
                input_signals = signal_collector.collect_from_organism_result(input_result, 'INPUT')
                output_signals = signal_collector.collect_from_organism_result(output_result, 'OUTPUT')
                learning_signals = signal_collector.collect_learning_signals(
                    input_signals, output_signals, pair_metadata
                )

                pair_record = signal_collector.create_pair_signal_record(
                    pair_id=pair_metadata.get('id', f'pair_{idx}'),
                    input_signals=input_signals,
                    output_signals=output_signals,
                    learning_signals=learning_signals,
                    context=pair_metadata
                )
            except Exception as e:
                print(f"   ⚠️  Signal collection failed: {e}")
                pair_record = None
        else:
            pair_record = None

        # ====================================================================
        # REAL-TIME HEALTH MONITORING (if available)
        # ====================================================================
        if health_monitor and pair_record:
            try:
                health_report = health_monitor.on_pair_complete(pair_record)
                if health_report:
                    print(f"   🏥 Health check triggered")
                    print(f"      Status: {health_report.get('status', 'UNKNOWN')}")
            except Exception as e:
                print(f"   ⚠️  Health monitoring failed: {e}")

        # Store results
        results.append({
            'pair_id': pair_metadata.get('id', f'pair_{idx}'),
            'category': pair_metadata.get('category', 'unknown'),

            # INPUT metrics
            'input_confidence': input_confidence,
            'input_nexus_count': input_nexus_count,
            'input_cycles': input_cycles,
            'input_v0_final': input_v0_final,
            'input_satisfaction': input_satisfaction,
            'input_signal_inflation': input_signal_inflation,

            # OUTPUT metrics
            'output_confidence': output_confidence,
            'output_nexus_count': output_nexus_count,
            'output_cycles': output_cycles,
            'output_v0_final': output_v0_final,
            'output_satisfaction': output_satisfaction,
            'output_signal_inflation': output_signal_inflation,

            # Deltas
            'satisfaction_delta': satisfaction_delta,
            'trauma_reduction': trauma_reduction,

            # Learning metrics
            'learned': learning_updates['learned'],
            'hebbian_updates': learning_updates['hebbian_updates'],
            'cluster_updates': learning_updates['cluster_updates'],
            'family_matured': learning_updates['family_matured'],
            'family_id': learning_updates.get('family_id', None),
            'patterns_total': learning_updates['patterns_total'],

            # Performance
            'processing_time': processing_time,
            'success': True
        })

        # Update metrics
        metrics['input_confidence_history'].append(input_confidence)
        metrics['output_confidence_history'].append(output_confidence)
        metrics['input_nexus_history'].append(input_nexus_count)
        metrics['output_nexus_history'].append(output_nexus_count)
        metrics['input_cycles_history'].append(input_cycles)
        metrics['output_cycles_history'].append(output_cycles)
        metrics['input_v0_history'].append(input_v0_final)
        metrics['output_v0_history'].append(output_v0_final)
        metrics['input_satisfaction_history'].append(input_satisfaction)
        metrics['output_satisfaction_history'].append(output_satisfaction)
        metrics['satisfaction_delta_history'].append(satisfaction_delta)
        metrics['trauma_reduction_history'].append(trauma_reduction)

        metrics['hebbian_updates_history'].append(learning_updates['hebbian_updates'])
        metrics['cluster_updates_history'].append(learning_updates['cluster_updates'])
        metrics['family_matured_history'].append(learning_updates['family_matured'])
        metrics['patterns_total_history'].append(learning_updates['patterns_total'])

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

# ================================================================
# TIER 4: AGGREGATE STATISTICS
# ================================================================
print(f"{'='*80}")
print(f"📊 EPOCH {EPOCH_NUM} RESULTS")
print(f"{'='*80}\n")

print(f"✅ Success Rate: {metrics['success_count']}/{NUM_PAIRS} ({metrics['success_count']/NUM_PAIRS*100:.1f}%)")
print(f"❌ Errors: {metrics['error_count']}\n")

if metrics['output_confidence_history']:
    print(f"📈 OUTPUT Emission Confidence:")
    print(f"   Mean: {np.mean(metrics['output_confidence_history']):.3f}")
    print(f"   Std: {np.std(metrics['output_confidence_history']):.3f}")
    print(f"   Min: {np.min(metrics['output_confidence_history']):.3f}")
    print(f"   Max: {np.max(metrics['output_confidence_history']):.3f}\n")

if metrics['satisfaction_delta_history']:
    print(f"🔄 Satisfaction Delta (OUTPUT - INPUT):")
    print(f"   Mean: {np.mean(metrics['satisfaction_delta_history']):+.3f}")
    print(f"   Positive deltas: {sum(1 for x in metrics['satisfaction_delta_history'] if x > 0)}/{len(metrics['satisfaction_delta_history'])}\n")

if metrics['trauma_reduction_history']:
    print(f"🛡️  Trauma Reduction (INPUT trauma - OUTPUT trauma):")
    print(f"   Mean: {np.mean(metrics['trauma_reduction_history']):+.3f}")
    print(f"   Trauma reduced: {sum(1 for x in metrics['trauma_reduction_history'] if x > 0)}/{len(metrics['trauma_reduction_history'])}\n")

if metrics['hebbian_updates_history']:
    total_hebbian = sum(metrics['hebbian_updates_history'])
    print(f"🧠 Hebbian Learning:")
    print(f"   Total updates: {total_hebbian}")
    print(f"   Final patterns: {metrics['patterns_total_history'][-1] if metrics['patterns_total_history'] else 0}\n")

if metrics['family_matured_history']:
    family_maturations = sum(metrics['family_matured_history'])
    print(f"🌱 Organic Families:")
    print(f"   Families matured: {family_maturations}\n")

if metrics['processing_time_history']:
    print(f"⚡ Processing Time:")
    print(f"   Mean: {np.mean(metrics['processing_time_history']):.2f}s")
    print(f"   Total: {sum(metrics['processing_time_history']):.1f}s\n")

# Get final learning stats
learning_stats = learning_coordinator.get_learning_stats()

print(f"🎯 Final Learning State:")
print(f"   Pairs learned from: {learning_coordinator.pairs_learned_from}/{NUM_PAIRS} ({learning_coordinator.pairs_learned_from/NUM_PAIRS*100:.1f}%)")
print(f"   Hebbian patterns: {learning_stats.get('hebbian_patterns', 0)}")
print(f"   Organic families: {learning_stats.get('organic_families', 0)}")
print(f"   Mature families: {learning_stats.get('mature_families', 0)}\n")

# ================================================================
# TIER 5: SAVE TRAINING LOG
# ================================================================
print(f"💾 Saving training log...")

training_log_path = OUTPUT_DIR / f"epoch_{EPOCH_NUM}.json"
training_log = {
    'metadata': {
        'epoch_num': EPOCH_NUM,
        'timestamp': datetime.now().isoformat(),
        'num_pairs': NUM_PAIRS,
        'enable_phase2': ENABLE_PHASE2,
        'enable_salience': ENABLE_SALIENCE,
        'learning_threshold': LEARNING_THRESHOLD,
        'save_frequency': SAVE_FREQUENCY
    },
    'aggregate_metrics': {
        'success_rate': metrics['success_count'] / NUM_PAIRS,
        'error_count': metrics['error_count'],

        # OUTPUT confidence
        'mean_output_confidence': float(np.mean(metrics['output_confidence_history'])) if metrics['output_confidence_history'] else 0.0,

        # Satisfaction delta
        'mean_satisfaction_delta': float(np.mean(metrics['satisfaction_delta_history'])) if metrics['satisfaction_delta_history'] else 0.0,
        'positive_satisfaction_deltas': sum(1 for x in metrics['satisfaction_delta_history'] if x > 0),

        # Trauma reduction
        'mean_trauma_reduction': float(np.mean(metrics['trauma_reduction_history'])) if metrics['trauma_reduction_history'] else 0.0,
        'trauma_reduced_count': sum(1 for x in metrics['trauma_reduction_history'] if x > 0),

        # Learning
        'total_hebbian_updates': sum(metrics['hebbian_updates_history']) if metrics['hebbian_updates_history'] else 0,
        'final_hebbian_patterns': metrics['patterns_total_history'][-1] if metrics['patterns_total_history'] else 0,
        'family_maturations': sum(metrics['family_matured_history']) if metrics['family_matured_history'] else 0,
        'pairs_learned_from': learning_coordinator.pairs_learned_from,

        # Performance
        'mean_processing_time': float(np.mean(metrics['processing_time_history'])) if metrics['processing_time_history'] else 0.0
    },
    'learning_stats': learning_stats,
    'time_series': metrics,
    'pair_results': results
}

try:
    with open(training_log_path, 'w') as f:
        json.dump(training_log, f, indent=2)
    print(f"   ✅ Training log saved: {training_log_path}\n")
except Exception as e:
    print(f"   ❌ Error saving training log: {e}\n")

# ================================================================
# TIER 6: POST-TRAINING ANALYSIS (if available)
# ================================================================
print(f"4️⃣ TIER 4: POST-TRAINING ANALYSIS")
print("="*80 + "\n")

try:
    analyzer = PostTrainingAnalyzer()
    analysis_report = analyzer.analyze_epoch(
        epoch_num=EPOCH_NUM,
        training_log_path=str(training_log_path)
    )

    # Save analysis report
    analysis_path = OUTPUT_DIR / f"epoch_{EPOCH_NUM}_analysis.json"
    with open(analysis_path, 'w') as f:
        json.dump(analysis_report, f, indent=2)

    print(f"   ✅ Post-training analysis complete")
    print(f"   📊 Analysis saved: {analysis_path}\n")

except Exception as e:
    print(f"   ⚠️  Post-training analysis not available: {e}\n")

# ================================================================
# FINAL SUMMARY
# ================================================================
print(f"{'='*80}")
print(f"🌀 EPOCH {EPOCH_NUM} COMPLETE")
print(f"{'='*80}\n")

print(f"📁 Output files:")
print(f"   Training log: {training_log_path}")
print(f"   Hebbian memory: TSK/conversational_hebbian_memory.json")
print(f"   Organic families: persona_layer/organic_families.json\n")

print(f"📈 Key Results:")
print(f"   Success rate: {metrics['success_count']}/{NUM_PAIRS}")
print(f"   Mean OUTPUT confidence: {np.mean(metrics['output_confidence_history']):.3f}")
print(f"   Mean satisfaction delta: {np.mean(metrics['satisfaction_delta_history']):+.3f}")
print(f"   Mean trauma reduction: {np.mean(metrics['trauma_reduction_history']):+.3f}")
print(f"   Hebbian patterns learned: {learning_stats.get('hebbian_patterns', 0)}")
print(f"   Organic families: {learning_stats.get('organic_families', 0)}\n")

print(f"🎯 Next Steps:")
print(f"   1. Review training log: {training_log_path}")
print(f"   2. Inspect R-matrix: TSK/conversational_hebbian_memory.json")
print(f"   3. Inspect families: persona_layer/organic_families.json")
print(f"   4. Run Epoch 2 with new training pairs")
print(f"   5. Compare Epoch 1 vs Epoch 2 progress\n")

print(f"✅ EXPANDED TRAINING SESSION COMPLETE\n")
