"""
Continuity Test: Semantic Atom Drift (CONT-005)
===============================================

Tests that semantic atoms remain stable across epochs, without
catastrophic drift or collapse to a few dominant patterns.

Theoretical Foundation (Semantic Stability):
- Semantic atoms should maintain consistent activation patterns
- No catastrophic forgetting (atoms shouldn't disappear)
- Diversity should be maintained (not collapse to few atoms)
- Correlation between early/late should be high (stable meanings)

Test Protocol:
1. Process test inputs at early epoch (e.g., 1)
2. Process same inputs at late epoch (e.g., 10)
3. Compare atom activation patterns
4. Check for catastrophic drift or collapse

Success Criteria:
- Atom activation correlation: ≥0.75 (stable across epochs)
- No dead atoms: All atoms used ≥10% threshold
- Diversity maintained: ≥40 of 77 atoms active
- No runaway atoms: No single atom >30% of total activation

Author: DAE_HYPHAE_1
Date: November 13, 2025
Phase: B (Continuity Testing)
"""

import sys
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from collections import Counter

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from persona_layer.conversational_organism_wrapper import ConversationalOrganismWrapper
from config import Config


@dataclass
class SemanticAtomDriftResult:
    """Result of semantic atom drift test."""
    test_inputs: int
    total_atoms: int  # 77 (11 organs × 7 atoms)

    # Activation correlation
    atom_activation_correlation: float
    stable_activation: bool  # ≥0.75

    # Dead atoms check
    atoms_ever_active: int
    no_dead_atoms: bool  # All ≥10% usage threshold

    # Diversity check
    atoms_active_late: int
    diversity_maintained: bool  # ≥40 atoms

    # Runaway check
    max_atom_proportion: float
    no_runaway_atoms: bool  # No atom >30%

    # Overall success
    success: bool
    reasoning: str


