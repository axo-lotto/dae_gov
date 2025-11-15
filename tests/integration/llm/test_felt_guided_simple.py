#!/usr/bin/env python3
"""
Simple Direct Test of Felt-Guided LLM
=====================================

Directly test the felt-guided LLM generator without going through
the full organism pipeline.
"""

import sys
from pathlib import Path
from dataclasses import dataclass

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from persona_layer.local_llm_bridge import MemoryEnrichedLLMBridge
from persona_layer.llm_felt_guidance import FeltGuidedLLMGenerator

print("🌀 SIMPLE FELT-GUIDED LLM TEST")
print("=" * 70)
print()

# Mock organ results
@dataclass
class MockOrganResult:
    confidence: float = 0.5
    self_zone: float = 0.65
    crisis_zone: int = 0
    urgency: float = 0.2
    polyvagal_state: str = "ventral_vagal"

# Test 1: Short greeting with low urgency
print("=" * 70)
print("Test 1: Short Greeting - Warm, Safe State")
print("=" * 70)
print()

llm_bridge = MemoryEnrichedLLMBridge(
    model_name=Config.HYBRID_LLM_MODEL,
    ollama_url=Config.HYBRID_LLM_OLLAMA_URL
)

felt_llm = FeltGuidedLLMGenerator(
    llm_bridge=llm_bridge,
    enable_safety_gates=True,
    enable_emergent_personality=True
)

mock_organ_results = {
    'BOND': MockOrganResult(self_zone=0.75),  # High self-energy (no trauma)
    'EO': MockOrganResult(polyvagal_state="ventral_vagal"),  # Safe/social state
    'NDAM': MockOrganResult(urgency=0.1, crisis_zone=0),  # Low urgency, no crisis
    'LISTENING': MockOrganResult(confidence=0.55),
    'EMPATHY': MockOrganResult(confidence=0.60),
    'PRESENCE': MockOrganResult(confidence=0.50),
}

user_input = "Hello there!"

print(f"Input: \"{user_input}\"")
print()

emission_text, confidence, metadata = felt_llm.generate_from_felt_state(
    user_input=user_input,
    organ_results=mock_organ_results,
    nexus_states=[],
    v0_energy=0.85,
    satisfaction=0.60,
    memory_context=None
)

print(f"💬 Emission:")
print(f"   \"{emission_text}\"")
print()
print(f"📊 Metadata:")
print(f"   Confidence: {confidence:.3f}")
print(f"   Strategy: {metadata.get('emission_path', 'unknown')}")
print(f"   Polyvagal state: {metadata.get('lures').polyvagal_state if 'lures' in metadata else 'unknown'}")
print(f"   Tone: {metadata.get('constraints').tone if 'constraints' in metadata else 'unknown'}")
print()

# Check for process-aware language
process_phrases = [
    "prehension", "prehended", "concrescence", "actual occasion",
    "nexus formation", "satisfaction", "v0", "kairos", "becoming"
]
has_process_language = any(phrase in emission_text.lower() for phrase in process_phrases)

if has_process_language:
    print("⚠️  WARNING: Process-aware language detected!")
else:
    print("✅ No process-aware language - natural conversation")

print()
print("=" * 70)
print()

# Test 2: Trauma-aware input
print("=" * 70)
print("Test 2: Trauma-Aware Input - Gentle, Safe Response")
print("=" * 70)
print()

mock_organ_results_trauma = {
    'BOND': MockOrganResult(self_zone=0.35),  # Low self-energy (trauma present)
    'EO': MockOrganResult(polyvagal_state="sympathetic"),  # Fight/flight
    'NDAM': MockOrganResult(urgency=0.75, crisis_zone=1),  # High urgency
    'LISTENING': MockOrganResult(confidence=0.60),
    'EMPATHY': MockOrganResult(confidence=0.70),
    'PRESENCE': MockOrganResult(confidence=0.55),
}

user_input_trauma = "I'm feeling really overwhelmed and scared"

print(f"Input: \"{user_input_trauma}\"")
print()

emission_text, confidence, metadata = felt_llm.generate_from_felt_state(
    user_input=user_input_trauma,
    organ_results=mock_organ_results_trauma,
    nexus_states=[],
    v0_energy=0.60,
    satisfaction=0.30,
    memory_context=None
)

print(f"💬 Emission:")
print(f"   \"{emission_text}\"")
print()
print(f"📊 Metadata:")
print(f"   Confidence: {confidence:.3f}")
print(f"   Strategy: {metadata.get('emission_path', 'unknown')}")
print(f"   Polyvagal state: {metadata.get('lures').polyvagal_state if 'lures' in metadata else 'unknown'}")
print(f"   Tone: {metadata.get('constraints').tone if 'constraints' in metadata else 'unknown'}")
print(f"   Gentleness boost: {metadata.get('constraints').gentleness_level if 'constraints' in metadata else 'unknown'}")
print()

# Check for gentle language
if confidence > 0.5:
    print("✅ Reasonable confidence in trauma-aware response")
else:
    print("⚠️  Low confidence in trauma response")

print()
print("=" * 70)
print()

# Test 3: Crisis detection
print("=" * 70)
print("Test 3: Crisis Detection - Safety Fallback")
print("=" * 70)
print()

mock_organ_results_crisis = {
    'BOND': MockOrganResult(self_zone=0.20),  # Very low self-energy
    'EO': MockOrganResult(polyvagal_state="dorsal_vagal"),  # Shutdown
    'NDAM': MockOrganResult(urgency=0.95, crisis_zone=3),  # CRISIS LEVEL
    'LISTENING': MockOrganResult(confidence=0.40),
    'EMPATHY': MockOrganResult(confidence=0.50),
    'PRESENCE': MockOrganResult(confidence=0.45),
}

user_input_crisis = "Everything is falling apart I can't handle this"

print(f"Input: \"{user_input_crisis}\"")
print()

emission_text, confidence, metadata = felt_llm.generate_from_felt_state(
    user_input=user_input_crisis,
    organ_results=mock_organ_results_crisis,
    nexus_states=[],
    v0_energy=0.40,
    satisfaction=0.10,
    memory_context=None
)

print(f"💬 Emission:")
print(f"   \"{emission_text}\"")
print()
print(f"📊 Metadata:")
print(f"   Confidence: {confidence:.3f}")
print(f"   Strategy: {metadata.get('emission_path', 'unknown')}")
print(f"   Crisis level: {metadata.get('lures').crisis_level if 'lures' in metadata else 'unknown'}")
print()

if metadata.get('emission_path') == 'safety_fallback':
    print("✅ Safety fallback triggered correctly for crisis")
else:
    print("⚠️  Safety fallback NOT triggered (expected for crisis > 0.7)")

print()
print("=" * 70)
print("✅ SIMPLE TEST COMPLETE")
print("=" * 70)
