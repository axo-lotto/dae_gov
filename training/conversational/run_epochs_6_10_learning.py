#!/usr/bin/env python3
"""
Epochs 6-10 Training with LEARNING ACTIVATION
==============================================

Learning-Guided Maturation Phase - Phase 5 learning + Hebbian R-matrix active.

Training with 200-pair corpus over 5 epochs WITH learning:
- Epoch 6: First learning activation
- Epoch 7-8: Family discovery accelerates
- Epoch 9-10: Archetypal patterns emerge

Expected improvements:
- Families: 1 → 5-8 discovered
- Confidence: 0.43 → 0.55-0.70
- Emission strategies: hebbian → family (30-50%) → direct (10-20%)
- Voice: Homogeneous → Archetypal (family-guided)
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
START_EPOCH = 6
END_EPOCH = 10
OUTPUT_DIR = "training/conversational"
LEARNING_ACTIVE = True  # ✅ LEARNING ENABLED!

print("="*80)
print("🧠 EPOCHS 6-10 TRAINING - LEARNING ACTIVATION PHASE")
print("="*80)
print()
print("📋 Configuration:")
print(f"   Training corpus: {TRAINING_PAIRS_PATH}")
print(f"   Num pairs: {NUM_PAIRS}")
print(f"   Phase 2: {ENABLE_PHASE2}")
print(f"   Epochs: {START_EPOCH}-{END_EPOCH}")
print(f"   Learning: ✅ ACTIVE (Phase 5 + Hebbian R-matrix)")
print()

# Load training pairs
print("📂 Loading training pairs...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"][:NUM_PAIRS]

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print()

# Initialize organism ONCE for all epochs (preserves learning state)
print("🧬 Initializing organism with learning enabled...")
wrapper = ConversationalOrganismWrapper()

# Check if Phase 5 learning is available
if not hasattr(wrapper, 'phase5_learning') or wrapper.phase5_learning is None:
    print("⚠️  WARNING: Phase 5 learning not initialized in wrapper!")
    print("   Continuing without Phase 5 learning (Hebbian R-matrix still active)")
    ENABLE_PHASE5 = False
else:
    print(f"   ✅ Phase 5 Organic Learning: {len(wrapper.phase5_learning.families.families)} existing families")
    ENABLE_PHASE5 = True

print("   ✅ Organism ready for learning")
print()

# Track metrics across epochs
all_epochs_results = []

for epoch_num in range(START_EPOCH, END_EPOCH + 1):
    print("="*80)
    print(f"🎓 EPOCH {epoch_num} BEGINNING (LEARNING ACTIVE)")
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

    # Learning tracking
    families_start = len(wrapper.phase5_learning.families.families) if ENABLE_PHASE5 else 0
    learning_applied_count = 0

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
            satisfaction = felt_states.get('satisfaction_final', 0.0)

            # ✅ LEARNING ACTIVATION: Phase 5 Organic Learning
            if ENABLE_PHASE5 and satisfaction >= 0.75:
                try:
                    # Extract organ results from felt_states (if available)
                    organ_results = felt_states.get('organ_results', {})

                    # Create minimal AssembledResponse-like object
                    assembled_response = type('obj', (object,), {
                        'text': emission_text,
                        'confidence': emission_confidence,
                        'emission_path': emission_path,
                        'satisfaction': satisfaction
                    })()

                    wrapper.phase5_learning.learn_from_conversation(
                        organ_results=organ_results,
                        assembled_response=assembled_response,
                        user_message=input_text,
                        conversation_id=f"epoch{epoch_num}_pair{idx:03d}"
                    )

                    learning_applied_count += 1
                except Exception as e:
                    if idx == 1:  # Only log first error
                        print(f"   ⚠️  Phase 5 learning error (will continue): {e}")

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
                "emission_confidence": float(emission_confidence),
                "emission_path": emission_path,
                "convergence_cycles": int(cycles),
                "nexuses_formed": int(nexuses_count),
                "zone_id": int(zone_id),
                "satisfaction": float(satisfaction),
                "learning_applied": bool(satisfaction >= 0.75)
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

    # Learning stats
    families_end = len(wrapper.phase5_learning.families.families) if ENABLE_PHASE5 else 0
    families_discovered = families_end - families_start

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

    if ENABLE_PHASE5:
        print("🧠 Learning Progress:")
        print(f"   Learning applied: {learning_applied_count}/{success_count} pairs (satisfaction ≥ 0.75)")
        print(f"   Families discovered this epoch: {families_discovered}")
        print(f"   Total families: {families_end}")
        print()

    # Save epoch results
    epoch_output = {
        "metadata": {
            "epoch": int(epoch_num),
            "timestamp": datetime.now().isoformat(),
            "training_pairs_path": TRAINING_PAIRS_PATH,
            "num_pairs": int(NUM_PAIRS),
            "phase2_enabled": bool(ENABLE_PHASE2),
            "reconstruction_enabled": True,
            "learning_active": True,
            "phase5_enabled": bool(ENABLE_PHASE5)
        },
        "summary": {
            "success_rate": float(success_count / NUM_PAIRS),
            "mean_confidence": float(mean_confidence),
            "mean_nexuses": float(mean_nexuses),
            "mean_cycles": float(mean_cycles),
            "zone_distribution": {int(k): int(v) for k, v in zone_counts.items()},
            "strategy_distribution": {str(k): int(v) for k, v in strategy_counts.items()},
            "category_diversity": int(len(category_counts)),
            "polyvagal_distribution": {str(k): int(v) for k, v in polyvagal_counts.items()},
            "pathway_coverage": {str(k): int(v) for k, v in pathway_counts.items()},
            "learning_applied_count": int(learning_applied_count if ENABLE_PHASE5 else 0),
            "families_discovered": int(families_discovered if ENABLE_PHASE5 else 0),
            "total_families": int(families_end if ENABLE_PHASE5 else 0)
        },
        "results": results
    }

    output_path = f"{OUTPUT_DIR}/epoch_{epoch_num}_learning_results.json"
    with open(output_path, 'w') as f:
        json.dump(epoch_output, f, indent=2)

    print(f"💾 Epoch {epoch_num} results saved to: {output_path}")

    # Track for summary
    all_epochs_results.append({
        "epoch": epoch_num,
        "mean_confidence": mean_confidence,
        "mean_nexuses": mean_nexuses,
        "mean_cycles": mean_cycles,
        "strategy_distribution": strategy_counts,
        "families_total": families_end if ENABLE_PHASE5 else 0,
        "families_discovered": families_discovered if ENABLE_PHASE5 else 0
    })
    print()

# Final summary across all epochs
print()
print("="*80)
print("🏆 EPOCHS 6-10 COMPLETE - LEARNING-GUIDED MATURATION PHASE")
print("="*80)
print()

print("📊 Progression Summary:")
print()
print("Epoch | Confidence | Nexuses | Cycles | Hebbian% | Family% | Direct% | Families")
print("-" * 85)
for er in all_epochs_results:
    total = sum(er['strategy_distribution'].values())
    heb_pct = (er['strategy_distribution']['hebbian_fallback'] / total * 100) if total > 0 else 0
    fam_pct = (er['strategy_distribution']['family_template'] / total * 100) if total > 0 else 0
    dir_pct = (er['strategy_distribution']['direct_reconstruction'] / total * 100) if total > 0 else 0
    families = er.get('families_total', 0)
    discovered = er.get('families_discovered', 0)
    discovered_str = f"+{discovered}" if discovered > 0 else ""
    print(f"  {er['epoch']}   |   {er['mean_confidence']:.3f}    |  {er['mean_nexuses']:.2f}   |  {er['mean_cycles']:.2f}  |  {heb_pct:5.1f}%  | {fam_pct:5.1f}%  | {dir_pct:5.1f}%  | {families} {discovered_str}")

print()
print("✅ Learning-guided maturation complete!")
print()
print("🎯 Learning Achievements:")
if ENABLE_PHASE5:
    print(f"   - Families discovered: {families_end}")
    print(f"   - Voice diversification: {strategy_counts.get('family_template', 0)} family-guided emissions")
else:
    print("   - Phase 5 learning not available")
print(f"   - Hebbian R-matrix: Active (check for non-identity weights)")
print()
print("📈 Expected Voice Evolution:")
print("   - Confidence: 0.43 → 0.55-0.70 (actual: {:.3f})".format(all_epochs_results[-1]['mean_confidence']))
print("   - Families: 1 → 5-8 (actual: {})".format(families_end if ENABLE_PHASE5 else 0))
print("   - Family strategy: 0% → 30-50%")
print()
print("🔬 Next Steps:")
print("   1. Inspect organic_families.json for discovered patterns")
print("   2. Review family-guided emissions for voice diversity")
print("   3. Check Hebbian R-matrix for learned phrase weights")
print("   4. Validate archetypal pattern emergence")
print()
