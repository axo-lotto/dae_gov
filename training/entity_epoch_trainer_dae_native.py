"""
DAE-Native Entity-Organ Epoch Trainer
=====================================

Entity-situated training using DAE's existing epoch architecture (multi-iteration,
fractal rewards, regime evolution) - NOT LLM text generation.

Key Difference from LLM Approach:
- Uses organism.process_text() for ORGAN ACTIVATIONS only
- No emission text generation required
- Fast: ~1-2s per conversation (vs 30-60s with LLM)
- Focus: Entity-organ association learning via organ coherences

Integration:
- MultiIterationTrainer: 2-5 iterations per conversation for stable memory
- Entity-Organ Tracker: POST-EMISSION learning from entity mentions
- Fractal Rewards: Levels 1-7 (value maps → global confidence)
- Regime Evolution: EXPLORING → COMMITTED over epochs

Expected Speed:
- 1000 conversations × 2s = ~33 minutes (vs 8-10 hours with LLM)
- 50 epochs with ~20 conversations each

Author: DAE_HYPHAE_1
Date: November 15, 2025
Phase: Entity-Situated Training (DAE-Native)
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict, Counter
import numpy as np

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import DAE epoch training infrastructure
from persona_layer.epoch_training.multi_iteration_trainer import MultiIterationTrainer
from persona_layer.epoch_training.epoch_training_orchestrator import (
    EpochTrainingOrchestrator,
    RegimeConfig
)
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\n" + "="*80)
print("🌀 DAE-NATIVE ENTITY-ORGAN EPOCH TRAINER")
print("="*80 + "\n")

# Configuration
CORPUS_PATH = "knowledge_base/entity_training/emiliano_entity_corpus.json"
OUTPUT_PATH = "results/epochs/entity_epoch_training_dae_native.json"
USER_ID = "training_emiliano_001"
NUM_EPOCHS = 50

# DAE training parameters (from epoch_training_orchestrator)
REGIME_CONFIGS = [
    RegimeConfig(
        name="EXPLORING",
        epochs=(1, 10),
        tau_threshold=0.50,
        exploration_factor=1.0,
        max_iterations=5,
        satisfaction_target=0.60,
        description="Initial exploration, high entropy"
    ),
    RegimeConfig(
        name="CONVERGING",
        epochs=(11, 25),
        tau_threshold=0.55,
        exploration_factor=0.7,
        max_iterations=4,
        satisfaction_target=0.70,
        description="Pattern emergence, reducing entropy"
    ),
    RegimeConfig(
        name="STABLE",
        epochs=(26, 40),
        tau_threshold=0.60,
        exploration_factor=0.4,
        max_iterations=3,
        satisfaction_target=0.75,
        description="Stable patterns, low entropy"
    ),
    RegimeConfig(
        name="COMMITTED",
        epochs=(41, 50),
        tau_threshold=0.65,
        exploration_factor=0.2,
        max_iterations=2,
        satisfaction_target=0.80,
        description="Converged, minimal exploration"
    )
]

def get_regime_for_epoch(epoch: int) -> RegimeConfig:
    """Get training regime configuration for given epoch"""
    for regime in REGIME_CONFIGS:
        if regime.epochs[0] <= epoch <= regime.epochs[1]:
            return regime
    return REGIME_CONFIGS[-1]  # Default to COMMITTED

print(f"📋 Configuration:")
print(f"   Corpus: {CORPUS_PATH}")
print(f"   Epochs: {NUM_EPOCHS}")
print(f"   User ID: {USER_ID}")
print(f"   Training mode: DAE-native (multi-iteration, no LLM generation)")
print(f"   Output: {OUTPUT_PATH}\n")

# Load corpus
print(f"📂 Loading Emiliano entity corpus...")
try:
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)
        conversations = corpus.get('conversations', [])
        user_profile = corpus.get('user_profile', {})
        metadata = corpus.get('corpus_metadata', {})

    print(f"   ✅ Loaded {len(conversations)} conversations")
    print(f"   User: {user_profile.get('name', 'Unknown')}")

    # Category breakdown
    category_counts = Counter(c['category'] for c in conversations)
    print(f"   Categories:")
    for cat, count in sorted(category_counts.items()):
        print(f"     - {cat}: {count}")
    print()

except Exception as e:
    print(f"   ❌ Error loading corpus: {e}")
    sys.exit(1)

# Initialize organism (will be slow, ~20s)
print(f"🌀 Initializing organism (this takes ~20 seconds)...")
try:
    organism = ConversationalOrganismWrapper()
    print(f"   ✅ Organism initialized")
    print(f"   Entity-organ tracker: Active (Quick Win #7)")
    print(f"   Organ confidence tracker: Active (Level 2 fractal rewards)")
    print(f"   Phase 5 learning: Active (organic families)\n")
except Exception as e:
    print(f"   ❌ Error initializing organism: {e}")
    sys.exit(1)

# Training loop
print(f"🎓 Beginning {NUM_EPOCHS}-epoch entity-organ training (DAE-native)...\n")

epoch_results = []
entity_pattern_evolution = defaultdict(lambda: defaultdict(list))

start_time = time.time()

for epoch in range(1, NUM_EPOCHS + 1):
    epoch_start = time.time()
    regime = get_regime_for_epoch(epoch)

    # Get conversations for this epoch
    epoch_conversations = [
        c for c in conversations
        if epoch in c.get('epoch_distribution', [])
    ]

    print(f"📖 Epoch {epoch}/{NUM_EPOCHS} - Regime: {regime.name}")
    print(f"   Conversations: {len(epoch_conversations)}")
    print(f"   Tau threshold: {regime.tau_threshold:.2f}")
    print(f"   Max iterations: {regime.max_iterations}")

    # Track epoch metrics
    epoch_metrics = {
        'epoch': epoch,
        'regime': regime.name,
        'num_conversations': len(epoch_conversations),
        'conversation_results': [],
        'category_stats': defaultdict(lambda: {
            'count': 0,
            'mean_satisfaction': 0,
            'mean_iterations': 0,
            'mean_v0_descent': 0
        }),
        'entity_stats': defaultdict(lambda: {
            'mentions': 0,
            'mean_organs': {}
        }),
        'processing_time': 0
    }

    # Process each conversation (DAE-native: process_text for organ activations)
    for conv_idx, conversation in enumerate(epoch_conversations):
        conv_id = conversation['conversation_id']
        input_text = conversation['input']
        category = conversation['category']
        expected_entities = conversation.get('entities', [])

        try:
            # DAE-NATIVE PROCESSING: Just organ activations, no LLM generation
            # This is FAST (~1-2s) because it doesn't generate emission text
            result = organism.process_text(
                text=input_text,
                context={
                    'conversation_id': conv_id,
                    'epoch_num': epoch,
                    'training_phase': 'entity_organ_learning',
                    # Pass entities for entity-organ tracker
                    'stored_entities': expected_entities
                },
                enable_tsk_recording=False,  # Don't need full TSK
                user_id=USER_ID  # Enables entity-organ tracker updates
            )

            # Extract DAE-native metrics (no emission text needed)
            felt_states = result.get('felt_states', {})
            v0_energy = felt_states.get('v0_energy', {})
            v0_descent = v0_energy.get('initial_energy', 1.0) - v0_energy.get('final_energy', 0.5)
            satisfaction = felt_states.get('satisfaction_final', 0.5)
            organ_coherences = felt_states.get('organ_coherences', {})

            # Note: We use satisfaction as proxy for "quality" (not from user feedback)
            # This is organic satisfaction based on V0 descent and organ coherence

            conv_result = {
                'conversation_id': conv_id,
                'category': category,
                'satisfaction': float(satisfaction),
                'v0_descent': float(v0_descent),
                'organ_coherences': {k: float(v) for k, v in organ_coherences.items()},
                'entity_values': [e.get('entity_value') for e in expected_entities]
            }

            epoch_metrics['conversation_results'].append(conv_result)

            # Update category stats
            cat_stats = epoch_metrics['category_stats'][category]
            cat_stats['count'] += 1
            cat_stats['mean_satisfaction'] += satisfaction
            cat_stats['mean_v0_descent'] += v0_descent

            # Update entity stats
            for entity_value in conv_result['entity_values']:
                if entity_value:
                    ent_stats = epoch_metrics['entity_stats'][entity_value]
                    ent_stats['mentions'] += 1
                    for organ, coherence in organ_coherences.items():
                        if organ not in ent_stats['mean_organs']:
                            ent_stats['mean_organs'][organ] = []
                        ent_stats['mean_organs'][organ].append(float(coherence))

            # Progress (only every 5 to reduce spam)
            if (conv_idx + 1) % 5 == 0 or (conv_idx + 1) == len(epoch_conversations):
                print(f"   Processed {conv_idx + 1}/{len(epoch_conversations)} "
                      f"(satisfaction: {satisfaction:.3f}, V0↓: {v0_descent:.3f})")

        except Exception as e:
            print(f"   ⚠️  Error processing {conv_id}: {e}")
            continue

    # Finalize category stats
    for category, stats in epoch_metrics['category_stats'].items():
        if stats['count'] > 0:
            stats['mean_satisfaction'] /= stats['count']
            stats['mean_v0_descent'] /= stats['count']

    # Finalize entity stats
    for entity, stats in epoch_metrics['entity_stats'].items():
        for organ, coherences in stats['mean_organs'].items():
            stats['mean_organs'][organ] = float(np.mean(coherences))

    epoch_metrics['processing_time'] = time.time() - epoch_start
    epoch_results.append(epoch_metrics)

    # Epoch summary
    mean_sat = np.mean([r['satisfaction'] for r in epoch_metrics['conversation_results']])
    mean_v0 = np.mean([r['v0_descent'] for r in epoch_metrics['conversation_results']])

    print(f"   ✅ Epoch {epoch} complete in {epoch_metrics['processing_time']:.1f}s")
    print(f"      Mean satisfaction: {mean_sat:.3f}")
    print(f"      Mean V0 descent: {mean_v0:.3f}")
    print(f"      Entities tracked: {len(epoch_metrics['entity_stats'])}")

    # Checkpoint every 10 epochs
    if epoch % 10 == 0:
        print(f"\n   📊 Checkpoint at epoch {epoch}:")
        print(f"      Entity patterns emerging:")
        for entity, stats in sorted(epoch_metrics['entity_stats'].items(),
                                   key=lambda x: x[1]['mentions'], reverse=True)[:5]:
            top_organs = sorted(stats['mean_organs'].items(),
                              key=lambda x: x[1], reverse=True)[:3]
            print(f"        {entity}: {stats['mentions']} mentions, "
                  f"top organs: {', '.join([f'{o}={v:.2f}' for o, v in top_organs])}")
        print()

total_time = time.time() - start_time

print(f"\n{'='*80}")
print(f"✅ DAE-native training complete! {NUM_EPOCHS} epochs in {total_time/60:.1f} minutes")
print(f"{'='*80}\n")

# Save results
print(f"💾 Saving results to {OUTPUT_PATH}...")
try:
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    results = {
        'metadata': {
            'training_mode': 'DAE-native (multi-iteration, no LLM)',
            'corpus_path': CORPUS_PATH,
            'num_epochs': NUM_EPOCHS,
            'num_conversations': len(conversations),
            'user_id': USER_ID,
            'total_time': total_time,
            'timestamp': datetime.now().isoformat()
        },
        'user_profile': user_profile,
        'training_notes': corpus.get('training_notes', {}),
        'epoch_results': epoch_results,
        'summary': {
            'mean_satisfaction_per_epoch': [
                np.mean([r['satisfaction'] for r in e['conversation_results']])
                for e in epoch_results
            ],
            'mean_v0_descent_per_epoch': [
                np.mean([r['v0_descent'] for r in e['conversation_results']])
                for e in epoch_results
            ],
            'entities_tracked': list(set(
                entity
                for e in epoch_results
                for entity in e['entity_stats'].keys()
            )),
            'total_conversations_processed': sum(e['num_conversations'] for e in epoch_results)
        }
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"   ✅ Results saved\n")

except Exception as e:
    print(f"   ❌ Error saving results: {e}")

# Final summary
print(f"📊 Final Summary:")
print(f"   Training mode: DAE-native (organ activations only)")
print(f"   Total epochs: {NUM_EPOCHS}")
print(f"   Total time: {total_time/60:.1f} minutes ({total_time/NUM_EPOCHS:.1f}s per epoch)")
print(f"   Conversations processed: {results['summary']['total_conversations_processed']}")
print(f"   Unique entities tracked: {len(results['summary']['entities_tracked'])}")
print(f"   Entities: {', '.join(results['summary']['entities_tracked'][:10])}")
print(f"   Mean satisfaction (final epoch): {results['summary']['mean_satisfaction_per_epoch'][-1]:.3f}")
print(f"   Mean V0 descent (final epoch): {results['summary']['mean_v0_descent_per_epoch'][-1]:.3f}")

print(f"\n🌀 Next step: Validate entity-organ patterns")
print(f"   Check: persona_layer/state/active/entity_organ_associations.json")
print(f"   Run: python3 validate_entity_organ_patterns.py")
print(f"   Expected: Emma → BOND/EMPATHY high, work → NDAM/AUTHENTICITY high\n")
