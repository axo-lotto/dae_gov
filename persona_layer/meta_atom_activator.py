"""
Meta-Atom Activator - Phase 3 of Trust the Process Activation
==============================================================

Activates shared meta-atoms based on thematic alignment across organs.

Philosophy:
- Meta-atoms emerge when 2+ organs detect thematically aligned patterns
- Bridge atoms enable nexus formation across disjoint 77D organ space
- Confidence reflects mean activation strength of participating organs

Integration:
- Called after organ processing, before nexus composition
- Adds meta-atom activations to semantic fields
- Enables Trust the Process phrase library usage

Date: November 12, 2025
Status: Phase 3 Implementation
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class MetaAtomActivation:
    """Represents an activated meta-atom with participating organs."""
    meta_atom: str
    confidence: float  # Mean activation strength [0,1]
    participating_organs: List[str]  # Which organs activated this meta-atom
    organ_activations: Dict[str, float]  # Individual organ contributions


class MetaAtomActivator:
    """
    Activates shared meta-atoms based on organ pattern detection.

    Meta-atoms activate when:
    1. ≥minimum_organs (typically 2) meet activation conditions
    2. Each organ has ≥1 required atom above threshold
    3. Confidence computed from mean organ activations
    """

    def __init__(self, rules_path: str = "persona_layer/config/atoms/meta_atom_activation_rules.json"):
        """
        Initialize meta-atom activator with activation rules.

        Args:
            rules_path: Path to activation rules JSON
        """
        self.rules_path = Path(rules_path)
        self.activation_rules = self._load_activation_rules()

    def _load_activation_rules(self) -> Dict:
        """Load meta-atom activation rules from JSON."""
        if not self.rules_path.exists():
            raise FileNotFoundError(f"Activation rules not found: {self.rules_path}")

        with open(self.rules_path, 'r') as f:
            data = json.load(f)
            return data.get('activation_rules', {})

    def activate_meta_atoms(
        self,
        organ_results: Dict,
        verbose: bool = False,
        field_coherence: float = 0.0
    ) -> List[MetaAtomActivation]:
        """
        Activate meta-atoms based on organ results.

        Phase 2 Integration (Nov 15, 2025):
        Now accepts field_coherence to modulate nexus formation thresholds.
        High field coherence = organs "listening" to each other = easier nexus formation.

        Args:
            organ_results: Dict[organ_name, organ_result] with atom_activations
            verbose: Print activation details
            field_coherence: Cross-organ prehensive field coherence [0.0, 1.0]

        Returns:
            List of MetaAtomActivation objects (sorted by confidence)
        """
        activated_meta_atoms = []

        for meta_atom_name, rule in self.activation_rules.items():
            activation = self._check_meta_atom_activation(
                meta_atom_name,
                rule,
                organ_results,
                verbose,
                field_coherence=field_coherence
            )

            if activation:
                activated_meta_atoms.append(activation)

        # Sort by confidence (highest first)
        activated_meta_atoms.sort(key=lambda x: x.confidence, reverse=True)

        if verbose and activated_meta_atoms:
            print(f"\n   🌀 META-ATOMS ACTIVATED: {len(activated_meta_atoms)}")
            for ma in activated_meta_atoms:
                print(f"      • {ma.meta_atom}: {ma.confidence:.3f} ({', '.join(ma.participating_organs)})")

        return activated_meta_atoms

    def _check_meta_atom_activation(
        self,
        meta_atom_name: str,
        rule: Dict,
        organ_results: Dict,
        verbose: bool,
        field_coherence: float = 0.0
    ) -> Optional[MetaAtomActivation]:
        """
        Check if a specific meta-atom should activate.

        Phase 2 Integration (Nov 15, 2025):
        Adjusts minimum_organs threshold based on field coherence.
        High coherence → easier nexus formation (lower threshold).

        Args:
            meta_atom_name: Name of meta-atom to check
            rule: Activation rule configuration
            organ_results: Organ processing results
            verbose: Print details
            field_coherence: Cross-organ prehensive field coherence [0.0, 1.0]

        Returns:
            MetaAtomActivation if activated, None otherwise
        """
        participating_organs_list = rule.get('participating_organs', [])
        activation_conditions = rule.get('activation_conditions', {})
        minimum_organs = rule.get('minimum_organs', 2)

        # 🌀 Phase 2 (Nov 15, 2025): Modulate minimum_organs based on DAE 3.0 coherence thresholds
        # Use empirically validated thresholds from DAE 3.0 (r=0.82 correlation with success)
        #
        # DAE 3.0 Coherence Thresholds:
        # - coherence ≥ 0.70: 82% success rate, 34% perfect rate → AGGRESSIVE nexus formation
        # - coherence 0.50-0.70: 61% success rate, 18% perfect rate → MODERATE nexus formation
        # - coherence < 0.50: 29% success rate, 7% perfect rate → CONSERVATIVE (no reduction)
        if field_coherence >= 0.70:
            # High coherence (82% success) - aggressive nexus formation
            reduction_factor = 0.6  # 40% threshold reduction
        elif field_coherence >= 0.50:
            # Medium coherence (61% success) - moderate nexus formation
            reduction_factor = 0.8  # 20% threshold reduction
        else:
            # Low coherence (<50% success) - conservative (no reduction)
            reduction_factor = 1.0

        minimum_organs_adjusted = int(minimum_organs * reduction_factor)
        minimum_organs_adjusted = max(1, minimum_organs_adjusted)  # At least 1 organ

        # Track which organs meet activation conditions
        activated_organs = {}

        for organ_name in participating_organs_list:
            if organ_name not in organ_results:
                continue  # Organ not present

            organ_result = organ_results[organ_name]

            # Get atom activations (handle both dataclass and dict)
            if hasattr(organ_result, 'atom_activations'):
                atom_activations = organ_result.atom_activations
            elif isinstance(organ_result, dict):
                atom_activations = organ_result.get('atom_activations', {})
            else:
                continue  # Can't extract activations

            # Check if organ meets activation conditions
            if organ_name in activation_conditions:
                condition = activation_conditions[organ_name]
                max_activation = self._check_organ_condition(
                    organ_name,
                    condition,
                    atom_activations
                )

                if max_activation is not None:
                    activated_organs[organ_name] = max_activation

        # Check if minimum organs threshold met (with field coherence adjustment)
        if len(activated_organs) >= minimum_organs_adjusted:
            # Compute confidence (mean of participating organ activations)
            confidence = np.mean(list(activated_organs.values()))

            return MetaAtomActivation(
                meta_atom=meta_atom_name,
                confidence=float(confidence),
                participating_organs=list(activated_organs.keys()),
                organ_activations=activated_organs
            )

        return None

    def _check_organ_condition(
        self,
        organ_name: str,
        condition: Dict,
        atom_activations: Dict[str, float]
    ) -> Optional[float]:
        """
        Check if organ meets activation condition.

        Args:
            organ_name: Name of organ
            condition: Activation condition config
            atom_activations: Organ's atom activations

        Returns:
            Max activation value if condition met, None otherwise
        """
        required_atoms = condition.get('required_atoms', [])
        threshold = condition.get('threshold', 0.5)
        logic = condition.get('logic', 'any')  # 'any' or 'all'

        if not required_atoms:
            return None

        # Check atom activations
        activated_atoms = []
        for atom in required_atoms:
            activation = atom_activations.get(atom, 0.0)
            if activation >= threshold:
                activated_atoms.append(activation)

        if logic == 'any' and len(activated_atoms) > 0:
            # Any required atom above threshold → activate
            return max(activated_atoms)
        elif logic == 'all' and len(activated_atoms) == len(required_atoms):
            # All required atoms above threshold → activate
            return np.mean(activated_atoms)

        return None

    def add_meta_atoms_to_semantic_fields(
        self,
        semantic_fields: List,
        meta_atom_activations: List[MetaAtomActivation]
    ) -> List:
        """
        Add meta-atom activations to semantic fields for nexus composition.

        Args:
            semantic_fields: Existing semantic fields from organs
            meta_atom_activations: Activated meta-atoms

        Returns:
            Updated semantic fields including meta-atoms
        """
        # Import SemanticField dynamically to avoid circular import
        from persona_layer.semantic_field_extractor import SemanticField

        for ma_activation in meta_atom_activations:
            # Create semantic field for meta-atom
            # Use meta-atom name as organ_name to create unique field
            meta_field = SemanticField(
                organ_name=f"META_{ma_activation.meta_atom}",
                coherence=ma_activation.confidence,
                lure=ma_activation.confidence,  # Meta-atoms have inherent lure
                atom_activations={ma_activation.meta_atom: ma_activation.confidence},
                pattern_count=len(ma_activation.participating_organs),
                field_strength=ma_activation.confidence
            )

            semantic_fields.append(meta_field)

        return semantic_fields


# Quick test
if __name__ == '__main__':
    print("="*80)
    print("🧪 META-ATOM ACTIVATOR TEST")
    print("="*80)

    # Mock organ results for testing
    from dataclasses import dataclass as dc

    @dataclass
    class MockOrganResult:
        coherence: float
        atom_activations: Dict[str, float]

    # Scenario 1: Trauma-aware activation
    # BOND detects firefighter_parts + EO detects sympathetic + NDAM detects crisis
    mock_organs_trauma = {
        'BOND': MockOrganResult(
            coherence=0.75,
            atom_activations={
                'firefighter_parts': 0.82,
                'exile_patterns': 0.45,
                'self_energy': 0.30
            }
        ),
        'EO': MockOrganResult(
            coherence=0.70,
            atom_activations={
                'sympathetic': 0.78,
                'ventral_vagal': 0.25,
                'dorsal_vagal': 0.40
            }
        ),
        'NDAM': MockOrganResult(
            coherence=0.85,
            atom_activations={
                'crisis_salience': 0.90,
                'urgency_detection': 0.75
            }
        )
    }

    # Scenario 2: Fierce holding activation
    # EMPATHY + AUTHENTICITY + BOND
    mock_organs_fierce = {
        'EMPATHY': MockOrganResult(
            coherence=0.80,
            atom_activations={
                'compassionate_presence': 0.85,
                'emotional_resonance': 0.75
            }
        ),
        'AUTHENTICITY': MockOrganResult(
            coherence=0.78,
            atom_activations={
                'honest_truth': 0.80,
                'vulnerability_sharing': 0.70
            }
        ),
        'BOND': MockOrganResult(
            coherence=0.72,
            atom_activations={
                'self_energy': 0.75,
                'parts_awareness': 0.65
            }
        )
    }

    try:
        activator = MetaAtomActivator()

        print(f"\n✅ MetaAtomActivator initialized")
        print(f"   Loaded {len(activator.activation_rules)} activation rules")

        # Test Scenario 1: Trauma-aware
        print(f"\n📋 SCENARIO 1: Trauma-aware activation")
        print(f"   Organs: BOND (firefighter), EO (sympathetic), NDAM (crisis)")
        activations_trauma = activator.activate_meta_atoms(mock_organs_trauma, verbose=True)

        if any(ma.meta_atom == 'trauma_aware' for ma in activations_trauma):
            print(f"   ✅ trauma_aware activated correctly!")
        else:
            print(f"   ⚠️  trauma_aware NOT activated")

        # Test Scenario 2: Fierce holding
        print(f"\n📋 SCENARIO 2: Fierce holding activation")
        print(f"   Organs: EMPATHY (compassion), AUTHENTICITY (truth), BOND (self_energy)")
        activations_fierce = activator.activate_meta_atoms(mock_organs_fierce, verbose=True)

        if any(ma.meta_atom == 'fierce_holding' for ma in activations_fierce):
            print(f"   ✅ fierce_holding activated correctly!")
        else:
            print(f"   ⚠️  fierce_holding NOT activated")

        print(f"\n✅ Meta-atom activation working correctly!")

    except Exception as e:
        print(f"\n❌ Meta-atom activation failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)
