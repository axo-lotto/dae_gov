#!/usr/bin/env python3
"""
Arc Training Epochs 18-20 - Lowered Threshold Experiment
========================================================

Test lowering assessment threshold from 0.65 to 0.50 to enable
learning from "high-partial" predictions.

Expected: 2-3× increase in learning rate (22-30% → 50%)

Date: November 12, 2025
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.arc_inspired_trainer import ArcInspiredTrainer

# Configuration
TRAINING_PAIRS_PATH = "/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/conversational_training_pairs_complete.json"
NUM_ARCS_PER_EPOCH = 50
START_EPOCH = 18
NUM_EPOCHS = 3  # Epochs 18-20
OUTPUT_DIR = "training/conversational"
ASSESSMENT_THRESHOLD = 0.50  # ⬅️ LOWERED from 0.65

print("="*80)
print("🌀 ARC TRAINING EPOCHS 18-20 - Lowered Threshold Experiment")
print("="*80)
print()
print("🎯 Experimental Hypothesis:")
print("   - Lowering threshold 0.65 → 0.50 enables learning from 'high-partial' predictions")
print("   - Expected learning rate: 22-30% → 50%")
print("   - Expected predictions learned: 11-15/epoch → 25/epoch")
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Arcs per epoch: {NUM_ARCS_PER_EPOCH} (×3 pairs = {NUM_ARCS_PER_EPOCH*3} exposures)")
print(f"   Epochs: {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1}")
print(f"   Assessment threshold: {ASSESSMENT_THRESHOLD} ⬅️ LOWERED (was 0.65)")
print(f"   Semantic similarity: SANS embeddings (384-dim)")
print(f"   Learning: ✅ ACTIVE")
print()

# Load training pairs
print("📂 Loading training pairs...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"]

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print()

# Initialize organism (preserves learning state from epochs 1-17)
print("🧬 Initializing organism with learned state...")
organism = ConversationalOrganismWrapper()

# Check Phase 5 learning availability
if not hasattr(organism, 'phase5_learning') or organism.phase5_learning is None:
    print("⚠️  WARNING: Phase 5 learning not initialized!")
    print("   Continuing without Phase 5 learning")
    ENABLE_PHASE5 = False
else:
    families_start = len(organism.phase5_learning.families.families)
    print(f"   ✅ Phase 5 Organic Learning: {families_start} existing families")
    ENABLE_PHASE5 = True

print("   ✅ Organism ready for arc training")
print()

# Initialize arc trainer (with SANS embeddings + lowered threshold)
print("🌀 Initializing Arc-Inspired Trainer...")
arc_trainer = ArcInspiredTrainer(
    organism_wrapper=organism,
    training_pairs=training_pairs,
    enable_learning=ENABLE_PHASE5,
    assessment_threshold=ASSESSMENT_THRESHOLD  # 0.50 (lowered)
)
print()

# Verify SANS embeddings are active
if not arc_trainer.use_embeddings:
    print("❌ ERROR: SANS embeddings not available!")
    sys.exit(1)

print("✅ SANS embeddings confirmed active")
print()

# Run epochs 18-20
all_epoch_summaries = []

for epoch_num in range(START_EPOCH, START_EPOCH + NUM_EPOCHS):
    print("\n")
    print("="*80)
    print(f"🎓 EPOCH {epoch_num} - ARC TRAINING (Threshold=0.50)")
    print("="*80)
    print()

    # Track families before epoch
    families_before = len(organism.phase5_learning.families.families) if ENABLE_PHASE5 else 0

    # Run epoch
    epoch_summary = arc_trainer.train_epoch(
        num_arcs=NUM_ARCS_PER_EPOCH,
        category_distribution=None,
        verbose=False  # Quiet mode for faster processing
    )

    # Track families after epoch
    families_after = len(organism.phase5_learning.families.families) if ENABLE_PHASE5 else 0
    families_discovered = families_after - families_before

    # Add metadata
    epoch_summary['families_discovered'] = families_discovered
    epoch_summary['total_families'] = families_after
    epoch_summary['epoch'] = epoch_num
    epoch_summary['threshold'] = ASSESSMENT_THRESHOLD

    all_epoch_summaries.append(epoch_summary)

    # Save epoch results
    epoch_output_path = f"{OUTPUT_DIR}/epoch_{epoch_num}_arc_training_results.json"
    arc_trainer.save_results(epoch_output_path)

    print(f"\n✅ Epoch {epoch_num} Complete")
    print(f"   Arcs: {epoch_summary['arcs_processed']}")
    print(f"   Success rate: {epoch_summary['success_rate']:.1%} ({epoch_summary['arcs_processed'] * epoch_summary['success_rate']:.0f}/{epoch_summary['arcs_processed']})")
    print(f"   Mean alignment: {epoch_summary['mean_alignment_score']:.3f}")
    print(f"   Mean confidence: {epoch_summary['mean_prediction_confidence']:.3f}")

    if ENABLE_PHASE5:
        print(f"   Families: {families_after} ({families_discovered:+d} this epoch)")

    print()

# Final summary
print()
print("="*80)
print(f"🏆 ARC TRAINING EPOCHS {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1} COMPLETE")
print("="*80)
print()

print("📊 Progression Summary:")
print()
print("Epoch | Arcs | Success% | Mean Alignment | Mean Confidence | Families")
print("-" * 85)

for summary in all_epoch_summaries:
    epoch = summary['epoch']
    arcs = summary['arcs_processed']
    success_pct = summary['success_rate'] * 100
    alignment = summary['mean_alignment_score']
    confidence = summary['mean_prediction_confidence']
    families = summary.get('total_families', 0)
    discovered = summary.get('families_discovered', 0)
    discovered_str = f"(+{discovered})" if discovered > 0 else ""

    print(f"  {epoch}  |  {arcs}  |  {success_pct:5.1f}%  |     {alignment:.3f}      |      {confidence:.3f}      | {families} {discovered_str}")

print()

# Overall statistics for epochs 18-20
total_arcs = sum(s['arcs_processed'] for s in all_epoch_summaries)
total_successful = sum(int(s['arcs_processed'] * s['success_rate']) for s in all_epoch_summaries)
overall_success_rate = total_successful / total_arcs

mean_alignment = sum(s['mean_alignment_score'] for s in all_epoch_summaries) / len(all_epoch_summaries)
mean_confidence = sum(s['mean_prediction_confidence'] for s in all_epoch_summaries) / len(all_epoch_summaries)

print("📈 Epochs 18-20 Overall Statistics (Threshold=0.50):")
print(f"   Total arcs: {total_arcs}")
print(f"   Success rate: {overall_success_rate:.1%} ({total_successful}/{total_arcs})")
print(f"   Mean alignment: {mean_alignment:.3f}")
print(f"   Mean confidence: {mean_confidence:.3f}")
print()

if ENABLE_PHASE5:
    families_final = organism.phase5_learning.families.families
    families_end = len(families_final)
    families_total_discovered = families_end - families_start

    print("🧠 Learning Outcomes:")
    print(f"   Families at start: {families_start}")
    print(f"   Families at end: {families_end}")
    print(f"   Total discovered: {families_total_discovered}")
    print()

# Comparison to epochs 15-17 (threshold=0.65)
print("="*80)
print("📊 COMPARISON: Epochs 15-17 (0.65) vs Epochs 18-20 (0.50)")
print("="*80)
print()

# Load epoch 15 for baseline comparison
try:
    with open(f'{OUTPUT_DIR}/epoch_15_arc_training_results.json') as f:
        epoch15 = json.load(f)

    e15_success = epoch15['metadata']['overall_success_rate']
    e15_alignment = sum(r['assessment']['overall_score'] for r in epoch15['results']) / len(epoch15['results'])

    print(f"Metric                  | Epochs 15-17 (0.65) | Epochs 18-20 (0.50) | Change")
    print("-" * 85)
    print(f"Assessment threshold    |    0.65             |    0.50             | -0.15")
    print(f"Success rate            |   {e15_success:.1%}              |   {overall_success_rate:.1%}             | {(overall_success_rate-e15_success)*100:+.1f}%")
    print(f"Mean alignment          |   {e15_alignment:.3f}            |   {mean_alignment:.3f}            | {mean_alignment-e15_alignment:+.3f}")
    print(f"Mean confidence         |   TBD               |   {mean_confidence:.3f}            | TBD")
    print()
except FileNotFoundError:
    print("⚠️  Could not load epoch 15 results for comparison")
    print()

print("✅ Epochs 18-20 complete!")
print()
print("🔬 Threshold Experiment Results:")
print()

if overall_success_rate >= 0.40:
    print("✅ HYPOTHESIS CONFIRMED: Lowering threshold increased learning rate")
    print(f"   - Success rate improved to {overall_success_rate:.1%}")
    print(f"   - More predictions learned from 'high-partial' category")
    print(f"   - Recommendation: Keep threshold at 0.50 for future epochs")
elif overall_success_rate >= 0.30:
    print("⚠️  HYPOTHESIS PARTIALLY CONFIRMED: Moderate improvement")
    print(f"   - Success rate: {overall_success_rate:.1%} (expected 50%)")
    print(f"   - Consider adjusting to 0.55 (middle ground)")
else:
    print("❌ HYPOTHESIS NOT CONFIRMED: Minimal improvement")
    print(f"   - Success rate: {overall_success_rate:.1%}")
    print(f"   - Recommendation: Revert to 0.65 threshold")

print()
print("🚀 Next Steps:")
print()
print("Option B: Expand corpus to 500-800 pairs (multi-domain, multi-family)")
print("Option C: Add response length modulation (match target length)")
print("Option D: Continue epochs 21-25 with optimal threshold")
print()
print("💾 All results saved to: training/conversational/epoch_{18,19,20}_arc_training_results.json")
print()
