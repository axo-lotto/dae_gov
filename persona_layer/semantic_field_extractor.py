"""
Semantic Field Extractor - Phase 1 of Emission Architecture
=============================================================

Converts organ keyword pattern detections → semantic field objects.

Purpose:
- Bridge existing organ processing (keywords) → emission layer (semantic atoms)
- Extract semantic fields from 5 conversational organs
- Compute atom activations based on pattern strength + coherence + lure
- Normalize and weight for downstream nexus formation

Philosophy:
- Keywords are felt patterns, not just matches
- Semantic fields emerge from organ prehensions
- Activations weighted by organ confidence (coherence) and drive (lure)

Integration Point:
- Called after organ processing, before nexus formation
- Input: Organ results (ListeningResult, EmpathyResult, etc.)
- Output: Semantic fields (atom activations per organ)

Date: November 11, 2025
Status: Phase 1 Implementation
"""

import json
import numpy as np
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SemanticField:
    """
    Organ-specific semantic field over atom space.

    Represents WHERE in semantic space an organ is activating.
    Analogous to spatial fields in FFITTSS, but over words/concepts.
    """
    organ_name: str
    coherence: float  # Organ confidence [0,1]
    lure: float  # Appetition pull [0,1]
    atom_activations: Dict[str, float] = field(default_factory=dict)  # {atom: activation [0,1]}
    pattern_count: int = 0  # How many keyword patterns detected
    field_strength: float = 0.0  # Overall field strength (mean activation)

    def __post_init__(self):
        """Compute derived metrics after initialization."""
        if self.atom_activations:
            self.field_strength = np.mean(list(self.atom_activations.values()))

    def get_top_atoms(self, k: int = 10) -> List[tuple]:
        """
        Get top-k most activated atoms.

        Returns:
            List of (atom, activation) tuples sorted by activation
        """
        sorted_atoms = sorted(
            self.atom_activations.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_atoms[:k]


class SemanticFieldExtractor:
    """
    Extract semantic fields from organ processing results.

    Strategy:
    1. Load semantic atoms from JSON (550 atoms, 50 per organ, 11 organs)
    2. For each organ result:
       - Match detected keyword patterns → semantic atoms
       - Compute activation = pattern_strength × coherence
       - Apply lure weighting (higher lure = stronger activations)
       - Normalize to [0,1]
    3. Return semantic fields for all 11 organs

    Organs Supported:
    - 5 Conversational: LISTENING, EMPATHY, WISDOM, AUTHENTICITY, PRESENCE
    - 6 Trauma/Context: BOND, SANS, NDAM, RNX, EO, CARD

    Matching Logic:
    - Exact match: keyword == atom (activation = pattern_strength × coherence)
    - Substring match: keyword in atom or atom in keyword (activation × 0.8)
    - Similarity boost: If multiple keywords match same atom, accumulate

    Weighting:
    - Base activation: pattern_strength × coherence
    - Lure modulation: activation × (0.5 + 0.5 × lure)
    - Result: Higher lure = stronger activations (appetition drives field)
    """

    def __init__(self, semantic_atoms_path: str):
        """
        Initialize semantic field extractor.

        Args:
            semantic_atoms_path: Path to semantic_atoms.json file
        """
        self.semantic_atoms_path = Path(semantic_atoms_path)
        self.semantic_atoms = self._load_semantic_atoms()

        # Flatten atom dictionaries for faster matching
        self.organ_atom_sets = self._build_atom_sets()

    def _load_semantic_atoms(self) -> Dict:
        """Load semantic atoms from JSON file."""
        if not self.semantic_atoms_path.exists():
            raise FileNotFoundError(
                f"Semantic atoms file not found: {self.semantic_atoms_path}"
            )

        with open(self.semantic_atoms_path, 'r') as f:
            atoms = json.load(f)

        return atoms

    def _build_atom_sets(self) -> Dict[str, Set[str]]:
        """
        Build flat sets of atoms per organ for fast lookup.

        Returns:
            {organ_name: Set of all atoms for that organ}
        """
        organ_sets = {}

        # 11 organs: 5 conversational + 6 trauma/context-aware
        all_organ_names = [
            'LISTENING', 'EMPATHY', 'WISDOM', 'AUTHENTICITY', 'PRESENCE',  # Conversational
            'BOND', 'SANS', 'NDAM', 'RNX', 'EO', 'CARD'  # Trauma/Context
        ]

        for organ_name in all_organ_names:
            if organ_name not in self.semantic_atoms:
                continue

            organ_data = self.semantic_atoms[organ_name]
            atom_set = set()

            # Collect all atoms from all categories
            for category_name, category_atoms in organ_data.items():
                if isinstance(category_atoms, dict) and category_name not in [
                    'description', 'dimension', 'field_type', 'total_atoms'
                ]:
                    atom_set.update(category_atoms.keys())

            organ_sets[organ_name] = atom_set

        return organ_sets

    def extract_fields(self, organ_results: Dict) -> Dict[str, SemanticField]:
        """
        Extract semantic fields from 11 organ results.

        Args:
            organ_results: {
                # Conversational organs
                'LISTENING': ListeningResult(...),
                'EMPATHY': EmpathyResult(...),
                'WISDOM': WisdomResult(...),
                'AUTHENTICITY': AuthenticityResult(...),
                'PRESENCE': PresenceResult(...),
                # Trauma/context organs
                'BOND': BONDResult(...),
                'SANS': SANSResult(...),
                'NDAM': NDAMResult(...),
                'RNX': RNXResult(...),
                'EO': EOResult(...),
                'CARD': CARDResult(...)
            }

        Returns:
            semantic_fields: {
                'LISTENING': SemanticField(atom_activations={...}),
                'BOND': SemanticField(atom_activations={...}),
                ...
            }
        """
        semantic_fields = {}

        for organ_name, organ_result in organ_results.items():
            if organ_name not in self.semantic_atoms:
                continue

            # Extract semantic field for this organ
            field = self._extract_organ_field(
                organ_name=organ_name,
                organ_result=organ_result
            )

            semantic_fields[organ_name] = field

        return semantic_fields

    def _extract_organ_field(self, organ_name: str, organ_result) -> SemanticField:
        """
        Extract semantic field for a single organ.

        Args:
            organ_name: 'LISTENING', 'EMPATHY', 'BOND', 'SANS', etc.
            organ_result: OrganResult object (various types depending on organ)

        Returns:
            SemanticField with atom activations
        """
        # Extract organ metrics (with fallbacks for organs that might not have all attributes)
        coherence = getattr(organ_result, 'coherence', 0.5)  # Default coherence
        lure = getattr(organ_result, 'lure', 0.5)  # Default lure

        # Handle different pattern attribute names
        # - Most organs use 'patterns'
        # - BOND uses 'parts_patterns'
        if hasattr(organ_result, 'patterns'):
            patterns = organ_result.patterns
        elif hasattr(organ_result, 'parts_patterns'):
            patterns = organ_result.parts_patterns
        else:
            # Fallback: no patterns detected
            patterns = []

        # Initialize field
        field = SemanticField(
            organ_name=organ_name,
            coherence=coherence,
            lure=lure,
            pattern_count=len(patterns)
        )

        # Get semantic atoms for this organ
        organ_atoms = self.semantic_atoms[organ_name]

        # For each detected pattern, find matching semantic atoms
        for pattern in patterns:
            # Extract keywords from pattern
            keywords = self._extract_keywords_from_pattern(pattern)

            # Match keywords → semantic atoms
            matches = self._match_keywords_to_atoms(
                keywords=keywords,
                organ_atoms=organ_atoms,
                organ_atom_set=self.organ_atom_sets[organ_name]
            )

            # Compute activations for matched atoms
            for atom, similarity in matches:
                # Get pattern strength (different attribute names across organs)
                if hasattr(pattern, 'strength'):
                    pattern_strength = pattern.strength
                elif hasattr(pattern, 'similarity_score'):
                    pattern_strength = pattern.similarity_score
                elif hasattr(pattern, 'confidence'):
                    pattern_strength = pattern.confidence
                else:
                    # Fallback: default strength
                    pattern_strength = 0.5

                # Base activation: pattern strength × similarity × coherence
                activation = pattern_strength * similarity * coherence

                # Accumulate (if multiple patterns match same atom, add up)
                field.atom_activations[atom] = field.atom_activations.get(atom, 0.0) + activation

        # Apply lure weighting (higher lure = stronger activations)
        # Formula: activation × (0.5 + 0.5 × lure)
        # - lure=0.0 → 0.5× (weaken)
        # - lure=0.5 → 0.75× (neutral)
        # - lure=1.0 → 1.0× (full strength)
        lure_weight = 0.5 + 0.5 * lure

        for atom in field.atom_activations:
            field.atom_activations[atom] *= lure_weight

        # Normalize to [0,1] (clip max to 1.0, prevent accumulation overflow)
        max_activation = max(field.atom_activations.values()) if field.atom_activations else 1.0
        if max_activation > 1.0:
            for atom in field.atom_activations:
                field.atom_activations[atom] /= max_activation

        # Recompute field strength after weighting
        if field.atom_activations:
            field.field_strength = np.mean(list(field.atom_activations.values()))

        return field

    def _extract_keywords_from_pattern(self, pattern) -> List[str]:
        """
        Extract keywords from organ pattern object.

        Args:
            pattern: Pattern object (ListeningPattern, EmpathyPattern, etc.)

        Returns:
            List of keyword strings (lowercased)
        """
        keywords = []

        # Extract from matched_keywords if available
        if hasattr(pattern, 'matched_keywords') and pattern.matched_keywords:
            keywords.extend([kw.lower().strip() for kw in pattern.matched_keywords])

        # Fallback: If no matched_keywords, infer from pattern_type
        elif hasattr(pattern, 'pattern_type'):
            # Use pattern type as keyword (e.g., 'acknowledgment' → 'acknowledg')
            keywords.append(pattern.pattern_type.lower().strip())

        return keywords

    def _match_keywords_to_atoms(
        self,
        keywords: List[str],
        organ_atoms: Dict,
        organ_atom_set: Set[str]
    ) -> List[tuple]:
        """
        Match detected keywords → semantic atoms.

        Matching strategy:
        1. Exact match: keyword == atom → similarity 1.0
        2. Substring match: keyword in atom or atom in keyword → similarity 0.8
        3. Partial match: shared 3+ characters → similarity 0.5

        Args:
            keywords: List of detected keyword strings
            organ_atoms: Semantic atoms dict for this organ
            organ_atom_set: Set of all atoms for fast lookup

        Returns:
            List of (atom, similarity) tuples
        """
        matches = []

        for keyword in keywords:
            # Try exact match first
            if keyword in organ_atom_set:
                matches.append((keyword, 1.0))
                continue

            # Try substring matches
            for atom in organ_atom_set:
                if keyword in atom or atom in keyword:
                    matches.append((atom, 0.8))
                    continue

                # Try partial match (shared 3+ characters)
                if len(keyword) >= 3 and len(atom) >= 3:
                    shared = self._count_shared_chars(keyword, atom)
                    if shared >= 3:
                        similarity = min(0.5, shared / len(keyword))
                        matches.append((atom, similarity))

        # Remove duplicates (keep highest similarity)
        unique_matches = {}
        for atom, similarity in matches:
            if atom not in unique_matches or similarity > unique_matches[atom]:
                unique_matches[atom] = similarity

        return list(unique_matches.items())

    def _count_shared_chars(self, s1: str, s2: str) -> int:
        """Count shared characters between two strings."""
        return len(set(s1) & set(s2))

    def get_statistics(self, semantic_fields: Dict[str, SemanticField]) -> Dict:
        """
        Compute statistics about extracted semantic fields.

        Args:
            semantic_fields: Dict of extracted semantic fields

        Returns:
            Statistics dict with coverage, strength, etc.
        """
        stats = {
            'total_organs': len(semantic_fields),
            'total_atoms_activated': 0,
            'mean_field_strength': 0.0,
            'mean_coherence': 0.0,
            'mean_lure': 0.0,
            'per_organ': {}
        }

        coherences = []
        lures = []
        field_strengths = []

        for organ_name, field in semantic_fields.items():
            organ_stats = {
                'atoms_activated': len(field.atom_activations),
                'field_strength': field.field_strength,
                'coherence': field.coherence,
                'lure': field.lure,
                'pattern_count': field.pattern_count,
                'top_atoms': field.get_top_atoms(k=5)
            }
            stats['per_organ'][organ_name] = organ_stats

            stats['total_atoms_activated'] += len(field.atom_activations)
            coherences.append(field.coherence)
            lures.append(field.lure)
            field_strengths.append(field.field_strength)

        if coherences:
            stats['mean_coherence'] = np.mean(coherences)
            stats['mean_lure'] = np.mean(lures)
            stats['mean_field_strength'] = np.mean(field_strengths)

        return stats


# Quick test
if __name__ == '__main__':
    print("="*70)
    print("🧪 SEMANTIC FIELD EXTRACTOR TEST")
    print("="*70)

    # Mock organ result for testing
    from dataclasses import dataclass

    @dataclass
    class MockPattern:
        pattern_type: str
        strength: float
        matched_keywords: List[str]

    @dataclass
    class MockOrganResult:
        coherence: float
        lure: float
        patterns: List

    # Create mock organ results
    mock_organ_results = {
        'LISTENING': MockOrganResult(
            coherence=0.75,
            lure=0.65,
            patterns=[
                MockPattern('exploration', 0.8, ['more', 'say', 'tell']),
                MockPattern('inquiry', 0.7, ['what', 'how', 'when'])
            ]
        ),
        'EMPATHY': MockOrganResult(
            coherence=0.82,
            lure=0.70,
            patterns=[
                MockPattern('feeling', 0.9, ['feel', 'feeling', 'sense']),
                MockPattern('somatic', 0.75, ['body', 'where', 'sensation'])
            ]
        ),
        'PRESENCE': MockOrganResult(
            coherence=0.68,
            lure=0.55,
            patterns=[
                MockPattern('grounding', 0.85, ['right now', 'here', 'present'])
            ]
        )
    }

    # Test extraction
    try:
        extractor = SemanticFieldExtractor(
            semantic_atoms_path='persona_layer/semantic_atoms.json'
        )

        semantic_fields = extractor.extract_fields(mock_organ_results)

        print(f"\n✅ Extraction successful!")
        print(f"   Organs processed: {len(semantic_fields)}")

        # Print field details
        for organ_name, field in semantic_fields.items():
            print(f"\n📊 {organ_name}:")
            print(f"   Coherence: {field.coherence:.2f}")
            print(f"   Lure: {field.lure:.2f}")
            print(f"   Field strength: {field.field_strength:.3f}")
            print(f"   Atoms activated: {len(field.atom_activations)}")
            print(f"   Top 5 atoms:")
            for atom, activation in field.get_top_atoms(k=5):
                print(f"     - {atom}: {activation:.3f}")

        # Print overall statistics
        stats = extractor.get_statistics(semantic_fields)
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   Total atoms activated: {stats['total_atoms_activated']}")
        print(f"   Mean field strength: {stats['mean_field_strength']:.3f}")
        print(f"   Mean coherence: {stats['mean_coherence']:.3f}")
        print(f"   Mean lure: {stats['mean_lure']:.3f}")

        print(f"\n✅ Semantic field extraction working correctly!")

    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70)
