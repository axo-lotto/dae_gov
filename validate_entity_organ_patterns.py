"""
Entity-Organ Pattern Validation Script
======================================

Validates entity-organ associations learned during 50-epoch training.

Tests:
1. Cross-session consistency (same entity → similar organ pattern?)
2. Entity differentiation (Emma vs work → different signatures?)
3. Polyvagal state consistency (Emma → ventral, work → sympathetic?)
4. V0 energy patterns (safe entities → low V0, stress entities → high V0?)

Success Criteria:
- Cross-session consistency: R > 0.85
- Entity differentiation: Cosine distance > 0.4
- Polyvagal consistency: >85% matching expected state
- V0 energy accuracy: >80% within expected ranges

Usage:
    python validate_entity_organ_patterns.py
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
from scipy.stats import pearsonr
from scipy.spatial.distance import cosine

print("\n" + "="*80)
print("🔬 ENTITY-ORGAN PATTERN VALIDATION")
print("="*80 + "\n")

# Configuration
TRACKER_PATH = "persona_layer/state/active/entity_organ_associations.json"
RESULTS_PATH = "results/epochs/entity_situated_training_results.json"
CORPUS_PATH = "knowledge_base/entity_training/emiliano_entity_corpus.json"

# Expected patterns from corpus
EXPECTED_PATTERNS = {
    'Emma': {
        'organs': ['BOND', 'EMPATHY', 'PRESENCE'],
        'polyvagal': 'ventral',
        'v0_range': (0.0, 0.35),
        'entity_type': 'Person'
    },
    'Lily': {
        'organs': ['BOND', 'PRESENCE', 'EMPATHY'],
        'polyvagal': 'ventral',
        'v0_range': (0.0, 0.40),
        'entity_type': 'Person'
    },
    'Sofia': {
        'organs': ['EMPATHY', 'BOND', 'AUTHENTICITY'],
        'polyvagal': 'mixed',
        'v0_range': (0.30, 0.55),
        'entity_type': 'Person'
    },
    'work': {
        'organs': ['NDAM', 'AUTHENTICITY', 'SANS'],
        'polyvagal': 'sympathetic',
        'v0_range': (0.55, 0.85),
        'entity_type': 'Place'
    },
    'Alex': {
        'organs': ['NDAM', 'EMPATHY', 'AUTHENTICITY'],
        'polyvagal': 'sympathetic',
        'v0_range': (0.50, 0.75),
        'entity_type': 'Person'
    }
}

# Load data
print("📂 Loading data...")
try:
    with open(TRACKER_PATH, 'r') as f:
        tracker_data = json.load(f)
    print(f"   ✅ Loaded entity-organ tracker")
    print(f"      Entities tracked: {len(tracker_data.get('entity_metrics', {}))}")
except Exception as e:
    print(f"   ❌ Error loading tracker: {e}")
    tracker_data = {}

try:
    with open(RESULTS_PATH, 'r') as f:
        training_results = json.load(f)
    print(f"   ✅ Loaded training results")
    print(f"      Epochs completed: {len(training_results.get('epoch_results', []))}")
except Exception as e:
    print(f"   ❌ Error loading results: {e}")
    training_results = {}

try:
    with open(CORPUS_PATH, 'r') as f:
        corpus = json.load(f)
    print(f"   ✅ Loaded corpus")
    print(f"      Conversations: {len(corpus.get('conversations', []))}\n")
except Exception as e:
    print(f"   ❌ Error loading corpus: {e}")
    corpus = {}

# Extract entity metrics from tracker
entity_metrics = tracker_data.get('entity_metrics', {})

if not entity_metrics:
    print("⚠️  No entity metrics found in tracker. Training may not have completed.")
    print("   Expected file: persona_layer/state/active/entity_organ_associations.json")
    exit(1)

print(f"🔍 Entities tracked: {', '.join(entity_metrics.keys())}\n")

# ===== TEST 1: Cross-Session Consistency =====
print("="*80)
print("TEST 1: Cross-Session Consistency")
print("="*80)
print("Question: Does same entity → similar organ pattern across sessions?")
print("Method: Pearson correlation of organ vectors across epochs")
print("Target: R > 0.85\n")

# Extract organ patterns per entity per epoch
entity_epoch_patterns = defaultdict(lambda: defaultdict(list))

for epoch_result in training_results.get('epoch_results', []):
    epoch_num = epoch_result['epoch']
    for conv_result in epoch_result.get('conversation_results', []):
        entities = conv_result.get('expected_entities', [])
        organ_coherences = conv_result.get('organ_coherences', {})

        for entity in entities:
            # Store organ vector for this entity mention
            entity_epoch_patterns[entity][epoch_num].append(organ_coherences)

# Compute cross-session consistency per entity
consistency_results = {}
for entity, epoch_patterns in entity_epoch_patterns.items():
    # Get mean organ vector per epoch
    epoch_vectors = []
    epoch_nums = []

    for epoch_num, patterns in sorted(epoch_patterns.items()):
        if patterns:
            # Average across multiple mentions in same epoch
            mean_vector = {}
            all_organs = set()
            for pattern in patterns:
                all_organs.update(pattern.keys())

            for organ in all_organs:
                values = [p.get(organ, 0.0) for p in patterns]
                mean_vector[organ] = np.mean(values)

            epoch_vectors.append(mean_vector)
            epoch_nums.append(epoch_num)

    # Compute pairwise correlations
    if len(epoch_vectors) >= 2:
        correlations = []
        organ_names = sorted(epoch_vectors[0].keys())

        for i in range(len(epoch_vectors)):
            for j in range(i + 1, len(epoch_vectors)):
                vec_i = [epoch_vectors[i].get(organ, 0.0) for organ in organ_names]
                vec_j = [epoch_vectors[j].get(organ, 0.0) for organ in organ_names]

                if np.std(vec_i) > 0 and np.std(vec_j) > 0:
                    r, _ = pearsonr(vec_i, vec_j)
                    correlations.append(r)

        mean_consistency = np.mean(correlations) if correlations else 0.0
        consistency_results[entity] = {
            'mean_correlation': mean_consistency,
            'num_comparisons': len(correlations),
            'epochs_observed': len(epoch_vectors)
        }

# Report results
for entity, result in sorted(consistency_results.items(), key=lambda x: x[1]['mean_correlation'], reverse=True):
    r = result['mean_correlation']
    status = "✅" if r > 0.85 else "⚠️" if r > 0.70 else "❌"
    print(f"{status} {entity}: R = {r:.3f} (across {result['epochs_observed']} epochs, {result['num_comparisons']} comparisons)")

overall_consistency = np.mean([r['mean_correlation'] for r in consistency_results.values()])
print(f"\n📊 Overall Cross-Session Consistency: {overall_consistency:.3f}")
print(f"   Target: >0.85, Status: {'✅ PASS' if overall_consistency > 0.85 else '⚠️ MARGINAL' if overall_consistency > 0.70 else '❌ FAIL'}\n")

# ===== TEST 2: Entity Differentiation =====
print("="*80)
print("TEST 2: Entity Differentiation")
print("="*80)
print("Question: Are Emma and work organ signatures clearly different?")
print("Method: Cosine distance between organ vectors")
print("Target: Distance > 0.4\n")

# Get learned organ patterns from tracker
entity_organ_vectors = {}
for entity_name, metrics in entity_metrics.items():
    organ_boosts = metrics.get('organ_boosts', {})
    if organ_boosts:
        entity_organ_vectors[entity_name] = organ_boosts

# Compute pairwise distances
differentiation_results = []
safe_entities = ['Emma', 'Lily']
stress_entities = ['work', 'Alex']

for safe_entity in safe_entities:
    for stress_entity in stress_entities:
        if safe_entity in entity_organ_vectors and stress_entity in entity_organ_vectors:
            # Get organ vectors
            all_organs = set(entity_organ_vectors[safe_entity].keys()) | set(entity_organ_vectors[stress_entity].keys())
            vec_safe = [entity_organ_vectors[safe_entity].get(organ, 0.0) for organ in sorted(all_organs)]
            vec_stress = [entity_organ_vectors[stress_entity].get(organ, 0.0) for organ in sorted(all_organs)]

            # Compute cosine distance
            distance = cosine(vec_safe, vec_stress)

            status = "✅" if distance > 0.4 else "⚠️" if distance > 0.25 else "❌"
            print(f"{status} {safe_entity} vs {stress_entity}: distance = {distance:.3f}")
            differentiation_results.append(distance)

if differentiation_results:
    mean_differentiation = np.mean(differentiation_results)
    print(f"\n📊 Mean Entity Differentiation: {mean_differentiation:.3f}")
    print(f"   Target: >0.4, Status: {'✅ PASS' if mean_differentiation > 0.4 else '⚠️ MARGINAL' if mean_differentiation > 0.25 else '❌ FAIL'}\n")

# ===== TEST 3: Polyvagal State Consistency =====
print("="*80)
print("TEST 3: Polyvagal State Consistency")
print("="*80)
print("Question: Emma → ventral, work → sympathetic?")
print("Method: % of mentions matching expected polyvagal state")
print("Target: >85%\n")

# Extract polyvagal states from tracker
polyvagal_results = {}
for entity_name, expected in EXPECTED_PATTERNS.items():
    if entity_name in entity_metrics:
        learned_state = entity_metrics[entity_name].get('typical_polyvagal_state', 'unknown')
        expected_state = expected['polyvagal']

        match = learned_state == expected_state or (expected_state == 'mixed' and learned_state in ['ventral', 'sympathetic', 'mixed'])

        status = "✅" if match else "❌"
        print(f"{status} {entity_name}: expected={expected_state}, learned={learned_state}")
        polyvagal_results[entity_name] = match

polyvagal_accuracy = np.mean([1.0 if v else 0.0 for v in polyvagal_results.values()]) if polyvagal_results else 0.0
print(f"\n📊 Polyvagal State Accuracy: {polyvagal_accuracy*100:.1f}%")
print(f"   Target: >85%, Status: {'✅ PASS' if polyvagal_accuracy > 0.85 else '⚠️ MARGINAL' if polyvagal_accuracy > 0.70 else '❌ FAIL'}\n")

# ===== TEST 4: V0 Energy Patterns =====
print("="*80)
print("TEST 4: V0 Energy Patterns")
print("="*80)
print("Question: Safe entities → low V0, stress entities → high V0?")
print("Method: % of entities with V0 in expected range")
print("Target: >80%\n")

v0_results = {}
for entity_name, expected in EXPECTED_PATTERNS.items():
    if entity_name in entity_metrics:
        learned_v0 = entity_metrics[entity_name].get('typical_v0_energy', 0.5)
        expected_min, expected_max = expected['v0_range']

        in_range = expected_min <= learned_v0 <= expected_max

        status = "✅" if in_range else "❌"
        print(f"{status} {entity_name}: expected=[{expected_min:.2f}, {expected_max:.2f}], learned={learned_v0:.3f}")
        v0_results[entity_name] = in_range

v0_accuracy = np.mean([1.0 if v else 0.0 for v in v0_results.values()]) if v0_results else 0.0
print(f"\n📊 V0 Energy Accuracy: {v0_accuracy*100:.1f}%")
print(f"   Target: >80%, Status: {'✅ PASS' if v0_accuracy > 0.80 else '⚠️ MARGINAL' if v0_accuracy > 0.65 else '❌ FAIL'}\n")

# ===== OVERALL SUMMARY =====
print("="*80)
print("📊 OVERALL VALIDATION SUMMARY")
print("="*80 + "\n")

tests_passed = 0
total_tests = 4

print(f"Test 1 - Cross-Session Consistency: {overall_consistency:.3f} (target: >0.85)")
if overall_consistency > 0.85:
    print(f"   ✅ PASS")
    tests_passed += 1
elif overall_consistency > 0.70:
    print(f"   ⚠️  MARGINAL")
else:
    print(f"   ❌ FAIL")

if differentiation_results:
    print(f"\nTest 2 - Entity Differentiation: {mean_differentiation:.3f} (target: >0.4)")
    if mean_differentiation > 0.4:
        print(f"   ✅ PASS")
        tests_passed += 1
    elif mean_differentiation > 0.25:
        print(f"   ⚠️  MARGINAL")
    else:
        print(f"   ❌ FAIL")

print(f"\nTest 3 - Polyvagal Consistency: {polyvagal_accuracy*100:.1f}% (target: >85%)")
if polyvagal_accuracy > 0.85:
    print(f"   ✅ PASS")
    tests_passed += 1
elif polyvagal_accuracy > 0.70:
    print(f"   ⚠️  MARGINAL")
else:
    print(f"   ❌ FAIL")

print(f"\nTest 4 - V0 Energy Patterns: {v0_accuracy*100:.1f}% (target: >80%)")
if v0_accuracy > 0.80:
    print(f"   ✅ PASS")
    tests_passed += 1
elif v0_accuracy > 0.65:
    print(f"   ⚠️  MARGINAL")
else:
    print(f"   ❌ FAIL")

print(f"\n{'='*80}")
print(f"FINAL RESULT: {tests_passed}/{total_tests} tests passed")
if tests_passed == total_tests:
    print(f"🎉 ✅ ALL TESTS PASSED - Entity-organ associations successfully learned!")
elif tests_passed >= 3:
    print(f"⚠️  PARTIAL SUCCESS - Most patterns learned, some tuning needed")
else:
    print(f"❌ INSUFFICIENT LEARNING - May need more epochs or corpus refinement")
print(f"{'='*80}\n")

# ===== LEARNED PATTERNS REPORT =====
print("="*80)
print("🌀 LEARNED ENTITY-ORGAN PATTERNS")
print("="*80 + "\n")

for entity_name in sorted(entity_metrics.keys()):
    metrics = entity_metrics[entity_name]
    print(f"Entity: {entity_name}")
    print(f"  Type: {metrics.get('entity_type', 'Unknown')}")
    print(f"  Mentions: {metrics.get('mention_count', 0)}")
    print(f"  Polyvagal: {metrics.get('typical_polyvagal_state', 'unknown')}")
    print(f"  V0 Energy: {metrics.get('typical_v0_energy', 0.5):.3f}")
    print(f"  Urgency: {metrics.get('typical_urgency', 0.0):.3f}")
    print(f"  Success Rate: {metrics.get('success_rate', 0.0):.3f}")

    organ_boosts = metrics.get('organ_boosts', {})
    if organ_boosts:
        top_organs = sorted(organ_boosts.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"  Top Organs:")
        for organ, boost in top_organs:
            multiplier = 1.0 + boost / 0.5  # Assuming boost scale
            print(f"    - {organ}: {boost:.3f} (multiplier: {multiplier:.2f}×)")

    print()

print("="*80)
print("✅ Validation complete!")
print("="*80)
