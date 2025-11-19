"""
Test multi-organ entity extraction with mock organ signals.

Validates FFITTSS T4 AffinityNexus pattern implementation:
1. Multi-organ intersection (3+ organs must agree)
2. Coherence gating (C̄ > 0.75 threshold)
3. NEXUS memory signal integration

Author: DAE_HYPHAE_1 Strategic Integration
Date: November 19, 2025
Status: Phase 0C - Multi-Organ Extraction Implementation
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

from persona_layer.multi_organ_entity_extractor import MultiOrganEntityExtractor
from organs.modular.nexus.core.nexus_text_core import NEXUSTextCore


def test_multi_organ_extraction():
    """Test multi-organ entity extraction with mock organ signals."""

    print("=" * 70)
    print("MULTI-ORGAN ENTITY EXTRACTION TEST (Phase 0C)")
    print("=" * 70)
    print()

    # Create extractor
    extractor = MultiOrganEntityExtractor(
        coherence_threshold=0.75,
        min_organs=3,
        ema_alpha=0.15
    )

    print(f"✅ Extractor initialized:")
    print(f"   Coherence threshold: {extractor.coherence_threshold}")
    print(f"   Minimum organs: {extractor.min_organs}")
    print()

    # Create mock organ results (12 organs detecting entities)
    print("Creating mock organ signals...")
    organ_results = {
        # LISTENING detects 'Emma' with high confidence
        'LISTENING': {
            'coherence': 0.85,
            'entity_signals': [
                {'entity_value': 'Emma', 'entity_type': 'Person', 'confidence': 0.90},
                {'entity_value': 'work', 'entity_type': 'Place', 'confidence': 0.60}
            ]
        },

        # EMPATHY also detects 'Emma' (agreement)
        'EMPATHY': {
            'coherence': 0.80,
            'entity_signals': [
                {'entity_value': 'Emma', 'entity_type': 'Person', 'confidence': 0.85},
                {'entity_value': 'kindergarten', 'entity_type': 'Place', 'confidence': 0.70}
            ]
        },

        # BOND detects 'Emma' (3rd organ = intersection threshold met)
        'BOND': {
            'coherence': 0.75,
            'entity_signals': [
                {'entity_value': 'Emma', 'entity_type': 'Person', 'confidence': 0.88}
            ]
        },

        # SANS detects 'kindergarten' (but only 2 organs total, below threshold)
        'SANS': {
            'coherence': 0.70,
            'entity_signals': [
                {'entity_value': 'kindergarten', 'entity_type': 'Place', 'confidence': 0.75}
            ]
        },

        # NDAM detects 'work' (but only 2 organs total)
        'NDAM': {
            'coherence': 0.65,
            'entity_signals': [
                {'entity_value': 'work', 'entity_type': 'Place', 'confidence': 0.55}
            ]
        },

        # Other organs with no entity signals
        'WISDOM': {'coherence': 0.60, 'entity_signals': []},
        'AUTHENTICITY': {'coherence': 0.65, 'entity_signals': []},
        'PRESENCE': {'coherence': 0.70, 'entity_signals': []},
        'RNX': {'coherence': 0.55, 'entity_signals': []},
        'EO': {'coherence': 0.60, 'entity_signals': []},
        'NEXUS': {'coherence': 0.50, 'entity_signals': []},
        'CARD': {'coherence': 0.65, 'entity_signals': []}
    }

    # Try to load NEXUS for memory signals (optional)
    nexus_organ = None
    try:
        nexus_organ = NEXUSTextCore(
            enable_neo4j=False,
            enable_entity_tracker=True
        )
        print("✅ NEXUS organ loaded for memory signal integration")
    except Exception as e:
        print(f"⚠️  NEXUS not available: {e}")

    print()

    # Run extraction
    print("Running multi-organ entity extraction...")
    extracted_entities = extractor.extract_entities_multi_organ(
        organ_results=organ_results,
        nexus_organ=nexus_organ
    )

    print(f"✅ Extraction complete: {len(extracted_entities)} entities extracted")
    print()

    # Display results
    print("=" * 70)
    print("EXTRACTION RESULTS")
    print("=" * 70)

    if extracted_entities:
        for i, entity in enumerate(extracted_entities, 1):
            print(f"\n[{i}] Entity: '{entity['entity_value']}' ({entity['entity_type']})")
            print(f"    Confidence: {entity['confidence']:.3f}")
            print(f"    Coherence:  {entity['coherence']:.3f} ({'✅ PASS' if entity['coherence'] >= 0.75 else '❌ FAIL'} 0.75 threshold)")
            print(f"    Organ agreement: {entity['num_organs']} organs")
            print(f"    Organs: {', '.join(entity['organ_agreement'])}")

            # Show signal details
            print(f"    Organ signals:")
            for organ_name, signal in entity['organ_signals'].items():
                conf = signal.get('confidence', 0.0)
                print(f"      - {organ_name}: {conf:.3f}")
    else:
        print("⚠️  No entities extracted (all below threshold or insufficient organ agreement)")

    print()
    print("=" * 70)
    print("EXPECTED RESULTS")
    print("=" * 70)
    print("✅ 'Emma' should be extracted:")
    print("   - 3 organs detect (LISTENING, EMPATHY, BOND)")
    print("   - Confidences: [0.90, 0.85, 0.88] → coherence should be very high (>0.99)")
    print("   - Should PASS 0.75 threshold")
    print()
    print("❌ 'work' should be REJECTED:")
    print("   - Only 2 organs detect (LISTENING, NDAM)")
    print("   - Below min_organs = 3 threshold")
    print()
    print("❌ 'kindergarten' should be REJECTED:")
    print("   - Only 2 organs detect (EMPATHY, SANS)")
    print("   - Below min_organs = 3 threshold")
    print()

    # Statistics
    stats = extractor.get_statistics()
    print("=" * 70)
    print("EXTRACTION STATISTICS")
    print("=" * 70)
    print(f"Total extractions: {stats['total_extractions']}")
    print(f"Mean coherence: {stats['mean_coherence']:.3f}")
    print(f"Gated rate: {stats['gated_rate']:.1%}")
    if stats['total_extractions'] > 0:
        print(f"Coherence range: [{stats['min_coherence']:.3f}, {stats['max_coherence']:.3f}]")
    print()


if __name__ == '__main__':
    test_multi_organ_extraction()
