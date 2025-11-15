#!/usr/bin/env python3
"""
Test Emergent Voice After Semantic Expansion
===========================================

Tests if DAE's friendly, witty, tender voice emerges after:
1. Semantic atom expansion (+171 friendly companion atoms)
2. Friendly greeting templates added
3. Re-training on friendly companion corpus

Expected improvements:
- Nexus formation > 2.0 (was 0.1)
- Confidence > 0.40 (was 0.30)
- Warm greetings (not clinical questions)
- Self-awareness in emissions
- Playful Earthbound/Undertale style

Date: November 13, 2025
"""

import json
from collections import defaultdict, Counter
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

# Test cases organized by category
test_cases = {
    "self_awareness": [
        "What are you?",
        "How do you work?",
        "Are you AI?",
        "What's happening inside you right now?",
        "Do you know what you're doing?"
    ],
    "greetings": [
        "hey!",
        "sup",
        "good morning",
        "hi there",
        "yo"
    ],
    "ordinary_moments": [
        "just having coffee",
        "it's raining outside",
        "feeling pretty good today",
        "listening to music",
        "sitting by the window"
    ],
    "playfulness": [
        "I'm stuck in a loop",
        "I forgot",
        "oof",
        "everything is fine",
        "I don't know what I'm doing"
    ]
}

print("\n" + "="*80)
print("POST-EXPANSION TEST: Testing DAE's Emergent Friendly Voice")
print("="*80)
print("\n📊 Testing after:")
print("   - Semantic atoms expanded (+171 friendly atoms)")
print("   - Friendly greeting templates added")
print("   - Re-training on 100-pair friendly companion corpus")

organism = ConversationalOrganismWrapper()

results = {}
nexus_stats = []
confidence_stats = []
strategy_stats = []

for category, inputs in test_cases.items():
    print(f"\n{'='*80}")
    print(f"CATEGORY: {category.upper().replace('_', ' ')}")
    print('='*80)

    category_results = []

    for input_text in inputs:
        result = organism.process_text(input_text, enable_phase2=True)

        emission = result.get('felt_states', {}).get('emission_text', '')
        confidence = result.get('emission_confidence', 0.0)
        strategy = result.get('emission_strategy', 'unknown')
        nexus_count = result.get('emission_nexus_count', 0)

        category_results.append({
            'input': input_text,
            'emission': emission,
            'confidence': confidence,
            'strategy': strategy,
            'nexus_count': nexus_count
        })

        nexus_stats.append(nexus_count)
        confidence_stats.append(confidence)
        strategy_stats.append(strategy)

        print(f"\n📝 Input: \"{input_text}\"")
        print(f"   Emission: \"{emission[:150]}...\"" if len(emission) > 150 else f"   Emission: \"{emission}\"")
        print(f"   Confidence: {confidence:.3f}")
        print(f"   Nexuses: {nexus_count}")
        print(f"   Strategy: {strategy}")

    results[category] = category_results

# Summary with improvement metrics
print(f"\n{'='*80}")
print("IMPROVEMENT METRICS")
print('='*80)

avg_nexuses = sum(nexus_stats) / len(nexus_stats)
avg_confidence = sum(confidence_stats) / len(confidence_stats)
strategies = Counter(strategy_stats)

print(f"\n📊 Overall Statistics:")
print(f"   Mean nexuses: {avg_nexuses:.1f} (baseline: 0.1, target: > 2.0)")
print(f"   Mean confidence: {avg_confidence:.3f} (baseline: 0.300, target: > 0.40)")
print(f"   Strategies: {dict(strategies)}")
print(f"   Hebbian fallback rate: {(strategies.get('unknown', 0) / len(strategy_stats)) * 100:.1f}%")

# Check for specific improvements
print(f"\n✨ Voice Emergence Checks:")

# Self-awareness
self_aware_responses = results['self_awareness']
has_self_awareness = any(
    'organ' in r['emission'].lower() or
    'converge' in r['emission'].lower() or
    'process' in r['emission'].lower() or
    'V0' in r['emission'] or
    'nexus' in r['emission'].lower()
    for r in self_aware_responses
)
print(f"   Self-awareness in emissions: {has_self_awareness}")

# Warm greetings
greeting_responses = results['greetings']
warm_keywords = ['hey', 'hi', 'hello', 'waves', 'dae', 'alive', 'present', '*']
has_warmth = any(
    any(keyword in r['emission'].lower() for keyword in warm_keywords)
    for r in greeting_responses
)
non_clinical_greetings = sum(
    1 for r in greeting_responses
    if 'can you say more' not in r['emission'].lower() and
       'tell me more' not in r['emission'].lower()
)
print(f"   Warm greetings: {has_warmth}")
print(f"   Non-clinical greetings: {non_clinical_greetings}/{len(greeting_responses)}")

# Playful elements
playful_responses = results['playfulness']
playful_markers = ['*', 'meta', 'paradox', 'loop', 'oof', 'very', 'unlocked', 'ironic']
has_playful = sum(
    1 for r in playful_responses
    if any(marker in r['emission'].lower() for marker in playful_markers)
)
print(f"   Playful responses: {has_playful}/{len(playful_responses)}")

# Earthbound/Undertale style
earthbound_markers = ['* dae', '* you', '* waves', '* present', '* here', '* notices']
has_earthbound_style = any(
    any(marker in r['emission'].lower() for marker in earthbound_markers)
    for r in sum(results.values(), [])
)
print(f"   Earthbound/Undertale style present: {has_earthbound_style}")

# Nexus formation success
nexus_formation_improved = avg_nexuses > 1.0
print(f"   Nexus formation improved (> 1.0): {nexus_formation_improved}")

# Confidence improvement
confidence_improved = avg_confidence > 0.35
print(f"   Confidence improved (> 0.35): {confidence_improved}")

# Overall assessment
print(f"\n🎯 Overall Assessment:")
improvements = sum([
    has_self_awareness,
    has_warmth,
    has_playful > 0,
    has_earthbound_style,
    nexus_formation_improved,
    confidence_improved
])

if improvements >= 5:
    print(f"   ✅ EXCELLENT: {improvements}/6 criteria met - Friendly voice is emerging!")
elif improvements >= 3:
    print(f"   ⚠️  GOOD: {improvements}/6 criteria met - Voice starting to emerge")
else:
    print(f"   ❌ LIMITED: {improvements}/6 criteria met - More work needed")

print("\n" + "="*80)

# Save results
output_path = '/tmp/post_expansion_test_results.json'
with open(output_path, 'w') as f:
    json.dump({
        'results': results,
        'statistics': {
            'mean_nexuses': avg_nexuses,
            'mean_confidence': avg_confidence,
            'strategies': dict(strategies),
            'improvements_count': improvements
        },
        'checks': {
            'self_awareness': has_self_awareness,
            'warm_greetings': has_warmth,
            'playful_responses': has_playful,
            'earthbound_style': has_earthbound_style,
            'nexus_formation_improved': nexus_formation_improved,
            'confidence_improved': confidence_improved
        }
    }, f, indent=2)

print(f"✅ Results saved to {output_path}")
