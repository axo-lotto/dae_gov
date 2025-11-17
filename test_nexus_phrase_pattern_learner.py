"""
Test Suite: Nexus-Phrase Pattern Learner
=========================================

Validates intersection-centered emission learning with 15 comprehensive tests.

Test Coverage:
1. Basic pattern recording and retrieval
2. EMA quality learning convergence
3. Fuzzy matching with bin relaxation
4. Coherence horizon enforcement (max 5000 patterns)
5. Recency weighting (temporal decay)
6. Success rate computation
7. JSON persistence and deserialization
8. Top-k phrase ranking
9. Pruning lowest quality patterns
10. Exact vs fuzzy matching
11. Multiple phrases per nexus
12. Quality computation (EMA × success_rate × recency)
13. Signature serialization/deserialization
14. Empty learner behavior
15. Statistics reporting

November 17, 2025 - Phase 1 Week 2, Day 5
"""

import unittest
import os
import tempfile
import json
import numpy as np
from persona_layer.nexus_signature_extractor import NexusSignature
from persona_layer.nexus_phrase_pattern_learner import (
    NexusPhrasePatternLearner,
    PhraseQualityMetrics,
    NexusPhrasePattern
)


class TestPhraseQualityMetrics(unittest.TestCase):
    """Test suite for PhraseQualityMetrics."""

    def test_compute_overall_quality_no_decay(self):
        """Test 1: Overall quality computation without decay."""
        phrase = PhraseQualityMetrics(
            text="I hear the weight...",
            ema_quality=0.8,
            success_count=8,
            total_attempts=10,
            success_rate=0.8,
            mean_satisfaction=0.75,
            last_used_turn=10
        )

        # No decay at same turn
        quality = phrase.compute_overall_quality(current_turn=10, decay_lambda=0.001)
        expected = 0.8 * 0.8 * 1.0  # EMA × success_rate × recency (no decay)
        self.assertAlmostEqual(quality, expected, places=3)

    def test_compute_overall_quality_with_decay(self):
        """Test 2: Overall quality with temporal decay."""
        phrase = PhraseQualityMetrics(
            text="I hear the weight...",
            ema_quality=0.8,
            success_count=8,
            total_attempts=10,
            success_rate=0.8,
            mean_satisfaction=0.75,
            last_used_turn=10
        )

        # Decay after 100 turns
        quality = phrase.compute_overall_quality(current_turn=110, decay_lambda=0.001)

        # Recency weight = exp(-0.001 × 100) = exp(-0.1) ≈ 0.9048
        expected_recency = np.exp(-0.001 * 100)
        expected = 0.8 * 0.8 * expected_recency

        self.assertAlmostEqual(quality, expected, places=3)
        self.assertAlmostEqual(phrase.recency_weight, expected_recency, places=3)


class TestNexusPhrasePattern(unittest.TestCase):
    """Test suite for NexusPhrasePattern."""

    def setUp(self):
        """Create test nexus signature."""
        self.signature = NexusSignature(
            participating_organs=frozenset(['EMPATHY', 'NDAM', 'RNX']),
            organ_count=3,
            nexus_type='PSYCHE',
            mechanism='CRISIS_WITNESSING',
            coherence_bin=6,
            urgency_bin=8,
            polyvagal_state='sympathetic',
            zone=4,
            v0_energy_bin=2,
            kairos_detected=False,
            field_strength_bin=5,
            dominant_meta_atom='emotional_resonance'
        )
        self.sig_hash = str(self.signature.to_hashable(precision='medium'))
        self.pattern = NexusPhrasePattern(
            signature_hash=self.sig_hash,
            signature=self.signature,
            phrases=[]
        )

    def test_add_phrase(self):
        """Test 3: Adding phrases to pattern."""
        self.pattern.add_phrase("I hear the weight...")
        self.assertEqual(len(self.pattern.phrases), 1)
        self.assertEqual(self.pattern.phrases[0].text, "I hear the weight...")

        # Adding duplicate should not create new entry
        self.pattern.add_phrase("I hear the weight...")
        self.assertEqual(len(self.pattern.phrases), 1)

    def test_update_phrase_quality_ema(self):
        """Test 4: EMA quality learning."""
        self.pattern.add_phrase("I hear the weight...", initial_quality=0.5)

        # Update with high satisfaction
        self.pattern.update_phrase_quality(
            phrase_text="I hear the weight...",
            user_satisfaction=0.9,
            current_turn=1,
            ema_alpha=0.15
        )

        phrase = self.pattern.phrases[0]
        # EMA: 0.15 × 0.9 + 0.85 × 0.5 = 0.135 + 0.425 = 0.56
        self.assertAlmostEqual(phrase.ema_quality, 0.56, places=2)
        self.assertEqual(phrase.total_attempts, 1)
        self.assertEqual(phrase.success_count, 1)  # 0.9 ≥ 0.6
        self.assertEqual(phrase.success_rate, 1.0)

    def test_update_phrase_quality_convergence(self):
        """Test 5: EMA converges to mean satisfaction."""
        self.pattern.add_phrase("I hear the weight...", initial_quality=0.5)

        # Simulate 20 updates with satisfaction=0.8
        for turn in range(1, 21):
            self.pattern.update_phrase_quality(
                phrase_text="I hear the weight...",
                user_satisfaction=0.8,
                current_turn=turn,
                ema_alpha=0.15
            )

        phrase = self.pattern.phrases[0]
        # EMA should converge toward 0.8
        self.assertGreater(phrase.ema_quality, 0.7)
        self.assertLess(phrase.ema_quality, 0.85)
        self.assertEqual(phrase.total_attempts, 20)
        self.assertEqual(phrase.success_count, 20)  # All 0.8 ≥ 0.6

    def test_get_top_phrases(self):
        """Test 6: Top-k phrase ranking."""
        self.pattern.add_phrase("Phrase A", initial_quality=0.6)
        self.pattern.add_phrase("Phrase B", initial_quality=0.8)
        self.pattern.add_phrase("Phrase C", initial_quality=0.5)

        # Update to create differentiation
        self.pattern.update_phrase_quality("Phrase A", 0.7, 1)
        self.pattern.update_phrase_quality("Phrase B", 0.9, 1)
        self.pattern.update_phrase_quality("Phrase C", 0.4, 1)

        top_phrases = self.pattern.get_top_phrases(k=2, current_turn=1)
        self.assertEqual(len(top_phrases), 2)
        self.assertEqual(top_phrases[0].text, "Phrase B")  # Highest quality
        self.assertEqual(top_phrases[1].text, "Phrase A")


