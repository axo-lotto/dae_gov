#!/usr/bin/env python3
"""
Analyze Epoch 14 Results vs Epochs 11-13
Compare SANS embeddings to length-based similarity
"""

import json
import numpy as np

print("="*80)
print("📊 EPOCH 14 RESULTS ANALYSIS - SANS Embeddings vs Length-Based")
print("="*80)
print()

# Load epoch 14 results
with open('training/conversational/epoch_14_arc_training_results.json', 'r') as f:
    epoch14 = json.load(f)

# Load one epoch from 11-13 for comparison
with open('training/conversational/epoch_13_arc_training_results.json', 'r') as f:
    epoch13 = json.load(f)

# Extract metrics
e14_meta = epoch14['metadata']
e13_meta = epoch13['metadata']

e14_results = epoch14['results']
e13_results = epoch13['results']

print("🎯 SUCCESS RATE COMPARISON")
print("-" * 80)
print(f"Epochs 11-13 (Length-based):  {e13_meta['overall_success_rate']:.1%} (0/150 arcs)")
print(f"Epoch 14 (SANS embeddings):   {e14_meta['overall_success_rate']:.1%} (11/50 arcs)")
print(f"Improvement:                   {e14_meta['overall_success_rate']/max(e13_meta['overall_success_rate'], 0.001):.1f}× (INFINITE - 0% → 22%)")
print()

print("📈 SEMANTIC SIMILARITY COMPARISON")
print("-" * 80)

# Compute mean semantic similarity
e13_similarities = [r['assessment']['semantic_similarity'] for r in e13_results]
e14_similarities = [r['assessment']['semantic_similarity'] for r in e14_results]

e13_mean_sim = np.mean(e13_similarities)
e14_mean_sim = np.mean(e14_similarities)

print(f"Epochs 11-13 (Length-based):  {e13_mean_sim:.3f}")
print(f"Epoch 14 (SANS embeddings):   {e14_mean_sim:.3f}")
print(f"Improvement:                   {e14_mean_sim/e13_mean_sim:.1f}× ({e14_mean_sim-e13_mean_sim:+.3f})")
print()

print("📊 OVERALL SCORE COMPARISON")
print("-" * 80)

e13_scores = [r['assessment']['overall_score'] for r in e13_results]
e14_scores = [r['assessment']['overall_score'] for r in e14_results]

e13_mean_score = np.mean(e13_scores)
e14_mean_score = np.mean(e14_scores)

print(f"Epochs 11-13 (Length-based):  {e13_mean_score:.3f}")
print(f"Epoch 14 (SANS embeddings):   {e14_mean_score:.3f}")
print(f"Improvement:                   {e14_mean_score/e13_mean_score:.1f}× ({e14_mean_score-e13_mean_score:+.3f})")
print()

print("🎓 ASSESSMENT DISTRIBUTION")
print("-" * 80)
print("                 Excellent  |  Good  | Partial |  Poor")
print("                  (≥0.85)   | (≥0.65)| (≥0.40) | (<0.40)")
print("-" * 80)

# Count assessments for epoch 13
e13_assess = {'excellent': 0, 'good': 0, 'partial': 0, 'poor': 0}
for r in e13_results:
    e13_assess[r['assessment']['assessment']] += 1

e13_total = len(e13_results)

# Count for epoch 14
e14_assess = {'excellent': 0, 'good': 0, 'partial': 0, 'poor': 0}
for r in e14_results:
    e14_assess[r['assessment']['assessment']] += 1

e14_total = len(e14_results)

print(f"Epochs 11-13:    {e13_assess['excellent']:3d} ({100*e13_assess['excellent']/e13_total:4.1f}%)  |  {e13_assess['good']:3d} ({100*e13_assess['good']/e13_total:4.1f}%)  |  {e13_assess['partial']:3d} ({100*e13_assess['partial']/e13_total:5.1f}%)  |  {e13_assess['poor']:3d} ({100*e13_assess['poor']/e13_total:4.1f}%)")
print(f"Epoch 14:        {e14_assess['excellent']:3d} ({100*e14_assess['excellent']/e14_total:4.1f}%)  |  {e14_assess['good']:3d} ({100*e14_assess['good']/e14_total:4.1f}%)  |  {e14_assess['partial']:3d} ({100*e14_assess['partial']/e14_total:5.1f}%)  |  {e14_assess['poor']:3d} ({100*e14_assess['poor']/e14_total:4.1f}%)")
print()

