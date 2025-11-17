#!/usr/bin/env python3
"""
Entity-Memory Epoch Training WITH TSK Logging + Organic Intelligence Metrics
Created: November 17, 2025
Enhanced: November 17, 2025 (Week 4 Day 1 - Organic Intelligence Integration)

CRITICAL: This version enables TSK logging for Superject learning and PRAXIS training.
ENHANCEMENT: Now includes comprehensive organic intelligence metrics for tracking
learning evolution across epochs.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Set PYTHONPATH
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.user_superject_learner import UserSuperjectLearner
from persona_layer.superject_structures import EnhancedUserProfile
from persona_layer.tsk_serialization_helper import tsk_to_dict_recursive, validate_json_serializable

# ✅ NEW: Import organic intelligence metrics
from training.organic_intelligence_metrics import OrganicIntelligenceEvaluator

print("\n" + "="*80)
print("🧠 ENTITY-MEMORY TRAINING WITH TSK LOGGING")
print("="*80 + "\n")

# ============================================================================
# CONFIGURATION
# ============================================================================

# Accept epoch number as command-line argument
EPOCH_NUM = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# Paths
TRAINING_PAIRS_PATH = "knowledge_base/entity_memory_training_pairs.json"
RESULTS_DIR = "results/epochs"
TSK_LOGS_DIR = f"results/tsk_logs/epoch_{EPOCH_NUM}"
EPOCH_DIR = f"results/epochs/epoch_{EPOCH_NUM}"

# Output files
MAIN_RESULTS_FILE = f"{RESULTS_DIR}/entity_memory_epoch_1_results.json"  # Backward compat
EPOCH_RESULTS_FILE = f"{EPOCH_DIR}/training_results.json"
EPOCH_METRICS_FILE = f"{EPOCH_DIR}/metrics_summary.json"
EPOCH_TSK_SUMMARY_FILE = f"{EPOCH_DIR}/tsk_summary.json"

# Training parameters
NUM_PAIRS = 50  # All 50 entity-memory pairs
ENABLE_PHASE2 = True  # Multi-cycle V0 convergence
ENABLE_TSK = True  # ✅ CRITICAL: Enable TSK logging for Superject/PRAXIS

print(f"📋 Configuration:")
print(f"   Epoch: {EPOCH_NUM}")
print(f"   Training pairs: {TRAINING_PAIRS_PATH}")
print(f"   Num pairs: {NUM_PAIRS}")
print(f"   Phase 2: {ENABLE_PHASE2}")
print(f"   TSK Recording: {ENABLE_TSK} ✅")
print(f"   Results: {EPOCH_RESULTS_FILE}")
print(f"   TSK Logs: {TSK_LOGS_DIR}\n")

# Create directories
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(TSK_LOGS_DIR, exist_ok=True)
os.makedirs(EPOCH_DIR, exist_ok=True)

# ============================================================================
# LOAD TRAINING DATA
# ============================================================================

print(f"📂 Loading entity-memory training pairs...")
try:
    with open(TRAINING_PAIRS_PATH) as f:
        data = json.load(f)
        training_pairs = data.get('training_pairs', [])
        metadata = data.get('metadata', {})

    print(f"   ✅ Loaded {len(training_pairs)} training pairs")
    print(f"   Categories: {metadata.get('num_categories', 'unknown')}")
    print(f"   Entities: {metadata.get('num_entities', 'unknown')}\n")

except Exception as e:
    print(f"   ❌ Error loading training pairs: {e}\n")
    sys.exit(1)

# ============================================================================
# INITIALIZE ORGANISM
# ============================================================================

print("🧬 Initializing organism...")
try:
    organism = ConversationalOrganismWrapper()
    print("   ✅ Organism initialized\n")
except Exception as e:
    print(f"   ❌ Error initializing organism: {e}\n")
    sys.exit(1)

# ============================================================================
# EVALUATION FUNCTION (WITH ENTITY MEMORY METRICS)
# ============================================================================

def evaluate_entity_prehension(pair: Dict, result: Dict) -> Dict:
    """
    Evaluate entity prehension performance.
    Measures actual NEXUS differentiation and entity memory activation.
    """
    felt_states = result.get('felt_states', {})

    # ✅ Check if entity prehension actually ran
    entity_prehension = felt_states.get('entity_prehension', {})
    entity_memory_available = entity_prehension.get('entity_memory_available', False)
    mentioned_entities = entity_prehension.get('mentioned_entities', [])

    # Entity recall accuracy = did we detect the expected entities?
    expected = pair.get('expected_prehension', {})
    expected_entities = set(expected.get('mentioned_entities', []))

    if expected_entities:
        detected_entities = set(e.get('name', '') for e in mentioned_entities)
        matched = expected_entities & detected_entities
        entity_recall_accuracy = len(matched) / len(expected_entities) if expected_entities else 0.0
    else:
        entity_recall_accuracy = 1.0 if not entity_memory_available else 0.0

    # ✅ Check if NEXUS differentiation executed
    nexus_differentiation_executed = False
    nexus_coherence_value = 0.0

    if entity_memory_available and mentioned_entities:
        organ_results = felt_states.get('organ_results', {})
        nexus_result = organ_results.get('NEXUS', {})
        nexus_coherence_value = nexus_result.get('coherence', 0.0)
        nexus_differentiation_executed = nexus_coherence_value > 0.0

    nexus_formation = nexus_differentiation_executed
    nexus_coherence = nexus_coherence_value

    # Emission correctness - check if emission mentions expected entities
    emission_text = felt_states.get('emission_text', '').lower()

    if expected_entities:
        mentioned_count = sum(1 for entity in expected_entities if entity.lower() in emission_text)
        emission_correctness = mentioned_count / len(expected_entities)
    else:
        emission_correctness = 0.5

    # ✅ Check if EntityOrganTracker was updated
    current_turn_entities = felt_states.get('current_turn_entities', [])
    entity_tracker_updated = len(current_turn_entities) > 0

    return {
        'entity_recall_accuracy': entity_recall_accuracy,
        'entity_memory_available': entity_memory_available,
        'mentioned_entity_count': len(mentioned_entities),
        'nexus_formation': nexus_formation,
        'nexus_coherence': nexus_coherence,
        'emission_correctness': emission_correctness,
        'entity_tracker_updated': entity_tracker_updated
    }

# ============================================================================
# TRAINING LOOP
# ============================================================================

print(f"🚀 Starting Epoch {EPOCH_NUM} training...\n")

results = []
metrics = {
    'entity_recall_accuracy': [],
    'entity_memory_available_rate': [],
    'nexus_formation_rate': [],
    'entity_tracker_update_rate': [],
    'emission_correctness': [],
    'confidence_history': [],
    'nexus_count_history': [],
    'cycle_history': [],
    'v0_final_history': [],
    'processing_time_history': []
}

# TSK aggregation
tsk_summary = {
    'epoch': EPOCH_NUM,
    'total_pairs': NUM_PAIRS,
    'zone_transitions': [],
    'polyvagal_trajectories': [],
    'kairos_detections': 0,
    'organ_signature_evolution': [],
    'transformation_pathways': []
}

# ✅ NEW: Initialize organic intelligence evaluator
intelligence_evaluator = OrganicIntelligenceEvaluator()

successful = 0
failed = 0

start_time = time.time()

for i, pair in enumerate(training_pairs[:NUM_PAIRS], 1):
    pair_id = pair.get('pair_id', f'pair_{i:03d}')
    input_text = pair['input']
    category = pair.get('category', 'unknown')
    difficulty = pair.get('difficulty', 'medium')

    print(f"{'='*80}")
    print(f"📝 Pair {i}/{NUM_PAIRS}: {pair_id}")
    print(f"{'='*80}")
    print(f"   Category: {category}")
    print(f"   Difficulty: {difficulty}")
    print(f"   Input: {input_text[:100]}...")

    try:
        # Process with organism
        processing_start = time.time()

        result = organism.process_text(
            input_text,
            enable_phase2=ENABLE_PHASE2,
            enable_tsk_recording=ENABLE_TSK,  # ✅ TSK ENABLED
            user_id=f"epoch_{EPOCH_NUM}_training",
            username="training_user"
        )

        processing_time = time.time() - processing_start

        # Extract metrics
        felt_states = result.get('felt_states', {})
        emission_confidence = felt_states.get('emission_confidence', 0.0)
        nexus_count = len(felt_states.get('nexuses_formed', []))
        cycles = felt_states.get('convergence_cycles', 1)
        v0_final = felt_states.get('v0_energy', {}).get('final_energy', 1.0)
        emission_path = felt_states.get('emission_path', 'unknown')

        # Evaluate entity prehension
        entity_eval = evaluate_entity_prehension(pair, result)

        # ✅ Save TSK log if available
        # ✅ FIX (Nov 17): Organism returns 'tsk_record', not 'tsk'!
        # ✅ FIX (Nov 17): Recursively convert nested TSK dataclasses to dicts
        if ENABLE_TSK and 'tsk_record' in result and result['tsk_record'] is not None:
            tsk_file = f"{TSK_LOGS_DIR}/{pair_id}_tsk.json"

            # Recursively convert ALL nested TSK objects to dicts
            tsk_data = tsk_to_dict_recursive(result['tsk_record'])

            # Validate serialization (debug)
            errors = validate_json_serializable(tsk_data)
            if errors:
                print(f"      ⚠️  TSK validation errors: {errors[:3]}")  # Show first 3

            with open(tsk_file, 'w') as f:
                json.dump(tsk_data, f, indent=2)

            # Aggregate TSK data (use dict version)
            # Extract from felt_states.tsk if nested
            felt_states_tsk = tsk_data.get('felt_states', {}).get('tsk', {})
            if felt_states_tsk:
                # Zone transitions (initial → final)
                initial_zone = felt_states_tsk.get('initial_zone')
                final_zone = felt_states_tsk.get('final_zone')
                if initial_zone is not None and final_zone is not None:
                    tsk_summary['zone_transitions'].append({
                        'from': initial_zone,
                        'to': final_zone,
                        'pair_id': pair_id
                    })

                # Polyvagal trajectory (initial → final)
                initial_pv = felt_states_tsk.get('initial_polyvagal_state')
                final_pv = felt_states_tsk.get('final_polyvagal_state')
                if initial_pv and final_pv:
                    tsk_summary['polyvagal_trajectories'].append({
                        'from': initial_pv,
                        'to': final_pv,
                        'pair_id': pair_id
                    })

                # Kairos detection
                if felt_states_tsk.get('kairos_detected', False):
                    tsk_summary['kairos_detections'] += 1

                # Organ signature evolution (57D) - store initial and final coherences
                tsk_summary['organ_signature_evolution'].append({
                    'pair_id': pair_id,
                    'initial': felt_states_tsk.get('initial_organ_coherences', {}),
                    'final': felt_states_tsk.get('final_organ_coherences', {}),
                    'v0_descent': felt_states_tsk.get('initial_v0_energy', 1.0) - felt_states_tsk.get('final_v0_energy', 0.5)
                })

                # Transformation pathways
                tsk_summary['transformation_pathways'].append({
                    'pair_id': pair_id,
                    'emission_path': felt_states_tsk.get('emission_path', 'unknown'),
                    'nexus_count': felt_states_tsk.get('nexus_count', 0),
                    'cycles': felt_states_tsk.get('convergence_cycles', 1)
                })

        print(f"   ✅ Processing complete ({processing_time:.2f}s)")
        print(f"      Convergence: {cycles} cycles")
        print(f"      V0 energy: 1.0 → {v0_final:.3f}")
        print(f"      Nexuses: {nexus_count}")
        print(f"      Emission confidence: {emission_confidence:.3f}")
        print(f"      Path: {emission_path}")
        print(f"      🧠 Entity recall accuracy: {entity_eval['entity_recall_accuracy']:.2f}")
        print(f"      🌀 Entity memory available: {'✅ Yes' if entity_eval['entity_memory_available'] else '❌ No'}")
        if entity_eval['entity_memory_available']:
            print(f"         Entities detected: {entity_eval['mentioned_entity_count']}")
        print(f"      🔗 NEXUS differentiation: {'✅ Executed' if entity_eval['nexus_formation'] else '❌ Not executed'}")
        if entity_eval['nexus_formation']:
            print(f"         NEXUS coherence: {entity_eval['nexus_coherence']:.3f}")
        print(f"      📝 EntityTracker updated: {'✅ Yes' if entity_eval['entity_tracker_updated'] else '❌ No'}")
        print(f"      💬 Emission correctness: {entity_eval['emission_correctness']:.2f}")
        # ✅ FIX (Nov 17): Only print if TSK was ACTUALLY saved
        if ENABLE_TSK and 'tsk_record' in result and result['tsk_record'] is not None:
            print(f"      📊 TSK logged: {TSK_LOGS_DIR}/{pair_id}_tsk.json")
        elif ENABLE_TSK:
            print(f"      ⚠️  TSK enabled but tsk_record not in result!")

        # Store results
        results.append({
            'pair_id': pair_id,
            'category': category,
            'difficulty': difficulty,
            'input_length': len(input_text),
            'emission_confidence': emission_confidence,
            'nexus_count': nexus_count,
            'cycles': cycles,
            'v0_final': v0_final,
            'processing_time': processing_time,
            'emission_path': emission_path,
            'entity_recall_accuracy': entity_eval['entity_recall_accuracy'],
            'entity_memory_available': entity_eval['entity_memory_available'],
            'mentioned_entity_count': entity_eval['mentioned_entity_count'],
            'nexus_formation': entity_eval['nexus_formation'],
            'nexus_coherence': entity_eval['nexus_coherence'],
            'entity_tracker_updated': entity_eval['entity_tracker_updated'],
            'emission_correctness': entity_eval['emission_correctness'],
            'success': True,
            # ✅ FIX (Nov 17): Only record if TSK was actually saved
            'tsk_file': f"{pair_id}_tsk.json" if (ENABLE_TSK and 'tsk_record' in result and result['tsk_record'] is not None) else None
        })

        # Update metrics
        metrics['entity_recall_accuracy'].append(entity_eval['entity_recall_accuracy'])
        metrics['entity_memory_available_rate'].append(1 if entity_eval['entity_memory_available'] else 0)
        metrics['nexus_formation_rate'].append(1 if entity_eval['nexus_formation'] else 0)
        metrics['entity_tracker_update_rate'].append(1 if entity_eval['entity_tracker_updated'] else 0)
        metrics['emission_correctness'].append(entity_eval['emission_correctness'])
        metrics['confidence_history'].append(emission_confidence)
        metrics['nexus_count_history'].append(nexus_count)
        metrics['cycle_history'].append(cycles)
        metrics['v0_final_history'].append(v0_final)
        metrics['processing_time_history'].append(processing_time)

        successful += 1

    except Exception as e:
        print(f"   ❌ Error processing pair: {e}")
        results.append({
            'pair_id': pair_id,
            'category': category,
            'difficulty': difficulty,
            'error': str(e),
            'success': False
        })
        failed += 1

    print()

elapsed_time = time.time() - start_time

# ============================================================================
# COMPUTE AGGREGATE METRICS
# ============================================================================

print("="*80)
print("📊 COMPUTING AGGREGATE METRICS")
print("="*80 + "\n")

import numpy as np

def safe_mean(values):
    return float(np.mean(values)) if values else 0.0

aggregate = {
    'entity_recall_accuracy_mean': safe_mean(metrics['entity_recall_accuracy']),
    'entity_memory_available_rate': safe_mean(metrics['entity_memory_available_rate']),
    'nexus_formation_rate': safe_mean(metrics['nexus_formation_rate']),
    'entity_tracker_update_rate': safe_mean(metrics['entity_tracker_update_rate']),
    'emission_correctness_mean': safe_mean(metrics['emission_correctness']),
    'confidence_mean': safe_mean(metrics['confidence_history']),
    'nexus_count_mean': safe_mean(metrics['nexus_count_history']),
    'cycles_mean': safe_mean(metrics['cycle_history']),
    'v0_final_mean': safe_mean(metrics['v0_final_history']),
    'processing_time_mean': safe_mean(metrics['processing_time_history'])
}

print(f"📈 Entity Memory Metrics:")
print(f"   Entity recall accuracy: {aggregate['entity_recall_accuracy_mean']*100:.1f}%")
print(f"   Entity memory available: {aggregate['entity_memory_available_rate']*100:.1f}%")
print(f"   NEXUS formation rate: {aggregate['nexus_formation_rate']*100:.1f}%")
print(f"   EntityTracker update rate: {aggregate['entity_tracker_update_rate']*100:.1f}%")
print(f"   Emission correctness: {aggregate['emission_correctness_mean']*100:.1f}%\n")

print(f"📊 General Metrics:")
print(f"   Mean confidence: {aggregate['confidence_mean']:.3f}")
print(f"   Mean nexus count: {aggregate['nexus_count_mean']:.1f}")
print(f"   Mean cycles: {aggregate['cycles_mean']:.1f}")
print(f"   Mean V0 final: {aggregate['v0_final_mean']:.3f}")
print(f"   Mean processing time: {aggregate['processing_time_mean']:.2f}s\n")

print(f"✅ Success: {successful}/{NUM_PAIRS} ({successful/NUM_PAIRS*100:.1f}%)")
print(f"❌ Failed: {failed}/{NUM_PAIRS}\n")

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("💾 Saving results...\n")

# ✅ NEW: Compute organic intelligence metrics
print("🧠 Computing organic intelligence metrics...\n")
try:
    # Load Hebbian memory and build pattern database structure
    from persona_layer.conversational_hebbian_memory import ConversationalHebbianMemory
    import json
    import os

    memory = ConversationalHebbianMemory()

    # Build pattern_database from ConversationalHebbianMemory patterns
    # The intelligence metrics expects: {'patterns': {pattern_id: {'phrases': {phrase_text: {...}}}}}
    # ConversationalHebbianMemory has: cascade_patterns, response_patterns, polyvagal_patterns, self_energy_patterns

    all_patterns = {}
    pattern_id = 0

    # Aggregate all pattern types from Hebbian memory
    for pattern_type, patterns_data in [
        ('cascade', memory.cascade_patterns),
        ('response', memory.response_patterns),
        ('polyvagal', memory.polyvagal_patterns),
        ('self_energy', memory.self_energy_patterns)
    ]:
        # Handle both dict and list pattern storage
        if isinstance(patterns_data, dict):
            for key, pattern_data in patterns_data.items():
                pattern_id += 1
                # Build compatible structure - phrases must be a DICT not a list!
                quality = pattern_data.get('success_rate', 0.5) if isinstance(pattern_data, dict) else 0.5
                count = pattern_data.get('count', 1) if isinstance(pattern_data, dict) else 1

                all_patterns[f"{pattern_type}_{pattern_id}"] = {
                    'phrases': {
                        key: {  # phrase_text → phrase_data mapping
                            'quality': quality,
                            'count': count
                        }
                    },
                    'type': pattern_type
                }
        elif isinstance(patterns_data, list):
            for idx, pattern_item in enumerate(patterns_data):
                pattern_id += 1
                # Handle list of patterns
                if isinstance(pattern_item, dict):
                    phrase = pattern_item.get('pattern', f"pattern_{idx}")
                    quality = pattern_item.get('success_rate', 0.5)
                    count = pattern_item.get('count', 1)
                else:
                    # List of strings
                    phrase = str(pattern_item)
                    quality = 0.5
                    count = 1

                all_patterns[f"{pattern_type}_{pattern_id}"] = {
                    'phrases': {
                        phrase: {  # phrase_text → phrase_data mapping
                            'quality': quality,
                            'count': count
                        }
                    },
                    'type': pattern_type
                }

    pattern_database = {
        'patterns': all_patterns,
        'total_patterns': len(all_patterns),
        'source': 'ConversationalHebbianMemory'
    }

    epoch_results_data = {
        'results': results,
        'aggregate_metrics': aggregate
    }

    intelligence_metrics = intelligence_evaluator.evaluate_epoch(
        epoch=EPOCH_NUM,
        pattern_database=pattern_database,
        epoch_results=epoch_results_data,
        training_corpus=training_pairs[:NUM_PAIRS]
    )

    # Display intelligence emergence report
    print("="*80)
    print("🌀 ORGANIC INTELLIGENCE EMERGENCE REPORT")
    print("="*80 + "\n")

    print(f"🎯 Intelligence Emergence Score: {intelligence_metrics.intelligence_emergence_score:.1f}/100")
    print(f"📊 Maturity Level: {intelligence_metrics.maturity_level}\n")

    print("📚 Pattern Learning:")
    pl = intelligence_metrics.pattern_learning
    print(f"   Total patterns: {pl.total_patterns}")
    print(f"   Total phrases: {pl.total_phrases}")
    print(f"   High quality phrases: {pl.high_quality_phrase_count} ({pl.high_quality_rate*100:.1f}%)")
    print(f"   Mean phrase quality: {pl.mean_phrase_quality:.3f}")
    print(f"   Learning velocity: {pl.learning_velocity:.3f}")
    print(f"   Convergence rate: {pl.convergence_rate:.3f}")
    if pl.zipf_alpha > 0:
        print(f"   Zipf's law: α={pl.zipf_alpha:.3f}, R²={pl.zipf_r_squared:.3f}")
        if pl.zipf_r_squared >= 0.85:
            print(f"      ✅ Personality emergence detected!")
    print()

    print("💬 Human Fluency:")
    hf = intelligence_metrics.human_fluency
    print(f"   Organic emission rate: {hf.organic_emission_rate*100:.1f}%")
    print(f"   LLM fallback rate: {hf.llm_fallback_rate*100:.1f}%")
    print(f"   Mean satisfaction: {hf.mean_satisfaction:.3f}")
    print(f"   Restorative success: {hf.restorative_success_rate*100:.1f}%")
    print(f"   Concrescent success: {hf.concrescent_success_rate*100:.1f}%")
    print()

    print("🌍 Generalization:")
    gen = intelligence_metrics.generalization
    print(f"   Total families: {gen.family_count}")
    print(f"   Mean family size: {gen.mean_family_size:.1f}")
    print(f"   Family separation: {gen.family_separation:.3f}")
    print(f"   Pattern reuse rate: {gen.pattern_reuse_rate*100:.1f}%")
    print(f"   Novel situation handling: {gen.novel_situation_handling:.3f}")
    print()

    print("📡 Learning Signals:")
    ls = intelligence_metrics.learning_signals
    print(f"   Learning update rate: {ls.learning_update_rate*100:.1f}%")
    print(f"   Satisfaction signal strength: {ls.satisfaction_signal_strength:.3f}")
    print(f"   Mean convergence cycles: {ls.mean_convergence_cycles:.1f}")
    print(f"   Nexus formation rate: {ls.nexus_formation_rate*100:.1f}%")
    print(f"   Mean nexuses per input: {ls.mean_nexuses_per_input:.1f}")
    print()

    # Save intelligence metrics
    intelligence_file = f"{EPOCH_DIR}/intelligence_metrics.json"
    intelligence_dict = {
        'epoch': intelligence_metrics.epoch,
        'intelligence_emergence_score': intelligence_metrics.intelligence_emergence_score,
        'maturity_level': intelligence_metrics.maturity_level,
        'pattern_learning': {
            'total_patterns': pl.total_patterns,
            'total_phrases': pl.total_phrases,
            'mean_phrase_quality': pl.mean_phrase_quality,
            'high_quality_phrase_count': pl.high_quality_phrase_count,
            'high_quality_rate': pl.high_quality_rate,
            'learning_velocity': pl.learning_velocity,
            'convergence_rate': pl.convergence_rate,
            'zipf_alpha': pl.zipf_alpha,
            'zipf_r_squared': pl.zipf_r_squared
        },
        'human_fluency': {
            'organic_emission_rate': hf.organic_emission_rate,
            'llm_fallback_rate': hf.llm_fallback_rate,
            'mean_satisfaction': hf.mean_satisfaction,
            'restorative_success_rate': hf.restorative_success_rate,
            'concrescent_success_rate': hf.concrescent_success_rate
        },
        'generalization': {
            'family_count': gen.family_count,
            'mean_family_size': gen.mean_family_size,
            'family_separation': gen.family_separation,
            'pattern_reuse_rate': gen.pattern_reuse_rate,
            'context_transfer_success': gen.context_transfer_success,
            'novel_situation_handling': gen.novel_situation_handling,
            'crisis_handling_confidence': gen.crisis_handling_confidence,
            'stable_handling_confidence': gen.stable_handling_confidence
        },
        'learning_signals': {
            'learning_update_rate': ls.learning_update_rate,
            'delayed_feedback_lag': ls.delayed_feedback_lag,
            'satisfaction_signal_strength': ls.satisfaction_signal_strength,
            'base_ema_contribution': ls.base_ema_contribution,
            'satisfaction_fingerprint_contribution': ls.satisfaction_fingerprint_contribution,
            'lyapunov_stability_contribution': ls.lyapunov_stability_contribution,
            'total_quality_boost': ls.total_quality_boost,
            'mean_convergence_cycles': ls.mean_convergence_cycles,
            'nexus_formation_rate': ls.nexus_formation_rate,
            'mean_nexuses_per_input': ls.mean_nexuses_per_input,
            'restorative_trajectory_detection': ls.restorative_trajectory_detection,
            'concrescent_trajectory_detection': ls.concrescent_trajectory_detection,
            'plateaued_trajectory_detection': ls.plateaued_trajectory_detection,
            'trajectory_classification_accuracy': ls.trajectory_classification_accuracy
        }
    }

    with open(intelligence_file, 'w') as f:
        json.dump(intelligence_dict, f, indent=2)
    print(f"   ✅ Intelligence metrics: {intelligence_file}\n")

except Exception as e:
    print(f"   ⚠️  Error computing intelligence metrics: {e}\n")
    intelligence_metrics = None

try:
    # Main output (backward compat)
    output = {
        'epoch': EPOCH_NUM,
        'timestamp': datetime.now().isoformat(),
        'elapsed_time': elapsed_time,
        'successful': successful,
        'failed': failed,
        'aggregate_metrics': aggregate,
        'results': results,
        'metrics': {
            'entity_recall_accuracy': metrics['entity_recall_accuracy'],
            'entity_memory_available_rate': metrics['entity_memory_available_rate'],
            'nexus_formation_rate': metrics['nexus_formation_rate'],
            'entity_tracker_update_rate': metrics['entity_tracker_update_rate'],
            'emission_correctness': metrics['emission_correctness'],
            'confidence_history': metrics['confidence_history'],
            'nexus_count_history': metrics['nexus_count_history'],
            'cycle_history': metrics['cycle_history'],
            'v0_final_history': metrics['v0_final_history'],
            'processing_time_history': metrics['processing_time_history']
        }
    }

    # Save main results (backward compat)
    with open(MAIN_RESULTS_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"   ✅ Main results: {MAIN_RESULTS_FILE}")

    # Save epoch-specific results
    with open(EPOCH_RESULTS_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"   ✅ Epoch results: {EPOCH_RESULTS_FILE}")

    # Save metrics summary
    with open(EPOCH_METRICS_FILE, 'w') as f:
        json.dump(aggregate, f, indent=2)
    print(f"   ✅ Metrics summary: {EPOCH_METRICS_FILE}")

    # Save TSK summary if enabled
    if ENABLE_TSK:
        with open(EPOCH_TSK_SUMMARY_FILE, 'w') as f:
            json.dump(tsk_summary, f, indent=2)
        print(f"   ✅ TSK summary: {EPOCH_TSK_SUMMARY_FILE}")
        print(f"   ✅ TSK logs: {TSK_LOGS_DIR}/ ({NUM_PAIRS} files)")

    print()

except Exception as e:
    print(f"   ❌ Error saving results: {e}\n")

print("="*80)
print(f"🌀 EPOCH {EPOCH_NUM} TRAINING COMPLETE")
print("="*80 + "\n")

print("📋 Results Locations:")
print(f"   Main: {MAIN_RESULTS_FILE}")
print(f"   Epoch: {EPOCH_RESULTS_FILE}")
print(f"   Metrics: {EPOCH_METRICS_FILE}")
print(f"   Intelligence: {EPOCH_DIR}/intelligence_metrics.json")
if ENABLE_TSK:
    print(f"   TSK Summary: {EPOCH_TSK_SUMMARY_FILE}")
    print(f"   TSK Logs: {TSK_LOGS_DIR}/")
print()

print("📊 Next Steps:")
print(f"   1. Review metrics in {EPOCH_METRICS_FILE}")
print(f"   2. Review intelligence emergence in {EPOCH_DIR}/intelligence_metrics.json")
if intelligence_metrics:
    print(f"   3. Track organic emission evolution: {intelligence_metrics.human_fluency.organic_emission_rate*100:.1f}%")
    print(f"   4. Monitor maturity progression: {intelligence_metrics.maturity_level}")
if ENABLE_TSK:
    print(f"   5. Analyze TSK logs for transformation patterns")
    print(f"   6. Use TSK data for Superject learning")
    print(f"   7. Train PRAXIS organ with TSK-enriched data")
print(f"   8. Run next epoch with: python3 training/entity_memory_epoch_training_with_tsk.py {EPOCH_NUM + 1}")
print()
