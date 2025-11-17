#!/usr/bin/env python3
"""
Nexus Signature Extractor - Intersection-Centered Pattern Matching

Transforms nexuses (temporary organ coalitions) into canonical 18D signatures
for learned phrase pattern lookup. Core component of foundational intelligence.

Philosophy:
  "The many become one" - A nexus is a temporary agreement between organs.
  The signature captures this agreement's FELT CONTEXT (not just organ names).

Architecture:
  Nexus → 18D Signature → Hashable Tuple → Dict Lookup → Learned Phrases

From REFINED_FOUNDATIONAL_INTELLIGENCE_SYNTHESIS_NOV17_2025.md
"""

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple, List, Dict, Any, Optional
import math


@dataclass(frozen=True)
class NexusSignature:
    """
    Canonical 18-dimensional signature for nexus pattern matching.

    Captures the INTERSECTION CONTEXT where organs agree, NOT just organ names.
    Designed for fuzzy matching via bin quantization.

    Dimensions (18D total):
      Core Identity (4D): participating_organs, organ_count, nexus_type, mechanism
      Felt Context (8D): coherence, urgency, polyvagal, zone, v0, kairos, field_strength, meta_atom
      TSK Enhancement (6D - Optional): constraint_pattern, transductive_vocab, satisfaction_tier,
                                        emission_path, convergence_cycles, entity_context

    Philosophy:
      "A nexus is not defined by WHO participates, but by the FELT STATE of participation."
    """

    # ═══════════════════════════════════════════════════════════════════════
    # CORE NEXUS IDENTITY (4D)
    # ═══════════════════════════════════════════════════════════════════════

    participating_organs: FrozenSet[str]  # frozenset({'BOND','NDAM','EMPATHY'})
    """Frozen set of organ names participating in nexus (order-independent)"""

    organ_count: int  # 2-7 (typical range for nexuses with 2+ organs)
    """Number of participating organs (redundant but useful for quick filtering)"""

    nexus_type: str  # From transduction_pathway_evaluator (14 types)
    """Nexus type: 'GUT_BOND_NDAM', 'PSYCHE_SANS', 'SOCIAL_EMPATHY', etc."""

    mechanism: str  # From transduction pathways (9 primary mechanisms)
    """Transduction mechanism: 'protective_stasis', 'coherence_repair', etc."""

    # ═══════════════════════════════════════════════════════════════════════
    # FELT-STATE CONTEXT (8D) - Critical for Pattern Matching!
    # ═══════════════════════════════════════════════════════════════════════

    coherence_bin: int  # Quantized [0.0-1.0] → 10 bins (0-9)
    """Field coherence bin: 0=chaos, 9=perfect harmony (bin width=0.1)"""

    urgency_bin: int  # Quantized [0.0-1.0] → 10 bins (0-9)
    """Urgency/crisis salience bin: 0=calm, 9=emergency (bin width=0.1)"""

    polyvagal_state: str  # 'ventral', 'sympathetic', 'dorsal', 'mixed_state'
    """Polyvagal state from EO organ (captures nervous system state)"""

    zone: int  # SELF Matrix zone (1-5)
    """SELF zone: 1=Peace, 2=Growth, 3=Threshold, 4=Compost, 5=Ground"""

    v0_energy_bin: int  # Quantized V0 final energy → 5 bins (0-4)
    """V0 energy bin: 0=depleted, 4=high energy (bin width=0.25)"""

    kairos_detected: bool  # True if kairos window [0.30, 0.50] detected
    """Opportune moment flag (78.6% detection rate from wave training)"""

    field_strength_bin: int  # Quantized mean(organ activations) → 5 bins (0-4)
    """Mean field strength bin: 0=weak, 4=strong (bin width=0.25)"""

    dominant_meta_atom: str  # From 10 shared meta-atoms
    """Dominant meta-atom: 'fierce_holding', 'somatic_wisdom', etc."""

    # ═══════════════════════════════════════════════════════════════════════
    # TSK ENHANCEMENT (6D - Optional, defaults to None)
    # ═══════════════════════════════════════════════════════════════════════

    constraint_pattern: Optional[str] = None  # e.g., "BOND_high_NDAM_high"
    """Constraint pattern from transduction trajectory"""

    transductive_vocabulary: Optional[FrozenSet[str]] = None  # e.g., frozenset({'signal_inflation'})
    """Transductive vocabulary terms (signal_inflation, salience_drift, etc.)"""

    satisfaction_tier: Optional[str] = None  # 'low', 'medium', 'high'
    """Satisfaction tier classification"""

    emission_path: Optional[str] = None  # 'organic', 'hebbian', 'felt_guided_llm'
    """Previous emission path (for learning what worked)"""

    convergence_cycles: Optional[int] = None  # 2-5 typical
    """Number of V0 convergence cycles"""

    entity_context: Optional[FrozenSet[str]] = None  # frozenset({'Emma', 'work'})
    """Mentioned entities (from NEXUS organ)"""

    def to_hashable(self, precision: str = 'medium') -> Tuple:
        """
        Convert signature to hashable tuple for dictionary lookup.

        Args:
            precision: 'low' (core only), 'medium' (core + felt), 'high' (all)

        Returns:
            Hashable tuple suitable for dict key

        Philosophy:
            "The many dimensions collapse to one hashable identity,
             preserving the felt context of intersection."
        """
        if precision == 'low':
            # Only core identity (4D)
            return (
                self.participating_organs,
                self.organ_count,
                self.nexus_type,
                self.mechanism
            )

        elif precision == 'medium':
            # Core + felt context (12D) - RECOMMENDED for pattern matching
            return (
                self.participating_organs,
                self.organ_count,
                self.nexus_type,
                self.mechanism,
                self.coherence_bin,
                self.urgency_bin,
                self.polyvagal_state,
                self.zone,
                self.v0_energy_bin,
                self.kairos_detected,
                self.field_strength_bin,
                self.dominant_meta_atom
            )

        elif precision == 'high':
            # All dimensions (18D) - Use for high-fidelity matching
            return (
                self.participating_organs,
                self.organ_count,
                self.nexus_type,
                self.mechanism,
                self.coherence_bin,
                self.urgency_bin,
                self.polyvagal_state,
                self.zone,
                self.v0_energy_bin,
                self.kairos_detected,
                self.field_strength_bin,
                self.dominant_meta_atom,
                self.constraint_pattern,
                self.transductive_vocabulary,
                self.satisfaction_tier,
                self.emission_path,
                self.convergence_cycles,
                self.entity_context
            )

        else:
            raise ValueError(f"Unknown precision: {precision}. Use 'low', 'medium', or 'high'.")

    def fuzzy_match_keys(self, tolerance: int = 1, precision: str = 'medium') -> List[Tuple]:
        """
        Generate fuzzy match keys by relaxing bin boundaries.

        Args:
            tolerance: Bin tolerance (±1 typical, ±2 aggressive)
            precision: Same as to_hashable()

        Returns:
            List of fuzzy-matched hashable tuples (length depends on bins relaxed)

        Philosophy:
            "Felt-states are continuous. Bins are discrete approximations.
             Fuzzy matching restores continuity by bridging bin boundaries."

        Example:
            If coherence_bin=7, urgency_bin=3, tolerance=1:
            - Generate coherence ∈ {6,7,8}, urgency ∈ {2,3,4}
            - Creates 3×3 = 9 fuzzy keys (including exact)
        """
        fuzzy_keys = []

        # Determine which bins to fuzz based on precision
        if precision == 'low':
            # No bins in low precision → return exact key only
            return [self.to_hashable(precision='low')]

        # Generate bin variations
        coherence_bins = self._bin_range(self.coherence_bin, min_val=0, max_val=9, tolerance=tolerance)
        urgency_bins = self._bin_range(self.urgency_bin, min_val=0, max_val=9, tolerance=tolerance)
        v0_bins = self._bin_range(self.v0_energy_bin, min_val=0, max_val=4, tolerance=tolerance)
        field_bins = self._bin_range(self.field_strength_bin, min_val=0, max_val=4, tolerance=tolerance)

        # Cartesian product of bin variations (limited to prevent explosion)
        # Strategy: Only fuzz the TWO most discriminating dimensions (coherence + urgency)
        for c_bin in coherence_bins:
            for u_bin in urgency_bins:
                # Create signature with fuzzed bins
                if precision == 'medium':
                    fuzzy_key = (
                        self.participating_organs,
                        self.organ_count,
                        self.nexus_type,
                        self.mechanism,
                        c_bin,  # Fuzzed
                        u_bin,  # Fuzzed
                        self.polyvagal_state,
                        self.zone,
                        self.v0_energy_bin,  # Exact (to limit combinatorial explosion)
                        self.kairos_detected,
                        self.field_strength_bin,  # Exact
                        self.dominant_meta_atom
                    )
                    fuzzy_keys.append(fuzzy_key)

                elif precision == 'high':
                    fuzzy_key = (
                        self.participating_organs,
                        self.organ_count,
                        self.nexus_type,
                        self.mechanism,
                        c_bin,  # Fuzzed
                        u_bin,  # Fuzzed
                        self.polyvagal_state,
                        self.zone,
                        self.v0_energy_bin,  # Exact
                        self.kairos_detected,
                        self.field_strength_bin,  # Exact
                        self.dominant_meta_atom,
                        self.constraint_pattern,
                        self.transductive_vocabulary,
                        self.satisfaction_tier,
                        self.emission_path,
                        self.convergence_cycles,
                        self.entity_context
                    )
                    fuzzy_keys.append(fuzzy_key)

        return fuzzy_keys

    def _bin_range(self, bin_value: int, min_val: int, max_val: int, tolerance: int) -> List[int]:
        """Generate bin range [bin - tolerance, bin + tolerance] clamped to [min_val, max_val]."""
        lower = max(min_val, bin_value - tolerance)
        upper = min(max_val, bin_value + tolerance)
        return list(range(lower, upper + 1))


