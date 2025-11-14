#!/usr/bin/env python3
"""
Epoch 1 Training with Humanized Complete Corpus
================================================

Training with 200-pair expanded corpus:
- 30 original (burnout/productivity)
- 80 humanized (casual + self-awareness + grounding)
- 90 transduction (9 pathways × 10 examples)

Expected improvements:
- Voice diversity (casual + therapeutic)
- Self-awareness capabilities
- Grounding language fluency
- Transduction pathway coverage
"""

import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

# Configuration
TRAINING_PAIRS_PATH = "/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/conversational_training_pairs_complete.json"
NUM_PAIRS = 200  # Use all pairs
ENABLE_PHASE2 = True  # Multi-cycle V0 convergence with reconstruction
EPOCH_NUM = 1
OUTPUT_PATH = f"training/conversational/epoch_{EPOCH_NUM}_humanized_results.json"

print("="*80)
print("🌀 EPOCH 1 TRAINING - HUMANIZED COMPLETE CORPUS")
print("="*80)
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Num pairs: {NUM_PAIRS}")
print(f"   Phase 2: {ENABLE_PHASE2}")
print(f"   Reconstruction: ENABLED")
print(f"   Epoch: {EPOCH_NUM}")
print(f"   Output: {OUTPUT_PATH}")
print()

# Load training pairs
print("📂 Loading training pairs...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"][:NUM_PAIRS]

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print(f"   📊 Corpus stats:")
print(f"      Total: {data['statistics']['total_pairs']}")
print(f"      Humanized: {data['statistics']['humanized_pairs']}")
print(f"      Transduction: {data['statistics']['transduction_pairs']}")
print()

# Initialize components
print("🧬 Initializing organism...")
wrapper = ConversationalOrganismWrapper()
print("   ✅ Organism ready")
print()

# Training metrics
results = []
total_confidence = 0.0
total_nexuses = 0
total_cycles = 0
zone_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
pathway_counts = {}
strategy_counts = {"direct_reconstruction": 0, "family_template": 0, "hebbian_fallback": 0}
success_count = 0

# Category tracking for diversity
category_counts = {}
polyvagal_counts = {"dorsal_vagal": 0, "sympathetic": 0, "ventral_vagal": 0, "mixed_state": 0}

print("🎓 Beginning training...")
print("="*80)

for idx, pair in enumerate(training_pairs, 1):
    pair_id = pair["pair_metadata"]["id"]
    category = pair["pair_metadata"].get("category", "unknown")
    polyvagal = pair["pair_metadata"].get("polyvagal_state", "mixed_state")
    pathway = pair["pair_metadata"].get("transduction_pathway")

    input_text = pair["input_text"]
    target_output = pair["output_text"]

    # Track category/polyvagal diversity
    category_counts[category] = category_counts.get(category, 0) + 1
    polyvagal_counts[polyvagal] = polyvagal_counts.get(polyvagal, 0) + 1
    if pathway:
        pathway_counts[pathway] = pathway_counts.get(pathway, 0) + 1

    print(f"\n[{idx}/{NUM_PAIRS}] {pair_id} ({category})")
    print(f"   Input: {input_text[:80]}...")

    try:
        # Process text with Phase 2 + reconstruction
        result = wrapper.process_text(
            input_text,
            context={'pair_id': pair_id, 'epoch': EPOCH_NUM},
            enable_tsk_recording=False,
            enable_phase2=ENABLE_PHASE2
        )

        # Extract metrics
        felt_states = result.get('felt_states', {})
        emission_text = result.get('emission_text', '')
        emission_confidence = result.get('emission_confidence', 0.0)
        emission_path = result.get('emission_path', 'unknown')
        cycles = felt_states.get('convergence_cycles', 1)
        zone_id = felt_states.get('zone_id', 0)
        nexuses_count = felt_states.get('nexuses_formed', 0)

        # Update strategy counts
        if emission_path in strategy_counts:
            strategy_counts[emission_path] += 1

        # Note: Learning happens implicitly through organism processing
        # No explicit learning coordinator needed for Phase 2

        # Track metrics
        total_confidence += emission_confidence
        total_nexuses += nexuses_count
        total_cycles += cycles
        if zone_id in zone_counts:
            zone_counts[zone_id] += 1

        success_count += 1

        print(f"   ✅ Confidence: {emission_confidence:.3f} | Cycles: {cycles} | Nexuses: {nexuses_count} | Zone: {zone_id}")
        print(f"   📝 Output: {emission_text[:80]}...")
        print(f"   🎯 Path: {emission_path}")

        # Store result
        results.append({
            "pair_id": pair_id,
            "category": category,
            "polyvagal_state": polyvagal,
            "transduction_pathway": pathway,
            "emission_confidence": emission_confidence,
            "emission_path": emission_path,
            "convergence_cycles": cycles,
            "nexuses_formed": nexuses_count,
            "zone_id": zone_id,
            "learning_applied": True
        })

    except Exception as e:
        print(f"   ❌ Error: {e}")
        results.append({
            "pair_id": pair_id,
            "error": str(e),
            "learning_applied": False
        })

