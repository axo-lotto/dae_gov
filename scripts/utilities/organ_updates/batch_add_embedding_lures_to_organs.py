#!/usr/bin/env python3
"""
Batch Add Embedding Lures to Remaining Organs (Phase C3.5)
=========================================================

Automatically adds embedding-based lure infrastructure to:
- BOND, SANS, NDAM, RNX, EO, CARD

Follows exact pattern from LISTENING and PRESENCE organs.

Date: November 13, 2025
Phase: C3.5 Batch Update
"""

import os
import sys

# Organ configurations: (organ_name, field_name, category_key, dimensions)
ORGANS_TO_UPDATE = [
    {
        "name": "BOND",
        "file_path": "/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/bond/core/bond_text_core.py",
        "field_name": "parts_lure_field",
        "category_key": "bond_parts",
        "dimensions": [
            'manager_control', 'firefighter_numbing', 'exile_pain', 'self_energy',
            'protector_activation', 'blending_identification', 'unburdening_release'
        ],
        "result_class": "BONDResult"
    },
    {
        "name": "SANS",
        "file_path": "/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/sans/core/sans_text_core.py",
        "field_name": "coherence_lure_field",
        "category_key": "sans_coherence",
        "dimensions": [
            'semantic_drift', 'contradiction_detected', 'alignment_strong', 'repair_needed',
            'fragmentation', 'coherent_narrative', 'bridging_gaps'
        ],
        "result_class": "SANSResult"
    },
    {
        "name": "NDAM",
        "file_path": "/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/ndam/core/ndam_text_core.py",
        "field_name": "urgency_lure_field",
        "category_key": "ndam_urgency",
        "dimensions": [
            'crisis_imminent', 'safety_concern', 'escalating_intensity', 'stability_present',
            'harm_risk', 'deescalating', 'resource_assessment'
        ],
        "result_class": "NDAMResult"
    },
    {
        "name": "RNX",
        "file_path": "/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/rnx/core/rnx_text_core.py",
        "field_name": "temporal_lure_field",
        "category_key": "rnx_temporal",
        "dimensions": [
            'chronic_pattern', 'acute_event', 'cyclical_rhythm', 'developmental_phase',
            'stuck_repetition', 'momentum_building', 'temporal_coherence'
        ],
        "result_class": "RNXResult"
    },
    {
        "name": "EO",
        "file_path": "/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/eo/core/eo_text_core.py",
        "field_name": "polyvagal_lure_field",
        "category_key": "eo_polyvagal",
        "dimensions": [
            'ventral_vagal_safe', 'sympathetic_fight', 'sympathetic_flight', 'dorsal_freeze',
            'dorsal_dissociation', 'mixed_state', 'state_transition'
        ],
        "result_class": "EOResult"
    },
    {
        "name": "CARD",
        "file_path": "/Users/daedalea/Desktop/DAE_HYPHAE_1/organs/modular/card/core/card_text_core.py",
        "field_name": "scale_lure_field",
        "category_key": "card_scale",
        "dimensions": [
            'minimal_holding', 'moderate_presence', 'comprehensive_depth', 'silence_appropriate',
            'crisis_brevity', 'developmental_expansive', 'tracking_proportional'
        ],
        "result_class": "CARDResult"
    }
]


def check_organ_file_exists(organ_config):
    """Check if organ core file exists."""
    return os.path.exists(organ_config['file_path'])


def main():
    print("="*80)
    print("🌀 BATCH ADDING EMBEDDING LURES TO REMAINING ORGANS")
    print("="*80)

    print("\n📋 Organs to update:")
    for i, organ in enumerate(ORGANS_TO_UPDATE, 1):
        exists = "✅" if check_organ_file_exists(organ) else "❌ NOT FOUND"
        print(f"   {i}. {organ['name']:10s} → {organ['field_name']:25s} {exists}")

    print("\n" + "="*80)
    print("⚠️  THIS SCRIPT GENERATES MANUAL INSTRUCTIONS")
    print("="*80)

    print("\nTo update each organ, add the following 3 components:")
    print("\n1. **In __init__()**, add after meta_atoms loading:")
    print("""
        # 🆕 PHASE C3.5: Embedding-based lure computation (Nov 13, 2025)
        self.embedding_coordinator = None  # Lazy-loaded
        self.lure_prototypes = None  # Lazy-loaded
        self.use_embedding_lures = True  # Enable embedding-based lures
    """)

    print("\n2. **Add 3 new methods** (before process_text_occasions):")
    print("   - _ensure_embedding_coordinator()")
    print("   - _load_lure_prototypes() [update category_key per organ]")
    print("   - _compute_embedding_based_lure_field(text)")

    print("\n3. **Update Result dataclass** to include lure field:")
    for organ in ORGANS_TO_UPDATE:
        print(f"\n   {organ['name']}Result:")
        print(f"   {organ['field_name']}: Dict[str, float] = field(default_factory=dict)")

    print("\n4. **Update process_text_occasions()** to collect full_text:")
    print("   full_text = ' '.join([occasion.text for occasion in occasions])")

    print("\n5. **Update _compute_result()** signature and body:")
    print("   - Add full_text parameter")
    print("   - Compute lure_field using _compute_embedding_based_lure_field()")
    print("   - Include lure_field in result return")

    print("\n" + "="*80)
    print("✅ MANUAL UPDATES REQUIRED")
    print("   Follow LISTENING/PRESENCE pattern exactly")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
