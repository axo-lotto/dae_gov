#!/usr/bin/env python3
"""
Test Interactive Mode Quality - November 15, 2025
==================================================

Verify that interactive mode produces quality emissions with the new
INTELLIGENCE_EMERGENCE_MODE flag system.

Expected behavior:
- Config.INTELLIGENCE_EMERGENCE_MODE should be False (default)
- Emissions should use felt-guided LLM (high quality)
- Entity extraction should work
- Responses should be coherent and answer the question
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


def test_interactive_quality():
    """Test that interactive mode produces quality emissions."""

    print("=" * 80)
    print("🧪 INTERACTIVE MODE QUALITY TEST")
    print("=" * 80)

    # Verify default mode
    print(f"\n1️⃣ Checking INTELLIGENCE_EMERGENCE_MODE flag...")
    print(f"   Current value: {Config.INTELLIGENCE_EMERGENCE_MODE}")

    if Config.INTELLIGENCE_EMERGENCE_MODE:
        print(f"   ⚠️  WARNING: Flag is True - interactive mode will use organic emissions")
        print(f"   Expected: False (for quality felt-guided LLM)")
    else:
        print(f"   ✅ CORRECT: Flag is False (quality mode)")

    # Initialize organism (should NOT set the flag)
    print(f"\n2️⃣ Initializing organism...")
    organism = ConversationalOrganismWrapper()
    print(f"   ✅ Organism initialized")

    # Re-check flag after initialization
    print(f"\n3️⃣ Re-checking flag after initialization...")
    print(f"   Current value: {Config.INTELLIGENCE_EMERGENCE_MODE}")

    if Config.INTELLIGENCE_EMERGENCE_MODE:
        print(f"   ❌ FAIL: Flag was changed during initialization!")
        return False
    else:
        print(f"   ✅ PASS: Flag remains False")

    # Test with a real conversational input
    print(f"\n4️⃣ Testing with real input...")
    test_input = "I'm feeling really overwhelmed right now."
    print(f"   Input: \"{test_input}\"")

    result = organism.process_text(
        test_input,
        user_id="test_interactive_quality",
        enable_phase2=True
    )

    # Extract results (wrapper uses 'emission_text', 'emission_confidence', 'emission_path')
    emission = result.get('emission_text', 'ERROR: No emission')
    confidence = result.get('emission_confidence', 0.0)
    emission_path = result.get('emission_path', 'unknown')

    print(f"\n5️⃣ Analyzing results...")
    print(f"   Emission path: {emission_path}")
    print(f"   Confidence: {confidence:.3f}")
    print(f"   Emission length: {len(emission)} chars")
    print(f"\n   Emission preview:")
    print(f"   \"{emission[:200]}{'...' if len(emission) > 200 else ''}\"")

    # Quality checks
    print(f"\n6️⃣ Quality checks...")

    checks_passed = 0
    total_checks = 4

    # Check 1: Should use felt-guided LLM
    if emission_path == 'felt_guided_llm':
        print(f"   ✅ Using felt-guided LLM (quality mode)")
        checks_passed += 1
    else:
        print(f"   ⚠️  Using {emission_path} (expected felt_guided_llm)")

    # Check 2: Confidence should be reasonable
    if confidence >= 0.4:
        print(f"   ✅ Confidence adequate ({confidence:.3f} >= 0.4)")
        checks_passed += 1
    else:
        print(f"   ⚠️  Low confidence ({confidence:.3f} < 0.4)")

    # Check 3: Emission should be coherent (no asterisks/gibberish)
    if '*' not in emission and len(emission) > 20:
        print(f"   ✅ Emission coherent (no asterisks, substantial length)")
        checks_passed += 1
    else:
        print(f"   ⚠️  Emission may be malformed")

    # Check 4: Should not contain reconstruction artifacts
    reconstruction_artifacts = ['There\'s something important here', 'universe is experiencing']
    has_artifacts = any(artifact in emission for artifact in reconstruction_artifacts)
    if not has_artifacts:
        print(f"   ✅ No organic reconstruction artifacts")
        checks_passed += 1
    else:
        print(f"   ⚠️  Contains organic reconstruction artifacts")

    # Final assessment
    print(f"\n" + "=" * 80)
    print(f"📊 FINAL ASSESSMENT")
    print(f"=" * 80)
    print(f"   Checks passed: {checks_passed}/{total_checks}")

    if checks_passed == total_checks:
        print(f"\n   ✅ INTERACTIVE MODE QUALITY: EXCELLENT")
        print(f"   System producing high-quality felt-guided LLM emissions")
        return True
    elif checks_passed >= 3:
        print(f"\n   ⚠️  INTERACTIVE MODE QUALITY: GOOD")
        print(f"   Minor issues detected, but generally functional")
        return True
    else:
        print(f"\n   ❌ INTERACTIVE MODE QUALITY: POOR")
        print(f"   Significant issues detected")
        return False


if __name__ == "__main__":
    success = test_interactive_quality()
    sys.exit(0 if success else 1)
