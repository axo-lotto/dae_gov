#!/usr/bin/env python3
"""
Arc Training Epochs 24-26 - Learning Threshold Test (0.75 → 0.55)
===================================================================

Testing lowered Phase 5 learning threshold to enable family emergence.

**Critical Question:**
Will lowering learning_threshold from 0.75 to 0.55 enable organic
family differentiation without compromising pattern quality?

**Changes from Epochs 21-23:**
- Learning threshold: 0.75 → 0.55 (26.7% reduction)
- Expected: More permissive family formation
- Hypothesis: 1 family → 2-4 families by epoch 26

**Corpus:**
- Workplace trauma: 200 pairs (62.7%)
- Grief & loss: 69 pairs (21.6%)
- Crisis/urgent: 50 pairs (15.7%)
- Total: 319 pairs across 3 domains

Date: November 12, 2025
"""

import sys
import json
from pathlib import Path
from collections import Counter

# Add project root to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from persona_layer.arc_inspired_trainer import ArcInspiredTrainer

# Configuration
TRAINING_PAIRS_PATH = "/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/conversational_training_pairs_v4_319.json"
NUM_ARCS_PER_EPOCH = 50
START_EPOCH = 24
NUM_EPOCHS = 3  # Epochs 24-26
OUTPUT_DIR = "training/conversational"
ASSESSMENT_THRESHOLD = 0.50  # Optimized from epochs 18-20

print("="*80)
print("🌀 ARC TRAINING EPOCHS 24-26 - Learning Threshold Test (0.55)")
print("="*80)
print()
print("🎯 Research Question:")
print("   Does lowering learning_threshold enable family emergence?")
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Total pairs: 319 (3 domains)")
print(f"   Arcs per epoch: {NUM_ARCS_PER_EPOCH}")
print(f"   Epochs: {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1}")
print(f"   Assessment threshold: {ASSESSMENT_THRESHOLD}")
print(f"   Learning threshold: 0.55 (was 0.75)")
print(f"   Semantic similarity: SANS embeddings (384-dim)")
print(f"   Learning: ✅ ACTIVE")
print()

# Load training pairs
print("📂 Loading multi-domain training corpus...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"]
    metadata = data.get("metadata", {})

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print()

# Domain distribution
domains = [p.get('domain', 'unknown') for p in training_pairs]
domain_counts = Counter(domains)

print("   📊 Domain Distribution:")
for domain, count in sorted(domain_counts.items()):
    percentage = (count / len(training_pairs)) * 100
    print(f"      {domain:20s} {count:3d} pairs ({percentage:5.1f}%)")
print()

# Initialize organism (preserves learning state from epochs 1-23)
print("🧬 Initializing organism with learned state...")
organism = ConversationalOrganismWrapper()

# Check Phase 5 learning availability
if not hasattr(organism, 'phase5_learning') or organism.phase5_learning is None:
    print("⚠️  WARNING: Phase 5 learning not initialized!")
    print("   Continuing without Phase 5 learning")
    ENABLE_PHASE5 = False
else:
    families_start = len(organism.phase5_learning.families.families)
    threshold = organism.phase5_learning.learning_threshold
    print(f"   ✅ Phase 5 Organic Learning: {families_start} existing families")
    print(f"   ✅ Learning threshold: {threshold:.2f} (lowered from 0.75)")
    ENABLE_PHASE5 = True

print("   ✅ Organism ready for threshold test")
print()

# Initialize arc trainer (with SANS embeddings + optimized threshold)
print("🌀 Initializing Arc-Inspired Trainer...")
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
    sys.exit(1)

print("✅ SANS embeddings confirmed active")
print()

# Run epochs 24-26
all_epoch_summaries = []