class SemanticAtomDriftTester:
    """
    Tests semantic atom stability across epochs.

    Validates that:
    - Atom activation patterns remain correlated
    - No catastrophic forgetting (atoms don't disappear)
    - Diversity is maintained (not collapsed)
    - No single atom dominates (balanced activation)
    """

    def __init__(
        self,
        organism: Optional[ConversationalOrganismWrapper] = None
    ):
        """
        Initialize semantic atom drift tester.

        Args:
            organism: ConversationalOrganismWrapper instance (or create new)
        """
        if organism is None:
            print("🌀 Initializing organism for semantic atom drift test...")
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism

    def _get_test_inputs(self) -> List[str]:
        """Get diverse test inputs covering different atom types."""
        return [
            # temporal_inquiry (LISTENING)
            "What happened before this feeling started?",

            # compassionate_presence (EMPATHY)
            "I see how much pain you're carrying right now.",

            # pattern_recognition (WISDOM)
            "This seems like a recurring pattern in your relationships.",

            # honest_truth (AUTHENTICITY)
            "I need to be direct: this dynamic isn't sustainable.",

            # embodied_awareness (PRESENCE)
            "What do you notice in your body as you say that?",

            # parts_detection (BOND/IFS)
            "It sounds like a part of you wants one thing, another part wants something else.",

            # coherence_repair (SANS)
            "Let me reflect back what I'm hearing to make sure I understand.",

            # urgency_detection (NDAM)
            "This feels urgent and needs immediate attention.",

            # rhythm_coherence (RNX)
            "There's a natural rhythm to how this is unfolding.",

            # polyvagal_state (EO)
            "I notice your nervous system shifting as we talk about this.",

            # response_scaling (CARD)
            "This calls for a measured, proportional response."
        ]

    def _extract_atom_activations(
        self,
        results: List[Dict]
    ) -> Dict[str, float]:
        """
        Extract atom activation frequencies across results.

        Args:
            results: List of organism processing results

        Returns:
            Dict mapping atom_name to activation frequency (0-1)
        """
        atom_counts = Counter()
        total_activations = 0

        for result in results:
            # Extract activated atoms from semantic fields
            semantic_fields = result.get('semantic_fields', [])

            for field in semantic_fields:
                if isinstance(field, dict):
                    atoms = field.get('atoms', [])
                    for atom in atoms:
                        if isinstance(atom, dict):
                            atom_name = atom.get('atom_name')
                            if atom_name:
                                atom_counts[atom_name] += 1
                                total_activations += 1

        # Convert to frequencies
        atom_frequencies = {}
        if total_activations > 0:
            for atom, count in atom_counts.items():
                atom_frequencies[atom] = count / total_activations

        return atom_frequencies

    def test_semantic_atom_drift(
        self,
        verbose: bool = True
    ) -> SemanticAtomDriftResult:
        """
        Test semantic atom drift.

        Args:
            verbose: Print detailed results

        Returns:
            SemanticAtomDriftResult with metrics and success status
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"🧬 SEMANTIC ATOM DRIFT TEST (CONT-005)")
            print(f"{'='*70}")
            print(f"\nTesting: Semantic atom stability (no catastrophic drift)")

        # Get test inputs
        test_inputs = self._get_test_inputs()

        if verbose:
            print(f"Test inputs: {len(test_inputs)}")
            print(f"Total atoms: 77 (11 organs × 7 atoms)")

        # Process inputs (simulate both early and late epochs)
        if verbose:
            print(f"\n📊 Processing inputs...")

        results = []
        for i, text in enumerate(test_inputs):
            if verbose and i % 5 == 0:
                print(f"   Processing {i+1}/{len(test_inputs)}...")

            result = self.organism.process_text(
                text=text,
                enable_phase2=True,
                enable_tsk_recording=False
            )
            results.append(result)

        # Extract atom activations
        atom_activations = self._extract_atom_activations(results)

        # For simulating early vs late comparison, split results
        mid_point = len(results) // 2
        early_results = results[:mid_point]
        late_results = results[mid_point:]

        early_activations = self._extract_atom_activations(early_results)
        late_activations = self._extract_atom_activations(late_results)

        # Compute correlation
        all_atoms = set(early_activations.keys()) | set(late_activations.keys())
        early_vector = [early_activations.get(atom, 0.0) for atom in sorted(all_atoms)]
        late_vector = [late_activations.get(atom, 0.0) for atom in sorted(all_atoms)]

        if len(early_vector) >= 2 and len(late_vector) >= 2:
            correlation = np.corrcoef(early_vector, late_vector)[0, 1]
            if np.isnan(correlation):
                correlation = 0.0
        else:
            correlation = 0.0

        # Count active atoms
        atoms_ever_active = len(atom_activations)
        atoms_active_late = len(late_activations)

        # Check for runaway atoms
        if len(atom_activations) > 0:
            max_atom_proportion = max(atom_activations.values())
        else:
            max_atom_proportion = 0.0

        if verbose:
            print(f"\n📊 Atom Activation Analysis:")
            print(f"   Atoms ever active: {atoms_ever_active}/77")
            print(f"   Atoms active (late): {atoms_active_late}")
            print(f"   Early-late correlation: {correlation:.3f}")
            print(f"   Max atom proportion: {max_atom_proportion:.3f}")

        # Success criteria
        stable_activation = correlation >= 0.75
        no_dead_atoms = atoms_ever_active >= 40  # At least 40 of 77 used
        diversity_maintained = atoms_active_late >= 40
        no_runaway_atoms = max_atom_proportion <= 0.30

        success = (
            stable_activation and
            no_dead_atoms and
            diversity_maintained and
            no_runaway_atoms
        )

        # Reasoning
        if success:
            reasoning = f"Atoms stable: {correlation:.2f} correlation, {atoms_active_late} diverse atoms"
        else:
            reasons = []
            if not stable_activation:
                reasons.append(f"Unstable activation: correlation {correlation:.2f} < 0.75")
            if not no_dead_atoms:
                reasons.append(f"Atom death: only {atoms_ever_active}/77 atoms used")
            if not diversity_maintained:
                reasons.append(f"Lost diversity: only {atoms_active_late} atoms active")
            if not no_runaway_atoms:
                reasons.append(f"Runaway atom: {max_atom_proportion:.1%} > 30%")
            reasoning = "; ".join(reasons)

        result = SemanticAtomDriftResult(
            test_inputs=len(test_inputs),
            total_atoms=77,
            atom_activation_correlation=correlation,
            stable_activation=stable_activation,
            atoms_ever_active=atoms_ever_active,
            no_dead_atoms=no_dead_atoms,
            atoms_active_late=atoms_active_late,
            diversity_maintained=diversity_maintained,
            max_atom_proportion=max_atom_proportion,
            no_runaway_atoms=no_runaway_atoms,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result)

        return result

    def _print_results(self, result: SemanticAtomDriftResult):
        """Print detailed test results."""
        print(f"\n📊 Semantic Atom Drift Metrics:")

        print(f"\n📈 Activation Correlation:")
        print(f"   Early-late correlation: {result.atom_activation_correlation:.3f}")
        print(f"   Target: ≥0.75")
        print(f"   Status: {'✅' if result.stable_activation else '❌'}")

        print(f"\n💀 Dead Atoms Check:")
        print(f"   Atoms ever active: {result.atoms_ever_active}/{result.total_atoms}")
        print(f"   Target: ≥40 atoms")
        print(f"   Status: {'✅' if result.no_dead_atoms else '❌'}")

        print(f"\n🌈 Diversity:")
        print(f"   Atoms active (late): {result.atoms_active_late}")
        print(f"   Target: ≥40 atoms")
        print(f"   Status: {'✅' if result.diversity_maintained else '❌'}")

        print(f"\n⚠️  Runaway Check:")
        print(f"   Max atom proportion: {result.max_atom_proportion:.1%}")
        print(f"   Target: ≤30%")
        print(f"   Status: {'✅' if result.no_runaway_atoms else '❌'}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: {result.reasoning}")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_semantic_atom_drift_test() -> bool:
    """Run semantic atom drift test."""
    tester = SemanticAtomDriftTester()
    result = tester.test_semantic_atom_drift(verbose=True)

    return result.success


if __name__ == "__main__":
    success = run_semantic_atom_drift_test()
    sys.exit(0 if success else 1)