class TestNexusPhrasePatternLearner(unittest.TestCase):
    """Test suite for NexusPhrasePatternLearner."""

    def setUp(self):
        """Create temporary memory file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.memory_path = os.path.join(self.temp_dir, "test_memory.json")
        self.learner = NexusPhrasePatternLearner(
            memory_path=self.memory_path,
            ema_alpha=0.15,
            fuzzy_tolerance=1,
            max_patterns=100  # Smaller for testing
        )

        self.signature = NexusSignature(
            participating_organs=frozenset(['EMPATHY', 'NDAM', 'RNX']),
            organ_count=3,
            nexus_type='PSYCHE',
            mechanism='CRISIS_WITNESSING',
            coherence_bin=6,
            urgency_bin=8,
            polyvagal_state='sympathetic',
            zone=4,
            v0_energy_bin=2,
            kairos_detected=False,
            field_strength_bin=5,
            dominant_meta_atom='emotional_resonance'
        )

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_record_emission_outcome(self):
        """Test 7: Recording emission outcome."""
        self.learner.record_emission_outcome(
            nexus_signature=self.signature,
            emitted_phrase="I hear the weight...",
            user_satisfaction=0.85,
            current_turn=1
        )

        # Check pattern was created
        sig_hash = str(self.signature.to_hashable(precision='medium'))
        self.assertIn(sig_hash, self.learner.patterns)

        pattern = self.learner.patterns[sig_hash]
        self.assertEqual(len(pattern.phrases), 1)
        self.assertEqual(pattern.phrases[0].text, "I hear the weight...")
        self.assertEqual(pattern.phrases[0].total_attempts, 1)

    def test_persistence_save_load(self):
        """Test 8: JSON persistence and deserialization."""
        self.learner.record_emission_outcome(
            nexus_signature=self.signature,
            emitted_phrase="I hear the weight...",
            user_satisfaction=0.85,
            current_turn=1
        )

        # Create new learner instance (loads from disk)
        learner2 = NexusPhrasePatternLearner(memory_path=self.memory_path)

        sig_hash = str(self.signature.to_hashable(precision='medium'))
        self.assertIn(sig_hash, learner2.patterns)

        pattern = learner2.patterns[sig_hash]
        self.assertEqual(len(pattern.phrases), 1)
        self.assertEqual(pattern.phrases[0].text, "I hear the weight...")
        self.assertAlmostEqual(pattern.phrases[0].ema_quality, 0.85, places=2)

    def test_get_candidate_phrases_exact_match(self):
        """Test 9: Exact match candidate retrieval."""
        self.learner.record_emission_outcome(
            nexus_signature=self.signature,
            emitted_phrase="I hear the weight...",
            user_satisfaction=0.85,
            current_turn=1
        )

        candidates = self.learner.get_candidate_phrases(
            nexus_signature=self.signature,
            k=5,
            current_turn=1,
            use_fuzzy=False
        )

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0][0], "I hear the weight...")
        self.assertGreater(candidates[0][1], 0.0)  # Non-zero quality

    def test_get_candidate_phrases_fuzzy_match(self):
        """Test 10: Fuzzy matching with bin relaxation."""
        # Record phrase with specific signature
        self.learner.record_emission_outcome(
            nexus_signature=self.signature,
            emitted_phrase="I hear the weight...",
            user_satisfaction=0.85,
            current_turn=1
        )

        # Create similar signature (coherence_bin 6 → 7)
        similar_signature = NexusSignature(
            participating_organs=frozenset(['EMPATHY', 'NDAM', 'RNX']),
            organ_count=3,
            nexus_type='PSYCHE',
            mechanism='CRISIS_WITNESSING',
            coherence_bin=7,  # Different bin (within tolerance=1)
            urgency_bin=8,
            polyvagal_state='sympathetic',
            zone=4,
            v0_energy_bin=2,
            kairos_detected=False,
            field_strength_bin=5,
            dominant_meta_atom='emotional_resonance'
        )

        candidates = self.learner.get_candidate_phrases(
            nexus_signature=similar_signature,
            k=5,
            current_turn=1,
            use_fuzzy=True
        )

        # Should find phrase via fuzzy matching
        self.assertGreater(len(candidates), 0)
        self.assertEqual(candidates[0][0], "I hear the weight...")

    def test_multiple_phrases_per_nexus(self):
        """Test 11: Multiple phrases for same nexus."""
        self.learner.record_emission_outcome(
            nexus_signature=self.signature,
            emitted_phrase="I hear the weight...",
            user_satisfaction=0.85,
            current_turn=1
        )

        self.learner.record_emission_outcome(
            nexus_signature=self.signature,
            emitted_phrase="I sense the burden...",
            user_satisfaction=0.75,
            current_turn=2
        )

        candidates = self.learner.get_candidate_phrases(
            nexus_signature=self.signature,
            k=5,
            current_turn=2
        )

        self.assertEqual(len(candidates), 2)
        # Higher satisfaction should rank higher
        self.assertEqual(candidates[0][0], "I hear the weight...")

    def test_coherence_horizon_pruning(self):
        """Test 12: Coherence horizon enforcement (max patterns)."""
        # Fill up to max_patterns (100)
        for i in range(110):  # Exceed max by 10
            sig = NexusSignature(
                participating_organs=frozenset(['EMPATHY']),
                organ_count=1,
                nexus_type='PSYCHE',
                mechanism=f'MECHANISM_{i}',  # Unique mechanism
                coherence_bin=i % 10,
                urgency_bin=5,
                polyvagal_state='ventral',
                zone=1,
                v0_energy_bin=2,
                kairos_detected=False,
                field_strength_bin=5,
                dominant_meta_atom='presence'
            )

            self.learner.record_emission_outcome(
                nexus_signature=sig,
                emitted_phrase=f"Phrase {i}",
                user_satisfaction=0.5,
                current_turn=i
            )

        # Should not exceed max_patterns
        self.assertLessEqual(len(self.learner.patterns), 100)

    def test_empty_learner_behavior(self):
        """Test 13: Empty learner returns no candidates."""
        candidates = self.learner.get_candidate_phrases(
            nexus_signature=self.signature,
            k=5,
            current_turn=1
        )

        self.assertEqual(len(candidates), 0)

    def test_success_rate_computation(self):
        """Test 14: Success rate tracks satisfaction ≥ 0.6."""
        # Record 10 emissions: 6 success (≥0.6), 4 failures
        # Success: 0.8, 0.7, 0.9, 0.75, 0.85, 0.65 = 6
        # Failure: 0.4, 0.5, 0.3, 0.55 = 4
        satisfactions = [0.8, 0.7, 0.9, 0.4, 0.5, 0.75, 0.3, 0.85, 0.65, 0.55]

        for turn, sat in enumerate(satisfactions, start=1):
            self.learner.record_emission_outcome(
                nexus_signature=self.signature,
                emitted_phrase="I hear the weight...",
                user_satisfaction=sat,
                current_turn=turn
            )

        sig_hash = str(self.signature.to_hashable(precision='medium'))
        phrase = self.learner.patterns[sig_hash].phrases[0]

        expected_success = sum(1 for s in satisfactions if s >= 0.6)
        self.assertEqual(phrase.success_count, expected_success)  # 6 (not 7)
        self.assertEqual(phrase.total_attempts, 10)
        self.assertAlmostEqual(phrase.success_rate, 0.6, places=2)

    def test_get_stats(self):
        """Test 15: Statistics reporting."""
        # Record multiple emissions
        for i in range(5):
            sig = NexusSignature(
                participating_organs=frozenset(['EMPATHY']),
                organ_count=1,
                nexus_type='PSYCHE',
                mechanism=f'MECHANISM_{i}',
                coherence_bin=i,
                urgency_bin=5,
                polyvagal_state='ventral',
                zone=1,
                v0_energy_bin=2,
                kairos_detected=False,
                field_strength_bin=5,
                dominant_meta_atom='presence'
            )

            self.learner.record_emission_outcome(
                nexus_signature=sig,
                emitted_phrase=f"Phrase {i}",
                user_satisfaction=0.8,
                current_turn=i
            )

        stats = self.learner.get_stats()

        self.assertEqual(stats['total_patterns'], 5)
        self.assertEqual(stats['total_phrases'], 5)
        self.assertGreater(stats['mean_phrase_quality'], 0.0)
        self.assertLessEqual(stats['coherence_horizon_utilization'], 1.0)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
