#!/usr/bin/env python3
"""
LLM-Augmented Training - Proof of Concept
==========================================

Train organism by directly modifying organ semantic_atoms.json with LLM activations.
This bypasses keyword processing and should enable multi-family differentiation.

Approach:
1. Load baseline semantic_atoms.json (keyword-based)
2. For each training pair with cached LLM activations:
   - Replace atom activations in semantic_atoms.json with LLM values
   - Process pair through organism (triggers learning)
   - Restore original semantic_atoms.json
3. Analyze family formation

Date: November 13, 2025
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("=" * 80)
print("🧠 LLM-AUGMENTED TRAINING (Proof of Concept)")
print("=" * 80)
print()
print("Training organism with cached LLM activations")
print("Goal: Achieve multi-family differentiation (5-10 families vs 1 baseline)")
print()

# Paths
TRAINING_PAIRS_PATH = "knowledge_base/zones_1_4_training_pairs.json"
CACHE_PATH = "persona_layer/llm_activation_cache_local.json"
SEMANTIC_ATOMS_PATH = "persona_layer/semantic_atoms.json"
SEMANTIC_ATOMS_BACKUP = "persona_layer/semantic_atoms_backup.json"
FAMILIES_PATH = "persona_layer/organic_families.json"

# Load training pairs
print("1️⃣  Loading training pairs and cache...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"]

with open(CACHE_PATH) as f:
    cache = json.load(f)

print(f"   ✅ Loaded {len(training_pairs)} training pairs")
print(f"   ✅ Loaded {len(cache)} cached activations")
print()

# Filter to only pairs with cached activations
cached_pairs = [p for p in training_pairs if p["pair_metadata"]["id"] in cache]
print(f"   📊 Pairs with cache: {len(cached_pairs)}")
print()

# Backup original semantic_atoms.json
print("2️⃣  Backing up original semantic_atoms.json...")
with open(SEMANTIC_ATOMS_PATH) as f:
    semantic_atoms_original = json.load(f)

with open(SEMANTIC_ATOMS_BACKUP, 'w') as f:
    json.dump(semantic_atoms_original, f, indent=2)
print("   ✅ Backup created")
print()

# Backup original families
print("3️⃣  Saving baseline family state...")
with open(FAMILIES_PATH) as f:
    families_before = json.load(f)
baseline_families = len(families_before.get("families", {}))
print(f"   📊 Baseline families: {baseline_families}")
print()

# Initialize organism ONCE (will reload between pairs via direct modification)
print("4️⃣  Initializing organism...")
organism = ConversationalOrganismWrapper()
print("   ✅ Organism ready")
print()

# Training loop
print("5️⃣  Training with LLM activations...")
print()

results = []
for idx, pair in enumerate(cached_pairs, 1):
    pair_id = pair["pair_metadata"]["id"]
    zone = pair["pair_metadata"]["zone"]
    input_text = pair["input_text"]

    print(f"[{idx}/{len(cached_pairs)}] Zone {zone}: {pair_id}")

    # Get cached activations for this pair
    cached_acts = cache[pair_id]

    # Modify semantic_atoms.json to inject LLM activations
    # (simplified: just set all atoms of each organ to the activation value)
    modified_atoms = {}
    for organ_name, activation in cached_acts.items():
        # Set all atoms of this organ to the LLM activation
        if organ_name in semantic_atoms_original:
            modified_atoms[organ_name] = {}
            for atom_name in semantic_atoms_original[organ_name].keys():
                modified_atoms[organ_name][atom_name] = activation

    # Write modified semantic_atoms.json
    with open(SEMANTIC_ATOMS_PATH, 'w') as f:
        json.dump(modified_atoms, f, indent=2)

    # Reinitialize organism to pick up new semantic_atoms
    organism = ConversationalOrganismWrapper()

    # Process input (this will trigger learning automatically)
    start_time = time.time()
    result = organism.process_text(
        input_text,
        context={'pair_id': pair_id},
        enable_tsk_recording=False,
        enable_phase2=True
    )
    processing_time = time.time() - start_time

    # Extract metrics
    felt_states = result.get('felt_states', {})
    confidence = felt_states.get('emission_confidence', 0.0)

    print(f"   ✅ Processed ({processing_time:.2f}s, confidence={confidence:.3f})")

    results.append({
        "pair_id": pair_id,
        "zone": zone,
        "confidence": confidence,
        "processing_time": processing_time
    })

print()

# Restore original semantic_atoms.json
print("6️⃣  Restoring original semantic_atoms.json...")
with open(SEMANTIC_ATOMS_BACKUP) as f:
    semantic_atoms_original = json.load(f)
with open(SEMANTIC_ATOMS_PATH, 'w') as f:
    json.dump(semantic_atoms_original, f, indent=2)
print("   ✅ Restored")
print()

# Analyze family formation
print("7️⃣  Analyzing family formation...")
with open(FAMILIES_PATH) as f:
    families_after = json.load(f)

families = families_after.get("families", {})
num_families = len(families)

print(f"   📊 Families after training: {num_families}")
print()

# Family analysis
if num_families > 0:
    for fam_id, fam_data in sorted(families.items()):
        members = fam_data.get("conversations", [])
        print(f"   {fam_id}: {len(members)} members")
        # Show zone distribution
        zone_counts = {}
        for member in members:
            zone = None
            # Try to extract zone from conversation_id
            for pair in cached_pairs:
                if pair["pair_metadata"]["id"] in member.get("conversation_id", ""):
                    zone = pair["pair_metadata"]["zone"]
                    break
            if zone:
                zone_counts[zone] = zone_counts.get(zone, 0) + 1
        if zone_counts:
            print(f"      Zones: {dict(sorted(zone_counts.items()))}")
print()

# Save results
output_path = "results/llm_augmented_training_results.json"
Path(output_path).parent.mkdir(parents=True, exist_ok=True)
with open(output_path, 'w') as f:
    json.dump({
        "metadata": {
            "pairs_trained": len(results),
            "baseline_families": baseline_families,
            "families_after": num_families,
            "cache_size": len(cache)
        },
        "results": results,
        "families": {fam_id: len(fam_data.get("conversations", []))
                    for fam_id, fam_data in families.items()}
    }, f, indent=2)

print(f"💾 Results saved to: {output_path}")
print()

# Verdict
print("=" * 80)
if num_families > baseline_families:
    print(f"✅ SUCCESS: Multi-family differentiation achieved!")
    print(f"   Baseline: {baseline_families} family/families")
    print(f"   LLM-augmented: {num_families} families")
    print()
    print("   🎉 LLM activations solve the keyword ceiling problem!")
else:
    print(f"⚠️  PARTIAL: Still {num_families} family/families")
    print(f"   Baseline: {baseline_families}")
    print(f"   Possible causes:")
    print(f"   - LLM activations too uniform (many all 1.0s)")
    print(f"   - Need more cached activations (currently {len(cache)}/240)")
    print(f"   - Family learning threshold too high")
print("=" * 80)
