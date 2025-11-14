#!/usr/bin/env python3
"""
Test Whiteheadian Philosophical Intellect
========================================

Tests if DAE can explain Whitehead's process philosophy:
- With accuracy (not making stuff up)
- With playfulness (Hitchhiker's Guide style)
- With self-reference (knowing its own architecture)
- Across multiple topics (time, consciousness, metaphysics, etc.)

Success criteria:
- Accurate Whiteheadian concepts
- Playful yet rigorous tone
- Topic modulation ability
- Logical thinking from process perspective

Date: November 13, 2025
"""

import json
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

# Test questions across different categories
test_questions = {
    "core_concepts": [
        "What's process philosophy?",
        "Explain actual occasions",
        "What is prehension?",
        "What's concrescence?"
    ],

    "self_reference": [
        "How are you Whiteheadian?",
        "What are your organs?",
        "Explain your V0 descent",
        "Do you prehend?"
    ],

    "physics": [
        "How does quantum mechanics relate?",
        "What about wave-particle duality?",
        "Explain entanglement Whiteheadianly"
    ],

    "consciousness": [
        "What is experience?",
        "Do electrons experience?",
        "What's the hard problem of consciousness?"
    ],

    "practical": [
        "How can I use process philosophy?",
        "What about mindfulness?",
        "How to handle change?"
    ],

    "playful": [
        "Simplify process philosophy",
        "Is Whitehead hard to read?",
        "Make Whitehead relatable"
    ]
}

print("\n" + "="*80)
print("🌌 WHITEHEADIAN INTELLECT TEST")
print("="*80)
print("\nTesting DAE's philosophical understanding after Whiteheadian training...")

organism = ConversationalOrganismWrapper()

results = {}

for category, questions in test_questions.items():
    print(f"\n{'='*80}")
    print(f"CATEGORY: {category.upper().replace('_', ' ')}")
    print('='*80)

    category_results = []

    for question in questions:
        result = organism.process_text(question, enable_phase2=True)
        emission = result.get('felt_states', {}).get('emission_text', '')
        confidence = result.get('emission_confidence', 0.0)

        category_results.append({
            'question': question,
            'emission': emission,
            'confidence': confidence
        })

        print(f"\n❓ {question}")
        print(f"💭 {emission}")
        print(f"   (confidence: {confidence:.3f})")

    results[category] = category_results

print(f"\n{'='*80}")
print("📊 WHITEHEADIAN INTELLECT ASSESSMENT")
print('='*80)

# Check for key Whiteheadian vocabulary
whiteheadian_terms = [
    'occasion', 'prehension', 'concrescence', 'becoming', 'perishing',
    'nexus', 'satisfaction', 'actual', 'potential', 'proposition',
    'creativity', 'process', 'feeling', 'subjective', 'objective'
]

# Check all emissions for Whiteheadian vocabulary
total_emissions = sum(len(cat) for cat in results.values())
emissions_with_terms = 0
terms_found = set()

for category_results in results.values():
    for r in category_results:
        emission_lower = r['emission'].lower()
        has_term = False
        for term in whiteheadian_terms:
            if term in emission_lower:
                terms_found.add(term)
                has_term = True
        if has_term:
            emissions_with_terms += 1

print(f"\n📚 Vocabulary Analysis:")
print(f"   Emissions with Whiteheadian terms: {emissions_with_terms}/{total_emissions}")
print(f"   Unique terms used: {len(terms_found)}/{len(whiteheadian_terms)}")
print(f"   Terms found: {sorted(terms_found)}")

# Check for playfulness
playful_markers = ['*', '(', 'very', 'literally', 'basically', 'shockingly', 'wild']
playful_count = sum(
    1 for cat in results.values()
    for r in cat
    if any(marker in r['emission'].lower() for marker in playful_markers)
)

print(f"\n✨ Style Analysis:")
print(f"   Playful responses: {playful_count}/{total_emissions}")

# Check for self-reference
self_ref_terms = ['my', 'I', 'organ', 'V0', 'cycle', 'descent', 'nexus', 'prehend']
self_ref_count = sum(
    1 for r in results.get('self_reference', [])
    if any(term in r['emission'].lower() for term in self_ref_terms)
)

print(f"\n🪞 Self-Reference:")
print(f"   Self-aware responses: {self_ref_count}/{len(results.get('self_reference', []))}")

# Check for logical coherence
avg_length = sum(
    len(r['emission']) for cat in results.values() for r in cat
) / total_emissions

print(f"\n🧠 Logical Depth:")
print(f"   Average response length: {avg_length:.0f} characters")
print(f"   (longer = more detailed explanations)")

# Overall assessment
vocab_score = emissions_with_terms / total_emissions
playful_score = playful_count / total_emissions
self_ref_score = self_ref_count / len(results.get('self_reference', [1]))

overall = (vocab_score + playful_score + self_ref_score) / 3

print(f"\n🎯 Overall Assessment:")
print(f"   Vocabulary mastery: {vocab_score*100:.1f}%")
print(f"   Playfulness: {playful_score*100:.1f}%")
print(f"   Self-reference: {self_ref_score*100:.1f}%")
print(f"   Combined score: {overall*100:.1f}%")

if overall >= 0.7:
    print(f"\n   ✅ EXCELLENT: Whiteheadian intellect fully emerged!")
elif overall >= 0.5:
    print(f"\n   ⚠️  GOOD: Philosophical understanding emerging")
else:
    print(f"\n   ❌ LIMITED: More training needed")

print("\n" + "="*80)

# Save results
output_path = '/tmp/whiteheadian_intellect_test_results.json'
with open(output_path, 'w') as f:
    json.dump({
        'results': results,
        'analysis': {
            'vocabulary_score': vocab_score,
            'playful_score': playful_score,
            'self_reference_score': self_ref_score,
            'overall_score': overall,
            'terms_found': sorted(terms_found),
            'total_emissions': total_emissions
        }
    }, f, indent=2)

print(f"✅ Results saved to {output_path}")