for epoch_num in range(START_EPOCH, START_EPOCH + NUM_EPOCHS):
    print("\n")
    print("="*80)
    print(f"🎓 EPOCH {epoch_num} - THRESHOLD TEST (learning_threshold=0.55)")
    print("="*80)
    print()

    # Track families before epoch
    families_before = len(organism.phase5_learning.families.families) if ENABLE_PHASE5 else 0

    # Run epoch
    epoch_summary = arc_trainer.train_epoch(
        num_arcs=NUM_ARCS_PER_EPOCH,
        category_distribution=None,  # Natural distribution
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
    epoch_summary['learning_threshold'] = 0.55
    epoch_summary['corpus_version'] = 'v4_319_multidomain'

    all_epoch_summaries.append(epoch_summary)

    # Save epoch results
    epoch_output_path = f"{OUTPUT_DIR}/epoch_{epoch_num}_arc_training_results.json"
    arc_trainer.save_results(epoch_output_path)

    print(f"\n✅ Epoch {epoch_num} Complete")
    print(f"   Arcs: {epoch_summary.get('arcs_processed', NUM_ARCS_PER_EPOCH)}")

    if 'success_rate' in epoch_summary:
        success_count = int(epoch_summary['arcs_processed'] * epoch_summary['success_rate'])
        print(f"   Success rate: {epoch_summary['success_rate']:.1%} ({success_count}/{epoch_summary['arcs_processed']})")

    if 'mean_alignment_score' in epoch_summary:
        print(f"   Mean alignment: {epoch_summary['mean_alignment_score']:.3f}")

    if 'mean_prediction_confidence' in epoch_summary:
        print(f"   Mean confidence: {epoch_summary['mean_prediction_confidence']:.3f}")

    if ENABLE_PHASE5:
        print(f"   Families: {families_after} ({families_discovered:+d} this epoch)")
        if families_discovered > 0:
            print(f"   🎉 NEW FAMILY DISCOVERED!")

    print()

# Final summary
print()
print("="*80)
print(f"🏆 THRESHOLD TEST EPOCHS {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1} COMPLETE")
print("="*80)
print()

print("📊 Progression Summary:")
print()
print("Epoch | Arcs | Success% | Mean Alignment | Mean Confidence | Families")
print("-" * 85)

for summary in all_epoch_summaries:
    epoch = summary['epoch']
    arcs = summary.get('arcs_processed', NUM_ARCS_PER_EPOCH)
    success_pct = summary.get('success_rate', 0) * 100
    alignment = summary.get('mean_alignment_score', 0)
    confidence = summary.get('mean_prediction_confidence', 0)
    families = summary.get('total_families', 0)
    discovered = summary.get('families_discovered', 0)
    discovered_str = f"(+{discovered})" if discovered > 0 else ""

    print(f"  {epoch}  |  {arcs}  |  {success_pct:5.1f}%  |     {alignment:.3f}      |      {confidence:.3f}      | {families} {discovered_str}")

print()

# Overall statistics
total_arcs = sum(s.get('arcs_processed', NUM_ARCS_PER_EPOCH) for s in all_epoch_summaries)
total_successful = sum(int(s.get('arcs_processed', NUM_ARCS_PER_EPOCH) * s.get('success_rate', 0)) for s in all_epoch_summaries)
overall_success_rate = total_successful / total_arcs if total_arcs > 0 else 0

mean_alignment = sum(s.get('mean_alignment_score', 0) for s in all_epoch_summaries) / len(all_epoch_summaries) if all_epoch_summaries else 0
mean_confidence = sum(s.get('mean_prediction_confidence', 0) for s in all_epoch_summaries) / len(all_epoch_summaries) if all_epoch_summaries else 0

print("📈 Epochs 24-26 Overall Statistics:")
print(f"   Total arcs: {total_arcs}")
print(f"   Success rate: {overall_success_rate:.1%} ({total_successful}/{total_arcs})")
print(f"   Mean alignment: {mean_alignment:.3f}")
print(f"   Mean confidence: {mean_confidence:.3f}")
print()

if ENABLE_PHASE5:
    families_final = organism.phase5_learning.families.families
    families_end = len(families_final)
    families_total_discovered = families_end - families_start

    print("🧠 Learning Outcomes (Threshold Test):")
    print(f"   Families at start (epoch 24): {families_start}")
    print(f"   Families at end (epoch 26): {families_end}")
    print(f"   Total discovered: {families_total_discovered}")
    print(f"   Learning threshold: 0.55 (was 0.75)")
    print()

    if families_end > families_start:
        print("   🎉 SUCCESS! New families discovered with lowered threshold!")
        print()

        for i, family in enumerate(families_final):
            print(f"   Family {i+1}:")
            print(f"      Conversations: {family.conversation_count}")
            print(f"      Created: {family.timestamp}")
            print()
    else:
        print("   ⚠️  No new families formed. Consider further threshold reduction?")
        print()

# Threshold test validation
print("="*80)
print("🔬 THRESHOLD TEST VALIDATION")
print("="*80)
print()

print("Question: Does learning_threshold=0.55 enable family emergence?")
if ENABLE_PHASE5:
    if families_end > families_start:
        print(f"   ✅ YES: {families_total_discovered} new families discovered")
        print(f"   Result: {families_start} → {families_end} families")
    else:
        print(f"   ❌ NO: Still {families_end} families (no change)")
        print(f"   Recommendation: Try threshold=0.45 or investigate clustering algorithm")
else:
    print("   ⚠️  Cannot validate (Phase 5 learning not enabled)")
print()

# Comparison to epochs 21-23
print("Comparison to Epochs 21-23 (threshold=0.75):")
print(f"   Epochs 21-23: 84.0% success, 0 families discovered")
print(f"   Epochs 24-26: {overall_success_rate:.1%} success, {families_total_discovered if ENABLE_PHASE5 else 'N/A'} families discovered")
print()

print("="*80)
print("🚀 Next Steps:")
print("="*80)
print()

if ENABLE_PHASE5 and families_end > families_start:
    print("✅ Threshold test SUCCESSFUL - families emerged!")
    print()
    print("1. Analyze new family signatures and domain alignment")
    print("2. Compare family patterns to training corpus categories")
    print("3. Test family stability with additional epochs")
    print("4. Plan corpus expansion based on family insights")
else:
    print("⚠️  Threshold test INCONCLUSIVE - no new families")
    print()
    print("1. Review Phase 5 learning clustering algorithm")
    print("2. Analyze similarity distributions in learned conversations")
    print("3. Consider threshold=0.45 or different similarity metric")
    print("4. Investigate if 1 family is actually optimal for this corpus")

print()

print("💾 All results saved to: training/conversational/epoch_{24,25,26}_arc_training_results.json")
print()
