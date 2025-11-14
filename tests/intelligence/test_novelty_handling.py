"""
Intelligence Test: Novelty Handling (INTEL-003)
===============================================

Tests the organism's ability to gracefully handle completely novel inputs
that have no matches in the training corpus.

Theoretical Foundation (Graceful Degradation):
- Novel inputs should activate general vs. specific organs
- Should fall back to hebbian strategy appropriately
- Should express appropriate uncertainty (not overconfident)

Test Protocol:
1. Present inputs with no training corpus similarity
2. Measure organ participation breadth
3. Validate emission strategy (should use hebbian fallback)
4. Check confidence calibration (appropriate uncertainty)

Success Criteria:
- No crashes/exceptions on novel input
- ≥5 organs active (general response, not over-specialized)
- Emission strategy: hebbian_fallback (appropriate for uncertainty)
- Confidence in range [0.20, 0.40] (appropriate uncertainty, not collapsed or overconfident)

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Intelligence Testing)
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


@dataclass
class NoveltyHandlingResult:
    """Result of novelty handling test."""
    input_text: str
    novelty_level: str  # "moderate", "high", "extreme"

    # System stability
    processed_successfully: bool
    exception_raised: bool
    exception_message: str

    # Organ participation
    active_organs: int  # Count with satisfaction > 0.1
    general_response: bool  # ≥5 organs active

    # Emission strategy
    emission_strategy: str
    appropriate_strategy: bool  # hebbian_fallback expected

    # Confidence calibration
    confidence: float
    confidence_calibrated: bool  # In range [0.20, 0.40]

    # Overall success
    success: bool
    reasoning: str


class NoveltyHandlingTester:
    """
    Tests novelty handling on out-of-distribution inputs.

    Validates that the organism:
    - Doesn't crash on novel inputs
    - Activates general organs (not overspecialized)
    - Uses appropriate fallback strategies
    - Expresses appropriate uncertainty
    """

    def __init__(
        self,
        organism: Optional[ConversationalOrganismWrapper] = None
    ):
        """
        Initialize novelty handling tester.

        Args:
            organism: ConversationalOrganismWrapper instance (or create new)
        """
        if organism is None:
            print("🌀 Initializing organism for novelty handling test...")
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism

    def _get_novel_inputs(self) -> Dict[str, Dict]:
        """
        Get novel inputs at different novelty levels.

        Returns:
            Dict mapping novelty_id to input spec
        """
        return {
            # Moderate novelty: Topic shift but emotional/relational structure recognizable
            "quantum_grief": {
                "level": "moderate",
                "text": "I'm experiencing quantum superposition grief - simultaneously mourning "
                       "the collapse of all possible futures that didn't actualize. Every decision "
                       "is a wave function collapse that kills infinite parallel selves.",
                "description": "Physics metaphor for grief/regret, but emotional core recognizable"
            },

            # High novelty: Abstract mathematical framing of relational dynamics
            "topology_intimacy": {
                "level": "high",
                "text": "Our relationship has a non-orientable topology - like a Möbius strip, "
                       "there's no clear inside or outside, self or other. Every attempt to establish "
                       "boundaries loops back into entanglement. The genus of our connection space is ambiguous.",
                "description": "Topological metaphor for enmeshment, very abstract"
            },

            # Extreme novelty: Pure technical content, no emotional valence
            "algorithm_efficiency": {
                "level": "extreme",
                "text": "The time complexity of merge sort is O(n log n) in all cases, whereas "
                       "quicksort averages O(n log n) but degrades to O(n²) on already-sorted arrays. "
                       "For in-place sorting with guaranteed performance, heapsort is optimal.",
                "description": "Pure algorithm analysis, no relational/emotional content"
            },

            # Extreme novelty: Sensory experience description
            "synesthesia": {
                "level": "extreme",
                "text": "The number seven tastes like copper and smells purple. Monday mornings "
                       "have a texture like velvet but sound like breaking glass. Every word you speak "
                       "creates geometric shapes that float in the air - triangles for verbs, spirals for emotions.",
                "description": "Synesthetic perception, no clear emotional or relational frame"
            },

            # Moderate novelty: Cultural context shift
            "ritual_belonging": {
                "level": "moderate",
                "text": "During the Sukkot harvest festival, dwelling in temporary structures reminds us "
                       "that all belonging is provisional. The fragility of the sukkah's walls mirrors the "
                       "impermanence of community. We're always just passing through.",
                "description": "Specific cultural/religious frame, but themes of impermanence/belonging recognizable"
            }
        }

    def test_novelty_handling(
        self,
        novelty_id: Optional[str] = None,
        verbose: bool = True
    ) -> NoveltyHandlingResult:
        """
        Test novelty handling on a novel input.

        Args:
            novelty_id: Novelty scenario to test (or random if None)
            verbose: Print detailed results

        Returns:
            NoveltyHandlingResult with metrics and success status
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"🆕 NOVELTY HANDLING TEST (INTEL-003)")
            print(f"{'='*70}")
            print(f"\nTesting: Graceful degradation on out-of-distribution inputs")

        # Get novel inputs
        novel_inputs = self._get_novel_inputs()

        if novelty_id is None:
            novelty_id = list(novel_inputs.keys())[0]

        if novelty_id not in novel_inputs:
            raise ValueError(f"Unknown novelty scenario: {novelty_id}")

        spec = novel_inputs[novelty_id]
        input_text = spec["text"]
        novelty_level = spec["level"]

        if verbose:
            print(f"Novelty scenario: {novelty_id}")
            print(f"Level: {novelty_level}")
            print(f"Description: {spec['description']}")
            print(f"\nInput: {input_text[:120]}...")

        # Attempt to process
        processed_successfully = False
        exception_raised = False
        exception_message = ""
        result = None

        try:
            if verbose:
                print(f"\n📊 Processing novel input...")

            result = self.organism.process_text(
                text=input_text,
                enable_phase2=True,
                enable_tsk_recording=False
            )

            processed_successfully = True

            if verbose:
                print(f"   ✅ Processed successfully (no crash)")

        except Exception as e:
            exception_raised = True
            exception_message = str(e)
            if verbose:
                print(f"   ❌ Exception raised: {exception_message}")

        # Extract metrics if processing succeeded
        if processed_successfully and result:
            # Count active organs
            organ_results = result.get('organ_results', {})
            active_count = 0

            for organ_name in ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                             'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']:
                organ_result = organ_results.get(organ_name)
                if organ_result:
                    # Check coherence (most organs) or attention_score
                    coherence = getattr(organ_result, 'coherence', 0.0)
                    if coherence > 0.1:
                        active_count += 1

            # Get emission strategy (strategy is in emission_path, not felt_states)
            emission_path = result.get('emission_path', 'unknown')
            emission_strategy = emission_path if emission_path else 'unknown'

            # Get confidence from top-level result, not felt_states
            confidence = result.get('emission_confidence', 0.0)

            if verbose:
                print(f"   Active organs: {active_count}/11")
                print(f"   Emission strategy: {emission_strategy}")
                print(f"   Confidence: {confidence:.3f}")

        else:
            active_count = 0
            emission_strategy = "none"
            confidence = 0.0

        # Success criteria
        general_response = active_count >= 5
        appropriate_strategy = emission_strategy == "hebbian_fallback"
        confidence_calibrated = 0.20 <= confidence <= 0.40

        success = (
            processed_successfully and
            general_response and
            appropriate_strategy and
            confidence_calibrated
        )

        # Reasoning
        if success:
            reasoning = f"Novelty handled gracefully: {active_count} organs active, appropriate uncertainty"
        else:
            reasons = []
            if not processed_successfully:
                reasons.append(f"System crash: {exception_message}")
            if not general_response:
                reasons.append(f"Overspecialized: only {active_count} organs active (need ≥5)")
            if not appropriate_strategy:
                reasons.append(f"Inappropriate strategy: {emission_strategy} (expected hebbian_fallback)")
            if not confidence_calibrated:
                reasons.append(f"Miscalibrated confidence: {confidence:.2f} (expected 0.20-0.40)")
            reasoning = "; ".join(reasons)

        result = NoveltyHandlingResult(
            input_text=input_text[:100],
            novelty_level=novelty_level,
            processed_successfully=processed_successfully,
            exception_raised=exception_raised,
            exception_message=exception_message,
            active_organs=active_count,
            general_response=general_response,
            emission_strategy=emission_strategy,
            appropriate_strategy=appropriate_strategy,
            confidence=confidence,
            confidence_calibrated=confidence_calibrated,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result)

        return result

    def _print_results(self, result: NoveltyHandlingResult):
        """Print detailed test results."""
        print(f"\n📊 Novelty Handling Metrics:")

        print(f"\n🛡️  System Stability:")
        print(f"   Processed successfully: {'✅' if result.processed_successfully else '❌'}")
        if result.exception_raised:
            print(f"   Exception: {result.exception_message[:80]}")

        print(f"\n🧬 Organ Participation:")
        print(f"   Active organs: {result.active_organs}/11")
        print(f"   Target: ≥5 (general response)")
        print(f"   Status: {'✅' if result.general_response else '❌'}")

        print(f"\n💬 Emission Strategy:")
        print(f"   Strategy: {result.emission_strategy}")
        print(f"   Target: hebbian_fallback")
        print(f"   Status: {'✅' if result.appropriate_strategy else '❌'}")

        print(f"\n📈 Confidence Calibration:")
        print(f"   Confidence: {result.confidence:.3f}")
        print(f"   Target: [0.20, 0.40]")
        print(f"   Status: {'✅' if result.confidence_calibrated else '❌'}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: {result.reasoning}")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_novelty_handling_test(
    novelty_id: Optional[str] = None
) -> bool:
    """Run novelty handling test."""
    tester = NoveltyHandlingTester()
    result = tester.test_novelty_handling(
        novelty_id=novelty_id,
        verbose=True
    )

    return result.success


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test novelty handling")
    parser.add_argument('--novelty', type=str, default=None,
                       help='Novelty scenario to test (quantum_grief, topology_intimacy, algorithm_efficiency, synesthesia, ritual_belonging)')

    args = parser.parse_args()

    success = run_novelty_handling_test(novelty_id=args.novelty)

    sys.exit(0 if success else 1)
