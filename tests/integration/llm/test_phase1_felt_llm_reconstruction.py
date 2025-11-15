"""
Test Phase 1: Felt-Guided LLM Replacing Phrase-Based Reconstruction
==================================================================

Tests that the reconstruction pipeline uses felt-guided LLM instead of
meta-atom phrase selection when nexuses form.

User's example input: "Hello there i am feeling good today!"
Expected: Natural language response, NO "The past is alive here", NO 🌀🍄

Date: November 13, 2025
"""

import sys
import os

# Set PYTHONPATH
sys.path.insert(0, '/Users/daedalea/Desktop/DAE_HYPHAE_1')
os.environ['PYTHONPATH'] = '/Users/daedalea/Desktop/DAE_HYPHAE_1:' + os.environ.get('PYTHONPATH', '')

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config

def test_user_example_no_process_language():
    """
    Test user's exact example: 'Hello there i am feeling good today!'

    Expected behavior:
    - Natural conversational response
    - NO Whiteheadian phrases ("The past is alive here")
    - NO random emojis (🌀🍄)
    - Felt-guided LLM should be triggered
    """
    print("=" * 80)
    print("TEST: User Example - 'Hello there i am feeling good today!'")
    print("=" * 80)

    # Verify felt-guided LLM is enabled
    print(f"\nConfig check:")
    print(f"  LOCAL_LLM_ENABLED: {Config.LOCAL_LLM_ENABLED}")
    print(f"  FELT_GUIDED_LLM_ENABLED: {Config.FELT_GUIDED_LLM_ENABLED}")
    print(f"  HYBRID_ENABLED: {Config.HYBRID_ENABLED}")

    if not Config.LOCAL_LLM_ENABLED or not Config.FELT_GUIDED_LLM_ENABLED:
        print("\n❌ SKIPPING: Felt-guided LLM not enabled in config")
        print("   Set LOCAL_LLM_ENABLED=True and FELT_GUIDED_LLM_ENABLED=True in config.py")
        return

    # Initialize organism
    print("\n📦 Initializing organism...")
    try:
        organism = ConversationalOrganismWrapper(
            bundle_path="Bundle/test_felt_llm"
        )
    except Exception as e:
        print(f"\n❌ Failed to initialize organism: {e}")
        print(f"   Make sure Ollama is running: ps aux | grep ollama")
        import traceback
        traceback.print_exc()
        return

    print("✅ Organism initialized")

    # Test input
    user_input = "Hello there i am feeling good today!"

    print(f"\n💬 User input: '{user_input}'")
    print("\n🔄 Processing...")

    # Process input
    try:
        result = organism.process_text(user_input)
    except Exception as e:
        print(f"\n❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Extract results
    emission = result.get('emission', '')
    confidence = result.get('emission_confidence', 0.0)
    path = result.get('emission_path', 'unknown')

    print(f"\n📝 Results:")
    print(f"   Emission (full): '{emission}'")
    print(f"   Emission length: {len(emission)} chars")
    print(f"   Confidence: {confidence:.3f}")
    print(f"   Path: {path}")

    # Validation checks
    print(f"\n✅ Validation:")

    # Check 1: No Whiteheadian process language
    process_phrases = [
        "The past is alive here",
        "occasions prehended",
        "influence flows",
        "actual occasions",
        "concrescence",
        "subjective aim"
    ]

    has_process_language = any(phrase in emission for phrase in process_phrases)
    if has_process_language:
        print(f"   ❌ FAIL: Process-aware language detected!")
        for phrase in process_phrases:
            if phrase in emission:
                print(f"      Found: '{phrase}'")
    else:
        print(f"   ✅ PASS: No process-aware language")

    # Check 2: No random emojis
    random_emojis = ['🌀', '🍄']
    has_random_emojis = any(emoji in emission for emoji in random_emojis)
    if has_random_emojis:
        print(f"   ❌ FAIL: Random emojis detected: {[e for e in random_emojis if e in emission]}")
    else:
        print(f"   ✅ PASS: No random emojis")

    # Check 3: Felt-guided LLM was used
    if path == 'felt_guided_llm':
        print(f"   ✅ PASS: Felt-guided LLM path used")
    else:
        print(f"   ⚠️  WARNING: Unexpected path '{path}' (expected 'felt_guided_llm')")

    # Check 4: Natural conversational response
    if len(emission) > 0 and not has_process_language:
        print(f"   ✅ PASS: Natural language response generated")
    else:
        print(f"   ❌ FAIL: Response not natural or empty")

    # Overall result
    print(f"\n{'='*80}")
    if not has_process_language and not has_random_emojis and path == 'felt_guided_llm':
        print("🎉 SUCCESS: Phase 1 working! Natural language, no process phrases, no emojis!")
    else:
        print("❌ FAILURE: Phase 1 not fully working")
    print(f"{'='*80}")

if __name__ == '__main__':
    test_user_example_no_process_language()
