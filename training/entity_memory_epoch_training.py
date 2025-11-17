"""
Entity-Memory Training Session - Week 1 of Sequential Training Plan
====================================================================

Trains organism on 50 entity-memory pairs to develop:
- NEXUS organ activation on entity mentions
- Pre-emission entity prehension retrieval
- Entity Memory Nexus formation (coherence > 0.7)
- Entity-organ association strengthening
- Hebbian learning of entity patterns

Training Methodology:
- Each pair has pre-existing entities stored in user profile
- Input requires entity recall/resolution
- Success measured by entity recall accuracy, nexus formation, emission correctness

Expected Learning Trajectory (from training plan):
- Epoch 1: Entity recall 45%, Nexus formation 15%, Emission correctness 40%
- Epoch 10: Entity recall 65%, Nexus formation 35%, Emission correctness 60%
- Epoch 20: Entity recall 75%, Nexus formation 50%, Emission correctness 75%
- Epoch 40: Entity recall 85%, Nexus formation 70%, Emission correctness 90%

Date: November 16, 2025
Phase: Entity-Memory Training (Week 1)
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
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.user_superject_learner import UserSuperjectLearner
from persona_layer.superject_structures import EnhancedUserProfile

print("\n" + "="*80)
print("🧠 ENTITY-MEMORY TRAINING SESSION - WEEK 1 SEQUENTIAL TRAINING")
print("="*80 + "\n")

# Configuration
TRAINING_PAIRS_PATH = "knowledge_base/entity_memory_training_pairs.json"
OUTPUT_PATH = "results/epochs/entity_memory_epoch_1_results.json"
NUM_PAIRS = 50  # All 50 entity-memory pairs
ENABLE_PHASE2 = True  # Multi-cycle V0 convergence
ENABLE_TSK = False  # Don't need full TSK recording for this training

print(f"📋 Configuration:")
print(f"   Training pairs: {TRAINING_PAIRS_PATH}")
print(f"   Num pairs: {NUM_PAIRS}")
print(f"   Phase 2: {ENABLE_PHASE2}")
print(f"   TSK Recording: {ENABLE_TSK}")
print(f"   Output: {OUTPUT_PATH}\n")

# Load training pairs
print(f"📂 Loading entity-memory training pairs...")
try:
    with open(TRAINING_PAIRS_PATH) as f:
        data = json.load(f)
        training_pairs = data.get('training_pairs', [])
        metadata = data.get('metadata', {})

    print(f"   ✅ Loaded {len(training_pairs)} training pairs")
    print(f"   Categories: {list(metadata.get('categories', {}).keys())}")
    print(f"   Total pairs: {metadata.get('total_pairs', 0)}")
    print(f"   Version: {metadata.get('version', 'unknown')}\n")
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

# Initialize user profile learner
print(f"👤 Initializing user profile learner...")
try:
    learner = UserSuperjectLearner()
    print(f"   ✅ Learner initialized\n")
except Exception as e:
    print(f"   ❌ Error initializing learner: {e}")
    traceback.print_exc()
    sys.exit(1)

# Training loop
results = []
metrics = {
    'entity_recall_accuracy': [],  # Did organism retrieve correct entities?
    'nexus_formation_rate': [],     # Did Entity Memory Nexus form?
    'emission_correctness': [],     # Does emission mention expected entities?
    'nexus_coherence': [],          # Entity Memory Nexus coherence values
    'confidence_history': [],
    'nexus_count_history': [],
    'cycle_history': [],
    'v0_final_history': [],
    'processing_time_history': [],
    'error_count': 0,
    'success_count': 0
}

def setup_user_profile(pair: Dict) -> str:
    """
    Set up user profile with pre-existing entities for this training pair.

    Args:
        pair: Training pair with 'setup' containing user_id and pre_existing_entities

    Returns:
        user_id to use for this pair
    """
    setup = pair.get('setup', {})
    user_id = setup.get('user_id', 'training_user')
    pre_existing = setup.get('pre_existing_entities', {})

    # Get or create profile
    profile = learner.get_or_create_profile(user_id)

    # Store pre-existing entities
    if pre_existing:
        profile.store_entities(pre_existing)
        learner.save_profile(profile)

    return user_id

def evaluate_entity_prehension(pair: Dict, result: Dict) -> Dict:
    """
    Evaluate if entity prehension worked correctly.

    Returns dict with:
    - entity_recall_accuracy: 0.0-1.0 (were expected entities retrieved?)
    - nexus_formation: bool (did Entity Memory Nexus form?)
    - emission_correctness: 0.0-1.0 (does emission mention expected entities?)
    - nexus_coherence: float (Entity Memory Nexus coherence if formed)
    """
    expected = pair.get('expected_prehension', {})
    expected_entities = set(expected.get('mentioned_entities', []))

    # Check if entities were retrieved (would be in felt_states entity context)
    felt_states = result.get('felt_states', {})

    # ✅ FIX (Nov 16, 2025): Measure actual entity prehension, not placeholder
    # Check if entity prehension actually ran and detected entities
    entity_prehension = felt_states.get('entity_prehension', {})
    entity_memory_available = entity_prehension.get('entity_memory_available', False)
    mentioned_entities = entity_prehension.get('mentioned_entities', [])

    # Entity recall accuracy = did we detect the expected entities?
    if expected_entities:
        detected_entities = set(e.get('name', '') for e in mentioned_entities)
        matched = expected_entities & detected_entities
        entity_recall_accuracy = len(matched) / len(expected_entities) if expected_entities else 0.0
    else:
        # No entities expected - score based on whether prehension ran appropriately
        entity_recall_accuracy = 1.0 if not entity_memory_available else 0.0

    # ✅ FIX (Nov 16, 2025): Check if NEXUS differentiation executed
    # NEXUS organ should activate with entity context and >0 coherence
    nexus_differentiation_executed = False
    nexus_coherence_value = 0.0

    if entity_memory_available and mentioned_entities:
        # Check organ results for NEXUS activation
        organ_results = felt_states.get('organ_results', {})
        nexus_result = organ_results.get('NEXUS', {})
        nexus_coherence_value = nexus_result.get('coherence', 0.0)
        nexus_differentiation_executed = nexus_coherence_value > 0.0

    nexus_formation = nexus_differentiation_executed
    nexus_coherence = nexus_coherence_value

    # Emission correctness - check if emission mentions expected entities
    emission_text = felt_states.get('emission_text', '').lower()

    # Simple heuristic: count how many expected entities appear in emission
    if expected_entities:
        mentioned_count = sum(1 for entity in expected_entities if entity.lower() in emission_text)
        emission_correctness = mentioned_count / len(expected_entities)
    else:
        emission_correctness = 0.5  # No entities expected, neutral score

    # ✅ FIX (Nov 16, 2025): Check if EntityOrganTracker was updated
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

print(f"🎯 Beginning entity-memory training loop ({NUM_PAIRS} pairs)...\n")
print(f"{'='*80}\n")

for idx, pair in enumerate(training_pairs[:NUM_PAIRS], 1):
    pair_id = pair.get('pair_id', f'pair_{idx}')
    category = pair.get('category', 'unknown')
    difficulty = pair.get('difficulty', 'medium')
    input_text = pair['input']
    expected_output = pair['output']

    print(f"📝 Training Pair {idx}/{NUM_PAIRS}")
    print(f"   ID: {pair_id}")
    print(f"   Category: {category}")
    print(f"   Difficulty: {difficulty}")
    print(f"   Input: \"{input_text[:60]}...\" ({len(input_text)} chars)")

    # Set up user profile with pre-existing entities
    try:
        user_id = setup_user_profile(pair)
        setup = pair.get('setup', {})
        pre_existing = setup.get('pre_existing_entities', {})
        entity_count = len(pre_existing.get('relationships', []))
        print(f"   👤 User: {user_id} ({entity_count} pre-existing entities)")
    except Exception as e:
        print(f"   ⚠️  Error setting up profile: {e}")
        user_id = 'training_user'

    start_time = time.time()

    try:
        # Process through Phase 2 with entity prehension
        result = wrapper.process_text(
            input_text,
            context={'pair_id': pair_id, 'category': category},
            user_id=user_id,  # CRITICAL: Pass user_id for entity prehension
            enable_tsk_recording=ENABLE_TSK,
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

        # Evaluate entity-specific metrics
        entity_eval = evaluate_entity_prehension(pair, result)

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

        # Truncate emission for display
        if emission_text:
            display_emission = emission_text[:80] + "..." if len(emission_text) > 80 else emission_text
            print(f"      Emission: \"{display_emission}\"")

        # Store results (✅ Nov 16: Added new entity memory metrics)
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
            'success': True
        })

        # Update metrics
        metrics['entity_recall_accuracy'].append(entity_eval['entity_recall_accuracy'])
        metrics['nexus_formation_rate'].append(1.0 if entity_eval['nexus_formation'] else 0.0)
        metrics['emission_correctness'].append(entity_eval['emission_correctness'])
        metrics['nexus_coherence'].append(entity_eval['nexus_coherence'])
        metrics['confidence_history'].append(emission_confidence)
        metrics['nexus_count_history'].append(nexus_count)
        metrics['cycle_history'].append(cycles)
        metrics['v0_final_history'].append(v0_final)
        metrics['processing_time_history'].append(processing_time)
        metrics['success_count'] += 1

    except Exception as e:
        processing_time = time.time() - start_time
        print(f"   ❌ Error processing pair: {e}")
        traceback.print_exc()

        results.append({
            'pair_id': pair_id,
            'category': category,
            'error': str(e),
            'processing_time': processing_time,
            'success': False
        })

        metrics['error_count'] += 1

    print()  # Blank line between pairs

# Training complete - summarize
print("="*80)
print("📊 ENTITY-MEMORY TRAINING SUMMARY")
print("="*80 + "\n")

print(f"✅ Success: {metrics['success_count']}/{NUM_PAIRS} pairs")
print(f"❌ Errors: {metrics['error_count']}/{NUM_PAIRS} pairs\n")

if metrics['entity_recall_accuracy']:
    print(f"🧠 Entity Recall Accuracy:")
    print(f"   Mean: {np.mean(metrics['entity_recall_accuracy']):.2%}")
    print(f"   Std:  {np.std(metrics['entity_recall_accuracy']):.2%}")
    print(f"   Target Epoch 1: 45% (baseline)\n")

if metrics['nexus_formation_rate']:
    formation_rate = np.mean(metrics['nexus_formation_rate'])
    print(f"🔗 Entity Memory Nexus Formation:")
    print(f"   Rate: {formation_rate:.2%}")
    print(f"   Target Epoch 1: 15% (baseline)\n")

if metrics['nexus_coherence']:
    active_coherences = [c for c in metrics['nexus_coherence'] if c > 0]
    if active_coherences:
        print(f"   Mean coherence (when formed): {np.mean(active_coherences):.3f}")
        print(f"   Target: > 0.7\n")

if metrics['emission_correctness']:
    print(f"💬 Emission Entity Correctness:")
    print(f"   Mean: {np.mean(metrics['emission_correctness']):.2%}")
    print(f"   Std:  {np.std(metrics['emission_correctness']):.2%}")
    print(f"   Target Epoch 1: 40% (baseline)\n")

if metrics['confidence_history']:
    print(f"📈 General Metrics:")
    print(f"   Mean confidence: {np.mean(metrics['confidence_history']):.3f}")
    print(f"   Mean nexuses: {np.mean(metrics['nexus_count_history']):.1f}")
    print(f"   Mean cycles: {np.mean(metrics['cycle_history']):.1f}")
    print(f"   Mean V0 final: {np.mean(metrics['v0_final_history']):.3f}")
    print(f"   Mean processing time: {np.mean(metrics['processing_time_history']):.2f}s\n")

# Save results
print(f"💾 Saving results to {OUTPUT_PATH}...")
try:
    # Ensure results directory exists
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    output = {
        'metadata': {
            'timestamp': datetime.utcnow().isoformat(),
            'training_type': 'entity_memory_epoch_1',
            'num_pairs': NUM_PAIRS,
            'enable_phase2': ENABLE_PHASE2,
            'enable_tsk': ENABLE_TSK
        },
        'summary': {
            'success_count': metrics['success_count'],
            'error_count': metrics['error_count'],
            'mean_entity_recall_accuracy': float(np.mean(metrics['entity_recall_accuracy'])) if metrics['entity_recall_accuracy'] else 0.0,
            'nexus_formation_rate': float(np.mean(metrics['nexus_formation_rate'])) if metrics['nexus_formation_rate'] else 0.0,
            'mean_emission_correctness': float(np.mean(metrics['emission_correctness'])) if metrics['emission_correctness'] else 0.0,
            'mean_nexus_coherence': float(np.mean([c for c in metrics['nexus_coherence'] if c > 0])) if any(c > 0 for c in metrics['nexus_coherence']) else 0.0,
            'mean_confidence': float(np.mean(metrics['confidence_history'])) if metrics['confidence_history'] else 0.0,
            'mean_nexus_count': float(np.mean(metrics['nexus_count_history'])) if metrics['nexus_count_history'] else 0.0,
            'mean_cycles': float(np.mean(metrics['cycle_history'])) if metrics['cycle_history'] else 0.0,
            'mean_processing_time': float(np.mean(metrics['processing_time_history'])) if metrics['processing_time_history'] else 0.0
        },
        'detailed_results': results,
        'metrics': {
            'entity_recall_accuracy': metrics['entity_recall_accuracy'],
            'nexus_formation_rate': metrics['nexus_formation_rate'],
            'emission_correctness': metrics['emission_correctness'],
            'nexus_coherence': metrics['nexus_coherence'],
            'confidence_history': metrics['confidence_history'],
            'nexus_count_history': metrics['nexus_count_history'],
            'cycle_history': metrics['cycle_history'],
            'v0_final_history': metrics['v0_final_history'],
            'processing_time_history': metrics['processing_time_history']
        }
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"   ✅ Results saved\n")

except Exception as e:
    print(f"   ❌ Error saving results: {e}\n")

print("="*80)
print("🌀 ENTITY-MEMORY TRAINING COMPLETE")
print("="*80 + "\n")

print("📋 Next Steps:")
print("   1. Review results in:", OUTPUT_PATH)
print("   2. Compare against baseline targets:")
print("      - Entity recall: 45% (target)")
print("      - Nexus formation: 15% (target)")
print("      - Emission correctness: 40% (target)")
print("   3. If metrics below targets, investigate entity prehension integration")
print("   4. Run additional epochs (10, 20) to track learning trajectory")
print("   5. Week 2: Temporal awareness + session continuity training\n")
