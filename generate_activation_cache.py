#!/usr/bin/env python3
"""
Generate LLM Activation Cache
==============================

Computes contextual organ activations for all training pairs using Claude.
Caches results for fast retrieval during training.

This enables true multi-family differentiation by giving organs
the contextual understanding that keywords cannot provide.
"""

import sys
import json
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.llm_activation_computer import LLMActivationComputer

# Configuration
TRAINING_PAIRS_PATH = "knowledge_base/zones_1_4_training_pairs.json"
CACHE_PATH = "persona_layer/llm_activation_cache.json"

print("=" * 80)
print("🧠 LLM ACTIVATION CACHE GENERATION")
print("=" * 80)
print()
print("Using Claude to compute contextual organ activations")
print(f"Input: {TRAINING_PAIRS_PATH}")
print(f"Output: {CACHE_PATH}")
print()

# Load training pairs
print("1️⃣ Loading training pairs...")
with open(TRAINING_PAIRS_PATH) as f:
    data = json.load(f)
    training_pairs = data["training_pairs"]

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print(f"   📊 Zones: {data['metadata']['zones']}")
print()

# Initialize LLM computer
print("2️⃣ Initializing LLM activation computer...")
try:
    computer = LLMActivationComputer(cache_path=CACHE_PATH)
    print("   ✅ Initialized (ANTHROPIC_API_KEY found)")
except ValueError as e:
    print(f"   ❌ Error: {e}")
    print()
    print("   Please set ANTHROPIC_API_KEY environment variable:")
    print("   export ANTHROPIC_API_KEY='your-key-here'")
    sys.exit(1)
print()

# Compute activations for INPUT texts
print("3️⃣ Computing activations for INPUT texts (120 pairs)...")
print()

input_results = computer.batch_compute(
    pairs=training_pairs,
    text_key="input_text",
    id_key="pair_metadata"
)

print()
print("4️⃣ Computing activations for OUTPUT texts (120 pairs)...")
print()

# Modify pair IDs for outputs
output_pairs = []
for pair in training_pairs:
    output_pair = pair.copy()
    output_pair["pair_metadata"] = pair["pair_metadata"].copy()
    output_pair["pair_metadata"]["id"] = pair["pair_metadata"]["id"] + "_OUTPUT"
    output_pair["input_text"] = pair["output_text"]  # Use output_text as input
    output_pairs.append(output_pair)

output_results = computer.batch_compute(
    pairs=output_pairs,
    text_key="input_text",
    id_key="pair_metadata"
)

print()
print("=" * 80)
print("📊 CACHE GENERATION COMPLETE")
print("=" * 80)
print()

# Statistics
stats = computer.get_stats()
print(f"✅ Total activations computed: {stats['cache_size']}")
print(f"   Expected: 240 (120 inputs + 120 outputs)")
print(f"   Cache hits: {stats['cache_hits']}")
print(f"   Cache misses: {stats['cache_misses']}")
print(f"   Hit rate: {stats['hit_rate']:.1%}")
print()

# Analyze diversity
print("📊 Analyzing activation diversity by zone...")
print()

zone_stats = {}
for pair in training_pairs:
    pair_id = pair["pair_metadata"]["id"]
    zone = pair["pair_metadata"]["zone"]

    if zone not in zone_stats:
        zone_stats[zone] = {
            "NDAM": [],
            "EO": [],
            "BOND": [],
            "PRESENCE": [],
            "SANS": []
        }

    activations = input_results.get(pair_id, {})
    for organ in ["NDAM", "EO", "BOND", "PRESENCE", "SANS"]:
        if organ in activations:
            zone_stats[zone][organ].append(activations[organ])

# Print zone averages
for zone in sorted(zone_stats.keys()):
    print(f"Zone {zone}:")
    stats = zone_stats[zone]
    for organ in ["NDAM", "EO", "BOND", "PRESENCE", "SANS"]:
        if stats[organ]:
            mean = sum(stats[organ]) / len(stats[organ])
            print(f"   {organ}: {mean:.2f}")
    print()

print("=" * 80)
print("✅ ACTIVATION CACHE READY FOR TRAINING")
print("=" * 80)
print()
print("Next step: Run training with LLM activations")
print("Command: python3 training/conversational/run_llm_augmented_training.py")
print()
