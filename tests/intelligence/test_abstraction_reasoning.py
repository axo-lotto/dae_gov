"""
Intelligence Test: Abstraction Reasoning (INTEL-001)
===================================================

Tests the organism's ability to reason across abstraction levels and detect
patterns in increasingly abstract inputs.

Theoretical Foundation (ARC-Inspired):
- Concrete → Semi-Abstract → Abstract progression
- Pattern detection across representation types
- Transfer learning validation (learns from one, applies to another)

Test Protocol:
1. Present 3 inputs at different abstraction levels on same underlying pattern
2. Measure organ activation consistency across levels
3. Validate nexus formation stability
4. Check emission coherence despite representation changes

Success Criteria:
- Organ activation correlation: ≥0.70 across levels
- Same nexus types formed: ≥60% overlap
- Emission similarity: ≥0.60 (semantic alignment)
- Confidence stability: ±0.15 range (not wildly different)

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Intelligence Testing)
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import Counter

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config
from tests.intelligence.utils.test_utils import IntelligenceTestUtils


@dataclass
class AbstractionLevel:
    """Single abstraction level test input."""
    level: str  # "concrete", "semi_abstract", "abstract"
    input_text: str
    pattern_id: str  # Underlying pattern this represents


@dataclass
class AbstractionReasoningResult:
    """Result of abstraction reasoning test."""
    pattern_id: str
    levels_tested: int

    # Organ activation correlation
    organ_activation_correlation: float  # Mean pairwise correlation
    organ_consistency: bool  # ≥0.70

    # Nexus formation overlap
    nexus_overlap_rate: float  # % shared nexus types
    nexus_stability: bool  # ≥60%

    # Emission similarity
    emission_similarity: float  # Mean cosine similarity
    emission_coherence: bool  # ≥0.60

    # Confidence stability
    confidence_range: float  # Max - min confidence
    confidence_stable: bool  # ±0.15

    # Overall success
    success: bool
    reasoning: str


class AbstractionReasoningTester:
    """
    Tests abstraction reasoning across representation levels.

    Validates that the organism can:
    - Detect same patterns in different representations
    - Maintain organ activation consistency
    - Form similar nexus structures
    - Generate coherent emissions
    """

    def __init__(
        self,
        organism: Optional[ConversationalOrganismWrapper] = None
    ):
        """
        Initialize abstraction reasoning tester.

        Args:
            organism: ConversationalOrganismWrapper instance (or create new)
        """
        if organism is None:
            print("🌀 Initializing organism for abstraction reasoning test...")
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism

        # Initialize test utilities
        self.utils = IntelligenceTestUtils()

    def _get_test_patterns(self) -> Dict[str, List[AbstractionLevel]]:
        """
        Get test patterns across abstraction levels.

        Returns:
            Dict mapping pattern_id to list of abstraction levels
        """
        patterns = {
            # Pattern 1: Scapegoating dynamics
            "scapegoating": [
                AbstractionLevel(
                    level="concrete",
                    input_text="Every time our project fails, everyone blames the QA team. "
                              "They're the scapegoat for our collective inability to write good code. "
                              "It's easier to point fingers than to look at our own contribution.",
                    pattern_id="scapegoating"
                ),
                AbstractionLevel(
                    level="semi_abstract",
                    input_text="There's a systemic pattern where one group consistently carries "
                              "the collective shadow. The blamed party becomes a container for "
                              "everyone else's disavowed responsibility.",
                    pattern_id="scapegoating"
                ),
                AbstractionLevel(
                    level="abstract",
                    input_text="A mechanism where collective accountability fragments into "
                              "concentrated attribution. The system maintains equilibrium by "
                              "externalizing dissonance onto a designated receiver.",
                    pattern_id="scapegoating"
                )
            ],

            # Pattern 2: Witnessing presence
            "witnessing": [
                AbstractionLevel(
                    level="concrete",
                    input_text="I just need someone to listen without trying to fix it. "
                              "Not advice, not solutions. Just... presence. Just being here with me.",
                    pattern_id="witnessing"
                ),
                AbstractionLevel(
                    level="semi_abstract",
                    input_text="The need isn't for intervention but for accompaniment. "
                              "A request for co-regulation through attunement rather than "
                              "problem-solving through action.",
                    pattern_id="witnessing"
                ),
                AbstractionLevel(
                    level="abstract",
                    input_text="A relational configuration where holding space supersedes "
                              "instrumental response. The therapeutic mechanism is presence itself, "
                              "not derived outcomes.",
                    pattern_id="witnessing"
                )
            ],

            # Pattern 3: Burnout spiral
            "burnout": [
                AbstractionLevel(
                    level="concrete",
                    input_text="I work 80 hours a week and still feel like I'm failing. "
                              "Every time I rest, I feel guilty. The exhaustion is crushing but "
                              "I can't stop because stopping means I'm weak.",
                    pattern_id="burnout"
                ),
                AbstractionLevel(
                    level="semi_abstract",
                    input_text="A recursive loop where rest is pathologized and productivity is "
                              "conflated with worthiness. The system demands continuous output "
                              "while depleting the capacity to generate it.",
                    pattern_id="burnout"
                ),
                AbstractionLevel(
                    level="abstract",
                    input_text="Self-perpetuating energetic depletion where recovery mechanisms "
                              "are inhibited by the same value structures that drive overextension. "
                              "The attractor basin deepens with each iteration.",
                    pattern_id="burnout"
                )
            ]
        }

        return patterns

    def _compute_organ_activation_correlation(
        self,
        results: List[Dict]
    ) -> float:
        """
        Compute pairwise correlation of organ activations across results.

        Args:
            results: List of organism processing results

        Returns:
            Mean pairwise correlation coefficient
        """
        # Extract organ activation dictionaries
        activation_dicts = []
        for result in results:
            organ_results = result.get('organ_results', {})
            # Create dict of coherence scores
            activations = {}
            for organ_name in ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                             'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']:
                organ_result = organ_results.get(organ_name)
                if organ_result:
                    # Use coherence attribute (not satisfaction)
                    coherence = getattr(organ_result, 'coherence', 0.0)
                    activations[organ_name] = coherence
                else:
                    activations[organ_name] = 0.0
            activation_dicts.append(activations)

        if len(activation_dicts) < 2:
            return 0.0

        # Compute pairwise correlations using test utils
        correlations = []
        for i in range(len(activation_dicts)):
            for j in range(i + 1, len(activation_dicts)):
                corr = self.utils.compute_organ_activation_correlation(
                    activation_dicts[i],
                    activation_dicts[j]
                )
                correlations.append(corr)

        if len(correlations) == 0:
            return 0.0

        return float(np.mean(correlations))

    def _compute_nexus_overlap(
        self,
        results: List[Dict]
    ) -> float:
        """
        Compute overlap in nexus types formed across results.

        Args:
            results: List of organism processing results

        Returns:
            Percentage of shared nexus types (0-1)
        """
        nexus_sets = []
        for result in results:
            nexuses = result.get('nexuses', [])
            # Extract nexus types (e.g., "relational_attunement", "compassion_safety")
            nexus_types = set()
            for nexus in nexuses:
                if isinstance(nexus, dict):
                    nexus_type = nexus.get('atom_name') or nexus.get('meta_atom_name')
                    if nexus_type:
                        nexus_types.add(nexus_type)
            nexus_sets.append(nexus_types)

        if len(nexus_sets) < 2:
            return 0.0

        # Compute Jaccard similarity between all pairs
        overlaps = []
        for i in range(len(nexus_sets)):
            for j in range(i + 1, len(nexus_sets)):
                intersection = len(nexus_sets[i] & nexus_sets[j])
                union = len(nexus_sets[i] | nexus_sets[j])
                if union > 0:
                    overlaps.append(intersection / union)

        if len(overlaps) == 0:
            return 0.0

        return float(np.mean(overlaps))

    def _compute_emission_similarity(
        self,
        results: List[Dict]
    ) -> float:
        """
        Compute semantic similarity of emissions using embeddings.

        Args:
            results: List of organism processing results

        Returns:
            Mean pairwise emission similarity (0-1)
        """
        emissions = []
        for result in results:
            emission = result.get('emission', '')
            emissions.append(emission)

        if len(emissions) < 2:
            return 0.0

        # Compute semantic similarity using test utils
        similarities = []
        for i in range(len(emissions)):
            for j in range(i + 1, len(emissions)):
                sim = self.utils.compute_emission_semantic_similarity(
                    emissions[i],
                    emissions[j]
                )
                similarities.append(sim)

        if len(similarities) == 0:
            return 0.0

        return float(np.mean(similarities))

    def test_abstraction_reasoning(
        self,
        pattern_id: Optional[str] = None,
        verbose: bool = True
    ) -> AbstractionReasoningResult:
        """
        Test abstraction reasoning on a pattern.

        Args:
            pattern_id: Pattern to test (or random if None)
            verbose: Print detailed results

        Returns:
            AbstractionReasoningResult with metrics and success status
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"🧠 ABSTRACTION REASONING TEST (INTEL-001)")
            print(f"{'='*70}")
            print(f"\nTesting: Pattern detection across abstraction levels")

        # Get test patterns
        patterns = self._get_test_patterns()

        if pattern_id is None:
            pattern_id = list(patterns.keys())[0]

        if pattern_id not in patterns:
            raise ValueError(f"Unknown pattern: {pattern_id}")

        levels = patterns[pattern_id]

        if verbose:
            print(f"Pattern: {pattern_id}")
            print(f"Levels: {len(levels)} (concrete → semi-abstract → abstract)")

        # Process each abstraction level
        results = []
        confidences = []

        for level_data in levels:
            if verbose:
                print(f"\n📊 Processing {level_data.level}...")
                print(f"   Input: {level_data.input_text[:100]}...")

            result = self.organism.process_text(
                text=level_data.input_text,
                enable_phase2=True,
                enable_tsk_recording=False
            )

            results.append(result)

            # Get confidence from top-level result (not felt_states)
            confidence = result.get('emission_confidence', 0.0)
            confidences.append(confidence)

            if verbose:
                nexuses = result.get('nexuses', [])
                print(f"   Confidence: {confidence:.3f}")
                print(f"   Nexuses: {len(nexuses)}")

        # Compute metrics
        organ_correlation = self._compute_organ_activation_correlation(results)
        nexus_overlap = self._compute_nexus_overlap(results)
        emission_similarity = self._compute_emission_similarity(results)
        confidence_range = max(confidences) - min(confidences)

        # Success criteria
        organ_consistency = organ_correlation >= 0.70
        nexus_stability = nexus_overlap >= 0.60
        emission_coherence = emission_similarity >= 0.60
        confidence_stable = confidence_range <= 0.15

        success = (
            organ_consistency and
            nexus_stability and
            emission_coherence and
            confidence_stable
        )

        # Reasoning
        if success:
            reasoning = f"Abstraction reasoning successful: pattern '{pattern_id}' detected across {len(levels)} levels"
        else:
            reasons = []
            if not organ_consistency:
                reasons.append(f"Organ inconsistency: {organ_correlation:.2f} < 0.70")
            if not nexus_stability:
                reasons.append(f"Nexus instability: {nexus_overlap:.2f} < 0.60")
            if not emission_coherence:
                reasons.append(f"Emission incoherence: {emission_similarity:.2f} < 0.60")
            if not confidence_stable:
                reasons.append(f"Confidence unstable: range={confidence_range:.2f} > 0.15")
            reasoning = "; ".join(reasons)

        result = AbstractionReasoningResult(
            pattern_id=pattern_id,
            levels_tested=len(levels),
            organ_activation_correlation=organ_correlation,
            organ_consistency=organ_consistency,
            nexus_overlap_rate=nexus_overlap,
            nexus_stability=nexus_stability,
            emission_similarity=emission_similarity,
            emission_coherence=emission_coherence,
            confidence_range=confidence_range,
            confidence_stable=confidence_stable,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result)

        return result

    def _print_results(self, result: AbstractionReasoningResult):
        """Print detailed test results."""
        print(f"\n📊 Abstraction Reasoning Metrics:")
        print(f"   Organ activation correlation: {result.organ_activation_correlation:.3f}")
        print(f"   Target: ≥0.70")
        print(f"   Status: {'✅' if result.organ_consistency else '❌'}")

        print(f"\n🔗 Nexus Formation:")
        print(f"   Overlap rate: {result.nexus_overlap_rate:.3f}")
        print(f"   Target: ≥0.60")
        print(f"   Status: {'✅' if result.nexus_stability else '❌'}")

        print(f"\n💬 Emission Coherence:")
        print(f"   Similarity: {result.emission_similarity:.3f}")
        print(f"   Target: ≥0.60")
        print(f"   Status: {'✅' if result.emission_coherence else '❌'}")

        print(f"\n📈 Confidence Stability:")
        print(f"   Range: {result.confidence_range:.3f}")
        print(f"   Target: ≤0.15")
        print(f"   Status: {'✅' if result.confidence_stable else '❌'}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: {result.reasoning}")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_abstraction_reasoning_test(
    pattern_id: Optional[str] = None
) -> bool:
    """Run abstraction reasoning test."""
    tester = AbstractionReasoningTester()
    result = tester.test_abstraction_reasoning(
        pattern_id=pattern_id,
        verbose=True
    )

    return result.success


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test abstraction reasoning")
    parser.add_argument('--pattern', type=str, default=None,
                       help='Pattern to test (scapegoating, witnessing, burnout)')

    args = parser.parse_args()

    success = run_abstraction_reasoning_test(pattern_id=args.pattern)

    sys.exit(0 if success else 1)
