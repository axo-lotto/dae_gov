#!/usr/bin/env python3
"""
Arc Training Epochs 21-23 - Multi-Domain Family Emergence Test
===============================================================

First test of multi-domain corpus (319 pairs across 3 therapeutic domains).

**Critical Hypotheses:**
1. Multi-domain training enables family differentiation (1 → 3-5 families)
2. Cross-domain transfer penalty: 82% (within) → 70-75% (cross)
3. Organ specialization emerges (NDAM/EO variance increases in crisis)
4. PRESENCE acts as bridge organ across domains

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
START_EPOCH = 21
NUM_EPOCHS = 3  # Epochs 21-23
OUTPUT_DIR = "training/conversational"
ASSESSMENT_THRESHOLD = 0.50  # Optimized from epochs 18-20

print("="*80)
print("🌀 ARC TRAINING EPOCHS 21-23 - Multi-Domain Family Emergence Test")
print("="*80)
print()
print("🎯 Research Hypotheses:")
print("   H1: Family differentiation (1 family → 3-5 families)")
print("   H2: Cross-domain transfer penalty (82% → 70-75%)")
print("   H3: Organ specialization (NDAM/EO variance ↑ in crisis)")
print("   H4: PRESENCE acts as bridge organ")
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Total pairs: 319 (3 domains)")
print(f"   Arcs per epoch: {NUM_ARCS_PER_EPOCH}")
print(f"   Epochs: {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1}")
print(f"   Assessment threshold: {ASSESSMENT_THRESHOLD} (optimized)")
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

# Initialize organism (preserves learning state from epochs 1-20)
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

print("   ✅ Organism ready for multi-domain arc training")
print()

# Initialize arc trainer (with SANS embeddings + optimized threshold)
print("🌀 Initializing Arc-Inspired Trainer...")
arc_trainer = ArcInspiredTrainer(
    organism_wrapper=organism,
    training_pairs=training_pairs,
    enable_learning=ENABLE_PHASE5,
    assessment_threshold=ASSESSMENT_THRESHOLD  # 0.50 (optimized from epochs 18-20)
)
print()

# Verify SANS embeddings are active
if not arc_trainer.use_embeddings:
    print("❌ ERROR: SANS embeddings not available!")
    sys.exit(1)

print("✅ SANS embeddings confirmed active")
print()

# Run epochs 21-23
all_epoch_summaries = []

for epoch_num in range(START_EPOCH, START_EPOCH + NUM_EPOCHS):
    print("\n")
    print("="*80)
    print(f"🎓 EPOCH {epoch_num} - MULTI-DOMAIN ARC TRAINING")
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

    print()

# Final summary
print()
print("="*80)
print(f"🏆 MULTI-DOMAIN ARC TRAINING EPOCHS {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1} COMPLETE")
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

# Overall statistics for epochs 21-23
total_arcs = sum(s.get('arcs_processed', NUM_ARCS_PER_EPOCH) for s in all_epoch_summaries)
total_successful = sum(int(s.get('arcs_processed', NUM_ARCS_PER_EPOCH) * s.get('success_rate', 0)) for s in all_epoch_summaries)
overall_success_rate = total_successful / total_arcs if total_arcs > 0 else 0

mean_alignment = sum(s.get('mean_alignment_score', 0) for s in all_epoch_summaries) / len(all_epoch_summaries) if all_epoch_summaries else 0
mean_confidence = sum(s.get('mean_prediction_confidence', 0) for s in all_epoch_summaries) / len(all_epoch_summaries) if all_epoch_summaries else 0

print("📈 Epochs 21-23 Overall Statistics (Multi-Domain):")
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

    if families_end > families_start:
        print("   🎉 New families discovered! Analyzing signatures...")
        print()

        for i, family in enumerate(families_final):
            print(f"   Family {i+1}:")
            print(f"      Conversations: {family.conversation_count}")
            print(f"      Created: {family.timestamp}")
            # Could add more family analysis here
            print()

# Hypothesis validation
print("="*80)
print("🔬 HYPOTHESIS VALIDATION")
print("="*80)
print()

# H1: Family differentiation
print("H1: Family Differentiation (1 → 3-5 families)")
if ENABLE_PHASE5:
    if families_end >= 3:
        print(f"   ✅ CONFIRMED: {families_end} families (was {families_start})")
    elif families_end > families_start:
        print(f"   ⚠️  PARTIAL: {families_end} families (expected 3-5)")
    else:
        print(f"   ❌ NOT CONFIRMED: Still {families_end} families")
else:
    print("   ⚠️  Cannot validate (Phase 5 learning not enabled)")
print()

# H2: Cross-domain transfer
print("H2: Cross-Domain Transfer Penalty (82% → 70-75%)")
if overall_success_rate >= 0.70 and overall_success_rate <= 0.82:
    print(f"   ✅ CONFIRMED: {overall_success_rate:.1%} success rate (expected 70-82%)")
elif overall_success_rate > 0.82:
    print(f"   🎉 EXCEEDED: {overall_success_rate:.1%} success rate (better than expected!)")
elif overall_success_rate >= 0.65:
    print(f"   ⚠️  PARTIAL: {overall_success_rate:.1%} success rate (slightly below 70%)")
else:
    print(f"   ❌ NOT CONFIRMED: {overall_success_rate:.1%} success rate (below 65%)")
print()

# Note for H3 and H4
print("H3: Organ Specialization")
print("   📊 Requires detailed organ activation variance analysis")
print("   → Run analyze_organ_specialization.py after training")
print()

print("H4: PRESENCE as Bridge Organ")
print("   📊 Requires cross-domain activation correlation analysis")
print("   → Run analyze_bridge_organs.py after training")
print()

print("="*80)
print("🚀 Next Steps:")
print("="*80)
print()
print("1. Analyze family signatures and domain alignment")
print("2. Compute organ specialization metrics (NDAM/EO variance)")
print("3. Measure cross-domain transfer rates by domain pair")
print("4. Identify bridge organs (shared activations)")
print("5. Plan Phase 2 corpus expansion (if validated)")
print()

print("💾 All results saved to: training/conversational/epoch_{21,22,23}_arc_training_results.json")
print()
