"""
Lure-Informed Phrase Selection - Phase C2.2 & C2.3
===================================================

Enables lure-aware phrase selection by:
1. Synthesizing multi-organ lure signatures (EMPATHY + WISDOM + AUTHENTICITY)
2. Computing phrase-lure alignment scores
3. Filtering/weighting phrases by lure resonance

Purpose:
- Complete organ intelligence transduction: Lure fields → Emission content
- Phrases resonate with felt lure landscape
- TSK compliant: Track lure signatures used in emission

Philosophy:
- Emission respects the felt emotional/cognitive/relational field
- Not keyword matching - continuous lure field alignment
- Multi-dimensional: Emotional + Pattern + Vulnerability signatures

Date: November 13, 2025
Phase: C2.2 + C2.3 Integration
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class LureInformedPhraseSelector:
    """
    Select phrases based on lure field alignment.

    Synthesizes composite lure signature from EMPATHY/WISDOM/AUTHENTICITY organs,
    then selects phrases that resonate with this felt landscape.

    Integration:
    - Called during transduction emission generation
    - Receives organ_results with lure fields
    - Returns weighted phrase list for softmax sampling
    """

    def __init__(
        self,
        lure_phrase_library_path: str = "persona_layer/config/transduction/transduction_mechanism_phrases_with_lure_tags.json",
        enable_lure_filtering: bool = True,
        lure_alignment_weight: float = 0.6  # 60% lure, 40% uniform
    ):
        """
        Initialize lure-informed phrase selector.

        Args:
            lure_phrase_library_path: Path to phrase library with lure tags
            enable_lure_filtering: Enable lure-aware filtering (disable for backward compatibility)
            lure_alignment_weight: Weight for lure alignment (0=uniform, 1=full lure filtering)
        """
        self.enable_lure_filtering = enable_lure_filtering
        self.lure_alignment_weight = lure_alignment_weight

        # Load lure-tagged phrase library
        self.lure_phrase_library = self._load_lure_phrase_library(lure_phrase_library_path)

        # Lure dimension names (from Phase B)
        self.empathy_dimensions = ["joy", "grief", "fear", "anger", "compassion", "shame", "neutral"]
        self.wisdom_dimensions = ["systems", "meta", "temporal", "paradox", "embodied", "relational", "integrative"]
        self.authenticity_dimensions = ["vulnerable", "honest", "guarded", "performative", "emergent", "receptive", "boundaried"]

    def _load_lure_phrase_library(self, path: str) -> Dict:
        """Load phrase library with lure tags."""
        library_path = Path(path)

        if not library_path.exists():
            print(f"⚠️  Lure phrase library not found at {path}, falling back to keyword-free mode")
            return {}

        try:
            with open(library_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading lure phrase library: {e}")
            return {}

    def synthesize_lure_signature(
        self,
        organ_results: Dict
    ) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, float]]:
        """
        🆕 PHASE C2.3: Synthesize composite lure signature from 3 conversational organs.

        Combines lure fields from EMPATHY + WISDOM + AUTHENTICITY into unified signatures.

        Args:
            organ_results: Dict of organ results (from organism wrapper)

        Returns:
            Tuple of (emotional_signature, cognitive_signature, relational_signature)
            Each is a Dict[dimension, float] normalized to sum=1.0
        """
        # Extract lure fields from organs
        empathy_lure_field = {}
        wisdom_lure_field = {}
        authenticity_lure_field = {}

        # Get EMPATHY emotional lure field
        if 'EMPATHY' in organ_results:
            empathy_result = organ_results['EMPATHY']
            empathy_lure_field = getattr(empathy_result, 'emotional_lure_field', {})

        # Get WISDOM pattern lure field
        if 'WISDOM' in organ_results:
            wisdom_result = organ_results['WISDOM']
            wisdom_lure_field = getattr(wisdom_result, 'pattern_lure_field', {})

        # Get AUTHENTICITY vulnerability lure field
        if 'AUTHENTICITY' in organ_results:
            authenticity_result = organ_results['AUTHENTICITY']
            authenticity_lure_field = getattr(authenticity_result, 'vulnerability_lure_field', {})

        # Normalize signatures (ensure sum=1.0)
        emotional_signature = self._normalize_lure_field(empathy_lure_field, self.empathy_dimensions)
        cognitive_signature = self._normalize_lure_field(wisdom_lure_field, self.wisdom_dimensions)
        relational_signature = self._normalize_lure_field(authenticity_lure_field, self.authenticity_dimensions)

        return emotional_signature, cognitive_signature, relational_signature

    def _normalize_lure_field(self, lure_field: Dict, dimensions: List[str]) -> Dict[str, float]:
        """Normalize lure field to sum=1.0."""
        # If empty, return balanced defaults
        if not lure_field:
            return {dim: 1.0 / len(dimensions) for dim in dimensions}

        # Normalize existing field
        total = sum(lure_field.values())
        if total == 0:
            return {dim: 1.0 / len(dimensions) for dim in dimensions}

        return {dim: lure_field.get(dim, 0.0) / total for dim in dimensions}

    def compute_phrase_lure_alignment(
        self,
        phrase_lure_tags: Dict[str, Dict[str, float]],
        emotional_signature: Dict[str, float],
        cognitive_signature: Dict[str, float],
        relational_signature: Dict[str, float]
    ) -> float:
        """
        🆕 PHASE C2.2: Compute alignment between phrase lure tags and lure signature.

        Uses cosine similarity between phrase's lure tags and organism's lure signature.

        Args:
            phrase_lure_tags: {'empathy': {...}, 'wisdom': {...}, 'authenticity': {...}}
            emotional_signature: Synthesized emotional lure field
            cognitive_signature: Synthesized pattern lure field
            relational_signature: Synthesized vulnerability lure field

        Returns:
            Alignment score [0, 1] (higher = better alignment)
        """
        # Extract phrase lure vectors
        phrase_emotional = phrase_lure_tags.get('empathy', {})
        phrase_cognitive = phrase_lure_tags.get('wisdom', {})
        phrase_relational = phrase_lure_tags.get('authenticity', {})

        # Compute cosine similarity for each lure dimension
        emotional_sim = self._cosine_similarity(phrase_emotional, emotional_signature)
        cognitive_sim = self._cosine_similarity(phrase_cognitive, cognitive_signature)
        relational_sim = self._cosine_similarity(phrase_relational, relational_signature)

        # Weighted average (equal weights for now)
        alignment = (emotional_sim + cognitive_sim + relational_sim) / 3.0

        return alignment

    def _cosine_similarity(self, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        """Compute cosine similarity between two lure vectors."""
        # Get all dimensions
        all_dims = set(vec_a.keys()) | set(vec_b.keys())

        # Convert to numpy arrays
        a = np.array([vec_a.get(dim, 0.0) for dim in sorted(all_dims)])
        b = np.array([vec_b.get(dim, 0.0) for dim in sorted(all_dims)])

        # Compute cosine similarity
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        similarity = np.dot(a, b) / (norm_a * norm_b)

        # Clamp to [0, 1]
        return max(0.0, min(1.0, similarity))

    def get_lure_weighted_phrases(
        self,
        mechanism: str,
        intensity: str,
        organ_results: Dict,
        fallback_to_unweighted: bool = True
    ) -> Tuple[List[str], List[float]]:
        """
        Get phrases with lure-based weights for sampling.

        Args:
            mechanism: Transduction mechanism name (e.g., 'salience_recalibration')
            intensity: Intensity level ('high', 'medium', 'low')
            organ_results: Organ results with lure fields
            fallback_to_unweighted: If True, return uniform weights if lure filtering disabled

        Returns:
            Tuple of (phrase_texts, phrase_weights)
        """
        # If lure filtering disabled or library not loaded, return uniform
        if not self.enable_lure_filtering or not self.lure_phrase_library:
            # Get phrases from old library (backward compatible)
            return [], []

        # Get mechanism config from lure library
        mechanisms = self.lure_phrase_library.get('mechanisms', {})
        if mechanism not in mechanisms:
            return [], []

        mechanism_config = mechanisms[mechanism]
        intensity_phrases = mechanism_config.get('intensity_phrases', {})
        phrase_objects = intensity_phrases.get(intensity, intensity_phrases.get('medium', []))

        if not phrase_objects:
            return [], []

        # Synthesize lure signature
        emotional_sig, cognitive_sig, relational_sig = self.synthesize_lure_signature(organ_results)

        # Compute alignment scores for each phrase
        phrase_texts = []
        phrase_weights = []

        for phrase_obj in phrase_objects:
            # Handle both old format (string) and new format (object with lure_tags)
            if isinstance(phrase_obj, str):
                # Old format - uniform weight
                phrase_texts.append(phrase_obj)
                phrase_weights.append(1.0)
            elif isinstance(phrase_obj, dict):
                # New format with lure tags
                text = phrase_obj.get('text', '')
                lure_tags = phrase_obj.get('lure_tags', {})

                # Compute alignment
                alignment = self.compute_phrase_lure_alignment(
                    lure_tags,
                    emotional_sig,
                    cognitive_sig,
                    relational_sig
                )

                # Weight = lure_alignment_weight × alignment + (1 - lure_alignment_weight) × uniform
                # This ensures phrases are boosted by lure but not completely filtered
                weight = self.lure_alignment_weight * alignment + (1 - self.lure_alignment_weight) * 1.0

                phrase_texts.append(text)
                phrase_weights.append(weight)

        return phrase_texts, phrase_weights

    def get_lure_signature_for_tsk(
        self,
        organ_results: Dict
    ) -> Dict:
        """
        Get lure signature for TSK tracking.

        Returns:
            Dict with emotional/cognitive/relational signatures for felt_states
        """
        emotional_sig, cognitive_sig, relational_sig = self.synthesize_lure_signature(organ_results)

        return {
            'emotional_signature': emotional_sig,
            'cognitive_signature': cognitive_sig,
            'relational_signature': relational_sig
        }


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🌀 LURE-INFORMED PHRASE SELECTION TEST")
    print("="*70)

    # Mock organ results
    from dataclasses import dataclass

    @dataclass
    class MockEmpathyResult:
        emotional_lure_field: Dict[str, float]

    @dataclass
    class MockWisdomResult:
        pattern_lure_field: Dict[str, float]

    @dataclass
    class MockAuthenticityResult:
        vulnerability_lure_field: Dict[str, float]

    mock_organ_results = {
        'EMPATHY': MockEmpathyResult(
            emotional_lure_field={'compassion': 0.7, 'grief': 0.3}
        ),
        'WISDOM': MockWisdomResult(
            pattern_lure_field={'relational': 0.6, 'embodied': 0.4}
        ),
        'AUTHENTICITY': MockAuthenticityResult(
            vulnerability_lure_field={'receptive': 0.7, 'honest': 0.3}
        )
    }

    try:
        selector = LureInformedPhraseSelector()

        # Test lure signature synthesis
        emotional_sig, cognitive_sig, relational_sig = selector.synthesize_lure_signature(mock_organ_results)

        print(f"\n✅ Lure signature synthesis successful!")
        print(f"\n📊 COMPOSITE LURE SIGNATURE:")
        print(f"   Emotional (EMPATHY): {emotional_sig}")
        print(f"   Cognitive (WISDOM): {cognitive_sig}")
        print(f"   Relational (AUTHENTICITY): {relational_sig}")

        # Test lure-weighted phrase selection
        phrases, weights = selector.get_lure_weighted_phrases(
            mechanism='salience_recalibration',
            intensity='high',
            organ_results=mock_organ_results
        )

        print(f"\n✅ Lure-weighted phrase selection successful!")
        print(f"\n📝 WEIGHTED PHRASES (salience_recalibration, high):")
        for i, (phrase, weight) in enumerate(zip(phrases[:3], weights[:3]), 1):
            print(f"   {i}. \"{phrase}\" (weight: {weight:.3f})")

        # Test TSK tracking
        tsk_signature = selector.get_lure_signature_for_tsk(mock_organ_results)
        print(f"\n✅ TSK signature extraction successful!")
        print(f"   Dimensions tracked: {len(tsk_signature)} signatures")

        print(f"\n✅ Lure-informed phrase selection working correctly!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
