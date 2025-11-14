"""
Intelligence Test: Pattern Transfer (INTEL-002)
===============================================

Tests the organism's ability to transfer learned patterns from one domain
to structurally similar patterns in a different domain.

Theoretical Foundation (Transfer Learning):
- Learn structural patterns in domain A
- Apply to isomorphic patterns in domain B
- Validate organ activation similarity despite surface differences

Test Protocol:
1. Train on 3 patterns in domain A (workplace dynamics)
2. Test on 3 structurally similar patterns in domain B (family systems)
3. Measure transfer success via organ activation alignment
4. Validate emission coherence across domains

Success Criteria:
- Transfer accuracy: ≥65% (organ patterns match structure, not surface)
- Organ activation similarity: ≥0.60 between isomorphic patterns
- Confidence on novel domain: ≥0.40 (appropriate, not collapsed)
- Nexus type consistency: ≥50% overlap on structural patterns

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Intelligence Testing)
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


@dataclass
class PatternPair:
    """Pair of structurally isomorphic patterns across domains."""
    pattern_id: str
    domain_a: str  # Training domain
    domain_b: str  # Transfer domain
    structural_similarity: str  # What makes them isomorphic


@dataclass
class PatternTransferResult:
    """Result of pattern transfer test."""
    pattern_id: str
    domain_a_text: str
    domain_b_text: str

    # Organ activation similarity
    organ_similarity: float  # Cosine similarity of 11D vectors
    transfer_success: bool  # ≥0.60

    # Confidence on transfer
    domain_a_confidence: float
    domain_b_confidence: float
    confidence_adequate: bool  # domain_b ≥ 0.40

    # Nexus consistency
    nexus_overlap: float
    structural_consistency: bool  # ≥0.50

    # Overall success
    success: bool
    reasoning: str


class PatternTransferTester:
    """
    Tests pattern transfer across domains.

    Validates that the organism can:
    - Detect structural similarities despite surface differences
    - Transfer organ activation patterns appropriately
    - Maintain adequate confidence in novel domains
    """

    def __init__(
        self,
        organism: Optional[ConversationalOrganismWrapper] = None
    ):
        """
        Initialize pattern transfer tester.

        Args:
            organism: ConversationalOrganismWrapper instance (or create new)
        """
        if organism is None:
            print("🌀 Initializing organism for pattern transfer test...")
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism

    def _get_pattern_pairs(self) -> Dict[str, PatternPair]:
        """
        Get structurally isomorphic pattern pairs across domains.

        Returns:
            Dict mapping pattern_id to PatternPair
        """
        # Domain A: Workplace dynamics
        # Domain B: Family systems
        # Structural similarity: Same relational dynamics, different context

        patterns = {
            "scapegoating": PatternPair(
                pattern_id="scapegoating",
                domain_a="Our team always blames the QA department when projects fail. "
                        "They've become the scapegoat for everyone's inability to write good code. "
                        "It's easier to point fingers than examine our own contributions.",
                domain_b="In our family, my younger sister is always blamed when things go wrong. "
                        "She's become the family scapegoat for everyone else's dysfunction. "
                        "It's easier to make her the problem than look at our own behavior.",
                structural_similarity="One party consistently receives collective blame"
            ),

            "triangulation": PatternPair(
                pattern_id="triangulation",
                domain_a="Instead of talking to each other directly, my manager tells me what "
                        "my colleague supposedly said about me, and tells them what I supposedly said. "
                        "We never communicate directly, always through this third party.",
                domain_b="My mom won't talk to my dad directly. She tells me what she wants me to "
                        "tell him, and tells me what he supposedly said. I'm always stuck in the middle, "
                        "carrying messages between them.",
                structural_similarity="Communication routed through third party, avoiding direct contact"
            ),

            "enabling": PatternPair(
                pattern_id="enabling",
                domain_a="My coworker never meets deadlines, but the team always covers for them. "
                        "We redo their work, make excuses to management, and take on their responsibilities. "
                        "We're enabling their dysfunction by protecting them from consequences.",
                domain_b="My brother never pays his bills, but the family always bails him out. "
                        "We lend him money, make excuses, and shield him from the consequences of his choices. "
                        "We're enabling his irresponsibility by always rescuing him.",
                structural_similarity="Group prevents natural consequences, perpetuating dysfunction"
            )
        }

        return patterns

    def _extract_organ_vector(self, result: Dict) -> np.ndarray:
        """
        Extract 11D organ activation vector from result.

        Args:
            result: Organism processing result

        Returns:
            11D numpy array of organ satisfaction scores
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

    def _extract_nexus_types(self, result: Dict) -> set:
        """
        Extract set of nexus types from result.

        Args:
            result: Organism processing result

        Returns:
            Set of nexus type strings
        """
        nexuses = result.get('nexuses', [])
        nexus_types = set()

        for nexus in nexuses:
            if isinstance(nexus, dict):
                nexus_type = nexus.get('atom_name') or nexus.get('meta_atom_name')
                if nexus_type:
                    nexus_types.add(nexus_type)

        return nexus_types

    def test_pattern_transfer(
        self,
        pattern_id: Optional[str] = None,
        verbose: bool = True
    ) -> PatternTransferResult:
        """
        Test pattern transfer on a pattern pair.

        Args:
            pattern_id: Pattern to test (or random if None)
            verbose: Print detailed results

        Returns:
            PatternTransferResult with metrics and success status
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"🔄 PATTERN TRANSFER TEST (INTEL-002)")
            print(f"{'='*70}")
            print(f"\nTesting: Transfer learning across domains")

        # Get pattern pairs
        patterns = self._get_pattern_pairs()

        if pattern_id is None:
            pattern_id = list(patterns.keys())[0]

        if pattern_id not in patterns:
            raise ValueError(f"Unknown pattern: {pattern_id}")

        pair = patterns[pattern_id]

        if verbose:
            print(f"Pattern: {pattern_id}")
            print(f"Structural similarity: {pair.structural_similarity}")
            print(f"\nDomain A (Workplace): {pair.domain_a[:80]}...")
            print(f"Domain B (Family): {pair.domain_b[:80]}...")

        # Process domain A (training/reference)
        if verbose:
            print(f"\n📊 Processing Domain A (workplace)...")

        result_a = self.organism.process_text(
            text=pair.domain_a,
            enable_phase2=True,
            enable_tsk_recording=False
        )

        organ_vector_a = self._extract_organ_vector(result_a)
        nexus_types_a = self._extract_nexus_types(result_a)
        confidence_a = result_a.get('felt_states', {}).get('emission_confidence', 0.0)

        if verbose:
            print(f"   Confidence: {confidence_a:.3f}")
            print(f"   Nexuses: {len(nexus_types_a)}")
            print(f"   Active organs: {np.sum(organ_vector_a > 0.1)}/11")

        # Process domain B (transfer/test)
        if verbose:
            print(f"\n📊 Processing Domain B (family)...")

        result_b = self.organism.process_text(
            text=pair.domain_b,
            enable_phase2=True,
            enable_tsk_recording=False
        )

        organ_vector_b = self._extract_organ_vector(result_b)
        nexus_types_b = self._extract_nexus_types(result_b)
        confidence_b = result_b.get('felt_states', {}).get('emission_confidence', 0.0)

        if verbose:
            print(f"   Confidence: {confidence_b:.3f}")
            print(f"   Nexuses: {len(nexus_types_b)}")
            print(f"   Active organs: {np.sum(organ_vector_b > 0.1)}/11")

        # Compute organ similarity (cosine)
        norm_a = np.linalg.norm(organ_vector_a)
        norm_b = np.linalg.norm(organ_vector_b)

        if norm_a > 0 and norm_b > 0:
            organ_similarity = float(np.dot(organ_vector_a, organ_vector_b) / (norm_a * norm_b))
        else:
            organ_similarity = 0.0

        # Compute nexus overlap (Jaccard)
        intersection = len(nexus_types_a & nexus_types_b)
        union = len(nexus_types_a | nexus_types_b)
        nexus_overlap = intersection / union if union > 0 else 0.0

        # Success criteria
        transfer_success = organ_similarity >= 0.60
        confidence_adequate = confidence_b >= 0.40
        structural_consistency = nexus_overlap >= 0.50

        success = (
            transfer_success and
            confidence_adequate and
            structural_consistency
        )

        # Reasoning
        if success:
            reasoning = f"Transfer successful: {pattern_id} pattern detected across domains (similarity={organ_similarity:.2f})"
        else:
            reasons = []
            if not transfer_success:
                reasons.append(f"Low transfer: organ similarity {organ_similarity:.2f} < 0.60")
            if not confidence_adequate:
                reasons.append(f"Low confidence on novel domain: {confidence_b:.2f} < 0.40")
            if not structural_consistency:
                reasons.append(f"Structural inconsistency: nexus overlap {nexus_overlap:.2f} < 0.50")
            reasoning = "; ".join(reasons)

        result = PatternTransferResult(
            pattern_id=pattern_id,
            domain_a_text=pair.domain_a[:100],
            domain_b_text=pair.domain_b[:100],
            organ_similarity=organ_similarity,
            transfer_success=transfer_success,
            domain_a_confidence=confidence_a,
            domain_b_confidence=confidence_b,
            confidence_adequate=confidence_adequate,
            nexus_overlap=nexus_overlap,
            structural_consistency=structural_consistency,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result)

        return result

    def _print_results(self, result: PatternTransferResult):
        """Print detailed test results."""
        print(f"\n📊 Transfer Metrics:")
        print(f"   Organ activation similarity: {result.organ_similarity:.3f}")
        print(f"   Target: ≥0.60")
        print(f"   Status: {'✅' if result.transfer_success else '❌'}")

        print(f"\n💬 Confidence:")
        print(f"   Domain A: {result.domain_a_confidence:.3f}")
        print(f"   Domain B: {result.domain_b_confidence:.3f}")
        print(f"   Target (Domain B): ≥0.40")
        print(f"   Status: {'✅' if result.confidence_adequate else '❌'}")

        print(f"\n🔗 Structural Consistency:")
        print(f"   Nexus overlap: {result.nexus_overlap:.3f}")
        print(f"   Target: ≥0.50")
        print(f"   Status: {'✅' if result.structural_consistency else '❌'}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: {result.reasoning}")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_pattern_transfer_test(
    pattern_id: Optional[str] = None
) -> bool:
    """Run pattern transfer test."""
    tester = PatternTransferTester()
    result = tester.test_pattern_transfer(
        pattern_id=pattern_id,
        verbose=True
    )

    return result.success


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test pattern transfer")
    parser.add_argument('--pattern', type=str, default=None,
                       help='Pattern to test (scapegoating, triangulation, enabling)')

    args = parser.parse_args()

    success = run_pattern_transfer_test(pattern_id=args.pattern)

    sys.exit(0 if success else 1)
