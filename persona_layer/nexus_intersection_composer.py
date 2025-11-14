"""
Nexus Intersection Composer - Phase 2 of Emission Architecture
================================================================

Forms organ coalitions in semantic space where 2+ organs activate the same atom.

Purpose:
- Receive semantic fields from 11 organs (5 conversational + 6 trauma/context)
- Identify intersection nexuses (atoms activated by 2+ organs)
- Weight by Hebbian R-matrix coupling (organ co-activation strength)
- Sort by intersection strength for emission generation

Philosophy:
- Nexuses are felt agreements, not just overlaps
- R-matrix coupling reflects learned organ relationships
- Intersection strength = appetition pull toward emission
- Coalitions respect existing 4-gate architecture from DAE 3.0

Integration Point:
- Called after semantic field extraction
- Before emission generation
- Input: 11 SemanticField objects (full organism)
- Output: Sorted list of SemanticNexus objects

Date: November 11, 2025
Status: Phase 3 Implementation - 11×11 R-matrix Support
"""

import json
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict


@dataclass
class SemanticNexus:
    """
    Organ coalition in semantic space.

    Represents WHERE 2+ organs agree on semantic atoms.
    Analogous to FFITTSS spatial nexuses, but over words/concepts.
    """
    atom: str  # Semantic atom where intersection occurs
    participants: List[str]  # Organ names that activated this atom
    activations: Dict[str, float]  # {organ_name: activation} for each participant

    # Nexus metrics (from 4-gate architecture)
    intersection_strength: float = 0.0  # Σ activations × R-matrix coupling
    coherence: float = 0.0  # Agreement among participants (1 - std)
    field_strength: float = 0.0  # Mean activation across participants
    r_matrix_weight: float = 0.0  # Hebbian coupling strength

    # Emission readiness (inspired by ΔC from FFITTSS)
    emission_readiness: float = 0.0  # Combined score for emission priority

    def __post_init__(self):
        """Compute derived metrics after initialization."""
        if self.activations:
            # Field strength: mean activation
            self.field_strength = np.mean(list(self.activations.values()))

            # Coherence: agreement (1 - standard deviation)
            if len(self.activations) > 1:
                self.coherence = 1.0 - np.std(list(self.activations.values()))
            else:
                self.coherence = 1.0  # Perfect coherence for single organ

            # Clip coherence to [0, 1]
            self.coherence = max(0.0, min(1.0, self.coherence))