print()
print("="*80)
print("📊 EPOCH 1 TRAINING COMPLETE")
print("="*80)

# Calculate statistics
mean_confidence = total_confidence / success_count if success_count > 0 else 0.0
mean_nexuses = total_nexuses / success_count if success_count > 0 else 0.0
mean_cycles = total_cycles / success_count if success_count > 0 else 0.0

print(f"\n🎯 Success Rate: {success_count}/{NUM_PAIRS} ({100*success_count/NUM_PAIRS:.1f}%)")
print(f"📈 Mean Confidence: {mean_confidence:.3f}")
print(f"🌀 Mean Nexuses: {mean_nexuses:.2f}")
print(f"⏱️  Mean Cycles: {mean_cycles:.2f}")
print()

print("🗺️  SELF Matrix Zone Distribution:")
for zone_id in sorted(zone_counts.keys()):
    count = zone_counts[zone_id]
    pct = (count / success_count * 100) if success_count > 0 else 0.0
    zone_name = ["Unknown", "Safe", "Regulated Stress", "High Stress", "Crisis", "Shutdown"][zone_id] if zone_id <= 5 else "Unknown"
    print(f"   Zone {zone_id} ({zone_name}): {count} ({pct:.1f}%)")
print()

print("🎭 Emission Strategy Distribution:")
for strategy, count in sorted(strategy_counts.items()):
    pct = (count / success_count * 100) if success_count > 0 else 0.0
    print(f"   {strategy}: {count} ({pct:.1f}%)")
print()

print("🌈 Category Diversity:")
print(f"   Unique categories: {len(category_counts)}")
top_10_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for cat, count in top_10_cats:
    print(f"   {cat}: {count}")
print()

print("🧠 Polyvagal State Distribution:")
for state, count in sorted(polyvagal_counts.items()):
    pct = (count / NUM_PAIRS * 100)
    print(f"   {state}: {count} ({pct:.1f}%)")
print()

if pathway_counts:
    print("🌀 Transduction Pathway Coverage:")
    for pathway, count in sorted(pathway_counts.items()):
        print(f"   {pathway}: {count}")
    print()

# Save results
output_data = {
    "metadata": {
        "epoch": EPOCH_NUM,
        "timestamp": datetime.now().isoformat(),
        "training_pairs_path": TRAINING_PAIRS_PATH,
        "num_pairs": NUM_PAIRS,
        "phase2_enabled": ENABLE_PHASE2,
        "reconstruction_enabled": True
    },
    "summary": {
        "success_rate": success_count / NUM_PAIRS,
        "mean_confidence": mean_confidence,
        "mean_nexuses": mean_nexuses,
        "mean_cycles": mean_cycles,
        "zone_distribution": zone_counts,
        "strategy_distribution": strategy_counts,
        "category_diversity": len(category_counts),
        "polyvagal_distribution": polyvagal_counts,
        "pathway_coverage": pathway_counts
    },
    "results": results
}

with open(OUTPUT_PATH, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"💾 Results saved to: {OUTPUT_PATH}")
print()
print("✅ Epoch 1 training complete!")
print()
print("🎯 Next Steps:")
print("   1. Review voice diversity (casual vs therapeutic)")
print("   2. Validate self-awareness responses")
print("   3. Check grounding language integration")
print("   4. Run epochs 2-3 for voice maturation")
