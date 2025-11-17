#!/usr/bin/env python3
"""
Test script to reproduce the Config error in interactive mode.
"""

import sys
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

print("Initializing organism...")
organism = ConversationalOrganismWrapper()
print(f"Organism created: {organism}")
print(f"Emission generator: {organism.emission_generator}")

if organism.emission_generator:
    print("\n✅ Emission generator initialized successfully")

    # Try to process text like interactive mode does
    print("\nProcessing test input...")
    try:
        result = organism.process_text(
            "I'm feeling overwhelmed",
            context={},
            enable_tsk_recording=False,
            enable_phase2=True,
            user_id="test_user",
            username="Test User"
        )
        print(f"✅ Processing successful")
        print(f"Emission: {result.get('emission', 'None')}")
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n❌ Emission generator is None!")
    sys.exit(1)
