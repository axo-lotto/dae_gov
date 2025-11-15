#!/usr/bin/env python3
"""
Merge Training Corpora - Create Unified Multi-Domain Corpus
============================================================

Merges existing corpus (200 workplace pairs) with expanded corpus (119 crisis/grief pairs)
into a single unified corpus for multi-domain training.

Date: November 12, 2025
"""

import json
from datetime import datetime
from collections import Counter

print("="*80)
print("🔗 CORPUS MERGER - Multi-Domain Training Corpus")
print("="*80)
print()

# Paths
EXISTING_PATH = "knowledge_base/conversational_training_pairs_complete.json"
EXPANDED_PATH = "knowledge_base/conversational_training_pairs_expanded_phase1.json"
OUTPUT_PATH = "knowledge_base/conversational_training_pairs_v4_319.json"

# Load existing corpus
print(f"📂 Loading existing corpus: {EXISTING_PATH}")
with open(EXISTING_PATH) as f:
    existing_data = json.load(f)
    existing_pairs = existing_data['training_pairs']

print(f"   ✅ Loaded {len(existing_pairs)} workplace trauma/burnout pairs")
print()

# Load expanded corpus
print(f"📂 Loading expanded corpus: {EXPANDED_PATH}")
with open(EXPANDED_PATH) as f:
    expanded_data = json.load(f)
    expanded_pairs = expanded_data['training_pairs']

print(f"   ✅ Loaded {len(expanded_pairs)} crisis/grief pairs")
print()

# Normalize existing pairs to include domain field
print("🔧 Normalizing existing pairs...")
normalized_existing = []

for pair in existing_pairs:
    normalized_pair = {
        'input': pair.get('input_text', pair.get('input', '')),
        'output': pair.get('output_text', pair.get('output', '')),
        'category': pair.get('pair_metadata', {}).get('category', 'workplace_trauma'),
        'domain': 'workplace_trauma'  # Add domain field
    }
    normalized_existing.append(normalized_pair)

print(f"   ✅ Normalized {len(normalized_existing)} pairs with domain='workplace_trauma'")
print()

# Combine corpora
print("🔗 Merging corpora...")
merged_pairs = normalized_existing + expanded_pairs

print(f"   ✅ Combined {len(normalized_existing)} + {len(expanded_pairs)} = {len(merged_pairs)} total pairs")
print()

# Analyze merged corpus
print("📊 Analyzing merged corpus...")
print()

domains = [p.get('domain', 'unknown') for p in merged_pairs]
domain_counts = Counter(domains)

print("   Domain Distribution:")
for domain, count in sorted(domain_counts.items()):
    percentage = (count / len(merged_pairs)) * 100
    print(f"      {domain}: {count} pairs ({percentage:.1f}%)")
print()

categories = [p.get('category', 'unknown') for p in merged_pairs]
category_counts = Counter(categories)

print(f"   Total categories: {len(category_counts)}")
print()

# Create merged corpus metadata
merged_metadata = {
    "description": "Multi-domain training corpus v4.0 - Workplace + Crisis + Grief",
    "created": datetime.now().isoformat(),
    "version": "4.0_multi_domain",
    "domains": [
        f"workplace_trauma ({domain_counts['workplace_trauma']} pairs)",
        f"crisis_urgent ({domain_counts.get('crisis_urgent', 0)} pairs)",
        f"grief_loss ({domain_counts.get('grief_loss', 0)} pairs)"
    ],
    "purpose": "Multi-domain arc training for organic family emergence",
    "total_pairs": len(merged_pairs),
    "sources": [
        "conversational_training_pairs_complete.json (200 workplace pairs)",
        "conversational_training_pairs_expanded_phase1.json (119 crisis/grief pairs)"
    ],
    "merge_date": datetime.now().isoformat(),
    "expected_families": "3-5 families by epoch 30 (workplace, crisis, grief clusters)",
    "training_readiness": "✅ Ready for epochs 21-23 multi-domain arc training"
}

# Create merged corpus structure
merged_corpus = {
    "metadata": merged_metadata,
    "statistics": {
        "total_pairs": len(merged_pairs),
        "domain_distribution": dict(domain_counts),
        "category_count": len(category_counts),
        "sources": {
            "existing_corpus": len(normalized_existing),
            "expanded_corpus": len(expanded_pairs)
        }
    },
    "training_pairs": merged_pairs
}

# Save merged corpus
print(f"💾 Saving merged corpus: {OUTPUT_PATH}")
with open(OUTPUT_PATH, 'w') as f:
    json.dump(merged_corpus, f, indent=2)

print(f"   ✅ Saved successfully")
print()

# Validation
print("✅ MERGE COMPLETE")
print()
print(f"   Total pairs: {len(merged_pairs)}")
print(f"   Domains: {len(domain_counts)}")
print(f"   Categories: {len(category_counts)}")
print(f"   Output: {OUTPUT_PATH}")
print()

print("📊 Domain Breakdown:")
print()
for domain, count in sorted(domain_counts.items()):
    percentage = (count / len(merged_pairs)) * 100
    print(f"   {domain:20s} {count:3d} pairs ({percentage:5.1f}%)")
print()

print("🎯 Next Steps:")
print()
print("   1. Validate merged corpus structure")
print("   2. Create epochs 21-23 training script")
print("   3. Run multi-domain arc training")
print("   4. Analyze family emergence patterns")
print()

print("="*80)
