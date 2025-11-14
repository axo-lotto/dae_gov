#!/usr/bin/env python3
"""
Epochs 2-5 Training with Humanized Complete Corpus
==================================================

Pattern Foundation Phase - Organic emergence without learning activation.

Training with 200-pair expanded corpus over 4 epochs:
- Epoch 2: Pattern repetition begins
- Epoch 3: Meta-atom activation increases
- Epoch 4: Nexus formation starts
- Epoch 5: Reconstruction strategies mature

Learning activation after Epoch 5 (next session).
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
START_EPOCH = 2
END_EPOCH = 5
OUTPUT_DIR = "training/conversational"

print("="*80)
print("🌀 EPOCHS 2-5 TRAINING - PATTERN FOUNDATION PHASE")
print("="*80)
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Num pairs: {NUM_PAIRS}")
print(f"   Phase 2: {ENABLE_PHASE2}")
print(f"   Epochs: {START_EPOCH}-{END_EPOCH}")
print(f"   Learning: INACTIVE (pattern foundation)")
print()

# Load training pairs
print("📂 Loading training pairs...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"][:NUM_PAIRS]

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print()

# Initialize organism ONCE for all epochs
print("🧬 Initializing organism...")
wrapper = ConversationalOrganismWrapper()
print("   ✅ Organism ready")
print()

# Track metrics across epochs
all_epochs_results = []

for epoch_num in range(START_EPOCH, END_EPOCH + 1):
    print("="*80)
    print(f"🎓 EPOCH {epoch_num} BEGINNING")
    print("="*80)
    print()

    # Epoch metrics
    results = []
    total_confidence = 0.0
    total_nexuses = 0
    total_cycles = 0
    zone_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    pathway_counts = {}
    strategy_counts = {"direct_reconstruction": 0, "family_template": 0, "hebbian_fallback": 0}
    success_count = 0

    # Category tracking
    category_counts = {}
    polyvagal_counts = {"dorsal_vagal": 0, "sympathetic": 0, "ventral_vagal": 0, "mixed_state": 0}

    for idx, pair in enumerate(training_pairs, 1):
        pair_id = pair["pair_metadata"]["id"]
        category = pair["pair_metadata"].get("category", "unknown")
        polyvagal = pair["pair_metadata"].get("polyvagal_state", "mixed_state")
        pathway = pair["pair_metadata"].get("transduction_pathway")

        input_text = pair["input_text"]
        target_output = pair["output_text"]

        # Track diversity
        category_counts[category] = category_counts.get(category, 0) + 1
        polyvagal_counts[polyvagal] = polyvagal_counts.get(polyvagal, 0) + 1
        if pathway:
            pathway_counts[pathway] = pathway_counts.get(pathway, 0) + 1

        # Print progress every 20 pairs
        if idx % 20 == 0 or idx == 1:
            print(f"[{idx}/{NUM_PAIRS}] {pair_id} ({category})")

        try:
            # Process text with Phase 2 + reconstruction
            result = wrapper.process_text(
                input_text,
                context={'pair_id': pair_id, 'epoch': epoch_num},
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

            # Track metrics
            total_confidence += emission_confidence
            total_nexuses += nexuses_count
            total_cycles += cycles
            if zone_id in zone_counts:
                zone_counts[zone_id] += 1

            success_count += 1

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
                "zone_id": zone_id
            })

        except Exception as e:
            print(f"   ❌ Error on pair {pair_id}: {e}")
            results.append({
                "pair_id": pair_id,
                "error": str(e)
            })

    print()
    print("="*80)
    print(f"📊 EPOCH {epoch_num} COMPLETE")
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

    print("🎭 Emission Strategy Distribution:")
    for strategy, count in sorted(strategy_counts.items()):
        pct = (count / success_count * 100) if success_count > 0 else 0.0
        print(f"   {strategy}: {count} ({pct:.1f}%)")
    print()

    # Save epoch results
    epoch_output = {
        "metadata": {
            "epoch": epoch_num,
            "timestamp": datetime.now().isoformat(),
            "training_pairs_path": TRAINING_PAIRS_PATH,
            "num_pairs": NUM_PAIRS,
            "phase2_enabled": ENABLE_PHASE2,
            "reconstruction_enabled": True,
            "learning_active": False
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

    output_path = f"{OUTPUT_DIR}/epoch_{epoch_num}_humanized_results.json"
    with open(output_path, 'w') as f:
        json.dump(epoch_output, f, indent=2)

    print(f"💾 Epoch {epoch_num} results saved to: {output_path}")

    # Track for summary
    all_epochs_results.append({
        "epoch": epoch_num,
        "mean_confidence": mean_confidence,
        "mean_nexuses": mean_nexuses,
        "mean_cycles": mean_cycles,
        "strategy_distribution": strategy_counts
    })
    print()

# Final summary across all epochs
print()
print("="*80)
print("🏆 EPOCHS 2-5 COMPLETE - PATTERN FOUNDATION ESTABLISHED")
print("="*80)
print()

print("📊 Progression Summary:")
print()
print("Epoch | Confidence | Nexuses | Cycles | Hebbian% | Family% | Direct%")
print("-" * 75)
for er in all_epochs_results:
    total = sum(er['strategy_distribution'].values())
    heb_pct = (er['strategy_distribution']['hebbian_fallback'] / total * 100) if total > 0 else 0
    fam_pct = (er['strategy_distribution']['family_template'] / total * 100) if total > 0 else 0
    dir_pct = (er['strategy_distribution']['direct_reconstruction'] / total * 100) if total > 0 else 0
    print(f"  {er['epoch']}   |   {er['mean_confidence']:.3f}    |  {er['mean_nexuses']:.2f}   |  {er['mean_cycles']:.2f}  |  {heb_pct:5.1f}%  | {fam_pct:5.1f}%  | {dir_pct:5.1f}%")

print()
print("✅ Pattern foundation complete!")
print()
print("🎯 Next Steps:")
print("   1. Review nexus formation trajectory")
print("   2. Examine meta-atom activation patterns")
print("   3. Activate learning after analysis")
print("   4. Run epochs 6-10 with learning enabled")
print()
print("📈 Expected After Learning Activation:")
print("   - Confidence: 0.43 → 0.55-0.70")
print("   - Nexuses: 0-3 → 5-10")
print("   - Family strategy: 0% → 30-50%")
print("   - Direct reconstruction: 0% → 10-20%")
