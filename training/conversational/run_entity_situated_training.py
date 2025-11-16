"""
Entity-Situated Epoch Training - Emiliano Corpus
=================================================

Trains organism with 100 conversations containing consistent entity graph to develop
entity-organ associations through accumulated experience.

Entity Graph:
- Emiliano (user): Engineering lead at tech startup, father of two daughters
- Emma (5yo): Starting kindergarten, sensitive, loves hugs
- Lily (3yo): Preschool age, energetic, learning independence
- Sofia (partner): Wife, co-parent, source of support and tension
- Alex (colleague-friend): Work colleague, understands startup pressure
- Rich (friend): Childhood friend, grounding presence
- Work (place): Tech startup, high stress environment

Training Strategy:
- 50 epochs total (each conversation appears 5 times across epochs 1-50)
- 100 conversations distributed across 5 categories:
  * family_safe (30) - bonding moments with Emma, Lily, Sofia
  * family_worry (20) - parental anxiety about development
  * work_stress (25) - deadline pressure, team conflicts
  * relationship (15) - connection/tension with Sofia
  * self_care (10) - gym time, walks, moments alone

Expected Outcomes:
- Epoch 1-10: Exploration (no strong entity-organ patterns yet)
- Epoch 11-30: Pattern emergence (Emma → BOND/EMPATHY, work → NDAM)
- Epoch 31-50: Consolidation (>85% cross-session consistency)

Success Criteria:
- Emma pattern: BOND/EMPATHY >0.80, ventral state, V0 <0.30, success_rate >0.85
- Lily pattern: BOND/PRESENCE >0.75, ventral state, V0 <0.35, success_rate >0.82
- Work pattern: NDAM/AUTHENTICITY >0.75, sympathetic state, V0 >0.60, urgency >0.5
- Cross-session consistency: >85% same entity → similar organ pattern
- Entity success correlation: R² > 0.75

Date: November 15, 2025
"""

import sys
import json
import time
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import numpy as np
from collections import defaultdict, Counter

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("\n" + "="*80)
print("🌀 ENTITY-SITUATED EPOCH TRAINING - EMILIANO CORPUS")
print("="*80 + "\n")

# Configuration
CORPUS_PATH = "knowledge_base/entity_training/emiliano_entity_corpus.json"
OUTPUT_PATH = "results/epochs/entity_situated_training_results.json"
NUM_EPOCHS = 50
USER_ID = "training_emiliano_001"
ENABLE_ENTITY_TRACKING = True  # Enable entity-organ association tracking

print(f"📋 Configuration:")
print(f"   Corpus: {CORPUS_PATH}")
print(f"   Epochs: {NUM_EPOCHS}")
print(f"   User ID: {USER_ID}")
print(f"   Entity tracking: {ENABLE_ENTITY_TRACKING}")
print(f"   Output: {OUTPUT_PATH}\n")

# Load corpus
print(f"📂 Loading Emiliano entity corpus...")
try:
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)
        conversations = corpus.get('conversations', [])
        user_profile = corpus.get('user_profile', {})
        metadata = corpus.get('corpus_metadata', {})
        training_notes = corpus.get('training_notes', {})

    print(f"   ✅ Loaded {len(conversations)} conversations")
    print(f"   User: {user_profile.get('name', 'Unknown')}")
    print(f"   Entity graph entities: {len(user_profile.get('entity_graph', {}).get('family', {}).get('daughters', []))} daughters, "
          f"{1 if user_profile.get('entity_graph', {}).get('family', {}).get('partner') else 0} partner")

    # Category breakdown
    category_counts = Counter(c['category'] for c in conversations)
    print(f"   Categories:")
    for cat, count in sorted(category_counts.items()):
        print(f"     - {cat}: {count}")
    print()

except Exception as e:
    print(f"   ❌ Error loading corpus: {e}")
    traceback.print_exc()
    sys.exit(1)

