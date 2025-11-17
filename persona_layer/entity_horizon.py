"""
Entity Horizon - Morpheable Memory Boundary
============================================

Implements the FFITTSS-inspired morpheable horizon where memory depth adapts
based on conversational coherence. When the organism is tightly coupled (high
field coherence), memory deepens. When scattered, it focuses on recent.

Philosophy (Whitehead):
- Not all entities are felt every turn—only those within morpheable horizon are prehended
- Horizon morphs with conversational quality (coherence determines depth)
- Turn-based visibility (occasions, not clock-time)

Architecture:
- Layer 1 of the 3-layer prehension system (HORIZON → SALIENCE → OPTIMIZATION)
- Integrates with dae_interactive.py pre-query section
- Replaces fixed limit=20 with adaptive computation
- Uses field coherence from ConversationalOccasion

Author: DAE_HYPHAE_1 + Claude Code
Date: November 17, 2025
"""

from dataclasses import dataclass
from typing import Optional
from config import Config


@dataclass
class HorizonMetrics:
    """
    Metrics for tracking horizon behavior over time.

    Attributes:
        field_coherence: Current field coherence (1 - std([organs]))
        horizon_size: Computed horizon size (100-500 entities)
        recent_limit: Limit for recent entity query
        fuzzy_limit: Limit for fuzzy match query
        total_entities_available: Total entities in Neo4j for user
        entities_retrieved: Actual entities returned
        horizon_utilization: Percentage of horizon filled
    """
    field_coherence: float
    horizon_size: int
    recent_limit: int
    fuzzy_limit: int
    total_entities_available: int = 0
    entities_retrieved: int = 0
    horizon_utilization: float = 0.0


