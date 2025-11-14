#!/usr/bin/env python3
"""
Test Appetition Bug - Debug Version
====================================

Tests appetition calculation with debug logging to identify why it's returning 0.10.
"""

import sys
from pathlib import Path

# Add DAE_HYPHAE_1 to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the class but bypass __init__
from dae_gov_cli import DAEGovCLI

# Create a mock DAEGovCLI instance with minimal setup
cli = object.__new__(DAEGovCLI)

# Set up minimal required attributes
class MockUserContext:
    def __init__(self):
        self.user_token = "test_user"
        self.user_dir = "/tmp/test_user"
        self.traces_dir = "/tmp/test_user/traces"

class MockSessionContext:
    def __init__(self):
        self.session_id = "test_session"
        self.human_name = "Test User"
        self.user_token = "test_user"
        self.user_context = {
            'user_dir': '/tmp/test_user',
            'traces_dir': '/tmp/test_user/traces'
        }
        self.global_organism = {
            'confidence': 1.0,
            'total_successes': 100,
            'success_rate': 0.8
        }
        self.conversation_history = []
        self.felt_state_trajectory = []
        self.kairos_moments = []
        self.traces_created = []
        self.total_sessions = 1
        self.total_traces = 0
        self.started_at = "2025-11-11"

cli.session_context = MockSessionContext()

# Import required modules
import numpy as np
from typing import Dict, List

# Test knowledge search results (simulating what user saw)
test_knowledge = [
    {'text': 'Whitehead quote about superject...', 'source': 'process_reality', 'score': 0.02},
    {'text': 'Superject definition...', 'source': 'glossary', 'score': 0.01},
    {'text': 'More about superject...', 'source': 'conversations', 'score': 0.03},
    {'text': 'Actual occasions and superject...', 'source': 'process_reality_2', 'score': 0.015},
    {'text': 'Subject and superject...', 'source': 'process_reality_3', 'score': 0.025}
]

knowledge_available = len(test_knowledge) > 0
knowledge_relevance = np.mean([k.get('score', 0.0) for k in test_knowledge])

print("="*70)
print("APPETITION BUG DEBUG TEST")
print("="*70)

print(f"\n📚 Knowledge Search Results:")
print(f"   Found: {len(test_knowledge)} results")
print(f"   Scores: {[k['score'] for k in test_knowledge]}")
print(f"   Average relevance: {knowledge_relevance:.4f}")

# Test conversational analysis (simulating organ processing)
test_conversational_analysis = {
    'curiosity_triggered': True,
    'nexus_decision': type('obj', (object,), {
        'coherence_score': 1.0,
        'question_type': 'exploration',
        'question_organ': 'LISTENING',
        'intersection_count': 0.0
    })(),
    'organ_results': {
        'LISTENING': type('obj', (object,), {'coherence': 1.0})(),
        'EMPATHY': type('obj', (object,), {'coherence': 0.8})(),
        'WISDOM': type('obj', (object,), {'coherence': 0.9})(),
        'AUTHENTICITY': type('obj', (object,), {'coherence': 0.85})(),
        'PRESENCE': type('obj', (object,), {'coherence': 0.95})()
    }
}

print(f"\n🧠 Conversational Analysis:")
print(f"   Organs processed: {list(test_conversational_analysis['organ_results'].keys())}")
print(f"   Coherences: {[o.coherence for o in test_conversational_analysis['organ_results'].values()]}")
print(f"   Mean coherence: {np.mean([o.coherence for o in test_conversational_analysis['organ_results'].values()]):.2f}")

# Call the appetition calculation
print(f"\n🔬 Calling _compute_appetition_to_answer()...")

appetition_result = cli._compute_appetition_to_answer(
    knowledge_available=knowledge_available,
    knowledge_relevance=knowledge_relevance,
    conversational_analysis=test_conversational_analysis
)

print(f"\n📊 APPETITION CALCULATION BREAKDOWN:")
print(f"="*70)
print(f"\nInputs:")
print(f"   knowledge_available: {knowledge_available}")
print(f"   knowledge_relevance: {knowledge_relevance:.4f}  ← SUSPICIOUS (very low!)")
print(f"   mean_coherence: {appetition_result['mean_coherence']:.3f}")
print(f"   organism_energy: {appetition_result['organism_energy']:.3f}")
print(f"   resonance: {appetition_result['resonance']:.3f}")

print(f"\nFormula Components (weight × value):")
print(f"   Knowledge    (0.4 × {knowledge_relevance:.4f}): {appetition_result['components']['knowledge_contribution']:.4f}")
print(f"   Coherence    (0.3 × {appetition_result['mean_coherence']:.3f}): {appetition_result['components']['coherence_contribution']:.3f}")
print(f"   Energy       (0.2 × {1-appetition_result['organism_energy']:.3f}): {appetition_result['components']['energy_contribution']:.3f}")
print(f"   Resonance    (0.1 × {appetition_result['resonance']:.3f}): {appetition_result['components']['resonance_contribution']:.3f}")

print(f"\nTotal Appetition: {appetition_result['appetition_to_answer']:.4f}")
print(f"Threshold:        0.6000")
print(f"Gate Opens:       {'✅ YES' if appetition_result['appetition_to_answer'] > 0.6 else '❌ NO'}")

print(f"\n" + "="*70)
print(f"🔍 ROOT CAUSE IDENTIFIED:")
print(f"="*70)
print(f"\nThe knowledge_relevance is {knowledge_relevance:.4f} (essentially 0!)")
print(f"This means the 'score' values from search_knowledge() are VERY LOW.")
print(f"\nExpected: scores around 0.7-0.9 for relevant results")
print(f"Actual:   scores around 0.01-0.03 (100× too low!)")
print(f"\nThis causes:")
print(f"   knowledge_contribution = 0.4 × 0.02 = 0.008")
print(f"   Even with high coherence (0.3 × 0.9 = 0.27),")
print(f"   Total appetition = 0.008 + 0.27 + ... ≈ 0.30")
print(f"   Which is below threshold of 0.6 → CURIOSITY triggers instead!")

print(f"\n🔧 FIX REQUIRED:")
print(f"   The search_knowledge() method must be returning very low scores.")
print(f"   Need to investigate why FAISS similarity scores are 0.01-0.03")
print(f"   instead of expected 0.7-0.9 for relevant matches.")
print(f"\n   Possible causes:")
print(f"     1. Vector normalization issue")
print(f"     2. Distance metric vs similarity conversion")
print(f"     3. Score scaling problem")
print(f"")

