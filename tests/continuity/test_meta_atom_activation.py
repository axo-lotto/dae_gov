"""
Continuity Test: Meta-Atom Activation Patterns (CONT-006)
=========================================================

Tests that the 10 shared meta-atoms activate appropriately based on
context - trauma-informed atoms on crisis, bridge atoms on multi-organ nexuses.

Theoretical Foundation (Meta-Atom Bridges):
- Meta-atoms bridge multiple organs (shared semantic space)
- Trauma-informed atoms: Activate on crisis/safety contexts
- Bridge atoms: Activate when multiple organs co-participate
- Contextual appropriateness: Right meta-atoms for right situations

Test Protocol:
1. Test trauma-informed meta-atoms on crisis inputs
2. Test bridge meta-atoms on multi-organ nexus inputs
3. Validate appropriate activation patterns
4. Check overall meta-atom usage diversity

Success Criteria:
- ≥5 of 10 meta-atoms used by epoch 10 (diversity)
- Trauma meta-atoms: Activate on crisis inputs (≥80%)
- Bridge meta-atoms: Activate on multi-organ nexuses (≥60%)
- Contextual appropriateness: Right atoms for right contexts (≥70%)

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
class MetaAtomActivationResult:
    """Result of meta-atom activation pattern test."""
    test_inputs: int

    # Diversity
    meta_atoms_used: int
    meta_atoms_total: int  # 10
    sufficient_diversity: bool  # ≥5

    # Trauma-informed activation
    trauma_inputs_tested: int
    trauma_inputs_with_trauma_atoms: int
    trauma_activation_rate: float
    trauma_appropriate: bool  # ≥80%

    # Bridge activation
    nexus_inputs_tested: int
    nexus_inputs_with_bridge_atoms: int
    bridge_activation_rate: float
    bridge_appropriate: bool  # ≥60%

    # Overall contextual appropriateness
    contextual_accuracy: float  # % correct activations
    well_calibrated: bool  # ≥70%

    # Overall success
    success: bool
    reasoning: str


class MetaAtomActivationTester:
    """
    Tests meta-atom activation patterns.

    Validates that:
    - Meta-atoms are used (not ignored)
    - Trauma-informed atoms activate on crisis
    - Bridge atoms activate on multi-organ nexuses
    - Contextual appropriateness is high
    """

    # Meta-atom classification
    TRAUMA_INFORMED_ATOMS = {
        'trauma_aware',
        'window_of_tolerance',
        'somatic_wisdom'
    }

    BRIDGE_ATOMS = {
        'compassion_safety',
        'fierce_holding',
        'relational_attunement',
        'coherence_integration',
        'kairos_emergence',
        'temporal_grounding'
    }

    def __init__(
        self,
        organism: Optional[ConversationalOrganismWrapper] = None
    ):
        """
        Initialize meta-atom activation tester.

        Args:
            organism: ConversationalOrganismWrapper instance (or create new)
        """
        if organism is None:
            print("🌀 Initializing organism for meta-atom activation test...")
            self.organism = ConversationalOrganismWrapper()
        else:
            self.organism = organism

    def _get_test_inputs(self) -> Dict[str, List[str]]:
        """
        Get test inputs categorized by expected meta-atom type.

        Returns:
            Dict mapping category to list of inputs
        """
        return {
            # Crisis/trauma inputs (expect trauma-informed atoms)
            'trauma': [
                "I'm in crisis right now and my nervous system is completely dysregulated.",
                "Everything feels dangerous and I can't find safety anywhere.",
                "I'm having a trauma response and need to get grounded.",
                "My window of tolerance is completely exceeded right now.",
                "I'm dissociating and losing connection to my body."
            ],

            # Multi-organ nexus inputs (expect bridge atoms)
            'nexus': [
                "This conversation creates such a sense of safety and compassion.",
                "I feel the perfect timing of this moment, like everything is aligned.",
                "There's a fierce protective quality and tender care happening simultaneously.",
                "I notice how present and attuned you are to what I'm experiencing.",
                "The coherence between what I'm saying and what you're hearing is remarkable."
            ],

            # General inputs (variable meta-atom activation)
            'general': [
                "I'm feeling overwhelmed with my workload.",
                "This reminds me of a pattern I keep repeating.",
                "I need some space to process what we discussed."
            ]
        }

    def _extract_meta_atoms(self, result: Dict) -> Set[str]:
        """
        Extract activated meta-atoms from result.

        Args:
            result: Organism processing result

        Returns:
            Set of activated meta-atom names
        """
        meta_atoms = set()

        # Check semantic fields for meta-atoms
        semantic_fields = result.get('semantic_fields', [])
        for field in semantic_fields:
            if isinstance(field, dict):
                field_meta_atoms = field.get('meta_atoms', {})
                if isinstance(field_meta_atoms, dict):
                    meta_atoms.update(field_meta_atoms.keys())

        # Check felt states
        felt_states = result.get('felt_states', {})
        if isinstance(felt_states, dict):
            meta_atoms_activated = felt_states.get('meta_atoms_activated', [])
            if isinstance(meta_atoms_activated, list):
                meta_atoms.update(meta_atoms_activated)

        return meta_atoms

    def test_meta_atom_activation(
        self,
        verbose: bool = True
    ) -> MetaAtomActivationResult:
        """
        Test meta-atom activation patterns.

        Args:
            verbose: Print detailed results

        Returns:
            MetaAtomActivationResult with metrics and success status
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"🔗 META-ATOM ACTIVATION TEST (CONT-006)")
            print(f"{'='*70}")
            print(f"\nTesting: Contextually appropriate meta-atom activation")
            print(f"Meta-atoms: 10 total (3 trauma-informed, 6 bridge, 1 other)")

        # Get test inputs
        test_input_sets = self._get_test_inputs()

        all_meta_atoms_seen = set()
        trauma_results = []
        nexus_results = []

        # Process trauma inputs
        if verbose:
            print(f"\n🚨 Testing trauma-informed activation ({len(test_input_sets['trauma'])} inputs)...")

        for text in test_input_sets['trauma']:
            result = self.organism.process_text(
                text=text,
                enable_phase2=True,
                enable_tsk_recording=False
            )

            meta_atoms = self._extract_meta_atoms(result)
            all_meta_atoms_seen.update(meta_atoms)

            # Check if trauma-informed atoms activated
            has_trauma_atom = bool(meta_atoms & self.TRAUMA_INFORMED_ATOMS)
            trauma_results.append(has_trauma_atom)

        # Process nexus inputs
        if verbose:
            print(f"🔗 Testing bridge activation ({len(test_input_sets['nexus'])} inputs)...")

        for text in test_input_sets['nexus']:
            result = self.organism.process_text(
                text=text,
                enable_phase2=True,
                enable_tsk_recording=False
            )

            meta_atoms = self._extract_meta_atoms(result)
            all_meta_atoms_seen.update(meta_atoms)

            # Check if bridge atoms activated
            has_bridge_atom = bool(meta_atoms & self.BRIDGE_ATOMS)
            nexus_results.append(has_bridge_atom)

        # Process general inputs (for diversity)
        if verbose:
            print(f"📊 Testing general inputs ({len(test_input_sets['general'])} inputs)...")

        for text in test_input_sets['general']:
            result = self.organism.process_text(
                text=text,
                enable_phase2=True,
                enable_tsk_recording=False
            )

            meta_atoms = self._extract_meta_atoms(result)
            all_meta_atoms_seen.update(meta_atoms)

        # Compute metrics
        meta_atoms_used = len(all_meta_atoms_seen)

        trauma_inputs_tested = len(trauma_results)
        trauma_inputs_with_trauma_atoms = sum(trauma_results)
        trauma_activation_rate = trauma_inputs_with_trauma_atoms / trauma_inputs_tested if trauma_inputs_tested > 0 else 0.0

        nexus_inputs_tested = len(nexus_results)
        nexus_inputs_with_bridge_atoms = sum(nexus_results)
        bridge_activation_rate = nexus_inputs_with_bridge_atoms / nexus_inputs_tested if nexus_inputs_tested > 0 else 0.0

        # Overall contextual accuracy
        correct_activations = trauma_inputs_with_trauma_atoms + nexus_inputs_with_bridge_atoms
        total_contextual_inputs = trauma_inputs_tested + nexus_inputs_tested
        contextual_accuracy = correct_activations / total_contextual_inputs if total_contextual_inputs > 0 else 0.0

        if verbose:
            print(f"\n📊 Activation Analysis:")
            print(f"   Meta-atoms used: {meta_atoms_used}/10")
            print(f"   Trauma activation rate: {trauma_activation_rate:.1%}")
            print(f"   Bridge activation rate: {bridge_activation_rate:.1%}")
            print(f"   Contextual accuracy: {contextual_accuracy:.1%}")

        # Success criteria
        sufficient_diversity = meta_atoms_used >= 5
        trauma_appropriate = trauma_activation_rate >= 0.80
        bridge_appropriate = bridge_activation_rate >= 0.60
        well_calibrated = contextual_accuracy >= 0.70

        success = (
            sufficient_diversity and
            trauma_appropriate and
            bridge_appropriate and
            well_calibrated
        )

        # Reasoning
        if success:
            reasoning = f"Meta-atoms well-calibrated: {meta_atoms_used} used, {contextual_accuracy:.1%} contextual accuracy"
        else:
            reasons = []
            if not sufficient_diversity:
                reasons.append(f"Low diversity: {meta_atoms_used}/10 meta-atoms used (need ≥5)")
            if not trauma_appropriate:
                reasons.append(f"Trauma activation low: {trauma_activation_rate:.1%} < 80%")
            if not bridge_appropriate:
                reasons.append(f"Bridge activation low: {bridge_activation_rate:.1%} < 60%")
            if not well_calibrated:
                reasons.append(f"Poor calibration: {contextual_accuracy:.1%} < 70%")
            reasoning = "; ".join(reasons)

        result = MetaAtomActivationResult(
            test_inputs=sum(len(v) for v in test_input_sets.values()),
            meta_atoms_used=meta_atoms_used,
            meta_atoms_total=10,
            sufficient_diversity=sufficient_diversity,
            trauma_inputs_tested=trauma_inputs_tested,
            trauma_inputs_with_trauma_atoms=trauma_inputs_with_trauma_atoms,
            trauma_activation_rate=trauma_activation_rate,
            trauma_appropriate=trauma_appropriate,
            nexus_inputs_tested=nexus_inputs_tested,
            nexus_inputs_with_bridge_atoms=nexus_inputs_with_bridge_atoms,
            bridge_activation_rate=bridge_activation_rate,
            bridge_appropriate=bridge_appropriate,
            contextual_accuracy=contextual_accuracy,
            well_calibrated=well_calibrated,
            success=success,
            reasoning=reasoning
        )

        if verbose:
            self._print_results(result)

        return result

    def _print_results(self, result: MetaAtomActivationResult):
        """Print detailed test results."""
        print(f"\n📊 Meta-Atom Activation Metrics:")

        print(f"\n🌈 Diversity:")
        print(f"   Meta-atoms used: {result.meta_atoms_used}/{result.meta_atoms_total}")
        print(f"   Target: ≥5")
        print(f"   Status: {'✅' if result.sufficient_diversity else '❌'}")

        print(f"\n🚨 Trauma-Informed Activation:")
        print(f"   Activation rate: {result.trauma_activation_rate:.1%}")
        print(f"   ({result.trauma_inputs_with_trauma_atoms}/{result.trauma_inputs_tested} trauma inputs)")
        print(f"   Target: ≥80%")
        print(f"   Status: {'✅' if result.trauma_appropriate else '❌'}")

        print(f"\n🔗 Bridge Activation:")
        print(f"   Activation rate: {result.bridge_activation_rate:.1%}")
        print(f"   ({result.nexus_inputs_with_bridge_atoms}/{result.nexus_inputs_tested} nexus inputs)")
        print(f"   Target: ≥60%")
        print(f"   Status: {'✅' if result.bridge_appropriate else '❌'}")

        print(f"\n🎯 Contextual Appropriateness:")
        print(f"   Overall accuracy: {result.contextual_accuracy:.1%}")
        print(f"   Target: ≥70%")
        print(f"   Status: {'✅' if result.well_calibrated else '❌'}")

        print(f"\n{'='*70}")
        if result.success:
            print(f"✅ TEST PASSED: {result.reasoning}")
        else:
            print(f"❌ TEST FAILED: {result.reasoning}")
        print(f"{'='*70}")


def run_meta_atom_activation_test() -> bool:
    """Run meta-atom activation test."""
    tester = MetaAtomActivationTester()
    result = tester.test_meta_atom_activation(verbose=True)

    return result.success


if __name__ == "__main__":
    success = run_meta_atom_activation_test()
    sys.exit(0 if success else 1)
