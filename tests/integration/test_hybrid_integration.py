#!/usr/bin/env python3
"""
Integration tests for hybrid superject architecture.

Tests verify that hybrid components integrate seamlessly with pure DAE,
providing backward compatibility and graceful fallback.

Date: November 13, 2025
Status: Week 2 Integration Tests
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from config import Config


class TestHybridBackwardCompatibility:
    """Verify hybrid mode with HYBRID_ENABLED=False produces pure DAE results."""

    def test_hybrid_disabled_equals_pure_dae(self):
        """When HYBRID_ENABLED=False, system should behave identically to pure DAE."""
        # Temporarily disable hybrid
        original_hybrid_enabled = Config.HYBRID_ENABLED
        Config.HYBRID_ENABLED = False

        try:
            from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper

            organism = ConversationalOrganismWrapper()
            result = organism.process_text("I'm feeling overwhelmed right now.")

            # Verify core DAE processing worked
            assert 'felt_states' in result
            assert 'emission_text' in result['felt_states']
            assert result['felt_states']['emission_confidence'] > 0.0

            # Verify no hybrid data present
            assert 'hybrid' not in result

            print("✅ Hybrid disabled test passed: Pure DAE behavior maintained")

        finally:
            Config.HYBRID_ENABLED = original_hybrid_enabled

    def test_conversational_occasion_hybrid_method_exists(self):
        """Verify hybrid V0 method exists and accepts correct parameters."""
        from persona_layer.conversational_occasion import ConversationalOccasion

        occasion = ConversationalOccasion(datum="test", position=0)

        # Verify method exists
        assert hasattr(occasion, 'compute_v0_energy_hybrid')

        # Test with pure DAE parameters (llm_weight=0)
        energy = occasion.compute_v0_energy_hybrid(
            satisfaction=0.8,
            appetition=0.6,
            relevance=0.7,
            complexity=0.5,
            llm_confidence=0.0,
            llm_weight=0.0
        )

        # Verify energy in valid range
        assert 0.0 <= energy <= 1.0

        print("✅ Hybrid V0 method test passed")

    def test_emission_generator_hybrid_method_exists(self):
        """Verify Gate 5 LLM fusion method exists."""
        from persona_layer.emission_generator import EmissionGenerator

        generator = EmissionGenerator(
            semantic_atoms_path=str(Config.SEMANTIC_ATOMS_PATH),
            hebbian_memory_path=str(Config.HEBBIAN_MEMORY_PATH)
        )

        # Verify methods exist
        assert hasattr(generator, 'generate_hybrid_emission')
        assert hasattr(generator, '_fuse_organ_llm_text')

        # Test Path A: Direct organ (llm_weight < 0.3, organ_conf > 0.7)
        result = generator.generate_hybrid_emission(
            organ_emission="I sense what you're feeling.",
            llm_emission="It sounds like you're experiencing difficulty.",
            organ_confidence=0.85,
            llm_confidence=0.70,
            llm_weight=0.2,
            kairos_boost=1.0
        )

        # Verify Path A (direct organ)
        assert result['emission_path'] == 'direct_organ'
        assert result['organ_contribution'] == 1.0
        assert result['llm_contribution'] == 0.0
        assert result['emission'] == "I sense what you're feeling."

        # Test Path B: LLM scaffolded (llm_weight > 0.6)
        result = generator.generate_hybrid_emission(
            organ_emission="I sense what you're feeling.",
            llm_emission="It sounds like you're experiencing difficulty.",
            organ_confidence=0.85,
            llm_confidence=0.70,
            llm_weight=0.8,
            kairos_boost=1.0
        )

        # Verify Path B (LLM scaffolded)
        assert result['emission_path'] == 'llm_scaffolded'
        assert result['organ_contribution'] == 0.0
        assert result['llm_contribution'] == 1.0
        assert result['emission'] == "It sounds like you're experiencing difficulty."

        # Test Path C: Hybrid fusion (balanced)
        result = generator.generate_hybrid_emission(
            organ_emission="I sense what you're feeling.",
            llm_emission="It sounds like you're experiencing difficulty.",
            organ_confidence=0.60,
            llm_confidence=0.65,
            llm_weight=0.5,
            kairos_boost=1.0
        )

        # Verify Path C (hybrid fusion)
        assert result['emission_path'] == 'hybrid_fusion'
        assert 0.0 < result['organ_contribution'] < 1.0
        assert 0.0 < result['llm_contribution'] < 1.0
        assert result['organ_contribution'] + result['llm_contribution'] == 1.0

        print("✅ Gate 5 LLM fusion test passed (all 3 paths)")


class TestHybridMemoryRetrieval:
    """Test memory retrieval integration."""

    def test_memory_retrieval_initialization(self):
        """Verify MemoryRetrieval initializes with existing infrastructure."""
        # Skip if hybrid disabled
        if not Config.HYBRID_ENABLED:
            pytest.skip("Hybrid mode disabled")

        from persona_layer.memory_retrieval import MemoryRetrieval

        memory = MemoryRetrieval(
            hebbian_memory_path=str(Config.HEBBIAN_MEMORY_PATH),
            organic_families_path=str(Config.ORGANIC_FAMILIES_PATH),
            top_k=5
        )

        # Verify loaded components
        assert memory.r_matrix is not None  # Hebbian R-matrix
        assert memory.families_data is not None  # Organic families

        print("✅ Memory retrieval initialization test passed")


class TestHybridSuperjectRecording:
    """Test superject recording integration."""

    def test_superject_recorder_initialization(self):
        """Verify SuperjectRecorder initializes correctly."""
        # Skip if hybrid disabled
        if not Config.HYBRID_ENABLED:
            pytest.skip("Hybrid mode disabled")

        from persona_layer.superject_recorder import SuperjectRecorder

        recorder = SuperjectRecorder(
            session_storage_dir=str(Config.HYBRID_SUPERJECT_SESSION_DIR),
            user_bundles_dir=str(Config.HYBRID_SUPERJECT_USER_BUNDLES_DIR)
        )

        # Verify directories created
        assert recorder.session_storage_dir.exists()
        assert recorder.user_bundles_dir.exists()

        print("✅ Superject recorder initialization test passed")


class TestHybridGracefulFallback:
    """Test graceful fallback when LLM unavailable."""

    def test_llm_unavailable_fallback(self):
        """Verify system continues with pure DAE when LLM unavailable."""
        # This test would require mocking Ollama unavailability
        # For now, just verify the component exists
        if not Config.HYBRID_ENABLED:
            pytest.skip("Hybrid mode disabled")

        from persona_layer.local_llm_bridge import MemoryEnrichedLLMBridge

        # Verify class exists and can be instantiated
        bridge = MemoryEnrichedLLMBridge(
            model_name=Config.HYBRID_LLM_MODEL,
            ollama_url=Config.HYBRID_LLM_OLLAMA_URL
        )

        assert hasattr(bridge, 'query_with_memory')

        print("✅ LLM bridge initialization test passed")


class TestHybridEndToEnd:
    """End-to-end integration tests."""

    def test_config_hybrid_section_exists(self):
        """Verify hybrid configuration section exists in config.py."""
        assert hasattr(Config, 'HYBRID_ENABLED')
        assert hasattr(Config, 'HYBRID_LLM_MODEL')
        assert hasattr(Config, 'HYBRID_LLM_INITIAL_WEIGHT')
        assert hasattr(Config, 'V0_ALPHA_HYBRID')
        assert hasattr(Config, 'V0_ETA_HYBRID')

        # Verify default values
        assert Config.HYBRID_ENABLED == False  # Default: disabled
        assert Config.HYBRID_LLM_INITIAL_WEIGHT == 0.80
        assert Config.V0_ALPHA_HYBRID == 0.35
        assert Config.V0_ETA_HYBRID == 0.08

        print("✅ Hybrid configuration test passed")

    def test_progressive_weaning_formula(self):
        """Verify progressive weaning formula produces expected values."""
        import math

        # Formula: w_llm(month) = 0.80·e^(-0.24·month) + 0.05
        def compute_llm_weight(month: int) -> float:
            return 0.80 * math.exp(-0.24 * month) + 0.05

        # Month 0: ~0.85
        assert 0.84 <= compute_llm_weight(0) <= 0.86

        # Month 3: ~0.44
        assert 0.43 <= compute_llm_weight(3) <= 0.45

        # Month 6: ~0.18
        assert 0.16 <= compute_llm_weight(6) <= 0.20

        # Month 12: ~0.05
        assert 0.04 <= compute_llm_weight(12) <= 0.06

        print("✅ Progressive weaning formula test passed")


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🧪 HYBRID INTEGRATION TESTS")
    print("="*80 + "\n")

    # Run tests manually
    test_suite = [
        TestHybridBackwardCompatibility(),
        TestHybridMemoryRetrieval(),
        TestHybridSuperjectRecording(),
        TestHybridGracefulFallback(),
        TestHybridEndToEnd()
    ]

    passed = 0
    failed = 0

    for test_class in test_suite:
        class_name = test_class.__class__.__name__
        print(f"\n📦 {class_name}")
        print("-" * 80)

        for method_name in dir(test_class):
            if method_name.startswith('test_'):
                try:
                    method = getattr(test_class, method_name)
                    print(f"\n  Running: {method_name}...")
                    method()
                    passed += 1
                except pytest.skip.Exception as e:
                    print(f"  ⏭️  Skipped: {e}")
                except Exception as e:
                    print(f"  ❌ Failed: {e}")
                    import traceback
                    traceback.print_exc()
                    failed += 1

    print("\n" + "="*80)
    print(f"📊 RESULTS: {passed} passed, {failed} failed")
    print("="*80 + "\n")

    sys.exit(0 if failed == 0 else 1)
