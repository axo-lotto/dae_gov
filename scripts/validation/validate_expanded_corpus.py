#!/usr/bin/env python3
"""
Validate Expanded Corpus Structure and Compatibility
=====================================================

Ensures expanded corpus is compatible with arc trainer and organism.

Date: November 12, 2025
"""

import sys
import json
from pathlib import Path
from collections import Counter

sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

print("="*80)
print("🔍 EXPANDED CORPUS VALIDATION")
print("="*80)
print()

# Load expanded corpus
EXPANDED_PATH = "knowledge_base/conversational_training_pairs_expanded_phase1.json"

print(f"📂 Loading expanded corpus: {EXPANDED_PATH}")
with open(EXPANDED_PATH) as f:
    expanded_data = json.load(f)

print(f"   ✅ Loaded successfully")
print()

# Validate structure
print("🔬 Validating Structure:")
print()

# Check metadata
metadata = expanded_data.get('metadata', {})
print(f"   Metadata:")
print(f"      Description: {metadata.get('description', 'MISSING')}")
print(f"      Version: {metadata.get('version', 'MISSING')}")
print(f"      Total pairs: {metadata.get('total_pairs', 'MISSING')}")
print(f"      Domains: {', '.join(metadata.get('domains', []))}")
print()

# Check training pairs
training_pairs = expanded_data.get('training_pairs', [])
print(f"   Training Pairs:")
print(f"      Count: {len(training_pairs)}")
print()

# Validate each pair has required fields
required_fields = ['input', 'output', 'category', 'domain']
optional_fields = ['self_zone', 'expected_organs', 'response_length']

print("   Validating pair structure...")
valid_pairs = 0
invalid_pairs = []

for i, pair in enumerate(training_pairs):
    # Check required fields
    missing_required = [f for f in required_fields if f not in pair]
    if missing_required:
        invalid_pairs.append((i, f"Missing required fields: {missing_required}"))
        continue

    # Check input/output not empty
    if not pair['input'] or not pair['output']:
        invalid_pairs.append((i, "Empty input or output"))
        continue

    valid_pairs += 1

print(f"      Valid pairs: {valid_pairs}/{len(training_pairs)}")
if invalid_pairs:
    print(f"      ❌ Invalid pairs found: {len(invalid_pairs)}")
    for idx, reason in invalid_pairs[:5]:  # Show first 5
        print(f"         Pair {idx}: {reason}")
else:
    print(f"      ✅ All pairs valid")
print()

# Domain distribution
print("📊 Domain Distribution:")
print()

domains = [pair['domain'] for pair in training_pairs if 'domain' in pair]
domain_counts = Counter(domains)

for domain, count in sorted(domain_counts.items()):
    percentage = (count / len(training_pairs)) * 100
    print(f"   {domain}: {count} pairs ({percentage:.1f}%)")
print()

# Category distribution (top 20)
print("🏷️  Category Distribution (top 20):")
print()

categories = [pair['category'] for pair in training_pairs if 'category' in pair]
category_counts = Counter(categories)

for i, (category, count) in enumerate(category_counts.most_common(20)):
    print(f"   {i+1}. {category}: {count}")
print()

# SELF Zone distribution
print("🧭 SELF Zone Distribution:")
print()

zones = [pair.get('self_zone') for pair in training_pairs if 'self_zone' in pair]
zone_counts = Counter(zones)

zone_names = {
    1: "Core SELF Orbit",
    2: "Creative Periphery",
    3: "Symbolic Threshold",
    4: "Shadow/Compost",
    5: "Exile/Collapse"
}

for zone in sorted(zone_counts.keys()):
    count = zone_counts[zone]
    percentage = (count / len(zones)) * 100
    zone_name = zone_names.get(zone, "Unknown")
    print(f"   Zone {zone} ({zone_name}): {count} pairs ({percentage:.1f}%)")
print()

# Response length distribution
print("📏 Response Length Distribution:")
print()

