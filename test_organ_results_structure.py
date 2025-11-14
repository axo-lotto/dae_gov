#!/usr/bin/env python3
"""
Quick diagnostic: Check organ_results structure from wrapper.
"""

import sys
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

# Initialize wrapper (suppress verbose output)
import io
from contextlib import redirect_stdout

print("Initializing organism (output suppressed)...")
with redirect_stdout(io.StringIO()):
    wrapper = ConversationalOrganismWrapper()

print("\n=== Testing organ_results structure ===\n")

# Process simple input
print("Processing: 'I am feeling overwhelmed'")
result = wrapper.process_text('I am feeling overwhelmed', context={}, enable_phase2=True)

# Check organ_results
print("\n--- Result structure ---")
print(f"Result keys: {list(result.keys())}")

if 'organ_results' in result:
    print(f"\n✅ organ_results EXISTS")
    organ_results = result['organ_results']
    print(f"Type: {type(organ_results)}")

    if hasattr(organ_results, 'keys'):
        print(f"Organ count: {len(organ_results)}")
        print(f"Organs: {list(organ_results.keys())}")

        # Check first organ structure
        first_organ = list(organ_results.keys())[0]
        organ_data = organ_results[first_organ]
        print(f"\n--- First organ: {first_organ} ---")
        print(f"Type: {type(organ_data)}")
        print(f"Is dict: {isinstance(organ_data, dict)}")

        if isinstance(organ_data, dict):
            print(f"Dict keys: {list(organ_data.keys())[:10]}")
        else:
            print(f"Has __dict__: {hasattr(organ_data, '__dict__')}")
            if hasattr(organ_data, '__dict__'):
                print(f"Attributes: {list(organ_data.__dict__.keys())[:10]}")

        # Check if signature extractor can handle it
        print("\n--- Testing signature extraction ---")
        try:
            from persona_layer.organ_signature_extractor import OrganSignatureExtractor
            extractor = OrganSignatureExtractor()

            # Try extracting signature
            sig = extractor._extract_organ_signature(first_organ, organ_data)
            print(f"✅ Signature extraction WORKS")
            print(f"   Signature shape: {sig.shape}")
            print(f"   Sample values: {sig[:3]}")
        except Exception as e:
            print(f"❌ Signature extraction FAILED: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ organ_results is not a dict!")
else:
    print(f"❌ organ_results NOT in result!")

# Check if learning call would work
print("\n--- Testing learning call ---")
if 'organ_results' in result and hasattr(wrapper, 'phase5_learning'):
    try:
        # Create mock assembled response
        from dataclasses import dataclass

        @dataclass
        class MockResponse:
            text: str = result.get('emission_text', '')
            confidence: float = result.get('emission_confidence', 0.0)
            emission_path: str = result.get('emission_path', '')
            satisfaction: float = 0.85  # High satisfaction
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

        mock_response = MockResponse()

        # Try learning call
        learning_result = wrapper.phase5_learning.learn_from_conversation(
            organ_results=result['organ_results'],
            assembled_response=mock_response,
            user_message='I am feeling overwhelmed',
            conversation_id='test_diagnostic_001'
        )

        if learning_result:
            print(f"✅ Learning call SUCCEEDED!")
            print(f"   Family: {learning_result.get('family_id')}")
            print(f"   Is new: {learning_result.get('is_new_family')}")
            print(f"   Total families: {learning_result.get('total_families')}")
        else:
            print(f"⚠️  Learning call returned None (satisfaction too low?)")

    except Exception as e:
        print(f"❌ Learning call FAILED: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"⚠️  Cannot test learning (missing organ_results or phase5_learning)")

print("\n=== Diagnostic complete ===")
