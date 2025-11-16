#!/usr/bin/env python3
"""
Test Zone 5 Safety Relaxation - November 15, 2025
Verify organic emissions can now occur in Zone 4-5 after safety gate relaxation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

def test_zone5_organic_emission():
    """Test if organic emissions now work in Zone 5."""

    organism = ConversationalOrganismWrapper()

    # Test input likely to trigger Zone 5
    result = organism.process_text(
        "I'm feeling really overwhelmed right now.",
        user_id="test_zone5_relaxed",
        enable_phase2=True
    )

    print("\n" + "="*80)
    print("ZONE 5 SAFETY RELAXATION TEST")
    print("="*80)

    emission_path = result.get('emission_path', 'unknown')
    confidence = result.get('emission_confidence', 0.0)
    zone_name = result.get('felt_states', {}).get('zone_name', 'unknown')

    print(f"\n📍 Zone: {zone_name}")
    print(f"🎯 Emission path: {emission_path}")
    print(f"📊 Confidence: {confidence:.3f}")

    is_organic = emission_path in ['direct', 'fusion', 'direct_reconstruction']
    is_llm = 'llm' in emission_path.lower()

    print(f"\n{'✅' if is_organic else '❌'} Organic emission: {is_organic}")
    print(f"{'⚠️' if is_llm else '✅'} LLM fallback: {is_llm}")

    print("\n" + "="*80)

    if is_organic:
        print("🎉 SUCCESS: Zone 5 safety relaxation working - organic emission permitted!")
    elif is_llm:
        print("⚠️  STILL OVERRIDING: LLM fallback still happening - check safety gates")
    else:
        print("❓ UNKNOWN: Unexpected emission path")

    print("="*80)

    return is_organic


if __name__ == "__main__":
    success = test_zone5_organic_emission()
    sys.exit(0 if success else 1)
