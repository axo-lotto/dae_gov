#!/usr/bin/env python3
"""
Test Felt-Guided LLM Initialization
===================================

Tests that the felt-guided LLM system initializes correctly.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config

print("🌀 FELT-GUIDED LLM INITIALIZATION TEST")
print("=" * 60)
print()

# Check config flags
print("📋 Configuration Check:")
print(f"   HYBRID_ENABLED: {Config.HYBRID_ENABLED}")
print(f"   FELT_GUIDED_LLM_ENABLED: {Config.FELT_GUIDED_LLM_ENABLED}")
print()

if not Config.HYBRID_ENABLED:
    print("❌ HYBRID_ENABLED is False - cannot test")
    sys.exit(1)

if not Config.FELT_GUIDED_LLM_ENABLED:
    print("❌ FELT_GUIDED_LLM_ENABLED is False - cannot test")
    sys.exit(1)

# Test import
print("🔍 Testing imports...")
try:
    from persona_layer.llm_felt_guidance import FeltGuidedLLMGenerator
    print("   ✅ FeltGuidedLLMGenerator imported successfully")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test LLM bridge initialization
print()
print("🔍 Testing LLM bridge...")
try:
    from persona_layer.local_llm_bridge import MemoryEnrichedLLMBridge

    llm_bridge = MemoryEnrichedLLMBridge(
        model_name=Config.HYBRID_LLM_MODEL,
        ollama_url=Config.HYBRID_LLM_OLLAMA_URL
    )
    print(f"   ✅ LLM bridge initialized (model: {Config.HYBRID_LLM_MODEL})")
except Exception as e:
    print(f"   ❌ LLM bridge failed: {e}")
    sys.exit(1)

# Test felt-guided LLM initialization
print()
print("🔍 Testing FeltGuidedLLMGenerator initialization...")
try:
    felt_llm = FeltGuidedLLMGenerator(
        llm_bridge=llm_bridge,
        enable_safety_gates=True,
        enable_emergent_personality=True
    )
    print("   ✅ FeltGuidedLLMGenerator initialized")
    print(f"   ✅ Safety gates enabled: {felt_llm.enable_safety_gates}")
    print(f"   ✅ Emergent personality enabled: {felt_llm.enable_emergent_personality}")
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test felt lure extraction (with mock data)
print()
print("🔍 Testing felt lure extraction...")
try:
    from dataclasses import dataclass

    # Mock organ results
    @dataclass
    class MockOrganResult:
        confidence: float = 0.5
        self_zone: float = 0.65
        crisis_zone: int = 0
        urgency: float = 0.2
        polyvagal_state: str = "ventral_vagal"

    mock_organ_results = {
        'BOND': MockOrganResult(self_zone=0.65),
        'EO': MockOrganResult(polyvagal_state="ventral_vagal"),
        'NDAM': MockOrganResult(urgency=0.2, crisis_zone=0),
        'LISTENING': MockOrganResult(confidence=0.45),
        'EMPATHY': MockOrganResult(confidence=0.52),
    }

    lures = felt_llm.extract_felt_lures(
        organ_results=mock_organ_results,
        nexus_states=[],
        v0_energy=0.85,
        satisfaction=0.60
    )

    print("   ✅ Lures extracted successfully")
    print(f"      - Polyvagal state: {lures.polyvagal_state}")
    print(f"      - Self energy: {lures.self_energy}")
    print(f"      - Trauma present: {lures.trauma_present}")
    print(f"      - Crisis level: {lures.crisis_level}")
    print(f"      - Urgency: {lures.urgency}")

except Exception as e:
    print(f"   ❌ Lure extraction failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test constraint mapping
print()
print("🔍 Testing constraint mapping...")
try:
    constraints = felt_llm.lures_to_constraints(lures)
    print("   ✅ Constraints mapped successfully")
    print(f"      - Tone: {constraints.tone}")
    print(f"      - Response length: {constraints.response_length}")
    print(f"      - Detail level: {constraints.detail_level}")
    print(f"      - Gentleness level: {constraints.gentleness_level}")
    print(f"      - Empathy level: {constraints.empathy_level}")

except Exception as e:
    print(f"   ❌ Constraint mapping failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test prompt building
print()
print("🔍 Testing prompt building...")
try:
    prompt = felt_llm.build_felt_prompt(
        user_input="Hello there!",
        constraints=constraints,
        lures=lures,
        memory_context=None
    )
    print("   ✅ Prompt built successfully")
    print(f"      Prompt length: {len(prompt)} chars")
    print(f"      Contains 'warm tone': {'warm' in prompt.lower()}")
    print(f"      Contains user input: {'hello' in prompt.lower()}")

except Exception as e:
    print(f"   ❌ Prompt building failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✅ ALL TESTS PASSED - Felt-guided LLM ready for testing!")
print("=" * 60)
print()
print("🎯 Next Step: Test with actual conversation input")
print("   Run: python3 test_felt_guided_llm_conversation.py")
