#!/usr/bin/env python3
"""
Multi-Family Discovery Training - Proper Architecture
======================================================

Uses ProductionLearningCoordinator to enable Phase 5 family learning
with the 102-pair expanded corpus.

Based on successful test_integrated_training.py that created epoch_1.json
with 1 family and 30/30 pairs learned.

Expected Results:
- 5-10 families discovered
- 200-300 hebbian patterns
- Family maturation tracking
- Real-time progress monitoring
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

# Import organism wrapper
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

# Import production learning coordinator (THE KEY!)
from persona_layer.epoch_training.production_learning_coordinator import ProductionLearningCoordinator

# Configuration
TRAINING_PAIRS_PATH = "knowledge_base/conversational_training_pairs_expanded.json"
EPOCH_NUM = 2
ENABLE_PHASE2 = True
LEARNING_THRESHOLD = 0.30  # Lowered to learn from safety-boosted emissions
SAVE_FREQUENCY = 10  # Save families every 10 pairs
OUTPUT_DIR = "results/epochs"

print("="*80)
print("🧠 MULTI-FAMILY DISCOVERY TRAINING - PROPER ARCHITECTURE")
print("="*80)
print()
print("Using ProductionLearningCoordinator (same as successful epoch_1 training)")
print(f"Training corpus: {TRAINING_PAIRS_PATH}")
print(f"Learning threshold: {LEARNING_THRESHOLD}")
print()

# ============================================================================
# STEP 1: Initialize Components
# ============================================================================
print("1️⃣ Initializing organism and learning coordinator...")
print()

# Initialize organism wrapper
wrapper = ConversationalOrganismWrapper()
print()

# ✅ Initialize Production Learning Coordinator (THIS IS THE KEY!)
learning_coordinator = ProductionLearningCoordinator(
    hebbian_storage="TSK/conversational_hebbian_memory.json",
    phase5_storage="persona_layer",
    learning_threshold=LEARNING_THRESHOLD,
    save_frequency=SAVE_FREQUENCY,
    enable_hebbian=True,
    enable_phase5=True
)
print()

# ============================================================================
# STEP 2: Load Training Pairs
# ============================================================================
print("2️⃣ Loading training pairs...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"]

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print(f"   📊 Categories: {data['statistics']['total_pairs']} pairs across {len(data['statistics']['categories'])} categories")
print()

# ============================================================================
# STEP 3: Training Loop with Real Learning
# ============================================================================
print("3️⃣ Starting training loop...")
print()

# Metrics tracking
results = []
success_count = 0
error_count = 0

# Family tracking
initial_families = len(learning_coordinator.phase5_learning.families.families) if learning_coordinator.enable_phase5 else 0
print(f"   Initial families: {initial_families}")
print()

for idx, pair in enumerate(training_pairs, 1):
    pair_id = pair["pair_metadata"]["id"]
    category = pair["pair_metadata"].get("category", "unknown")
    input_text = pair["input_text"]
    output_text = pair["output_text"]

    # Progress indicator (every 10 pairs)
    if idx % 10 == 0 or idx == 1:
        print(f"📘 [{idx}/{len(training_pairs)}] {pair_id} ({category})")

    try:
        # ----------------------------------------------------------------
        # Process INPUT through organism
        # ----------------------------------------------------------------
        input_result = wrapper.process_text(
            text=input_text,
            context={
                'conversation_id': f"{pair_id}_INPUT",
                'epoch_num': EPOCH_NUM,
                'training_phase': 'input'
            },
            enable_tsk_recording=False,
            enable_phase2=ENABLE_PHASE2
        )

        # ----------------------------------------------------------------
        # Process OUTPUT through organism
        # ----------------------------------------------------------------
        output_result = wrapper.process_text(
            text=output_text,
            context={
                'conversation_id': f"{pair_id}_OUTPUT",
                'epoch_num': EPOCH_NUM,
                'training_phase': 'output'
            },
            enable_tsk_recording=False,
            enable_phase2=ENABLE_PHASE2
        )

        # ----------------------------------------------------------------
        # ✅ REAL LEARNING via ProductionLearningCoordinator
        # ----------------------------------------------------------------
        learning_updates = learning_coordinator.learn_from_training_pair(
            input_result=input_result,
            output_result=output_result,
            pair_metadata=pair['pair_metadata'],
            input_text=input_text,
            output_text=output_text
        )

        # Extract metrics
        input_satisfaction = input_result['felt_states']['satisfaction_final']
        output_satisfaction = output_result['felt_states']['satisfaction_final']
        satisfaction_delta = output_satisfaction - input_satisfaction

        # Store result
        results.append({
            "pair_id": pair_id,
            "category": category,
            "input_satisfaction": float(input_satisfaction),
            "output_satisfaction": float(output_satisfaction),
            "satisfaction_delta": float(satisfaction_delta),
            "learned": learning_updates['learned'],
            "hebbian_updates": learning_updates['hebbian_updates'],
            "cluster_updates": learning_updates['cluster_updates'],
            "family_matured": learning_updates['family_matured'],
            "family_id": learning_updates.get('family_id'),
            "patterns_total": learning_updates.get('patterns_total', 0)
        })

        success_count += 1

        # Real-time family monitoring
        if learning_updates['learned']:
            print(f"   📚 Learned: Family {learning_updates.get('family_id', 'unknown')}")

        if learning_updates['family_matured']:
            current_families = len(learning_coordinator.phase5_learning.families.families)
            print(f"\n   ✨ FAMILY MATURED! Family: {learning_updates['family_id']}")
            print(f"      Total families: {current_families}")
            print()

        # Family status check every 20 pairs
        if idx % 20 == 0:
            current_families = len(learning_coordinator.phase5_learning.families.families) if learning_coordinator.enable_phase5 else 0
            families_discovered = current_families - initial_families
            print(f"\n   📊 Status after {idx} pairs:")
            print(f"      Total families: {current_families} ({families_discovered} new)")
            print(f"      Hebbian patterns: {learning_updates.get('patterns_total', 0)}")
            print()

    except Exception as e:
        print(f"   ❌ Error on pair {pair_id}: {e}")
        import traceback
        traceback.print_exc()
        error_count += 1
        results.append({
            "pair_id": pair_id,
            "error": str(e)
        })

print()
print("="*80)
print("📊 TRAINING COMPLETE")
print("="*80)
print()

# ============================================================================
# STEP 4: Learning Statistics
# ============================================================================
learning_stats = learning_coordinator.get_learning_stats()

final_families = len(learning_coordinator.phase5_learning.families.families) if learning_coordinator.enable_phase5 else 0
families_discovered = final_families - initial_families

print(f"🎯 Success Rate: {success_count}/{len(training_pairs)} ({100*success_count/len(training_pairs):.1f}%)")
print(f"❌ Errors: {error_count}")
print()

print("🧠 Learning Statistics:")
print(f"   Pairs processed: {learning_stats['pairs_processed']}")
print(f"   Pairs learned from: {learning_stats['pairs_learned_from']}")
print(f"   Learning rate: {learning_stats['learning_rate']:.1%}")
print()

if learning_stats.get('hebbian_enabled'):
    print("🧬 Hebbian Learning:")
    print(f"   Patterns: {learning_stats.get('hebbian_patterns', 0)}")
    print(f"   Success: {learning_stats.get('hebbian_success_count', 0)}")
    print(f"   Failure: {learning_stats.get('hebbian_failure_count', 0)}")
    print()

if learning_stats.get('phase5_enabled'):
    print("🌀 Phase 5 Organic Learning:")
    print(f"   Families discovered: {families_discovered}")
    print(f"   Total families: {final_families}")
    print(f"   Mature families: {learning_stats.get('mature_families', 0)}")
    print()

# ============================================================================
# STEP 5: Save Results
# ============================================================================
output_path = Path(OUTPUT_DIR) / f"epoch_{EPOCH_NUM}_multi_family_discovery.json"
output_path.parent.mkdir(parents=True, exist_ok=True)

epoch_output = {
    "metadata": {
        "epoch": EPOCH_NUM,
        "timestamp": datetime.now().isoformat(),
        "num_pairs": len(training_pairs),
        "learning_threshold": LEARNING_THRESHOLD,
        "phase2_enabled": ENABLE_PHASE2
    },
    "summary": {
        "success_rate": float(success_count / len(training_pairs)),
        "families_discovered": families_discovered,
        "total_families": final_families,
        "mature_families": learning_stats.get('mature_families', 0),
        "hebbian_patterns": learning_stats.get('hebbian_patterns', 0),
        "pairs_learned_from": learning_stats['pairs_learned_from']
    },
    "learning_stats": learning_stats,
    "results": results
}

with open(output_path, 'w') as f:
    json.dump(epoch_output, f, indent=2)

print(f"💾 Results saved: {output_path}")
print()

# ============================================================================
# STEP 6: Family Analysis
# ============================================================================
if families_discovered > 0:
    print("="*80)
    print("🌱 FAMILY ANALYSIS")
    print("="*80)
    print()

    families_data = learning_coordinator.phase5_learning.families

    for family_id, family_data in families_data.families.items():
        sample_count = family_data.get('sample_count', 0)
        mean_satisfaction = family_data.get('mean_satisfaction', 0)
        maturity = "mature" if sample_count >= 3 else "infant"

        print(f"   {family_id} ({maturity}):")
        print(f"      Samples: {sample_count}")
        print(f"      Mean satisfaction: {mean_satisfaction:.3f}")
        print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("="*80)
print("✅ MULTI-FAMILY DISCOVERY COMPLETE")
print("="*80)
print()

if families_discovered > 0:
    print(f"🎉 SUCCESS: {families_discovered} new families discovered!")
    print()
    print("📁 Check these files:")
    print(f"   - {output_path}")
    print(f"   - persona_layer/organic_families.json")
    print(f"   - TSK/conversational_hebbian_memory.json")
else:
    print("⚠️  No new families discovered. Diagnostics:")
    print(f"   - Pairs learned from: {learning_stats['pairs_learned_from']}/{len(training_pairs)}")
    print(f"   - Learning threshold: {LEARNING_THRESHOLD}")
    print(f"   - Check satisfaction distribution in results")
    print(f"   - Consider lowering learning_threshold or similarity_threshold")

print()