class NexusIntersectionComposer:
    """
    Form organ coalitions in semantic space.

    Strategy:
    1. Load Hebbian R-matrix (5×5 organ coupling)
    2. For each semantic atom:
       - Find organs that activated it (activation > threshold)
       - If 2+ organs: create nexus
       - Weight by R-matrix coupling (organ co-activation)
       - Compute intersection strength
    3. Sort nexuses by emission readiness

    4-Gate Integration (from DAE 3.0):
    - Gate 1: Intersection (≥2 organs, τ_I = 1.5)
    - Gate 2: Coherence (agreement, τ_C = 0.4)
    - Gate 3: Satisfaction (field strength, τ_S ∈ [0.45, 0.70])
    - Gate 4: Felt Energy (R-matrix weight, higher = stronger)

    Emission Readiness:
    ΔC = α·coherence + β·intersection + γ·field_strength + δ·r_matrix_weight
    Using FFITTSS weights: α=0.47, β=0.35, γ=0.11, δ=0.07
    """

    def __init__(self, r_matrix_path: str, intersection_threshold: float = 0.01):
        """
        Initialize nexus intersection composer.

        Args:
            r_matrix_path: Path to conversational_hebbian_memory.json
            intersection_threshold: Minimum activation for organ participation
                (Lowered from 0.3 to 0.01 to enable nexus formation - Nov 13, 2025)
        """
        self.r_matrix_path = Path(r_matrix_path)
        self.intersection_threshold = intersection_threshold

        # Load R-matrix (11×11 organ coupling)
        self.r_matrix = self._load_r_matrix()

        # Load semantic synonyms for atom normalization (Nov 13, 2025)
        self.synonym_map = self._load_semantic_synonyms()

        # Organ names (from DAE_HYPHAE_1) - 11 organs total
        self.organ_names = [
            'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',  # Conversational (5)
            'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'  # Trauma/Context (6)
        ]

        # Emission readiness formula weights (from FFITTSS ΔC)
        self.alpha = 0.47  # Coherence weight
        self.beta = 0.35   # Intersection strength weight
        self.gamma = 0.11  # Field strength weight
        self.delta = 0.07  # R-matrix coupling weight

    def _load_r_matrix(self) -> np.ndarray:
        """
        Load Hebbian R-matrix from conversational_hebbian_memory.json.

        Returns:
            11×11 symmetric coupling matrix
        """
        if not self.r_matrix_path.exists():
            # Initialize identity matrix if file doesn't exist
            print(f"⚠️  R-matrix not found at {self.r_matrix_path}, using identity matrix")
            return np.eye(11)

        try:
            with open(self.r_matrix_path, 'r') as f:
                memory = json.load(f)

            # Extract R-matrix if present
            if 'r_matrix' in memory:
                r_matrix = np.array(memory['r_matrix'])
                if r_matrix.shape == (11, 11):
                    return r_matrix
                elif r_matrix.shape == (5, 5):
                    # Legacy 5×5 matrix - expand to 11×11 with identity for new organs
                    print(f"⚠️  Legacy 5×5 R-matrix detected, expanding to 11×11")
                    expanded = np.eye(11)
                    expanded[:5, :5] = r_matrix  # Copy existing 5×5 coupling
                    return expanded

            # Fallback to identity
            print(f"⚠️  R-matrix not in expected format, using identity matrix")
            return np.eye(11)

        except Exception as e:
            print(f"⚠️  Error loading R-matrix: {e}, using identity matrix")
            return np.eye(11)

    def _load_semantic_synonyms(self) -> Dict[str, str]:
        """
        Load semantic synonym mappings for atom normalization.

        Returns:
            Dict mapping synonym → canonical form
            Example: {"feel": "sense", "notice": "sense", "aware": "sense"}
        """
        synonyms_path = Path(__file__).parent / "semantic_synonyms.json"

        if not synonyms_path.exists():
            # No synonyms file - return empty map (atoms used as-is)
            return {}

        try:
            with open(synonyms_path, 'r') as f:
                data = json.load(f)

            # Build reverse map: synonym → canonical
            synonym_map = {}
            for group in data.get('synonym_groups', []):
                canonical = group['canonical']
                # Map canonical to itself
                synonym_map[canonical] = canonical
                # Map all synonyms to canonical
                for syn in group.get('synonyms', []):
                    synonym_map[syn] = canonical

            print(f"   ✅ Loaded {len(synonym_map)} semantic synonym mappings")
            return synonym_map

        except Exception as e:
            print(f"⚠️  Error loading semantic synonyms: {e}, using exact matching")
            return {}

    def _normalize_atom(self, atom: str) -> str:
        """
        Normalize atom name to canonical form using synonym map.

        Args:
            atom: Original atom name

        Returns:
            Canonical atom name (or original if no mapping)
        """
        # Try exact match first
        if atom in self.synonym_map:
            return self.synonym_map[atom]

        # Try lowercase match
        atom_lower = atom.lower()
        if atom_lower in self.synonym_map:
            return self.synonym_map[atom_lower]

        # Try with underscores replaced by spaces
        atom_spaced = atom.replace('_', ' ')
        if atom_spaced in self.synonym_map:
            return self.synonym_map[atom_spaced]

        # No mapping found - return original
        return atom

    def _get_r_matrix_coupling(self, organ1: str, organ2: str) -> float:
        """
        Get Hebbian coupling strength between two organs.

        Args:
            organ1, organ2: Organ names

        Returns:
            R-matrix coupling value [0, 1]
        """
        try:
            idx1 = self.organ_names.index(organ1)
            idx2 = self.organ_names.index(organ2)
            return float(self.r_matrix[idx1, idx2])
        except (ValueError, IndexError):
            return 0.0

    def compose_nexuses(self, semantic_fields: Dict) -> List[SemanticNexus]:
        """
        Form organ coalitions from semantic fields.

        Args:
            semantic_fields: {
                'LISTENING': SemanticField(...),
                'EMPATHY': SemanticField(...),
                ...
            }

        Returns:
            List of SemanticNexus objects, sorted by emission_readiness (descending)
        """
        # Collect all atoms activated by any organ (normalized to canonical forms)
        # Build normalized atom map: canonical → [(organ, original_atom, activation)]
        normalized_atoms = {}

        for organ_name, field in semantic_fields.items():
            for atom, activation in field.atom_activations.items():
                # Normalize atom to canonical form (e.g., "feel" → "sense")
                canonical_atom = self._normalize_atom(atom)

                if canonical_atom not in normalized_atoms:
                    normalized_atoms[canonical_atom] = []

                normalized_atoms[canonical_atom].append((organ_name, atom, activation))

        nexuses = []

        # For each canonical atom, check for organ intersections
        for canonical_atom, organ_activations in normalized_atoms.items():
            # Find organs that activated this canonical atom above threshold
            participants = {}

            for organ_name, original_atom, activation in organ_activations:
                if activation >= self.intersection_threshold:
                    # If multiple atoms from same organ map to same canonical,
                    # take the maximum activation
                    if organ_name not in participants:
                        participants[organ_name] = activation
                    else:
                        participants[organ_name] = max(participants[organ_name], activation)

            # Gate 1: Intersection (need 2+ organs)
            if len(participants) < 2:
                continue

            # Use canonical atom for nexus (allows synonyms to form nexuses)
            atom = canonical_atom

            # Create nexus
            nexus = SemanticNexus(
                atom=atom,
                participants=list(participants.keys()),
                activations=participants
            )

            # Compute R-matrix weighted intersection strength
            # Sum of pairwise organ coupling × activations
            r_matrix_sum = 0.0
            activation_sum = 0.0
            pair_count = 0

            participant_list = list(participants.keys())
            for i, organ1 in enumerate(participant_list):
                for organ2 in participant_list[i+1:]:
                    # R-matrix coupling between organs
                    coupling = self._get_r_matrix_coupling(organ1, organ2)

                    # Weighted by both activations
                    activation_product = participants[organ1] * participants[organ2]

                    r_matrix_sum += coupling * activation_product
                    activation_sum += activation_product
                    pair_count += 1

            # Normalize by number of pairs
            if pair_count > 0:
                nexus.r_matrix_weight = r_matrix_sum / pair_count
                nexus.intersection_strength = activation_sum / pair_count
            else:
                nexus.r_matrix_weight = 0.0
                nexus.intersection_strength = 0.0

            # Compute emission readiness (ΔC formula from FFITTSS)
            nexus.emission_readiness = (
                self.alpha * nexus.coherence +
                self.beta * nexus.intersection_strength +
                self.gamma * nexus.field_strength +
                self.delta * nexus.r_matrix_weight
            )

            # Gate 2: Coherence threshold
            if nexus.coherence < 0.4:
                continue

            nexuses.append(nexus)

        # Sort by emission readiness (descending)
        nexuses.sort(key=lambda n: n.emission_readiness, reverse=True)

        return nexuses

    def filter_by_gates(
        self,
        nexuses: List[SemanticNexus],
        coherence_threshold: float = 0.4,
        satisfaction_window: Tuple[float, float] = (0.45, 0.70),
        min_emission_readiness: float = 0.5
    ) -> List[SemanticNexus]:
        """
        Apply 4-gate filtering to nexuses.

        Args:
            nexuses: List of nexuses to filter
            coherence_threshold: Gate 2 (coherence)
            satisfaction_window: Gate 3 (field strength)
            min_emission_readiness: Gate 4 (ΔC threshold)

        Returns:
            Filtered nexuses passing all gates
        """
        filtered = []

        for nexus in nexuses:
            # Gate 1: Intersection (already enforced in compose_nexuses, ≥2 organs)
            if len(nexus.participants) < 2:
                continue

            # Gate 2: Coherence
            if nexus.coherence < coherence_threshold:
                continue

            # Gate 3: Satisfaction (field strength in Kairos window)
            if not (satisfaction_window[0] <= nexus.field_strength <= satisfaction_window[1]):
                continue

            # Gate 4: Felt Energy (emission readiness)
            if nexus.emission_readiness < min_emission_readiness:
                continue

            filtered.append(nexus)

        return filtered

    def get_top_nexuses(
        self,
        nexuses: List[SemanticNexus],
        k: int = 10,
        apply_gates: bool = True
    ) -> List[SemanticNexus]:
        """
        Get top-k nexuses by emission readiness.

        Args:
            nexuses: List of nexuses
            k: Number to return
            apply_gates: Whether to apply 4-gate filtering first

        Returns:
            Top-k nexuses (or fewer if gates filter too many)
        """
        if apply_gates:
            nexuses = self.filter_by_gates(nexuses)

        return nexuses[:k]

    def get_statistics(self, nexuses: List[SemanticNexus]) -> Dict:
        """
        Compute statistics about nexus composition.

        Args:
            nexuses: List of nexuses

        Returns:
            Statistics dict with coverage, strength, etc.
        """
        if not nexuses:
            return {
                'total_nexuses': 0,
                'mean_emission_readiness': 0.0,
                'mean_coherence': 0.0,
                'mean_field_strength': 0.0,
                'mean_participants': 0.0,
                'participant_distribution': {},
                'top_atoms': []
            }

        stats = {
            'total_nexuses': len(nexuses),
            'mean_emission_readiness': np.mean([n.emission_readiness for n in nexuses]),
            'mean_coherence': np.mean([n.coherence for n in nexuses]),
            'mean_field_strength': np.mean([n.field_strength for n in nexuses]),
            'mean_participants': np.mean([len(n.participants) for n in nexuses]),
            'participant_distribution': defaultdict(int),
            'top_atoms': [(n.atom, n.emission_readiness) for n in nexuses[:10]]
        }

        # Count participant sizes
        for nexus in nexuses:
            stats['participant_distribution'][len(nexus.participants)] += 1

        return stats


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 NEXUS INTERSECTION COMPOSER TEST")
    print("="*70)

    # Mock semantic fields for testing
    from dataclasses import dataclass, field as dc_field

    @dataclass
    class MockSemanticField:
        organ_name: str
        coherence: float
        lure: float
        atom_activations: Dict[str, float] = dc_field(default_factory=dict)
        pattern_count: int = 0
        field_strength: float = 0.0

    # Create mock semantic fields with overlapping atoms
    mock_fields = {
        'LISTENING': MockSemanticField(
            organ_name='LISTENING',
            coherence=0.75,
            lure=0.65,
            atom_activations={
                'more': 0.85,
                'what': 0.75,
                'how': 0.70,
                'tell': 0.65,  # Shared with EMPATHY
                'sense': 0.60  # Shared with EMPATHY
            }
        ),
        'EMPATHY': MockSemanticField(
            organ_name='EMPATHY',
            coherence=0.82,
            lure=0.70,
            atom_activations={
                'feel': 0.90,
                'sense': 0.80,  # Shared with LISTENING
                'tell': 0.70,   # Shared with LISTENING
                'body': 0.65,
                'where': 0.60   # Shared with PRESENCE
            }
        ),
        'WISDOM': MockSemanticField(
            organ_name='WISDOM',
            coherence=0.78,
            lure=0.68,
            atom_activations={
                'pattern': 0.82,
                'sense': 0.75,  # Shared with LISTENING, EMPATHY
                'context': 0.70,
                'meaning': 0.65
            }
        ),
        'PRESENCE': MockSemanticField(
            organ_name='PRESENCE',
            coherence=0.68,
            lure=0.55,
            atom_activations={
                'right now': 0.85,
                'here': 0.80,
                'where': 0.70,  # Shared with EMPATHY
                'sense': 0.65   # Shared with LISTENING, EMPATHY, WISDOM
            }
        )
    }

    # Test nexus composition
    try:
        composer = NexusIntersectionComposer(
            r_matrix_path='persona_layer/conversational_hebbian_memory.json',
            intersection_threshold=0.3
        )

        nexuses = composer.compose_nexuses(mock_fields)

        print(f"\n✅ Nexus composition successful!")
        print(f"   Total nexuses formed: {len(nexuses)}")

        # Print top nexuses
        print(f"\n📊 TOP NEXUSES BY EMISSION READINESS:")
        for i, nexus in enumerate(nexuses[:5], 1):
            print(f"\n{i}. Atom: '{nexus.atom}'")
            print(f"   Participants: {', '.join(nexus.participants)} ({len(nexus.participants)} organs)")
            print(f"   Emission readiness: {nexus.emission_readiness:.3f}")
            print(f"   Coherence: {nexus.coherence:.3f}")
            print(f"   Field strength: {nexus.field_strength:.3f}")
            print(f"   R-matrix weight: {nexus.r_matrix_weight:.3f}")
            print(f"   Activations:")
            for organ, activation in nexus.activations.items():
                print(f"     - {organ}: {activation:.3f}")

        # Apply 4-gate filtering
        filtered = composer.filter_by_gates(nexuses)
        print(f"\n🚪 4-GATE FILTERING:")
        print(f"   Before gates: {len(nexuses)} nexuses")
        print(f"   After gates: {len(filtered)} nexuses")
        print(f"   Pass rate: {len(filtered)/len(nexuses)*100:.1f}%")

        # Print statistics
        stats = composer.get_statistics(nexuses)
        print(f"\n📈 NEXUS STATISTICS:")
        print(f"   Total nexuses: {stats['total_nexuses']}")
        print(f"   Mean emission readiness: {stats['mean_emission_readiness']:.3f}")
        print(f"   Mean coherence: {stats['mean_coherence']:.3f}")
        print(f"   Mean field strength: {stats['mean_field_strength']:.3f}")
        print(f"   Mean participants: {stats['mean_participants']:.1f} organs")
        print(f"   Participant distribution:")
        for size, count in sorted(stats['participant_distribution'].items()):
            print(f"     - {size} organs: {count} nexuses")

        print(f"\n✅ Nexus intersection composition working correctly!")

    except Exception as e:
        print(f"\n❌ Nexus composition failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