# Initialize organism
print(f"🌀 Initializing organism...")
try:
    organism = ConversationalOrganismWrapper()
    print(f"   ✅ Organism initialized")
    print(f"   Phase 2: Always enabled (multi-cycle V0 convergence)")
    print(f"   Entity tracking: {ENABLE_ENTITY_TRACKING}\n")
except Exception as e:
    print(f"   ❌ Error initializing organism: {e}")
    traceback.print_exc()
    sys.exit(1)

# Training loop
print(f"🎓 Beginning {NUM_EPOCHS}-epoch training...\n")

epoch_results = []
entity_pattern_evolution = defaultdict(lambda: defaultdict(list))  # entity -> metric -> [values over epochs]

start_time = time.time()

for epoch in range(1, NUM_EPOCHS + 1):
    epoch_start = time.time()

    # Get conversations for this epoch
    epoch_conversations = [
        c for c in conversations
        if epoch in c.get('epoch_distribution', [])
    ]

    print(f"📖 Epoch {epoch}/{NUM_EPOCHS} - {len(epoch_conversations)} conversations")

    # Track epoch-level metrics
    epoch_metrics = {
        'epoch': epoch,
        'num_conversations': len(epoch_conversations),
        'conversation_results': [],
        'category_stats': defaultdict(lambda: {'count': 0, 'mean_confidence': 0, 'mean_v0_descent': 0}),
        'entity_stats': defaultdict(lambda: {'mentions': 0, 'mean_organs': {}}),
        'processing_time': 0
    }

    # Process each conversation
    for conv_idx, conversation in enumerate(epoch_conversations):
        conv_id = conversation['conversation_id']
        input_text = conversation['input']
        category = conversation['category']
        expected_entities = conversation.get('entities', [])
        expected_patterns = conversation.get('expected_patterns', {})

        try:
            # Process conversation
            result = organism.process_text(
                text=input_text,
                user_id=USER_ID,
                user_satisfaction=None  # Training mode - no explicit satisfaction
            )

            # Extract result metrics
            confidence = result.get('emission_confidence', 0)
            felt_states = result.get('felt_states', {})
            v0_energy = felt_states.get('v0_energy', {})
            v0_start = v0_energy.get('initial_energy', 1.0)
            v0_final = v0_energy.get('final_energy', 0.5)
            v0_descent = v0_start - v0_final
            organ_coherences = felt_states.get('organ_coherences', {})
            active_organs = sum(1 for v in organ_coherences.values() if v > 0.5)

            # Track entity mentions and organ activations
            # For training, we don't have stored_entities in context, extract from input
            extracted_entities = []  # Will populate from conversation's expected entities

            # Use expected entities from conversation definition
            entity_values = [e.get('entity_value') for e in expected_entities]

            conv_result = {
                'conversation_id': conv_id,
                'category': category,
                'confidence': confidence,
                'v0_descent': v0_descent,
                'active_organs': active_organs,
                'expected_entities': entity_values,
                'organ_coherences': {k: float(v) for k, v in organ_coherences.items()}
            }

            epoch_metrics['conversation_results'].append(conv_result)

            # Update category stats
            cat_stats = epoch_metrics['category_stats'][category]
            cat_stats['count'] += 1
            cat_stats['mean_confidence'] += confidence
            cat_stats['mean_v0_descent'] += v0_descent

            # Update entity stats using expected entities
            for entity_value in entity_values:
                if entity_value:
                    ent_stats = epoch_metrics['entity_stats'][entity_value]
                    ent_stats['mentions'] += 1
                    for organ, coherence in organ_coherences.items():
                        if organ not in ent_stats['mean_organs']:
                            ent_stats['mean_organs'][organ] = []
                        ent_stats['mean_organs'][organ].append(float(coherence))

            # Progress indicator
            if (conv_idx + 1) % 10 == 0:
                print(f"   Processed {conv_idx + 1}/{len(epoch_conversations)} conversations...")

        except Exception as e:
            print(f"   ⚠️  Error processing {conv_id}: {e}")
            traceback.print_exc()
            continue

    # Finalize category stats
    for category, stats in epoch_metrics['category_stats'].items():
        if stats['count'] > 0:
            stats['mean_confidence'] /= stats['count']
            stats['mean_v0_descent'] /= stats['count']

    # Finalize entity stats
    for entity, stats in epoch_metrics['entity_stats'].items():
        for organ, activations in stats['mean_organs'].items():
            stats['mean_organs'][organ] = float(np.mean(activations))

    epoch_metrics['processing_time'] = time.time() - epoch_start
    epoch_results.append(epoch_metrics)

    # Print epoch summary
    print(f"   ✅ Epoch {epoch} complete in {epoch_metrics['processing_time']:.2f}s")
    print(f"      Mean confidence: {np.mean([r['confidence'] for r in epoch_metrics['conversation_results']]):.3f}")
    print(f"      Mean V0 descent: {np.mean([r['v0_descent'] for r in epoch_metrics['conversation_results']]):.3f}")
    print(f"      Entities tracked: {len(epoch_metrics['entity_stats'])}")

    # Checkpoint every 10 epochs
    if epoch % 10 == 0:
        print(f"\n   📊 Checkpoint at epoch {epoch}:")
        print(f"      Entity patterns emerging:")
        for entity, stats in sorted(epoch_metrics['entity_stats'].items(), key=lambda x: x[1]['mentions'], reverse=True)[:5]:
            top_organs = sorted(stats['mean_organs'].items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"        {entity}: {stats['mentions']} mentions, top organs: {', '.join([f'{o}={v:.2f}' for o, v in top_organs])}")
        print()

