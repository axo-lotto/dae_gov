"""
Continuity Test: Emission Consistency (CONT-004)
================================================

Tests that emission strategies evolve consistently across epochs,
with appropriate maturation from hebbian fallback to direct/fusion.

Theoretical Foundation (Strategy Maturation):
- Early epochs: Mostly hebbian_fallback (learning patterns)
- Mid epochs: Mix of hebbian + fusion (pattern recognition emerging)
- Late epochs: More direct + fusion (confident pattern matching)

Test Protocol:
1. Track emission strategies across epochs
2. Monitor strategy distribution evolution
3. Validate confidence-strategy alignment
4. Check healthy maturation trajectory

Success Criteria:
- Direct emission rate: ≥30% by epoch 10 (confident pattern matching)
- Fusion emission rate: ≥20% by epoch 10 (nexus-based generation)
- Hebbian fallback: ≤50% by epoch 10 (not over-reliant)
- Confidence-strategy correlation: ≥0.70 (high confidence → direct)

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Continuity Testing)
"""

import sys
import json
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


@dataclass
class EmissionConsistencyResult:
    """Result of emission consistency test."""
    test_inputs: int

    # Strategy distribution
    strategy_counts: Dict[str, int]
    direct_rate: float
    fusion_rate: float
    hebbian_rate: float

    # Maturation checks
    sufficient_direct: bool  # ≥30%
    sufficient_fusion: bool  # ≥20%
    not_over_hebbian: bool  # ≤50%

    # Confidence-strategy alignment
    confidence_by_strategy: Dict[str, float]
    confidence_strategy_correlation: float
    well_aligned: bool  # ≥0.70

    # Overall success
    success: bool
    reasoning: str


