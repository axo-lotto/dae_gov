"""
Intelligence Test: Context Integration (INTEL-004)
==================================================

Tests the organism's ability to track and adapt to evolving context
across multiple conversational turns.

Theoretical Foundation (Multi-Turn Adaptation):
- Context accumulates across turns
- Organ activation should adapt to evolving emotional/relational state
- Emissions should reference and build on previous turns

Test Protocol:
1. Present 3-turn conversation with evolving context
2. Track organ activation changes per turn
3. Measure emission adaptation (novel content per turn)
4. Validate satisfaction increase (deepening engagement)

Success Criteria:
- Context sensitivity: Different organ patterns per turn (≥0.30 correlation change)
- Emission evolution: ≥40% unique words per turn (not repetitive)
- Satisfaction increase: +0.10 by turn 3 (deepening engagement)
- No degradation: Confidence remains ≥0.30 across all turns

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Intelligence Testing)
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


@dataclass
class ContextIntegrationResult:
    """Result of context integration test."""
    scenario_id: str
    turns: int

    # Context sensitivity (organ activation adaptation)
    organ_correlation_change: float  # Max change between turns
    context_sensitive: bool  # ≥0.30 change

    # Emission evolution
    unique_word_rates: List[float]  # % unique words per turn
    emission_evolving: bool  # All turns ≥40% unique

    # Engagement deepening
    satisfaction_trend: List[float]
    satisfaction_increase: float  # Final - initial
    engagement_deepening: bool  # +0.10 by turn 3

    # Stability
    confidence_trend: List[float]
    no_degradation: bool  # All ≥0.30

    # Overall success
    success: bool
    reasoning: str


class ContextIntegrationTester:
    """
    Tests context integration across conversational turns.

    Validates that the organism:
    - Adapts organ activation to evolving context
    - Generates evolving emissions (not repetitive)
    - Deepens engagement over turns
    - Maintains stable confidence
    """

    def __init__(
        self,
        organism: Optional[ConversationalOrganismWrapper] = None
    ):
        """
        Initialize context integration tester.

        Args:
            organism: ConversationalOrganismWrapper instance (or create new)
        """
        if organism is None:
            print("🌀 Initializing organism for context integration test...")
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism

    def _get_multi_turn_scenarios(self) -> Dict[str, List[str]]:
        """
        Get multi-turn conversation scenarios.

        Returns:
            Dict mapping scenario_id to list of turn texts
        """
        return {
            # Scenario 1: Escalating crisis → stabilization
            "crisis_escalation": [
                "I'm feeling a bit overwhelmed with everything on my plate right now.",  # Turn 1: Initial distress
                "It's worse than that. I can't sleep, can't eat. Everything feels impossible. "
                "I'm barely holding it together.",  # Turn 2: Crisis escalation
                "Okay. I think I just needed to say that out loud. I can feel my breathing slowing. "
                "Maybe I can take this one step at a time."  # Turn 3: Stabilization
            ],

            # Scenario 2: Intellectual → emotional deepening
            "intellectual_to_emotional": [
                "I've been thinking about the concept of attachment theory and how it applies to "
                "organizational dynamics.",  # Turn 1: Abstract/intellectual
                "Actually, this isn't just academic curiosity. I think I have an anxious attachment "
                "style at work - always seeking validation from my manager.",  # Turn 2: Personal connection
                "It's exhausting. I'm tired of performing for approval. I want to just... be enough "
                "as I am."  # Turn 3: Emotional core
            ],

            # Scenario 3: Defensive → vulnerable
            "defense_to_vulnerability": [
                "My team is fine. We work well together. No real issues.",  # Turn 1: Defensive
                "Okay, there's some tension. But it's not a big deal. These things happen in teams.",  # Turn 2: Softening
                "The truth is... I feel invisible there. Like my contributions don't matter. "
                "And it hurts more than I want to admit."  # Turn 3: Vulnerable
            ]
        }

    def _extract_organ_vector(self, result: Dict) -> np.ndarray:
        """
        Extract 11D organ activation vector.

        Args:
            result: Organism processing result

        Returns:
            11D numpy array of satisfaction scores
        """
        organ_results = result.get('organ_results', {})
        vector = []

        for organ_name in ['LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',
                         'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD']:
            organ_result = organ_results.get(organ_name)
            if organ_result and hasattr(organ_result, 'satisfaction'):
                satisfaction = organ_result.satisfaction
            else:
                satisfaction = 0.0
            vector.append(satisfaction)

        return np.array(vector)

    def _compute_unique_word_rate(
        self,
        emission: str,
        previous_emissions: List[str]
    ) -> float:
        """
        Compute percentage of unique words in emission vs previous emissions.

        Args:
            emission: Current emission text
            previous_emissions: List of previous emission texts

        Returns:
            Percentage of unique words (0-1)
        """
        current_words = set(emission.lower().split())

        if len(current_words) == 0:
            return 0.0

        if len(previous_emissions) == 0:
            return 1.0  # First emission, all words are unique

        previous_words = set()
        for prev in previous_emissions:
            previous_words.update(prev.lower().split())

        unique_words = current_words - previous_words
        return len(unique_words) / len(current_words)

    def test_context_integration(
        self,
        scenario_id: Optional[str] = None,
        verbose: bool = True
    ) -> ContextIntegrationResult:
        """
        Test context integration on a multi-turn scenario.

        Args:
            scenario_id: Scenario to test (or random if None)
            verbose: Print detailed results

        Returns:
            ContextIntegrationResult with metrics and success status
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"🔄 CONTEXT INTEGRATION TEST (INTEL-004)")
            print(f"{'='*70}")
            print(f"\nTesting: Multi-turn context tracking and adaptation")

        # Get scenarios
        scenarios = self._get_multi_turn_scenarios()

        if scenario_id is None:
            scenario_id = list(scenarios.keys())[0]

        if scenario_id not in scenarios:
            raise ValueError(f"Unknown scenario: {scenario_id}")

        turns = scenarios[scenario_id]

        if verbose:
            print(f"Scenario: {scenario_id}")
            print(f"Turns: {len(turns)}")

        # Process each turn
        organ_vectors = []
        satisfactions = []
        confidences = []
        emissions = []

        for i, turn_text in enumerate(turns):
            if verbose:
                print(f"\n📊 Turn {i+1}/{len(turns)}:")
                print(f"   Input: {turn_text[:80]}...")

            result = self.organism.process_text(
                text=turn_text,
                enable_phase2=True,
                enable_tsk_recording=False
            )

            # Extract metrics
            organ_vector = self._extract_organ_vector(result)
            felt_states = result.get('felt_states', {})
            satisfaction = felt_states.get('satisfaction_final', 0.0)
            confidence = felt_states.get('emission_confidence', 0.0)
            emission = result.get('emission', '')

            organ_vectors.append(organ_vector)
            satisfactions.append(satisfaction)
            confidences.append(confidence)
            emissions.append(emission)

            if verbose:
                active_organs = np.sum(organ_vector > 0.1)
                print(f"   Active organs: {active_organs}/11")
                print(f"   Satisfaction: {satisfaction:.3f}")
                print(f"   Confidence: {confidence:.3f}")
                print(f"   Emission: {emission[:80]}...")

        # Compute organ correlation changes
        correlations = []
        for i in range(len(organ_vectors) - 1):
            corr = np.corrcoef(organ_vectors[i], organ_vectors[i+1])[0, 1]
            if not np.isnan(corr):
                correlations.append(abs(1.0 - corr))  # Distance from perfect correlation

        organ_correlation_change = max(correlations) if len(correlations) > 0 else 0.0

        # Compute unique word rates
        unique_word_rates = []
        for i, emission in enumerate(emissions):
            rate = self._compute_unique_word_rate(emission, emissions[:i])
            unique_word_rates.append(rate)

        # Compute satisfaction trend
        satisfaction_increase = satisfactions[-1] - satisfactions[0] if len(satisfactions) > 1 else 0.0

        # Success criteria
        context_sensitive = organ_correlation_change >= 0.30
        emission_evolving = all(rate >= 0.40 for rate in unique_word_rates)
        engagement_deepening = satisfaction_increase >= 0.10
        no_degradation = all(conf >= 0.30 for conf in confidences)

        success = (
            context_sensitive and
            emission_evolving and
            engagement_deepening and
            no_degradation
        )

        # Reasoning
        if success:
            reasoning = f"Context integrated: {len(turns)} turns with adaptation and deepening"
        else:
            reasons = []
            if not context_sensitive:
                reasons.append(f"Low context sensitivity: max correlation change {organ_correlation_change:.2f} < 0.30")
            if not emission_evolving:
                min_unique = min(unique_word_rates) if unique_word_rates else 0.0
                reasons.append(f"Repetitive emissions: min unique rate {min_unique:.2f} < 0.40")
            if not engagement_deepening:
                reasons.append(f"No deepening: satisfaction change {satisfaction_increase:+.2f} < +0.10")
            if not no_degradation:
                min_conf = min(confidences) if confidences else 0.0
                reasons.append(f"Confidence degradation: min {min_conf:.2f} < 0.30")
            reasoning = "; ".join(reasons)

        result = ContextIntegrationResult(
            scenario_id=scenario_id,
            turns=len(turns),
            organ_correlation_change=organ_correlation_change,
            context_sensitive=context_sensitive,
            unique_word_rates=unique_word_rates,
            emission_evolving=emission_evolving,
            satisfaction_trend=satisfactions,
            satisfaction_increase=satisfaction_increase,
            engagement_deepening=engagement_deepening,
            confidence_trend=confidences,
            no_degradation=no_degradation,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result)

        return result

    def _print_results(self, result: ContextIntegrationResult):
        """Print detailed test results."""
        print(f"\n📊 Context Integration Metrics:")

        print(f"\n🧬 Context Sensitivity:")
        print(f"   Organ correlation change: {result.organ_correlation_change:.3f}")
        print(f"   Target: ≥0.30")
        print(f"   Status: {'✅' if result.context_sensitive else '❌'}")

        print(f"\n💬 Emission Evolution:")
        for i, rate in enumerate(result.unique_word_rates):
            print(f"   Turn {i+1} unique words: {rate:.1%}")
        print(f"   Target: ≥40% per turn")
        print(f"   Status: {'✅' if result.emission_evolving else '❌'}")

        print(f"\n📈 Engagement Deepening:")
        for i, sat in enumerate(result.satisfaction_trend):
            marker = "📍" if i == 0 else ("🎯" if i == len(result.satisfaction_trend) - 1 else "  ")
            print(f"   {marker} Turn {i+1}: {sat:.3f}")
        print(f"   Change: {result.satisfaction_increase:+.3f}")
        print(f"   Target: +0.10")
        print(f"   Status: {'✅' if result.engagement_deepening else '❌'}")

        print(f"\n🛡️  Stability:")
        print(f"   Confidence range: [{min(result.confidence_trend):.3f}, {max(result.confidence_trend):.3f}]")
        print(f"   Target: All ≥0.30")
        print(f"   Status: {'✅' if result.no_degradation else '❌'}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: {result.reasoning}")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_context_integration_test(
    scenario_id: Optional[str] = None
) -> bool:
    """Run context integration test."""
    tester = ContextIntegrationTester()
    result = tester.test_context_integration(
        scenario_id=scenario_id,
        verbose=True
    )

    return result.success


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test context integration")
    parser.add_argument('--scenario', type=str, default=None,
                       help='Scenario to test (crisis_escalation, intellectual_to_emotional, defense_to_vulnerability)')

    args = parser.parse_args()

    success = run_context_integration_test(scenario_id=args.scenario)

    sys.exit(0 if success else 1)
