#!/usr/bin/env python3
"""
V0 Emission Commit - 3-Phase Emission Generation for DAE
=========================================================

Adapted from FFITTSS V0's T5 commit architecture for conversational processing.

Architecture:
    Phase 1: COLLECT - Gather emission candidates from multiple sources
    Phase 2: RANK - Score candidates by readiness, apply budget
    Phase 3: EMIT - Select final emission, return stats

Key Concepts (from FFITTSS):
    - ΔC Readiness: Quality score for emission confidence
    - 3-Phase Separation: Clean gate/rank/emit logic
    - Budget Policies: Top-p, family-aware selection
    - TSK Tracking: Complete provenance

Date: November 12, 2025
Status: Phase 1 Implementation Starter
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class EmissionSource(Enum):
    """Source of emission candidate."""
    RECONSTRUCTION = "reconstruction"  # Base emission from pipeline
    TRANSDUCTION = "transduction"      # Alternative transduction phrases
    PERSONA = "persona"                # Persona layer variations
    HEBBIAN = "hebbian"                # Fallback safety net


@dataclass
class EmissionCandidate:
    """
    Candidate emission (pre-ranking).

    Analogous to FFITTSS's V0Candidate at nexus positions.
    DAE generates multiple phrase candidates from different sources.
    """

    # Phrase identification
    phrase_text: str
    phrase_source: EmissionSource
    phrase_category: str  # mechanism, template type, etc.

    # Confidence metrics (components of ΔC_text)
    nexus_coherence: float  # Dominant nexus coherence [0,1]
    transduction_confidence: float  # Pathway confidence [0,1]
    zone_appropriateness: float  # SELF Matrix safety [0,1]
    persona_confidence: float  # Template fit [0,1]

    # Composite readiness (DAE's ΔC equivalent)
    emission_readiness: float  # Computed from above metrics [0,1]

    # Safety context
    zone: int  # SELF Matrix zone (1-5)
    ndam_urgency: float  # Crisis level [0,1]
    polyvagal_state: str  # 'ventral_vagal', 'sympathetic', 'dorsal_vagal'
    safety_gradient: float  # Combined safety penalty [0,1]

    # V0 context
    v0_energy: float  # Current V0 energy [0,1]
    satisfaction: float  # Position satisfaction [0,1]
    kairos_detected: bool  # Opportune moment flag

    # Metadata
    convergence_cycle: int  # Which V0 cycle produced this
    timestamp: str  # When generated


@dataclass
class EmissionRanked:
    """
    Ranked emission (post-scoring).

    Analogous to FFITTSS's V0Ranked with score and budget acceptance.
    """

    candidate: EmissionCandidate
    score: float  # Composite score for ranking
    rank: int  # Position in ranking (1-indexed)
    accepted: bool  # Whether budget policy accepted
    budget_reason: str  # Acceptance/rejection reason


@dataclass
class EmissionStats:
    """
    Emission commit statistics.

    Analogous to FFITTSS's V0CommitStats.
    Tracks candidates collected, ranked, accepted.
    """

    # Candidate counts
    total_candidates: int
    accepted_candidates: int
    rejected_candidates: int

    # Source distribution
    source_counts: Dict[str, int]  # {source: count}

    # Final selection
    final_source: EmissionSource
    final_readiness: float
    final_score: float
    final_rank: int

    # Threshold used
    emission_threshold_tau: float

    # Budget policy
    budget_policy: str
    budget_param: float


# ============================================================================
# PHASE 1: COLLECT CANDIDATES
# ============================================================================

def compute_emission_readiness(
    nexus_coherence: float,
    transduction_confidence: float,
    zone_appropriateness: float,
    persona_confidence: float,
    safety_gradient: float,
    v0_energy: float,
    alpha: float = 0.35,  # Nexus weight
    beta: float = 0.25,   # Transduction weight
    gamma: float = 0.20,  # Zone weight
    zeta: float = 0.10,   # Persona weight
    chi: float = 0.10     # Safety penalty weight
) -> float:
    """
    Compute emission readiness score (DAE's ΔC equivalent).

    Adapted from FFITTSS's ΔC formula:
        ΔC = σ(α·coh + β·evid - χ·ΔE + γ·R + ζ·ctx)

    DAE Mapping:
        coh     → nexus_coherence
        evid    → transduction_confidence
        ΔE      → safety_gradient
        R       → zone_appropriateness
        ctx     → persona_confidence

    Higher scores = more confident, safer emissions
    Lower scores = uncertain, potentially unsafe emissions

    Args:
        nexus_coherence: Dominant nexus coherence [0,1]
        transduction_confidence: Pathway confidence [0,1]
        zone_appropriateness: SELF Matrix safety alignment [0,1]
        persona_confidence: Template fit [0,1]
        safety_gradient: Combined safety penalty (NDAM + EO) [0,1]
        v0_energy: Current V0 energy [0,1]
        alpha-chi: Component weights (must sum to 1.0)

    Returns:
        Emission readiness score [0,1]
    """
    # Base readiness formula
    readiness = (
        alpha * nexus_coherence +
        beta * transduction_confidence +
        gamma * zone_appropriateness +
        zeta * persona_confidence -
        chi * safety_gradient
    )

    # V0 modulation (lower V0 = higher confidence)
    v0_factor = 1.0 - v0_energy  # Inverted (0.2 V0 → 0.8 factor)
    readiness *= v0_factor

    return np.clip(readiness, 0.0, 1.0)


def compute_zone_appropriateness(zone: int) -> float:
    """
    Compute SELF Matrix zone appropriateness score.

    Zone-based safety assessment for emission strategies.

    Args:
        zone: SELF Matrix zone (1-5)

    Returns:
        Appropriateness score [0,1]
            1.0 = Core SELF, all strategies safe
            0.1 = Collapse, minimal emission only
    """
    ZONE_APPROPRIATENESS = {
        1: 1.0,  # Core SELF - all strategies safe
        2: 0.9,  # Firefighter - mostly safe
        3: 0.7,  # Manager - moderate caution
        4: 0.3,  # Protective - high caution
        5: 0.1   # Collapse - minimal emission only
    }
    return ZONE_APPROPRIATENESS.get(zone, 0.5)


def compute_safety_gradient(
    ndam_urgency: float,
    polyvagal_state: str
) -> float:
    """
    Compute combined safety gradient (penalty term).

    Combines NDAM urgency with polyvagal state for safety assessment.

    Args:
        ndam_urgency: Crisis urgency level [0,1]
        polyvagal_state: 'ventral_vagal', 'sympathetic', 'dorsal_vagal', 'mixed_state'

    Returns:
        Safety gradient [0,1]
            0.0 = Maximum safety (ventral + low urgency)
            1.0 = Maximum danger (dorsal + high urgency)
    """
    # Polyvagal safety mapping
    POLYVAGAL_SAFETY = {
        'ventral_vagal': 1.0,    # Safe & social
        'mixed_state': 0.5,      # Neutral
        'sympathetic': 0.3,      # Fight/flight
        'dorsal_vagal': 0.0      # Shutdown/collapse
    }

    polyvagal_safety = POLYVAGAL_SAFETY.get(polyvagal_state, 0.5)

    # Combined gradient (higher = more unsafe)
    safety_gradient = (ndam_urgency + (1.0 - polyvagal_safety)) / 2.0

    return np.clip(safety_gradient, 0.0, 1.0)


# ============================================================================
# PHASE 2: RANK CANDIDATES
# ============================================================================

def rank_emission_candidates(
    candidates: List[EmissionCandidate],
    budget_policy: str = 'top_p',
    budget_param: float = 0.7
) -> List[EmissionRanked]:
    """
    Phase 2: Score and rank candidates, apply budget.

    Score formula (adapted from FFITTSS PR-2):
        score = readiness × zone_safety × v0_factor

    Budget policies:
        - 'top_p': Select top-p by score (e.g., 0.7 = top 70%)
        - 'soft_budget': Temperatured softmax until cumulative ≤ B
        - 'family_aware': Dynamic budget from family params (Phase 4)

    Args:
        candidates: List of emission candidates from Phase 1
        budget_policy: Budget selection policy
        budget_param: Policy-specific parameter

    Returns:
        List of ranked emissions with acceptance decisions
    """
    ranked = []

    for candidate in candidates:
        # Composite score
        zone_safety = 1.0 - candidate.safety_gradient
        v0_factor = 1.0 - candidate.v0_energy

        score = (
            candidate.emission_readiness *
            zone_safety *
            v0_factor
        )

        ranked.append(EmissionRanked(
            candidate=candidate,
            score=score,
            rank=0,  # Set after sorting
            accepted=False,  # Set by budget policy
            budget_reason=""
        ))

    # Sort by score (descending)
    ranked.sort(key=lambda r: r.score, reverse=True)

    # Assign ranks
    for i, r in enumerate(ranked):
        r.rank = i + 1

    # Apply budget policy
    if budget_policy == 'top_p':
        cutoff = max(1, int(len(ranked) * budget_param))
        for i, r in enumerate(ranked):
            if i < cutoff:
                r.accepted = True
                r.budget_reason = 'top_p_accepted'
            else:
                r.accepted = False
                r.budget_reason = f'top_p_rejected (rank {r.rank} > cutoff {cutoff})'

    elif budget_policy == 'soft_budget':
        # Temperatured softmax (future implementation)
        pass

    return ranked


# ============================================================================
# PHASE 3: EMIT FINAL EMISSION
# ============================================================================

def emit_final_emission(
    ranked: List[EmissionRanked],
    emission_threshold_tau: float = 0.50
) -> Tuple[str, EmissionStats]:
    """
    Phase 3: Select top emission and return stats.

    Selection logic:
    1. Get top accepted candidate
    2. If no accepted candidates, fallback to lowest-risk hebbian
    3. Return emission text + comprehensive stats

    Args:
        ranked: List of ranked emissions from Phase 2
        emission_threshold_tau: Minimum readiness threshold

    Returns:
        (final_emission_text, emission_stats)
    """
    # Get accepted candidates
    accepted = [r for r in ranked if r.accepted]

    if not accepted:
        # Safety fallback: use lowest-risk hebbian
        hebbian_candidates = [
            r for r in ranked
            if r.candidate.phrase_source == EmissionSource.HEBBIAN
        ]
        if hebbian_candidates:
            accepted = hebbian_candidates
        else:
            # Ultimate fallback: top ranked (even if not accepted)
            accepted = [ranked[0]] if ranked else []

    if not accepted:
        raise ValueError("No emission candidates available (should never happen)")

    # Select top accepted
    top = accepted[0]

    # Compute source distribution
    source_counts = {}
    for r in ranked:
        source_name = r.candidate.phrase_source.value
        source_counts[source_name] = source_counts.get(source_name, 0) + 1

    # Build stats
    stats = EmissionStats(
        total_candidates=len(ranked),
        accepted_candidates=len([r for r in ranked if r.accepted]),
        rejected_candidates=len([r for r in ranked if not r.accepted]),
        source_counts=source_counts,
        final_source=top.candidate.phrase_source,
        final_readiness=top.candidate.emission_readiness,
        final_score=top.score,
        final_rank=top.rank,
        emission_threshold_tau=emission_threshold_tau,
        budget_policy='top_p',  # TODO: Make configurable
        budget_param=0.7  # TODO: Make configurable
    )

    return top.candidate.phrase_text, stats


# ============================================================================
# MAIN 3-PHASE PIPELINE
# ============================================================================

def commit_and_emit_v0(
    base_emission: str,
    felt_state: Dict[str, Any],
    enable_score_ranking: bool = True,
    emission_threshold_tau: float = 0.50,
    budget_policy: str = 'top_p',
    budget_param: float = 0.7
) -> Tuple[str, EmissionStats]:
    """
    Main V0 commit pipeline for DAE emissions.

    3-Phase Architecture (adapted from FFITTSS T5):
        Phase 1: Collect candidates from multiple sources
        Phase 2: Rank by readiness score, apply budget
        Phase 3: Emit final selection with stats

    Args:
        base_emission: Base emission from reconstruction pipeline
        felt_state: Complete felt state from organism processing
        enable_score_ranking: Use 3-phase (True) or direct emit (False)
        emission_threshold_tau: Minimum readiness threshold
        budget_policy: Budget selection policy ('top_p', 'soft_budget')
        budget_param: Policy-specific parameter

    Returns:
        (final_emission_text, emission_stats)
    """
    if not enable_score_ranking:
        # Legacy path: Direct emission (backward compatible)
        stats = EmissionStats(
            total_candidates=1,
            accepted_candidates=1,
            rejected_candidates=0,
            source_counts={'reconstruction': 1},
            final_source=EmissionSource.RECONSTRUCTION,
            final_readiness=felt_state.get('emission_confidence', 0.5),
            final_score=1.0,
            final_rank=1,
            emission_threshold_tau=emission_threshold_tau,
            budget_policy='direct',
            budget_param=1.0
        )
        return base_emission, stats

    # 3-PHASE ARCHITECTURE (NEW)

    # Phase 1: COLLECT
    # TODO: Implement collect_emission_candidates()
    # For now, just use base emission as single candidate
    candidates = [
        EmissionCandidate(
            phrase_text=base_emission,
            phrase_source=EmissionSource.RECONSTRUCTION,
            phrase_category='base',
            nexus_coherence=felt_state.get('mean_coherence', 0.5),
            transduction_confidence=felt_state.get('emission_confidence', 0.5),
            zone_appropriateness=compute_zone_appropriateness(
                felt_state.get('zone', 1)
            ),
            persona_confidence=0.8,
            emission_readiness=compute_emission_readiness(
                nexus_coherence=felt_state.get('mean_coherence', 0.5),
                transduction_confidence=felt_state.get('emission_confidence', 0.5),
                zone_appropriateness=compute_zone_appropriateness(
                    felt_state.get('zone', 1)
                ),
                persona_confidence=0.8,
                safety_gradient=compute_safety_gradient(
                    ndam_urgency=felt_state.get('NDAM_urgency_level', 0.0),
                    polyvagal_state=felt_state.get('EO_polyvagal_state', 'mixed_state')
                ),
                v0_energy=felt_state.get('v0_energy_final', 0.5)
            ),
            zone=felt_state.get('zone', 1),
            ndam_urgency=felt_state.get('NDAM_urgency_level', 0.0),
            polyvagal_state=felt_state.get('EO_polyvagal_state', 'mixed_state'),
            safety_gradient=compute_safety_gradient(
                ndam_urgency=felt_state.get('NDAM_urgency_level', 0.0),
                polyvagal_state=felt_state.get('EO_polyvagal_state', 'mixed_state')
            ),
            v0_energy=felt_state.get('v0_energy_final', 0.5),
            satisfaction=felt_state.get('satisfaction_final', 0.5),
            kairos_detected=felt_state.get('kairos_detected', False),
            convergence_cycle=felt_state.get('convergence_cycles', 1),
            timestamp=felt_state.get('timestamp', '')
        )
    ]

    # Phase 2: RANK
    ranked = rank_emission_candidates(
        candidates=candidates,
        budget_policy=budget_policy,
        budget_param=budget_param
    )

    # Phase 3: EMIT
    final_emission, stats = emit_final_emission(
        ranked=ranked,
        emission_threshold_tau=emission_threshold_tau
    )

    return final_emission, stats


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_zone_from_felt_state(felt_state: Dict[str, Any]) -> int:
    """
    Extract SELF Matrix zone from felt state.

    Uses bond_self_distance to classify zone (1-5).
    """
    bond_self_distance = felt_state.get('bond_self_distance', 0.0)

    if bond_self_distance > 0.7:
        return 5  # Collapse/Exile
    elif bond_self_distance > 0.5:
        return 4  # Protective
    elif bond_self_distance > 0.35:
        return 3  # Manager
    elif bond_self_distance > 0.2:
        return 2  # Firefighter
    else:
        return 1  # Core SELF


# ============================================================================
# TESTING & VALIDATION
# ============================================================================

def test_emission_readiness_computation():
    """Unit test for ΔC_text formula."""
    readiness = compute_emission_readiness(
        nexus_coherence=0.8,
        transduction_confidence=0.7,
        zone_appropriateness=1.0,
        persona_confidence=0.8,
        safety_gradient=0.1,
        v0_energy=0.3
    )

    assert 0.0 <= readiness <= 1.0, f"Readiness out of bounds: {readiness}"
    assert readiness > 0.5, f"Expected high confidence, got {readiness}"

    print(f"✅ Emission readiness test passed: {readiness:.3f}")


def test_3phase_pipeline():
    """Integration test for 3-phase pipeline."""
    # Mock felt state
    felt_state = {
        'mean_coherence': 0.75,
        'emission_confidence': 0.60,
        'zone': 1,
        'NDAM_urgency_level': 0.1,
        'EO_polyvagal_state': 'ventral_vagal',
        'v0_energy_final': 0.3,
        'satisfaction_final': 0.85,
        'kairos_detected': True,
        'convergence_cycles': 2
    }

    base_emission = "What's present for you right now?"

    # Run 3-phase pipeline
    final_emission, stats = commit_and_emit_v0(
        base_emission=base_emission,
        felt_state=felt_state,
        enable_score_ranking=True
    )

    assert final_emission is not None
    assert stats.total_candidates > 0
    assert stats.final_readiness > 0.0

    print(f"✅ 3-phase pipeline test passed")
    print(f"   Final emission: '{final_emission}'")
    print(f"   Stats: {stats.total_candidates} candidates, {stats.final_readiness:.3f} readiness")


if __name__ == "__main__":
    print("="*80)
    print("V0 EMISSION COMMIT - UNIT TESTS")
    print("="*80)

    test_emission_readiness_computation()
    test_3phase_pipeline()

    print("\n✅ All tests passed!")
