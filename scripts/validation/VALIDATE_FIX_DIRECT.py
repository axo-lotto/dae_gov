#!/usr/bin/env python3
"""
Direct validation - test through phase5 learning (not manual extraction).
"""

import sys
import io
from contextlib import redirect_stdout

sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

print("="*80)
print("🧪 DIRECT VALIDATION: Testing Through Phase5 Learning")
print("="*80)
print()

# Initialize organism
print("Initializing organism...")
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

with redirect_stdout(io.StringIO()):
    wrapper = ConversationalOrganismWrapper()

print(f"✅ Organism initialized")
print(f"   Starting families: {len(wrapper.phase5_learning.families.families)}")
print()

# Process text
print("Processing: 'I am feeling overwhelmed'")
result = wrapper.process_text('I am feeling overwhelmed', context={}, enable_phase2=True)
print(f"✅ Processing complete")
print(f"   Emission: {result['emission_text'][:50]}...")
print()

# Try learning (THIS is where conversion happens)
print("Testing learning call (with conversion)...")
from dataclasses import dataclass

@dataclass
class MockResponse:
    text: str = result['emission_text']
    satisfaction: float = 0.85
    mean_coherence: float = 0.75
    mean_confidence: float = 0.75
    num_phrases: int = 2
    strategies_used: list = None
    field_types: list = None

    def __post_init__(self):
        if self.strategies_used is None:
            self.strategies_used = ['direct']
        if self.field_types is None:
            self.field_types = ['action']

mock = MockResponse()

try:
    # This should use recursive conversion internally
    report = wrapper.phase5_learning.learn_from_conversation(
        organ_results=result['organ_results'],  # Dataclass objects
        assembled_response=mock,
        user_message='I am feeling overwhelmed',
        conversation_id='direct_validation_001'
    )

    if report:
        print(f"✅ LEARNING SUCCEEDED!")
        print(f"   Family: {report['family_id']}")
        print(f"   Is new: {report['is_new_family']}")
        print(f"   Total families: {report['total_families']}")
        print()
        print("="*80)
        print("🎉 FIX VALIDATED - Learning works with dataclass objects!")
        print("="*80)
    else:
        print(f"⚠️  Learning returned None")
        print(f"   Satisfaction: {mock.satisfaction}")
        print(f"   Threshold: {wrapper.phase5_learning.learning_threshold}")
        print()
        print("This may be expected if satisfaction is below threshold")

except Exception as e:
    print(f"❌ LEARNING FAILED: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("="*80)
    print("🔴 FIX NOT WORKING - Check recursive conversion")
    print("="*80)
    sys.exit(1)

# Quick 10-arc test
print("\n" + "="*80)
print("🧪 Quick 10-Arc Test")
print("="*80)

try:
    import json
    from persona_layer.arc_inspired_trainer import ArcInspiredTrainer

    # Load corpus
    with open('/Users/daedalea/Desktop/DAE_HYPHAE_1/knowledge_base/conversational_training_pairs_v4_319.json') as f:
        data = json.load(f)
        pairs = data['training_pairs']

    print(f"   Corpus: {len(pairs)} pairs")

    # Fresh organism
    with redirect_stdout(io.StringIO()):
        fresh_wrapper = ConversationalOrganismWrapper()

    families_start = len(fresh_wrapper.phase5_learning.families.families)
    print(f"   Starting families: {families_start}")

    # Arc trainer
    trainer = ArcInspiredTrainer(
        organism_wrapper=fresh_wrapper,
        training_pairs=pairs,
        enable_learning=True,
        assessment_threshold=0.50
    )

    # Run 10 arcs
    print("   Running 10 arcs...")
    for i in range(10):
        trainer.train_arc(verbose=False)
        if (i+1) % 5 == 0:
            fam_count = len(fresh_wrapper.phase5_learning.families.families)
            print(f"      Arc {i+1}: {fam_count} families")

    families_end = len(fresh_wrapper.phase5_learning.families.families)
    print(f"\n   Final families: {families_end} (+{families_end - families_start})")

    if families_end > families_start:
        print(f"   🎉 SUCCESS: {families_end - families_start} families created!")
    else:
        print(f"   ⚠️  No new families yet (may need more arcs)")

except Exception as e:
    print(f"   ❌ Arc test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✅ VALIDATION COMPLETE")
print("="*80)
