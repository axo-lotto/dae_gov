#!/usr/bin/env python3
"""
Generate LLM Activation Cache (Local)
======================================

Computes contextual organ activations for all training pairs using Ollama.
Caches results for fast retrieval during training.

100% local, zero cost, data privacy preserved.

Date: November 13, 2025
"""

import sys
import json
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.llm_activation_computer_local import LocalLLMActivationComputer

# Configuration
TRAINING_PAIRS_PATH = "knowledge_base/zones_1_4_training_pairs.json"
CACHE_PATH = "persona_layer/llm_activation_cache_local.json"

print("=" * 80)
print("🧠 LOCAL LLM ACTIVATION CACHE GENERATION")
print("=" * 80)
print()
print("Using Ollama (Llama 3.2 3B) for contextual organ activations")
print(f"Input: {TRAINING_PAIRS_PATH}")
print(f"Output: {CACHE_PATH}")
print()
print("✅ Benefits:")
print("   - $0 cost (vs $5-10 for Claude)")
print("   - 100% data privacy (local processing)")
print("   - Open source, auditable")
print()
print("⚠️  Expected time: ~30-40 minutes for 240 activations")
print("   (Local LLM is slower but free)")
print()

# Load training pairs
print("1️⃣ Loading training pairs...")
try:
    with open(TRAINING_PAIRS_PATH) as f:
        data = json.load(f)
        training_pairs = data["training_pairs"]
except FileNotFoundError:
    print(f"❌ Training pairs not found at: {TRAINING_PAIRS_PATH}")
    print()
    print("Please ensure you've created the zone corpus first.")
    sys.exit(1)

print(f"   ✅ Loaded {len(training_pairs)} pairs")
print(f"   📊 Zones: {data['metadata']['zones']}")
print()

# Initialize local LLM computer
print("2️⃣ Initializing local LLM activation computer...")
try:
    computer = LocalLLMActivationComputer(
        model="llama3.2:3b",
        cache_path=CACHE_PATH
    )
    print("   ✅ Initialized (Ollama running on localhost)")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print()
    print("   Make sure Ollama is running:")
    print("   brew services start ollama")
    print("   ollama pull llama3.2:3b")
    sys.exit(1)
print()

# Test connection
print("3️⃣ Testing Ollama connection...")
try:
    import requests
    response = requests.get("http://localhost:11434/api/version", timeout=5)
    if response.status_code == 200:
        version = response.json()
        print(f"   ✅ Ollama version: {version.get('version', 'unknown')}")
    else:
        print(f"   ⚠️  Ollama responded with status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Cannot connect to Ollama: {e}")
    print()
    print("   Please start Ollama:")
    print("   brew services start ollama")
    sys.exit(1)
print()

# Compute activations for INPUT texts
print("4️⃣ Computing activations for INPUT texts (120 pairs)...")
print("   This will take ~15-20 minutes...")
print()

input_results = computer.batch_compute(
    pairs=training_pairs,
    text_key="input_text",
    id_key="pair_metadata"
)

print()
print("5️⃣ Computing activations for OUTPUT texts (120 pairs)...")
print("   This will take another ~15-20 minutes...")
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
print(f"   Failed parses: {stats['failed_parses']}")
print(f"   Parse success rate: {stats['parse_success_rate']:.1%}")
print(f"   Total time: {stats['total_time']:.1f}s ({stats['total_time']/60:.1f} min)")
print(f"   Avg time per activation: {stats['avg_time_per_miss']:.1f}s")
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
    stats_dict = zone_stats[zone]
    for organ in ["NDAM", "EO", "BOND", "PRESENCE", "SANS"]:
        if stats_dict[organ]:
            mean = sum(stats_dict[organ]) / len(stats_dict[organ])
            std = (sum((x - mean)**2 for x in stats_dict[organ]) / len(stats_dict[organ]))**0.5
            print(f"   {organ}: mean={mean:.2f}, std={std:.2f}")
    print()

print("=" * 80)
print("✅ ACTIVATION CACHE READY FOR TRAINING")
print("=" * 80)
print()
print("Next step: Run training with LLM activations")
print("Command: python3 training/conversational/run_llm_augmented_training.py")
print()
print("Expected result: 5-10 families (vs 1 family with keywords alone)")
print()
