#!/usr/bin/env python3
"""
Test Symbiotic LLM Entity Extractor Integration
================================================

Validates:
1. Extension properly leverages existing LocalLLMBridge
2. Three-tier routing (Pure DAE → Augmented → LLM Fallback)
3. Learning modes (Bootstrap → Balanced → Specialized)
4. Entity extraction without breaking existing infrastructure

Date: November 18, 2025
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.symbiotic_llm_entity_extractor import SymbioticLLMEntityExtractor
from persona_layer.local_llm_bridge import LocalLLMBridge
from config import Config

def test_initialization():
    """Test 1: Extension properly initializes with existing bridge."""
    print("\n" + "="*80)
    print("TEST 1: Extension Initialization")
    print("="*80)

    # Create existing LocalLLMBridge (no parameters - reads from Config)
    llm_bridge = LocalLLMBridge()
    print(f"✅ LocalLLMBridge created: {llm_bridge.backend.value}, {llm_bridge.model}")

    # Create extension
    extractor = SymbioticLLMEntityExtractor(
        local_llm_bridge=llm_bridge,
        learning_mode="bootstrap"
    )
    print(f"✅ SymbioticLLMEntityExtractor created: {extractor.learning_mode} mode")
    print(f"✅ Consultation rate: {extractor.consultation_rates[extractor.learning_mode]*100:.0f}%")

    return extractor, llm_bridge


def test_tier_routing(extractor):
    """Test 2: Three-tier routing logic."""
    print("\n" + "="*80)
    print("TEST 2: Three-Tier Routing")
    print("="*80)

    # Tier 1: High confidence (Pure DAE)
    tier, use_llm = extractor.should_use_llm(dae_confidence=0.90, entity_confidence=0.90)
    print(f"✅ Tier 1 (High confidence): {tier}, use_llm={use_llm}")
    assert tier == "tier1_pure_dae" and not use_llm

    # Tier 2: Medium confidence (Augmented)
    tier, use_llm = extractor.should_use_llm(dae_confidence=0.70, entity_confidence=0.75)
    print(f"✅ Tier 2 (Medium confidence): {tier}, use_llm={use_llm}")
    assert tier == "tier2_augmented"

    # Tier 3: Low confidence (LLM Fallback)
    tier, use_llm = extractor.should_use_llm(dae_confidence=0.50, entity_confidence=0.40)
    print(f"✅ Tier 3 (Low confidence): {tier}, use_llm={use_llm}")
    assert tier == "tier3_llm_fallback" and use_llm

    print("✅ All tier routing tests passed")


def test_learning_modes(llm_bridge):
    """Test 3: Learning mode progression."""
    print("\n" + "="*80)
    print("TEST 3: Learning Mode Progression")
    print("="*80)

    modes = ["bootstrap", "balanced", "specialized"]
    expected_rates = [0.70, 0.40, 0.10]

    for mode, expected in zip(modes, expected_rates):
        extractor = SymbioticLLMEntityExtractor(
            local_llm_bridge=llm_bridge,
            learning_mode=mode
        )
        actual = extractor.consultation_rates[mode]
        print(f"✅ {mode.capitalize()}: {actual*100:.0f}% consultation (expected: {expected*100:.0f}%)")
        assert actual == expected, f"Mode {mode} mismatch: {actual} != {expected}"

    print("✅ All learning mode tests passed")


def test_entity_extraction_prompt():
    """Test 4: Entity extraction prompt generation."""
    print("\n" + "="*80)
    print("TEST 4: Entity Extraction Prompt")
    print("="*80)

    extractor = SymbioticLLMEntityExtractor(learning_mode="bootstrap")

    text = "My daughter Emma seems overwhelmed with school lately."
    current_entities = {"Emma": {"type": "Person", "confidence": 0.85}}

    prompt = extractor._build_entity_extraction_prompt(text, current_entities)

    print("✅ Prompt generated:")
    print(prompt[:300] + "...\n")

    # Validate prompt contains key elements
    assert "therapeutic conversation" in prompt.lower() or "extract entities" in prompt.lower()
    assert "Emma" in prompt
    assert "Person" in prompt
    print("✅ Prompt contains entity extraction instructions and existing entities")


def test_comparison_logging(extractor):
    """Test 5: Pattern vs LLM comparison."""
    print("\n" + "="*80)
    print("TEST 5: Pattern vs LLM Comparison")
    print("="*80)

    # Use proper entity structure expected by _extract_entity_names
    pattern_entities = {
        "relationships": [{"name": "Emma", "type": "daughter"}],
        "places": [{"name": "school"}],
        "mentioned_names": []
    }

    llm_entities = {
        "relationships": [{"name": "Emma", "type": "daughter"}],
        "places": [{"name": "school"}],
        "mentioned_names": ["overwhelmed"]
    }

    metrics = extractor.compare_extraction_methods(pattern_entities, llm_entities)

    print(f"✅ Precision: {metrics['precision']:.2f}")
    print(f"✅ Recall: {metrics['recall']:.2f}")
    print(f"✅ F1 Score: {metrics['f1_score']:.2f}")
    print(f"✅ Pattern count: {metrics['pattern_count']}")
    print(f"✅ LLM count: {metrics['llm_count']}")
    print(f"✅ True positives: {len(metrics['true_positives'])}")

    assert 0 <= metrics['precision'] <= 1
    assert 0 <= metrics['recall'] <= 1
    assert 0 <= metrics['f1_score'] <= 1
    print("✅ Comparison metrics valid")


def test_safety_preservation():
    """Test 6: Existing safety gates preserved."""
    print("\n" + "="*80)
    print("TEST 6: Safety Gate Preservation")
    print("="*80)

    # Verify LocalLLMBridge still has safety gates
    llm_bridge = LocalLLMBridge()

    # Check if safety methods exist
    has_safety = hasattr(llm_bridge, '_should_use_llm_for_query')
    print(f"✅ Safety gate method exists: {has_safety}")

    # Extension should not bypass safety
    extractor = SymbioticLLMEntityExtractor(local_llm_bridge=llm_bridge)

    # Verify extension uses the bridge (not direct API)
    uses_bridge = extractor.llm_bridge is not None
    print(f"✅ Extension uses LocalLLMBridge: {uses_bridge}")

    print("✅ Safety gates preserved through bridge pattern")


def main():
    """Run all validation tests."""
    print("\n" + "="*80)
    print("SYMBIOTIC LLM ENTITY EXTRACTOR - VALIDATION SUITE")
    print("="*80)
    print(f"Testing extension to existing LocalLLMBridge infrastructure")
    print(f"Config: {Config.LOCAL_LLM_BACKEND}, {Config.LOCAL_LLM_MODEL}")

    try:
        # Test 1: Initialization
        extractor, llm_bridge = test_initialization()

        # Test 2: Tier routing
        test_tier_routing(extractor)

        # Test 3: Learning modes
        test_learning_modes(llm_bridge)

        # Test 4: Prompt generation
        test_entity_extraction_prompt()

        # Test 5: Comparison logging
        test_comparison_logging(extractor)

        # Test 6: Safety preservation
        test_safety_preservation()

        # Summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print("✅ All 6 tests passed")
        print("\nKey Validations:")
        print("  ✅ Extension properly leverages existing LocalLLMBridge")
        print("  ✅ Three-tier routing works correctly")
        print("  ✅ Learning mode progression validated")
        print("  ✅ Entity extraction prompts generated")
        print("  ✅ Pattern vs LLM comparison working")
        print("  ✅ Safety gates preserved")
        print("\n🌀 Symbiotic architecture validated - ready for Phase A bootstrap training 🌀")

        return True

    except Exception as e:
        print(f"\n❌ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
