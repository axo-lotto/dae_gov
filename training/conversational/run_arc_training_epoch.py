#!/usr/bin/env python3
"""
Arc-Inspired Training Runner - Pattern Completion Learning
==========================================================

Runs arc training epochs where organism:
1. Sees 2 examples (pattern recognition)
2. Predicts 3rd output (pattern completion)
3. Self-assesses prediction quality
4. Learns from misalignment

Expected benefits:
- Faster family discovery through explicit pattern exposure
- Better confidence calibration through self-assessment
- Meta-learning (learning how to learn from examples)
- Voice consistency across related inputs

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
NUM_ARCS_PER_EPOCH = 50  # Each arc = 3 pairs, so 50 arcs = 150 pair exposures
NUM_EPOCHS = 3  # Epochs 11-13 (arc training phase)
START_EPOCH = 11
OUTPUT_DIR = "training/conversational"
ASSESSMENT_THRESHOLD = 0.65  # Min similarity for "good" prediction

print("="*80)
print("🌀 ARC-INSPIRED TRAINING - Pattern Completion Learning")
print("="*80)
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Arcs per epoch: {NUM_ARCS_PER_EPOCH} (×3 pairs = {NUM_ARCS_PER_EPOCH*3} exposures)")
print(f"   Epochs: {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1}")
print(f"   Assessment threshold: {ASSESSMENT_THRESHOLD}")
print(f"   Learning: ✅ ACTIVE")
print()

# Load training pairs
print("📂 Loading training pairs...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"]

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print()

# Initialize organism (preserves learning state from epochs 1-10)
print("🧬 Initializing organism with learned state...")
organism = ConversationalOrganismWrapper()

# Check Phase 5 learning availability
if not hasattr(organism, 'phase5_learning') or organism.phase5_learning is None:
    print("⚠️  WARNING: Phase 5 learning not initialized!")
    print("   Continuing without Phase 5 learning")
    ENABLE_PHASE5 = False
else:
    print(f"   ✅ Phase 5 Organic Learning: {len(organism.phase5_learning.families.families)} existing families")
    ENABLE_PHASE5 = True

print("   ✅ Organism ready for arc training")
print()

# Initialize arc trainer
print("🌀 Initializing Arc-Inspired Trainer...")
arc_trainer = ArcInspiredTrainer(
    organism_wrapper=organism,
    training_pairs=training_pairs,
    enable_learning=ENABLE_PHASE5,
    assessment_threshold=ASSESSMENT_THRESHOLD
)
print()

# Run arc training epochs
all_epoch_summaries = []

for epoch_num in range(START_EPOCH, START_EPOCH + NUM_EPOCHS):
    print("\n")
    print("="*80)
    print(f"🎓 EPOCH {epoch_num} - ARC TRAINING")
    print("="*80)
    print()

    # Track families before epoch
    families_start = len(organism.phase5_learning.families.families) if ENABLE_PHASE5 else 0

    # Run epoch
    epoch_summary = arc_trainer.train_epoch(
        num_arcs=NUM_ARCS_PER_EPOCH,
        category_distribution=None,  # Uniform sampling across categories
        verbose=False  # Set True for detailed per-arc output
    )

    # Track families after epoch
    families_end = len(organism.phase5_learning.families.families) if ENABLE_PHASE5 else 0
    families_discovered = families_end - families_start

    # Add family discovery to summary
    epoch_summary['families_discovered'] = families_discovered
    epoch_summary['total_families'] = families_end
    epoch_summary['epoch'] = epoch_num

    all_epoch_summaries.append(epoch_summary)

    # Save epoch results
    epoch_output_path = f"{OUTPUT_DIR}/epoch_{epoch_num}_arc_training_results.json"
    arc_trainer.save_results(epoch_output_path)

    # Print learning progress
    if ENABLE_PHASE5:
        print(f"\n🧠 Learning Progress:")
        print(f"   Families discovered this epoch: {families_discovered}")
        print(f"   Total families: {families_end}")
        print()

# Final summary across all arc epochs
print()
print("="*80)
print(f"🏆 ARC TRAINING COMPLETE - Epochs {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1}")
print("="*80)
print()

print("📊 Progression Summary:")
print()
print("Epoch | Arcs | Success% | Excellent | Good | Partial | Poor | Families")
print("-" * 85)
for summary in all_epoch_summaries:
    epoch = summary['epoch']
    arcs = summary['arcs_processed']
    success_pct = summary['success_rate'] * 100
    assess_dist = summary['assessment_distribution']
    families = summary.get('total_families', 0)
    discovered = summary.get('families_discovered', 0)
    discovered_str = f"+{discovered}" if discovered > 0 else ""

    print(f"  {epoch}  |  {arcs}  |  {success_pct:5.1f}%  |    {assess_dist['excellent']:2d}     |  {assess_dist['good']:2d}   |   {assess_dist['partial']:2d}    |  {assess_dist['poor']:2d}  | {families} {discovered_str}")

print()

# Get overall statistics
overall_stats = arc_trainer.get_statistics()
print("🎯 Overall Arc Training Statistics:")
print(f"   Total arcs processed: {overall_stats['total_arcs']}")
print(f"   Overall success rate: {overall_stats['success_rate']:.1%}")
print(f"   Mean alignment score: {overall_stats['mean_alignment_score']:.3f}")
print(f"   Mean prediction confidence: {overall_stats['mean_prediction_confidence']:.3f}")
print()

if ENABLE_PHASE5:
    print("🧠 Learning Outcomes:")
    print(f"   Final families: {families_end}")
    print(f"   Total families discovered: {families_end - (families_start if 'families_start' in locals() else 1)}")
    print()

print("✅ Arc training complete!")
print()
print("🔬 Key Insights:")
print("   - Arc training provides explicit pattern exposure")
print("   - Self-assessment calibrates organism's confidence")
print("   - Learning from contrast (predicted vs actual)")
print("   - Meta-learning: organism learns how to learn")
print()
print("📈 Expected Benefits vs Standard Training:")
print("   - Faster family discovery (patterns made explicit)")
print("   - Better confidence calibration (self-assessment feedback)")
print("   - Improved voice consistency (arc coherence)")
print("   - Enhanced pattern recognition (2-shot learning)")
print()
