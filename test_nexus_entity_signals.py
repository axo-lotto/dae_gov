"""
Test NEXUS entity signal extraction for Phase 0C multi-organ intersection.

Validates that extract_entity_signals() properly extracts 5 memory-based signals:
1. memory_strength - Mention count normalized
2. memory_recency - Temporal recency proxy
3. co_occurrence - Neighbor diversity
4. relationship_richness - Relationship depth
5. temporal_grounding - Time/date awareness

Author: DAE_HYPHAE_1 Strategic Integration
Date: November 19, 2025
Status: Phase 0C Activation - NEXUS Signal Extraction
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

from organs.modular.nexus.core.nexus_text_core import NEXUSTextCore


def test_nexus_entity_signals():
    """Test NEXUS entity signal extraction with mock entity tracker."""

    print("=" * 70)
    print("NEXUS ENTITY SIGNAL EXTRACTION TEST (Phase 0C)")
    print("=" * 70)
    print()

    # Initialize NEXUS (with entity tracker if available)
    print("Initializing NEXUS organ...")
    nexus = NEXUSTextCore(
        enable_neo4j=False,  # Don't need Neo4j for signal extraction
        enable_entity_tracker=True  # Need tracker for signals
    )

    if not nexus.entity_tracker:
        print("⚠️  Entity tracker not available - cannot test signal extraction")
        print("   Run entity-memory training first to populate tracker patterns")
        return

    print("✅ NEXUS initialized with entity tracker")
    print()

    # Test signal extraction for known entities
    test_entities = ['I', 'Emma', 'Lily', 'work', 'Boston']

    print(f"Testing signal extraction for {len(test_entities)} entities:")
    print("-" * 70)

    for entity_value in test_entities:
        print(f"\nEntity: '{entity_value}'")

        # Extract signals
        signals = nexus.extract_entity_signals(
            entity_value=entity_value,
            user_id='user_20251117_160809'  # Default user from training
        )

        # Display signals
        print(f"  Signals:")
        for signal_name, signal_strength in signals.items():
            bar_length = int(signal_strength * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"    {signal_name:25s} {signal_strength:.3f} {bar}")

        # Check if entity has any memory
        has_memory = any(v > 0.0 for v in signals.values())
        if has_memory:
            print(f"  Status: ✅ Memory signals detected")
        else:
            print(f"  Status: ⚠️  No memory signals (new/unknown entity)")

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    print()
    print("Expected behavior:")
    print("- Known entities (I, Emma, Lily) should have strong signals")
    print("- Unknown entities should have zero signals")
    print("- memory_strength should correlate with mention count")
    print("- co_occurrence should correlate with neighbor diversity")
    print()


if __name__ == '__main__':
    test_nexus_entity_signals()
