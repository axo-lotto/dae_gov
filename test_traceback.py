#!/usr/bin/env python3
"""
Get full traceback for the Config error.
"""

import sys
import traceback
from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

try:
    print("Initializing organism...")
    organism = ConversationalOrganismWrapper()
except Exception as e:
    print(f"\n❌ FULL TRACEBACK:")
    traceback.print_exc()
    sys.exit(1)
