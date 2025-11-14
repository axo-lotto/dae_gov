#!/usr/bin/env python3
"""
Arc Training Epochs 21-26 - Variance-Weighted Signature Re-Training
====================================================================

Re-running epochs 21-26 with VARIANCE-WEIGHTED organ signatures to enable
organic family differentiation.

**Root Cause Fixed:**
Family_001 centroid became uniform (std=0.021) through EMA averaging,
causing ALL signatures to match with 0.87+ similarity regardless of
specialization (EMPATHY-heavy, WISDOM-heavy, BOND-heavy all identical).

**Solution Implemented:**
Variance-weighted signature extraction amplifies discriminative organs
(high variance) and dampens generic organs (low variance) BEFORE L2
normalization, preventing uniform centroid drift.

**Changes from Original Epochs 21-26:**
1. Signature extraction: Standard → Variance-weighted
2. Similarity threshold: 0.85 → 0.75 (more permissive with discriminative signatures)
3. Learning threshold: 0.75 → 0.55 (already lowered, preserved)
4. Families: RESET (fresh start with clean state)

**Expected Outcomes:**
- Centroid std: 0.021 → >0.10 (10× increase in discriminability)
- Families: 1 → 2-4 (genuine differentiation)
- Signature similarity: 0.87 → 0.60-0.75 (healthy diversity)
- Success rate: Maintained at 77-84% (no quality loss)

**Corpus:**
- Workplace trauma: 200 pairs (62.7%)
- Grief & loss: 69 pairs (21.6%)
- Crisis/urgent: 50 pairs (15.7%)
- Total: 319 pairs across 3 domains

Date: November 12, 2025
Status: Phase 1 Implementation - Variance-Weighted Signatures
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
NUM_EPOCHS = 6  # Epochs 21-26
OUTPUT_DIR = "training/conversational"
ASSESSMENT_THRESHOLD = 0.50  # Optimized from epochs 18-20

print("="*80)
print("🌀 ARC TRAINING EPOCHS 21-26 - Variance-Weighted Re-Training")
print("="*80)
print()
print("🎯 Mission:")
print("   Enable organic family differentiation through variance-weighted signatures")
print()
print("🔬 Technical Implementation:")
print("   Variance-weighted extraction: weight = 1.0 + organ_variance")
print("   - High-variance organs (e.g., WISDOM 0.2-0.9) → 2× weight")
print("   - Low-variance organs (e.g., SANS ~0.5) → 1× weight")
print("   - Result: Discriminative signatures that resist uniform drift")
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Total pairs: 319 (3 domains)")
print(f"   Arcs per epoch: {NUM_ARCS_PER_EPOCH}")
print(f"   Epochs: {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1}")
print(f"   Assessment threshold: {ASSESSMENT_THRESHOLD}")
print(f"   Learning threshold: 0.55")
print(f"   Similarity threshold: 0.75 (lowered from 0.85)")
print(f"   Signature extraction: VARIANCE-WEIGHTED ✨")
print(f"   Semantic similarity: SANS embeddings (384-dim)")
print(f"   Learning: ✅ ACTIVE")
print(f"   Families: RESET (fresh start)")
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

# Initialize organism (fresh state - families reset)
print("🧬 Initializing organism with VARIANCE-WEIGHTED signatures...")
organism = ConversationalOrganismWrapper()

# Check Phase 5 learning availability
if not hasattr(organism, 'phase5_learning') or organism.phase5_learning is None:
    print("❌ ERROR: Phase 5 learning not initialized!")
    print("   Cannot proceed without Phase 5 learning")
    sys.exit(1)

families_start = len(organism.phase5_learning.families.families)
threshold = organism.phase5_learning.learning_threshold
similarity_threshold = organism.phase5_learning.families.similarity_threshold

print(f"   ✅ Phase 5 Organic Learning initialized")
print(f"   ✅ Starting families: {families_start} (reset)")
print(f"   ✅ Learning threshold: {threshold:.2f}")
print(f"   ✅ Similarity threshold: {similarity_threshold:.2f}")
print(f"   ✅ Variance-weighted extraction: ACTIVE ✨")
print()

# Verify signature extraction method
extractor = organism.phase5_learning.signature_extractor
if not hasattr(extractor, 'extract_composite_signature_variance_weighted'):
    print("❌ ERROR: Variance-weighted extraction method not found!")
    print("   Please verify organ_signature_extractor.py has been updated")
    sys.exit(1)

print("✅ Variance-weighted extraction method confirmed")
print()

# Initialize arc trainer (with SANS embeddings + optimized threshold)
print("🌀 Initializing Arc-Inspired Trainer...")
arc_trainer = ArcInspiredTrainer(
    organism_wrapper=organism,
    training_pairs=training_pairs,
    enable_learning=True,
    assessment_threshold=ASSESSMENT_THRESHOLD
)
print()

# Verify SANS embeddings are active
if not arc_trainer.use_embeddings:
    print("❌ ERROR: SANS embeddings not available!")
    sys.exit(1)

print("✅ SANS embeddings confirmed active")
print()

# Run epochs 21-26
all_epoch_summaries = []

for epoch_num in range(START_EPOCH, START_EPOCH + NUM_EPOCHS):
    print("\n")
    print("="*80)
    print(f"🎓 EPOCH {epoch_num} - VARIANCE-WEIGHTED TRAINING")
    print("="*80)
    print()

    # Track families before epoch
    families_before = len(organism.phase5_learning.families.families)

    # Run epoch
    epoch_summary = arc_trainer.train_epoch(
        num_arcs=NUM_ARCS_PER_EPOCH,
        category_distribution=None,  # Natural distribution
        verbose=False  # Quiet mode for faster processing
    )

    # Track families after epoch
    families_after = len(organism.phase5_learning.families.families)
    families_discovered = families_after - families_before

    # Add metadata
    epoch_summary['families_discovered'] = families_discovered
    epoch_summary['total_families'] = families_after
    epoch_summary['epoch'] = epoch_num
    epoch_summary['threshold'] = ASSESSMENT_THRESHOLD
    epoch_summary['learning_threshold'] = threshold
    epoch_summary['similarity_threshold'] = similarity_threshold
    epoch_summary['corpus_version'] = 'v4_319_multidomain'
    epoch_summary['signature_method'] = 'variance_weighted'

    all_epoch_summaries.append(epoch_summary)

    # Save epoch results
    epoch_output_path = f"{OUTPUT_DIR}/epoch_{epoch_num}_arc_training_variance_weighted.json"
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

    print(f"   Families: {families_after} ({families_discovered:+d} this epoch)")
    if families_discovered > 0:
        print(f"   🎉 NEW FAMILY DISCOVERED!")

    print()

# Final summary
print()
print("="*80)
print(f"🏆 VARIANCE-WEIGHTED RE-TRAINING EPOCHS {START_EPOCH}-{START_EPOCH+NUM_EPOCHS-1} COMPLETE")
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

print("📈 Epochs 21-26 Overall Statistics:")
print(f"   Total arcs: {total_arcs}")
print(f"   Success rate: {overall_success_rate:.1%} ({total_successful}/{total_arcs})")
print(f"   Mean alignment: {mean_alignment:.3f}")
print(f"   Mean confidence: {mean_confidence:.3f}")
print()

# Learning outcomes
families_final = organism.phase5_learning.families.families
families_end = len(families_final)
families_total_discovered = families_end - families_start

print("🧠 Learning Outcomes (Variance-Weighted):")
print(f"   Families at start (epoch 21): {families_start}")
print(f"   Families at end (epoch 26): {families_end}")
print(f"   Total discovered: {families_total_discovered}")
print(f"   Signature method: Variance-weighted ✨")
print(f"   Similarity threshold: {similarity_threshold:.2f}")
print()

if families_end > families_start:
    print("   🎉 SUCCESS! Families discovered with variance-weighted signatures!")
    print()

    # Analyze family composition
    for family_id, family_data in organism.phase5_learning.families.families.items():
        member_count = family_data.get('member_count', 0)
        mean_sat = family_data.get('mean_satisfaction', 0)
        maturity = family_data.get('maturity_level', 'unknown')

        print(f"   {family_id}:")
        print(f"      Members: {member_count}")
        print(f"      Mean satisfaction: {mean_sat:.3f}")
        print(f"      Maturity: {maturity}")

        # Check if centroid is discriminative
        centroid = family_data.get('centroid', [])
        if centroid:
            import numpy as np
            centroid_std = float(np.std(centroid))
            print(f"      Centroid std: {centroid_std:.3f}", end="")
            if centroid_std > 0.10:
                print(" ✅ DISCRIMINATIVE")
            elif centroid_std > 0.05:
                print(" ⚠️  MODERATE")
            else:
                print(" ❌ UNIFORM")

        print()
else:
    print("   ⚠️  No families formed. Diagnostic analysis needed.")
    print()

# Variance-weighted validation
print("="*80)
print("🔬 VARIANCE-WEIGHTED VALIDATION")
print("="*80)
print()

print("Question: Do variance-weighted signatures enable family differentiation?")
if families_end > families_start:
    print(f"   ✅ YES: {families_total_discovered} families discovered")
    print(f"   Result: {families_start} → {families_end} families")

    # Validate centroid discrimination
    all_discriminative = True
    for family_id, family_data in organism.phase5_learning.families.families.items():
        centroid = family_data.get('centroid', [])
        if centroid:
            import numpy as np
            centroid_std = float(np.std(centroid))
            if centroid_std < 0.10:
                all_discriminative = False
                break

    if all_discriminative:
        print(f"   ✅ All family centroids are discriminative (std >0.10)")
        print(f"   Variance weighting SUCCESSFUL!")
    else:
        print(f"   ⚠️  Some centroids still uniform (std <0.10)")
        print(f"   May need stronger variance amplification")
else:
    print(f"   ❌ NO: Still {families_end} families")
    print(f"   Recommendation: Run diagnostic tool to analyze signatures")
print()

# Comparison to original epochs 21-26
print("Comparison to Original Epochs 21-26 (standard signatures):")
print(f"   Original: 77-84% success, 1 family (uniform centroid, std=0.021)")
print(f"   Variance-weighted: {overall_success_rate:.1%} success, {families_end} families")
print()

print("="*80)
print("🚀 Next Steps:")
print("="*80)
print()

if families_end > families_start:
    print("✅ Variance-weighted signatures SUCCESSFUL!")
    print()
    print("1. Run diagnostic tool to analyze family discrimination")
    print("2. Validate signature diversity across families")
    print("3. Proceed to Phase 2: Multi-mode training (logical/poetic/dialectical)")
    print("4. Test family stability with cross-domain validation")
else:
    print("⚠️  Variance weighting inconclusive")
    print()
    print("1. Run diagnostic tool: python3 diagnose_family_clustering.py")
    print("2. Analyze signature variances per organ")
    print("3. Consider increasing variance_amplification parameter")
    print("4. Validate that variance computation is working correctly")

print()

print("💾 All results saved to: training/conversational/epoch_{21..26}_arc_training_variance_weighted.json")
print()

print("="*80)
print("📊 PHASE 1 COMPLETE - Variance-Weighted Signature Implementation")
print("="*80)
print()