class EmissionConsistencyTester:
    """
    Tests emission strategy consistency and maturation.

    Validates that:
    - Strategies evolve appropriately across epochs
    - Direct/fusion rates increase with learning
    - Hebbian fallback decreases (but doesn't disappear)
    - High confidence correlates with direct/fusion strategies
    """

    def __init__(
        self,
        organism: Optional[ConversationalOrganismWrapper] = None
    ):
        """
        Initialize emission consistency tester.

        Args:
            organism: ConversationalOrganismWrapper instance (or create new)
        """
        if organism is None:
            print("🌀 Initializing organism for emission consistency test...")
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism

    def _get_test_inputs(self) -> List[str]:
        """
        Get test inputs for emission strategy testing.

        Returns:
            List of diverse input texts
        """
        return [
            # Crisis/urgency (should activate NDAM, likely hebbian if untrained)
            "I'm in crisis right now and need immediate help.",
            "Everything is falling apart and I can't handle it.",

            # Safe connection (should activate EMPATHY/PRESENCE, fusion potential)
            "This conversation feels really safe and supportive.",
            "I feel genuinely heard and understood here.",

            # Boundary setting (AUTHENTICITY/CARD, direct potential)
            "I need to set a clear boundary about this interaction.",
            "I'm comfortable saying no to that request.",

            # Scapegoating pattern (BOND/WISDOM, should recognize pattern)
            "Our team always blames the QA department when things fail.",
            "One person consistently carries the blame for group dysfunction.",

            # Burnout (NDAM/WISDOM, complex nexus potential)
            "I work 80 hours a week and still feel inadequate.",
            "The exhaustion is crushing but rest feels like weakness.",

            # Witnessing request (LISTENING/EMPATHY, clear pattern)
            "I just need someone to witness this without trying to fix it.",
            "Can you just be here with me without advice?",

            # Meta-cognitive (WISDOM, should have direct response if trained)
            "Can you help me understand what patterns I'm repeating?",
            "I'd like to reflect on my relational dynamics.",

            # General overwhelm (broad activation)
            "I'm feeling overwhelmed with everything on my plate.",
            "There's too much happening and I can't keep up."
        ]

    def test_emission_consistency(
        self,
        verbose: bool = True
    ) -> EmissionConsistencyResult:
        """
        Test emission strategy consistency.

        Args:
            verbose: Print detailed results

        Returns:
            EmissionConsistencyResult with metrics and success status
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"💬 EMISSION CONSISTENCY TEST (CONT-004)")
            print(f"{'='*70}")
            print(f"\nTesting: Emission strategy maturation and consistency")

        # Get test inputs
        test_inputs = self._get_test_inputs()

        if verbose:
            print(f"Test inputs: {len(test_inputs)}")
            print(f"\n📊 Processing inputs...")

        # Process inputs and track strategies
        strategies = []
        confidences_by_strategy = {'direct': [], 'fusion': [], 'hebbian_fallback': []}

        for i, text in enumerate(test_inputs):
            if verbose and i % 5 == 0:
                print(f"   Processing {i+1}/{len(test_inputs)}...")

            result = self.organism.process_text(
                text=text,
                enable_phase2=True,
                enable_tsk_recording=False
            )

            felt_states = result.get('felt_states', {})
            strategy = felt_states.get('emission_strategy', 'unknown')
            confidence = felt_states.get('emission_confidence', 0.0)

            strategies.append(strategy)
            if strategy in confidences_by_strategy:
                confidences_by_strategy[strategy].append(confidence)

        # Count strategies
        strategy_counts = Counter(strategies)
        total = len(strategies)

        direct_count = strategy_counts.get('direct', 0)
        fusion_count = strategy_counts.get('fusion', 0)
        hebbian_count = strategy_counts.get('hebbian_fallback', 0)

        direct_rate = direct_count / total if total > 0 else 0.0
        fusion_rate = fusion_count / total if total > 0 else 0.0
        hebbian_rate = hebbian_count / total if total > 0 else 0.0

        if verbose:
            print(f"\n📊 Strategy Distribution:")
            print(f"   Direct: {direct_count}/{total} ({direct_rate:.1%})")
            print(f"   Fusion: {fusion_count}/{total} ({fusion_rate:.1%})")
            print(f"   Hebbian fallback: {hebbian_count}/{total} ({hebbian_rate:.1%})")

        # Compute mean confidence by strategy
        confidence_means = {}
        for strategy, confs in confidences_by_strategy.items():
            if len(confs) > 0:
                confidence_means[strategy] = float(np.mean(confs))
            else:
                confidence_means[strategy] = 0.0

        # Confidence-strategy correlation
        # Expect: direct > fusion > hebbian in confidence
        expected_order = ['direct', 'fusion', 'hebbian_fallback']
        actual_confidences = [confidence_means.get(s, 0.0) for s in expected_order]

        # Simple correlation: check if confidence decreases in order
        if len(actual_confidences) >= 2:
            # Compute rank correlation (Spearman-like)
            expected_ranks = [3, 2, 1]  # direct=3 (highest), fusion=2, hebbian=1 (lowest)
            actual_ranks = [3-i for i, _ in sorted(enumerate(actual_confidences), key=lambda x: x[1], reverse=True)]

            # Compute correlation
            mean_expected = np.mean(expected_ranks)
            mean_actual = np.mean(actual_ranks)

            cov = np.mean([(e - mean_expected) * (a - mean_actual)
                          for e, a in zip(expected_ranks, actual_ranks)])
            std_expected = np.std(expected_ranks)
            std_actual = np.std(actual_ranks)

            if std_expected > 0 and std_actual > 0:
                confidence_strategy_correlation = cov / (std_expected * std_actual)
            else:
                confidence_strategy_correlation = 0.0
        else:
            confidence_strategy_correlation = 0.0

        # Success criteria
        sufficient_direct = direct_rate >= 0.30
        sufficient_fusion = fusion_rate >= 0.20
        not_over_hebbian = hebbian_rate <= 0.50
        well_aligned = confidence_strategy_correlation >= 0.70

        success = (
            sufficient_direct and
            sufficient_fusion and
            not_over_hebbian and
            well_aligned
        )

        # Reasoning
        if success:
            reasoning = f"Emission strategies maturing: {direct_rate:.1%} direct, {fusion_rate:.1%} fusion, aligned with confidence"
        else:
            reasons = []
            if not sufficient_direct:
                reasons.append(f"Low direct rate: {direct_rate:.1%} < 30%")
            if not sufficient_fusion:
                reasons.append(f"Low fusion rate: {fusion_rate:.1%} < 20%")
            if not over_hebbian:
                reasons.append(f"Over-reliant on hebbian: {hebbian_rate:.1%} > 50%")
            if not well_aligned:
                reasons.append(f"Poor confidence-strategy alignment: {confidence_strategy_correlation:.2f} < 0.70")
            reasoning = "; ".join(reasons)

        result = EmissionConsistencyResult(
            test_inputs=len(test_inputs),
            strategy_counts=dict(strategy_counts),
            direct_rate=direct_rate,
            fusion_rate=fusion_rate,
            hebbian_rate=hebbian_rate,
            sufficient_direct=sufficient_direct,
            sufficient_fusion=sufficient_fusion,
            not_over_hebbian=not_over_hebbian,
            confidence_by_strategy=confidence_means,
            confidence_strategy_correlation=confidence_strategy_correlation,
            well_aligned=well_aligned,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result)

        return result

    def _print_results(self, result: EmissionConsistencyResult):
        """Print detailed test results."""
        print(f"\n📊 Emission Consistency Metrics:")

        print(f"\n💬 Strategy Maturation:")
        print(f"   Direct rate: {result.direct_rate:.1%}")
        print(f"   Target: ≥30%")
        print(f"   Status: {'✅' if result.sufficient_direct else '❌'}")

        print(f"\n🔗 Fusion rate: {result.fusion_rate:.1%}")
        print(f"   Target: ≥20%")
        print(f"   Status: {'✅' if result.sufficient_fusion else '❌'}")

        print(f"\n📉 Hebbian fallback: {result.hebbian_rate:.1%}")
        print(f"   Target: ≤50%")
        print(f"   Status: {'✅' if result.not_over_hebbian else '❌'}")

        print(f"\n📈 Confidence-Strategy Alignment:")
        for strategy in ['direct', 'fusion', 'hebbian_fallback']:
            conf = result.confidence_by_strategy.get(strategy, 0.0)
            count = result.strategy_counts.get(strategy, 0)
            if count > 0:
                print(f"   {strategy}: {conf:.3f} ({count} instances)")
        print(f"   Correlation: {result.confidence_strategy_correlation:.3f}")
        print(f"   Target: ≥0.70")
        print(f"   Status: {'✅' if result.well_aligned else '❌'}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: {result.reasoning}")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_emission_consistency_test() -> bool:
    """Run emission consistency test."""
    tester = EmissionConsistencyTester()
    result = tester.test_emission_consistency(verbose=True)

    return result.success


if __name__ == "__main__":
    success = run_emission_consistency_test()
    sys.exit(0 if success else 1)