class NexusSignatureExtractor:
    """
    Extracts canonical signatures from nexuses for pattern matching.

    Philosophy:
      "A nexus is a temporary organ coalition in felt-space.
       The signature captures the WHERE (felt context) of this coalition."

    Usage:
        extractor = NexusSignatureExtractor()
        sig = extractor.extract(nexus, organ_results, felt_state)
        hashable_key = sig.to_hashable(precision='medium')
        fuzzy_keys = sig.fuzzy_match_keys(tolerance=1)
    """

    def __init__(self):
        """Initialize extractor (stateless, no configuration needed)."""
        pass

    def extract(
        self,
        nexus: Dict[str, Any],
        organ_results: Dict[str, Any],
        felt_state: Dict[str, Any]
    ) -> NexusSignature:
        """
        Extract 18D signature from nexus + felt-state context.

        Args:
            nexus: Nexus dict with keys: participating_organs, nexus_type, mechanism, etc.
            organ_results: Dict of organ outputs (for field strength)
            felt_state: Dict of felt-state (coherence, urgency, polyvagal, zone, v0, etc.)

        Returns:
            NexusSignature (18D canonical representation)

        Philosophy:
            "The signature is not computed—it is FELT.
             We quantize the continuous felt-space into discrete bins
             to enable pattern matching while preserving fuzzy boundaries."
        """

        # ═══════════════════════════════════════════════════════════════════
        # CORE NEXUS IDENTITY (4D)
        # ═══════════════════════════════════════════════════════════════════

        participating_organs = frozenset(nexus.get('participating_organs', []))
        organ_count = len(participating_organs)
        nexus_type = nexus.get('nexus_type', 'UNKNOWN')
        mechanism = nexus.get('mechanism', 'unknown')

        # ═══════════════════════════════════════════════════════════════════
        # FELT-STATE CONTEXT (8D) - QUANTIZATION
        # ═══════════════════════════════════════════════════════════════════

        # Coherence: [0.0, 1.0] → bins [0-9] (bin width 0.1)
        coherence = felt_state.get('field_coherence', 0.5)
        coherence_bin = self._quantize(coherence, num_bins=10, min_val=0.0, max_val=1.0)

        # Urgency: [0.0, 1.0] → bins [0-9]
        urgency = felt_state.get('urgency', 0.5)
        urgency_bin = self._quantize(urgency, num_bins=10, min_val=0.0, max_val=1.0)

        # Polyvagal state (categorical)
        polyvagal_state = felt_state.get('polyvagal_state', 'mixed_state')

        # SELF Zone (1-5, already discrete)
        zone = felt_state.get('zone', 3)

        # V0 energy: [0.0, 1.0] → bins [0-4] (bin width 0.25)
        v0_final = felt_state.get('v0_final', 0.5)
        v0_energy_bin = self._quantize(v0_final, num_bins=5, min_val=0.0, max_val=1.0)

        # Kairos detection (boolean)
        kairos_detected = felt_state.get('kairos_detected', False)

        # Field strength: mean(organ coherences) → bins [0-4]
        field_strength = self._compute_field_strength(organ_results)
        field_strength_bin = self._quantize(field_strength, num_bins=5, min_val=0.0, max_val=1.0)

        # Dominant meta-atom
        dominant_meta_atom = felt_state.get('dominant_meta_atom', 'none')

        # ═══════════════════════════════════════════════════════════════════
        # TSK ENHANCEMENT (6D - Optional)
        # ═══════════════════════════════════════════════════════════════════

        constraint_pattern = felt_state.get('constraint_pattern', None)

        transductive_vocab = felt_state.get('transductive_vocabulary', None)
        if transductive_vocab is not None and not isinstance(transductive_vocab, frozenset):
            transductive_vocab = frozenset(transductive_vocab) if transductive_vocab else None

        satisfaction_tier = felt_state.get('satisfaction_tier', None)
        emission_path = felt_state.get('emission_path', None)
        convergence_cycles = felt_state.get('convergence_cycles', None)

        entity_context = felt_state.get('entity_context', None)
        if entity_context is not None and not isinstance(entity_context, frozenset):
            entity_context = frozenset(entity_context) if entity_context else None

        # ═══════════════════════════════════════════════════════════════════
        # CONSTRUCT SIGNATURE
        # ═══════════════════════════════════════════════════════════════════

        return NexusSignature(
            participating_organs=participating_organs,
            organ_count=organ_count,
            nexus_type=nexus_type,
            mechanism=mechanism,
            coherence_bin=coherence_bin,
            urgency_bin=urgency_bin,
            polyvagal_state=polyvagal_state,
            zone=zone,
            v0_energy_bin=v0_energy_bin,
            kairos_detected=kairos_detected,
            field_strength_bin=field_strength_bin,
            dominant_meta_atom=dominant_meta_atom,
            constraint_pattern=constraint_pattern,
            transductive_vocabulary=transductive_vocab,
            satisfaction_tier=satisfaction_tier,
            emission_path=emission_path,
            convergence_cycles=convergence_cycles,
            entity_context=entity_context
        )

    def _quantize(self, value: float, num_bins: int, min_val: float, max_val: float) -> int:
        """
        Quantize continuous value into discrete bins.

        Args:
            value: Continuous value to quantize
            num_bins: Number of bins (e.g., 10 for deciles)
            min_val: Minimum value (bin 0 lower bound)
            max_val: Maximum value (bin N-1 upper bound)

        Returns:
            Bin index [0, num_bins-1]

        Example:
            _quantize(0.73, num_bins=10, min_val=0.0, max_val=1.0) → 7
        """
        # Clamp to range
        value = max(min_val, min(max_val, value))

        # Compute bin width
        bin_width = (max_val - min_val) / num_bins

        # Compute bin index
        bin_idx = int((value - min_val) / bin_width)

        # Handle edge case: value exactly at max_val → last bin
        if bin_idx >= num_bins:
            bin_idx = num_bins - 1

        return bin_idx

    def _compute_field_strength(self, organ_results: Dict[str, Any]) -> float:
        """
        Compute mean field strength from organ coherences.

        Args:
            organ_results: Dict of organ outputs (key: organ_name, value: organ_data)

        Returns:
            Mean coherence [0.0, 1.0]
        """
        if not organ_results:
            return 0.5  # Default neutral

        coherences = []
        for organ_name, organ_data in organ_results.items():
            if isinstance(organ_data, dict):
                coherence = organ_data.get('coherence', 0.5)
                coherences.append(coherence)

        if not coherences:
            return 0.5

        return sum(coherences) / len(coherences)