total_time = time.time() - start_time

print(f"\n{'='*80}")
print(f"✅ Training complete! {NUM_EPOCHS} epochs in {total_time/60:.1f} minutes")
print(f"{'='*80}\n")

# Save results
print(f"💾 Saving results to {OUTPUT_PATH}...")
try:
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    results = {
        'metadata': {
            'corpus_path': CORPUS_PATH,
            'num_epochs': NUM_EPOCHS,
            'num_conversations': len(conversations),
            'user_id': USER_ID,
            'entity_tracking_enabled': ENABLE_ENTITY_TRACKING,
            'total_time': total_time,
            'timestamp': datetime.now().isoformat()
        },
        'user_profile': user_profile,
        'training_notes': training_notes,
        'epoch_results': epoch_results,
        'summary': {
            'mean_confidence_per_epoch': [np.mean([r['confidence'] for r in e['conversation_results']]) for e in epoch_results],
            'mean_v0_descent_per_epoch': [np.mean([r['v0_descent'] for r in e['conversation_results']]) for e in epoch_results],
            'entities_tracked': list(set(entity for e in epoch_results for entity in e['entity_stats'].keys())),
            'total_conversations_processed': sum(e['num_conversations'] for e in epoch_results)
        }
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"   ✅ Results saved\n")

except Exception as e:
    print(f"   ❌ Error saving results: {e}")
    traceback.print_exc()

# Final summary
print(f"📊 Final Summary:")
print(f"   Total epochs: {NUM_EPOCHS}")
print(f"   Total conversations processed: {results['summary']['total_conversations_processed']}")
print(f"   Unique entities tracked: {len(results['summary']['entities_tracked'])}")
print(f"   Entities: {', '.join(results['summary']['entities_tracked'][:10])}")
print(f"   Mean confidence (final epoch): {results['summary']['mean_confidence_per_epoch'][-1]:.3f}")
print(f"   Mean V0 descent (final epoch): {results['summary']['mean_v0_descent_per_epoch'][-1]:.3f}")
print(f"\n🌀 Next step: Validate entity-organ pattern emergence")
print(f"   Check: persona_layer/state/active/entity_organ_associations.json")
print(f"   Expected: Emma → BOND/EMPATHY high, work → NDAM/AUTHENTICITY high\n")