lengths = [pair.get('response_length') for pair in training_pairs if 'response_length' in pair]
length_counts = Counter(lengths)

for length, count in sorted(length_counts.items(), key=lambda x: ['minimal', 'brief', 'moderate', 'extended'].index(x[0]) if x[0] in ['minimal', 'brief', 'moderate', 'extended'] else 999):
    percentage = (count / len(lengths)) * 100
    print(f"   {length}: {count} pairs ({percentage:.1f}%)")
print()

# Organ signature distribution
print("🧬 Expected Organ Distribution:")
print()

all_organs = []
for pair in training_pairs:
    if 'expected_organs' in pair:
        all_organs.extend(pair['expected_organs'])

organ_counts = Counter(all_organs)

print(f"   Total organ mentions: {len(all_organs)}")
print(f"   Unique organs: {len(organ_counts)}")
print()

for organ, count in sorted(organ_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(all_organs)) * 100
    print(f"   {organ}: {count} mentions ({percentage:.1f}%)")
print()

# Compatibility test
print("🔧 Compatibility Testing:")
print()

print("   Testing with Arc-Inspired Trainer structure...")

# Check if structure matches existing corpus format
EXISTING_PATH = "knowledge_base/conversational_training_pairs_complete.json"
with open(EXISTING_PATH) as f:
    existing_data = json.load(f)

existing_pair = existing_data['training_pairs'][0]
expanded_pair = training_pairs[0]

existing_fields = set(existing_pair.keys())
expanded_fields = set(expanded_pair.keys())

print(f"      Existing corpus fields: {sorted(existing_fields)}")
print(f"      Expanded corpus fields: {sorted(expanded_fields)}")
print()

# Core fields required by arc trainer
core_fields = {'input', 'output', 'category'}
has_core = core_fields.issubset(expanded_fields)

print(f"      Core fields present: {has_core}")
if has_core:
    print(f"      ✅ Compatible with arc trainer")
else:
    print(f"      ❌ Missing core fields: {core_fields - expanded_fields}")
print()

# Additional fields (won't break compatibility)
additional_fields = expanded_fields - existing_fields
if additional_fields:
    print(f"      Additional fields in expanded corpus: {sorted(additional_fields)}")
    print(f"      ℹ️  These add metadata but won't break training")
print()

# Sample pair quality check
print("📝 Sample Pair Quality Check:")
print()

# Show 3 sample pairs from each domain
for domain in domain_counts.keys():
    domain_pairs = [p for p in training_pairs if p.get('domain') == domain]
    sample = domain_pairs[:3]

    print(f"   Domain: {domain}")
    print()

    for i, pair in enumerate(sample):
        print(f"      Sample {i+1}:")
        print(f"         Input: {pair['input'][:60]}...")
        print(f"         Output: {pair['output'][:60]}...")
        print(f"         Category: {pair['category']}")
        print(f"         Zone: {pair.get('self_zone', 'N/A')}")
        print(f"         Length: {pair.get('response_length', 'N/A')}")
        print()
    print()

# Final summary
print("="*80)
print("📊 VALIDATION SUMMARY")
print("="*80)
print()

issues = []

if invalid_pairs:
    issues.append(f"{len(invalid_pairs)} invalid pairs")

if not has_core:
    issues.append("Missing core fields")

if len(training_pairs) < metadata.get('total_pairs', 0):
    issues.append(f"Pair count mismatch: {len(training_pairs)} vs {metadata.get('total_pairs', 0)}")

if issues:
    print("❌ Issues Found:")
    for issue in issues:
        print(f"   - {issue}")
    print()
    print("   Recommendation: Fix issues before training")
else:
    print("✅ All Checks Passed!")
    print()
    print(f"   Total pairs: {len(training_pairs)}")
    print(f"   Domains: {len(domain_counts)}")
    print(f"   Categories: {len(category_counts)}")
    print(f"   Compatible with arc trainer: ✅")
    print()
    print("   Ready for training!")

print()
print("="*80)
