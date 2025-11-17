"""
Diagnose NDAM Urgency Detection
================================

Test whether NDAM organ is detecting urgency keywords in crisis inputs.

Purpose: Understand why validation showed 0.000 urgency for all crisis inputs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from organs.modular.ndam.core.ndam_text_core import NDAMTextCore
from transductive.text_occasion import TextOccasion

def test_ndam_keyword_detection():
    """Test NDAM keyword detection on crisis inputs."""

    print("=" * 80)
    print("🔍 DIAGNOSING NDAM URGENCY DETECTION")
    print("=" * 80)

    # Initialize NDAM organ
    print("\n🔧 Initializing NDAM organ...")
    ndam = NDAMTextCore()
    print(f"   ✅ NDAM initialized")
    print(f"   Keywords loaded: {len(ndam.keyword_patterns)}")
    print(f"   Keyword groups: {list(ndam.keyword_groups.keys())}")
    print(f"   Urgency threshold: {ndam.config.urgency_threshold}")

    # Test inputs from crisis validation
    test_cases = [
        {
            "id": "crisis_high_1",
            "text": "I'm terrified about Emma's surgery tomorrow and I can't stop my mind from spiraling",
            "expected_keywords": ["terrified", "can't stop", "spiraling"]
        },
        {
            "id": "crisis_high_2",
            "text": "Work is completely crushing me right now - I can't breathe, everything is too much",
            "expected_keywords": ["crushing", "can't breathe", "too much"]
        },
        {
            "id": "shadow_1",
            "text": "There's a part of me I'm deeply ashamed of and I don't want to look at it",
            "expected_keywords": ["ashamed"]
        },
        {
            "id": "exile_1",
            "text": "I feel completely shut down and numb - like I'm watching life from behind glass",
            "expected_keywords": ["shut down", "numb"]
        }
    ]

    print(f"\n📊 Testing {len(test_cases)} crisis inputs...\n")

    for test_case in test_cases:
        print(f"{'=' * 80}")
        print(f"TEST: {test_case['id']}")
        print(f"{'=' * 80}")
        print(f"\n📝 INPUT:")
        print(f'   "{test_case["text"]}"')

        # Create TextOccasion
        import numpy as np
        occasion = TextOccasion(
            chunk_id=f"doc_1_para_1_sent_1_chunk_1",  # Valid format
            position=0,
            text=test_case["text"],
            embedding=np.zeros(384)  # Dummy embedding
        )

        # Process through NDAM
        try:
            result = ndam.process_text_occasions([occasion], cycle=1)

            print(f"\n🧠 NDAM RESULTS:")
            print(f"   Coherence: {result.coherence:.3f}")
            print(f"   Mean urgency: {result.mean_urgency:.3f}")
            print(f"   Max urgency: {result.max_urgency:.3f}")
            print(f"   Keywords matched: {result.keywords_matched}")
            print(f"   Patterns detected: {len(result.patterns)}")

            if result.patterns:
                print(f"\n   📍 DETECTED PATTERNS:")
                for pattern in result.patterns:
                    print(f"      • Type: {pattern.pattern_type}")
                    print(f"        Strength: {pattern.strength:.3f}")
                    print(f"        Confidence: {pattern.confidence:.3f}")
                    print(f"        Keywords: {pattern.matched_keywords}")
            else:
                print(f"\n   ⚠️  NO PATTERNS DETECTED")

            # Check atom activations
            if result.atom_activations:
                print(f"\n   ⚡ ATOM ACTIVATIONS:")
                for atom, activation in result.atom_activations.items():
                    if activation > 0:
                        print(f"      • {atom}: {activation:.3f}")
            else:
                print(f"\n   ⚠️  NO ATOM ACTIVATIONS")

            # Expected vs actual
            print(f"\n   📋 EXPECTED:")
            print(f"      Keywords: {test_case['expected_keywords']}")

            print(f"\n   {'✅' if result.keywords_matched > 0 else '❌'} DETECTION {'SUCCESS' if result.keywords_matched > 0 else 'FAILED'}")

        except Exception as e:
            print(f"\n   ❌ ERROR: {e}")
            import traceback
            traceback.print_exc()

        print()

    print("=" * 80)
    print("✅ DIAGNOSTIC COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    test_ndam_keyword_detection()
