#!/usr/bin/env python3
"""
Test Meta-Commentary Fix
November 14, 2025

Verifies that organism no longer mentions internal processing
(organs, felt states, etc.) in emissions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper


def test_greeting_no_meta_commentary():
    """Test that greeting doesn't mention organs/processing."""
    print("=" * 80)
    print("TEST 1: Greeting - No Meta-Commentary")
    print("=" * 80)

    organism = ConversationalOrganismWrapper()

    context = {
        'stored_entities': {
            'user_name': 'Emiliano',
            'family_members': [],
            'friends': [],
            'preferences': {}
        },
        'username': 'Emiliano'
    }

    text = "Hello There! my name is Emiliano, nice to finally meet you"

    print(f"\n📥 Input: \"{text}\"")

    result = organism.process_text(
        text=text,
        context=context,
        enable_tsk_recording=False
    )

    emission = result['emission_text']
    print(f"\n📤 Emission: \"{emission}\"")

    # Check for meta-commentary patterns
    meta_patterns = [
        'organ',
        '11 organs',
        'consulted',
        'deliberating',
        'process thing',
        'getting familiar',
        'scent',
        'still working'
    ]

    found_meta = []
    for pattern in meta_patterns:
        if pattern.lower() in emission.lower():
            found_meta.append(pattern)

    if found_meta:
        print(f"\n❌ FAIL: Meta-commentary detected: {found_meta}")
        return False
    else:
        print(f"\n✅ PASS: No meta-commentary detected")
        return True


def test_name_recall_no_meta_commentary():
    """Test that name recall doesn't mention organs/processing."""
    print("\n\n" + "=" * 80)
    print("TEST 2: Name Recall - No Meta-Commentary")
    print("=" * 80)

    organism = ConversationalOrganismWrapper()

    context = {
        'stored_entities': {
            'user_name': 'Emiliano',
            'family_members': [],
            'friends': [],
            'preferences': {}
        },
        'username': 'Emiliano'
    }

    text = "Hello do you remember my name?"

    print(f"\n📥 Input: \"{text}\"")

    result = organism.process_text(
        text=text,
        context=context,
        enable_tsk_recording=False
    )

    emission = result['emission_text']
    print(f"\n📤 Emission: \"{emission}\"")

    # Check for meta-commentary patterns
    meta_patterns = [
        'organ',
        '11 organs',
        'consulted',
        'deliberating',
        'process thing',
        'still working'
    ]

    found_meta = []
    for pattern in meta_patterns:
        if pattern.lower() in emission.lower():
            found_meta.append(pattern)

    # Check if name is mentioned (should be)
    mentions_name = 'emiliano' in emission.lower()

    if found_meta:
        print(f"\n❌ FAIL: Meta-commentary detected: {found_meta}")
        return False
    elif not mentions_name:
        print(f"\n⚠️  WARNING: Name not mentioned (entity context may not be working)")
        return True  # Still pass - meta-commentary is the focus
    else:
        print(f"\n✅ PASS: No meta-commentary, name recalled correctly")
        return True


def test_prompt_building():
    """Test that prompt doesn't expose organs to LLM."""
    print("\n\n" + "=" * 80)
    print("TEST 3: Prompt Building - No Organ Exposure")
    print("=" * 80)

    from persona_layer.llm_felt_guidance import FeltGuidedLLMGenerator, FeltLures, LLMConstraints

    # Mock LLM bridge
    class MockLLMBridge:
        def query_direct(self, prompt, temperature=0.7, max_tokens=150):
            # Check if prompt exposes organs
            print(f"\n📄 Prompt excerpt:\n{prompt[:500]}...")

            if 'Dominant organs' in prompt or 'LISTENING' in prompt or 'EMPATHY' in prompt:
                print("\n❌ Prompt exposes organs!")
                return {'response': 'Test response', 'confidence': 0.7}
            else:
                print("\n✅ Prompt does NOT expose organs")
                return {'response': 'Test response', 'confidence': 0.7}

    llm_gen = FeltGuidedLLMGenerator(
        llm_bridge=MockLLMBridge(),
        enable_safety_gates=True,
        enable_emergent_personality=True
    )

    # Create mock felt lures
    lures = FeltLures(
        polyvagal_state='mixed_state',
        dominant_organs=['LISTENING', 'EMPATHY', 'WISDOM'],
        nexus_count=0,
        v0_energy=0.5,
        satisfaction=0.7
    )

    constraints = LLMConstraints(
        tone='warm',
        response_length='medium',
        empathy_level=0.8,
        groundedness=0.7
    )

    # Build prompt
    prompt = llm_gen.build_felt_prompt(
        user_input="Hello!",
        constraints=constraints,
        lures=lures,
        memory_context=None
    )

    # Check if prompt exposes organs
    if 'Dominant organs' in prompt:
        print(f"\n❌ FAIL: Prompt still exposes 'Dominant organs'")
        return False
    elif 'LISTENING' in prompt or 'EMPATHY' in prompt:
        print(f"\n❌ FAIL: Prompt still mentions specific organs")
        return False
    else:
        print(f"\n✅ PASS: Prompt uses implicit guidance only")
        return True


def main():
    """Run all meta-commentary tests."""
    print("\n🌀 Meta-Commentary Fix Verification")
    print("Testing that organism no longer mentions internal processing\n")

    results = []

    # Test 1: Greeting
    results.append(("Greeting", test_greeting_no_meta_commentary()))

    # Test 2: Name recall
    results.append(("Name Recall", test_name_recall_no_meta_commentary()))

    # Test 3: Prompt building
    results.append(("Prompt Building", test_prompt_building()))

    # Summary
    print("\n\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Meta-commentary fix is working.")
        print("\nExpected behavior:")
        print("  - Organism responds naturally, no organ mentions")
        print("  - Felt constraints guide tone/style implicitly")
        print("  - Entity context enables name recall")
    else:
        print("\n⚠️  Some tests failed. Check output above.")

    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
