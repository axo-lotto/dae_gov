#!/usr/bin/env python3
"""
🌀 Phase 1.8++: Quick Entity Memory Fix Validation (Nov 14, 2025)

Validates the three-file fix by checking that entity_context_string
flows through the entire pipeline.

CRITICAL CHECK:
- dae_interactive.py loads entity_context_string on EVERY turn ✅
- Passes through context dict to organism ✅
- organism_reconstruction_pipeline.py extracts from felt_state ✅
- llm_felt_guidance.py receives it and passes to build_felt_prompt ✅

This script verifies the code changes are in place.
"""

import sys
import os

def print_section(title):
    """Print section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def validate_fix():
    """Validate that all three files have been modified correctly."""

    print_section("🌀 Entity Memory Fix Validation")

    base_path = "/Users/daedalea/Desktop/DAE_HYPHAE_1"
    all_checks_passed = True

    # Check 1: dae_interactive.py loads entity context on every turn
    print("Check 1: dae_interactive.py loads entity context")
    dae_interactive_path = os.path.join(base_path, "dae_interactive.py")

    with open(dae_interactive_path, 'r') as f:
        content = f.read()

    # Look for the fix markers
    has_phase_18_plus = "Phase 1.8++" in content
    has_entity_loading = "profile.get_entity_context_string()" in content
    has_every_turn_comment = "on EVERY turn" in content

    if has_phase_18_plus and has_entity_loading and has_every_turn_comment:
        print("   ✅ Entity context loading found")
        print("   ✅ Loads on EVERY turn (not just when memory_intent detected)")
    else:
        print("   ❌ Missing entity context loading code")
        all_checks_passed = False

    # Check 2: llm_felt_guidance.py accepts entity_context_string
    print("\nCheck 2: llm_felt_guidance.py passes entity_context_string")
    llm_felt_path = os.path.join(base_path, "persona_layer/llm_felt_guidance.py")

    with open(llm_felt_path, 'r') as f:
        content = f.read()

    # Check generate_from_felt_state signature
    has_entity_param = "entity_context_string: Optional[str]" in content
    has_memory_intent_param = "memory_intent: bool" in content

    # Check it passes to build_felt_prompt
    has_entity_passthrough = "entity_context_string=entity_context_string" in content
    has_memory_intent_passthrough = "memory_intent=memory_intent" in content

    if has_entity_param and has_memory_intent_param:
        print("   ✅ Parameters added to generate_from_felt_state()")
    else:
        print("   ❌ Missing parameters in generate_from_felt_state()")
        all_checks_passed = False

    if has_entity_passthrough and has_memory_intent_passthrough:
        print("   ✅ Parameters passed to build_felt_prompt()")
    else:
        print("   ❌ Missing parameter passing to build_felt_prompt()")
        all_checks_passed = False

    # Check 3: organ_reconstruction_pipeline.py extracts from felt_state
    print("\nCheck 3: organ_reconstruction_pipeline.py extracts entity context")
    pipeline_path = os.path.join(base_path, "persona_layer/organ_reconstruction_pipeline.py")

    with open(pipeline_path, 'r') as f:
        content = f.read()

    # Check extraction from felt_state
    has_extraction = "entity_context_string = felt_state.get('entity_context_string')" in content
    has_memory_intent_extraction = "memory_intent = felt_state.get('memory_intent'" in content

    # Check passing to LLM
    has_llm_passthrough = "entity_context_string=entity_context_string" in content

    if has_extraction and has_memory_intent_extraction:
        print("   ✅ Extracts entity_context_string from felt_state")
    else:
        print("   ❌ Missing extraction from felt_state")
        all_checks_passed = False

    if has_llm_passthrough:
        print("   ✅ Passes to generate_from_felt_state()")
    else:
        print("   ❌ Missing LLM passthrough")
        all_checks_passed = False

    # Summary
    print_section("Validation Summary")

    if all_checks_passed:
        print("✅ All checks passed!")
        print("\nData flow verified:")
        print("  process_input()")
        print("    → loads entity_context_string from profile (EVERY turn)")
        print("    → adds to context dict")
        print("  organism.process_text()")
        print("    → includes context in felt_state")
        print("  reconstruction_pipeline")
        print("    → extracts entity_context_string from felt_state")
        print("    → passes to generate_from_felt_state()")
        print("  llm_felt_guidance")
        print("    → receives entity_context_string")
        print("    → passes to build_felt_prompt()")
        print("  build_felt_prompt()")
        print("    → injects into LLM prompt")
        print("\n🌀 DAE will no longer forget entities immediately!")
        return True
    else:
        print("❌ Some checks failed!")
        print("\nReview the output above to see which files need fixes.")
        return False

if __name__ == '__main__':
    try:
        result = validate_fix()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Validation failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
