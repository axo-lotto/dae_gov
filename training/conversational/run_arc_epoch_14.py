#!/usr/bin/env python3
"""
Arc Training Epoch 14 - SANS Embeddings Upgrade
===============================================

First epoch with upgraded semantic similarity (SANS embeddings).

Hypothesis: Semantic embedding-based similarity will improve:
- Mean alignment score: 0.275 → 0.40-0.50
- Success rate: 0% → 10-20%
- Learning from predictions: 0 → 5-10 predictions

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
NUM_ARCS = 50  # Each arc = 3 pairs, so 50 arcs = 150 pair exposures
EPOCH_NUM = 14
OUTPUT_DIR = "training/conversational"
ASSESSMENT_THRESHOLD = 0.65  # Keep same as epochs 11-13 for comparison

print("="*80)
print("🌀 ARC TRAINING EPOCH 14 - SANS Embeddings Upgrade")
print("="*80)
print()
print("🎯 Hypothesis Testing:")
print("   Semantic embeddings should improve alignment score 3-4×")
print("   Expected success rate: 10-20% (vs 0% with length-based)")
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Arcs: {NUM_ARCS} (×3 pairs = {NUM_ARCS*3} exposures)")
print(f"   Epoch: {EPOCH_NUM}")
print(f"   Assessment threshold: {ASSESSMENT_THRESHOLD}")
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

# Initialize organism (preserves learning state from epochs 1-13)
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

# Initialize arc trainer (with SANS embeddings!)
print("🌀 Initializing Arc-Inspired Trainer with SANS embeddings...")
arc_trainer = ArcInspiredTrainer(
    organism_wrapper=organism,
    training_pairs=training_pairs,
    enable_learning=ENABLE_PHASE5,
    assessment_threshold=ASSESSMENT_THRESHOLD
)
print()

# Verify SANS embeddings are active
if not arc_trainer.use_embeddings:
    print("❌ ERROR: SANS embeddings not available!")
    print("   Install with: pip install sentence-transformers")
    sys.exit(1)

print("✅ SANS embeddings confirmed active")
print()

# Track families before epoch
families_start = len(organism.phase5_learning.families.families) if ENABLE_PHASE5 else 0

# Run epoch 14
print("="*80)
print(f"🎓 EPOCH {EPOCH_NUM} - SANS EMBEDDINGS TEST")
print("="*80)
print()

epoch_summary = arc_trainer.train_epoch(
    num_arcs=NUM_ARCS,
    category_distribution=None,  # Uniform sampling across categories
    verbose=True  # Show detailed progress for first epoch with embeddings
)

# Track families after epoch
families_end = len(organism.phase5_learning.families.families) if ENABLE_PHASE5 else 0
families_discovered = families_end - families_start

# Add family discovery to summary
epoch_summary['families_discovered'] = families_discovered
epoch_summary['total_families'] = families_end
epoch_summary['epoch'] = EPOCH_NUM

# Save epoch results
epoch_output_path = f"{OUTPUT_DIR}/epoch_{EPOCH_NUM}_arc_training_results.json"
arc_trainer.save_results(epoch_output_path)

print()
print("="*80)
print(f"🏆 EPOCH {EPOCH_NUM} COMPLETE")
print("="*80)
print()

# Get epoch statistics
print("📊 Epoch 14 Results:")
print()
print(f"   Arcs processed: {epoch_summary['arcs_processed']}")
print(f"   Success rate: {epoch_summary['success_rate']:.1%} ({epoch_summary['successful_predictions']}/{epoch_summary['arcs_processed']})")
print(f"   Mean alignment score: {epoch_summary['mean_alignment_score']:.3f}")
print(f"   Mean prediction confidence: {epoch_summary['mean_prediction_confidence']:.3f}")
print()

print("   Assessment Distribution:")
dist = epoch_summary['assessment_distribution']
print(f"      Excellent (≥0.85): {dist['excellent']} ({100*dist['excellent']/NUM_ARCS:.1f}%)")
print(f"      Good (≥0.65): {dist['good']} ({100*dist['good']/NUM_ARCS:.1f}%)")
print(f"      Partial (≥0.40): {dist['partial']} ({100*dist['partial']/NUM_ARCS:.1f}%)")
print(f"      Poor (<0.40): {dist['poor']} ({100*dist['poor']/NUM_ARCS:.1f}%)")
print()

if ENABLE_PHASE5:
    print("🧠 Learning Outcomes:")
    print(f"   Families discovered: {families_discovered}")
    print(f"   Total families: {families_end}")
    print()

# Comparison to epochs 11-13
print("="*80)
print("📈 COMPARISON: Epochs 11-13 (Length-based) vs Epoch 14 (SANS Embeddings)")
print("="*80)
print()

print("Metric                        | Epochs 11-13 | Epoch 14  | Change")
print("-" * 75)
print(f"Mean alignment score          |    0.275     | {epoch_summary['mean_alignment_score']:7.3f}  | {epoch_summary['mean_alignment_score']/0.275:+.1f}×")
print(f"Success rate                  |     0.0%     | {epoch_summary['success_rate']*100:6.1f}%  | {epoch_summary['successful_predictions']:+2d} successful")
print(f"Mean prediction confidence    |    0.680     | {epoch_summary['mean_prediction_confidence']:7.3f}  | {(epoch_summary['mean_prediction_confidence']-0.680):+.3f}")
print(f"Excellent assessments         |       0      |   {dist['excellent']:3d}    | {dist['excellent']:+3d}")
print(f"Good assessments              |       0      |   {dist['good']:3d}    | {dist['good']:+3d}")
print()

# Hypothesis validation
print("🔬 Hypothesis Validation:")
print()

expected_alignment = 0.40  # Lower bound of prediction
actual_alignment = epoch_summary['mean_alignment_score']
alignment_met = actual_alignment >= expected_alignment

expected_success_low = 0.10  # 10% lower bound
actual_success = epoch_summary['success_rate']
success_met = actual_success >= expected_success_low

print(f"   H1: Mean alignment score ≥ 0.40")
print(f"       Result: {actual_alignment:.3f} - {'✅ CONFIRMED' if alignment_met else '❌ NOT MET'}")
print()

print(f"   H2: Success rate ≥ 10%")
print(f"       Result: {actual_success:.1%} - {'✅ CONFIRMED' if success_met else '❌ NOT MET'}")
print()

print(f"   H3: Organism learns from predictions")
print(f"       Result: {epoch_summary['successful_predictions']} predictions learned - {'✅ CONFIRMED' if epoch_summary['successful_predictions'] > 0 else '❌ NOT MET'}")
print()

if alignment_met and success_met:
    print("🎉 SANS embeddings upgrade SUCCESSFUL!")
    print("   Semantic similarity metric is now production-ready")
else:
    print("⚠️  Results partially met expectations")
    print("   Further calibration may be needed")

print()
print(f"💾 Results saved to: {epoch_output_path}")
print()
print("✅ Epoch 14 complete!")
print()