class EntityHorizon:
    """
    Morpheable horizon of prehendable entities.

    The horizon depth is not fixed by time or rules—it morphs based on the
    quality of conversational coherence. High coherence → deep memory access.
    Low coherence → focus on recent.

    Integration Points:
    - dae_interactive.py:367-392 - Replaces fixed limit=20
    - TextOccasion.known_entities - Transductive core
    - NEXUS organ - Coherence gating (τ=0.3)
    - ConversationalOccasion - Field coherence source

    FFITTSS Patterns:
    - Coherence gating: τ_recall = 0.3 (minimum threshold)
    - Turn-based: Occasions as fundamental units
    - Bounded: 100-500 entities (prevents explosion)
    - Adaptive: Morphs with conversational quality
    """

    # Horizon boundaries (FFITTSS-inspired)
    MIN_HORIZON_SIZE = 100   # Low coherence baseline
    MAX_HORIZON_SIZE = 500   # High coherence maximum

    # Coherence thresholds (from DAE 3.0 empirical validation)
    COHERENCE_HIGH = 0.70    # 82% success rate tier
    COHERENCE_MEDIUM = 0.50  # 61% success rate tier
    COHERENCE_LOW = 0.30     # 29% success rate tier (NEXUS τ_recall)

    def __init__(self):
        """Initialize entity horizon."""
        self.last_metrics: Optional[HorizonMetrics] = None

    def compute_horizon_size(self, field_coherence: float) -> int:
        """
        Compute adaptive horizon size based on field coherence.

        Mapping (empirically validated from DAE 3.0):
        - coherence ≥0.70: 500 entities (high harmony → deep memory)
        - coherence 0.50-0.70: 100-500 (linear interpolation)
        - coherence 0.30-0.50: 100 entities (focus on recent)
        - coherence <0.30: 100 entities (minimum baseline)

        Args:
            field_coherence: Field coherence from ConversationalOccasion (0.0-1.0)

        Returns:
            Horizon size (100-500 entities)
        """
        # Clamp coherence to valid range
        coherence = max(0.0, min(1.0, field_coherence))

        # High coherence → maximum depth
        if coherence >= self.COHERENCE_HIGH:
            return self.MAX_HORIZON_SIZE

        # Medium-high coherence → linear interpolation
        elif coherence >= self.COHERENCE_MEDIUM:
            # Map [0.50, 0.70] → [100, 500]
            t = (coherence - self.COHERENCE_MEDIUM) / (self.COHERENCE_HIGH - self.COHERENCE_MEDIUM)
            return int(self.MIN_HORIZON_SIZE + t * (self.MAX_HORIZON_SIZE - self.MIN_HORIZON_SIZE))

        # Low-medium coherence → minimum baseline
        else:
            # Below 0.50: Focus on recent (100 entities)
            return self.MIN_HORIZON_SIZE

    def compute_query_limits(self, horizon_size: int) -> tuple[int, int]:
        """
        Compute query limits for recent and fuzzy match queries.

        Strategy:
        - recent_limit: 50% of horizon (temporal recency bias)
        - fuzzy_limit: 30% of horizon (keyword-based recall)
        - Remaining 20%: Session entities (from conversation buffer)

        Args:
            horizon_size: Total horizon size (100-500)

        Returns:
            Tuple of (recent_limit, fuzzy_limit)
        """
        recent_limit = min(horizon_size // 2, 250)  # Max 250 for recent
        fuzzy_limit = min(horizon_size // 3, 150)   # Max 150 for fuzzy

        return recent_limit, fuzzy_limit

    def compute_adaptive_horizon(
        self,
        field_coherence: float,
        total_entities_available: int = 0
    ) -> HorizonMetrics:
        """
        Compute complete adaptive horizon metrics.

        This is the primary method called by dae_interactive.py to replace
        fixed limit=20 with adaptive computation.

        Args:
            field_coherence: Current field coherence (0.0-1.0)
            total_entities_available: Total entities in Neo4j (optional)

        Returns:
            HorizonMetrics with computed limits and metadata
        """
        # Compute morpheable horizon size
        horizon_size = self.compute_horizon_size(field_coherence)

        # Compute query limits
        recent_limit, fuzzy_limit = self.compute_query_limits(horizon_size)

        # Build metrics
        metrics = HorizonMetrics(
            field_coherence=field_coherence,
            horizon_size=horizon_size,
            recent_limit=recent_limit,
            fuzzy_limit=fuzzy_limit,
            total_entities_available=total_entities_available
        )

        # Store for tracking
        self.last_metrics = metrics

        return metrics

    def update_retrieval_stats(
        self,
        entities_retrieved: int
    ):
        """
        Update retrieval statistics after entity queries complete.

        This enables tracking horizon utilization over time and can inform
        future optimizations (e.g., if utilization consistently <50%, reduce limits).

        Args:
            entities_retrieved: Number of entities actually returned
        """
        if self.last_metrics:
            self.last_metrics.entities_retrieved = entities_retrieved

            # Compute utilization
            if self.last_metrics.horizon_size > 0:
                self.last_metrics.horizon_utilization = (
                    entities_retrieved / self.last_metrics.horizon_size
                )

    def get_coherence_tier(self, field_coherence: float) -> str:
        """
        Get coherence tier name for logging/debugging.

        Args:
            field_coherence: Field coherence (0.0-1.0)

        Returns:
            Tier name: "high", "medium", "low", or "minimal"
        """
        if field_coherence >= self.COHERENCE_HIGH:
            return "high"
        elif field_coherence >= self.COHERENCE_MEDIUM:
            return "medium"
        elif field_coherence >= self.COHERENCE_LOW:
            return "low"
        else:
            return "minimal"

    def should_gate_retrieval(self, field_coherence: float) -> bool:
        """
        Determine if entity retrieval should be gated (skipped).

        Following NEXUS organ pattern: Only query Neo4j if coherence > τ_recall.
        If coherence too low, skip expensive queries (rely on session buffer only).

        Args:
            field_coherence: Current field coherence (0.0-1.0)

        Returns:
            True if retrieval should proceed, False if gated
        """
        # NEXUS τ_recall = 0.3 (from FFITTSS)
        return field_coherence >= self.COHERENCE_LOW


# Module-level singleton for convenience
_default_horizon = None

def get_default_horizon() -> EntityHorizon:
    """Get or create default EntityHorizon singleton."""
    global _default_horizon
    if _default_horizon is None:
        _default_horizon = EntityHorizon()
    return _default_horizon