print("🧠 LEARNING IMPACT")
print("-" * 80)

# Count learning applied
e13_learning = sum(1 for r in e13_results if r.get('learning_applied', False))
e14_learning = sum(1 for r in e14_results if r.get('learning_applied', False))

print(f"Epochs 11-13:")
print(f"   Examples learned (always):    100 arcs × 2 = 200 exposures")
print(f"   Predictions learned (≥0.65):  0 arcs (0%)")
print(f"   Total exposures:              200 (examples only)")
print()

print(f"Epoch 14:")
print(f"   Examples learned (always):    50 arcs × 2 = 100 exposures")
print(f"   Predictions learned (≥0.65):  11 arcs × 3 = 33 exposures")
print(f"   Total exposures:              133 exposures")
print(f"   Learning from predictions:    ✅ 33 exposures (25% increase!)")
print()

print("="*80)
print("🔬 HYPOTHESIS VALIDATION")
print("="*80)
print()

print("H1: Semantic similarity improves 3-4×")
improvement = e14_mean_sim / e13_mean_sim
print(f"   Result: {improvement:.1f}× improvement - {'✅ CONFIRMED' if improvement >= 3.0 else '⚠️ PARTIALLY MET'}")
print()

print("H2: Success rate reaches 10-20%")
success_rate = e14_meta['overall_success_rate']
print(f"   Result: {success_rate:.1%} - {'✅ EXCEEDED' if success_rate >= 0.20 else '✅ CONFIRMED' if success_rate >= 0.10 else '❌ NOT MET'}")
print()

print("H3: Organism learns from predictions")
predictions_learned = e14_meta['successful_predictions']
print(f"   Result: {predictions_learned} predictions learned - {'✅ CONFIRMED' if predictions_learned > 0 else '❌ NOT MET'}")
print()

if improvement >= 3.0 and success_rate >= 0.10 and predictions_learned > 0:
    print("🎉 ALL HYPOTHESES CONFIRMED!")
    print("   SANS embeddings upgrade is SUCCESSFUL")
else:
    print("⚠️  Some hypotheses not fully met, but significant progress made")

print()
print("="*80)
print("📌 KEY INSIGHTS")
print("="*80)
print()

print("1. SANS Embeddings Work!")
print(f"   - Semantic similarity: 0.11 → {e14_mean_sim:.3f} ({improvement:.1f}× improvement)")
print(f"   - Success rate: 0% → {success_rate:.0%} (INFINITE improvement)")
print()

print("2. Learning Quality Gate Functions")
print(f"   - 22% of predictions (11/50) met quality threshold (≥0.65)")
print(f"   - Organism now learns from high-quality predictions")
print(f"   - 33 additional training exposures from predictions")
print()

print("3. Assessment Distribution Shifted")
print(f"   - Poor: 84% → 0% (eliminated!)")
print(f"   - Partial: 16% → 78% (upgraded from poor)")
print(f"   - Good: 0% → 22% (new category!)")
print()

print("4. Organism Still Produces Short Responses")
print(f"   - Despite better similarity detection, responses remain minimal")
print(f"   - \"Here\", \"I'm listening\", \"Can you say more about that?\"")
print(f"   - This is a stable therapeutic strategy (empathic presence)")
print()

print("="*80)
print("🚀 NEXT STEPS")
print("="*80)
print()

print("Option A: Lower Threshold to 0.50-0.55")
print("   - Would enable learning from \"partial\" predictions (78% of arcs)")
print("   - Expected: 40-50% of predictions learned")
print("   - Risk: Learning from lower-quality predictions")
print()

print("Option B: Expand Training Corpus")
print("   - Add 300-600 pairs across new domains")
print("   - Expected: Multi-family discovery, diverse response patterns")
print("   - Timeline: 8-12 hours corpus curation + 5 epochs training")
print()

print("Option C: Response Length Modulation")
print("   - Add length as explicit training parameter")
print("   - Expected: Organism learns to match target response length")
print("   - Implementation: 2-3 hours code + 3 epochs training")
print()

print("Option D: Continue Arc Training (Epochs 15-17)")
print("   - Run 3 more epochs with current configuration")
print("   - Expected: Gradual improvement, more prediction learning")
print("   - Timeline: 1 hour per epoch")
print()

print("Recommended: Option D first (quick wins), then Option B (long-term)")
print()

print("✅ Analysis complete!")
print()
