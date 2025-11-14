#!/usr/bin/env python3
"""
Debug why learning call returns None despite high satisfaction.
"""

import sys
import io
from contextlib import redirect_stdout

sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

print("="*80)
print("🔍 DEBUG: Why Learning Returns None")
print("="*80)
print()

# Initialize
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("Initializing organism...")
with redirect_stdout(io.StringIO()):
    wrapper = ConversationalOrganismWrapper()

learning = wrapper.phase5_learning
print(f"✅ Learning enabled: {learning.enable_learning}")
print(f"✅ Learning threshold: {learning.learning_threshold}")
print()

# Process
result = wrapper.process_text('I am feeling overwhelmed', context={}, enable_phase2=True)
print(f"✅ Processing complete")
print()

# Create response
from dataclasses import dataclass

@dataclass
class MockResponse:
    text: str = result['emission_text']
    satisfaction: float = 0.85
    mean_satisfaction: float = 0.85  # Try both attributes
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

print("Mock response attributes:")
print(f"   satisfaction: {mock.satisfaction}")
print(f"   mean_satisfaction: {mock.mean_satisfaction}")
print(f"   text: {mock.text[:50]}...")
print()

# Add instrumentation
print("Calling learn_from_conversation with debug...")
print(f"   enable_learning: {learning.enable_learning}")
print()

# Check what satisfaction extraction does
satisfaction_score = getattr(mock, 'mean_satisfaction', None)
print(f"Step 1 - getattr(mock, 'mean_satisfaction', None): {satisfaction_score}")

if satisfaction_score is None:
    satisfaction_score = getattr(mock, 'satisfaction_score', None)
    print(f"Step 2 - getattr(mock, 'satisfaction_score', None): {satisfaction_score}")

if satisfaction_score is None:
    satisfaction_score = getattr(mock, 'satisfaction', None)
    print(f"Step 3 - getattr(mock, 'satisfaction', None): {satisfaction_score}")

print(f"Final satisfaction_score: {satisfaction_score}")
print(f"Threshold: {learning.learning_threshold}")
print(f"Passes threshold? {satisfaction_score >= learning.learning_threshold if satisfaction_score else False}")
print()

# Now try actual call
try:
    print("Attempting learning call...")
    report = learning.learn_from_conversation(
        organ_results=result['organ_results'],
        assembled_response=mock,
        user_message='I am feeling overwhelmed',
        conversation_id='debug_001'
    )

    if report:
        print(f"✅ LEARNING SUCCEEDED!")
        print(f"   {report}")
    else:
        print(f"❌ LEARNING RETURNED NONE")
        print()
        print("Debugging - check inside learn_from_conversation:")
        print("   1. Is enable_learning True?", learning.enable_learning)
        print("   2. What satisfaction value was extracted?")
        print("   3. Was threshold check passed?")
        print("   4. Did signature extraction fail?")

except Exception as e:
    print(f"❌ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*80)