# ═══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def extract_nexus_signature_from_field(organ_results: Dict[str, Any]) -> Optional[NexusSignature]:
    """
    🌀 WEEK 3, DAYS 3-4: Extract nexus signature from organ_results when no explicit nexuses exist.

    This function creates a "synthetic" nexus signature from organ field data, enabling
    pattern learning even when nexus formation didn't occur (weak activations, no coalitions).

    Args:
        organ_results: Dictionary of organ outputs {organ_name: organ_data}

    Returns:
        NexusSignature if extractable, None if insufficient data

    Philosophy:
        "Even in diffuse activation, there is a felt pattern worth learning."
        The signature captures the FIELD STATE, not just explicit coalitions.
    """
    if not organ_results or len(organ_results) == 0:
        return None

    try:
        # Extract participating organs (organs with coherence > 0.1)
        participating_organs = set()
        for organ_name, organ_data in organ_results.items():
            if hasattr(organ_data, 'coherence'):
                coherence = organ_data.coherence
            elif isinstance(organ_data, dict):
                coherence = organ_data.get('coherence', 0.0)
            else:
                coherence = 0.0

            if coherence > 0.1:  # Threshold for "participation"
                participating_organs.add(organ_name)

        if len(participating_organs) == 0:
            return None  # No organs activated sufficiently

        # Compute mean coherence (field strength)
        coherences = []
        for organ_name, organ_data in organ_results.items():
            if hasattr(organ_data, 'coherence'):
                coherences.append(organ_data.coherence)
            elif isinstance(organ_data, dict):
                coherences.append(organ_data.get('coherence', 0.5))

        mean_coherence = sum(coherences) / len(coherences) if coherences else 0.5
        coherence_bin = min(9, int(mean_coherence * 10))  # Bin [0-9]
        field_strength_bin = min(4, int(mean_coherence / 0.25))  # Bin [0-4]

        # Extract urgency from NDAM (if present)
        urgency = 0.0
        if 'NDAM' in organ_results:
            ndam_data = organ_results['NDAM']
            if hasattr(ndam_data, 'mean_urgency'):
                urgency = ndam_data.mean_urgency
            elif isinstance(ndam_data, dict):
                urgency = ndam_data.get('mean_urgency', 0.0)

        urgency_bin = min(9, int(urgency * 10))  # Bin [0-9]

        # Extract polyvagal state from EO (if present)
        polyvagal_state = 'ventral'  # Default
        if 'EO' in organ_results:
            eo_data = organ_results['EO']
            if hasattr(eo_data, 'polyvagal_state'):
                polyvagal_state = eo_data.polyvagal_state
            elif isinstance(eo_data, dict):
                polyvagal_state = eo_data.get('polyvagal_state', 'ventral')

        # Extract SELF zone from BOND (if present)
        zone = 1  # Default: Zone 1 (SELF)
        if 'BOND' in organ_results:
            bond_data = organ_results['BOND']
            if hasattr(bond_data, 'mean_self_distance'):
                bond_self_dist = bond_data.mean_self_distance
                # Convert BOND self_distance to SELF Matrix zone (1-5)
                if bond_self_dist > 0.8:
                    zone = 5  # Collapse/shutdown
                elif bond_self_dist > 0.6:
                    zone = 4  # Protective parts
                elif bond_self_dist > 0.4:
                    zone = 3  # Manager parts
                elif bond_self_dist > 0.2:
                    zone = 2  # Firefighter parts
                else:
                    zone = 1  # SELF (connected)

        # Determine nexus type from organ composition (simplified heuristic)
        if {'BOND', 'NDAM'}.issubset(participating_organs):
            nexus_type = 'GUT_BOND_NDAM'
            mechanism = 'protective_stasis'
        elif {'EMPATHY', 'LISTENING'}.issubset(participating_organs):
            nexus_type = 'SOCIAL_EMPATHY_LISTENING'
            mechanism = 'resonant_witnessing'
        elif {'SANS', 'WISDOM'}.issubset(participating_organs):
            nexus_type = 'PSYCHE_SANS_WISDOM'
            mechanism = 'coherence_repair'
        else:
            nexus_type = 'DIFFUSE_FIELD'
            mechanism = 'ambient_support'

        # Create signature with defaults for unknown fields
        signature = NexusSignature(
            participating_organs=frozenset(participating_organs),
            organ_count=len(participating_organs),
            nexus_type=nexus_type,
            mechanism=mechanism,
            coherence_bin=coherence_bin,
            urgency_bin=urgency_bin,
            polyvagal_state=polyvagal_state,
            zone=zone,
            v0_energy_bin=2,  # Default: mid-range
            kairos_detected=False,  # Unknown
            field_strength_bin=field_strength_bin,
            dominant_meta_atom='compassion_safety'  # Default
        )

        return signature

    except Exception as e:
        # Silent failure - return None to signal extraction failed
        return None


def get_default_extractor() -> NexusSignatureExtractor:
    """Get default nexus signature extractor (stateless singleton)."""
    return NexusSignatureExtractor()
