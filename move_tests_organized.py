#!/usr/bin/env python3
"""
Move test files to organized test subdirectories
Safe, systematic test file organization
"""

import shutil
from pathlib import Path

# Mapping of test files to destinations
TEST_MOVES = {
    # Unit tests - organs
    'tests/unit/organs/': [
        'test_authenticity_embedding_lures.py',
        'test_authenticity_lure.py',
        'test_bond_embedding_lures.py',
        'test_empathy_embedding_lures.py',
        'test_empathy_lure.py',
        'test_listening_embedding_lures.py',
        'test_presence_embedding_lures.py',
        'test_wisdom_embedding_lures.py',
        'test_wisdom_lure.py',
    ],

    # Unit tests - mechanisms
    'tests/unit/mechanisms/': [
        'test_meta_atom_integration.py',
        'test_meta_atom_library.py',
        'test_organ_confidence.py',
        'test_r_matrix_learning.py',
        'test_generative_processual_emission.py',
        'test_regime_confidence_modulation.py',
        'test_v0_guided_emission.py',
        'test_sans_embeddings_arc.py',
        'test_organ_results_structure.py',
    ],

    # Integration tests - entities
    'tests/integration/entities/': [
        'test_entity_integration_basic.py',
        'test_entity_memory_fix_direct.py',
        'test_entity_memory_persistence.py',
        'test_entity_persistence_interactive.py',
        'test_entity_recall_complete.py',
        'test_entity_recall_simple.py',
        'test_hebbian_entity_memory_fix.py',
        'test_relationship_extraction.py',
        'test_tsk_entity_enrichment.py',
    ],

    # Integration tests - families
    'tests/integration/families/': [
        'test_family_detection_understanding.py',
        'test_family_v0_integration.py',
    ],

    # Integration tests - LLM
    'tests/integration/llm/': [
        'test_felt_guided_llm_conversation.py',
        'test_felt_guided_llm_init.py',
        'test_felt_guided_simple.py',
        'test_phase1_felt_llm_reconstruction.py',
    ],

    # Integration tests - phases
    'tests/integration/phases/': [
        'test_phase2_reconstruction.py',
        'test_phase_c2_integration.py',
        'test_reconstruction_integration.py',
        'test_training_with_reconstruction.py',
    ],

    # Integration tests - organisms
    'tests/integration/organisms/': [
        'test_emergent_voice_post_expansion.py',
        'test_whiteheadian_intellect.py',
        'test_simple_interactions.py',
        'test_continuous_reflection.py',
        'test_zone5_transductive.py',
        'test_organism_capabilities.py',
    ],

    # Integration tests - training
    'tests/integration/training/': [
        'test_epoch_orchestrator.py',
        'test_gradient_organ_weights.py',
        'test_memory_persistence.py',
    ],

    # Validation tests - system
    'tests/validation/system/': [
        'test_complete_system_assessment.py',
    ],

    # Superject tests
    'tests/superject/': [
        'test_superject_persistence.py',
    ],

    # Debug tests
    'tests/debug/': [
        'test_empty_input_bug.py',
        'test_no_nexus_fix.py',
        'test_entity_flow_debug.py',
        'test_meta_commentary_fix.py',
        'TEST_BOTH_FIXES.py',
    ],
}

def move_tests():
    """Move test files to organized subdirectories."""
    moved = 0
    not_found = 0

    print("=" * 70)
    print("🧪 ORGANIZING TEST FILES")
    print("=" * 70)
    print()

    for dest_dir, files in TEST_MOVES.items():
        # Ensure destination exists
        Path(dest_dir).mkdir(parents=True, exist_ok=True)

        for filename in files:
            src = Path(filename)
            if src.exists():
                dst = Path(dest_dir) / filename
                shutil.move(str(src), str(dst))
                print(f"✓ {filename:50} → {dest_dir}")
                moved += 1
            else:
                print(f"⚠ {filename:50} (not found)")
                not_found += 1

    print()
    print("=" * 70)
    print(f"✅ Moved: {moved} files")
    if not_found > 0:
        print(f"⚠  Not found: {not_found} files (may have been moved already)")
    print("=" * 70)
    print()

    # Verify
    remaining = list(Path('.').glob('test_*.py')) + list(Path('.').glob('TEST_*.py'))
    print(f"📊 Test files remaining in root: {len(remaining)}")
    if remaining:
        print("Remaining files:")
        for f in remaining:
            print(f"  • {f.name}")

if __name__ == '__main__':
    move_tests()
